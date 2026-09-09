# SRS — Приоритет заявки
Change CHG-ticket-priority-a1b2c3; DEMO-SRS-1. Адаптированный SRS, EARS-подобные формулировки; не нормативная сертификация.
## 1. Scope и определения
Только API priority; owner — из существующей authentication boundary; version — положительное целое.
## 2. Контекст
CMP-api/CMP-store, ADR-001; источники PRD/business и архитектура.
## 3. Интерфейсы
GET /api/tickets/{id} возвращает id/title/priority/version. PATCH /api/tickets/{id}/priority принимает JSON priority/expectedVersion.
HTTP 200 — успех; 400 — invalid_json/invalid_priority/invalid_version/unknown_field; 401 unauthorized; 404 not_found;
409 version_conflict; 413 body_too_large; 415 json_required; 405 method_not_allowed; 500 internal_error без деталей.
Токены fixtures только в изолированной среде; логирование токена запрещено.
## 4. Функциональные требования
| ID | Требование | Приёмка |
|---|---|---|
| SR-001 | Когда alice меняет priority на high, система должна обеспечить: 200; priority=high/version=2; последующий GET возвращает то же. | AC-001 |
| SR-002 | Когда сервис перезапускается на той же бд, система должна обеспечить: GET возвращает сохранённые priority и version. | AC-002 |
| SR-003 | Когда bob выполняет get/patch t-alice, система должна обеспечить: 404/not_found, тело заявки не раскрыто, данные не изменены. | AC-003 |
| SR-004 | Когда клиент выполняет patch, система должна обеспечить: 401/unauthorized и отсутствие изменения данных. | AC-004 |
| SR-005 | Когда patch с priority=urgent, система должна обеспечить: 400/invalid_priority, прежние priority/version сохранены. | AC-005 |
| SR-006 | Когда patch с broken json, missing/noninteger version либо неизвестным полем, система должна обеспечить: 400 с error для структуры/JSON, 415 для не-JSON content-type, 413 для тела >8192 bytes; состояние заявки не меняется. | AC-006 |
| SR-007 | Когда одновременно отправляют разные приоритеты с expectedversion=1, система должна обеспечить: Ровно один 200 и один 409; версия становится 2, победившее значение не потеряно. | AC-007 |
| SR-008 | Когда запускается обновлённое приложение, система должна обеспечить: id/title сохранены; GET содержит priority=normal, version=1. | AC-008 |
| SR-009 | Когда авторизованный пользователь меняет приоритет, система должна обеспечить: 404/not_found как для чужой заявки; существующие записи не изменены. | AC-009 |
## 5. Данные
Ticket(id TEXT PK,title TEXT NOT NULL,owner TEXT NOT NULL,priority enum NOT NULL DEFAULT normal,version INTEGER>=1 DEFAULT 1).
Миграция аддитивная; id/title/owner не переписываются. Auth precedes validation disclosure. Никаких новых классов PII.
## 6. Security
Owner из token map, не request body. Foreign и missing имеют единый 404. SQL параметризован. Input<=8192 bytes.
## 7. Надёжность
Conditional SQL атомарно отклоняет stale версии; нет фонового retry. State сохраняется в файле, restart не сбрасывает запись.
## 8. NFR
Численный production latency SLA отсутствует: не выдумывается и не заявляется проверенным. Test deadline 3s — защита harness, не SLA продукта.
## 9. Verification
SR-001…009 → реальные E2E-001…009. Unit tests дополняют SR-005/006, не заменяют публичную проверку.
## 10. Неизвестное и границы
Production IAM/масштаб/retention политика не определены учебным примером; не делать deployment.
