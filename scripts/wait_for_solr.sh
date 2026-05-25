#!/usr/bin/env bash
# wait_for_solr.sh — polls /admin/ping on all three Solr instances until
# each responds 200. Call this between `up.sh` and `load.sh` so that
# load retries don't silently swallow startup failures.
set -euo pipefail

SOLR5="${SOLR5:-http://127.0.0.1:8985/solr/core1}"
SOLR8="${SOLR8:-http://127.0.0.1:8988/solr/core1}"
SOLR9="${SOLR9:-http://127.0.0.1:8989/solr/core1}"

MAX_WAIT="${MAX_WAIT:-90}"   # seconds before giving up
INTERVAL=3

wait_for () {
  local name="$1"
  local url="$2/admin/ping?wt=json"
  local elapsed=0

  echo "Waiting for $name at $url ..."
  while true; do
    code="$(curl -sS --max-time 5 -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || true)"
    if [[ "$code" == "200" ]]; then
      echo "  $name is ready."
      return 0
    fi
    if [[ $elapsed -ge $MAX_WAIT ]]; then
      echo "  TIMEOUT: $name did not become ready within ${MAX_WAIT}s (last HTTP $code)."
      return 1
    fi
    sleep "$INTERVAL"
    elapsed=$(( elapsed + INTERVAL ))
  done
}

wait_for "solr5" "$SOLR5"
wait_for "solr8" "$SOLR8"
wait_for "solr9" "$SOLR9"

echo "All Solr instances ready."
