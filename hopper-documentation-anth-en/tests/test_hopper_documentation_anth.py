"""Tests of the skill program. They call no model and install nothing."""

import datetime
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import hopper_documentation_anth as hd  # noqa: E402

SESSION = "3f9c2a71-5b8e-4d0a-9c61-2e7f4b1a8d05"
TOKEN = "ghp_" + "Ab1" * 12


def msg(kind, uuid, content, sidechain=False):
    return {"type": kind, "uuid": uuid, "message": {"role": kind, "content": content}, "sidechain": sidechain}


def content(**over):
    base = {"nothing_new": False, "summary": "Test work", **{k: "text " + k for k in hd.SECTION_KEYS}}
    base.update(over)
    return base


class Mask(unittest.TestCase):
    def test_tokens(self):
        for secret in (TOKEN, "sk-ant-api03-abcdefghijklmnop", "xoxb-123456789012-abcdefghij", "AKIAABCDEFGHIJKLMNOP",
                       "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N"):
            self.assertNotIn(secret, hd.mask("value " + secret + " end"))

    def test_labeled_values(self):
        self.assertEqual(hd.mask("senha: Abc123xyz"), "senha: " + hd.MASK)
        self.assertEqual(hd.mask("API_KEY=abcdef123456"), "API_KEY=" + hd.MASK)
        self.assertEqual(hd.mask("o token é zz11yy22xx"), "o token é " + hd.MASK)
        self.assertIn(hd.MASK, hd.mask("postgres://user:segredo1@host/db"))

    def test_markdown_code_and_generated(self):
        for text in ("- **Password:**\n```\nXy1#Ab2Cd3Ef4Gh5\n```", "**password**: `Xy1Ab2Cd3Ef4`",
                     "key Xy1Ab2Cd3Ef4Gh5Ij6K end"):
            masked = hd.mask(text)
            self.assertNotIn("Xy1", masked, text)

    def test_ordinary_text_stays(self):
        for text in ("Troque a senha e apague o rascunho; o token e a chave ficam no cofre.",
                     "The password is stored in the vault and the token is rotated weekly."):
            self.assertEqual(hd.mask(text), text)

    def test_technical_identifiers_stay(self):
        text = ("commit a41e9d2b5c sha256 " + "a" * 64 + " uuid " + SESSION + " max_tokens: 4096 "
                "/home/user/.claude/plugins/cache/x/0.1.0 example-plugin-name "
                "CLAUDE_CODE_SESSION_ID ExampleRelease20260101 msg_" + "0" * 4 + "ExampleMessageId")
        self.assertEqual(hd.mask(text), text)


class Conversation(unittest.TestCase):
    def test_keeps_texts_answers_and_plans(self):
        messages = [
            msg("user", "u1", "Create the script."),
            msg("assistant", "a1", [{"type": "thinking", "thinking": "x"},
                                    {"type": "tool_use", "id": "t1", "name": "Bash", "input": {}},
                                    {"type": "text", "text": "Created."}]),
            msg("user", "u2", [{"type": "tool_result", "tool_use_id": "t1", "content": "tool output"}]),
            msg("assistant", "a2", [{"type": "tool_use", "id": "q1", "name": "AskUserQuestion",
                                     "input": {"questions": [{"question": "Which?"}]}}]),
            msg("user", "u3", [{"type": "tool_result", "tool_use_id": "q1", "content": "Option A"}]),
            msg("user", "u4", "<task-notification>x</task-notification>"),
            msg("user", "u5", "Another Claude session sent a message: report"),
            msg("assistant", "s1", "side chain", sidechain=True),
        ]
        entries = hd.conversation(messages)
        self.assertEqual([e[0] for e in entries], ["user", "assistant", "answer", "agent"])
        self.assertIn("Option A", entries[2][1])
        self.assertNotIn("tool output", " ".join(e[1] for e in entries))

    def test_after_cursor_and_gap(self):
        entries = [("user", "a", "1"), ("assistant", "b", "2"), ("user", "c", "3")]
        self.assertEqual(hd.after(entries, "2"), ([("user", "c", "3")], False))
        self.assertEqual(hd.after(entries, "gone"), (entries, True))
        self.assertEqual(hd.after(entries, None), (entries, False))

    def test_parts_keep_order_and_cursor(self):
        with mock.patch.object(hd, "PART_LIMIT", 60):
            parts = hd.split_parts(hd.render([("user", "x" * 30, "1"), ("assistant", "y" * 30, "2"),
                                              ("user", "z", "3")]))
        self.assertGreater(len(parts), 1)
        self.assertEqual(parts[-1][-1][1], "3")


