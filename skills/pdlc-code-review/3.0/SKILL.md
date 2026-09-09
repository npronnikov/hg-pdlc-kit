---
name: pdlc-code-review
description: Трёхстороннее ревью кода. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Трёхстороннее ревью кода


Построй diff от manifest baseline, включая новые файлы. Запусти три каталожных subagent: blind-hunter (diff без спецификации), edge-case-hunter (diff+read-only relevant code), acceptance-auditor (diff+PRD/SRS/stories/trace). Не подменяй вызов ролью, разыгранной в одной сессии. При недоступном subagent отметь gap и on_blocked; штатного «считаем изолированным reasoning-проходом» нет.
Дедуплицируй findings, укажи file:line, entity IDs, последствия и свидетельство. Классификация BMAD-референса: patch, bad_spec, intent_gap, defer, reject; дополнения: test_defect, environment. Критичные/существенные findings блокируют. Сам reviewer код не исправляет, чтобы не смешать автора и проверяющего.
code-review.json (run): прочитанные файлы, вызываемые роли, findings, verdict. on_code→implement; on_system→SRS; on_architecture→architecture; on_intent→discover; on_success→авторство E2E. Deferred риск сохраняется в финальном acceptance, не исчезает из-за категории.
