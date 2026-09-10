---
name: sdd-recover-specs
description: Восстанавливает знания из кода с доказательствами, не превращая случайную
  реализацию в желаемое поведение.
---

# Восстановление спецификаций as-is

## Цель
Поддержать recovery flow: бизнес-картина, C4, SRS и каталог существующих тестов с уровнем достоверности. Product source/tests не изменять и новые фичи не реализовывать.
## Метод
Прочитай код/README/specs/контракты/migrations/routes/тесты по capability и relevant call chain. Каждое восстановленное утверждение имеет evidence file:line + commit/hash; классификацию observed_in_code / observed_in_test / human_confirmed / inferred / unknown. Комментарий разработчика — источник с риском устаревания, не execution evidence. Coverage slice оговаривается; не утверждай полный анализ миллионов строк после краткого поиска.

Business: observable value/roles/journeys/rules; цель, мотивация и desired behavior подтверждаются ВП, не выводятся достоверно только из code. Architecture: реальные containers/trust boundaries/protocols/dependencies, reconstructed decisions вместо выдуманных исторических ADR. System: обнаруженные interfaces/data/states/constraints; undocumented choices отдельно. Test inventory: native selectors, layers, channels, assertions и known gaps; существующий test ≠ passing test. Исполнение тестов не обязательно для recovery, если не запрашивалось/нет среды; status not_run, не green.

Сверь противоречия docs↔code↔test↔ВП в conflict register. Confirmed business norm может не совпадать с текущим кодом — это defect/gap, а не автоматический rewrite norm. Неизвестные NFR численно не заполняй. Принятие baseline означает «согласны с картой фактов, ограничений и пробелов», не «система удовлетворяет всем требованиям».
## Выход
recovery-evidence.json: claims[{id,text,classification,evidence_refs,confidence,human_confirmation}], conflicts[], unknowns[], coverage_boundary, inventory_test_status. Для каждой стадии обычный профильный шаблон, но с меткой reconstructed/as-is и ссылками evidence. Финальный baseline-plan добавляет только проверенную/помеченную информацию и ссылки на имеющиеся canonical specs.

## Без дублирования контрактов
В r01/r03/r05/r08 хранится только recovery-evidence.json со ссылками на существующие source paths/hashes. Нативные candidate contract files создаёт только r07-system-inventory, где подключён sdd-contracts-data. Ни docs-only recovery, ни одобрение ВП не означают e2e-pass.

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
        "r01-discover"
      ],
      "scope": "run",
      "path": "00-context/recovery-evidence.json",
      "resolved_path": "00-context/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r01-discover"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/00-context/recovery-evidence.json",
      "resolved_path": "docs/sdd/changes/<run.id>/00-context/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r03-business"
      ],
      "scope": "run",
      "path": "10-business/recovery-evidence.json",
      "resolved_path": "10-business/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r03-business"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/10-business/recovery-evidence.json",
      "resolved_path": "docs/sdd/changes/<run.id>/10-business/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r05-architecture"
      ],
      "scope": "run",
      "path": "20-architecture/recovery-evidence.json",
      "resolved_path": "20-architecture/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r05-architecture"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/20-architecture/recovery-evidence.json",
      "resolved_path": "docs/sdd/changes/<run.id>/20-architecture/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "run",
      "path": "30-system/recovery-evidence.json",
      "resolved_path": "30-system/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r07-system-inventory"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/30-system/recovery-evidence.json",
      "resolved_path": "docs/sdd/changes/<run.id>/30-system/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/recovery-evidence.json",
      "resolved_path": "70-acceptance/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/recovery-evidence.json",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/recovery-evidence.json",
      "required": true,
      "condition": "always",
      "template_id": "recovery-evidence",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `recovery-evidence` — Достоверность восстановленных знаний

Native contracts копируются только r07-system-inventory; другие recover stages ссылаются на точные исходные canonical paths в evidence. Не размножать контрактные files без contracts skill.

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
  "claims": [],
  "conflicts": [],
  "unknowns": [],
  "coverage_boundary": {
    "included_paths": [],
    "excluded_paths": [],
    "capabilities": [],
    "limitations": []
  },
  "inventory_test_status": "not_run"
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"claims":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string"},"text":{"type":"string"},"classification":{"type":"string","enum":["observed_in_code","observed_in_test","human_confirmed","inferred","unknown"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"confidence":{"type":"string","enum":["high","medium","low","unknown"]},"human_confirmation":{"anyOf":[{"type":"object","properties":{"human_node":{"type":"string"},"attempt":{"type":"integer","minimum":1},"question_id":{"type":"string"},"answer_source_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."}},"required":["human_node","attempt","question_id","answer_source_sha256"],"additionalProperties":false},{"type":"null"}]}},"required":["id","text","classification","evidence_refs","confidence","human_confirmation"],"additionalProperties":false},"minItems":0},"conflicts":{"type":"array","items":{"$ref":"#/$defs/finding"},"minItems":0},"unknowns":{"type":"array","items":{"$ref":"#/$defs/unknown"},"minItems":0},"coverage_boundary":{"type":"object","properties":{"included_paths":{"type":"array","items":{"type":"string"},"minItems":0},"excluded_paths":{"type":"array","items":{"type":"string"},"minItems":0},"capabilities":{"type":"array","items":{"type":"string"},"minItems":0},"limitations":{"type":"array","items":{"type":"string"},"minItems":0}},"required":["included_paths","excluded_paths","capabilities","limitations"],"additionalProperties":false},"inventory_test_status":{"type":"string","enum":["not_run","unknown"]}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","claims","conflicts","unknowns","coverage_boundary","inventory_test_status"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:recovery-evidence","title":"Достоверность восстановленных знаний","$defs":{"finding":{"type":"object","properties":{"id":{"type":"string"},"severity":{"type":"string","enum":["critical","major","minor","info"]},"source":{"$ref":"#/$defs/source_ref"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"issue":{"type":"string"},"impact":{"type":"string"},"required_fix":{"type":"string"},"owner":{"type":"string"},"disposition":{"type":"string","enum":["open","fixed","accepted_nonblocking","not_applicable"]},"resolution_evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","severity","source","requirement_ids","test_ids","issue","impact","required_fix","owner","disposition","resolution_evidence"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"unknown":{"type":"object","properties":{"id":{"type":"string"},"question":{"type":"string"},"owner":{"type":"string"},"blocking":{"type":"boolean"},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"resolution":{"type":["string","null"]}},"required":["id","question","owner","blocking","source_refs","resolution"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S11] C4 model: diagrams: https://c4model.com/diagrams
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
