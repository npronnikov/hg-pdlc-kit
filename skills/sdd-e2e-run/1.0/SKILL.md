---
name: sdd-e2e-run
description: Запускает реальные команды, сопоставляет native reports с моделью и отделяет
  blocked/fail/flaky от pass.
---

# Исполнение e2e и сбор evidence

## Цель
Создать execution.md, execution.json, evidence-index.json и raw native reports в RUN. Не изменять production code или oracle.
## Исполнение
Сверь hashes source tree, lockfiles, test bindings, accepted SRS/model и test-review. Проверь только test env, правильную build revision, readiness/dependencies/auth env NAMES. Перед любыми seeds/cleanup убедись, что это изолированная среда и данные принадлежат текущему run. Нет доступа/браузера/сети/dependency => blocked с точной причиной. Это не fail продукта и не pass.

Выполни plan commands в их реальном cwd через shell. Сохрани точный argv/cmd, start/end, timeout, exit code, stdout/stderr paths/hash, tool/browser versions, source/tests/spec fingerprints, environment descriptor. Запускай build/lint/unit/integration регрессию по affected area и всю согласованную e2e suite. Не только новый один happy path. API/UI/CLI/events соответствуют утверждённой модели; если модель требует UI, browser project обязателен.

Парси native JSON/JUnit/test reports, не считай текст `All passed` доказательством. Map actual selectors к TC. Различай expected, discovered, executed, passed, failed, skipped, flaky, not_run. Каждый required TC обязан существовать в report и пройти на проверяемой revision; exit code=0 и нулевой test count не успех. Retry diagnosis разрешён ограниченно; pass только после исправления причины и нового чистого прогона. Не называть flaky pass обычным pass.

При падении сохрани first failure и минимальное воспроизведение; UI — trace/screenshot/DOM/network где допустимо; API — очищенный request/response; events — correlation trace. Ошибки нельзя swallow, `|| true` запрещено для критериев выхода. Не закрывай runner до фактического окончания и teardown; по timeout фиксируй timeout, не pass. Заверши только запущенные этим run процессы и очисти только свои fixtures.
## execution.json
schema_version, document_revision, run_id, kind=delivery, status, source_fingerprint, test_fingerprint, spec_fingerprint, environment, commands[], cases[{test_id,selector,result,attempts,native_report,evidence}], totals{expected,discovered,executed,passed,failed,skipped,flaky,not_run}, blockers[], defects[], started_at, finished_at. Источники timestamps — системные/runner, не придумывать.
## Exit
on_success только при satisfied exit_policy, полных native reports, всех required TC passed, нуле required skip/flaky и blocking defects. Failed product/test → triage. Blocked environment → human blocker. Человек не отменяет красный обязательный тест кликом approve: изменённый scope проходит upstream gates.

## Основания и границы адаптации
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver
- [S20] Playwright: authentication: https://playwright.dev/docs/auth

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
