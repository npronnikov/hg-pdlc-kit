---
name: sdd-business-prd
description: Превращает ответы ВП в проверяемый бизнес-контракт с правилами, scope
  и acceptance examples.
---

# Исчерпывающий BRD/PRD

## Цель
Создать prd.md и business-requirements.json по проверенному контексту и фактическим ответам human_input. Полнота означает отсутствие неразрешённых обязательных решений в принятом scope, а не предсказание любых будущих потребностей.
## Шаги
Сверь запрос, существующие specs и ответы. Выдели as-is/to-be, affected capabilities, changes added/modified/removed. Не превращай техническую гипотезу в бизнес-потребность. Для каждого требования обеспечь источник, rationale, priority, owner, acceptance, зависимости и исключения. Проведи ревью через business-auditor; покажи findings без самоодобрения.
## Обязательная структура prd.md
1. Паспорт: ID изменения, версия, статус draft, авторские источники, владельцы решений.
2. Проблема и текущее состояние: доказательства, последствия, почему нужно изменение.
3. Цели и метрики: baseline/target/window/measurement/guardrails; неизвестная цифра не выдумывается.
4. Стейкхолдеры, персоны и роли; владельцы бизнес-решений и границы полномочий.
5. In scope / out of scope; ограничения, зависимости, предположения.
6. Пользовательские journeys: триггер, предусловия, happy path, альтернативы, ошибки, postconditions.
7. BR-ID: атомарные бизнес-требования; RULE-ID: правила/decision tables, границы, исключения, приоритет конфликтующих правил.
8. Информация: сущности и бизнес-смысл, источники, качество, владение, жизненный цикл, удаление.
9. Взаимодействия: другие продукты/люди, уведомления, ответственность, отказы и восстановление.
10. Бизнес-ограничения качества: доступность/latency/объёмы/privacy/security/a11y/локаль; измеримые критерии или вопрос ВП.
11. AC-ID: observable Given/When/Then на happy/negative/boundary/permission cases, без привязки к внутреннему методу.
12. Риски, спорные вопросы и решения; unresolved must-have = запрет on_success.
13. Приёмочная матрица BR→RULE→AC→Q-ID; changelog и delta относительно baseline.

Для малого изменения раздел может содержать «не применимо: причина и источник», но не быть молча пропущен. Технические endpoint signatures, classes и выбор БД не подменяют бизнес-требования.
## business-requirements.json
schema_version, document_revision, change_id, capability_ids, goals[], requirements[{id,statement,rationale,source_refs,priority,owner,acceptance_ids,rule_ids,status}], rules[], acceptance[{id,given,when,then,negative,source_refs}], decisions[], unresolved[].
## Exit
ready только если каждый обязательный пункт либо раскрыт, либо обоснованно not-applicable; все существенные вопросы решены человеком, auditor не нашёл blocking gaps. Human gate всё равно обязателен. На архитектурной/кодовой стадии нельзя «уточнять» BR без возврата сюда и нового approval.

## Основания и границы адаптации
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S15] Cucumber: Gherkin reference: https://cucumber.io/docs/gherkin/reference/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
