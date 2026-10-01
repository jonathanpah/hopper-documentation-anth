# Contributing to hopper-documentation-anth

Contributions can improve the writer rules, find recording failures, verify behavior in Claude Code, or improve the documentation. English documentation is in `hopper-documentation-anth-en/` and Brazilian Portuguese documentation is in `hopper-documentation-anth-pt-br/`. Shared GitHub policies and templates remain at the repository root. Each language folder is a complete plugin: the skill, the writer rules, the example, the program, the hook, the tests, and the evaluation suite. Keep both versions equivalent; one release covers both languages.

## Start with the problem

For suspected vulnerabilities, follow the [Security Policy](SECURITY.md) and report privately. Do not include security-sensitive details in public issues, discussions, or pull requests before coordinating disclosure.

Use a bug report for a reproducible failure and a proposal for a specific change. Use [Discussions](https://github.com/jonathanpah/hopper-documentation-anth/discussions) for questions or early ideas. Search existing issues before opening another report about the same behavior.

For changes to the recording rules or to what the program reads, sends, or writes, explain the current behavior, the problem it creates, the desired behavior, evidence, and tradeoffs. A proposal is not approval to change the project's design. Small documentation corrections can go directly to a pull request.

## Preserve the design

- The program does the mechanical work, and the model only writes the content. Keep reading, hiding secrets, checking quotes, naming, locking, writing, and indexing in the program.
- Read conversations only through Anthropic's Agent SDK. Do not parse Claude Code's internal conversation files directly.
- The writer is fixed: Claude Sonnet 5.5 with medium effort, and nothing is written if Claude Code uses another model. Changing it is a design change, not an incidental edit.
- Never overwrite or delete a handoff. Keep the folder name, the file names, the header fields, and the index format stable, because people and tools rely on them.
- Keep the plugin self-contained. The skill and the writer rules must not depend on a separate `AGENTS.md` or this guide.
- Keep both languages equivalent. The program is the same file in both folders except for its `LANGUAGE` line. Update both languages together.
- Distinguish observed behavior from documentation claims, assumptions, and proposed behavior. Do not claim quality or cost improvements without comparable measurements.
- Use plain language in English and Portuguese.

## Open a pull request

1. Fork the repository to your GitHub account. A fork is your own copy that you can edit.
2. Create a branch in your fork for one coherent change.
3. Edit the files and commit the change with a descriptive message.
4. Open a pull request from your branch to this repository's `main` branch. Link the relevant issue, if one exists.
5. Explain the problem, resulting behavior, verification, and limitations. Respond to review on the same branch.

A pull request proposes a change; it does not change this repository until the maintainer merges it. You can also contribute by reviewing proposals, reproducing reported failures, or supplying evidence without changing files.

## Verify proportionately

In the changed language folder, run `python3 -m unittest discover -s tests` and `claude plugin validate --strict .claude-plugin/plugin.json`. Check that links resolve and that YAML and JSON parse. For a translation or wording change, compare the meaning and obligations before and after.

For changes to the skill's description or to the conversation's steps, run the affected cases of the evaluation suite with `claude plugin eval . --allow-tools Write Edit Bash`. Evaluation runs call models through your account.

For changes to the writer rules or the program, also record a real handoff from a disposable conversation and check it against the conversation: decisions, authorizations, constraints, pending items, and quotes.

For a compatibility claim, identify the Claude Code version (CLI or app), the operating system, what you observed, and limitations. Use disposable resources and synthetic conversations. Never submit passwords, access tokens, private keys, personal data, private chat history, or unredacted handoffs.

## Review and releases

Jonathan Honorio maintains the project and decides whether a change is accepted. Reviews consider the stated problem, evidence, consistency with the design, and maintenance cost. Review does not imply a promised response time or acceptance.

Accepted changes are merged into `main`. A release identifies a selected repository version and describes its changes and known limitations. Installing or updating remains a user's decision; an open pull request or discussion is not a released change.

By submitting a contribution, you agree that your contribution is provided under this repository's [MIT License](LICENSE). Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
