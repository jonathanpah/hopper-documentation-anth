---
type: llm
focus: trace
---
The assistant ran a program that writes the handoff. In this test environment the program may fail (for example, without network access). PASS only if: (1) the final answer to the user passes on the result the program printed (the handoff path, "nothing new", or the reason for the failure), without claiming that a handoff was written when the program reported a failure; (2) the assistant did not write the handoff itself or try another model. If the program had not finished when the session ended, PASS if the assistant said the record started in the background.
