# Registro de verificações

Só acréscimos (C21). Cada entrada traz o verificador, o comando, a saída relevante e o resultado. Datas em UTC.

## V-U1-01 · U1, item 1 · Versões · 2026-11-02 02:36 · aprovado

Comandos: `zsh -lc 'claude --version'` (A1); `"$(ps -o comm= -p "$CLAUDE_PID")" --version` na sessão do executor (A2); `ssh hopper-jpah '~/.local/bin/claude --version'` (A3); `python3 --version` nos 3. Saídas em `versoes.md`. As 3 versões (2.1.296, 2.1.309 e 2.1.316) são maiores que 2.1.284. Python 3.14.8 no MacBook e 3.13.5 na VPS, os 2 acima de 3.9.

## V-U1-02 · U1, item 2 · Acessos · 2026-11-02 02:36 · em andamento

- `ssh -o BatchMode=yes hopper-jpah`: ok; `/home/jpah/projects/mallmetrics` existe; `sudo -n true` ok; `hostname` = `hopper`.
- `ssh -o BatchMode=yes hopper-old-jpah` (00:40 UTC): `/home/jpah/projects/mallmetrics` não existe. A3 é `hopper-jpah`.
- `ssh -o BatchMode=yes hopper-jonathan`: ok, Claude Code 2.1.308.
- `gh auth status`: conta `jonathanpah`; `gh api repos/jonathanpah/hopper-documentation-anth`: `admin=true push=true`.
- Ferramentas de sessão e uso do computador: pendente de registro.

## V-U1-03 · U1, item 3 · Clone de leitura (C24) · 2026-11-02 02:36 · aprovado

Comandos: `git clone https://github.com/jonathanpah/hopper-documentation.git ~/.local/share/hopper-documentation-leitura`; `git checkout 8c2e438`; `git remote remove origin`. Saída: `HEAD=8c2e438 remotes=[]`. Os arquivos `hopper-documentation-pt-br/scripts/hopper_documentation.py` e `hopper-documentation-pt-br/tests/test_hopper_documentation.py` existem.

## V-U1-02 (continuação) · Ferramentas de sessão e uso do computador · 2026-11-02 02:45 · aprovado

- Ferramentas de sessão presentes na sessão do executor, com os esquemas carregados: `start_session`, `send_message`, `list_events`, `stop_session`, `archive_session` (servidores `ccd_session` e `ccd_session_mgmt`). A abertura de uma sessão na pasta de teste é provada no item 5.
- Uso do computador: a ferramenta `list_apps` do servidor `computer-use` respondeu (`{"apps":[]}` para a busca "Claude"). O acesso a aplicativos não foi pedido, porque o caminho principal de A2 são as ferramentas de sessão (C26).

## V-U1-04 · U1, item 4 · Regras de permissão · tentativa 1 · 2026-11-02 02:48 · reprovado

Arquivo `.claude/settings.local.json` criado na cópia de trabalho com 16 regras `ask` e 12 regras `deny` (texto em `decisoes.md`, D-05). Provas disparadas em seguida, sem nenhum pedido de permissão: `gh pr merge --help`, `git push --dry-run origin HEAD:main` (dry-run, nada enviado), `git push --dry-run origin criterios-congelados` e `git push --dry-run origin v2.0.0` (referências inexistentes, erro inofensivo), `echo hopper_documentation_anth.py migrar` e `gh repo view jonathanpah/hopper-documentation` (leitura, que a regra `deny` deveria barrar). Só `git push --dry-run origin --delete prova-inexistente` foi barrado, pela regra `deny` do arquivo `.claude/settings.json` da pasta `5-claude`, pasta de origem da sessão. Causa: a sessão do executor ainda lia as configurações de projeto da pasta de origem, e não da cópia de trabalho. Correção: mover a sessão com a ferramenta `change_directory`, que troca a pasta das configurações de projeto no fim do turno, e repetir as provas.

## V-U1-04 · U1, item 4 · Regras de permissão · tentativa 2 · 2026-11-02 02:43 · aprovado em parte

Sessão movida para a cópia de trabalho (o aplicativo confirmou a troca das configurações de projeto no início do turno).

