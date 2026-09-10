---
name: sdd-test-model
description: Формирует риск-ориентированную модель, сценарии и матрицу покрытия до
  реализации.
---

# Тестовая модель до написания кода

## Цель
Создать test-model.md, test-model.json, acceptance.feature и traceability.csv по принятому PRD и кандидатному SRS; зафиксировать oracle до реализации, затем принять SRS и модель вместе.
## Модель
Ось покрытия: capability → business journey → risk → SYS/AC → SCN → TC → native test selector → execution evidence. Слои unit/component/contract/integration/e2e различаются. E2E пересекает настоящую внешнюю границу системы и проверяет бизнес-результат через UI/API/CLI/event; не внутренний вызов сервиса. Не всё нужно проверять дорогим UI.

Для каждого TC опиши ID, rationale, requirement_ids, acceptance_ids, scenario_id, priority, layer, channel, preconditions, roles, fixture data, steps, oracle, cleanup, environment, automation, mock policy, native selector (planned до реализации), evidence requirements. Happy, alternative, boundary, invalid input, permission/tenant denial, повтор/конкуренция/восстановление — по рискам; каждый исключённый аспект имеет N/A с причиной и approval в модели.

UI-changing feature обязательно имеет UI e2e для ключевого принятого journey, состояния формы/ошибки/права и persistence после reload, если применимо. API-only feature не получает искусственный UI; API e2e проходит реальную app+data/integration boundary. Внешнюю платную/опасную систему можно заменить sandbox/contract-faithful double по согласованию, но core path продукта не замокировать и называть full e2e. Границы и ограничения отражаются в verdict.

NFR может требовать отдельный performance/security/accessibility test или inspection, а не UI e2e; mapping verification_method честный. Доля coverage считается по утверждённому набору обязательных требований, не по числу сгенерированных сценариев.
## Форматы
acceptance.feature: Gherkin на языке команды, комментарии с AC/SCN-ID; не добавляй новые metadata tags. BDD runner не обязателен: .feature может быть specification, native runner tests должны иметь однозначные selectors в model.
traceability.csv: row_kind,document_revision,br_id,ac_id,sys_id,adr_id,scenario_id,test_id,layer,channel,selector,status,evidence_ref. row_kind=metadata содержит только ревизию, row_kind=mapping — реальную связь; metadata не включается в coverage. Одна строка на связь; нет висячих ID. status planned до исполнения.
test-model.json: schema_version, document_revision, change_id, scope_requirements, cases[], exclusions[], exit_policy, risk_matrix[], coverage.
exit_policy: обязательные TC исполняются без skip; 0 тестов не успех; нет flaky обязательных сценариев; нет blocking defects; UI evidence для UI scope; code/tests/spec hashes совпадают с tested revision.
## Ревью
Spec-test auditor независимо ищет дырки/ошибки oracle. Не менять критерий так, чтобы он совпал с уже написанным кодом. Any oracle change возвращается на SRS/model human gate.


## Полный файловый контракт

Этот раздел задаёт имена, scope, условие создания и точный шаблон каждого выхода. Краткие списки выше — обзор, не дополнительные outputs. Выбери только строки текущей ноды из `nodes`; не создавай файлы других стадий. Если `required: false`, всё равно действуют template и condition.