class Quotes(unittest.TestCase):
    sources = ["<message>You may fix it and   commit on the fix-shipping branch. Do not publish anything now.</message>"]

    def check(self, text):
        return hd.unverified_quotes({"decisions": text}, self.sources)

    def test_literal_and_cut_quotes_pass(self):
        self.assertEqual(self.check('Authorization: "You may fix it and commit on the fix-shipping branch".'), [])
        self.assertEqual(self.check('“You may fix it and commit… Do not publish anything now”'), [])
        self.assertEqual(self.check('Said "You may fix it and `commit` on the **fix-shipping** branch" today.'), [])

    def test_invented_or_paraphrased_quote_fails(self):
        self.assertEqual(len(self.check('Said "You may publish the new version on GitHub".')), 1)
        self.assertEqual(len(self.check('Said "You may fix and commit on the fix-shipping branch".')), 1)

    def test_pairs_of_quotes_are_read_separately(self):
        self.assertEqual(self.check('"Do not publish anything now"; "You may fix it and commit"'), [])

    def test_short_and_inner_quotes_are_ignored(self):
        self.assertEqual(self.check('commit "Adds" and --settings \'{"a":"a rather long value"}\''), [])


class Attributions(unittest.TestCase):
    def test_flags_only_unquoted_affirmative_attributions(self):
        found = hd.unquoted_attributions({"topics": "O usuário relatou ter fechado o pedido. "
                                                    "The user did not authorize publishing. "
                                                    'The user asked: "Leave it pending for later". '
                                                    "The assistant said it was done."})
        self.assertEqual(found, ["O usuário relatou ter fechado o pedido."])


class Files(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_never_overwrites(self):
        target = self.folder / "handoff-20260101-000000-abcdefgh.md"
        hd.write_atomic(target, "one")
        with self.assertRaises(FileExistsError):
            hd.write_atomic(target, "two")
        self.assertEqual(target.read_text(), "one")
        self.assertEqual([p.name for p in self.folder.iterdir()], [target.name])

    def test_index_reads_both_languages_and_other_formats(self):
        own = hd.assemble(content(summary="New summary"),
                          {"date": "2026-01-15 10:16:55 +00:00", "conversation": SESSION, "directory": "/d",
                           "previous": "none", "trigger": "x", "writer": "y", "last": "u9"})
        (self.folder / "handoff-20260115-101655-3f9c2a71.md").write_text(own)
        (self.folder / "handoff-20260115-101700-3f9c2a71.md").write_text(
            "# Handoff: English one\n\n- **Date:** 2026-01-15 10:17:00 +00:00\n- **Conversation:** " + SESSION +
            "\n- **Last recorded message:** u10\n")
        (self.folder / "handoff-20260115-101149.md").write_text(
            "# Handoff 2026-01-15 10:11:49\n\n- Resumo: Outro formato\n- Conversa: " + SESSION + "\n")
        (self.folder / "handoff-20260114-100000.md").write_text("no header\n")
        hd.rebuild_index(self.folder)
        lines = [l for l in (self.folder / "index.md").read_text().splitlines() if l.startswith("- ")]
        self.assertEqual(len(lines), 4)
        self.assertIn("English one", lines[0])
        self.assertIn("New summary", lines[1])
        self.assertIn("Outro formato", lines[2])
        self.assertIn("2026-01-14 10:00:00", lines[3])
        previous = hd.previous_handoff(self.folder, SESSION)
        self.assertEqual(previous.name, "handoff-20260115-101700-3f9c2a71.md")
        self.assertEqual(hd.header_of(previous)["last"], "u10")

    def test_assemble_has_all_sections_and_masks(self):
        text = hd.assemble(content(summary="r" * 80, gaps="senha: Abc123xyz", goal=""),
                           {k: "v" for k in hd.HEADER_KEYS})
        self.assertTrue(text.startswith("# Handoff: " + "r" * 59 + "…"))
        for _, title in hd.SECTIONS:
            self.assertIn("## " + title + "\n", text)
        self.assertIn(hd.T["nothing"], text)
        self.assertNotIn("Abc123xyz", text)

    def test_offset_label(self):
        moment = datetime.datetime(2026, 1, 15, 10, 1, 2, tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))
        self.assertEqual(hd.offset_label(moment), "2026-01-15 10:01:02 -05:00")


