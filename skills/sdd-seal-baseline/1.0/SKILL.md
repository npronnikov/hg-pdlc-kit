---
name: sdd-seal-baseline
description: После реального approve применяет только подготовленный документационный
  patch и записывает receipt.
---

# Фиксация принятой базы в репозитории

## Цель
Завершить текущий scope после финальной человеческой приёмки; никаких push/PR/deploy. seal.md и seal.json — техническая фиксация, не новая фаза разработки.
## Предусловия
Instruction содержит trusted runtime gate: decision=approve, route=on_approve, gate attempt. Прочитай acceptance packet + baseline-plan и перепроверь exact hashes. Старый approval от другой attempt/revision не подходит. Проверь current source/tests/spec fingerprints и registry_before_sha256. При drift/concurrent change не трогай canonical docs и верни rework к acceptance verification или blocker; при изменённом product/test коде — повтор e2e.
## Операция
Применяй только prepared canonical_updates, byte-for-byte, с before/after checks; обнови registry как последний commit-point локальной materialization. Используй временные файлы и atomic replace в пределах FS; перед каждой заменой CAS before_sha256. Сохрани transaction journal / backups только собственных изменяемых docs. При частичном сбое откати только собственные замены при совпадении их after hash, иначе blocker; registry не должен указывать на частично подготовленную базу. Это файловый протокол, не распределённая транзакция и не замена host-level workspace isolation.

Добавь immutable receipt в текущий CHANGE_ROOT/71-seal/seal.json (не изменяй принятый 70-acceptance packet): trusted gate fields, packet hash, runtime audit reference, materialized canonical hashes, source/tests/evidence fingerprints, documentation kind. Не выдумывай approver username/time: null, если runtime их не предоставил. Не переименовывай raw test report в green.

Обнови docs/sdd/README.md/registry навигацию и product glossary лишь в пределах уже принятого canonical plan; старые change snapshots остаются historical. После фиксации ещё раз проверь хэши неизменности source code/tests — после e2e они не должны меняться.
## Выход
seal.json содержит status=sealed, mode=delivery|baseline, receipt, canonical_updates_applied, fingerprints и final limitations. Если операция невозможна, не выдавай sealed. Runtime publish mode должен быть LOCAL (проверяется оператором при создании run, не выдуманным YAML ключом).

## Основания и границы адаптации
- [S03] HGSDLC: runtime variables: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/runtime_variables/spec.md
- [S04] HGSDLC: artifacts: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/artifacts/spec.md
- [S06] HGSDLC: run lifecycle: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/run_lifecycle/spec.md
- [S08] OpenSpec: https://github.com/Fission-AI/OpenSpec

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
