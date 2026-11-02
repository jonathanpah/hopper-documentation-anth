# Tarefa 14 para o Codex: destino de cada arquivo antigo conferido antes da gravação (U9)

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`, `SPEC.md`, `.github/` nem nos `evals/`).

## Evidência

Migração real de `/home/jpah/projects/mallmetrics/repo` (2 handoffs e `index.md`), programa do commit `9642ece`: "verificação interna da migração reprovou: arquivos sem destino: index.md". O redator não citou o `index.md` antigo em nenhuma origem, em `sem_conteudo` nem no documento 7. Como `verificacao_interna` roda depois da gravação, os documentos 1, 4, 5, 6 e 7 ficaram gravados com os arquivos antigos ainda na pasta (R31 respeitado), e o diário ficou guardado. Uma nova execução de `migrar` reaproveita a resposta do diário e reprova de novo, sem saída.

## O que fazer (decisão do verificador)

1. Em `validar_resposta`, com `migracao=True`, confira antes da gravação a mesma condição de destino de `verificacao_interna`: cada nome de `arquivos_validos` aparece em uma origem de `itens_novos` ou de `mudancas`, em `sem_conteudo` ou no texto de algum `handoffs_antigos[].handoff`. O que faltar vira `RespostaCorrigivel` ("arquivos sem destino: …"), para usar a nova tentativa existente. A `verificacao_interna` depois da gravação continua igual.
2. Em `modelos.md` e `templates.md`, na seção "Migração", acrescente 1 frase: todo arquivo antigo precisa de destino; um arquivo sem conteúdo próprio, como o `index.md` antigo que só lista os handoffs, vai em `sem_conteudo`.
3. Teste no executor de cada pacote: 1ª resposta sem destino para o `index.md` e 2ª com `index.md` em `sem_conteudo` conclui a migração e apaga os arquivos antigos; 2 respostas sem destino falham sem gravar os documentos 4 a 7 e sem apagar os arquivos antigos.
4. Gere o programa en pelo `sed` de sempre e confira com `diff`.

Verificação com os 3 comandos da tarefa 01. Relatório em `execucao/codex/tarefa-14-relatorio.md`.
