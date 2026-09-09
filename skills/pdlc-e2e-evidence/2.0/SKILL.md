---
name: pdlc-e2e-evidence
description: Require real end-to-end execution evidence with fresh identifiers, fingerprints, and honest system boundaries.
---

# Реальные E2E и доказательства

Тестовая модель определяется до кода; executable E2E создаются после реализации, затем исполняются command node. UI feature требует browser path; API-only не доказывает UI. Внутренние системы и persistence не заменяются mock, внешние doubles явно фиксируются в boundary. Unit/integration/performance/security checks дополняют E2E. Каждый mandatory testcase имеет уникальный [TEST-ID], fresh JUnit, process exit и source+graph fingerprint. Empty/missing/unknown/duplicate/skipped/flaky/retried cases блокируют gate; админское ограничение стенда — blocked. Test pass не доказывает бизнес-эффект. Hash controls не защищают от агента с теми же OS правами на verifier/evidence: production должна разделять доверенные command executors и model-writable checkout.
