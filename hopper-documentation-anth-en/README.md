# hopper-documentation-anth

**English** | [Português (Brasil)](../hopper-documentation-anth-pt-br/README.md)

A Claude Code plugin that records the conversation in **handoffs**: Markdown files that tell someone who did not see the conversation where the work stands, what was decided, and how to continue. Another person, another Claude session, or another AI resumes the work by reading the most recent handoff and checking the real state, without opening the conversation.

## How it works

Recording happens at two moments:

- **On request:** when you ask to document or record the conversation, the skill runs the plugin's program in the background, and you keep working.
- **Before each compaction:** a hook (`PreCompact`) runs the same program in the background, for manual and automatic compaction. If it fails, the conversation is notified; compaction is not affected.

The program does the mechanical work and leaves only the writing to the model:

1. it reads the conversation's new messages since the last handoff through Anthropic's official library, the Agent SDK, without depending on the internal format of conversation files;
2. it keeps only the user's messages, the assistant's replies, the answers to questions, and the approved plans, and it hides passwords, tokens, and keys;
3. it asks Claude Sonnet 5.5, with medium effort and no tools, to write the content following the writer rules; if Claude Code uses another model, nothing is written;
4. it checks, letter by letter, every passage the handoff quotes; if one of them is not in the conversation, it asks for a correction once and, if it is still wrong, writes nothing. Sentences that attribute words or authorizations to the user without quoting them also get a second chance; if they remain, the handoff lists them under Gaps as the writer's interpretation;
5. it writes the handoff without ever overwriting a file, under a lock that prevents two writes at the same time in the same folder, and rebuilds the index.

Very long conversations are split into parts, each in a handoff that continues the previous one. When there is nothing new, the program does not call the model.

## What it writes

At the root of the working directory, the `docs-by-hopper-documentation/` folder receives:

- `handoff-YYYYMMDD-HHMMSS-<conversation>.md`, one file per record, never changed after it is written;
- `index.md`, with every handoff in the folder, including those in other formats, from the most recent to the oldest.

Each handoff has a header (date with the UTC offset, conversation, directory, previous handoff, trigger, model and effort used, and the last recorded message) and nine sections: goal, topics and current state, next step, decisions and authorizations, constraints in force, findings and discarded approaches, pending items and commitments, gaps, and how to resume.

## What it runs, sends, and fetches

- **Runs:** `python3` with the plugin's program; Claude Code's own executable, in non-interactive mode, with no tools and without loading plugins, to write the content; `git` only to read the directory's state.
- **Sends:** the conversation's new messages, with secrets hidden, to Claude Sonnet 5.5, through your Claude account.
- **Fetches:** on the first run, it installs the Agent SDK (`claude-agent-sdk`, pinned version) from PyPI into its own Python environment, in the plugin's data directory (`${CLAUDE_PLUGIN_DATA}`), about 55 MB.
- **Writes:** only in the handoff folder and in the plugin's data directory, which holds the Python environment, the locks, and a run log.

## Requirements

- Claude Code, in the CLI or the app, on macOS or Linux.
- Python 3.9 or newer for the program, and Python 3.10 or newer, with the `venv` module, for Anthropic's library. The program finds a Python 3.10 or newer on its own: the system one, a `python3.1x` on PATH or in `~/.local/bin`, Homebrew's, or the python.org installer's. On Debian and Ubuntu, the `venv` module requires the `python3-venv` package (for example, `python3.13-venv`). macOS ships only Python 3.9; install a newer one first.
- Access to PyPI on the first run.

## Model

The writer is always Claude Sonnet 5.5 with medium effort. There is no option to change it. If that model is not available, the record reports the problem and does not use another one.

## Installation

The plugin and the skill are named `hopper-documentation-anth` in both languages. Choose one language. The `hopper-documentation-anth-en/` folder contains the complete English plugin: the skill, the program, the hook, and the tests.

Clone the repository once:

```sh
mkdir -p "$HOME/.local/share"
git clone https://github.com/jonathanpah/hopper-documentation-anth.git "$HOME/.local/share/hopper-documentation-anth"
```

If the destination already exists, check its origin and local changes before updating it.

In Claude Code:

```sh
claude plugin marketplace add "$HOME/.local/share/hopper-documentation-anth/hopper-documentation-anth-en"
claude plugin install hopper-documentation-anth@hopper-documentation-anth
```

In a session that is already open, send `/reload-plugins` as a separate message. Check with `claude plugin details hopper-documentation-anth@hopper-documentation-anth`: the skill and the hook should appear. A CLI installation does not prove presence in the app: in the Claude app, check **Customize → Plugins → Yours** and **Skills → Yours**.

The skill's full identifier is `hopper-documentation-anth:hopper-documentation-anth`: the first part names the plugin, and the second, the skill.

## Use

Ask in plain language, for example "document this conversation" or "record what we did so I can continue tomorrow", or invoke `/hopper-documentation-anth:hopper-documentation-anth`. Explaining, reviewing, or editing the skill writes nothing.

To resume in a new session, ask Claude to read the folder's `index.md` and the conversation's most recent handoff and follow its "How to resume" section.

## Limits

- The handoff is written from the conversation's text messages, not from tool output. A result that only appeared in a command's output goes in as the assistant's report, and the handoff says so. The program reads the git state at the time of the record.
- The Agent SDK reads the conversation since the last compaction. The record before compaction keeps the part that would be summarized; after it, the next handoff starts from the previous one and records the limitation.
- Hiding covers common credential formats, not every possible secret.
- Models are not deterministic. The quote check proves that each quoted passage exists, not that the text written from it is faithful.
- A handoff is a historical record. It does not replace checking the real state, and it does not authorize repeating completed operations.
- Windows is not supported.

## Tests

```sh
python3 -m unittest discover -s tests
```

The tests call no model and install nothing. The behavior suite is in `evals/` and runs with Claude Code's official evaluation, which calls models through your account:

```sh
claude plugin eval . --allow-tools Write Edit Bash
```

## Updates and removal

Check local changes and update the clone with `git pull --ff-only`. Then run `claude plugin marketplace update hopper-documentation-anth` and `claude plugin update hopper-documentation-anth@hopper-documentation-anth`, and send `/reload-plugins` in open sessions.

To remove it, use `claude plugin uninstall hopper-documentation-anth@hopper-documentation-anth`. The handoffs written in your projects remain.

## Contributing

For suspected vulnerabilities, follow the [Security Policy](../SECURITY.md) and report privately. Use [Issues](https://github.com/jonathanpah/hopper-documentation-anth/issues) for reproducible problems and concrete proposals, and [Discussions](https://github.com/jonathanpah/hopper-documentation-anth/discussions) for questions and ideas. See [CONTRIBUTING.md](../CONTRIBUTING.md) and the [Code of Conduct](../CODE_OF_CONDUCT.md).

## License and maintainer

Copyright (c) 2026 Jonathan Honorio. Released under the [MIT License](LICENSE).

Maintained by [Jonathan Honorio (@jonathanpah)](https://github.com/jonathanpah). This is an independent project, with no claim of affiliation with or endorsement by Anthropic.
