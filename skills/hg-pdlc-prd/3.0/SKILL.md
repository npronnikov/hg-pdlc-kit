---
name: hg-pdlc-prd
description: "Формирует полный в согласованных границах PRD, решения ВП и атомарные бизнес-требования с приёмкой."
---

# Бизнес-контракт PRD + BR/AC

## Входы
Заполненная форма human-interview (by_value), intent, context, baseline, rework из PRD-review/human-prd/diagnosis.
## Шаги
1. Проверить required ответы, конфликтующие решения и их происхождение. Нельзя самому дописать ответ ВП.
2. Заполнить все секции `templates/prd.md`; для неприменимого — обоснование, для неизвестного — owner/impact/blocking.
3. Разложить BR по наблюдаемой бизнес-потребности, AC по Given/When/Then. Каждому BR — хотя бы один AC.
   Поля BR: id, statement, rationale, priority, source_refs, acceptance_ids. AC: id, business_ids,
   given, when, then, negative_or_boundary. Не подменять бизнес-требование именем класса/таблицы.
4. Проверить матрицу применимости: роли/запреты, happy/negative/boundary, состояния/переходы, валидация, время,
   лимиты, retries/idempotency, конкуренция, совместимость, данные/retention, доступность, измерение эффекта.
5. Зафиксировать гипотезу KPI: формула, baseline (unknown допустим), target/решение ВП, окно, guardrails,
   события. Не выдавать прохождение E2E за доказательство эффекта; release/outcome за границей flow.
6. Записать decisions.md со ссылками на вопрос, gate и фактический ответ. Согласование PRD — отдельное событие,
   которое нельзя выдумывать до human-prd; capture происходит на следующем этапе по runtime gate context.
## Выходы
project `docs/changes/<CHG>/prd.md`, `business.json`, `decisions.md`; run `prd-index.md` c executive decision summary.
Формат `business.json` — schema ресурса; в PRD те же ID. На любой смысловой rework снова пройти human-prd.
## DoR
Нет скрытых blocking unknown; цель/границы ясны; BR/AC атомарны; негативные сценарии покрыты; источники различимы.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
