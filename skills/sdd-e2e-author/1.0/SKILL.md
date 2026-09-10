---
name: sdd-e2e-author
description: Преобразует принятую модель в исполняемые UI/API/CLI/event тесты, не
  подменяя e2e unit тестами.
---

# Автор реальных сквозных тестов

## Цель
Написать исполняемые тестовые файлы, fixture/harness/config, runnable selectors и e2e-author.md/json. Тестовая модель задаёт expected behavior, текущий код — только способ взаимодействия.
## Выбор стека
Сохрани уже используемый browser/API/CLI framework. Для нового web harness допустим Playwright в TS/JS (или установленный проектом язык), даже если backend Java/Go/Python; это решение заранее отражено в architecture/plan. Для API-only используй native HTTP runner с реальной системой и data dependencies; component test с mock DB — не substitute e2e. Для CLI запускай бинарь/subprocess, проверяй exit/stdout/stderr и observable side effects. Для events проверяй producer→broker→consumer→external outcome с bounded polling, unique correlation IDs и cleanup.

Подними/используй утверждённую изолированную среду. Обследуй реальные routes/DOM/ARIA и API schemas; для UI вызови обязательный skill sdd-ui-playwright. Наличие MCP не предполагай; установленный browser runner может получать DOM/screenshot/trace и выполнять тесты. Необходимая UI проверка без доступного браузера => blocked, не переход к API-only.

Напиши позитивные, отрицательные и граничные TC из модели. Fixtures независимы, seed детерминированный, IDs уникальны на run/worker; не зависит от порядка. Пользовательское действие проверяй пользовательским результатом; API setup допустим, но не должен выполнять за UI сам проверяемый action. Приложи реальные assertions, а не только screenshot/click/HTTP 200. Core business path не mock; third-party double явно отражён в принятой модели.

Для каждого TC запиши file и точный runner selector в test-bindings.json, включая связку AC/SYS. Gherkin файл без step implementation/native mapping остаётся specification, не test. Изменение oracle/приоритетов/skip требует возврата к модели и gate. Не правь production code в этой ноде: обнаруженный дефект идёт через triage/code.
## Exit
Тесты реально discoverable, config разбирается, selectors уникальны, тесты не .only/.skip, нет placeholder assert(true). Проверка discover/compile не означает passed e2e; status authored. Сохрани перечень тестовых файлов/хэшей/команд и environment assumptions.


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
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "run",
      "path": "60-e2e-author/e2e-author.md",
      "resolved_path": "60-e2e-author/e2e-author.md",
      "required": true,
      "condition": "always",
      "template_id": "e2e-author",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "run",
      "path": "60-e2e-author/e2e-author.json",
      "resolved_path": "60-e2e-author/e2e-author.json",
      "required": true,
      "condition": "always",
      "template_id": "e2e-author-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "run",
      "path": "60-e2e-author/test-bindings.json",
      "resolved_path": "60-e2e-author/test-bindings.json",
      "required": true,
      "condition": "always",
      "template_id": "test-bindings",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/60-e2e-author/e2e-author.md",
      "resolved_path": "docs/sdd/changes/<run.id>/60-e2e-author/e2e-author.md",
      "required": true,
      "condition": "always",
      "template_id": "e2e-author",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/60-e2e-author/e2e-author.json",
      "resolved_path": "docs/sdd/changes/<run.id>/60-e2e-author/e2e-author.json",
      "required": true,
      "condition": "always",
      "template_id": "e2e-author-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/60-e2e-author/test-bindings.json",
      "resolved_path": "docs/sdd/changes/<run.id>/60-e2e-author/test-bindings.json",
      "required": true,
      "condition": "always",
      "template_id": "test-bindings",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "e2e-author.json: test_files[].path + harness_files[].path; test-bindings.json: bindings[].file",
      "scope": "project",
      "when": "declare concrete paths before creating native tests/config/fixtures",
      "template_ids": [
        "native-test"
      ],
      "nodes": [
        "f14-e2e-author",
        "b09-e2e-author"
      ]
    }
  ]
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `e2e-author` — Авторинг сквозных тестов

