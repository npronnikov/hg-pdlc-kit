---
name: pdlc-build-review
description: Разбор фактической сборки. Контракт соответствующего этапа PDLC для одной монорепы.
---

# Разбор фактической сборки


Прочитай build-report.json и code-check.json из актуальных command-нод, stdout/stderr. on_success разрешён только при passed обоих. Классифицируй process exit, timeout, отсутствующий инструмент, compile/test error. Для product defect отправь on_rework в ai-implement; неверный SRS/ADR — соответствующий route; недоступный worker, требуемый секрет, запрещённая загрузка зависимости — on_blocked. Не называй ошибку окружения дефектом требований и не ставь skip.
build-review.json — run, содержит причинные ссылки FR/STORY/CODE, реальные ошибки, требуемую правку, что сохранить. Замечание передавай через native summary и FTL, не отдельный retry-state файл.
