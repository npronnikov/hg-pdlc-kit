---
name: sdd-ui-playwright
description: Обучает UI-автора исследовать интерфейс и писать надёжные browser tests
  в реальной среде.
---

# UI e2e: браузер, семантика и устойчивость

## Цель
Обеспечить реальный browser end-to-end путь; приложение может быть на любом backend-языке. Сохрани существующий качественный UI framework; следующие принципы обязательны, примеры Playwright адаптируются к нему.
## Инструменты
Проверь доступность фактического runner и browser binaries; зафиксируй versions. Для исследования UI используй Playwright scripts/runner с DOM snapshots, accessibility roles, screenshots и traces; browser MCP может ускорить исследование, но не обязательная зависимость и не доказательство исполнения native tests. Не предполагай наличие сервера MCP или конкретных имён его tools.

## Сценарий работы
1. Прочитай UI contracts, routes, components и accepted AC. Найди реальный элемент в DOM браузера; не выдумывай locator по скриншоту или исходнику без проверки. Используй getByRole/getByLabel/текст; test id — явный устойчивый контракт; CSS/XPath только обоснованно.
2. Подготовь отдельные fixture data и role account. storageState держи в ignored test-auth каталоге, не в docs/Git; не логируй cookies/tokens. Login сам по себе тоже нуждается в UI тесте, если входит в scope; API login для остальных тестов не должен подменять login acceptance.
3. Действуй через UI: navigate→ввод→action→observable confirmation→состояние после reload/new session по AC. Перепроверь бизнес-состояние через публичный API, где это усиливает oracle.
4. Negative: validation/no submit, forbidden action/tenant access, empty/loading/error/retry states; responsive/keyboarding/focus and basic a11y checks при включении в модель. Автоматический a11y scan не доказывает полное WCAG соответствие; visual baseline сравнивай только после human approval, не auto-update ради green.
5. Используй auto-wait и web-first assertions; запрети sleep/waitForTimeout как синхронизацию. Для eventual consistency — bounded poll с явным timeout/diagnostic. Не `force: true`, не `nth()` как маскировку неоднозначного selector, не disable security для удобства.
6. Runner управляет lifecycle сервера: webServer либо safe setup/teardown, readiness endpoint, timeout, остановка только собственных процессов. `reuseExistingServer` допускается только после проверки версии/среды, чтобы не тестировать старый процесс. Настрой native JSON/JUnit report и trace on failure; screenshot на ошибке, очищай sensitive evidence.

## Каркас одного теста (не готовый тест конкретного продукта)
```ts
import { test, expect } from '@playwright/test';
// TC/CAP/SYS/AC IDs are placed in the title or an explicit binding registry.
test('TC-example-001 / AC-example-001: confirmed user outcome', async ({ page }) => {
  // Replace with REAL approved route, labels, fixtures and expected outcome.
  // Arrange must not perform the user action under test.
  await page.goto('/approved-real-route');
  await page.getByLabel('Approved real field label').fill('isolated fixture value');
  await page.getByRole('button', { name: 'Approved real action' }).click();
  await expect(page.getByRole('status')).toHaveText('Approved observable result');
  await page.reload();
  await expect(page.getByRole('status')).toHaveText('Approved observable result');
});
```
Ни один placeholder каркаса не разрешён в итоговых тестах. Заголовок/expected oracle берётся из model, не из фактического ответа приложения.
## Выход
ui-observations.md: реально просмотренные экраны, DOM/role evidence, выбранные selectors, browser/tool versions, ограничения. Исполняемые native UI tests, role fixtures, runner config и mapping TC→selector. `authored` отдельно от `executed/passed`.

## Основания и границы адаптации
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S17] Playwright: locators: https://playwright.dev/docs/locators
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver
- [S20] Playwright: authentication: https://playwright.dev/docs/auth

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
