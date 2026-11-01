# Spec: hopper-documentation-anth, versão 2

- Proprietário: Jonathan Honorio (@jonathanpah).
- Autor da spec: Claude Opus 5.5, em uma sessão do Claude Code na nuvem, em 2026-11-01.
- Skill usada para escrever: `hopper-spec-anth`, versão `0.2.0`.
- Situação: aguardando a aprovação do proprietário.
- Horários: as datas e horas das decisões estão em UTC.

## 1. Objetivo e resultado que encerra o trabalho

**Objetivo.** Substituir a versão atual do plugin `hopper-documentation-anth` por uma versão nova. A versão nova documenta cada conversa do Claude Code em 7 documentos Markdown. A documentação roda antes de toda compactação e quando o usuário pede.

**Resultado que encerra o trabalho.** O trabalho termina quando os 5 itens abaixo estão comprovados pelos verificadores.

1. A versão nova está na branch `main` do repositório `jonathanpah/hopper-documentation-anth`, em português e em inglês, sem código nem documentação da versão atual.
2. O plugin está instalado e aprovado no roteiro de aceite nos 3 ambientes (A1, A2 e A3 do glossário).
3. Em cada ambiente, uma conversa de teste foi documentada a pedido e antes de uma compactação automática, e o conferidor aprovou a pasta de documentação gerada.
4. As pastas de documentação do formato antigo, no MacBook e na VPS, foram migradas, e os arquivos antigos foram apagados.
5. A verificação do GitHub do commit integrado à `main` mostra todos os verificadores aprovados juntos.

## 2. Participantes

| Quem | O que faz |
| --- | --- |
| Proprietário | Jonathan Honorio. Aprova esta spec. Durante a execução, só responde "sim" ou "não" aos pedidos de permissão das ações da seção 10 e às perguntas previstas na garantia G07. Não executa nenhuma outra tarefa (decisão P18). |
| Autor da spec | Claude Opus 5.5. Escreveu esta spec. Não executa. |
| Executor | Uma sessão do Claude Code no MacBook, aberta na aba Code do Claude Desktop, em sessão local. Faz todo o trabalho: código, testes, instalação nos 3 ambientes, aceite, migração e integração. Acessa a VPS por SSH a partir do MacBook. |
| Verificadores | Os programas e roteiros da coluna "Verificador" da seção 5. O executor roda os verificadores, mas não altera os critérios deles (G03). |
| Revisor | Um subagente sem o contexto do executor, aberto pelo executor no fim de cada unidade de trabalho (G09). |

## 3. Glossário

Cada coisa tem um único nome nesta spec.

| Nome | Significado |
| --- | --- |
| Plugin | O pacote `hopper-documentation-anth` instalado no Claude Code. Contém a skill, o gatilho e o programa. |
| Skill | A skill `hopper-documentation-anth`, que roda quando o usuário pede a documentação. |
| Gatilho | Os 2 comandos que o plugin registra no evento `PreCompact` do Claude Code: o gatilho de cópia e o gatilho de escrita. |
| Programa | O arquivo `scripts/hopper_documentation_anth.py`. Usa só a biblioteca padrão do Python. |
| Copiador | A parte do programa que grava a conversa integral. Não usa IA. |
| Redator | O Claude Code sem janela (`claude -p`) com o modelo Claude Sonnet 5.5. Escreve o conteúdo dos documentos 3 a 7. |
| Conversa | Uma sessão do Claude Code, com um identificador único (UUID). |
| Código da conversa | Os 8 primeiros caracteres do identificador da conversa. Exemplo: `e4bad083`. |
| Pasta do projeto | A pasta em que a conversa foi aberta. O programa lê essa pasta no campo `cwd` do primeiro registro do arquivo de histórico. |
| Pasta de documentação | `<pasta do projeto>/docs-by-hopper-documentation/`. |
| Pasta da conversa | `<pasta de documentação>/conversas/<AAAA-MM-DD>-<código da conversa>/`. No pacote em inglês, a subpasta se chama `conversations/`. |
| Pasta de configuração | O valor de `CLAUDE_CONFIG_DIR`, quando definido. Senão, `~/.claude`. |
| Arquivo de histórico | O arquivo JSONL que o Claude Code grava para cada conversa, em `<pasta de configuração>/projects/<pasta codificada>/<identificador>.jsonl`. |
| Pasta de dados | `<pasta de configuração>/plugins/data/hopper-documentation-anth/`. Guarda travas, diários e o registro de rodadas. É a mesma no terminal e no Desktop. |
| Mensagem | Uma entrada da conversa integral, com identificador `M<n>-<código da conversa>`. |
| Item | Uma entrada dos documentos 4, 5 ou 6, com identificador `D<n>-<código>`, `F<n>-<código>` ou `PD<n>-<código>`. |
| Rodada | Uma execução completa do programa para uma conversa: cópia, escrita e gravação. |
| Trecho novo | As mensagens da conversa integral que ainda não estão cobertas por um bloco da conversa simplificada. |
| Diário | O arquivo da pasta de dados que guarda a resposta do redator antes da gravação nos documentos. |
| Registro de rodadas | O arquivo `rodadas.jsonl` da pasta de dados. Recebe 1 linha por rodada, com data, conversa, resultado e motivo de falha. |
| Formato antigo | Os arquivos `index.md` e `handoff-*.md` gravados na raiz da pasta de documentação pelas versões anteriores do anth e pelo plugin `hopper-documentation`. |
| Verificação interna | A função do programa que confere a pasta de documentação antes de apagar arquivos do formato antigo (R31). |
| Conferidor | O programa `aceite/conferir.py` do repositório. Confere uma pasta de documentação contra os requisitos (Anexo F). Não faz parte do plugin instalado. |
| Regras de escrita | A lista do Anexo A. |
| A1 | Claude Code no terminal do MacBook. |
| A2 | Claude Desktop no MacBook, aba Code, sessão local. |
| A3 | Claude Code no terminal da VPS (Linux). |
| Branch de trabalho | A branch `versao-2` do repositório. |
| Integrar | Enviar commits da branch de trabalho ao GitHub. |
| Registro de execução | A pasta `execucao/` da branch de trabalho (G08). |
| Roteiro de aceite | O roteiro do Anexo F, executado em cada ambiente. |
| Anth | Forma curta do repositório e do plugin `hopper-documentation-anth`. |
| Versão atual | O conteúdo da branch `main` do anth no commit `8dbb40b`, antes desta spec. |
| PR #1 | O pedido de alteração aberto em 2026-11-01 no anth, com a correção provisória da conferência de citações, na branch `fix/conferencia-de-citacoes`. |
| Verificação do GitHub | O fluxo `.github/workflows/verificar.yml`, que roda no GitHub a cada envio de commits. |
| Verificação completa | Uma execução de todos os verificadores juntos. Na garantia G05, copiada sem mudança, a expressão "rodada completa" tem esse sentido e não se refere à rodada deste glossário. |
| Uso do computador | O recurso do Claude Desktop que permite ao Claude ver a tela e usar o mouse e o teclado (computer use). |
| Plugin de sonda | O plugin temporário de U1, descrito no Anexo G. |
| Pasta de teste | Uma pasta nova, criada pelo executor para o roteiro de aceite, como `~/hopper-teste-a1`. |
| Conversa de teste | A conversa do roteiro de aceite (Anexo F, passo F-C). |
| Lista de hooks | A lista que o comando `/hooks` do Claude Code mostra. |

**Os 7 documentos.**

| Nº | Nome em português | Nome em inglês | Onde fica | Quem escreve |
| --- | --- | --- | --- | --- |
| 1 | `1-indice.md` | `1-index.md` | Pasta de documentação | Programa, com o resumo de cada conversa escrito pelo redator |
| 2 | `2-conversa-integral.md` | `2-full-conversation.md` | Pasta da conversa | Copiador |
| 3 | `3-conversa-simplificada.md` | `3-simplified-conversation.md` | Pasta da conversa | Redator |
| 4 | `4-decisoes.md` | `4-decisions.md` | Pasta de documentação | Redator. O programa dá os números |
| 5 | `5-funcoes.md` | `5-functions.md` | Pasta de documentação | Redator. O programa dá os números |
| 6 | `6-pendencias.md` | `6-pending.md` | Pasta de documentação | Redator. O programa dá os números |
| 7 | `7-handoff.md` | `7-handoff.md` | Pasta da conversa | Redator |

## 4. Decisões do proprietário

As palavras estão copiadas da conversa de 2026-11-01. "[…]" marca um corte.

| Nº | Data e hora (UTC) | Palavras do proprietário | Decisão |
| --- | --- | --- | --- |
| P01 | 2026-11-01 21:23 | "Documento 1: index -> roteiro/índice para todos os documentos" […] "Documento 7: handoff final garantindo contexto full para a próxima sessão" | Os 7 documentos da seção 3. |
| P02 | 2026-11-01 21:23 | "Documento 2: Conversa completa do chat (integral), sem mudar nada, a cada rodada da skill, só add a parte nova ainda não processada." | A conversa integral só recebe acréscimos. |
| P03 | 2026-11-01 21:23 | "Documento 3: Conversa do documento 2 atualizada para um formato com cerca de 70% do ASD-ASD-STE100, Simplified Technical English, porém em português" | Regras de escrita do Anexo A. |
| P04 | 2026-11-01 21:23 | "sem rodar programas paralelos, somente a IA mesmo, sonnet 5.5, fazendo" | O redator é o Claude Sonnet 5.5. A parte "sem rodar programas paralelos" foi substituída pelas decisões P06 e P14. |
| P05 | 2026-11-01 21:23 | "Quero que a skill defina os "o ques...", o "como" a ia faz.." | O SKILL.md descreve o que a skill produz e como ela roda (R41). |
| P06 | 2026-11-01 22:08 | "1. Script" | O copiador é um programa, e não a IA. |
| P07 | 2026-11-01 22:08 | "2. Ocultar" | Senhas e tokens viram `[oculto]` na conversa integral. |
| P08 | 2026-11-01 22:08 | "3. 1 linha" | Cada uso de ferramenta vira 1 linha, sem o resultado. |
| P09 | 2026-11-01 22:08 | "4. 1 por pasta em que a conversa foi aberta, porém cada sessão chat tem suas questões específicas" […] "Toda pasta/projeto, tem uma única pasta: docs-by-hopper-documentation/" | Estrutura de pastas da seção 3. |
| P10 | 2026-11-01 22:08 | "5. Sempre antes da compactação automática." […] "Eu tb posso rodar quando quiser." | O gatilho roda antes da compactação, e a skill roda a pedido. |
| P11 | 2026-11-01 22:08 | "teremos uma skill para Anthropic e outra para codex e nenhuma com os dois (iremos deletar o repositório que não trata específicamente da skill de cada modelo para evitar confusão)." | Esta spec cobre só a skill do Claude. |
| P12 | 2026-11-01 22:16 | "Porque vc não vincula o número ao número da conversa também?" […] "M42-e4bad083 ou algo do tipo." | Todo identificador leva o código da conversa. |
| P13 | 2026-11-01 22:16 | "Vamos apagar […], mas 'so no final […]. Não faça nada com esse repositório agora" | O repositório `hopper-documentation` não é tocado nesta spec. |
| P14 | 2026-11-01 22:22 | "B" | O gatilho chama o Claude sem janela (`claude -p`) para escrever, sempre. |
| P15 | 2026-11-01 22:32 | "Na spec tem que constar a instalação no Claude code do macbook CLI, Desktop e no CLI da VPS." […] "nao faremos spec do codex antes da skill no claude code estar 100% operante" | Instalação e aceite em A1, A2 e A3. A skill do Codex fica fora. |
| P16 | 2026-11-01 22:33 | "estou confortável, escreva a spec" | Autoriza esta spec. |
| P17 | 2026-11-01 23:17 | "1. Ok" | Esta spec fica no arquivo `SPEC.md` do repositório e passa por um pedido de alteração (PR). |
| P18 | 2026-11-01 23:17 | "2. Claude no macbook faz tudo. Eu não faço nada." | O executor é o Claude no MacBook (seção 2). |
| P19 | 2026-11-01 23:17 | "3. Inglês e portugês […]" | O repositório mantém os pacotes em português e em inglês. |
| P20 | 2026-11-01 23:17 | "4. Nao guardamos lixo. Nao aproveita-se nada de arquivo antigo. Copai-se o q tem q copiar para ser aproveitado/reescrito, depois delta tudo. O repositório so mantem a nova." | O formato antigo é migrado e depois apagado (R30, R31). O repositório fica só com a versão nova (R32). |
| P21 | 2026-11-01 23:17 | "5. ok" | As regras de escrita seguem o texto do proprietário, sem repetições e sem 3 frases que valem só para o chat (Anexo A). |
| P22 | 2026-11-01 23:17 | "6. ok" | "Função implementada" é qualquer entrega concluída na conversa: código, configuração, documento ou processo. |
| P23 | 2026-11-01 23:17 | "7. ok" | Cada projeto é documentado em uma máquina só. |
| P24 | 2026-11-01 23:17 | Decorre da resposta 4: "Nao guardamos lixo" | Fechar o PR #1 (`fix/conferencia-de-citacoes`) sem integrar. **Pendente de confirmação** (seção 15). |

