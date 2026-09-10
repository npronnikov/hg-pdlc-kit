---
name: sdd-blocker-handling
description: Делает ограничения среды, доступа и scope явными без фиктивного прохода
  quality gate.
---

# Остановка и решение блокировки человеком

## Цель
blocker.md и recovery-input.md для human_approval разблокировки. Это не approval результата; человек устраняет препятствие, записывает решение в комментарии gate и выбирает Approve для повторной проверки условий.
## Работа
Прочитай CHANGE_ROOT/control/blocker.json, который обязан записать AI, выбравший blocker route. Если файла нет, восстанови контекст по переданным runtime step summaries и создай точный diagnostic, не угадывай. Классы: tool/subagent_missing, browser_missing, env_unavailable, unsafe_target, credentials_missing, unresolved_business, conflicting_baseline, concurrent_change, scope_not_bugfix, unknown.

blocker.md: что не выполнено; observed evidence; impact; кто может решить; безопасные варианты; что нельзя обойти. recovery-input.md: памятка, какие сведения указать в комментарии human_approval (решение, безопасная среда/роль/ограничения, имена env vars). Этот RUN файл read-only; редактируемого artifact input на данном gate нет. Не проси секреты в документ. ВП может cancel run штатным действием; on_rework возвращает формулировку блокера; on_approve возвращает discovery и повторные затронутые gate. Ранее введённые ответы сохраняются.

Нельзя на blocker gate разрешить «считать тест прошедшим», отключить обязательный UI или изменить oracle. Scope change требует full business/architecture/SRS approval. При баге, который оказался фичей, оператор завершает/cancel bugfix и запускает полный flow с тем же issue/evidence; YAML не умеет выдуманный subflow jump.


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
        "b16-blocker",
        "f21-blocker",
        "r11-blocker"
      ],
      "scope": "run",
      "path": "90-blocker/blocker.md",
      "resolved_path": "90-blocker/blocker.md",
      "required": true,
      "condition": "always",
      "template_id": "blocker",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b16-blocker",
        "f21-blocker",
        "r11-blocker"
      ],
      "scope": "run",
      "path": "90-blocker/recovery-input.md",
      "resolved_path": "90-blocker/recovery-input.md",
      "required": true,
      "condition": "always",
      "template_id": "recovery-input",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b16-blocker",
        "f21-blocker",
        "r11-blocker"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/90-blocker/blocker.md",
      "resolved_path": "docs/sdd/changes/<run.id>/90-blocker/blocker.md",
      "required": true,
      "condition": "always",
      "template_id": "blocker",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b16-blocker",
        "f21-blocker",
        "r11-blocker"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/90-blocker/recovery-input.md",
      "resolved_path": "docs/sdd/changes/<run.id>/90-blocker/recovery-input.md",
      "required": true,
      "condition": "always",
      "template_id": "recovery-input",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": []
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `blocker` — Блокировка выполнения

```markdown
# Блокировка выполнения

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Что не выполнено
{{Origin node/attempt/phase и честный статус; не failure продукта без доказательства.}}
## Причина и evidence
{{Категория, observed facts, hashes/log refs; источник control/blocker.json либо trusted runtime failure.}}
## Влияние
{{Какие mandatory outputs/проверки недоступны.}}
## Кто и что должен решить
{{Owner, safe required action, необходимые права/среда.}}
## Безопасные варианты
{{Исправить среду / уточнить scope / отменить run; не передавать секреты.}}
## Запрещённые обходы
{{Не считать red green, не skip required UI, не менять oracle без upstream approvals.}}
## Возобновление
{{Human gate comment → discovery → повтор затронутых approvals.}}
```

### Шаблон `recovery-input` — Памятка для разблокировки

```markdown
# Памятка для разблокировки

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Заполняется в комментарии runtime gate
{{Сам этот файл read-only; human_approval не является редактируемым human_input.}}
## Структура комментария
Решение: {{что реально исправлено}}
Безопасная среда: {{test-only URL / workspace / роль}}
Доступные инструменты: {{фактические runner / browser / Task}}
Переменные окружения: {{только ИМЕНА}}
Ограничения: {{что остаётся недоступным}}
Проверка исправления: {{observed evidence / ссылка}}
## Смысл кнопок
{{Approve: условия готовы к повторной проверке, не приёмка продукта. Rework: уточнить блокер. Cancel: завершить запуск штатно.}}
```

## Основания и границы адаптации
- [S01] HGSDLC: инструкция создания flow: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/agent/create-flow-instruction.md
- [S06] HGSDLC: run lifecycle: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/run_lifecycle/spec.md

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
