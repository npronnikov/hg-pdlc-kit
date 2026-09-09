---
name: pdlc-baseline-review
description: Приёмка восстановленной базы. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Приёмка восстановленной базы


Сначала baseline-check.json, затем независимые repository-scout/system-auditor и business-auditor. Сверь выборку утверждений с реальными путями и sha256, всю ключевую границу системы и источники бизнес-мотивов. Нет ли invented behavior, потерянной архитектуры, объявленных тестами заглушек или выданного за approved inference?
bootstrap-review.json (run): coverage, findings, unknowns, bundle_digest из machine-check. При замечаниях on_rework→ai-baseline; иначе on_success→human-baseline-approval. Только после human-gate command-baseline-seal создаёт project baseline.json. Бизнес-неизвестное не исчезает от общего approve.
