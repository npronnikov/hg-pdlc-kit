<#assign feedback0 = step["human-exception"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из human-exception (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
Из diagnosis создай exception.form.json в run и полезный blocker.md в текущем CHG.
Покажи наблюдение, последствия, варианты и какое решение требуется. Секреты не вводятся в форму.
Необратимую/внешнюю операцию не выполнять по молчанию. После ответа diagnosis перепроверяет причину.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
