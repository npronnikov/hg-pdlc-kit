---
name: pdlc-traceability
description: Enforce typed requirement links, revision freshness, reverse impact analysis, and evidence provenance.
---

# Трассируемость и актуальность

Стабильные namespaced ID и typed links обязательны на каждом результате. INT/HYP/BR/ADR/FR/NFR/AC/STORY/CODE/E2E/CHECK составляют содержательный граф; execution trail — HG run/node/attempt/artifact. Направление требований вниз, reverse impact при ошибке вверх. При изменении семантики revision увеличивается, downstream требует пересмотра; старые links/evidence нельзя массово перепривязывать без проверки. Нет «100% coverage» только по ID: deterministic lint + независимый semantic review. Source bytes и graph fingerprints должны соответствовать test evidence. Изменившееся решение не покрывается старым approval.
