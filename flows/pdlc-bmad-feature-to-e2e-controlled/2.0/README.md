# BMAD: PRD → архитектура → SRS → stories → код → E2E · controlled

## Узлы

| Нода | Тип | Skill | Subagent | Выходы |
|---|---|---|---|---|
| ai-intake | ai | pdlc-intake@2.0, pdlc-contracts@2.0 |  | run: binding.json<br>project: pdlc/changes/*/intent.md |
| command-inventory | command |  |  | run: report.json<br>run: inventory.json |
| ai-context | ai | pdlc-context-interview@2.0, pdlc-contracts@2.0 | pdlc-repository-scout@2.0 | project: pdlc/changes/*/analysis.md<br>run: context-index.md<br>run: interview.md |
| human-interview | human_input |  |  | run: interview.md |
| ai-prd | ai | pdlc-prd@2.0, pdlc-contracts@2.0 |  | project: pdlc/changes/*/PRD.md<br>project: pdlc/changes/*/hypothesis.md<br>project: pdlc/changes/*/decisions.json<br>project: pdlc/changes/*/trace/graph.json |
| ai-prd-review | ai | pdlc-prd-review@2.0, pdlc-contracts@2.0 | pdlc-prd-reviewer@2.0 | run: review.json |
| command-prd-check | command |  |  | run: report.json |
| human-prd | human_approval |  |  |  |
| command-freeze-intent | command |  |  | run: report.json<br>run: freeze.json |
| ai-architecture | ai | pdlc-architecture@2.0, pdlc-contracts@2.0 |  | project: pdlc/changes/*/architecture.md<br>project: pdlc/changes/*/architecture.dsl<br>project: pdlc/changes/*/adr.md<br>project: pdlc/changes/*/trace/graph.json<br>project: pdlc/product/verification.json |
| ai-srs | ai | pdlc-srs@2.0, pdlc-contracts@2.0 |  | project: pdlc/changes/*/SRS.md<br>project: pdlc/changes/*/contracts.md<br>project: pdlc/changes/*/trace/graph.json<br>project: pdlc/changes/*/contracts/openapi.yaml<br>project: pdlc/changes/*/contracts/asyncapi.yaml |
| ai-test-design | ai | pdlc-test-design@2.0, pdlc-contracts@2.0 |  | project: pdlc/changes/*/test-model.json<br>project: pdlc/changes/*/test-model.feature<br>project: pdlc/changes/*/trace/graph.json |
| ai-stories | ai | pdlc-stories@2.0, pdlc-contracts@2.0 |  | project: pdlc/changes/*/epics.md<br>project: pdlc/changes/*/stories.json<br>project: pdlc/changes/*/trace/graph.json |
| ai-design-review | ai | pdlc-readiness-review@2.0, pdlc-contracts@2.0 | pdlc-design-reviewer@2.0 | run: review.json |
| command-readiness | command |  |  | run: report.json |
| human-tech | human_approval |  |  |  |
| command-freeze-design | command |  |  | run: report.json<br>run: freeze.json |
| ai-implement | ai | pdlc-build-stories@2.0, pdlc-contracts@2.0 | pdlc-implementer@2.0 | project: pdlc/changes/*/implementation-map.json<br>project: pdlc/changes/*/trace/graph.json |
| ai-e2e-author | ai | pdlc-e2e-author@2.0, pdlc-contracts@2.0 | pdlc-e2e-engineer@2.0 | project: pdlc/changes/*/implementation-map.json |
| ai-code-review | ai | pdlc-code-review@2.0, pdlc-contracts@2.0 | pdlc-code-reviewer@2.0 | run: review.json |
| ai-test-review | ai | pdlc-test-review@2.0, pdlc-contracts@2.0 | pdlc-test-reviewer@2.0 | run: review.json |
| command-checks | command |  |  | run: report.json<br>run: checks-evidence.json<br>run: evidence-index.json<br>run: execution.json<br>run: test.stdout.log<br>run: test.stderr.log<br>run: junit.xml |
| command-e2e | command |  |  | run: report.json<br>run: evidence.json<br>run: evidence-index.json<br>run: execution.json<br>run: test.stdout.log<br>run: test.stderr.log<br>run: junit.xml<br>run: browser-traces.zip |
| command-trace-verify | command |  |  | run: report.json<br>run: trace-result.json |
| ai-acceptance | ai | pdlc-acceptance@2.0, pdlc-contracts@2.0 | pdlc-acceptance-auditor@2.0 | run: review.json |
| command-final | command |  |  | run: report.json<br>project: pdlc/changes/*/validation-summary.json<br>project: pdlc/changes/*/trace/matrix.md |
| ai-triage | ai | pdlc-correct-course@2.0, pdlc-contracts@2.0 |  | run: triage.json |
| ai-environment | ai | pdlc-environment@2.0, pdlc-contracts@2.0 |  | run: environment-report.md |
| terminal-verified | terminal |  |  |  |
| terminal-blocked | terminal |  |  |  |

## Совместимость
Native-профиль subagent требует проверки импортера. Для старого снимка используйте tools/export_compat.py; весь вывод остаётся каталогом. Никакие статусы/счётчики запуска не сохраняются в pdlc/.

## Граница
Подробные контракты: pdlc-contracts@2.0; у каждого этапа собственный skill. Ошибки исполнения идут в terminal-blocked через failure_node_id; negative quality verdict — через declared route. Участие человека не требует ручной передачи файлов.
