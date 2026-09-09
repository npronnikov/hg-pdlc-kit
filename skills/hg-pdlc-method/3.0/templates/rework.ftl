<#assign feedback = step["human-prd"]!{} />
<#if feedback.rework_instruction?has_content>
  <#if (feedback.keep_changes!false)>
Режим: точечная доработка поверх сохранённых изменений.
  <#else>
Режим: повтор на восстановленном HG SDLC workspace; исходную задачу выполнить с учётом замечаний.
  </#if>
Корректирующая инструкция:
${feedback.rework_instruction}
</#if>
Исходный контракт шага остаётся обязательным в обоих режимах.
