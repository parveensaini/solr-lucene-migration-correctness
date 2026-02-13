import json, os, sys
import requests

SOLR5 = os.environ.get("SOLR5", "http://localhost:8985/solr/core1")
SOLR8 = os.environ.get("SOLR8", "http://localhost:8988/solr/core1")
QFILE = sys.argv[1] if len(sys.argv) > 1 else "corpus/queries.json"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else "reports"
TOPN = int(os.environ.get("TOPN", "10"))
EXPLAIN_TOP = int(os.environ.get("EXPLAIN_TOP", "2"))
TIMEOUT = int(os.environ.get("TIMEOUT", "20"))

# thresholds (tune per org)
MAX_AVG_ABS_RANK_DELTA = float(os.environ.get("MAX_AVG_ABS_RANK_DELTA", "1.0"))
MAX_MAX_ABS_RANK_DELTA = int(os.environ.get("MAX_MAX_ABS_RANK_DELTA", "4"))
MAX_MAX_ABS_NORM_DRIFT = float(os.environ.get("MAX_MAX_ABS_NORM_DRIFT", "0.15"))
NEAR_TIE_NORM_EPS = float(os.environ.get("NEAR_TIE_NORM_EPS", "0.05"))

def select(base, params):
  r = requests.get(f"{base}/select", params=params, timeout=TIMEOUT)
  r.raise_for_status()
  data = r.json()
  docs = data.get("response", {}).get("docs", [])
  ids = [str(d.get("id")) for d in docs]
  scores = {str(d.get("id")): float(d.get("score")) for d in docs if "id" in d and "score" in d}
  return data, ids, scores

def select_debug(base, params):
  p = dict(params)
  p["debugQuery"] = "on"
  r = requests.get(f"{base}/select", params=p, timeout=TIMEOUT)
  r.raise_for_status()
  return r.json()

def jaccard(a, b):
  sa, sb = set(a), set(b)
  return 1.0 if not sa and not sb else len(sa & sb) / max(1, len(sa | sb))

def rank_positions(ids):
  return {doc_id: i for i, doc_id in enumerate(ids)}

def rank_churn(top5, top8):
  pos5 = rank_positions(top5)
  pos8 = rank_positions(top8)
  common = [doc_id for doc_id in top5 if doc_id in pos8]
  deltas = [abs(pos8[d] - pos5[d]) for d in common]
  avg_abs_delta = (sum(deltas) / len(deltas)) if deltas else 0.0
  max_abs_delta = max(deltas) if deltas else 0
  movers = sorted(
    [{"id": d, "rank5": pos5[d] + 1, "rank8": pos8[d] + 1, "delta": (pos8[d] - pos5[d])} for d in common],
    key=lambda x: abs(x["delta"]),
    reverse=True
  )
  num_changed = sum(1 for d in common if pos5[d] != pos8[d])
  return {
    "common": len(common),
    "avg_abs_rank_delta": avg_abs_delta,
    "max_abs_rank_delta": max_abs_delta,
    "num_rank_changes": num_changed,
    "top_movers": movers[: min(5, len(movers))]
  }

def extract_explains(debug_json, doc_ids):
  dbg = (debug_json or {}).get("debug", {})
  exp = dbg.get("explain", {}) if isinstance(dbg.get("explain", {}), dict) else {}
  out = {}
  for doc_id in doc_ids:
    if doc_id in exp:
      out[doc_id] = exp[doc_id]
  return out

def classify(churn, max_abs_norm):
  # FAIL: strong evidence of semantic drift
  if churn["max_abs_rank_delta"] >= MAX_MAX_ABS_RANK_DELTA:
    # If normalized drift is tiny, this is probably near-tie jitter, not semantic drift.
    if max_abs_norm < NEAR_TIE_NORM_EPS:
      return ("WARN", f"max_abs_rank_delta {churn['max_abs_rank_delta']} >= {MAX_MAX_ABS_RANK_DELTA} but max_abs_norm_drift {max_abs_norm:.3f} < {NEAR_TIE_NORM_EPS} (near-tie churn)")
    return ("FAIL", f"max_abs_rank_delta {churn['max_abs_rank_delta']} >= {MAX_MAX_ABS_RANK_DELTA} (not near-tie; max_abs_norm_drift {max_abs_norm:.3f})")
  if max_abs_norm >= MAX_MAX_ABS_NORM_DRIFT:
    return ("FAIL", f"max_abs_norm_drift {max_abs_norm:.3f} >= {MAX_MAX_ABS_NORM_DRIFT}")

  # WARN: meaningful churn, but not clearly semantic drift
  if churn["avg_abs_rank_delta"] >= MAX_AVG_ABS_RANK_DELTA:
    return ("WARN", f"avg_abs_rank_delta {churn['avg_abs_rank_delta']:.2f} >= {MAX_AVG_ABS_RANK_DELTA}")

  return ("PASS", "")

