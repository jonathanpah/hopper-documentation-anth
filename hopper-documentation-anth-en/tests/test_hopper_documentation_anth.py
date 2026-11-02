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


class RegressoesDaTarefa02(unittest.TestCase):
    setUp = RegressoesDaTarefa01.setUp
    gravar_historico = RegressoesDaTarefa01.gravar_historico

    def resposta(self, nome="rodada-b1"):
        r = json.loads((CASOS / "redator" / (nome + ".json")).read_text())["structured_output"]
        for item in r["itens_novos"]:
            item["situacao"] = T["situacoes"][item["tipo"]][0]
        if "conversa_simplificada" in r:
            r["conversa_simplificada"] = r["conversa_simplificada"].replace("**Assunto: ", T["assunto"])
        return r

    def preparar_rodada(self):
        registros = programa.ler_registros(CASOS / "b1" / "historico.jsonl")
        for r in registros:
            r.update(cwd=str(self.projeto), sessionId=self.sessao)
        self.historico.write_text("".join(json.dumps(r) + "\n" for r in registros))
        return programa.copiar(self.sessao, self.historico)

    def preparar_migracao(self):
        pasta = self.projeto / programa.PASTA_DOC
        pasta.mkdir(exist_ok=True)
        for a in (CASOS / "b3" / "anth").iterdir():
            (pasta / a.name).write_bytes(a.read_bytes())
        return pasta

    def test_01_reserva_numeros_por_tipo_e_codigo(self):
        pasta = self.preparar_migracao()
        r = self.resposta("migracao-b3-anth")
        r["itens_novos"].append(dict(r["itens_novos"][0], ref="N4", texto="Segunda decisão."))
        with patch.object(programa, "chamar_redator", return_value=(r, {})):
            programa.migrar(self.projeto)
        self.assertEqual([i["id"] for i in programa.itens_de(programa.ler(pasta / T["d4"]))],
                         ["D1-3f9c2a71", "D2-3f9c2a71"])

    def test_02_diario_guarda_mapa_e_reaplica_sem_comparar_texto(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        r = self.resposta()
        r["itens_novos"][1]["texto"] = "Função conforme N1."
        r["conversa_simplificada"] += "\n\nN2 concluída. (M2-3f9c2a71)"
        gravar = programa.gravar_itens
        def grava_e_interrompe(*args):
            gravar(*args)
            raise OSError("depois dos itens")
        with patch.object(programa, "chamar_redator", return_value=(r, {})), \
                patch.object(programa, "gravar_itens", side_effect=grava_e_interrompe):
            with self.assertRaises(OSError):
                programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        diario = next((programa.pasta_de_dados() / "diarios").glob("*.json"))
        dados = json.loads(diario.read_text())
        self.assertEqual(dados["mapa"]["N2"], "F1-3f9c2a71")
        self.assertEqual(dados["resposta"]["itens_novos"][1]["texto"], "Função conforme N1.")
        with patch.object(programa, "chamar_redator", side_effect=AssertionError("chamou outra vez")):
            programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        self.assertEqual([i["id"] for i in programa.todos_os_itens(pasta_doc)],
                         ["D1-3f9c2a71", "F1-3f9c2a71", "PD1-3f9c2a71"])
        self.assertFalse(diario.exists())
        self.assertIn("F1-3f9c2a71 concluída.", programa.ler(pasta / T["d3"]))
        self.assertNotIn("N2", programa.ler(pasta / T["d3"]))

    def test_03_copia_recomeca_no_registro_bruto_seguinte(self):
        for varios in (False, True):
            with self.subTest(varios=varios):
                pasta_doc = self.projeto / programa.PASTA_DOC
                if pasta_doc.exists():
                    import shutil
                    shutil.rmtree(pasta_doc)
                msgs = [{"type": "user", "message": {"content": "Pedido"}},
                        {"type": "assistant", "message": {"content": "Primeira parte"}}]
                if varios:
                    msgs.append({"type": "assistant", "message": {"content": "Segunda parte"}})
                self.gravar_historico(msgs)
                _, pasta, _, *_ = programa.copiar(self.sessao, self.historico)
                antes = (pasta / T["d2"]).read_bytes()
                self.gravar_historico(msgs + [{"type": "assistant", "message": {"content": "Fechamento"}},
                                              {"type": "user", "message": {"content": "Outro pedido"}}])
                with patch.object(programa, "extrair_mensagens", wraps=programa.extrair_mensagens) as extrair:
                    *_, novas, aviso = programa.copiar(self.sessao, self.historico)
                self.assertEqual(extrair.call_count, 1)
                self.assertEqual(extrair.call_args[0][0][0]["uuid"], f"registro-{len(msgs) + 1}")
                self.assertEqual([m["texto"] for m in novas], ["Fechamento", "Outro pedido"])
                self.assertEqual(aviso, "")
                self.assertTrue((pasta / T["d2"]).read_bytes().startswith(antes))
                self.assertEqual([m["n"] for m in programa.Documento2(pasta / T["d2"]).mensagens()], [1, 2, 3, 4])

    def test_04_mudanca_invalida_nao_grava_nem_deixa_diario(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        programa.garantir_documentos_compartilhados(pasta_doc)
        base = self.resposta()
        programa.gravar_itens(pasta_doc, codigo, base, "anterior", {})
        antes = {p: p.read_bytes() for p in pasta_doc.rglob("*.md")}
        r = self.resposta()
        r["mudancas"] = [{"id": "PD1-3f9c2a71", "situacao": "encerrada", "origem": ["M1-3f9c2a71"]}]
        with patch.object(programa, "chamar_redator", return_value=(r, {})):
            with self.assertRaises(programa.Falha):
                programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        self.assertEqual({p: p.read_bytes() for p in pasta_doc.rglob("*.md")}, antes)
        self.assertFalse(list((programa.pasta_de_dados() / "diarios").glob("*.json")))

    def test_05_migracao_rejeita_codigo_com_separador_antes_de_gravar(self):
        pasta = self.preparar_migracao()
        antes = {p: p.read_bytes() for p in pasta.rglob("*") if p.is_file()}
        r = self.resposta("migracao-b3-anth")
        for i in r["itens_novos"]:
            i["conversa"] = "antigo-x/../../../../FORA"
        r["handoffs_antigos"][0]["conversa"] = "antigo-x/../../../../FORA"
        with patch.object(programa, "chamar_redator", return_value=(r, {})):
            with self.assertRaises(programa.Falha):
                programa.migrar(self.projeto)
        self.assertEqual({p: p.read_bytes() for p in pasta.rglob("*") if p.is_file()}, antes)
        self.assertFalse(list(self.raiz.rglob("FORA")))

    def test_06_verificacao_confere_origens_gravadas_no_disco(self):
        pasta = self.preparar_migracao()
        r = self.resposta("migracao-b3-anth")
        with patch.object(programa, "gravar_itens", return_value={}), \
                patch.object(programa, "chamar_redator", return_value=(r, {})):
            with self.assertRaises(programa.Falha):
                programa.migrar(self.projeto)
        self.assertEqual(len(programa.arquivos_antigos(pasta)), 3)

    def test_07_migracao_retomada_usa_diario_sem_redator(self):
        pasta = self.preparar_migracao()
        r = self.resposta("migracao-b3-anth")
        gravar = programa.gravar_itens
        def grava_e_interrompe(*args):
            gravar(*args)
            raise OSError("interrupção")
        with patch.object(programa, "chamar_redator", return_value=(r, {})), \
                patch.object(programa, "gravar_itens", side_effect=grava_e_interrompe):
            with self.assertRaises(OSError):
                programa.migrar(self.projeto)
        with patch.object(programa, "chamar_redator", side_effect=AssertionError("redator repetido")):
            self.assertEqual(programa.migrar(self.projeto), 3)
        self.assertEqual(len(programa.todos_os_itens(pasta)), 3)
        self.assertEqual(programa.arquivos_antigos(pasta), [])

    def test_08_falha_migracao_continua_rodada_e_grava_indice(self):
        pasta = self.preparar_migracao()
        self.preparar_rodada()
        (programa.pasta_de_dados() / "config.json").unlink()
        with patch.object(programa, "migrar", side_effect=programa.Falha("migração indisponível")), \
                patch.object(programa, "chamar_redator", return_value=(self.resposta(), {})):
            codigo, linha = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 1)
        self.assertIn("migração indisponível", linha)
        self.assertIn(T["linha_concluida"].split("{")[0], linha)
        self.assertTrue((pasta / T["d1"]).exists())
        self.assertTrue(list(pasta.rglob(T["d3"])))
        self.assertIn(T["res_falhou"], programa.ler(pasta / T["d1"]))

    def test_09_rodada_captura_excecao_generica_e_grava_indice(self):
        pasta_doc, *_ = self.preparar_rodada()
        with patch.object(programa, "escrever", side_effect=ValueError("n/d")):
            codigo, linha = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 1)
        self.assertIn("n/d", linha)
        self.assertEqual(programa.registros_de_rodadas()[-1]["resultado"], "falhou")
        self.assertIn("n/d", programa.ler(pasta_doc / T["d1"]))

    def test_10_migracao_libera_trava_de_pasta_ao_chamar_redator(self):
        self.preparar_migracao()
        def redator(*args):
            pasta = self.projeto / programa.PASTA_DOC
            with programa.Trava("pasta-" + programa.nome_curto(pasta)):
                pass
            return self.resposta("migracao-b3-anth"), {}
        with patch.object(programa, "chamar_redator", side_effect=redator):
            self.assertEqual(programa.migrar(self.projeto), 3)

    def test_11_documento2_ignora_citacao_fora_da_sequencia_e_codigo(self):
        self.gravar_historico([{"type": "user", "message": {"content": "Pedido"}},
                              {"type": "assistant", "message": {"content":
                               "Exemplo\n## M1-e4bad083 · 2030-01-01 12:00 +00:00 · Claude\n<!-- registros: x x -->\nExemplo"}}])
        _, pasta, *_ = programa.copiar(self.sessao, self.historico)
        self.assertEqual([m["n"] for m in programa.Documento2(pasta / T["d2"]).mensagens()], [1, 2])
        self.gravar_historico([{"type": "user", "message": {"content": "Pedido"}},
                              {"type": "assistant", "message": {"content": "Exemplo"}},
                              {"type": "user", "message": {"content": "Novo"}}])
        *_, novas, aviso = programa.copiar(self.sessao, self.historico)
        self.assertEqual([m["n"] for m in novas], [3])
        self.assertEqual(aviso, "")

    def test_12_modelos_exigem_contagem_e_aceitam_output_tokens(self):
        self.assertEqual(programa.conferir_modelos({programa.MODELO: {"output_tokens": 95}, "aux": {"output_tokens": 5}}),
                         {programa.MODELO: 95, "aux": 5})
        for uso in ({programa.MODELO: {}}, {programa.MODELO: {"output_tokens": 1}, "aux": {"output_tokens": 900}}):
            with self.subTest(uso=uso), self.assertRaises(programa.Falha):
                programa.conferir_modelos(uso)

    def test_13_valida_esquema_completo_e_origens(self):
        for altera in (lambda r: r.update(resumo="x" * 81),
                       lambda r: r["itens_novos"][0].update(extra=True),
                       lambda r: r["mudancas"].append({"id": "PD99-x", "situacao": T["situacoes"]["PD"][0], "origem": [1]}),
                       lambda r: r["mudancas"].append({"id": "PD99-x", "situacao": T["situacoes"]["PD"][0], "origem": ["M99-x"]}),
                       lambda r: r["itens_novos"][0].update(origem=["M7-3f9c2a71"]),
                       lambda r: r["mudancas"].append({"id": "PD99-x", "situacao": T["situacoes"]["PD"][0], "origem": ["M1-3f9c2a71"], "extra": 1})):
            r = self.resposta()
            altera(r)
            with self.subTest(resposta=r), self.assertRaises(programa.Falha):
                programa.validar_resposta(r, programa.ESQUEMA_RODADA, {f"M{n}-3f9c2a71" for n in range(1, 7)}, set())
        for campo, valor in (("data", "2026-99-99"), ("extra", "x"), ("resumo", "x" * 81)):
            r = self.resposta("migracao-b3-anth")
            r["handoffs_antigos"][0][campo] = valor
            with self.subTest(campo=campo), self.assertRaises(programa.Falha):
                programa.validar_resposta(r, programa.esquema_de_migracao(), set(), set(), migracao=True,
                                         arquivos_validos={a.name for a in (CASOS / "b3" / "anth").iterdir()})

        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        with patch.object(programa, "chamar_redator", return_value=(self.resposta(), {})):
            programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        with self.historico.open("a") as f:
            f.write(json.dumps({"type": "user", "uuid": "nova-janela", "timestamp": "2026-11-02T10:02:00Z",
                                "sessionId": self.sessao, "cwd": str(self.projeto), "message": {"content": "Novo pedido"}}) + "\n")
        programa.copiar(self.sessao, self.historico)
        with patch.object(programa, "chamar_redator", return_value=(self.resposta(), {})):
            with self.assertRaises(programa.Falha):
                programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        self.assertFalse(list((programa.pasta_de_dados() / "diarios").glob("*.json")))

    def test_14_migracao_oculta_entrada_e_todos_campos_de_texto(self):
        pasta = self.preparar_migracao()
        (pasta / "index.md").write_text("a senha do servidor é Pl4nt@d4#2026 hoje")
        entrada = programa.entrada_da_migracao(pasta, programa.arquivos_antigos(pasta))
        self.assertNotIn("Pl4nt@d4#2026", entrada)
        r = self.resposta("migracao-b3-anth")
        r["resumo"] = "senha=Pl4nt@d4#2026"
        r["itens_novos"][0]["texto"] = "senha=Pl4nt@d4#2026"
        r["itens_novos"][2]["recomendacao"] = "senha=Pl4nt@d4#2026"
        r["itens_novos"][2]["depende_de"] = "senha=Pl4nt@d4#2026"
        r["handoffs_antigos"][0]["handoff"]["objetivo"] = "senha=Pl4nt@d4#2026"
        with patch.object(programa, "chamar_redator", return_value=(r, {})):
            programa.migrar(self.projeto)
        self.assertTrue(all("Pl4nt@d4#2026" not in p.read_text() for p in pasta.rglob("*.md")))

    def test_15_colisao_de_codigo_entra_no_registro(self):
        self.preparar_rodada()
        outra = "3f9c2a71-abcd-5678-9abc-123456789abc"
        registros = programa.ler_registros(self.historico)
        for r in registros:
            r["sessionId"] = outra
        self.historico.write_text("".join(json.dumps(r) + "\n" for r in registros))
        _, _, codigo, *_ = programa.copiar(outra, self.historico)
        self.assertEqual(codigo, "3f9c2a71abcd")
        self.assertTrue(any(r["conversa"] == outra and ("colisão" if programa.LANGUAGE == "pt-br" else "collision") in r["motivo"].lower() for r in programa.registros_de_rodadas()))

    def test_16_resumo_e_acrescentado_sem_regravar_registro(self):
        programa.registrar("outra", self.projeto, "pedido", "copia", "concluída")
        antes = (programa.pasta_de_dados() / "rodadas.jsonl").read_bytes()
        original = Path.write_text
        def escrita(caminho, *args, **kwargs):
            self.assertNotEqual(caminho.name, "rodadas.jsonl", "regravou todo o registro")
            return original(caminho, *args, **kwargs)
        with patch.object(Path, "write_text", escrita):
            linha = programa.registrar_escrita(self.sessao, self.projeto, "pedido", "concluída", resumo="Resumo")
        self.assertEqual(linha["resumo"], "Resumo")
        self.assertTrue((programa.pasta_de_dados() / "rodadas.jsonl").read_bytes().startswith(antes))

    def test_17_configuracao_invalida_desliga_migracao_e_registra(self):
        arquivo = programa.pasta_de_dados() / "config.json"
        for texto in ("{", "[]", '"texto"', '{"migracao_automatica":"false"}', '{}'):
            with self.subTest(texto=texto):
                arquivo.write_text(texto)
                self.assertFalse(programa.configuracao()["migracao_automatica"])
                self.assertIn("config.json", programa.registros_de_rodadas()[-1]["motivo"])
        arquivo.unlink()
        self.assertTrue(programa.configuracao()["migracao_automatica"])

    def test_18_rejeita_bloco_sem_linha_de_assunto(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        r = self.resposta()
        r["conversa_simplificada"] = "Texto sem assunto."
        with patch.object(programa, "chamar_redator", return_value=(r, {})):
            with self.assertRaises(programa.Falha):
                programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        self.assertFalse((pasta / T["d3"]).exists())
        self.assertFalse(list((programa.pasta_de_dados() / "diarios").glob("*.json")))


class RegressoesDaTarefa05(unittest.TestCase):
    setUp = RegressoesDaTarefa01.setUp
    gravar_historico = RegressoesDaTarefa01.gravar_historico
    resposta = RegressoesDaTarefa02.resposta
    preparar_rodada = RegressoesDaTarefa02.preparar_rodada
    preparar_migracao = RegressoesDaTarefa02.preparar_migracao

    def validar(self, resposta, itens=()):
        return programa.validar_resposta(resposta, programa.ESQUEMA_RODADA,
                                         {f"M{n}-3f9c2a71" for n in range(1, 7)}, set(itens))

    def campos_de_texto(self, resposta):
        resposta["mudancas"] = [{"id": "N3", "situacao": T["situacoes"]["PD"][1] + "M1-3f9c2a71 (fim)",
                                  "origem": ["M1-3f9c2a71"]}]
        return ([(resposta, "conversa_simplificada")] +
                [(resposta["handoff"], k) for k in programa.ESQUEMA_HANDOFF] +
                [(i, k) for i in resposta["itens_novos"] for k in ("texto", "recomendacao", "depende_de")] +
                [(resposta["mudancas"][0], "situacao")])

    def test_mensagem_inexistente_e_rejeitada_em_todos_os_campos(self):
        for indice in range(len(self.campos_de_texto(self.resposta()))):
            r = self.resposta()
            objeto, campo = self.campos_de_texto(r)[indice]
            objeto[campo] += " M19-3f9c2a71"
            with self.subTest(indice=indice, campo=campo), self.assertRaisesRegex(programa.Falha, "M19-3f9c2a71"):
                self.validar(r)

    def test_item_futuro_ou_codigo_inexistente_e_rejeitado_em_todos_os_campos(self):
        itens = {"D7-3f9c2a71", "F2-antigo-abcd", "PD3-outraconversa",
                 "F30-3f9c2a71", "D30-antigo-abcd", "D30-outraconversa"}
        for identificador in ("D8-3f9c2a71", "F3-antigo-abcd", "PD4-outraconversa",
                              "D1-ausente", "F1-ausente", "PD1-ausente", "F1-outraconversa"):
            for indice in range(len(self.campos_de_texto(self.resposta()))):
                r = self.resposta()
                objeto, campo = self.campos_de_texto(r)[indice]
                objeto[campo] += " " + identificador
                with self.subTest(id=identificador, indice=indice), self.assertRaisesRegex(programa.Falha, identificador):
                    self.validar(r, itens)

    def test_item_apagado_a_mao_continua_aceito(self):
        pasta_doc = self.projeto / programa.PASTA_DOC
        pasta_doc.mkdir()
        apagados = set()
        for tipo, caminho in programa.documentos_da_pasta(pasta_doc).items():
            texto = ""
            for codigo in ("3f9c2a71", "antigo-abcd"):
                apagados.add(f"{tipo}1-{codigo}")
                texto += f"### {tipo}1-{codigo}\nItem apagado.\n\n### {tipo}2-{codigo}\nItem preservado.\n\n"
            caminho.write_text(texto)
            for identificador in apagados:
                texto = texto.replace(f"### {identificador}\nItem apagado.\n\n", "")
            caminho.write_text(texto)
        itens = {i["id"] for i in programa.todos_os_itens(pasta_doc)}
        self.assertEqual(itens, {f"{tipo}2-{codigo}" for tipo in ("D", "F", "PD")
                                 for codigo in ("3f9c2a71", "antigo-abcd")})
        self.assertTrue(apagados.isdisjoint(itens))
        r = self.resposta()
        for objeto, campo in self.campos_de_texto(r):
            objeto[campo] += " " + " ".join(sorted(apagados))
        r["itens_novos"][0]["situacao"] = T["situacoes"]["D"][1] + "D1-3f9c2a71"
        self.assertIs(self.validar(r, itens), r)

    def test_N1_e_itens_existentes_continuam_aceitos(self):
        r = self.resposta()
        itens = {"D7-outraconversa", "F2-antigo-abcd", "PD3-outraconversa"}
        for objeto, campo in self.campos_de_texto(r):
            objeto[campo] += " N1 " + " ".join(sorted(itens))
        self.assertIs(self.validar(r, itens), r)
        r["itens_novos"][0]["situacao"] = T["situacoes"]["D"][1] + "N1"
        self.validar(r, itens)

    def test_referencia_N_inexistente_e_situacao_de_item_novo_sao_conferidas(self):
        for identificador in ("N99", "D19-3f9c2a71"):
            r = self.resposta()
            r["itens_novos"][0]["situacao"] = T["situacoes"]["D"][1] + identificador
            with self.subTest(id=identificador), self.assertRaisesRegex(programa.Falha, identificador):
                self.validar(r)

    def test_rodada_repete_uma_vez_e_registra_as_duas_chamadas(self):
        pasta_doc, pasta, *_ = self.preparar_rodada()
        invalida = self.resposta()
        invalida["handoff"]["proximo_passo"] = "A próxima rodada deve cobrir M19-3f9c2a71 em diante."
        with patch.object(programa, "chamar_redator", side_effect=[(invalida, {programa.MODELO: 11}),
                                                                 (self.resposta(), {programa.MODELO: 23})]) as redator:
            codigo, _ = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 0)
        self.assertEqual(redator.call_count, 2)
        entrada = redator.call_args_list[0].args[0]
        linha = ("Problemas na resposta anterior: referências inexistentes: M19-3f9c2a71."
                 if programa.LANGUAGE == "pt-br" else
                 "Problems in the previous response: nonexistent references: M19-3f9c2a71.")
        self.assertEqual(redator.call_args_list[1].args, (entrada + linha + "\n", programa.ESQUEMA_RODADA))
        registros = [r for r in programa.registros_de_rodadas() if r["etapa"] == "escrita"]
        self.assertEqual([r["modelos"] for r in registros], [{programa.MODELO: 11}, {programa.MODELO: 23}])
        self.assertEqual([r["resultado"] for r in registros], ["em andamento", "concluída"])
        self.assertIn("M19-3f9c2a71", registros[0]["motivo"])
        self.assertNotIn("M19-3f9c2a71", "\n".join(p.read_text() for p in pasta_doc.rglob("*.md")))
        self.assertTrue((pasta / T["d7"]).exists())

    def test_segunda_resposta_invalida_falha_sem_gravar_documentos_3_a_7(self):
        pasta_doc, pasta, *_ = self.preparar_rodada()
        invalida = self.resposta()
        invalida["handoff"]["proximo_passo"] += " M19-3f9c2a71"
        with patch.object(programa, "chamar_redator", side_effect=[(invalida, {programa.MODELO: 11}),
                                                                 (invalida, {programa.MODELO: 23})]) as redator:
            codigo, linha = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 1)
        self.assertIn("M19-3f9c2a71", linha)
        self.assertEqual(redator.call_count, 2)
        self.assertFalse((pasta / T["d3"]).exists())
        self.assertFalse((pasta / T["d7"]).exists())
        self.assertFalse(any(p.exists() for p in programa.documentos_da_pasta(pasta_doc).values()))
        self.assertFalse(list((programa.pasta_de_dados() / "diarios").glob("*.json")))
        registros = [r for r in programa.registros_de_rodadas() if r["etapa"] == "escrita"]
        self.assertEqual([r["modelos"] for r in registros if r["modelos"]],
                         [{programa.MODELO: 11}, {programa.MODELO: 23}])
        self.assertEqual(registros[-1]["resultado"], "falhou")
        self.assertIn("M19-3f9c2a71", programa.ler(pasta_doc / T["d1"]))

    def test_erro_de_esquema_nao_aciona_nova_tentativa(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        r = self.resposta()
        r["extra"] = True
        r["handoff"]["proximo_passo"] += " M19-3f9c2a71"
        r["itens_novos"][0]["origem"] = ["M19-3f9c2a71"]
        r["itens_novos"][0]["situacao"] = "invalida"
        with patch.object(programa, "chamar_redator", return_value=(r, {})) as redator:
            with self.assertRaises(programa.Falha):
                programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
            self.assertEqual(redator.call_count, 1)

    def test_textos_aceitam_mensagens_anteriores_e_de_outra_conversa(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        outra = pasta_doc / T["conversas"] / "2026-03-13-abc12345"
        outra.mkdir()
        (outra / T["d2"]).write_text(programa.ler(pasta / T["d2"]).replace(codigo, "abc12345"))
        r = self.resposta()
        for i in r["itens_novos"]:
            i["origem"] = ["M4-3f9c2a71"]
        r["handoff"]["objetivo"] += " M1-abc12345"
        with patch.object(programa, "ultimo_coberto", return_value=3), \
                patch.object(programa, "chamar_redator", return_value=(r, {})) as redator:
            programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        self.assertEqual(redator.call_count, 1)
        self.assertIn("M1-abc12345", programa.ler(pasta / T["d7"]))

    def test_mensagem_ja_copiada_depois_do_fim_do_trecho_e_rejeitada(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        mensagens = programa.Documento2(pasta / T["d2"]).mensagens()
        r = self.resposta()
        r["itens_novos"] = []
        r["conversa_simplificada"] = T["assunto"] + "teste.** (M2-3f9c2a71)"
        r["handoff"] = {k: "M1-3f9c2a71" for k in programa.ESQUEMA_HANDOFF}
        with patch.object(programa, "partes_do_trecho", return_value=[mensagens[:1]]), \
                patch.object(programa, "chamar_redator", return_value=(r, {})) as redator:
            with self.assertRaisesRegex(programa.Falha, "M2-3f9c2a71"):
                programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
        self.assertEqual(redator.call_count, 2)

    def test_migracao_rejeita_mensagens_e_itens_inexistentes_antes_de_gravar(self):
        pasta = self.preparar_migracao()
        antes = {p: p.read_bytes() for p in pasta.rglob("*") if p.is_file()}
        for identificador in ("M1-3f9c2a71", "PD19-antigo-abcd"):
            for destino in ("item", *programa.ESQUEMA_HANDOFF):
                r = self.resposta("migracao-b3-anth")
                if destino == "item":
                    r["itens_novos"][0]["texto"] += " " + identificador
                else:
                    r["handoffs_antigos"][0]["handoff"][destino] += " " + identificador
                with self.subTest(id=identificador, destino=destino), \
                        patch.object(programa, "chamar_redator", return_value=(r, {})) as redator:
                    with self.assertRaisesRegex(programa.Falha, identificador):
                        programa.migrar(self.projeto)
                    self.assertEqual(redator.call_count, 2)
                self.assertEqual({p: p.read_bytes() for p in pasta.rglob("*") if p.is_file()}, antes)
        self.assertFalse(list((programa.pasta_de_dados() / "diarios").glob("*.json")))

    def test_migracao_repete_e_aceita_N1(self):
        pasta = self.preparar_migracao()
        invalida = self.resposta("migracao-b3-anth")
        invalida["handoffs_antigos"][0]["handoff"]["objetivo"] += " M1-3f9c2a71"
        valida = self.resposta("migracao-b3-anth")
        valida["itens_novos"][1]["texto"] += " Conforme N1."
        with patch.object(programa, "chamar_redator", side_effect=[(invalida, {programa.MODELO: 11}),
                                                                 (valida, {programa.MODELO: 23})]) as redator:
            self.assertEqual(programa.migrar(self.projeto), 3)
        self.assertEqual(redator.call_count, 2)
        self.assertEqual(programa.arquivos_antigos(pasta), [])
        self.assertIn("Conforme D1-3f9c2a71.", programa.ler(pasta / T["d5"]))
        registros = [r for r in programa.registros_de_rodadas() if r["etapa"] == "migracao"]
        self.assertEqual(registros[0]["modelos"], {programa.MODELO: 11})
        self.assertEqual(registros[-1]["modelos"], {programa.MODELO: 23})


class RegressoesDaTarefa08(unittest.TestCase):
    setUp = RegressoesDaTarefa01.setUp
    resposta = RegressoesDaTarefa02.resposta
    preparar_rodada = RegressoesDaTarefa02.preparar_rodada

    def preparar_incremento(self):
        pasta_doc, pasta, *_ = self.preparar_rodada()
        with patch.object(programa, "chamar_redator", return_value=(self.resposta(), {})):
            self.assertEqual(programa.rodada(self.sessao, caminho_historico=self.historico)[0], 0)
        self.assertEqual(programa.ultimo_coberto(pasta), 6)
        with self.historico.open("a", encoding="utf-8") as f:
            for n, tipo in ((7, "user"), (8, "assistant")):
                f.write(json.dumps({"type": tipo, "uuid": f"incremento-{n}", "sessionId": self.sessao,
                                    "cwd": str(self.projeto), "timestamp": f"2026-11-02T11:00:0{n}Z",
                                    "message": {"content": f"Continuação {n}."}}) + "\n")
        return pasta_doc, pasta

    def resposta_do_incremento(self):
        r = self.resposta()
        for item in r["itens_novos"]:
            item["origem"] = ["M7-3f9c2a71"]
        r["conversa_simplificada"] = T["assunto"] + "continuidade.**\n\nContinuação. (M7-3f9c2a71)"
        r["handoff"] = {k: "Continuação. (M7-3f9c2a71)" for k in programa.ESQUEMA_HANDOFF}
        r["mudancas"] = [{"id": "PD1-3f9c2a71", "situacao": T["situacoes"]["PD"][1] + "M8-3f9c2a71 (fim)",
                           "origem": ["M8-3f9c2a71"]}]
        return r

    def conferir_correcao_de_origem(self, campo):
        pasta_doc, pasta = self.preparar_incremento()
        invalida = self.resposta_do_incremento()
        invalida[campo][0]["origem"] = ["M6-3f9c2a71"]
        self.assertIn("M6-3f9c2a71", programa.ler(pasta / T["d2"]))
        with patch.object(programa, "chamar_redator", side_effect=[(invalida, {programa.MODELO: 11}),
                                                                 (self.resposta_do_incremento(), {programa.MODELO: 23})]) as redator:
            codigo, _ = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 0)
        self.assertEqual(redator.call_count, 2)
        entrada = redator.call_args_list[0].args[0]
        linha = ("Problemas na resposta anterior: origem fora do trecho novo: M6-3f9c2a71; "
                 "a origem de um item novo ou de uma mudança é uma mensagem de M7-3f9c2a71 a M8-3f9c2a71 ou um item existente."
                 if programa.LANGUAGE == "pt-br" else
                 "Problems in the previous response: source outside the new segment: M6-3f9c2a71; "
                 "the source of a new item or a change is a message from M7-3f9c2a71 to M8-3f9c2a71 or an existing item.")
        self.assertEqual(redator.call_args_list[1].args, (entrada + linha + "\n", programa.ESQUEMA_RODADA))
        registros = [r for r in programa.registros_de_rodadas() if r["etapa"] == "escrita"][-2:]
        self.assertEqual([r["modelos"] for r in registros], [{programa.MODELO: 11}, {programa.MODELO: 23}])
        self.assertEqual([r["resultado"] for r in registros], ["em andamento", "concluída"])
        self.assertEqual(programa.ultimo_coberto(pasta), 8)
        self.assertIn("M8-3f9c2a71", programa.ler(pasta / T["d7"]))
        self.assertIn("### D2-3f9c2a71", programa.ler(pasta_doc / T["d4"]))
        self.assertIn(T["situacoes"]["PD"][1] + "M8-3f9c2a71", programa.ler(pasta_doc / T["d6"]))

    def test_origem_anterior_em_item_novo_repete_e_conclui(self):
        self.conferir_correcao_de_origem("itens_novos")

    def test_origem_anterior_em_mudanca_repete_e_conclui(self):
        self.conferir_correcao_de_origem("mudancas")

    def test_origem_anterior_duas_vezes_falha_e_preserva_documentos(self):
        pasta_doc, pasta = self.preparar_incremento()
        antes = {p: p.read_bytes() for p in [pasta / T["d3"], pasta / T["d7"],
                                             *programa.documentos_da_pasta(pasta_doc).values()]}
        invalida = self.resposta_do_incremento()
        invalida["itens_novos"][0]["origem"] = ["M6-3f9c2a71"]
        invalida["mudancas"][0]["origem"] = ["M5-3f9c2a71"]
        with patch.object(programa, "chamar_redator", side_effect=[(invalida, {programa.MODELO: 11}),
                                                                 (invalida, {programa.MODELO: 23})]) as redator:
            codigo, linha = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 1)
        self.assertEqual(redator.call_count, 2)
        for origem in ("M5-3f9c2a71", "M6-3f9c2a71"):
            self.assertIn(origem, linha)
        self.assertEqual({p: p.read_bytes() for p in antes}, antes)
        self.assertEqual(programa.ultimo_coberto(pasta), 6)
        self.assertFalse(list((programa.pasta_de_dados() / "diarios").glob("*.json")))
        registros = [r for r in programa.registros_de_rodadas() if r["etapa"] == "escrita"][-3:]
        self.assertEqual([r["modelos"] for r in registros], [{programa.MODELO: 11}, {programa.MODELO: 23}, {}])
        self.assertEqual(registros[-1]["resultado"], "falhou")
        self.assertIn("M6-3f9c2a71", programa.ler(pasta_doc / T["d1"]))

    def test_situacao_e_assunto_repete_com_lista_de_todos_os_problemas(self):
        _, pasta, *_ = self.preparar_rodada()
        invalida = self.resposta()
        invalida["conversa_simplificada"] = "Texto sem assunto."
        invalida["itens_novos"][0]["situacao"] = "invalida\nna linha seguinte"
        invalida["itens_novos"][0]["origem"] = ["M19-3f9c2a71"]
        invalida["mudancas"] = [{"id": "N3", "situacao": "outra invalida", "origem": ["M1-3f9c2a71"]}]
        invalida["handoff"]["proximo_passo"] += " M99-3f9c2a71"
        with patch.object(programa, "chamar_redator", side_effect=[(invalida, {programa.MODELO: 11}),
                                                                 (self.resposta(), {programa.MODELO: 23})]) as redator:
            codigo, _ = programa.rodada(self.sessao, caminho_historico=self.historico)
        self.assertEqual(codigo, 0)
        self.assertEqual(redator.call_count, 2)
        entrada = redator.call_args_list[0].args[0]
        segunda = redator.call_args_list[1].args[0]
        self.assertTrue(segunda.startswith(entrada))
        linha = segunda[len(entrada):]
        self.assertEqual(len(linha.splitlines()), 1)
        for problema in ("invalida", "na linha seguinte", "outra invalida", "conversa_simplificada", "M19-3f9c2a71", "M99-3f9c2a71"):
            self.assertIn(problema, linha)
        self.assertIn("M1-3f9c2a71 a M6-3f9c2a71" if programa.LANGUAGE == "pt-br" else
                      "M1-3f9c2a71 to M6-3f9c2a71", linha)
        self.assertNotIn("M99-3f9c2a71", programa.ler(pasta / T["d7"]))

    def test_modelo_e_tempo_nao_acionam_nova_tentativa(self):
        pasta_doc, pasta, codigo, *_ = self.preparar_rodada()
        envelope = {"structured_output": self.resposta(), "modelUsage": {"outro-modelo": {"outputTokens": 10}}}
        casos = (("modelo", subprocess.CompletedProcess([], 0, json.dumps(envelope), "")),
                 ("tempo", subprocess.TimeoutExpired(["redator-simulado"], 900)))
        for motivo, resultado in casos:
            opcoes = {"side_effect": resultado} if isinstance(resultado, Exception) else {"return_value": resultado}
            with self.subTest(motivo=motivo), patch.object(programa, "executavel_do_claude", return_value="redator-simulado"), \
                    patch.object(programa.subprocess, "run", **opcoes) as processo:
                with self.assertRaises(programa.Falha) as erro:
                    programa.escrever(self.sessao, self.projeto, pasta_doc, pasta, codigo, "pedido")
                self.assertEqual(processo.call_count, 1)
                self.assertIn(T["motivo_modelo"].format(modelo=programa.MODELO) if motivo == "modelo" else
                              T["motivo_tempo"].format(min=15), str(erro.exception))


class RegressoesDaTarefa11(unittest.TestCase):
    def test_rodada_sem_permissao_imprime_falha_original_mesmo_sem_registro_ou_marcador(self):
        with tempfile.TemporaryDirectory() as temporario:
            raiz = Path(temporario).resolve()
            config = raiz / "config"
            config.mkdir()
            marcador_bloqueado = raiz / "marcador-bloqueado"
            marcador_bloqueado.mkdir()
            marcador_gravavel = raiz / "marcador.json"
            config.chmod(0o555)
            try:
                self.assertFalse(os.access(config, os.W_OK))
                for marcador in (None, marcador_gravavel, marcador_bloqueado):
                    with self.subTest(marcador=marcador):
                        comando = [sys.executable, str(RAIZ / "scripts" / "hopper_documentation_anth.py"),
                                   "rodada", "--sessao", "3f9c2a71-1234-5678-9abc-123456789abc"]
                        if marcador is not None:
                            comando.extend(["--marcador", str(marcador)])
                        resultado = subprocess.run(comando, text=True, capture_output=True, timeout=10,
                                                   env={**os.environ, "CLAUDE_CONFIG_DIR": str(config)})
                        self.assertEqual(resultado.returncode, 1, resultado.stderr)
                        self.assertNotIn("Traceback", resultado.stderr)
                        self.assertTrue(resultado.stdout, resultado.stderr)
                        linha = resultado.stdout.splitlines()[-1]
                        prefixo = "Documentação falhou:" if programa.LANGUAGE == "pt-br" else "Documentation failed:"
                        self.assertTrue(linha.startswith(prefixo), linha)
                        self.assertIn("PermissionError", linha)
                        self.assertNotIn("IsADirectoryError", linha)
                        self.assertEqual(resultado.stderr, linha + "\n")
                        if marcador == marcador_gravavel:
                            self.assertEqual(json.loads(marcador.read_text(encoding="utf-8")),
                                             {"codigo": 1, "linha": linha})
                self.assertFalse((config / "plugins").exists())
            finally:
                config.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