```markdown
# Авторинг сквозных тестов

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Принятая тестовая модель
{{Hash модели, SYS/AC/TC и неизменный oracle.}}
## Реализация по каналам
{{UI/API/CLI/events; настоящая внешняя граница, согласованные doubles.}}
## Тестовые файлы и selectors
| TC | File | Native selector | SYS/AC | Channel | Hash |
|---|---|---|---|---|---|
| {{TC-ID}} | {{project-relative}} | {{exact selector}} | {{IDs}} | {{channel}} | {{sha256}} |
## Fixtures, среда и cleanup
{{Изоляция run/worker, deterministic seed, auth env names, readiness и teardown.}}
## Проверка discover/compile
{{Команды, real reports, counts; это не passed e2e.}}
## UI observation
{{ui-observations.md; N/A с доказательством для non-UI.}}
## Ограничения
{{Authored / blocked; обязательные TC не пропускать.}}
```

### Шаблон `e2e-author-json` — Машинный результат авторинга e2e

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
  "model_sha256": null,
  "bindings_sha256": null,
  "source_fingerprint": {
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
  "channels": [],
  "test_files": [],
  "harness_files": [],
  "commands": [],
  "discovery": {
    "expected_required": 1,
    "discovered_required": 1,
    "missing_test_ids": [],
    "duplicate_selectors": [],
    "evidence_refs": []
  },
  "oracle_unchanged": false,
  "ui_observations_ref": {
    "scope": "run",
    "path": "{{PATH}}",
    "node_id": null,
    "attempt": null,
    "sha256": null,
    "purpose": "{{PURPOSE}}"
  },
  "raw_evidence": [],
  "execution_status": "not_run",
  "blockers": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["authored","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"model_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"bindings_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"source_fingerprint":{"$ref":"#/$defs/fingerprint"},"test_fingerprint":{"$ref":"#/$defs/fingerprint"},"channels":{"type":"array","items":{"type":"string"},"minItems":0},"test_files":{"type":"array","items":{"$ref":"#/$defs/mutation"},"minItems":0},"harness_files":{"type":"array","items":{"$ref":"#/$defs/mutation"},"minItems":0},"commands":{"type":"array","items":{"$ref":"#/$defs/command"},"minItems":0},"discovery":{"type":"object","properties":{"expected_required":{"type":"integer","minimum":0},"discovered_required":{"type":"integer","minimum":0},"missing_test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"duplicate_selectors":{"type":"array","items":{"type":"string"},"minItems":0},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0}},"required":["expected_required","discovered_required","missing_test_ids","duplicate_selectors","evidence_refs"],"additionalProperties":false},"oracle_unchanged":{"type":"boolean"},"ui_observations_ref":{"$ref":"#/$defs/file_ref"},"raw_evidence":{"type":"array","items":{"$ref":"#/$defs/evidence_item"},"minItems":0},"execution_status":{"type":"string","enum":["not_run"]},"blockers":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","model_sha256","bindings_sha256","source_fingerprint","test_fingerprint","channels","test_files","harness_files","commands","discovery","oracle_unchanged","ui_observations_ref","raw_evidence","execution_status","blockers"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:e2e-author-json","title":"Машинный результат авторинга e2e","$defs":{"command":{"type":"object","properties":{"id":{"type":"string"},"cmd":{"type":"string","description":"Точная выполненная команда, без значений секретов."},"cwd":{"type":"string","description":"Фактический рабочий каталог"},"timeout_seconds":{"type":"integer","minimum":1},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"exit_code":{"type":["integer","null"],"minimum":-65535},"timed_out":{"type":"boolean"},"stdout":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"stderr":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"native_reports":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"result":{"type":"string","enum":["pass","fail","blocked","not_run"]},"tool_versions":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"version":{"type":"string"}},"required":["name","version"],"additionalProperties":false},"minItems":0}},"required":["id","cmd","cwd","timeout_seconds","started_at","finished_at","exit_code","timed_out","stdout","stderr","native_reports","result","tool_versions"],"additionalProperties":false},"evidence_item":{"type":"object","properties":{"id":{"type":"string"},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"command_id":{"type":"string"},"kind":{"type":"string","enum":["native_json","junit_xml","stdout","stderr","trace","screenshot","video","other"]},"path":{"type":"string","description":"Конкретный путь в RUN; не glob."},"scope":{"type":"string","enum":["run"]},"original_source_path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"media_type":{"type":"string"},"bytes":{"type":"integer","minimum":0},"producer":{"type":"string"},"producer_version":{"type":"string"},"created_at":{"type":["string","null"]},"redaction":{"type":"string","enum":["none","sanitized_derivative","restricted_original"]},"access_policy":{"type":"string"},"retention":{"type":"string"},"validated":{"type":"boolean"},"validation_notes":{"type":"string"}},"required":["id","test_ids","command_id","kind","path","scope","original_source_path","sha256","media_type","bytes","producer","producer_version","created_at","redaction","access_policy","retention","validated","validation_notes"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"mutation":{"type":"object","properties":{"path":{"type":"string","description":"Точный project-relative путь, без glob"},"operation":{"type":"string","enum":["create","modify","delete"]},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"task_ids":{"type":"array","items":{"type":"string"},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"template_id":{"type":"string","description":"Для новой программы: native-code; для теста: native-test; для canonical docs: template_id из принятого плана."},"reason":{"type":"string"}},"required":["path","operation","before_sha256","after_sha256","task_ids","requirement_ids","template_id","reason"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
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

### Шаблон `test-bindings` — Привязка TC к исполняемым тестам

Один test_id может иметь несколько browser projects, но tuple runner/project/selector уникален. Required TC без binding запрещает authored/ready. Hash test file и oracle фактические.

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
  "model_sha256": null,
  "bindings": [],
  "unbound_required_ids": [],
  "duplicate_selectors": [],
  "discovery_commands": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"model_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"bindings":{"type":"array","items":{"$ref":"#/$defs/binding"},"minItems":0},"unbound_required_ids":{"type":"array","items":{"type":"string"},"minItems":0},"duplicate_selectors":{"type":"array","items":{"type":"string"},"minItems":0},"discovery_commands":{"type":"array","items":{"$ref":"#/$defs/command"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","model_sha256","bindings","unbound_required_ids","duplicate_selectors","discovery_commands"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:test-bindings","title":"Привязка TC к исполняемым тестам","$defs":{"binding":{"type":"object","properties":{"test_id":{"type":"string"},"acceptance_ids":{"type":"array","items":{"type":"string"},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"scenario_id":{"type":"string"},"file":{"type":"string","description":"Реальный project-relative test file"},"file_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"runner":{"type":"string"},"runner_version":{"type":"string"},"selector":{"type":"string"},"channel":{"type":"string","enum":["ui","api","cli","events","data","other"]},"required":{"type":"boolean"},"project_or_suite":{"type":"string"},"oracle_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"discovery_evidence":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]}},"required":["test_id","acceptance_ids","requirement_ids","scenario_id","file","file_sha256","runner","runner_version","selector","channel","required","project_or_suite","oracle_sha256","discovery_evidence"],"additionalProperties":false},"command":{"type":"object","properties":{"id":{"type":"string"},"cmd":{"type":"string","description":"Точная выполненная команда, без значений секретов."},"cwd":{"type":"string","description":"Фактический рабочий каталог"},"timeout_seconds":{"type":"integer","minimum":1},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"exit_code":{"type":["integer","null"],"minimum":-65535},"timed_out":{"type":"boolean"},"stdout":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"stderr":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"native_reports":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"result":{"type":"string","enum":["pass","fail","blocked","not_run"]},"tool_versions":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"version":{"type":"string"}},"required":["name","version"],"additionalProperties":false},"minItems":0}},"required":["id","cmd","cwd","timeout_seconds","started_at","finished_at","exit_code","timed_out","stdout","stderr","native_reports","result","tool_versions"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S15] Cucumber: Gherkin reference: https://cucumber.io/docs/gherkin/reference/
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
