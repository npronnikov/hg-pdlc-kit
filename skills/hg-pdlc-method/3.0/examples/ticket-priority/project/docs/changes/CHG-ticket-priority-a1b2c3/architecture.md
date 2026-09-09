# Архитектура изменения — arc42-lite
Change CHG-ticket-priority-a1b2c3; DEMO-ARCH-1.
## 1. Цели и ограничения
Реальное API-only end-to-end поведение, сохранение legacy данных, запрет lost update. Один Git-корень.
## 2. Контекст (C4 L1)
Внешний HTTP-клиент владельца → Ticket API. Identity fixture даёт проверяемый owner, но не production IAM.
## 3. Building blocks (C4 L2)
CMP-api: Node HTTP приложение; CMP-store: файловая SQLite. Один application process обслуживает запросы, DB сохраняет состояние.
## 4. Стратегия и альтернативы
Reuse SQLite vs новая БД: reuse сохраняет минимальный delta. Optimistic version check vs last-write-wins: выбран version check (ADR-001).
## 5. Runtime
PATCH: auth → ownership lookup → parse/validate → conditional SQL UPDATE(version=expected) → 200 либо 409.
GET после записи и после restart подтверждает persisted state; response не доверяет входному owner.
## 6. Deployment для проверки
Отдельный child process на ephemeral localhost port; отдельный temp DB per case; readiness и bounded cleanup. Production не запускается.
## 7. Сквозные решения
Prepared statements, no-store HTTP responses, 8 KiB input cap, uniform 404 для missing/foreign, без логирования token.
## 8. Инварианты
Только owner меняет объект; failed request не меняет state; две записи одной версии не проходят одновременно; legacy id/title сохраняются.
## 9. Миграция
Проверить PRAGMA table_info; добавить priority NOT NULL DEFAULT normal и version DEFAULT 1. Тест создаёт старую схему ДО запуска приложения.
## 10. Quality scenarios
AC-002 restart persistence; AC-007 conflict; AC-003 tenant boundary; AC-008 legacy compatibility.
## 11. Риски
Auth fixture nonproduction. SQLite API текущего Node example experimental. Не заявляется performance/security сертификация.
## 12. Trace
BR-001/004 → CMP-api/CMP-store/ADR-001; BR-002/003 → CMP-api; BR-005 → CMP-store migration.