## 5. Requisitos

Cada requisito tem 1 verificador. Os testes "T<nn>" ficam em `tests/` de cada pacote e são escritos a partir dos anexos desta spec (G04). Os casos de borda de cada requisito estão na seção 6.

### 5.1 Estrutura

| ID | Requisito | Verificador |
| --- | --- | --- |
| R01 | Na primeira rodada em uma pasta do projeto, o programa cria a pasta de documentação com os documentos 1, 4, 5 e 6 e a subpasta de conversas. | T01, com pasta vazia e a árvore esperada do Anexo E. |
| R02 | Para cada conversa, o programa cria a pasta da conversa com os documentos 2, 3 e 7, com a data da primeira mensagem no fuso da máquina. | T02. |
| R03 | O programa grava só dentro da pasta de documentação e da pasta de dados. | T03: 1 rodada inteira em pasta temporária. A lista de arquivos criados ou alterados fora dessas 2 pastas fica vazia. |

### 5.2 Conversa integral (documento 2)

| ID | Requisito | Verificador |
| --- | --- | --- |
| R04 | A cada rodada, o copiador acrescenta ao documento 2 só as mensagens posteriores à última mensagem já copiada, e os bytes já gravados continuam idênticos. | T04: 2 rodadas com o caso B1. O SHA-256 do conteúdo anterior não muda. |
| R05 | Cada mensagem do documento 2 tem o cabeçalho, o comentário de registros e o texto do Anexo E, com n começando em 1 e crescendo de 1 em 1 na conversa. | T05, com a saída literal esperada do caso B1. |
| R06 | O copiador grava cada uso de ferramenta do Claude como 1 linha `Ferramenta: <nome> · <alvo>`, sem o resultado, com o alvo cortado em 120 caracteres. | T06, com o caso B1. |
| R07 | O copiador troca senhas, tokens, chaves e códigos de acesso por `[oculto]` (no pacote em inglês, `[hidden]`), no mínimo nos formatos do caso B2. | T07, com os casos B2. |
| R08 | O copiador inclui as mensagens do usuário, inclusive as enviadas enquanto o Claude trabalha, as respostas do Claude, as respostas a perguntas estruturadas, os planos aprovados, as mensagens de outras sessões, as interrupções e a indicação de anexos. | T08, com o caso B1. |
| R09 | O copiador exclui lembretes do sistema, saídas de gatilhos, notificações de tarefas, ecos de comandos, resumos de compactação, cadeias laterais de subagentes, raciocínio interno e resultados de ferramentas. | T09, com o caso B1. |
| R10 | O copiador conta uma vez os registros repetidos de uma conversa retomada ou bifurcada. | T10, com o caso herdado `test_fork_and_rewritten_records` do `hopper-documentation`. |

### 5.3 Redator e documentos 1, 3 a 7

| ID | Requisito | Verificador |
| --- | --- | --- |
| R11 | A cada rodada com trecho novo, o programa envia ao redator só o trecho novo, os documentos 4, 5 e 6 atuais, o documento 7 anterior da conversa, as regras de escrita e os modelos do Anexo E. | T11: redator simulado que registra a entrada recebida. |
| R12 | O programa chama o redator com o modelo `claude-sonnet-5-5`, esforço `high`, modo seguro, sem ferramentas e sem persistir a sessão, e descarta a resposta que não cumpre a regra de modelo da decisão C04. | T12, com o comando montado. U1 e U8, com resposta real. |
| R13 | A cada rodada, o programa acrescenta ao documento 3 um bloco por intervalo de mensagens, e cada parágrafo do bloco termina com as mensagens de origem entre parênteses. | T13. Conferidor, verificações F3. |
| R14 | O programa numera cada item novo com o próximo número livre do código da conversa e nunca reaproveita um número existente. | T14. Conferidor, verificação F4. |
| R15 | Cada item tem identificador, texto, origem com 1 ou mais mensagens ou arquivos antigos, situação e rodada, no formato do Anexo E. | Conferidor, verificações F4. |
| R16 | O programa aplica as mudanças de situação pedidas pelo redator a itens existentes da mesma pasta de documentação, inclusive de outras conversas, e registra sem aplicar os pedidos para identificadores inexistentes. | T16. |
| R17 | A cada rodada, o programa reescreve inteiro o documento 7 da conversa com as 9 seções do Anexo E. | T17. Conferidor, verificação F5. |
| R18 | A cada rodada, o programa reescreve o documento 1 com a ordem de leitura, os links relativos dos documentos e a tabela das conversas do Anexo E. | T18. Conferidor, verificação F6. |
| R19 | Nos documentos 3 a 7 escritos pelo redator, no mínimo 90% das frases têm até 25 palavras, nenhuma frase passa de 40 palavras e nenhum parágrafo passa de 6 frases. | Conferidor, verificação F7, nas pastas geradas pelo roteiro de aceite. |
| R20 | Todo identificador de mensagem ou de item citado nos documentos 3 a 7 existe na pasta de documentação. | Conferidor, verificação F8. |
| R21 | Na conversa de teste, a mensagem da decisão é origem de um item D, a mensagem da pendência é origem de um item PD, e a criação do arquivo `nota.txt` é origem de um item F. | Conferidor, verificação F9, com os identificadores registrados no roteiro de aceite. |

### 5.4 Execução

| ID | Requisito | Verificador |
| --- | --- | --- |
| R22 | Antes de toda compactação, automática ou manual, o gatilho de cópia roda o copiador de forma síncrona, termina em até 60 segundos e sai sempre com código 0. | T22, com histórico de 50 MB. U1 e U8: no registro de rodadas, a cópia termina antes do registro de compactação do arquivo de histórico. |
| R23 | Depois da cópia, o gatilho de escrita inicia a rodada em um processo separado do Claude Code, e a rodada termina mesmo com o Claude Code fechado 5 segundos depois do início da compactação. | U1 e U8, em A1, A2 e A3. |
| R24 | Quando uma rodada falha, a falha fica no registro de rodadas e no documento 1, e a conversa recebe 1 aviso com o motivo se o Claude Code continuar aberto. | T24, com redator simulado que falha. U8. |
| R25 | A skill roda a mesma rodada quando o usuário pede a documentação, em segundo plano, e informa ao usuário a linha final do programa. | Avaliações de acionamento positivas (`claude plugin eval`). U8. |
| R26 | A skill não roda quando o pedido é explicar, revisar ou editar a skill. | Avaliações de acionamento negativas, herdadas da versão atual. |
| R27 | O programa roda no máximo 1 rodada por conversa ao mesmo tempo, e a segunda rodada espera até 15 minutos antes de desistir com aviso. | T27. |
| R28 | Uma rodada sem mensagem nova não chama o redator, não altera nenhum arquivo e informa "nada novo". | T28. |
| R29 | Uma rodada interrompida em qualquer etapa é concluída pela rodada seguinte, sem bloco duplicado, sem item duplicado e sem mensagem perdida. | T29: interrupção simulada depois da cópia, depois do diário e no meio da gravação. |

### 5.5 Migração e limpeza

| ID | Requisito | Verificador |
| --- | --- | --- |
| R30 | Na primeira rodada em uma pasta de documentação com arquivos do formato antigo, ou com o comando `migrar --pasta <pasta do projeto>`, o programa grava nos documentos 4, 5 e 6 as decisões, funções e pendências extraídas pelo redator, com origem igual ao nome do arquivo antigo, e grava o último handoff de cada conversa antiga como documento 7 da pasta dessa conversa. | T30, com os casos B3. |
| R31 | O programa apaga os arquivos do formato antigo só depois de gravar a migração e de a verificação interna aprovar a pasta de documentação. | T31: com a verificação interna reprovada, nenhum arquivo é apagado. |
| R32 | A branch `main` contém só os arquivos do inventário do Anexo C, e nenhum arquivo contém `claude_agent_sdk`, `get_session_messages` ou `unverified_quotes`. | T32, teste de inventário. |
| R33 | Nos ambientes A1, A2 e A3, a pasta de dados não contém a pasta `venv` da versão atual, e o plugin `hopper-documentation` não está instalado. | Roteiro de aceite, passo F-L. |
| R34 | O PR #1 está fechado sem integração, e a branch `fix/conferencia-de-citacoes` não existe no GitHub. | `gh pr view 1 --json state` mostra `CLOSED`. `git ls-remote origin fix/conferencia-de-citacoes` não devolve nada. |

### 5.6 Idiomas, compatibilidade e instalação

| ID | Requisito | Verificador |
| --- | --- | --- |
| R35 | O repositório tem 2 pacotes completos, `hopper-documentation-anth-pt-br` e `hopper-documentation-anth-en`, e o programa é o mesmo arquivo nos 2, exceto a linha `LANGUAGE`. | T35: a comparação dos 2 arquivos mostra só essa linha. |
| R36 | O programa roda com Python 3.9 ou mais novo, só com a biblioteca padrão. | Verificação automática do GitHub com Python 3.9 e 3.13. Versões registradas em U1. |
| R37 | O programa encontra o arquivo de histórico pela pasta de configuração, inclusive com `CLAUDE_CONFIG_DIR` definida. | T37. |
| R38 | O programa encontra o executável do Claude Code que iniciou o gatilho nos 3 ambientes, inclusive a cópia própria do Claude Desktop. | T38. U1 e U8 em A2. |
| R39 | Nos ambientes A1, A2 e A3, o plugin aparece como instalado e ativo, a skill aparece na lista de comandos, e os 2 comandos do gatilho aparecem na lista de hooks. | Roteiro de aceite, passo F-I, com as saídas registradas. |
| R40 | Em cada ambiente, a conversa de teste gera uma pasta de documentação aprovada pelo conferidor depois de 1 rodada a pedido e de 1 compactação automática. | Conferidor, verificações F1 a F10. |
| R41 | O SKILL.md de cada pacote tem as seções "O que a skill produz" e "Como a skill roda", com menos de 500 linhas. | T41. |

## 6. Casos de borda

