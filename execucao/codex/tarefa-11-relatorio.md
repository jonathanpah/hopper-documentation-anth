# Relatório da tarefa 11

A correção está implementada nos 2 pacotes. Os 49 testes do executor passam em cada pacote. O aceite passou em 41 dos 42 testes de cada pacote. O teste T38 permanece limitado pelo isolamento, que impede executar `/bin/ps`; ele também falha com os programas originais de `HEAD`.

Ambiente verificado em 2026-11-02. Branch `versao-2`, Python 3.14.8, execução local sem rede.

## Alterações por item

1. No ramo `rodada` de [`main()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1694), a linha de falha é preparada antes de tentar registrar a exceção. Uma exceção de `registrar_escrita()` deixa de impedir sua impressão. A gravação do marcador também fica protegida. Se a rodada já falhou, sua linha e seu motivo são preservados. Se apenas o marcador falhar após uma rodada bem-sucedida, o comando retorna 1 e informa o erro do marcador. A linha continua sendo a última da saída padrão e também aparece na saída de erro. Nenhum texto de `T` mudou.
2. Foi acrescentado 1 teste em cada arquivo `tests/test_hopper_documentation_anth.py`, na classe `RegressoesDaTarefa11`. O teste executa o programa real com `CLAUDE_CONFIG_DIR` em uma pasta com modo `0555`. Os 3 subcasos usam ausência de marcador, marcador gravável e um diretório como destino inválido do marcador. Todos exigem código 1, última linha com o prefixo do idioma, erro original de permissão e saída de erro sem `Traceback`. O marcador gravável deve conter código e linha corretos. As permissões e os temporários são restaurados e removidos pelo teste.
3. O programa inglês foi gerado a partir do português pelo `sed` exigido. O `diff` mostra somente `LANGUAGE`, e os arquivos de testes dos 2 pacotes são idênticos.
4. O [`CONTRIBUTING.md` da raiz](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/CONTRIBUTING.md:19) recebeu 1 frase com o comando de avaliação e a explicação sobre a liberação do Bash por `--allow-tools`.

## Regressão e verificações adicionais

Antes da correção, o novo teste falhou nos 3 subcasos de cada pacote pela presença de `Traceback`. Depois da correção, passou nos 2 pacotes.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s hopper-documentation-anth-pt-br/tests -p 'test_hopper_documentation_anth.py' -k RegressoesDaTarefa11
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s hopper-documentation-anth-en/tests -p 'test_hopper_documentation_anth.py' -k RegressoesDaTarefa11
```

Saída após a correção, em cada pacote.

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.175s

OK
```

Uma verificação adicional de `main()` com falhas simuladas conferiu motivos diferentes para a rodada, o registro e o marcador. Ela confirmou a preservação do erro original e a conversão de uma falha isolada do marcador em código 1.

```text
pt-br: excecao, registro e marcador falham: OK
pt-br: rodada devolve falha e marcador falha: OK
pt-br: rodada conclui e marcador falha: OK
en: excecao, registro e marcador falham: OK
en: rodada devolve falha e marcador falha: OK
en: rodada conclui e marcador falha: OK
```

## Os 3 comandos da tarefa 01

Os comandos abaixo rodaram com `PYTHONDONTWRITEBYTECODE=1`, para não criar bytecode nos diretórios protegidos. Os comandos 1 e 2 foram executados pelo Bash com `pipefail`. A ordem das saídas é português e inglês.

### Comando 1

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

```text
Ran 42 tests in 30.917s

FAILED (failures=1)
Ran 42 tests in 29.552s

FAILED (failures=1)
```

Código do comando `0`.

### Comando 2

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

```text
Ran 49 tests in 0.759s

OK
Ran 49 tests in 0.688s

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

Código do comando `1`.

O código 0 do comando 1 decorre do `cd` final. Os 2 resumos registram reprovação e não foram tratados como aprovação. O código 1 do `diff` é esperado, pois existe a diferença permitida na linha `LANGUAGE`.

## Limitação do aceite

A leitura da saída completa identificou a mesma falha T38 nos 2 pacotes, no subcaso `CLAUDE_PID antes do PATH`.

```text
FAIL: test_R38_encontra_o_executavel_do_claude_code
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

O programa tenta consultar `ps` para resolver `CLAUDE_PID`. A consulta é bloqueada pelo isolamento, e a busca segue para o candidato de `PATH`. Uma sonda direta confirmou o bloqueio.

```text
PermissionError: [Errno 1] Operation not permitted: '/bin/ps'
```

O T38 também foi executado com os programas originais de `HEAD`, copiados para uma pasta temporária, sem substituir os arquivos de trabalho. Ambos produziram a mesma divergência entre `/usr/bin/true` e `/bin/sleep`. Isso confirma que essa reprovação não foi introduzida pela tarefa 11. Nenhum teste foi alterado ou ignorado para obter aprovação.

## Preservação e escopo

A comparação de SHA-256 e permissões confirmou a preservação dos 263 arquivos existentes em `SPEC.md`, `aceite/`, `.github/`, `.claude/` e nos `evals/` dos pacotes. Isso inclui os 2 prompts de avaliação que já estavam alterados antes desta tarefa. As avaliações e a tarefa 11 preexistentes em `execucao/` foram preservadas.

`git diff --check` passou. A sintaxe Python dos 4 arquivos alterados foi validada sem gerar bytecode. Não foram feitos commit, push, merge, instalação, acesso à VPS, chamadas de rede ou execução real do redator.

## O que ficou sem fazer

1. A aprovação integral do aceite permanece pendente apenas em T38. Recomendo que o verificador repita o comando 1 em um ambiente que permita executar `ps`. O isolamento desta sessão impede essa verificação. A correção, o teste de regressão, a geração do programa inglês e a atualização documental estão entregues.
