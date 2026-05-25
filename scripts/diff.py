"""
Solr migration correctness harness.

Compares search results between any two Solr instances and produces
per-query diff reports (JSON + Markdown).

Usage:
  # All pairs (5v8, 8v9, 5v9)
  python scripts/diff.py corpus/queries.json reports

  # Single pair via env vars
  PAIR=5v8 python scripts/diff.py corpus/queries.json reports
  PAIR=8v9 python scripts/diff.py corpus/queries.json reports
  PAIR=5v9 python scripts/diff.py corpus/queries.json reports

  # Arbitrary endpoints
  SOLR_A=http://host1/solr/core1 SOLR_B=http://host2/solr/core1 \
    PAIR_LABEL=custom python scripts/diff.py corpus/queries.json reports
"""

import json
import os
import sys

import requests

# ---------------------------------------------------------------------------
# Solr endpoints
# ---------------------------------------------------------------------------
SOLR5 = os.environ.get("SOLR5", "http://localhost:8985/solr/core1")
SOLR8 = os.environ.get("SOLR8", "http://localhost:8988/solr/core1")
SOLR9 = os.environ.get("SOLR9", "http://localhost:8989/solr/core1")

# ---------------------------------------------------------------------------
# CLI / env
# ---------------------------------------------------------------------------
QFILE  = sys.argv[1] if len(sys.argv) > 1 else "corpus/queries.json"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else "reports"

TOPN        = int(os.environ.get("TOPN",        "10"))
EXPLAIN_TOP = int(os.environ.get("EXPLAIN_TOP", "2"))
TIMEOUT     = int(os.environ.get("TIMEOUT",     "20"))
RBO_P       = float(os.environ.get("RBO_P",     "0.9"))

# Thresholds (tune per org)
MAX_AVG_ABS_RANK_DELTA = float(os.environ.get("MAX_AVG_ABS_RANK_DELTA", "1.0"))
MAX_MAX_ABS_RANK_DELTA = int(os.environ.get("MAX_MAX_ABS_RANK_DELTA",   "4"))
MAX_MAX_ABS_NORM_DRIFT = float(os.environ.get("MAX_MAX_ABS_NORM_DRIFT", "0.15"))
NEAR_TIE_NORM_EPS      = float(os.environ.get("NEAR_TIE_NORM_EPS",     "0.05"))

# Which pair(s) to run.  "all" runs every combination.
PAIR = os.environ.get("PAIR", "all").lower()

# ---------------------------------------------------------------------------
# All known pairs: label -> (endpoint_a, label_a, endpoint_b, label_b)
# ---------------------------------------------------------------------------
ALL_PAIRS = {
    "5v8": (SOLR5, "solr5", SOLR8, "solr8"),
    "8v9": (SOLR8, "solr8", SOLR9, "solr9"),
    "5v9": (SOLR5, "solr5", SOLR9, "solr9"),
}

# Support arbitrary endpoints via env
if os.environ.get("SOLR_A") and os.environ.get("SOLR_B"):
    label = os.environ.get("PAIR_LABEL", "custom")
    ALL_PAIRS[label] = (
        os.environ["SOLR_A"], os.environ.get("LABEL_A", "solr_a"),
        os.environ["SOLR_B"], os.environ.get("LABEL_B", "solr_b"),
    )

if PAIR == "all":
    PAIRS_TO_RUN = list(ALL_PAIRS.items())
elif PAIR in ALL_PAIRS:
    PAIRS_TO_RUN = [(PAIR, ALL_PAIRS[PAIR])]
