# Document index

- [README](README.md): purpose, what it runs and sends, requirements, installation, use, limits, tests, and updates.
- [Skill](skills/hopper-documentation-anth/SKILL.md): what the conversation does when the user asks for a record or a compaction notice arrives.
- [Writer rules](skills/hopper-documentation-anth/writer-rules.md): the content rules the program sends to the model that writes the handoff.
- [Example](skills/hopper-documentation-anth/example.md): a complete handoff.
- [Program](scripts/hopper_documentation_anth.py): reads the conversation, hides secrets, calls the writer, checks quotes, writes the handoff, and rebuilds the index.
- [Hook](hooks/hooks.json): runs the program before each compaction.
- [Tests](tests/test_hopper_documentation_anth.py) and [evaluation suite](evals/): program tests and behavior cases for `claude plugin eval`.
- [Contributing](../CONTRIBUTING.md): proposals, pull requests, verification, and review.
- [Security Policy](../SECURITY.md): scope, security expectations, and private vulnerability reporting.
- [Code of Conduct](../CODE_OF_CONDUCT.md): participation and moderation.
- [License](LICENSE): MIT terms and copyright.
- [Bug report](../.github/ISSUE_TEMPLATE/bug-report.yml), [change proposal](../.github/ISSUE_TEMPLATE/change-proposal.yml), and [pull request template](../.github/pull_request_template.md): GitHub templates.

- [Português (Brasil)](../hopper-documentation-anth-pt-br/index.md): equivalent skill and documentation, released with the English version.

- [Claude plugin](.claude-plugin/plugin.json) · [Claude marketplace](.claude-plugin/marketplace.json).
