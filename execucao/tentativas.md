# Tentativas e contadores (C20)

## Contadores

| Contador | Limite | Usado |
| --- | --- | --- |
| Chamadas reais ao redator, U1 a U8 | 40 | 2 (U1, item 6) |
| Rodadas disparadas pelas compactações da sessão do executor (fora do limite) | sem limite | 0 |
| Outras chamadas reais fora do redator (retomada, sonda) | sem limite | 1 retomada (U1, item 7); sessões de sonda com Haiku 5.5 |
| Execuções completas das avaliações de acionamento | 3 | 0 |
| Passadas de revisão por unidade | 2 | U1: 0 |

## Tentativas por falha

| Unidade | Verificador | Tentativa | Data (UTC) | O que mudou | Resultado |
| --- | --- | --- | --- | --- | --- |
| U1 | Item 4, provas das regras | 1 | 2026-11-02 02:48 | Arquivo de regras criado na cópia de trabalho; sessão ainda com as configurações da pasta de origem | reprovado (V-U1-04) |
| U1 | Item 4, provas das regras | 2 | 2026-11-02 02:42 | Sessão movida para a cópia de trabalho com `change_directory` | em andamento |