class Flow(unittest.TestCase):
    """The full flow with the model and the conversation reader simulated."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = Path(self.tmp.name, "proj")
        self.cwd.mkdir()
        self.data = Path(self.tmp.name, "data")
        self.messages = [msg("user", "u1", "You may fix the shipping. Do not publish anything."),
                         msg("assistant", "a1", [{"type": "text", "text": "Fixed."}])]
        self.calls = []
        for patch in (mock.patch.object(hd, "ensure_sdk", return_value="py"),
                      mock.patch.object(hd, "find_claude", return_value="claude"),
                      mock.patch.object(hd, "read_messages", side_effect=lambda *a: list(self.messages)),
                      mock.patch.object(hd, "git_state", return_value=None)):
            patch.start()
            self.addCleanup(patch.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def model(self, *answers):
        answers = list(answers)

        def fake(claude, prompt, model, effort, cwd):
            self.calls.append(prompt)
            answer = answers.pop(0)
            if isinstance(answer, Exception):
                raise answer
            return answer, [model], 0.01
        return mock.patch.object(hd, "call_model", side_effect=fake)

    def run_doc(self, trigger="x"):
        return hd.document(SESSION, str(self.cwd), str(self.data), trigger)

    def folder(self):
        return self.cwd / hd.FOLDER

    def handoffs(self):
        return sorted(self.folder().glob("handoff-*.md"))

    def test_first_handoff_header_index_and_cursor(self):
        (self.cwd / "README.md").write_text("doc")
        with self.model(content(constraints='"You may fix the shipping. Do not publish anything."')):
            out = self.run_doc()
        self.assertTrue(out.startswith(hd.T["written"]))
        text = self.handoffs()[0].read_text()
        self.assertIn(hd.T["writer"].format(hd.MODEL, hd.EFFORT), text)
        self.assertIn(hd.HEADER_FIELDS["last"] + ":** a1", text)
        self.assertIn("README.md", self.calls[0])
        self.assertIn(self.handoffs()[0].name, (self.folder() / "index.md").read_text())

    def test_nothing_new_skips_the_model(self):
        with self.model(content()):
            self.run_doc()
        with self.model():
            out = self.run_doc()
        self.assertTrue(out.startswith(hd.T["nothing_new"]))
        self.assertEqual(len(self.calls), 1)

    def test_incremental_sends_only_new_messages_and_links_previous(self):
        with self.model(content()):
            self.run_doc()
        self.messages.append(msg("user", "u2", "A new message from the user."))
        with self.model(content(summary="Second")):
            self.run_doc()
        new_part = self.calls[1].split("<" + hd.T["new_tag"] + ">")[1]
        self.assertNotIn("You may fix the shipping", new_part)
        self.assertIn("A new message from the user.", new_part)
        self.assertIn("[handoff-", self.handoffs()[-1].read_text())

    def test_model_says_nothing_new(self):
        with self.model(content()):
            self.run_doc()
        self.messages.append(msg("user", "u2", "Record the conversation."))
        with self.model(content(nothing_new=True)):
            out = self.run_doc()
        self.assertTrue(out.startswith(hd.T["nothing_new"]))
        self.assertEqual(len(self.handoffs()), 1)

    def test_gap_after_compaction_is_reported_to_the_model(self):
        with self.model(content()):
            self.run_doc()
        self.messages[:] = [msg("user", "c1", "Compaction summary."), msg("user", "u3", "New request.")]
        with self.model(content()):
            self.run_doc()
        self.assertIn(hd.T["gap_note"], self.calls[1])

    def test_bad_quote_is_retried_then_accepted(self):
        bad = content(decisions='"You may publish everything today"')
        good = content(decisions='"You may fix the shipping"')
        with self.model(bad, good):
            self.assertTrue(self.run_doc().startswith(hd.T["written"]))
        self.assertIn("You may publish everything today", self.calls[1].split(hd.T["retry"])[1])

    def test_bad_quote_twice_writes_nothing(self):
        bad = content(decisions='"You may publish everything today"')
        with self.model(bad, bad), self.assertRaises(hd.Failure):
            self.run_doc()
        self.assertEqual(self.handoffs(), [])

    def test_unquoted_attribution_is_retried_then_listed_under_gaps(self):
        bad = content(topics="The user confirmed that the deploy finished.")
        with self.model(bad, bad):
            self.run_doc()
        gaps = self.handoffs()[0].read_text().split("## " + hd.T["sections"][7])[1]
        self.assertIn("confirmed that the deploy finished", gaps)
        self.assertIn(hd.T["retry_attr"][:20], self.calls[1])

    def test_model_failure_writes_nothing(self):
        with self.model(hd.Failure("unavailable")), self.assertRaises(hd.Failure):
            self.run_doc()
        self.assertEqual(list(self.folder().glob("handoff-*")), [])

    def test_long_conversation_is_split_into_chained_parts(self):
        self.messages[:] = [msg("user", "m%d" % i, "x" * 50) for i in range(9)]
        with mock.patch.object(hd, "PART_LIMIT", 200), self.model(*[content() for _ in range(9)]):
            self.run_doc()
        files = self.handoffs()
        self.assertGreater(len(files), 1)
        self.assertIn(hd.T["part_note"].format(1, len(files)), self.calls[0])
        self.assertEqual(hd.header_of(files[-1]).get("last"), "m8")
        index = [l for l in (self.folder() / "index.md").read_text().splitlines() if l.startswith("- ")]
        self.assertEqual(len(index), len(files))

    def test_secrets_never_reach_model_or_file(self):
        self.messages.append(msg("user", "u9", "the password is Example22secret and the token " + TOKEN))
        with self.model(content(gaps="token " + TOKEN)):
            self.run_doc()
        self.assertNotIn("Example22secret", self.calls[0])
        self.assertNotIn(TOKEN, self.calls[0])
        self.assertNotIn(TOKEN, self.handoffs()[0].read_text())

    def test_concurrent_runs_do_not_duplicate(self):
        results = []

        def fake(claude, prompt, model, effort, cwd):
            time.sleep(0.2)
            return content(), [model], 0.01
        with mock.patch.object(hd, "call_model", side_effect=fake):
            threads = [threading.Thread(target=lambda: results.append(self.run_doc())) for _ in range(4)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        self.assertEqual(len(self.handoffs()), 1)
        self.assertEqual(sum(r.startswith(hd.T["nothing_new"]) for r in results), 3)


class Model(unittest.TestCase):
    def test_fixed_model_and_effort(self):
        self.assertEqual((hd.MODEL, hd.EFFORT), ("claude-sonnet-5-5", "medium"))

    def test_fallback_to_another_model_fails(self):
        out = json.dumps({"is_error": False, "structured_output": {}, "modelUsage": {"claude-opus-5-5": {}}})
        with mock.patch("subprocess.run", return_value=mock.Mock(stdout=out, stderr="", returncode=0)):
            with self.assertRaises(hd.Failure):
                hd.call_model("claude", "p", hd.MODEL, hd.EFFORT, "/tmp")


class Python(unittest.TestCase):
    def test_current_python_is_used_when_new_enough(self):
        with mock.patch.object(hd.sys, "version_info", (3, 13, 0)):
            self.assertEqual(hd.sdk_python(), hd.sys.executable)

    def test_old_python_without_alternative_fails_clearly(self):
        with mock.patch.object(hd.sys, "version_info", (3, 9, 0)), \
                mock.patch.object(hd.shutil, "which", return_value=None), \
                mock.patch.object(hd.os, "access", return_value=False):
            with self.assertRaises(hd.Failure) as error:
                hd.sdk_python()
        self.assertIn("3.10", str(error.exception))


class Hook(unittest.TestCase):
    def test_child_run_does_nothing(self):
        with mock.patch.dict(os.environ, {hd.RUN_FLAG: "1"}):
            self.assertEqual(hd.command_hook(), 0)

    def test_failure_wakes_the_conversation(self):
        event = json.dumps({"session_id": SESSION, "cwd": "/tmp", "trigger": "auto"})
        with tempfile.TemporaryDirectory() as data, \
                mock.patch.dict(os.environ, {"CLAUDE_PLUGIN_DATA": data}), \
                mock.patch("sys.stdin", io.StringIO(event)), \
                mock.patch.object(hd, "document", side_effect=hd.Failure("model unavailable")), \
                mock.patch("sys.stderr", new_callable=io.StringIO) as err:
            self.assertEqual(hd.command_hook(), 2)
        self.assertIn("model unavailable", err.getvalue())


if __name__ == "__main__":
    unittest.main()