| Requisito | Caso de borda | Comportamento esperado |
| --- | --- | --- |
| R01 | A pasta do projeto não aceita gravação. | A rodada falha com o motivo, nada é gravado, e o aviso de R24 é enviado. |
| R02 | A conversa começa perto da meia-noite. | A data da pasta é a da primeira mensagem, e não a da rodada. |
| R02 | 2 conversas da mesma pasta têm os mesmos 8 primeiros caracteres. | A conversa mais nova usa os 12 primeiros caracteres como código, e o fato entra no registro de rodadas. |
| R04 | O arquivo de histórico ainda está sendo gravado. | O copiador espera o tamanho do arquivo ficar igual por 1 segundo, até 5 segundos no total (C09). Mensagens gravadas depois entram na rodada seguinte. |
| R04 | O registro da última mensagem copiada não existe mais no arquivo de histórico. | O copiador continua pelos registros com data e hora posteriores às da última mensagem copiada e anota o fato no registro de rodadas. |
| R04 | O arquivo de histórico foi apagado pela retenção do Claude Code (30 dias). | A rodada falha com o motivo "arquivo de histórico não encontrado", e os documentos existentes ficam como estão. |
| R06 | A ferramenta não tem campo de alvo. | A linha traz só o nome da ferramenta. |
| R06 | O alvo contém uma senha. | A senha vira `[oculto]` (R07). |
| R07 | O texto tem as palavras "senha" ou "token" sem valor. | O texto fica igual (caso B2). |
| R08 | O usuário anexa uma imagem ou um arquivo. | O copiador grava `[imagem anexada]` ou `[arquivo anexado: <nome>]`. |
| R08 | O usuário interrompe a resposta do Claude. | O copiador grava uma mensagem com autor "Evento" e o texto "O usuário interrompeu a resposta.". |
| R11 | O trecho novo passa de 300 mil caracteres. | O programa divide o trecho em partes consecutivas, sem dividir uma mensagem, e faz 1 chamada ao redator por parte, em ordem. |
| R12 | O redator não responde em 15 minutos, ou responde sem o JSON do Anexo D. | A rodada falha, nada é gravado nos documentos 1 e 3 a 7, e a rodada seguinte repete a chamada. |
| R14 | Um item foi apagado à mão de um documento. | O programa não detecta itens apagados à mão. O próximo número é o maior número existente mais 1. |
| R16 | O redator pede mudança de um identificador que não existe. | O pedido não é aplicado e entra no registro de rodadas. |
| R22 | O copiador falha. | O gatilho de cópia sai com código 0, a compactação continua, e a falha entra no registro de rodadas. O gatilho de escrita tenta a cópia de novo dentro da rodada. |
| R23 | O Claude Code é fechado durante a rodada. | A rodada continua no processo separado. A falha, se houver, fica no registro de rodadas e no documento 1. |
| R25 | O usuário pede a documentação enquanto o gatilho roda uma rodada da mesma conversa. | A rodada do pedido espera (R27) e depois informa "nada novo" ou grava o que faltou. |
| R27 | A espera passa de 15 minutos. | A segunda rodada desiste e informa o motivo. |
| R30 | Um arquivo do formato antigo não tem o identificador da conversa no cabeçalho nem no nome. | O código usado é `antigo` seguido dos 4 primeiros caracteres do SHA-256 do nome do arquivo, e o item cita o arquivo como origem. |
| R30 | A pasta de documentação tem handoffs antigos de conversas do Codex. | Eles são migrados como os do Claude, com o código da conversa do Codex. |
| R31 | A rodada é interrompida depois da migração e antes da exclusão. | A rodada seguinte refaz a verificação interna e apaga os arquivos antigos que restaram. |
| R05 | Um registro do usuário fica vazio depois de retirar os lembretes do sistema. | O copiador não cria mensagem para esse registro. |
| R13 | O redator devolve `nada_relevante` igual a `true`. | O bloco do documento 3 traz só "Sem conteúdo novo relevante.", e o intervalo fica coberto. |
| R17 | O redator devolve `nada_relevante` igual a `true`. | O documento 7 não muda. |
| R18 | A pasta tem uma conversa migrada do formato antigo. | A tabela mostra "sem conversa integral" na coluna "Última mensagem". |
| R19 | O texto tem títulos, tabelas, listas de metadados ou blocos de código. | Esses trechos ficam fora da contagem (verificação F7). |
| R20 | Um documento cita um item de outra conversa da mesma pasta. | A citação é válida. |
| R26 | O usuário pergunta o que é um handoff. | A skill não roda (avaliação herdada `nao-o-que-e-handoff`). |
| R39 | O plugin está instalado, mas desativado. | R39 reprova, e o executor ativa o plugin com `claude plugin enable`. |

Os demais requisitos não têm caso de borda além do comportamento descrito no próprio requisito.

## 7. O que nunca pode acontecer

| ID | Proibição |
| --- | --- |
| N01 | Alterar ou apagar uma mensagem já gravada no documento 2. |
| N02 | Gravar fora da pasta de documentação e da pasta de dados. |
| N03 | Reaproveitar um número de mensagem ou de item. |
| N04 | Gravar nos documentos texto escrito por outro modelo que não o Claude Sonnet 5.5. |
| N05 | Gravar uma senha ou um token nos formatos do caso B2 sem ocultar. |
| N06 | Apagar um arquivo do formato antigo antes de a migração estar gravada e aprovada pela verificação interna. |
| N07 | O gatilho de cópia sair com código 2. Esse código bloqueia a compactação. |
| N08 | O redator receber ferramentas, plugins, gatilhos, skills, servidores MCP ou arquivos `CLAUDE.md`. |
| N09 | O executor fazer uma ação da seção 10 sem o "sim" do proprietário no pedido de permissão. |
| N10 | O executor alterar critérios congelados sem o proprietário (G03). |
| N11 | O executor alterar o repositório `hopper-documentation` (P13). |

## 8. O que fica fora

- A skill do Codex e o repositório `hopper-documentation-openai` (P11, P15).
- Qualquer alteração no repositório `hopper-documentation`. O executor só lê o código dele (P13).
- A mesma pasta de projeto sincronizada entre o MacBook e a VPS, por git ou Dropbox (P23).
- Os documentos 2 e 3 de conversas que só existem no formato antigo.
- Windows, WSL e sessões na nuvem do Claude Desktop, porque o Desktop não carrega plugins nelas (fonte: `code.claude.com/docs/en/desktop.md`, lida em 2026-11-01).
- O chat do claude.ai fora do Claude Code.
- Publicar release no GitHub.

## 9. Unidades de trabalho e ordem

| Unidade | Conteúdo | Depende de |
| --- | --- | --- |
| U1 | **Prova do ambiente (G11).** Ver abaixo. | Nada. |
| U2 | **Critérios congelados.** Criar `aceite/casos/` a partir dos Anexos B e F, o conferidor (`aceite/conferir.py`), o manifesto `aceite/MANIFESTO.sha256` e a verificação automática do GitHub (`.github/workflows/verificar.yml`). Mostrar que cada teste novo falha no código atual. | U1 |
| U3 | **Copiador.** R04 a R10, R07 e R37. Reaproveita o leitor e a ocultação do `hopper-documentation` (C01, C13). | U2 |
| U4 | **Redator e gravação.** R11 a R21 e R27 a R29. | U3 |
| U5 | **Gatilho e skill.** R22 a R26, R38 e R41. | U4 |
| U6 | **Migração.** R30 e R31. | U4 |
| U7 | **Repositório e documentação.** R32, R35 e R36. Apagar o código e a documentação da versão atual. Atualizar README, CONTRIBUTING, SECURITY, `index.md` e avaliações nos 2 idiomas. | U5, U6 |
| U8 | **Instalação e aceite nos 3 ambientes,** a partir da branch de trabalho. R39, R40, R22 e R23 com dados reais. | U7 |
| U9 | **Migração real e limpeza dos ambientes.** Procurar as pastas de documentação do formato antigo no MacBook e na VPS e rodar o comando `migrar` em cada uma. Desinstalar o plugin `hopper-documentation` e apagar a `venv` antiga. R30, R31 e R33 com dados reais. | U8 |
| U10 | **Integração na `main`.** Abrir o PR da branch de trabalho, rodar todos os verificadores juntos, apagar a pasta `execucao/`, rodar de novo, integrar com o "sim" do proprietário, atualizar a instalação nos 3 ambientes a partir da `main` e fechar o PR #1 (R34). | U9 |

**U1, em detalhe.** O executor prova cada item abaixo executando e grava o resultado em `execucao/versoes.md` e `execucao/verificacoes.md`.

1. Versões: Claude Code em A1 e A3, versão da aba Code do Desktop pelo `/status` em A2, todas iguais ou maiores que 2.1.284. Python 3 em A1, A3 e no ambiente em que o gatilho roda no Desktop.
2. Acesso: SSH do MacBook para a VPS. `gh auth status` com permissão de envio ao repositório. Uso do computador (computer use) disponível na sessão do executor, para conduzir sessões do Desktop em A2.
3. Regras de permissão da seção 10 ativas na sessão do executor.
4. Plugin de sonda temporário, com os 2 gatilhos de `PreCompact` do Anexo G. A sonda grava a hora de cada etapa. Provar em A1, A2 e A3 que:
   - o gatilho síncrono roda antes da compactação, e a compactação espera por ele;
   - o processo separado do gatilho de escrita continua depois de o Claude Code ser fechado;
   - o JSON de entrada traz `session_id`, `transcript_path`, `cwd` e `trigger`;
   - a variável `CLAUDE_PID` aponta para o executável do Claude Code;
   - o arquivo de histórico mantém as mensagens anteriores à compactação depois dela.
5. Chamada real ao redator, com as opções da decisão C03, a partir do MacBook e da VPS. A resposta traz `structured_output` e `modelUsage` com `claude-sonnet-5-5`.
6. Remover o plugin de sonda dos 3 ambientes.

Se um item falhar em um ambiente, os requisitos que dependem dele ficam "bloqueados" naquele ambiente (G06), e o executor leva a pergunta ao proprietário no fim de U1 (G07).

## 10. Ações que passam pelo proprietário

O executor usa as credenciais do proprietário no MacBook (GitHub e Claude). Por isso, o limite vem de mecanismo do Claude Code: regras `ask` e `deny` no arquivo `.claude/settings.local.json` da cópia de trabalho, criado em U1 e não versionado. A sessão do executor não pode usar o modo `bypassPermissions`. O executor não edita esse arquivo depois de U1.

| Ação | Quem decide | Mecanismo |
| --- | --- | --- |
| Integrar a branch de trabalho na `main`, o que publica o plugin | Proprietário, com "sim" | Regra `ask` para `gh pr merge*` e para `git push* main*`. |
| Desinstalar plugins nos ambientes | Proprietário, com "sim" | Regra `ask` para `claude plugin uninstall*`. |
| Apagar pastas ou arquivos fora da cópia de trabalho e das pastas de teste, como a `venv` antiga | Proprietário, com "sim" | Regra `ask` para `rm *`. |
| Rodar o comando `migrar` nas pastas reais do formato antigo (U9), o que apaga os arquivos antigos | Proprietário, com "sim" | Regra `ask` para o comando `migrar` do programa. |
| Fechar o PR #1 e apagar a branch dele | Proprietário, com "sim" (P24 pendente) | Regra `ask` para `gh pr close*` e `git push* --delete*`. |
| Apagar repositório ou reescrever histórico | Ninguém nesta spec | Regra `deny` para `gh repo delete*` e `git push* --force*`. |
| Qualquer ação no repositório `hopper-documentation` | Ninguém nesta spec | Regra `deny` para comandos com `hopper-documentation.git` e `jonathanpah/hopper-documentation ` (com espaço no fim). |
| Gastar cota do plano com chamadas reais | Proprietário, pela aprovação desta spec | Limite de G06: até 40 chamadas reais ao redator e até 2 rodadas completas das avaliações de acionamento por execução. O registro de execução conta as chamadas. |

A sintaxe exata das regras segue `code.claude.com/docs/en/settings.md` na data da execução e fica registrada em `execucao/decisoes.md`.

Na operação normal do plugin, depois da entrega, a migração apaga os arquivos do formato antigo sem perguntar. Essa é a decisão P20. O mecanismo de segurança é R31.

## 11. Garantias