<!-- OUTPUT_CONTRACTS_BEGIN -->
```json
{
  "contract_version": "r4",
  "path_rules": {
    "run": "Путь относительно RUN output root текущей попытки, который дал runtime.",
    "project": "resolved_path относительно выбранного repository root. <run.id> — текущий run, остальные safe IDs из registry; glob в FLOW не задаёт имя каталога."
  },
  "outputs": [
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/test-model.md",
      "resolved_path": "10-defect-contract/test-model.md",
      "required": true,
      "condition": "always",
      "template_id": "test-model",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/test-model.json",
      "resolved_path": "10-defect-contract/test-model.json",
      "required": true,
      "condition": "always",
      "template_id": "test-model-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/acceptance.feature",
      "resolved_path": "10-defect-contract/acceptance.feature",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-feature",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/traceability.csv",
      "resolved_path": "10-defect-contract/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/model-review.md",
      "resolved_path": "10-defect-contract/model-review.md",
      "required": true,
      "condition": "always",
      "template_id": "model-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/test-model.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/test-model.md",
      "required": true,
      "condition": "always",
      "template_id": "test-model",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/test-model.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/test-model.json",
      "required": true,
      "condition": "always",
      "template_id": "test-model-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/acceptance.feature",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/acceptance.feature",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-feature",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/traceability.csv",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/model-review.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/model-review.md",
      "required": true,
      "condition": "always",
      "template_id": "model-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "run",
      "path": "40-test-model/test-model.md",
      "resolved_path": "40-test-model/test-model.md",
      "required": true,
      "condition": "always",
      "template_id": "test-model",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "run",
      "path": "40-test-model/test-model.json",
      "resolved_path": "40-test-model/test-model.json",
      "required": true,
      "condition": "always",
      "template_id": "test-model-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "run",
      "path": "40-test-model/acceptance.feature",
      "resolved_path": "40-test-model/acceptance.feature",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-feature",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "run",
      "path": "40-test-model/traceability.csv",
      "resolved_path": "40-test-model/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "run",
      "path": "40-test-model/model-review.md",
      "resolved_path": "40-test-model/model-review.md",
      "required": true,
      "condition": "always",
      "template_id": "model-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/40-test-model/test-model.md",
      "resolved_path": "docs/sdd/changes/<run.id>/40-test-model/test-model.md",
      "required": true,
      "condition": "always",
      "template_id": "test-model",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/40-test-model/test-model.json",
      "resolved_path": "docs/sdd/changes/<run.id>/40-test-model/test-model.json",
      "required": true,
      "condition": "always",
      "template_id": "test-model-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/40-test-model/acceptance.feature",
      "resolved_path": "docs/sdd/changes/<run.id>/40-test-model/acceptance.feature",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-feature",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/40-test-model/traceability.csv",
      "resolved_path": "docs/sdd/changes/<run.id>/40-test-model/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f08-test-model"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/40-test-model/model-review.md",
      "resolved_path": "docs/sdd/changes/<run.id>/40-test-model/model-review.md",
      "required": true,
      "condition": "always",
      "template_id": "model-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/test-model.md",
      "resolved_path": "30-system/test-model.md",
      "required": true,
      "condition": "always",
      "template_id": "test-model",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/test-model.json",
      "resolved_path": "30-system/test-model.json",
      "required": true,
      "condition": "always",
      "template_id": "test-model-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/traceability.csv",
      "resolved_path": "30-system/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/acceptance.feature",
      "resolved_path": "30-system/acceptance.feature",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-feature",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/model-review.md",
      "resolved_path": "30-system/model-review.md",
      "required": true,
      "condition": "always",
      "template_id": "model-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/test-model.md",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/test-model.md",
      "required": true,
      "condition": "always",
      "template_id": "test-model",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/test-model.json",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/test-model.json",
      "required": true,
      "condition": "always",
      "template_id": "test-model-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/traceability.csv",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/acceptance.feature",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/acceptance.feature",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-feature",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/model-review.md",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/model-review.md",
      "required": true,
      "condition": "always",
      "template_id": "model-review",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `acceptance-feature` — Gherkin спецификация

Не добавлять новые metadata/BDD tags; ID в комментариях. Это спецификация, пока нет executable binding.

```gherkin
# language: ru
# revision: {{REVISION}}; run_id: {{RUN_ID}}; step_id: {{NODE_ID}}; attempt: {{ATTEMPT}}
# sources: {{BR_AC_SYS_IDS_AND_HASHES}}
Функциональность: {{подтверждённая capability}}
  # SCN-{{cap}}-001; AC-{{cap}}-001; SYS-{{cap}}-001
  Сценарий: {{наблюдаемый бизнес-результат}}
    Допустим {{подтверждённые предусловия и роль}}
    Когда {{действие на внешней границе}}
    Тогда {{проверяемый результат из AC}}
  # SCN-{{cap}}-002; AC-{{cap}}-002
  Сценарий: {{подтверждённый отрицательный исход}}
    Допустим {{условие отказа}}
    Когда {{проверяемое действие}}
    Тогда {{безопасный отказ и отсутствие побочного эффекта}}
