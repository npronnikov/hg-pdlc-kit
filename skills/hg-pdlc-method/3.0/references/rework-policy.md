# FreeMarker и возвраты
1. Read source summary через `step["source-id"]!{}`; ?has_content защищает отсутствующее замечание.
2. `keep_changes!false`: true → минимальная коррекция; false → полная постановка + замечание на восстановленной базе.
3. Исходный контракт и обязательные выходы находятся ПОСЛЕ условного блока, чтобы обе ветви сохраняли полноту.
4. Несколько источников возврата указаны в target instruction отдельно. У каждого feedback должен быть finding_id и basis_hash.
5. Старый summary в step — исторический контекст: writer проверяет scope/hash и already-resolved finding, не повторяет исправленное.
6. AI custom handlers содержат max_loop_count, keep_changes и session_policy; human gates — on_rework без max_loop_count.
7. Новое бизнес-решение → PRD + human-prd; не автоподтверждать изменённые acceptance criteria.
8. HG owns rollback/session; skill не выполняет git reset и не выбирает alternate runtime.

## Пример
human-prd возвращает F-PRD-01 с keep_changes=true: PRD writer точечно уточняет роль, обновляет BR/AC,
повторно выпускает все свои outputs, PRD reviewer перепроверяет, ВП снова утверждает.
Тот же feedback c keep_changes=false: HG восстанавливает checkpoint, writer выполняет исходный PRD contract,
обязательно добавляет ограничение роли. Замечание НЕ теряется в else-ветке.

## Каскад
PRD → architecture → SRS → test-model → plan → contract check → implementation → build → review → E2E → evidence.
Code rework → build → code review → E2E. Test automation repair → E2E. Environment repair → E2E.
Ранние результаты полезны в project, но до новой успешной проверки нельзя считать их актуально accepted.
