# Solr 5 vs Solr 8 Side-by-Side Drift Harness

This harness runs Solr **5.5.4** and Solr **8.9.0** side-by-side, loads the same documents into both versions, executes the same query corpus, and generates a drift report.

The goal is to make **score drift and rank churn observable and reproducible** during major-version upgrades.

---

# What Is “Drift”?

Even when both versions return the same documents, a major Solr/Lucene upgrade can change:

- Score values (score drift)
- Ordering (rank churn), especially among near-ties
- Relative score distribution (shape drift)

This matters when:

- Top-K results feed downstream ML rerankers
- Score thresholds are used for filtering
- Minor ordering changes affect candidate selection
- Business logic depends on ranking stability

This harness detects and quantifies those changes.

---

# What the Diff Script Does

For each query in `corpus/queries.json`, the script:

1. Sends the same request to Solr 5 and Solr 8
2. Collects the top-N results (id + score)
3. Computes:

   - Jaccard(topN) — document overlap
   - Average rank movement
   - Maximum rank movement
   - Raw score drift (absolute difference)
   - Top1-normalized score drift (relative shape comparison)

4. Optionally fetches `debugQuery=on` explain output for top drift documents
5. Writes:

   - `reports/report.md` (human-readable report)
   - `reports/summary.json` (machine-readable summary)

---

# Quickstart (Recommended)

Repository includes `scripts/demo.sh`, run:

```bash
bash scripts/demo.sh
```

This will:

- Start both Solr containers
- Wait for both cores to become ready
- Load the sample corpus into both
- Run the diff harness
- Generate `reports/report.md`

---

# Manual Setup

Run from the repository root.

## 1. Create Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Start Solr 5 and Solr 8

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Verify:

```bash
curl "http://localhost:8985/solr/admin/cores?action=STATUS&wt=json"
curl "http://localhost:8988/solr/admin/cores?action=STATUS&wt=json"
```

Both should show `core1`.

---

## 3. Load the Same Documents into Both

```bash
bash scripts/load.sh corpus/docs.json
```

---

## 4. Run the Drift Harness

```bash
TOPN=10 EXPLAIN_TOP=2 python3 scripts/diff.py corpus/queries.json reports
```

Parameters:

- `TOPN` — number of top results to compare
- `EXPLAIN_TOP` — number of highest-drift docs to fetch explain output for

---

## 5. View the Report

```bash
cat reports/report.md
```

---

# Deterministic Sorting

Queries should use:

```
sort=score desc, id asc
```

This prevents unstable ordering among equal scores.

---

# Output Files

After execution:

- `reports/report.md` — full per-query drift report
- `reports/summary.json` — structured summary (useful for CI gating)

---

# What This Project Demonstrates

This project does NOT claim that Lucene scoring changes are undocumented.

Lucene documentation clearly states that scoring and similarity behavior may evolve across major versions.

This repository demonstrates:

- How to perform deterministic side-by-side behavioral comparison
- How to quantify rank churn and score drift
- How to classify upgrade impact with configurable thresholds
- How to extract explain-level evidence for root cause analysis

The goal is not to prove drift exists —  
the goal is to provide a reproducible framework to detect and gate drift before production migration.

---

# Intended Use

This harness is useful for:

- Major Solr/Lucene upgrades
- Migration RFC validation
- ML candidate retrieval verification
- Pre-production rollout gating
- Upgrade risk mitigation analysis

---
