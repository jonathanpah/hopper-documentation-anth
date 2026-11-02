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

**A3, passagem 3 (a3-c3, fechar 5 s depois do início), sessão `1d4c0d45`.** Sonda versão 2: fork duplo com `setsid`, neto executado com o init como pai (`ppid` 1), e o gatilho assíncrono espera um arquivo marcador em vez de `wait()`. `sync-inicio` 03:31:15.899; `async-separado-criado` 03:31:15.908; `separado-inicio` 03:31:15.935 com `ppid` 1; `sync-fim` 03:31:18.902; SIGHUP ao grupo do Claude Code às 03:31:22, Claude Code morto; **`separado-fim` 03:33:15.938**, 120 s depois do início, e o arquivo marcador gravado. O gatilho assíncrono morreu com o Claude Code (sem `async-fim`), como esperado. Aprovado: o processo separado sobrevive ao fechamento do Claude Code quando criado por fork duplo com `setsid`.

**Situação do item 5.** A3: aprovado em todos os subitens (gatilho síncrono antes da compactação e compactação à espera; processo separado sobrevive, com fork duplo; JSON de entrada com `session_id`, `transcript_path`, `cwd` e `trigger`; `CLAUDE_PID` aponta para o executável; o histórico mantém as mensagens anteriores; condução por pseudoterminal com resposta ao diálogo de confiança; valor de `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` = 70 com janela de 100 mil tokens dispara a compactação na 2ª mensagem a partir de um contexto inicial de 59,7 mil tokens; para o roteiro de aceite, com 6 mensagens curtas antes, o valor precisa ser maior, a calibrar em U8 com a mesma medição). A1: bloqueado, Terminal sem login (P-02). A2: bloqueado, pasta de teste não confiada (P-03); a própria sessão do executor é uma sessão da aba Code com a sonda instalada e vai registrar o gatilho na próxima compactação dela.

## V-U1-02 (repetição) · Acessos · 2026-11-02 03:51 · aprovado

`ssh -o BatchMode=yes hopper-old-jpah`, repetido dentro de U1: `hostname` = `hopper`, usuário `jpah`, `/home/jpah/projects/mallmetrics` inexistente ("Arquivo ou diretório inexistente"). Confirma que A3 é só `hopper-jpah`. Atende ao achado 2 da revisão U1-passada-1.

## V-U1-04 · tentativa 3 · 2026-11-02 03:50 · provas `deny` completas · aprovado

Atende ao achado 4 da revisão U1-passada-1. Mais 4 provas, todas barradas: `gh repo view jonathanpah/hopper-documentation` (nome no fim do comando, regra `Bash(gh *jonathanpah/hopper-documentation)`); `git push /tmp/prova-u1/clone-descartavel.git -f HEAD:prova-descartavel` (regra `Bash(git push * -f *)`); `git push /tmp/prova-u1/clone-descartavel.git HEAD:prova-descartavel -f` (regra `Bash(git push * -f)`); gravação de `.claude/settings.local.json` pela ferramenta Write ("File is in a directory that is denied by your permission settings", regra `Edit(...)`, que cobre a ferramenta Write). Com as 8 provas da tentativa 2 (`gh repo view … --json name` para a regra com espaço, `gh api repos/jonathanpah/hopper-documentation/contents/README.md` para a regra com barra, `gh repo delete`, `git push --force`, `git push -f <destino> …`, `git push … +HEAD:…`, `git push --dry-run https://github.com/jonathanpah/hopper-documentation.git …` e a ferramenta Edit), as 12 regras `deny` de D-05 têm prova. As 2 regras `Edit` (caminho relativo e absoluto) apontam o mesmo arquivo e foram provadas pelas 2 ferramentas; o registro não distingue qual das 2 casou.

Correção de cronologia (achado 6): os horários de V-U1-04 foram estimados. Ordem real, pela saída do comando `date -u` (02:43:31Z) e pela ordem dos registros desta sessão: arquivo de regras criado e provas da tentativa 1 entre 02:38 e 02:41 (ainda na pasta de origem); `change_directory` em 02:41; tentativa 2 entre 02:43 e 02:46; D-05, D-06 e P-01 gravadas em 02:46 e 02:47. Ressalva (achado 5): a prova da regra `git push *hopper-documentation.git*` usou a URL real com `--dry-run`, e não um alvo descartável; a regra barrou o comando antes de qualquer execução.

