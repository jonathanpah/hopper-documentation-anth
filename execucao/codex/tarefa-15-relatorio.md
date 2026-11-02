# Relatório da tarefa 15

A migração em partes está implementada nos 2 pacotes. Os 65 testes do executor passam em cada pacote, incluindo os 6 novos. O aceite aprova 41 de 42 testes em cada idioma. A aprovação integral depende de T38, que também reprova com o programa anterior neste ambiente isolado.

Execução local em 2026-11-02, na branch `versao-2`, com Python 3.14.8. O commit inicial é `33479d999c58761bf5eaf7995ddc8f742a01494d`. Foram seguidas as regras aplicáveis das tarefas 01, 05, 12 e 14.

## Alterações

1. A nova função [`partes_da_migracao()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1462) soma os caracteres dos arquivos antigos e usa `LIMITE_DO_TRECHO`, de 300.000 caracteres. Até esse limite, devolve a lista original como 1 parte. Acima dele, agrupa os handoffs pelo identificador da conversa, em ordem de data e hora dos nomes dos arquivos. Ordena as conversas pela data do primeiro handoff e preserva cada conversa inteira quando ela cabe no limite. Conversas maiores são divididas em partes consecutivas dos seus handoffs. O último handoff fica na última parte da conversa. O `index.md` antigo entra na 1ª parte.
2. Em [`migrar()`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py:1543), cada parte passa pelo ciclo existente de chamada, validação e nova tentativa, diário, gravação, verificação interna e exclusão. A entrada da parte seguinte é montada depois da gravação da anterior e lê os documentos 4, 5 e 6 atualizados. A validação recebe somente os nomes dos arquivos da parte atual. O registro de rodadas recebe os registros de migração e exclusão de cada parte.
3. O diário mantém o nome e o formato existentes. Quando existe, sua parte é reaplicada primeiro, com a resposta e os identificadores reservados. Os arquivos dessa parte são excluídos do planejamento restante. Uma falha interrompe o comando com a linha final existente e preserva as partes concluídas. A próxima execução processa os arquivos restantes. O retorno de `migrar()` soma os arquivos concluídos em todas as partes da execução, incluindo uma parte recuperada do diário.
4. A seção de migração de [`modelos.md`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/skills/hopper-documentation-anth/modelos.md:60) e de [`templates.md`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/skills/hopper-documentation-anth/templates.md:60) ganhou a frase pedida, com tradução fiel. Handoffs intermediários substituídos por um posterior vão em `sem_conteudo`. Os parágrafos do documento 7 citam os handoffs de origem.
5. A classe [`RegressoesDaTarefa15`](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py:1091) acrescenta 6 testes. O arquivo de testes foi copiado para o pacote inglês. Os testes usam o redator falso existente, interceptando o processo chamado pelo executor. Nenhum redator real foi executado.
6. O programa inglês foi gerado com o `sed` solicitado. O `diff` mostra somente `LANGUAGE`.

```sh
sed 's/^LANGUAGE = "pt-br"$/LANGUAGE = "en"/' hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py > hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

O limite conta caracteres, incluindo caracteres multibyte, e preserva os arquivos inteiros. Um arquivo individual maior que 300.000 caracteres ocupa uma parte própria e excede o limite, como ocorre com uma mensagem indivisível no tratamento de R11.

## Testes novos

| Teste | Resultado verificado |
| --- | --- |
| `test_duas_conversas_grandes_fazem_duas_chamadas_com_documentos_atualizados` | Uma pasta com 380.020 caracteres, 2 conversas e datas intercaladas gera 2 chamadas. Confere o agrupamento, o índice na 1ª parte, os documentos 4 a 6 atualizados na 2ª chamada, 2 verificações internas, 2 exclusões e a soma final de 5 arquivos. |
| `test_falha_na_segunda_parte_preserva_primeira_e_nova_execucao_conclui` | A 2ª parte recebe data inválida nas 2 tentativas. O comando falha após 3 chamadas totais. A 1ª parte fica gravada e seus arquivos antigos são apagados. Os arquivos da 2ª ficam intactos. Outra execução faz 1 chamada, conclui os 2 arquivos restantes e preserva o handoff da 1ª parte. |
| `test_diario_da_segunda_parte_reaplica_sem_redator_nem_itens_duplicados` | Em uma pasta com 3 conversas, interrompe a gravação dos itens da 2ª parte. O diário contém somente os arquivos dessa parte. Outra execução a reaplica sem repetir sua chamada e chama o redator somente para a 3ª parte, com os documentos atualizados. Confere a soma de 3 arquivos restantes e a ausência de itens duplicados. |
| `test_conversa_maior_que_limite_termina_com_ultimo_handoff` | Uma conversa com 3 handoffs de 160.000 caracteres gera 3 chamadas em ordem. O documento 7 final vem do último handoff. Os 9 itens e a soma de 4 arquivos são preservados, sem arquivos antigos restantes. |
| `test_limite_exato_mantem_uma_chamada_e_ordem_original` | Uma pasta com exatamente 300.000 caracteres mantém a ordem original e faz 1 chamada, mesmo usando caracteres multibyte. |
| `test_arquivo_indivisivel_acima_do_limite_fica_inteiro` | Um handoff individual de 300.001 caracteres fica inteiro em uma parte própria, depois da parte do índice. |

Os 2 primeiros testes foram executados também com a cópia do programa anterior, guardada antes das alterações e carregada em processo isolado. Ambos reprovaram, confirmando que exercitam comportamentos ausentes no programa original.

```text
Ran 2 tests in 0.116s

FAILED (failures=2)
```

Com a implementação, a execução isolada dos 6 testes novos em português passou. A suíte completa abaixo inclui os mesmos 6 testes nos 2 pacotes.

```text
Ran 6 tests in 0.422s

OK
```

## Os 3 comandos da tarefa 01

Os comandos rodaram com `PYTHONDONTWRITEBYTECODE=1`, para preservar os diretórios protegidos. Nos comandos 1 e 2, `tee` capturou a saída completa antes de `tail`, em pasta temporária. O código de cada suíte foi capturado com `PIPESTATUS[0]`. Abaixo estão os comandos pedidos e suas saídas, na ordem português e inglês.

### Comando 1

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

```text
Ran 42 tests in 31.967s

FAILED (failures=1)
Ran 42 tests in 32.947s

FAILED (failures=1)
```

Cada suíte retornou código `1`. O comando completo terminou com código `0` devido ao `cd` final. As suítes não foram tratadas como integralmente aprovadas. T30 e T31 passaram nos 2 pacotes.

### Comando 2

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

```text
Ran 65 tests in 1.439s

OK
Ran 65 tests in 1.270s

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

As saídas completas dos 2 pacotes mostram somente a reprovação de [T38](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/aceite/testes/test_repositorio.py:160), no subcaso `CLAUDE_PID antes do PATH`.

```text
AssertionError: PosixPath('/usr/bin/true') != PosixPath('/bin/sleep')
```

O mesmo teste foi executado com o programa anterior, sem alterar os arquivos de aceite. Reproduziu a mesma falha.

```text
Ran 1 test in 0.183s

FAILED (failures=1)
```

Uma consulta direta ao processo atual por `ps -o comm= -p <pid>` foi bloqueada pelo isolamento.

```text
PermissionError: [Errno 1] Operation not permitted: 'ps'
```

Essa evidência explica a limitação da consulta usada por T38 neste ambiente. A função de localização do executável e os critérios de aceite foram preservados.

## Conferência final e limites

`git diff --check` passou. A sintaxe dos 4 arquivos Python foi validada sem gerar bytecode. Os testes dos 2 pacotes são idênticos. A comparação das árvores sintáticas dos programas anterior e atual mostrou somente a alteração de `migrar()` e a inclusão de `partes_da_migracao()`. As funções de validação, nova tentativa, gravação e verificação interna mantêm o código anterior.

A comparação de SHA-256 e permissões dos 552 arquivos preexistentes confirmou mudanças somente nos programas, testes e modelos dos 2 idiomas. Os outros 546 arquivos foram preservados, incluindo `SPEC.md`, `aceite/`, `.github/`, `.claude/`, os `evals/` e os arquivos anteriores de `execucao/`. O único arquivo acrescentado é este relatório. A tarefa 15, que já estava sem rastreamento no início, foi preservada.

Não foram feitos comandos `git` que gravem, chamadas de rede, acesso à VPS, instalação ou execução real de `claude -p`. A migração real citada na tarefa e seu diário não foram alterados. Os testes usaram pastas temporárias isoladas. Os temporários desta execução foram removidos depois de registrar os resultados.

## Pendência

1. A aprovação integral do aceite depende de T38. Recomendo que o verificador execute o aceite em um ambiente que permita consultar `ps`. Essa execução fica com o verificador, fora deste isolamento. Não ficou implementação pendente no escopo da tarefa 15.
