---
layout: post
title: "常驻 agent 并不一直开着"
date: 2026-11-14
sources:
  - https://claude.com/resources/articles/building-always-on-agents
status: draft
tags:
  - agents
  - harness
  - memory
  - scheduling
  - permissions
---

Anthropic 11 月 13 日发了一篇工程指南，作者 William Hu。客户开始问怎么把现有 agent 做得更主动，或者从零做一个会自己找上门的产品。文章把「常驻」拆开讲：用户感觉它一直在，但进程大部分时间在睡觉。每次醒来叫一次 run——收到事件、做完活、把该留下的写下，然后接着睡。循环靠五个部件撑着：event inbox、timer、memory、权限、outbox。

11 月 13 日那篇 OpenClaw 札记写的是常驻 agent 的硬边界。这篇写的是同一类产品背后，怎么把唤醒、记忆和投递搭起来。

## 事件先入 inbox，不要直接喊 agent

多数 agent 只在用户发消息时跑。常驻 agent 还会被 webhook、定时任务、后台作业叫醒。每个来源直接调 agent，会碰到两件麻烦事：两个事件同时到，run 互相抢；进程挂了，事件就丢了。

他们的做法是所有来源只往 inbox 写。最简单的 inbox 三件事就够：一份持久化的事件列表（通常是数据库表）、一个很快确认并写入的 handler（通常是 HTTP 接口）、一个从列表里取活的 worker。建议按用户各用一个 inbox，需要并行再拆。inbox 要记下每条事件的状态，并用来源的唯一标识去重。

几条写得很具体：

- Handler 要尽快确认。Webhook 提供方把慢响应当成失败。提示注入这类更深的检查，放到 run 里做，不要堵在入口。
- 以 inbox 为准。Worker 被叫醒后，先从 inbox 拉最新待处理事件。中途挂了，下一个 worker 还能拿到同一条，再试一次。
- 一个 inbox 同一时刻只允许一个在跑的 worker，避免重复劳动或互相覆盖。Run 做到一半又来新事件，可以留给下一次、并进当前这次，或者中断重来。
- Worker 要把待处理事件打包。用户连着发几句，合成一次 run，agent 回一条就行。
- 接着先前工作的事件（比如用户的回复）恢复已有 session；其余的开新 session。

## Timer 单独存放，到期了再写进 inbox

光有 inbox 还不够主动。Timer 分两类：follow-up 是 agent 给自己设的截止日期，比如过一会儿再看有没有回复；schedule 是已知节奏的重复任务，比如每天一封简报。

Timer 放在自己的持久化表里，不要跟 inbox 混。Inbox 里只放已经可以开工的事件。Scheduler 按固定间隔扫描到期项：follow-up 标记完成，schedule 改到下一次，然后往 inbox 写一条事件并叫醒 worker。Timer 自己不启动 run。

## Memory 只留下查不回来的东西

常驻 agent 的 run 是一段一段的，连续性靠 memory。存储要能活过 worker，通常是数据库或对象存储，目录映射过去就行，和 Claude Code 的 auto memory、Messages API 的 memory tool 同一思路。

一条经验：已经在别的系统里的东西，只存指针。Issue 跟踪器里查得到的，不必再抄一份。要存的大致是四类：

- 用户对 agent 行为的说明：单独成文件，每次 run 一开始就加载。人不在旁边时，这些说明得自己带着走。
- 对用户的笔记：角色、偏好、纠正。先从单文件开始，变长了再拆成许多小文件，开头只加载索引，需要时再取。
- 已经对用户说过的话：避免重复。可以单独成文件每次加载，也可以由 worker 带上最近几条对外消息。
- 进行中的任务进度：做了什么、还剩什么。新 run 读完就能接着干；同样是先加载索引。

他们也提到可以用 dreaming 在 run 之外整理记忆。这件事 11 月 9 日那篇已经写过，这里不展开。

每次 run 开始都会带上 system prompt、工具定义和 memory 文件，这笔固定开销要尽量瘦，并走 prompt caching。新 session 只有这份开销和触发事件；已有 session 还会带回先前的消息和工具调用。Session 太长时，可以压缩旧消息，也可以新开一个——两种都会丢细节，所以该留下的要在中途写入 memory。

## 权限：把凭证放在代理里，把审批做成可恢复的中断

无人值守的 run 拿着用户的访问权，风险最大。工具调用只有三条路：自己继续、拦住、等批准。

凭证不要放进 agent 的环境。请求先不含密钥发出去，由环境外的代理在转发前注入。这点和 11 月 13 日 OpenClaw 札记里的 credential broker 是同一方向。

Claude Code 的 auto mode 用分类器拦高风险动作，逼 agent 换更安全的做法；最要紧的决定还是要人看。需要澄清或批准时，用 deferred tool call：这次 run 结束，session 停在调用中间，请求交给用户（比如用 MCP Apps 做一张可交互卡片），用户的答复作为事件回到 inbox，新的 run 带着这份输入恢复 session。等回复的同时，worker 可以去处理别的事件。

## Outbox 默认先少说话

常驻 agent 多半在后台干活。用户拿到的是结果和少量细节，不是逐步推理的全程回放。一次 run 结束只有三种结果：往 outbox 发一条消息、决定什么都不发、用 deferred tool call 要权限或补充信息。

多数情况，一个「发送」工具直接把消息交给用户就够了。只有需要控制发送节奏，或让发送失败后还能重试时，才值得单独做 outbox：一张待发送表，外加一个类似 worker 的 dispatcher 负责真正投递。

发送量要调。话太多会吵，话太少会漏掉用户该知道的事。他们建议用 eval 找平衡，而且宁可先安静，再慢慢多说。

## 五个部件怎么转起来

一次 run 总是从 inbox 里的事件开始，不管它来自用户消息、webhook 还是到期的 timer。Worker 取出事件，在新 session 或已有 session 里叫醒 agent。Agent 先读 memory，在权限范围内做事，再把学到的写回 memory。Run 结束后，该通知用户的进 outbox，由 dispatcher 投递。Run 里也可以再设一个 timer，到期后又变成 inbox 里的新事件；用户若回复，答复同样回到 inbox。每次 run 都很短，这个圈一直转，用户才会觉得它是常驻的。

## 可立刻落到自己仓的五点

1. Webhook 和 cron 不要直接打进 agent 循环。前面加一个持久化 inbox，一个 inbox 同一时刻只跑一个 worker，挂了就从 inbox 重试。
2. Follow-up 和日程放在单独的 timer 表里，到期后再写成 inbox 事件。Inbox 只装已经可以开工的活。
3. 用户说明每次 run 都加载；笔记和任务进度用索引加按需文件；外部系统里已有的记录只存指针。
4. 需要人批准时结束这次 run，把 session 停在调用中间，用 inbox 事件恢复。不要让 worker 在那里空等。
5. 对外默认少说话。发送量和该不该打扰，用 eval 调，不要一上来就每一步都推送。

来源见 front matter；正文是读后札记，不是原文转载。
