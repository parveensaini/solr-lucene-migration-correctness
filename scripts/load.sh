#!/usr/bin/env bash
set -euo pipefail

SOLR5="${SOLR5:-http://127.0.0.1:8985/solr/core1}"
SOLR8="${SOLR8:-http://127.0.0.1:8988/solr/core1}"
DOCS="${1:-corpus/docs.json}"

post_update () {
  local base="$1"
  echo "Loading into $base"

  # Retry a few times to survive container warmup/restarts
  for attempt in 1 2 3 4 5; do
    # Capture HTTP status + body
    tmp="$(mktemp)"
    code="$(curl -sS --max-time 10 --retry 0 \
      -o "$tmp" -w "%{http_code}" \
      -H 'Content-Type: application/json' \
      --data-binary @"${DOCS}" \
      "${base}/update?commit=true" || true)"

    if [[ "$code" == "200" ]]; then
      # Validate Solr returned status 0
      if grep -q '"status"[[:space:]]*:[[:space:]]*0' "$tmp"; then
        rm -f "$tmp"
        echo "OK"
        return 0
      fi
      echo "Non-zero Solr status (attempt $attempt). Response:"
      cat "$tmp"; echo
    else
      echo "HTTP $code (attempt $attempt). Response:"
      cat "$tmp" 2>/dev/null || true
      echo
    fi

    rm -f "$tmp"
    sleep 1
  done

  echo "FAILED loading into $base after retries."
  return 1
}

post_update "$SOLR5"
post_update "$SOLR8"
echo "Done."
