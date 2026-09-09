# Независимая модель E2E
Модель подготовлена до реализации как демонстрационный контракт, не выведена из passed tests.
## Граница
Внешний HTTP-клиент → child process Node API → настоящая файловая SQLite. Нет UI и mocked core components.
## Подготовка
На каждый E2E собственный mkdtemp, legacy SQL table, alice/bob tickets. Процесс слушает ephemeral port; readiness deadline 6s.
## Сценарии
- E2E-001 → AC-001 / SR-001: 200; priority=high/version=2; последующий GET возвращает то же
- E2E-002 → AC-002 / SR-002: GET возвращает сохранённые priority и version
- E2E-003 → AC-003 / SR-003: 404/not_found, тело заявки не раскрыто, данные не изменены
- E2E-004 → AC-004 / SR-004: 401/unauthorized и отсутствие изменения данных
- E2E-005 → AC-005 / SR-005: 400/invalid_priority, прежние priority/version сохранены
- E2E-006 → AC-006 / SR-006: 400 с error для структуры/JSON, 415 для не-JSON content-type, 413 для тела >8192 bytes; состояние заявки не меняется
- E2E-007 → AC-007 / SR-007: Ровно один 200 и один 409; версия становится 2, победившее значение не потеряно
- E2E-008 → AC-008 / SR-008: id/title сохранены; GET содержит priority=normal, version=1
- E2E-009 → AC-009 / SR-009: 404/not_found как для чужой заявки; существующие записи не изменены
## Изоляция и cleanup
Все запросы через HTTP. SIGTERM и ожидание child exit; затем удалить только свою temp directory.
## Success
Все девять required IDs passed, attempts=1, файл новый, source/contract hashes совпадают до/после.
Unit checks отдельно; никаких допущений о production throughput.
