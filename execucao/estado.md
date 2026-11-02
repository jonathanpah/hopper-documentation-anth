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
| 5. Plugin de sonda | A3 aprovado (3 passagens e calibração: 90%). A1 desbloqueado (o falso bloqueio vinha do isolamento da ferramenta Bash; V-U1-02, correção de A1); prova da sonda em A1 pelo painel de Terminal em andamento. A2 bloqueado · motivo: a abertura da sessão de teste na pasta `hopper-sonda-a2` foi recusada (pasta não confiada; classificador do modo auto) · evidência: erros das ferramentas `start_session` às 03:1x e 03:22 UTC · pergunta P-03. | V-U1-05, D-10, D-11 |
| 6. Chamada real ao redator | pronto | V-U1-06 |
| 7. Retomada | pronto | V-U1-07 |
| 8. Avaliações | pronto | V-U1-08 |
| 9. Limpeza | pendente | |

## Unidades

| Unidade | Situação |
| --- | --- |
| U1 | itens 1 a 4 e 6 a 8 prontos (4: `ask` bloqueado, D-06); item 5: A3 pronto, A1 e A2 bloqueados (P-02, P-03); item 9 pendente; revisão passada 1 feita |
| U2 | critérios escritos e testados; falta a revisão independente (derrubada pelo limite do plano, retoma depois de 05:30 UTC), o manifesto, a tag e a prova de C18 |
| U3 e U4 | programa escrito; 31 testes de aceite aprovados nos 2 pacotes; revisão pendente |
| U5 | gatilho e skill escritos; T41 aprovado; execução completa das avaliações pendente; revisão pendente |
| U6 | migração escrita; T30, T31 e T42 aprovados; revisão pendente |
| U7 | repositório e documentação atualizados; T32 e T35 aprovados; revisão pendente |
| U8 | 2.0.0 instalada nas 3 contas com a migração desligada (V-U8-01); aceite depende do limite do plano (05:30 UTC), de A1 (P-02) e de A2 (P-03) |
| U9 e U10 | pendentes |

## Requisitos

R01 a R42: pendentes. Bloqueados: nenhum.

## Ações da seção 10 feitas com o "sim" do proprietário

| Data (UTC) | Ação | Palavras do proprietário | Registro |
| --- | --- | --- | --- |
| 2026-11-02 01:25 | Incorporar o PR #2 à `main` (commit `b2954f2`) | "Faça o merge, mas antes de iniciar, quero que o Fable faça uma avaliação da SPEC." | `decisoes.md`, D-01 |
| 2026-11-02 02:48 | Autorizações antecipadas para U1 (sonda), U2 a U7, U8 e U9 (até 60 chamadas); U10 com pergunta na hora | 4 respostas "Sim (Recomendado)" e "U9 sim, U10 pergunte (Recomendado)" no chat | `decisoes.md`, D-08 |
