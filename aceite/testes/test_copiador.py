"""Testes de aceite T04 a T10 (conversa integral, documento 2). Critério congelado da spec, seção 5.2."""
import json
import threading
import time
import unittest

from apoio import CASOS, CODIGO_B1, IDIOMA, SESSAO_B1, CasoDeAceite, TEXTO, corpo_do_documento_2, le, registros_de, sha256


def usuario(uuid, texto, hora):
    return {"type": "user", "uuid": uuid, "timestamp": hora, "message": {"role": "user", "content": texto}}


class Copiador(CasoDeAceite):
    def test_R04_acrescenta_so_o_novo(self):
        """T04: 2 rodadas com B1; a 2ª acrescenta só M7, e os bytes anteriores não mudam."""
        self.amb.historico_b1()
        self.assertEqual(self.amb.copia().returncode, 0)
        antes = self.amb.d(2).read_bytes()
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        self.assertEqual(self.amb.copia().returncode, 0)
        depois = self.amb.d(2).read_bytes()
        self.assertTrue(depois.startswith(antes), "os bytes já gravados mudaram")
        self.assertEqual(depois[len(antes):].decode("utf-8").strip() + "\n", le(CASOS / "b1" / f"esperado-m7-{IDIOMA}.md").lstrip("\n"))
        # 3ª cópia sem registro novo: nada muda
        self.assertEqual(self.amb.copia().returncode, 0)
        self.assertEqual(self.amb.d(2).read_bytes(), depois)

    def test_R04_espera_o_arquivo_de_historico_parar_de_crescer(self):
        """T04 (C09): um registro gravado logo depois do início da cópia entra na mesma cópia."""
        self.amb.historico_b1()
        novo = registros_de(CASOS / "b1" / "segunda-rodada.jsonl")

        def acrescenta():
            for n in range(12):
                time.sleep(0.05)
                registro = dict(novo[0], uuid=f"crescimento-{n}", message={"content": f"acréscimo {n}"})
                self.amb.acrescenta_historico(SESSAO_B1, [registro])

        t = threading.Thread(target=acrescenta)
        t.start()
        r = self.amb.copia(escala="0.5")  # espera de C09: 0,25 s por leitura, 0,5 s estável, 2,5 s no máximo
        t.join()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("acréscimo 11", le(self.amb.d(2)))

    def test_R05_cabecalhos_comentarios_e_texto_do_caso_b1(self):
        """T05: o corpo do documento 2 é igual à saída literal esperada do caso B1."""
        self.amb.historico_b1()
        self.assertEqual(self.amb.copia().returncode, 0)
        texto = le(self.amb.d(2))
        self.assertTrue(texto.startswith(f"# {TEXTO['titulo_d2']} · {CODIGO_B1}\n\n- {TEXTO['conversa']}: {SESSAO_B1}\n"
                                         f"- {TEXTO['pasta_do_projeto']}: {self.amb.projeto}\n- {TEXTO['fuso']}: +00:00\n\n"), texto[:300])
        self.assertEqual(corpo_do_documento_2(texto).strip() + "\n", le(CASOS / "b1" / f"esperado-{IDIOMA}.md"))

    def test_R05_titulo_no_texto_de_uma_mensagem_nao_e_cabecalho(self):
        """T05: uma resposta do Claude com linhas "## " (achado do aceite em A3, V-U8-02) não quebra a numeração nem a retomada."""
        texto_com_titulos = "Resumo da skill.\n\n## O que a skill produz\n\nOs 7 documentos.\n\n## Como a skill roda\n\nEm segundo plano."
        registros = [
            usuario("u1", "Explique a skill.", "2026-03-14T15:00:00.000Z"),
            {"type": "assistant", "uuid": "a1", "timestamp": "2026-03-14T15:00:05.000Z",
             "message": {"role": "assistant", "content": [{"type": "text", "text": texto_com_titulos}]}},
        ]
        self.amb.grava_historico(SESSAO_B1, registros)
        self.assertEqual(self.amb.copia().returncode, 0)
        antes = self.amb.d(2).read_bytes()
        self.assertIn(texto_com_titulos, antes.decode("utf-8"))
        self.amb.acrescenta_historico(SESSAO_B1, [usuario("u2", "Obrigado.", "2026-03-14T15:01:00.000Z")])
        self.assertEqual(self.amb.copia().returncode, 0)
        depois = le(self.amb.d(2))
        self.assertTrue(depois.encode("utf-8").startswith(antes))
        self.assertIn(f"## M3-{CODIGO_B1} · ", depois)
        self.assertEqual(depois.count(f"## M3-{CODIGO_B1} "), 1)
        self.assertEqual(depois.count("Obrigado."), 1)
        # resposta sem itens (as origens de rodada-b1 citam M4, que esta conversa não tem)
        resposta = json.loads(le(self.amb.resposta("rodada-nada-relevante")))
        resposta["structured_output"]["handoff"] = {k: f"Sem alteração. (M1-{CODIGO_B1} a M3-{CODIGO_B1})"
                                                   for k in resposta["structured_output"]["handoff"]}
        arquivo = self.amb.respostas / "somente-m1-a-m3.json"
        arquivo.write_text(json.dumps(resposta), encoding="utf-8")
        self.assertEqual(self.amb.rodada(respostas=(), extra={"HOPPER_DOCUMENTATION_ANTH_SIMULADO": str(arquivo)}).returncode, 0)
        self.assertIn(f"## M1-{CODIGO_B1} a M3-{CODIGO_B1}", le(self.amb.d(3)))
        self.assertIn(texto_com_titulos, self.amb.chamadas()[0]["stdin"])

    def test_R06_uma_linha_por_ferramenta_sem_resultado(self):
        """T06: linha `Ferramenta: <nome> · <alvo>`, alvo cortado em 120 caracteres, sem o resultado; sem alvo, só o nome."""
        longo = "x" * 200
        registros = [
            usuario("u1", "oi", "2026-03-14T15:00:00.000Z"),
            {"type": "assistant", "uuid": "a1", "timestamp": "2026-03-14T15:00:01.000Z", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": longo}},
                {"type": "tool_use", "id": "t2", "name": "Read", "input": {"file_path": "/tmp/a.txt"}},
                {"type": "tool_use", "id": "t3", "name": "Glob", "input": {"pattern": "**/*.py"}},
                {"type": "tool_use", "id": "t4", "name": "WebFetch", "input": {"url": "https://exemplo.test/p"}},
                {"type": "tool_use", "id": "t5", "name": "Skill", "input": {"skill": "hopper-documentation-anth"}},
                {"type": "tool_use", "id": "t6", "name": "Semalvo", "input": {}},
                {"type": "tool_use", "id": "t7", "name": "Bash", "input": {"command": "echo senha=Pl4nt@d4#2026", "description": "senha=Pl4nt@d4#2026"}}]}},
            {"type": "user", "uuid": "u2", "timestamp": "2026-03-14T15:00:02.000Z", "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "t1", "content": "RESULTADO-QUE-NAO-ENTRA"}]}},
        ]
        self.amb.grava_historico(SESSAO_B1, registros)
        self.assertEqual(self.amb.copia().returncode, 0)
        texto = le(self.amb.d(2))
        f = TEXTO["ferramenta"]
        self.assertIn(f"{f}Bash · " + "x" * 120 + "\n", texto)
        self.assertNotIn("x" * 121, texto)
        self.assertIn(f"{f}Read · /tmp/a.txt\n", texto)
        self.assertIn(f"{f}Glob · **/*.py\n", texto)
        self.assertIn(f"{f}WebFetch · https://exemplo.test/p\n", texto)
        self.assertIn(f"{f}Skill · hopper-documentation-anth\n", texto)
        self.assertIn(f"{f}Semalvo\n", texto)
        self.assertIn(f"{f}Bash · senha={TEXTO['oculto']}\n", texto)
        self.assertNotIn("RESULTADO-QUE-NAO-ENTRA", texto)
        self.assertNotIn("Pl4nt@d4#2026", texto)

    def test_R07_oculta_senhas_tokens_e_chaves(self):
        """T07: todos os casos da classe Masking do clone de leitura e os 3 casos do Anexo B, pela cópia."""
        casos = json.loads(le(CASOS / "b2" / "ocultacao.json"))
        registros, esperados = [], []
        n = 0
        for c in casos["casos"]:
            n += 1
            registros.append(usuario(f"u{n}", c["texto"], f"2026-03-14T15:{n // 60:02d}:{n % 60:02d}.000Z"))
            esperados.append(("caso", c))
        for c in casos["json_aninhado"]:
            n += 1
            registros.append(usuario(f"u{n}", c["texto"], f"2026-03-14T16:00:{n % 60:02d}Z"))
            esperados.append(("aninhado", c))
        for token in casos["tokens_inteiros"]:
            n += 1
            registros.append(usuario(f"u{n}", token, f"2026-03-14T16:{n // 60:02d}:{n % 60:02d}.000Z"))
            esperados.append(("inteiro", token))
        for c in casos["casos_da_spec"]:
            n += 1
            registros.append(usuario(f"u{n}", c["texto"], f"2026-03-14T17:{n // 60:02d}:{n % 60:02d}.000Z"))
            esperados.append(("spec", c))
        self.amb.grava_historico(SESSAO_B1, registros)
        r = self.amb.copia()
        self.assertEqual(r.returncode, 0, r.stderr)
        texto = le(self.amb.d(2))
        mensagens = texto.split("\n## ")[1:]
        self.assertEqual(len(mensagens), len(esperados))
        for m, (tipo, c) in zip(mensagens, esperados):
            corpo = "\n".join(m.split("\n")[2:]).strip()
            if tipo == "caso":
                for oculto in c["ocultos"]:
                    self.assertNotIn(oculto, corpo, c["texto"])
                for mantido in c["mantidos"]:
                    self.assertIn(mantido, corpo, c["texto"])
            elif tipo == "aninhado":
                for oculto in c["ocultos"]:
                    self.assertNotIn(oculto, corpo)
                decodificado = corpo
                for _ in range(c["profundidade"]):
                    decodificado = json.loads(decodificado)
                self.assertEqual(decodificado["note"], "visible")
            elif tipo == "inteiro":
                self.assertEqual(corpo, TEXTO["oculto"], c)
            else:
                self.assertEqual(corpo, c[f"esperado_{IDIOMA}"])

    def test_R07_ocultacao_em_tempo_linear(self):
        """T07: os 8 textos longos da classe Masking, cada cópia em menos de 2 segundos."""
        textos = ("A" * 200000, "token" * 40000, "\\" * 100000 + '"', ("n" * 50 + "=") * 4000,
                  "password" * 25000 + "=v", "a." * 100000, "eyJhIjoxfQ." * 20000,
                  "-----BEGIN A PRIVATE KEY-----\n" * 7000)
        for n, texto in enumerate(textos):
            sessao = f"cccc{n:04d}-0000-4000-8000-000000000001"
            self.amb.grava_historico(sessao, [usuario(f"tempo-{n}", texto, "2026-03-14T15:00:00Z")])
            inicio = time.monotonic()
            r = self.amb.copia(sessao)
            self.assertLess(time.monotonic() - inicio, 2, texto[:20])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(self.amb.d(2, sessao[:8]).exists())

    def test_R04_ancora_ausente_continua_pela_data_e_avisa(self):
        self.amb.grava_historico(SESSAO_B1, [usuario("antes", "Anterior", "2026-03-14T15:00:00Z")])
        self.amb.copia()
        antes = self.amb.d(2).read_bytes()
        self.amb.grava_historico(SESSAO_B1, [usuario("depois", "Posterior", "2026-03-14T15:01:01Z")])
        self.amb.copia()
        self.assertTrue(self.amb.d(2).read_bytes().startswith(antes))
        self.assertIn(f"## M2-{CODIGO_B1}", le(self.amb.d(2)))
        self.assertIn("Posterior", le(self.amb.d(2)))
        self.assertTrue(self.amb.rodadas()[-1]["motivo"])

    def test_R05_ignora_usuario_vazio_depois_dos_lembretes(self):
        self.amb.grava_historico(SESSAO_B1, [usuario("vazio", "<system-reminder>interno</system-reminder>", "2026-03-14T15:00:00Z"),
                                           usuario("real", "Pedido real", "2026-03-14T15:00:01Z")])
        self.amb.copia()
        texto = le(self.amb.d(2))
        self.assertEqual(texto.count("\n## M"), 1)
        self.assertIn("<!-- registros: real real -->", texto)

    def test_R08_inclui_usuario_claude_respostas_planos_mensagens_de_agente_interrupcoes_e_anexos(self):
        """T08: caso B1 e os casos herdados do clone de leitura (respostas a perguntas, plano aprovado, mensagens na fila)."""
        self.amb.historico_b1()
        self.assertEqual(self.amb.copia().returncode, 0)
        texto = le(self.amb.d(2))
        a = TEXTO["autores"]
        self.assertIn(f"· {a['usuario']}\n", texto)
        self.assertIn(f"· {a['claude']}\n", texto)
        self.assertIn(f"· {a['evento']}\n<!-- registros: u6 u6 -->\n\n{TEXTO['interrupcao']}\n", texto)
        self.assertIn(f"· {a['agente']}\n", texto)
        self.assertIn(TEXTO["imagem"], texto)
        self.assertIn("Fica pendente escolher o formato do gráfico.", texto)
        # casos herdados: test_structured_answers_and_approved_plan e test_messages_sent_while_the_assistant_works
        sessao = "aaaa2222-0000-4000-8000-000000000002"
        registros = [
            usuario("u1", "início", "2026-09-28T10:00:00.000Z"),
            {"type": "user", "uuid": "r1", "timestamp": "2026-09-28T10:00:10.000Z",
             "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "q1", "content": "answered"}]},
             "toolUseResult": {"questions": [], "answers": {"Which model?": "Luna"}, "annotations": {"Which model?": {"notes": "only for now"}}}},
            {"type": "user", "uuid": "p1", "timestamp": "2026-09-28T10:00:11.000Z",
             "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "p1", "content": "approved"}]},
             "toolUseResult": {"plan": "# Plan\nStep one.", "filePath": "/p.md"}},
            {"type": "user", "uuid": "p2", "timestamp": "2026-09-28T10:00:12.000Z",
             "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "p2", "is_error": True, "content": "no"}]},
             "toolUseResult": {"plan": "# Rejected plan"}},
            {"type": "attachment", "uuid": "f1", "timestamp": "2026-09-28T10:00:13.000Z",
             "attachment": {"type": "queued_command", "prompt": "Also send it on Tuesdays.", "commandMode": "prompt", "origin": {"kind": "human"}}},
            {"type": "attachment", "uuid": "f2", "timestamp": "2026-09-28T10:00:14.000Z",
             "attachment": {"type": "queued_command", "prompt": [{"type": "text", "text": "And keep it short."}], "commandMode": "prompt"}},
            {"type": "attachment", "uuid": "f3", "timestamp": "2026-09-28T10:00:15.000Z",
             "attachment": {"type": "queued_command", "prompt": "<task-notification>done</task-notification>", "commandMode": "task-notification"}},
            {"type": "user", "uuid": "u9", "timestamp": "2026-09-28T10:00:16.000Z", "message": {"role": "user", "content": [
                {"type": "text", "text": "veja o arquivo"}, {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": "JVBER"}, "title": "relatorio.pdf"}]}},
        ]
        self.amb.grava_historico(sessao, registros)
        r = self.amb.copia(sessao)
        self.assertEqual(r.returncode, 0, r.stderr)
        texto = le(self.amb.d(2, "aaaa2222", "2026-09-28"))
        self.assertIn(f"· {a['resposta']}\n<!-- registros: r1 r1 -->\n\n- Which model? → Luna (only for now)\n", texto)
        self.assertIn(f"· {a['plano']}\n<!-- registros: p1 p1 -->\n\n# Plan\nStep one.\n", texto)
        self.assertNotIn("Rejected plan", texto)
        self.assertIn("Also send it on Tuesdays.", texto)
        self.assertIn("And keep it short.", texto)
        self.assertNotIn("task-notification", texto)
        self.assertIn(f"{TEXTO['arquivo']}relatorio.pdf]", texto)

    def test_R09_exclui_lembretes_gatilhos_notificacoes_resumos_subagentes_raciocinio_e_resultados(self):
        """T09: nada do que a spec exclui aparece no documento 2 do caso B1."""
        self.amb.historico_b1()
        self.assertEqual(self.amb.copia().returncode, 0)
        texto = le(self.amb.d(2))
        for proibido in ("lembrete interno", "system-reminder", "task-notification", "tarefa concluída", "Resumo da compactação",
                         "texto de subagente", "raciocínio interno", "File created", "nota.txt\n\nFerramenta: Bash · Lista os arquivos da pasta\n\nnota.txt"):
            self.assertNotIn(proibido, texto, proibido)
        # saída de gatilho e eco de comando
        sessao = "aaaa3333-0000-4000-8000-000000000003"
        registros = [
            {"type": "user", "uuid": "h1", "timestamp": "2026-03-14T15:00:00.000Z", "message": {"role": "user", "content": [
                {"type": "text", "text": "<user-prompt-submit-hook>saída do gatilho</user-prompt-submit-hook>"}]}},
            {"type": "user", "uuid": "c1", "timestamp": "2026-03-14T15:00:01.000Z", "message": {"role": "user", "content": [
                {"type": "text", "text": "<command-name>/clear</command-name><command-message>clear</command-message>"}]}},
            {"type": "user", "uuid": "c2", "timestamp": "2026-03-14T15:00:02.000Z", "message": {"role": "user", "content": [
                {"type": "text", "text": "<local-command-stdout>eco do comando</local-command-stdout>"}]}},
            usuario("u2", "mensagem real", "2026-03-14T15:00:03.000Z"),
        ]
        self.amb.grava_historico(sessao, registros)
        self.assertEqual(self.amb.copia(sessao).returncode, 0)
        texto = le(self.amb.d(2, "aaaa3333"))
        for proibido in ("saída do gatilho", "command-name", "eco do comando"):
            self.assertNotIn(proibido, texto)
        self.assertIn("mensagem real", texto)
        self.assertEqual(texto.count("\n## M"), 1)

    def test_R10_conta_uma_vez_registros_repetidos(self):
        """T10: caso herdado test_fork_and_rewritten_records: o registro repetido entra 1 vez."""
        sessao = "aaaa4444-0000-4000-8000-000000000004"
        original = usuario("u-1", "Earlier decision: weekly report.", "2026-09-28T09:00:00.000Z")
        de_novo = dict(original, timestamp="2026-09-28T09:00:01.000Z")
        proprio = usuario("u-2", "New request in the fork.", "2026-09-28T10:00:00.000Z")
        caminho = self.amb.grava_historico(sessao, [original, de_novo, proprio])
        # o registro de origem traz o sessionId da conversa de origem, como numa bifurcação
        linhas = caminho.read_text(encoding="utf-8").splitlines()
        linhas[0] = json.dumps(dict(json.loads(linhas[0]), sessionId="origem-0000-4000-8000-000000000000"))
        linhas[1] = json.dumps(dict(json.loads(linhas[1]), sessionId="origem-0000-4000-8000-000000000000"))
        caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        r = self.amb.copia(sessao)
        self.assertEqual(r.returncode, 0, r.stderr)
        texto = le(self.amb.d(2, "aaaa4444", "2026-09-28"))
        self.assertEqual(texto.count("\n## M"), 2)
        self.assertEqual(texto.count("Earlier decision: weekly report."), 1)
        self.assertIn("New request in the fork.", texto)


if __name__ == "__main__":
    unittest.main()
