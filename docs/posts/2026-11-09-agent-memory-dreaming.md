---
layout: post
title: "先记什么、离线再整理：agent memory 的 dreaming"
date: 2026-11-09
sources:
  - https://www.anthropic.com/research/components-of-agent-memory
status: published
tags:
  - agents
  - memory
  - context-engineering
  - dreaming
---

会话一长，transcript 就堆成山。下次开新会话，agent 到底该带着什么走？Anthropic 这篇把 agent memory 拆成两段：当场只记下「以后大概率用得上」的东西，空闲时再用 dreaming 对照 transcript 纠错、建索引、把该常驻的条目顶到会话开头。

这里的 memory 指跨会话可读写的经验笔记（常见形态是一个目录），不是改权重，也不是单次对话里的 in-context learning，更不是 compaction 那种「摘要顶替旧轮次」。

## 当场写笔记：在赌未来会再需要

写一条规则，其实是在预测：以后还会撞上同类问题。CL-Bench 那种跨会话查库题里，每道题开新会话，只允许读同一个 memory 目录。弱一点的模型会堆一堆没验证的猜测；强一点的会把「已核对 / 仍存疑」、失败原因和陷阱写进同一份参考，真正把「答错 → 记规则 → 下次用」闭环跑通。

Pokémon 长程局里，salience 判断差很多。Sonnet 3.7 几乎什么都存：战斗、物品、NPC 各一份文件，一万步左右已经几百个文件、两百多个文件夹，还在花步数整理 master 目录，游戏本身几乎不动。Fable 5 只留大约九个文件加一个 `global.md`：当前目标、通关计划、自己定的记忆用法，以及游戏不会直接告诉它、但试出来的策略。屏幕上随时能读到的状态不写；写了也会过期，检索成本反而拖后腿。

实践上：告诉 agent「有一个 memory 目录可用、重要就记」，比提前钉死「只记失败」更有效——强模型自己会判 salience；「只记失败」反而砍掉了不少增益。弱模型才需要更细的推：读记忆再答、把猜测测一遍。

## Dreaming：对照 transcript，别让错笔记进下一局

当场写的笔记可能一开始就错，也可能环境变了还留着。Dreaming 是离线（或空闲）再跑一轮：拿原始 transcript 当地面真相，改笔记、补表示、决定哪些条目该注入下一会话。

Mt. Moon 那个例子很直白：笔记把 PokéCenter 方位写反了，agent 以为山洞已经过完，反复掉下单向崖。对同一份错笔记跑 dreaming 之后，对照 transcript 改对方位，下一局直接回到洞口并到达下一城；没改的那次绕回上一个镇，任务失败。

Dreaming 还能干三件更「基建」的事：

1. **建可遍历的表示**（比如 wiki）：在大约 35 万份内部文档上，连续 dreaming 多轮后，问答命中率随 wiki 变厚而升；wiki + 搜索比单用搜索更稳，也更省 token。单文档就能搜到答案的题，wiki 增益很小；wiki 膨胀到比原文还大时，等于没抽象。
2. **把笔记往记忆层级顶上推**：harness 可以在每会话开头注入一小段「必读」索引（Claude Code auto memory 类似只加载 `MEMORY.md` 前 200 行 / 25KB）。注入层必须短——错笔记会污染每一局，长说明还会降低遵从度。
3. **按目标整形**：同一套合同语料，没说清「条款必须原样保留」时，多 agent 抢写一张共享表会丢事实；反思失败并改 dreaming 指令后，一合同一页、原文引用，brief 覆盖从七成左右到满分。第二轮 dreaming 还能补死链、加索引。

## 可立刻落到自己仓的四点

1. Memory 目录只存「屏幕/工具当下读不到、但验证过」的规则与计划；可变状态别当长期记忆。
2. 给强模型留 salience 判断权：说明 memory 用途即可，少写死「必须记什么」。
3. 错笔记比没笔记更危险——加一轮对照 transcript / 日志的 dreaming（或等价的离线整理 job），再允许注入下一会话。
4. 注入层当索引，不当全书：短 header + 链接到下层笔记；wiki 只服务「要跨很多文件拼答案」的任务，并定期剪枝。

来源见 front matter；正文是读后札记，不是原文转载。
