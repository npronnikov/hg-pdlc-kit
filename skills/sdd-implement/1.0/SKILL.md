---
name: sdd-implement
description: Пишет код в нативном стеке и подтверждает каждый slice unit/integration
  проверками.
---

# Реализация Qwen с коротким TDD-циклом

## Цель
Реализовать утверждённый implementation plan. Product code пишет Qwen, не reviewer.
## Работа
Сверь hashes approved inputs и исходный рабочий diff. Прочитай затронутые исходники, локальные conventions и соседние tests. Для поведения сначала зафиксируй failing unit/integration test, где применимо; отсутствие механизма red объясни, не фальсифицируй log. Реализуй минимальный slice, выполни native build/lint/typecheck/unit/integration, затем рефакторинг без смены поведения. Для Java используй существующие Gradle/Maven и тестовые библиотеки, Go — имеющиеся go tools, Python — runner проекта, JS/TS — lockfile/toolchain проекта.

Сохраняй совместимость интерфейсов, error handling, authn/authz на сервере, транзакции и idempotency; UI — все согласованные состояния, label/role/keyboard semantics. Не прячь ошибку empty catch, не ослабляй validations и не меняй expected result для зелёного теста. Не включай tests-only bypass в production API. Если requirement невозможно выполнить в принятой architecture — route upstream вместо скрытого решения.

implementation.md перечисляет task status, changed files и requirement IDs; implementation.json содержит before/after fingerprints, raw command evidence refs, unit/integration results, actual code diff, outstanding. Код/тесты материализуются в реальных source/test directories. README о том, что «код будет написан», не считается implementation. E2E ещё не пройдены — явно not_run, не «все тесты зелёные».
## Exit
Обязательные lower-level проверки успешны, все accepted tasks сделаны, нет scope drift. Допустимы только file_allowlist и обоснованные companion files; неожиданное изменение -> остановка/ревью.

## Порядок
В f12-code/b07-code этот skill запускается ТОЛЬКО после sdd-implementation-plan и записи обеих plan files. Сверь план с approved hashes, затем меняй production code. Верификационные output paths описаны здесь и в sdd-workspace-contract; дополнительные необъявленные отчёты не придумывать.

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
        "b07-code",
        "f12-code"
      ],
      "scope": "run",
      "path": "51-code/implementation.md",
      "resolved_path": "51-code/implementation.md",
      "required": true,
      "condition": "always",
      "template_id": "implementation",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b07-code",
        "f12-code"
      ],
      "scope": "run",
      "path": "51-code/implementation.json",
      "resolved_path": "51-code/implementation.json",
      "required": true,
      "condition": "always",
      "template_id": "implementation-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b07-code",
        "f12-code"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/51-code/implementation.md",
      "resolved_path": "docs/sdd/changes/<run.id>/51-code/implementation.md",
      "required": true,
      "condition": "always",
      "template_id": "implementation",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b07-code",
        "f12-code"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/51-code/implementation.json",
      "resolved_path": "docs/sdd/changes/<run.id>/51-code/implementation.json",
      "required": true,
      "condition": "always",
      "template_id": "implementation-json",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "implementation-plan.json: file_allowlist + tasks[].files[].path",
      "scope": "project",
      "when": "accepted task implementation",
      "template_ids": [
        "native-code",
        "native-test"
      ],
      "nodes": [
        "f12-code",
        "b07-code"
      ]
    }
  ]
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `implementation` — Результат реализации

```markdown
# Результат реализации

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Входной контракт и план
{{Approved hashes, plan before source changes, границы работы.}}
## Выполненные TASK
| TASK | SYS/AC | Состояние | Файлы | Проверка / evidence |
|---|---|---|---|---|
| {{TASK-ID}} | {{IDs}} | {{done/blocked}} | {{paths}} | {{command/report}} |
## Реальные изменения
{{Create/modify/delete, before/after hash, source/test fingerprints; нет посторонних files.}}
## Lower-level проверки
{{TDD RED когда выполнен → fix → build/lint/unit/integration; фактические exit и отчёты.}}
## E2E
{{not_run: e2e исполняются позже; authored != passed.}}
## Незавершённое и ограничения
{{Blockers, justified N/A, scope drift с возвратом вверх.}}
```

