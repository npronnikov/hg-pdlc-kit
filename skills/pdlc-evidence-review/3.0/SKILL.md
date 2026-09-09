---
name: pdlc-evidence-review
description: Трассируемая приёмка и triage. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Трассируемая приёмка и triage


Прочитай текущие e2e-report.json, raw JUnit/stdout/stderr и project verification.json. Только command produced evidence может быть основанием фактических статусов. Отдельный acceptance-auditor сверяет frozen PRD/SRS, граф, выполненные тесты, code-map, рассмотренные findings.
При failed/blocked укажи обратную цепочку RESULT/E2E→AC/FR→ADR/BR→HYP/INT и связь STORY/CODE. Найди первопричину на основе лога и воспроизведения, не автоматической догадки по ID. on_code→implement; on_test→e2e author; on_model→test-model; on_system→SRS; on_architecture→architecture; on_intent→discover; environment/нет evidence→on_blocked. Передай KEEP-инструкции и минимальную правку через rework summary. Нельзя менять criteria задним числом.
Успех требует: реальные обязательные тесты passed, нет skip/missing/duplicate/unexpected IDs, источники/definitions не изменились после теста, PRD/design seals актуальны, блокирующих findings нет. CHECK не считается E2E. Утверждение автора «готово» не доказательство.
project acceptance.json: verdict accepted/rework/blocked, blocking_findings, deferred_risks, reviewed_execution_id, evidence_refs, business_outcome:'not-measured', integration_status:'not-integrated'. run acceptance-review.json — промежуточный разбор.
Даже при on_success итог решает command-finalize: он не пропускает несвежий/неполный E2E. Финальный статус — verified-not-integrated; ничего после тестирования не исполняется.
