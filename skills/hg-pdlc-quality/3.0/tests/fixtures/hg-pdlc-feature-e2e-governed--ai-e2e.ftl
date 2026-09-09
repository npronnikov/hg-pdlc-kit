<#assign feedback0 = step["ai-diagnose"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из ai-diagnose (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["ai-evidence-review"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из ai-evidence-review (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
Напиши все required E2E из модели после реализации. Реальные boundary/components; UI — настоящий браузер.
Адаптируй reporter и фикстуры, сохрани полезные tests и e2e-automation.md. Сырые результаты пока не создавать.
Тестовые ожидания должны соответствовать AC/SR; ошибочное ожидание возвращается в test-model/SRS, не правится молча.
Следующие command-regression и command-e2e выполнят полную проверку на одном текущем snapshot.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