As garantias abaixo estão copiadas sem mudança da skill `hopper-spec-anth`, versão `0.2.0`. Depois de cada uma, a linha "Como esta spec cumpre" aponta a decisão de como.

# Garantias da spec

Toda spec copia esta lista sem mudança. Cada garantia é uma propriedade que se verifica, e não um mecanismo. O mecanismo que cumpre cada uma é uma decisão de como, escrita na spec. As garantias G01 a G05 valem sempre. As demais podem ficar como "não se aplica", com o motivo registrado.

Cada garantia traz o motivo que a sustenta. Uma garantia entra ou sai desta lista só com evidência de execução.

## G01. Quem executa não decide o pronto

**Garantia.** Um requisito está pronto só quando o seu verificador diz que está. O verificador é um programa, uma medição ou a aprovação do proprietário, e o executor não o controla.

**Motivo.** Sem verificação externa, quem executa tende a não achar os próprios erros e a declarar pronto sem prova.

**Prova.** A spec nomeia o verificador de cada requisito e mostra por que o executor não o controla.

**Como esta spec cumpre.** Decisão C17. Cada requisito da seção 5 nomeia o verificador. Os critérios ficam congelados (G03) e rodam no GitHub, fora da máquina do executor.

## G02. Requisito verificável

**Garantia.** Cada requisito tem identificador estável, 1 frase em voz ativa, quantidades com unidade e o verificador. Termo vago vira medida ou sai. Requisito sem verificador fica fora da spec.

**Motivo.** Requisito vago aceita qualquer entrega, e o executor preenche a lacuna por conta própria.

**Prova.** A conferência de todos os requisitos, feita na escrita da spec.

**Como esta spec cumpre.** Seção 5. Conferência registrada na seção 17.

## G03. Critérios congelados

**Garantia.** O executor não altera critérios, verificadores nem referências. Ele pode acrescentar verificadores, com registro. Mudar ou remover um verificador exige o proprietário. Diante de um verificador que reprova, o executor corrige a entrega, e nunca a expectativa.

**Motivo.** Executores pressionados para terminar chegam a alterar o próprio critério de aprovação.

**Prova.** A spec descreve o mecanismo de proteção e uma tentativa de alteração que ele barra ou detecta.

**Como esta spec cumpre.** Decisão C18.

## G04. Expectativa independente

**Garantia.** O resultado esperado vem de uma fonte que não é a própria entrega, por exemplo a spec, uma referência existente ou um cálculo feito à parte. Cada verificação nova falha sem a mudança que ela cobre.

**Motivo.** Uma verificação que repete a lógica da entrega passa sempre e não prova nada.

**Prova.** Cada verificador indica a fonte da expectativa, e a falha sem a mudança fica registrada.

**Como esta spec cumpre.** As expectativas vêm dos Anexos B, E e F e dos casos herdados do `hopper-documentation`. Em U2, o executor roda cada teste novo no código atual da `main` e registra a falha em `execucao/verificacoes.md`.

## G05. Prova registrada antes e depois de integrar

**Garantia.** Vale o registro da execução dos verificadores, e não o relato do executor. Antes de integrar uma mudança, rodam os verificadores que ela pode afetar, escolhidos por um mapa definido na spec. Sem mapa, rodam todos. Depois de integrar, todos os verificadores rodam juntos, e o executor segue o trabalho enquanto eles rodam. Uma falha nessa rodada completa suspende novas integrações até a mudança culpada ser corrigida ou desfeita. Uma falha que o mapa não previu atualiza o mapa, com registro. A entrega e as ações caras ou impossíveis de desfazer (G10), como publicar, só partem de uma versão em que todos os verificadores passaram juntos depois da última mudança. O que não rodou é "bloqueado", e nunca "passou". Uma verificação que não verificou nada é falha. Um resultado que oscila é repetido até mostrar estabilidade.

**Motivo.** Relatos de conclusão sem execução e verificações vazias são as formas mais comuns de falso pronto. Rodar todos os verificadores antes de cada integração deixa o executor parado à espera. A escolha pelo mapa antes e a rodada completa depois mantêm o trabalho andando e acham a falha antes de qualquer ação sem volta.

**Prova.** A spec diz onde fica o registro, como ele mostra quantas verificações rodaram, qual mapa escolhe os verificadores antes de integrar e como uma falha da rodada completa suspende as integrações seguintes.

**Como esta spec cumpre.** Decisões C17 e C19 e Anexo G.

## G06. Bloqueio e limites

**Garantia.** Cada requisito pode ficar "bloqueado", com motivo, evidência e o modo de reproduzir. Bloquear não é falha. Contornar o verificador é. As tentativas por falha, por unidade e por execução têm limite finito, definido na spec. As passadas de revisão por etapa também têm limite finito, definido na spec. Sem progresso, o executor para aquela parte e segue nas partes independentes. Uma verificação que passava e agora falha é regressão até prova em contrário.

**Motivo.** Sem saída honesta e sem limite, o executor contorna o verificador ou repete tentativas sem fim.

**Prova.** A spec fixa os limites e o formato do registro de bloqueio.

**Como esta spec cumpre.** Decisão C20.

## G07. Dúvida vira registro

**Garantia.** Durante a execução, a dúvida não para o trabalho. Se a spec tem regra para o caso, o executor aplica a regra e registra. Se não tem, ele bloqueia a parte, segue nas independentes e leva a pergunta ao proprietário no momento definido na spec.

**Motivo.** Perguntas no meio da execução param o trabalho, e decisões sem registro se perdem.

**Prova.** A spec define onde ficam as perguntas e quando o proprietário as recebe.

**Como esta spec cumpre.** As perguntas ficam em `execucao/perguntas.md`. O proprietário as recebe juntas, no chat da sessão do executor, no fim de cada unidade, numeradas e cada uma com a resposta recomendada.

## G08. Estado durável e retomada

**Garantia.** O plano, a situação de cada requisito, o registro de tentativas, as decisões, as perguntas e os achados fora do escopo ficam em meio durável, fora da memória do executor. Qualquer sessão retoma o trabalho a partir deles. Ao retomar, o executor confere de novo o estado externo. Operações repetidas não produzem efeito duplo. Cada item concluído tem um ponto de restauração.

**Motivo.** O contexto de quem executa acaba ou é trocado, e o trabalho não pode depender dele.

**Prova.** A spec indica onde fica cada registro e como uma sessão nova retoma.

**Como esta spec cumpre.** Decisão C21.

## G09. Revisão independente

**Garantia.** No fim de cada etapa, revisores sem o contexto de quem executou recebem só os critérios, a evidência bruta e a mudança, e nunca o resumo do executor. Eles apontam só falhas de requisito e de correção. Antes da revisão, 1 levantamento completo da parte afetada junta os defeitos em 1 lista. Cada passada olha só a mudança desde a passada anterior. Um achado de antes da etapa, ou fora do escopo dela, vira pendência registrada e não reabre a etapa. A revisão é triagem, e o verificador continua sendo quem decide o pronto. Um erro mecânico que se repete vira verificação automática.

**Motivo.** Quem fez o trabalho, e quem leu o resumo dele, tende a ver o que espera.

**Prova.** A spec define quem revisa, o que recebe e quando.

**Como esta spec cumpre.** Decisão C22.

## G10. Aprovação pelo custo de desfazer

**Garantia.** Ações caras ou impossíveis de desfazer passam pelo proprietário, por exemplo publicar, gastar, apagar, enviar mensagens ou mudar dados reais. Os limites vêm de mecanismo, e não só de texto. Credenciais ficam fora do alcance do executor.

**Motivo.** Uma instrução escrita não impede uma ação. Só um mecanismo impede.

**Prova.** Uma tabela de ações e responsáveis, com o mecanismo de cada limite.

**Como esta spec cumpre.** Seção 10. Limite conhecido: as credenciais do proprietário ficam no alcance do executor, porque o proprietário decidiu não executar nada (P18). O limite vem das regras `ask` e `deny` do Claude Code (risco K06).

## G11. Ambiente provado primeiro

**Garantia.** Antes do trabalho principal, uma unidade curta prova, executando, que cada caminho necessário funciona, como ferramentas, acessos e destinos. As versões em uso ficam registradas.

**Motivo.** Uma falha de ambiente descoberta no meio do trabalho custa mais e se confunde com uma falha da entrega.

**Prova.** A 1ª unidade da spec é essa prova, com o registro do resultado.

**Como esta spec cumpre.** Unidade U1.

## G12. Defeito vira verificador

**Garantia.** Todo defeito encontrado depois da entrega vira primeiro uma verificação que falha sem a correção. Depois de revisada, ela entra nos critérios congelados (G03). Um defeito que escapou dos verificadores gera uma prevenção registrada.

**Motivo.** Sem isso, o mesmo defeito volta.

**Prova.** A spec descreve o caminho de um defeito relatado até o novo verificador.

**Como esta spec cumpre.** Seção 14.

## G13. Um responsável por item

**Garantia.** Cada item alterável tem um único responsável por vez. O trabalho em paralelo acontece só em frentes independentes, integradas uma de cada vez.

**Motivo.** 2 responsáveis pelo mesmo item perdem o trabalho um do outro.

**Prova.** A divisão das unidades mostra o responsável de cada item.

**Como esta spec cumpre.** Uma única sessão do executor faz as unidades em sequência e é a responsável por todos os arquivos. Subagentes só leem e revisam.

## G14. Mecanismo extra só com evidência

**Garantia.** A spec começa com o mínimo que cumpre estas garantias. Um mecanismo extra entra quando os registros da execução mostram a falha que ele evita. Metas impossíveis ficam fora da spec e viram "bloqueado" ou saem do escopo.

**Motivo.** Mecanismo em excesso custa manutenção, e uma meta impossível empurra o executor a contornar o verificador.

**Prova.** Cada mecanismo da spec aponta a garantia, o requisito ou a evidência que o justifica.

**Como esta spec cumpre.** Cada decisão de como aponta o requisito ou a garantia. Ficam de fora, até existir evidência: correção automática do estilo pelo redator, nova chamada ao redator por conteúdo fraco, injeção de contexto no início da sessão e memória com busca.

## G15. Como fixo durante a execução

**Garantia.** As decisões de como da spec valem durante toda a execução. Elas são revistas só entre etapas, com registro. Trocar um mecanismo de verificação exige o proprietário.

**Motivo.** Trocar o mecanismo no meio da execução impede comparar rodadas e pode enfraquecer um verificador sem ninguém perceber.

**Prova.** A spec indica quando as decisões de como podem ser revistas e por quem.

**Como esta spec cumpre.** O executor revê uma decisão de como só entre unidades, com o motivo e a evidência em `execucao/decisoes.md`. Trocar C17, C18 ou o conferidor exige o "sim" do proprietário.

## 12. Decisões de como

Fontes lidas em 2026-11-01, salvo outra data indicada.

**C01. Leitura direta do arquivo de histórico.**
- Atende a: R04 a R10, P06.
- Alternativas: Agent SDK (`get_session_messages`), comando `/export`, leitura direta.
- Fontes: `code.claude.com/docs/en/sessions.md` (formato interno, sujeito a mudança); `code.claude.com/docs/en/agent-sdk/sessions.md`; README do anth na `main`, commit `8dbb40b` (o Agent SDK lê só desde a última compactação e exige Python 3.10 e cerca de 55 MB); código do `hopper-documentation`, commit `8c2e438` (leitor com 57 testes); `code.claude.com/docs/en/commands.md` (`/export` só pelo usuário).
- Motivo: a leitura direta não instala nada, roda com Python 3.9 e já tem testes. O `/export` não pode ser acionado pelo programa.
- Prova: T04 a T10 e U1, item 4 (mensagens antigas mantidas depois da compactação).

