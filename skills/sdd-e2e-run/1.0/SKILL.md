---
name: sdd-e2e-run
description: Запускает реальные команды, сопоставляет native reports с моделью и отделяет
  blocked/fail/flaky от pass.
---

# Исполнение e2e и сбор evidence

## Цель
Создать execution.md, execution.json, evidence-index.json и raw native reports в RUN. Не изменять production code или oracle.
## Исполнение
Сверь hashes source tree, lockfiles, test bindings, accepted SRS/model и test-review. Проверь только test env, правильную build revision, readiness/dependencies/auth env NAMES. Перед любыми seeds/cleanup убедись, что это изолированная среда и данные принадлежат текущему run. Нет доступа/браузера/сети/dependency => blocked с точной причиной. Это не fail продукта и не pass.

Выполни plan commands в их реальном cwd через shell. Сохрани точный argv/cmd, start/end, timeout, exit code, stdout/stderr paths/hash, tool/browser versions, source/tests/spec fingerprints, environment descriptor. Запускай build/lint/unit/integration регрессию по affected area и всю согласованную e2e suite. Не только новый один happy path. API/UI/CLI/events соответствуют утверждённой модели; если модель требует UI, browser project обязателен.

Парси native JSON/JUnit/test reports, не считай текст `All passed` доказательством. Map actual selectors к TC. Различай expected, discovered, executed, passed, failed, skipped, flaky, not_run. Каждый required TC обязан существовать в report и пройти на проверяемой revision; exit code=0 и нулевой test count не успех. Retry diagnosis разрешён ограниченно; pass только после исправления причины и нового чистого прогона. Не называть flaky pass обычным pass.

При падении сохрани first failure и минимальное воспроизведение; UI — trace/screenshot/DOM/network где допустимо; API — очищенный request/response; events — correlation trace. Ошибки нельзя swallow, `|| true` запрещено для критериев выхода. Не закрывай runner до фактического окончания и teardown; по timeout фиксируй timeout, не pass. Заверши только запущенные этим run процессы и очисти только свои fixtures.
## execution.json
schema_version, document_revision, run_id, kind=delivery, status, source_fingerprint, test_fingerprint, spec_fingerprint, environment, commands[], cases[{test_id,selector,result,attempts,native_report,evidence}], totals{expected,discovered,executed,passed,failed,skipped,flaky,not_run}, blockers[], defects[], started_at, finished_at. Источники timestamps — системные/runner, не придумывать.
## Exit
on_success только при satisfied exit_policy, полных native reports, всех required TC passed, нуле required skip/flaky и blocking defects. Failed product/test → triage. Blocked environment → human blocker. Человек не отменяет красный обязательный тест кликом approve: изменённый scope проходит upstream gates.


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
        "b11-run-e2e",
        "f16-run-e2e"
      ],
      "scope": "run",
      "path": "62-execution/execution.md",
      "resolved_path": "62-execution/execution.md",
      "required": true,
      "condition": "always",
      "template_id": "execution",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b11-run-e2e",
        "f16-run-e2e"
      ],
      "scope": "run",
      "path": "62-execution/execution.json",
      "resolved_path": "62-execution/execution.json",
      "required": true,
      "condition": "always",
      "template_id": "execution-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b11-run-e2e",
        "f16-run-e2e"
      ],
      "scope": "run",
      "path": "62-execution/evidence-index.json",
      "resolved_path": "62-execution/evidence-index.json",
      "required": true,
      "condition": "always",
      "template_id": "evidence-index",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b11-run-e2e",
        "f16-run-e2e"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/62-execution/execution.md",
      "resolved_path": "docs/sdd/changes/<run.id>/62-execution/execution.md",
      "required": true,
      "condition": "always",
      "template_id": "execution",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b11-run-e2e",
        "f16-run-e2e"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/62-execution/execution.json",
      "resolved_path": "docs/sdd/changes/<run.id>/62-execution/execution.json",
      "required": true,
      "condition": "always",
      "template_id": "execution-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b11-run-e2e",
        "f16-run-e2e"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/62-execution/evidence-index.json",
      "resolved_path": "docs/sdd/changes/<run.id>/62-execution/evidence-index.json",
      "required": true,
      "condition": "always",
      "template_id": "evidence-index",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `evidence-index` — Индекс фактических доказательств

