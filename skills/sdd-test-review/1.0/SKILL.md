---
name: sdd-test-review
description: Не даёт получить зелёный результат за счёт слабых assertions, пропуска
  UI или скрытых mocks.
---

# Ревью тестов и oracle

## Цель
test-review.md/json с reviewed_test_hash и verdict. Вызови UI-test-auditor для UI scope (для non-UI — честный N/A) и spec-test-auditor.
## Контроль
Сверь каждый accepted TC с actual selector/file; required tests discoverable, .only/.skip отсутствуют, не отключены ранее существовавшие tests. Oracle соответствует AC, не copied from implementation; assertion проверяет outcome, а не только navigation/200. Setup не выполняет проверяемое действие; core path проходит реальную систему; permissions/negative path действительно negative. Fixtures независимы, cleanup не трогает чужие данные. Flakiness risk: fixed waits, random uncontrolled data, clock/timezone assumptions, flaky external dependency. Для UI — реальный browser, semantic locators, assertions, persistence, states по scope.

Reviewer не пишет исправления и не запускает destructive tests. Findings c file:line, affected TC/SYS, severity and fix. Тестовая ошибка → e2e-author; требование/oracle нужно изменить → system/model gate; production fault → code. Должно быть невозможно «принять» невыполненный тест по красивому отчёту.

## Основания и границы адаптации
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S17] Playwright: locators: https://playwright.dev/docs/locators
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
