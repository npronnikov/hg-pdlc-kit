---
name: sdd-seal-baseline
description: После реального approve применяет только подготовленный документационный
  patch и записывает receipt.
---

# Фиксация принятой базы в репозитории

## Цель
Завершить текущий scope после финальной человеческой приёмки; никаких push/PR/deploy. seal.md и seal.json — техническая фиксация, не новая фаза разработки.
## Предусловия
Instruction содержит trusted runtime gate: decision=approve, route=on_approve, gate attempt. Прочитай acceptance packet + baseline-plan и перепроверь exact hashes. Старый approval от другой attempt/revision не подходит. Проверь current source/tests/spec fingerprints и registry_before_sha256. При drift/concurrent change не трогай canonical docs и верни rework к acceptance verification или blocker; при изменённом product/test коде — повтор e2e.
## Операция
Применяй только prepared canonical_updates, byte-for-byte, с before/after checks; обнови registry как последний commit-point локальной materialization. Используй временные файлы и atomic replace в пределах FS; перед каждой заменой CAS before_sha256. Сохрани объявленные RUN 71-seal/journal.json и 71-seal/backups/<safe-slot-id>/content.txt только для собственных изменяемых docs. При частичном сбое откати только собственные замены при совпадении их after hash, иначе blocker; registry не должен указывать на частично подготовленную базу. Это файловый протокол, не распределённая транзакция и не замена host-level workspace isolation.

Добавь receipt текущей попытки в текущий CHANGE_ROOT/71-seal/seal.json (не изменяй принятый 70-acceptance packet): trusted gate fields, packet hash, runtime audit reference, materialized canonical hashes, source/tests/evidence fingerprints, documentation kind. Не выдумывай approver username/time: null, если runtime их не предоставил. Не переименовывай raw test report в green.

Обнови docs/sdd/README.md/registry навигацию и product glossary лишь в пределах уже принятого canonical plan; старые change snapshots остаются historical. После фиксации ещё раз проверь хэши неизменности source code/tests — после e2e они не должны меняться.
## Выход
seal.json содержит status=sealed, mode=delivery|baseline, receipt, canonical_updates_applied, fingerprints и final limitations. Если операция невозможна, не выдавай sealed. Runtime publish mode должен быть LOCAL (проверяется оператором при создании run, не выдуманным YAML ключом).

## Явные служебные выходы
Журнал — RUN 71-seal/journal.json, резервные bytes — RUN 71-seal/backups/<safe-slot-id>/content.txt. Их форматы ниже; в PROJECT не зеркалировать. Временный atomic file имеет только path/template из mutation_contracts и удаляется после операции. Canonical target names известны из принятого baseline-plan, seal новых целей и содержания не придумывает. Повторная attempt создаёт новый receipt, прошлую принятую RUN attempt не меняет.

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
        "b15-seal",
        "f20-seal",
        "r10-seal"
      ],
      "scope": "run",
      "path": "71-seal/seal.md",
      "resolved_path": "71-seal/seal.md",
      "required": true,
      "condition": "always",
      "template_id": "seal",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b15-seal",
        "f20-seal",
        "r10-seal"
      ],
      "scope": "run",
      "path": "71-seal/seal.json",
      "resolved_path": "71-seal/seal.json",
      "required": true,
      "condition": "always",
      "template_id": "seal-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b15-seal",
        "f20-seal",
        "r10-seal"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/71-seal/seal.md",
      "resolved_path": "docs/sdd/changes/<run.id>/71-seal/seal.md",
      "required": true,
      "condition": "always",
      "template_id": "seal",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b15-seal",
        "f20-seal",
        "r10-seal"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/71-seal/seal.json",
      "resolved_path": "docs/sdd/changes/<run.id>/71-seal/seal.json",
      "required": true,
      "condition": "always",
      "template_id": "seal-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b15-seal",
        "f20-seal",
        "r10-seal"
      ],
      "scope": "run",
      "path": "71-seal/journal.json",
      "resolved_path": "71-seal/journal.json",
      "required": true,
      "condition": "always",
      "template_id": "seal-journal",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b15-seal",
        "f20-seal",
        "r10-seal"
      ],
      "scope": "run",
      "path": "71-seal/backups/*/content.txt",
      "resolved_path": "71-seal/backups/<safe-slot-id>/content.txt",
      "required": false,
      "condition": "when_existing_canonical_target",
      "template_id": "seal-backup",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "approved baseline-plan.json: canonical_updates[].target_path; temp <target_path>.sdd.<run.id>.<attempt>.tmp",
      "scope": "project",
      "when": "exact accepted canonical bytes, registry last; temporary file removed",
      "template_ids": [
        "seal-backup",
        "atomic-temp"
      ],
      "nodes": [
        "f20-seal",
        "b15-seal",
        "r10-seal"
      ]
    }
  ]
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `atomic-temp` — Временная атомарная запись canonical документа

