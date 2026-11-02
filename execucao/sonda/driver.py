#!/usr/bin/env python3
"""Conduz uma sessão interativa do Claude Code por pseudoterminal (U1, item 5).

Uso: driver.py --pasta DIR --marca ID [--pct N] [--modelo M] [--modo medir|compactar] [--fechar]
  medir      abre a sessão, responde ao diálogo de confiança, envia 1 mensagem e mede o contexto inicial.
  compactar  além disso, envia mensagens de enchimento até o gatilho de cópia da sonda registrar
             "sync-inicio"; com --fechar, mata o Claude Code 5 segundos depois (SIGHUP ao grupo).
Imprime 1 JSON na saída padrão com o resultado.
"""
import argparse
import fcntl
import json
import os
import pty
import re
import select
import signal
import struct
import sys
import termios
import threading
import time
from pathlib import Path

REGISTRO = Path.home() / "hopper-sonda" / "registro.jsonl"
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\x1b[()][A-Z0-9]|\r")


def agora():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z"


class Sessao:
    def __init__(self, pasta, marca, pct, modelo, claude):
        self.pasta = Path(pasta).expanduser()
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.marca = marca
        self.log = REGISTRO.parent / f"saida-{marca}.log"
        self.buffer = ""
        self.parou = False
        env = dict(os.environ)
        env.update({
            "TERM": "xterm-256color",
            "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "100000",
            "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": str(pct),
        })
        for chave in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PID", "CLAUDE_CODE_SESSION_ID"):
            env.pop(chave, None)
        pid, fd = pty.fork()
        if pid == 0:
            os.chdir(self.pasta)
            os.execvpe(claude, [claude, "--model", modelo], env)
        self.pid, self.fd = pid, fd
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 50, 200, 0, 0))
        threading.Thread(target=self._ler, daemon=True).start()

    def _ler(self):
        with self.log.open("ab") as lf:
            while not self.parou:
                r, _, _ = select.select([self.fd], [], [], 0.5)
                if not r:
                    continue
                try:
                    dados = os.read(self.fd, 65536)
                except OSError:
                    break
                if not dados:
                    break
                lf.write(dados)
                lf.flush()
                self.buffer = (self.buffer + ANSI.sub("", dados.decode("utf-8", "replace")))[-20000:]

    def espera_texto(self, padrao, segundos):
        fim = time.time() + segundos
        while time.time() < fim:
            if re.search(padrao, self.buffer, re.I):
                return True
            time.sleep(0.5)
        return False

    def tecla(self, texto):
        os.write(self.fd, texto.encode())

    def envia(self, mensagem):
        self.tecla(mensagem)
        time.sleep(1.0)
        self.tecla("\r")

    def vivo(self):
        try:
            return os.waitpid(self.pid, os.WNOHANG) == (0, 0)
        except ChildProcessError:
            return False

    def fecha(self):
        try:
            os.killpg(os.getpgid(self.pid), signal.SIGHUP)
        except ProcessLookupError:
            pass
        self.parou = True


def pasta_codificada(pasta):
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path(pasta).expanduser()))


def historico_mais_novo(pasta, depois_de):
    candidatos = [p for p in pasta_codificada(pasta).glob("*.jsonl") if p.stat().st_mtime >= depois_de - 5]
    return max(candidatos, key=lambda p: p.stat().st_mtime) if candidatos else None


def registros(caminho):
    saida = []
    with open(caminho, encoding="utf-8", errors="replace") as f:
        for linha in f:
            try:
                saida.append(json.loads(linha))
            except json.JSONDecodeError:
                pass
    return saida


def espera_resposta(caminho, n_usuario, segundos=240):
    """Espera o registro de resposta do Claude à n-ésima mensagem do usuário."""
    fim = time.time() + segundos
    tamanho_anterior, estavel_desde = -1, time.time()
    while time.time() < fim:
        if caminho and Path(caminho).exists():
            tamanho = Path(caminho).stat().st_size
            if tamanho != tamanho_anterior:
                tamanho_anterior, estavel_desde = tamanho, time.time()
            regs = registros(caminho)
            idx_usuarios = [i for i, r in enumerate(regs) if r.get("type") == "user" and not r.get("isCompactSummary")
                            and isinstance(r.get("message", {}).get("content"), str)]
            if len(idx_usuarios) >= n_usuario:
                depois = regs[idx_usuarios[n_usuario - 1] + 1:]
                if any(r.get("type") == "assistant" for r in depois) and time.time() - estavel_desde > 4:
                    return regs
        time.sleep(1)
    return registros(caminho) if caminho and Path(caminho).exists() else []


