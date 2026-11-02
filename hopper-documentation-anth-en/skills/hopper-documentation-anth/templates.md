# Document templates

The program writes the headers, the block titles and the final identifiers. You write the content. Use `N1`, `N2`… for new items in any field; the program replaces those references with the final identifiers.

Cite only messages from the new segment or before it and items that exist in the folder. Use `N1`, `N2`… for new items in this response. To discuss what comes after the new segment, write without an identifier. During migration, cite old files and items, since the messages do not exist.

## Document 3, simplified conversation

The `conversa_simplificada` field is the body of 1 block. It starts with the subject line and continues with short paragraphs. Each paragraph ends with the source messages in parentheses, separated by commas. A range uses the form `M3-e4bad083 a M7-e4bad083`.

```markdown
**Subject: failure of the automatic anth record.**

The automatic anth record failed before compaction. The program rejected 2 quotes that were not identical in the conversation. (M1-e4bad083)
```

When the segment brings nothing relevant, return `nada_relevante` equal to `true` and leave `conversa_simplificada` empty.

## Documents 4, 5 and 6, items

Each item of `itens_novos` has `tipo` (`D` decision, `F` implemented function, `PD` pending item), `texto` (1 or 2 sentences), `origem` (messages of the new segment or existing items), `situacao` and, only in pending items, `recomendacao` and `depende_de`. An "implemented function" is any delivery finished in the conversation: code, configuration, document or process.

Allowed statuses:

| Type | Statuses |
| --- | --- |
| D, decisions | `in force`, `replaced by <ID>`, `revoked in <M-ID>` |
| F, implemented functions | `done`, `replaced by <ID>`, `undone in <M-ID>` |
| PD, pending items | `open`, `closed in <M-ID> (<short reason>)` |

How the program writes an item:

```markdown
### PD1-e4bad083
Write the spec of the 7-document model.

- Recommendation: write it with the hopper-spec-anth skill.
- Depends on: Jonathan saying he is comfortable with the model.
- Source: M66-e4bad083
- Status: closed in M80-e4bad083 (the owner authorized the spec)
- Run range: M56-e4bad083 a M80-e4bad083
```

To change the status of an item that already exists, including one from another conversation of the same folder, use `mudancas`, with the identifier, the new status and the source. The source of a new item or a change is a message from the new segment or an existing item, never a message from an earlier segment. During migration, the source is the old file name.

## Document 7, handoff

The 9 keys of the `handoff` field become the 9 sections, in this order: Goal; Topics and current state; Next step; Decisions and authorizations in force; Constraints in force; Findings and discarded approaches; Pending items and commitments; Gaps; How to resume. Write each section in short paragraphs, each with the source messages in parentheses. The handoff is rewritten in full on every run: include what still holds from the previous handoff.

## Summary

The `resumo` field has up to 80 characters and goes to the folder index, in the "Subject" column.

## Migration

The `handoffs_antigos` field is a list with the last handoff of each old conversation. Each entry has `conversa` (identifier given in the file), `data`, `resumo` (up to 80 characters) and `handoff` (the 9 keys of document 7). In `data`, use the date of the conversation's last old handoff in `YYYY-MM-DD`, without a time, for example `2026-09-30`.

The `sem_conteudo` field lists the names of old files with no relevant content. During migration, each item of `itens_novos` also includes `conversa`.
