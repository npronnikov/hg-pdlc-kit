---
name: sdd-acceptance-pack
description: 'Собирает проверяемый результат для ВП: scope, работающий outcome, покрытие
  и свежие доказательства.'
---

# Пакет финальной приёмки

## Цель
acceptance.md, acceptance.json, baseline-plan.json и traceability.csv. Пакет делает человеку видимыми все значимые решения и результат выполнения; не создаёт approval.
## Проверки
Вызови evidence-auditor по native reports, accepted docs и source/test fingerprints. Не доверяй summary исполнителя без report. Все обязательные TC есть, прошли, связаны с AC/SYS; no missing/skipped/flaky/blocking. Code, test and spec hashes совпадают с последним полноценным run; любые последующие изменения исходников/тестов возвращают на verification, а requirements — upstream.

Собери компактный executive summary «что обещано → что сделано → как доказано», demo reproduction steps безопасной среды, coverage matrix, screenshots/traces links для UI, applied scope, limitations и незатронутые NFR. Человек видит точный список файлов/ревизий/хэшей. В run acceptance.md включи содержательные выдержки BR/architecture/SRS и таблицу TC, не только непрозрачные ссылки.

Подготовь точный canonical documentation update plan, но ещё не применяй. baseline-plan.json: registry_before_sha256, source_revision, approved_candidate_files[{path,sha256}], canonical_updates[{target_path,before_sha256|null,candidate_path,after_sha256,operation}], authoritative_map, conflicts. Обновляй только затронутые capabilities; сохраняй незатронутую нормативную часть. Для OpenSpec sync delta в existing canonical specs, не перенос в parallel docs. Для удаления — tombstone/history. Canonical target content должен быть полностью подготовлен до final gate; seal не сочиняет новый текст.

acceptance.json: kind(delivery|baseline), candidate_packet_hashes, gate_receipts, traceability, test_evidence, pending_blockers, canonical_plan_sha256, verdict=ready_for_human. Recovery baseline не притворяется прошедшей доставкой: execution kind=baseline_inventory, tests status unknown/not_run, принятие касается точности документации.
## Exit
Delivery: только verified pass. Baseline: все factual claims traced, неизвестные явно исключены из подтверждённого знания; baseline gate допускает зафиксированный долг, но не «всё протестировано». Final human approval принимается только отдельной нодой.

## Шаблоны canonical targets
Каждый baseline-plan canonical_update указывает точный project-relative target_path, format, template_id, template_origin (точный файл/hash источника шаблона либо null для встроенного шаблона), prepared content path и before/after hashes. Новый registry имеет шаблон registry; docs/sdd/README.md — canonical-readme; product glossary — canonical-glossary. PRD/architecture/SRS/model используют одноимённые шаблоны набора. Existing OpenSpec/иной SDD — exact existing-native structure/validator с source origin; не заменять его общей формой. Для формата, которого нет в текущем knowledge context, прочитай соответствующий template из принятого upstream документа/источника; если он не определён, blocked, а не content.txt неизвестной структуры.

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
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/acceptance.md",
      "resolved_path": "70-acceptance/acceptance.md",
      "required": true,
      "condition": "always",
      "template_id": "acceptance",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/acceptance.json",
      "resolved_path": "70-acceptance/acceptance.json",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/baseline-plan.json",
      "resolved_path": "70-acceptance/baseline-plan.json",
      "required": true,
      "condition": "always",
      "template_id": "baseline-plan",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/traceability.csv",
      "resolved_path": "70-acceptance/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/acceptance.md",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/acceptance.md",
      "required": true,
      "condition": "always",
      "template_id": "acceptance",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/acceptance.json",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/acceptance.json",
      "required": true,
      "condition": "always",
      "template_id": "acceptance-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/baseline-plan.json",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/baseline-plan.json",
      "required": true,
      "condition": "always",
      "template_id": "baseline-plan",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/traceability.csv",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/traceability.csv",
      "required": true,
      "condition": "always",
      "template_id": "traceability",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/canonical-candidates/*/content.txt",
      "resolved_path": "70-acceptance/canonical-candidates/<safe-slot-id>/content.txt",
      "required": false,
      "condition": "when_canonical_update_planned",
      "template_id": "canonical-content",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b13-acceptance-pack",
        "f18-acceptance-pack",
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/canonical-candidates/*/content.txt",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/canonical-candidates/<safe-slot-id>/content.txt",
      "required": false,
      "condition": "when_canonical_update_planned",
      "template_id": "canonical-content",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "baseline-plan.json: canonical_updates[].target_path",
      "scope": "project",
      "when": "prepare only, materialize later after human gate",
      "template_ids": [
        "canonical-content",
        "registry",
        "canonical-readme",
        "canonical-glossary"
      ],
      "nodes": [
        "f18-acceptance-pack",
        "b13-acceptance-pack",
        "r08-baseline-pack"
      ]
    }
  ]
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `acceptance` — Пакет человеческой приёмки

