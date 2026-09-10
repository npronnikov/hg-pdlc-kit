---
name: sdd-failure-triage
description: Разделяет дефект продукта, теста, требований и среды и выбирает минимальную
  корректную фазу возврата.
---

# Классификация обратной связи и сбоев

## Цель
triage.md/json с root cause evidence, affected requirements и route. Не пытаться одновременно переписать product code, test oracle и PRD.
## Алгоритм
Прочитай actual execution reports либо feedback final human gate. Восстанови reproduction, сравни expected из approved model с actual. Категории: product_defect; test_defect (locator/fixture/harness, но oracle прежний); system_or_architecture_gap; business_intent_change; environment_blocker. Не доказано — environment/unknown blocker, не бессрочный repair loop.

Для product_defect верни code writer, затем code review→test author/review→полный e2e rerun. Для test_defect верни test author, запрети production/requirements mutation. Для SYS/architecture gap возврат к architecture/SRS и повторные human approvals. Для BR/AC изменения — интервью/PRD. Для env/tool problem — blocker gate, после исправления безопасный повтор через discovery с сохранением ответов.

Отметь какие approval hashes и evidence invalidated. `triage.json`: category, evidence_refs, conflicting_ids, root_cause, minimal_repro, required_fix, allowed_files, invalidated_gates, chosen_route. Route в JSON summary — один из объявленных в ноде; значение on_success в этой конкретной ноде означает «диагностика закончена, исправлять тест», а не «продукт принят».
## Лимиты
Для технических repair/upstream handlers — не больше трёх автоматических возвратов в пределах run. Исключение: on_rework к новому раунду интервью в f03-prd/r03-business/b03-reproduce имеет бюджет 8; on_success имеет защитный бюджет 32, чтобы обычные повторные human approvals не исчерпывали лимит 3. Лимиты обеспечены max_loop_count; после исчерпания runtime failure и решение человека, не обход через новый alias. На повторных одинаковых failure сначала изменяется гипотеза/diagnostic, не ослабляется тест.


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
        "b12-triage",
        "f17-triage"
      ],
      "scope": "run",
      "path": "63-triage/triage.md",
      "resolved_path": "63-triage/triage.md",
      "required": true,
      "condition": "always",
      "template_id": "triage",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b12-triage",
        "f17-triage"
      ],
      "scope": "run",
      "path": "63-triage/triage.json",
      "resolved_path": "63-triage/triage.json",
      "required": true,
      "condition": "always",
      "template_id": "triage-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b12-triage",
        "f17-triage"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/63-triage/triage.md",
      "resolved_path": "docs/sdd/changes/<run.id>/63-triage/triage.md",
      "required": true,
      "condition": "always",
      "template_id": "triage",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b12-triage",
        "f17-triage"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/63-triage/triage.json",
      "resolved_path": "docs/sdd/changes/<run.id>/63-triage/triage.json",
      "required": true,
      "condition": "always",
      "template_id": "triage-json",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `triage` — Диагностика сбоя

```markdown
# Диагностика сбоя

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Наблюдаемый сбой
{{Execution report / final-gate feedback, run/attempt/revision.}}
## Expected и actual
{{Expected из approved AC/SYS/model; actual из native evidence.}}
## Минимальное воспроизведение и причина
{{Факты, подтверждённая root cause либо unknown; альтернативные гипотезы.}}
## Классификация
{{product_defect / test_defect / system_or_architecture_gap / business_intent_change / environment_blocker.}}
## Разрешённая поправка
{{Конкретные files, запрещённые изменения, owner; oracle не менять для green.}}
## Инвалидация
{{Какие reviews, gates, evidence устарели.}}
## Маршрут
{{Объявленный handler и target; on_success здесь может означать возврат к test author, не delivery pass.}}
```

### Шаблон `triage-json` — Маршрутизация исправления

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
  "category": "unknown",
  "evidence_refs": [],
  "conflicting_ids": [],
  "root_cause": null,
  "minimal_repro": "{{MINIMAL_REPRO}}",
  "required_fix": "{{REQUIRED_FIX}}",
  "allowed_files": [],
  "invalidated_gates": [],
  "invalidated_evidence": [],
  "chosen_route": "{{CHOSEN_ROUTE}}",
  "target_node": "{{TARGET_NODE}}"
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"category":{"type":"string","enum":["product_defect","test_defect","system_or_architecture_gap","business_intent_change","environment_blocker","unknown"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"conflicting_ids":{"type":"array","items":{"type":"string"},"minItems":0},"root_cause":{"type":["string","null"]},"minimal_repro":{"type":"string"},"required_fix":{"type":"string"},"allowed_files":{"type":"array","items":{"type":"string"},"minItems":0},"invalidated_gates":{"type":"array","items":{"type":"string"},"minItems":0},"invalidated_evidence":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"chosen_route":{"type":"string"},"target_node":{"type":"string"}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","category","evidence_refs","conflicting_ids","root_cause","minimal_repro","required_fix","allowed_files","invalidated_gates","invalidated_evidence","chosen_route","target_node"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:triage-json","title":"Маршрутизация исправления","$defs":{"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S01] HGSDLC: инструкция создания flow: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/agent/create-flow-instruction.md
- [S05] HGSDLC: node validation: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/node_validation/design.md
- [S06] HGSDLC: run lifecycle: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/run_lifecycle/spec.md

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
