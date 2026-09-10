---
name: sdd-contracts-data
description: Поддерживает SRS конкретными API/event/UI/data контрактами в нативных
  форматах проекта.
---

# Контракты интерфейсов и данных

## Цель
Создать contracts.md с точным индексом и contracts.json (реестр), а применимые машинные контракты — в проектном каталоге change и затем в canonical paths по принятому patch.
## Работа
Используй существующие OpenAPI/JSON Schema/GraphQL/protobuf/AsyncAPI форматы и версии репозитория; не обновляй spec version автоматически. REST: operations, request/response schemas, status/error codes, auth, pagination, idempotency и examples. Events: producer/consumer, schema evolution, ordering/delivery, dedup, poison handling. CLI/files: grammar, exit codes, stdout/stderr, encoding. UI: routes/screens, field schemas, loading/empty/error/success/disabled/permission states, validation, focus/keyboard/a11y, responsive/localized behavior.

Для каждого contract: owner, canonical source, proposed path, linked SYS/AC, compatibility delta, validation command и фактический результат. Для данных — keys, constraints, precision/units/timezone, ownership, retention, migration up/down compatibility and rollback concept; migrations исполнять только в test environment. Секреты только как env-name, никогда value.

contracts.json содержит interfaces[{id,kind,source_path,candidate_path,requirement_ids,version,validation}], data_changes[], ui_states[], not_applicable[]. contracts.md агрегирует содержание для human gate, а не даёт неопределённый glob на множество файлов. Нет интерфейса данного типа — обоснованный N/A; не создавать фиктивный API в CLI-проекте.


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
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contracts.md",
      "resolved_path": "10-defect-contract/contracts.md",
      "required": true,
      "condition": "always",
      "template_id": "contracts",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contracts.json",
      "resolved_path": "10-defect-contract/contracts.json",
      "required": true,
      "condition": "always",
      "template_id": "contracts-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contracts.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contracts.md",
      "required": true,
      "condition": "always",
      "template_id": "contracts",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contracts.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contracts.json",
      "required": true,
      "condition": "always",
      "template_id": "contracts-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contracts/*/contract.yaml",
      "resolved_path": "10-defect-contract/contracts/<safe-contract-id>/contract.yaml",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-yaml",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contracts/*/contract.yaml",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contracts/<safe-contract-id>/contract.yaml",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-yaml",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contracts/*/contract.json",
      "resolved_path": "10-defect-contract/contracts/<safe-contract-id>/contract.json",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contracts/*/contract.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contracts/<safe-contract-id>/contract.json",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contracts/*/contract.proto",
      "resolved_path": "10-defect-contract/contracts/<safe-contract-id>/contract.proto",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-proto",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contracts/*/contract.proto",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contracts/<safe-contract-id>/contract.proto",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-proto",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/contracts/*/contract.sql",
      "resolved_path": "10-defect-contract/contracts/<safe-contract-id>/contract.sql",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-sql",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/contracts/*/contract.sql",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/contracts/<safe-contract-id>/contract.sql",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-sql",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/contracts.md",
      "resolved_path": "30-system/contracts.md",
      "required": true,
      "condition": "always",
      "template_id": "contracts",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/contracts.json",
      "resolved_path": "30-system/contracts.json",
      "required": true,
      "condition": "always",
      "template_id": "contracts-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/contracts.md",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/contracts.md",
      "required": true,
      "condition": "always",
      "template_id": "contracts",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/contracts.json",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/contracts.json",
      "required": true,
      "condition": "always",
      "template_id": "contracts-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/contracts/*/contract.yaml",
      "resolved_path": "30-system/contracts/<safe-contract-id>/contract.yaml",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-yaml",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/contracts/*/contract.yaml",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/contracts/<safe-contract-id>/contract.yaml",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-yaml",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/contracts/*/contract.json",
      "resolved_path": "30-system/contracts/<safe-contract-id>/contract.json",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/contracts/*/contract.json",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/contracts/<safe-contract-id>/contract.json",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/contracts/*/contract.proto",
      "resolved_path": "30-system/contracts/<safe-contract-id>/contract.proto",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-proto",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/contracts/*/contract.proto",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/contracts/<safe-contract-id>/contract.proto",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-proto",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/contracts/*/contract.sql",
      "resolved_path": "30-system/contracts/<safe-contract-id>/contract.sql",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-sql",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/contracts/*/contract.sql",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/contracts/<safe-contract-id>/contract.sql",
      "required": false,
      "condition": "when_applicable_contract_exists",
      "template_id": "native-contract-sql",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `contracts` — Индекс интерфейсов и данных

