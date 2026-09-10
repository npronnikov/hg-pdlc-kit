---
name: sdd-recover-specs
description: Восстанавливает знания из кода с доказательствами, не превращая случайную
  реализацию в желаемое поведение.
---

# Восстановление спецификаций as-is

## Цель
Поддержать recovery flow: бизнес-картина, C4, SRS и каталог существующих тестов с уровнем достоверности. Product source/tests не изменять и новые фичи не реализовывать.
## Метод
Прочитай код/README/specs/контракты/migrations/routes/тесты по capability и relevant call chain. Каждое восстановленное утверждение имеет evidence file:line + commit/hash; классификацию observed_in_code / observed_in_test / human_confirmed / inferred / unknown. Комментарий разработчика — источник с риском устаревания, не execution evidence. Coverage slice оговаривается; не утверждай полный анализ миллионов строк после краткого поиска.

Business: observable value/roles/journeys/rules; цель, мотивация и desired behavior подтверждаются ВП, не выводятся достоверно только из code. Architecture: реальные containers/trust boundaries/protocols/dependencies, reconstructed decisions вместо выдуманных исторических ADR. System: обнаруженные interfaces/data/states/constraints; undocumented choices отдельно. Test inventory: native selectors, layers, channels, assertions и known gaps; существующий test ≠ passing test. Исполнение тестов не обязательно для recovery, если не запрашивалось/нет среды; status not_run, не green.

Сверь противоречия docs↔code↔test↔ВП в conflict register. Confirmed business norm может не совпадать с текущим кодом — это defect/gap, а не автоматический rewrite norm. Неизвестные NFR численно не заполняй. Принятие baseline означает «согласны с картой фактов, ограничений и пробелов», не «система удовлетворяет всем требованиям».
## Выход
recovery-evidence.json: claims[{id,text,classification,evidence_refs,confidence,human_confirmation}], conflicts[], unknowns[], coverage_boundary, inventory_test_status. Для каждой стадии обычный профильный шаблон, но с меткой reconstructed/as-is и ссылками evidence. Финальный baseline-plan добавляет только проверенную/помеченную информацию и ссылки на имеющиеся canonical specs.

## Основания и границы адаптации
- [S09] AWS AI-DLC workflows: https://github.com/awslabs/aidlc-workflows
- [S11] C4 model: diagrams: https://c4model.com/diagrams
- [S14] ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html

Инструкции набора — оригинальная адаптация; внешние frameworks не устанавливаются и не запускаются неявно.
