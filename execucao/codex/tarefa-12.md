# Tarefa 12 para o Codex: migração real (U9)

Mesmas regras da tarefa 05 (isolamento sem rede; não toque em `aceite/`, `SPEC.md`, `.github/` nem nos `evals/`).

## Evidência

Migração real com a versão instalada (`migrar --pasta`), 2026-11-02:

1. 5 de 6 tentativas falharam com "resposta do redator fora do esquema (data)". Respostas capturadas: `handoffs_antigos[].data` = `2026-09-30 12:20:55` e `2026-09-30 17:34:54`. O Anexo D exige `AAAA-MM-DD`, mas `esquema_de_migracao()` declara `data` só como `{"type": "string"}`, e `modelos.md` e `templates.md` não descrevem os campos da migração. O erro de data não é `RespostaCorrigivel`, então não existe nova tentativa.
2. 1 tentativa no MacBook falhou com "resposta de outro modelo que não o claude-sonnet-5-5". Nas capturas do MacBook, o `modelUsage` traz `claude-haiku-5-5` com cerca de 5.850 tokens de entrada e de 21 a 347 de saída (até 7,8%), ao lado do Sonnet; na VPS, só o Sonnet. A falha da regra de C04 também não tem nova tentativa.
3. Quando o comando `migrar` falha, nenhuma linha `migracao` `falhou` vai para o registro de rodadas.

## O que fazer (decisão do verificador)

1. Em `esquema_de_migracao()`, o campo `data` passa a ter `"pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"` e uma `description` curta (data do último handoff antigo da conversa, só a data, sem hora).
2. Em `modelos.md` e `templates.md`, acrescente uma seção curta "Migração" ("Migration") com os campos `handoffs_antigos` (`conversa`, `data` em `AAAA-MM-DD` sem hora, por exemplo `2026-09-30`, `resumo` até 80 caracteres, `handoff` com as 9 chaves) e `sem_conteudo`. Siga as regras de escrita do próprio arquivo.
3. Data fora do formato em `validar_resposta` passa a ser `RespostaCorrigivel`, com o problema descrito (identificador da conversa e valor recebido), para usar a nova tentativa que já existe.
4. Em `chamar_redator_validado`, a falha da regra de modelo (C04) na 1ª chamada ganha 1 nova chamada com a mesma entrada; a resposta descartada entra no registro de rodadas como as outras descartadas (resultado `em andamento`, motivo e modelos). Na 2ª falha, a rodada falha como hoje. O limite total continua em 2 chamadas por rodada ou migração.
5. No ramo `migrar` de `main()`, registre a falha (`migracao`, `falhou`, motivo, pasta do projeto), sem deixar o registro impedir a linha final, como na tarefa 11.
6. Testes no `tests/test_hopper_documentation_anth.py` de cada pacote, com o redator falso que os testes já usam: data com hora na 1ª resposta e certa na 2ª conclui a migração; data com hora nas 2 respostas falha sem apagar os arquivos antigos; regra de modelo reprovada na 1ª e aprovada na 2ª conclui; falha do `migrar` gera a linha no registro.
7. Gere o programa en pelo `sed` de sempre e confira com `diff`.

Verificação com os 3 comandos da tarefa 01. Relatório em `execucao/codex/tarefa-12-relatorio.md`.
