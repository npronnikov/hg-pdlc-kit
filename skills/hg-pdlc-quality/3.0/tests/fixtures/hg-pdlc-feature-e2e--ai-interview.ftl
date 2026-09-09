<#assign feedback0 = step["human-interview"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из human-interview (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["ai-prd-review"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из ai-prd-review (проверить актуальность finding_id и basis_hash):
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
Изучи context и baseline. Спроси только недостающие бизнес-решения; при повторе сохрани валидные прежние ответы.
Создай questions.form.json точно в human-form формате ресурса и краткий interview-brief.md.
Вопросы и сырой ответ — run, не project. Не выбирай ответ за ВП.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
