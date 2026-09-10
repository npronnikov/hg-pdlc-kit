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

## Основания и границы адаптации
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S22] OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