## V-U1-05 (continuação) · 2026-11-02 03:55 · correções da revisão U1-passada-1

- Intervalo do cabeçalho de V-U1-05: as 3 passagens rodaram de 03:22:40 a 03:33:16 (achado 13).
- O valor de `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` **não está aprovado** (achado 10): 70 dispara a compactação na 2ª mensagem. Calibração em andamento com 85 (`a3-c4`), com a contagem de mensagens até a compactação; o valor aprovado para F-K entra em V-U1-05 quando a calibração terminar.
- Marco da compactação (achado 11): os registros `system` do histórico `fab76d38` têm só o subtipo `turn_duration`; as 2 linhas com "compact" no texto são o `api-request-shape` (texto do prompt do sistema) e um `attachment` `prompt_snapshot`. Nenhum registro descreve a compactação. D-11 fica como está, com essa evidência.
- Tentativa (achado 14): a passagem 2 (sonda v1) reprovou e a passagem 3 (sonda v2, fork duplo) aprovou; é 1 tentativa, registrada em `tentativas.md`.
- Saídas brutas (achado 16): `registro.jsonl` e `resultado-a3-c1.json`, `-c2`, `-c3` da VPS, `saida-a1-medir*.log` do MacBook, `sonda.py`, `hooks.json` e `driver.py` copiados para `execucao/sonda/`; `aggregate-result.json` da avaliação copiado para `execucao/avaliacoes/u1/`.
- A2, registro no formato de C20 (achado 12): `item 5, A2 · bloqueado · motivo: a sessão de teste não pode ser aberta na pasta de teste · evidência: ferramenta start_session (initiation user_asked, context fresh, cwd /Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-sonda-a2, use_worktree false, model claude-haiku-5-5), 1ª chamada às 03:16 UTC: "…hopper-sonda-a2 on this computer is not a trusted workspace yet and the app could not ask the user to trust it (the Code tab is not showing this conversation, or another trust prompt was open). Nothing started"; 2ª chamada às 03:22 UTC: "Permission for this action was denied by the Claude Code auto mode classifier … judged this action dangerous" · como reproduzir: chamar start_session com esses parâmetros em uma pasta ainda não confiada`. A via alternativa (uso do computador, C26) exige o pedido de acesso ao aplicativo Claude, que é um pedido de permissão ao proprietário; o proprietário pediu para não receber pedidos esta noite (D-08). P-03 pede ao proprietário só a aprovação da pasta (ato de permissão, como o "sim" da seção 10), e não uma tarefa.
- Item 8 (achado 15): rodou no ambiente da sessão do executor (A2) com o executável 2.1.296 de A1; repetir em A1 quando o Terminal tiver login (P-02).
- Item 1 (achado 1): o Python do ambiente do gatilho em A2 fica provado quando a sonda registrar o gatilho em A2 (`executavel` e `sys.executable` no registro).
- C08 e `setsid` (fora do escopo 2): `os.setsid()` existe no macOS; o que não existe é o programa `setsid`. A prova de D-10 no macOS depende de A1 (P-02).

## V-U2-01 · U2 · Testes de aceite no código da versão atual (G04) · 2026-11-02 03:56 · reprovações registradas

Comando: `HOPPER_DOCUMENTATION_ANTH_PACOTE=hopper-documentation-anth-pt-br TZ=UTC python3 -m unittest discover -s aceite/testes -p 'test_*.py' -v`, na cópia de trabalho com o código da versão 0.1.4 (commit `fb208df`). Resultado: `Ran 31 tests`, `FAILED (failures=29, errors=2)`; nenhum teste passa. Os 2 erros (T24 e T31) são `IndexError` ao ler o registro de rodadas, que a versão atual não grava. Saída completa em `execucao/avaliacoes/u2/aceite-versao-atual-pt-br.log`. Casos do conferidor: `valida` aprova F1 a F8 e F10 (F9 reprova sem a conversa de teste, como esperado), e cada `invalida-F<n>` reprova em F<n> (F1 também em F5 e F2 também em F8, por falta do mesmo objeto, como o Anexo F admite).

