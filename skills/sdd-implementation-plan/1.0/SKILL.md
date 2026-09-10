---
name: sdd-implementation-plan
description: Делит требования на вертикальные проверяемые шаги с файлами, тестами
  и зависимостями.
---

# План реализации по принятому пакету

## Цель
Создать tasks.md + implementation-plan.json только после действующих business, architecture и SRS/model approvals.
## План
Для TASK-ID: linked SYS/AC/TC, concrete files/modules, dependencies, work type, definition of done, unit/integration check, e2e impact, migration/compatibility risk. Делай небольшие вертикальные slices, учитывай frontend+backend+data+auth и негативные сценарии. Отдельно запланируй local test harness, fixtures и stable UI semantics, если они отсутствуют. Не меняй stack ради удобства агента. В план входят только scope accepted; отсутствующее решение — возврат вверх.

Команды verification должны завершаться: build/lint/unit/integration/e2e runner. Долгоживущий backend/frontend запускается управляемо внутри test runner/webServer или wrapper с readiness, timeout и teardown. Не считать `npm run dev` успешной проверкой. Для test runtime зафиксируй base URL, required env NAMES, binary/tool versions и ограничения, без секретов.
## Выход
implementation-plan.json: task_ids, tasks[], dependency_graph, file_allowlist, verification_commands[{argv/cmd,cwd,timeout,expected_exit,scope}], test_environment_plan, acceptance_hashes. Все tasks сначала pending; unchecked обязательная задача блокирует финальную приёмку. Runtime-generated files/.qwen исключаются из product diff audit, но не от произвольной записи.

## Объединённая нода
Отдельных f11-plan/b06-plan больше нет. Навык первым выполняется внутри f12-code/b07-code: сначала полный план в 51-code, потом код. До первой product mutation paths/template_id/DoD конкретны; в последующих попытках repair не превращается в смену принятого scope. E2E остаётся последующим отдельным авторингом, ревью и исполнением.

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
      "path": "51-code/tasks.md",
      "resolved_path": "51-code/tasks.md",
      "required": true,
      "condition": "always",
      "template_id": "tasks",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b07-code",
        "f12-code"
      ],
      "scope": "run",
      "path": "51-code/implementation-plan.json",
      "resolved_path": "51-code/implementation-plan.json",
      "required": true,
      "condition": "always",
      "template_id": "implementation-plan",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b07-code",
        "f12-code"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/51-code/tasks.md",
      "resolved_path": "docs/sdd/changes/<run.id>/51-code/tasks.md",
      "required": true,
      "condition": "always",
      "template_id": "tasks",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b07-code",
        "f12-code"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/51-code/implementation-plan.json",
      "resolved_path": "docs/sdd/changes/<run.id>/51-code/implementation-plan.json",
      "required": true,
      "condition": "always",
      "template_id": "implementation-plan",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "implementation-plan.json: tasks[].files[].path",
      "scope": "project",
      "when": "before any planned code/test creation",
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

