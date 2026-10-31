# 札记模板

这个文件不是一篇札记。Jekyll 会跳过以下划线开头的文件，所以它不会出现在站点上。

复制下面整段，另存为 `docs/posts/YYYY-MM-DD-short-slug.md`。`date` 写成写作当天，不要加引号，也不要留着 `YYYY-MM-DD`。

~~~yaml
---
layout: post
title: "用一句短标题写出这篇在讨论什么"
date: YYYY-MM-DD
sources:
  - https://www.anthropic.com/engineering
status: draft
tags:
  - agents
---

用自己的话写。不要整段粘贴原文。

标题用 front matter 的 title，正文里不必再写一个大标题。
来源只写在 sources 里，页面会列出来。
~~~

`status` 只用这两个值：

- `draft`：不进公开索引，页面上也不展示正文。
- `published`：合并进 `main` 之后出现在索引上，新的在前。

评审通过之前保持 `draft`。
