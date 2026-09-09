---
name: pdlc-traceability
description: Сквозная трассируемость. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Сквозная трассируемость


# Связи от намерения до доказательства

## Модель
Авторитетный текст находится в документе с явным `<a id="ID"></a>`. `trace/<stage>.json` — его машинный реестр, а `trace/graph.json` и `trace/matrix.md` — производные сборки command-проверки. Не веди две независимо редактируемые формулировки: `statement` должен буквально присутствовать в указанной секции документа.
Каждый фрагмент имеет `schema_version: "3.0"`, `nodes: []`, `edges: []`. Узел: id, kind, revision (целое >=1), statement (атомарное обязательство), artifact.path (от корня единственной монорепы), artifact.anchor. Для CODE anchor не требуется, путь должен вести к реальному файлу. Дополнительно: rationale, source_refs, assumption_status; для NFR обязательно measurement; для E2E — boundary, preconditions, test_data, steps, expected.
ID не переиспользуется. Смысловое изменение поднимает revision; смена форматирования вне секции сама по себе не новое требование. Ребро содержит from, relation, to, from_revision, to_revision. Устаревшие ребра — ошибка, а не молчаливый update.

## Направления
INT —motivates→ HYP —justifies→ BR. BR —accepted_by→ AC; BR —realized_by→ ADR; BR —specified_by→ FR/NFR; ADR —constrains→ FR/NFR. AC —verified_by→ E2E; FR/NFR —verified_by→ E2E/CHECK. FR/NFR —implemented_by→ STORY —changes→ CODE —exercised_by→ E2E/CHECK. E2E/CHECK —evidenced_by→ RESULT; RUN —includes→ RESULT.

## Владение
PRD-автор: intent.json (INT/HYP/BR/AC). Архитектор: architecture.json (ADR и ребра от BR). Системный аналитик: system.json (FR/NFR и их основания). Тест-дизайнер: tests.json (E2E/CHECK и coverage). Планировщик: stories.json. Разработчик: code.json и implementation-map.json. Command-E2E: evidence.json, RUN/RESULT из реально обнаруженных testcases.
Не создавай E2E-результаты в AI-ноду. Не заполняй неизвестное ложным passed. CHECK может быть дополнительной нагрузочной/безопасностной/компонентной проверкой; он не считается E2E и не заменяет AC→E2E.

## Формат фрагмента
```json
{"schema_version":"3.0","nodes":[{"id":"FR-EMAIL-001","kind":"FR","revision":1,"statement":"Система должна сохранять выбранное пользователем значение настройки.","artifact":{"path":"pdlc/changes/CHANGE-ID/SRS.md","anchor":"FR-EMAIL-001"}}],"edges":[{"from":"BR-EMAIL-001","relation":"specified_by","to":"FR-EMAIL-001","from_revision":1,"to_revision":1}]}
```
Это ФРАГМЕНТ: ссылка на BR разрешается только вместе с intent.json. Не копируй placeholder CHANGE-ID в реальный продукт.

## Диагностика
Для ошибки E2E покажи обратную цепочку: RESULT ← E2E ← AC и FR/NFR ← ADR/BR ← HYP ← INT; далее STORY→CODE. Root cause определяется свидетельствами, не одним ID теста. `bad_spec` возвращает в SRS/архитектуру, `intent_gap` — к ВП, `patch` — в код, `test_defect` — в авторство тестов; окружение/недостаток полномочий блокирует, а не превращает результат в success.
