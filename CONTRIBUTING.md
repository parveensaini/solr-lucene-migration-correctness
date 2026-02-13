# Contributing

Thanks for checking out this repository.

This is a **demo harness** to measure Solr 5 vs Solr 8 behavioral drift
(overlap, rank churn, score drift) under controlled configurations.

Quick start:

    bash scripts/demo.sh

Outputs:
- reports/report.md
- reports/summary.json

Helpful contributions:
- Add new query scenarios (with a short note explaining what it demonstrates)
- Add realistic documents to the corpus (keep it small and explain intent)
- Improve report metrics (e.g., pairwise ordering flips)
- Clarify interpretation of PASS/WARN/FAIL

Ground rules:
- Keep changes reproducible and deterministic.
- Avoid overstating claims: drift ≠ bug.
