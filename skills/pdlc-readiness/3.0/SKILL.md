---
name: pdlc-readiness
description: Implementation readiness и техническое решение. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Implementation readiness и техническое решение


## Работа
Сначала design-check.json: любой error блокирует реализацию. Вызови architecture-auditor, system-auditor и security-reviewer с ограниченным независимым контекстом. Сверь PRD↔ADR↔SRS↔контракты↔AC↔E2E↔STORY. Оцени полноту, тестируемость, инварианты, реалистичность стенда и отсутствие неопределённых бизнес-решений.
readiness-review.json (run): findings с классификацией, список прочитанного, актуальные ревизии, bundle_digest из command-check, risk flags, verdict. В успешном summary скопируй bundle_digest. Нельзя подменить неуспешный машинный отчёт мнением.
Маршруты: on_architecture / on_system / on_model / on_plan / on_intent — возврат владельцу, с feedback_id, rework_target, ясной строкой rework_instruction. on_approval — human-design-approval при риске. on_success — policy-seal только для всех false, либо human-gate в controlled-flow. Не выдавай policy decision за человеческое согласование.
Если риск невозможно ограничить sandbox/полномочиями или нужно production действие — on_blocked.
