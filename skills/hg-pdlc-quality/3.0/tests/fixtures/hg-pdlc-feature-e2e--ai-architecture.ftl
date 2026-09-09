<#assign feedback0 = step["ai-architecture-review"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из ai-architecture-review (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["human-architecture"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из human-architecture (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
<#assign feedback2 = step["ai-srs-review"]!{} />
<#if feedback2.rework_instruction?has_content>
Замечания из ai-srs-review (проверить актуальность finding_id и basis_hash):
<#if (feedback2.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback2.rework_instruction}
</#if>
<#assign feedback3 = step["ai-code-review"]!{} />
<#if feedback3.rework_instruction?has_content>
Замечания из ai-code-review (проверить актуальность finding_id и basis_hash):
<#if (feedback3.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback3.rework_instruction}
</#if>
<#assign feedback4 = step["ai-diagnose"]!{} />
<#if feedback4.rework_instruction?has_content>
Замечания из ai-diagnose (проверить актуальность finding_id и basis_hash):
<#if (feedback4.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback4.rework_instruction}
</#if>
<#assign approvedPrd = step["human-prd"]!{} />
Runtime human-prd status: ${(approvedPrd.status)!"unavailable"}; route: ${(approvedPrd.route)!"unavailable"}.
Зафиксируй реальный факт human-prd по runtime gate/step context в approval-record.json (gate/node, revision/hash, available actor/time).
Если runtime не раскрывает actor/time, укажи unavailable; не выдумывай подписанта. Отметь статус approved без изменения принятого текста PRD.
Создай architecture.md (arc42-lite), C4 Context/Containers, sequence и реальные ADR, components.json.
Сохрани architecture-index.md как scalar handoff. Подготовь risk findings для технического gate.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
