# Политика scope
Полезность, а не «окончательность», определяет scope. Draft PRD полезен для изменения → project.
Вопросник — временный интерфейс сбора решения → run. Само подтверждённое решение → project decisions.md.
Развёрнутые промежуточные AI-рецензии → run; финальное полезное заключение/решения/доказательства → project.
Raw test report и log относятся к попытке → run; выбранные финальные receipts/report в evidence становятся project.
Индексы stage handoff → run, канонический product index → project.

## Физические пути
FLOW задаёт логические `path`+`scope`. AI использует разрешённые runtime пути, предоставленные execution_context.
Command-узлы следуют приложенным образцам: создают объявленные run-файлы в рабочей директории command,
после чего HG SDLC материализует их согласно produced_artifacts. Это staging, не самостоятельный project-scope артефакт.
Имена `pdlc-run-*` зарезервированы для такого staging и исключены из Git `.gitignore`. Не commit-ить их.
Файлы из execution_context читать по разрешённой ссылке, НЕ предполагать соседство физического run-root и project-root.
В этом каталоге нет придуманных переменных `run.artifacts_dir`, `project_root` и shell-экспансии feature_request.

## Скаляры и glob
Используется `node_id` + один scalar `*-index.md` для набора файлов. Полезные документы с change_id объявлены
через `docs/changes/*/...`; каждый writer трогает только одну папку текущего CHG.
Недопустим `artifact_ref` на `docs/changes/*/decisions/*.md`, если результатов несколько: передать индекс.
Не использовать FTL внутри поля `path`: референс подтверждает шаблонизацию instruction, не всех YAML-полей.
