---
name: hg-pdlc-plan
description: "Готовит задачи по модулям монорепы и обычные проверочные команды для command-нод HG SDLC."
---

# План, контракты команд и проверочные ресурсы

## Входы
PRD, архитектура, SRS, модель E2E, доступные build/test команды и замечания contract-review.
## Шаги
1. Разложить на TASK с dependency DAG, SR/AC, файлами create/modify, проверкой done и owner-role.
   Greenfield scaffold — явные задачи; brownfield — минимальный delta и регрессия, без смены стека по умолчанию.
2. Подготовить полезные project `tools/hg/build.sh`, `tools/hg/e2e.sh` и `tools/hg/verify.mjs`.
   verify.mjs копируется БЕЗ изменения из resources skill hg-pdlc-quality; это валидатор артефактов, не runtime.
   build/e2e — конечные shell wrappers над штатными командами проекта. Никогда не запускают следующий этап или агента.
3. build.sh работает из Git-корня и возвращает ненулевой rc при провале; если system.nfr непустой,
   пишет свежий NFR-report по пути первого аргумента (templates/nfr-report.schema.json skill quality); stdout собирает HG command.
   e2e.sh получает путь свежего JSON-отчёта первым аргументом, сам создаёт изолированную среду,
   дожидается readiness, запускает E2E, чистит ТОЛЬКО своё окружение и возвращает реальный rc.
4. Использовать template test-report.schema.json и reporter-contract.md. Нулевые тесты, missing report,
   skipped/failed/flaky обязательные кейсы — провал. Expected case IDs берутся из approved test-model.json.
5. Указать команды для Java/JS/Go/Python по обнаруженному build manifest, не по вкусу агента.
   Docker не обязателен: реально использованная БД/процессы важнее упаковки. Никакого production URL/credential.
6. Зафиксировать provenance проверочных файлов и hash ресурсов в implementation-plan.json; content snapshot
   командой до и после тестов привязывает результат к коду, specs и test-model. Self-reported verdict не заменяет execution.
## Выходы
project implementation-plan.md, implementation-plan.json и tools/hg/*.sh, verify.mjs;
run plan-index.md. Команды запускает HG SDLC, а не этот skill. Не устанавливать отдельный PDLC framework.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
