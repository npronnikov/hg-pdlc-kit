# Автоматизация
Девять сценариев test-model автоматизированы в tests/e2e/ticket-priority.e2e.mjs.
Это API-only E2E: отдельный HTTP server process и реальная SQLite с независимой fixture. Результат формируется runner по actual assertions.
За счёт внешнего входа, persistence/restart и tenant checks это не unit вызов handler. UI не входит в продукт примера.
