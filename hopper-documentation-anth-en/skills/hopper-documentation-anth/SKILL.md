---
name: hopper-documentation-anth
description: Documents the current Claude Code conversation, or another conversation given by its code, in 7 documents (index, full conversation, simplified conversation, decisions, implemented functions, pending items and handoff) in the project's docs-by-hopper-documentation folder. Use when the user asks to document or record the conversation, save progress, write a handoff or document another conversation before continuing it. Do not use to explain, review or edit this skill.
compatibility: Requires Claude Code 2.1.284 or newer, in the CLI or in the app, with the hopper-documentation-anth plugin and Python 3.9 or newer.
allowed-tools: Bash(python3 *)
---

# hopper-documentation-anth

## What the skill produces

The skill documents the conversation in 7 Markdown documents, inside `docs-by-hopper-documentation/`, in the folder where the conversation was opened. There is 1 such folder per project folder, and 1 subfolder per conversation.

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

- **Document 2, full conversation.** A faithful copy of the user's and Claude's messages, without tool results, without internal reasoning and with passwords and tokens replaced by `[hidden]`. Each tool use becomes 1 line. It only receives additions. Each message has an identifier such as `M42-e4bad083`.
- **Document 3, simplified conversation.** The same content, rewritten in short sentences, 1 block per run, with the source message at the end of each paragraph.
- **Documents 4, 5 and 6.** Items numbered per conversation (`D1-e4bad083`, `F1-e4bad083`, `PD1-e4bad083`), each with source, status and the range of the run that created it.
- **Document 7, handoff.** Rewritten in full on every run, with 9 sections: goal, topics and current state, next step, decisions and authorizations in force, constraints in force, findings and discarded approaches, pending items and commitments, gaps and how to resume.
- **Document 1, index.** The reading order and the table of the folder's conversations.

The plugin's program writes document 2 without AI. Claude Sonnet 5.5, called headless (`claude -p`) and without tools, writes the content of documents 3 to 7 following `writing-rules.md` and `templates.md` in this folder. The program validates the answer, numbers the items and writes the files.

The same run happens by itself before every compaction, through a plugin hook. The first run in a folder that has old-format handoffs (`index.md` and `handoff-*.md` at the root) migrates those files and deletes them when the `migracao_automatica` setting is on, as it is by default.

## How the skill runs

When the user asks to document or record the conversation, save progress or write a handoff, follow these steps.

1. Run the command below now, in this same response, with the Bash tool in the background.

   ```sh
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hopper_documentation_anth.py" rodada --sessao "${CLAUDE_SESSION_ID}"
   ```

   If the request is to document another conversation, replace `"${CLAUDE_SESSION_ID}"` with the code the user gives. The code has 8 or 12 letters and appears in the table of the folder's index, as in "document conversation b2b21be3". The full identifier also works. The other conversation must have run on this same machine and in this same account.

2. Say in 1 sentence that the documentation started in the background.
3. When the program finishes, repeat the last line of its output to the user, without changing the text.

Do not write or edit any file of `docs-by-hopper-documentation/` yourself. If the program fails, report the failure. Do not try another model or another path.

Do not run the skill when the request is to explain, review or edit the skill, or when the question is about what a handoff is.
