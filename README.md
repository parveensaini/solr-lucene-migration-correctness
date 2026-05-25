# Solr / Lucene Ranking Drift Validation Harness
A simple harness to detect ranking drift during Solr / Lucene upgrades by comparing candidate overlap, rank movement, score drift, and explain output across versions.

## Run the demo

```bash
docker-compose -f docker/docker-compose.yml up -d
bash scripts/wait_for_solr.sh
bash scripts/load.sh
make diff
# Outputs:
#   reports/5v8/report.md   — Solr 5 vs Solr 8
#   reports/8v9/report.md   — Solr 8 vs Solr 9
#   reports/5v9/report.md   — Solr 5 vs Solr 9
#   reports/combined_summary.md
```

**Supported sample comparisons**

This harness includes sample drift reports for:

- Solr 5 → Solr 8
- Solr 5 → Solr 9
- Solr 8 → Solr 9

The combined report is at `reports/sample/combined_summary.md`.

**Interpretation:** In this sample corpus and configuration, the Solr 5 → 8 and Solr 5 → 9 comparisons show measurable candidate, rank, and score drift. The Solr 8 → 9 sample is stable under the same controlled setup. This illustrates why migration validation should be measured per version pair and configuration, rather than assumed from successful query execution alone.

This is a demo harness to quantify behavior drift across Solr/Lucene major versions under controlled configs and make ranking differences observable before migration rollout.
It does not claim Lucene is "wrong"—only that behavior can differ and should be measured for migrations.

### For Ranking-Critical, ML-Driven, and Revenue-Sensitive Systems

> **Audience**  
> Senior engineers operating Solr/Lucene where search feeds ranking, ML pipelines, auctions, or revenue-critical decisioning.
>
> **Scope**  
> Major version upgrades (e.g., Solr/Lucene 5 to 8) where *silent semantic drift and tail-latency regressions* are more dangerous than obvious failures.

This approach focuses on **correctness and semantic equivalence**, not just configuration or dependency upgrades.

---

## Example drift signals from the sample reports

### Solr 5 vs Solr 8 — significant drift across Lucene major version boundary

- `q_basic` → Jaccard: `0.818`, RBO(p=0.9): `0.943`, max normalized drift: `0.190` ❌
- `q_phrase_freq` → Jaccard: `0.667`, RBO(p=0.9): `0.852`, max rank delta: `4`, max normalized drift: `0.335` ❌
- `q_brand_anker` → Jaccard: `1.000`, RBO(p=0.9): `0.469`, no rank changes, but max normalized drift: `0.276` ❌

### Solr 8 vs Solr 9 — clean migration with equivalent similarity configuration

- All 8 queries: Jaccard: `1.000`, RBO(p=0.9): `1.000`, rank delta: `0`, score drift: `0.000` ✅

This contrast illustrates the core value of the harness: the Solr 5 → 8 boundary introduced measurable ranking drift across 7 of 8 queries, while Solr 8 → 9 (with explicitly configured ClassicSimilarity) produced zero drift — giving teams confidence their migration is safe before switching production traffic.

## Drift Metrics

The harness reports the following metrics per query pair:

**Jaccard(top-N)** measures candidate set overlap as an unweighted ratio. It detects when documents enter or leave the result set but is blind to rank order changes within the set.

