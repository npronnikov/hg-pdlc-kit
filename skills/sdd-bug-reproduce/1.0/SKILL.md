---
name: sdd-bug-reproduce
description: Отделяет баг от новой фичи и получает доказанный сбой до изменения production
  кода.
---

# Дефект: ожидаемое поведение и red-reproducer

## Цель
defect.md, reproduction.json и воспроизводящий test по подтверждённому expected behavior. Пока не исправлять production код.
## Работа
Сверь reported actual/expected, принятые BR/SYS/AC и ответы ВП. Если новое желаемое поведение отсутствует в согласованной базе, это scope decision: не выдавай feature за bug. Узкий defect flow допустим только при ограниченной поправке в существующую capability; новая бизнес-политика/контракт/архитектурная граница — blocker с рекомендацией полного feature flow.

Зафиксируй affected version, environment, inputs, role, preconditions, steps, expected from source, actual, frequency, impact, earliest observed, security/privacy scope. Создай минимальный red-reproducer на реальной внешней границе, где разумно; unit reproduction допустим как дополнительный diagnostic, но финальная regression имеет e2e. Запусти против исходного snapshot без product patch. Сохрани nonzero/failed native report и докажи, что падение от неверного поведения, а не синтаксиса/недоступной среды.

Если не воспроизводится: не изобретай root cause. Подготовь адресные вопросы и instrumentation proposal без destructive changes; human blocker. В крайнем environment-specific дефекте перечисли препятствие и разрешённые evidence; отсутствие red не превращается автоматически в принятие.
## Выход
reproduction.json: expected_refs, baseline_fingerprint, command_evidence, failing_selector, failure_reason, root_cause_hypothesis, classification, affected_paths, scope_eligibility. В defect contract затем явно фиксируются BR/architecture/SRS delta/no-impact и регрессионная test model, которые принимает человек до code.


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
        "b03-reproduce"
      ],
      "scope": "run",
      "path": "05-reproduction/defect.md",
      "resolved_path": "05-reproduction/defect.md",
      "required": true,
      "condition": "always",
      "template_id": "defect",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b03-reproduce"
      ],
      "scope": "run",
      "path": "05-reproduction/reproduction.json",
      "resolved_path": "05-reproduction/reproduction.json",
      "required": true,
      "condition": "always",
      "template_id": "reproduction",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b03-reproduce"
      ],
      "scope": "run",
      "path": "05-reproduction/answers-record.md",
      "resolved_path": "05-reproduction/answers-record.md",
      "required": true,
      "condition": "always",
      "template_id": "answers-record",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b03-reproduce"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/05-reproduction/defect.md",
      "resolved_path": "docs/sdd/changes/<run.id>/05-reproduction/defect.md",
      "required": true,
      "condition": "always",
      "template_id": "defect",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b03-reproduce"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/05-reproduction/reproduction.json",
      "resolved_path": "docs/sdd/changes/<run.id>/05-reproduction/reproduction.json",
      "required": true,
      "condition": "always",
      "template_id": "reproduction",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b03-reproduce"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/05-reproduction/answers-record.md",
      "resolved_path": "docs/sdd/changes/<run.id>/05-reproduction/answers-record.md",
      "required": true,
      "condition": "always",
      "template_id": "answers-record",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "reproduction.json: reproducer_files[].path (declare before creating)",
      "scope": "project",
      "when": "create a baseline red reproducer; product source unchanged",
      "template_ids": [
        "native-test"
      ],
      "nodes": [
        "b03-reproduce"
      ]
    }
  ]
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

### Шаблон `defect` — Паспорт дефекта