def status_badge(status):
  return {"PASS":"PASS ✅", "WARN":"WARN ⚠️", "FAIL":"FAIL ❌"}.get(status, status)

def main():
  os.makedirs(OUTDIR, exist_ok=True)
  queries = json.load(open(QFILE))
  report = {"solr5": SOLR5, "solr8": SOLR8, "queries": []}

  for q in queries:
    name = q["name"]
    params = dict(q.get("params", {}))

    fq = params.get("fq")
    if fq is None:
      pass
    elif isinstance(fq, str):
      params["fq"] = [fq]

    params.setdefault("wt", "json")
    params.setdefault("rows", TOPN)
    params.setdefault("df", "body")
    params.setdefault("q.op", "OR")
    params.setdefault("sort", "score desc,id asc")
    params.setdefault("fl", "id,score")

    raw5, ids5, s5 = select(SOLR5, params)
    raw8, ids8, s8 = select(SOLR8, params)

    top5, top8 = ids5[:TOPN], ids8[:TOPN]
    only5 = [x for x in top5 if x not in set(top8)]
    only8 = [x for x in top8 if x not in set(top5)]
    common = [x for x in top5 if x in set(top8)]

    topScore5 = s5.get(top5[0], 0.0) if top5 else 0.0
    topScore8 = s8.get(top8[0], 0.0) if top8 else 0.0
    denom5 = topScore5 if abs(topScore5) > 1e-12 else 1.0
    denom8 = topScore8 if abs(topScore8) > 1e-12 else 1.0

    drift_raw = []
    drift_norm = []
    for doc_id in common:
      if doc_id in s5 and doc_id in s8:
        score5 = s5[doc_id]
        score8 = s8[doc_id]
        denom_rel = max(abs(score5), 1e-9)
        drift_raw.append({
          "id": doc_id,
          "score5": score5,
          "score8": score8,
          "abs": score8 - score5,
          "rel": (score8 - score5) / denom_rel
        })
        n5 = score5 / denom5
        n8 = score8 / denom8
        denom_nrel = max(abs(n5), 1e-9)
        drift_norm.append({
          "id": doc_id,
          "norm5": n5,
          "norm8": n8,
          "abs": n8 - n5,
          "rel": (n8 - n5) / denom_nrel
        })

    drift_abs = sorted(drift_raw, key=lambda x: abs(x["abs"]), reverse=True)
    drift_norm_abs = sorted(drift_norm, key=lambda x: abs(x["abs"]), reverse=True)

    churn = rank_churn(top5, top8)
    max_abs_norm = abs(drift_norm_abs[0]["abs"]) if drift_norm_abs else 0.0

    status, reason = classify(churn, max_abs_norm)

    explain_ids = [d["id"] for d in drift_abs[:EXPLAIN_TOP]] if EXPLAIN_TOP > 0 else []
    explains = {"solr5": {}, "solr8": {}}
    if explain_ids:
      dbg5 = select_debug(SOLR5, params)
      dbg8 = select_debug(SOLR8, params)
      explains["solr5"] = extract_explains(dbg5, explain_ids)
      explains["solr8"] = extract_explains(dbg8, explain_ids)
      json.dump(dbg5, open(os.path.join(OUTDIR, f"{name}.solr5.debug.json"), "w"), indent=2)
      json.dump(dbg8, open(os.path.join(OUTDIR, f"{name}.solr8.debug.json"), "w"), indent=2)

    entry = {
      "name": name,
      "params": params,
      "topn": TOPN,
      "status": status,
      "reason": reason,
      "passed": (status == "PASS"),
      "jaccard_topn": jaccard(top5, top8),
      "only_in_5_topn": only5,
      "only_in_8_topn": only8,
      "rank_churn": churn,
      "top_score": {"solr5": topScore5, "solr8": topScore8},
      "max_abs_norm_drift": max_abs_norm,
      "score_drift_top_abs": drift_abs[:5],
      "norm_score_drift_top_abs": drift_norm_abs[:5],
      "explain_ids": explain_ids,
      "explains": explains
    }
    report["queries"].append(entry)

    json.dump(raw5, open(os.path.join(OUTDIR, f"{name}.solr5.json"), "w"), indent=2)
    json.dump(raw8, open(os.path.join(OUTDIR, f"{name}.solr8.json"), "w"), indent=2)

  json.dump(report, open(os.path.join(OUTDIR, "summary.json"), "w"), indent=2)

  lines = [
    "# Solr 5 vs 8 Drift Report\n",
    f"- Solr5: `{SOLR5}`\n- Solr8: `{SOLR8}`\n\n",
    "Thresholds:\n",
    f"- MAX_AVG_ABS_RANK_DELTA={MAX_AVG_ABS_RANK_DELTA}\n",
    f"- MAX_MAX_ABS_RANK_DELTA={MAX_MAX_ABS_RANK_DELTA}\n",
    f"- MAX_MAX_ABS_NORM_DRIFT={MAX_MAX_ABS_NORM_DRIFT}\n\n"
  ]

  for e in report["queries"]:
    lines.append(f"## {e['name']} — {status_badge(e['status'])}\n")
    if e["reason"]:
      lines.append(f"- Reason: {e['reason']}\n")

    lines.append(f"- Jaccard(top{e['topn']}): **{e['jaccard_topn']:.3f}**\n")
    lines.append(f"- Avg abs rank delta: **{e['rank_churn']['avg_abs_rank_delta']:.2f}** (max: {e['rank_churn']['max_abs_rank_delta']}, changes: {e['rank_churn']['num_rank_changes']})\n")
    lines.append(f"- Top score (Solr5/Solr8): **{e['top_score']['solr5']:.6f} / {e['top_score']['solr8']:.6f}**\n")
    lines.append(f"- Max abs normalized drift (top1-normalized): **{e['max_abs_norm_drift']:.3f}**\n")
    lines.append(f"- Only in Solr5 top{e['topn']}: {e['only_in_5_topn']}\n")
    lines.append(f"- Only in Solr8 top{e['topn']}: {e['only_in_8_topn']}\n")

    if e["rank_churn"]["top_movers"]:
      lines.append("\nTop movers:\n\n| id | rank5 | rank8 | delta |\n|---|---:|---:|---:|\n")
      for m in e["rank_churn"]["top_movers"]:
        lines.append(f"| {m['id']} | {m['rank5']} | {m['rank8']} | {m['delta']} |\n")

    if e["score_drift_top_abs"]:
      lines.append("\nTop score drifts (raw, abs):\n\n| id | score5 | score8 | abs | rel |\n|---|---:|---:|---:|---:|\n")
      for d in e["score_drift_top_abs"]:
        lines.append(f"| {d['id']} | {d['score5']:.6f} | {d['score8']:.6f} | {d['abs']:.6f} | {d['rel']:.3f} |\n")

    if e["norm_score_drift_top_abs"]:
      lines.append("\nTop score drifts (normalized by top1, abs):\n\n| id | norm5 | norm8 | abs | rel |\n|---|---:|---:|---:|---:|\n")
      for d in e["norm_score_drift_top_abs"]:
        lines.append(f"| {d['id']} | {d['norm5']:.6f} | {d['norm8']:.6f} | {d['abs']:.6f} | {d['rel']:.3f} |\n")

    if e["explain_ids"]:
      lines.append("\nExplain snippets (top raw-drift docs):\n")
      for doc_id in e["explain_ids"]:
        s5 = e["explains"]["solr5"].get(doc_id, "")
        s8 = e["explains"]["solr8"].get(doc_id, "")
        lines.append(f"\n**doc id {doc_id}**\n")
        lines.append(f"\n- Solr5 explain (prefix): `{(s5[:400]).replace('`','\\`')}`\n")
        lines.append(f"- Solr8 explain (prefix): `{(s8[:400]).replace('`','\\`')}`\n")

    lines.append("\n")

  open(os.path.join(OUTDIR, "report.md"), "w").write("".join(lines))
  print(f"Wrote {OUTDIR}/report.md and {OUTDIR}/summary.json")

if __name__ == "__main__":
  main()
