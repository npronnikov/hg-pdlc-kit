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

## Основания и границы адаптации
- [S01] HGSDLC: инструкция создания flow: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/agent/create-flow-instruction.md
- [S06] HGSDLC: run lifecycle: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/run_lifecycle/spec.md

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
