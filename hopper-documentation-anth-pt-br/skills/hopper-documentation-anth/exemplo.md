# Exemplo de handoff

Handoff completo de uma conversa fictícia. Ele mostra o nível de detalhe esperado: frases completas, caminhos e identificadores exatos, falas do usuário entre aspas e nada que os arquivos ou o git já mostrem. O programa escreve o cabeçalho e os títulos; o redator escreve o resumo e o texto de cada seção.

```markdown
# Handoff: Correção do cálculo de frete no checkout

- **Data:** 2026-03-14 18:42:07 +00:00
- **Conversa:** 3f9c2a71-5b8e-4d0a-9c61-2e7f4b1a8d05
- **Diretório de trabalho:** /home/ana/projetos/loja
- **Handoff anterior desta conversa:** [handoff-20260314-151203-3f9c2a71.md](handoff-20260314-151203-3f9c2a71.md)
- **Acionamento:** a pedido
- **Redator:** claude-sonnet-5-5 com esforço medium
- **Última mensagem registrada:** 8d1e0f42-77a3-4c2b-9e15-0b6a2f9c3d81

## Objetivo

Corrigir o frete cobrado em pedidos acima de R$ 300,00, que deveria ser zero. O trabalho termina quando os testes de `tests/test_frete.py` passarem e a correção estiver num commit na branch `corrige-frete`.

## Pautas e estado atual

- **P1 — Correção da regra de frete grátis: concluída.** A regra foi corrigida em `/home/ana/projetos/loja/frete/calculo.py`, função `calcular_frete`. Os 14 testes de `tests/test_frete.py` passaram (saída do `pytest` na conversa). Commit `a41e9d2` na branch `corrige-frete`.
- **P2 — Arredondamento do frete: aguardando.** A usuária vai decidir entre arredondar para cima ou para o centavo mais próximo.

## Próximo passo

Aguardando decisão do usuário sobre o arredondamento (P2). A usuária disse que decide amanhã.

## Decisões e autorizações

- Decisão: o limite do frete grátis vale para o total depois dos descontos. Motivo: é a regra publicada na página de ajuda da loja.
- Autorização: "Pode corrigir e fazer commit na branch corrige-frete". Alcance: só a branch `corrige-frete`. Já usada no commit `a41e9d2`.

## Restrições vigentes

- "Não faça merge na main nem publique nada" — da usuária, no início da conversa.
- Mensagens de commit em português — preferência da usuária.

## Descobertas e tentativas descartadas

- O erro vinha da comparação com o total antes dos descontos.
- Descartado: mover a regra para `pedido/total.py`. A usuária recusou porque outros módulos importam essa função.

## Pendências e compromissos

- **PD1 — Atualizar `docs/regras-de-frete.md`:** compromisso da IA depois da decisão de P2. Encerra quando o arquivo refletir a regra escolhida. Situação: aguardando P2.

## Lacunas

- Os testes de integração em `tests/integracao/` não foram rodados; a conversa não mostra o motivo.

## Como retomar

1. Leia este handoff e o `index.md` desta pasta.
2. Confira o estado real antes de agir: `git log` da branch `corrige-frete` deve mostrar o commit `a41e9d2`, e `git status` deve estar limpo.
3. Não refaça a correção nem o commit: já estão concluídos.
4. Pergunte à usuária a decisão sobre o arredondamento, se ela ainda não tiver respondido.
```
