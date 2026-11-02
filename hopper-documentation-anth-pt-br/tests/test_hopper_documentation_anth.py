"""Testes do executor (unitários) do programa da versão 2. Os testes de aceite ficam em aceite/testes/."""
import importlib.util
import json
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("programa", RAIZ / "scripts" / "hopper_documentation_anth.py")
programa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(programa)
T = programa.T
CASOS = RAIZ.parent / "aceite" / "casos"


class Ocultacao(unittest.TestCase):
    def test_casos_da_spec(self):
        self.assertEqual(programa.ocultar("a senha do servidor é Pl4nt@d4#2026 hoje"), f"a senha do servidor é {T['oculto']} hoje")
        self.assertEqual(programa.ocultar("Quero seguir o sitema, claro ou escuro."), "Quero seguir o sitema, claro ou escuro.")
        texto = "Troque a senha e apague o rascunho; o token e a chave ficam no cofre."
        self.assertEqual(programa.ocultar(texto), texto)

    def test_casos_herdados(self):
        if not (CASOS / "b2" / "ocultacao.json").exists():
            self.skipTest("casos de aceite ausentes")
        casos = json.loads((CASOS / "b2" / "ocultacao.json").read_text(encoding="utf-8"))
        for caso in casos["casos"]:
            resultado = programa.ocultar(caso["texto"])
            for oculto in caso["ocultos"]:
                self.assertNotIn(oculto, resultado, caso["texto"])
            for mantido in caso["mantidos"]:
                self.assertIn(mantido, resultado, caso["texto"])


class Mensagens(unittest.TestCase):
    def test_caso_b1(self):
        if not (CASOS / "b1" / "historico.jsonl").exists():
            self.skipTest("casos de aceite ausentes")
        registros = programa.ler_registros(CASOS / "b1" / "historico.jsonl")
        mensagens = programa.extrair_mensagens(registros)
        self.assertEqual([m["autor"] for m in mensagens],
                         [T["usuario"], T["claude"], T["usuario"], T["usuario"], T["evento"], T["agente"]])
        self.assertEqual(mensagens[1]["primeiro"], "a1")
        self.assertEqual(mensagens[1]["ultimo"], "a4")
        self.assertIn(T["oculto"], mensagens[2]["texto"])

    def test_alvo_da_ferramenta(self):
        self.assertEqual(programa.alvo_da_ferramenta({"command": "x" * 200}), "x" * 120)
        self.assertEqual(programa.alvo_da_ferramenta({"description": "d", "file_path": "f"}), "d")
        self.assertEqual(programa.alvo_da_ferramenta({}), "")


class Situacoes(unittest.TestCase):
    def test_permitidas(self):
        self.assertTrue(programa.situacao_permitida("D", T["situacoes"]["D"][0]))
        self.assertTrue(programa.situacao_permitida("PD", T["situacoes"]["PD"][1] + "M7-abc (motivo)"))
        self.assertFalse(programa.situacao_permitida("PD", "pendente"))
        self.assertFalse(programa.situacao_permitida("D", T["situacoes"]["D"][1].strip()))


if __name__ == "__main__":
    unittest.main()
