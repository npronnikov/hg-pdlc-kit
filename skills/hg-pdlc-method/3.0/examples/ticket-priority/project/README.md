# Ticket API — учебная монорепа
Пример — API-only продукт, поэтому E2E проходит external HTTP client → настоящий Node API → файловая SQLite.
Нет фронтенда в scope этого примера. UI-фичи основного flow требуют browser E2E и не покрываются этими API-тестами.
Node >=22.16.0 с node:sqlite; БД экспериментального Node API используется только в учебном примере.
Нет сторонних npm dependencies. `npm test` — unit; `npm run test:e2e -- pdlc-run-e2e-report.json` — реальные E2E.
Это обычные команды продукта. HG SDLC исполняет их через command-ноды; здесь нет другого workflow runtime.
Сервер принимает TEST_TOKENS_JSON с фикстурными токенами только при DEMO_MODE=1; НЕ развёртывать как production auth.
Демо-документы/ответы/approval — подготовленные иллюстративные fixtures, не выдаются за реальный запуск AI/HG.
Результаты E2E в evidence получены реальными локальными командами и отделены от этих fixtures.
