---
name: sdd-test-review
description: Не даёт получить зелёный результат за счёт слабых assertions, пропуска
  UI или скрытых mocks.
---

# Ревью тестов и oracle

## Цель
test-review.md/json с reviewed_test_hash и verdict. Вызови оба объявленных сабагента: UI-test-auditor и spec-test-auditor. Для non-UI scope UI-test-auditor сам подтверждает NOT_APPLICABLE с обоснованием; дождись завершения обоих вызовов.
## Контроль
Сверь каждый accepted TC с actual selector/file; required tests discoverable, .only/.skip отсутствуют, не отключены ранее существовавшие tests. Oracle соответствует AC, не copied from implementation; assertion проверяет outcome, а не только navigation/200. Setup не выполняет проверяемое действие; core path проходит реальную систему; permissions/negative path действительно negative. Fixtures независимы, cleanup не трогает чужие данные. Flakiness risk: fixed waits, random uncontrolled data, clock/timezone assumptions, flaky external dependency. Для UI — реальный browser, semantic locators, assertions, persistence, states по scope.

Reviewer не пишет исправления и не запускает destructive tests. Findings c file:line, affected TC/SYS, severity and fix. Тестовая ошибка → e2e-author; требование/oracle нужно изменить → system/model gate; production fault → code. Должно быть невозможно «принять» невыполненный тест по красивому отчёту.


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
        "b10-test-review",
        "f15-test-review"
      ],
      "scope": "run",
      "path": "61-test-review/test-review.md",
      "resolved_path": "61-test-review/test-review.md",
      "required": true,
      "condition": "always",
      "template_id": "test-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b10-test-review",
        "f15-test-review"
      ],
      "scope": "run",
      "path": "61-test-review/test-review.json",
      "resolved_path": "61-test-review/test-review.json",
      "required": true,
      "condition": "always",
      "template_id": "test-review-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b10-test-review",
        "f15-test-review"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/61-test-review/test-review.md",
      "resolved_path": "docs/sdd/changes/<run.id>/61-test-review/test-review.md",
      "required": true,
      "condition": "always",
      "template_id": "test-review",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b10-test-review",
        "f15-test-review"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/61-test-review/test-review.json",
      "resolved_path": "docs/sdd/changes/<run.id>/61-test-review/test-review.json",
      "required": true,
      "condition": "always",
      "template_id": "test-review-json",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `test-review` — Ревью исполняемых тестов

```markdown
# Ревью исполняемых тестов

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

### Шаблон `test-review-json` — Машинное ревью тестов

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
  "checks": [],
  "findings": [],
  "reviewed_hashes": [],
  "invoked_subagents": [],
  "unresolved_blockers": [],
  "verdict": "blocked",
  "unverified": [],
  "reviewed_test_hash": null,
  "approved_oracle_hash": null,
  "bindings_sha256": null,
  "required_tests": [],
  "ui_scope": false,
  "ui_verdict": "blocked"
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"checks":{"type":"array","items":{"$ref":"#/$defs/check"},"minItems":0},"findings":{"type":"array","items":{"$ref":"#/$defs/finding"},"minItems":0},"reviewed_hashes":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"invoked_subagents":{"type":"array","items":{"$ref":"#/$defs/subagent"},"minItems":0},"unresolved_blockers":{"type":"array","items":{"type":"string"},"minItems":0},"verdict":{"type":"string","enum":["ready","needs_rework","upstream_change","blocked"]},"unverified":{"type":"array","items":{"type":"string"},"minItems":0},"reviewed_test_hash":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"approved_oracle_hash":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"bindings_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"required_tests":{"type":"array","items":{"type":"string"},"minItems":0},"ui_scope":{"type":"boolean"},"ui_verdict":{"type":"string","enum":["pass","fail","blocked","not_applicable"]}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","checks","findings","reviewed_hashes","invoked_subagents","unresolved_blockers","verdict","unverified","reviewed_test_hash","approved_oracle_hash","bindings_sha256","required_tests","ui_scope","ui_verdict"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:test-review-json","title":"Машинное ревью тестов","$defs":{"check":{"type":"object","properties":{"id":{"type":"string"},"description":{"type":"string"},"result":{"type":"string","enum":["pass","fail","blocked","not_run","not_applicable"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"reason":{"type":"string"}},"required":["id","description","result","evidence_refs","reason"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"finding":{"type":"object","properties":{"id":{"type":"string"},"severity":{"type":"string","enum":["critical","major","minor","info"]},"source":{"$ref":"#/$defs/source_ref"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"issue":{"type":"string"},"impact":{"type":"string"},"required_fix":{"type":"string"},"owner":{"type":"string"},"disposition":{"type":"string","enum":["open","fixed","accepted_nonblocking","not_applicable"]},"resolution_evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","severity","source","requirement_ids","test_ids","issue","impact","required_fix","owner","disposition","resolution_evidence"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"subagent":{"type":"object","properties":{"name":{"type":"string"},"task_id":{"type":["string","null"]},"invocation_status":{"type":"string","enum":["completed","failed","timed_out","unavailable"]},"input_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"verdict":{"type":"string","enum":["PASS","REWORK","BLOCKED","NOT_APPLICABLE"]},"result_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"result_location":{"type":"string","description":"Путь к секции выходного документа родителя или runtime transcript; сабагент файлов не создаёт."},"diff_unchanged":{"type":"boolean"},"blocker_reason":{"type":["string","null"]}},"required":["name","task_id","invocation_status","input_refs","started_at","finished_at","verdict","result_sha256","result_location","diff_unchanged","blocker_reason"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S17] Playwright: locators: https://playwright.dev/docs/locators
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
