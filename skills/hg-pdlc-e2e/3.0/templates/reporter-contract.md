# Контракт E2E reporter
Это нейтральный JSON-результат исполнения; он не имитирует собственный формат Playwright/JUnit.
Adapter должен формировать его из фактических событий тестового runner и сохранять родной отчёт/логи как дополнительные evidence.
Путь результата передаёт HG command → e2e.sh первым аргументом. До попытки старый файл удаляется.
`cases` — все исполненные тесты со стабильными E2E-ID. Нельзя писать passed без assertion; attempts>1 считается flaky для required.
`environment.real_components` и `chain` должны соответствовать реальному boundary теста и модели сценария.
Missing/empty/старый report, незапущенный обязательный тест, duplicated ID, skipped/blocked/failed/flaky → failure.
stdout/stderr, exit, duration и source/contract fingerprint фиксирует command независимо от отчёта тестов.
Валидатор проверяет структуру/coverage/fingerprint, но не является криптографическим доказательством честности произвольного кода.
Поэтому sandbox, защита ожиданий и независимое ревью reporter остаются обязательны.