**C02. Gatilho com 2 comandos no `PreCompact`.**
- Atende a: R22, R23, R24, P10, P14.
- Decisão: um comando síncrono (gatilho de cópia, tempo-limite de 60 segundos) e um comando com `async: true` e `asyncRewake: true` (gatilho de escrita, tempo-limite de 3.600 segundos). O gatilho de escrita inicia a rodada em processo separado, espera o fim dela, sai com código 0 em sucesso e com código 2 e o motivo na saída de erro em falha.
- Alternativas: 1 comando síncrono que faz tudo, 1 comando assíncrono que faz tudo, gatilho `PostCompact`, gatilho `SessionStart`.
- Fontes: `code.claude.com/docs/en/hooks.md` (gatilhos do mesmo evento rodam em paralelo; gatilho síncrono bloqueia até terminar; código 2 bloqueia a compactação no `PreCompact`; `asyncRewake` acorda o Claude com código 2; a página indica processo totalmente separado para trabalho que deve sobreviver).
- Motivo: a cópia precisa acontecer antes da compactação, e a escrita leva minutos e não pode atrasar a compactação.
- Prova: U1, item 4, e T22 a T24.

**C03. Chamada ao redator.**
- Atende a: R12, N04, N08.
- Decisão: `claude -p --model claude-sonnet-5-5 --effort high --tools "" --strict-mcp-config --disable-slash-commands --no-session-persistence --output-format json --json-schema <Anexo D> --system-prompt <instrução do redator>`, com as variáveis `CLAUDE_CODE_SAFE_MODE=1`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` e `HOPPER_DOCUMENTATION_ANTH_RUN=1`. A entrada vai pela entrada padrão. O processo roda na pasta de dados, e não na pasta do projeto. Tempo-limite de 15 minutos por chamada.
- Alternativas: `--bare` (exige chave de API), subagente com `context: fork` (não pode ser chamado por gatilho), API com chave (o proprietário usa assinatura).
- Fontes: `code.claude.com/docs/en/cli-reference.md`, `env-vars.md` e `headless.md` (modo seguro mantém a autenticação e desliga CLAUDE.md, skills, plugins, gatilhos, MCP e memória automática; sem modo seguro, `-p` roda gatilhos do projeto); `model-config.md` (Sonnet 5.5 exige Claude Code 2.1.284 ou mais novo); código do anth na `main` (mesma chamada em uso).
- Motivo: usa a assinatura do proprietário e isola o redator de tudo o que não é o material enviado.
- Prova: T12 e U1, item 5.

**C04. Regra de modelo.**
- Atende a: R12, N04, P04.
- Decisão: o programa aceita a resposta só quando `modelUsage` contém `claude-sonnet-5-5` e esse modelo responde por no mínimo 90% dos tokens de saída. Outros modelos listados entram no registro de rodadas. Sem acesso ao Sonnet 5.5, a rodada falha e não usa outro modelo.
- Alternativas: exigir só o Sonnet 5.5 na lista, como faz a versão atual; não conferir.
- Fontes: código do anth na `main` (conferência estrita); `headless.md` (formato da saída JSON).
- Motivo: o Claude Code pode listar modelos auxiliares. A regra de 90% mantém a garantia de autoria sem falhas por modelos auxiliares.
- Prova: T12 e U1, item 5.

**C05. Saída estruturada e gravação pelo programa.**
- Atende a: R13 a R18, R29, N02, N03.
- Decisão: o redator devolve o JSON do Anexo D. O programa valida o JSON, troca as referências provisórias (`N1`, `N2`…) pelos identificadores finais, grava os arquivos e confere a gravação. O redator não recebe ferramenta de gravação.
- Alternativas: o redator edita os arquivos com as ferramentas Write e Edit.
- Fontes: `anthropic.com/engineering/effective-harnesses-for-long-running-agents` (o modelo altera JSON por engano com menos frequência do que Markdown); `github.com/steveyegge/beads` e `github.com/github/spec-kit` (identificadores atribuídos por programa).
- Motivo: números estáveis, nenhuma gravação fora das pastas permitidas e gravação repetível.
- Prova: T13 a T18 e T29.

**C06. Identificadores e numeração.**
- Atende a: R05, R14, P12.
- Decisão: mensagens `M<n>-<código>`, numeradas de 1 em 1 por conversa. Itens `D<n>-<código>`, `F<n>-<código>` e `PD<n>-<código>`, com n igual ao maior número existente daquele tipo e daquele código, mais 1. Os mesmos prefixos valem no pacote em inglês.
- Alternativas: identificadores por hash, como o beads.
- Fontes: decisão P12; `github.com/steveyegge/beads`.
- Motivo: o código da conversa evita números repetidos entre conversas, e o número sequencial fica legível.
- Prova: T05 e T14.

**C07. Travas.**
- Atende a: R27, R29, R22.
- Decisão: 3 travas `flock` na pasta de dados. A trava de cópia, por conversa, é usada só durante a cópia. A trava de rodada, por conversa, cobre a chamada ao redator. A trava de pasta, por pasta de documentação, cobre a gravação dos documentos compartilhados.
- Alternativas: 1 trava por pasta para tudo.
- Fontes: código do anth na `main` (trava `flock` na pasta de dados); `hooks.md` (os 2 comandos do gatilho rodam em paralelo).
- Motivo: o gatilho de cópia nunca espera uma chamada ao redator, e 2 conversas da mesma pasta não gravam os documentos 1, 4, 5 e 6 ao mesmo tempo.
- Prova: T22 e T27.

**C08. Processo separado.**
- Atende a: R23.
- Decisão: o gatilho de escrita inicia o comando `rodada` com `subprocess.Popen(..., start_new_session=True)`, com a saída no registro de rodadas, e espera o fim dele.
- Alternativas: `nohup`; `setsid`, que não existe no macOS.
- Fontes: `hooks.md` (processo totalmente separado); documentação do módulo `subprocess` do Python (`start_new_session` funciona em macOS e Linux).
- Motivo: funciona nas 2 máquinas sem programa externo.
- Prova: U1, item 4, e U8.

**C09. Espera pela gravação do histórico.**
- Atende a: R04, K02.
- Decisão: antes de ler, o copiador confere o tamanho do arquivo de histórico a cada 0,5 segundo. A leitura começa quando o tamanho fica igual por 1 segundo, ou depois de 5 segundos.
- Alternativas: ler sem esperar; esperar um tempo fixo.
- Fontes: `hooks.md` (o arquivo de histórico é gravado de forma assíncrona e pode estar atrasado em relação à conversa).
- Motivo: pega as últimas mensagens na maioria dos casos e cabe no tempo-limite de 60 segundos do gatilho de cópia.
- Prova: T04, com um arquivo que cresce durante a cópia.

**C10. Ponto de retomada da cópia.**
- Atende a: R04, N01.
- Decisão: cada mensagem do documento 2 guarda, em um comentário, os identificadores do primeiro e do último registro que ela cobre. A cópia seguinte começa no registro depois do último identificador da última mensagem.
- Alternativas: arquivo de estado separado na pasta de dados; data e hora da última mensagem.
- Fontes: decisão P02; código do anth na versão atual (retomada pelo identificador do último registro).
- Motivo: o documento 2 se basta, sem arquivo de estado, e o identificador de um registro não se repete.
- Prova: T04.

**C11. Localização do arquivo de histórico e da pasta do projeto.**
- Atende a: R02, R37.
- Decisão: no gatilho, o campo `transcript_path` da entrada. Na skill, a busca por `<pasta de configuração>/projects/*/<identificador>.jsonl`, com `${CLAUDE_SESSION_ID}`. O programa confere que o `sessionId` dos registros mais recentes é o da conversa. A pasta do projeto é o `cwd` do primeiro registro do arquivo.
- Alternativas: a pasta atual do processo; a variável `CLAUDE_PROJECT_DIR`.
- Fontes: `hooks.md`; `sessions.md`; `env-vars.md` (`CLAUDE_CONFIG_DIR`); código do `hopper-documentation` (`find_transcript` e `verify_identity`).
- Motivo: o primeiro registro dá a mesma pasta ao gatilho e à skill, mesmo que o Claude mude de pasta durante a conversa.
- Prova: T37 e U1, item 4.

**C12. Executável do Claude Code.**
- Atende a: R38.
- Decisão: o programa usa o executável indicado por `CLAUDE_PID` (por `/proc/<pid>/exe` no Linux e por `ps -o comm=` no macOS). Depois, o `claude` do `PATH`. Depois, `~/.local/bin/claude`.
- Alternativas: só o `claude` do `PATH`.
- Fontes: código do anth na versão atual (`find_claude`); `desktop.md` (a aba Code roda uma cópia própria do Claude Code); `troubleshoot-install.md` (a instalação nativa fica em `~/.local/bin/claude`).
- Motivo: no Desktop, o `claude` do `PATH` pode ser outra versão ou não existir.
- Prova: T38 e U1, item 4.

**C13. Ocultação.**
- Atende a: R07, N05, P07.
- Decisão: copiar a função `mask` do `hopper-documentation` e os testes dela.
- Alternativas: a função de ocultação da versão atual do anth, com menos casos de teste.
- Fontes: código do `hopper-documentation`, commit `8c2e438`, classe de testes `Masking`, com mais de 40 casos; código do anth na versão atual.
- Motivo: é a ocultação com mais casos testados, inclusive textos comuns que não podem ser ocultados.
- Prova: T07.

**C14. Regras de escrita para o redator.**
- Atende a: R19, P03, P21.
- Alternativas: enviar o texto original do proprietário, com as repetições; conferir o estilo e pedir correção automática ao redator.
- Decisão: o Anexo A vai no arquivo `regras-de-escrita.md` (inglês: `writing-rules.md`) da skill, e o Anexo E vai no arquivo `modelos.md` (inglês: `templates.md`). O programa envia os 2 ao redator. O conferidor mede só as regras contáveis (R19).
- Fontes: ASD-STE100 Issue 9, de 2025-01-15 (`tcworld.info`, `simplified-english.co.uk/rules-ste9.html`): até 20 palavras por frase em instruções, até 25 em descrições e até 6 frases por parágrafo; Lei 15.263/2025 (linguagem simples); ISO 24495-1; estudos de seguimento de instruções (`arxiv.org/abs/2509.21051`: o cumprimento cai quando o número de regras sobe; `arxiv.org/abs/2505.16234`: limites de tamanho são seguidos com pouca confiança).
- Motivo: uma lista única e curta é cumprida melhor. O limite de 25 e 40 palavras do conferidor aceita a variação que os estudos mostram.
- Prova: conferidor, verificação F7, nas pastas do aceite.

**C15. Formato da skill.**
- Atende a: R25, R26, R41, P05.
- Decisão: o SKILL.md tem o nome `hopper-documentation-anth`, a descrição do Anexo E e as seções "O que a skill produz" e "Como a skill roda". A skill aceita acionamento pelo modelo (sem `disable-model-invocation`), para que um pedido em linguagem natural funcione. Ela roda `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hopper_documentation_anth.py" rodada --sessao "${CLAUDE_SESSION_ID}"` em segundo plano e informa a linha final.
- Alternativas: skill com `context: fork` e `model: sonnet`, rodando em subagente; skill acionada só pelo comando `/`.
- Fontes: `code.claude.com/docs/en/skills.md` (substituições `${CLAUDE_SESSION_ID}` e `${CLAUDE_PLUGIN_ROOT}`, limite recomendado de 500 linhas, `disable-model-invocation`); `tools-reference.md` (Bash em segundo plano sem limite de tempo no terminal e no Desktop); avaliações de acionamento do anth na versão atual.
- Motivo: o mesmo comando atende o gatilho e o pedido, e o resultado é igual nos 2 caminhos (P10, P14).
- Prova: T41 e avaliações de acionamento.

**C16. Pacotes e instalação.**
- Atende a: R35, R39, P19.
- Decisão: manter as 2 pastas de idioma, cada uma com plugin e catálogo (marketplace) completos, como hoje. A instalação clona o repositório e adiciona a pasta do idioma como catálogo (Anexo H). Em A2, o executor confere se o plugin instalado pela CLI aparece no Desktop. Se não aparecer, instala pelo botão "+" e pela opção "Add plugins" da aba Code, com o uso do computador. Se o Desktop não aceitar um catálogo local, o executor cria `.claude-plugin/marketplace.json` na raiz do repositório, apontando para a pasta em português, e registra a mudança.
- Alternativas: 1 pacote só, com o idioma escolhido por configuração; catálogo só na raiz do repositório.
- Fontes: `code.claude.com/docs/en/plugins/cli-reference.md` (`marketplace add` aceita pasta local e repositório do GitHub; `install`, `update`, `list`, `details`); `desktop.md` (instalação pelo "+"; plugins carregam em sessões locais); `support.claude.com/en/articles/13837440-use-plugins-in-claude`; README do anth na versão atual.
- Motivo: o formato atual já foi instalado e usado no terminal e no Desktop, e o proprietário manteve os 2 idiomas (P19).
- Prova: roteiro de aceite, passo F-I.

**C17. Verificadores e verificação completa.**
- Atende a: G01, G05, R36.
- Decisão: a verificação do GitHub roda em todo envio à branch de trabalho e em todo PR. Ela roda os testes dos 2 pacotes em Ubuntu e macOS, com Python 3.9 e 3.13, o conferidor nos casos de `aceite/casos/`, a conferência do manifesto (C18) e o teste de inventário (T32). Na máquina do executor, antes de integrar, rodam os verificadores do mapa do Anexo G. A conferência de plugin roda com `claude plugin validate --strict` nos 2 pacotes.
- Alternativas: só testes na máquina do executor.
- Fontes: CONTRIBUTING do anth na versão atual (testes e validação de plugin); documentação do GitHub Actions.
- Motivo: a verificação completa roda fora da máquina do executor, e o registro dela fica no GitHub.
- Prova: execução registrada no GitHub e em `execucao/verificacoes.md`, com o total de verificações rodadas, aprovadas, reprovadas e bloqueadas.

**C18. Congelamento dos critérios.**
- Atende a: G03, N10.
- Decisão: em U2, o executor grava o SHA-256 de cada arquivo de `aceite/`, de `.github/workflows/verificar.yml` e de `SPEC.md` em `aceite/MANIFESTO.sha256`. A verificação do GitHub falha com a mensagem "CRITÉRIO ALTERADO" se algum desses arquivos mudar. Atualizar o manifesto exige o "sim" do proprietário, em commit próprio com a mensagem "Atualiza critérios congelados, aprovado por Jonathan em <data>". O revisor (C22) aponta qualquer mudança nesses arquivos.
- Alternativas: proteção de branch no GitHub com aprovação obrigatória do proprietário; arquivos só de leitura na máquina do executor.
- Fontes: garantia G03 da skill `hopper-spec-anth` 0.2.0; documentação do GitHub Actions (um passo que falha reprova a verificação).
- Motivo: a proteção de branch exigiria trabalho do proprietário no GitHub (P18). O manifesto detecta qualquer mudança sem trabalho dele.
- Prova: em U2, o executor altera 1 caractere de um caso de `aceite/casos/` em uma branch descartável, registra a falha "CRITÉRIO ALTERADO" e apaga a branch.

**C19. Integração e suspensão.**
- Atende a: G05.
- Decisão: integrar é enviar commits à branch de trabalho. Se a verificação completa do GitHub falhar, o executor só envia a correção ou a reversão da mudança culpada até a verificação completa passar. Uma falha que o mapa do Anexo G não previu atualiza o mapa, com registro. A integração na `main` (U10) só parte de um commit em que a verificação completa passou depois da última mudança.
- Alternativas: integrar direto na `main` a cada unidade.
- Fontes: garantia G05 da skill `hopper-spec-anth` 0.2.0.
- Motivo: a branch de trabalho isola a versão nova da `main`, que continua instalada nos ambientes do proprietário até U10.
- Prova: `execucao/verificacoes.md` e o histórico da verificação do GitHub.

**C20. Bloqueio e limites.**
- Atende a: G06, K09.
- Decisão: até 3 tentativas por falha, até 10 tentativas por unidade, até 2 passadas de revisão por unidade, até 40 chamadas reais ao redator e até 2 execuções completas das avaliações de acionamento por execução da spec. Com 2 unidades bloqueadas sem progresso, o executor para e leva as perguntas ao proprietário. O bloqueio é registrado em `execucao/estado.md` no formato `<ID> · bloqueado · motivo · evidência (comando e saída) · como reproduzir`.
- Alternativas: sem limite de chamadas reais; limite por tempo.
- Fontes: garantia G06 da skill `hopper-spec-anth` 0.2.0.
- Motivo: os limites param repetições sem progresso e mantêm previsível o gasto da cota.
- Prova: `execucao/tentativas.md`, com a contagem de tentativas e de chamadas reais.

**C21. Estado durável e retomada.**
- Atende a: G08.
- Decisão: a pasta `execucao/` da branch de trabalho guarda `estado.md` (plano e situação de cada requisito: pendente, em andamento, pronto com o verificador e o registro, ou bloqueado), `tentativas.md`, `decisoes.md`, `perguntas.md`, `fora-do-escopo.md`, `verificacoes.md` (só acréscimos), `versoes.md` e `revisoes/`. Cada item concluído tem um commit, que é o ponto de restauração. Uma sessão nova lê `SPEC.md` e `execucao/`, confere de novo o estado externo (git, verificação do GitHub e instalação nos 3 ambientes) e continua. A instalação e as rodadas são repetíveis sem efeito duplo (R29). Em U10, a pasta `execucao/` sai da branch antes da integração, e o histórico do PR a preserva.
- Alternativas: estado só na descrição do PR no GitHub.
- Fontes: garantia G08 da skill `hopper-spec-anth` 0.2.0.
- Motivo: arquivos na branch de trabalho sobrevivem ao fim da sessão e ficam junto do código.
- Prova: em U1, o executor encerra a sessão, abre outra, retoma pela leitura de `SPEC.md` e `execucao/` e registra o resultado.

**C22. Revisão independente.**
- Atende a: G09.
- Decisão: no fim de cada unidade, o executor roda o levantamento completo (todos os testes, o conferidor e o inventário) e junta os defeitos em 1 lista. Depois, abre um subagente sem o contexto da sessão e entrega a ele o texto dos requisitos da unidade copiado desta spec, a saída bruta dos verificadores e o `git diff` desde o início da unidade. O revisor aponta só falhas de requisito e de correção. A 2ª passada olha só o que mudou desde a 1ª. Achados fora da unidade vão para `execucao/fora-do-escopo.md`.
- Alternativas: revisão pelo próprio executor; revisão pelo proprietário.
- Fontes: garantia G09 da skill `hopper-spec-anth` 0.2.0; ferramenta Agent do Claude Code (subagente sem o contexto da sessão).
- Motivo: o revisor não lê o resumo do executor, e o proprietário não executa tarefas (P18).
- Prova: a saída de cada revisão fica em `execucao/revisoes/<unidade>.md`.

## 13. Riscos

| ID | Risco | Tratamento |
| --- | --- | --- |
| K01 | O formato do arquivo de histórico muda em uma atualização do Claude Code. A Anthropic declara esse formato como interno. | Testes com registros reais. U1 registra a versão. O programa falha com a mensagem "formato do histórico não reconhecido". A correção segue a seção 14. |
| K02 | O arquivo de histórico é gravado com atraso, e as últimas mensagens antes da compactação ainda não estão nele. | Espera de C09. As mensagens que chegarem depois entram na rodada seguinte. |
| K03 | O Claude Desktop não dispara o `PreCompact` ou não carrega o plugin instalado pela CLI. A documentação não confirma o gatilho no Desktop. | U1 prova logo no início. Se falhar, A2 fica bloqueado com evidência, e a pergunta vai ao proprietário no fim de U1. |
| K04 | O modo seguro é descrito na documentação como recurso de solução de problemas e pode mudar. | U1 prova. T12 confere as opções. A regra de C04 descarta respostas de outro modelo. |
| K05 | O Claude Code apaga arquivos de histórico com mais de 30 dias. | A cópia roda antes de toda compactação. O README avisa. A rodada a pedido em conversa antiga falha com motivo claro. |
| K06 | O executor usa as credenciais do proprietário. | Regras `ask` e `deny` da seção 10. Cada ação da seção 10 fica registrada em `execucao/estado.md`. |
| K07 | A migração apaga informação útil. | R31, casos B3 com os 2 formatos antigos e U9 só depois do aceite. |
| K08 | O uso do computador não está disponível para conduzir o Desktop em A2. | U1 prova. Se faltar, os requisitos de A2 que dependem dele ficam bloqueados, e a pergunta vai ao proprietário. |
| K09 | As rodadas consomem a cota do plano do proprietário. | Limite de C20 durante a execução. Na operação, 1 rodada por compactação ou por pedido. |

## 14. Correções depois da entrega

1. O defeito chega por issue no GitHub ou por mensagem do proprietário.
2. O executor escreve um teste que falha na `main` atual e registra a falha.
3. O executor corrige em uma branch nova e roda os verificadores do mapa.
4. Um revisor sem contexto revisa a correção (C22).
5. Com o "sim" do proprietário, o teste entra nos critérios congelados (C18) e a correção é integrada.
6. Se o defeito escapou dos verificadores, o executor registra a prevenção no CONTRIBUTING dos 2 idiomas.

## 15. Pendências para o proprietário

1. **Fechar o PR #1 (P24).** O que está pendente: confirmar o fechamento sem integração. Recomendação: fechar, porque a versão nova substitui o código que ele corrige e "Nao guardamos lixo". O que precisa do proprietário: "sim" ou "não". Até a resposta, R34 fica bloqueado, e o resto da execução segue.

## 16. Skill usada

`hopper-spec-anth`, versão `0.2.0`.

## 17. Conferência da spec

Esta seção é preenchida na conferência da escrita (passo 5 da skill) e registra o resultado da leitura por um leitor sem contexto.

---

## Anexo A. Regras de escrita

Origem: texto do proprietário (P03), sem as repetições (P21). Valem para os documentos 3 a 7. O pacote em inglês usa a tradução fiel desta lista.

Formato amigável para TDAH, sem infantilizar nem sacrificar a precisão.

1. Comece pela conclusão. Depois, explique só o necessário, em ordem lógica e sem pular etapas indispensáveis.
2. Escreva para um leitor inteligente que não conhece o tema. Não infantilize e não presuma conhecimento técnico.
3. Comece cada bloco da conversa simplificada com 1 linha que diz o assunto.
4. Escreva uma ideia por frase e um assunto por parágrafo, com até 6 frases.
5. Use até 20 palavras por frase em instruções e até 25 em explicações.
6. Escreva uma ação por instrução, com o verbo no imperativo.
7. Use voz ativa e ordem direta, sem frases intercaladas.
8. Use palavras comuns e literais, sem jargão, e o mesmo termo para o mesmo conceito.
9. Explique cada termo técnico ou sigla na primeira vez em que aparecer.
10. Prefira verbos a substantivos. Por exemplo, "verificar", e não "fazer a verificação".
11. Corte introduções, repetições, redundâncias, floreios, tangentes, recapitulações, exemplos dispensáveis e encerramentos genéricos.
12. Nunca omita fatos, números, riscos, limites, ressalvas ou conceitos. Cortar redundância não pode apagar um conceito.
13. Use títulos e listas só quando facilitarem a leitura. Destaque em negrito o que o leitor deve reter.
14. Cada pendência traz o que está pendente, a recomendação e o que depende do usuário. Sugestão não é pendência.

**Regras de fidelidade**, aproveitadas da versão atual (P20):

15. Diferencie fato, relato, proposta e decisão. Sem evidência na conversa, escreva "relatado, não verificado".
16. Uma autorização vale só no alcance dito. Registrar uma pendência não autoriza executá-la.
17. A última versão de um fato prevalece em todos os documentos. Falta de registro não prova que algo não aconteceu.
18. Toda afirmação dos documentos 3 a 7 cita a mensagem de origem.

**Frases do texto do proprietário que ficam fora** (P21), porque valem só para respostas no chat:

- "não peça nova validação do que já foi confirmado".
- "só faça perguntas quando faltar informação essencial ou existir uma decisão relevante".
- "Este pedido autoriza apenas a reescrita da resposta, não a execução de comandos, a alteração de arquivos ou qualquer ação em sistemas." Na skill, essa frase proibiria a gravação dos documentos.

## Anexo B. Casos de teste

Os testes rodam com `TZ=UTC`. O identificador da conversa dos casos é `3f9c2a71-5b8e-4d0a-9c61-2e7f4b1a8d05`, e a pasta do projeto é `/tmp/projeto-teste`.

### B1. Arquivo de histórico sintético

Cada linha abaixo é um registro do arquivo `historico.jsonl`. Os campos `sessionId` (com o identificador acima) e `cwd` (com `/tmp/projeto-teste`) estão em todos os registros e foram omitidos aqui para facilitar a leitura.

```jsonl
{"type":"user","uuid":"u1","timestamp":"2026-03-14T15:00:00.000Z","message":{"role":"user","content":[{"type":"text","text":"Quero seguir o sitema, claro ou escuro.\n<system-reminder>lembrete interno</system-reminder>"},{"type":"image","source":{"type":"base64","media_type":"image/png","data":"iVBORw0KGgo="}}]}}
{"type":"assistant","uuid":"a1","timestamp":"2026-03-14T15:00:05.000Z","message":{"role":"assistant","content":[{"type":"thinking","thinking":"raciocínio interno"},{"type":"text","text":"Vou criar o arquivo."}]}}
{"type":"assistant","uuid":"a2","timestamp":"2026-03-14T15:00:06.000Z","message":{"role":"assistant","content":[{"type":"tool_use","id":"toolu_1","name":"Write","input":{"file_path":"/tmp/projeto-teste/nota.txt","content":"teste"}}]}}
{"type":"user","uuid":"u2","timestamp":"2026-03-14T15:00:07.000Z","message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"toolu_1","content":"File created"}]}}
{"type":"assistant","uuid":"a3","timestamp":"2026-03-14T15:00:08.000Z","message":{"role":"assistant","content":[{"type":"tool_use","id":"toolu_2","name":"Bash","input":{"command":"ls -la","description":"Lista os arquivos da pasta"}}]}}
{"type":"user","uuid":"u3","timestamp":"2026-03-14T15:00:09.000Z","message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"toolu_2","content":"nota.txt"}]}}
{"type":"assistant","uuid":"a4","timestamp":"2026-03-14T15:00:10.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Arquivo criado."}]}}
{"type":"user","uuid":"u4","timestamp":"2026-03-14T15:01:00.000Z","message":{"role":"user","content":"a senha do servidor é Pl4nt@d4#2026 hoje"}}
{"type":"user","uuid":"u5","timestamp":"2026-03-14T15:01:30.000Z","message":{"role":"user","content":"<task-notification>tarefa concluída</task-notification>"}}
{"type":"attachment","uuid":"q1","timestamp":"2026-03-14T15:02:00.000Z","attachment":{"type":"queued_command","commandMode":"prompt","prompt":"Fica pendente escolher o formato do gráfico."}}
{"type":"user","uuid":"u6","timestamp":"2026-03-14T15:02:30.000Z","message":{"role":"user","content":[{"type":"text","text":"[Request interrupted by user]"}]}}
{"type":"user","uuid":"u7","timestamp":"2026-03-14T15:03:00.000Z","isCompactSummary":true,"message":{"role":"user","content":"Resumo da compactação"}}
{"type":"assistant","uuid":"s1","timestamp":"2026-03-14T15:03:10.000Z","isSidechain":true,"message":{"role":"assistant","content":[{"type":"text","text":"texto de subagente"}]}}
{"type":"user","uuid":"u8","timestamp":"2026-03-14T15:04:00.000Z","message":{"role":"user","content":"Another Claude session sent a message:\n<agent-message from=\"x\">Relatório pronto.</agent-message>"}}
```

**Documento 2 esperado (pacote em português).** Esta é a saída literal do corpo, depois do cabeçalho do arquivo do Anexo E.

```markdown
## M1-3f9c2a71 · 2026-03-14 15:00 +00:00 · Usuário
<!-- registros: u1 u1 -->

Quero seguir o sitema, claro ou escuro.

[imagem anexada]

## M2-3f9c2a71 · 2026-03-14 15:00 +00:00 · Claude
<!-- registros: a1 a4 -->

Vou criar o arquivo.

Ferramenta: Write · /tmp/projeto-teste/nota.txt

Ferramenta: Bash · Lista os arquivos da pasta

Arquivo criado.

## M3-3f9c2a71 · 2026-03-14 15:01 +00:00 · Usuário
<!-- registros: u4 u4 -->

a senha do servidor é [oculto] hoje

## M4-3f9c2a71 · 2026-03-14 15:02 +00:00 · Usuário
<!-- registros: q1 q1 -->

Fica pendente escolher o formato do gráfico.

## M5-3f9c2a71 · 2026-03-14 15:02 +00:00 · Evento
<!-- registros: u6 u6 -->

O usuário interrompeu a resposta.

## M6-3f9c2a71 · 2026-03-14 15:04 +00:00 · Relato de agente
<!-- registros: u8 u8 -->

Another Claude session sent a message:
<agent-message from="x">Relatório pronto.</agent-message>
```

Regras que o caso mostra:

- Uma mensagem do Claude junta os textos e as linhas de ferramenta seguidos do Claude, até a próxima mensagem de outro autor ou até o fim da cópia.
- O comentário de registros traz o primeiro e o último registro cobertos pela mensagem.
- A hora do cabeçalho é a do primeiro registro da mensagem.
- O alvo da linha de ferramenta é o primeiro destes campos que existir: `description`, `file_path`, `pattern`, `url`, `query`, `skill`, `command`.

**Segunda rodada.** Depois de acrescentar ao arquivo o registro abaixo, a segunda rodada acrescenta só a mensagem M7, e os bytes das mensagens M1 a M6 ficam iguais.

```jsonl
{"type":"user","uuid":"u9","timestamp":"2026-03-14T15:10:00.000Z","message":{"role":"user","content":"Decidimos usar a cor azul no painel."}}
```

```markdown
## M7-3f9c2a71 · 2026-03-14 15:10 +00:00 · Usuário
<!-- registros: u9 u9 -->

Decidimos usar a cor azul no painel.
```

**Respostas a perguntas e planos aprovados.** O teste T08 também usa os casos herdados `test_structured_answers_and_approved_plan` e `test_messages_sent_while_the_assistant_works` do `hopper-documentation`. Nesses casos, o autor é "Resposta do usuário" ou "Plano aprovado", e o texto segue o formato herdado.

### B2. Ocultação

O teste T07 usa todos os casos da classe `Masking` do `hopper-documentation` (commit `8c2e438`) e mais estes 3:

| Entrada | Saída esperada |
| --- | --- |
| `a senha do servidor é Pl4nt@d4#2026 hoje` | `a senha do servidor é [oculto] hoje` |
| `Quero seguir o sitema, claro ou escuro.` | `Quero seguir o sitema, claro ou escuro.` |
| `Troque a senha e apague o rascunho; o token e a chave ficam no cofre.` | `Troque a senha e apague o rascunho; o token e a chave ficam no cofre.` |

### B3. Formato antigo

O executor cria 2 pastas de teste com arquivos do formato antigo:

- uma com 2 handoffs no formato do anth na `main` (nome `handoff-AAAAMMDD-HHMMSS-<8 caracteres>.md`, cabeçalho com "Conversa") e o `index.md` dele;
- uma com 2 handoffs no formato do `hopper-documentation` (nome `handoff-AAAAMMDD-HHMMSS.md`, cabeçalho com "Conversa: Claude <identificador>" e "Conversa: Codex <identificador>") e o `index.md` dele.

Os arquivos são gerados pelo código real de cada versão, a partir de conversas sintéticas com pelo menos 1 decisão, 1 pendência e 1 entrega. Expectativa de T30 com redator simulado: os documentos 4, 5 e 6 têm itens com a origem igual ao nome de cada arquivo antigo, cada conversa antiga tem o documento 7 na pasta dela, e não sobra nenhum arquivo do formato antigo.

## Anexo C. Inventário do repositório depois da entrega

T32 aceita só estes caminhos. `**` vale para qualquer arquivo abaixo da pasta.

```text
.github/ISSUE_TEMPLATE/bug-report.yml
.github/ISSUE_TEMPLATE/change-proposal.yml
.github/pull_request_template.md
.github/workflows/verificar.yml
.gitignore
CODE_OF_CONDUCT.md
CONTRIBUTING.md
LICENSE
README.md
SECURITY.md
SPEC.md
index.md
aceite/conferir.py
aceite/MANIFESTO.sha256
aceite/casos/**
<pacote>/.claude-plugin/plugin.json
<pacote>/.claude-plugin/marketplace.json
<pacote>/hooks/hooks.json
<pacote>/scripts/hopper_documentation_anth.py
<pacote>/skills/hopper-documentation-anth/SKILL.md
<pacote>/skills/hopper-documentation-anth/LICENSE
<pacote>/skills/hopper-documentation-anth/<regras>
<pacote>/skills/hopper-documentation-anth/<modelos>
<pacote>/tests/test_hopper_documentation_anth.py
<pacote>/evals/**
<pacote>/.gitignore
<pacote>/LICENSE
<pacote>/README.md
<pacote>/index.md
hopper-documentation-anth-pt-br/CODE_OF_CONDUCT.md
hopper-documentation-anth-pt-br/CONTRIBUTING.md
hopper-documentation-anth-pt-br/SECURITY.md
hopper-documentation-anth-pt-br/.github/**
```

`<pacote>` é `hopper-documentation-anth-pt-br` ou `hopper-documentation-anth-en`. `<regras>` é `regras-de-escrita.md` ou `writing-rules.md`. `<modelos>` é `modelos.md` ou `templates.md`. A versão do plugin nos 2 `plugin.json` é `2.0.0`.

## Anexo D. Resposta do redator

O redator devolve 1 objeto JSON. Os nomes dos campos são iguais nos 2 idiomas.

```json
{
  "nada_relevante": false,
  "resumo": "Assunto da conversa, em até 80 caracteres",
  "conversa_simplificada": "Texto Markdown do bloco novo do documento 3",
  "itens_novos": [
    {
      "ref": "N1",
      "tipo": "D",
      "texto": "Texto do item",
      "origem": ["M7-3f9c2a71"],
      "situacao": "vigente",
      "recomendacao": "",
      "depende_de": ""
    }
  ],
  "mudancas": [
    {"id": "D2-3f9c2a71", "situacao": "substituída por N1", "origem": ["M7-3f9c2a71"]}
  ],
  "handoff": {
    "objetivo": "",
    "pautas_e_estado": "",
    "proximo_passo": "",
    "decisoes_e_autorizacoes": "",
    "restricoes": "",
    "descobertas": "",
    "pendencias": "",
    "lacunas": "",
    "como_retomar": ""
  }
}
```

- `tipo` aceita `D`, `F` ou `PD`. `recomendacao` e `depende_de` valem só para `PD`.
- `situacao` aceita os valores do Anexo E para o tipo do item.
- O redator usa `N1`, `N2`… para itens novos em qualquer campo de texto. O programa troca essas referências pelos identificadores finais.
- Com `nada_relevante` igual a `true`, o bloco do documento 3 traz só "Sem conteúdo novo relevante.", e os documentos 4, 5, 6 e 7 não mudam.
- **Migração.** A chamada de migração (R30) recebe os arquivos do formato antigo e devolve `itens_novos` com a origem igual ao nome do arquivo e mais o campo `handoffs_antigos`, uma lista com `conversa` (identificador), `data` (AAAA-MM-DD) e `handoff` (as mesmas 9 chaves acima).

## Anexo E. Formato dos documentos

Os exemplos usam dados reais da conversa `e4bad083-d7c0-5bd0-8e2a-677c1f7fd7b2`, de 2026-11-01. A numeração das decisões é ilustrativa.

### Árvore

```text
docs-by-hopper-documentation/
├── 1-indice.md
├── 4-decisoes.md
├── 5-funcoes.md
├── 6-pendencias.md
└── conversas/
    └── 2026-11-01-e4bad083/
        ├── 2-conversa-integral.md
        ├── 3-conversa-simplificada.md
        └── 7-handoff.md
```

### Documento 2

```markdown
# Conversa integral · e4bad083

- Conversa: e4bad083-d7c0-5bd0-8e2a-677c1f7fd7b2
- Pasta do projeto: /home/user
- Fuso dos horários: +00:00

## M1-e4bad083 · 2026-11-01 01:13 +00:00 · Usuário
<!-- registros: 03d2dbd2-7a25-4204-9fae-5d3f41583b0e 03d2dbd2-7a25-4204-9fae-5d3f41583b0e -->

Esse tipo de situação está acontecendo SEMPRE. Qual é o erro da skill? Ela nunca funciona!

[imagem anexada]
```

Autores possíveis: Usuário, Claude, Resposta do usuário, Plano aprovado, Relato de agente e Evento. No pacote em inglês: User, Claude, User answer, Approved plan, Agent report e Event.

### Documento 3

```markdown
# Conversa simplificada · e4bad083

## M1-e4bad083 a M19-e4bad083

**Assunto: falha do registro automático do anth.**

O registro automático do anth falhou antes da compactação. O programa recusou 2 citações que não estavam iguais na conversa. (M1-e4bad083)
```

Cada parágrafo termina com as mensagens de origem entre parênteses, separadas por vírgula. Um intervalo usa a forma `M3-e4bad083 a M7-e4bad083`.

### Documentos 4, 5 e 6

```markdown
# Decisões

### D8-e4bad083
Ter 2 skills, uma para o Claude e outra para o Codex. Nenhuma atende os 2.

- Origem: M66-e4bad083
- Situação: vigente
- Rodada: M56-e4bad083 a M80-e4bad083
```

```markdown
# Pendências

### PD1-e4bad083
Escrever a spec do modelo de 7 documentos.

- Recomendação: escrever com a skill hopper-spec-anth.
- Depende de: Jonathan dizer que está confortável com o modelo.
- Origem: M66-e4bad083
- Situação: encerrada em M80-e4bad083 (o proprietário autorizou a spec)
- Rodada: M56-e4bad083 a M80-e4bad083
```

Situações permitidas:

| Documento | Situações |
| --- | --- |
| 4. Decisões | `vigente`, `substituída por <ID>`, `revogada em <M-ID>` |
| 5. Funções implementadas | `concluída`, `substituída por <ID>`, `desfeita em <M-ID>` |
| 6. Pendências | `aberta`, `encerrada em <M-ID> (<motivo curto>)` |

Item migrado do formato antigo: a origem é o nome do arquivo, por exemplo `Origem: handoff-20261031-164340-d0eaf19d.md`, e a rodada é `migração`.

### Documento 7

```markdown
# Handoff · e4bad083

- Conversa: e4bad083-d7c0-5bd0-8e2a-677c1f7fd7b2
- Pasta do projeto: /home/user
- Última mensagem coberta: M85-e4bad083
- Rodada: 2026-11-01 23:30 +00:00
- Redator: claude-sonnet-5-5, esforço high

## Objetivo
## Pautas e estado atual
## Próximo passo
## Decisões e autorizações vigentes
## Restrições vigentes
## Descobertas e tentativas descartadas
## Pendências e compromissos
## Lacunas
## Como retomar
```

No pacote em inglês, as 9 seções são: Goal, Topics and current state, Next step, Decisions and authorizations in force, Constraints in force, Findings and discarded approaches, Pending items and commitments, Gaps e How to resume.

### Documento 1

```markdown
# Índice da documentação

Pasta do projeto: /home/user

## Ordem de leitura

1. Este índice.
2. O handoff da conversa mais recente (documento 7).
3. As pendências: [6-pendencias.md](6-pendencias.md).
4. As decisões: [4-decisoes.md](4-decisoes.md).
5. As funções implementadas: [5-funcoes.md](5-funcoes.md).
6. A conversa simplificada da conversa que você vai continuar (documento 3).
7. A conversa integral, para conferir uma origem (documento 2).

## Conversas

| Conversa | Início | Última mensagem | Última rodada | Resultado | Assunto |
| --- | --- | --- | --- | --- | --- |
| [e4bad083](conversas/2026-11-01-e4bad083/) | 2026-11-01 | M85-e4bad083 | 2026-11-01 23:30 +00:00 | concluída | Skill de documentação em 7 documentos |
```

Uma conversa migrada do formato antigo mostra "sem conversa integral" na coluna "Última mensagem".

### Descrição da skill

`Documenta a conversa atual do Claude Code em 7 documentos (índice, conversa integral, conversa simplificada, decisões, funções implementadas, pendências e handoff) na pasta docs-by-hopper-documentation do projeto. Use quando o usuário pedir para documentar ou registrar a conversa, salvar o progresso ou fazer um handoff. Não use para explicar, revisar ou editar esta skill.`

## Anexo F. Conferidor e roteiro de aceite

### Verificações do conferidor

`python3 aceite/conferir.py <pasta de documentação> --idioma pt-br|en [--roteiro <arquivo>]` imprime o total de verificações rodadas, aprovadas e reprovadas, e sai com código 0 só se todas passarem. Uma verificação que não encontra nada para conferir conta como reprovada.

| ID | Verificação |
| --- | --- |
| F1 | Os arquivos e as pastas da árvore do Anexo E existem para cada conversa. |
| F2 | No documento 2, os cabeçalhos seguem o formato do Anexo E, n começa em 1 sem saltos, cada mensagem tem o comentário de registros, e nenhum registro aparece em 2 mensagens. |
| F3 | No documento 3, os blocos cobrem intervalos seguidos desde M1, sem sobreposição. Cada bloco começa com a linha de assunto, e cada parágrafo termina com mensagens de origem. |
| F4 | Nos documentos 4, 5 e 6, cada item tem identificador único, texto, origem, situação permitida e rodada. "substituída por" aponta um item existente. |
| F5 | O documento 7 tem as 9 seções. |
| F6 | O documento 1 tem links válidos e lista todas as pastas de conversa. |
| F7 | Nos documentos 3 a 7, no mínimo 90% das frases têm até 25 palavras, nenhuma passa de 40, e nenhum parágrafo passa de 6 frases. Ficam fora da contagem os títulos, as linhas de metadados, as tabelas, os blocos de código e os identificadores. |
| F8 | Todo identificador de mensagem ou de item citado nos documentos 3 a 7 existe. |
| F9 | Com `--roteiro`, as asserções do roteiro de aceite passam (abaixo). |
| F10 | Nenhum arquivo do formato antigo está na raiz da pasta de documentação. |

### Roteiro de aceite

O executor roda o roteiro em A1, A2 e A3, em uma pasta de teste nova (`~/hopper-teste-a1`, `~/hopper-teste-a2` e `~/hopper-teste-a3`). Em A1 e A3, ele conduz a sessão interativa por um pseudoterminal. Em A2, ele conduz a sessão da aba Code com o uso do computador.

- **F-I. Instalação.** Instalar pelo Anexo H. Registrar a saída de `claude plugin list`, a lista de comandos com a skill e a lista de hooks com os 2 comandos do gatilho.
- **F-C. Conversa de teste.** Enviar estas 6 mensagens, nesta ordem, e anotar o identificador M de cada uma no arquivo de roteiro:
  1. "Vamos testar a documentação. Decidimos usar a cor azul no painel."
  2. "a senha do servidor é Pl4nt@d4#2026 hoje"
  3. "Quero seguir o sitema, claro ou escuro."
  4. "Crie o arquivo nota.txt com o texto teste."
  5. "Fica pendente escolher o formato do gráfico."
  6. "Documente a conversa."
- **F-A. Asserções depois da mensagem 6.** O documento 2 contém "sitema" e "[oculto]", não contém "Pl4nt@d4#2026" e tem uma linha que começa com "Ferramenta: Write" e termina com "nota.txt". O documento 4 tem um item D com a origem da mensagem 1. O documento 6 tem um item PD com a origem da mensagem 5. O documento 5 tem um item F com a origem da mensagem 4 ou da mensagem do Claude que contém a linha da ferramenta Write.
- **F-K. Compactação automática.** Reduzir o limite da compactação automática pela configuração documentada vigente (consultar `code.claude.com/docs/en/env-vars.md` na data da execução e registrar a variável usada). Continuar a conversa até a compactação automática. Fechar o Claude Code 5 segundos depois do início da compactação. Esperar até 10 minutos. Conferir no registro de rodadas que a cópia terminou antes do registro de compactação e que a rodada terminou depois do fechamento.
- **F-V. Conferidor.** Rodar o conferidor com `--roteiro` na pasta de documentação da pasta de teste.
- **F-L. Limpeza.** Registrar que a pasta de dados não tem `venv` e que `claude plugin list` não mostra o plugin `hopper-documentation`.

## Anexo G. Mapa de verificadores antes de integrar

| Caminho alterado | Verificadores que rodam antes de integrar |
| --- | --- |
| `*/scripts/hopper_documentation_anth.py` | Todos os testes do pacote alterado, a comparação T35 e o conferidor nos casos de `aceite/casos/` |
| `*/skills/**` | T41 e as avaliações de acionamento afetadas |
| `*/hooks/hooks.json` ou `*/.claude-plugin/*` | T22 a T24 e `claude plugin validate --strict` |
| `aceite/**`, `.github/workflows/verificar.yml` ou `SPEC.md` | Proibido sem o "sim" do proprietário (C18) |
| Documentação em Markdown | Conferência de links e T32 |
| `execucao/**` | Nenhum |

Depois de integrar, a verificação do GitHub roda tudo (C17).

**Plugin de sonda de U1.** Um plugin temporário com 2 comandos no `PreCompact`, no mesmo formato de C02. O comando síncrono grava a hora de início e de fim. O comando assíncrono inicia um processo separado que espera 120 segundos e grava a hora. O executor apaga a sonda no fim de U1.

## Anexo H. Instalação

**A1 e A3 (terminal).**

```sh
mkdir -p "$HOME/.local/share"
git clone https://github.com/jonathanpah/hopper-documentation-anth.git "$HOME/.local/share/hopper-documentation-anth"
claude plugin marketplace add "$HOME/.local/share/hopper-documentation-anth/hopper-documentation-anth-pt-br"
claude plugin install hopper-documentation-anth@hopper-documentation-anth
```

Durante U8, o clone usa a branch de trabalho (`git -C <clone> checkout versao-2`). Depois de U10, a `main`. Para atualizar: `git -C <clone> pull --ff-only`, `claude plugin marketplace update hopper-documentation-anth` e `claude plugin update hopper-documentation-anth@hopper-documentation-anth`. Numa sessão aberta, enviar `/reload-plugins`.

**A2 (Claude Desktop).** Conferir, pelo uso do computador, se o plugin instalado em A1 aparece na aba Code. Se não aparecer, instalar pelo botão "+" e pela opção "Add plugins", seguindo C16.
