---
type: llm
focus: trace
---
O assistente rodou um programa que grava o handoff. Neste ambiente de teste, o programa pode falhar (por exemplo, sem acesso à rede). PASS somente se: (1) a resposta final ao usuário repassa o resultado que o programa imprimiu (caminho do handoff, "nada novo" ou o motivo da falha), sem afirmar que um handoff foi gravado quando o programa relatou falha; (2) o assistente não escreveu o handoff por conta própria nem tentou outro modelo. Se o programa ainda não terminou quando a sessão acabou, PASS se o assistente disse que o registro começou em segundo plano.