Native files не создаются по JSON-примеру. Только bytes, реально произведённые tool. report.json — полная JSON структура выбранного reporter; JUnit XML парсится; trace/png/webm проверяются по format и tool provenance.

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
  "spec_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "items": [],
  "missing_required": [],
  "report_parsers": [],
  "access_policy": "{{ACCESS_POLICY}}",
  "retention_policy": "{{RETENTION_POLICY}}"
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"source_fingerprint":{"$ref":"#/$defs/fingerprint"},"test_fingerprint":{"$ref":"#/$defs/fingerprint"},"spec_fingerprint":{"$ref":"#/$defs/fingerprint"},"items":{"type":"array","items":{"$ref":"#/$defs/evidence_item"},"minItems":0},"missing_required":{"type":"array","items":{"type":"object","properties":{"test_id":{"type":"string"},"kind":{"type":"string"},"reason":{"type":"string"}},"required":["test_id","kind","reason"],"additionalProperties":false},"minItems":0},"report_parsers":{"type":"array","items":{"type":"object","properties":{"producer":{"type":"string"},"version":{"type":"string"},"format":{"type":"string"},"schema_or_parser_ref":{"type":"string"},"validation_result":{"type":"string","enum":["pass","fail","blocked"]}},"required":["producer","version","format","schema_or_parser_ref","validation_result"],"additionalProperties":false},"minItems":0},"access_policy":{"type":"string"},"retention_policy":{"type":"string"}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","source_fingerprint","test_fingerprint","spec_fingerprint","items","missing_required","report_parsers","access_policy","retention_policy"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:evidence-index","title":"Индекс фактических доказательств","$defs":{"evidence_item":{"type":"object","properties":{"id":{"type":"string"},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"command_id":{"type":"string"},"kind":{"type":"string","enum":["native_json","junit_xml","stdout","stderr","trace","screenshot","video","other"]},"path":{"type":"string","description":"Конкретный путь в RUN; не glob."},"scope":{"type":"string","enum":["run"]},"original_source_path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"media_type":{"type":"string"},"bytes":{"type":"integer","minimum":0},"producer":{"type":"string"},"producer_version":{"type":"string"},"created_at":{"type":["string","null"]},"redaction":{"type":"string","enum":["none","sanitized_derivative","restricted_original"]},"access_policy":{"type":"string"},"retention":{"type":"string"},"validated":{"type":"boolean"},"validation_notes":{"type":"string"}},"required":["id","test_ids","command_id","kind","path","scope","original_source_path","sha256","media_type","bytes","producer","producer_version","created_at","redaction","access_policy","retention","validated","validation_notes"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

### Шаблон `execution` — Результаты исполнения e2e

```markdown
# Результаты исполнения e2e

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Проверенная ревизия и входы
{{Source/test/spec fingerprints, accepted model, test-review, build/environment identity.}}
## Среда и команды
{{Test-only URL, runner/browser versions, cmd/cwd/timeout, real start/end, exit, teardown.}}
## Покрытие и результаты
| TC / Selector | Required | Channel | Result | Attempts | Native report | Evidence |
|---|---|---|---|---|---|---|
| {{TC-ID / selector}} | {{yes/no}} | {{UI/API/CLI/events}} | {{passed/failed/skipped/flaky/not_run/blocked}} | {{N}} | {{path/hash}} | {{refs}} |
## Сводные счётчики
{{Expected, discovered, executed, passed, failed, skipped, flaky, not_run; не путать с attempts.}}
## Ошибки и блокеры
{{First failure, observed vs expected, дефект продукта/теста/среды.}}
## Evidence и свежесть
{{evidence-index.json; реальные reports, UI traces/screenshots при необходимости; stale запрещён.}}
## Вердикт
{{Pass только при выполнении всей exit_policy; иначе triage или blocker.}}
```

### Шаблон `execution-json` — Машинный протокол исполнения

counts — по уникальным test_id/selector/project, не retries. Expected = обязательные bindings, report считается отдельно. passed требует expected>0, все required rows passed, 0 required skips/flaky/not_run, actual native report, current source/tests/specs, успешный teardown. Статус blocked cases включается в not_run count.

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
  "kind": "delivery",
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
  "spec_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "environment": {
    "name": "{{NAME}}",
    "base_urls": [],
    "build_revision": "{{BUILD_REVISION}}",
    "is_test_only": false,
    "isolation": "{{ISOLATION}}",
    "tool_versions": [],
    "browser_projects": []
  },
  "commands": [],
  "cases": [],
  "totals": {
    "expected": 1,
    "discovered": 1,
    "executed": 1,
    "passed": 1,
    "failed": 1,
    "skipped": 1,
    "flaky": 1,
    "not_run": 1
  },
  "blockers": [],
  "defects": [],
  "started_at": null,
  "finished_at": null,
  "teardown": {
    "id": "{{ID}}",
    "description": "{{DESCRIPTION}}",
    "result": "blocked",
    "evidence_refs": [],
    "reason": "{{REASON}}"
  }
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["passed","failed","flaky","blocked","not_run"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"kind":{"type":"string","enum":["delivery"]},"source_fingerprint":{"$ref":"#/$defs/fingerprint"},"test_fingerprint":{"$ref":"#/$defs/fingerprint"},"spec_fingerprint":{"$ref":"#/$defs/fingerprint"},"environment":{"type":"object","properties":{"name":{"type":"string"},"base_urls":{"type":"array","items":{"type":"string"},"minItems":0},"build_revision":{"type":"string"},"is_test_only":{"type":"boolean"},"isolation":{"type":"string"},"tool_versions":{"type":"array","items":{"type":"string"},"minItems":0},"browser_projects":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["name","base_urls","build_revision","is_test_only","isolation","tool_versions","browser_projects"],"additionalProperties":false},"commands":{"type":"array","items":{"$ref":"#/$defs/command"},"minItems":0},"cases":{"type":"array","items":{"type":"object","properties":{"test_id":{"type":"string"},"selector":{"type":"string"},"project_or_suite":{"type":"string"},"required":{"type":"boolean"},"result":{"type":"string","enum":["passed","failed","skipped","flaky","not_run","blocked"]},"attempts":{"type":"integer","minimum":0},"native_report":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"evidence":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"actual":{"type":"string"},"expected":{"type":"string"},"failure_reason":{"type":["string","null"]}},"required":["test_id","selector","project_or_suite","required","result","attempts","native_report","evidence","actual","expected","failure_reason"],"additionalProperties":false},"minItems":0},"totals":{"type":"object","properties":{"expected":{"type":"integer","minimum":0},"discovered":{"type":"integer","minimum":0},"executed":{"type":"integer","minimum":0},"passed":{"type":"integer","minimum":0},"failed":{"type":"integer","minimum":0},"skipped":{"type":"integer","minimum":0},"flaky":{"type":"integer","minimum":0},"not_run":{"type":"integer","minimum":0}},"required":["expected","discovered","executed","passed","failed","skipped","flaky","not_run"],"additionalProperties":false},"blockers":{"type":"array","items":{"type":"string"},"minItems":0},"defects":{"type":"array","items":{"$ref":"#/$defs/finding"},"minItems":0},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"teardown":{"$ref":"#/$defs/check"}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","kind","source_fingerprint","test_fingerprint","spec_fingerprint","environment","commands","cases","totals","blockers","defects","started_at","finished_at","teardown"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:execution-json","title":"Машинный протокол исполнения","$defs":{"check":{"type":"object","properties":{"id":{"type":"string"},"description":{"type":"string"},"result":{"type":"string","enum":["pass","fail","blocked","not_run","not_applicable"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"reason":{"type":"string"}},"required":["id","description","result","evidence_refs","reason"],"additionalProperties":false},"command":{"type":"object","properties":{"id":{"type":"string"},"cmd":{"type":"string","description":"Точная выполненная команда, без значений секретов."},"cwd":{"type":"string","description":"Фактический рабочий каталог"},"timeout_seconds":{"type":"integer","minimum":1},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"exit_code":{"type":["integer","null"],"minimum":-65535},"timed_out":{"type":"boolean"},"stdout":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"stderr":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"native_reports":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"result":{"type":"string","enum":["pass","fail","blocked","not_run"]},"tool_versions":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"version":{"type":"string"}},"required":["name","version"],"additionalProperties":false},"minItems":0}},"required":["id","cmd","cwd","timeout_seconds","started_at","finished_at","exit_code","timed_out","stdout","stderr","native_reports","result","tool_versions"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"finding":{"type":"object","properties":{"id":{"type":"string"},"severity":{"type":"string","enum":["critical","major","minor","info"]},"source":{"$ref":"#/$defs/source_ref"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"issue":{"type":"string"},"impact":{"type":"string"},"required_fix":{"type":"string"},"owner":{"type":"string"},"disposition":{"type":"string","enum":["open","fixed","accepted_nonblocking","not_applicable"]},"resolution_evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","severity","source","requirement_ids","test_ids","issue","impact","required_fix","owner","disposition","resolution_evidence"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver
- [S20] Playwright: authentication: https://playwright.dev/docs/auth

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