def contexto_inicial(regs):
    for r in regs:
        if r.get("type") == "assistant":
            uso = r.get("message", {}).get("usage") or {}
            return sum(uso.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return None


def linhas_da_sonda(session_id):
    if not REGISTRO.exists():
        return []
    return [json.loads(l) for l in REGISTRO.read_text(encoding="utf-8").splitlines() if session_id in l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", required=True)
    ap.add_argument("--marca", required=True)
    ap.add_argument("--pct", type=int, default=100)
    ap.add_argument("--modelo", default="haiku")
    ap.add_argument("--claude", default="claude")
    ap.add_argument("--modo", choices=["medir", "compactar"], default="medir")
    ap.add_argument("--fechar", action="store_true")
    ap.add_argument("--max-mensagens", type=int, default=12)
    args = ap.parse_args()

    resultado = {"marca": args.marca, "pasta": str(Path(args.pasta).expanduser()), "pct": args.pct,
                 "modelo": args.modelo, "modo": args.modo, "fechar": args.fechar, "eventos": []}
    inicio = time.time()
    s = Sessao(args.pasta, args.marca, args.pct, args.modelo, args.claude)
    resultado["eventos"].append({"hora": agora(), "evento": "claude iniciado", "pid": s.pid})

    if s.espera_texto(r"trust|confia", 25):
        time.sleep(1)
        s.tecla("\x1b[B")  # seta para baixo: a opção padrão é "No, exit"
        time.sleep(0.7)
        s.tecla("\r")
        resultado["eventos"].append({"hora": agora(), "evento": "diálogo de confiança respondido com seta para baixo e Enter"})
        time.sleep(3)
    s.espera_texto(r"\?\s*for shortcuts|shortcuts|bypass|Claude Code", 20)
    time.sleep(2)

    s.envia(f"SONDA-MARCA-{args.marca}: responda só com a palavra ok.")
    n = 1
    resultado["eventos"].append({"hora": agora(), "evento": "mensagem 1 enviada"})
    caminho = None
    for _ in range(60):
        caminho = historico_mais_novo(args.pasta, inicio)
        if caminho:
            break
        time.sleep(1)
    resultado["historico"] = str(caminho)
    regs = espera_resposta(caminho, n)
    resultado["session_id"] = regs[0].get("sessionId") if regs else None
    resultado["contexto_inicial_tokens"] = contexto_inicial(regs)
    resultado["eventos"].append({"hora": agora(), "evento": "resposta 1 recebida", "registros": len(regs)})

    if args.modo == "compactar":
        enchimento = "Escreva um texto corrido de 1500 palavras sobre a história do papel, sem listas e sem títulos."
        compactou = False
        while n < args.max_mensagens and not compactou:
            s.envia(enchimento if n % 2 == 1 else "Continue o texto com mais 1500 palavras, sem listas.")
            n += 1
            resultado["eventos"].append({"hora": agora(), "evento": f"mensagem {n} enviada"})
            fim = time.time() + 300
            while time.time() < fim:
                sonda = [l for l in linhas_da_sonda(resultado["session_id"] or "") if l["etapa"] == "sync-inicio"]
                if sonda:
                    compactou = True
                    resultado["eventos"].append({"hora": agora(), "evento": "sync-inicio visto na sonda", "sonda_hora": sonda[0]["hora"]})
                    break
                regs = registros(caminho)
                if regs and regs[-1].get("type") == "assistant" and len([r for r in regs if r.get("type") == "user" and isinstance(r.get("message", {}).get("content"), str) and not r.get("isCompactSummary")]) >= n:
                    time.sleep(5)
                    sonda = [l for l in linhas_da_sonda(resultado["session_id"] or "") if l["etapa"] == "sync-inicio"]
                    if sonda:
                        compactou = True
                        resultado["eventos"].append({"hora": agora(), "evento": "sync-inicio visto na sonda", "sonda_hora": sonda[0]["hora"]})
                    break
                time.sleep(2)
        resultado["mensagens_enviadas"] = n
        resultado["compactou"] = compactou
        if compactou and args.fechar:
            time.sleep(5)
            s.fecha()
            resultado["eventos"].append({"hora": agora(), "evento": "SIGHUP enviado ao grupo do Claude Code, 5 s depois do sync-inicio"})
            time.sleep(3)
            resultado["claude_vivo_apos_fechar"] = s.vivo()
        else:
            # espera o fim da rodada da sonda com a sessão aberta
            time.sleep(10)
        fim = time.time() + 150
        while time.time() < fim:
            if any(l["etapa"] == "separado-fim" for l in linhas_da_sonda(resultado["session_id"] or "")):
                break
            time.sleep(3)
        resultado["sonda"] = linhas_da_sonda(resultado["session_id"] or "")
        regs = registros(caminho)
        resultado["historico_final"] = {"linhas": len(regs), "marca_presente": any("SONDA-MARCA" in json.dumps(r) for r in regs),
                                        "resumos_de_compactacao": sum(1 for r in regs if r.get("isCompactSummary"))}
    if s.vivo():
        s.fecha()
    resultado["eventos"].append({"hora": agora(), "evento": "fim"})
    print(json.dumps(resultado, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
