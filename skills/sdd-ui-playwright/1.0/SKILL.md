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


## Полный файловый контракт

Этот раздел задаёт имена, scope, условие создания и точный шаблон каждого выхода. Краткие списки выше — обзор, не дополнительные outputs. Выбери только строки текущей ноды из `nodes`; не создавай файлы других стадий. Если `required: false`, всё равно действуют template и condition.

<!-- OUTPUT_CONTRACTS_BEGIN -->
```json
{
  "contract_version": "r4",
  "path_rules": {
    "run": "Путь относительно RUN output root текущей попытки, который дал runtime.",
    "project": "resolved_path относительно выбранного repository root. <run.id> — текущий run, остальные safe IDs из registry; glob в FLOW не задаёт имя каталога."
  },
  "outputs": [
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "run",
      "path": "60-e2e-author/ui-observations.md",
      "resolved_path": "60-e2e-author/ui-observations.md",
      "required": true,
      "condition": "always",
      "template_id": "ui-observations",
      "writer": "main_agent"
    },
    {
      "nodes": [
        "b09-e2e-author",
        "f14-e2e-author"
      ],
      "scope": "project",
      "path": "docs/sdd/changes/*/60-e2e-author/ui-observations.md",
      "resolved_path": "docs/sdd/changes/<run.id>/60-e2e-author/ui-observations.md",
      "required": true,
      "condition": "always",
      "template_id": "ui-observations",
      "writer": "main_agent"
    }
  ],
  "mutation_contracts": [
    {
      "path_source": "e2e-author.json: test_files[].path + harness_files[].path",
      "scope": "project",
      "when": "applicable UI scope, no product changes",
      "template_ids": [
        "native-test"
      ],
      "nodes": [
        "f14-e2e-author",
        "b09-e2e-author"
      ]
    }
  ]
}
```
<!-- OUTPUT_CONTRACTS_END -->

### Шаблон `native-test` — Параметризованный шаблон исполняемого теста

```text
Путь: implementation-plan file contract (для lower-level) либо e2e-author.test_files и test-bindings.file (для e2e), конкретный project-relative path ДО записи; template_id=native-test.
Native skeleton: imports/fixtures/setup → test title с TC/SYS/AC → Arrange уникальных isolated данных → Act через выбранную real system boundary → Assert observable oracle из accepted model → Cleanup в finally/teardown.
UI: реальная DOM/ARIA проверка, semantic locator, действие через browser, web-first assertions, persistence по scope; API setup не выполняет проверяемое UI действие.
API: запрос к настоящей app+data границе, статус + schema + бизнес-результат/побочный эффект и отрицательные права.
CLI: subprocess реального executable, bounded timeout, exit/stdout/stderr + observable state.
Events: real producer/broker/consumer boundary, correlation ID, bounded poll outcome, cleanup own messages/data.
Fixture/config: environment и toolchain только из принятого плана, readiness/start/stop, pinned reporter и browser versions, без .only/.skip/assert(true), фиксированных sleep и auto-accept visual snapshots.
Report binding: exact file hash + unique runner/project/selector → TC/AC/SYS. Authored/discovered не равно passed; результат фиксирует run-e2e.
Шаблон адаптируется к уже принятому стеку; для Playwright UI конкретный каркас есть в sdd-ui-playwright. Никаких placeholders в итоговом тесте.
```

### Шаблон `ui-observations` — Наблюдения интерфейса

```markdown
# Наблюдения интерфейса

Revision: {{REVISION}} | run_id: {{RUN_ID}} | flow: {{FLOW}} | step_id: {{NODE_ID}} | attempt: {{ATTEMPT}} | stage: {{STAGE}}
Status: {{ready / needs_input / needs_rework / blocked}}
Sources: {{точные file:line / Q-ID / runtime references с ревизиями}}

## Применимость UI
{{applicable / not_applicable; reason со ссылкой на model/context.}}
## Браузер и окружение
{{Реальные runner/browser versions, URL test-only, source revision, доступность DOM tools.}}
## Просмотренные экраны
| Route | Роль | Наблюдаемое состояние | DOM/ARIA evidence | Связанные AC/TC |
|---|---|---|---|---|
| {{route}} | {{role}} | {{state}} | {{real evidence path}} | {{IDs}} |
## Локаторы
| Элемент | Locator | Почему устойчив | Проверен в browser? | Неоднозначность |
|---|---|---|---|---|
| {{element}} | {{getByRole/getByLabel/approved testid}} | {{reason}} | {{real result}} | {{none/issue}} |
## Сценарии и оракулы
{{Действие через UI → user outcome → persistence; API setup не исполняет тестируемое действие.}}
## Raw evidence и приватность
{{Точные RUN refs/hashes; cookies/storageState/PII не копировать в Git.}}
## Ограничения
{{Не проверенные состояния и причина; no-browser при required UI — blocked.}}
```

## Основания и границы адаптации
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S17] Playwright: locators: https://playwright.dev/docs/locators
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver
- [S20] Playwright: authentication: https://playwright.dev/docs/auth

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
