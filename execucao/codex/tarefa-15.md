# Tarefa 15 para o Codex: migração de pasta grande em partes (U9)

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`, `SPEC.md`, `.github/` nem nos `evals/`).

## Evidência

Migração real de `/home/jpah/projects/mallmetrics` (`index.md` e 79 handoffs de 18 conversas, 1,2 MB), programa do commit `9642ece`: 1 chamada ao redator, 129.244 tokens de saída em cerca de 20 minutos, e "verificação interna da migração reprovou: arquivos sem destino: handoff-20261003-075846-d0e28895.md, handoff-20261003-150404-d0e28895.md, …". O redator reescreveu cada documento 7 a partir do último handoff da conversa e não deu destino aos handoffs intermediários. Com a tarefa 14, a nova tentativa repetiria uma chamada desse tamanho.

## O que fazer (decisão do verificador)

1. Em `migrar`, quando o total de caracteres dos arquivos antigos passa de 300 mil (o mesmo limite de R11), divida a migração em partes consecutivas de até 300 mil caracteres: conversas inteiras em ordem de data, sem dividir um arquivo; uma conversa maior que o limite é dividida em partes consecutivas dos seus handoffs, em ordem, e a última parte traz o último handoff dela. O `index.md` antigo vai na 1ª parte. Abaixo do limite, nada muda (1 chamada, como hoje; T30 e T31 continuam iguais).
2. Cada parte faz o ciclo completo que já existe: chamada, validação com a nova tentativa, diário, gravação, verificação interna e exclusão só dos arquivos daquela parte. A parte seguinte lê os documentos 4, 5 e 6 já gravados. Uma falha encerra o comando com a linha final de falha, e as partes concluídas ficam gravadas; uma nova execução continua das que faltam (o diário da parte em curso continua valendo como hoje).
3. A linha final de sucesso soma os arquivos de todas as partes. Cada parte entra no registro de rodadas como hoje.
4. Em `modelos.md` e `templates.md`, na seção "Migração", acrescente 1 frase: um handoff intermediário, cujo conteúdo um handoff posterior da mesma conversa substituiu, vai em `sem_conteudo`; os parágrafos do documento 7 citam como origem os handoffs de onde vieram.
5. Testes no executor de cada pacote, com o redator falso: pasta acima de 300 mil caracteres com 2 conversas gera 2 chamadas, migra e apaga todos os arquivos; falha na 2ª parte deixa a 1ª gravada e apagada, e a nova execução conclui a 2ª.
6. Gere o programa en pelo `sed` de sempre e confira com `diff`.

Verificação com os 3 comandos da tarefa 01. Relatório em `execucao/codex/tarefa-15-relatorio.md`.
