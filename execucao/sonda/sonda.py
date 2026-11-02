#!/usr/bin/env python3
"""Plugin de sonda de U1: registra o comportamento do evento PreCompact.

Modos:
  sync      gatilho síncrono: grava início e fim, espera 3 segundos.
  async     gatilho assíncrono: cria o processo separado logo no início e espera por ele.
  separado  processo separado: espera 120 segundos e grava a hora.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REGISTRO = Path.home() / "hopper-sonda" / "registro.jsonl"


def agora():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def executavel_de(pid):
    if not pid:
        return ""
    try:
        if sys.platform.startswith("linux"):
            return os.readlink(f"/proc/{pid}/exe")
        saida = subprocess.run(["ps", "-o", "comm=", "-p", str(pid)], capture_output=True, text=True, timeout=5)
        return saida.stdout.strip()
    except Exception as erro:  # noqa: BLE001
        return f"erro: {erro}"


def estado_do_historico(caminho):
    estado = {"linhas": 0, "marca_presente": False, "resumos_de_compactacao": 0, "tamanho": 0}
    try:
        arquivo = Path(caminho)
        estado["tamanho"] = arquivo.stat().st_size
        with arquivo.open(encoding="utf-8", errors="replace") as f:
            for linha in f:
                estado["linhas"] += 1
                if "SONDA-MARCA" in linha:
                    estado["marca_presente"] = True
                if '"isCompactSummary":true' in linha:
                    estado["resumos_de_compactacao"] += 1
    except Exception as erro:  # noqa: BLE001
        estado["erro"] = str(erro)
    return estado


def grava(etapa, entrada, extra=None):
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    pid_claude = os.environ.get("CLAUDE_PID")
    linha = {
        "hora": agora(),
        "etapa": etapa,
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "session_id": entrada.get("session_id"),
        "transcript_path": entrada.get("transcript_path"),
        "cwd": entrada.get("cwd"),
        "trigger": entrada.get("trigger"),
        "hook_event_name": entrada.get("hook_event_name"),
        "claude_pid": pid_claude,
        "executavel": executavel_de(pid_claude),
        "plugin_data": os.environ.get("CLAUDE_PLUGIN_DATA"),
        "plugin_root": os.environ.get("CLAUDE_PLUGIN_ROOT"),
        "historico": estado_do_historico(entrada.get("transcript_path") or ""),
    }
    if extra:
        linha.update(extra)
    with REGISTRO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo == "separado":
        entrada = json.loads(sys.argv[2])
        grava("separado-inicio", entrada)
        time.sleep(120)
        grava("separado-fim", entrada)
        (REGISTRO.parent / f"fim-{entrada.get('session_id', 'sem-id')}.marca").write_text(agora())
        return 0
    bruto = sys.stdin.read()
    try:
        entrada = json.loads(bruto)
    except Exception:  # noqa: BLE001
        entrada = {"bruto": bruto[:500]}
    if modo == "sync":
        grava("sync-inicio", entrada, {"chaves_da_entrada": sorted(entrada.keys())})
        time.sleep(3)
        grava("sync-fim", entrada)
        return 0
    if modo == "async":
        # Versão 2 da sonda: fork duplo com setsid, para que o processo separado
        # fique com o init como pai e fora da árvore de processos do gatilho.
        # A versão 1 usava Popen(start_new_session=True) e esperava o filho; o
        # processo morreu junto com o Claude Code no teste a3-c2 (V-U1-05).
        grava("async-inicio", entrada)
        sessao = entrada.get("session_id", "sem-id")
        log = REGISTRO.parent / f"separado-{sessao}.log"
        marcador = REGISTRO.parent / f"fim-{sessao}.marca"
        pid = os.fork()
        if pid == 0:
            os.setsid()
            if os.fork() == 0:
                fd = os.open(str(log), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
                nulo = os.open(os.devnull, os.O_RDONLY)
                os.dup2(nulo, 0)
                os.dup2(fd, 1)
                os.dup2(fd, 2)
                os.chdir(str(REGISTRO.parent))
                os.execv(sys.executable, [sys.executable, os.path.abspath(__file__), "separado", json.dumps(entrada)])
            os._exit(0)
        os.waitpid(pid, 0)
        grava("async-separado-criado", entrada, {"modo_de_criacao": "fork duplo + setsid, pai = init"})
        fim = time.time() + 3000
        while time.time() < fim and not marcador.exists():
            time.sleep(2)
        grava("async-fim", entrada, {"marcador_encontrado": marcador.exists()})
        return 0
    sys.stderr.write("modo desconhecido\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