```markdown
# Пакет человеческой приёмки

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Что обещано → что сделано → как доказано
{{Executive summary без ложного approval; kind delivery либо baseline.}}
## Принятый scope и изменения
{{Содержательные выдержки BR/architecture/SRS; added/modified/removed.}}
## Матрица приёмки
| BR/AC/SYS | Обещанный outcome | TC/Selector | Факт / статус | Evidence / hash |
|---|---|---|---|---|
| {{IDs}} | {{expected}} | {{TC}} | {{actual/not_run for baseline}} | {{refs}} |
## Демонстрация
{{Безопасные шаги ВП, test-only адрес, роли без секретов; UI evidence.}}
## Ограничения и незатронутые области
{{Unknown NFR, source coverage, excluded cases; каждый risk явен.}}
## Документационный patch
{{Точные canonical targets, before/after hashes, content slots; всё содержание подготовлено ДО gate.}}
## Независимый evidence audit
{{Task ID, полный завершённый ответ аудитора по шаблону subagent-result; родитель дождался.}}
## Решение человека
{{Рекомендация ready_for_human, approve происходит только в следующей runtime gate.}}
```

### Шаблон `acceptance-json` — Машинный пакет приёмки

kind=delivery: ready_for_human только с проверенным passed. kind=baseline: unknown/not_run, factual claims traceable, не delivery pass. Исключить manifest/acceptance self hash из candidate_packet_hashes; packet hash — hash manifest из gate audit.

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
  "candidate_packet_hashes": [],
  "gate_receipts": [],
  "traceability": {
    "scope": "run",
    "path": "{{PATH}}",
    "node_id": null,
    "attempt": null,
    "sha256": null,
    "purpose": "{{PURPOSE}}"
  },
  "test_evidence": [],
  "inventory_test_status": "not_run",
  "pending_blockers": [],
  "canonical_plan_sha256": null,
  "invoked_subagents": [],
  "limitations": [],
  "verdict": "blocked"
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"kind":{"type":"string","enum":["delivery","baseline"]},"candidate_packet_hashes":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"gate_receipts":{"type":"array","items":{"$ref":"#/$defs/gate_receipt"},"minItems":0},"traceability":{"$ref":"#/$defs/file_ref"},"test_evidence":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"inventory_test_status":{"type":"string","enum":["passed","unknown","not_run"]},"pending_blockers":{"type":"array","items":{"type":"string"},"minItems":0},"canonical_plan_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"invoked_subagents":{"type":"array","items":{"$ref":"#/$defs/subagent"},"minItems":0},"limitations":{"type":"array","items":{"type":"string"},"minItems":0},"verdict":{"type":"string","enum":["ready_for_human","needs_rework","blocked"]}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","kind","candidate_packet_hashes","gate_receipts","traceability","test_evidence","inventory_test_status","pending_blockers","canonical_plan_sha256","invoked_subagents","limitations","verdict"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:acceptance-json","title":"Машинный пакет приёмки","$defs":{"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"gate_receipt":{"type":"object","properties":{"run_id":{"type":"string"},"gate_id":{"type":"string"},"gate_attempt":{"type":"integer","minimum":1},"decision":{"type":"string","enum":["approve","rework","missing"]},"route":{"type":"string"},"packet_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"comment":{"type":"string"},"approver":{"type":["string","null"]},"decided_at":{"type":["string","null"]},"runtime_audit_ref":{"type":["string","null"]},"valid":{"type":"boolean"},"invalidated_by":{"type":["string","null"]}},"required":["run_id","gate_id","gate_attempt","decision","route","packet_sha256","comment","approver","decided_at","runtime_audit_ref","valid","invalidated_by"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"subagent":{"type":"object","properties":{"name":{"type":"string"},"task_id":{"type":["string","null"]},"invocation_status":{"type":"string","enum":["completed","failed","timed_out","unavailable"]},"input_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"verdict":{"type":"string","enum":["PASS","REWORK","BLOCKED","NOT_APPLICABLE"]},"result_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"result_location":{"type":"string","description":"Путь к секции выходного документа родителя или runtime transcript; сабагент файлов не создаёт."},"diff_unchanged":{"type":"boolean"},"blocker_reason":{"type":["string","null"]}},"required":["name","task_id","invocation_status","input_refs","started_at","finished_at","verdict","result_sha256","result_location","diff_unchanged","blocker_reason"],"additionalProperties":false}}}
```

### Шаблон `baseline-plan` — Точный план канонической фиксации

Каждому canonical_update нужен существующий content.txt и template_id выбранного формата; bytes target == bytes candidate. Registry update последний. Пустые updates допустимы только при no_op с evidence. Candidate не подменять после human gate.

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
  "registry_before_sha256": null,
  "source_revision": "{{SOURCE_REVISION}}",
  "approved_candidate_files": [],
  "canonical_updates": [],
  "authoritative_map": [],
  "conflicts": [],
  "no_op": false,
  "no_op_evidence": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"registry_before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"source_revision":{"type":"string"},"approved_candidate_files":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"canonical_updates":{"type":"array","items":{"$ref":"#/$defs/canonical_update"},"minItems":0},"authoritative_map":{"type":"array","items":{"type":"object","properties":{"capability_id":{"type":"string"},"kind":{"type":"string"},"target_path":{"type":"string"},"existing_sdd":{"type":["string","null"]}},"required":["capability_id","kind","target_path","existing_sdd"],"additionalProperties":false},"minItems":0},"conflicts":{"type":"array","items":{"$ref":"#/$defs/finding"},"minItems":0},"no_op":{"type":"boolean"},"no_op_evidence":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","registry_before_sha256","source_revision","approved_candidate_files","canonical_updates","authoritative_map","conflicts","no_op","no_op_evidence"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:baseline-plan","title":"Точный план канонической фиксации","$defs":{"canonical_update":{"type":"object","properties":{"target_path":{"type":"string","description":"Точный путь от корня проекта; без .., абсолютных путей и glob."},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"candidate_path":{"type":"string","description":"RUN путь 70-acceptance/canonical-candidates/<slot>/content.txt"},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"operation":{"type":"string","enum":["create","replace","tombstone"]},"format":{"type":"string"},"template_id":{"type":"string","description":"Выбранный шаблон содержимого: prd, architecture, srs, test-model, registry, canonical-readme, canonical-glossary или existing-native."},"validation_command":{"type":["string","null"]},"template_origin":{"anyOf":[{"$ref":"#/$defs/file_ref"},{"type":"null"}]},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["target_path","before_sha256","candidate_path","after_sha256","operation","format","template_id","validation_command","template_origin","requirement_ids"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"finding":{"type":"object","properties":{"id":{"type":"string"},"severity":{"type":"string","enum":["critical","major","minor","info"]},"source":{"$ref":"#/$defs/source_ref"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"issue":{"type":"string"},"impact":{"type":"string"},"required_fix":{"type":"string"},"owner":{"type":"string"},"disposition":{"type":"string","enum":["open","fixed","accepted_nonblocking","not_applicable"]},"resolution_evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","severity","source","requirement_ids","test_ids","issue","impact","required_fix","owner","disposition","resolution_evidence"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

### Шаблон `canonical-content` — Подготовленное содержимое canonical файла

```text
Transport: RUN и очищенный PROJECT 70-acceptance/canonical-candidates/<safe-slot-id>/content.txt.
Шаблон payload: baseline-plan.canonical_updates[].template_id обязателен; выбрать prd / business-requirements / architecture / decisions / srs / system-requirements / test-model / test-model-json / traceability / registry / canonical-readme / canonical-glossary / existing-native.
Для шаблона набора: применить его полную структуру. Для existing-native: точный target_path существующего нормативного файла и его подтверждённая структура/validator, сохранять незатронутые секции; добавить template_origin в описании validation_command/plan references.
Bytes: полный будущий target, не описание diff и не Markdown-обёртка. Расширение .txt — только транспорт, format задаёт целевой parser.
До final gate: все target_paths, formats, before/after hashes, source/target template, полный content и validator result известны; слот один к одному с update.
После gate: только byte-for-byte CAS materialization, никаких новых фраз/ADR/регистров. Пустые candidates допустимы только для доказанного no-op без updates.
```

### Шаблон `canonical-glossary` — Глоссарий продукта

```markdown
# Глоссарий продукта

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Термины
| Термин | Определение | Capability | Источник / Owner | Связанные ID |
|---|---|---|---|---|
| {{term}} | {{confirmed meaning}} | {{CAP-ID}} | {{source/owner}} | {{BR/SYS}} |
## Конфликты и синонимы
{{Не исправлять бизнес-смысл самостоятельно; unresolved и source.}}
```

### Шаблон `canonical-readme` — Навигация по спецификациям продукта

```markdown
# Навигация по спецификациям продукта

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Нормативные источники
{{docs/sdd/registry.json; existing OpenSpec/иной SDD остаётся authoritative по capability.}}
## Продукт и бизнес-требования
{{Точные пути по capability, owner и версии; не создавать вторую истину.}}
## Архитектура и системные требования
{{C4/ADR/SRS/contracts; связность по IDs.}}
## Тестовая модель и доказательства
{{Модели отдельно от native tests; accepted change snapshots с проверенными evidence.}}
## Изменения и правила актуализации
{{Только через accepted baseline-plan; actual run snapshot, no auto deploy.}}
```

### Шаблон `registry` — Реестр канонических знаний

PROJECT target docs/sdd/registry.json через принятый baseline-plan. Не хранить self hash registry; registry не хеширует seal receipt, чтобы избежать цикла registry↔receipt.

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
  "capabilities": [],
  "history": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"capabilities":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"authoritative_documents":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string"},"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"version":{"type":"string"},"existing_sdd":{"type":["string","null"]}},"required":["kind","path","sha256","version","existing_sdd"],"additionalProperties":false},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_model_path":{"type":["string","null"]},"accepted_change_ref":{"type":"string"},"known_gaps":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["id","name","authoritative_documents","requirement_ids","test_model_path","accepted_change_ref","known_gaps"],"additionalProperties":false},"minItems":0},"history":{"type":"array","items":{"type":"object","properties":{"change_id":{"type":"string"},"kind":{"type":"string","enum":["delivery","baseline"]},"packet_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"gate_audit_ref":{"type":["string","null"]},"changed_capabilities":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["change_id","kind","packet_sha256","gate_audit_ref","changed_capabilities"],"additionalProperties":false},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","capabilities","history"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:registry","title":"Реестр канонических знаний","$defs":{"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

### Шаблон `traceability` — Матрица трассировки

UTF-8, RFC4180 quoting, 13 столбцов. Ровно одна metadata-строка: только первые два поля. Одна mapping-строка на связь; пустой ADR допустим с N/A в SRS. На моделировании planned/not_run; при приёмке only actual pass/fail/blocked/not_run. Coverage считает только mapping, не metadata.

```csv
row_kind,document_revision,br_id,ac_id,sys_id,adr_id,scenario_id,test_id,layer,channel,selector,status,evidence_ref
metadata,{{REVISION}},,,,,,,,,,,
mapping,{{REVISION}},{{BR_ID}},{{AC_ID}},{{SYS_OR_NFR_ID}},{{ADR_ID_OR_EMPTY}},{{SCN_ID}},{{TC_ID}},{{LAYER}},{{CHANNEL}},{{SELECTOR_OR_PLANNED}},{{STATUS}},{{EVIDENCE_OR_EMPTY}}
```

## Основания и границы адаптации
- [S04] HGSDLC: artifacts: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/artifacts/spec.md
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
