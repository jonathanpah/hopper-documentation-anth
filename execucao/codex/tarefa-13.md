# Tarefa 13 para o Codex: desfazer a nova tentativa de C04 (item 4 da tarefa 12)

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`, `SPEC.md`, `.github/` nem nos `evals/`).

O teste congelado T12 (`aceite/testes/test_redator.py`, linhas 105 a 119) exige que a resposta de outro modelo faça a rodada falhar sem nova chamada na mesma rodada. Os critérios congelados prevalecem sobre a tarefa 12.

## O que fazer (decisão do verificador)

1. Desfaça só o item 4 da tarefa 12: a falha da regra de modelo volta a encerrar a chamada sem nova tentativa, como no commit `62d2746`. Remova a classe `ModeloInvalido` se ela deixar de ter uso, e o teste do executor da nova tentativa de modelo.
2. Mantenha os itens 1, 2, 3, 5 e 6 restantes da tarefa 12.
3. Gere o programa en pelo `sed` de sempre e confira com `diff`.

Verificação com os 3 comandos da tarefa 01: o aceite deve passar em 41 de 42 por pacote no seu isolamento (só T38, pelo `ps`). Acrescente o resultado ao fim de `execucao/codex/tarefa-12-relatorio.md`, em uma seção "Tarefa 13".