```

### Шаблон `model-review` — Ревью тестовой модели

```markdown
# Ревью тестовой модели

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Объект и границы проверки
{{Профиль ревью, входные files/hashes, принятые требования, out-of-scope.}}
## Независимые задания и ожидание
| Сабагент | Task ID | Проверенные входы | Завершение | Verdict | Ссылка на полный ответ |
|---|---|---|---|---|---|
| {{name}} | {{actual id}} | {{hashes}} | {{completed/failed/timed_out}} | {{PASS/REWORK/BLOCKED/N/A}} | {{section}} |
## Проверки
| Check ID | Условие | Результат | Evidence |
|---|---|---|---|
| {{id}} | {{check}} | {{pass/fail/blocked/not_run/N/A}} | {{file:line / hash}} |
## Findings
| ID | Severity | File:line | BR/SYS/AC/TC | Факт | Последствие | Исправление | Owner | Disposition |
|---|---|---|---|---|---|---|---|---|
| {{id}} | {{critical/major/minor/info}} | {{source}} | {{IDs}} | {{fact}} | {{impact}} | {{fix}} | {{owner}} | {{open/fixed/nonblocking}} |
## Непроверенное и блокеры
{{Что невозможно подтвердить; никакого PASS по отсутствующему ответу.}}
## Полные ответы сабагентов
{{Ответ каждого по шаблону subagent-result; не заменять вымышленным резюме.}}
## Вердикт и маршрут
{{ready / needs_rework / upstream_change / blocked; причина и target. Это не human approve.}}
```

### Шаблон `test-model` — Тестовая модель

```markdown
# Тестовая модель

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Scope, риски и границы e2e
{{Capabilities, must-have SYS/AC, real system boundary, риски, исключения.}}
## Матрица рисков
| Risk | Impact | Likelihood | BR/SYS/AC | Verification layer/channel | TC |
|---|---|---|---|---|---|
| {{risk}} | {{impact}} | {{likelihood}} | {{IDs}} | {{layer/channel}} | {{IDs}} |
## Карточки тестов
### {{TC-ID}} — {{цель}}
SYS/AC/SCN: {{IDs}}; Priority: {{must/should/could}}; Required: {{yes/no}}
Layer/channel: {{e2e + ui/api/cli/events либо иной честный слой}}
Preconditions/roles/fixtures: {{isolated seed / actor / environment}}
Steps: {{action → observable expected outcome}}
Oracle: {{из принятого требования, не текущей реализации}}
Cleanup: {{только own fixtures}}; Mock policy: {{core real; согласованные third-party doubles}}
Automation/selector: {{planned до авторинга, exact native selector после}}
Evidence: {{native report / browser trace / API outcome и т.п.}}
## Negative, boundary и recovery
{{Validation, denial/tenant, retries/concurrency, persistence, failure states по риску.}}
## Политика выхода
{{Все required TC выполнены; не 0 tests; no skip/flaky/blocker; hashes актуальны.}}
## Исключения и неприменимость
{{Причина, источник и принятый scope; recovery not_run не маскировать как PASS.}}
## Трассировка и нерешённое
{{BR → AC → SYS/NFR → SCN → TC; orphan IDs запрещены.}}
```

### Шаблон `test-model-json` — Машинная тестовая модель

В recover это inventory/model: выполнение not_run. exit_policy описывает будущую доставку и НЕ позволяет объявить baseline e2e-pass.

Каркас файла (значения заменить фактическими; полный контракт элементов массивов — в схеме):
```json
{
  "schema_version": 1,
  "document_revision": "{{DOCUMENT_REVISION}}",
  "run_id": "{{RUN_ID}}",
  "flow": "{{FLOW}}",
  "step_id": "{{STEP_ID}}",
  "attempt": 1,
  "stage": "{{STAGE}}",
  "status": "blocked",
  "source_refs": [],
  "change_id": "{{CHANGE_ID}}",
  "scope_requirements": [],
  "cases": [],
  "exclusions": [],
  "exit_policy": {
    "all_required_pass": true,
    "allow_zero_tests": false,
    "allow_required_skip": false,
    "allow_required_flaky": false,
    "blocking_defects_allowed": false,
    "require_ui_for_ui_scope": true,
    "require_fresh_fingerprints": true
  },
  "risk_matrix": [],
  "coverage": {
    "required": 1,
    "mapped": 1,
    "unmapped_ids": [],
    "calculation": "{{CALCULATION}}"
  }
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"change_id":{"type":"string"},"scope_requirements":{"type":"array","items":{"type":"string"},"minItems":0},"cases":{"type":"array","items":{"$ref":"#/$defs/test_case"},"minItems":0},"exclusions":{"type":"array","items":{"type":"object","properties":{"aspect":{"type":"string"},"reason":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"decision_ref":{"type":"string"}},"required":["aspect","reason","requirement_ids","decision_ref"],"additionalProperties":false},"minItems":0},"exit_policy":{"type":"object","properties":{"all_required_pass":{"const":true},"allow_zero_tests":{"const":false},"allow_required_skip":{"const":false},"allow_required_flaky":{"const":false},"blocking_defects_allowed":{"const":false},"require_ui_for_ui_scope":{"const":true},"require_fresh_fingerprints":{"const":true}},"required":["all_required_pass","allow_zero_tests","allow_required_skip","allow_required_flaky","blocking_defects_allowed","require_ui_for_ui_scope","require_fresh_fingerprints"],"additionalProperties":false},"risk_matrix":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"impact":{"type":"string"},"likelihood":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["id","impact","likelihood","requirement_ids","test_ids"],"additionalProperties":false},"minItems":0},"coverage":{"type":"object","properties":{"required":{"type":"integer","minimum":0},"mapped":{"type":"integer","minimum":0},"unmapped_ids":{"type":"array","items":{"type":"string"},"minItems":0},"calculation":{"type":"string"}},"required":["required","mapped","unmapped_ids","calculation"],"additionalProperties":false}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","change_id","scope_requirements","cases","exclusions","exit_policy","risk_matrix","coverage"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:test-model-json","title":"Машинная тестовая модель","$defs":{"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"test_case":{"type":"object","properties":{"id":{"type":"string"},"rationale":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"acceptance_ids":{"type":"array","items":{"type":"string"},"minItems":0},"scenario_id":{"type":"string"},"priority":{"type":"string","enum":["must","should","could"]},"required":{"type":"boolean"},"layer":{"type":"string","enum":["unit","component","contract","integration","e2e","inspection","analysis"]},"channel":{"type":"string","enum":["ui","api","cli","events","data","other"]},"preconditions":{"type":"array","items":{"type":"string"},"minItems":0},"roles":{"type":"array","items":{"type":"string"},"minItems":0},"fixture_data":{"type":"array","items":{"type":"string"},"minItems":0},"steps":{"type":"array","items":{"type":"object","properties":{"number":{"type":"integer","minimum":1},"action":{"type":"string"},"expected":{"type":"string"}},"required":["number","action","expected"],"additionalProperties":false},"minItems":0},"oracle":{"type":"string"},"cleanup":{"type":"string"},"environment":{"type":"string"},"automation":{"type":"string","enum":["planned","automated","manual","not_applicable"]},"mock_policy":{"type":"string"},"selector":{"type":["string","null"]},"evidence_requirements":{"type":"array","items":{"type":"string"},"minItems":0},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","rationale","requirement_ids","acceptance_ids","scenario_id","priority","required","layer","channel","preconditions","roles","fixture_data","steps","oracle","cleanup","environment","automation","mock_policy","selector","evidence_requirements","source_refs"],"additionalProperties":false}}}
```

### Шаблон `traceability` — Матрица трассировки

UTF-8, RFC4180 quoting, 13 столбцов. Ровно одна metadata-строка: только первые два поля. Одна mapping-строка на связь; пустой ADR допустим с N/A в SRS. На моделировании planned/not_run; при приёмке only actual pass/fail/blocked/not_run. Coverage считает только mapping, не metadata.

```csv
row_kind,document_revision,br_id,ac_id,sys_id,adr_id,scenario_id,test_id,layer,channel,selector,status,evidence_ref
metadata,{{REVISION}},,,,,,,,,,,
mapping,{{REVISION}},{{BR_ID}},{{AC_ID}},{{SYS_OR_NFR_ID}},{{ADR_ID_OR_EMPTY}},{{SCN_ID}},{{TC_ID}},{{LAYER}},{{CHANNEL}},{{SELECTOR_OR_PLANNED}},{{STATUS}},{{EVIDENCE_OR_EMPTY}}
```

## Основания и границы адаптации
- [S15] Cucumber: Gherkin reference: https://cucumber.io/docs/gherkin/reference/
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
