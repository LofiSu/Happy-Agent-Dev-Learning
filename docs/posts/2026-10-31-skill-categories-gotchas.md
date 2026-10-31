---
layout: post
title: "软 Skill 不是又长又全的 README：九类分类与 Gotchas"
date: 2026-10-31
sources:
  - https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/
  - https://code.claude.com/docs/en/skills
status: published
tags:
  - agents
  - skills
  - claude-code
---

Anthropic Claude Code 团队在 2026-06 发了一篇内部经验帖：他们在公司里跑着几百个 skills，整理出了九类，以及几条很具体的写法。

对本地 Markdown skill / Cursor 类 agent 来说，这篇最有用的不是「再写一篇更长的说明」，而是两件事：先想清楚这个 skill 属于哪一类；再把失败经验收成 Gotchas。

## 九类在干什么

他们把内部 skills 粗分成九类，并强调：一个 skill 最好只站稳一类。跨类堆功能时，模型更容易在「该不该触发」上犹豫。

1. Library / API reference：内部库、CLI、SDK 的正确用法与踩坑。
2. Product verification：怎么验证产物真的对（常配浏览器、TTY、断言）。他们写：验证类 skill 对输出质量的提升最可测，值得单独投入。
3. Data fetching and analysis：连自家数仓 / 监控时用的表、字段别名、常用查询。
4. Business process：站会、建票、周报这类重复流程。
5. Scaffolding：带组织约定的脚手架，而不只是框架默认模板。
6. Code quality / review：风格、测试习惯、adversarial review。
7. CI/CD and deploy：看护 PR、发布与回滚。
8. Runbooks：从症状走到结构化排查报告。
9. Infra ops：运维例行，尤其是带破坏性动作、需要确认闸门的那些。

对 LoomLab 这种「文档优先、软闸」的 skill 仓，最常先落地的是 1、2、6、8：参考、验证、评审习惯、排障手册。硬产品闸门（平台里拦不住就过不去的那种）不在这篇的范围里——那是另一层。

## 别写模型本来就会的话

帖里反复说：Claude 会写代码、会读仓库。把默认流程再抄一遍，只是多占上下文。知识型 skill 要写的是「会把模型推出默认习惯」的信息——他们举了 frontend design：刻意避开 Inter + 紫渐变这类模型爱用的套路。

## Gotchas 才是高信号

他们认为技能文件里信号最强的往往是 Gotchas：从真实失败里长出来，而不是先写百科。例子包括：某表是 append-only，该取最高 version 而不是最新 created_at；网关里叫 `@request_id`、账单服务里叫 `trace_id`，其实是同一个值；Staging 返回 200 不代表 webhook 真处理完，要去查事件表。

可操作的习惯：每遇到一次模型用这个 skill 仍踩坑，就往 Gotchas 加一条，而不是扩写「概述」。

## 文件夹 + 渐进披露

他们纠正一个常见误解：skill 不只是单个 Markdown。`SKILL.md` 可以指向 `references/`、`assets/`、脚本；模型按需再读。这和「一上来把全部 API 塞进系统提示」相反——入口短，细节在链上。

description 也要写给模型扫触发条件用，不是给人读摘要：把会触发的词（比如 babysit）写进 description。

## 少用铁路式步骤

给目标与约束，不要把每一步钉死；skill 越可复用，过度具体的步骤越容易在新场景里绑死模型。需要用户配置时（Slack 频道等），缺配置就问，而不是猜。

## 我们能立刻用上的检查清单

写或改一个 soft skill 之前，先问：

1. 它主要落在九类里的哪一类？若答不上来，先拆。
2. Gotchas 里有没有至少一条来自真实失败？没有的话先别扩功能面。
3. `SKILL.md` 是否只做入口，长参考是否拆文件？
4. description 是否写了触发场景，而不是产品口号？

来源见 front matter；正文是读后札记，不是原文转载。
