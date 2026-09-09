---
name: pdlc-implement
description: Разработка по stories. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Разработка по stories


## Работа
Проверь принятые PRD/design seals и свежие stories. Читай только релевантный код и стандарты монорепы, не «весь Repomix» без фильтра. Выполняй stories по зависимостям. Для каждой: назови проверяемое поведение, измени существующие файлы (brownfield) или создай минимальную структуру (greenfield), добавь unit/integration tests, выполни доступные локальные проверки. Это не замена следующему command-build и E2E.
Используй фактический стек: Java/JS/TS/Go/Python и текущие инструменты сборки. Не создавай *_modified копии, не меняй contract/AC после провала. Не трогай verifier, approved artifacts и test oracle. Если невозможно реализовать без изменения намерения/архитектуры — on_intent/on_architecture/on_system с основаниями.
implementation-map.json: changes [{story_ids:[STORY-ID], paths:[точные пути], rationale, verification}], baseline_commit из manifest, test_files и известные gaps. implementation.md: что реально изменено и почему, необработанные риски, ссылки. trace/code.json: CODE-ID на реальный product file, STORY→CODE и CODE→E2E/CHECK. При доработке increment revisions изменённых CODE, не придумывай commit hash незакоммиченного дерева.
Нельзя объявить done только из-за завершения сессии. Статус выполнения — результат command-check/build/review.