```markdown
# Индекс интерфейсов и данных

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Границы и применимость
{{REST/events/CLI/UI/files/data; для каждого N/A с причиной.}}
## Реестр контрактов
| ID | Вид / формат / версия | Canonical source | Candidate RUN + PROJECT | SYS/AC | Compatibility delta | Проверка |
|---|---|---|---|---|---|---|
| {{id}} | {{kind/format/version}} | {{exact path}} | {{exact paths}} | {{IDs}} | {{delta}} | {{cmd, result, report}} |
## Семантика интерфейсов
{{Operations/messages/grammar, request/response/error, auth, pagination, timeouts, idempotency.}}
## Данные и миграции
{{Keys, constraints, units/precision/timezone, lifecycle, ownership, backward compatibility.}}
## UI-состояния
{{Screens, routes, fields, loading/empty/error/success/permission, focus/keyboard.}}
## Валидация и ограничения
{{Нативные validators версии проекта; unknown/blocked явно.}}
```

### Шаблон `contracts-json` — Реестр машинных контрактов

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
  "interfaces": [],
  "data_changes": [],
  "ui_states": [],
  "not_applicable": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"interfaces":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"kind":{"type":"string","enum":["rest","events","cli","ui","file","rpc","data","other"]},"format":{"type":"string"},"source_path":{"type":["string","null"]},"candidate_path":{"type":["string","null"]},"project_candidate_path":{"type":["string","null"]},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"acceptance_ids":{"type":"array","items":{"type":"string"},"minItems":0},"version":{"type":"string"},"owner":{"type":"string"},"compatibility_delta":{"type":"string"},"validation":{"$ref":"#/$defs/check"},"validation_command":{"type":["string","null"]},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["id","kind","format","source_path","candidate_path","project_candidate_path","requirement_ids","acceptance_ids","version","owner","compatibility_delta","validation","validation_command","sha256"],"additionalProperties":false},"minItems":0},"data_changes":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"entity":{"type":"string"},"change":{"type":"string"},"constraints":{"type":"array","items":{"type":"string"},"minItems":0},"migration":{"type":"string"},"compatibility":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["id","entity","change","constraints","migration","compatibility","requirement_ids"],"additionalProperties":false},"minItems":0},"ui_states":{"type":"array","items":{"type":"object","properties":{"screen":{"type":"string"},"route":{"type":"string"},"states":{"type":"array","items":{"type":"string"},"minItems":0},"field_rules":{"type":"array","items":{"type":"string"},"minItems":0},"authorization":{"type":"string"},"accessibility":{"type":"array","items":{"type":"string"},"minItems":0},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["screen","route","states","field_rules","authorization","accessibility","requirement_ids"],"additionalProperties":false},"minItems":0},"not_applicable":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string"},"reason":{"type":"string"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["kind","reason","source_refs"],"additionalProperties":false},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","interfaces","data_changes","ui_states","not_applicable"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:contracts-json","title":"Реестр машинных контрактов","$defs":{"check":{"type":"object","properties":{"id":{"type":"string"},"description":{"type":"string"},"result":{"type":"string","enum":["pass","fail","blocked","not_run","not_applicable"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"reason":{"type":"string"}},"required":["id","description","result","evidence_refs","reason"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

### Шаблон `native-contract-json` — Нативный контракт .json

Это параметризованный шаблон существующего нативного формата, а не разрешение выбрать произвольный формат после gate. Он требует source/scaffold, версии, конкретных полей интерфейса и validator в contracts registry.

````text
Формат: JSON Schema / OpenAPI / AsyncAPI версии репозитория.
Выбор шаблона: сначала source_path существующего контракта/одобренный нативный schema definition; сохранить этот format и version. Для нового контракта — минимальный валидный scaffold выбранного в архитектуре формата, его schema/validator закрепляется в contracts.json до записи.
Содержимое: конкретные согласованные SYS/AC интерфейса/данных; операции/messages/types/constraints/auth/errors/compatibility по виду. Пустой placeholder не является контрактом.
Паспорт: contracts.json interfaces[] с kind, format, version, source_path, candidate_path, project_candidate_path, owner, requirement_ids, acceptance_ids, compatibility_delta, sha256, validation, validation_command.
Пути: конкретный safe-contract-id вместо *; только текущий run. RUN и PROJECT очищенного нативного контракта равны bytes.
Валидация: parser/compiler/schema выбранной версии и реальный command result. Нет валидатора — явно blocked/unverified, не выдуманный результат.
Metadata внутрь формата не вставлять; version/hash хранить в registry и manifest. В recovery source copy без изменения поведения; на других стадиях — только source refs, не дополнительные copies.


Параметризованный scaffold для НОВОЙ JSON Schema данных (только если выбран этот формат):
```json
{
  "$schema": "{{PROJECT_JSON_SCHEMA_DIALECT_URI}}",
  "title": "{{APPROVED_DATA_CONTRACT}}",
  "type": "object",
  "properties": {"{{APPROVED_FIELD}}": {"type": "{{APPROVED_TYPE}}"}},
  "required": ["{{APPROVED_REQUIRED_FIELD}}"],
  "additionalProperties": false
}
```
Ограничения длины/диапазона/nullability/additionalProperties выбрать из принятого SYS, не по умолчанию каркаса. Для OpenAPI/AsyncAPI JSON использовать соответствующий существующий source/schema, не этот data-schema каркас.
````

### Шаблон `native-contract-proto` — Нативный контракт .proto

Это параметризованный шаблон существующего нативного формата, а не разрешение выбрать произвольный формат после gate. Он требует source/scaffold, версии, конкретных полей интерфейса и validator в contracts registry.

````text
Формат: syntax версии проекта; package/import/message/service реального protobuf контракта.
Выбор шаблона: сначала source_path существующего контракта/одобренный нативный schema definition; сохранить этот format и version. Для нового контракта — минимальный валидный scaffold выбранного в архитектуре формата, его schema/validator закрепляется в contracts.json до записи.
Содержимое: конкретные согласованные SYS/AC интерфейса/данных; операции/messages/types/constraints/auth/errors/compatibility по виду. Пустой placeholder не является контрактом.
Паспорт: contracts.json interfaces[] с kind, format, version, source_path, candidate_path, project_candidate_path, owner, requirement_ids, acceptance_ids, compatibility_delta, sha256, validation, validation_command.
Пути: конкретный safe-contract-id вместо *; только текущий run. RUN и PROJECT очищенного нативного контракта равны bytes.
Валидация: parser/compiler/schema выбранной версии и реальный command result. Нет валидатора — явно blocked/unverified, не выдуманный результат.
Metadata внутрь формата не вставлять; version/hash хранить в registry и manifest. В recovery source copy без изменения поведения; на других стадиях — только source refs, не дополнительные copies.


Параметризованный scaffold для НОВОГО protobuf-контракта при принятом syntax-based формате:
```proto
syntax = "{{PROJECT_PROTO_SYNTAX}}";
package {{APPROVED_PACKAGE}};
message {{APPROVED_MESSAGE}} {
  {{APPROVED_TYPE}} {{APPROVED_FIELD}} = {{STABLE_FIELD_NUMBER}};
}
service {{APPROVED_SERVICE}} {
  rpc {{APPROVED_OPERATION}} ({{APPROVED_REQUEST}}) returns ({{APPROVED_RESPONSE}});
}
```
Не переиспользовать retired field numbers. Для existing/edition-based источника сохранять его структуру. Опустить service в data-only contract с зафиксированным N/A.
````

### Шаблон `native-contract-sql` — Нативный контракт .sql

Это параметризованный шаблон существующего нативного формата, а не разрешение выбрать произвольный формат после gate. Он требует source/scaffold, версии, конкретных полей интерфейса и validator в contracts registry.

````text
Формат: SQL dialect/DDL/migration conventions выбранного проекта.
Выбор шаблона: сначала source_path существующего контракта/одобренный нативный schema definition; сохранить этот format и version. Для нового контракта — минимальный валидный scaffold выбранного в архитектуре формата, его schema/validator закрепляется в contracts.json до записи.
Содержимое: конкретные согласованные SYS/AC интерфейса/данных; операции/messages/types/constraints/auth/errors/compatibility по виду. Пустой placeholder не является контрактом.
Паспорт: contracts.json interfaces[] с kind, format, version, source_path, candidate_path, project_candidate_path, owner, requirement_ids, acceptance_ids, compatibility_delta, sha256, validation, validation_command.
Пути: конкретный safe-contract-id вместо *; только текущий run. RUN и PROJECT очищенного нативного контракта равны bytes.
Валидация: parser/compiler/schema выбранной версии и реальный command result. Нет валидатора — явно blocked/unverified, не выдуманный результат.
Metadata внутрь формата не вставлять; version/hash хранить в registry и manifest. В recovery source copy без изменения поведения; на других стадиях — только source refs, не дополнительные copies.


Параметризованный scaffold для НОВОГО DDL в принятом dialect:
```sql
CREATE TABLE {{APPROVED_TABLE}} (
  {{APPROVED_KEY}} {{DIALECT_KEY_TYPE}} PRIMARY KEY,
  {{APPROVED_FIELD}} {{APPROVED_TYPE}} {{APPROVED_NULLABILITY}}
);
```
Это пример формы, не требование создавать таблицу. Existing migration сохраняет migration framework/sequence. Constraints/indexes/compatibility/rollback только по принятому SYS; проверить parser и disposable database, production не трогать.
````

### Шаблон `native-contract-yaml` — Нативный контракт .yaml

Это параметризованный шаблон существующего нативного формата, а не разрешение выбрать произвольный формат после gate. Он требует source/scaffold, версии, конкретных полей интерфейса и validator в contracts registry.

````text
Формат: OpenAPI / AsyncAPI версии репозитория.
Выбор шаблона: сначала source_path существующего контракта/одобренный нативный schema definition; сохранить этот format и version. Для нового контракта — минимальный валидный scaffold выбранного в архитектуре формата, его schema/validator закрепляется в contracts.json до записи.
Содержимое: конкретные согласованные SYS/AC интерфейса/данных; операции/messages/types/constraints/auth/errors/compatibility по виду. Пустой placeholder не является контрактом.
Паспорт: contracts.json interfaces[] с kind, format, version, source_path, candidate_path, project_candidate_path, owner, requirement_ids, acceptance_ids, compatibility_delta, sha256, validation, validation_command.
Пути: конкретный safe-contract-id вместо *; только текущий run. RUN и PROJECT очищенного нативного контракта равны bytes.
Валидация: parser/compiler/schema выбранной версии и реальный command result. Нет валидатора — явно blocked/unverified, не выдуманный результат.
Metadata внутрь формата не вставлять; version/hash хранить в registry и manifest. В recovery source copy без изменения поведения; на других стадиях — только source refs, не дополнительные copies.


Параметризованный scaffold для НОВОГО REST/OpenAPI контракта (только если этот формат принят):
```yaml
openapi: "{{PROJECT_OPENAPI_VERSION}}"
info:
  title: "{{APPROVED_INTERFACE_NAME}}"
  version: "{{APPROVED_CONTRACT_VERSION}}"
paths:
  /{{APPROVED_RESOURCE}}:
    {{APPROVED_HTTP_METHOD}}:
      operationId: "{{APPROVED_OPERATION_ID}}"
      summary: "{{SYS_LINKED_BEHAVIOR}}"
      responses:
        "{{APPROVED_STATUS_CODE}}":
          description: "{{OBSERVABLE_RESULT}}"
```
Заполнить request/schema/auth/error/compatibility из SYS. Для AsyncAPI или существующего YAML взять его собственный исходный scaffold и точную native schema; не выдавать OpenAPI-каркас за AsyncAPI.
````

## Основания и границы адаптации
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S22] OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