| Teste | Resultado no código atual |
| --- | --- |
| test_R01_primeira_rodada_cria_a_pasta_de_documentacao | FAIL |
| test_R02_pasta_da_conversa_com_a_data_da_primeira_mensagem | FAIL |
| test_R03_grava_so_na_pasta_de_documentacao_e_na_pasta_de_dados | FAIL |
| test_R04_acrescenta_so_o_novo | FAIL |
| test_R04_espera_o_arquivo_de_historico_parar_de_crescer | FAIL |
| test_R05_cabecalhos_comentarios_e_texto_do_caso_b1 | FAIL |
| test_R06_uma_linha_por_ferramenta_sem_resultado | FAIL |
| test_R07_oculta_senhas_tokens_e_chaves | FAIL |
| test_R08_inclui_usuario_claude_respostas_planos_mensagens_de_agente_interrupcoes_e_anexos | FAIL |
| test_R09_exclui_lembretes_gatilhos_notificacoes_resumos_subagentes_raciocinio_e_resultados | FAIL |
| test_R10_conta_uma_vez_registros_repetidos | FAIL |
| test_R11_envia_so_o_trecho_novo_e_os_documentos_atuais | FAIL |
| test_R12_chama_o_redator_com_as_opcoes_de_C03_e_descarta_resposta_invalida | FAIL |
| test_R13_acrescenta_um_bloco_por_intervalo | FAIL |
| test_R14_numera_com_o_proximo_numero_livre | FAIL |
| test_R16_aplica_mudancas_de_situacao_e_registra_as_inexistentes | FAIL |
| test_R17_reescreve_o_documento_7_inteiro | FAIL |
| test_R18_reescreve_o_documento_1 | FAIL |
| test_R22_gatilho_de_copia_termina_em_60_segundos_e_sai_com_0 | FAIL |
| test_R24_falha_de_rodada_fica_no_registro_no_documento_1_e_no_aviso | ERROR |
| test_R27_uma_rodada_por_conversa_por_vez | FAIL |
| test_R28_nada_novo_nao_chama_o_redator_nem_altera_os_documentos | FAIL |
| test_R29_rodada_interrompida_e_concluida_pela_seguinte | FAIL |
| test_R30_migra_handoffs_do_anth_e_do_clone_de_leitura | FAIL |
| test_R31_so_apaga_depois_da_verificacao_interna | ERROR |
| test_R32_inventario_da_main | FAIL |
| test_R35_dois_pacotes_com_o_mesmo_programa | FAIL |
| test_R37_encontra_o_historico_pela_pasta_de_configuracao | FAIL |
| test_R38_encontra_o_executavel_do_claude_code | FAIL |
| test_R41_skill_md_com_as_secoes_e_menos_de_500_linhas | FAIL |
| test_R42_migracao_automatica_desligada | FAIL |
| total | 31 testes, todos reprovados (31) |

## V-U1-05 (calibração) · `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` em A3 · 2026-11-02 03:51 a 03:59 · aprovado para A3

Passagem `a3-c4`, sessão nova com janela de 100 mil tokens e 85%: contexto inicial 59.703 tokens; a 1ª resposta de enchimento somou 5.711 tokens de saída; a compactação disparou na 3ª mensagem, com o contexto em cerca de 65,5 mil tokens. Com 70% ela disparou na 2ª mensagem (`a3-c1`). Leitura: o limite efetivo é cerca de 0,765 × percentual mil tokens (janela de 100 mil menos a reserva), ou seja, 53,5 mil com 70% e 65 mil com 85%. Para o passo F-K em A3, com 6 mensagens curtas e 1 criação de arquivo (cerca de 2 a 3 mil tokens) depois do contexto inicial, o valor aprovado é **90** (limite de cerca de 68,9 mil tokens): a compactação não acontece antes das 6 mensagens e acontece depois de 1 ou 2 mensagens de enchimento. Em A1 e A2 o contexto inicial é outro e o valor é medido quando o ambiente destravar (P-02, P-03), pela mesma regra: `percentual = teto(((contexto inicial + 6.000) / 765))`. Resultado bruto em `execucao/sonda/a3/resultado-a3-c4.json`. Observação: a partir de 03:57:21 UTC o histórico mostra registros `assistant` com uso zero a cada 4 segundos; é o limite de uso do plano do proprietário (erro 429, "session limit · resets 2:30am America/Sao_Paulo"), que também derrubou o revisor independente de U2 às 04:0x UTC. As chamadas reais ficam indisponíveis até 05:30 UTC.

