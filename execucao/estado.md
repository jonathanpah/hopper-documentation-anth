# Estado da execução

- Spec: `SPEC.md`, aprovada em 2026-11-02, commit `b2954f2` da `main`, corrigida pela avaliação do Fable no commit `313e160` da branch de trabalho.
- Branch de trabalho: `versao-2`.
- Executor: sessão local da aba Code do Claude Desktop no MacBook (A2), id `local_4da427f6-6bda-488d-8ff0-9968e8c1c252`, conversa `0f5ecff8-dcad-44a9-be90-0bad629caed5`, modelo Claude Fable 5.1, esforço max, modo de permissão `auto`.
- Cópia de trabalho: `/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth`, pasta da sessão do executor desde 2026-11-02 02:41 UTC (`change_directory`; antes disso a sessão lia as configurações da pasta de origem).

## Unidade atual: U1, prova do ambiente

Início: 2026-11-02 02:36 UTC.

| Item | Situação | Registro |
| --- | --- | --- |
| 1. Versões | pronto | `versoes.md`, V-U1-01 |
| 2. Acessos | pronto | `versoes.md`, V-U1-02 |
| 3. Clone de leitura | pronto | V-U1-03 |
| 4. Regras de permissão | `deny` aprovado (12 regras, 12 provas, V-U1-04 tentativa 3); `ask` bloqueado · motivo: as regras `ask` não geram pedido nesta sessão · evidência: V-U1-04, tentativa 2 (5 comandos rodaram sem pedido; proprietário confirmou no chat) · como reproduzir: rodar `echo hopper_documentation_anth.py migrar` com a regra `Bash(*hopper_documentation_anth.py migrar*)` em `.claude/settings.local.json`, em sessão da aba Code em modo `auto`. Mecanismo substituto: D-06. | V-U1-04, D-05, D-06, P-01 |
| 5. Plugin de sonda | A3 aprovado (3 passagens e calibração: 90%). A1 bloqueado · motivo: Terminal sem login · evidência: `claude auth status` → `loggedIn: false` (03:22 UTC) · como reproduzir: `env -i HOME=$HOME PATH=$PATH claude auth status` · pergunta P-02. A2 bloqueado · motivo: a abertura da sessão de teste na pasta `hopper-sonda-a2` foi recusada (pasta não confiada; classificador do modo auto) · evidência: erros das ferramentas `start_session` às 03:1x e 03:22 UTC · pergunta P-03. | V-U1-05, D-10, D-11 |
| 6. Chamada real ao redator | pronto | V-U1-06 |
| 7. Retomada | pronto | V-U1-07 |
| 8. Avaliações | pronto | V-U1-08 |
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
