"""Apoio dos testes de aceite (critério congelado, U2). Interface do programa pela decisão D-09.

Os testes tratam o programa como caixa preta: chamam `python3 <pacote>/scripts/hopper_documentation_anth.py`
com uma pasta de configuração temporária (`CLAUDE_CONFIG_DIR`), o redator simulado e a escala de tempo reduzida.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PACOTE = os.environ.get("HOPPER_DOCUMENTATION_ANTH_PACOTE", "hopper-documentation-anth-pt-br")
IDIOMA = "en" if PACOTE.endswith("-en") else "pt-br"
PROGRAMA = RAIZ / PACOTE / "scripts" / "hopper_documentation_anth.py"
SKILL = RAIZ / PACOTE / "skills" / "hopper-documentation-anth"
CASOS = RAIZ / "aceite" / "casos"
SIMULADO = CASOS / "redator" / "claude-simulado.py"
SESSAO_B1 = "3f9c2a71-5b8e-4d0a-9c61-2e7f4b1a8d05"
CODIGO_B1 = "3f9c2a71"
PASTA_DE_DADOS = "hopper-documentation-anth-hopper-documentation-anth"

TEXTO = {
    "pt-br": {
        "pasta_doc": "docs-by-hopper-documentation", "conversas": "conversas",
        "d1": "1-indice.md", "d2": "2-conversa-integral.md", "d3": "3-conversa-simplificada.md",
        "d4": "4-decisoes.md", "d5": "5-funcoes.md", "d6": "6-pendencias.md", "d7": "7-handoff.md",
        "titulo_d1": "Índice da documentação", "titulo_d2": "Conversa integral", "titulo_d3": "Conversa simplificada",
        "titulo_d4": "Decisões", "titulo_d5": "Funções implementadas", "titulo_d6": "Pendências", "titulo_d7": "Handoff",
        "conversa": "Conversa", "pasta_do_projeto": "Pasta do projeto", "fuso": "Fuso dos horários",
        "origem": "Origem", "situacao": "Situação", "intervalo": "Intervalo da rodada",
        "recomendacao": "Recomendação", "depende_de": "Depende de",
        "ultima_coberta": "Última mensagem coberta", "data_da_rodada": "Data da rodada", "redator": "Redator",
        "vigente": "vigente", "substituida": "substituída por", "revogada": "revogada em",
        "concluida": "concluída", "desfeita": "desfeita em", "aberta": "aberta", "encerrada": "encerrada em",
        "ordem": "Ordem de leitura", "secao_conversas": "Conversas",
        "colunas": ["Conversa", "Início", "Última mensagem", "Última rodada", "Resultado", "Assunto"],
        "res_concluida": "concluída", "res_falhou": "falhou", "res_nada_novo": "nada novo", "res_andamento": "em andamento",
        "sem_integral": "sem conversa integral", "assunto": "**Assunto: ", "sem_conteudo": "Sem conteúdo novo relevante.",
        "migracao": "migração", "oculto": "[oculto]", "imagem": "[imagem anexada]", "arquivo": "[arquivo anexado: ",
        "interrupcao": "O usuário interrompeu a resposta.", "ferramenta": "Ferramenta: ",
        "autores": {"usuario": "Usuário", "claude": "Claude", "resposta": "Resposta do usuário",
                    "plano": "Plano aprovado", "agente": "Relato de agente", "evento": "Evento"},
        "secoes_d7": ["Objetivo", "Pautas e estado atual", "Próximo passo", "Decisões e autorizações vigentes",
                      "Restrições vigentes", "Descobertas e tentativas descartadas", "Pendências e compromissos",
                      "Lacunas", "Como retomar"],
        "secoes_skill": ["O que a skill produz", "Como a skill roda"],
        "regras": "regras-de-escrita.md", "modelos": "modelos.md",
    },
    "en": {
        "pasta_doc": "docs-by-hopper-documentation", "conversas": "conversations",
        "d1": "1-index.md", "d2": "2-full-conversation.md", "d3": "3-simplified-conversation.md",
        "d4": "4-decisions.md", "d5": "5-functions.md", "d6": "6-pending.md", "d7": "7-handoff.md",
        "titulo_d1": "Documentation index", "titulo_d2": "Full conversation", "titulo_d3": "Simplified conversation",
        "titulo_d4": "Decisions", "titulo_d5": "Implemented functions", "titulo_d6": "Pending items", "titulo_d7": "Handoff",
        "conversa": "Conversation", "pasta_do_projeto": "Project folder", "fuso": "Time zone",
        "origem": "Source", "situacao": "Status", "intervalo": "Run range",
        "recomendacao": "Recommendation", "depende_de": "Depends on",
        "ultima_coberta": "Last covered message", "data_da_rodada": "Run date", "redator": "Writer",
        "vigente": "in force", "substituida": "replaced by", "revogada": "revoked in",
        "concluida": "done", "desfeita": "undone in", "aberta": "open", "encerrada": "closed in",
        "ordem": "Reading order", "secao_conversas": "Conversations",
        "colunas": ["Conversation", "Start", "Last message", "Last run", "Result", "Subject"],
        "res_concluida": "done", "res_falhou": "failed", "res_nada_novo": "nothing new", "res_andamento": "in progress",
        "sem_integral": "no full conversation", "assunto": "**Subject: ", "sem_conteudo": "No relevant new content.",
        "migracao": "migration", "oculto": "[hidden]", "imagem": "[image attached]", "arquivo": "[file attached: ",
        "interrupcao": "The user interrupted the response.", "ferramenta": "Tool: ",
        "autores": {"usuario": "User", "claude": "Claude", "resposta": "User answer",
                    "plano": "Approved plan", "agente": "Agent report", "evento": "Event"},
        "secoes_d7": ["Goal", "Topics and current state", "Next step", "Decisions and authorizations in force",
                      "Constraints in force", "Findings and discarded approaches", "Pending items and commitments",
                      "Gaps", "How to resume"],
        "secoes_skill": ["What the skill produces", "How the skill runs"],
        "regras": "writing-rules.md", "modelos": "templates.md",
    },
}[IDIOMA]

SITUACOES_PT_EN = {"vigente": "in force", "substituída por": "replaced by", "revogada em": "revoked in",
                   "concluída": "done", "desfeita em": "undone in", "aberta": "open", "encerrada em": "closed in"}


def sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def le(caminho):
    return Path(caminho).read_text(encoding="utf-8")


def pasta_codificada(pasta):
    return "".join(c if c.isalnum() else "-" for c in str(pasta))


class Ambiente:
    """Pasta temporária com a pasta de configuração, a pasta do projeto e o redator simulado."""

    def __init__(self):
        self.raiz = Path(tempfile.mkdtemp(prefix="aceite-")).resolve()
        self.config = self.raiz / "config"
        self.projeto = self.raiz / "projeto"
        self.projeto.mkdir(parents=True)
        self.dados = self.config / "plugins" / "data" / PASTA_DE_DADOS
        self.registro_simulado = self.raiz / "simulado"
        self.respostas = self.raiz / "respostas"
        self.respostas.mkdir()
        self.config.mkdir(parents=True)

    def limpa(self):
        shutil.rmtree(self.raiz, ignore_errors=True)

    # --- histórico -----------------------------------------------------------------------------------
    def historico(self, sessao):
        return self.config / "projects" / pasta_codificada(self.projeto) / f"{sessao}.jsonl"

    def grava_historico(self, sessao, registros, pasta_do_projeto=None):
        """Grava os registros com `sessionId` e `cwd` da pasta do projeto deste ambiente."""
        caminho = self.historico(sessao)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with caminho.open("w", encoding="utf-8") as f:
            for r in registros:
                if isinstance(r, dict) and r.get("type") != "summary":
                    r = dict(r, sessionId=sessao, cwd=str(pasta_do_projeto or self.projeto))
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        return caminho

    def historico_b1(self, sessao=SESSAO_B1):
        return self.grava_historico(sessao, registros_de(CASOS / "b1" / "historico.jsonl"))

    def acrescenta_historico(self, sessao, registros):
        with self.historico(sessao).open("a", encoding="utf-8") as f:
            for r in registros:
                r = dict(r, sessionId=sessao, cwd=str(self.projeto))
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # --- documentos -------------------------------------------------------------------------------------
    @property
    def doc(self):
        return self.projeto / TEXTO["pasta_doc"]

    def pasta_conversa(self, codigo=CODIGO_B1, data="2026-03-14"):
        return self.doc / TEXTO["conversas"] / f"{data}-{codigo}"

    def d(self, n, codigo=CODIGO_B1, data="2026-03-14"):
        nome = TEXTO[f"d{n}"]
        if n in (2, 3, 7):
            return self.pasta_conversa(codigo, data) / nome
        return self.doc / nome

    def rodadas(self):
        caminho = self.dados / "rodadas.jsonl"
        if not caminho.exists():
            return []
        return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]

    def chamadas(self):
        """Chamadas recebidas pelo redator simulado, em ordem."""
        if not self.registro_simulado.exists():
            return []
        return [json.loads(p.read_text(encoding="utf-8"))
                for p in sorted(self.registro_simulado.glob("chamada-*.json"), key=lambda p: int(p.stem.split("-")[1]))]

    # --- respostas do redator ------------------------------------------------------------------------------
    def resposta(self, nome):
        """Caminho da resposta canônica, traduzida para o pacote em inglês quando preciso."""
        origem = CASOS / "redator" / f"{nome}.json"
        if IDIOMA == "pt-br":
            return origem
        texto = origem.read_text(encoding="utf-8")
        for pt, en in SITUACOES_PT_EN.items():
            texto = texto.replace(f'"situacao": "{pt}', f'"situacao": "{en}')
        texto = texto.replace("**Assunto: ", "**Subject: ")
        destino = self.respostas / f"{nome}.json"
        destino.write_text(texto, encoding="utf-8")
        return destino

    # --- execução -----------------------------------------------------------------------------------------
    def ambiente(self, respostas=(), escala="0.01", extra=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "HOPPER_DOCUMENTATION_ANTH"))}
        env.update({
            "CLAUDE_CONFIG_DIR": str(self.config),
            "TZ": "UTC",
            "HOPPER_DOCUMENTATION_ANTH_CLAUDE": str(SIMULADO),
            "HOPPER_DOCUMENTATION_ANTH_SIMULADO": ",".join(str(self.resposta(r)) for r in respostas),
            "HOPPER_DOCUMENTATION_ANTH_SIMULADO_REGISTRO": str(self.registro_simulado),
            "HOPPER_DOCUMENTATION_ANTH_ESCALA_DE_TEMPO": escala,
        })
        if extra:
            env.update(extra)
        return env

    def roda(self, *args, entrada=None, respostas=(), escala="0.01", extra=None, tempo=120):
        return subprocess.run([sys.executable, str(PROGRAMA), *args], input=entrada, capture_output=True,
                              text=True, env=self.ambiente(respostas, escala, extra), cwd=str(self.raiz), timeout=tempo)

    def rodada(self, sessao=SESSAO_B1, respostas=("rodada-b1",), **kw):
        return self.roda("rodada", "--sessao", sessao, respostas=respostas, **kw)

    def evento(self, sessao=SESSAO_B1, trigger="auto"):
        return json.dumps({"session_id": sessao, "transcript_path": str(self.historico(sessao)),
                           "cwd": str(self.projeto), "hook_event_name": "PreCompact", "trigger": trigger})

    def copia(self, sessao=SESSAO_B1, **kw):
        return self.roda("copia", entrada=self.evento(sessao), **kw)

    def escrita(self, sessao=SESSAO_B1, respostas=("rodada-b1",), **kw):
        return self.roda("escrita", entrada=self.evento(sessao), respostas=respostas, **kw)

    def migrar(self, pasta=None, respostas=("migracao-b3",), **kw):
        return self.roda("migrar", "--pasta", str(pasta or self.projeto), respostas=respostas, **kw)


def registros_de(caminho):
    return [json.loads(l) for l in Path(caminho).read_text(encoding="utf-8").splitlines() if l.strip()]


def corpo_do_documento_2(texto):
    """Devolve o corpo do documento 2, depois do cabeçalho (título, 3 linhas de rótulo e linha em branco)."""
    linhas = texto.split("\n")
    i = 0
    while i < len(linhas) and not linhas[i].startswith("## "):
        i += 1
    return "\n".join(linhas[i:])


def itens(texto):
    """Itens de um documento 4, 5 ou 6: lista de (id, texto, campos)."""
    saida = []
    atual = None
    for linha in texto.split("\n"):
        if linha.startswith("### "):
            atual = {"id": linha[4:].strip(), "texto": "", "campos": {}}
            saida.append(atual)
        elif atual is not None and linha.startswith("- ") and ":" in linha:
            chave, _, valor = linha[2:].partition(":")
            atual["campos"][chave.strip()] = valor.strip()
        elif atual is not None and linha.strip() and not atual["texto"] and not linha.startswith("-"):
            atual["texto"] = linha.strip()
    return saida


def blocos_do_documento_3(texto):
    return [l[3:].strip() for l in texto.split("\n") if l.startswith("## ")]


def ultima_linha(saida):
    linhas = [l for l in saida.strip().split("\n") if l.strip()]
    return linhas[-1] if linhas else ""


class CasoDeAceite(unittest.TestCase):
    def setUp(self):
        self.amb = Ambiente()
        self.addCleanup(self.amb.limpa)
