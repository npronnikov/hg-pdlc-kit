---
name: hg-pdlc-e2e
description: "Пишет исполняемые E2E и reporter, сохраняя ранее согласованные ожидания."
---

# Автоматизация E2E после кода

## Входы
Успешный build, implementation, независимо подготовленная test-model, SRS, commands и code-review.
## Шаги
1. Реализовать все required scenarios под стабильными E2E-ID в tests/e2e или существующей папке runner (отразить в index).
2. Использовать настоящий публичный вход и тестовый экземпляр приложения/БД; не monkeypatch handler/service/repository.
   UI: browser automation с user-level selectors и реальным network. API-only: внешний HTTP client и реальные side effects.
3. Устойчивость: независимая фикстура на сценарий, свежая БД/namespace, readiness polling с deadline,
   осмысленные ожидания, никаких sleep как главного oracle, cleanup finally/trap.
4. reporter пишет output contract из `templates/test-report.schema.json`: timestamps, runner, environment,
   cases c id/status/attempts/duration_ms/assertions/chain. expected IDs берутся из test-model, не из произвольного grep.
5. Исходники E2E и reusable fixtures — project. Сырые execution logs/report — run и создаются command-e2e,
   а не агентом заранее. На nonzero или crash создаётся incomplete report/receipt, не прошлый green report.
6. Исправление test bug разрешено только без ослабления согласованного oracle; источник дефекта указать в diagnosis.
   Внешняя sandbox dependency описана и явно видна в отчёте. Не использовать продуктивные данные.
## Выходы
project E2E source/fixtures и e2e-automation.md; run e2e-index.md. Следующий шаг HG сам запускает tools/hg/e2e.sh.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
