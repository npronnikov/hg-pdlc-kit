---
name: sdd-bug-reproduce
description: Отделяет баг от новой фичи и получает доказанный сбой до изменения production
  кода.
---

# Дефект: ожидаемое поведение и red-reproducer

## Цель
defect.md, reproduction.json и воспроизводящий test по подтверждённому expected behavior. Пока не исправлять production код.
## Работа
Сверь reported actual/expected, принятые BR/SYS/AC и ответы ВП. Если новое желаемое поведение отсутствует в согласованной базе, это scope decision: не выдавай feature за bug. Узкий defect flow допустим только при ограниченной поправке в существующую capability; новая бизнес-политика/контракт/архитектурная граница — blocker с рекомендацией полного feature flow.

Зафиксируй affected version, environment, inputs, role, preconditions, steps, expected from source, actual, frequency, impact, earliest observed, security/privacy scope. Создай минимальный red-reproducer на реальной внешней границе, где разумно; unit reproduction допустим как дополнительный diagnostic, но финальная regression имеет e2e. Запусти против исходного snapshot без product patch. Сохрани nonzero/failed native report и докажи, что падение от неверного поведения, а не синтаксиса/недоступной среды.

Если не воспроизводится: не изобретай root cause. Подготовь адресные вопросы и instrumentation proposal без destructive changes; human blocker. В крайнем environment-specific дефекте перечисли препятствие и разрешённые evidence; отсутствие red не превращается автоматически в принятие.
## Выход
reproduction.json: expected_refs, baseline_fingerprint, command_evidence, failing_selector, failure_reason, root_cause_hypothesis, classification, affected_paths, scope_eligibility. В defect contract затем явно фиксируются BR/architecture/SRS delta/no-impact и регрессионная test model, которые принимает человек до code.

## Основания и границы адаптации
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
