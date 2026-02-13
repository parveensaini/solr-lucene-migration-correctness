#!/usr/bin/env bash
set -euo pipefail

SOLR5="${SOLR5:-http://127.0.0.1:8985/solr}"
SOLR8="${SOLR8:-http://127.0.0.1:8988/solr}"

wait_one () {
  local base="$1"
  local name="$2"
  echo "Waiting for $name ..."
  for i in {1..30}; do
    if curl -sS --max-time 2 "${base}/admin/info/system?wt=json" >/dev/null; then
      echo "$name ready"
      return 0
    fi
    sleep 1
  done
  echo "$name not ready"
  return 1
}

wait_one "$SOLR5" "solr5"
wait_one "$SOLR8" "solr8"
