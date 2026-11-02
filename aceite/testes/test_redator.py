"""Testes de aceite T11 a T14 e T16 a T18 (redator e documentos 1, 3 a 7). Critério congelado da spec, seção 5.3."""
import json
import re
import unittest

from apoio import CASOS, CODIGO_B1, SESSAO_B1, SKILL, CasoDeAceite, TEXTO, blocos_do_documento_3, itens, le, registros_de, sha256

M = lambda n: f"M{n}-{CODIGO_B1}"  # noqa: E731


class Redator(CasoDeAceite):
    def setUp(self):
        super().setUp()
        self.amb.historico_b1()

    def test_R11_envia_so_o_trecho_novo_e_os_documentos_atuais(self):
        """T11: a entrada do redator segue o Anexo D e traz só o trecho novo; na 2ª rodada, o handoff anterior."""
        self.assertEqual(self.amb.rodada().returncode, 0)
        chamadas = self.amb.chamadas()
        self.assertEqual(len(chamadas), 1)
        entrada = chamadas[0]["stdin"]
        self.assertTrue(entrada.startswith(f"Conversa: {SESSAO_B1}. Código: {CODIGO_B1}. Intervalo: {M(1)} a {M(6)}."), entrada[:200])
        for tag in ("regras_de_escrita", "modelos", "decisoes", "funcoes", "pendencias", "handoff_anterior", "trecho_novo"):
            self.assertIn(f"<{tag}>", entrada)
            self.assertIn(f"</{tag}>", entrada)
        regras = re.search(r"<regras_de_escrita>(.*?)</regras_de_escrita>", entrada, re.S).group(1)
        self.assertEqual(regras.strip(), le(SKILL / TEXTO["regras"]).strip())
        modelos = re.search(r"<modelos>(.*?)</modelos>", entrada, re.S).group(1)
        self.assertEqual(modelos.strip(), le(SKILL / TEXTO["modelos"]).strip())
        trecho = re.search(r"<trecho_novo>(.*?)</trecho_novo>", entrada, re.S).group(1)
        self.assertIn(f"## {M(1)} ", trecho)
        self.assertIn(f"## {M(6)} ", trecho)
        self.assertNotIn(f"## {M(7)} ", trecho)
        self.assertIn("Tarefa:", entrada.split("</trecho_novo>")[1])
        handoff_1 = le(self.amb.d(7))
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        self.assertEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-m7")).returncode, 0)
        entrada2 = self.amb.chamadas()[1]["stdin"]
        self.assertIn(f"Intervalo: {M(7)} a {M(7)}.", entrada2)
        trecho2 = re.search(r"<trecho_novo>(.*?)</trecho_novo>", entrada2, re.S).group(1)
        self.assertIn(f"## {M(7)} ", trecho2)
        self.assertNotIn(f"## {M(6)} ", trecho2)
        anterior = re.search(r"<handoff_anterior>(.*?)</handoff_anterior>", entrada2, re.S).group(1)
        self.assertEqual(anterior.strip(), handoff_1.strip())
        decisoes = re.search(r"<decisoes>(.*?)</decisoes>", entrada2, re.S).group(1)
        self.assertIn(f"### D1-{CODIGO_B1}", decisoes)

    def test_R12_chama_o_redator_com_as_opcoes_de_C03_e_descarta_resposta_invalida(self):
        """T12: comando e ambiente montados pela decisão C03; respostas fora do esquema ou de outro modelo são descartadas."""
        extra = {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": "100000", "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70",
                 "CLAUDE_CODE_EFFORT_LEVEL": "low", "ANTHROPIC_MODEL": "claude-opus-5-5"}
        self.assertEqual(self.amb.rodada(extra=extra).returncode, 0)
        chamada = self.amb.chamadas()[0]
        argv = chamada["argv"]
        self.assertIn("-p", argv)
        texto = " ".join(argv)
        for opcao in ("--model claude-sonnet-5-5", "--effort high", "--strict-mcp-config", "--disable-slash-commands",
                      "--no-session-persistence", "--output-format json"):
            self.assertIn(opcao, texto, texto)
        self.assertEqual(argv[argv.index("--tools") + 1], "")
        esquema = json.loads(argv[argv.index("--json-schema") + 1])
        self.assertEqual(esquema["required"], ["nada_relevante", "resumo", "conversa_simplificada", "itens_novos", "mudancas", "handoff"])
        self.assertEqual(esquema["properties"]["handoff"]["required"],
                         ["objetivo", "pautas_e_estado", "proximo_passo", "decisoes_e_autorizacoes", "restricoes", "descobertas", "pendencias", "lacunas", "como_retomar"])
        self.assertTrue(argv[argv.index("--system-prompt") + 1].strip())
        env = chamada["env"]
        for chave in ("CLAUDE_CODE_SAFE_MODE", "CLAUDE_CODE_DISABLE_CLAUDE_MDS", "CLAUDE_CODE_DISABLE_AUTO_MEMORY", "HOPPER_DOCUMENTATION_ANTH_RUN"):
            self.assertEqual(env.get(chave), "1", chave)
        for chave in ("CLAUDE_CODE_AUTO_COMPACT_WINDOW", "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE", "CLAUDE_CODE_EFFORT_LEVEL", "ANTHROPIC_MODEL"):
            self.assertNotIn(chave, env, chave)
        self.assertEqual(chamada["cwd"], str(self.amb.dados))
        # resposta fora do esquema: nada gravado nos documentos 3 a 7, falha registrada
        for resposta in ("rodada-fora-do-esquema", "rodada-modelo-errado"):
            amb = type(self.amb)()
            self.addCleanup(amb.limpa)
            amb.historico_b1()
            r = amb.rodada(respostas=(resposta,))
            self.assertNotEqual(r.returncode, 0, resposta)
            self.assertFalse(amb.d(3).exists(), resposta)
            self.assertFalse(amb.d(7).exists(), resposta)
            self.assertEqual(len(itens(le(amb.d(4)))), 0, resposta)
            self.assertEqual([x["resultado"] for x in amb.rodadas() if x["etapa"] == "escrita"][-1], "falhou", resposta)

    def test_R13_acrescenta_um_bloco_por_intervalo(self):
        """T13: 1 bloco por intervalo no documento 3, inclusive o bloco sem conteúdo novo."""
        self.assertEqual(self.amb.rodada().returncode, 0)
        texto = le(self.amb.d(3))
        self.assertTrue(texto.startswith(f"# {TEXTO['titulo_d3']} · {CODIGO_B1}\n"))
        self.assertEqual(blocos_do_documento_3(texto), [f"{M(1)} a {M(6)}"])
        bloco = texto.split(f"## {M(1)} a {M(6)}\n")[1]
        self.assertTrue(bloco.lstrip("\n").startswith(TEXTO["assunto"]), bloco[:80])
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        self.assertEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-nada-relevante")).returncode, 0)
        texto = le(self.amb.d(3))
        self.assertEqual(blocos_do_documento_3(texto), [f"{M(1)} a {M(6)}", f"{M(7)} a {M(7)}"])
        self.assertIn(f"## {M(7)} a {M(7)}\n\n{TEXTO['assunto']}", texto)
        self.assertIn(f"{TEXTO['sem_conteudo']} ({M(7)} a {M(7)})", texto)

    def test_R14_numera_com_o_proximo_numero_livre(self):
        """T14: D1, F1 e PD1 na 1ª rodada; D2 na 2ª; depois de apagar D1 à mão, o próximo é D3."""
        self.assertEqual(self.amb.rodada().returncode, 0)
        self.assertEqual([i["id"] for i in itens(le(self.amb.d(4)))], [f"D1-{CODIGO_B1}"])
        self.assertEqual([i["id"] for i in itens(le(self.amb.d(5)))], [f"F1-{CODIGO_B1}"])
        self.assertEqual([i["id"] for i in itens(le(self.amb.d(6)))], [f"PD1-{CODIGO_B1}"])
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        self.assertEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-m7")).returncode, 0)
        self.assertEqual([i["id"] for i in itens(le(self.amb.d(4)))], [f"D1-{CODIGO_B1}", f"D2-{CODIGO_B1}"])
        texto = le(self.amb.d(4))
        inicio = texto.index(f"### D1-{CODIGO_B1}")
        fim = texto.index(f"### D2-{CODIGO_B1}")
        self.amb.d(4).write_text(texto[:inicio] + texto[fim:], encoding="utf-8")
        self.amb.acrescenta_historico(SESSAO_B1, [{"type": "user", "uuid": "u10", "timestamp": "2026-03-14T15:20:00.000Z",
                                                   "message": {"role": "user", "content": "Decidimos usar a cor azul no painel."}}])
        self.assertEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-m7", "rodada-m7")).returncode, 0)
        self.assertEqual([i["id"] for i in itens(le(self.amb.d(4)))], [f"D2-{CODIGO_B1}", f"D3-{CODIGO_B1}"])

    def test_R16_aplica_mudancas_de_situacao_e_registra_as_inexistentes(self):
        """T16: mudança aplicada a item existente, inclusive de outra conversa; identificador inexistente só vai ao registro."""
        outro = (f"\n### PD1-aaaa9999\nRevisar o relatório mensal.\n\n- {TEXTO['recomendacao']}: revisar.\n- {TEXTO['depende_de']}: nada.\n"
                 f"- {TEXTO['origem']}: M2-aaaa9999\n- {TEXTO['situacao']}: {TEXTO['aberta']}\n- {TEXTO['intervalo']}: M1-aaaa9999 a M3-aaaa9999\n")
        self.assertEqual(self.amb.rodada().returncode, 0)
        with self.amb.d(6).open("a", encoding="utf-8") as f:
            f.write(outro)
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        r = self.amb.rodada(respostas=("rodada-b1", "rodada-mudanca-inexistente"))
        self.assertEqual(r.returncode, 0, r.stderr)
        pendencias = {i["id"]: i for i in itens(le(self.amb.d(6)))}
        self.assertTrue(pendencias[f"PD1-{CODIGO_B1}"]["campos"][TEXTO["situacao"]].startswith(f"{TEXTO['encerrada']} {M(7)}"))
        self.assertIn(M(7), pendencias[f"PD1-{CODIGO_B1}"]["campos"][TEXTO["origem"]])
        self.assertIn("M4-" + CODIGO_B1, pendencias[f"PD1-{CODIGO_B1}"]["campos"][TEXTO["origem"]])
        self.assertEqual(pendencias["PD1-aaaa9999"]["campos"][TEXTO["situacao"]], TEXTO["aberta"])
        self.assertNotIn("PD99", le(self.amb.d(6)))
        registro = json.dumps(self.amb.rodadas(), ensure_ascii=False)
        self.assertIn(f"PD99-{CODIGO_B1}", registro)
        # mudança em item de outra conversa da mesma pasta
        self.amb.acrescenta_historico(SESSAO_B1, [{"type": "user", "uuid": "u11", "timestamp": "2026-03-14T15:30:00.000Z",
                                                   "message": {"role": "user", "content": "O relatório mensal foi revisado."}}])
        resposta = json.loads(le(self.amb.resposta("rodada-mudanca-inexistente")))
        resposta["structured_output"]["mudancas"] = [{"id": "PD1-aaaa9999", "situacao": f"{TEXTO['encerrada']} M8-{CODIGO_B1} (revisado)", "origem": [f"M8-{CODIGO_B1}"]}]
        resposta["structured_output"]["conversa_simplificada"] = f"{TEXTO['assunto']}relatório mensal.**\n\nO relatório foi revisado. (M8-{CODIGO_B1})"
        outra = self.amb.respostas / "outra-conversa.json"
        outra.write_text(json.dumps(resposta, ensure_ascii=False), encoding="utf-8")
        r = self.amb.roda("rodada", "--sessao", SESSAO_B1, respostas=(), extra={"HOPPER_DOCUMENTATION_ANTH_SIMULADO": str(outra)})
        self.assertEqual(r.returncode, 0, r.stderr)
        pendencias = {i["id"]: i for i in itens(le(self.amb.d(6)))}
        self.assertTrue(pendencias["PD1-aaaa9999"]["campos"][TEXTO["situacao"]].startswith(f"{TEXTO['encerrada']} M8-{CODIGO_B1}"))

    def test_R17_reescreve_o_documento_7_inteiro(self):
        """T17: 9 seções e cabeçalho; reescrito a cada rodada com trecho novo; inalterado com nada_relevante."""
        self.assertEqual(self.amb.rodada().returncode, 0)
        texto = le(self.amb.d(7))
        self.assertTrue(texto.startswith(f"# {TEXTO['titulo_d7']} · {CODIGO_B1}\n\n- {TEXTO['conversa']}: {SESSAO_B1}\n- {TEXTO['pasta_do_projeto']}: {self.amb.projeto}\n- {TEXTO['ultima_coberta']}: {M(6)}\n- {TEXTO['data_da_rodada']}: "), texto[:400])
        self.assertIn(f"- {TEXTO['redator']}: claude-sonnet-5-5", texto)
        self.assertEqual([l[3:] for l in texto.split("\n") if l.startswith("## ")], TEXTO["secoes_d7"])
        self.assertIn(f"PD1-{CODIGO_B1}", texto)
        self.assertNotIn("N3", texto)
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        self.assertEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-m7")).returncode, 0)
        texto2 = le(self.amb.d(7))
        self.assertIn(f"- {TEXTO['ultima_coberta']}: {M(7)}\n", texto2)
        self.assertIn(f"D2-{CODIGO_B1}", texto2)
        self.assertNotIn("Criar o arquivo nota.txt e definir o gráfico.", texto2)
        assinatura = sha256(self.amb.d(7))
        self.amb.acrescenta_historico(SESSAO_B1, [{"type": "user", "uuid": "u12", "timestamp": "2026-03-14T15:40:00.000Z",
                                                   "message": {"role": "user", "content": "ok"}}])
        self.assertEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-m7", "rodada-nada-relevante")).returncode, 0)
        self.assertEqual(sha256(self.amb.d(7)), assinatura)

    def test_R18_reescreve_o_documento_1(self):
        """T18: ordem de leitura, links relativos e tabela das conversas; depois de falha, o resultado mostra a falha."""
        self.assertEqual(self.amb.rodada().returncode, 0)
        texto = le(self.amb.d(1))
        self.assertTrue(texto.startswith(f"# {TEXTO['titulo_d1']}\n\n{TEXTO['pasta_do_projeto']}: {self.amb.projeto}\n"))
        self.assertIn(f"## {TEXTO['ordem']}\n", texto)
        self.assertIn(f"## {TEXTO['secao_conversas']}\n", texto)
        for n in (4, 5, 6):
            self.assertIn(f"[{TEXTO[f'd{n}']}]({TEXTO[f'd{n}']})", texto)
        self.assertIn("| " + " | ".join(TEXTO["colunas"]) + " |", texto)
        linha = [l for l in texto.split("\n") if l.startswith(f"| [{CODIGO_B1}]")][0]
        self.assertIn(f"({TEXTO['conversas']}/2026-03-14-{CODIGO_B1}/)", linha)
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        self.assertEqual(celulas[1], "2026-03-14")
        self.assertEqual(celulas[2], M(6))
        self.assertEqual(celulas[4], TEXTO["res_concluida"])
        self.assertEqual(celulas[5], "Arquivo nota.txt criado e formato do gráfico pendente")
        self.amb.acrescenta_historico(SESSAO_B1, registros_de(CASOS / "b1" / "segunda-rodada.jsonl"))
        self.assertNotEqual(self.amb.rodada(respostas=("rodada-b1", "rodada-fora-do-esquema")).returncode, 0)
        linha = [l for l in le(self.amb.d(1)).split("\n") if l.startswith(f"| [{CODIGO_B1}]")][0]
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        self.assertTrue(celulas[4].startswith(TEXTO["res_falhou"] + ":"), celulas)
        self.assertEqual(celulas[2], M(7))


if __name__ == "__main__":
    unittest.main()
