---
name: sdd-readiness-review
description: Проверяет PRD, архитектуру, SRS, контракты и тестовую модель как единый
  пакет.
---

# Проверка связности до кода

## Цель
Сформировать readiness.md + readiness.json и пакет для human acceptance SRS/test model. Прочитай исходные документы, а не только summary writer.
## Проверки
Полнота BR/RULE/AC; каждое SYS имеет BR/AC либо обоснованный platform constraint; архитектурные решения поддерживают NFR; интерфейсы и data model непротиворечивы; каждый must-have имеет verification method и минимум один TC/evidence; UI scope имеет UI e2e; нет orphan tests или требований; executable selectors пока могут быть planned, но намерение testable. Env requirements исполнимы либо явно включены в план; product decisions resolved, no critical TBD.

Вызови spec-test-auditor и architecture-auditor. Сохрани findings: id,severity,source file:line,requirement IDs,impact,proposed owner,disposition. Игнорировать blocker нельзя; optional suggestions не раздувают scope. Verdict ready / needs_rework / upstream_change / blocked.
## Выход
readiness.json: checks[], findings[], coverage_counts, unresolved_blockers, reviewed_hashes, invoked_subagents. `ready` — рекомендация для человека, не approval.
## Routing
Вычисли минимальную безопасную фазу возврата согласно handlers ноды: дефект SRS/model — их writer; конфликт architecture — architect; business meaning — PRD/interview; missing tool/env — blocker. После upstream change обнови downstream docs и gate; нельзя старым approval подтвердить новый hash.


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
        "f09-readiness"
      ],
      "scope": "run",
      "path": "45-readiness/readiness.md",
      "resolved_path": "45-readiness/readiness.md",
      "required": true,
      "condition": "always",
      "template_id": "readiness",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f09-readiness"
      ],
      "scope": "run",
      "path": "45-readiness/readiness.json",
      "resolved_path": "45-readiness/readiness.json",
      "required": true,
      "condition": "always",
      "template_id": "readiness-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f09-readiness"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/45-readiness/readiness.md",
      "resolved_path": "docs/sdd/changes/<run.id>/45-readiness/readiness.md",
      "required": true,
      "condition": "always",
      "template_id": "readiness",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "f09-readiness"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/45-readiness/readiness.json",
      "resolved_path": "docs/sdd/changes/<run.id>/45-readiness/readiness.json",
      "required": true,
      "condition": "always",
      "template_id": "readiness-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/readiness.md",
      "resolved_path": "70-acceptance/readiness.md",
      "required": true,
      "condition": "always",
      "template_id": "readiness",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r08-baseline-pack"
      ],
      "scope": "run",
      "path": "70-acceptance/readiness.json",
      "resolved_path": "70-acceptance/readiness.json",
      "required": true,
      "condition": "always",
      "template_id": "readiness-json",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/readiness.md",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/readiness.md",
      "required": true,
      "condition": "always",
      "template_id": "readiness",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "r08-baseline-pack"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/70-acceptance/readiness.json",
      "resolved_path": "docs/sdd/changes/<run.id>/70-acceptance/readiness.json",
      "required": true,
      "condition": "always",
      "template_id": "readiness-json",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `readiness` — Готовность связанного пакета

```markdown
# Готовность связанного пакета

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Объект и границы проверки
{{Профиль ревью, входные files/hashes, принятые требования, out-of-scope.}}
## Независимые задания и ожидание
| Сабагент | Task ID | Проверенные входы | Завершение | Verdict | Ссылка на полный ответ |
|---|---|---|---|---|---|
| {{name}} | {{actual id}} | {{hashes}} | {{completed/failed/timed_out}} | {{PASS/REWORK/BLOCKED/N/A}} | {{section}} |
## Проверки
| Check ID | Условие | Результат | Evidence |
|---|---|---|---|
| {{id}} | {{check}} | {{pass/fail/blocked/not_run/N/A}} | {{file:line / hash}} |
## Findings
| ID | Severity | File:line | BR/SYS/AC/TC | Факт | Последствие | Исправление | Owner | Disposition |
|---|---|---|---|---|---|---|---|---|
| {{id}} | {{critical/major/minor/info}} | {{source}} | {{IDs}} | {{fact}} | {{impact}} | {{fix}} | {{owner}} | {{open/fixed/nonblocking}} |
## Непроверенное и блокеры
{{Что невозможно подтвердить; никакого PASS по отсутствующему ответу.}}
## Полные ответы сабагентов
{{Ответ каждого по шаблону subagent-result; не заменять вымышленным резюме.}}
## Вердикт и маршрут
{{ready / needs_rework / upstream_change / blocked; причина и target. Это не human approve.}}
```

