---
name: sdd-implement
description: Пишет код в нативном стеке и подтверждает каждый slice unit/integration
  проверками.
---

# Реализация Qwen с коротким TDD-циклом

## Цель
Реализовать утверждённый implementation plan. Product code пишет Qwen, не reviewer.
## Работа
Сверь hashes approved inputs и исходный рабочий diff. Прочитай затронутые исходники, локальные conventions и соседние tests. Для поведения сначала зафиксируй failing unit/integration test, где применимо; отсутствие механизма red объясни, не фальсифицируй log. Реализуй минимальный slice, выполни native build/lint/typecheck/unit/integration, затем рефакторинг без смены поведения. Для Java используй существующие Gradle/Maven и тестовые библиотеки, Go — имеющиеся go tools, Python — runner проекта, JS/TS — lockfile/toolchain проекта.

Сохраняй совместимость интерфейсов, error handling, authn/authz на сервере, транзакции и idempotency; UI — все согласованные состояния, label/role/keyboard semantics. Не прячь ошибку empty catch, не ослабляй validations и не меняй expected result для зелёного теста. Не включай tests-only bypass в production API. Если requirement невозможно выполнить в принятой architecture — route upstream вместо скрытого решения.

implementation.md перечисляет task status, changed files и requirement IDs; implementation.json содержит before/after fingerprints, raw command evidence refs, unit/integration results, actual code diff, outstanding. Код/тесты материализуются в реальных source/test directories. README о том, что «код будет написан», не считается implementation. E2E ещё не пройдены — явно not_run, не «все тесты зелёные».
## Exit
Обязательные lower-level проверки успешны, все accepted tasks сделаны, нет scope drift. Допустимы только file_allowlist и обоснованные companion files; неожиданное изменение -> остановка/ревью.

## Основания и границы адаптации
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
