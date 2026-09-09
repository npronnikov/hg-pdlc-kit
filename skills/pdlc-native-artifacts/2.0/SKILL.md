---
name: pdlc-native-artifacts
description: Keep durable product knowledge in Git and execution state in HG-native run artifacts.
---

# Единственный runtime — HG SDLC

Flow, skills (включая policies), subagents, их templates и helper source — Git-каталог. pdlc/product и pdlc/changes в продуктовом Git хранят постоянные знания. Runtime reports, interview/answers, freeze snapshots, raw tests, questions, triage, logs — scope: run; координаты назначает/сохраняет HG. Не создавай собственные .pdlc/state, active run file, очереди, retry counters или provider-native folders. Номер попытки/переходы/rework/max_loop_count принадлежат HG. Helper только читает известный native layout и исполняет конечную проверку. Один run — один isolated workspace; parallel runs не используют общий рабочий checkout.
