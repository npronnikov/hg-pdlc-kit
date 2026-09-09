#!/usr/bin/env bash
set -euo pipefail
node --check apps/api/server.mjs
node --check tests/e2e/ticket-priority.e2e.mjs
node --test tests/unit/*.test.mjs
