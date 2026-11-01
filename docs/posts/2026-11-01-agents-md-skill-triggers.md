---
layout: post
title: "AGENTS.md 写 if/then：把仓内 skill 变成强制工作流"
date: 2026-11-01
sources:
  - https://developers.openai.com/blog/skills-agents-sdk
tags:
  - agents
  - skills
  - agents-md
  - openai
status: published
---

OpenAI 工程博客写了他们怎么用 Codex 维护 Agents SDK（Python / TypeScript）两个活跃开源仓：仓库政策放在 `AGENTS.md`，可复用流程收成 `.agents/skills/` 下的 repo-local skills，需要时再挂 Codex GitHub Action。结果不是「多写几段提示词」，而是把验证、发版检查、PR 交接变成可重复的工作流。

对本地编码 agent / soft skill 实践来说，这篇最值得抄的是三层分工：什么时候必须调 skill、`description` 怎么路由、脚本和模型各管什么。

## 强制触发写在 AGENTS.md，不写在闲聊里

两边仓都用短 if/then 规则，把最高价值的触发条件顶在 `AGENTS.md` 前面。大意是：改 runtime / API 兼容边界前先跑 `$implementation-strategy`；动到 SDK 代码、测试、examples 或构建行为就跑 `$code-change-verification`；JS 包变更碰到 release metadata 就跑 `$changeset-validation`；收尾要交接时再跑 `$pr-draft-summary`。

关键点：条件写清楚。「有改动就全量验证」太重；「改了 runtime / 测试 / examples / 构建行为才验证，而且没过不许标完成」才可执行。docs-only 工作可以保持轻量，SDK 代码变更则走仓内定义的验证栈（Python 的 `make format/lint/typecheck/tests`，JS 的固定 `pnpm` 顺序）。

兼容性硬规则也可以和触发条件放同一文件：例如公开构造参数与 dataclass 字段保持位置语义、新可选参数尽量追加在末尾。skill 管流程，`AGENTS.md` 管「每次开工都生效」的仓规。

## description 是路由元数据，不是产品口号

Agent Skills 的渐进披露：启动时先看 `name` + `description`，选中后才读完整 `SKILL.md`，脚本和 references 按需再加载。所以 `description` 要同时回答三件事——做什么、什么时候触发、输出是什么——而不是一句「跑验证」。

他们对比了含糊版和实装版。含糊：`Run the mandatory verification stack in the OpenAI Agents JS monorepo.` 实装会补上「当改动影响 runtime / tests / build 行为时」。`pr-draft-summary` 同理：写明这是收尾 skill、面向中等以上实质改动、产出是 PR-ready 块，而不是随便写一段摘要。

路由不稳时，先改 metadata，再堆脚本。

## 模型管判断，scripts 管机械步骤

可靠拆法：解释、对比、报告留给模型；确定、重复的 shell 放进 `scripts/`。例如 examples 自动跑：先有 auto mode 跑例、落日志、生成 rerun 文件；skill 再让模型按「读源码意图 → 对日志」逐个核对，而不是把正确性全写死成固定断言。JS 仓还有 Verdaccio 本地发布 + 多 runtime 安装冒烟，抓的是「源码里能跑」之外的发布路径问题。

有些 skill 故意不做硬闸：`docs-sync`、`test-coverage-improver` 先出报告、排优先级，改文件前要人点头。发版 review 也类似——从「默认可发」出发，只有 diff 里有具体证据才拦，并附上 unblock 清单。

## 本地稳了再进 CI，评审也分层

同一套 skill 本地跑顺之后，再挂 Codex GitHub Action；公开仓尤其要管好谁能触发、输入怎么消毒、密钥权限。PR 自动 review 适合重复的正确性检查；API 取舍、兼容承诺、命名与发布沟通仍要人拍板。`AGENTS.md` 也可以写清：哪些正确性模式交给自动审，哪些必须人类决策。

## 可立刻落到自己仓的四步

1. 列 3～5 个「没做就不算完成」的仓内流程，各收成一个窄 skill（验证、docs 对账、PR 草稿等）。
2. 在 `AGENTS.md`（或等价仓规）顶部写 if/then，只强制最高价值触发。
3. 重写每个 skill 的 `description`：场景词 + 触发条件 + 产出形态。
4. 把固定命令顺序推进 `scripts/`；模型只做对比与是否放行的说明。

来源见 front matter；正文是读后札记，不是原文转载。
