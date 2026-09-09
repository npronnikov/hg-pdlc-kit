# BMAD monorepo: PRD → architecture → SRS → code → E2E

Версия 3.0. Реальный контракт — FLOW.yaml.

| Нода | Тип | Назначение | Следующие переходы |
|---|---|---|---|
| command-prepare | command | Подготовить project verifier и исходный снимок | on_success → ai-discover |
| ai-discover | ai | Изучить монорепозиторий и подготовить интервью | on_success → human-interview |
| human-interview | human_input | Интервью владельца продукта | on_submit → ai-prd; on_rework → ai-discover |
| ai-prd | ai | PRD, бизнес-правила и критерии приёмки | on_success → command-prd-check; on_questions → ai-discover; on_blocked → terminal-blocked |
| command-prd-check | command | Проверить PRD-трассировку | on_success → ai-prd-review |
| ai-prd-review | ai | Независимо проверить бизнес-полноту | on_success → human-prd-approval; on_rework → ai-prd; on_intent → ai-discover; on_blocked → terminal-blocked |
| human-prd-approval | human_approval | Утвердить намерение и PRD | on_approve → command-seal-prd; on_rework → ai-prd |
| command-seal-prd | command | Зафиксировать принятый набор PRD | on_success → ai-architecture |
| ai-architecture | ai | C4, arc42-профиль и ADR | on_success → ai-srs; on_intent → ai-discover; on_blocked → terminal-blocked |
| ai-srs | ai | SRS и интерфейсные контракты | on_success → ai-test-model; on_architecture → ai-architecture; on_intent → ai-discover; on_blocked → terminal-blocked |
| ai-test-model | ai | Модель E2E и конечный план проверок | on_success → ai-stories; on_system → ai-srs; on_intent → ai-discover; on_blocked → terminal-blocked |
| ai-stories | ai | Epics/stories, зависимости и риск | on_success → command-design-check; on_system → ai-srs; on_blocked → terminal-blocked |
| command-design-check | command | Проверить связность design→тесты→stories | on_success → ai-readiness |
| ai-readiness | ai | Implementation readiness и карта решения человека | on_success → command-seal-design-auto; on_approval → human-design-approval; on_architecture → ai-architecture; on_system → ai-srs; on_model → ai-test-model; on_plan → ai-stories; on_intent → ai-discover; on_blocked → terminal-blocked |
| human-design-approval | human_approval | Техническое решение по дизайну и риску | on_approve → command-seal-design-human; on_rework → ai-architecture |
| command-seal-design-auto | command | Применить согласованную low-risk политику | on_success → ai-implement |
| command-seal-design-human | command | Зафиксировать техническое согласование | on_success → ai-implement |
| ai-implement | ai | Реализовать stories в монорепозитории | on_success → command-code-check; on_architecture → ai-architecture; on_system → ai-srs; on_intent → ai-discover; on_blocked → terminal-blocked |
| command-code-check | command | Проверить stories→реальный код | on_success → command-build |
| command-build | command | Выполнить настоящую конечную сборку/проверки | on_success → ai-build-review |
| ai-build-review | ai | Разобрать результат сборки и структурной проверки | on_success → ai-code-review; on_rework → ai-implement; on_system → ai-srs; on_architecture → ai-architecture; on_blocked → terminal-blocked |
| ai-code-review | ai | Три независимых каталожных code reviewer | on_success → ai-e2e; on_code → ai-implement; on_system → ai-srs; on_architecture → ai-architecture; on_intent → ai-discover; on_blocked → terminal-blocked |
| ai-e2e | ai | Написать исполняемые E2E по принятой модели | on_success → ai-test-review; on_model → ai-test-model; on_system → ai-srs; on_blocked → terminal-blocked |
| ai-test-review | ai | Проверить E2E oracle и настоящий системный контур | on_success → command-e2e; on_rework → ai-e2e; on_model → ai-test-model; on_blocked → terminal-blocked |
| command-e2e | command | Исполнить E2E и сопоставить реальные результаты с ID | on_success → ai-evidence-review |
| ai-evidence-review | ai | Приёмка evidence или трассируемый возврат | on_success → command-finalize; on_code → ai-implement; on_test → ai-e2e; on_model → ai-test-model; on_system → ai-srs; on_architecture → ai-architecture; on_intent → ai-discover; on_blocked → terminal-blocked |
| command-finalize | command | Закончить только со свежими полными E2E | on_success → terminal-done |
| terminal-done | terminal | Проверено — без интеграции и релиза |  |
| terminal-blocked | terminal | Остановлено: ошибка, блокер или исчерпанный rework |  |

