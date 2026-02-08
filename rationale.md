# Rationale

This checklist distills lessons learned from multiple large-scale Solr/Lucene major-version migrations in ranking- and ML-sensitive production systems.

It focuses on failure modes that are often silent:
- semantic drift
- rank churn
- candidate loss
- tail-latency regressions

The checklist is intended as field guidance for senior engineers and is complementary to
official Solr/Lucene upgrade documentation.