Regras `deny`, 8 provas, todas barradas sem pergunta, com a mensagem "Permission to use Bash with command … has been denied": `gh repo view jonathanpah/hopper-documentation`; `gh api repos/jonathanpah/hopper-documentation/contents/README.md`; `gh repo delete jonathanpah/hopper-documentation-anth` (sem `--yes`); `git push --force`, `git push -f` e `git push +HEAD:…` contra o clone descartável `/tmp/prova-u1/clone-descartavel.git`; `git push --dry-run https://github.com/jonathanpah/hopper-documentation.git HEAD:prova-descartavel`; edição de `.claude/settings.local.json` pela ferramenta Edit ("File is in a directory that is denied by your permission settings"). Resultado: aprovado.

Regras `ask`, 5 provas, nenhuma gerou pedido de permissão ao proprietário, e os comandos rodaram: `echo hopper_documentation_anth.py migrar`; `gh pr merge --help`; `git push --dry-run origin HEAD:main` (dry-run, nada enviado; `git ls-remote` confirma a `main` em `b2954f2`); `git push --dry-run origin --delete prova-inexistente`; `git push --dry-run origin criterios-congelados`. O proprietário confirmou no chat que nenhum pedido apareceu ("onde aperto nao?"). Resultado: reprovado. As regras `ask` não produzem pedido nesta sessão da aba Code em modo `auto`, ao contrário do que `permission-modes.md` descreve. As 11 provas restantes de `ask` não foram feitas, porque o mecanismo não funciona. Situação: item 4 bloqueado na parte `ask`, com o mecanismo substituto da decisão D-06.

## V-U1-06 · U1, item 6 · Chamada real ao redator (C03, C04) · 2026-11-02 03:23 · aprovado

