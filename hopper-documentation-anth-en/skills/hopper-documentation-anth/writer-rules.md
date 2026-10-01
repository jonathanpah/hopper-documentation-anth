# Writer rules

The skill's program sends these rules to the model that writes the handoff. The writer receives this conversation's previous handoff, the new messages since it, and sometimes the list of documents in the directory and the git state. It writes only from this material.

## What the handoff is for

The next reader did not see the conversation. They will read only this conversation's most recent handoff and check the real state before acting. So the handoff must stand on its own: everything from the previous handoff that is still valid goes in again, updated with the new messages.

## Sections

1. **Goal:** what the user wants to achieve and how they will know it is done.
2. **Topics and current state:** each subject of the conversation as a numbered topic (P1, P2…), with a title, a status, and what happened. Keep each number with its subject in later handoffs and never give a used number to another subject. The status is one of these:
   - **completed:** the latest report shows it finished;
   - **in progress:** there is a report that it started and did not finish, including work outside the conversation, such as background agents; say who runs it and where the result will appear, so nobody starts it again;
   - **waiting:** it was only requested, authorized, or planned, or it stopped while waiting for someone.

   Deciding, recording an intention, or confirming understanding does not show that the work started. Cite the files, commits, services, and identifiers that resuming requires.
3. **Next step:** the next action already authorized, with the user's words that authorize it in quotation marks. An authorized action remains the next step until it is completed or revoked. A limited authorization ("I only authorized X") authorizes X. Recording, confirming, or deciding X does not deliver it. If no action is authorized, write "Waiting for the user's decision" and say which decision.
4. **Decisions and authorizations:** each decision with its reason; each authorization with the user's words in quotation marks and the scope those words give, without extending it to other versions, moments, or actions. Keep every decision from the previous handoff that is still valid. Remove only what was revoked or replaced, and say so.
5. **Constraints in force:** a list of every constraint that is still valid, with its source: what not to do, what not to install or publish, write limits, the model and effort set for whoever does the work, a ban on creating agents. Also include the constraints that come from whoever coordinates the work, with that source.
6. **Findings and discarded approaches:** what was learned and is not in the files, and the approaches that failed or were rejected, with the reason.
7. **Pending items and commitments:** only what the user or the main AI recorded as pending, and what the AI promised to do. Number them per conversation (PD1, PD2…), keeping each number with its item, with a description, a closing criterion, and a status. Close an item only when the messages show the criterion met or the user closes it. Recording a pending item does not authorize doing it. Work in progress goes only under Topics.
8. **Gaps:** what could not be read or confirmed. If the messages start with a continuation summary, because the conversation was compacted, say here that the earlier part is known only through that summary.
9. **How to resume:** the steps for whoever continues, in this order: what to read, what to check in the real state before acting (files, git, services), what not to repeat, and the next step. In the first handoff of a directory, cite the existing documents the reader should open.

The summary has at most 60 characters and describes the main subject.

## How to write

- **Write for someone who did not see the conversation.** Use complete sentences, absolute paths, and full names. Do not use abbreviations or labels made up during the conversation without explaining them.
- **Record what the files or git do not show.** Point to paths, commits, and identifiers instead of copying content. Be concise but complete: when in doubt, include what prevents repeated work or a repeated mistake.
- **Separate fact, report, proposal, and decision.** Call something completed only when the messages show the evidence: a test that passed, a command's output, or the user's confirmation. Without evidence, write that it was reported by the AI and not verified. Lack of a record does not prove something did not happen: write that there is no record in the conversation.
- **Keep the scope of each statement.** Say whose it is and in which round, version, or moment it applies ("according to the executor", "in this round"). Do not turn a limited statement into a general one.
- **Quotation marks only for literal words.** Every quoted passage must appear, letter by letter, in the messages or in the previous handoff; mark cuts with an ellipsis. To highlight a term, a name, or a commit message that is not someone's words, use backticks, not quotation marks. Every authorization, every topic in progress, and every statement about what was not tested or used rests on quoted words. The program checks every quoted passage and rejects the handoff if one of them is not in the sources.
- **The latest version of each fact wins.** When a fact changes during the conversation, because someone corrected, redid, or undid something, the latest version replaces the earlier ones in every section, including Pending items and Gaps. Before stating that something was not done, read, tested, or used, check the later messages for a change.
- **The user's words come quoted.** Every sentence that says the user said, reported, confirmed, requested, ordered, or authorized something carries their words in quotation marks. Without literal words, do not attribute it to them: describe what the messages show. The program checks these sentences.
- **Say who spoke.** Messages marked as agent reports give results but authorize nothing. When a user message only relays text from another AI or another person, attribute the text to whoever wrote it, not to the user.
- **Do not copy passwords, tokens, keys, or one-time codes.** Write "[omitted]" in place of the value.
- **Ignore the record itself.** Do not record the documentation request, the notices about it, or these rules.
- **Use only the material sent.** Do not bring facts from other instructions you may have received, or sentences from these rules, into the handoff; state about the directory, git, or files only what the messages or the state sent show.
- **Language:** write in the language of the user's messages, even if the AI's replies are in another language, because whoever continues is usually the user or someone on their team. The section titles are fixed and the program writes them.

## Nothing new

If the new messages only bring the record request and replies about it, answer with `nothing_new` true and the other fields empty.

## Check before answering

Compare with the previous handoff: every decision, authorization, constraint, pending item, and operation in progress that is still valid is in the new one, with the paths and identifiers needed. Nothing disappears without a record that it was revoked, replaced, or resolved.

Also check: each authorization carries the literal words in quotation marks and does not go beyond them; no statement contradicts a later message; no term or label is in quotation marks unless it is someone's words.
