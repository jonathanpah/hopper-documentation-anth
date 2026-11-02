# Avaliação da spec hopper-documentation-anth, versão 2

- Revisor: Claude Fable 5.1, sem acesso à conversa em que a spec foi escrita.
- Data: 2026-11-02.
- Objeto: `SPEC.md` na branch `main` do repositório `jonathanpah/hopper-documentation-anth`, commit `b2954f2`, 1.432 linhas, lido inteiro.
- Fontes consultadas, só leitura: `SKILL.md` e `garantias.md` da skill `hopper-spec-anth` 0.2.0; a documentação oficial do Claude Code baixada em 2026-11-02 (hooks, settings, settings-reference, permissions, permission-modes, env-vars, desktop, cli-reference, headless, skills, model-config e plugins/cli-reference) e a página `plugins/components.md` lida online; o código da versão 0.1.4 do plugin na cópia de trabalho; o programa e os testes do `hopper-documentation` no commit `8c2e438`, lidos pelo GitHub; `claude --version` (2.1.296), `claude --help`, `claude plugin --help`, `claude plugin eval --help`, `claude plugin validate --help`, `claude plugin list` e `claude plugin marketplace list` no MacBook; a pasta `~/.claude/plugins/` do MacBook; as descrições das ferramentas de sessão do Claude Desktop disponíveis nesta sessão. Nenhum `claude -p` foi executado, nada foi instalado, e nenhum arquivo do repositório foi alterado além da criação deste arquivo.

## Veredito

Executar depois de corrigir os itens bloqueantes, que são os achados 1 e 2. Recomendo corrigir também os achados 3 a 8 antes de U2, porque eles tocam critérios que congelam em U2 ou decisões que U1 e U8 vão provar.

## Achados

### 1. Em A2, o caminho principal da conversa de teste reprova F9 por construção

