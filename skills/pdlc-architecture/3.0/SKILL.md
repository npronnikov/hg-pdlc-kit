---
name: pdlc-architecture
description: Архитектура изменения. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Архитектура изменения


## Вход
Только согласованный PRD, решения, анализ монорепы и реально существующая архитектура. Проверь approvals/prd.json. При конфликте смысла возврат к ВП, а не скрытая правка PRD.
## Работа
architecture.md следует arc42-профилю из 12 разделов: introduction/goals, constraints, context/scope, solution strategy, building blocks, runtime view, deployment view, cross-cutting concepts, architecture decisions, quality requirements, risks/debt, glossary. Для фичи полностью проработай затронутые разделы, для остальных дай осмысленную ссылку на базу/N/A.
architecture.dsl: валидный текст Structurizr DSL с C4 Context + Container. В монорепе контейнеры — исполняемые/хранимые компоненты, не Git-репозитории. Отрази trust boundaries и внешние системы. Code-level схему не рисуй вместо архитектуры. Runtime-сценарии Mermaid допустимы внутри architecture.md.
adr.md: ADR-ID, контекст и BR-основания, минимум реалистичные альтернативы, решение, последствия/риски, сохраняемые инварианты, отмена/совместимость. Новая зависимость/необратимая миграция/изменение прав получает явный риск, не «техническую мелочь».
Brownfield: раздели as-is и to-be, укажи существующие пути apps/services/packages, совместимость старых данных/клиентов и regression obligations. Greenfield: as-is отсутствует; выбери минимальную целевую систему, обоснуй стек и environment foundation.
trace/architecture.json содержит ADR и BR→ADR. Реестр компонентов/путей ведётся в architecture.md, не отдельной многорепозиторной карте.
## Выход
project: architecture.md, architecture.dsl, adr.md, trace/architecture.json. Никакого application code на этом этапе.
