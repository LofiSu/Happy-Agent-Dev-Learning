---
layout: post
title: "只把沙箱放进来还不够"
date: 2026-11-15
sources:
  - https://claude.com/resources/articles/self-hosted-claude-managed-agents
status: published
tags:
  - agents
  - harness
  - security
  - sandbox
  - self-hosting
---

Anthropic 11 月 12 日发了一篇工程说明，宣布 Self-hosted Claude Managed Agents 进入 private beta：可以把整套 Managed Agents 服务跑在自己的云或机房里，不只是把沙箱搬进来。

Managed Agents 是一套可组合的 API，用来把长期运行的 agent 送进生产环境，覆盖 harness、沙箱、凭证处理和 session 历史。他们最先做的是 Anthropic 托管的平台服务；后来给需要代码留在自己环境里的团队，加了自托管沙箱。现在 agent 开始干修坏掉的构建、测发布、分拣告警、清 bug 积压这类活，会在没人盯着的时候碰内部系统和代码。对这种访问级别，有的团队希望整套服务都在自己环境里，而不只是沙箱。以前这就等于自己搭平台。

11 月 13 日那篇 OpenClaw 札记写的是控制面怎么和执行面拆开、硬边界怎么写死。11 月 14 日那篇写的是常驻循环怎么靠 inbox 和 timer 搭起来。这篇补的是控制面本身放在哪儿，以及同一套安全原则在三种托管方式里怎么坚持。

## 控制面、凭证和历史都要能自己管

自托管之后，harness、沙箱、凭证和 session 历史都跑在你的云或机房里。你要运维 Managed Agents 服务器、它的数据库，以及 agent 跑 shell 和文件工具的 worker。发给 Claude 的请求走哪条路由你选：直连 Anthropic、云厂商（Amazon Bedrock、Google 的 Agent Platform、Microsoft Foundry），或自己的网关。开发者用的还是和托管版相同的核心 API。

Session 历史存在你自己的数据库里。如果组织和 Anthropic 签了 zero data retention（ZDR），发往 Claude 的请求按和普通 Messages API 一样的规则处理。

## 安全先写在架构里

无人值守的 agent 进了你的代码和内部系统，就不能指望每一步都有人看。限制必须做进系统。他们给 Managed Agents 定了四条原则，三种部署方式都适用：Anthropic 全托管、只自托管沙箱、整套自托管。

脑和手要拆开。Harness（脑）负责调用 Claude；沙箱（手）才是 agent 代码运行的地方。Agent 循环、session 历史和 vault 里的密钥留在沙箱外面。这样一次 run 不必绑死在同一个沙箱上，沙箱只在工具真正要用时才启动，session 历史作为事件日志活在沙箱外。

凭证不要进沙箱。对 MCP 工具和受支持的 API 调用，沙箱外的代理会在请求里补上凭证。自托管时，凭证也可以放到你自己的密钥管理服务里。

网络可以收紧。每个环境可以只放行一份允许的主机名单，其余一律拦住。修构建的 agent，名单里也许只需 git 托管和包仓库。自己托管沙箱时，同样的限制写进自己的防火墙。

每次 session 都留下完整记录。包括它调用了哪些工具、返回了什么。记录可以通过 OpenTelemetry 导出，送到你已有的监控里，和别的系统一起看。

## 可立刻落到自己仓的四点

1. Agent 要在没人盯着的时候改代码、碰内部系统，先问控制面放在哪。只把沙箱搬进自己的网，harness、凭证和 session 历史还在外面，对有的团队不够。能自托管整套服务时，再决定要不要自己运维。
2. 继续坚持脑和手分开：循环、历史、密钥在控制面，代码只在沙箱里跑。不要让一次 run 绑死在某一个沙箱容器上；工具要用再起沙箱。
3. 凭证走沙箱外的代理，或放到自己的密钥管理服务，不要写进沙箱环境。网络按环境做允许名单，修构建这类任务尤其不要给开放外网。
4. Session 全程记下来，并用 OpenTelemetry 接到现有监控。出了偏离，要能按步骤回放，而不是只看最终输出。

来源见 front matter；正文是读后札记，不是原文转载。
