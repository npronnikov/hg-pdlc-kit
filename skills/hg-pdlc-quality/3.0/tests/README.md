# FreeMarker validation probe — NOT RUN in the delivery environment
Только проверка авторского каталога; не runtime и не симулятор flow. Probe не запускает команды/агентов,
не выбирает handlers и не изменяет продукт. Fixtures — точные тексты instruction из вложенных FLOW.yaml.
Проверяются три набора данных: первый проход, rework с keep_changes=true, rework после rollback.

В исходной среде отсутствует FreeMarker JAR, поэтому эта проверка **не выполнялась**. Подготовьте в своей
среде JDK 17+ и совместимый с HG FreeMarker (API 2.3.32+), затем из каталога tests:
```bash
mkdir -p /tmp/hg-ftl-probe-classes
javac -cp "$FREEMARKER_JAR" -d /tmp/hg-ftl-probe-classes FtlRenderProbe.java
java -cp "/tmp/hg-ftl-probe-classes:$FREEMARKER_JAR" FtlRenderProbe fixtures
```
JAR не входит в архив. Успешный probe проверяет синтаксис с fixture-данными, но не подтверждает контекстную
модель конкретного HG SDLC, работу materialization, subagent вызовы или rollback. Для этого обязателен
hg-pdlc-catalog-smoke, затем контрольный delivery run в настоящем HG.
