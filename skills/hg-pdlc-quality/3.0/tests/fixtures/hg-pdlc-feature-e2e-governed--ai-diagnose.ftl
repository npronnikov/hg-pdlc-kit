<#assign feedback0 = step["command-e2e"]!{} />
<#if feedback0.rework_instruction?has_content>
Замечания из command-e2e (проверить актуальность finding_id и basis_hash):
<#if (feedback0.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback0.rework_instruction}
</#if>
<#assign feedback1 = step["command-regression"]!{} />
<#if feedback1.rework_instruction?has_content>
Замечания из command-regression (проверить актуальность finding_id и basis_hash):
<#if (feedback1.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback1.rework_instruction}
</#if>
<#assign feedback2 = step["ai-evidence-review"]!{} />
<#if feedback2.rework_instruction?has_content>
Замечания из ai-evidence-review (проверить актуальность finding_id и basis_hash):
<#if (feedback2.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback2.rework_instruction}
</#if>
<#assign feedback3 = step["human-exception"]!{} />
<#if feedback3.rework_instruction?has_content>
Замечания из human-exception (проверить актуальность finding_id и basis_hash):
<#if (feedback3.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback3.rework_instruction}
</#if>
<#assign feedback4 = step["command-final"]!{} />
<#if feedback4.rework_instruction?has_content>
Замечания из command-final (проверить актуальность finding_id и basis_hash):
<#if (feedback4.keep_changes!false)>
ДОРАБОТКА: сохранить корректные изменения, точечно устранить замечания и повторить проверки.
<#else>
ПОВТОР ПОСЛЕ ОТКАТА: HG SDLC восстановил рабочую базу; выполнить исходный контракт целиком с учётом замечаний.
Не делать самостоятельный git reset. Даже при keep_changes=false замечания обязательны.
</#if>
${feedback4.rework_instruction}
</#if>
Прочитай доступные свежие command receipts/logs/review; после human-exception учти решение из формы.
Диагностируй code/test-code/oracle/environment/requirements/architecture/SRS, не подавляй проверку.
Создай diagnosis.md. on_documents — только ошибка копирования/консолидации после command-final, без source/contract drift. on_environment — ограниченная починка изолированной среды; on_blocked — нужен человек;
on_success разрешён ТОЛЬКО для разрешённого environmental false alarm и ведёт на повтор regression, а не final.
При отсутствии достаточных данных выбирай blocked, а не случайный implementation rework.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».

Запиши route строго из объявленных handlers: on_success, on_code, on_tests, on_oracle, on_environment, on_requirements, on_srs, on_architecture, on_documents, on_blocked. При возврате обязательна конкретная rework_instruction.