else:
    print(f"Unknown PAIR={PAIR!r}. Choose from: {list(ALL_PAIRS)} or 'all'", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------
def select(base, params):
    r = requests.get(f"{base}/select", params=params, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    docs   = data.get("response", {}).get("docs", [])
    ids    = [str(d.get("id")) for d in docs]
    scores = {str(d["id"]): float(d["score"]) for d in docs if "id" in d and "score" in d}
    return data, ids, scores


def select_debug(base, params):
    p = dict(params)
    p["debugQuery"] = "on"
    r = requests.get(f"{base}/select", params=p, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def extract_explains(debug_json, doc_ids):
    dbg = (debug_json or {}).get("debug", {})
    exp = dbg.get("explain", {}) if isinstance(dbg.get("explain", {}), dict) else {}
    return {doc_id: exp[doc_id] for doc_id in doc_ids if doc_id in exp}


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def jaccard(a, b):
    sa, sb = set(a), set(b)
    return 1.0 if not sa and not sb else len(sa & sb) / max(1, len(sa | sb))


def rbo(list_a, list_b, p=0.9):
    """
    Rank-Biased Overlap (RBO) for two finite ranked lists.

    Uses the RBO_EXT (extrapolated) variant from Webber et al. (2010)
    which adds a residual term to account for the unobserved tail,
    ensuring identical lists return 1.0 regardless of length.

    Unlike Jaccard, which measures unweighted set overlap, RBO weights
    agreement at the top of the ranking more heavily than the bottom.
    This makes it more sensitive to changes near rank 1, which matter
    most in search and retrieval.

    p (persistence) controls the top-weight emphasis:
      - lower p (e.g. 0.5): only top ranks matter
      - higher p (e.g. 0.99): deeper ranks contribute more
      - default p=0.9: rank 1 carries ~10x the weight of rank 10

    Reference: Webber et al., "A Similarity Measure for Indefinite Rankings"
    ACM TOIS 2010. https://doi.org/10.1145/1852102.1852106
    """
    if not list_a and not list_b:
        return 1.0

    depth  = max(len(list_a), len(list_b))
    seen_a = set()
    seen_b = set()
    score  = 0.0

    for d in range(1, depth + 1):
        if d <= len(list_a):
            seen_a.add(list_a[d - 1])
        if d <= len(list_b):
            seen_b.add(list_b[d - 1])
        overlap   = len(seen_a & seen_b)
        agreement = overlap / d
        score    += agreement * (p ** (d - 1))

    # Residual term: accounts for the unobserved tail beyond depth d.
    # Without this, identical finite lists return < 1.0.
    overlap_at_d = len(seen_a & seen_b)
    residual = (overlap_at_d / depth) * (p ** depth)

    return (1 - p) * score + residual


def rank_positions(ids):
    return {doc_id: i for i, doc_id in enumerate(ids)}


def rank_churn(ids_a, ids_b):
    pos_a = rank_positions(ids_a)
    pos_b = rank_positions(ids_b)
    common  = [d for d in ids_a if d in pos_b]
    deltas  = [abs(pos_b[d] - pos_a[d]) for d in common]
    avg_abs = (sum(deltas) / len(deltas)) if deltas else 0.0
    max_abs = max(deltas) if deltas else 0
    movers  = sorted(
        [{"id": d,
          "rank_a": pos_a[d] + 1,
          "rank_b": pos_b[d] + 1,
          "delta":  pos_b[d] - pos_a[d]}
         for d in common],
        key=lambda x: abs(x["delta"]),
        reverse=True,
    )
    return {
        "common":             len(common),
        "avg_abs_rank_delta": avg_abs,
        "max_abs_rank_delta": max_abs,
        "num_rank_changes":   sum(1 for d in common if pos_a[d] != pos_b[d]),
        "top_movers":         movers[:5],
    }


def classify(churn, max_abs_norm):
    if churn["max_abs_rank_delta"] >= MAX_MAX_ABS_RANK_DELTA:
        if max_abs_norm < NEAR_TIE_NORM_EPS:
            return ("WARN",
                    f"max_abs_rank_delta {churn['max_abs_rank_delta']} >= {MAX_MAX_ABS_RANK_DELTA} "
                    f"but max_abs_norm_drift {max_abs_norm:.3f} < {NEAR_TIE_NORM_EPS} (near-tie churn)")
        return ("FAIL",
                f"max_abs_rank_delta {churn['max_abs_rank_delta']} >= {MAX_MAX_ABS_RANK_DELTA} "
                f"(not near-tie; max_abs_norm_drift {max_abs_norm:.3f})")
    if max_abs_norm >= MAX_MAX_ABS_NORM_DRIFT:
        return ("FAIL", f"max_abs_norm_drift {max_abs_norm:.3f} >= {MAX_MAX_ABS_NORM_DRIFT}")
    if churn["avg_abs_rank_delta"] >= MAX_AVG_ABS_RANK_DELTA:
        return ("WARN", f"avg_abs_rank_delta {churn['avg_abs_rank_delta']:.2f} >= {MAX_AVG_ABS_RANK_DELTA}")
    return ("PASS", "")


def status_badge(status):
    return {"PASS": "PASS ✅", "WARN": "WARN ⚠️", "FAIL": "FAIL ❌"}.get(status, status)


# ---------------------------------------------------------------------------
# Per-pair diff
# ---------------------------------------------------------------------------
def run_pair(pair_label, url_a, lbl_a, url_b, lbl_b, queries, pair_outdir):
    os.makedirs(pair_outdir, exist_ok=True)
    report = {lbl_a: url_a, lbl_b: url_b, "pair": pair_label, "queries": []}

    for q in queries:
        name   = q["name"]
        params = dict(q.get("params", {}))

        fq = params.get("fq")
        if isinstance(fq, str):
            params["fq"] = [fq]

        params.setdefault("wt",   "json")
        params.setdefault("rows", TOPN)
        params.setdefault("df",   "body")
        params.setdefault("q.op", "OR")
        params.setdefault("sort", "score desc,id asc")
        params.setdefault("fl",   "id,score")

        raw_a, ids_a, s_a = select(url_a, params)
        raw_b, ids_b, s_b = select(url_b, params)

        top_a = ids_a[:TOPN]
        top_b = ids_b[:TOPN]
        only_a = [x for x in top_a if x not in set(top_b)]
        only_b = [x for x in top_b if x not in set(top_a)]
        common = [x for x in top_a if x in set(top_b)]

        top_score_a = s_a.get(top_a[0], 0.0) if top_a else 0.0
        top_score_b = s_b.get(top_b[0], 0.0) if top_b else 0.0
        denom_a = top_score_a if abs(top_score_a) > 1e-12 else 1.0
        denom_b = top_score_b if abs(top_score_b) > 1e-12 else 1.0

        drift_raw  = []
        drift_norm = []
        for doc_id in common:
            if doc_id in s_a and doc_id in s_b:
                sa = s_a[doc_id]
                sb = s_b[doc_id]
                denom_rel = max(abs(sa), 1e-9)
                drift_raw.append({
                    "id": doc_id,
                    f"score_{lbl_a}": sa,
                    f"score_{lbl_b}": sb,
                    "abs": sb - sa,
                    "rel": (sb - sa) / denom_rel,
                })
                na = sa / denom_a
                nb = sb / denom_b
                denom_nrel = max(abs(na), 1e-9)
                drift_norm.append({
                    "id": doc_id,
                    f"norm_{lbl_a}": na,
                    f"norm_{lbl_b}": nb,
                    "abs": nb - na,
                    "rel": (nb - na) / denom_nrel,
                })

        drift_abs      = sorted(drift_raw,  key=lambda x: abs(x["abs"]), reverse=True)
        drift_norm_abs = sorted(drift_norm, key=lambda x: abs(x["abs"]), reverse=True)

        churn        = rank_churn(top_a, top_b)
        max_abs_norm = abs(drift_norm_abs[0]["abs"]) if drift_norm_abs else 0.0
        status, reason = classify(churn, max_abs_norm)

        rbo_score = rbo(top_a, top_b, p=RBO_P)

        explain_ids = [d["id"] for d in drift_abs[:EXPLAIN_TOP]] if EXPLAIN_TOP > 0 else []
        explains    = {lbl_a: {}, lbl_b: {}}
        if explain_ids:
            dbg_a = select_debug(url_a, params)
            dbg_b = select_debug(url_b, params)
            explains[lbl_a] = extract_explains(dbg_a, explain_ids)
            explains[lbl_b] = extract_explains(dbg_b, explain_ids)
            json.dump(dbg_a, open(os.path.join(pair_outdir, f"{name}.{lbl_a}.debug.json"), "w"), indent=2)
            json.dump(dbg_b, open(os.path.join(pair_outdir, f"{name}.{lbl_b}.debug.json"), "w"), indent=2)

        entry = {
            "name":                     name,
            "params":                   params,
            "topn":                     TOPN,
            "status":                   status,
            "reason":                   reason,
            "passed":                   status == "PASS",
            "jaccard_topn":             jaccard(top_a, top_b),
            "rbo":                      round(rbo_score, 4),
            "rbo_p":                    RBO_P,
            f"only_in_{lbl_a}_topn":    only_a,
            f"only_in_{lbl_b}_topn":    only_b,
            "rank_churn":               churn,
            "top_score":                {lbl_a: top_score_a, lbl_b: top_score_b},
            "max_abs_norm_drift":       max_abs_norm,
            "score_drift_top_abs":      drift_abs[:5],
            "norm_score_drift_top_abs": drift_norm_abs[:5],
            "explain_ids":              explain_ids,
            "explains":                 explains,
        }
        report["queries"].append(entry)

        json.dump(raw_a, open(os.path.join(pair_outdir, f"{name}.{lbl_a}.json"), "w"), indent=2)
        json.dump(raw_b, open(os.path.join(pair_outdir, f"{name}.{lbl_b}.json"), "w"), indent=2)

    json.dump(report, open(os.path.join(pair_outdir, "summary.json"), "w"), indent=2)
    _write_markdown(report, pair_outdir, lbl_a, lbl_b, pair_label)
    print(f"[{pair_label}] Wrote {pair_outdir}/report.md and summary.json")
    return report


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------
def _write_markdown(report, outdir, lbl_a, lbl_b, pair_label):
    A = lbl_a.upper()
    B = lbl_b.upper()
    lines = [
        f"# {A} vs {B} Drift Report\n\n",
        f"- {A}: `{report[lbl_a]}`\n",
        f"- {B}: `{report[lbl_b]}`\n\n",
        "Thresholds:\n",
        f"- MAX_AVG_ABS_RANK_DELTA={MAX_AVG_ABS_RANK_DELTA}\n",
        f"- MAX_MAX_ABS_RANK_DELTA={MAX_MAX_ABS_RANK_DELTA}\n",
        f"- MAX_MAX_ABS_NORM_DRIFT={MAX_MAX_ABS_NORM_DRIFT}\n\n",
        "> **RBO** (Rank-Biased Overlap, p={:.2f}) measures top-weighted ranked-list agreement. ".format(RBO_P),
        "Unlike Jaccard, which only measures set overlap, RBO penalizes changes near the top of the "
        "result list more heavily than changes near the bottom. A value of 1.0 means identical ranking.\n\n",
    ]

    for e in report["queries"]:
        lines.append(f"## {e['name']} — {status_badge(e['status'])}\n")
        if e["reason"]:
            lines.append(f"- Reason: {e['reason']}\n")

        lines.append(f"- Jaccard(top{e['topn']}): **{e['jaccard_topn']:.3f}**\n")
        lines.append(f"- RBO(p={e['rbo_p']}): **{e['rbo']:.4f}**\n")
        lines.append(
            f"- Avg abs rank delta: **{e['rank_churn']['avg_abs_rank_delta']:.2f}**"
            f" (max: {e['rank_churn']['max_abs_rank_delta']},"
            f" changes: {e['rank_churn']['num_rank_changes']})\n"
        )
        lines.append(
            f"- Top score ({A}/{B}): "
            f"**{e['top_score'][lbl_a]:.6f} / {e['top_score'][lbl_b]:.6f}**\n"
        )
        lines.append(f"- Max abs normalized drift: **{e['max_abs_norm_drift']:.3f}**\n")
        lines.append(f"- Only in {A} top{e['topn']}: {e[f'only_in_{lbl_a}_topn']}\n")
        lines.append(f"- Only in {B} top{e['topn']}: {e[f'only_in_{lbl_b}_topn']}\n")

        if e["rank_churn"]["top_movers"]:
            lines.append(f"\nTop movers:\n\n| id | rank_{lbl_a} | rank_{lbl_b} | delta |\n|---|---:|---:|---:|\n")
            for m in e["rank_churn"]["top_movers"]:
                lines.append(f"| {m['id']} | {m['rank_a']} | {m['rank_b']} | {m['delta']} |\n")

        if e["score_drift_top_abs"]:
            lines.append(
                f"\nTop score drifts (raw, abs):\n\n"
                f"| id | score_{lbl_a} | score_{lbl_b} | abs | rel |\n"
                f"|---|---:|---:|---:|---:|\n"
            )
            for d in e["score_drift_top_abs"]:
                lines.append(
                    f"| {d['id']} | {d[f'score_{lbl_a}']:.6f}"
                    f" | {d[f'score_{lbl_b}']:.6f}"
                    f" | {d['abs']:.6f} | {d['rel']:.3f} |\n"
                )

        if e["norm_score_drift_top_abs"]:
            lines.append(
                f"\nTop score drifts (normalized by top1, abs):\n\n"
                f"| id | norm_{lbl_a} | norm_{lbl_b} | abs | rel |\n"
                f"|---|---:|---:|---:|---:|\n"
            )
            for d in e["norm_score_drift_top_abs"]:
                lines.append(
                    f"| {d['id']} | {d[f'norm_{lbl_a}']:.6f}"
                    f" | {d[f'norm_{lbl_b}']:.6f}"
                    f" | {d['abs']:.6f} | {d['rel']:.3f} |\n"
                )

        if e["explain_ids"]:
            lines.append("\nExplain snippets (top raw-drift docs):\n")
            for doc_id in e["explain_ids"]:
                ea = e["explains"][lbl_a].get(doc_id, "")
                eb = e["explains"][lbl_b].get(doc_id, "")
                lines.append(f"\n**doc id {doc_id}**\n")
                lines.append(f"\n- {A} explain: `{ea[:400].replace('`', chr(96))}`\n")
                lines.append(f"- {B} explain: `{eb[:400].replace('`', chr(96))}`\n")

        lines.append("\n")

    open(os.path.join(outdir, "report.md"), "w").write("".join(lines))


# ---------------------------------------------------------------------------
# Cross-pair summary
# ---------------------------------------------------------------------------
def write_combined_summary(all_reports, outdir):
    lines = [
        "# Combined Migration Summary\n\n",
        "> **RBO** (Rank-Biased Overlap) measures top-weighted ranked-list similarity. "
        "Unlike Jaccard, RBO penalizes rank changes near the top more heavily than changes near the bottom. "
        "A value of 1.0 means identical ranking.\n\n",
        "| Pair | Query | Status | Jaccard | RBO(p=0.9) | Avg Rank Δ | Max Norm Drift |\n",
        "|---|---|---|---:|---:|---:|---:|\n",
    ]

    for pair_label, report in all_reports:
        for e in report["queries"]:
            lines.append(
                f"| {pair_label} | {e['name']} | {status_badge(e['status'])}"
                f" | {e['jaccard_topn']:.3f}"
                f" | {e['rbo']:.4f}"
                f" | {e['rank_churn']['avg_abs_rank_delta']:.2f}"
                f" | {e['max_abs_norm_drift']:.3f} |\n"
            )

    open(os.path.join(outdir, "combined_summary.md"), "w").write("".join(lines))
    print(f"Wrote {outdir}/combined_summary.md")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTDIR, exist_ok=True)
    queries    = json.load(open(QFILE))
    all_reports = []

    for pair_label, (url_a, lbl_a, url_b, lbl_b) in PAIRS_TO_RUN:
        pair_outdir = os.path.join(OUTDIR, pair_label)
        print(f"\n=== Running pair: {pair_label} ({lbl_a} vs {lbl_b}) ===")
        report = run_pair(pair_label, url_a, lbl_a, url_b, lbl_b, queries, pair_outdir)
        all_reports.append((pair_label, report))

    if len(all_reports) > 1:
        write_combined_summary(all_reports, OUTDIR)


if __name__ == "__main__":
    main()