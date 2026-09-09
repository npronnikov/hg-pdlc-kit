# План реализации
DEMO-PLAN-1; один Git-корень, Node API и SQLite; изменение требований только через upstream rework.
## DAG
TASK-001 migration → TASK-002 HTTP/auth/CAS → TASK-003 validation → TASK-004 E2E; точный DAG в JSON.
## Commands
bash tools/hg/build.sh: syntax + node unit tests, timeout HG 900s.
bash tools/hg/e2e.sh <run-report>: настоящие isolated process/DB, readiness, сценарии и cleanup.
## Защита
verify.mjs и schemas копируются из catalog resources, hashes в JSON; PRD/business закреплены approval fixture hash.
## Verification
После автоматизации E2E повторить regression, затем E2E на том же snapshot. Финализация не меняет код/контракты.
