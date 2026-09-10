---
name: sdd-architecture
description: Проектирует решение по принятому PRD, сравнивает варианты и фиксирует
  архитектурные последствия.
---

# Архитектура C4 + arc42 + ADR

## Цель
Создать architecture.md, c4-context.mmd, c4-containers.mmd, runtime.mmd и decisions.md после подтверждения PRD. В recover описывать наблюдаемую архитектуру, не переизобретать систему.
## Workflow
Проверь trusted PRD approval и hashes. Прочитай existing architecture/ADR/code. Сохрани current stack и конвенции, если требование не обосновывает изменение. Рассмотри минимум два разумных подхода для значимого решения (включая отсутствие нового сервиса/зависимости); объясни choice, trade-offs, reversibility, стоимость и риски. Для тривиального изменения допустима no-impact запись с доказательством.

arc42-adapted architecture.md: цели и quality drivers; constraints; context/scope; solution strategy; building blocks; runtime views; test-environment/deployment view только как контекст; cross-cutting concerns; decisions; measurable quality scenarios; risks/debt; glossary. Это документация устройства среды, не выполнение deployment.

C4 L1/L2 — Mermaid flowchart: каждый элемент имеет тип Person/SoftwareSystem/Container, имя, responsibility; контейнер содержит technology; связи имеют назначение и protocol. Явные system/trust boundaries, external dependencies, data stores. C4 Container не равно Docker container. L3 только для затронутого сложного компонента. Не называй произвольный flowchart C4 без этих семантических атрибутов. Не используй экспериментальный Mermaid C4 синтаксис; notation-independent C4 реализуется обычным flowchart.

Runtime sequence: основной пользовательский сценарий + значимый отказ/retry/idempotency; стрелки с сообщениями и межсервисными границами. Данные: сущности, ownership, transactional boundaries, migrations/compatibility. Security: trust boundaries, authn/authz, tenant isolation, validation, sensitive data; testability: управляемые часы, fixtures, доступные UI-семантики, observability результатов, без тестовых backdoors в production.

ADR запись: ID, status proposed/accepted/superseded, context, options, decision, consequences, linked BR/SYS (если ещё нет SYS — pending link), evidence. До gate только proposed. В recover не выдумывай исторические ADR: reconstructed decision + evidence + confidence.
## Exit
architecture-auditor проверяет PRD coverage, отсутствие gratuitous complexity, реалистичность NFR и тестируемость. При конфликте с BR возвращай upstream; при вопросе к архитектуре rework. Все .mmd синтаксически проверить доступным parser/renderer; отсутствие renderer явно помечается и требуется визуальная проверка человеком, не ложное «rendered».

## Основания и границы адаптации
- [S11] C4 model: diagrams: https://c4model.com/diagrams
- [S12] arc42: template overview: https://arc42.org/overview/
- [S13] Mermaid: flowchart: https://mermaid.js.org/syntax/flowchart.html
- [S22] OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
