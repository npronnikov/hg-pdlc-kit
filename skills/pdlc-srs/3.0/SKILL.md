---
name: pdlc-srs
description: Системные требования и контракты. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Системные требования и контракты


## Работа
Создай SRS.md по профилю ISO/IEC/IEEE 29148 (адаптация, не заявление формального соответствия): purpose/scope/references; product context/actors/dependencies; FR; external interfaces; logical data; state transitions; NFR; security/privacy; error/recovery; compatibility/migration; verification and traceability; assumptions/TBD.
Формулируй атомарные FR/NFR в стиле EARS: «Когда <событие>, при <условии> система должна <наблюдаемый ответ>». Добавь state-driven, нежелательные события и инварианты там, где нужны. У каждого FR/NFR есть BR/ADR, приоритет, предусловие/вход, ответ, ошибки, verification method. У NFR — измерение, условия и порог; не пиши «быстро/безопасно».
contracts/index.md — индекс всех затронутых интерфейсов и schemas. HTTP: OpenAPI с auth, status codes, request/response, ошибками, idempotency; events: AsyncAPI при применимости; UI: states/validation/a11y; CLI: args/stdout/stderr/exit. Настоящие контракты хранятся в contracts/, индекс не заменяет схемы. Сохрани локальные схемы без network fetch.
Проверь concurrency, повтор/таймаут, частичный сбой, default/backfill, идентификаторы, время, retention, ownership и проверку доступа. Не переносить внутренние детали в бизнес-требования. Неприменимое отмечай с обоснованием.
trace/system.json: FR/NFR, BR→FR/NFR, ADR→FR/NFR. Если обнаружен design conflict, сохрани явно неполный draft и on_architecture; intent gap — on_intent; без конфликта on_success. Последующие машинные/семантические проверки не пропустят draft как готовый.