## Артефакты по нодам

### command-prepare

- `project: pdlc/tooling/verify.py` — required
- `run: setup-report.json` — required
- `project: pdlc/changes/*/manifest.json` — required

### ai-discover

- `project: pdlc/changes/*/intent.md` — required
- `project: pdlc/changes/*/analysis.md` — required
- `project: pdlc/changes/*/sources.json` — required
- `run: interview.md` — required

### human-interview

- `run: interview.md` — required

### ai-prd

- `project: pdlc/changes/*/PRD.md` — required
- `project: pdlc/changes/*/decisions.md` — required
- `project: pdlc/changes/*/trace/intent.json` — required

### command-prd-check

- `run: prd-check.json` — required
- `project: pdlc/changes/*/trace/graph.json` — required
- `project: pdlc/changes/*/trace/matrix.md` — required

### ai-prd-review

- `run: prd-review.json` — required

### command-seal-prd

- `run: seal-prd.json` — required
- `project: pdlc/changes/*/approvals/prd.json` — required

### ai-architecture

- `project: pdlc/changes/*/architecture.md` — required
- `project: pdlc/changes/*/architecture.dsl` — required
- `project: pdlc/changes/*/adr.md` — required
- `project: pdlc/changes/*/trace/architecture.json` — required

### ai-srs

- `project: pdlc/changes/*/SRS.md` — required
- `project: pdlc/changes/*/contracts/index.md` — required
- `project: pdlc/changes/*/contracts/openapi.yaml` — optional
- `project: pdlc/changes/*/contracts/asyncapi.yaml` — optional
- `project: pdlc/changes/*/contracts/ui.md` — optional
- `project: pdlc/changes/*/contracts/cli.md` — optional
- `project: pdlc/changes/*/trace/system.json` — required

### ai-test-model

- `project: pdlc/changes/*/test-model.md` — required
- `project: pdlc/changes/*/test-model.feature` — required
- `project: pdlc/changes/*/verification-plan.json` — required
- `project: pdlc/changes/*/trace/tests.json` — required

### ai-stories

- `project: pdlc/changes/*/stories.md` — required
- `project: pdlc/changes/*/risk.json` — required
- `project: pdlc/changes/*/trace/stories.json` — required

### command-design-check

- `run: design-check.json` — required
- `project: pdlc/changes/*/trace/graph.json` — required
- `project: pdlc/changes/*/trace/matrix.md` — required

### ai-readiness

- `run: readiness-review.json` — required

### command-seal-design-auto

- `run: seal-design.json` — required
- `project: pdlc/changes/*/approvals/design.json` — required

### command-seal-design-human

- `run: seal-design.json` — required
- `project: pdlc/changes/*/approvals/design.json` — required

### ai-implement

- `project: pdlc/changes/*/implementation.md` — required
- `project: pdlc/changes/*/implementation-map.json` — required
- `project: pdlc/changes/*/trace/code.json` — required

### command-code-check

- `run: code-check.json` — required
- `project: pdlc/changes/*/trace/graph.json` — required
- `project: pdlc/changes/*/trace/matrix.md` — required

### command-build

- `run: build-report.json` — required
- `run: build.stdout.log` — required
- `run: build.stderr.log` — required

### ai-build-review

- `run: build-review.json` — required

### ai-code-review

- `run: code-review.json` — required

### ai-e2e

- `project: pdlc/changes/*/e2e-map.json` — required
- `project: pdlc/changes/*/e2e-implementation.md` — required

### ai-test-review

- `run: test-review.json` — required

### command-e2e

- `run: e2e-report.json` — required
- `run: e2e-results.xml` — required
- `run: e2e.stdout.log` — required
- `run: e2e.stderr.log` — required
- `project: pdlc/changes/*/verification.json` — required
- `project: pdlc/changes/*/verification.md` — required
- `project: pdlc/changes/*/trace/evidence.json` — required

### ai-evidence-review

- `run: acceptance-review.json` — required
- `project: pdlc/changes/*/acceptance.json` — required

### command-finalize

- `run: finalize-report.json` — required
- `project: pdlc/changes/*/delivery.md` — required
- `project: pdlc/changes/*/trace/graph.json` — required
- `project: pdlc/changes/*/trace/matrix.md` — required
