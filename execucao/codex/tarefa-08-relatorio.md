# Relatório da tarefa 08

A correção foi implementada nos 2 pacotes. Os 48 testes do executor passaram em cada idioma, incluindo 5 testes novos. O aceite terminou com 41 aprovações em 42 testes por pacote. Somente T38 falhou, porque o sandbox bloqueia a consulta de processo por `ps`. Portanto, a aprovação integral exigida pela tarefa permanece sem comprovação neste ambiente.

## Ambiente e alcance

- Execução local em 2026-11-02, Darwin arm64, Python 3.14.8.
- Pasta `/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth`, branch `versao-2`, HEAD inicial `a48d2d60734867ec305e30466bd587f81870388c`. A árvore estava sem alterações.
- Código e testes editados somente no pacote em português. O programa em inglês foi regenerado com o `sed` da tarefa 01. O arquivo de testes foi copiado para o pacote em inglês.
- `modelos.md` e `templates.md` receberam a mesma regra de origem, com tradução fiel. Os novos textos fixos do programa também existem nos 2 idiomas.
- Sem rede, VPS, instalação, chamada real a `claude -p` ou comando Git de gravação. Os testes usaram arquivos temporários, mocks e o redator simulado local.
- As suítes rodaram com `PYTHONDONTWRITEBYTECODE=1`. Capturei a saída integral antes de aplicar `tail -3`, usando `tee`, e preservei o código do unittest pelo `PIPESTATUS`. Os pacotes foram verificados em paralelo, com pastas temporárias independentes.

## Alterações por item

O programa principal é [hopper_documentation_anth.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py). A cópia regenerada fica no [programa em inglês](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/scripts/hopper_documentation_anth.py).

| Item | Arquivo e função | Alteração |
| --- | --- | --- |
| 1. Falhas corrigíveis | Programa, `RespostaCorrigivel`, `ReferenciasInexistentes` e `validar_resposta` | Reúne referências inexistentes, origens inválidas, situações não permitidas e ausência da linha de assunto. Lista todos os problemas encontrados, sem parar na primeira falha corrigível. |
| 1. Limites da nova tentativa | Programa, `validar_resposta` e `chamar_redator_validado` | Erros de esquema continuam encerrando a rodada sem nova tentativa. Isso inclui campos inválidos, referências provisórias duplicadas e os campos estruturais da migração. Falhas de modelo C04 e de tempo continuam sem nova tentativa. |
| 1. Entrada e registro | Programa, `TEXTOS` e `chamar_redator_validado` | Acrescenta à mesma entrada somente 1 linha com a lista de problemas. Quando a origem é inválida, informa o intervalo permitido. Remove quebras de linha dos problemas nessa instrução. Mantém o limite de 2 chamadas e registra os tokens das respostas descartadas e aceitas. |
| 1. Origem | Programa, `validar_resposta` e `origem_valida` | Mantém a exigência de origem no trecho novo ou nos itens permitidos. Uma mensagem anterior continua inválida como origem, mesmo existindo no documento 2. Ela pode continuar citada nos campos textuais, conforme a regra anterior. |
| 2. Regra para o redator | [modelos.md](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/skills/hopper-documentation-anth/modelos.md:44) e [templates.md](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/skills/hopper-documentation-anth/templates.md:44) | Explicita que a origem de um item novo ou de uma mudança deve ser uma mensagem do trecho novo ou um item existente, nunca uma mensagem anterior. Preserva a exceção da migração, que usa o nome do arquivo antigo. |
| 3. Testes | [test_hopper_documentation_anth.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py:720), classe `RegressoesDaTarefa08`, e cópia idêntica em inglês | Acrescenta 5 métodos, descritos abaixo. Ajusta 2 testes da tarefa 05 para a nova instrução e para a mudança dos erros que permitem nova tentativa. |

A conferência de referências da tarefa 06 foi preservada. Itens apagados manualmente, dentro do maior número existente por tipo e código, continuam aceitos nas citações. O alvo inexistente de uma mudança continua sujeito ao registro de mudança não aplicada. A validação e a nova tentativa acontecem antes do diário e da gravação dos documentos 3 a 7.

## Testes novos

| Método em `RegressoesDaTarefa08` | Resultado observado |
| --- | --- |
| `test_origem_anterior_em_item_novo_repete_e_conclui` | Depois de uma rodada concluída até M6, acrescenta M7 e M8. A primeira resposta usa M6 como origem de um item novo. A segunda corrige a origem. A rodada conclui com exatamente 2 chamadas, registra os tokens de ambas e cobre até M8. |
| `test_origem_anterior_em_mudanca_repete_e_conclui` | Repete o cenário para a origem de uma mudança de situação de um item existente. Confere a instrução exata nos 2 idiomas e a situação gravada. |
| `test_origem_anterior_duas_vezes_falha_e_preserva_documentos` | As 2 respostas usam origens anteriores em um item novo e em uma mudança. A rodada falha com exatamente 2 chamadas. Preserva os documentos 3 a 7 da rodada anterior, não deixa diário e registra a falha no índice. |
| `test_situacao_e_assunto_repete_com_lista_de_todos_os_problemas` | Uma resposta combina situações inválidas, assunto ausente, origem fora do trecho e referência inexistente. A nova instrução lista todos os problemas em 1 linha, mesmo quando um valor inválido contém quebra de linha. A segunda resposta válida conclui a rodada. |
| `test_modelo_e_tempo_nao_acionam_nova_tentativa` | Usa a função real de chamada do redator com o processo simulado. Uma resposta de outro modelo e um estouro do tempo fazem somente 1 chamada, cada um com o motivo esperado. |

