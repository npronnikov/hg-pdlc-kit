# BMAD monorepo: восстановление проверяемой базы

Версия 3.0. Реальный контракт — FLOW.yaml.

| Нода | Тип | Назначение | Следующие переходы |
|---|---|---|---|
| command-prepare | command | Подготовить project verifier и исходный снимок | on_success → ai-baseline |
| ai-baseline | ai | Восстановить as-is базу одного монорепозитория | on_success → human-baseline-interview; on_blocked → terminal-blocked |
| human-baseline-interview | human_input | Уточнить противоречия восстановленной базы | on_submit → ai-baseline-refine; on_rework → ai-baseline |
| ai-baseline-refine | ai | Перенести решения ВП в полезную базу | on_success → command-baseline-check; on_questions → ai-baseline; on_blocked → terminal-blocked |
| command-baseline-check | command | Проверить происхождение и актуальность базы | on_success → ai-baseline-review |
| ai-baseline-review | ai | Проверить восстановленные знания | on_success → human-baseline-approval; on_rework → ai-baseline; on_blocked → terminal-blocked |
| human-baseline-approval | human_approval | Принять базу с сохранением неизвестного | on_approve → command-baseline-seal; on_rework → ai-baseline |
| command-baseline-seal | command | Зафиксировать принятый as-is baseline | on_success → terminal-done |
| terminal-done | terminal | База принята с сохранением unknown |  |
| terminal-blocked | terminal | Остановлено: ошибка, блокер или исчерпанный rework |  |

## Артефакты по нодам

### command-prepare

- `project: pdlc/tooling/verify.py` — required
- `run: setup-report.json` — required

### ai-baseline

- `project: pdlc/product/index.md` — required
- `project: pdlc/product/business.md` — required
- `project: pdlc/product/architecture.md` — required
- `project: pdlc/product/architecture.dsl` — required
- `project: pdlc/product/system.md` — required
- `project: pdlc/product/test-model.md` — required
- `project: pdlc/product/sources.json` — required
- `project: pdlc/product/trace.json` — required
- `run: interview.md` — required

### human-baseline-interview

- `run: interview.md` — required

### ai-baseline-refine

- `project: pdlc/product/index.md` — required
- `project: pdlc/product/business.md` — required
- `project: pdlc/product/architecture.md` — required
- `project: pdlc/product/architecture.dsl` — required
- `project: pdlc/product/system.md` — required
- `project: pdlc/product/test-model.md` — required
- `project: pdlc/product/sources.json` — required
- `project: pdlc/product/trace.json` — required

### command-baseline-check

- `run: baseline-check.json` — required

### ai-baseline-review

- `run: bootstrap-review.json` — required

### command-baseline-seal

- `run: baseline-seal.json` — required
- `project: pdlc/product/baseline.json` — required