```text
Временный путь: <target_path>.sdd.<run.id>.<attempt>.tmp, рядом с точным target из принятого baseline-plan, только внутри разрешённого project workspace.
Payload template: exact-copy(approved candidate bytes); hash == canonical_update.after_sha256.
Создать эксклюзивно без перезаписи чужого существующего temp, fsync по возможностям хоста; перед replace повторить CAS before hash. При конфликте убрать только собственный temp при совпадении hash.
Это временный operational file, должен отсутствовать после успешного seal; не produced_artifact. Journal хранит фазу/target; никаких случайных файлов/содержимого вне плана.
Не использовать temp/replace для source/tests и не считать протокол распределённой транзакцией.
```

### Шаблон `seal` — Фиксация принятой документационной базы

```markdown
# Фиксация принятой документационной базы

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Основание
{{Trusted final gate: id, attempt, decision, route, audit ref; packet hash.}}
## Проверки до записи
{{Source/tests/spec fingerprints, canonical before hashes, неизменность candidate bytes.}}
## Применённые обновления
| Target от корня проекта | Operation | Before hash | Candidate / template | After hash | Результат |
|---|---|---|---|---|---|
| {{path}} | {{create/replace/tombstone}} | {{hash/null}} | {{slot/template}} | {{hash}} | {{applied/no_op/rolled_back}} |
## Registry и журнал
{{Registry как последний commit-point; RUN journal/backups с exact paths.}}
## Неизменность кода и тестов
{{До/после fingerprints; после e2e не менялись.}}
## Receipt и ограничения
{{sealed / blocked / needs_rework; approver/time null, если runtime не дал. Никаких PR/push/deploy.}}
```

### Шаблон `seal-backup` — Резервная копия изменяемого canonical документа

```text
RUN path: 71-seal/backups/<safe-slot-id>/content.txt.
Payload template: exact-copy(existing canonical target bytes) перед заменой. Это не новое знание и не генерируемый документ.
Для каждого существующего target из baseline-plan создать backup и запись journal{slot_id,target_path,before_sha256,backup_path,candidate_path,after_sha256,phase}.
Backup bytes hash == before_sha256. Для create с before=null backup не нужен; journal.backup_path=null.
Сохранять только собственные нормативные docs, не source/tests/секреты. PROJECT mirror отсутствует.
Rollback: восстанавливать только если текущий target hash == own after_sha256; иначе blocked concurrent conflict. Не удалять backup до успешного receipt.
```

### Шаблон `seal-journal` — Журнал канонической записи

Сохранять в RUN 71-seal/journal.json, обновлять перед каждой заменой и после. Это сознательно объявленный файл, не скрытый output. backup отсутствующего target не создаётся; удаление при rollback create допустимо только при совпадении own after hash.

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
  "packet_sha256": null,
  "entries": [],
  "registry_target": "{{REGISTRY_TARGET}}",
  "registry_written_last": false,
  "transaction_status": "blocked"
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"packet_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"entries":{"type":"array","items":{"type":"object","properties":{"slot_id":{"type":"string"},"target_path":{"type":"string"},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"backup_path":{"type":["string","null"]},"candidate_path":{"type":"string"},"phase":{"type":"string","enum":["prepared","applied","rolled_back","conflict"]},"error":{"type":["string","null"]}},"required":["slot_id","target_path","before_sha256","after_sha256","backup_path","candidate_path","phase","error"],"additionalProperties":false},"minItems":0},"registry_target":{"type":"string"},"registry_written_last":{"type":"boolean"},"transaction_status":{"type":"string","enum":["prepared","applied","rolled_back","blocked"]}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","packet_sha256","entries","registry_target","registry_written_last","transaction_status"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:seal-journal","title":"Журнал канонической записи","$defs":{"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

