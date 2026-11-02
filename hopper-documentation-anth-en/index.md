# Index of the English package

- `README.md`: what the plugin writes, how it runs, requirements, installation, limits and tests.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`: plugin manifest and catalog.
- `hooks/hooks.json`: the 2 commands of the `PreCompact` event (copy and writing).
- `scripts/hopper_documentation_anth.py`: the program (copier, writer call, writing, hooks and migration).
- `skills/hopper-documentation-anth/SKILL.md`: the skill, with what it produces and how it runs.
- `skills/hopper-documentation-anth/writing-rules.md` and `templates.md`: what the writer receives.
- `tests/`: executor tests.
- `evals/`: triggering evals (`claude plugin eval`).
- `LICENSE`: MIT license. Community files are at the repository root.
