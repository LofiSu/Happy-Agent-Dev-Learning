# Happy-Agent-Dev-Learning

Learning path and notes for agent development engineers.

The folders in this repository are the outline. Each topic `readme.md` is still a placeholder, so use the table below as the order to fill them in.

## Learning path

The order follows the folders already in the tree: model background, then agent mechanisms, then evaluation and deployment.

| Step | Topic | Notes | Scope of the placeholder |
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

Multi-agent has two extra placeholder files, kept under their current names: [什么是MutilAgent](Agent/Multi-Agent/什么是MutilAgent.md) and [MutilAgent的架构](Agent/Multi-Agent/MutilAgent的架构.md).

## Repository layout

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
```

## How to use this with a coding agent

Clone the repository and open it in the agent host you already use (Cursor, Claude Code, Codex, or another host that can read the tree). Work one step from the table at a time. A useful prompt stays inside that folder:

```text
Read Agent/ReAct/readme.md. It is a placeholder.
Draft a short note on the ReAct loop for someone building agents.
Cite the public sources you actually used.
Do not edit other folders.
```

Read the diff before you keep it. If the file is still empty, that topic has not been written yet.

## How this fits with Agent Skills

An Agent Skill is a directory with a `SKILL.md` entry file. A host loads that file when a task matches the skill description. The format is documented in the [Agent Skills specification](https://agentskills.io/specification).

This repository has no `SKILL.md` files. It is the reading path. When a skill needs background, point it at one folder here. Packaged procedures live in their own repositories. [recruiting-skills](https://github.com/LofiSu/recruiting-skills) is one of those, and it is listed again below.

## Related public repositories

Other public repositories on the same GitHub account. The learning path above stands on its own.

- [recruiting-skills](https://github.com/LofiSu/recruiting-skills) — Agent Skills that enrich public author profiles from an arXiv paper, or screen a local index by graduation year and paper thresholds.
- [LLM-NoteBook](https://github.com/LofiSu/LLM-NoteBook) — longer notes from Transformer basics through RAG and agents, plus interview prep.
- [Agent_Kimi_ClaudeCode](https://github.com/LofiSu/Agent_Kimi_ClaudeCode) — a short setup walkthrough for Claude Code with the Kimi K2 API.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Notes can be written in Chinese or English.

## License

[MIT License](LICENSE). Copyright (c) 2026 LofiSu.
