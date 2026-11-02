# Relatório da tarefa 14

As alterações pedidas estão implementadas nos 2 pacotes. Os 59 testes do executor passam em cada pacote, incluindo os 4 novos. O aceite aprova 41 de 42 testes por pacote. A aprovação integral continua pendente por T38, que também reprova com o programa anterior à alteração no ambiente isolado.

Execução local em 2026-11-02, na branch `versao-2`, com Python 3.14.8. O commit inicial é `9642eced003a8774a6a04a03673490ef9537f05a`. Foram respeitadas as restrições das tarefas 01, 05 e 12.

## Alterações

1. Em [`validar_resposta()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:954), a migração confere o destino de cada nome de `arquivos_validos` antes do diário e da gravação. Aceita nomes nas origens de `itens_novos` ou `mudancas`, em `sem_conteudo` ou no texto de qualquer uma das 9 chaves dos handoffs antigos. Os nomes ausentes são ordenados e acrescentados aos problemas de `RespostaCorrigivel`. A mensagem em português é `arquivos sem destino: <lista>`, com tradução correspondente em inglês. A nova tentativa existente recebe esse motivo e mantém o limite total de 2 chamadas.
2. A seção de migração de [`modelos.md`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/skills/hopper-documentation-anth/modelos.md:60) e de [`templates.md`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/skills/hopper-documentation-anth/templates.md:60) ganhou 1 frase em cada idioma. Ela exige destino para todo arquivo antigo e orienta incluir em `sem_conteudo` o `index.md` antigo que só lista handoffs.
3. A classe `RegressoesDaTarefa14` foi acrescentada aos [testes em português](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py:996) e copiada para os [testes em inglês](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/tests/test_hopper_documentation_anth.py:996). As chamadas ao redator foram simuladas pelo mecanismo já usado na tarefa 12. Nenhum redator real foi executado.
4. O [programa inglês](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/scripts/hopper_documentation_anth.py:954) foi gerado com o `sed` exigido. O `diff` mostra somente `LANGUAGE`.

```sh
sed 's/^LANGUAGE = "pt-br"$/LANGUAGE = "en"/' hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py > hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

`verificacao_interna()` permanece com o mesmo código e continua sendo executada depois da gravação. Também permaneceram iguais `chamar_redator_validado()`, `migrar()`, `esquema_de_migracao()` e `main()`.

## Testes novos

| Teste | Comportamento verificado |
| --- | --- |
| `test_indice_sem_destino_repete_e_conclui_sem_gravar_a_primeira_resposta` | A 1ª resposta omite o destino do `index.md`. A 2ª inclui o arquivo em `sem_conteudo`. Confere ausência de gravação e diário antes das chamadas, instrução de correção, registro das chamadas, documentos finais, verificação interna e exclusão dos 3 arquivos antigos. |
| `test_indice_sem_destino_duas_vezes_falha_sem_gravar_nem_apagar` | As 2 respostas omitem o destino. O comando falha após 2 chamadas, registra os descartes e a falha final, preserva todos os arquivos antigos e não grava documentos 4 a 7 nem diário. |
| `test_indice_aceito_em_origem_sem_conteudo_ou_qualquer_campo_do_handoff` | Aceita o destino nas origens de itens novos e mudanças, em `sem_conteudo` e em cada uma das 9 chaves do handoff. |
| `test_arquivos_sem_destino_sao_corrigiveis_e_listados_em_ordem` | Lista 2 arquivos ausentes em ordem e gera `RespostaCorrigivel`. Citar nomes apenas no texto de um item não atende à condição de destino. |

Antes da correção, os testes foram executados com o programa original em português. Os 2 cenários de migração falharam porque o programa parou depois de 1 chamada. A validação direta também falhou porque não gerou `RespostaCorrigivel`. O teste dos destinos permitidos já passava.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s hopper-documentation-anth-pt-br/tests -p 'test_hopper_documentation_anth.py' -k RegressoesDaTarefa14
```

```text
Ran 4 tests in 0.029s

FAILED (failures=3)
```

Depois da correção, o mesmo comando foi executado para cada pacote. A saída foi igual nos 2 idiomas.

```text
Ran 4 tests in 0.026s

OK
```

## Os 3 comandos da tarefa 01

Os comandos rodaram com `PYTHONDONTWRITEBYTECODE=1`, para evitar bytecode nos diretórios protegidos. Nos comandos 1 e 2, foram usados Bash com `pipefail` e `tee` antes de `tail` para capturar a saída completa em pasta temporária. O código de cada suíte foi capturado por `PIPESTATUS[0]`. Abaixo constam os comandos solicitados, sem essa captura auxiliar. A ordem das saídas é português e inglês.

### Comando 1

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

```text
Ran 42 tests in 30.768s

FAILED (failures=1)
Ran 42 tests in 33.118s

FAILED (failures=1)
```

Cada suíte retornou código `1`. O comando completo termina com código `0` devido ao `cd` final. As suítes não foram tratadas como integralmente aprovadas.

### Comando 2

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

```text
Ran 59 tests in 0.849s

OK
Ran 59 tests in 0.827s

OK
```

Cada suíte retornou código `0`.

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

Código `1`, esperado pela diferença permitida em `LANGUAGE`.

## Limitação do aceite

As saídas completas dos 2 pacotes mostram exclusivamente a reprovação de [T38](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/aceite/testes/test_repositorio.py:160), no subcaso `CLAUDE_PID antes do PATH`.

```text
FAIL: test_R38_encontra_o_executavel_do_claude_code
(candidato='CLAUDE_PID antes do PATH')
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

Uma sonda local confirmou que o isolamento impede executar `ps`.

```text
PermissionError(1, 'Operation not permitted')
```

T38 também foi executado isoladamente contra uma cópia temporária do programa português anterior à alteração. O teste congelado foi importado sem edição, apontando `PROGRAMA` para essa cópia. A reprovação foi a mesma.

```text
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
Ran 1 test in 0.365s

FAILED (failures=1)
```

Essa comparação confirma que a falha já ocorria antes desta tarefa. Os testes e os critérios de aceite foram preservados.

## Conferência final e limites

`git diff --check` passou. A sintaxe dos 4 arquivos Python foi validada sem gerar bytecode. Os arquivos de testes dos 2 pacotes são idênticos. A comparação do código das funções confirmou a preservação da verificação interna e do fluxo existente de migração e nova tentativa.

A comparação de SHA-256 e permissões dos 549 arquivos preexistentes confirmou mudanças somente nos programas, nos testes e nos modelos dos 2 idiomas. Os outros 543 arquivos foram preservados. Isso inclui `SPEC.md`, `aceite/`, `.github/`, `.claude/`, os `evals/` e os arquivos preexistentes de `execucao/`. O único arquivo acrescentado é este relatório. A tarefa 14, que já estava sem rastreamento no início, foi preservada.

Não foram feitos comandos `git` que gravem, chamadas de rede, acesso à VPS, instalação ou execução real de `claude -p`. Os testes usaram pastas temporárias isoladas. A migração real citada na tarefa e seu diário não foram alterados. Os temporários desta execução foram removidos depois de registrar os resultados.

## Pendência

1. A aprovação integral do aceite permanece pendente por T38. Recomendo que o verificador execute o aceite em um ambiente que permita consultar `ps`. Isso depende da execução pelo verificador fora deste isolamento. Não ficou correção de código pendente no escopo da tarefa 14.
