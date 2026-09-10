---
name: sdd-business-prd
description: Превращает ответы ВП в проверяемый бизнес-контракт с правилами, scope
  и acceptance examples.
---

# Исчерпывающий BRD/PRD

## Цель
Создать prd.md и business-requirements.json по проверенному контексту и фактическим ответам human_input. Полнота означает отсутствие неразрешённых обязательных решений в принятом scope, а не предсказание любых будущих потребностей.
## Шаги
Сверь запрос, существующие specs и ответы. Выдели as-is/to-be, affected capabilities, changes added/modified/removed. Не превращай техническую гипотезу в бизнес-потребность. Для каждого требования обеспечь источник, rationale, priority, owner, acceptance, зависимости и исключения. Проведи ревью через business-auditor; покажи findings без самоодобрения.
## Обязательная структура prd.md
1. Паспорт: ID изменения, версия, статус draft, авторские источники, владельцы решений.
2. Проблема и текущее состояние: доказательства, последствия, почему нужно изменение.
3. Цели и метрики: baseline/target/window/measurement/guardrails; неизвестная цифра не выдумывается.
4. Стейкхолдеры, персоны и роли; владельцы бизнес-решений и границы полномочий.
5. In scope / out of scope; ограничения, зависимости, предположения.
6. Пользовательские journeys: триггер, предусловия, happy path, альтернативы, ошибки, postconditions.
7. BR-ID: атомарные бизнес-требования; RULE-ID: правила/decision tables, границы, исключения, приоритет конфликтующих правил.
8. Информация: сущности и бизнес-смысл, источники, качество, владение, жизненный цикл, удаление.
9. Взаимодействия: другие продукты/люди, уведомления, ответственность, отказы и восстановление.
10. Бизнес-ограничения качества: доступность/latency/объёмы/privacy/security/a11y/локаль; измеримые критерии или вопрос ВП.
11. AC-ID: observable Given/When/Then на happy/negative/boundary/permission cases, без привязки к внутреннему методу.
12. Риски, спорные вопросы и решения; unresolved must-have = запрет on_success.
13. Приёмочная матрица BR→RULE→AC→Q-ID; changelog и delta относительно baseline.

Для малого изменения раздел может содержать «не применимо: причина и источник», но не быть молча пропущен. Технические endpoint signatures, classes и выбор БД не подменяют бизнес-требования.
## business-requirements.json
schema_version, document_revision, change_id, capability_ids, goals[], requirements[{id,statement,rationale,source_refs,priority,owner,acceptance_ids,rule_ids,status}], rules[], acceptance[{id,given,when,then,negative,source_refs}], decisions[], unresolved[].
## Exit
ready только если каждый обязательный пункт либо раскрыт, либо обоснованно not-applicable; все существенные вопросы решены человеком, auditor не нашёл blocking gaps. Human gate всё равно обязателен. На архитектурной/кодовой стадии нельзя «уточнять» BR без возврата сюда и нового approval.


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
      "path": "10-defect-contract/prd.md",
      "resolved_path": "10-defect-contract/prd.md",
      "required": true,
      "condition": "always",
      "template_id": "prd",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/business-requirements.json",
      "resolved_path": "10-defect-contract/business-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "business-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contract-review.md",
      "resolved_path": "10-defect-contract/contract-review.md",
      "required": true,
      "condition": "always",
      "template_id": "contract-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/prd.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/prd.md",
      "required": true,
      "condition": "always",
      "template_id": "prd",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/business-requirements.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/business-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "business-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contract-review.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contract-review.md",
      "required": true,
      "condition": "always",
      "template_id": "contract-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "run",
      "path": "10-business/prd.md",
      "resolved_path": "10-business/prd.md",
      "required": true,
      "condition": "always",
      "template_id": "prd",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "run",
      "path": "10-business/business-requirements.json",
      "resolved_path": "10-business/business-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "business-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "run",
      "path": "10-business/answers-record.md",
      "resolved_path": "10-business/answers-record.md",
      "required": true,
      "condition": "always",
      "template_id": "answers-record",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "run",
      "path": "10-business/business-review.md",
      "resolved_path": "10-business/business-review.md",
      "required": true,
      "condition": "always",
      "template_id": "business-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-business/prd.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-business/prd.md",
      "required": true,
      "condition": "always",
      "template_id": "prd",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-business/business-requirements.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-business/business-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "business-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-business/answers-record.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-business/answers-record.md",
      "required": true,
      "condition": "always",
      "template_id": "answers-record",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f03-prd",
        "r03-business"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-business/business-review.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-business/business-review.md",
      "required": true,
      "condition": "always",
      "template_id": "business-review",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `answers-record` — Запись ответов ВП

Обёртка имеет собственную ревизию; дословное исходное тело сохраняется внутри. При rework сохранять все ранее полученные ответы и их human attempts; не выдумывать одобрение.

```markdown
# Запись ответов ВП

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Происхождение
Human node: {{реальный f02-interview / b02-interview / r02-interview}}
Human attempt: {{trusted runtime attempt либо null с причиной}}
Источник RUN: {{полный адрес полученного interview.md}}
Источник SHA-256: {{hash bytes исходного документа}}
## Дословный полученный документ
<!-- BEGIN VERBATIM INTERVIEW -->
{{Вставить исходный interview.md без изменения текста ответов. Не заменять пересказом.}}
<!-- END VERBATIM INTERVIEW -->
## Индекс ответов
| Q-ID | Ответ дан? | Ссылка на исходный раздел | Неопределённость | Влияние |
|---|---|---|---|---|
| {{Q-ID}} | {{yes/no/deferred}} | {{heading}} | {{unknown}} | {{BR/AC / scope}} |
## Интерпретация агента — не ответ человека
{{Явно отделённые выводы и новые вопросы; не менять исходный текст.}}
```

