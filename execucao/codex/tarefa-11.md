# Tarefa 11 para o Codex: a rodada sempre imprime a linha final (R25)

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`, `SPEC.md`, `.github/` nem nos `evals/`).

## Evidência

Avaliação `registra-pedido`, rodada com `--allow-tools 'Bash(python3 *)'`. No isolamento da avaliação, a pasta `config/plugins` não aceita escrita. O comando `rodada` caiu assim:

1. `rodada()` chama `Trava(...)`, que chama `pasta_de_dados()`; o `mkdir` levanta `PermissionError`.
2. O `except Exception` de `main()` (ramo `rodada`) chama `registrar_escrita(...)`, que chama `pasta_de_dados()` de novo e levanta outra vez, agora dentro do `except`.
3. Resultado: traceback, código 1 e nenhuma linha `Documentação falhou: …`. O juiz da avaliação reprova porque não existe linha final para repassar.

## O que fazer (decisão do verificador)

1. No ramo `rodada` de `main()`, garanta a linha final em qualquer falha: se `registrar_escrita` ou a gravação do marcador falharem, siga em frente e imprima a linha `linha_falhou` com o motivo do erro original. A linha vai para a saída padrão como a última linha, e também para a saída de erro, como hoje. Mudança mínima; não mude os textos de `T`.
2. Acrescente 1 teste em `tests/test_hopper_documentation_anth.py` de cada pacote: com `CLAUDE_CONFIG_DIR` apontando para uma pasta sem permissão de escrita, `rodada --sessao <id>` termina com código 1, a última linha da saída padrão começa com `Documentação falhou:` (en: `Documentation failed:`) e a saída de erro não contém `Traceback`.
3. Gere o programa en a partir do pt-br pelo `sed` de sempre e confira com `diff` que só a linha `LANGUAGE` muda.
4. No `CONTRIBUTING.md` da raiz, onde descreve os testes, acrescente 1 frase: as avaliações rodam com `claude plugin eval ./<pacote> --ablation none --trust-plugin --model sonnet --allow-tools 'Bash(python3 *)'`, porque a skill roda o programa pelo Bash e a avaliação só libera o Bash com `--allow-tools`.

Verificação com os 3 comandos da tarefa 01. Relatório em `execucao/codex/tarefa-11-relatorio.md`.
