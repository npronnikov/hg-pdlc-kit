---
name: pdlc-prd-review
description: Независимая проверка PRD. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Независимая проверка PRD


## Работа
Прочитай prd-check.json текущего command-прогона. Любой статус кроме passed запрещает on_success. Отдельному business-auditor передай PRD, decisions, analysis, исходную фичу и ограниченный контекст; не передавай самопохвалу автора.
Проверь сохранность намерения, полноту BR/AC, согласованность источников и scope, измеримость цели, исключения и последствия. Устрани неоднозначность в finding, не редактируя PRD самостоятельно.
`prd-review.json` (run): verdict, blocking_findings [{id, severity, entity_ids, source, issue, required_fix, classification}], checked_artifacts, machine_check, bundle_digest. При успешной проверке скопируй bundle_digest из prd-check.json в step-summary БЕЗ пересчёта/выдумывания. Его подтвердит seal после human-gate.
Маршрут on_rework — исправление PRD автором; on_intent — вопросы ВП через discover; on_success — human-prd-approval. Сам агент не может утвердить продуктовую цель.
