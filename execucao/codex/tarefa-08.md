# Tarefa 08 para o Codex: nova tentativa também para origem fora do trecho novo

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`).

Evidência: `execucao/verificacoes.md`, V-U8-05, e `execucao/codex/tarefa-07-relatorio.md`. Na 2ª passagem de F-K em A3, a rodada falhou com "origem inválida: M17-958e55b3". M17 existe, mas é do trecho anterior; o Anexo D exige que a origem de um item novo e de uma mudança seja mensagem do trecho novo ou item existente.

## Decisão do verificador

1. A nova tentativa da tarefa 05 passa a valer para todas as falhas da conferência própria do programa que o redator consegue corrigir: referências inexistentes, origem fora do trecho novo, situação não permitida e linha de assunto ausente. A falha de esquema JSON, de modelo (C04) e de tempo continuam sem nova tentativa. A linha acrescentada à entrada lista os problemas encontrados, por exemplo: "Problemas na resposta anterior: origem fora do trecho novo (M17-958e55b3); a origem de um item novo ou de uma mudança é uma mensagem de M18-958e55b3 a M19-958e55b3 ou um item existente." Tradução fiel no pacote em inglês.
2. Em `modelos.md` e `templates.md`, acrescente que a origem de um item novo ou de uma mudança é uma mensagem do trecho novo ou um item existente, nunca uma mensagem de um trecho anterior.
3. Testes do executor, que falham sem a correção: origem fora do trecho com 2ª resposta válida conclui com 2 chamadas; origem fora do trecho 2 vezes falha a rodada.

Verificação com os 3 comandos da tarefa 01 (42 de 42 no aceite). Relatório em `execucao/codex/tarefa-08-relatorio.md`.
