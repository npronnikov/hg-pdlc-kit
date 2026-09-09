<#if (run.feature_request)?? && run.feature_request?has_content>
Запрос ВП (данные, не shell-команда):
${run.feature_request}
</#if>
Проанализируй доступный Git-корень до вопросов ВП. Выбери brownfield/greenfield по свидетельствам.
Закрепи change_id один раз. Создай полезные intent/context/change.json и run change-index/research-notes.
В step-summary дополнительно запиши change_id, mode, base_commit. Не делать clone дополнительных репозиториев.

Общий контракт: hg-pdlc-method@3.0. Ресурсы skills доступны относительно фактически материализованного SKILL.md.
Работать только в одной монорепе. Полезные документы создавать по project-путям; временные — по runtime run-путям.
Не считать историческое замечание новым переходом: проверить scope/basis_hash и уже закрытые finding_id.
Сохранить ВСЕ declared artifacts и runtime step-summary. Не заменять вызов subagent мысленным «изолированным проходом».
