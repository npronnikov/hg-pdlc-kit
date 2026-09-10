---
name: sdd-test-model
description: Формирует риск-ориентированную модель, сценарии и матрицу покрытия до
  реализации.
---

# Тестовая модель до написания кода

## Цель
Создать test-model.md, test-model.json, acceptance.feature и traceability.csv по принятому PRD и кандидатному SRS; зафиксировать oracle до реализации, затем принять SRS и модель вместе.
## Модель
Ось покрытия: capability → business journey → risk → SYS/AC → SCN → TC → native test selector → execution evidence. Слои unit/component/contract/integration/e2e различаются. E2E пересекает настоящую внешнюю границу системы и проверяет бизнес-результат через UI/API/CLI/event; не внутренний вызов сервиса. Не всё нужно проверять дорогим UI.

Для каждого TC опиши ID, rationale, requirement_ids, acceptance_ids, scenario_id, priority, layer, channel, preconditions, roles, fixture data, steps, oracle, cleanup, environment, automation, mock policy, native selector (planned до реализации), evidence requirements. Happy, alternative, boundary, invalid input, permission/tenant denial, повтор/конкуренция/восстановление — по рискам; каждый исключённый аспект имеет N/A с причиной и approval в модели.

UI-changing feature обязательно имеет UI e2e для ключевого принятого journey, состояния формы/ошибки/права и persistence после reload, если применимо. API-only feature не получает искусственный UI; API e2e проходит реальную app+data/integration boundary. Внешнюю платную/опасную систему можно заменить sandbox/contract-faithful double по согласованию, но core path продукта не замокировать и называть full e2e. Границы и ограничения отражаются в verdict.

NFR может требовать отдельный performance/security/accessibility test или inspection, а не UI e2e; mapping verification_method честный. Доля coverage считается по утверждённому набору обязательных требований, не по числу сгенерированных сценариев.
## Форматы
acceptance.feature: Gherkin на языке команды, комментарии с AC/SCN-ID; не добавляй новые metadata tags. BDD runner не обязателен: .feature может быть specification, native runner tests должны иметь однозначные selectors в model.
traceability.csv: row_kind,document_revision,br_id,ac_id,sys_id,adr_id,scenario_id,test_id,layer,channel,selector,status,evidence_ref. row_kind=metadata содержит только ревизию, row_kind=mapping — реальную связь; metadata не включается в coverage. Одна строка на связь; нет висячих ID. status planned до исполнения.
test-model.json: schema_version, document_revision, change_id, scope_requirements, cases[], exclusions[], exit_policy, risk_matrix[], coverage.
exit_policy: обязательные TC исполняются без skip; 0 тестов не успех; нет flaky обязательных сценариев; нет blocking defects; UI evidence для UI scope; code/tests/spec hashes совпадают с tested revision.
## Ревью
Spec-test auditor независимо ищет дырки/ошибки oracle. Не менять критерий так, чтобы он совпал с уже написанным кодом. Any oracle change возвращается на SRS/model human gate.

## Основания и границы адаптации
- [S15] Cucumber: Gherkin reference: https://cucumber.io/docs/gherkin/reference/
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S18] Playwright: API testing: https://playwright.dev/docs/api-testing

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
