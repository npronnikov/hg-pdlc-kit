# Основания и отличия от референса

Основной источник формата — приложенный пользователем `aidlc(1).zip`, а не недоступный «последний master». Проверяемый SHA256 архива и выбранных исходных файлов находится в `source-manifest.json`. Статья пользователя задаёт смысл связанного процесса: достаточные контекст и результат, автоматический переход, проверяемые артефакты и участие человека в содержательных решениях.

| Референс в приложенном архиве | Что использовано | Что изменено под задачу |
|---|---|---|
| flows/qwen-subagent-smoke-flow/1.0 | coding_agent=qwen, subagent_refs, human approval, FreeMarker feedback | Собственные роли и самостоятельный smoke ресурсов |
| subagents/aidlc-qwen-review-acceptance-auditor/1.0 | metadata entity_type=subagent, definition_file=<id>.md, frontmatter name/description/model: inherit | Никакого SUBAGENT.md по догадке; единый Qwen профиль |
| flows/hgdlc-light-development-flow/1.0 | writer/critic, несколько reviewer roles, rework handlers и step-context | Вместо лёгкого плана — полный PRD/architecture/SRS/E2E |
| flows/questions-form-flow/1.1 и skills/generate-form-questions | kind=human-form, version=1, fields, human_input run/by_ref | Вопросы после анализа монорепы; пустое required поле не считается согласием |
| flows/qwen-command-node-template-demo/1.0 | run/step FreeMarker, json_string, quoted heredoc, stdout STEP_SUMMARY | Данные не превращаются в shell; актуальные receipts/snapshot |
| flows/openspec-full-cycle и skills/openspec-propose | change package, delta-spec, scalar index, актуализация текущих specs | Единые слои docs/product и docs/changes, расширенная трасса |
| flows/aidlc-full-process-flow и requirements skill | Связанные этапы, явные входы/выходы, требования/архитектура/реализация | Меньше штатных human gates, отделённый PRD и стандартизованный SRS |
| flows/aidlc-reverse-engineering-flow | Восстановление исходной документации | Разделение observed/inferred/confirmed и greenfield proposed |
| flows/glob-test | project paths с glob и node_id | В наборах файлов downstream использует scalar index |
| skills/hgdlc-code-review и superpowers-guided-dev-flow | Evidence before completion, самостоятельное adversarial review | **Не перенесён** запрет браузера/local service: он противоречит требованию настоящего E2E |

## Ссылки на происхождение
Ссылки ниже помогают найти исходные проекты и нотации; актуальная совместимость каталога утверждается по приложенным файлам, не по неподтверждённой версии онлайн-репозитория.

- [HG SDLC](https://github.com/npronnikov/hgsdlc) и [исходный каталог](https://github.com/npronnikov/hgsdlc/tree/master/docs/aidlc).
- [Инструкция создания flow](https://github.com/npronnikov/hgsdlc/blob/master/docs/agent/create-flow-instruction.md).
- [OpenSpec](https://github.com/Fission-AI/OpenSpec): change/delta/canonical-spec подход; здесь не запускается его отдельный CLI workflow.
- [AWS AI-DLC workflows](https://github.com/awslabs/aidlc-workflows): фазы и артефакты, представленные в референсном aidlc-full-process.
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD): роль-ориентированные проверки; не переносится весь внешний runtime.
- [arc42](https://arc42.org/overview), [C4](https://c4model.com/), [Mermaid](https://mermaid.js.org/): архитектурное представление, использованное в собственных templates.
- [Gherkin reference](https://cucumber.io/docs/gherkin/reference): человекочитаемые сценарии.
- [OpenAPI specification](https://spec.openapis.org/oas/v3.1.0): HTTP-контракт 3.1 в примере.
- [Apache FreeMarker manual](https://freemarker.apache.org/docs/): синтаксис шаблонов; runtime rendering принадлежит HG SDLC.

Элементы PRD/SRS/quality-policy и расширенные machine-checks — авторская адаптация под запрос пользователя. Не заявляется, что эти файлы присутствовали в исходном архиве либо что все upstream frameworks имеют такой же формат. Статья, внешние frameworks и референсная упаковка не смешиваются в один неподтверждённый стандарт.
