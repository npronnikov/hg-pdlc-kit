# Контекст исследования (подготовленная демонстрация)
Режим brownfield; monorepo; modules apps/api, tests, tools. Исходный пример — before/apps/api/server.mjs.
## Наблюдения
Есть GET /api/tickets/{id}, token → owner mapping в изолированном fixture, SQLite(id,title,owner).
Поля priority/version и write use case отсутствуют. Источник: before/apps/api/server.mjs, обработчик GET и CREATE TABLE.
## Неизвестное до интервью
Кто меняет priority; enum/default; конфликты; UI scope; future metric.
## Границы доверия
Авторизация fixture не является production identity provider. Пример не утверждает готовность к production.
## Impact
API/DB migration/tests; нет сторонних репозиториев, UI, release или outcome анализа.
