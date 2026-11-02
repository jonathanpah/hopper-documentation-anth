# Tentativas e contadores (C20)

## Contadores

| Contador | Limite | Usado |
| --- | --- | --- |
| Chamadas reais ao redator, U1 a U8 | 40 | 2 (U1, item 6) |
| Rodadas disparadas pelas compactações da sessão do executor (fora do limite) | sem limite | 0 |
| Outras chamadas reais fora do redator (retomada, sonda) | sem limite | 1 retomada (U1, item 7); sessões de sonda com Haiku 5.5 |
| Execuções completas das avaliações de acionamento | 3 | 0 |
| Passadas de revisão por unidade | 2 | U1: 1 |

## Tentativas por falha

| Unidade | Verificador | Tentativa | Data (UTC) | O que mudou | Resultado |
| --- | --- | --- | --- | --- | --- |
| U1 | Item 4, provas das regras | 1 | 2026-11-02 02:48 | Arquivo de regras criado na cópia de trabalho; sessão ainda com as configurações da pasta de origem | reprovado (V-U1-04) |
| U1 | Item 4, provas das regras | 2 | 2026-11-02 02:42 | Sessão movida para a cópia de trabalho com `change_directory` | `deny` aprovado em parte; `ask` reprovado (V-U1-04) |
| U1 | Item 4, provas das regras `deny` | 3 | 2026-11-02 03:50 | 4 provas a mais, pela revisão U1-passada-1 | aprovado |
| U1 | Item 5, processo separado (C08) | 1 | 2026-11-02 03:30 | Sonda v2: fork duplo com setsid no lugar de Popen(start_new_session=True) | aprovado (V-U1-05, passagem 3) |
| U1 | Item 5, valor de CLAUDE_AUTOCOMPACT_PCT_OVERRIDE | 1 | 2026-11-02 03:52 | 85 no lugar de 70, com contagem de mensagens; valor derivado: 90 | aprovado para A3 (V-U1-05, calibração) |
