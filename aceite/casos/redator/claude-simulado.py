#!/usr/bin/env python3
"""Redator simulado para os testes de aceite (Anexo B, B4; decisão D-09).

Imita o `claude -p --output-format json`: grava os argumentos, as variáveis de ambiente relevantes,
a pasta atual e a entrada padrão recebidos em `$HOPPER_DOCUMENTATION_ANTH_SIMULADO_REGISTRO/chamada-<n>.json`
e devolve a resposta canônica indicada por `$HOPPER_DOCUMENTATION_ANTH_SIMULADO` (1 arquivo, ou vários separados
por vírgula, consumidos em ordem; o último repete).

Campos aceitos no arquivo de resposta:
  structured_output   objeto devolvido como `structured_output` e, em texto, como `result`
  resultado_texto     texto devolvido como `result` quando não existe `structured_output`
  modelUsage          objeto `modelUsage`; padrão: só `claude-sonnet-5-5`
  is_error            padrão false
  espera_segundos     espera antes de responder (padrão 0)
  codigo_de_saida     código de saída do processo (padrão 0)
"""
import json
import os
import sys
import time
from pathlib import Path

registro = Path(os.environ.get("HOPPER_DOCUMENTATION_ANTH_SIMULADO_REGISTRO", "."))
registro.mkdir(parents=True, exist_ok=True)
contador = registro / "contador"
n = int(contador.read_text()) + 1 if contador.exists() else 1
contador.write_text(str(n))

entrada = sys.stdin.read()
(registro / f"chamada-{n}.json").write_text(json.dumps({
    "argv": sys.argv[1:],
    "env": {k: v for k, v in os.environ.items() if k.startswith(("CLAUDE", "HOPPER_DOCUMENTATION_ANTH", "ANTHROPIC"))},
    "cwd": os.getcwd(),
    "stdin": entrada,
}, ensure_ascii=False, indent=1), encoding="utf-8")

arquivos = [a for a in os.environ.get("HOPPER_DOCUMENTATION_ANTH_SIMULADO", "").split(",") if a]
resposta = {}
if arquivos:
    resposta = json.loads(Path(arquivos[min(n, len(arquivos)) - 1]).read_text(encoding="utf-8"))

time.sleep(float(resposta.get("espera_segundos", 0)))
envelope = {
    "type": "result",
    "subtype": "success",
    "is_error": bool(resposta.get("is_error", False)),
    "duration_ms": 1,
    "num_turns": 1,
    "session_id": "simulado",
    "total_cost_usd": 0,
    "modelUsage": resposta.get("modelUsage", {"claude-sonnet-5-5": {"inputTokens": 10, "outputTokens": 100}}),
}
if "structured_output" in resposta:
    envelope["structured_output"] = resposta["structured_output"]
    envelope["result"] = json.dumps(resposta["structured_output"], ensure_ascii=False)
else:
    envelope["result"] = resposta.get("resultado_texto", "")
print(json.dumps(envelope, ensure_ascii=False))
sys.exit(int(resposta.get("codigo_de_saida", 0)))
