<#assign feedback0 = step["ai-prd-review"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из ai-prd-review (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["human-prd"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из human-prd (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
<#assign feedback2 = step["ai-architecture-review"]!{} />
<#if feedback2.rework_instruction?has_content>
Замечания из ai-architecture-review (проверить актуальность finding_id и basis_hash):
<#if (feedback2.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback2.rework_instruction}
</#if>
<#assign feedback3 = step["ai-srs-review"]!{} />
<#if feedback3.rework_instruction?has_content>
Замечания из ai-srs-review (проверить актуальность finding_id и basis_hash):
<#if (feedback3.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback3.rework_instruction}
</#if>
<#assign feedback4 = step["ai-contract-review"]!{} />
<#if feedback4.rework_instruction?has_content>
Замечания из ai-contract-review (проверить актуальность finding_id и basis_hash):
<#if (feedback4.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback4.rework_instruction}
</#if>
<#assign feedback5 = step["ai-code-review"]!{} />
<#if feedback5.rework_instruction?has_content>
Замечания из ai-code-review (проверить актуальность finding_id и basis_hash):
<#if (feedback5.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback5.rework_instruction}
</#if>
<#assign feedback6 = step["ai-diagnose"]!{} />
<#if feedback6.rework_instruction?has_content>
Замечания из ai-diagnose (проверить актуальность finding_id и basis_hash):
<#if (feedback6.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback6.rework_instruction}
</#if>
Прочитай заполненную форму by_value, baseline и intent. Создай prd.md/business.json/decisions.md в текущем CHG.
Не проставляй approved до gate. Сохрани run prd-index.md с точными ссылками и резюме решения для ВП.
Вычисли SHA256 business.json и prd.md в index; следующий human-prd должен видеть именно эту ревизию.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
