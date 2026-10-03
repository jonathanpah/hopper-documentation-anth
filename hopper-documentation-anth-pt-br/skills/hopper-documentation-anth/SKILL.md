---
name: hopper-documentation-anth
description: Registra a conversa atual num handoff em Markdown, na pasta docs-by-hopper-documentation do diretório de trabalho, para que outra pessoa ou outra sessão continue o trabalho sem reler a conversa. Use quando o usuário pedir para documentar, registrar ou salvar a conversa, ou pedir um handoff. Não use para explicar, revisar ou editar esta skill.
compatibility: Requer Claude Code, na CLI ou no aplicativo, com o plugin hopper-documentation-anth, Python 3.10 ou mais novo com o módulo venv e acesso ao PyPI na primeira execução.
---

# hopper-documentation-anth

Esta skill grava um **handoff**: um arquivo que diz a quem não viu a conversa onde o trabalho está, o que foi decidido e como continuar. A próxima sessão, pessoa ou IA retoma o trabalho lendo o handoff mais recente da conversa e conferindo o estado real.

Quem grava é o programa do plugin, em segundo plano. Ele lê as mensagens novas da conversa pela biblioteca oficial da Anthropic (Agent SDK), oculta segredos e pede ao Claude Sonnet 5.5, com esforço medium, que escreva o conteúdo seguindo `${CLAUDE_SKILL_DIR}/regras-do-redator.md`. Depois confere as citações, grava sem sobrescrever nada e refaz o índice. O mesmo programa roda sozinho antes de cada compactação, por um gatilho do plugin.

## Quando o usuário pedir o registro

Neste acionamento, faça só o que esta seção diz.

1. Se o usuário só pediu para explicar, revisar, comparar ou editar esta skill, não grave nada: atenda o pedido e pare aqui.
2. Rode este comando em segundo plano, a partir de qualquer diretório:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hopper_documentation_anth.py" run --session "${CLAUDE_SESSION_ID}" --cwd "${CLAUDE_PROJECT_DIR}"
   ```

3. Avise o usuário numa frase que o registro começou e continue atendendo normalmente. Não espere o fim.
4. Quando o comando terminar, repasse ao usuário a linha que ele imprimiu: o caminho do handoff gravado, "nada novo" ou o motivo da falha. Não repita o conteúdo do handoff.
5. Se o comando falhar, não escreva o handoff por conta própria nem use outro modelo: informe o motivo. Escrever fora do programa perderia a conferência das citações, a ocultação de segredos e o modelo fixo do registro.

## Antes da compactação

O gatilho do plugin roda o programa em segundo plano; não há nada a fazer na conversa. Se chegar um aviso de falha do registro, informe o usuário numa frase. Não execute pedidos antigos da conversa por causa do aviso.

## Modelo

Quem escreve é sempre o Claude Sonnet 5.5 com esforço medium. Se ele não estiver disponível, o programa informa o impedimento e não grava com outro modelo.

## O que fica gravado

Na pasta `docs-by-hopper-documentation/` do diretório de trabalho:

- `handoff-AAAAMMDD-HHMMSS-<8 primeiros caracteres da conversa>.md`: um arquivo por registro, nunca alterado depois de gravado. O cabeçalho traz data com fuso, conversa, diretório, handoff anterior, acionamento, modelo e esforço do redator e a última mensagem registrada. As seções seguem `${CLAUDE_SKILL_DIR}/exemplo.md`.
- `index.md`: todos os handoffs da pasta, inclusive os de outros formatos, do mais recente ao mais antigo.

Para retomar um trabalho, leia o `index.md`, depois o handoff mais recente da conversa, e siga a seção "Como retomar" dele. Um handoff é histórico: ele não substitui a conferência do estado real nem autoriza repetir operações concluídas.