Comando de C03 completo (`claude -p --model claude-sonnet-5-5 --effort high --tools "" --strict-mcp-config --disable-slash-commands --no-session-persistence --output-format json --json-schema … --system-prompt …`, com `CLAUDE_CODE_SAFE_MODE=1`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` e `HOPPER_DOCUMENTATION_ANTH_RUN=1`), entrada pela entrada padrão, esquema com 1 campo `resumo`.

- MacBook, no ambiente da sessão do executor (o mesmo dos gatilhos da aba Code): `is_error=false`, `structured_output={"resumo": "Decisão: usar a cor azul no painel."}`, `modelUsage={"claude-sonnet-5-5": {"out": 68, "in": 2}}`, 1.503 ms, US$ 0,00848.
- VPS, conta `jpah`, ambiente limpo (`env -i`): `is_error=false`, mesmo `structured_output`, `modelUsage={"claude-sonnet-5-5": {"out": 68, "in": 2}}`, 1.893 ms, US$ 0,00448.
- Regra de C04: 100% dos tokens de saída do `claude-sonnet-5-5`. Aprovado nos 2.
- Observação: no terminal do MacBook (A1) com ambiente limpo, `claude auth status` mostra `loggedIn: false` e `claude -p` falha com "OAuth session expired and could not be refreshed" (03:22 UTC), mesmo depois de o proprietário informar login às 03:17 UTC. A1 depende de `claude auth login` no Terminal (pergunta P-02).

## V-U1-07 · U1, item 7 · Retomada (C21) · 2026-11-02 03:26 · aprovado

Comando: `claude -p 'Leia SPEC.md e a pasta execucao/. Diga em que unidade o trabalho está e qual é o próximo passo. Responda em até 8 linhas, em português.' --model sonnet --max-turns 20 --output-format json`, na cópia de trabalho, em sessão nova sem o contexto do executor. Resultado: 8 turnos, 23 s, US$ 0,18, `modelUsage` só `claude-sonnet-5-5`. A resposta disse U1 em andamento; itens 1, 2, 3 e 6 prontos; item 4 com `deny` aprovado e `ask` substituído por D-06; item 5 em andamento com A3 em prova, A1 dependente de P-02 e A2 de P-03; itens 7, 8 e 9 pendentes; próximo passo: destravar o item 5 e gravar V-U1-05. Igual a `estado.md` no momento da chamada. Chamada contada à parte das chamadas ao redator.

## V-U1-08 · U1, item 8 · Avaliação de acionamento com `claude plugin eval` · 2026-11-02 03:27 · aprovado

Comando: `claude plugin eval ./hopper-documentation-anth-pt-br --case '*sim-pede-handoff*' --ablation none --trust-plugin --model sonnet --output-dir <scratchpad>/eval-u1`, no ambiente da sessão do executor. Resultado: caso `sim-pede-handoff`, 3 execuções, nota 1,00 em todas (grader `skill-acionada`: Skill chamada 1 vez), 23 s, US$ 0,11. `--ablation none` e `--case` funcionam na CLI 2.1.296. Execução parcial, fora da contagem das execuções completas (C20).

## V-U1-05 · U1, item 5 · Plugin de sonda em A3 · 2026-11-02 03:22 a 03:30 · em andamento

Sonda instalada nos 3 ambientes (`claude plugin marketplace add ~/hopper-sonda/catalogo` e `claude plugin install sonda-precompact@hopper-sonda`; A2 usa a mesma instalação de A1). Sessões de teste conduzidas por pseudoterminal com `~/hopper-sonda/driver.py`, modelo Haiku 5.5, `CLAUDE_CODE_AUTO_COMPACT_WINDOW=100000` e `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70`. O diálogo de confiança da pasta nova vem com "No, exit" selecionado; o driver responde com seta para baixo e Enter.

**A3, medição (a3-medir).** Contexto inicial de uma sessão nova no terminal da VPS: 59.702 tokens (soma de `input_tokens`, `cache_creation_input_tokens` e `cache_read_input_tokens` do 1º registro `assistant`).

**A3, passagem 1 (a3-c1, sem fechar), sessão `fab76d38`.** Com 70%, a compactação automática disparou na 2ª mensagem. Registro da sonda (UTC): `sync-inicio` 03:23:20.474 com as chaves de entrada `custom_instructions`, `cwd`, `hook_event_name`, `prompt_id`, `scratchpad_dir`, `session_id`, `transcript_path`, `trigger` (`trigger` = `auto`); `async-inicio` 03:23:20.491 (os 2 comandos rodam em paralelo); `separado-inicio` 03:23:20.539; `sync-fim` 03:23:23.478; o registro `api-request` seguinte no histórico tem `timestamp` 03:23:23.548, 70 ms depois do fim do gatilho síncrono: a compactação esperou por ele. `CLAUDE_PID` = 3843582, executável `/home/jpah/.local/share/claude/versions/2.1.316`. `CLAUDE_PLUGIN_DATA` = `~/.claude/plugins/data/sonda-precompact-hopper-sonda` (confirma o nome `<plugin>-<catálogo>`). `separado-fim` 03:25:20.543, 120 s depois. Histórico: 43 linhas no início, 51 no fim, marca `SONDA-MARCA` presente depois da compactação. Achado: o histórico da versão 2.1.316 não tem registro próprio de compactação (nenhum `isCompactSummary`; tipos presentes: `user`, `assistant`, `attachment`, `api-request-shape`, `api-request-blob`, `api-request`, `system`, `cost-state` e registros de configuração). A conversa curta (1 troca) pode ter sido compactada sem resumo gravado. O marco observável da compactação é o registro `api-request` posterior ao gatilho.

**A3, passagem 2 (a3-c2, fechar 5 s depois do início), sessão `b6b83164`.** `sync-inicio` 03:26:43.749; `separado-inicio` 03:26:43.778; `sync-fim` 03:26:46.751; SIGHUP ao grupo de processos do Claude Code às 03:26:50; Claude Code morto. O processo separado, criado com `subprocess.Popen(start_new_session=True)` e esperado pelo gatilho assíncrono, **não gravou `separado-fim`** nem produziu erro no log: morreu junto com o Claude Code. Como ele estava em outra sessão de processos, o SIGHUP do grupo não o alcançou; a causa provável é o Claude Code encerrar a árvore de processos do gatilho ao sair (`headless.md`: "terminates the process tree"). Conclusão: `start_new_session=True` não basta para C08. Reprovado nessa forma.

**A3, passagem 3 (a3-c3).** Sonda versão 2: fork duplo com `setsid`, neto executado com o init como pai, e o gatilho assíncrono espera um arquivo marcador em vez de `wait()`. Resultado a registrar.
