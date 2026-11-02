# Perguntas ao proprietário

O proprietário recebe as perguntas juntas, no chat da sessão do executor, no fim de cada unidade (G07). Cada pergunta traz a resposta recomendada. Datas em UTC.

| Nº | Unidade | Data | Pergunta | Resposta recomendada | Entregue em | Resposta |
| --- | --- | --- | --- | --- | --- | --- |
| P-01 | U1 | 2026-11-02 02:43 | As regras `ask` da seção 10 não geram pedido de permissão nesta sessão. Confirma o mecanismo substituto da decisão D-06 (pergunta direta no chat antes de cada ação que exige o "sim", com as regras `deny` mantidas)? | Sim. É o mesmo mecanismo usado para incorporar o PR #2, e as regras `deny` continuam barrando as ações proibidas. | 2026-11-02 02:48, no chat | Sim (D-08) |
| P-02 | U1 | 2026-11-02 03:23 | O Claude Code do Terminal (A1) está sem login (`claude auth status` → `loggedIn: false`). Pode rodar `claude auth login` em uma janela do Terminal e concluir o login no navegador? | Sim, assim que puder. Até lá, A1 fica bloqueado e o resto segue. | 2026-11-02 03:25, no chat | |
| P-03 | U1 | 2026-11-02 03:23 | A abertura da sessão de teste de A2 na pasta `Dropbox/5-ai/5-claude/hopper-sonda-a2` foi recusada (pasta ainda não confiada; classificador do modo auto). Pode abrir essa pasta 1 vez em "New session" no app, para ela ficar confiada? | Sim. Sem isso, a prova de A2 usa só a própria sessão do executor, sem a interrupção de C25. | 2026-11-02 03:25, no chat | |
