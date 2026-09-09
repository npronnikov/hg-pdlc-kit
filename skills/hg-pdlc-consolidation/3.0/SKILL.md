---
name: hg-pdlc-consolidation
description: "Сохраняет подтверждённый change-set и актуальные продуктовые ссылки после реальных E2E."
---

# Актуализация продукта и доказательства

## Входы
PRD/архитектура/SRS/модель/план/код, approvals, passed E2E receipt/report и независимое acceptance-review.
## Шаги
1. Нельзя финализировать без актуальной связанной проверки. Проверить source и contract fingerprints.
2. При непустом system.nfr также сохранить фактический nfr-report.json из command-regression; numeric threshold проверит валидатор.
2a. Скопировать выбранный receipt/report и полезную часть лога из разрешённых run-артефактов в project
   `docs/changes/<CHG>/evidence/`. Не изобретать отсутствующий файл. Redaction — отдельная пометка/новый checksum.
3. Создать verification.md: что реализовано/проверено, AC→SR→E2E→result, реальные команды, среда, версии,
   исключения, provenance human/agent decisions, даты и ссылки. Непроверенное маркировать not_run.
4. Обновить каноническую product-документацию и index.json на основе delta только затронутых capability/requirement,
   сохранив unrelated capabilities и ссылки на прошлые CHG. Текущая архитектура не должна противоречить TO-BE принятого изменения.
5. Зафиксировать `change.json.status=e2e_verified_not_released`, never released/validated_business_outcome.
   Если консолидация меняет code/tests/contracts/approved expectations — не переносить старый evidence на новую версию.
6. Передать run final-index.md; command-final проверит копии и fingerprints. Нельзя менять код/ослаблять checker
   на rework финализации; вернуть upstream через evidence-review/diagnosis.
## Recovery-only
После human-baseline создать baseline-record.md и product index c `status: observed_reviewed`, не E2E-verified.
Не заполнять feature evidence искусственно. Цикл восстановления завершается без кода и тестов новой фичи.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
