---
layout: post
title: "本机跑命令，用权限 profile 卡住边界"
date: 2026-11-19
sources:
  - https://openai.com/index/inside-the-codex-sandbox
status: published
tags:
  - agents
  - sandbox
  - security
  - harness
  - coding
---

OpenAI 11 月 18 日发了一篇工程文，讲 Codex 怎么在用户自己的机器上跑命令，同时又把文件系统和网络限制住。编码 agent 最常见、也最危险的动作之一，就是在本机执行 shell。他们的选择不是把计算搬进虚拟机或容器，而是用各平台自己的沙箱机制，把限制套在现有开发环境里的进程树上。

前几天写过常驻 agent 要先拆控制面、再加硬边界。这篇落到更近的一层：一次普通的本地编码会话，命令到底在什么权限下启动。

## 默认 :workspace 是在换空间，不是封死

内置 `:workspace` profile 默认允许在工作区里写代码，不必每次改文件都问人；但把 `.git`、`.codex`，以及 `.agents`、`.aws` 一类目录设成只读，避免直接改 hook 或 `config.toml`。读权限则放得很开，只受操作系统原有权限约束——编译器和 SDK 往往在仓库外面，把读范围收进工作区，日常构建会立刻断掉。代价是，机器上其他地方的配置和密钥，命令也可能读到。

网络默认关掉。这样能挡住直接外传，但装依赖、拉文档也一起停了，需要时再单独开口。文里也写得很直白：这些限制能挡住一大类坏事，但不是全部。例如往 `node_modules/prettier` 里塞一份恶意实现，`git status` 常常看不见（它通常被忽略）；用户保存文件时，编辑器若调用这份 Prettier，代码就会在沙箱外执行。所以他们把沙箱只当作纵深防御的一层，还要靠训练和对齐约束模型怎么用这些权限。

## 为什么不默认进容器

虚拟机和容器隔离更干净，但本地开发环境常常是一台改来改去的笔记本。文里举了在 Mac 上做 iOS 的例子：如果把 Codex 放进 Docker，它跑不了宿主上的原生工具链，也拉不起来 iPhone 模拟器；若把构建和模拟器再交回宿主机，这些步骤又落在容器沙箱外面，得另外设限制。他们宁愿把力气花在操作系统级沙箱上，让命令就在任务真正该发生的环境里跑。

harness 把三端差异收成同一套 API：给一条命令和一个 permission profile，需要受限联网时再配一个网络代理，然后 `spawn_command_under_sandbox()` 拉起进程。子进程继承同一套约束，整棵进程树都在里面，哪怕有的子进程比最初那条命令活得更久。

对 shell 工具来说，就是把原来的 `subprocess.Popen()` 换成这次启动。模型可以为单条命令申请扩权（`with_additional_permissions`）或完全出沙箱（`require_escalated`），但 harness 按用户偏好决定是否同意，可能直接问人，也可能走 auto-review。模型开口，不等于已经获准。

## 配置要能复用，也要能被组织卡住

权限写成具名 profile，放在 `config.toml` 的 `[permissions]` 里，可以 `extends` 内置的 `:workspace`。文件系统条目只有三档：`read`、`write`、`deny`。`:workspace_roots` 下的规则会应用到每个工作区根，例如把 `.vscode`、`.devcontainer` 设成只读，或直接 `deny` `**/*.env` 和 `secrets`。

网络大致三种：全关（`:workspace` 默认）、全开直连（`:danger-full-access` 默认），以及只许走到代理，由 profile 里的域名规则放行或拒绝。明确拒绝优先于允许。没匹配到的域名，代理可以先挂起，再交给人或者 auto-review。文里特别强调顺序：即便一次 DNS 查询，也可能把信息编进主机名里，所以代理只有在允许或批准之后，才去解析这个名字。光靠注入 `HTTP_PROXY`、`PIP_PROXY` 不够，因为不是所有程序都会认这些环境变量；直连会被操作系统侧的沙箱挡住。

个人可以把默认配置叠到某个信任的项目上。企业则用分层的 `config.toml`，再用 `requirements.toml` 做 managed requirements，比如只允许 `:read-only`，明确关掉 `:danger-full-access`。用户仍能在允许范围内改细节，但不能自行选出被禁用的 profile。

## 沙箱应当是一条可单独调用的命令

CLI 提供了 `codex sandbox --permission-profile ... -- 命令`，不必开一轮 agent 会话就能验证这条 profile 是否真能挡住它该挡住的事。文里的例子是尝试改 `.vscode/settings.json`，把保存时的格式化工具指到一份恶意实现；在 `dev` profile 下，`.vscode` 只读，macOS 上会得到 `Operation not permitted`。

同一套机制也可以包到自己的工具上。默认启动 stdio MCP server 时，Codex 不会擅自套沙箱，因为它推断不准这个服务要读写哪些路径、要连哪些网。文里把 `@modelcontextprotocol/server-memory` 的 `npx` 包进 `codex sandbox`：先在沙箱外建好数据目录、把钉死版本装进 npm 缓存，再以断网、只准写缓存和数据目录的 profile 启动。沙箱能往已有目录里写，但不能替你把目录建出来。

实现上，macOS 走内核强制的 Seatbelt（`sandbox-exec`，默认 `(deny default)`）；Linux 用 bubblewrap 做文件系统视图和独立网络命名空间，再用 seccomp-bpf 限制系统调用，代理连接通过命名空间内的 loopback 监听器转到外面的共享代理；Windows 正在从需要管理员权限、会改主机 ACL 和防火墙的旧方案，迁到 Microsoft 的 MXC，用系统自带的进程隔离，避免在主机上留下持久的沙箱状态。

## 可立刻落到本地编码 agent 的五点

1. 默认「工作区可写、网络关闭」是为了还能干活，不是完整边界。读范围放宽之后，仓库外的密钥仍可能被读到；`.env`、`.git/hooks`、编辑器配置这类路径，要写成明确的只读或拒绝。
2. 本地编码 agent 不必默认搬进容器。需要宿主工具链时，更值得投资的是操作系统级沙箱，外加可复用的 permission profile。
3. 模型为单条命令申请扩权或出沙箱，必须由 harness 按策略决定，可以问人，也可以走 auto-review，不能把请求本身当成批准。
4. 把沙箱做成可单独调用的命令，先用它验证 profile 能否挡住你担心的写入和联网，再拿去包 MCP server 或其他工具，不要只套在 agent 的 shell 工具上。
5. 受限联网时，域名规则要在代理里执行，DNS 应在放行之后再解析；同时用操作系统挡住直连。只改环境变量里的代理地址是不够的。

来源见 front matter；正文是读后札记，不是原文转载。
