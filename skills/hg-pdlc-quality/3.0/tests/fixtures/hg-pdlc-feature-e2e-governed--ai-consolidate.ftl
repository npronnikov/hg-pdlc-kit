<#assign feedback0 = step["command-final"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из command-final (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["ai-diagnose"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из ai-diagnose (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
Сохрани финальные regression/e2e receipts и e2e report в project evidence как точные копии переданных run artifacts.
Если system.nfr непустой, скопируй свежий pdlc-run-nfr-report.json из command-regression в project evidence/nfr-report.json.
Скопируй полезный e2e.log с policy redaction, не меняя raw JSON. Запиши verification.md, update product current.md/index.json,
baseline/architecture/system/quality canonical docs только по затронутому delta, сохраняя unrelated content.
Обнови change.json.status=e2e_verified_not_released. Не менять код, тесты, contracts, PRD/SRS/модель.
Сохрани final-index.md; финальный command ещё проверит hashes/copies/current index. Не выполнять release.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
