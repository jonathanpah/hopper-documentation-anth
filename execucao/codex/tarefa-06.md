# Tarefa 06 para o Codex: compatibilizar a conferência de referências com o caso de borda de R14

Mesmas regras da tarefa 05. Os critérios estão congelados: não toque em `aceite/`.

T14 (`test_R14_numera_com_o_proximo_numero_livre`, congelado) reprova depois da tarefa 05. O teste apaga D1 à mão e a resposta seguinte do redator cita D1 no handoff. A seção 6 da spec, caso de borda de R14, diz: "Um item foi apagado à mão de um documento. O programa não detecta itens apagados à mão. O próximo número é o maior número existente mais 1." Na vida real, o handoff anterior também cita o item apagado, e o redator tende a repeti-lo; rejeitar a resposta faria toda rodada falhar depois de uma exclusão manual.

## Decisão do verificador

Na conferência de referências da tarefa 05:

- **Mensagens** continuam exigidas como estão: a mensagem citada existe no documento 2 da pasta, até o fim do trecho novo. É isso que corrige o defeito real de A3 (M19 futura).
- **Itens:** além dos existentes e das referências `N<n>` da resposta, aceite um identificador `D|F|PD<n>-<código>` que não existe mais na pasta quando `n` é menor ou igual ao maior número já usado desse tipo e desse código (item apagado à mão). Rejeite só os itens "do futuro" (número maior que o maior existente) e os de código inexistente na pasta.
- Ajuste os testes do executor da tarefa 05 a essa regra e acrescente 1 teste para o item apagado à mão.

## Verificação

Os 3 comandos da tarefa 01, com 42 de 42 no aceite (T38 pode reprovar no seu isolamento por causa do `ps`; diga se for só ele). Relatório em `execucao/codex/tarefa-06-relatorio.md`.
