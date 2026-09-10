---
name: sdd-readiness-review
description: Проверяет PRD, архитектуру, SRS, контракты и тестовую модель как единый
  пакет.
---

# Проверка связности до кода

## Цель
Сформировать readiness.md + readiness.json и пакет для human acceptance SRS/test model. Прочитай исходные документы, а не только summary writer.
## Проверки
Полнота BR/RULE/AC; каждое SYS имеет BR/AC либо обоснованный platform constraint; архитектурные решения поддерживают NFR; интерфейсы и data model непротиворечивы; каждый must-have имеет verification method и минимум один TC/evidence; UI scope имеет UI e2e; нет orphan tests или требований; executable selectors пока могут быть planned, но намерение testable. Env requirements исполнимы либо явно включены в план; product decisions resolved, no critical TBD.

Вызови spec-test-auditor и architecture-auditor. Сохрани findings: id,severity,source file:line,requirement IDs,impact,proposed owner,disposition. Игнорировать blocker нельзя; optional suggestions не раздувают scope. Verdict ready / needs_rework / upstream_change / blocked.
## Выход
readiness.json: checks[], findings[], coverage_counts, unresolved_blockers, reviewed_hashes, invoked_subagents. `ready` — рекомендация для человека, не approval.
## Routing
Вычисли минимальную безопасную фазу возврата согласно handlers ноды: дефект SRS/model — их writer; конфликт architecture — architect; business meaning — PRD/interview; missing tool/env — blocker. После upstream change обнови downstream docs и gate; нельзя старым approval подтвердить новый hash.

## Основания и границы адаптации
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
