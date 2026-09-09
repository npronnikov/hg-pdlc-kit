---
name: pdlc-test-model
description: Тестовая модель до реализации. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Тестовая модель до реализации


## Работа
Из согласованного поведения PRD/SRS, а НЕ текущего кода, создай test-model.md, test-model.feature и trace/tests.json. На каждый AC — минимум один настоящий E2E, плюс негативные, права/изоляция, границы, сохранность и регрессия. Для каждого E2E-ID: purpose, boundary (browser-system/api-system/cli-system), реальные in-scope components, preconditions, данные/setup, действие, внешний oracle, expected, cleanup. Gherkin — читаемая модель, ещё НЕ факт тестирования.
Web-продукт требует browser journeys по UI→API→настоящая БД; API/CLI допускают соответствующую реальную внешнюю границу. Внутренние сервисы продукта нельзя мокать в приёмочном E2E. Допустимый внешний sandbox/эмулятор за границей продукта явно перечисляется. Unit/component/contract tests полезны, но не переименовываются в E2E. CHECK-ID для дополнительных NFR проверок остаётся отдельным типом.
verification-plan.json задаёт конечные build и e2e команды: argv (массив, не shell), cwd относительно монорепы, timeout_seconds, boundary, in_scope_components, internal_mocks:false, excluded_external_systems. E2E argv содержит {junit}; runner передаёт свежий logical run path. Все E2E и обязательные CHECK выдаются в итоговом JUnit с [ID], пропуск считается неуспехом.
Выбери существующий стек: JS/TS обычно локально установленный Playwright; Java/Go/Python — текущий системный harness, browser driver при UI. Не заставляй продукт переезжать на пример Python. Для greenfield включи создание стенда в foundation story, не предполагай его существование.
Никакой реализации E2E-кода на этом этапе. После утверждения дизайна ожидаемые результаты заморожены. Исполняемые тесты создаёт отдельный шаг после application code.
