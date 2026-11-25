---
layout: post
title: "长会话不必每轮把历史再传一遍"
date: 2026-11-17
sources:
  - https://claude.com/resources/articles/message-threads
  - https://platform.claude.com/docs/en/build-with-claude/message-threads
status: draft
tags:
  - agents
  - harness
  - latency
  - coding
---

Anthropic 11 月 2 日宣布，Messages API 的 message threads 进入 public beta。编码 agent 一轮会话里可能打上百次请求，以前每轮都要把此前所有消息和工具结果再传一遍。会话到几十万、上百万 token 时，光是把历史再交上去，首 token 就会被拖慢。

11 月 2 日那篇札记写的是长跑任务换会话时从零开始，得靠 harness 把班次缝起来。这篇说的是同一段还没结束的长会话：历史不用每轮再寄一遍。

## 先把整段交上去，后面只寄新的

第一次请求仍带上完整对话，并加上 `thread` 参数，类型为 `create`；请求还要带 beta 头 `message-threads-2026-08-12`。之后每轮只传上次回复之后的新消息，以及上一则回复的 id，类型为 `continue`。`system` 和 `tools` 在创建时就固定下来，续传时不必再带。

Anthropic 说，多数 Claude Code 用户已默认打开。在 50 万到 100 万 token 的请求上，首 token 时间的中位数大约下降 35%。计费和速率限制不变。

## token 没有变少

容易把它理解成「少传了就能少算 token」。文里写的是：虽然请求变小了，模型每一轮仍会读完整段对话，token 用量不变。省下的是上传、校验和重新分词的时间，所以首包会更快、也更稳。

计算机使用这类会反复传截图的 agent，以及文档、图片很重的流程，更适合用线程：大块内容留在线程里，不用每轮再上传。

## 线程很短，完整历史还得自己留

线程是 best-effort。上次请求过后 5 分钟会过期；若这一轮被成功存下，5 分钟会重新起算。服务端至多在最后一次使用后 1 小时内删掉它。内容只放在内存里，加密存放，不写进持久存储。续传时如果已经找不到，会返回 404，这时要把完整对话再发一次，重新 `create`。

没有哪次成功响应会告诉你「这一轮已经存好了」，要到下一次 `continue` 才知道。完整对话要以应用自己那份为准：从一开始就留一份完整副本，并准备好重放。SDK 的 helper 可以在进程还活着时帮忙做这件事，但进程一结束，副本不会自动留下来。

它和 Claude Managed Agents 里的 session threads 也不是同一个机制，不要混用。

## 可立刻落到自己仓的四点

1. 长会话变慢，先看每轮是不是把全部历史和工具结果又传了一遍。能开 message threads 就开，尤其是编码循环和带截图的计算机使用。
2. 不要按「省 token」来预期。用量和限速不变，图的是首 token 更快。
3. 客户端必须自留完整对话。线程 5 分钟无请求就会过期，404 之后用完整历史重新 `create`，不要假设服务端还记得。
4. 续传时不要改已经固定的 `system` 和 `tools`；文件是按引用挂在线程上的，对话还在用的文件得一直可取。

来源见 front matter；正文是读后札记，不是原文转载。文中的时延数字是原文给出的 Claude Code 口径。
