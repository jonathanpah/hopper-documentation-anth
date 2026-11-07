# hopper-documentation-anth

Claude Code plugin that documents each conversation in 7 Markdown documents, on request and before every compaction, so another person or session can continue the work. Version 2.1.0, built from `SPEC.md` (the changes of version 2.1 are at the end of the spec).

| Package | Language | README |
| --- | --- | --- |
| `hopper-documentation-anth-pt-br/` | Portuguese (Brazil) | [README.md](hopper-documentation-anth-pt-br/README.md) |
| `hopper-documentation-anth-en/` | English | [README.md](hopper-documentation-anth-en/README.md) |

Each package is a complete plugin and its own catalog (marketplace). Install one of them:

```sh
claude plugin marketplace add /path/to/hopper-documentation-anth-en
claude plugin install hopper-documentation-anth@hopper-documentation-anth
```

The program is the same file in both packages, except for the `LANGUAGE` line. The acceptance criteria of the spec live in `aceite/` and are frozen (see `CONTRIBUTING.md`). `index.md` lists the files.

License: MIT.
