<#assign feedback0 = step["ai-contract-review"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из ai-contract-review (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["command-contract-check"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из command-contract-check (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
<#assign feedback2 = step["ai-diagnose"]!{} />
<#if feedback2.rework_instruction?has_content>
Замечания из ai-diagnose (проверить актуальность finding_id и basis_hash):
<#if (feedback2.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback2.rework_instruction}
</#if>
Создай implementation-plan.md/json с DAG и file-level задачами. Адаптируй templates build.sh/e2e.sh к монорепе.
Скопируй verify.mjs и JSON schemas из ресурсов подключённых skills в project tools/hg; проверь hash копий.
Это не установка runtime: scripts только проверяют артефакты/сборку/тесты, переходы оставлены в FLOW.
В .gitignore добавь только `pdlc-run-*` и служебные output patterns штатного runner, сохранив существующие правила.
Объявленные полезные outputs должны существовать и при rework; план и oracle не ослаблять ради failed test.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
