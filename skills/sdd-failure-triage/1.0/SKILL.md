---
name: sdd-failure-triage
description: Разделяет дефект продукта, теста, требований и среды и выбирает минимальную
  корректную фазу возврата.
---

# Классификация обратной связи и сбоев

## Цель
triage.md/json с root cause evidence, affected requirements и route. Не пытаться одновременно переписать product code, test oracle и PRD.
## Алгоритм
Прочитай actual execution reports либо feedback final human gate. Восстанови reproduction, сравни expected из approved model с actual. Категории: product_defect; test_defect (locator/fixture/harness, но oracle прежний); system_or_architecture_gap; business_intent_change; environment_blocker. Не доказано — environment/unknown blocker, не бессрочный repair loop.

Для product_defect верни code writer, затем code review→test author/review→полный e2e rerun. Для test_defect верни test author, запрети production/requirements mutation. Для SYS/architecture gap возврат к architecture/SRS и повторные human approvals. Для BR/AC изменения — интервью/PRD. Для env/tool problem — blocker gate, после исправления безопасный повтор через discovery с сохранением ответов.

Отметь какие approval hashes и evidence invalidated. `triage.json`: category, evidence_refs, conflicting_ids, root_cause, minimal_repro, required_fix, allowed_files, invalidated_gates, chosen_route. Route в JSON summary — один из объявленных в ноде; значение on_success в этой конкретной ноде означает «диагностика закончена, исправлять тест», а не «продукт принят».
## Лимиты
Для технических repair/upstream handlers — не больше трёх автоматических возвратов в пределах run. Исключение: on_rework к новому раунду интервью в f03-prd/r03-business/b03-reproduce имеет бюджет 8; on_success имеет защитный бюджет 32, чтобы обычные повторные human approvals не исчерпывали лимит 3. Лимиты обеспечены max_loop_count; после исчерпания runtime failure и решение человека, не обход через новый alias. На повторных одинаковых failure сначала изменяется гипотеза/diagnostic, не ослабляется тест.

## Основания и границы адаптации
- [S01] HGSDLC: инструкция создания flow: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/agent/create-flow-instruction.md
- [S05] HGSDLC: node validation: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/node_validation/design.md
- [S06] HGSDLC: run lifecycle: https://github.com/npronnikov/hgsdlc/blob/a92d294a0118edd35b803eca3429de5eed1fd078/docs/spec/execution/run_lifecycle/spec.md

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
