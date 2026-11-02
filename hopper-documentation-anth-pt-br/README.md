# hopper-documentation-anth (português)

Plugin do Claude Code que documenta cada conversa em 7 documentos Markdown, a pedido e antes de toda compactação, para que outra pessoa ou outra sessão continue o trabalho sem reler a conversa.

## O que fica gravado

Dentro da pasta em que a conversa foi aberta, o plugin mantém 1 pasta `docs-by-hopper-documentation/`:

```text
docs-by-hopper-documentation/
├── 1-indice.md                 índice e ordem de leitura
├── 4-decisoes.md               decisões de todas as conversas da pasta
├── 5-funcoes.md                funções implementadas (entregas concluídas)
├── 6-pendencias.md             pendências abertas e encerradas
└── conversas/
    └── 2026-11-01-e4bad083/    1 pasta por conversa: data da 1ª mensagem e código
        ├── 2-conversa-integral.md
        ├── 3-conversa-simplificada.md
        └── 7-handoff.md
```

- O **documento 2** é a cópia fiel das mensagens, sem resultados de ferramentas e sem raciocínio interno. Senhas, tokens e chaves viram `[oculto]`. Ele só recebe acréscimos, e cada mensagem tem um identificador como `M42-e4bad083`.
- Os **documentos 3 a 7** são escritos pelo Claude Sonnet 5.5, chamado sem janela (`claude -p`), sem ferramentas e em modo seguro. O programa valida a resposta, numera os itens (`D1-e4bad083`, `F1-e4bad083`, `PD1-e4bad083`) e grava os arquivos.
- O **documento 7** é o handoff, reescrito inteiro a cada rodada, com 9 seções.

## Como roda

- **Antes de toda compactação**, automática ou manual, 2 comandos do evento `PreCompact` rodam: a cópia (síncrona, até 60 segundos) e a escrita (em processo separado, que termina mesmo que o Claude Code seja fechado).
- **A pedido**, quando você pede para documentar ou registrar a conversa, salvar o progresso ou fazer um handoff. A skill roda o mesmo programa em segundo plano e informa a linha final.
- **Na primeira rodada** em uma pasta com handoffs do formato antigo (`index.md` e `handoff-*.md` na raiz), o programa migra esses arquivos para os documentos 4 a 7 e os apaga. Para desligar a migração automática, grave `{"migracao_automatica": false}` em `config.json` na pasta de dados. O comando `migrar --pasta <pasta do projeto>` migra a qualquer momento.

Registros internos ficam na pasta de dados do plugin, `~/.claude/plugins/data/hopper-documentation-anth-hopper-documentation-anth/`: `rodadas.jsonl` (1 linha por etapa, com resultado e motivo), `saidas/` (saída completa de cada processo separado), travas e diários.

## Requisitos

- Claude Code 2.1.284 ou mais novo, na CLI ou no aplicativo (sessões locais), com acesso ao Claude Sonnet 5.5 pela sua conta.
- Python 3.9 ou mais novo, só com a biblioteca padrão.
- macOS ou Linux.

## Instalação

A pasta `hopper-documentation-anth-pt-br/` é o plugin completo e também o catálogo. Com uma cópia dela no computador (clone do repositório ou pasta extraída de uma tag):

```sh
claude plugin marketplace add /caminho/para/hopper-documentation-anth-pt-br
claude plugin install hopper-documentation-anth@hopper-documentation-anth
```

Em uma sessão já aberta, envie `/reload-plugins`. Confira com `claude plugin details hopper-documentation-anth@hopper-documentation-anth`: a skill e o gatilho `PreCompact` devem aparecer. Para atualizar, atualize a cópia e rode `claude plugin marketplace update hopper-documentation-anth` e `claude plugin update hopper-documentation-anth@hopper-documentation-anth`. Para remover, `claude plugin uninstall hopper-documentation-anth@hopper-documentation-anth`; os documentos gravados nos projetos permanecem.

## Limites e custos

- Cada rodada com conteúdo novo faz pelo menos 1 chamada ao Claude Sonnet 5.5 pela sua conta. Um trecho novo com mais de 300 mil caracteres é dividido em partes, com 1 chamada por parte. Em modelos com janela de 1 milhão de tokens, uma compactação pode gerar várias chamadas.
- O Claude Code do terminal apaga os arquivos de histórico com mais de 30 dias. A cópia antes de toda compactação protege a conversa, mas uma rodada a pedido em uma conversa antiga demais falha com o motivo "arquivo de histórico não encontrado".
- O formato do arquivo de histórico é interno do Claude Code e pode mudar. Nesse caso o programa falha com motivo claro, e a correção segue o `CONTRIBUTING.md`.
- Uma rodada por conversa por vez. A segunda espera até 15 minutos.

## Testes

Os testes de aceite da spec ficam em `aceite/` na raiz do repositório e rodam com `python3 -m unittest discover -s aceite/testes` (variável `HOPPER_DOCUMENTATION_ANTH_PACOTE` escolhe o pacote). Os testes do executor ficam em `tests/`. As avaliações de acionamento ficam em `evals/` e rodam com `claude plugin eval ./hopper-documentation-anth-pt-br --ablation none`.

## Licença

MIT. Veja `LICENSE`.
