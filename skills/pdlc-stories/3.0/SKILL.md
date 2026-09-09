---
name: pdlc-stories
description: Epics, stories и план реализации. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Epics, stories и план реализации


## Работа
Построй stories.md и trace/stories.json в BMAD-стиле: epic/цель, STORY-ID, зависимость, «Как <actor> хочу <поведение> чтобы <ценность>», FR/NFR/AC/E2E, затронутые пути, задачи реализации, тестовый контекст и definition of done. Каждая story — проверяемый вертикальный slice, не отдельная роль. Для greenfield первая foundation story создаёт структуру/стенд, но всё равно имеет критерии готовности.
Проверь DAG зависимостей, миграцию/совместимость, тестовые данные, lockfiles и конечные build/e2e команды. Включи задачи создания нужного кода и E2E, не задачу «ручной smoke» или вечный `npm run dev` как финальную verification command.
risk.json: flags.authorization_changes, sensitive_data_changes, destructive_migration, public_contract_break, new_external_dependency, production_access — все boolean с основаниями. Unknown не превращать в false. Любой true требует technical gate. Низкий риск допускает автоматический технический переход только в границах принятой PRD политики. Задачи production_access не исполняются даже после gate в этом flow.
## Выход
project: stories.md, risk.json, trace/stories.json. Истории не отмечаются выполненными до реального изменения и проверок.
