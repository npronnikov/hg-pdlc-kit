---
name: sdd-discovery
description: Заземляет запрос в текущем коде, спецификациях, тестах и реальных возможностях
  инструментов.
---

# Анализ репозитория и готовности среды

## Цель
Сформировать context.json/repository-map.md до интервью, чтобы вопросы ВП опирались на продукт и код, а не были общей анкетой.
## Шаги
Определи границы выбранного репозитория, stack и native build/test tools: Java/Maven/Gradle, JS/TS, Go, Python либо иной найденный стек. Прочитай README, AGENTS/QWEN, продуктовые docs, OpenSpec/spec-kit/AI-DLC каталоги, ADR, API schema, migrations, frontend routes, authorization и тесты. Проверь не только имена файлов, но релевантное содержимое. При большой базе используй ограниченную карту и точечное чтение; repomix возможен лишь локально после исключения секретов и generated/vendor директорий, не обязателен.

Построй capability/component map с file:line evidence и repo commit/fingerprint. Разделяй documented, observed_in_code, observed_in_test, executed, inferred, unknown. Наличие теста не значит, что он проходит. Расхождение specs/code — явный конфликт, не автоматическое «истина в коде».

Проверь Qwen file tools, shell, subagent delegation, write access только в разрешённых местах; для UI — установленный browser-capable runner, доступность browser binaries и способ DOM inspection. MCP browser необязателен: настоящий Playwright runner через shell достаточен. Для API/CLI/events выбери реальную границу системы. Сохрани версии фактически доступных инструментов, не требуй перевести проект на новый стек.