- Gravidade: bloqueante.
- Onde: Anexo F, verificação F9 e passo F-C; decisão C26; glossário "Ferramentas de sessão".
- Problema: Pelas ferramentas de sessão, cada mensagem chega à sessão de teste com um rótulo "From <título da sessão>" e um link, e a sessão nasce com o briefing como primeira mensagem do usuário. F9 exige que o texto da mensagem seja igual ao texto fixo do roteiro, então F9 reprova em A2 sempre que o executor usa o caminho que C26 define como principal.
- Evidência: Descrição da ferramenta `send_message` do Claude Desktop, lida nesta sessão: "The message arrives in the target session as a user turn labelled "From {this session's title}" with a link back here". Descrição de `start_session`: o modo "fresh" exige `prompt` (o briefing) e `background`, e o `prompt` é o primeiro turno da sessão nova. Anexo F, F9: "localiza no documento 2 as mensagens do usuário cujo texto é igual aos textos fixos do roteiro".
- Correção: F9 e F-A passam a localizar as mensagens por "contém o texto fixo", e o roteiro registra que em A2 a primeira mensagem é o briefing.

### 2. R33 e F-L tratam como resíduo uma pasta que o próprio Claude Code cria

- Gravidade: bloqueante.
- Onde: R33; passo F-L do Anexo F; glossário "Pasta de dados".
- Problema: A pasta `plugins/data/hopper-documentation-anth-hopper-documentation-anth` não é resíduo de versão anterior. É a pasta de dados que o Claude Code reserva ao plugin instalado, no padrão `<nome>-<catálogo>`, e cria quando um gatilho do plugin roda. R33 exige que ela não exista, então F-L reprova de novo depois de cada rodada do gatilho, e o executor apaga uma pasta que a plataforma recria.
- Evidência: `plugins/components.md`: "`${CLAUDE_PLUGIN_DATA}`: a directory that survives updates [...] It resolves to `~/.claude/plugins/data/<id>/` and is created when first referenced" e "`my-plugin@my-marketplace` becomes `my-plugin-my-marketplace`". Mesma página: "every hook process receives `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` in its environment". `ls -la ~/.claude/plugins/data` em 2026-11-01: a pasta `hopper-documentation-anth-hopper-documentation-anth` está vazia, com data 2026-10-24 07:10, o mesmo minuto da última alteração de `hopper-documentation-anth/locks`, gravada por uma rodada do gatilho. O programa 0.1.4 (`scripts/hopper_documentation_anth.py`, função `data_dir`) só cria a pasta `hopper-documentation-anth`. A própria spec registra a pasta nas 2 máquinas (F-L).
- Correção: R33 e F-L passam a excluir a pasta `<nome>-<catálogo>` do plugin instalado, ou a spec adota essa pasta como pasta de dados.

### 3. As ferramentas de sessão não encerram a sessão de teste no meio da compactação

- Gravidade: importante.
- Onde: Decisão C25; R23, verificador em A2; risco K10; glossário "Ferramentas de sessão".
- Problema: `stop_session` só interrompe o turno e mantém a sessão aberta. `archive_session` encerra o processo, mas recusa uma sessão em trabalho e pede aprovação do proprietário. Encerrar a sessão de teste "5 segundos depois do início da compactação" não é possível por essas ferramentas, então a prova de R23 em A2 fica sem mecanismo.
- Evidência: Descrição de `stop_session`: "Interrupt another CCD session's in-flight turn [...] The session stays open and idle afterwards". Descrição de `archive_session`: "Archiving stops the session's process [...] A session that is still working (mid-turn, or with live background work) is not archived and the call says so" e "The app asks the user to approve each call, except in auto mode".
- Correção: C25 define a prova de A2 como interrupção do turno por `stop_session`, com o gatilho cancelado e o processo separado vivo, ou declara que R23 em A2 é coberto por A1, como K10 já faz para o fechamento do app, e o glossário nomeia as ferramentas e seus limites.

### 4. Uma cópia interrompida pode deixar o documento 2 truncado, sem caminho de recuperação

- Gravidade: importante.
- Onde: R04, R22, R29, N01; decisões C09 e C10.
- Problema: O gatilho de cópia é cancelado aos 60 segundos e morre quando o Claude Code é fechado durante a cópia, como na 2ª passagem de F-K. Se a morte acontece no meio da gravação do documento 2, a última mensagem fica truncada e sem o comentário de registros que C10 usa para retomar, e N01 proíbe corrigi-la. T29 não cobre interrupção durante a cópia.
- Evidência: `hooks.md`: "Claude Code cancels a `command`, `http`, or `mcp_tool` hook that reaches its `timeout`, discarding the hook's output". `headless.md`: "On SIGTERM, Claude Code terminates the process tree of any Bash command that is still running". T29 cobre só "depois da cópia, depois do diário e no meio da gravação". O programa 0.1.4 já grava por arquivo temporário e `os.replace` (função `write_atomic`), mas a spec não exige isso para o acréscimo ao documento 2.
- Correção: C10 exige gravação atômica do documento 2, por arquivo temporário na mesma pasta e renomeação, e T29 ganha o caso "interrupção no meio da cópia".

### 5. O mecanismo de limite da seção 10 é mais fraco do que a spec descreve

- Gravidade: importante.
- Onde: Seção 10; garantia G10; risco K06.
- Problema: As regras `ask` e `deny` casam só com o texto do comando Bash. Elas não alcançam o mesmo programa por caminho completo, dentro de `bash -c`, por `python3 -c` ou por `subprocess` em um script. A edição de `.claude/settings.local.json` no modo `auto` vai ao classificador, e não ao proprietário, então "O executor não edita esse arquivo depois de U1" é só texto. O `deny` do `hopper-documentation` cobre `gh` e não cobre `git push` com a URL do repositório.
- Evidência: `permissions.md`: "A Bash rule matches the command text Claude writes [...] It doesn't match the same program invoked in a different form, so a deny or ask rule covers the invocation Claude usually produces and isn't a security boundary around the program"; tabela: "`Bash(rm *)` | `rm -rf build/` | `/bin/rm -rf build/`, `bash -c 'rm -rf build/'`". `permission-modes.md`, "Protected paths": "`auto` | Routed to the classifier", e `.claude` está na lista de diretórios protegidos.
- Correção: K06 e G10 registram esse limite como risco residual aceito, e a seção 10 acrescenta regras `deny` para a edição de `.claude/settings.local.json` e para `git push` com `hopper-documentation.git`.

### 6. A proteção de C18 confere a si mesma

- Gravidade: importante.
- Onde: Decisão C18; garantia G03.
- Problema: A conferência do manifesto e da tag vive em `.github/workflows/verificar.yml`, que é ele mesmo um critério congelado. Um commit que altera o fluxo, o manifesto e um caso ao mesmo tempo passa sem "CRITÉRIO ALTERADO", e o revisor que apontaria a mudança é um subagente aberto pelo executor (C22). A prova de C18 altera só um caso e não exercita esse caminho.
- Evidência: C18: "A verificação do GitHub falha com a mensagem "CRITÉRIO ALTERADO" quando um critério congelado não confere com o manifesto, ou quando o manifesto difere do manifesto da tag". Glossário "Critérios congelados" inclui `verificar.yml`. C22: "abre um subagente sem o contexto da sessão".
- Correção: U10 grava na descrição do PR o commit da tag `criterios-congelados` e o commit de U2, para o proprietário comparar os 2 valores no GitHub antes do "sim", e a prova de C18 inclui 1 alteração no próprio fluxo.

### 7. T32 reprova durante toda a execução e esconde violações novas do inventário

- Gravidade: importante.
- Onde: R32; Anexo C; decisões C17 e C19; unidade U10.
- Problema: A pasta `execucao/` fica na branch de trabalho de U1 a U10 e não está no inventário, então T32 reprova em todo envio de commits até o último commit de U10. Uma reprovação permanente de T32 esconde qualquer outra violação do inventário, como um arquivo de `.claude/` versionado por engano, porque C19 só suspende integrações por reprovação nova.
- Evidência: Anexo C não lista `execucao/**`. C17: "roda em todo envio de commits a qualquer branch e em todo PR". C19: "As reprovações de requisitos ainda pendentes, presentes desde U2, não suspendem".
- Correção: T32 ignora `execucao/**` fora da `main`, e U7 registra em `execucao/verificacoes.md` a primeira execução em que T32 passa sem essa exceção.

### 8. O redator herda do gatilho variáveis que mudam o modelo, o esforço e a compactação

- Gravidade: importante.
- Onde: Decisão C03; decisão C27; passo F-K; T12.
- Problema: O redator herda o ambiente do gatilho, e em U8 esse ambiente traz as variáveis de compactação da sessão de teste. O `claude -p` do redator também compacta, e um limite baixo pode disparar a compactação no meio da resposta estruturada. C03 lista as variáveis que acrescenta, mas não as que remove, e `CLAUDE_CODE_EFFORT_LEVEL` no ambiente anula `--effort high` sem o programa perceber.
- Evidência: `env-vars.md`: "`CLAUDE_CODE_EFFORT_LEVEL` [...] Takes precedence over `--effort`"; "`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` [...] Applies to both main conversations and subagents". C27: as 2 variáveis vão no ambiente do comando `claude` da sessão de teste em A1 e A3. O programa 0.1.4 monta o ambiente do redator com `dict(os.environ, ...)` e não remove nada (função `call_model`).
- Correção: C03 remove do ambiente do redator `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, `CLAUDE_CODE_EFFORT_LEVEL` e `ANTHROPIC_MODEL`, e T12 confere a remoção.

### 9. A calibração da compactação em A2 pode não ter solução

- Gravidade: menor.
- Onde: U1, item 5, último subitem; decisão C27.
- Problema: O limite de compactação é uma porcentagem da janela de 100 mil tokens, e uma sessão nova do Desktop já carrega o prompt do sistema, as ferramentas e os conectores ativos. Se esse contexto inicial passa de janela vezes porcentagem, a compactação acontece na primeira mensagem para qualquer valor, e a condição "depois de 6 mensagens e não antes" fica sem solução em A2.
- Evidência: `env-vars.md`: "`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Set the percentage (1-100) of the auto-compact window". `model-config.md`: a janela mínima é 100.000 tokens. A spec não registra o contexto inicial de uma sessão de teste.
- Correção: U1 mede o contexto inicial da sessão de teste em cada ambiente antes de escolher a porcentagem e prevê abrir a sessão de A2 sem conectores.

### 10. Provar uma regra `deny` executa o comando perigoso quando o padrão não casa

- Gravidade: menor.
- Onde: U1, item 4; seção 10.
- Problema: Provar uma regra `deny` exige executar o comando que ela deveria barrar. Se o padrão não casar, o comando roda de verdade, por exemplo `git push --force`.
- Evidência: U1, item 4: "Provar cada regra `deny` mostrando o bloqueio". `permissions.md`: as regras casam "as written".
- Correção: As provas de `deny` usam uma branch descartável e um clone descartável como alvo, e `gh repo delete` é provado sem `--yes`.

### 11. A atualização da pasta de produção com `cp -R` aninha a cópia

- Gravidade: menor.
- Onde: Anexo H, "Atualizar durante U8"; decisão C16.
- Problema: `cp -R <origem> <destino>` copia a origem para dentro do destino quando o destino já existe, e não apaga arquivos que saíram do pacote. A atualização de U8 com o mesmo comando cria `pt-br/hopper-documentation-anth-pt-br/` e deixa arquivos velhos na pasta de produção.
- Evidência: `man cp` no macOS: "In the second synopsis form, the contents of each named source_file is copied to the destination target_directory" e "target_directory must exist unless there is only one named source_file which is a directory and the -R flag is specified". Anexo H: "Copiar de novo a `<origem>` sobre a pasta de produção".
- Correção: A atualização apaga a pasta de produção antes de copiar, ou usa `rsync -a --delete`, e a conferência arquivo a arquivo contra a origem passa a valer também em U8.

### 12. A mensagem 4 do roteiro não garante a ferramenta Write, e o diálogo de confiança não é tratado

- Gravidade: menor.
- Onde: Passo F-C, mensagem 4; passo F-A; U1, item 5.
- Problema: F-A exige uma linha "Ferramenta: Write" no documento 2, mas a mensagem 4 não pede a ferramenta Write, e o Claude da sessão de teste pode criar o arquivo por Bash. A primeira abertura de uma pasta nova mostra o diálogo de confiança, e a spec não diz que o pseudoterminal o responde.
- Evidência: F-A: "tem uma linha que começa com "Ferramenta: Write" e termina com "nota.txt"". `settings.md`: os valores de `env` do projeto "apply only after each teammate trusts the folder".
- Correção: A mensagem 4 passa a "Use a ferramenta Write para criar o arquivo nota.txt com o texto teste.", e U1, item 5, prova que o pseudoterminal responde ao diálogo de confiança.

### 13. F-K espera menos tempo do que o limite do redator

- Gravidade: menor.
- Onde: Passo F-K; caso de borda de R12.
- Problema: F-K espera até 10 minutos pelo fim da rodada, e o redator tem 15 minutos de limite. Uma chamada lenta reprova F-K sem defeito do plugin.
- Evidência: F-K: "Esperar até 10 minutos". Caso de borda de R12: "O redator não responde em 15 minutos".
- Correção: F-K espera até 16 minutos ou até a linha de fim da rodada no registro de rodadas.

### 14. O limite de tentativas por unidade ignora os 3 ambientes de U8

- Gravidade: menor.
- Onde: Decisão C20; unidades U1 e U8.
- Problema: "Até 10 tentativas por unidade" vale igual para U3, que é código com testes locais, e para U8, que automatiza 3 ambientes por pseudoterminal, SSH e ferramentas de sessão. U8 tende a esgotar o limite por causa de ambiente, e não de entrega, e parar para perguntar ao proprietário.
- Evidência: C20: "até 10 tentativas por unidade". U8 cobre A1, A2 e A3 com os passos F-I, F-C, F-A, F-K e F-V em cada um.
- Correção: C20 conta as tentativas de U1 e U8 por ambiente.

### 15. A regra `ask` para `rm *` gera pedidos fora da tabela da seção 10

- Gravidade: menor.
- Onde: Seção 10, regra `ask` para `rm *`.
- Problema: O executor usa `rm` o tempo todo em arquivos temporários próprios, e cada uso vira um pedido ao proprietário, contra a intenção de P18. Os alvos que importam já estão listados na tabela.
- Evidência: Seção 10: "Regra `ask` para `rm *`". `permissions.md` aceita `*` no meio do padrão, como em "`Bash(* --version)`".
- Correção: A regra `ask` de `rm` cobre só os caminhos da tabela, que são `venv`, `releases`, `plugins/data`, as pastas de teste e as pastas de documentação.

### 16. O arquivo de regras criado à mão não é ignorado pelo git

- Gravidade: menor.
- Onde: Seção 10; U1, item 4; Anexo C.
- Problema: O arquivo `.claude/settings.local.json` criado à mão não entra nas exclusões do git automaticamente, e `.claude/` não está no inventário. Um `git add -A` o versiona e T32 reprova.
- Evidência: `settings.md`: "If you created the file by hand and Claude Code hasn't written to it yet, add it to `.gitignore` yourself".
- Correção: U1 acrescenta `.claude/` ao `.gitignore`, que está no inventário.

### 17. R13 contradiz R28 na rodada sem trecho novo

- Gravidade: menor.
- Onde: R13 e R28.
- Problema: R13 manda acrescentar um bloco ao documento 3 "a cada rodada", e R28 manda não alterar os documentos 1 a 7 na rodada sem trecho novo. R11, R17 e R18 já dizem "com trecho novo".
- Evidência: R13: "A cada rodada, o programa acrescenta ao documento 3 um bloco". R28: "a rodada não chama o redator, não altera os documentos 1 a 7".
- Correção: R13 passa a "A cada rodada com trecho novo".

### 18. O primeiro registro do arquivo de histórico pode não ter `cwd`

- Gravidade: menor.
- Onde: Glossário "Pasta do projeto"; decisão C11; caso B1.
- Problema: O primeiro registro do arquivo pode ser um resumo ou um instantâneo sem o campo `cwd`. O programa precisa procurar o primeiro registro que tem o campo, e B1 não testa esse caso.
- Evidência: Glossário: "lê essa pasta no campo `cwd` do primeiro registro do arquivo de histórico". B1 omite `cwd` de todos os registros só por legibilidade.
- Correção: O glossário e C11 passam a "primeiro registro que traz `cwd`", e B1 ganha 1 registro inicial sem o campo.

### 19. N02 e R03 não cabem nas gravações do próprio Claude Code

- Gravidade: menor.
- Onde: R03, N02, T03.
- Problema: O redator é um `claude -p`, que grava arquivos próprios em `~/.claude/` e `~/.claude.json` mesmo com `--no-session-persistence`. R03 e N02 valem para "o programa", mas T03 roda com redator simulado e não observa essas gravações, e a leitura literal de N02 fica impossível de cumprir.
- Evidência: `settings.md`: "Claude Code also keeps a fifth file, `~/.claude.json`, that it writes for itself". T03: "A lista de arquivos criados ou alterados fora dessas 2 pastas fica vazia".
- Correção: R03 e N02 excluem as gravações do próprio Claude Code na pasta de configuração.

### 20. As avaliações de acionamento custam o dobro do que a spec conta

- Gravidade: menor.
- Onde: Decisão C20; R25; unidades U5, U8 e U10.
- Problema: Por padrão, `claude plugin eval` roda cada caso 2 vezes, com e sem o plugin, e cada rodada é um processo `claude` completo com a credencial do proprietário. São 20 casos por pacote, então 1 execução completa custa 40 sessões por pacote, e as 3 execuções de C20 custam 120 sessões por pacote.
- Evidência: `claude plugin eval --help`: "--ablation <mode> Run a no-plugin baseline arm [...] default: with-without whenever a plugin resolves" e "Each run is a full claude child on your own credential". Pasta `evals/acionamento` da versão atual: 20 casos.
- Correção: C20 fixa `--ablation none` nas execuções de acionamento ou conta as 2 passagens no limite.

### 21. O custo de operação por compactação não está estimado

- Gravidade: menor.
- Onde: Caso de borda de R11; risco K09; README (U7).
- Problema: Nos modelos atuais, a compactação automática acontece perto de 967 mil tokens, então o trecho novo de uma rodada pode ter vários megabytes. Com partes de 300 mil caracteres, 1 compactação pode custar 10 ou mais chamadas ao Sonnet 5.5, cada uma reenviando os documentos 4, 5 e 6. A spec só trata o custo da execução.
- Evidência: `model-config.md`: "Models running with a native 1M window compact before the window fills, at about 967K tokens by default". Caso de borda de R11: "1 chamada ao redator por parte".
- Correção: K09 registra a estimativa de chamadas por compactação, e o README avisa o usuário.

### 22. Quatro requisitos têm mais de 1 frase ou mais de 1 comportamento

- Gravidade: menor.
- Onde: R30, R33, R35, R39; garantia G02; seção 17.
- Problema: G02 exige 1 frase por requisito. R30 tem 1 frase de cerca de 90 palavras com 3 comportamentos, R33 reúne 4 condições, e R35 e R39 têm 2 frases. A seção 17 declara a conferência aprovada.
- Evidência: `garantias.md`, G02: "Cada requisito tem identificador estável, 1 frase em voz ativa".
- Correção: Dividir R30, R33, R35 e R39 em requisitos numerados, por exemplo R30a e R30b, com o mesmo verificador, ou registrar o desvio na seção 17.

### 23. Três coisas têm 2 nomes, e as ferramentas de sessão não têm nome

- Gravidade: menor.
- Onde: Glossário; U1, item 5; C25, C26, C27; F-K; R33; F-L; U10.
- Problema: "Sessão de teste" e "conversa de teste" nomeiam a mesma coisa, e o glossário define "Conversa" como "uma sessão do Claude Code". "Release" (R33, F-L, U10) e "pasta de produção" se sobrepõem. "Ferramentas de sessão" não traz os nomes das ferramentas, então um executor fora desta sessão não sabe o que procurar.
- Evidência: Glossário: "Conversa | Uma sessão do Claude Code" e "Conversa de teste | A conversa do roteiro de aceite". U1: "a sessão de teste é conduzida por um pseudoterminal". R33: "a pasta `releases/` da raiz de produção contém só a release instalada".
- Correção: O glossário fixa 1 nome para cada uma dessas 3 coisas e lista as ferramentas `start_session`, `send_message`, `list_events`, `stop_session` e `archive_session`, com os limites do achado 3.

### 24. Seis garantias apontam para texto solto, sem prova

- Gravidade: menor.
- Onde: Seção 11, garantias G02, G04, G07, G13, G14 e G15.
- Problema: Essas garantias apontam para texto solto em vez de uma decisão de como com os 5 campos da skill, e G07, G13, G14 e G15 não dizem qual é a prova. A seção 17 conta só as 27 decisões C.
- Evidência: `SKILL.md`, passo 5: "Toda garantia tem decisão de como e prova". G07, "Como esta spec cumpre": só o destino das perguntas e o momento da entrega.
- Correção: Cada uma dessas garantias ganha a linha "Prova", por exemplo G07 com `execucao/perguntas.md` numerado e datado, ou aponta uma decisão C nova.

### 25. A fonte de C02 sobre processo separado vale para `claude -p`

- Gravidade: menor.
- Onde: Decisão C02, campo Fontes.
- Problema: A frase da documentação sobre processo totalmente separado vale para sessões `claude -p`. A spec a usa como fonte para a sobrevivência ao fechamento de uma sessão interativa, que a documentação não descreve.
- Evidência: `hooks.md`: "If your hook's work must outlive a `claude -p` session, start a fully detached process from it".
- Correção: C02 cita a frase com esse alcance e aponta U1, item 5, como a única prova para sessões interativas.

### 26. C01 e C13 descrevem o clone de leitura com números imprecisos

- Gravidade: menor.
- Onde: Decisões C01 e C13.
- Problema: "Leitor com 57 testes" atribui ao leitor a suíte inteira do clone de leitura. A suíte tem 57 testes, dos quais 14 cobrem o histórico, e a classe `Masking` tem 4 métodos sobre uma tabela de 46 casos.
- Evidência: `hopper-documentation-pt-br/tests/test_hopper_documentation.py` no commit `8c2e438`: classes `Masking` (4 testes, lista `CASES` com 46 entradas), `History` (14), `Publication` (12), `Sources` (9) e `Commands` (18). Os 3 testes herdados citados em B1 e R10 existem e usam só arquivos JSONL sintéticos. As funções `claude_texts`, `extract_messages`, `find_transcript`, `verify_identity` e `mask` existem no programa, que usa só a biblioteca padrão.
- Correção: C01 diz "suíte com 57 testes, 14 do leitor" e C13 diz "46 casos".

### 27. K05 generaliza aos 3 ambientes uma retenção que não vale no Desktop

- Gravidade: menor.
- Onde: Risco K05; caso de borda de R04.
- Problema: A retenção de 30 dias vale para sessões do terminal. Sessões abertas no Claude Desktop ficam sem limite de idade por padrão.
- Evidência: `settings-reference.md`, `desktopSessionCleanupPeriodDays`: "Without this key, Claude Code keeps those transcripts at any age".
- Correção: K05 registra que o limite de 30 dias vale para A1 e A3 e não vale para A2 por padrão.

### 28. F-I não diz de onde vem a "lista de comandos" em A1 e A3

- Gravidade: menor.
- Onde: Passo F-I; R39.
- Problema: "A lista de comandos com a skill" não diz como é capturada no terminal. Capturar o menu "/" por pseudoterminal é frágil, e `claude plugin details` já lista os componentes do plugin.
- Evidência: `claude plugin --help`: "details [options] <name> Show a plugin's component inventory and projected token cost".
- Correção: F-I define a saída de `claude plugin details` como a prova da skill em A1 e A3, e a lista de comandos vira prova só em A2.

### 29. O cabeçalho ficou desatualizado depois da incorporação

- Gravidade: menor.
- Onde: Cabeçalho, "Situação"; seção 9, "Antes de U1"; seção 15.
- Problema: O PR #2 já foi incorporado e a branch `versao-2` já existe, mas o cabeçalho diz "em aprovação". O PR #1 continua aberto, coerente com P24 pendente.
- Evidência: `git log`: "b2954f2 Merge pull request #2"; `git branch -a`: `versao-2` e `origin/versao-2`; `gh pr view 1 --json state`: `OPEN`.
- Correção: O cabeçalho passa a "aprovada em <data>, commit b2954f2", em commit na branch de trabalho antes de U2, quando `SPEC.md` congela.

## O que foi conferido e passou

As afirmações técnicas abaixo têm apoio na documentação ou na CLI instalada e não geraram achado. `PreCompact` recebe `session_id`, `transcript_path`, `cwd` e `trigger`, e o código de saída 2 bloqueia a compactação (`hooks.md`). Gatilhos do mesmo evento rodam em paralelo, `async` e `asyncRewake` existem, o `timeout` continua valendo com `asyncRewake`, e a saída 2 de um `asyncRewake` acorda o Claude (`hooks.md`). O arquivo de histórico é gravado de forma assíncrona (`hooks.md`). Todas as opções de C03 existem em `cli-reference.md` e em `claude --help`, `CLAUDE_CODE_SAFE_MODE`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS` e `CLAUDE_CODE_DISABLE_AUTO_MEMORY` existem em `env-vars.md`, e `--bare` exige chave de API segundo `claude --help`. O campo `modelUsage` existe (`model-config.md`), e o Sonnet 5.5 exige 2.1.284 ou mais novo (`model-config.md`). `CLAUDE_PID` existe desde 2.1.214 e a aba Code roda uma cópia própria do Claude Code (`env-vars.md`, `desktop.md`). `${CLAUDE_SESSION_ID}` e `${CLAUDE_PLUGIN_ROOT}` são substituídos em skills de plugin (`skills.md`). `claude plugin marketplace add` aceita pasta local, e `remove`, `update`, `install`, `update`, `list`, `details`, `validate --strict` e `eval` existem na CLI 2.1.296. A instalação atual segue a convenção de C16 (`claude plugin list` e `known_marketplaces.json`). No modo `auto`, as regras `ask` continuam pedindo e as regras `deny` continuam bloqueando (`permission-modes.md`), e as regras `deny` e `ask` de projeto valem sem o passo de confiança (`settings.md`). Mover a sessão de pasta recarrega as configurações de projeto (`settings.md` e a ferramenta `change_directory`). `CLAUDE_CODE_AUTO_COMPACT_WINDOW` tem mínimo de 100.000, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` só abaixa o limite, nenhuma das 2 está na lista de variáveis ignoradas em `env` de projeto, e `/autocompact` grava nas configurações do usuário (`env-vars.md`, `settings-reference.md`, `model-config.md`). O `/status` mostra a versão na aba Code, e os comandos de painel respondem "isn't available in this environment" (`desktop.md`). Plugins não carregam em sessões na nuvem nem em WSL (`desktop.md`). `/reload-plugins` existe (`plugins/cli-reference.md`). A retenção padrão de 30 dias existe para o terminal (`hooks.md`). O `claude -p` chamado de dentro de um gatilho é permitido (`env-vars.md`, `CLAUDE_CODE_CHILD_SESSION`). As 15 garantias da seção 11 são iguais ao `garantias.md` da skill 0.2.0.

## O que não foi possível verificar

Não verifiquei o estado da VPS (A3), as cópias de `OPERATIONS.md` e `ACCESS.md`, nem as versões 2.1.309 de A2 e 2.1.316 de A3, porque não acessei essas máquinas nem esses arquivos. Não confirmei se o rótulo "From <título>" de `send_message` fica no texto da mensagem gravada no arquivo de histórico, porque isso exigiria abrir uma sessão de teste; o achado 1 vem da descrição da ferramenta. Não confirmei o comportamento do Claude Code interativo ao ser fechado durante um gatilho, porque a documentação não o descreve e o teste exigiria executar o plugin. Não li `tools-reference.md`, `troubleshoot-install.md` nem `sessions.md`, que não estavam na pasta baixada, nem o artigo do `support.claude.com` citado em C16. Não conferi as fontes externas de C05 e C14 (o artigo de engenharia da Anthropic, `beads`, `spec-kit`, a ASD-STE100 Issue 9, a Lei 15.263/2025, a ISO 24495-1 e os 2 artigos do arXiv). Não confirmei se os runners macOS do GitHub oferecem Python 3.9 para a matriz de C17, nem o formato exato da saída de `claude plugin details`. Não executei `claude -p`, então C03 e C04 foram conferidas pela documentação e pelo código 0.1.4, que usa a mesma chamada e o mesmo campo `modelUsage`.
