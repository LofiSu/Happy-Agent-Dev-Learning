# Happy-Agent-Dev-Learning

Learning path and notes for agent development engineers.

The folders are the outline. Each topic `readme.md` is still empty. Fill them in this order: model background, then agent mechanisms, then evaluation and deployment.

## Learning path

| Step | Topic | Path | Will cover |
| --- | --- | --- | --- |
| 1 | Reinforcement learning | [MachineLearning/RL](MachineLearning/RL/readme.md) | Feedback loops that later show up in agent training. |
| 2 | Language models | [LLM](LLM/readme.md) | Model behavior before tools and retrieval. |
| 3 | ReAct | [Agent/ReAct](Agent/ReAct/readme.md) | The reason-and-act loop. |
| 4 | RAG | [Agent/Rag](Agent/Rag/readme.md) | Retrieval-augmented generation. |
| 5 | Memory | [Agent/Memory](Agent/Memory/readme.md) | What an agent keeps across turns. |
| 6 | Context | [Agent/Context](Agent/Context/readme.md) | What goes into the model context. |
| 7 | Multi-agent | [Agent/Multi-Agent](Agent/Multi-Agent/readme.md) | Splitting work across agents. |
| 8 | Evaluation | [Agent/Evaluate](Agent/Evaluate/readme.md) | Judging whether an agent run worked. |
| 9 | Deploy and optimize | [Deploy and Optimis](<Deploy and Optimis/readme.md>) | Running an agent and making that run cheaper or faster. |

Multi-agent has two more placeholders. The filenames stay as they are:

- [什么是MutilAgent](Agent/Multi-Agent/什么是MutilAgent.md) — what a multi-agent system is.
- [MutilAgent的架构](Agent/Multi-Agent/MutilAgent的架构.md) — the architecture of that system.

## Repository layout

The learning-path files, in the same order, plus the daily digest under `docs/`:

```text
MachineLearning/RL/readme.md
LLM/readme.md
Agent/ReAct/readme.md
Agent/Rag/readme.md
Agent/Memory/readme.md
Agent/Context/readme.md
Agent/Multi-Agent/readme.md
Agent/Multi-Agent/什么是MutilAgent.md
Agent/Multi-Agent/MutilAgent的架构.md
Agent/Evaluate/readme.md
Deploy and Optimis/readme.md
docs/_config.yml
docs/index.md
docs/posts/
```

## How to use this with a coding agent

Clone the repository and open it in the agent host you already use (Cursor, Claude Code, Codex, or another host that can read the tree). Work one step from the table at a time, and keep the prompt inside that folder:

```text
Read Agent/ReAct/readme.md. It is a placeholder.
Draft a short note on the ReAct loop for someone building agents.
Cite the public sources you actually used.
Do not edit other folders.
```

Read the diff before you keep it. An empty file means that topic has not been written yet.

## How this fits with Agent Skills

An Agent Skill is a directory with a `SKILL.md` entry file. A host loads that file when a task matches the skill description. The format is documented in the [Agent Skills specification](https://agentskills.io/specification).

This repository has no `SKILL.md` files. It is the reading path. When a skill needs background, point it at one folder here. Packaged procedures live in their own repositories, for example [recruiting-skills](https://github.com/LofiSu/recruiting-skills).

## Related public repositories

Other public repositories on the same GitHub account:

- [recruiting-skills](https://github.com/LofiSu/recruiting-skills) — Agent Skills that enrich public author profiles from an arXiv paper, or screen a local index by graduation year and paper thresholds.
- [LLM-NoteBook](https://github.com/LofiSu/LLM-NoteBook) — longer notes from Transformer basics through RAG and agents, plus interview prep.
- [Agent_Kimi_ClaudeCode](https://github.com/LofiSu/Agent_Kimi_ClaudeCode) — a short setup walkthrough for Claude Code with the Kimi K2 API.

## Daily engineering digest

GitHub Pages serves the daily notes from [`docs/`](docs/index.md). The learning-path folders at the repository root stay as they are.

A note is a Markdown file in [`docs/posts/`](docs/posts/_template.md). Front matter has `title`, `date` (`YYYY-MM-DD`, unquoted), `sources` (a list of URLs), `tags`, and `status`. Name the file `YYYY-MM-DD-short-slug.md`, and use that same date in `date`.

1. Open the pull request while the note is still a draft (`status: draft`). Use the [daily-post template](.github/PULL_REQUEST_TEMPLATE/daily-post.md). On the compare page, set `?template=daily-post.md`.
2. A person reviews the note: the wording is original, the citations match `sources`, and the note has no personal email addresses, QQ numbers, phone numbers, personal blogs, or other private data.
3. After that review, set `status: published` and merge into `main`.

The public index lists notes with `status: published` only, newest first. A draft stays in the folder and off the index. Its page does not render the note body.

### Enable GitHub Pages

The site is stock Jekyll, configured in [`docs/_config.yml`](docs/_config.yml). This repository has no Pages workflow. Use GitHub's built-in builder:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Choose branch **`main`** and folder **`/docs`**, then save.

An admin has to save that once. The site address is `https://lofisu.github.io/Happy-Agent-Dev-Learning/`. Nothing is served there until those settings are saved and the first build finishes. The notes stay in `docs/` on `main` either way.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Notes can be written in Chinese or English.

## License

[MIT License](LICENSE). Copyright (c) 2026 LofiSu.
