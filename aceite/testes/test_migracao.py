"""Testes de aceite T30, T31 e T42 (migração do formato antigo). Critério congelado da spec, seção 5.5."""
import json
import shutil
import unittest

from apoio import CASOS, CasoDeAceite, TEXTO, itens, le

ANTH = ["index.md", "handoff-20260314-151203-3f9c2a71.md", "handoff-20260314-184207-3f9c2a71.md"]
ANTIGO = ["index.md", "handoff-20260929-041132.md", "handoff-20260929-102703-01a0ead4.md"]


class Migracao(CasoDeAceite):
    def copia_formato_antigo(self, nome):
        destino = self.amb.doc
        destino.mkdir(parents=True, exist_ok=True)
        for arquivo in (CASOS / "b3" / nome).iterdir():
            shutil.copy(arquivo, destino / arquivo.name)

    def test_R30_migra_handoffs_do_anth_e_do_clone_de_leitura(self):
        """T30: itens com a origem igual ao nome do arquivo antigo, documento 7 por conversa antiga e nenhum arquivo antigo sobrando."""
        self.copia_formato_antigo("anth")
        r = self.amb.migrar(respostas=("migracao-b3-anth",))
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        for nome in ANTH:
            self.assertFalse((self.amb.doc / nome).exists(), nome)
        decisoes = itens(le(self.amb.d(4)))
        self.assertEqual([i["id"] for i in decisoes], ["D1-3f9c2a71"])
        self.assertIn("handoff-20260314-151203-3f9c2a71.md", decisoes[0]["campos"][TEXTO["origem"]])
        self.assertEqual(decisoes[0]["campos"][TEXTO["intervalo"]], TEXTO["migracao"])
        self.assertEqual(decisoes[0]["campos"][TEXTO["situacao"]], TEXTO["vigente"])
        self.assertEqual([i["id"] for i in itens(le(self.amb.d(5)))], ["F1-3f9c2a71"])
        pendencias = itens(le(self.amb.d(6)))
        self.assertEqual([i["id"] for i in pendencias], ["PD1-3f9c2a71"])
        self.assertEqual(pendencias[0]["campos"][TEXTO["situacao"]], TEXTO["aberta"])
        d7 = self.amb.d(7, "3f9c2a71", "2026-03-14")
        self.assertTrue(d7.exists(), list(self.amb.doc.rglob("*")))
        texto = le(d7)
        self.assertIn(f"- {TEXTO['conversa']}: 3f9c2a71-5b8e-4d0a-9c61-2e7f4b1a8d05\n", texto)
        self.assertIn(f"- {TEXTO['ultima_coberta']}: {TEXTO['sem_integral']}\n", texto)
        self.assertEqual([l[3:] for l in texto.split("\n") if l.startswith("## ")], TEXTO["secoes_d7"])
        self.assertIn("PD1-3f9c2a71", texto)
        self.assertFalse(self.amb.d(2, "3f9c2a71", "2026-03-14").exists())
        indice = le(self.amb.d(1))
        linha = [l for l in indice.split("\n") if l.startswith("| [3f9c2a71]")][0]
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        self.assertEqual(celulas[1], "2026-03-14")
        self.assertEqual(celulas[2], TEXTO["sem_integral"])
        self.assertEqual(celulas[4], TEXTO["res_concluida"])
        self.assertEqual([x["etapa"] for x in self.amb.rodadas() if x["acionamento"] == "migrar"][-2:], ["migracao", "exclusao"])
        # clone de leitura: 1 conversa do Claude sem identificador e 1 do Codex
        amb = type(self.amb)()
        self.addCleanup(amb.limpa)
        amb.doc.mkdir(parents=True)
        for arquivo in (CASOS / "b3" / "antigo").iterdir():
            shutil.copy(arquivo, amb.doc / arquivo.name)
        r = amb.migrar(respostas=("migracao-b3-antigo",))
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        for nome in ANTIGO:
            self.assertFalse((amb.doc / nome).exists(), nome)
        self.assertEqual([i["id"] for i in itens(le(amb.d(4)))], ["D1-antigo-a2f1", "D1-01a0ead4"])
        self.assertEqual([i["id"] for i in itens(le(amb.d(5)))], ["F1-antigo-a2f1", "F1-01a0ead4"])
        self.assertEqual([i["id"] for i in itens(le(amb.d(6)))], ["PD1-antigo-a2f1", "PD1-01a0ead4"])
        self.assertTrue(amb.d(7, "antigo-a2f1", "2026-09-29").exists(), list(amb.doc.rglob("*")))
        self.assertTrue(amb.d(7, "01a0ead4", "2026-09-29").exists())
        self.assertIn("handoff-20260929-041132.md", le(amb.d(4)))
        entrada = amb.chamadas()[0]["stdin"]
        self.assertIn("<arquivos_antigos>", entrada)
        self.assertIn("antigo-a2f1", entrada)
        self.assertNotIn("<trecho_novo>", entrada)

    def test_R31_so_apaga_depois_da_verificacao_interna(self):
        """T31: com 1 condição reprovada (arquivo antigo sem destino), nenhum arquivo é apagado."""
        self.copia_formato_antigo("anth")
        r = self.amb.migrar(respostas=("migracao-b3-anth-incompleta",))
        self.assertNotEqual(r.returncode, 0)
        for nome in ANTH:
            self.assertTrue((self.amb.doc / nome).exists(), nome)
        registro = self.amb.rodadas()
        self.assertEqual([x["resultado"] for x in registro if x["etapa"] == "migracao"][-1], "falhou")
        self.assertNotIn("exclusao", [x["etapa"] for x in registro])
        # interrupção depois da migração e antes da exclusão: a rodada seguinte refaz a verificação e apaga
        amb = type(self.amb)()
        self.addCleanup(amb.limpa)
        amb.doc.mkdir(parents=True)
        for arquivo in (CASOS / "b3" / "anth").iterdir():
            shutil.copy(arquivo, amb.doc / arquivo.name)
        r = amb.migrar(respostas=("migracao-b3-anth",), extra={"HOPPER_DOCUMENTATION_ANTH_INTERROMPER_EM": "antes-da-exclusao"})
        self.assertNotEqual(r.returncode, 0)
        for nome in ANTH:
            self.assertTrue((amb.doc / nome).exists(), nome)
        r = amb.migrar(respostas=("migracao-b3-anth",))
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        for nome in ANTH:
            self.assertFalse((amb.doc / nome).exists(), nome)
        self.assertEqual([i["id"] for i in itens(le(amb.d(4)))], ["D1-3f9c2a71"])

    def test_R42_migracao_automatica_desligada(self):
        """T42: com `migracao_automatica` falsa, a rodada não migra nem apaga os arquivos antigos; com verdadeira (padrão), migra."""
        self.copia_formato_antigo("anth")
        self.amb.historico_b1()
        self.amb.dados.mkdir(parents=True, exist_ok=True)
        (self.amb.dados / "config.json").write_text(json.dumps({"migracao_automatica": False}), encoding="utf-8")
        r = self.amb.rodada(respostas=("rodada-b1",))
        self.assertEqual(r.returncode, 0, r.stderr)
        for nome in ANTH:
            self.assertTrue((self.amb.doc / nome).exists(), nome)
        self.assertEqual(len(self.amb.chamadas()), 1)
        self.assertNotIn("handoff-20260314-184207-3f9c2a71.md", le(self.amb.d(4)))
        amb = type(self.amb)()
        self.addCleanup(amb.limpa)
        amb.doc.mkdir(parents=True)
        for arquivo in (CASOS / "b3" / "anth").iterdir():
            shutil.copy(arquivo, amb.doc / arquivo.name)
        amb.historico_b1()
        r = amb.rodada(respostas=("migracao-b3-anth", "rodada-b1"))
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        for nome in ANTH:
            self.assertFalse((amb.doc / nome).exists(), nome)
        self.assertEqual(len(amb.chamadas()), 2)
        self.assertIn("handoff-20260314-184207-3f9c2a71.md", le(amb.d(4)))


if __name__ == "__main__":
    unittest.main()
