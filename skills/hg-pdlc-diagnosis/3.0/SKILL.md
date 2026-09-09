---
name: hg-pdlc-diagnosis
description: "Возвращает дефект к источнику и исправляет только тестовую среду без ослабления требований."
---

# Диагностика и ограниченный ремонт среды

## Входы
Свежие command receipts/logs, review, spec/test-model, код и история предыдущих corrections.
## Шаги
1. Отличить assertion failure от старта среды, отсутствия dependency, timeout, mismatch версий, ошибочного oracle,
   implementation bug и ошибки SRS/архитектуры. Отсутствие запуска = blocked/not_run, не failure продукта.
2. Записать diagnosis.md (run): наблюдение, команда/rc, evidence path, связанные ID, root cause или unknown,
   необходимая правка, тест перепроверки, target. Причину unknown не выдавать за установленную.
3. Для environment repair: исправить readiness, namespace/ports, test dependency/config, timeout только при обосновании.
   Не расширять production-доступ, не выключать auth, не удалять assertions и не подавлять rc.
4. Если требуется секрет, полномочие или новое бизнес-решение — создать exception.form.json (run) и useful blocker.md (project).
   Человек передаёт только необходимые решения; секреты вводятся через штатную настройку runtime, НЕ текст формы.
5. На корректируемом сбое: route + rework_instruction с root cause и повторной проверкой. Лимит хранит HG handler.
   После человеческого решения сначала diagnosis, а не безусловный success.
## Выходы
run diagnosis.md / environment-repair.md / exception.form.json; при блокере project blocker.md.
Полезное изменение tools/hg или тестовой конфигурации — project и снова review/execute по графу.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