## V-U2-02 · U2 · Correções de critérios antes do congelamento · 2026-11-02 09:57

Correções feitas nos testes de aceite enquanto os critérios ainda não estavam congelados (sem tag nem manifesto), ao rodá-los contra a implementação: (1) `apoio.py` resolve o caminho da pasta temporária (`/var` vira `/private/var` no macOS); (2) T27, 2º cenário: a 1ª rodada usa a escala 0,01, e só a 2ª usa 0,001, porque a escala 0,001 também encurta o tempo-limite do redator; (3) T29 compara o corpo do documento 2, porque o cabeçalho traz a pasta do projeto, que muda por ambiente; (4) T38 usa link simbólico para o executável falso, porque uma cópia de binário do sistema é morta no macOS (código 137); (5) T11 aceita "Tarefa:" ou "Task:", tradução fiel no pacote em inglês. Nenhuma correção muda o que a spec exige.

## V-U3-U7 · U3 a U7 · Testes de aceite e do executor na versão 2 · 2026-11-02 09:57 · aprovado

Comandos: `python3 -m unittest discover -s aceite/testes` com `HOPPER_DOCUMENTATION_ANTH_PACOTE` em `hopper-documentation-anth-pt-br` e em `hopper-documentation-anth-en`, `TZ=UTC`; `python3 -m unittest discover -s tests` em cada pacote; `claude plugin validate --strict` nos 2 pacotes. Resultado: 31 testes de aceite aprovados em cada pacote (`Ran 31 tests … OK`), 5 testes do executor aprovados em cada pacote, validação aprovada nos 2. Requisitos cobertos pelos testes: R01 a R14, R16 a R18, R22, R24, R27 a R32, R35, R37, R38, R41 e R42. Pendentes de prova com dados reais em U8: R19 a R21, R23, R25, R26, R33, R36 (verificação do GitHub), R39 e R40. R34 fica para U10.

## V-U8-01 · U8 · Instalação da versão 2.0.0 (passo F-I, parte 1) · 2026-11-02 09:57 · aprovado em parte

Pré-autorizado por D-08. Em cada conta, nesta ordem: `config.json` com `{"migracao_automatica": false}` na pasta de dados; pasta de produção `releases/2.0.0/pt-br` copiada do commit `e2dfa59` da branch de trabalho; `claude plugin uninstall hopper-documentation-anth@hopper-documentation-anth` (0.1.4); `claude plugin marketplace remove hopper-documentation-anth`; `marketplace add` com a pasta de produção; `plugin install`.
- MacBook, `jonathan` (A1 e A2): `claude plugin list` mostra 2.0.0, `Read from: ~/Library/Application Support/hopper-documentation-anth/releases/2.0.0/pt-br`, `Status: enabled`; `details`: Skills (1), Hooks (1) PreCompact.
- VPS, `jpah` (A3): 2.0.0, `Read from: /opt/hopper-documentation-anth/releases/2.0.0/pt-br`; `details`: Skills (1), Hooks (1) PreCompact. Pasta de produção `root:root`, 0755 e 0644.
- VPS, `jonathan`: 2.0.0, mesma pasta de produção.
Faltam: a lista de hooks com os 2 comandos (A1 e A3, por pseudoterminal), os passos F-C, F-A, F-K e F-V, que dependem de chamadas reais (limite do plano até 05:30 UTC), de A1 (P-02) e de A2 (P-03).

## V-U8-01 (correção) · 2026-11-02 10:00

A desinstalação da 0.1.4 apagou a pasta de dados e o `config.json` gravado antes (D-14). O arquivo foi regravado nas 3 contas (MacBook `jonathan`, VPS `jpah` e `jonathan`) com `{"migracao_automatica": false}` e conferido por leitura. Nenhuma rodada da versão 2 rodou antes disso (nenhum `rodadas.jsonl` existia). N12 preservada.

