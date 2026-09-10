---
name: sdd-implementation-plan
description: Делит требования на вертикальные проверяемые шаги с файлами, тестами
  и зависимостями.
---

# План реализации по принятому пакету

## Цель
Создать tasks.md + implementation-plan.json только после действующих business, architecture и SRS/model approvals.
## План
Для TASK-ID: linked SYS/AC/TC, concrete files/modules, dependencies, work type, definition of done, unit/integration check, e2e impact, migration/compatibility risk. Делай небольшие вертикальные slices, учитывай frontend+backend+data+auth и негативные сценарии. Отдельно запланируй local test harness, fixtures и stable UI semantics, если они отсутствуют. Не меняй stack ради удобства агента. В план входят только scope accepted; отсутствующее решение — возврат вверх.

Команды verification должны завершаться: build/lint/unit/integration/e2e runner. Долгоживущий backend/frontend запускается управляемо внутри test runner/webServer или wrapper с readiness, timeout и teardown. Не считать `npm run dev` успешной проверкой. Для test runtime зафиксируй base URL, required env NAMES, binary/tool versions и ограничения, без секретов.
## Выход
implementation-plan.json: task_ids, tasks[], dependency_graph, file_allowlist, verification_commands[{argv/cmd,cwd,timeout,expected_exit,scope}], test_environment_plan, acceptance_hashes. Все tasks сначала pending; unchecked обязательная задача блокирует финальную приёмку. Runtime-generated files/.qwen исключаются из product diff audit, но не от произвольной записи.

## Основания и границы адаптации
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec
- [S10] BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- [S19] Playwright: web server: https://playwright.dev/docs/test-webserver

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
