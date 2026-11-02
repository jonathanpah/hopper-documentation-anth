# Relatório da tarefa 03

Os 2 ajustes foram aplicados sem alterar o programa. Os 31 testes do executor passaram em cada pacote. O aceite teve 41 aprovações em 42 testes por pacote. T04 passou nas 5 repetições pedidas. T38 falhou nas 5 porque este sandbox impede executar `ps`.

A implementação está entregue, mas a exigência de aprovação integral permanece sem comprovação neste ambiente.

## Ambiente e alcance

- Execução local em 2026-11-02, no macOS 27.2, arquitetura arm64, com Python 3.14.8 em `/usr/local/bin/python3`.
- Pasta `/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth`, branch `versao-2`, commit inicial `ac90b2483b91d9c638b4100c3c3a0f441ad255b1`. A árvore estava sem alterações.
- Aplicadas as regras da tarefa 01 e a exceção da tarefa 03. Alterados somente os 2 testes autorizados e criado este relatório.
- Sem alteração ou regeneração dos programas, conforme a proibição específica da tarefa 03. Sem commit, push, merge, rede, acesso à VPS, instalação de plugin ou chamada a `claude -p`.
- Usado `PYTHONDONTWRITEBYTECODE=1` em todas as execuções de testes. As saídas completas foram capturadas em uma pasta temporária própria, removida após a conferência deste relatório.

## Alterações por item

| Item | Arquivo e função | Alteração |
| --- | --- | --- |
| 1, T38 | [test_repositorio.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/aceite/testes/test_repositorio.py), `Localizacao.test_R38_encontra_o_executavel_do_claude_code` | No Linux, o processo usa `sys.executable -c "import time; time.sleep(30)"`. O resultado esperado é `Path(sys.executable).resolve()`. No macOS, preservados o link simbólico para `sleep` e sua execução. |
| 1, candidatos seguintes | Mesmo arquivo e função | O candidato do `PATH` continua apontando para `true`. O candidato local agora é um arquivo executável próprio. Assim, os 3 candidatos resolvem para arquivos diferentes, inclusive no macOS e quando os utilitários compartilham um binário. Acrescentada a comparação entre o esperado pelo PID e o candidato local. Preservadas as verificações de prioridade do `PATH` e da localização local. |
| 2, T04 | [test_copiador.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/aceite/testes/test_copiador.py), `Copiador.test_R04_espera_o_arquivo_de_historico_parar_de_crescer` | A escala passou de `0.2` para `0.5`. A espera de C09 passa a consultar a cada 0,25 s, exigir 0,5 s de estabilidade e ter teto de 2,5 s. Preservados os 12 acréscimos, separados por 0,05 s, e a exigência de `acréscimo 11` no documento 2. |

Não foram criados testes novos. Foram corrigidos os 2 métodos existentes, sem ampliar o escopo para o programa ou para os testes do executor.

## Diagnóstico local

Antes da edição, executei o comando dos 2 testes indicados. T04 passou. T38 falhou na prioridade de `CLAUDE_PID`, retornando `/usr/bin/true` em vez de `/bin/sleep`. A consulta direta confirmou a restrição do ambiente.

```sh
/bin/ps -o comm= -p $$
```

```text
zsh:1: operation not permitted: /bin/ps
```

O programa consulta `ps` no macOS e segue para o `PATH` quando essa consulta falha. Isso explica a reprovação local. A falha do binário multicall no Ubuntu e a instabilidade no macOS com Python 3.13 são relatos fornecidos pela tarefa 03. Não foram reproduzidas nesta máquina.

A investigação adicional das falhas remotas foi dispensada porque a tarefa já forneceu os sintomas e determinou as correções. Não alterei o teste para ignorar T38 nem simulei uma aprovação da consulta por PID.

## Verificações da tarefa 01

Os comandos abaixo foram executados com captura integral da saída e `pipefail`, preservando os códigos de falha dos testes mesmo com `tail -3`.

### 1. Aceite nos 2 pacotes

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

Saída de `hopper-documentation-anth-pt-br`, código do unittest 1.

```text
Ran 42 tests in 29.005s

FAILED (failures=1)
```

Saída de `hopper-documentation-anth-en`, código do unittest 1.

```text
Ran 42 tests in 29.461s

FAILED (failures=1)
```

As saídas completas identificam somente T38 como reprovado, no cenário `CLAUDE_PID antes do PATH`. T04 passou em ambos os pacotes.

### 2. Testes do executor nos 2 pacotes

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

Saída de `hopper-documentation-anth-pt-br`, código 0.

```text
Ran 31 tests in 0.304s

OK
```

Saída de `hopper-documentation-anth-en`, código 0.

```text
Ran 31 tests in 0.309s

OK
```

### 3. Diferença entre os programas

```sh
diff hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

```diff
31c31
< LANGUAGE = "pt-br"
---
> LANGUAGE = "en"
```

O código 1 do `diff` corresponde à diferença esperada. A única linha diferente é `LANGUAGE`.

## 5 repetições consecutivas

Em `aceite/testes`, com `PYTHONDONTWRITEBYTECODE=1` e `TZ=UTC`, executei o comando abaixo 5 vezes seguidas. O pacote padrão é o português.

```sh
python3 -m unittest test_repositorio.Localizacao.test_R38_encontra_o_executavel_do_claude_code test_copiador.Copiador.test_R04_espera_o_arquivo_de_historico_parar_de_crescer
```

| Repetição | Saída de duração | T38 | T04 | Resultado e código |
| --- | --- | --- | --- | --- |
| 1 | `Ran 2 tests in 1.490s` | Falhou | Passou | `FAILED (failures=1)`, código 1 |
| 2 | `Ran 2 tests in 1.497s` | Falhou | Passou | `FAILED (failures=1)`, código 1 |
| 3 | `Ran 2 tests in 1.484s` | Falhou | Passou | `FAILED (failures=1)`, código 1 |
| 4 | `Ran 2 tests in 1.483s` | Falhou | Passou | `FAILED (failures=1)`, código 1 |
| 5 | `Ran 2 tests in 1.492s` | Falhou | Passou | `FAILED (failures=1)`, código 1 |

As 5 saídas trazem a mesma reprovação, na linha 160 de `test_repositorio.py`.

```text
FAIL: test_R38_encontra_o_executavel_do_claude_code (test_repositorio.Localizacao.test_R38_encontra_o_executavel_do_claude_code) (candidato='CLAUDE_PID antes do PATH')
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

Portanto, não foi possível demonstrar as 5 aprovações conjuntas exigidas. Os cenários seguintes de T38, de prioridade do `PATH` e de uso do executável local, não apresentaram falhas.

## Conferência de escopo

Conferi os hashes SHA-256 dos 326 arquivos versionados contra o registro inicial. Somente `aceite/testes/test_repositorio.py` e `aceite/testes/test_copiador.py` mudaram. Este relatório é o único arquivo novo. Os 2 programas mantiveram os hashes iniciais.

`git diff --check` terminou com código 0, sem saída. Nenhuma alteração em `SPEC.md`, `.github/`, `.claude/` ou nos demais registros de `execucao/`.

## Pendência de validação

1. Comprovar a aprovação integral do aceite e das 5 repetições, incluindo T38, em ambiente que permita consultar processos. Recomendo que o Claude verificador repita os comandos fora deste sandbox e confira a matriz do GitHub. Nesta sessão, não foi possível executar os cenários Linux nem as versões Python 3.9 e 3.13. Não existe nova decisão necessária do proprietário.
