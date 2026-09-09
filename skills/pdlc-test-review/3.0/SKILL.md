---
name: pdlc-test-review
description: Независимая проверка E2E. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Независимая проверка E2E


Вызови test-auditor с test-model, SRS, исполняемыми тестами, harness и границами системы. Проверь IDs, внешний oracle, setup/cleanup, отсутствие внутренних моков, реальные пути и запуск, негативные сценарии, bounded timeouts. Отдельно проверь, что тест упадёт при нарушении требования; mutation-проверка полезна, но мутация должна быть изолирована от рабочих файлов.
Не запускай вместо command-e2e собственный «финальный» тест и не выдумывай pass. test-review.json (run) содержит findings/прочитанное/verdict; on_rework→ai-e2e, on_model→ai-test-model, on_success→command-e2e. Reviewer не переписывает assertions.
