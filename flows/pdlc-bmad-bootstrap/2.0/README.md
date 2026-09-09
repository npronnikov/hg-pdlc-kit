# BMAD brownfield: восстановление базы знаний

## Узлы

| Нода | Тип | Skill | Subagent | Выходы |
|---|---|---|---|---|
| ai-intake | ai | pdlc-intake@2.0, pdlc-contracts@2.0 |  | run: binding.json<br>project: pdlc/changes/*/intent.md |
| command-inventory | command |  |  | run: report.json<br>run: inventory.json |
| ai-bootstrap | ai | pdlc-bootstrap@2.0, pdlc-contracts@2.0 | pdlc-repository-scout@2.0 | project: pdlc/changes/*/baseline/index.md<br>project: pdlc/changes/*/baseline/business.md<br>project: pdlc/changes/*/baseline/architecture.md<br>project: pdlc/changes/*/baseline/architecture.dsl<br>project: pdlc/changes/*/baseline/SRS.md<br>project: pdlc/changes/*/baseline/test-model.json<br>project: pdlc/changes/*/baseline/facts.json |
| ai-baseline-review | ai | pdlc-baseline-review@2.0, pdlc-contracts@2.0 | pdlc-baseline-auditor@2.0 | run: review.json |
| command-baseline-check | command |  |  | run: report.json<br>run: baseline-digest.json |
| human-baseline | human_approval |  |  |  |
| command-baseline-seal | command |  |  | run: report.json<br>project: pdlc/product/context.md<br>project: pdlc/product/business/overview.md<br>project: pdlc/product/architecture/architecture.md<br>project: pdlc/product/architecture/architecture.dsl<br>project: pdlc/product/system/SRS.md<br>project: pdlc/product/tests/model.json<br>project: pdlc/product/trace/facts.json |
| terminal-baseline | terminal |  |  |  |
| terminal-blocked | terminal |  |  |  |

## Совместимость
Native-профиль subagent требует проверки импортера. Для старого снимка используйте tools/export_compat.py; весь вывод остаётся каталогом. Никакие статусы/счётчики запуска не сохраняются в pdlc/.

## Граница
Подробные контракты: pdlc-contracts@2.0; у каждого этапа собственный skill. Ошибки исполнения идут в terminal-blocked через failure_node_id; negative quality verdict — через declared route. Участие человека не требует ручной передачи файлов.
