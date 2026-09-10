---
name: sdd-acceptance-pack
description: 'Собирает проверяемый результат для ВП: scope, работающий outcome, покрытие
  и свежие доказательства.'
---

# Пакет финальной приёмки

## Цель
acceptance.md, acceptance.json, baseline-plan.json и traceability.csv. Пакет делает человеку видимыми все значимые решения и результат выполнения; не создаёт approval.
## Проверки
Вызови evidence-auditor по native reports, accepted docs и source/test fingerprints. Не доверяй summary исполнителя без report. Все обязательные TC есть, прошли, связаны с AC/SYS; no missing/skipped/flaky/blocking. Code, test and spec hashes совпадают с последним полноценным run; любые последующие изменения исходников/тестов возвращают на verification, а requirements — upstream.

Собери компактный executive summary «что обещано → что сделано → как доказано», demo reproduction steps безопасной среды, coverage matrix, screenshots/traces links для UI, applied scope, limitations и незатронутые NFR. Человек видит точный список файлов/ревизий/хэшей. В run acceptance.md включи содержательные выдержки BR/architecture/SRS и таблицу TC, не только непрозрачные ссылки.

Подготовь точный canonical documentation update plan, но ещё не применяй. baseline-plan.json: registry_before_sha256, source_revision, approved_candidate_files[{path,sha256}], canonical_updates[{target_path,before_sha256|null,candidate_path,after_sha256,operation}], authoritative_map, conflicts. Обновляй только затронутые capabilities; сохраняй незатронутую нормативную часть. Для OpenSpec sync delta в existing canonical specs, не перенос в parallel docs. Для удаления — tombstone/history. Canonical target content должен быть полностью подготовлен до final gate; seal не сочиняет новый текст.

acceptance.json: kind(delivery|baseline), candidate_packet_hashes, gate_receipts, traceability, test_evidence, pending_blockers, canonical_plan_sha256, verdict=ready_for_human. Recovery baseline не притворяется прошедшей доставкой: execution kind=baseline_inventory, tests status unknown/not_run, принятие касается точности документации.
## Exit
Delivery: только verified pass. Baseline: все factual claims traced, неизвестные явно исключены из подтверждённого знания; baseline gate допускает зафиксированный долг, но не «всё протестировано». Final human approval принимается только отдельной нодой.

## Основания и границы адаптации
- [S04] HGSDLC: artifacts: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/artifacts/spec.md
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S16] Playwright: best practices: https://playwright.dev/docs/best-practices
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
