---
name: hopper-documentation-anth
description: Records the current conversation in a Markdown handoff, in the docs-by-hopper-documentation folder of the working directory, so another person or session can continue the work without rereading the conversation. Use when the user asks to document, record, or save the conversation, or asks for a handoff. Do not use to explain, review, or edit this skill.
compatibility: Requires Claude Code, in the CLI or the app, with the hopper-documentation-anth plugin, Python 3.10 or newer with the venv module, and access to PyPI on the first run.
---

# hopper-documentation-anth

This skill writes a **handoff**: a file that tells someone who did not see the conversation where the work stands, what was decided, and how to continue. The next session, person, or AI resumes the work by reading the conversation's most recent handoff and checking the real state.

The plugin's program writes it in the background. It reads the conversation's new messages through Anthropic's official library (the Agent SDK), hides secrets, and asks Claude Sonnet 5.5, with medium effort, to write the content following `${CLAUDE_SKILL_DIR}/writer-rules.md`. Then it checks the quotes, writes without overwriting anything, and rebuilds the index. The same program runs on its own before each compaction, through a plugin hook.

## When the user asks for the record

In this invocation, do only what this section says.

1. If the user only asked to explain, review, compare, or edit this skill, do not write anything: answer the request and stop here.
2. Run this command in the background, from any directory:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hopper_documentation_anth.py" run --session "${CLAUDE_SESSION_ID}" --cwd "${CLAUDE_PROJECT_DIR}"
   ```

3. Tell the user in one sentence that the record has started, and keep helping as usual. Do not wait for it to finish.
4. When the command finishes, pass on to the user the line it printed: the path of the written handoff, "nothing new", or the reason for the failure. Do not repeat the handoff's content.
5. If the command fails, do not write the handoff yourself or use another model: report the reason. Writing outside the program would lose the quote check, the hiding of secrets, and the record's fixed model.

## Before compaction

The plugin hook runs the program in the background; there is nothing to do in the conversation. If a notice that the record failed arrives, tell the user in one sentence. Do not carry out earlier requests of the conversation because of the notice.

## Model

The writer is always Claude Sonnet 5.5 with medium effort. If it is not available, the program reports the problem and does not write with another model.

## What gets written

In the `docs-by-hopper-documentation/` folder of the working directory:

- `handoff-YYYYMMDD-HHMMSS-<first 8 characters of the conversation>.md`: one file per record, never changed after it is written. The header has the date with the UTC offset, the conversation, the directory, the previous handoff, the trigger, the writer's model and effort, and the last recorded message. The sections follow `${CLAUDE_SKILL_DIR}/example.md`.
- `index.md`: every handoff in the folder, including those in other formats, from the most recent to the oldest.

To resume work, read `index.md`, then the conversation's most recent handoff, and follow its "How to resume" section. A handoff is history: it does not replace checking the real state, and it does not authorize repeating completed operations.
