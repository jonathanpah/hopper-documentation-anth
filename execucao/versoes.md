# Versões e acessos (U1, itens 1 e 2)

Leitura em 2026-11-02 02:36 UTC, pela sessão do executor. Mínimo do Claude Code pela spec: 2.1.284 (Sonnet 5.5).

| Ambiente | Claude Code | Caminho do executável | Python 3 | Sistema |
| --- | --- | --- | --- | --- |
| A1, terminal do MacBook (zsh de login) | 2.1.296 | `/Users/jonathan/.local/bin/claude` | 3.14.8, `/usr/local/bin/python3` | macOS (Darwin 27.2.0) |
| A2, aba Code do Claude Desktop (executável apontado por `CLAUDE_PID`, método do item 1 de U1) | 2.1.309 | `/Users/jonathan/Library/Application Support/Claude/claude-code/2.1.309/5af865b9901c/claude.app/Contents/MacOS/claude` | 3.14.8, `/usr/local/bin/python3` (ambiente da ferramenta Bash, o mesmo dos gatilhos) | macOS, Claude Desktop 4.4212.0 |
| A3, VPS `hopper`, conta `jpah` (alias `hopper-jpah`) | 2.1.316 | `/home/jpah/.local/bin/claude` (fora do `PATH` das sessões SSH não interativas) | 3.13.5, `/usr/bin/python3` | Debian GNU/Linux 13 (trixie) |
| VPS `hopper`, conta `jonathan` (alias `hopper-jonathan`), só instalação | 2.1.308 | `/home/jonathan/.local/bin/claude` | 3.13.5 | Debian GNU/Linux 13 (trixie) |

## Acessos

| Acesso | Resultado |
| --- | --- |
| `ssh hopper-jpah` | ok, `hostname` = `hopper`, usuário `jpah`, `/home/jpah/projects/mallmetrics` existe, `sudo -n true` ok |
| `ssh hopper-old-jpah` (conferência de 2026-11-02 00:40 UTC) | responde, `hostname` = `hopper`, mas `/home/jpah/projects/mallmetrics` não existe. Não é A3. |
| `ssh hopper-jonathan` | ok, usuário `jonathan`, Claude Code 2.1.308 |
| `gh auth status` | conta `jonathanpah`, escopos `gist`, `read:org`, `repo`, `workflow`; permissão `admin` e `push` no anth |
| Ferramentas de sessão na sessão do executor | ver V-U1-02 em `verificacoes.md` |
| Uso do computador na sessão do executor | ver V-U1-02 em `verificacoes.md` |

## Plugins instalados antes da execução (2026-11-02)

| Conta | `hopper-documentation-anth` | Origem (`Read from`) | Outras pastas em `plugins/data/` com `hopper-documentation` |
| --- | --- | --- | --- |
| MacBook, `jonathan` | 0.1.4, ativado | `~/Library/Application Support/hopper-documentation-anth/releases/0.1.4/pt-br` | `hopper-documentation-anth` (com `venv`), `hopper-documentation-anth-inline`, `hopper-documentation-anth-hopper-documentation-anth` (vazia, do Claude Code) |
| VPS, `jpah` | 0.1.4, ativado | `/opt/hopper-documentation-anth/releases/0.1.4/pt-br` | `hopper-documentation-anth` (com `venv`), `hopper-documentation-inline`, `hopper-documentation-anth-hopper-documentation-anth` |
| VPS, `jonathan` | a conferir em U8 | | `hopper-documentation-anth` |