```markdown
# Паспорт дефекта

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Сообщение и ожидаемое поведение
{{Reported actual/expected, версия, источник expected BR/SYS/AC и ответы ВП.}}
## Влияние и scope eligibility
{{Severity, frequency, affected users/capabilities; это отклонение, не новая бизнес-политика.}}
## Среда и baseline
{{Commit, source fingerprint, безопасная среда, роли, inputs без секретов.}}
## Минимальное воспроизведение
{{Preconditions → точные шаги → observable expected → actual.}}
## Доказанный RED
{{Failing selector, команда, exit/report hashes; причина поведения, не syntax/env failure.}}
## Гипотеза причины
{{Evidence, alternatives; не выдавать гипотезу за факт.}}
## Ограничения и вопросы
{{Не воспроизведено / blocked / неизвестное; owner/action.}}
## План регрессии
{{Требования и e2e boundary; production пока не изменён.}}
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

### Шаблон `reproduction` — Воспроизведение дефекта

ready/on_success только при red_proven, eligible и unchanged baseline source. Nonzero из-за среды/синтаксиса не доказывает defect.

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
  "expected_refs": [],
  "baseline_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "command_evidence": [],
  "failing_selector": null,
  "failure_reason": "{{FAILURE_REASON}}",
  "root_cause_hypothesis": null,
  "classification": "unknown",
  "affected_paths": [],
  "scope_eligibility": {
    "eligible": false,
    "reason": "{{REASON}}",
    "canonical_expected_refs": []
  },
  "red_proven": false,
  "product_source_unchanged": false,
  "reproducer_files": [],
  "raw_evidence": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"expected_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"baseline_fingerprint":{"$ref":"#/$defs/fingerprint"},"command_evidence":{"type":"array","items":{"$ref":"#/$defs/command"},"minItems":0},"failing_selector":{"type":["string","null"]},"failure_reason":{"type":"string"},"root_cause_hypothesis":{"type":["string","null"]},"classification":{"type":"string","enum":["product_defect","test_defect","environment_blocker","scope_change","not_reproduced","unknown"]},"affected_paths":{"type":"array","items":{"type":"string"},"minItems":0},"scope_eligibility":{"type":"object","properties":{"eligible":{"type":"boolean"},"reason":{"type":"string"},"canonical_expected_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["eligible","reason","canonical_expected_refs"],"additionalProperties":false},"red_proven":{"type":"boolean"},"product_source_unchanged":{"type":"boolean"},"reproducer_files":{"type":"array","items":{"$ref":"#/$defs/mutation"},"minItems":0},"raw_evidence":{"type":"array","items":{"$ref":"#/$defs/evidence_item"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","expected_refs","baseline_fingerprint","command_evidence","failing_selector","failure_reason","root_cause_hypothesis","classification","affected_paths","scope_eligibility","red_proven","product_source_unchanged","reproducer_files","raw_evidence"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:reproduction","title":"Воспроизведение дефекта","$defs":{"command":{"type":"object","properties":{"id":{"type":"string"},"cmd":{"type":"string","description":"Точная выполненная команда, без значений секретов."},"cwd":{"type":"string","description":"Фактический рабочий каталог"},"timeout_seconds":{"type":"integer","minimum":1},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"exit_code":{"type":["integer","null"],"minimum":-65535},"timed_out":{"type":"boolean"},"stdout":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"stderr":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"native_reports":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"result":{"type":"string","enum":["pass","fail","blocked","not_run"]},"tool_versions":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"version":{"type":"string"}},"required":["name","version"],"additionalProperties":false},"minItems":0}},"required":["id","cmd","cwd","timeout_seconds","started_at","finished_at","exit_code","timed_out","stdout","stderr","native_reports","result","tool_versions"],"additionalProperties":false},"evidence_item":{"type":"object","properties":{"id":{"type":"string"},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"command_id":{"type":"string"},"kind":{"type":"string","enum":["native_json","junit_xml","stdout","stderr","trace","screenshot","video","other"]},"path":{"type":"string","description":"Конкретный путь в RUN; не glob."},"scope":{"type":"string","enum":["run"]},"original_source_path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"media_type":{"type":"string"},"bytes":{"type":"integer","minimum":0},"producer":{"type":"string"},"producer_version":{"type":"string"},"created_at":{"type":["string","null"]},"redaction":{"type":"string","enum":["none","sanitized_derivative","restricted_original"]},"access_policy":{"type":"string"},"retention":{"type":"string"},"validated":{"type":"boolean"},"validation_notes":{"type":"string"}},"required":["id","test_ids","command_id","kind","path","scope","original_source_path","sha256","media_type","bytes","producer","producer_version","created_at","redaction","access_policy","retention","validated","validation_notes"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"mutation":{"type":"object","properties":{"path":{"type":"string","description":"Точный project-relative путь, без glob"},"operation":{"type":"string","enum":["create","modify","delete"]},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"task_ids":{"type":"array","items":{"type":"string"},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"template_id":{"type":"string","description":"Для новой программы: native-code; для теста: native-test; для canonical docs: template_id из принятого плана."},"reason":{"type":"string"}},"required":["path","operation","before_sha256","after_sha256","task_ids","requirement_ids","template_id","reason"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