### Шаблон `implementation-json` — Машинный результат реализации

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
  "plan_sha256": null,
  "before_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "after_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "test_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "tasks": [],
  "commands": [],
  "unit_integration_results": [],
  "actual_code_diff": [],
  "outstanding": [],
  "e2e_status": "not_run",
  "raw_evidence": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"plan_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"before_fingerprint":{"$ref":"#/$defs/fingerprint"},"after_fingerprint":{"$ref":"#/$defs/fingerprint"},"test_fingerprint":{"$ref":"#/$defs/fingerprint"},"tasks":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"status":{"type":"string","enum":["pending","in_progress","done","blocked"]},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0}},"required":["id","status","requirement_ids","evidence_refs"],"additionalProperties":false},"minItems":0},"commands":{"type":"array","items":{"$ref":"#/$defs/command"},"minItems":0},"unit_integration_results":{"type":"array","items":{"$ref":"#/$defs/check"},"minItems":0},"actual_code_diff":{"type":"array","items":{"$ref":"#/$defs/mutation"},"minItems":0},"outstanding":{"type":"array","items":{"$ref":"#/$defs/unknown"},"minItems":0},"e2e_status":{"type":"string","enum":["not_run"]},"raw_evidence":{"type":"array","items":{"$ref":"#/$defs/evidence_item"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","plan_sha256","before_fingerprint","after_fingerprint","test_fingerprint","tasks","commands","unit_integration_results","actual_code_diff","outstanding","e2e_status","raw_evidence"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:implementation-json","title":"Машинный результат реализации","$defs":{"check":{"type":"object","properties":{"id":{"type":"string"},"description":{"type":"string"},"result":{"type":"string","enum":["pass","fail","blocked","not_run","not_applicable"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"reason":{"type":"string"}},"required":["id","description","result","evidence_refs","reason"],"additionalProperties":false},"command":{"type":"object","properties":{"id":{"type":"string"},"cmd":{"type":"string","description":"Точная выполненная команда, без значений секретов."},"cwd":{"type":"string","description":"Фактический рабочий каталог"},"timeout_seconds":{"type":"integer","minimum":1},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"exit_code":{"type":["integer","null"],"minimum":-65535},"timed_out":{"type":"boolean"},"stdout":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"stderr":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"native_reports":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"result":{"type":"string","enum":["pass","fail","blocked","not_run"]},"tool_versions":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"version":{"type":"string"}},"required":["name","version"],"additionalProperties":false},"minItems":0}},"required":["id","cmd","cwd","timeout_seconds","started_at","finished_at","exit_code","timed_out","stdout","stderr","native_reports","result","tool_versions"],"additionalProperties":false},"evidence_item":{"type":"object","properties":{"id":{"type":"string"},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"command_id":{"type":"string"},"kind":{"type":"string","enum":["native_json","junit_xml","stdout","stderr","trace","screenshot","video","other"]},"path":{"type":"string","description":"Конкретный путь в RUN; не glob."},"scope":{"type":"string","enum":["run"]},"original_source_path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"media_type":{"type":"string"},"bytes":{"type":"integer","minimum":0},"producer":{"type":"string"},"producer_version":{"type":"string"},"created_at":{"type":["string","null"]},"redaction":{"type":"string","enum":["none","sanitized_derivative","restricted_original"]},"access_policy":{"type":"string"},"retention":{"type":"string"},"validated":{"type":"boolean"},"validation_notes":{"type":"string"}},"required":["id","test_ids","command_id","kind","path","scope","original_source_path","sha256","media_type","bytes","producer","producer_version","created_at","redaction","access_policy","retention","validated","validation_notes"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"mutation":{"type":"object","properties":{"path":{"type":"string","description":"Точный project-relative путь, без glob"},"operation":{"type":"string","enum":["create","modify","delete"]},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"task_ids":{"type":"array","items":{"type":"string"},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"template_id":{"type":"string","description":"Для новой программы: native-code; для теста: native-test; для canonical docs: template_id из принятого плана."},"reason":{"type":"string"}},"required":["path","operation","before_sha256","after_sha256","task_ids","requirement_ids","template_id","reason"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"unknown":{"type":"object","properties":{"id":{"type":"string"},"question":{"type":"string"},"owner":{"type":"string"},"blocking":{"type":"boolean"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"resolution":{"type":["string","null"]}},"required":["id","question","owner","blocking","source_refs","resolution"],"additionalProperties":false}}}
```

### Шаблон `native-code` — Параметризованный шаблон production-кода

```text
Путь: implementation-plan.tasks[].files[].path — точный путь от корня проекта ДО записи; operation=create|modify|delete; template_id=native-code.
Template origin: существующий соседний файл/модуль того же типа и принятые проектом conventions. Не создавать выдуманное src/Feature.java для неизвестного проекта.
Структура новой единицы: штатный module/package/imports; публичный контракт по SYS/API; typed data/validation; бизнес-операция; authn/authz; observable errors; concurrency/idempotency/transactions по requirement; комментарии только для rationale; сопутствующие lower-level tests по template native-test.
Для существующего файла: сохранять style/public API/неизменённые области; patch только по task/SYS; никаких empty catch, hardcoded secrets, test bypass.
Проверка: компиляция/линт/типизация и unit/integration по native command plan; реально выполненные reports. Для delete: compatibility и references проверяются отдельно.
Учёт: implementation.json.actual_code_diff и manifest.mutations с before/after SHA-256, TASK/SYS, template_id и rationale. Glob expected_mutations — аудит, не разрешение менять всё.
Незапланированный новый companion file сначала добавляется в план с причиной; изменение approved scope/architecture возвращается на gate.
```

### Шаблон `native-test` — Параметризованный шаблон исполняемого теста

```text
Путь: implementation-plan file contract (для lower-level) либо e2e-author.test_files и test-bindings.file (для e2e), конкретный project-relative path ДО записи; template_id=native-test.
Native skeleton: imports/fixtures/setup → test title с TC/SYS/AC → Arrange уникальных isolated данных → Act через выбранную real system boundary → Assert observable oracle из accepted model → Cleanup в finally/teardown.
UI: реальная DOM/ARIA проверка, semantic locator, действие через browser, web-first assertions, persistence по scope; API setup не выполняет проверяемое UI действие.
API: запрос к настоящей app+data границе, статус + schema + бизнес-результат/побочный эффект и отрицательные права.
CLI: subprocess реального executable, bounded timeout, exit/stdout/stderr + observable state.
Events: real producer/broker/consumer boundary, correlation ID, bounded poll outcome, cleanup own messages/data.
Fixture/config: environment и toolchain только из принятого плана, readiness/start/stop, pinned reporter и browser versions, без .only/.skip/assert(true), фиксированных sleep и auto-accept visual snapshots.
Report binding: exact file hash + unique runner/project/selector → TC/AC/SYS. Authored/discovered не равно passed; результат фиксирует run-e2e.
Шаблон адаптируется к уже принятому стеку; для Playwright UI конкретный каркас есть в sdd-ui-playwright. Никаких placeholders в итоговом тесте.
```

## Основания и границы адаптации
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
