# HG PDLC BMAD catalog 2.0

Единый каталог: 3 flow, 24 skills и 9 subagents. Четыре обязательные process policies входят в эти 24 skills. Все runtime scripts, JSON Schema и шаблоны также входят в skills; установка provider-native `.claude/agents` в продукте не используется.

Это native-профиль текущего HG importer: `subagent_refs` поддерживаются, definition хранится в `<id>.md`, а `definition_file` указан явно. Все сущности используют `coding_agent: qwen`, `platform_code: BACK` и per-entity SHA-256.

Из корня поставки `tools/export_compat.py` экспортирует каталог без native subagent сущностей: 9 ролей становятся skills на тех же AI-нодах. Не импортируйте оба профиля с одинаковыми canonical flow names.

Публикуйте flow, skills, роли и worker-toolkit из одного Git snapshot. Конечный `pdlc.py` находится в skills/pdlc-runtime-tools/2.0/scripts; его assets — в skills/pdlc-contracts/2.0/assets. `hgpdlc-v2 catalog-root` возвращает установленную read-only копию каталога. Состояние исполнения остаётся в HG, постоянные документы продукта — в `pdlc/`.
