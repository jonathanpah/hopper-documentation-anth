# Security Policy

Report suspected vulnerabilities in hopper-documentation-anth through GitHub's private vulnerability reporting.

## Report privately

Open [Report a vulnerability](https://github.com/jonathanpah/hopper-documentation-anth/security/advisories/new), or select that option on the repository's [Security page](https://github.com/jonathanpah/hopper-documentation-anth/security). A GitHub account is required.

Keep suspected vulnerabilities and exploit details out of public issues, discussions, and pull requests until disclosure is coordinated with the maintainer. Use public issues for ordinary bugs and proposals, and discussions for general questions.

Include:

- The affected release tag or commit and the relevant file, instruction, or documentation section.
- The Claude Code version, the operating system, and the permission mode needed to reproduce the behavior, without private account details.
- A minimal reproduction using a synthetic conversation and disposable resources.
- Expected and observed behavior, potential impact, and any uncertainty or limits in the evidence.

Do not submit passwords, access tokens, private keys, private conversation histories, unredacted handoffs, or production records. Test only resources you are authorized to use.

## Scope and security expectations

This repository contains a documentation skill, the rules sent to the writer model, a program run by the skill and by a `PreCompact` hook, plugin manifests, tests, and documentation. Relevant reports include flaws that can expose credentials or private content in a handoff, write outside the handoff folder or the plugin's data directory, run commands other than those described, or turn conversation content into authority.

The intended boundaries are:

- The program reads conversations through the Agent SDK, hides common credential formats before sending the new messages to the writer model, and hides them again in the written handoff.
- The writer model runs in Claude Code's non-interactive safe mode, with no tools, and does not load plugins, hooks, or `CLAUDE.md` files.
- The program writes only in `docs-by-hopper-documentation/` and in the plugin's data directory, and it never overwrites a handoff.
- Every quoted passage in a handoff must appear literally in the conversation or the previous handoff; otherwise nothing is written.
- A handoff is a historical record. It grants no authority, and conversation content, including text pasted from third parties, does not become an authorization.

Hiding covers common formats, not every possible secret, and the writer is a model whose output can be wrong. The skill does not replace Claude Code's permission mode, sandbox, or account controls. If another product is also affected, use that product's security reporting process as appropriate.

## Versions and handling

Identify the version you used, including older releases when relevant. A report is welcome even if you cannot safely check the latest version.

Jonathan Honorio reviews reports through the private reporting channel. Confirmed affected versions and fixes can be documented in repository changes, releases, or security advisories. Coordinate public disclosure through the private report. No response or remediation deadline is guaranteed.