### Шаблон `seal-json` — Receipt фиксации

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
  "mode": "delivery",
  "receipt": {
    "run_id": "{{RUN_ID}}",
    "gate_id": "{{GATE_ID}}",
    "gate_attempt": 1,
    "decision": "approve",
    "route": "{{ROUTE}}",
    "packet_sha256": null,
    "comment": "{{COMMENT}}",
    "approver": null,
    "decided_at": null,
    "runtime_audit_ref": null,
    "valid": false,
    "invalidated_by": null
  },
  "packet_sha256": null,
  "canonical_updates_applied": [],
  "source_fingerprint": {
    "sha256": null,
    "included_paths": [],
    "excluded_paths": [],
    "files": [],
    "algorithm": "sha256-sorted-path-content-v1"
  },
  "test_fingerprint": null,
  "evidence_fingerprint": null,
  "registry_after_sha256": null,
  "journal_ref": {
    "scope": "run",
    "path": "{{PATH}}",
    "node_id": null,
    "attempt": null,
    "sha256": null,
    "purpose": "{{PURPOSE}}"
  },
  "final_limitations": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["sealed","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"mode":{"type":"string","enum":["delivery","baseline"]},"receipt":{"$ref":"#/$defs/gate_receipt"},"packet_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"canonical_updates_applied":{"type":"array","items":{"type":"object","properties":{"target_path":{"type":"string"},"before_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"operation":{"type":"string"},"result":{"type":"string","enum":["applied","no_op","rolled_back","blocked"]}},"required":["target_path","before_sha256","after_sha256","operation","result"],"additionalProperties":false},"minItems":0},"source_fingerprint":{"$ref":"#/$defs/fingerprint"},"test_fingerprint":{"anyOf":[{"$ref":"#/$defs/fingerprint"},{"type":"null"}]},"evidence_fingerprint":{"anyOf":[{"$ref":"#/$defs/fingerprint"},{"type":"null"}]},"registry_after_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"journal_ref":{"$ref":"#/$defs/file_ref"},"final_limitations":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","mode","receipt","packet_sha256","canonical_updates_applied","source_fingerprint","test_fingerprint","evidence_fingerprint","registry_after_sha256","journal_ref","final_limitations"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:seal-json","title":"Receipt фиксации","$defs":{"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"fingerprint":{"type":"object","properties":{"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["path","sha256"],"additionalProperties":false},"minItems":0},"algorithm":{"type":"string","enum":["sha256-sorted-path-content-v1"]}},"required":["sha256","included_paths","excluded_paths","files","algorithm"],"additionalProperties":false},"gate_receipt":{"type":"object","properties":{"run_id":{"type":"string"},"gate_id":{"type":"string"},"gate_attempt":{"type":"integer","minimum":1},"decision":{"type":"string","enum":["approve","rework","missing"]},"route":{"type":"string"},"packet_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"comment":{"type":"string"},"approver":{"type":["string","null"]},"decided_at":{"type":["string","null"]},"runtime_audit_ref":{"type":["string","null"]},"valid":{"type":"boolean"},"invalidated_by":{"type":["string","null"]}},"required":["run_id","gate_id","gate_attempt","decision","route","packet_sha256","comment","approver","decided_at","runtime_audit_ref","valid","invalidated_by"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S03] HGSDLC: runtime variables: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/runtime_variables/spec.md
- [S04] HGSDLC: artifacts: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/artifacts/spec.md
- [S06] HGSDLC: run lifecycle: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/run_lifecycle/spec.md
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
