# Modelos dos documentos

O programa grava os cabeçalhos, os títulos dos blocos e os identificadores finais. Você escreve o conteúdo. Use `N1`, `N2`… para os itens novos em qualquer campo; o programa troca essas referências pelos identificadores finais.

Cite só mensagens do trecho novo ou anteriores a ele e itens existentes na pasta. Use `N1`, `N2`… para itens novos desta resposta. Para falar do que vem depois do trecho novo, escreva sem identificador. Na migração, cite arquivos antigos e itens, pois as mensagens não existem.

## Documento 3, conversa simplificada

O campo `conversa_simplificada` é o corpo de 1 bloco. Ele começa com a linha de assunto e segue com parágrafos curtos. Cada parágrafo termina com as mensagens de origem entre parênteses, separadas por vírgula. Um intervalo usa a forma `M3-e4bad083 a M7-e4bad083`.

```markdown
**Assunto: falha do registro automático do anth.**

O registro automático do anth falhou antes da compactação. O programa recusou 2 citações que não estavam iguais na conversa. (M1-e4bad083)
```

Quando o trecho não traz nada relevante, devolva `nada_relevante` igual a `true` e deixe `conversa_simplificada` vazio.

## Documentos 4, 5 e 6, itens

Cada item de `itens_novos` tem `tipo` (`D` decisão, `F` função implementada, `PD` pendência), `texto` (1 ou 2 frases), `origem` (mensagens do trecho novo ou itens existentes), `situacao` e, só nas pendências, `recomendacao` e `depende_de`. "Função implementada" é qualquer entrega concluída na conversa: código, configuração, documento ou processo.

Situações permitidas:

| Tipo | Situações |
| --- | --- |
| D, decisões | `vigente`, `substituída por <ID>`, `revogada em <M-ID>` |
| F, funções implementadas | `concluída`, `substituída por <ID>`, `desfeita em <M-ID>` |
| PD, pendências | `aberta`, `encerrada em <M-ID> (<motivo curto>)` |

Como o programa grava um item:

```markdown
### PD1-e4bad083
Escrever a spec do modelo de 7 documentos.

- Recomendação: escrever com a skill hopper-spec-anth.
- Depende de: Jonathan dizer que está confortável com o modelo.
- Origem: M66-e4bad083
- Situação: encerrada em M80-e4bad083 (o proprietário autorizou a spec)
- Intervalo da rodada: M56-e4bad083 a M80-e4bad083
```

Para mudar a situação de um item que já existe, inclusive de outra conversa da mesma pasta, use `mudancas`, com o identificador, a situação nova e a origem. A origem de um item novo ou de uma mudança é uma mensagem do trecho novo ou um item existente, nunca uma mensagem de um trecho anterior. Na migração, a origem é o nome do arquivo antigo.

## Documento 7, handoff

As 9 chaves do campo `handoff` viram as 9 seções, nesta ordem: Objetivo; Pautas e estado atual; Próximo passo; Decisões e autorizações vigentes; Restrições vigentes; Descobertas e tentativas descartadas; Pendências e compromissos; Lacunas; Como retomar. Escreva cada seção em parágrafos curtos, cada um com as mensagens de origem entre parênteses. O handoff é reescrito inteiro a cada rodada: inclua o que ainda vale do handoff anterior.

## Resumo

O campo `resumo` tem até 80 caracteres e vai para o índice da pasta, na coluna "Assunto".

## Migração

O campo `handoffs_antigos` é uma lista com o último handoff de cada conversa antiga. Cada entrada tem `conversa` (identificador indicado no arquivo), `data`, `resumo` (até 80 caracteres) e `handoff` (as 9 chaves do documento 7). Em `data`, use a data do último handoff antigo da conversa em `AAAA-MM-DD`, sem hora, por exemplo `2026-09-30`.

O campo `sem_conteudo` lista os nomes dos arquivos antigos sem conteúdo relevante. Na migração, cada item de `itens_novos` também traz `conversa`.
