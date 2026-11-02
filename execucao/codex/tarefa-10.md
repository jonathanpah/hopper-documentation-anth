# Tarefa 10 para o Codex: a skill sempre roda o programa (R25)

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`).

Evidência: `execucao/verificacoes.md`, V-U8-07. No caso de avaliação de pedido explícito de registro, o modelo às vezes aciona a skill mas não chama o Bash, e às vezes o relato da linha final reprova no juiz.

## O que fazer (decisão do verificador)

1. Nos 2 SKILL.md, acrescente ao cabeçalho `allowed-tools: Bash(python3 *)`, para que o comando da skill rode sem pedido de permissão no turno que a aciona (fonte: `code.claude.com/docs/en/skills.md`, campo `allowed-tools`). Não mude o `name` nem a `description` (texto fixo do Anexo E).
2. Reescreva os passos de "Como a skill roda" de forma mais direta: o 1º passo é rodar o comando agora, na mesma resposta, com a ferramenta Bash em segundo plano; o 2º é dizer em 1 frase que a documentação começou; o 3º é, quando o programa terminar, repetir a última linha dele sem mudar o texto. Tradução fiel no inglês.
3. Confira T41 e `claude plugin validate --strict` nos 2 pacotes (se o `validate` não rodar no seu isolamento, diga no relatório).

Verificação com os 3 comandos da tarefa 01. Relatório em `execucao/codex/tarefa-10-relatorio.md`.
