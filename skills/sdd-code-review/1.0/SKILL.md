---
name: sdd-code-review
description: Сверяет diff с требованиями и проверяет correctness, security, данные
  и влияние на регрессию.
---

# Независимое ревью реализации

## Цель
code-review.md и code-review.json на основе действительного diff и принятых docs. Вызови code-auditor и spec-test-auditor в отдельных контекстах; сначала дай specification, затем diff. Автор реализации не объявляет ревью выполненным за субагента.
## Проверки
Coverage TASK/SYS/AC; authz на правильной границе; business invariants; errors/timeouts/retries; data races/transactions/tenant boundaries; API compatibility/migrations; secrets/dependencies; frontend состояния; тестируемость и качество assertions; unintended files. Измеряй факты file:line, отделяй blocker от optional improvement. Проверяй unit/integration evidence по native reports, а не тексту implementation summary.
## Выход
findings[{id,severity,path,line,requirement_ids,issue,impact,fix,disposition}], reviewed_diff_hash, verified_commands, unresolved_blockers, verdict. Нельзя изменить product code в reviewer node. На blocker — rework в code; если дефект требования — соответствующий upstream route. После исправления новое ревью обязательно.

## Основания и границы адаптации
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/
- [S22] OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