### Шаблон `business-requirements` — Бизнес-требования

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
  "capability_ids": [],
  "goals": [],
  "requirements": [],
  "rules": [],
  "acceptance": [],
  "decisions": [],
  "unresolved": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"change_id":{"type":"string"},"capability_ids":{"type":"array","items":{"type":"string"},"minItems":0},"goals":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"goal":{"type":"string"},"baseline":{"type":["string","null"]},"target":{"type":["string","null"]},"window":{"type":["string","null"]},"measurement":{"type":"string"},"guardrails":{"type":"array","items":{"type":"string"},"minItems":0},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","goal","baseline","target","window","measurement","guardrails","source_refs"],"additionalProperties":false},"minItems":0},"requirements":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"statement":{"type":"string"},"rationale":{"type":"string"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"priority":{"type":"string","enum":["must","should","could"]},"owner":{"type":"string"},"acceptance_ids":{"type":"array","items":{"type":"string"},"minItems":0},"rule_ids":{"type":"array","items":{"type":"string"},"minItems":0},"status":{"type":"string","enum":["candidate","reconstructed","removed"]}},"required":["id","statement","rationale","source_refs","priority","owner","acceptance_ids","rule_ids","status"],"additionalProperties":false},"minItems":0},"rules":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"statement":{"type":"string"},"decision_table":{"type":"array","items":{"type":"object","properties":{"conditions":{"type":"array","items":{"type":"string"},"minItems":0},"outcome":{"type":"string"},"exceptions":{"type":"array","items":{"type":"string"},"minItems":0},"priority":{"type":"integer","minimum":0}},"required":["conditions","outcome","exceptions","priority"],"additionalProperties":false},"minItems":0},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","statement","decision_table","source_refs"],"additionalProperties":false},"minItems":0},"acceptance":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"given":{"type":"string"},"when":{"type":"string"},"then":{"type":"string"},"negative":{"type":"boolean"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","given","when","then","negative","requirement_ids","source_refs"],"additionalProperties":false},"minItems":0},"decisions":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"decision":{"type":"string"},"owner":{"type":"string"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","decision","owner","source_refs"],"additionalProperties":false},"minItems":0},"unresolved":{"type":"array","items":{"$ref":"#/$defs/unknown"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","change_id","capability_ids","goals","requirements","rules","acceptance","decisions","unresolved"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:business-requirements","title":"Бизнес-требования","$defs":{"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"unknown":{"type":"object","properties":{"id":{"type":"string"},"question":{"type":"string"},"owner":{"type":"string"},"blocking":{"type":"boolean"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"resolution":{"type":["string","null"]}},"required":["id","question","owner","blocking","source_refs","resolution"],"additionalProperties":false}}}
```

### Шаблон `business-review` — Ревью бизнес-требований

```markdown
# Ревью бизнес-требований

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

### Шаблон `contract-review` — Ревью ограниченного дефектного контракта

```markdown
# Ревью ограниченного дефектного контракта

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

### Шаблон `prd` — BRD / PRD изменения

```markdown
# BRD / PRD изменения

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## 1. Паспорт и управление документом
{{Change ID, capability, draft/reconstructed, владельцы, baseline и delta added/modified/removed.}}
## 2. Проблема и as-is
{{Факты, evidence, ущерб/возможность; current != desired.}}
## 3. Цели и метрики
| Цель | Baseline | Target | Окно | Метод измерения | Guardrail | Источник |
|---|---|---|---|---|---|---|
| {{goal}} | {{known/unknown}} | {{confirmed/unknown}} | {{window}} | {{method}} | {{guardrail}} | {{Q-ID}} |
## 4. Стейкхолдеры, персоны, роли и права
{{Кто делает/принимает/видит; границы полномочий.}}
## 5. Scope и ограничения
{{In scope, out of scope, assumptions, dependencies; каждому N/A причина.}}
## 6. Пользовательские journeys
{{Для каждого: trigger, actor, preconditions, happy path, alternatives, errors, postconditions.}}
## 7. Бизнес-требования и правила
| BR-ID | Требование | Обоснование | Приоритет | Owner | RULE / AC | Q-ID / источник |
|---|---|---|---|---|---|---|
| {{BR-ID}} | {{атомарное поведение}} | {{why}} | {{must/should/could}} | {{owner}} | {{IDs}} | {{source}} |
### Таблицы решений RULE-ID
{{Условия, границы, исключения, результат, приоритет конфликтующих правил.}}
## 8. Данные как бизнес-понятия
{{Смысл, источники, качество, ownership, lifecycle, удаление.}}
## 9. Взаимодействия и отказы
{{Зависимые продукты/люди, уведомления, recovery, ответственность.}}
## 10. Ограничения качества
{{Измеримые latency/availability/volume/security/privacy/a11y/localization; неизвестные — вопросы.}}
## 11. Критерии приёмки
| AC-ID | Given | When | Then | Тип | BR / RULE / source |
|---|---|---|---|---|---|
| {{AC-ID}} | {{given}} | {{when}} | {{observable then}} | {{happy/negative/boundary/permission}} | {{IDs}} |
## 12. Риски и нерешённые вопросы
{{Owner, impact, blocking; must-have unresolved запрещает ready.}}
## 13. Трассировка и история
{{BR → RULE → AC → Q-ID; изменённые/удалённые ID не переиспользовать.}}
```

## Основания и границы адаптации
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S15] Cucumber: Gherkin reference: https://cucumber.io/docs/gherkin/reference/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
