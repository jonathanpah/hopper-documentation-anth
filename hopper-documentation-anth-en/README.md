# hopper-documentation-anth (English)

Claude Code plugin that documents each conversation in 7 Markdown documents, on request and before every compaction, so another person or another session can continue the work without rereading the conversation.

## What gets written

Inside the folder where the conversation was opened, the plugin keeps 1 `docs-by-hopper-documentation/` folder:

```text
docs-by-hopper-documentation/
├── 1-index.md                  index and reading order
├── 4-decisions.md              decisions of every conversation of the folder
├── 5-functions.md              implemented functions (finished deliveries)
├── 6-pending.md                open and closed pending items
└── conversations/
    └── 2026-11-01-e4bad083/    1 folder per conversation: date of the 1st message and code
        ├── 2-full-conversation.md
        ├── 3-simplified-conversation.md
        └── 7-handoff.md
```

- **Document 2** is the faithful copy of the messages, without tool results and without internal reasoning. Passwords, tokens and keys become `[hidden]`. It only receives additions, and each message has an identifier such as `M42-e4bad083`.
- **Documents 3 to 7** are written by Claude Sonnet 5.5, called headless (`claude -p`), without tools and in safe mode. The program validates the answer, numbers the items (`D1-e4bad083`, `F1-e4bad083`, `PD1-e4bad083`) and writes the files.
- **Document 7** is the handoff, rewritten in full on every run, with 9 sections.

## How it runs

- **Before every compaction**, automatic or manual, 2 commands of the `PreCompact` event run: the copy (synchronous, up to 60 seconds) and the writing (in a separate process, which finishes even if Claude Code is closed).
- **On request**, when you ask to document or record the conversation, save progress or write a handoff. The skill runs the same program in the background and reports the last line.
- **On the first run** in a folder with old-format handoffs (`index.md` and `handoff-*.md` at the root), the program migrates those files into documents 4 to 7 and deletes them. To turn automatic migration off, write `{"migracao_automatica": false}` to `config.json` in the data folder. The `migrar --pasta <project folder>` command migrates at any time.

Internal records live in the plugin's data folder, `~/.claude/plugins/data/hopper-documentation-anth-hopper-documentation-anth/`: `rodadas.jsonl` (1 line per step, with result and reason), `saidas/` (full output of each separate process), locks and diaries.

## Requirements

- Claude Code 2.1.284 or newer, in the CLI or in the app (local sessions), with access to Claude Sonnet 5.5 through your account.
- Python 3.9 or newer, standard library only.
- macOS or Linux.

## Installation

The `hopper-documentation-anth-en/` folder is the complete plugin and also the catalog. With a copy of it on the computer (a clone of the repository or a folder extracted from a tag):

```sh
claude plugin marketplace add /path/to/hopper-documentation-anth-en
claude plugin install hopper-documentation-anth@hopper-documentation-anth
```

In an open session, send `/reload-plugins`. Check with `claude plugin details hopper-documentation-anth@hopper-documentation-anth`: the skill and the `PreCompact` hook must appear. To update, update the copy and run `claude plugin uninstall --keep-data hopper-documentation-anth@hopper-documentation-anth` followed by `claude plugin install hopper-documentation-anth@hopper-documentation-anth`. This procedure also refreshes a copy with the same version and preserves the data folder and `config.json`. To remove, `claude plugin uninstall hopper-documentation-anth@hopper-documentation-anth`; the documents written in the projects remain.

## Limits and costs

- Each run with new content makes at least 1 call to Claude Sonnet 5.5 through your account. A new segment with more than 300,000 characters is split into parts, with 1 call per part. On models with a 1-million-token window, one compaction can produce several calls.
- The terminal Claude Code deletes transcript files older than 30 days. The copy before every compaction protects the conversation, but a run on request in a conversation that is too old fails with the reason "transcript file not found".
- The transcript file format is internal to Claude Code and may change. In that case the program fails with a clear reason, and the fix follows `CONTRIBUTING.md`.
- One run per conversation at a time. The second one waits up to 15 minutes.

## Tests

The acceptance tests of the spec live in `aceite/` at the root of the repository and run with `python3 -m unittest discover -s aceite/testes` (the `HOPPER_DOCUMENTATION_ANTH_PACOTE` variable picks the package). The executor tests live in `tests/`. The triggering evals live in `evals/` and run with `claude plugin eval ./hopper-documentation-anth-en --ablation none`.

## License

MIT. See `LICENSE`.