### Шаблон `implementation-plan` — Машинный план реализации

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
  "task_ids": [],
  "tasks": [],
  "dependency_graph": [],
  "file_allowlist": [],
  "verification_commands": [],
  "test_environment_plan": {
    "base_urls": [],
    "env_names": [],
    "tool_versions": [],
    "readiness": "{{READINESS}}",
    "lifecycle": "{{LIFECYCLE}}",
    "fixtures": "{{FIXTURES}}",
    "teardown": "{{TEARDOWN}}",
    "restrictions": []
  },
  "acceptance_hashes": [],
  "gate_receipts": [],
  "planned_before_source_change": false,
  "previous_plan_sha256": null
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"task_ids":{"type":"array","items":{"type":"string"},"minItems":0},"tasks":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"title":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"acceptance_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"operation":{"type":"string","enum":["create","modify","delete"]},"template_id":{"type":"string"},"purpose":{"type":"string"}},"required":["path","operation","template_id","purpose"],"additionalProperties":false},"minItems":0},"dependencies":{"type":"array","items":{"type":"string"},"minItems":0},"work_type":{"type":"string"},"definition_of_done":{"type":"string"},"verification_command_ids":{"type":"array","items":{"type":"string"},"minItems":0},"risks":{"type":"array","items":{"type":"string"},"minItems":0},"status":{"type":"string","enum":["pending","in_progress","done","blocked"]}},"required":["id","title","requirement_ids","acceptance_ids","test_ids","files","dependencies","work_type","definition_of_done","verification_command_ids","risks","status"],"additionalProperties":false},"minItems":0},"dependency_graph":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"}},"required":["from","to"],"additionalProperties":false},"minItems":0},"file_allowlist":{"type":"array","items":{"type":"string"},"minItems":0},"verification_commands":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"cmd":{"type":"string"},"cwd":{"type":"string"},"timeout_seconds":{"type":"integer","minimum":1},"expected_exit":{"type":"integer","minimum":0},"scope":{"type":"string"},"required":{"type":"boolean"}},"required":["id","cmd","cwd","timeout_seconds","expected_exit","scope","required"],"additionalProperties":false},"minItems":0},"test_environment_plan":{"type":"object","properties":{"base_urls":{"type":"array","items":{"type":"string"},"minItems":0},"env_names":{"type":"array","items":{"type":"string"},"minItems":0},"tool_versions":{"type":"array","items":{"type":"string"},"minItems":0},"readiness":{"type":"string"},"lifecycle":{"type":"string"},"fixtures":{"type":"string"},"teardown":{"type":"string"},"restrictions":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["base_urls","env_names","tool_versions","readiness","lifecycle","fixtures","teardown","restrictions"],"additionalProperties":false},"acceptance_hashes":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"gate_receipts":{"type":"array","items":{"$ref":"#/$defs/gate_receipt"},"minItems":0},"planned_before_source_change":{"type":"boolean"},"previous_plan_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","task_ids","tasks","dependency_graph","file_allowlist","verification_commands","test_environment_plan","acceptance_hashes","gate_receipts","planned_before_source_change","previous_plan_sha256"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:implementation-plan","title":"Машинный план реализации","$defs":{"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"gate_receipt":{"type":"object","properties":{"run_id":{"type":"string"},"gate_id":{"type":"string"},"gate_attempt":{"type":"integer","minimum":1},"decision":{"type":"string","enum":["approve","rework","missing"]},"route":{"type":"string"},"packet_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"comment":{"type":"string"},"approver":{"type":["string","null"]},"decided_at":{"type":["string","null"]},"runtime_audit_ref":{"type":["string","null"]},"valid":{"type":"boolean"},"invalidated_by":{"type":["string","null"]}},"required":["run_id","gate_id","gate_attempt","decision","route","packet_sha256","comment","approver","decided_at","runtime_audit_ref","valid","invalidated_by"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
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

### Шаблон `tasks` — План вертикальных шагов

В объединённой code-ноде полный план записывается ДО первой мутации product source. После выполнения статус TASK синхронизируется с implementation.json; план не переписывает accepted oracle.

```markdown
# План вертикальных шагов

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Принятые входы
{{Gate receipts и hashes PRD/architecture/SRS/model либо defect contract.}}
## TASK-карточки
### {{TASK-ID}} — {{вертикальный результат}}
Status: {{pending/in_progress/done/blocked}}
SYS/AC/TC: {{IDs}}
Dependencies: {{TASK IDs либо none}}
Files: {{точные project-relative пути; create/modify/delete}}
Template: {{native-code/native-test/existing file style; почему}}
Definition of done: {{проверяемый результат}}
Verification: {{cmd, cwd, timeout, expected exit, evidence}}
Risks: {{migration/compatibility/security}}
## Среда и harness
{{Безопасные URLs, env NAMES, readiness, start/stop/cleanup owned resources; не npm run dev как проверка.}}
## Allowlist и порядок
{{Files, companion files с rationale, DAG; не менять stack без принятого решения.}}
## Повторная попытка
{{Только repair в принятом scope; old/new plan hashes; новый scope требует upstream gate.}}
```

## Основания и границы адаптации
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