**RBO (Rank-Biased Overlap, p=0.9)** measures top-weighted ranked-list similarity. Unlike Jaccard, RBO penalizes rank changes near the top of the result list more heavily than changes near the bottom — rank 1 carries roughly 10x the weight of rank 10. A value of 1.0 means identical ranking; 0.0 means completely disjoint. Suggested by [@epugh](https://github.com/epugh). Implemented following Webber et al., ACM TOIS 2010.

**Avg / Max Abs Rank Delta** measures how far individual documents moved in rank position across versions.

**Max Abs Normalized Score Drift** measures score distribution change normalized by the top document score, making it comparable across queries with different score magnitudes.

## Production Use

This approach was used to validate a production migration from Solr 5 to Solr 8 in a large-scale ads retrieval system.

The same methodology was later reused during a Solr 8 to Solr 9 upgrade.

The goal is to provide a repeatable way to analyze ranking drift during major search infrastructure upgrades.

The public harness includes sample reports for 5→8, 5→9, and 8→9 comparisons.

## Why This Approach Exists

Many Solr/Lucene migrations fail in production even when:
- queries succeed,
- tests pass,
- dashboards look healthy.

The failures are typically **silent**:
- candidate recall drops without errors,
- ranking becomes unstable (rank churn),
- ML feature distributions drift,
- p99 latency regresses while averages remain flat.

These issues arise from **cumulative semantic and execution-path changes**, not from missing configuration or tuning mistakes.

---

## 0. Define the Equivalence Contract (Before Any Upgrade)

### Why this matters
Without an explicit definition of “equivalent behavior,” migration debates become subjective and regressions get normalized as “acceptable differences.”

### Define upfront
- **Candidate recall**  
  Top-K eligible documents must not disappear beyond an agreed threshold.
- **Relative ordering stability (rank churn bounds)**  
  Small score changes are acceptable; unstable ordering is not.
- **Feature compatibility**  
  Extracted features must remain semantically consistent for downstream ML.
- **Tail latency budget**  
  p95/p99 under realistic load must remain within SLO.

### Practical guidance
- Write these constraints down *before* starting the migration.
- Make them measurable.
- Use them as **hard gates**, not advisory checks.

### Freeze a representative query set
Include:
- Head queries (high traffic, systemic effects)
- Tail queries (rare but often revenue-critical)
- Complex query shapes:
  - function queries and boosts
  - filters and minShouldMatch
  - joins / nested docs
  - transformers
- Known edge cases (negative boosts, large field payloads)

---

## 1. Side-by-Side Semantic Validation (Old vs New Version)

### Why this matters
Solr/Lucene upgrades often produce **valid but different** results. API-level success does not imply semantic equivalence.

Run **old and new versions against identical inputs** and compare outputs explicitly.

---

### 1.1 Candidate Set Stability

**Why**  
Candidate loss upstream is catastrophic for ML and auctions, yet often invisible.

**What to check**
- Compare top-N document IDs per query.
- Measure overlap / recall deltas.
- Identify documents that disappear entirely.

**Common failure mode**
Changes in scoring, collectors, or query rewrites silently exclude documents early in the pipeline.

---

### 1.2 Rank Churn & Ordering Drift

**Definition**  
Rank churn is instability in document ordering for identical queries, even when recall is unchanged.

**Why**  
Many systems depend on *relative order*, not absolute scores.

**What to check**
- Rank correlation for top-N.
- Queries with unstable ordering across retries.
- Whether churn is global or tied to specific queries.

**Common failure mode**
Small floating-point or normalization changes compound under concurrency, producing different winners per execution.

---

### 1.3 Score Distribution Drift (Relative > Absolute)

**Why**  
Absolute scores rarely matter; relative differences do.

**What to check**
- Score histograms and quantiles.
- Near-ties and tie-breaking behavior.
- Changes in normalization or scaling.

**Common failure mode**
Seemingly minor normalization changes invalidate downstream assumptions encoded in ML features or ranking heuristics.

---

## 2. Explain / Debug Analysis (Structural, Not Ad-Hoc)

> **Goal**  
> Understand *why* semantics changed, not just *that* they changed.

Explain output is powerful but easy to misuse.

---

### 2.1 When to Enable Debug / Explain

**Guidelines**
- Enable `debugQuery=true` only for:
  - representative, high-impact queries
  - queries exhibiting rank churn or candidate loss
- Never rely on a single explain output.

Explain analysis should be **targeted and comparative**, not exploratory.

---

### 2.2 What to Compare Across Versions

Compare structurally, not just numerically:
- Parsed query (`parsedquery`, `parsedquery_toString`)
- Rewritten query trees
- Weight to Scorer hierarchy
- Per-clause score contributions
- Similarity and normalization components

---

### 2.3 What Not to Assume

- Identical explain trees != identical semantics
- Similar final scores != equivalent ranking under load
- Explain output != full execution-path behavior

Explain shows *logical scoring*, not collector order, concurrency effects, or response-path cost.

---

### 2.4 Explain Patterns That Signal Semantic Drift

Watch for:
- Missing scorer branches that previously contributed
- Function queries producing negative intermediate values
- Changed normalization or coordination factors
- Collector behavior that suppresses documents silently

---

### 2.5 Safe Scaling of Explain Analysis

**Why**  
Explain can distort production behavior.

**How**
- Capture explains offline or via shadow traffic
- Avoid enabling debug on hot production paths
- Correlate explain findings with:
  - rank churn metrics
  - candidate recall loss
  - feature drift

---

## 3. Negative Scores & Suppression Hazards

### Why this matters
Negative-score handling differs across Lucene versions and can silently remove candidates.

### What to do
- Audit all function queries and boosts.
- Identify queries producing negative intermediate values.
- Verify whether collectors suppress such documents.

### Guideline
Apply offsets or transformations **only if relative ordering intent is preserved**. Fix semantics before tuning.

---

## 4. ML Feature Compatibility (If Retrieval Feeds Ranking Models)

### 4.1 Training–Serving Parity

**Why**
Models encode retrieval assumptions implicitly.

**What to check**
- Feature vectors across versions.
- Statistical drift (mean, variance, quantiles).
- Missing or newly introduced features.

---

### 4.2 Feature Dependency Mapping

Map which features depend on:
- Scores, norms, similarity
- DocValues or stored fields
- Function queries or boosts

This helps isolate which retrieval changes break models.

---

### 4.3 Decision Rule

If recall or ordering semantics change:
- **Fix retrieval first**
- Retraining alone rarely restores correctness when upstream assumptions break

---

## 5. Query Rewrite & “Valid but Different” Behavior

### Why this matters
Solr/Lucene may rewrite, alter, or disallow sub-queries without throwing errors.

### What to check
- Rewritten query trees across versions
- Silently altered or removed clauses
- Impact on candidate set and ordering

Treat “valid responses” as suspect if semantics differ.

---

## 6. Performance Validation: Measure the Right Thing

### 6.1 Phase-Level Breakdown

**Why**

Most regressions hide outside core matching.

Measure separately:
- Matching / scoring
- Top-K selection
- Field loading
- Transformer execution
- Response construction and serialization

---

### 6.2 Tail Latency Under Real Load

**Why**

Averages hide risk.

**How**
- Use production-like concurrency
- Use realistic payload sizes
- Match index segment structure
- Track p95 / p99 / worst-minute latency

---

### 6.3 Query Shape Sensitivity

Identify regressions correlated with:
- Transformer-heavy queries
- Stored fields vs DocValues
- Joins or nested documents
- Large response payloads

---

## 7. System-Level Integration Checks (Deployment-Specific)

### Why this matters
System integration often amplifies Solr-level changes.

Check:
- Client retries and timeouts
- Correct attribution of response-path cost
- Embedded or same-JVM deployments:
  - CPU and allocation profiling
  - Avoidable serialization boundaries

---

## 8. Rollout & Safety Gates

### Why this matters
Some failures only surface after exposure to real traffic.

### Required gates
- Canary with shadow traffic
- Online comparison of:
  - candidate overlap
  - rank churn
  - feature drift
- Explicit rollback triggers on:
  - recall loss
  - p99 regression
  - feature drift thresholds
- Preserve “golden” debug traces for rapid diagnosis

---

## 9. Migration Report (Required Deliverable)

Produce a written report capturing:
- Semantic equivalence metrics (overlap, churn, drift)
- Tail-latency phase breakdowns
- Root-cause categories encountered
- Residual deltas accepted (and why)

This report is the *final artifact* of the migration.

---
## Related Article

This repository was created while diagnosing a Solr 5 to Solr 8 migration in a production ads retrieval system.

The full story behind the migration, including the semantic drift issues, ML feature compatibility challenges, and response-path latency optimizations, is described in this article:

**Unblocking a Failed Solr 5 to Solr 8 Migration in a Large-Scale Ads Retrieval System**

https://dzone.com/articles/solr5-to-solr8-migration-ads-system

---
## Key Takeaway

> **Major Solr/Lucene upgrades fail not because of missing configuration, but because semantic and execution-path assumptions evolve independently of downstream systems.**  
> Correct migrations require **explicit semantic validation**, **structured explain analysis**, and **tail-latency awareness**—not just successful queries.

---

This repository provides a practical and repeatable approach for detecting ranking drift during major Solr/Lucene upgrades.
