<#assign feedback0 = step["ai-srs-review"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из ai-srs-review (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["ai-contract-review"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из ai-contract-review (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
<#assign feedback2 = step["ai-code-review"]!{} />
<#if feedback2.rework_instruction?has_content>
Замечания из ai-code-review (проверить актуальность finding_id и basis_hash):
<#if (feedback2.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback2.rework_instruction}
</#if>
<#assign feedback3 = step["ai-diagnose"]!{} />
<#if feedback3.rework_instruction?has_content>
Замечания из ai-diagnose (проверить актуальность finding_id и basis_hash):
<#if (feedback3.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback3.rework_instruction}
</#if>
<#assign architectureGate = step["human-architecture"]!{} />
<#assign architectureReview = step["ai-architecture-review"]!{} />
Runtime architecture review route: ${(architectureReview.route)!"unavailable"}.
Runtime technical gate status: ${(architectureGate.status)!"unavailable"}; route: ${(architectureGate.route)!"unavailable"}.
После архитектуры создай SRS/system.json и применимые контракты.
Зафиксируй architecture-approval.json: architecture_sha256, requires_human, decision=approved либо not_required,
mode=risk_adaptive, gate/evidence и unavailable поля вместо выдуманных actor/time. on_risk требует actual human-architecture;
историческое approval другой ревизии не переносить. В governed-profile technical approval требуется всегда. Все SR/NFR измеримы либо проверяемы с указанным методом.
contracts-index.md объясняет применимость HTTP/events/UI. Если HTTP есть, выпусти полноценный OpenAPI, не пустой template.
Передай srs-index.md с точными файлами, версиями, ссылками на BR/AC/CMP/ADR. Код пока не писать.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
