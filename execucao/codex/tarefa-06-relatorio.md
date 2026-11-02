# Relatório da tarefa 06

A correção foi implementada nos 2 pacotes. T14 passou e os 43 testes do executor passaram em cada idioma. O aceite terminou com 41 aprovações em 42 testes por pacote. Somente T38 reprovou, pela restrição de `ps` no sandbox, exceção prevista na tarefa 06.

## Ambiente e alcance

- Execução local em 2026-11-02, Darwin arm64, Python 3.14.8, branch `versao-2`, HEAD `e5ba224ea14190a249f836d54e672e33a930d4cd`.
- Pasta `/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth`.
- As alterações da tarefa 05 já estavam no disco. Foram preservadas, incluindo os textos de `modelos.md` e `templates.md`.
- Código e testes editados somente no pacote em português. O programa em inglês foi regenerado com o `sed` exigido na tarefa 01. Os testes foram copiados para o pacote em inglês.
- Sem rede, VPS, instalação, chamada real a `claude -p` ou comando Git de gravação.
- Os testes rodaram com `PYTHONDONTWRITEBYTECODE=1`. As saídas completas foram capturadas em uma pasta temporária própria antes de aplicar `tail -3`. O código do unittest foi conferido separadamente do código do `tail`.

## Alterações

Em [hopper_documentation_anth.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:988), `validar_resposta` calcula o maior número existente por tipo e código. A expressão `RE_ID_ITEM` identifica os componentes de cada item. A cópia regenerada fica no [programa em inglês](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/scripts/hopper_documentation_anth.py:988).

Na conferência textual, um item ausente passa quando seu número é menor ou igual ao maior existente do mesmo tipo e código. Itens futuros, códigos sem itens desse tipo e referências provisórias inexistentes continuam rejeitados. A regra vale também na validação das respostas de migração.

A validação de mensagens foi preservada. Uma mensagem citada deve existir no documento 2, com número até o fim do trecho processado. A alteração não muda a conferência de origens, a numeração dos novos itens ou o tratamento de mudanças não aplicadas. A nova tentativa e seus registros continuam como na tarefa 05.

## Testes do executor

Os testes ficam em [test_hopper_documentation_anth.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py:553), classe `RegressoesDaTarefa05`, e na [cópia idêntica em inglês](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/tests/test_hopper_documentation_anth.py:553).

| Teste | Alteração e cobertura |
| --- | --- |
| `test_item_futuro_ou_codigo_inexistente_e_rejeitado_em_todos_os_campos` | Ajustado o teste anterior de item inexistente. Confere os limites de D, F e PD, códigos ausentes e a separação dos máximos por tipo e código. Números maiores de outro tipo ou código não liberam a referência inválida. |
| `test_item_apagado_a_mao_continua_aceito` | Novo teste. Grava itens 1 e 2 nos documentos 4, 5 e 6, apaga os itens 1 e relê a pasta. As referências apagadas passam nos campos textuais, no handoff e nas situações. Cobre os códigos `3f9c2a71` e `antigo-abcd`. |

Os testes existentes continuam cobrindo M19 inexistente, mensagem copiada depois do fim do trecho, `N1`, itens existentes, migração e as 2 chamadas do redator simulado.

Antes da correção, T14 falhou na terceira rodada, após a exclusão manual. Depois, passou sem alterar o aceite.

```text
Antes
Ran 1 test in 0.344s

FAILED (failures=1)

Depois
Ran 1 test in 0.320s

OK
```

O novo teste também foi executado antes da correção. A classe passou de 11 para 12 métodos. Somente o novo método falhou, por rejeitar os 6 identificadores apagados. Depois da correção, todos passaram.

```text
Antes
Ran 12 tests in 0.190s

FAILED (errors=1)

Depois
Ran 12 tests in 0.168s

OK
```

## Verificações da tarefa 01

### 1. Aceite nos 2 pacotes

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

Saída do pacote em português, código do unittest 1.

```text
Ran 42 tests in 30.533s

FAILED (failures=1)
```

Saída do pacote em inglês, código do unittest 1.

```text
Ran 42 tests in 30.594s

FAILED (failures=1)
```

Nos 2 pacotes, a única falha foi `test_R38_encontra_o_executavel_do_claude_code`, no cenário `CLAUDE_PID antes do PATH`. T14 e os outros 40 testes passaram. Não existem erros nem testes ignorados nessas execuções.

T38 esperava `/bin/sleep`, mas recebeu `/usr/bin/true`, candidato do `PATH`. A consulta direta confirmou o bloqueio de `ps` no ambiente.

```sh
/bin/ps -o comm= -p $$
```

```text
zsh:1: operation not permitted: /bin/ps
```

### 2. Testes do executor nos 2 pacotes

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

Saída do pacote em português, código 0.

```text
Ran 43 tests in 0.542s

OK
```

Saída do pacote em inglês, código 0.

```text
Ran 43 tests in 0.513s

OK
```

### 3. Diferença entre os programas

```sh
diff hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

Saída, código 1, esperado pela única diferença de idioma.

```diff
31c31
< LANGUAGE = "pt-br"
---
> LANGUAGE = "en"
```

Os arquivos de testes são idênticos. `git diff --check` terminou com código 0.

## Conferidor do resultado antigo de A3

A verificação adicional da tarefa 05 foi repetida sobre o resultado antigo preservado.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 aceite/conferir.py execucao/aceite/a3-2/docs-by-hopper-documentation --idioma pt-br --roteiro aceite/roteiro.json
```

Saída, código 1, esperado para esse resultado antigo.

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

O inventário inicial registrou 790 arquivos, incluindo 628 arquivos em `SPEC.md`, `aceite/`, `.github/`, `.claude/`, `execucao/` e `.git/`. Os hashes SHA-256 desses 628 arquivos permaneceram iguais. Nesses destinos, o único arquivo novo é este relatório.

Comparada ao estado inicial, esta tarefa alterou somente os programas e os arquivos de testes dos 2 pacotes, além de criar este relatório. As alterações preexistentes dos modelos foram preservadas. A pasta temporária própria foi removida depois da conferência, sem deixar cópias ou backups no repositório.

## O que ficou sem fazer

1. Comprovar T38 fora do isolamento que bloqueia `ps`. Recomendo que o verificador execute esse teste em um ambiente que permita consultar o processo. Não preciso de informação ou decisão adicional do proprietário. A tarefa 06 prevê essa limitação, e nenhuma outra falha permaneceu no aceite.
