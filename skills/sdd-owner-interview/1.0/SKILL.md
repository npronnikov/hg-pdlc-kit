---
name: sdd-owner-interview
description: Формирует адресные вопросы, сохраняет ответы и возвращается к неразрешённым
  критическим пробелам.
---

# Интервью владельца продукта

## Цель
Дать человеку отредактировать interview.md в human_input. ВП определяет смысл и приоритеты; агент не заполняет ответы за него.
## Workflow
Из context отдели известное от требующего решения. По каждой затронутой capability покрой проблему/ценность, метрики, пользователи/роли/права, границы, ключевые и альтернативные journeys, бизнес-правила и таблицы решений, данные/владение/сроки, ошибки и восстановление, зависимости, объёмы/задержки, privacy/security/a11y/localization, совместимость, критерии приёмки и неприемлемые исходы. Не заставляй ВП придумывать техническую реализацию: технические предложения агент оформит позже, бизнес-ограничения подтверждаются сейчас.

Задавай адаптивные раунды; первая партия 5–12 важных вопросов, остальные по необходимости. Это размер раунда, не потолок полноты. Для каждого Q-ID укажи источник неопределённости, почему ответ влияет на решение, варианты с trade-offs (не навязанный default), поле [Answer]:, критичность и owner. Вопросы уже отвеченные не повторяй; сохрани ссылку на прежний ответ и спрашивай только о противоречии/изменении. Открытое «не знаю» — valid answer, но blocker по must-have поведению; неприменимость требует причины.

Вопросы среды спрашивают тип/адрес безопасного стенда и имена env-переменных, не пароль или токен. Один RUN interview.md содержит предыдущие подтверждённые ответы + новые вопросы; размер до 48 КиБ, иначе выпусти очередной раунд и индекс предыдущих ответов.
## Шаблон interview.md
# Интервью ВП
Revision / run / stage / mode
## Подтверждённые факты и границы
## Раунд N
### Q-001 — ...
Источник: file:line / исходный запрос. Влияние: ...
Варианты: A ...; B ...; X свой ответ.
[Answer]:
Статус: unanswered / answered / not-applicable / deferred. Owner: ...
## Проверка полноты
Таблица: область | ответ/источник | unknown | blocker | кто решает.
## Решения человека
Только дословные ответы либо явно помеченный пересказ со ссылкой Q-ID.
## Выход
interview.md; interview-state.json с Q-ID, dependencies, open_blockers, rounds и ссылками на human attempts. Submit означает «ответы отправлены», не «PRD утверждён». На неполные ответы writer выбирает rework к discover/interview, не пишет одобренный PRD.

## Human input и наследование шаблона
AI-предшественник создаёт конкретный RUN 00-context/interview.md по этому шаблону. Human_input не запускает skills: редактирует тот же файл и сохраняет разделы/Q-ID. Таблица контрактов явно включает f02/b02/r02 и помечает writer=human_input. Архивирование полученного ответа выполняют бизнес-/reproduce-skills по answers-record, не повторное придумывание вопросов.

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
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "run",
      "path": "00-context/interview.md",
      "resolved_path": "00-context/interview.md",
      "required": true,
      "condition": "always",
      "template_id": "interview",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "run",
      "path": "00-context/interview-state.json",
      "resolved_path": "00-context/interview-state.json",
      "required": true,
      "condition": "always",
      "template_id": "interview-state",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/00-context/interview.md",
      "resolved_path": "docs/sdd/changes/<run.id>/00-context/interview.md",
      "required": true,
      "condition": "always",
      "template_id": "interview",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/00-context/interview-state.json",
      "resolved_path": "docs/sdd/changes/<run.id>/00-context/interview-state.json",
      "required": true,
      "condition": "always",
      "template_id": "interview-state",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b02-interview",
        "f02-interview",
        "r02-interview"
      ],
      "scope": "run",
      "path": "00-context/interview.md",
      "resolved_path": "00-context/interview.md",
      "required": true,
      "condition": "always",
      "template_id": "interview",
      "writer": "human_input (upstream skill template)"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `interview` — Интервью владельца продукта

Human_input изменяет именно upstream RUN interview.md по этому шаблону. Не подключать skill_refs к human_input; полный шаблон материализует AI-предшественник.

```markdown
# Интервью владельца продукта

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Подтверждённые факты и границы
{{Только сведения с источником; предыдущие ответы не терять.}}
## Раунд {{N}}
### {{Q-ID}} — {{вопрос}}
Источник: {{file:line / запрос / противоречие}}
Влияние: {{какое решение зависит от ответа}}
Варианты: {{A + последствия; B + последствия; свой вариант}}
Критичность: {{blocking/nonblocking}}; Owner: {{роль}}
[Answer]: {{заполняет только человек; сохранённый ответ имеет ссылку на его attempt}}
Статус: {{unanswered/answered/not-applicable/deferred}}
## Проверка полноты
| Область | Q-ID / ответ / источник | Unknown | Blocker | Кто решает |
|---|---|---|---|---|
| {{область}} | {{source}} | {{yes/no}} | {{yes/no}} | {{owner}} |
## Решения человека
{{Дословные ответы либо помеченный пересказ со ссылкой; Submit не равен PRD approve.}}
```

### Шаблон `interview-state` — Состояние интервью

До human Submit новые вопросы unanswered; предыдущие human attempts переносить только с provenance, не присваивать текущему человеку выдуманный ответ.

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
  "round": 1,
  "questions": [],
  "open_blockers": [],
  "rounds": [],
  "preserved_answer_refs": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"round":{"type":"integer","minimum":1},"questions":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"text":{"type":"string"},"dependencies":{"type":"array","items":{"type":"string"},"minItems":0},"owner":{"type":"string"},"criticality":{"type":"string","enum":["blocking","nonblocking"]},"answer_status":{"type":"string","enum":["unanswered","answered","not_applicable","deferred"]},"answer_reference":{"type":["string","null"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","text","dependencies","owner","criticality","answer_status","answer_reference","source_refs"],"additionalProperties":false},"minItems":0},"open_blockers":{"type":"array","items":{"type":"string"},"minItems":0},"rounds":{"type":"array","items":{"type":"object","properties":{"round":{"type":"integer","minimum":1},"question_ids":{"type":"array","items":{"type":"string"},"minItems":0},"human_node":{"type":["string","null"]},"human_attempt":{"type":["integer","null"],"minimum":1},"human_document_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["round","question_ids","human_node","human_attempt","human_document_sha256"],"additionalProperties":false},"minItems":0},"preserved_answer_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","round","questions","open_blockers","rounds","preserved_answer_refs"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:interview-state","title":"Состояние интервью","$defs":{"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S01] HGSDLC: инструкция создания flow: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/agent/create-flow-instruction.md
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
