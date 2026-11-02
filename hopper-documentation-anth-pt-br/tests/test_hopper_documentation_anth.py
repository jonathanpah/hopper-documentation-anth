"""Testes do executor (unitários) do programa da versão 2. Os testes de aceite ficam em aceite/testes/."""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

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


class Relogio:
    def __init__(self):
        self.segundos = 0

    def agora(self):
        return self.segundos

    def dormir(self, segundos):
        self.segundos += segundos


class RegressoesDaTarefa01(unittest.TestCase):
    def setUp(self):
        temporario = tempfile.TemporaryDirectory()
        self.addCleanup(temporario.cleanup)
        self.raiz = Path(temporario.name).resolve()
        self.projeto = self.raiz / "projeto-original"
        self.projeto.mkdir()
        self.config = self.raiz / "config"
        self.sessao = "3f9c2a71-1234-5678-9abc-123456789abc"
        self.historico = self.raiz / "historico.jsonl"
        ambiente = patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(self.config),
                                          "HOPPER_DOCUMENTATION_ANTH_ESCALA_DE_TEMPO": "0.001",
                                          "HOPPER_DOCUMENTATION_ANTH_INTERROMPER_EM": ""})
        ambiente.start()
        self.addCleanup(ambiente.stop)
        (programa.pasta_de_dados() / "config.json").write_text(
            '{"migracao_automatica": false}', encoding="utf-8")
        self.evento = {"session_id": self.sessao, "transcript_path": str(self.historico),
                       "cwd": str(self.projeto), "trigger": "auto"}

    def gravar_historico(self, mensagens):
        registros = [{"type": "summary", "summary": "sem cwd"},
                     {"type": "summary", "cwd": str(self.projeto), "sessionId": self.sessao}]
        for n, mensagem in enumerate(mensagens, 1):
            registros.append({"uuid": f"registro-{n}", "timestamp": "2026-11-02T10:00:00Z",
                              "sessionId": self.sessao, "cwd": str(self.projeto), **mensagem})
        self.historico.write_text("".join(json.dumps(r) + "\n" for r in registros), encoding="utf-8")

    def test_escrita_usa_primeiro_cwd_do_historico_no_processo_separado(self):
        self.gravar_historico([])
        outra_pasta = self.raiz / "pasta-atual"
        outra_pasta.mkdir()
        with self.historico.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"type": "summary", "sessionId": self.sessao, "cwd": str(outra_pasta)}) + "\n")
        evento = {**self.evento, "cwd": str(outra_pasta)}
        resultado = subprocess.run([sys.executable, str(RAIZ / "scripts" / "hopper_documentation_anth.py"), "escrita"],
                                   input=json.dumps(evento), text=True, capture_output=True, timeout=10)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        registros = programa.registros_de_rodadas()
        self.assertEqual([r["etapa"] for r in registros], ["copia", "escrita"])
        self.assertTrue(all(r["pasta_do_projeto"] == str(self.projeto) for r in registros), registros)
        self.assertFalse(list((programa.pasta_de_dados() / "marcadores").glob("*.json")))

    def test_gatilho_registra_trigger_separado_e_intervalos_copiados(self):
        mensagens = [{"type": "user", "message": {"content": "Pedido inicial"}},
                     {"type": "assistant", "message": {"content": "Resposta inicial"}}]
        for novas, esperado in [(mensagens, "M1-3f9c2a71 a M2-3f9c2a71"),
                                (mensagens + [{"type": "user", "message": {"content": "Outro pedido"}}],
                                 "M3-3f9c2a71 a M3-3f9c2a71"),
                                (mensagens + [{"type": "user", "message": {"content": "Outro pedido"}}], "")]:
            with self.subTest(intervalo=esperado):
                self.gravar_historico(novas)
                with patch.object(sys, "stdin", io.StringIO(json.dumps(self.evento))):
                    self.assertEqual(programa.comando_copia(), 0)
                inicio, copia = programa.registros_de_rodadas()[-2:]
                self.assertEqual(inicio["motivo"], "")
                self.assertEqual(inicio["trigger"], "auto")
                self.assertEqual(copia["intervalo"], esperado)

    def test_rodada_registra_intervalos_copiados(self):
        mensagens = [{"type": "user", "message": {"content": "Pedido inicial"}},
                     {"type": "assistant", "message": {"content": "Resposta inicial"}}]
        for novas, esperado in [(mensagens, "M1-3f9c2a71 a M2-3f9c2a71"),
                                (mensagens + [{"type": "user", "message": {"content": "Outro pedido"}}],
                                 "M3-3f9c2a71 a M3-3f9c2a71"),
                                (mensagens + [{"type": "user", "message": {"content": "Outro pedido"}}], "")]:
            with self.subTest(intervalo=esperado), patch.object(programa, "escrever", return_value="fim"):
                self.gravar_historico(novas)
                codigo, _ = programa.rodada(self.sessao, caminho_historico=self.historico)
                self.assertEqual(codigo, 0)
                self.assertEqual(programa.registros_de_rodadas()[-1]["intervalo"], esperado)

    def test_gatilho_copia_soma_esperas_abaixo_de_60_segundos(self):
        self.gravar_historico([{"type": "user", "message": {"content": "Pedido"}}])
        relogio = Relogio()
        stat_original = Path.stat
        tamanhos = iter(range(1000))

        def stat(caminho, *args, **kwargs):
            resultado = stat_original(caminho, *args, **kwargs)
            if caminho == self.historico:
                return os.stat_result((resultado.st_mode, resultado.st_ino, resultado.st_dev, resultado.st_nlink,
                                       resultado.st_uid, resultado.st_gid, next(tamanhos), resultado.st_atime,
                                       resultado.st_mtime, resultado.st_ctime))
            return resultado

        def flock(arquivo, operacao):
            if operacao == programa.fcntl.LOCK_UN:
                return
            nome = Path(arquivo.name).name
            if nome.startswith("pasta-") or nome.startswith("copia-") and relogio.segundos < 20:
                raise BlockingIOError("trava ocupada")

        with patch.dict(os.environ, {"HOPPER_DOCUMENTATION_ANTH_ESCALA_DE_TEMPO": "1"}), \
                patch.object(programa.time, "monotonic", relogio.agora), \
                patch.object(programa.time, "sleep", relogio.dormir), \
                patch.object(programa.fcntl, "flock", flock), patch.object(Path, "stat", stat), \
                patch.object(sys, "stdin", io.StringIO(json.dumps(self.evento))):
            self.assertEqual(programa.comando_copia(), 0)
        self.assertEqual(relogio.segundos, 50)
        self.assertLess(relogio.segundos, 60)
        self.assertEqual(programa.registros_de_rodadas()[-1]["resultado"], "falhou")

    def test_trava_informa_espera_real_em_ambos_os_idiomas(self):
        for idioma, textos in programa.TEXTOS.items():
            for duracao in (20, 25, 60, 900):
                with self.subTest(idioma=idioma, segundos=duracao):
                    relogio = Relogio()
                    with patch.dict(os.environ, {"HOPPER_DOCUMENTATION_ANTH_ESCALA_DE_TEMPO": "1"}), \
                            patch.object(programa, "T", textos), \
                            patch.object(programa.time, "monotonic", relogio.agora), \
                            patch.object(programa.time, "sleep", relogio.dormir), \
                            patch.object(programa.fcntl, "flock", side_effect=BlockingIOError("ocupada")):
                        with self.assertRaises(programa.Falha) as falha:
                            with programa.Trava("ocupada", duracao):
                                self.fail("a trava ocupada foi adquirida")
                    esperado = (f"outra rodada da conversa ou da pasta em andamento; a espera de {duracao} segundos acabou"
                                if idioma == "pt-br" else
                                f"another run of the conversation or folder is in progress; the {duracao}-second wait expired")
                    self.assertEqual(str(falha.exception), esperado)
                    self.assertEqual(relogio.segundos, duracao)

    def test_main_registra_excecao_inesperada_e_marcador_de_falha(self):
        for erro in (OSError("leitura interrompida"), RuntimeError("erro inesperado"), KeyError("campo")):
            with self.subTest(erro=type(erro).__name__):
                marcador = self.raiz / "marcador.json"
                saida, erros = io.StringIO(), io.StringIO()
                with patch.object(programa, "rodada", side_effect=erro), redirect_stdout(saida), redirect_stderr(erros):
                    codigo = programa.main(["rodada", "--sessao", self.sessao, "--acionamento", "gatilho-escrita",
                                            "--historico", str(self.historico), "--marcador", str(marcador)])
                self.assertEqual(codigo, 1)
                linha = T["linha_falhou"].format(motivo=repr(erro))
                self.assertEqual(json.loads(marcador.read_text(encoding="utf-8")), {"codigo": 1, "linha": linha})
                self.assertEqual(saida.getvalue(), linha + "\n")
                self.assertEqual(erros.getvalue(), linha + "\n")
                registro = programa.registros_de_rodadas()[-1]
                self.assertEqual((registro["conversa"], registro["acionamento"], registro["etapa"], registro["resultado"]),
                                 (self.sessao, "gatilho-escrita", "escrita", "falhou"))
                self.assertEqual(registro["motivo"], repr(erro))

    def test_copiador_ignora_usuario_isMeta_e_preserva_mensagens_reais(self):
        self.gravar_historico([
            {"type": "user", "message": {"content": "Pedido real"}},
            {"type": "assistant", "message": {"content": "Antes da skill"}},
            {"type": "user", "isMeta": True, "message": {"content": "Base directory for this skill: /skill\nTexto injetado"}},
            {"type": "user", "isMeta": True, "message": {"content": [{"type": "text", "text": "Outro texto injetado"}]}},
            {"type": "assistant", "message": {"content": "Depois da skill"}},
            {"type": "user", "isMeta": False, "message": {"content": "Base directory for this skill: texto do usuário"}},
        ])
        _, pasta, _, _, _ = programa.copiar(self.sessao, self.historico)
        mensagens = programa.Documento2(pasta / T["d2"]).mensagens()
        self.assertEqual([m["autor"] for m in mensagens], [T["usuario"], T["claude"], T["usuario"]])
        self.assertEqual([m["n"] for m in mensagens], [1, 2, 3])
        self.assertEqual(mensagens[1]["texto"], "Antes da skill\n\nDepois da skill")
        self.assertEqual(mensagens[2]["texto"], "Base directory for this skill: texto do usuário")
        self.assertNotIn("injetado", (pasta / T["d2"]).read_text(encoding="utf-8"))

    def test_conversa_vazia_nao_cita_M0(self):
        self.gravar_historico([])
        codigo, linha = programa.rodada(self.sessao, caminho_historico=self.historico)
        esperado = "Documentação: nada novo." if programa.LANGUAGE == "pt-br" else "Documentation: nothing new."
        self.assertEqual(codigo, 0)
        self.assertEqual(linha, esperado)
        pasta_doc = self.projeto / programa.PASTA_DOC
        pasta = pasta_doc / T["conversas"] / "2026-11-02-3f9c2a71"
        pasta.mkdir(parents=True)
        self.assertEqual(programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, "3f9c2a71", "pedido"), esperado)


if __name__ == "__main__":
    unittest.main()
