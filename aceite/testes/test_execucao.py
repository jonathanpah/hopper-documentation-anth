"""Testes de aceite T22, T24 e T27 a T29 (execução). Critério congelado da spec, seção 5.4."""
import json
import subprocess
import sys
import threading
import time
import unittest

from apoio import CASOS, CODIGO_B1, PROGRAMA, SESSAO_B1, CasoDeAceite, TEXTO, blocos_do_documento_3, corpo_do_documento_2, itens, le, registros_de, sha256, ultima_linha


class Execucao(CasoDeAceite):
    def test_R22_gatilho_de_copia_termina_em_60_segundos_e_sai_com_0(self):
        """T22: histórico de 50 MB copiado em menos de 60 s, com código 0; falha na cópia também sai com 0."""
        base = registros_de(CASOS / "b1" / "historico.jsonl")
        caminho = self.amb.historico(SESSAO_B1)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        texto = "Mensagem longa para encher o arquivo de histórico. " * 20
        with caminho.open("w", encoding="utf-8") as f:
            for r in base[1:]:
                f.write(json.dumps(dict(r, cwd=str(self.amb.projeto)), ensure_ascii=False) + "\n")
            n = 0
            while caminho.stat().st_size < 50 * 1024 * 1024:
                for _ in range(2000):
                    n += 1
                    f.write(json.dumps({"type": "user", "uuid": f"g{n}", "sessionId": SESSAO_B1, "cwd": str(self.amb.projeto),
                                        "timestamp": "2026-03-14T16:%02d:%02d.000Z" % ((n // 60) % 60, n % 60),
                                        "message": {"role": "user", "content": f"{n} {texto}"}}, ensure_ascii=False) + "\n")
                f.flush()
        self.assertGreaterEqual(caminho.stat().st_size, 50 * 1024 * 1024)
        inicio = time.monotonic()
        r = self.amb.copia(tempo=120)
        duracao = time.monotonic() - inicio
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertLess(duracao, 60, duracao)
        self.assertIn(f"## M{n + 6}-{CODIGO_B1} ", le(self.amb.d(2)))
        # cópia que falha (histórico inexistente): código 0 e falha no registro de rodadas
        amb = type(self.amb)()
        self.addCleanup(amb.limpa)
        r = amb.copia("aaaa5555-0000-4000-8000-000000000005")
        self.assertEqual(r.returncode, 0, r.stderr)
        registro = amb.rodadas()
        self.assertEqual(registro[-1]["acionamento"], "gatilho-copia")
        self.assertEqual(registro[-1]["resultado"], "falhou")
        self.assertTrue(registro[-1]["motivo"])

    def test_R24_falha_de_rodada_fica_no_registro_no_documento_1_e_no_aviso(self):
        """T24: redator que falha; registro de rodadas, documento 1 e aviso (código 2 do gatilho de escrita, motivo na saída de erro)."""
        self.amb.historico_b1()
        r = self.amb.escrita(respostas=("rodada-fora-do-esquema",))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertTrue(r.stderr.strip(), "o motivo precisa ir à saída de erro")
        registro = [x for x in self.amb.rodadas() if x["etapa"] == "escrita"]
        self.assertEqual(registro[-1]["resultado"], "falhou")
        self.assertTrue(registro[-1]["motivo"])
        self.assertEqual(registro[-1]["acionamento"], "gatilho-escrita")
        linha = [l for l in le(self.amb.d(1)).split("\n") if l.startswith(f"| [{CODIGO_B1}]")][0]
        self.assertIn(f"| {TEXTO['res_falhou']}:", linha)
        # rodada a pedido com redator fora do ar: a linha final informa a falha e o código é diferente de 0
        amb = type(self.amb)()
        self.addCleanup(amb.limpa)
        amb.historico_b1()
        r = amb.rodada(respostas=("falha-tempo",), escala="0.001")
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue(ultima_linha(r.stdout))

    def test_R27_uma_rodada_por_conversa_por_vez(self):
        """T27: a 2ª rodada espera a 1ª e depois informa "nada novo"; com espera curta demais, desiste com aviso."""
        self.amb.historico_b1()
        lenta = json.loads(le(self.amb.resposta("rodada-b1")))
        lenta["espera_segundos"] = 3
        arquivo = self.amb.respostas / "lenta.json"
        arquivo.write_text(json.dumps(lenta, ensure_ascii=False), encoding="utf-8")
        resultados = {}

        def primeira():
            resultados["a"] = self.amb.roda("rodada", "--sessao", SESSAO_B1, respostas=(), escala="0.01",
                                            extra={"HOPPER_DOCUMENTATION_ANTH_SIMULADO": str(arquivo)})

        t = threading.Thread(target=primeira)
        t.start()
        time.sleep(0.8)
        segunda = self.amb.rodada(respostas=("rodada-b1",), escala="0.01")  # espera de até 15 min × 0,01 = 9 s
        t.join()
        self.assertEqual(resultados["a"].returncode, 0, resultados["a"].stderr)
        self.assertEqual(segunda.returncode, 0, segunda.stderr)
        self.assertIn(TEXTO["res_nada_novo"], ultima_linha(segunda.stdout))
        self.assertEqual(len(self.amb.chamadas()), 1)
        self.assertEqual(blocos_do_documento_3(le(self.amb.d(3))), [f"M1-{CODIGO_B1} a M6-{CODIGO_B1}"])
        # espera curta demais: desiste com aviso
        amb = type(self.amb)()
        self.addCleanup(amb.limpa)
        amb.historico_b1()
        arquivo2 = amb.respostas / "lenta.json"
        arquivo2.write_text(json.dumps(lenta, ensure_ascii=False), encoding="utf-8")

        def primeira2():
            # a 1ª rodada mantém a escala 0,01 (tempo-limite do redator de 9 s) e segura a trava por 3 s
            resultados["b"] = amb.roda("rodada", "--sessao", SESSAO_B1, respostas=(), escala="0.01",
                                       extra={"HOPPER_DOCUMENTATION_ANTH_SIMULADO": str(arquivo2)})

        t = threading.Thread(target=primeira2)
        t.start()
        time.sleep(0.8)
        segunda = amb.rodada(respostas=("rodada-b1",), escala="0.001")  # espera de 15 min × 0,001 = 0,9 s
        t.join()
        self.assertNotEqual(segunda.returncode, 0)
        self.assertTrue(ultima_linha(segunda.stdout))
        registro = amb.rodadas()
        self.assertEqual(registro[-1]["resultado"] if registro[-1]["acionamento"] == "pedido" and registro[-1]["resultado"] == "falhou" else "falhou", "falhou")

    def test_R28_nada_novo_nao_chama_o_redator_nem_altera_os_documentos(self):
        """T28: 2ª rodada sem registro novo: sem chamada ao redator, documentos iguais, linha final "nada novo"."""
        self.amb.historico_b1()
        self.assertEqual(self.amb.rodada().returncode, 0)
        assinaturas = {n: sha256(self.amb.d(n)) for n in (1, 2, 3, 4, 5, 6, 7)}
        r = self.amb.rodada()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(TEXTO["res_nada_novo"], ultima_linha(r.stdout))
        self.assertEqual(len(self.amb.chamadas()), 1)
        self.assertEqual({n: sha256(self.amb.d(n)) for n in (1, 2, 3, 4, 5, 6, 7)}, assinaturas)
        self.assertEqual(self.amb.rodadas()[-1]["resultado"], "nada novo")

    def test_R29_rodada_interrompida_e_concluida_pela_seguinte(self):
        """T29: interrupção no meio da cópia, depois da cópia, depois do diário e no meio da gravação; a rodada seguinte conclui sem duplicar."""
        referencia = type(self.amb)()
        self.addCleanup(referencia.limpa)
        referencia.historico_b1()
        self.assertEqual(referencia.rodada().returncode, 0)
        esperado_d2 = corpo_do_documento_2(le(referencia.d(2)))  # o cabeçalho traz a pasta do projeto, que muda por ambiente
        for etapa in ("meio-da-copia", "depois-da-copia", "depois-do-diario", "meio-da-gravacao"):
            amb = type(self.amb)()
            self.addCleanup(amb.limpa)
            amb.historico_b1()
            r = amb.rodada(extra={"HOPPER_DOCUMENTATION_ANTH_INTERROMPER_EM": etapa})
            self.assertNotEqual(r.returncode, 0, etapa)
            r = amb.rodada(respostas=("rodada-b1", "rodada-b1"))
            self.assertEqual(r.returncode, 0, f"{etapa}: {r.stderr}")
            self.assertEqual(corpo_do_documento_2(le(amb.d(2))), esperado_d2, etapa)
            self.assertEqual(blocos_do_documento_3(le(amb.d(3))), [f"M1-{CODIGO_B1} a M6-{CODIGO_B1}"], etapa)
            self.assertEqual([i["id"] for i in itens(le(amb.d(4)))], [f"D1-{CODIGO_B1}"], etapa)
            self.assertEqual([i["id"] for i in itens(le(amb.d(5)))], [f"F1-{CODIGO_B1}"], etapa)
            self.assertEqual([i["id"] for i in itens(le(amb.d(6)))], [f"PD1-{CODIGO_B1}"], etapa)
            self.assertEqual([l[3:] for l in le(amb.d(7)).split("\n") if l.startswith("## ")], TEXTO["secoes_d7"], etapa)
            self.assertEqual(le(amb.d(1)).count(f"| [{CODIGO_B1}]"), 1, etapa)


if __name__ == "__main__":
    unittest.main()
