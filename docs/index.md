---
layout: default
title: 每日工程札记
---

这里是 **LoomLab / Happy Agent** 的每日工程札记。读公开的工程写作，用自己的话记下可复核的做法，并附上来源。不复制原文。

题目多半从 [Anthropic Engineering](https://www.anthropic.com/engineering)、OpenAI 的工程与开发者文章、[Manus 博客](https://manus.im/blog)，以及同类工程博客和开发者文章里来。仓库根目录的学习路径保持原样，包括 `Agent/`、`LLM/`、`MachineLearning/`、`Deploy and Optimis/`。那些文件夹是提纲；这个站点只收按天写的短记。

## 已发布

{% include published-notes.html %}

## 下一篇怎么公开

1. 在 `docs/posts/` 新建 `YYYY-MM-DD-short-slug.md`。front matter 里的 `date` 用同一天，不要加引号。`status` 先写 `draft`。
2. 开一个 pull request，请人看过：是不是自己的话、`sources` 是否对得上、有没有个人邮箱、QQ、电话或其他不该公开的信息。
3. 通过之后把 `status` 改成 `published`，再合并进 `main`。索引只列出已发布的篇目，新的在前。

格式样例：[`docs/posts/_template.md`]({{ site.repository_url }}/blob/main/docs/posts/_template.md)。

~~~yaml
---
title: "这篇在讨论什么"
date: YYYY-MM-DD
sources:
  - https://www.anthropic.com/engineering
status: draft
tags:
  - agents
---
~~~
