#!/usr/bin/env python3
"""Conferidor de uma pasta de documentação (Anexo F da spec). Critério congelado da U2.

Uso: python3 aceite/conferir.py <pasta de documentação> --idioma pt-br|en [--roteiro aceite/roteiro.json]

Imprime o total de verificações rodadas, aprovadas e reprovadas e sai com código 0 só se todas as que rodaram
passarem. Uma verificação que não encontra o objeto que deve conferir reprova. Sem `--roteiro`, F9 aparece como
"não se aplica" e fica fora do total.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TEXTOS = {
    "pt-br": {
        "conversas": "conversas", "d1": "1-indice.md", "d2": "2-conversa-integral.md", "d3": "3-conversa-simplificada.md",
        "d4": "4-decisoes.md", "d5": "5-funcoes.md", "d6": "6-pendencias.md", "d7": "7-handoff.md",
        "origem": "Origem", "situacao": "Situação", "intervalo": "Intervalo da rodada",
        "ultima_coberta": "Última mensagem coberta", "sem_integral": "sem conversa integral",
        "assunto": "**Assunto: ", "autores": ["Usuário", "Claude", "Resposta do usuário", "Plano aprovado", "Relato de agente", "Evento"],
        "situacoes": {"d4": ["vigente", "substituída por ", "revogada em "], "d5": ["concluída", "substituída por ", "desfeita em "],
                      "d6": ["aberta", "encerrada em "]},
        "substituida": "substituída por ", "ferramenta": "Ferramenta: ", "oculto": "[oculto]",
        "secoes_d7": ["Objetivo", "Pautas e estado atual", "Próximo passo", "Decisões e autorizações vigentes",
                      "Restrições vigentes", "Descobertas e tentativas descartadas", "Pendências e compromissos", "Lacunas", "Como retomar"],
        "nao_se_aplica": "não se aplica",
    },
    "en": {
        "conversas": "conversations", "d1": "1-index.md", "d2": "2-full-conversation.md", "d3": "3-simplified-conversation.md",
        "d4": "4-decisions.md", "d5": "5-functions.md", "d6": "6-pending.md", "d7": "7-handoff.md",
        "origem": "Source", "situacao": "Status", "intervalo": "Run range",
        "ultima_coberta": "Last covered message", "sem_integral": "no full conversation",
        "assunto": "**Subject: ", "autores": ["User", "Claude", "User answer", "Approved plan", "Agent report", "Event"],
        "situacoes": {"d4": ["in force", "replaced by ", "revoked in "], "d5": ["done", "replaced by ", "undone in "],
                      "d6": ["open", "closed in "]},
        "substituida": "replaced by ", "ferramenta": "Tool: ", "oculto": "[hidden]",
        "secoes_d7": ["Goal", "Topics and current state", "Next step", "Decisions and authorizations in force",
                      "Constraints in force", "Findings and discarded approaches", "Pending items and commitments", "Gaps", "How to resume"],
        "nao_se_aplica": "not applicable",
    },
}
RE_MENSAGEM = re.compile(r"^## (M(\d+)-([A-Za-z0-9-]+)) · (\d{4}-\d{2}-\d{2} \d{2}:\d{2} [+-]\d{2}:\d{2}) · (.+)$")
RE_BLOCO = re.compile(r"^## M(\d+)-([A-Za-z0-9-]+) a M(\d+)-([A-Za-z0-9-]+)$")
RE_ORIGEM_FINAL = re.compile(r"\((M\d+-[A-Za-z0-9-]+(?: a M\d+-[A-Za-z0-9-]+)?(?:, M\d+-[A-Za-z0-9-]+(?: a M\d+-[A-Za-z0-9-]+)?)*)\)$")
RE_ID_MENSAGEM = re.compile(r"\bM(\d+)-([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\b")
RE_ID_ITEM = re.compile(r"\b((?:D|F|PD)\d+-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\b")
RE_ITEM = re.compile(r"^### ((?:D|F|PD)(\d+)-([A-Za-z0-9-]+))$")


def le(caminho):
    return Path(caminho).read_text(encoding="utf-8")


class Conferencia:
    def __init__(self, pasta, idioma, roteiro):
        self.pasta = Path(pasta)
        self.t = TEXTOS[idioma]
        self.idioma = idioma
        self.roteiro = json.loads(le(roteiro)) if roteiro else None
        self.resultados = {}
        self.falhas = {}

    def falha(self, f, mensagem):
        self.falhas.setdefault(f, []).append(mensagem)

    # --- apoio -----------------------------------------------------------------------------------------------
    def pastas_de_conversa(self):
        base = self.pasta / self.t["conversas"]
        return sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []

    def migrada(self, pasta):
        d7 = pasta / self.t["d7"]
        return d7.exists() and f"- {self.t['ultima_coberta']}: {self.t['sem_integral']}" in le(d7)

    def mensagens(self, pasta):
        """Lista de (n, codigo, autor, corpo, registros) do documento 2 de uma pasta de conversa."""
        d2 = pasta / self.t["d2"]
        if not d2.exists():
            return []
        # Reconhece a linha completa independentemente do comentário, para F2 detectar a ausência dele.
        linhas = le(d2).split("\n")
        inicios = [i for i, linha in enumerate(linhas) if RE_MENSAGEM.fullmatch(linha)]
        primeiro = next((i for i, linha in enumerate(linhas) if linha.startswith("## ")), None)
        if primeiro is not None and primeiro not in inicios:
            inicios.insert(0, primeiro)
        saida = []
        for k, i in enumerate(inicios):
            fim = inicios[k + 1] if k + 1 < len(inicios) else len(linhas)
            m = RE_MENSAGEM.match(linhas[i])
            registros = linhas[i + 1] if i + 1 < len(linhas) else ""
            corpo = "\n".join(linhas[i + 2:fim]).strip("\n")
            saida.append((int(m.group(2)) if m else None, m.group(3) if m else None, m.group(5) if m else linhas[i], corpo, registros, linhas[i]))
        return saida

    def ids_de_mensagens(self):
        ids = set()
        for pasta in self.pastas_de_conversa():
            for n, codigo, *_ in self.mensagens(pasta):
                if n is not None:
                    ids.add(f"M{n}-{codigo}")
        return ids

    def itens(self, nome):
        caminho = self.pasta / self.t[nome]
        if not caminho.exists():
            return []
        saida, atual = [], None
        for linha in le(caminho).split("\n"):
            m = RE_ITEM.match(linha)
            if m:
                atual = {"id": m.group(1), "texto": "", "campos": {}}
                saida.append(atual)
            elif atual is not None and linha.startswith("- ") and ":" in linha:
                chave, _, valor = linha[2:].partition(":")
                atual["campos"][chave.strip()] = valor.strip()
            elif atual is not None and linha.strip() and not atual["texto"] and not linha.startswith("-"):
                atual["texto"] = linha.strip()
        return saida

    def ids_de_itens(self):
        return {i["id"] for nome in ("d4", "d5", "d6") for i in self.itens(nome)}

    # --- verificações ----------------------------------------------------------------------------------------
    def f1(self):
        for nome in ("d1", "d4", "d5", "d6"):
            if not (self.pasta / self.t[nome]).exists():
                self.falha("F1", f"falta {self.t[nome]}")
        if not (self.pasta / self.t["conversas"]).is_dir():
            self.falha("F1", f"falta a pasta {self.t['conversas']}/")
        for pasta in self.pastas_de_conversa():
            if not (pasta / self.t["d7"]).exists():
                self.falha("F1", f"falta {pasta.name}/{self.t['d7']}")
            elif not self.migrada(pasta):
                for nome in ("d2", "d3"):
                    if not (pasta / self.t[nome]).exists():
                        self.falha("F1", f"falta {pasta.name}/{self.t[nome]}")

    def f2(self):
        objeto = False
        for pasta in self.pastas_de_conversa():
            if self.migrada(pasta):
                continue
            objeto = True
            vistos = set()
            esperado = 1
            for n, codigo, autor, corpo, registros, cabecalho in self.mensagens(pasta):
                if n is None:
                    self.falha("F2", f"{pasta.name}: cabeçalho fora do formato: {cabecalho}")
                    continue
                if n != esperado:
                    self.falha("F2", f"{pasta.name}: esperado M{esperado}, veio M{n}")
                esperado = n + 1
                if autor not in self.t["autores"]:
                    self.falha("F2", f"{pasta.name}: autor desconhecido em M{n}: {autor}")
                m = re.match(r"^<!-- registros: (\S+) (\S+) -->$", registros)
                if not m:
                    self.falha("F2", f"{pasta.name}: M{n} sem o comentário de registros")
                    continue
                for r in set(m.groups()):
                    if r in vistos:
                        self.falha("F2", f"{pasta.name}: registro {r} aparece em 2 mensagens")
                    vistos.add(r)
        if not objeto:
            self.falha("F2", "nenhuma conversa com documento 2")

    def f3(self):
        objeto = False
        for pasta in self.pastas_de_conversa():
            d3 = pasta / self.t["d3"]
            if not d3.exists():
                continue
            objeto = True
            esperado = 1
            partes = le(d3).split("\n## ")[1:]
            if not partes:
                self.falha("F3", f"{pasta.name}: documento 3 sem blocos")
            for parte in partes:
                linhas = ("## " + parte).split("\n")
                m = RE_BLOCO.match(linhas[0])
                if not m:
                    self.falha("F3", f"{pasta.name}: bloco fora do formato: {linhas[0]}")
                    continue
                a, b = int(m.group(1)), int(m.group(3))
                if a != esperado or b < a:
                    self.falha("F3", f"{pasta.name}: bloco {linhas[0]} não segue M{esperado}")
                esperado = b + 1
                paragrafos = [p.strip() for p in "\n".join(linhas[1:]).split("\n\n") if p.strip()]
                if not paragrafos or not paragrafos[0].startswith(self.t["assunto"]):
                    self.falha("F3", f"{pasta.name}: bloco {linhas[0]} sem a linha de assunto")
                for p in paragrafos[1:]:
                    if not RE_ORIGEM_FINAL.search(p.replace("\n", " ")):
                        self.falha("F3", f"{pasta.name}: parágrafo sem origem no bloco {linhas[0]}: {p[:60]}")
        if not objeto:
            self.falha("F3", "nenhum documento 3")

    def f4(self):
        ids = set()
        for nome in ("d4", "d5", "d6"):
            if not (self.pasta / self.t[nome]).exists():
                self.falha("F4", f"falta {self.t[nome]}")
                continue
            for item in self.itens(nome):
                if item["id"] in ids:
                    self.falha("F4", f"identificador repetido: {item['id']}")
                ids.add(item["id"])
                if not item["texto"]:
                    self.falha("F4", f"{item['id']} sem texto")
                for campo in (self.t["origem"], self.t["situacao"], self.t["intervalo"]):
                    if not item["campos"].get(campo):
                        self.falha("F4", f"{item['id']} sem o campo {campo}")
                situacao = item["campos"].get(self.t["situacao"], "")
                permitidas = self.t["situacoes"][nome]
                if not any(situacao == s or (s.endswith(" ") and situacao.startswith(s)) for s in permitidas):
                    self.falha("F4", f"{item['id']} com situação não permitida: {situacao}")
        for nome in ("d4", "d5", "d6"):
            for item in self.itens(nome):
                situacao = item["campos"].get(self.t["situacao"], "")
                if situacao.startswith(self.t["substituida"]):
                    alvo = situacao[len(self.t["substituida"]):].strip()
                    if alvo not in ids:
                        self.falha("F4", f"{item['id']} substituído por item inexistente: {alvo}")

    def f5(self):
        objeto = False
        for pasta in self.pastas_de_conversa():
            d7 = pasta / self.t["d7"]
            if not d7.exists():
                continue
            objeto = True
            secoes = [l[3:].strip() for l in le(d7).split("\n") if l.startswith("## ")]
            obrigatorias = [titulo for titulo in secoes if titulo in self.t["secoes_d7"]]
            if obrigatorias != self.t["secoes_d7"]:
                self.falha("F5", f"{pasta.name}: seções do documento 7: {secoes}")
        if not objeto:
            self.falha("F5", "nenhum documento 7")

    def f6(self):
        d1 = self.pasta / self.t["d1"]
        if not d1.exists():
            self.falha("F6", "falta o documento 1")
            return
        texto = le(d1)
        for alvo in re.findall(r"\]\(([^)]+)\)", texto):
            if alvo.startswith(("http://", "https://")):
                continue
            if not (self.pasta / alvo).exists():
                self.falha("F6", f"link quebrado: {alvo}")
        for pasta in self.pastas_de_conversa():
            if f"({self.t['conversas']}/{pasta.name}/)" not in texto:
                self.falha("F6", f"conversa fora do índice: {pasta.name}")

    def f7(self):
        objeto = False
        frases_total, longas = 0, 0
        for caminho in self.documentos_3_a_7():
            objeto = True
            for paragrafo in self.paragrafos_contaveis(le(caminho)):
                frases = [f for f in re.split(r"(?<=[.!?])\s+", paragrafo) if f.strip()]
                if len(frases) > 6:
                    self.falha("F7", f"{caminho.name}: parágrafo com {len(frases)} frases")
                for f in frases:
                    palavras = len(f.split())
                    frases_total += 1
                    if palavras > 25:
                        longas += 1
                    if palavras > 40:
                        self.falha("F7", f"{caminho.name}: frase com {palavras} palavras")
        if frases_total and longas / frases_total > 0.10:
            self.falha("F7", f"{longas} de {frases_total} frases passam de 25 palavras nos documentos 3 a 7")
        if not objeto:
            self.falha("F7", "nenhum documento 3 a 7")

    def documentos_3_a_7(self):
        saida = [self.pasta / self.t[n] for n in ("d4", "d5", "d6") if (self.pasta / self.t[n]).exists()]
        for pasta in self.pastas_de_conversa():
            saida += [pasta / self.t[n] for n in ("d3", "d7") if (pasta / self.t[n]).exists()]
        return saida

    def paragrafos_contaveis(self, texto):
        rotulos = ({"Conversa", "Pasta do projeto", "Fuso dos horários", "Origem", "Situação", "Intervalo da rodada",
                    "Recomendação", "Depende de", "Última mensagem coberta", "Data da rodada", "Redator"}
                   if self.idioma == "pt-br" else
                   {"Conversation", "Project folder", "Time zone", "Source", "Status", "Run range", "Recommendation",
                    "Depends on", "Last covered message", "Run date", "Writer"})
        metadado = re.compile(r"^- (?:" + "|".join(re.escape(r) for r in rotulos) + r"): ")
        dentro_codigo = False
        paragrafos, atual = [], []
        for linha in texto.split("\n"):
            if linha.startswith("```"):
                dentro_codigo = not dentro_codigo
                continue
            if dentro_codigo or linha.startswith("#") or linha.startswith(self.t["assunto"]) or metadado.match(linha) \
                    or linha.startswith("|") or linha.startswith("<!--"):
                continue
            if not linha.strip():
                if atual:
                    paragrafos.append(" ".join(atual))
                    atual = []
                continue
            limpa = RE_ID_MENSAGEM.sub("", RE_ID_ITEM.sub("", linha))
            limpa = re.sub(r"\((?:\s*a\s*|,\s*)*\)", "", limpa)
            atual.append(limpa.strip())
        if atual:
            paragrafos.append(" ".join(atual))
        return paragrafos

    def f8(self):
        mensagens = self.ids_de_mensagens()
        itens = self.ids_de_itens()
        objeto = False
        for caminho in self.documentos_3_a_7():
            objeto = True
            texto = le(caminho)
            for n, codigo in set(RE_ID_MENSAGEM.findall(texto)):
                if f"M{n}-{codigo}" not in mensagens:
                    self.falha("F8", f"{caminho.name}: mensagem inexistente M{n}-{codigo}")
            for item in set(RE_ID_ITEM.findall(texto)):
                if item not in itens:
                    self.falha("F8", f"{caminho.name}: item inexistente {item}")
        if not objeto:
            self.falha("F8", "nenhum documento 3 a 7")

    def f9(self):
        r = self.roteiro
        fixos = r["textos_fixos"][self.idioma]
        # No documento 2, a senha da mensagem 2 aparece oculta; o roteiro guarda o texto como gravado.
        textos = [t.replace("{oculto}", fixos["oculto"]) for t in r.get("mensagens_no_documento_2", r["mensagens"])]
        localizadas = {}
        for pasta in self.pastas_de_conversa():
            msgs = self.mensagens(pasta)
            for i, texto in enumerate(textos, 1):
                for pos, (n, codigo, autor, corpo, *_r) in enumerate(msgs):
                    if n is not None and autor == self.t["autores"][0] and texto in corpo:
                        localizadas.setdefault(i, (pasta, f"M{n}-{codigo}", pos))
        faltam = [i for i in range(1, len(textos) + 1) if i not in localizadas]
        if faltam:
            self.falha("F9", f"mensagens do roteiro não encontradas no documento 2: {faltam}")
            return
        pasta = localizadas[1][0]
        d2 = le(pasta / self.t["d2"])
        a = r["assercoes"]["documento_2"]
        for s in a["contem"]:
            if s not in d2:
                self.falha("F9", f"documento 2 sem {s!r}")
        if a.get("contem_oculto") and fixos["oculto"] not in d2:
            self.falha("F9", f"documento 2 sem {fixos['oculto']}")
        for s in a["nao_contem"]:
            if s in d2:
                self.falha("F9", f"documento 2 contém {s!r}")
        lf = a["linha_de_ferramenta"]
        linhas = [l for l in d2.split("\n") if l.startswith(fixos["ferramenta"] + lf["comeca_com"]) and l.rstrip().endswith(lf["termina_com"])]
        if not linhas:
            self.falha("F9", f"documento 2 sem a linha {fixos['ferramenta']}{lf['comeca_com']} … {lf['termina_com']}")
        for nome, chave in (("d4", "documento_4"), ("d6", "documento_6"), ("d5", "documento_5")):
            regra = r["assercoes"][chave]
            origens = {localizadas[regra["origem_na_mensagem"]][1]}
            if "ou_na_mensagem_do_claude_com_a_ferramenta" in regra:
                msgs = self.mensagens(pasta)
                pos = localizadas[regra["origem_na_mensagem"]][2]
                for n, codigo, autor, corpo, *_r in msgs[pos + 1:]:
                    if autor == self.t["autores"][1] and (fixos["ferramenta"] + regra["ou_na_mensagem_do_claude_com_a_ferramenta"]) in corpo:
                        origens.add(f"M{n}-{codigo}")
                        break
            encontrado = any(i["id"].startswith(regra["tipo"]) and not i["id"].startswith("PD" if regra["tipo"] == "D" else "\0")
                             and any(o in i["campos"].get(self.t["origem"], "") for o in origens) for i in self.itens(nome))
            if regra["tipo"] == "D":
                encontrado = any(re.match(r"^D\d+-", i["id"]) and any(o in i["campos"].get(self.t["origem"], "") for o in origens) for i in self.itens(nome))
            if not encontrado:
                self.falha("F9", f"{self.t[nome]} sem item {regra['tipo']} com origem em {sorted(origens)}")

    def f10(self):
        for p in self.pasta.iterdir():
            if p.is_file() and (p.name == "index.md" or (p.name.startswith("handoff-") and p.suffix == ".md")):
                self.falha("F10", f"arquivo do formato antigo na raiz: {p.name}")

    # --- execução ---------------------------------------------------------------------------------------------
    def roda(self):
        verificacoes = [("F1", self.f1), ("F2", self.f2), ("F3", self.f3), ("F4", self.f4), ("F5", self.f5), ("F6", self.f6),
                        ("F7", self.f7), ("F8", self.f8), ("F9", self.f9), ("F10", self.f10)]
        for nome, funcao in verificacoes:
            if nome == "F9" and not self.roteiro:
                self.resultados[nome] = self.t["nao_se_aplica"]
                continue
            try:
                funcao()
            except Exception as erro:  # noqa: BLE001
                self.falha(nome, f"erro na verificação: {erro!r}")
            self.resultados[nome] = "reprovada" if nome in self.falhas else "aprovada"
        rodadas = [n for n, r in self.resultados.items() if r != self.t["nao_se_aplica"]]
        aprovadas = [n for n in rodadas if self.resultados[n] == "aprovada"]
        reprovadas = [n for n in rodadas if self.resultados[n] == "reprovada"]
        for nome in verificacoes:
            n = nome[0]
            print(f"{n}: {self.resultados[n]}")
            for mensagem in self.falhas.get(n, []):
                print(f"  - {mensagem}")
        print(f"verificações rodadas: {len(rodadas)}, aprovadas: {len(aprovadas)}, reprovadas: {len(reprovadas)}")
        return 0 if not reprovadas else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--idioma", choices=["pt-br", "en"], required=True)
    ap.add_argument("--roteiro")
    args = ap.parse_args()
    if not Path(args.pasta).is_dir():
        print(f"pasta inexistente: {args.pasta}")
        return 2
    return Conferencia(args.pasta, args.idioma, args.roteiro).roda()


if __name__ == "__main__":
    sys.exit(main())
