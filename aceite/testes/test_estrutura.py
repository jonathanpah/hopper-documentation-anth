"""Testes de aceite T01 a T03 (estrutura). Critério congelado da spec, seção 5.1."""
import os
import unittest

from apoio import CODIGO_B1, CasoDeAceite, TEXTO, le


class Estrutura(CasoDeAceite):
    def test_R01_primeira_rodada_cria_a_pasta_de_documentacao(self):
        """T01: em pasta vazia, 1 rodada cria os documentos 1, 4, 5 e 6, a subpasta de conversas e a pasta da conversa."""
        self.amb.historico_b1()
        r = self.amb.rodada()
        self.assertEqual(r.returncode, 0, r.stderr)
        esperado = sorted([
            TEXTO["d1"], TEXTO["d4"], TEXTO["d5"], TEXTO["d6"],
            f"{TEXTO['conversas']}/2026-03-14-{CODIGO_B1}/{TEXTO['d2']}",
            f"{TEXTO['conversas']}/2026-03-14-{CODIGO_B1}/{TEXTO['d3']}",
            f"{TEXTO['conversas']}/2026-03-14-{CODIGO_B1}/{TEXTO['d7']}",
        ])
        encontrado = sorted(str(p.relative_to(self.amb.doc)) for p in self.amb.doc.rglob("*") if p.is_file())
        self.assertEqual(encontrado, esperado)
        self.assertTrue(le(self.amb.d(1)).startswith("# " + TEXTO["titulo_d1"]))
        self.assertTrue(le(self.amb.d(4)).startswith("# " + TEXTO["titulo_d4"]))
        self.assertTrue(le(self.amb.d(5)).startswith("# " + TEXTO["titulo_d5"]))
        self.assertTrue(le(self.amb.d(6)).startswith("# " + TEXTO["titulo_d6"]))

    def test_R02_pasta_da_conversa_com_a_data_da_primeira_mensagem(self):
        """T02: a cópia sozinha cria a pasta da conversa com a data da 1ª mensagem no fuso da máquina (TZ=UTC) e o documento 2."""
        self.amb.historico_b1()
        r = self.amb.copia()
        self.assertEqual(r.returncode, 0, r.stderr)
        pasta = self.amb.pasta_conversa()
        self.assertTrue(pasta.is_dir(), list(self.amb.doc.rglob("*")))
        self.assertTrue(self.amb.d(2).exists())
        self.assertFalse(self.amb.d(3).exists())
        self.assertFalse(self.amb.d(7).exists())
        # perto da meia-noite: a data é a da 1ª mensagem, e não a da rodada
        registros = [{"type": "user", "uuid": "n1", "timestamp": "2026-03-14T23:59:30.000Z",
                      "message": {"role": "user", "content": "mensagem perto da meia-noite"}}]
        self.amb.grava_historico("aaaa1111-0000-4000-8000-000000000001", registros)
        r = self.amb.copia("aaaa1111-0000-4000-8000-000000000001")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.amb.doc / TEXTO["conversas"] / "2026-03-14-aaaa1111").is_dir())

    def test_R03_grava_so_na_pasta_de_documentacao_e_na_pasta_de_dados(self):
        """T03: 1 rodada inteira; nenhum arquivo criado ou alterado fora das 2 pastas permitidas."""
        self.amb.historico_b1()
        (self.amb.projeto / "fonte.txt").write_text("conteúdo do projeto", encoding="utf-8")

        def inventario():
            saida = {}
            for base in (self.amb.raiz,):
                for dirpath, _, arquivos in os.walk(base):
                    for a in arquivos:
                        p = os.path.join(dirpath, a)
                        rel = os.path.relpath(p, base)
                        if rel.startswith(os.path.relpath(self.amb.doc, base)) or rel.startswith(os.path.relpath(self.amb.dados, base)) \
                                or rel.startswith("simulado") or rel.startswith("respostas"):
                            continue
                        saida[rel] = (os.path.getsize(p), os.path.getmtime(p))
            return saida

        antes = inventario()
        r = self.amb.rodada()
        self.assertEqual(r.returncode, 0, r.stderr)
        depois = inventario()
        self.assertEqual(sorted(set(depois) - set(antes)), [])
        self.assertEqual([k for k in antes if antes[k] != depois.get(k)], [])


if __name__ == "__main__":
    unittest.main()
