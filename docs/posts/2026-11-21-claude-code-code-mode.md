---
layout: post
title: "相关工具调用先写成一段代码再跑"
date: 2026-11-21
sources:
  - https://code.claude.com/docs/en/code-mode
  - https://github.com/anthropics/claude-code/releases/tag/v2.1.323
status: draft
tags:
  - agents
  - coding
  - harness
  - permissions
  - tools
---

Claude Code 在 v2.1.323 里加了一个实验功能，名叫 Code Mode。默认关掉，可能改，也可能在后续版本里拿掉。它改的是编码 agent 花回合的方式：以前 Claude 直接申请 Bash、Read、Edit，读完这一次的结果再决定下一步；打开之后，它改写一段 JavaScript，由 Claude Code 在当前会话里执行。一段代码里可以并行跑命令，也可以把上一步的结果接进下一调用，最后只把 Claude 接下来要读的那部分返回去。

前两天写的是本机跑命令时，permission profile 怎么卡住文件系统和网络。昨天写的是调查不要只留在某次会话里。这篇回到本地会话内部：相关的工具调用，能不能先收成一段程序再跑，以及这样做之后，权限审查的边界会往哪移。

## 会话里看见的是调用，不是脚本

你还是用自然语言下任务。文档给的例子是改一处重试上限：先用 `rg` 找出定义，再改文件，再跑相关测试。对话里你看到的是工具调用本身，比如这次编辑的 diff，默认看不到那段 JavaScript。要看代码，按 `Ctrl+O` 打开 transcript，展开折叠的 Code 行。

文档建议拿它试三类活：同一处改动要落到很多文件；搜索结果要先过滤，再让模型读；几条互不依赖的命令可以同时跑。这些都是「回合税」很重、但步骤之间关系清楚的工作。

要打开它，把环境变量 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` 设成 `1`，用 v2.1.323 或更新的原生终端版启动。第一次会请你确认，同意后会话顶部会标明 Code Mode 已打开。这套开关不能写在项目的 settings 里：你克隆来的仓库，没法替你打开 Code Mode。组织的 managed settings 只能把它强制关掉（写成 `0`），不能替所有人打开。要恢复某次 Code Mode 会话，启动时必须仍带着这个变量；关掉后再 `--resume`，会被拒绝。

限制也不少。它只在交互式终端会话里工作，不支持 VS Code 面板、Desktop、云会话，也不能走 Bedrock、网关或自定义 `ANTHROPIC_BASE_URL`。Claude 在前台等结果时，这段代码最多跑十分钟；放到后台（需要从 auto 或 `bypassPermissions` 模式启动），可以跑到两小时，期间你还能继续跟 Claude 说话。中止之后，还得去 `/tasks` 看它拉起来的 subagent、shell 和 MCP 调用是不是还在跑。

## 自动审查看的是整段代码，不是每一步

权限并没有因为写成脚本就消失。脚本里的每一次工具调用，仍会按原来的工具名走你的 `deny`、`ask` 规则和 `PreToolUse` hook，比如仍叫 `Bash`，或某个 MCP 工具自己的名字。

变化出在 auto mode。分类器审查的是整段要跑的代码，不再逐个看每一次调用；它也看不到运行时才算出来的值，比如从搜索结果里取出的路径。文档写得很直白：你必须卡住的调用，还是要靠规则和 hook，不能指望分类器在运行中再拦一次。其他权限模式下，需要确认的调用仍会按原来的方式弹出来。若希望先读脚本再放行，可以给运行这段代码的工具 `REPL` 加一条 `ask` 规则；对话里的提示不会直接展示代码，仍要 `Ctrl+O` 展开再决定。

写 hook 的人要注意命令会以什么形态到达。文档举过一例：在 `app` 目录里执行的 `git push`，可能变成 `cd 'app' && git push` 再交给 hook。如果 hook 只匹配整条等于 `git push` 的文本，就会漏掉。要审查脚本本身，让 `PreToolUse` 匹配 `REPL`，从 `tool_input.code` 读 JavaScript；要在模型读到返回值之前做检查或脱敏，用匹配 `REPL` 的 `PostToolUse` hook。

文档也提醒：Bash 规则匹配的是命令文本，Claude 可以用规则匹配不到的写法跑一条被拒绝的命令，这件事跟开不开 Code Mode 无关。不依赖命令文本的限制，还是要靠 sandbox。这和 11 月 19 日那篇讲 Codex 沙箱的札记是同一类问题：文本规则是一层方便的门，不是硬边界。

## 可立刻落到自己仓的五点

1. 适合步骤清楚、调用很多的任务；不要假定它在所有表面上都能用。实验功能默认关闭，项目配置也不能偷偷替你打开。
2. auto mode 下，审查单位从「一次调用」变成「一段脚本」，运行时才出现的路径分类器看不见。必须拦住的操作，写成 `deny` / `ask` 规则或 hook。
3. 若要先看脚本再跑，给 `REPL` 加 `ask`；若要在模型读到输出前脱敏，用 `PostToolUse` 匹配 `REPL`。hook 要按片段检查命令，不要只匹配完整一行。
4. 中止脚本之后，检查 `/tasks` 里它拉起的子进程是不是还在。恢复会话时必须仍打开 Code Mode。
5. 命令文本规则会被换一种写法绕过。真正要封住的路径和网络，用 sandbox 或 permission profile，不要只靠 Bash 规则。

来源见 front matter；正文是读后札记，不是原文转载。
