# Tarefa 05 para o Codex: referências inexistentes nos documentos (R20, achado do aceite em A3)

Mesmas regras da tarefa 01 (edite só o pacote em português e regenere o programa em inglês com o `sed`; não altere `SPEC.md`, `aceite/`, `.github/`, `.claude/`; nada de `git` que grave; sem rede). Os critérios estão congelados: não toque em `aceite/`.

Evidência em `execucao/verificacoes.md`, V-U8-03, e em `execucao/aceite/a3-2/`: o redator real escreveu no handoff que "a próxima rodada deve cobrir M19-67ed412f em diante", e M19 não existe. O conferidor reprovou F8 (R20: "Todo identificador de mensagem ou de item citado nos documentos 3 a 7 existe na pasta de documentação").

## O que fazer (decisão do verificador)

1. **Validação.** Antes de gravar, `validar_resposta` confere todos os identificadores de mensagem (`M<n>-<código>`) e de item (`D|F|PD<n>-<código>`) citados em `conversa_simplificada`, nos 9 campos do `handoff`, no texto, na recomendação e no "depende de" dos itens novos e nas situações das mudanças. Uma mensagem citada tem de existir no documento 2 da pasta (de qualquer conversa da pasta, pelo código) com número até o fim do trecho novo; um item citado tem de existir na pasta ou ser uma referência `N<n>` desta resposta. Na migração, o mesmo vale para os itens e os handoffs, onde as mensagens não existem e não podem ser citadas.
2. **Nova tentativa na mesma rodada.** Quando a resposta falha só nessa conferência, o programa chama o redator 1 vez mais, com a mesma entrada acrescida de 1 linha no fim: "Referências inexistentes na resposta anterior: <lista>. Cite só mensagens e itens que já existem." (e a tradução fiel no pacote em inglês). Se falhar de novo, a rodada falha como hoje (caso de borda de R12). As 2 chamadas entram no registro de rodadas.
3. **Regra para o redator.** Em `modelos.md` e `templates.md`, acrescente: cite só mensagens do trecho novo ou anteriores a ele e itens existentes; para falar do que vem depois, não use identificador.
4. **Testes do executor**, que falham sem a correção: resposta com M19 inexistente no handoff é rejeitada e, com uma 2ª resposta válida do redator simulado, a rodada conclui com 2 chamadas; resposta com item inexistente é rejeitada; referência `N1` continua aceita.

## Verificação e relatório

Os 3 comandos da tarefa 01. Rode também o conferidor com o roteiro na pasta `execucao/aceite/a3-2/docs-by-hopper-documentation` (deve continuar reprovando F8, porque é o resultado antigo) só para registrar. Relatório em `execucao/codex/tarefa-05-relatorio.md`.
