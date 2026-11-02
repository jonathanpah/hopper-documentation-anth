# Estado da execução

- Spec: `SPEC.md`, aprovada em 2026-11-02, commit `b2954f2` da `main`, corrigida pela avaliação do Fable no commit `313e160` da branch de trabalho.
- Branch de trabalho: `versao-2`.
- Executor: sessão local da aba Code do Claude Desktop no MacBook (A2), id `local_4da427f6-6bda-488d-8ff0-9968e8c1c252`, conversa `0f5ecff8-dcad-44a9-be90-0bad629caed5`, modelo Claude Fable 5.1, esforço max, modo de permissão `auto`.
- Cópia de trabalho: `/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth`, pasta da sessão do executor desde 2026-11-02 02:41 UTC (`change_directory`; antes disso a sessão lia as configurações da pasta de origem).

## Unidade atual: U9, migração

U1 a U8 aprovadas, com exceção do item 9 de U1 (limpeza das pastas da sonda, feita no fim de U10). Aceites A1, A2 e A3 aprovados (V-U8-04, V-U8-06 e V-U8-08 com as tentativas de A3 em V-U8-02 a V-U8-05 e anexos de `aceite/`); avaliações de acionamento aprovadas (V-U8-07 e V-U8-08). Critérios congelados no commit `e737aca`, tag `criterios-congelados`. As regras `ask` passaram a gerar pedido depois que a sessão mudou de pasta (as aprovações ficaram como `allow` em `.claude/settings.local.json`); D-06 continua como mecanismo de registro das ações da seção 10.

Próximo passo: U9 (D-08, até 60 chamadas ao redator) e depois U10 (D-19).

## Requisitos

R01 a R42: pendentes. Bloqueados: nenhum.

## Ações da seção 10 feitas com o "sim" do proprietário

| Data (UTC) | Ação | Palavras do proprietário | Registro |
| --- | --- | --- | --- |
| 2026-11-02 01:25 | Incorporar o PR #2 à `main` (commit `b2954f2`) | "Faça o merge, mas antes de iniciar, quero que o Fable faça uma avaliação da SPEC." | `decisoes.md`, D-01 |
| 2026-11-02 02:48 | Autorizações antecipadas para U1 (sonda), U2 a U7, U8 e U9 (até 60 chamadas); U10 com pergunta na hora | 4 respostas "Sim (Recomendado)" e "U9 sim, U10 pergunte (Recomendado)" no chat | `decisoes.md`, D-08 |
