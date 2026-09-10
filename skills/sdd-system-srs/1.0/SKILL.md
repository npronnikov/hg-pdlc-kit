---
name: sdd-system-srs
description: Формализует принятое бизнес-поведение и архитектуру в атомарные, трассируемые
  и верифицируемые требования.
---

# Системные требования в SRS

## Цель
Создать srs.md и system-requirements.json. Формат — адаптированный SRS, ориентированный на ISO/IEC/IEEE 29148; это не буквальная копия стандарта и не заявление о соответствии всем его положениям.
## Шаблон srs.md
1. Introduction: purpose, scope, definitions, references, document control.
2. Overall description: product context, users, assumptions/dependencies, constraints, operating environment.
3. External interfaces: UI behavior/states/accessibility; API/events/CLI/files; third-party protocols; failures/timeouts.
4. Functional requirements SYS-ID: trigger, preconditions, actor, SHALL/«система должна», observable result, exceptions, authorization, linked BR/RULE/AC/ADR.
5. Data: schemas, units/time zones/currencies, validation, integrity, ownership, retention/deletion, migration/backward compatibility.
6. State/concurrency: permitted transitions, retries, deduplication, idempotency, transaction boundaries and recovery.
7. Quality requirements NFR-ID: metric, threshold, workload/window, environment, verification method and linked business driver. Не использовать «быстро», «надёжно», «удобно» без критерия.
8. Security/privacy: applicable threats, roles/permissions, input/output validation, data minimization and audit; cite конкретную редакцию ASVS при применении, не сочинять номера контролей.
9. Verification: requirement→method(test/analysis/inspection)→test case / evidence owner; readiness/acceptance rules.
10. Traceability; rationale; unresolved; glossary; change record.

Правило атомарности: одно нормативное поведение на ID. Сценарный шаблон: «При <условие/событие> система должна <результат>, при <ошибка> должна <обработка>». Разделяй positive requirement и запрет/denial для независимой проверки. Порог ссылается на источник либо человеческое решение; нельзя придумать SLA за ВП.
## system-requirements.json
schema_version, document_revision, requirements[{id,kind,statement,source_br_ids,source_ac_ids,adr_ids,interface_refs,priority,verification_method,verification_criteria,scope,status}], external_interfaces[], data_rules[], state_models[], unresolved[].
## Процесс
Прочитай accepted PRD+architecture, отрази approved decisions. Восстанови bidirectional trace links. При архитектурном конфликте верни architecture stage; при изменении смысла BR — PRD. До SRS gate никакого product code. Нельзя реализовать только endpoint list и объявить полный SRS.


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
      "path": "10-defect-contract/srs.md",
      "resolved_path": "10-defect-contract/srs.md",
      "required": true,
      "condition": "always",
      "template_id": "srs",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "run",
      "path": "10-defect-contract/system-requirements.json",
      "resolved_path": "10-defect-contract/system-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "system-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/srs.md",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/srs.md",
      "required": true,
      "condition": "always",
      "template_id": "srs",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b04-defect-contract"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-defect-contract/system-requirements.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-defect-contract/system-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "system-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/srs.md",
      "resolved_path": "30-system/srs.md",
      "required": true,
      "condition": "always",
      "template_id": "srs",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/system-requirements.json",
      "resolved_path": "30-system/system-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "system-requirements",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/srs.md",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/srs.md",
      "required": true,
      "condition": "always",
      "template_id": "srs",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f07-srs",
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/system-requirements.json",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/system-requirements.json",
      "required": true,
      "condition": "always",
      "template_id": "system-requirements",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `srs` — SRS — системные требования

Авторская адаптация SRS из исходного набора, не буквальный стандарт и не сертификат соответствия ISO/IEC/IEEE 29148.

