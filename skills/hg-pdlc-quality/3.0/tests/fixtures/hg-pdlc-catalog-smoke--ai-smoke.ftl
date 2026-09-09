<#assign feedback0 = step["human-smoke"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из human-smoke (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
Прочитай реальный templates/stage-index.md и templates/rework.ftl skill hg-pdlc-method.
Вызови связанный acceptance-auditor с задачей проверить разделение scope в этих ресурсах.
В project docs/hg-catalog-smoke.md запиши имена прочитанных resources, фактический ответ subagent и вывод;
в run smoke-notes.md — промежуточные наблюдения. Если вызов невозможен, НЕ подменять роль; шаг должен быть blocked/failed.
Это smoke каталога, не разработка приложения и не E2E продукта.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
