# Contributing

Additions to this repository are topic notes on the learning path in [README.md](README.md).

## Add a note

- Edit the placeholder `readme.md` for one step, or add a markdown file in that same folder.
- Keep the change on a single topic.
- Leave existing folder names as they are, including `Deploy and Optimis` and the Multi-Agent filenames, unless a pull request also updates the path table in `README.md`.
- Write from sources you can link. A short paraphrase is enough. Skip long copies of books, paywalled posts, or other copyrighted text.
- Leave out phone numbers, private email addresses, and real-name contact lines.
- Leave out secrets, API keys, and private candidate data.

## Propose a new topic

Open an issue or a pull request that:

1. Says which existing step the topic follows.
2. Adds a folder with a `readme.md` that states the scope in a few sentences.
3. Adds a row to the learning-path table in `README.md`.

## Pull requests

1. Fork the repository and create a branch.
2. Keep the diff to markdown unless you are changing the file check.
3. From the repository root, run `python3 .github/check_docs.py`.
4. Open a pull request against `main` and name the topic you changed.

Pushes and pull requests run [`.github/workflows/check.yml`](.github/workflows/check.yml). The check requires `LICENSE` and `README.md` to be present, and it resolves links in `README.md` and `CONTRIBUTING.md`.

## License

Contributions are accepted under the [MIT License](LICENSE). Copyright for the project stays with LofiSu.
