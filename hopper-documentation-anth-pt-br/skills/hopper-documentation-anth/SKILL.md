---
name: hopper-documentation-anth
description: Documenta a conversa atual do Claude Code em 7 documentos (índice, conversa integral, conversa simplificada, decisões, funções implementadas, pendências e handoff) na pasta docs-by-hopper-documentation do projeto. Use quando o usuário pedir para documentar ou registrar a conversa, salvar o progresso ou fazer um handoff. Não use para explicar, revisar ou editar esta skill.
compatibility: Requer Claude Code 2.1.284 ou mais novo, na CLI ou no aplicativo, com o plugin hopper-documentation-anth e Python 3.9 ou mais novo.
---

# hopper-documentation-anth

## O que a skill produz

A skill documenta a conversa em 7 documentos Markdown, dentro de `docs-by-hopper-documentation/`, na pasta em que a conversa foi aberta. Existe 1 pasta dessas por pasta de projeto, e 1 subpasta por conversa.

```text
docs-by-hopper-documentation/
├── 1-indice.md                 índice e ordem de leitura
├── 4-decisoes.md               decisões de todas as conversas da pasta
├── 5-funcoes.md                funções implementadas (entregas concluídas)
├── 6-pendencias.md             pendências abertas e encerradas
└── conversas/
    └── 2026-11-01-e4bad083/    1 pasta por conversa: data da 1ª mensagem e código
        ├── 2-conversa-integral.md
        ├── 3-conversa-simplificada.md
        └── 7-handoff.md
```

- **Documento 2, conversa integral.** Cópia fiel das mensagens do usuário e do Claude, sem resultados de ferramentas, sem raciocínio interno e com senhas e tokens trocados por `[oculto]`. Cada uso de ferramenta vira 1 linha. Só recebe acréscimos. Cada mensagem tem um identificador como `M42-e4bad083`.
- **Documento 3, conversa simplificada.** O mesmo conteúdo, reescrito em frases curtas, 1 bloco por rodada, com a mensagem de origem no fim de cada parágrafo.
- **Documentos 4, 5 e 6.** Itens numerados por conversa (`D1-e4bad083`, `F1-e4bad083`, `PD1-e4bad083`), cada um com origem, situação e o intervalo da rodada que o criou.
- **Documento 7, handoff.** Reescrito inteiro a cada rodada, com 9 seções: objetivo, pautas e estado atual, próximo passo, decisões e autorizações vigentes, restrições vigentes, descobertas e tentativas descartadas, pendências e compromissos, lacunas e como retomar.
- **Documento 1, índice.** A ordem de leitura e a tabela das conversas da pasta.

O programa do plugin grava o documento 2 sem IA. O Claude Sonnet 5.5, chamado sem janela (`claude -p`) e sem ferramentas, escreve o conteúdo dos documentos 3 a 7 seguindo `regras-de-escrita.md` e `modelos.md` desta pasta. O programa valida a resposta, numera os itens e grava os arquivos.

A mesma rodada roda sozinha antes de toda compactação, por um gatilho do plugin. A primeira rodada em uma pasta que tem handoffs do formato antigo (`index.md` e `handoff-*.md` na raiz) migra esses arquivos e os apaga.

## Como a skill roda

Quando o usuário pedir para documentar ou registrar a conversa, salvar o progresso ou fazer um handoff:

1. Rode o programa em segundo plano, com a ferramenta Bash, sem esperar:

   ```sh
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hopper_documentation_anth.py" rodada --sessao "${CLAUDE_SESSION_ID}"
   ```

2. Quando o programa terminar, informe ao usuário a última linha da saída dele, sem mudar o sentido. Ela diz "Documentação concluída: …", "Documentação: nada novo …" ou "Documentação falhou: …".
3. Não escreva nem edite você mesmo nenhum arquivo de `docs-by-hopper-documentation/`. Não tente outro modelo nem outro caminho se o programa falhar: informe a falha.

Se o programa ainda estiver rodando quando você responder, diga que a documentação começou em segundo plano e informe o resultado quando ele chegar.

Não rode a skill quando o pedido for explicar, revisar ou editar a skill, ou quando a pergunta for sobre o que é um handoff.
