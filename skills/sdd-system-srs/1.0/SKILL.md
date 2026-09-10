---
name: sdd-system-srs
description: Формализует принятое бизнес-поведение и архитектуру в атомарные, трассируемые
  и верифицируемые требования.
---

# Системные требования в SRS

## Цель
Создать srs.md и system-requirements.json. Формат — адаптированный SRS, ориентированный на ISO/IEC/IEEE 29148; это не буквальная копия стандарта и не заявление о соответствии всем его положениям.
## Шаблон srs.md
1. Introduction: purpose, scope, definitions, references, document control.
2. Overall description: product context, users, assumptions/dependencies, constraints, operating environment.
3. External interfaces: UI behavior/states/accessibility; API/events/CLI/files; third-party protocols; failures/timeouts.
4. Functional requirements SYS-ID: trigger, preconditions, actor, SHALL/«система должна», observable result, exceptions, authorization, linked BR/RULE/AC/ADR.
5. Data: schemas, units/time zones/currencies, validation, integrity, ownership, retention/deletion, migration/backward compatibility.
6. State/concurrency: permitted transitions, retries, deduplication, idempotency, transaction boundaries and recovery.
7. Quality requirements NFR-ID: metric, threshold, workload/window, environment, verification method and linked business driver. Не использовать «быстро», «надёжно», «удобно» без критерия.
8. Security/privacy: applicable threats, roles/permissions, input/output validation, data minimization and audit; cite конкретную редакцию ASVS при применении, не сочинять номера контролей.
9. Verification: requirement→method(test/analysis/inspection)→test case / evidence owner; readiness/acceptance rules.
10. Traceability; rationale; unresolved; glossary; change record.

Правило атомарности: одно нормативное поведение на ID. Сценарный шаблон: «При <условие/событие> система должна <результат>, при <ошибка> должна <обработка>». Разделяй positive requirement и запрет/denial для независимой проверки. Порог ссылается на источник либо человеческое решение; нельзя придумать SLA за ВП.
## system-requirements.json
schema_version, document_revision, requirements[{id,kind,statement,source_br_ids,source_ac_ids,adr_ids,interface_refs,priority,verification_method,verification_criteria,scope,status}], external_interfaces[], data_rules[], state_models[], unresolved[].
## Процесс
Прочитай accepted PRD+architecture, отрази approved decisions. Восстанови bidirectional trace links. При архитектурном конфликте верни architecture stage; при изменении смысла BR — PRD. До SRS gate никакого product code. Нельзя реализовать только endpoint list и объявить полный SRS.

## Основания и границы адаптации
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- [S22] OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
