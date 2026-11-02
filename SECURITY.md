# Security

## What the plugin does with your data

- It reads the Claude Code transcript of the current conversation and writes Markdown files inside the project's `docs-by-hopper-documentation/` folder and the plugin's data folder (`~/.claude/plugins/data/hopper-documentation-anth-hopper-documentation-anth/`). It writes nowhere else, except for the files Claude Code itself writes in its configuration folder when the writer runs.
- Passwords, tokens, keys and access codes are replaced by `[hidden]` in the full conversation before anything is sent to the writer or written to disk. The hiding rules are tested against the cases in `aceite/casos/b2/`.
- The writer (Claude Sonnet 5.5) runs headless, in safe mode, without tools, plugins, hooks, MCP servers or `CLAUDE.md` files. It receives only the new segment, the current documents, the writing rules and the templates, and it returns a JSON object that the program validates before writing.
- The program accepts a response only when Claude Sonnet 5.5 produced at least 90% of its output tokens.
- Tool results, internal reasoning, system reminders and hook outputs never enter the documents.

## What it does not protect against

- Secrets written in a form the hiding rules do not recognize. Review document 2 before sharing it.
- Secrets inside the writer's output that came from the conversation text in an unrecognized form.

## Reporting a vulnerability

Open a private security advisory on GitHub or an issue without the sensitive content. Include the plugin version (`claude plugin details hopper-documentation-anth@hopper-documentation-anth`), the Claude Code version and the lines of `rodadas.jsonl` involved.
