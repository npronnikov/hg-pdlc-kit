@CHG-ticket-priority-a1b2c3
Feature: Владелец задаёт приоритет заявки

  @E2E-001 @AC-001 @SR-001
  Scenario: Приёмка 1
    Given Заявка t-alice принадлежит alice, version=1
    When alice меняет priority на high
    Then 200; priority=high/version=2; последующий GET возвращает то же

  @E2E-002 @AC-002 @SR-002
  Scenario: Приёмка 2
    Given priority собственной заявки успешно изменён
    When сервис перезапускается на той же БД
    Then GET возвращает сохранённые priority и version

  @E2E-003 @AC-003 @SR-003
  Scenario: Приёмка 3
    Given Заявка принадлежит другому пользователю
    When bob выполняет GET/PATCH t-alice
    Then 404/not_found, тело заявки не раскрыто, данные не изменены

  @E2E-004 @AC-004 @SR-004
  Scenario: Приёмка 4
    Given Нет действительного token
    When клиент выполняет PATCH
    Then 401/unauthorized и отсутствие изменения данных

  @E2E-005 @AC-005 @SR-005
  Scenario: Приёмка 5
    Given Валидный владелец и версия
    When PATCH с priority=urgent
    Then 400/invalid_priority, прежние priority/version сохранены

  @E2E-006 @AC-006 @SR-006
  Scenario: Приёмка 6
    Given Валидный владелец
    When PATCH с broken JSON, missing/noninteger version либо неизвестным полем
    Then 400 с error для структуры/JSON, 415 для не-JSON content-type, 413 для тела >8192 bytes; состояние заявки не меняется

  @E2E-007 @AC-007 @SR-007
  Scenario: Приёмка 7
    Given Два клиента прочитали version=1
    When одновременно отправляют разные приоритеты с expectedVersion=1
    Then Ровно один 200 и один 409; версия становится 2, победившее значение не потеряно

  @E2E-008 @AC-008 @SR-008
  Scenario: Приёмка 8
    Given Существующая таблица без priority/version
    When запускается обновлённое приложение
    Then id/title сохранены; GET содержит priority=normal, version=1

  @E2E-009 @AC-009 @SR-009
  Scenario: Приёмка 9
    Given Запрошен отсутствующий id
    When авторизованный пользователь меняет приоритет
    Then 404/not_found как для чужой заявки; существующие записи не изменены
