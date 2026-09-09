---
name: pdlc-e2e-author
description: Исполняемые E2E после кода. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Исполняемые E2E после кода


Создай настоящие исполняемые тесты по ЗАМОРОЖЕННЫМ test-model и AC, не по деталям новой реализации. В web-monorepo пройди UI, API и настоящую БД; API/CLI профиль использует соответствующую границу. Используй существующий framework и lifecycle: поднять изолированный стенд, дождаться readiness, подготовить данные, выполнить assertions, очистить, завершиться. Command-node не должна зависнуть на dev server.
Каждый testcase выводит ровно один [E2E-ID] (или отдельный [CHECK-ID]) в JUnit. Не допускай test.only, пропусков при отсутствующем endpoint, необоснованного quarantine, пустого suite, скрытых retry, assertions только на 200 без бизнес-результата. Проверяй сохранность после reload/перезапуска там, где это требование, и изоляцию чужих данных.
Сохрани e2e-map.json {tests:{ID:[точные пути исполняемых файлов]}} и e2e-implementation.md (project). Тестовый код — обычные project-файлы под существующим tests/...; это полезный результат, не run artifact. Raw JUnit/trace/screenshots/logs будут созданы command-e2e в run scope.
Не меняй verification-plan, AC или ожидаемый результат ради удобства. Для изменения тестовой модели — on_model, для SRS — on_system, иначе on_success к независимому test-review.
