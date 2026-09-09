---
name: hg-pdlc-architecture
description: "Проектирует архитектурный delta после PRD: границы, компоненты, контракты, инварианты и решения."
---

# Архитектура: arc42-lite + C4 + ADR

## Входы
Утверждённый PRD/BR/AC, baseline AS-IS, технические ограничения монорепы, gate event human-prd.
## Шаги
1. Сверить fingerprint утверждённого PRD с текущим файлом. Утверждение не переносится автоматически на новый текст.
2. Заполнить `architecture.md`: контекст/границы, ограничения, стратегия, building blocks, runtime,
   deployment для ТЕСТОВОЙ среды, cross-cutting concerns, quality scenarios, риски, решения.
3. Диаграммы: C4 L1 Context и L2 Containers в Mermaid flowchart c явными типами и границами;
   sequenceDiagram минимум для основного сценария и значимого сбоя. Это C4-модель в Mermaid,
   а не заявление об использовании синтаксиса C4 DSL или полной arc42-сертификации.
4. Для решений с реальным выбором — ADR: context, options, decision, consequences, linked BR/AC/NFR,
   retained invariants, compatibility/migration, testability. Отделить TO-BE от observed AS-IS.
5. В `components.json` указать id, type, responsibility, repo_paths, dependencies, interfaces и BR coverage.
   Взаимодействия внутри монорепы не требуют multi-repo orchestration; один исходный snapshot.
6. Выявить риск: auth/PII, необратимая миграция, breaking API, необоснованный техстек, внешние расходы.
   Обычный flow направит на human-architecture по on_risk; governed делает gate всегда.
## Выходы
project architecture.md, context.mmd, containers.mmd, sequence.mmd, decisions/ADR-*.md, components.json,
approval-record.json с реальной ссылкой на согласование PRD. run architecture-index.md.
Не писать детальную SRS раньше архитектуры; архитектурная невозможность бизнес-границы возвращается в PRD,
а не решается скрытым изменением BR. C4 L3 только если сложность затронутого контейнера оправдывает.

## Общие ограничения
Работать только внутри текущей HG SDLC-ноды и одной монорепы. Общие правила — в подключённом `hg-pdlc-method@3.0`.
Шаблоны читать относительно фактически материализованного `SKILL.md`, а не из выдуманного пути каталога.
Не доступны обязательный ресурс или сабагент — зафиксировать блокер; не изображать вызов или проверку.
Не менять согласованный upstream: сообщить finding и вернуть работу соответствующему владельцу артефакта.
Полезные результаты — `scope: project`; промежуточные материалы — `scope: run`. Пути брать из контракта ноды.
Записать все declared artifacts и step-summary; один текст «готово» не является результатом.
