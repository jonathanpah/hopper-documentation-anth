# Relatório da tarefa 12

As 7 alterações estão implementadas nos 2 pacotes. Os 56 testes do executor passam em cada pacote, incluindo 7 testes novos. O aceite passa em 40 dos 42 testes de cada pacote. T12 conflita com a nova tentativa de C04 exigida pela tarefa 12. T38 permanece limitado pelo isolamento, que bloqueia `ps`.

Execução local em 2026-11-02, sem rede, na branch `versao-2`, com Python 3.14.8. A referência anterior às alterações foi `HEAD` em `62d2746903dc5db330458aaae30e6a5851013c94`.

## Alterações por item

1. Em [`esquema_de_migracao()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:175), `handoffs_antigos[].data` recebeu o padrão exato `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`. A descrição informa que é a data do último handoff antigo da conversa, sem hora. A descrição segue o idioma do pacote.
2. As seções curtas “Migração” e “Migration” foram acrescentadas a [`modelos.md`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/skills/hopper-documentation-anth/modelos.md:54) e [`templates.md`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/skills/hopper-documentation-anth/templates.md:54). Elas explicam `handoffs_antigos`, `conversa`, `data`, `resumo`, `handoff` e `sem_conteudo`. Incluem o exemplo `2026-09-30`, o limite de 80 caracteres e as 9 chaves do handoff. Também esclarecem `conversa` nos itens novos da migração.
3. Em [`validar_resposta()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:958), datas textuais inválidas geram `RespostaCorrigivel`, com identificador da conversa e valor recebido. A conferência antecede a validação geral, para o novo `pattern` não transformar esse erro em falha sem nova tentativa. Datas impossíveis no calendário também continuam rejeitadas. Campos ausentes e tipos incorretos seguem para a validação do esquema.
4. [`conferir_modelos()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1065) agora identifica a reprovação de C04 pela exceção `ModeloInvalido`, que preserva os modelos recebidos. [`chamar_redator_validado()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1130) registra a resposta descartada como `em andamento`, com motivo e modelos, e repete a chamada com a mesma entrada. A 2ª reprovação falha. Erros de data, de referências e de modelo compartilham o mesmo limite de 2 chamadas. C04 continua exigindo pelo menos 90% dos tokens de saída do Sonnet. O tempo limite não recebeu nova tentativa.
5. No ramo `migrar` de [`main()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1689), qualquer exceção produz uma tentativa de registro com etapa `migracao`, resultado `falhou`, motivo original e pasta do projeto. Se o registro falhar, o comando ainda imprime a linha final e retorna 1. O erro do registro não substitui o erro original.
6. Foram acrescentados os 7 testes descritos abaixo. O arquivo de testes foi copiado do pacote português para o inglês. O teste anterior da tarefa 10 sobre modelo e tempo foi atualizado para esperar 2 chamadas na reprovação de modelo e 1 no tempo limite.
7. O programa inglês foi gerado pelo `sed` exigido. O `diff` mostra somente a linha `LANGUAGE`. Os arquivos de testes dos 2 pacotes são idênticos.

## Testes novos

A classe [`RegressoesDaTarefa12`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py:877) existe nos 2 pacotes. Os testes usam as respostas de migração e os mecanismos de simulação existentes. Nenhum redator real foi executado.

| Teste | Comportamento verificado |
| --- | --- |
| `test_data_com_hora_repete_e_conclui_migracao` | A 1ª resposta traz data com hora. A 2ª corrige e conclui. Confere o esquema, a instrução de correção, os modelos registrados e o handoff gravado. |
| `test_data_com_hora_duas_vezes_falha_registra_e_preserva_antigos` | As 2 respostas trazem data com hora. O comando falha, registra as respostas descartadas e a falha final, sem alterar ou apagar os arquivos antigos. |
| `test_datas_invalidas_sao_corrigiveis_com_conversa_e_valor` | Data com hora, data sem zero, dia impossível e string vazia geram erro corrigível com conversa e valor recebido. |
| `test_modelo_reprovado_repete_mesma_entrada_e_conclui_migracao` | C04 reprova a 1ª resposta e aprova a 2ª. A chamada repete os mesmos argumentos e a mesma entrada, registra os modelos e conclui a migração. |
| `test_modelo_reprovado_duas_vezes_falha_em_duas_chamadas` | As 2 respostas reprovam C04. O comando falha após 2 chamadas, preserva os arquivos antigos e registra modelos e falha final. |
| `test_data_e_modelo_compartilham_limite_de_duas_chamadas` | Nas 2 ordens possíveis, os erros de data e modelo consomem no máximo 2 chamadas. Os arquivos antigos ficam preservados. |
| `test_migrar_preserva_linha_final_se_registro_falhar` | Falha prevista e erro de permissão mantêm a linha final original mesmo quando a tentativa de registro também falha. |

Antes da correção, os 7 testes foram executados no pacote português e reproduziram as falhas.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s hopper-documentation-anth-pt-br/tests -p 'test_hopper_documentation_anth.py' -k RegressoesDaTarefa12
```

```text
Ran 7 tests in 0.030s

FAILED (failures=5, errors=7)
```

As contagens de falhas e erros incluem subcasos. Depois da correção, o mesmo comando foi executado para cada pacote. A saída foi igual nos 2 idiomas.

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.066s

OK
```

## Os 3 comandos da tarefa 01

Os comandos rodaram com `PYTHONDONTWRITEBYTECODE=1`, para não criar bytecode nos diretórios protegidos. Os comandos 1 e 2 usaram Bash com `pipefail`. Foi acrescentado `tee` antes de `tail` para capturar a saída completa em pasta temporária, sem mudar os testes. Os comandos abaixo preservam a forma solicitada, sem essa captura auxiliar. A ordem das saídas é português e inglês.

### Comando 1

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

```text
Ran 42 tests in 28.583s

FAILED (failures=2)
Ran 42 tests in 28.755s

FAILED (failures=2)
```

Código do comando `0`, devido ao `cd` final. As 2 suítes reprovaram e não foram tratadas como aprovadas.

### Comando 2

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

```text
Ran 56 tests in 0.697s

OK
Ran 56 tests in 0.730s

OK
```

Código do comando `0`.

### Comando 3

```sh
diff hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

```text
31c31
< LANGUAGE = "pt-br"
---
> LANGUAGE = "en"
```

Código do comando `1`, esperado pela diferença permitida em `LANGUAGE`.

## Reprovações do aceite

### T12 e a nova tentativa de C04

Nos 2 pacotes, [`test_redator.py`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/aceite/testes/test_redator.py:119) exige exatamente 2 chamadas acumuladas após uma rodada inválida e outra válida.

```text
FAIL: test_R12_chama_o_redator_com_as_opcoes_de_C03_e_descarta_resposta_invalida
AssertionError: 3 != 2
```

Com a alteração obrigatória do item 4, a 1ª rodada com modelo incorreto consome 2 chamadas. A rodada seguinte conclui com mais 1 chamada. O total de 3 entre as 2 rodadas cumpre o limite de 2 por rodada, mas reprova a contagem antiga do teste congelado.

A tarefa 12 exige a nova tentativa em `chamar_redator_validado`. Ela também proíbe alterar `aceite/`. Mantive o comportamento solicitado e preservei o teste. Não existe aprovação integral do aceite nesta entrega.

### T38 e o isolamento

Nos 2 pacotes, [`test_repositorio.py`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/aceite/testes/test_repositorio.py:160) reprova no subcaso `CLAUDE_PID antes do PATH`.

```text
FAIL: test_R38_encontra_o_executavel_do_claude_code
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

Uma sonda local confirmou que o isolamento impede consultar o executável do processo.

```text
PermissionError(1, 'Operation not permitted')
```

Para separar os efeitos desta tarefa, executei somente T12 e T38 com cópias temporárias dos programas originais de `HEAD`. Os arquivos de trabalho e os testes congelados ficaram intactos. O resultado foi o mesmo nos 2 pacotes.

```text
T12 ... ok
T38 ... FAIL
Ran 2 tests
FAILED (failures=1)
```

Essa comparação confirma que a reprovação de T12 decorre do novo comportamento solicitado. A reprovação de T38 já existia antes da alteração.

## Preservação e verificações finais

`git diff --check` passou. A sintaxe dos 4 arquivos Python foi validada sem gerar bytecode. Os testes dos 2 pacotes são idênticos. O programa inglês foi gerado com o comando exigido.

```sh
sed 's/^LANGUAGE = "pt-br"$/LANGUAGE = "en"/' hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py > hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

A comparação de SHA-256 e permissões preservou os 500 arquivos preexistentes registrados em `SPEC.md`, `aceite/`, `.github/`, `.claude/`, `execucao/` e nos `evals/` dos pacotes. O único acréscimo autorizado nesses destinos é este relatório. A tarefa 12, que já estava sem rastreamento no início, foi preservada.

As alterações se limitam aos programas, aos testes e aos modelos dos 2 idiomas, além deste relatório. Não foram feitos commit, push, merge, instalação, acesso à VPS, chamadas de rede ou execução real de `claude -p`. Os temporários desta execução foram removidos após registrar os resultados.

## O que ficou sem fazer

1. A aprovação de T12 permanece pendente pelo conflito entre sua contagem congelada e o item 4 da tarefa 12. Recomendo que o verificador resolva o critério antes de exigir aprovação integral. Depende de decisão do responsável pelos critérios, fora do escopo autorizado ao Codex.
2. A aprovação de T38 permanece pendente no ambiente isolado. Recomendo repetir o aceite em um ambiente que permita consultar `ps`. Depende da execução pelo verificador nesse ambiente.

A migração real e a instalação não foram executadas, conforme as restrições das tarefas 01 e 05. A conclusão verificada se limita ao código local e aos testes com redator simulado.

## Tarefa 13

A tarefa 13 está concluída no isolamento. A reprovação de C04 encerra a chamada sem nova tentativa. Os 55 testes do executor passam em cada pacote. O aceite passa em 41 de 42 testes por pacote, incluindo T12. Só T38 reprova, porque o isolamento impede executar `ps`.

Esta seção atualiza o resultado da tarefa 12 e encerra a pendência de T12 registrada acima. O histórico anterior do relatório foi preservado. Execução local em 2026-11-02, na branch `versao-2`, com Python 3.14.8 e `HEAD` em `62d2746903dc5db330458aaae30e6a5851013c94`.

### Alterações e preservação da tarefa 12

1. Em [`conferir_modelos()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1059), C04 voltou a gerar `Falha`. Em [`chamar_redator_validado()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1124), a chamada voltou a ficar fora do tratamento de erros corrigíveis. As 2 funções são idênticas às do commit `62d2746`. A classe `ModeloInvalido` foi removida, sem usos restantes nos programas.
2. O teste `test_modelo_reprovado_repete_mesma_entrada_e_conclui_migracao` foi removido dos 2 pacotes. O teste anterior `test_modelo_e_tempo_nao_acionam_nova_tentativa` foi restaurado. Os outros 2 testes afetados passaram a exigir falha após 1 chamada quando o modelo reprova. Quando uma data inválida precede essa falha, são 2 chamadas no total. Eles continuam conferindo a preservação dos arquivos antigos; o teste de modelo também confere o registro final de falha da migração.
3. Os itens 1, 2, 3, 5 e 6 restantes da tarefa 12 foram mantidos. Permanecem o formato e a descrição da data no esquema, as seções de migração em `modelos.md` e `templates.md`, a classificação de data inválida como `RespostaCorrigivel`, a nova tentativa para corrigir essa data e o registro de falha de `migrar`. Os testes correspondentes continuam passando. As outras funções e classes ficaram idênticas às encontradas no início desta tarefa.
4. O programa inglês foi gerado com o `sed` exigido. O arquivo de testes foi copiado do português para o inglês. Os testes dos 2 pacotes são idênticos.

```sh
sed 's/^LANGUAGE = "pt-br"$/LANGUAGE = "en"/' hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py > hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

### Verificação com os 3 comandos da tarefa 01

Os comandos rodaram com `PYTHONDONTWRITEBYTECODE=1`, para preservar os diretórios protegidos. Os comandos 1 e 2 usaram Bash com `pipefail` e `tee` antes de `tail` para capturar a saída completa em pasta temporária. Abaixo constam os comandos solicitados, sem essa captura auxiliar. A ordem das saídas é português e inglês.

Comando 1.

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

```text
Ran 42 tests in 29.320s

FAILED (failures=1)
Ran 42 tests in 29.200s

FAILED (failures=1)
```

O comando termina com código `0` devido ao `cd` final. As 2 suítes reprovam exclusivamente em T38. Não foram tratadas como integralmente aprovadas.

Comando 2.

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

```text
Ran 55 tests in 0.759s

OK
Ran 55 tests in 0.731s

OK
```

Código do comando `0`.

Comando 3.

```sh
diff hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

```text
31c31
< LANGUAGE = "pt-br"
---
> LANGUAGE = "en"
```

Código do comando `1`, esperado pela única diferença permitida em `LANGUAGE`.

### T12 corrigido e única limitação em T38

Antes da alteração, executei T12 isoladamente no pacote português. O teste reproduziu a falha da tarefa 12.

```text
AssertionError: 3 != 2
Ran 1 test in 0.529s

FAILED (failures=1)
```

Após a alteração, as saídas completas do aceite dos 2 pacotes mostram somente esta reprovação. T12 passou em ambos.

```text
FAIL: test_R38_encontra_o_executavel_do_claude_code
(candidato='CLAUDE_PID antes do PATH')
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

Uma sonda local de `ps` confirmou a restrição do isolamento nesta execução.

```text
PermissionError(1, 'Operation not permitted')
```

### Conferência final e limites

A comparação de SHA-256 e permissões dos 547 arquivos preexistentes confirmou que só mudaram os programas e os testes dos 2 idiomas e este relatório. Os outros 542 arquivos foram preservados, incluindo `SPEC.md`, `aceite/`, `.github/`, `.claude/`, os `evals/`, os modelos da tarefa 12 e os demais arquivos de `execucao/`. O conteúdo anterior deste relatório permaneceu como prefixo exato; só esta seção foi acrescentada.

`git diff --check` passou. A sintaxe dos 4 arquivos Python foi validada sem gerar bytecode. Não foram feitos comandos `git` que gravem, acesso à rede, acesso à VPS, instalação ou execução de redator real. A verificação usou os redatores simulados dos testes.

### Pendência

1. T38 continua pendente no isolamento. Recomendo que o verificador repita o aceite em um ambiente que permita consultar `ps`. Isso depende da execução pelo verificador, fora do escopo desta tarefa. Não ficou correção de código pendente no escopo da tarefa 13.
