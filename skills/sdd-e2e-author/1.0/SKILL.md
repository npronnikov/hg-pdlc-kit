---
name: sdd-e2e-author
description: Преобразует принятую модель в исполняемые UI/API/CLI/event тесты, не
  подменяя e2e unit тестами.
---

# Автор реальных сквозных тестов

## Цель
Написать исполняемые тестовые файлы, fixture/harness/config, runnable selectors и e2e-author.md/json. Тестовая модель задаёт expected behavior, текущий код — только способ взаимодействия.
## Выбор стека
Сохрани уже используемый browser/API/CLI framework. Для нового web harness допустим Playwright в TS/JS (или установленный проектом язык), даже если backend Java/Go/Python; это решение заранее отражено в architecture/plan. Для API-only используй native HTTP runner с реальной системой и data dependencies; component test с mock DB — не substitute e2e. Для CLI запускай бинарь/subprocess, проверяй exit/stdout/stderr и observable side effects. Для events проверяй producer→broker→consumer→external outcome с bounded polling, unique correlation IDs и cleanup.

Подними/используй утверждённую изолированную среду. Обследуй реальные routes/DOM/ARIA и API schemas; для UI вызови обязательный skill sdd-ui-playwright. Наличие MCP не предполагай; установленный browser runner может получать DOM/screenshot/trace и выполнять тесты. Необходимая UI проверка без доступного браузера => blocked, не переход к API-only.

Напиши позитивные, отрицательные и граничные TC из модели. Fixtures независимы, seed детерминированный, IDs уникальны на run/worker; не зависит от порядка. Пользовательское действие проверяй пользовательским результатом; API setup допустим, но не должен выполнять за UI сам проверяемый action. Приложи реальные assertions, а не только screenshot/click/HTTP 200. Core business path не mock; third-party double явно отражён в принятой модели.

Для каждого TC запиши file и точный runner selector в test-bindings.json, включая связку AC/SYS. Gherkin файл без step implementation/native mapping остаётся specification, не test. Изменение oracle/приоритетов/skip требует возврата к модели и gate. Не правь production code в этой ноде: обнаруженный дефект идёт через triage/code.
## Exit
Тесты реально discoverable, config разбирается, selectors уникальны, тесты не .only/.skip, нет placeholder assert(true). Проверка discover/compile не означает passed e2e; status authored. Сохрани перечень тестовых файлов/хэшей/команд и environment assumptions.

## Основания и границы адаптации
- [S15] Cucumber: Gherkin reference: https://cucumber.io/docs/gherkin/reference/
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