```markdown
# SRS — системные требования

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## 1. Введение и контроль документа
{{Purpose, scope, glossary, references, revision, approved PRD/architecture hashes.}}
## 2. Общее описание
{{Product context, users, environment, constraints, assumptions/dependencies.}}
## 3. Внешние интерфейсы
{{UI states / API / events / CLI / files; ссылки на contracts.json, ошибки и timeouts.}}
## 4. Функциональные требования
### {{SYS-ID}} — {{название}}
Trigger: {{событие}}; Preconditions: {{условия}}; Actor: {{роль}}
Система должна: {{одно атомарное наблюдаемое поведение}}
Exceptions / denial: {{отдельно проверяемые отказы}}
Authorization: {{кто и при каких условиях}}
Sources: {{BR/RULE/AC/ADR}}; Verification: {{метод и критерий}}
## 5. Данные
{{Schemas, constraints, единицы/точность/time zones, ownership, retention/deletion, migration compatibility.}}
## 6. Состояния и конкурентность
{{Allowed transitions, retries, dedup, idempotency, transaction boundaries, recovery.}}
## 7. Требования качества
| NFR-ID | Метрика | Порог | Нагрузка / окно | Среда | Метод проверки | Источник |
|---|---|---|---|---|---|---|
| {{NFR-ID}} | {{metric}} | {{confirmed threshold / unknown}} | {{workload}} | {{env}} | {{test/analysis/inspection}} | {{source}} |
## 8. Безопасность и privacy
{{Threats, permissions, validation, data minimization, audit. Конкретные controls только из источника.}}
## 9. Верификация
{{SYS/NFR → метод → TC/evidence owner; acceptance rules.}}
## 10. Трассировка, риски и история
{{Нет orphan IDs, unresolved must-have, delta и rationale.}}
```

### Шаблон `system-requirements` — Системные требования

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
  "requirements": [],
  "external_interfaces": [],
  "data_rules": [],
  "state_models": [],
  "unresolved": []
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"requirements":{"type":"array","items":{"$ref":"#/$defs/requirement"},"minItems":0},"external_interfaces":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"kind":{"type":"string"},"contract_ref":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["id","kind","contract_ref","requirement_ids"],"additionalProperties":false},"minItems":0},"data_rules":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"rule":{"type":"string"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"verification":{"type":"string"}},"required":["id","rule","requirement_ids","verification"],"additionalProperties":false},"minItems":0},"state_models":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"states":{"type":"array","items":{"type":"string"},"minItems":0},"transitions":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string"},"event":{"type":"string"},"guard":{"type":"string"},"to":{"type":"string"},"effects":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["from","event","guard","to","effects"],"additionalProperties":false},"minItems":0}},"required":["id","states","transitions"],"additionalProperties":false},"minItems":0},"unresolved":{"type":"array","items":{"$ref":"#/$defs/unknown"},"minItems":0}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","requirements","external_interfaces","data_rules","state_models","unresolved"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:system-requirements","title":"Системные требования","$defs":{"requirement":{"type":"object","properties":{"id":{"type":"string"},"kind":{"type":"string","enum":["functional","quality","constraint"]},"statement":{"type":"string"},"source_br_ids":{"type":"array","items":{"type":"string"},"minItems":0},"source_ac_ids":{"type":"array","items":{"type":"string"},"minItems":0},"adr_ids":{"type":"array","items":{"type":"string"},"minItems":0},"interface_refs":{"type":"array","items":{"type":"string"},"minItems":0},"priority":{"type":"string","enum":["must","should","could"]},"verification_method":{"type":"string","enum":["test","analysis","inspection"]},"verification_criteria":{"type":"string"},"scope":{"type":"string"},"status":{"type":"string","enum":["candidate","reconstructed","removed"]},"trigger":{"type":"string"},"preconditions":{"type":"array","items":{"type":"string"},"minItems":0},"observable_result":{"type":"string"},"exceptions":{"type":"array","items":{"type":"string"},"minItems":0},"authorization":{"type":"string"},"metric":{"type":["string","null"]},"threshold":{"type":["string","null"]},"workload":{"type":["string","null"]},"environment":{"type":["string","null"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","kind","statement","source_br_ids","source_ac_ids","adr_ids","interface_refs","priority","verification_method","verification_criteria","scope","status","trigger","preconditions","observable_result","exceptions","authorization","metric","threshold","workload","environment","source_refs"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"unknown":{"type":"object","properties":{"id":{"type":"string"},"question":{"type":"string"},"owner":{"type":"string"},"blocking":{"type":"boolean"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"resolution":{"type":["string","null"]}},"required":["id","question","owner","blocking","source_refs","resolution"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- [S22] OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
