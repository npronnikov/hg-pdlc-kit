---
name: pdlc-bootstrap
description: Восстановление brownfield-базы. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Восстановление brownfield-базы


Исследуй ОДИН монорепозиторий. Код не меняй. Прочти реальные modules/API/schemas/UI/tests и существующие спецификации; repository-scout получает ограниченные подзадачи. Создай pdlc/product/index.md (карта базы), business.md (способности/правила с происхождением), architecture.md + architecture.dsl (as-is C4 и инварианты), system.md (наблюдаемые интерфейсы/требования), test-model.md (фактически существующая регрессия и пробелы), sources.json (facts с classification observed/documented/inferred/unknown, path, sha256), trace.json (основание→поведение→код→существующий тест).
Отделяй documented intent от observed code. Никогда не «восстанавливай» KPI, юридическое согласие, приоритет или исторический PRD из поведения программы. Inferred остаётся inferred даже после принятия общего baseline. Отсутствующий тест — gap, не E2E passed.
Изменения в pdlc/changes/*/ — будущие/проверенные фичи, не автоматически состояние работающего продукта. Не смей переписать active target specs описанием code-as-is.
interview.md (run) готовит только вопросы о противоречиях и неизвестном бизнес-контексте. После ответов обнови базу и явно добавь решения в business.md; сырую форму не переноси в project. Для пустого greenfield не фабрикуй базу: отмечай отсутствие реализации и сохраняй brief/ограничения; следующий feature-flow строит target design.