### Шаблон `readiness-json` — Машинная проверка готовности

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
  "checks": [],
  "findings": [],
  "reviewed_hashes": [],
  "invoked_subagents": [],
  "unresolved_blockers": [],
  "verdict": "blocked",
  "unverified": [],
  "coverage_counts": {
    "business_required": 1,
    "system_required": 1,
    "mapped_requirements": 1,
    "unmapped_requirements": 1,
    "planned_required_tests": 1,
    "ui_journeys_required": 1,
    "ui_journeys_covered": 1
  }
}
```

Полная JSON Schema; самостоятельная, без внешних $ref:
```json
{"type":"object","properties":{"schema_version":{"const":1},"document_revision":{"type":"string","description":"Новая ревизия каждой попытки, например <run>:<node>:<attempt>."},"run_id":{"type":"string"},"flow":{"type":"string"},"step_id":{"type":"string"},"attempt":{"type":"integer","minimum":1},"stage":{"type":"string"},"status":{"type":"string","enum":["ready","needs_input","needs_rework","blocked"]},"source_refs":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0},"checks":{"type":"array","items":{"$ref":"#/$defs/check"},"minItems":0},"findings":{"type":"array","items":{"$ref":"#/$defs/finding"},"minItems":0},"reviewed_hashes":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"invoked_subagents":{"type":"array","items":{"$ref":"#/$defs/subagent"},"minItems":0},"unresolved_blockers":{"type":"array","items":{"type":"string"},"minItems":0},"verdict":{"type":"string","enum":["ready","needs_rework","upstream_change","blocked"]},"unverified":{"type":"array","items":{"type":"string"},"minItems":0},"coverage_counts":{"type":"object","properties":{"business_required":{"type":"integer","minimum":0},"system_required":{"type":"integer","minimum":0},"mapped_requirements":{"type":"integer","minimum":0},"unmapped_requirements":{"type":"integer","minimum":0},"planned_required_tests":{"type":"integer","minimum":0},"ui_journeys_required":{"type":"integer","minimum":0},"ui_journeys_covered":{"type":"integer","minimum":0}},"required":["business_required","system_required","mapped_requirements","unmapped_requirements","planned_required_tests","ui_journeys_required","ui_journeys_covered"],"additionalProperties":false}},"required":["schema_version","document_revision","run_id","flow","step_id","attempt","stage","status","source_refs","checks","findings","reviewed_hashes","invoked_subagents","unresolved_blockers","verdict","unverified","coverage_counts"],"additionalProperties":false,"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"urn:hgsdlc:sdd:r4:readiness-json","title":"Машинная проверка готовности","$defs":{"check":{"type":"object","properties":{"id":{"type":"string"},"description":{"type":"string"},"result":{"type":"string","enum":["pass","fail","blocked","not_run","not_applicable"]},"evidence_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"reason":{"type":"string"}},"required":["id","description","result","evidence_refs","reason"],"additionalProperties":false},"file_ref":{"type":"object","properties":{"scope":{"type":"string","enum":["run","project","runtime","external"]},"path":{"type":"string","description":"RUN relative или project-relative путь; для внешнего источника — точная ссылка."},"node_id":{"type":["string","null"]},"attempt":{"type":["integer","null"],"minimum":0},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"purpose":{"type":"string"}},"required":["scope","path","node_id","attempt","sha256","purpose"],"additionalProperties":false},"finding":{"type":"object","properties":{"id":{"type":"string"},"severity":{"type":"string","enum":["critical","major","minor","info"]},"source":{"$ref":"#/$defs/source_ref"},"requirement_ids":{"type":"array","items":{"type":"string"},"minItems":0},"test_ids":{"type":"array","items":{"type":"string"},"minItems":0},"issue":{"type":"string"},"impact":{"type":"string"},"required_fix":{"type":"string"},"owner":{"type":"string"},"disposition":{"type":"string","enum":["open","fixed","accepted_nonblocking","not_applicable"]},"resolution_evidence":{"type":"array","items":{"$ref":"#/$defs/source_ref"},"minItems":0}},"required":["id","severity","source","requirement_ids","test_ids","issue","impact","required_fix","owner","disposition","resolution_evidence"],"additionalProperties":false},"source_ref":{"type":"object","properties":{"kind":{"type":"string","enum":["repository","human_input","runtime_gate","command","document","inference"]},"reference":{"type":"string","description":"file:line, Q-ID/attempt, audit id или command id"},"sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"claim":{"type":"string"},"classification":{"type":"string","enum":["documented","observed_in_code","observed_in_test","executed","human_confirmed","inferred","unknown"]}},"required":["kind","reference","sha256","claim","classification"],"additionalProperties":false},"subagent":{"type":"object","properties":{"name":{"type":"string"},"task_id":{"type":["string","null"]},"invocation_status":{"type":"string","enum":["completed","failed","timed_out","unavailable"]},"input_refs":{"type":"array","items":{"$ref":"#/$defs/file_ref"},"minItems":0},"started_at":{"type":["string","null"]},"finished_at":{"type":["string","null"]},"verdict":{"type":"string","enum":["PASS","REWORK","BLOCKED","NOT_APPLICABLE"]},"result_sha256":{"type":["string","null"],"pattern":"^[a-f0-9]{64}$","description":"SHA-256 реальных bytes; null только если файл ещё не существует/проверка заблокирована. Не выдумывать hash."},"result_location":{"type":"string","description":"Путь к секции выходного документа родителя или runtime transcript; сабагент файлов не создаёт."},"diff_unchanged":{"type":"boolean"},"blocker_reason":{"type":["string","null"]}},"required":["name","task_id","invocation_status","input_refs","started_at","finished_at","verdict","result_sha256","result_location","diff_unchanged","blocker_reason"],"additionalProperties":false}}}
```

## Основания и границы адаптации
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
