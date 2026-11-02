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
