#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip -q install -r requirements.txt

docker-compose -f docker/docker-compose.yml up -d

# Wait for both cores to answer ping
for port in 8985 8988; do
  url="http://localhost:${port}/solr/core1/admin/ping?wt=json"
  echo "Waiting for ${url} ..."
  for i in $(seq 1 60); do
    if curl -sf "$url" >/dev/null; then
      echo "OK: ${port}"
      break
    fi
    sleep 1
  done
done

# Load corpus into both
bash scripts/load.sh corpus/docs.json

# Run diff
rm -rf reports/*
mkdir -p reports

TOPN="${TOPN:-10}"
EXPLAIN_TOP="${EXPLAIN_TOP:-2}"

TOPN="$TOPN" EXPLAIN_TOP="$EXPLAIN_TOP" python3 scripts/diff.py corpus/queries.json reports

echo "Wrote reports/report.md and reports/summary.json"
echo "Open: reports/report.md"
