---
name: sdd-discovery
description: Заземляет запрос в текущем коде, спецификациях, тестах и реальных возможностях
  инструментов.
---

# Анализ репозитория и готовности среды

## Цель
Сформировать context.json/repository-map.md до интервью, чтобы вопросы ВП опирались на продукт и код, а не были общей анкетой.
## Шаги
Определи границы выбранного репозитория, stack и native build/test tools: Java/Maven/Gradle, JS/TS, Go, Python либо иной найденный стек. Прочитай README, AGENTS/QWEN, продуктовые docs, OpenSpec/spec-kit/AI-DLC каталоги, ADR, API schema, migrations, frontend routes, authorization и тесты. Проверь не только имена файлов, но релевантное содержимое. При большой базе используй ограниченную карту и точечное чтение; repomix возможен лишь локально после исключения секретов и generated/vendor директорий, не обязателен.

Построй capability/component map с file:line evidence и repo commit/fingerprint. Разделяй documented, observed_in_code, observed_in_test, executed, inferred, unknown. Наличие теста не значит, что он проходит. Расхождение specs/code — явный конфликт, не автоматическое «истина в коде».

Проверь Qwen file tools, shell, subagent delegation, write access только в разрешённых местах; для UI — установленный browser-capable runner, доступность browser binaries и способ DOM inspection. MCP browser необязателен: настоящий Playwright runner через shell достаточен. Для API/CLI/events выбери реальную границу системы. Сохрани версии фактически доступных инструментов, не требуй перевести проект на новый стек.

Не запускай feature tests до согласования безопасной среды. Определи test-only endpoints, auth env variable names, fixture/cleanup strategy, команды readiness/teardown, сеть, ограничения. Если среда ещё не создана, это может быть согласованной задачей implementation plan; до реального запуска e2e она должна быть проверена.
## Формат
context.json: schema_version, mode(feature|recover|bugfix), feature_request, repo_root, commit, dirty_baseline, source_fingerprint, baseline_registry_sha256, canonical_path_map, affected_capabilities, stacks, entrypoints, existing_test_commands, ui_present, capability_checks, environment_questions, conflicts, unknowns, evidence[].
repository-map.md: границы; существующее поведение; продуктовые источники; компоненты; API/UI/data; тесты; риски; рекомендации по интервью. Никакой выдуманной абсолютной директории.
## Ограничения
Не менять product code. Отсутствующая база не блокирует полный feature flow сама по себе: ограниченно восстанови затронутую часть и вынеси неопределённости в интервью. Масштабная противоречивая база — рекомендация отдельного recover flow, без выдуманного автоматического вызова subflow.

## Основания и границы адаптации
- [S02] HGSDLC: существующие flow: https://github.com/npronnikov/hgsdlc/tree/a92d294a0118edd35b803eca3429de5eed1fd078/docs/aidlc/flows
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S21] Qwen Code: subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
