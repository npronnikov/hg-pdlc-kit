---
name: hg-pdlc-quality
description: "Проверяет полноту контрактов, трассу и фактические E2E; содержит детерминированные валидаторы."
---

# Независимые ревью и машинные проверки

## Входы
Артефакты конкретного этапа, источники baseline, runtime execution-context, diff и receipts доступных command-нод.
## Шаги
1. Выбрать checklist этапа из templates. Запустить привязанных subagents с явной задачей и границами контекста.
   Разделять автора и критика; ни один reviewer не должен выводить approve лишь из самоотчёта автора.
2. Консолидировать findings: id, severity critical/major/minor, artifact/locator, basis_hash, linked_ids,
   evidence, required_change, verification, target_stage. Не дублировать один дефект в трёх ревью.
3. Проверить BR/AC/SR/CMP/TASK/E2E graph на orphan/unknown IDs и coverage; templates/verify.mjs выполняет часть
   структурных проверок. Семантическую полноту и архитектурную корректность не выдавать за JSON-schema validation.
4. Проверить rework target: намерение → ai-prd/ai-interview; design → ai-architecture; SR → ai-srs;
   oracle → ai-test-model; plan → ai-plan; code → ai-implement; E2E code → ai-e2e; среда → ai-environment.
   Возвраты всегда через handlers текущего FLOW. Не запускать целевой шаг самостоятельно.
5. E2E acceptance: receipt exit=0, новый report, нужные кейсы passed/attempts=1, корректная реальная chain,
   JSON/log hashes соответствуют, source/contract fingerprint не изменился после выполнения.
   Все обязательные AC имеют выполненный E2E. Внесение поправок после E2E требует нового command-e2e.
6. Сохранить run review и step-summary route; при nonblocking minor указать follow-up, но не маскировать critical.
## Выходы
Только промежуточный run review конкретной ноды; финальный useful verification.md/evidence/ создаётся consolidation.
`templates/verify.mjs` — обычный checker, не выбирает шаг, не хранит workflow-state, не вызывает агента/гейты.
`tests/` — проверки авторства каталога, не runtime продукта; они не доказывают запуск HG SDLC.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