## V-U1-02 (correção de A1) · 2026-11-02 10:08 · A1 desbloqueado

O bloqueio de A1 (P-02) estava errado. No painel de Terminal do app, que roda o shell de login do proprietário fora do isolamento da ferramenta Bash, `claude auth status` mostra `"loggedIn": true` e `"authMethod": "claude.ai"`, e `claude -p 'Responda so com a palavra ok.' --model haiku` respondeu "ok". O registro do Chaves do macOS (`Claude Code-credentials`) tem data de alteração 2026-11-02 03:17:03 UTC, o horário em que o proprietário informou o login. Causa do falso bloqueio: a ferramenta Bash da sessão do executor roda isolada e não lê o Chaves do macOS, então o `claude` iniciado por ela aparece sem login. Consequência para o método: os testes de A1 rodam pelo painel de Terminal (ferramenta `run_in_terminal`), e não pela ferramenta Bash. P-02 retirada sem resposta do proprietário.

## V-U8-02 · U8 · Roteiro de aceite em A3 (F-C, F-A, F-K, F-V) · 09:59 a 10:09 · reprovado em F2 e F9

Sessão `9a0a7706` em `~/hopper-teste-a3`, Sonnet, janela de 100 mil e 90%. Resultados reais da versão 2.0.0:
- F-C: as 6 mensagens enviadas; a skill rodou a pedido 2 vezes (a mensagem 1, "Vamos testar a documentação…", também acionou a skill), com escrita concluída M1 a M4 e M5 a M13, só `claude-sonnet-5-5` em `modelos`.
- F-K passagem 1: compactação automática às 10:02:36; cópia concluída às 10:02:37; rodada do gatilho concluída às 10:03:17 (M14 a M15). Uma 2ª compactação às 10:03:01 (o contexto depois da 1ª continuou acima do limite de teste) terminou em "nada novo".
- F-K passagem 2: compactação às 10:08:20, cópia às 10:08:22, Claude Code fechado às 10:08:27, **rodada concluída às 10:08:57 (M16 a M18), 30 s depois do fechamento**. R23 provado em A3 com o plugin real.
- F-V (conferidor com roteiro): 8 aprovadas, 2 reprovadas. **F2**: uma resposta do Claude contém linhas que começam com "## " (títulos copiados do SKILL.md), e a leitura do documento 2 por "\n## " as toma por cabeçalhos de mensagem. O mesmo defeito existe na leitura do documento 2 pelo programa (`Documento2.mensagens`). **F9**: a mensagem 2 do roteiro tem a senha, que o documento 2 grava como "[oculto]", e a busca pelo texto literal não a encontra. Os 2 defeitos são de critério (conferidor e roteiro) e de entrega (leitura do documento 2), a corrigir antes do congelamento.
Pasta de documentação e resultado bruto em `execucao/aceite/a3/`.

## Pausa · 2026-11-02 10:10

Execução pausada a pedido do proprietário ("pause"). Interrompidos: avaliações de acionamento completas do pacote em português (sem resultado), 3 revisões independentes (U2, U3-U4-U6, U5-U7; retomáveis) e a medição de A1 no painel de Terminal. Observação: depois do falso bloqueio de A1, o arquivo `.claude/settings.local.json` recebeu regras `allow` gravadas pelo app a partir de aprovações do proprietário, o que indica que pedidos de permissão chegaram a ele; D-06 precisa ser revista na retomada.

## V-U8-02 (correção) · 2026-11-02 13:07 · F2 e F9 corrigidos

- Entrega: `Documento2.mensagens` passa a reconhecer como cabeçalho só a linha `## M<n>-<código> · …` seguida da linha do comentário de registros. Pacote em inglês regenerado (difere só em `LANGUAGE`).
- Critérios (ainda não congelados): o conferidor aplica a mesma regra; `aceite/roteiro.json` ganha `mensagens_no_documento_2`, com a mensagem 2 como gravada (`{oculto}`); o caso `valida` do conferidor ganha uma linha "## Plano" dentro da mensagem do Claude, e os casos `invalida-F<n>` foram regenerados; teste novo `test_R05_titulo_no_texto_de_uma_mensagem_nao_e_cabecalho`, que falha sem a correção.
- Resultados: conferidor nos casos (valida 9 de 9; cada invalida reprova na verificação dela); conferidor com roteiro na pasta real de A3 (`execucao/aceite/a3/`): **10 de 10 aprovadas**; testes de aceite: 32 de 32 nos 2 pacotes; testes do executor: aprovados nos 2.