Os 5 métodos novos foram executados antes da correção do programa. Os 3 cenários de origem e o cenário de problemas combinados falharam. O teste de modelo e tempo já passou, confirmando o comportamento que precisava ser preservado.

```text
Antes da correção
Ran 5 tests in 0.086s

FAILED (failures=4)

Depois da correção
Ran 5 tests in 0.081s

OK
```

## Verificações da tarefa 01

Os comandos abaixo identificam as 3 verificações solicitadas. A execução acrescentou `PYTHONDONTWRITEBYTECODE=1` e captura com `tee`, sem mudar a seleção dos testes. As saídas são as 3 últimas linhas reais de cada execução final. O código do unittest foi conferido separadamente do código do `tail`.

### 1. Aceite nos 2 pacotes

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

Saída de `hopper-documentation-anth-pt-br`, código do unittest 1.

```text
Ran 42 tests in 34.369s

FAILED (failures=1)
```

Saída de `hopper-documentation-anth-en`, código do unittest 1.

```text
Ran 42 tests in 34.334s

FAILED (failures=1)
```

Nos 2 pacotes, a única falha foi `test_R38_encontra_o_executavel_do_claude_code`, no cenário `CLAUDE_PID antes do PATH`. Os outros 41 testes passaram, sem erros nem testes ignorados. T38 esperava `/bin/sleep`, mas recebeu `/usr/bin/true`, candidato encontrado no `PATH`.

```text
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

A consulta direta ao processo confirmou a restrição do ambiente.

```sh
/bin/ps -o comm= -p $$
```

```text
zsh:1: operation not permitted: /bin/ps
```

O programa usa `ps` no macOS para localizar o executável pelo `CLAUDE_PID` e segue para o `PATH` quando a consulta falha. Essa limitação também foi registrada no relatório da tarefa 06. Nenhum teste ou critério de aceite foi alterado para contorná-la.

### 2. Testes do executor nos 2 pacotes

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

Saída de `hopper-documentation-anth-pt-br`, código 0.

```text
Ran 48 tests in 0.782s

OK
```

Saída de `hopper-documentation-anth-en`, código 0.

```text
Ran 48 tests in 0.783s

OK
```

### 3. Diferença entre os programas

```sh
diff hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

Saída, código 1 esperado pela diferença de idioma.

```diff
31c31
< LANGUAGE = "pt-br"
---
> LANGUAGE = "en"
```

Os arquivos de testes são idênticos por `cmp`. `git diff --check` terminou com código 0, sem saída.

## Conferidor do resultado antigo da tarefa 05

Executei também a conferência pedida na tarefa 05. O resultado antigo permaneceu reprovado somente em F8, como previsto.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 aceite/conferir.py execucao/aceite/a3-2/docs-by-hopper-documentation --idioma pt-br --roteiro aceite/roteiro.json
```

Saída, código 1.

```text
F1: aprovada
F2: aprovada
F3: aprovada
F4: aprovada
F5: aprovada
F6: aprovada
F7: aprovada
F8: reprovada
  - 7-handoff.md: mensagem inexistente M19-67ed412f
F9: aprovada
F10: aprovada
verificações rodadas: 10, aprovadas: 9, reprovadas: 1
```

## Integridade da entrega

O inventário inicial registrou 532 arquivos. Comparei seus hashes SHA-256 com o estado final. Os 370 arquivos preexistentes em `SPEC.md`, `aceite/`, `.github/`, `.claude/`, `execucao/` e `.git/` permaneceram iguais.

Esta tarefa alterou somente os programas, os testes e os modelos dos 2 pacotes, totalizando 6 arquivos preexistentes. O único arquivo novo é este relatório. Nenhum arquivo preexistente foi removido. A pasta temporária própria foi removida após incorporar as saídas e conferir a entrega.

## O que ficou sem fazer

1. Comprovar 42 de 42 testes de aceite nos 2 pacotes. T38 depende da consulta de processo bloqueada neste sandbox. Recomendo que o verificador repita a verificação em um ambiente que permita `ps`. Não preciso de informação ou decisão adicional do proprietário. A implementação e os 48 testes do executor por idioma estão entregues, mas o critério de aprovação integral do aceite permanece pendente.
