#!/usr/bin/env bash
set -euo pipefail
report="$1"
# Adapt to real app + test database + readiness + E2E + cleanup (trap/finally).
# The test runner must write reporter-contract JSON to "$report" and return its real exit code.
printf '%s\n' 'BLOCKED: configure real E2E, never replace with mocked unit tests' >&2
exit 78