## V-CODEX-01 · Tarefa 01 do Codex (revisão U5-U7) · 2026-11-02 13:27 · aprovado pelo verificador

Codex 0.166.0, `gpt-6.1-sol`, `xhigh`, modo Fast, `--sandbox workspace-write`; relatório em `execucao/codex/tarefa-01-relatorio.md`. Conferência própria do verificador, depois do fim da tarefa: testes de aceite 32 de 32 nos 2 pacotes; testes do executor 13 de 13 nos 2 (8 novos); `diff` dos 2 programas só na linha `LANGUAGE`; 14 arquivos alterados, nenhum em `SPEC.md`, `aceite/`, `.github/` ou `.claude/`. Verificação do GitHub do commit `62ce2d5` (antes da tarefa): critérios congelados reprova (manifesto ausente, esperado até U2); T38 reprova no Ubuntu (`/proc/<pid>/exe` resolve o link simbólico do executável falso), a corrigir na tarefa 02; macOS aprovado.

## V-CODEX-02 · Tarefa 02 do Codex (revisões U3-U6 e U2, condutor) · 2026-11-02 13:55 · aprovado pelo verificador

Relatório em `execucao/codex/tarefa-02-relatorio.md` (o Codex obteve 41 de 42 no aceite porque o isolamento dele bloqueia `/bin/ps`, usado por T38). Conferência própria do verificador: testes de aceite **42 de 42** nos 2 pacotes; testes do executor **31 de 31** nos 2 (18 novos); `diff` dos 2 programas só em `LANGUAGE`; conferidor: `valida` 9 de 9, `valida-roteiro` 10 de 10, os 11 casos `invalida-*` reprovam na verificação deles (inclusive `invalida-F2-sem-registros` e `invalida-F9` com `--roteiro`); pasta real de A3: 10 de 10. G04: os testes finais contra o código da versão atual (`8dbb40b`) dão `Ran 42`, `FAILED (failures=35, errors=5)`; os 4 que passam são do conferidor (`test_conferidor.py`), que não depende do programa; o teste novo de T05 passa no programa corrigido e reprova no programa de `7bcdf5d`. Saídas em `execucao/avaliacoes/u2/`. Nenhuma alteração em `SPEC.md` nem em `.claude/`.

## V-CODEX-03 · Tarefa 03 do Codex (T38 e T04 nos executores do GitHub) · 2026-11-02 16:33 · aprovado pelo verificador

A 1ª execução da tarefa ficou parada por cerca de 2h20 esperando a entrada padrão (o comando do Codex foi encadeado sem `< /dev/null`), sem alterar arquivos; foi encerrada e repetida com a entrada fechada. Mudanças: T38 usa o próprio interpretador como processo de `CLAUDE_PID` no Linux e um script como candidato de `~/.local/bin/claude`; T04 usa escala 0,5. Conferência própria: 42 de 42 nos 2 pacotes; os 2 testes alterados passaram em 3 repetições seguidas; programa sem alteração.

## V-U2-03 · U2 · Congelamento dos critérios (C18) · 2026-11-02 16:44

Verificação do GitHub do commit `cae0d61`: os 8 jobs de testes (Ubuntu 24.04 e macOS, Python 3.9 e 3.13, 2 pacotes) e o job do conferidor e do inventário aprovados; só o job de critérios congelados reprovado, por falta do manifesto, como esperado antes do congelamento. Manifesto `aceite/MANIFESTO.sha256` gerado com `shasum -a 256` sobre `git ls-files aceite .github/workflows/verificar.yml SPEC.md` (sem o próprio manifesto): 129 arquivos, conferência local 129 OK. Tag `criterios-congelados` no commit do manifesto, com o "sim" antecipado de D-08.

## V-U2-04 · U2 · Prova de C18 · 2026-11-02 18:14 · aprovado