Не запускай feature tests до согласования безопасной среды. Определи test-only endpoints, auth env variable names, fixture/cleanup strategy, команды readiness/teardown, сеть, ограничения. Если среда ещё не создана, это может быть согласованной задачей implementation plan; до реального запуска e2e она должна быть проверена.
## Формат
context.json: schema_version, mode(feature|recover|bugfix), feature_request, repo_root, commit, dirty_baseline, source_fingerprint, baseline_registry_sha256, canonical_path_map, affected_capabilities, stacks, entrypoints, existing_test_commands, ui_present, capability_checks, environment_questions, conflicts, unknowns, evidence[].
repository-map.md: границы; существующее поведение; продуктовые источники; компоненты; API/UI/data; тесты; риски; рекомендации по интервью. Никакой выдуманной абсолютной директории.
## Ограничения
Не менять product code. Отсутствующая база не блокирует полный feature flow сама по себе: ограниченно восстанови затронутую часть и вынеси неопределённости в интервью. Масштабная противоречивая база — рекомендация отдельного recover flow, без выдуманного автоматического вызова subflow.


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
      "path": "00-context/context.json",
      "resolved_path": "00-context/context.json",
      "required": true,
      "condition": "always",
      "template_id": "context",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "run",
      "path": "00-context/repository-map.md",
      "resolved_path": "00-context/repository-map.md",
      "required": true,
      "condition": "always",
      "template_id": "repository-map",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/00-context/context.json",
      "resolved_path": "docs/sdd/changes/<run.id>/00-context/context.json",
      "required": true,
      "condition": "always",
      "template_id": "context",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b01-discover",
        "f01-discover",
        "r01-discover"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/00-context/repository-map.md",
      "resolved_path": "docs/sdd/changes/<run.id>/00-context/repository-map.md",
      "required": true,
      "condition": "always",
      "template_id": "repository-map",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `context` — Контекст репозитория

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
  "mode": "feature",
  "feature_request": "{{FEATURE_REQUEST}}",
  "repo_root": "{{REPO_ROOT}}",
  "commit": null,
  "dirty_baseline": [],
  "source_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "baseline_registry_sha256": null,
  "canonical_path_map": [],
  "affected_capabilities": [],
  "stacks": [],
  "entrypoints": [],
  "existing_test_commands": [],
  "ui_present": false,
  "capability_checks": [],
  "environment_questions": [],
  "conflicts": [],
  "unknowns": [],
  "evidence": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"mode":{"type":"string","enum":["feature","bugfix","recover"]},"feature_request":{"type":"string"},"repo_root":{"type":"string"},"commit":{"type":["string","null"]},"dirty_baseline":{"type":"array","items":{"$ref":"#/$defs/mutation"},"minItems":0},"source_fingerprint":{"$ref":"#/$defs/fingerprint"},"baseline_registry_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"canonical_path_map":{"type":"array","items":{"type":"object","properties":{"capability_id":{"type":"string"},"kind":{"type":"string"},"path":{"type":"string"},"authoritative":{"type":"boolean"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["capability_id","kind","path","authoritative","source_refs"],"additionalProperties":false},"minItems":0},"affected_capabilities":{"type":"array","items":{"type":"string"},"minItems":0},"stacks":{"type":"array","items":{"type":"object","properties":{"language":{"type":"string"},"build_tool":{"type":"string"},"test_tool":{"type":"string"},"versions":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["language","build_tool","test_tool","versions"],"additionalProperties":false},"minItems":0},"entrypoints":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string"},"path":{"type":"string"},"purpose":{"type":"string"}},"required":["kind","path","purpose"],"additionalProperties":false},"minItems":0},"existing_test_commands":{"type":"array","items":{"type":"object","properties":{"cmd":{"type":"string"},"cwd":{"type":"string"},"layer":{"type":"string"},"status":{"type":"string","enum":["observed","executed","unknown"]}},"required":["cmd","cwd","layer","status"],"additionalProperties":false},"minItems":0},"ui_present":{"type":"boolean"},"capability_checks":{"type":"array","items":{"$ref":"#/$defs/check"},"minItems":0},"environment_questions":{"type":"array","items":{"type":"string"},"minItems":0},"conflicts":{"type":"array","items":{"$ref":"#/$defs/finding"},"minItems":0},"unknowns":{"type":"array","items":{"$ref":"#/$defs/unknown"},"minItems":0},"evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","mode","feature_request","repo_root","commit","dirty_baseline","source_fingerprint","baseline_registry_sha256","canonical_path_map","affected_capabilities","stacks","entrypoints","existing_test_commands","ui_present","capability_checks","environment_questions","conflicts","unknowns","evidence"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:context","title":"Контекст репозитория","$defs":{"check":{"type":"object","properties":{"id":{"type":"string"},"description":{"type":"string"},"result":{"type":"string","enum":["pass","fail","blocked","not_run","not_applicable"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"reason":{"type":"string"}},"required":["id","description","result","evidence_refs","reason"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"finding":{"type":"object","properties":{"id":{"type":"string"},"severity":{"type":"string","enum":["critical","major","minor","info"]},"source":{"$ref":"#/$defs/source_ref"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"issue":{"type":"string"},"impact":{"type":"string"},"required_fix":{"type":"string"},"owner":{"type":"string"},"disposition":{"type":"string","enum":["open","fixed","accepted_nonblocking","not_applicable"]},"resolution_evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","severity","source","requirement_ids","test_ids","issue","impact","required_fix","owner","disposition","resolution_evidence"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"mutation":{"type":"object","properties":{"path":{"type":"string","description":"Точный project-relative путь, без glob"},"operation":{"type":"string","enum":["create","modify","delete"]},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"task_ids":{"type":"array","items":{"type":"string"},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"template_id":{"type":"string","description":"Для новой программы: native-code; для теста: native-test; для canonical docs: template_id из принятого плана."},"reason":{"type":"string"}},"required":["path","operation","before_sha256","after_sha256","task_ids","requirement_ids","template_id","reason"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"unknown":{"type":"object","properties":{"id":{"type":"string"},"question":{"type":"string"},"owner":{"type":"string"},"blocking":{"type":"boolean"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"resolution":{"type":["string","null"]}},"required":["id","question","owner","blocking","source_refs","resolution"],"additionalProperties":false}}}
```

### Шаблон `repository-map` — Карта репозитория

```markdown
# Карта репозитория

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Границы обследования
{{Репозиторий, commit, включённые/исключённые области; coverage честно ограничить.}}
## Продуктовые источники и канонические пути
| Capability | Документ | Нормативный? | Версия / evidence | Конфликт |
|---|---|---|---|---|
| {{CAP-ID}} | {{repo-relative path}} | {{yes/no/unknown}} | {{file:line / hash}} | {{description}} |
## Компоненты и взаимодействия
{{Entrypoints → call chain → данные; UI/API/CLI/events; file:line.}}
## Существующее поведение
{{Documented / observed_in_code / observed_in_test / inferred / unknown отдельно.}}
## Тесты и среда
{{Runner, команды, selector inventory, реальный browser support; существование ≠ pass.}}
## Риски и противоречия
{{Specs ↔ code ↔ tests; безопасность, данные, технические ограничения.}}
## Вопросы интервью
{{Только адресные пробелы; Q-ID и влияние решения.}}
## Независимая проверка
{{Результат картографа и точный task_id; ссылки на полный возврат в index.md.}}
```

## Основания и границы адаптации
- [S02] HGSDLC: существующие flow: https://github.com/npronnikov/hgsdlc/tree/a92d294a0118edd35b803eca3429de5eed1fd078/docs/aidlc/flows
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
