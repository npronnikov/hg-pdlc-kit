---
name: hg-pdlc-srs
description: "Переводит PRD и архитектуру в проверяемые системные требования, API, данные, права и NFR."
---

# Системная спецификация SRS + EARS

## Входы
PRD, business.json, архитектурные компоненты/ADR, решения gate, текущие интерфейсы и schema.
## Шаги
1. Заполнить `templates/srs.md`: purpose/scope/references, system context, interfaces, functional requirements,
   data, security, quality attributes, constraints, verification, traceability/open issues.
   Это адаптированный SRS по общепринятой структуре, не воспроизведение нормативного текста ISO/IEC/IEEE 29148.
2. Использовать EARS-подобные формулировки «Когда <trigger>, система должна <observable response>»;
   state-driven «Пока <state>...», unwanted «Если <error>...». Одно обязательство на SR.
3. SR: id, statement, business_ids, acceptance_ids, component_ids, verification, priority, source_refs.
   NFR: id/statement/verification/rationale/metric/operator/threshold/unit/conditions, измеримый threshold, нагрузка/среда/окно/метод проверки; «быстро/безопасно» без метрики недопустимо.
4. Описать API request/response/status/errors/auth/versioning, данные/null/default/constraints/migration/retention,
   state transitions, idempotency/concurrency/timeouts, аудит и события измерения из PRD.
   API — OpenAPI 3.1 template если HTTP существует; иное — явное N/A с обоснованием в contracts-index.md.
5. Требование архитектурного свойства (например, отсутствие dependency cycle) может иметь static/integration verification.
   ВСЕ бизнес-AC обязаны получить E2E, а NFR дополнительно подходящий вид проверки; не выдавать unit за E2E.
6. Сохранить трассу BR/AC → SR/NFR → CMP/ADR. Без родителя — обосновать derived requirement либо исправить.
## Выходы
project srs.md, system.json, contracts-index.md, применимые contracts/*; run srs-index.md.
Неразрешимое противоречие архитектуры или PRD — review handler наверх, не локальное переопределение намерения.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