Branch descartável `prova-c18`, a partir do commit congelado `e737aca`. Commit `a0c61f7` (1 caractere a mais em `aceite/casos/b1/esperado-pt-br.md`): job de critérios congelados reprovado com `aceite/casos/b1/esperado-pt-br.md: FAILED` e "CRITÉRIO ALTERADO: um critério congelado não confere com o manifesto". Commit `3e486e7` (1 caractere alterado em `.github/workflows/verificar.yml`): reprovado com `.github/workflows/verificar.yml: FAILED` e a mesma mensagem. No commit congelado, o job de critérios congelados passou. A branch foi apagada do GitHub e do clone (D-08). Um job de macOS do commit congelado terminou como "cancelado" e foi mandado rodar de novo.

## V-U8-03 · U8 · Roteiro de aceite em A3, 2ª execução (tarefa 04 do Codex) · 2026-11-02 18:14 · reprovado em F8

Relatório em `execucao/codex/tarefa-04-relatorio.md`; dados em `execucao/aceite/a3-2/`. Sessão `67ed412f`, contexto inicial 58.979 tokens, 85%. Depois da mensagem 6, o conferidor aprovou 10 de 10. No fim das 2 passagens de F-K, 9 de 10: F8 reprovou porque o documento 7 cita `M19-67ed412f` ("a próxima rodada deve cobrir M19 em diante"), mensagem que não existe. Defeito de entrega: o programa não confere as referências dos campos de texto da resposta (R20). R23 aprovado (escrita concluída 39 s depois do fechamento). R22 aprovado na 1ª passagem (cópia antes do marco de D-11); na 2ª passagem o marco não existe porque a sessão foi fechada durante a compactação, o que é o objetivo dessa passagem. R25 e R39 com evidência positiva em A3. 4 escritas concluídas, só `claude-sonnet-5-5`. Contexto inicial medido em A1 pelo painel de Terminal: 58.874 tokens (percentual 85).

## V-CODEX-05-06 · Tarefas 05 e 06 do Codex (R20 e caso de borda de R14) · 2026-11-02 18:29 · aprovado pelo verificador

Tarefa 05: o programa confere os identificadores citados nos campos de texto da resposta e pede 1 nova resposta ao redator quando só essa conferência falha; `modelos.md` e `templates.md` ganharam a regra de citação. Ela reprovou T14 (congelado), porque recusava a citação de um item apagado à mão. Tarefa 06: aceita item de número até o maior já usado do tipo e do código (caso de borda de R14), e mantém a exigência de que a mensagem citada exista. Conferência própria: aceite 42 de 42 nos 2 pacotes; executor 43 de 43 nos 2; programas iguais exceto `LANGUAGE`; manifesto 129 de 129 OK.

## V-U8-04 · U8 · Roteiro de aceite em A1 (Terminal do MacBook) · 2026-11-02 18:47 · aprovado

Rodado pelo verificador no painel de Terminal (D-22), com o commit `715b229` instalado. Sessão `91348fa6`, pasta `~/hopper-teste-a1`, Sonnet, janela de 100 mil e 85% (contexto inicial 58.874 tokens). Conferidor com o roteiro: **10 de 10**. Registro de rodadas (`execucao/aceite/a1/rodadas.jsonl`): 2 rodadas a pedido concluídas (M1 a M2 e M3 a M12); 1ª compactação às 18:36:41 UTC com cópia concluída às 18:36:43 e escrita concluída às 18:37:17 (M13 a M16); 2ª compactação às 18:38:37, cópia às 18:38:38, Claude Code fechado às 18:38:43 e **escrita concluída às 18:39:11 (M17 a M18), 28 s depois do fechamento**, no macOS (R23 e K10). Dados em `execucao/aceite/a1/`.

## V-U8-05 · U8 · Roteiro de aceite em A3, 3ª execução (tarefa 07 do Codex) · 2026-11-02 18:47 · reprovado em R23

Relatório em `execucao/codex/tarefa-07-relatorio.md`. Conferidor 10 de 10, mas a escrita da 2ª passagem falhou com "origem inválida: M17-958e55b3": o redator citou como origem de um item uma mensagem do trecho anterior, e o Anexo D exige origem no trecho novo ou em item existente. A nova tentativa da tarefa 05 vale só para referências inexistentes, e não para origem fora do trecho. R22 (1ª passagem) e R25 aprovados.
