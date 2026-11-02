"""Critérios do Anexo F para os caminhos de borda do conferidor, sem usar o programa."""
import shutil
import subprocess
import sys

from apoio import CASOS, RAIZ, CasoDeAceite, le


class Conferidor(CasoDeAceite):
    def confere(self, nome="valida", roteiro=False):
        args = [sys.executable, str(RAIZ / "aceite" / "conferir.py"), str(self.pasta), "--idioma", "pt-br"]
        if roteiro:
            args += ["--roteiro", str(RAIZ / "aceite" / "roteiro.json")]
        return subprocess.run(args, capture_output=True, text=True)

    def caso(self, nome="valida"):
        self.pasta = self.amb.raiz / "documentacao"
        shutil.copytree(CASOS / "conferidor" / nome, self.pasta)
        self.d7 = self.pasta / "conversas/2026-03-14-3f9c2a71/7-handoff.md"

    def test_F2_cabecalho_sem_comentario_reprova(self):
        self.caso("invalida-F2-sem-registros")
        r = self.confere()
        self.assertEqual(r.returncode, 1)
        self.assertIn("F2: reprovada", r.stdout)
        self.assertIn("M6 sem o comentário", r.stdout)

    def test_F5_aceita_titulo_extra_e_exige_ordem(self):
        self.caso()
        texto = le(self.d7).replace("## Próximo passo", "## Detalhe adicional\n\nTexto curto.\n\n## Próximo passo")
        self.d7.write_text(texto)
        self.assertEqual(self.confere().returncode, 0)
        self.d7.write_text(texto.replace("## Objetivo", "## Lacunas").replace("## Como retomar", "## Objetivo"))
        self.assertIn("F5: reprovada", self.confere().stdout)

    def test_F7_conta_listas_e_total_dos_documentos(self):
        self.caso()
        d4 = self.pasta / "4-decisoes.md"
        d4.write_text(le(d4) + "\n" + " ".join(["palavra"] * 26) + ".\n")
        self.assertIn("F7: aprovada", self.confere().stdout)
        self.d7.write_text(le(self.d7) + "\n- " + " ".join(["palavra"] * 45) + ".\n")
        self.assertIn("F7: reprovada", self.confere().stdout)

    def test_F9_roteiro_e_conversa_migrada(self):
        self.caso("valida-roteiro")
        r = self.confere(roteiro=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        d4 = self.pasta / "4-decisoes.md"
        d4.write_text(le(d4).replace("substituída por D1-3f9c2a71", "substituída por D99-3f9c2a71"))
        self.assertIn("F4: reprovada", self.confere(roteiro=True).stdout)
