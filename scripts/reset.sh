#!/usr/bin/env bash
set -euo pipefail
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d

