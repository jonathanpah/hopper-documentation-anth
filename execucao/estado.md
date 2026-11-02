# Estado da execução

- Spec: `SPEC.md`, aprovada em 2026-11-02, commit `b2954f2` da `main`, corrigida pela avaliação do Fable no commit `313e160` da branch de trabalho.
- Branch de trabalho: `versao-2`.
- Executor: sessão local da aba Code do Claude Desktop no MacBook (A2), id `local_4da427f6-6bda-488d-8ff0-9968e8c1c252`, conversa `0f5ecff8-dcad-44a9-be90-0bad629caed5`, modelo Claude Fable 5.1, esforço max, modo de permissão `auto`.
- Cópia de trabalho: `/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth`, pasta da sessão do executor desde 2026-11-02 00:50 UTC.

## Unidade atual: U1, prova do ambiente

Início: 2026-11-02 02:36 UTC.

| Item | Situação | Registro |
| --- | --- | --- |
| 1. Versões | pronto | `versoes.md`, V-U1-01 |
| 2. Acessos | pronto | `versoes.md`, V-U1-02 |
| 3. Clone de leitura | pronto | V-U1-03 |
| 4. Regras de permissão | `deny` aprovado; `ask` bloqueado · motivo: as regras `ask` não geram pedido nesta sessão · evidência: V-U1-04, tentativa 2 (5 comandos rodaram sem pedido; proprietário confirmou no chat) · como reproduzir: rodar `echo hopper_documentation_anth.py migrar` com a regra `Bash(*hopper_documentation_anth.py migrar*)` em `.claude/settings.local.json`, em sessão da aba Code em modo `auto`. Mecanismo substituto: D-06. | V-U1-04, D-05, D-06, P-01 |
| 5. Plugin de sonda | em andamento: instalada em A1, A2 (mesma instalação) e A3; A3 em prova; A1 bloqueado por login do Terminal (P-02); A2 bloqueado por pasta não confiada (P-03) | V-U1-05 (a gravar) |
| 6. Chamada real ao redator | pronto | V-U1-06 |
| 7. Retomada | pendente | |
| 8. Avaliações | pendente | |
| 9. Limpeza | pendente | |

## Unidades

| Unidade | Situação |
| --- | --- |
| U1 | em andamento |
| U2 a U10 | pendentes |

## Requisitos

R01 a R42: pendentes. Bloqueados: nenhum.

## Ações da seção 10 feitas com o "sim" do proprietário

| Data (UTC) | Ação | Palavras do proprietário | Registro |
| --- | --- | --- | --- |
| 2026-11-02 01:25 | Incorporar o PR #2 à `main` (commit `b2954f2`) | "Faça o merge, mas antes de iniciar, quero que o Fable faça uma avaliação da SPEC." | `decisoes.md`, D-01 |
| 2026-11-02 02:48 | Autorizações antecipadas para U1 (sonda), U2 a U7, U8 e U9 (até 60 chamadas); U10 com pergunta na hora | 4 respostas "Sim (Recomendado)" e "U9 sim, U10 pergunte (Recomendado)" no chat | `decisoes.md`, D-08 |
