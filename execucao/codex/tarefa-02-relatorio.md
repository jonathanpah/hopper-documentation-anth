# Relatório da tarefa 02

As 3 partes foram implementadas. Os 31 testes do executor passam em cada pacote, incluindo 18 novos. Os 13 casos do conferidor produzem o resultado esperado. Os programas diferem somente em `LANGUAGE`.

O aceite tem 41 aprovações em 42 testes por pacote. A única reprovação é T38, na consulta por `CLAUDE_PID`, porque este sandbox impede executar `/bin/ps`. A aprovação integral do aceite continua sem comprovação neste ambiente.

## Ambiente e alcance

- Execução local em 2026-11-02, branch `versao-2`, commit de referência `896d5b5b1138ed960ba75a56f907b0c1172bbd8c`.
- Árvore inicialmente sem alterações. Regras lidas nas tarefas 01 e 02, nas 3 revisões citadas e nas decisões D-13 e D-18.
- Programa editado em português e regenerado em inglês com o `sed` da tarefa 01. Testes do executor copiados entre os pacotes e idênticos por `cmp`.
- Uso de `PYTHONDONTWRITEBYTECODE=1` nas verificações, preservando os caches existentes.
- Sem rede, VPS, instalação de plugin, chamada real a `claude -p` ou comando de gravação no git.
- Alterações em `aceite/` e no fluxo limitadas à autorização da parte 2. Em `execucao/`, somente este relatório e os 2 logs autorizados.
- Os arquivos externos alterados são [roteiro.py](/Users/jonathan/hopper-sonda/roteiro.py) e [driver.py](/Users/jonathan/hopper-sonda/driver.py).

## Parte 1. Correções do programa

Os arquivos centrais são [o programa em português](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py) e [a cópia em inglês](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-en/scripts/hopper_documentation_anth.py).

| Item da tarefa | Funções | Resultado |
| --- | --- | --- |
| 1, achado 1 | `reservar_itens e gravar_itens` | Reserva números consecutivos por tipo e código, começando no próximo número livre. Itens do mesmo tipo deixam de compartilhar o identificador. |
| 2, achados 1, 4 e 8 | `gravar_rodada, reaplicar_diarios, escrever e migrar` | O diário guarda resposta validada, mapa de referências e modelos antes de gravar documentos. A reaplicação usa os identificadores guardados e pula os já presentes, sem comparar textos. A migração tem diário por pasta e trava própria. A execução seguinte conclui sem chamar o redator, inclusive após exclusão parcial. Removida migracao_pendente. O documento 3 também recebe as referências finais. |
| 3, achado 2 | `copiar` | Localiza o uuid nos registros brutos e extrai mensagens somente dos registros posteriores. Uma continuação do Claude vira nova mensagem, sem mudar os bytes anteriores. Quando a âncora sumiu, compara instantes completos dos registros com o minuto do cabeçalho. O Anexo E fixa o comentário com 2 identificadores, sem campo de data. Por isso o programa mantém esse formato e registra o aviso de precisão limitada ao minuto. |
| 4, achado 4 | `validar_resposta` | Confere a situação das mudanças conforme o tipo do item existente antes de criar o diário. Identificadores inexistentes continuam para a lista de mudanças não aplicadas. Uma resposta inválida preserva os documentos e não deixa diário. |
| 5, achado 6 | `validar_resposta` | Aceita somente letras, dígitos e hífen nos identificadores de conversa de itens e handoffs da migração. Rejeita separadores de caminho antes de gravar. |
| 6, achado 7 | `verificacao_interna` | Obtém origens dos documentos 4, 5 e 6 e dos documentos 7 gravados no disco. A resposta só fornece a lista sem_conteudo e as conversas cujos handoffs devem existir. Os arquivos antigos permanecem quando a conferência reprova. |
| 7, achado 9 | `rodada` | Registra a falha da migração automática e continua com cópia e escrita. Regrava o documento 1 e retorna código 1. A linha final informa o resultado da documentação e a falha da migração. |
| 8, achado 10 | `rodada` | Captura qualquer Exception, registra o motivo e tenta gravar o documento 1, como no tratamento anterior de Falha. Mantido o tratamento adicional de main e do marcador, entregue na tarefa 01. |
| 9, achado 11 | `migrar` | A chamada ao redator ocorre fora da trava de pasta. A trava de migração serializa migrações do mesmo projeto. A trava de pasta cobre a leitura dos documentos atuais e a gravação, sem prender a cópia durante a chamada ao redator. |
| 10, achado 12 | `Documento2.mensagens` | Só aceita o próximo número esperado, começando em M1, com o código da conversa e o comentário na linha seguinte. Uma citação de outro código ou fora da sequência continua no corpo da mensagem. |
| 11, achado 13 | `conferir_modelos` | Lê outputTokens e output_tokens. Rejeita contagem ausente, inválida, negativa ou com total zero. Mantém a exigência de pelo menos 90% de tokens do Sonnet 5.5. |
| 12, achado 14 | `validar_esquema, validar_resposta e escrever` | Valida recursivamente os campos exigidos, tipos, listas, limites e campos extras do esquema. Confere resumo de até 80 caracteres, data válida em AAAA-MM-DD, origens das mudanças e dos itens. Na rodada, aceita mensagens somente da parte nova, itens existentes ou referências N. Na migração, aceita somente nomes dos arquivos antigos como origem. |
| 13, achado 15 | `entrada_da_migracao e ocultar_campos` | Oculta os textos dos arquivos antigos antes de enviá-los e cada campo textual da resposta antes do diário e da gravação. |
| 14, achado 16 | `codigo_de` | Registra a colisão em linha com motivo. Preservada a regra atual, que dá 12 caracteres à conversa documentada depois. O caso “a mais nova” não é tratado quando a conversa mais antiga é documentada depois. |
| 15, achado 17 | `registrar e registrar_escrita` | O resumo entra na própria linha acrescentada por registrar, por parâmetro opcional. Removidas registrar_resumo e as regravações completas do registro de rodadas. |
| 16, achado 18 | `configuracao` | Sem arquivo, mantém o padrão verdadeiro. Um arquivo presente que não seja objeto JSON com migracao_automatica booleano vale como falso. O motivo entra no registro de rodadas. |

### Achados já tratados pela tarefa 01

- Achado 3. `mensagem_de_usuario` já ignora `isMeta`. A correção e o teste da tarefa 01 foram preservados.
- Achado 5. `comando_escrita` já usa o primeiro `cwd` do histórico no processo separado, sem passar a pasta do evento. Teste preservado.
- Achado 10. `main` já captura exceções e grava o marcador. Faltava o tratamento dentro de `rodada` para regravar o documento 1. Esta tarefa completa essa parte.
- Achado 11. A tarefa 01 já limita a espera da trava de pasta da cópia a 25 segundos. Faltava liberar essa trava durante a chamada ao redator da migração, agora corrigido.

## Testes novos do executor

Os 18 testes estão em [test_hopper_documentation_anth.py](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py) e na cópia idêntica do pacote em inglês. Os 13 testes anteriores foram mantidos.

| Teste | Cobertura |
| --- | --- |
| `test_01_reserva_numeros_por_tipo_e_codigo` | Numeração distinta para 2 decisões migradas do mesmo tipo e conversa. |
| `test_02_diario_guarda_mapa_e_reaplica_sem_comparar_texto` | Diário com mapa, retomada após os itens e referência final no documento 3, sem nova chamada. |
| `test_03_copia_recomeca_no_registro_bruto_seguinte` | Continuação do Claude com 1 ou vários registros, só registros posteriores, bytes anteriores preservados. |
| `test_04_mudanca_invalida_nao_grava_nem_deixa_diario` | Mudança de situação inválida sem alteração nos documentos e sem diário. |
| `test_05_migracao_rejeita_codigo_com_separador_antes_de_gravar` | Identificador de migração com separador de caminho rejeitado antes de gravar. |
| `test_06_verificacao_confere_origens_gravadas_no_disco` | Item perdido no disco impede a exclusão dos arquivos antigos. |
| `test_07_migracao_retomada_usa_diario_sem_redator` | Migração interrompida após itens conclui pelo diário, sem chamar o redator. |
| `test_08_falha_migracao_continua_rodada_e_grava_indice` | Migração automática falha, mas a documentação continua, com índice e linha final completos. |
| `test_09_rodada_captura_excecao_generica_e_grava_indice` | Exceção genérica dentro da rodada registra falha e índice. |
| `test_10_migracao_libera_trava_de_pasta_ao_chamar_redator` | Redator da migração consegue adquirir a trava de pasta durante a chamada. |
| `test_11_documento2_ignora_citacao_fora_da_sequencia_e_codigo` | Citação de cabeçalho de outro código não muda a sequência nem a retomada. |
| `test_12_modelos_exigem_contagem_e_aceitam_output_tokens` | Contagem alternativa output_tokens, ausência de tokens e proporção insuficiente. |
| `test_13_valida_esquema_completo_e_origens` | Limites, campos extras, tipos, datas, origens e janela nova no caminho real da escrita. |
| `test_14_migracao_oculta_entrada_e_todos_campos_de_texto` | Ocultação na entrada da migração e nos campos de texto gravados. |
| `test_15_colisao_de_codigo_entra_no_registro` | Colisão registrada e código com 12 caracteres, nos 2 idiomas. |
| `test_16_resumo_e_acrescentado_sem_regravar_registro` | Resumo acrescentado sem regravar rodadas.jsonl. |
| `test_17_configuracao_invalida_desliga_migracao_e_registra` | Configurações inválidas desligam a migração e registram o motivo; ausência mantém o padrão. |
| `test_18_rejeita_bloco_sem_linha_de_assunto` | Resposta relevante sem linha de assunto não grava o bloco nem deixa diário. |

Antes das correções, a execução dos 31 testes produziu o resultado abaixo. As contagens incluem subverificações.

```text
Ran 31 tests in 0.263s

FAILED (failures=22, errors=8)
```

Após os ajustes finais dos testes, uma comparação adicional carregou o programa original de `HEAD` em arquivo temporário e executou os 18 testes novos. Todos reprovaram sem as correções. Nenhum teste novo passou por engano nessa comparação.

```text
Programa anterior da tarefa 02, HEAD 896d5b5: 18 testes novos executados, 18 reprovados.
test_01_reserva_numeros_por_tipo_e_codigo: reprovado sem a correção
test_02_diario_guarda_mapa_e_reaplica_sem_comparar_texto: reprovado sem a correção
test_03_copia_recomeca_no_registro_bruto_seguinte: reprovado sem a correção
test_04_mudanca_invalida_nao_grava_nem_deixa_diario: reprovado sem a correção
test_05_migracao_rejeita_codigo_com_separador_antes_de_gravar: reprovado sem a correção
test_06_verificacao_confere_origens_gravadas_no_disco: reprovado sem a correção
test_07_migracao_retomada_usa_diario_sem_redator: reprovado sem a correção
test_08_falha_migracao_continua_rodada_e_grava_indice: reprovado sem a correção
test_09_rodada_captura_excecao_generica_e_grava_indice: reprovado sem a correção
test_10_migracao_libera_trava_de_pasta_ao_chamar_redator: reprovado sem a correção
test_11_documento2_ignora_citacao_fora_da_sequencia_e_codigo: reprovado sem a correção
test_12_modelos_exigem_contagem_e_aceitam_output_tokens: reprovado sem a correção
test_13_valida_esquema_completo_e_origens: reprovado sem a correção
test_14_migracao_oculta_entrada_e_todos_campos_de_texto: reprovado sem a correção
test_15_colisao_de_codigo_entra_no_registro: reprovado sem a correção
test_16_resumo_e_acrescentado_sem_regravar_registro: reprovado sem a correção
test_17_configuracao_invalida_desliga_migracao_e_registra: reprovado sem a correção
test_18_rejeita_bloco_sem_linha_de_assunto: reprovado sem a correção
Subverificações: 21 falhas e 10 erros.
```

## Parte 2. Critérios de aceite

| Item da tarefa | Arquivos ou verificações | Resultado |
| --- | --- | --- |
| 1 | `apoio.resposta, validar_resposta e bloco_do_documento_3` | Traduz a linha de assunto nas respostas simuladas em inglês. Aplica D-18 (h), rejeitando o bloco relevante sem a linha correta. Deixa de criar assunto a partir do resumo. |
| 2 | `test_redator.py, T14` | A 3ª resposta é montada no teste com M8 no lugar de M7. |
| 3 | `verificar.yml, critérios congelados` | Compara os caminhos de git ls-files com os do manifesto, excluindo o próprio manifesto. Uma diferença informa CRITÉRIO ALTERADO. Prova local com lista completa e manifesto temporário que omite 1 arquivo versionado. |
| 4 | `conferir.py, mensagens e F2; invalida-F2-sem-registros; verificar.yml` | Reconhece o padrão completo RE_MENSAGEM sem depender do comentário. A ausência do comentário reprova F2. O laço extrai F2 de nomes com sufixo, sem confundir sem-registros com o número. |
| 5 | `test_redator.py, novo caso de T11` | Usa 4 mensagens de 100 mil caracteres. Exige pelo menos 2 chamadas em ordem, mensagens inteiras e 1 bloco do documento 3 por chamada. |
| 6, achados 6 a 13 | `test_estrutura.py, test_copiador.py, test_redator.py, test_execucao.py e test_repositorio.py` | Acrescenta pasta sem gravação, colisão registrada, âncora ausente, histórico apagado com motivo exato, usuário vazio e repetição após resposta inválida. Confere 95% de Sonnet com 5% de outro modelo e ambos no registro. Compara a instrução literal em português. Corrige a asserção de T27. T37 copia só projects e busca por sessão a partir do HOME temporário. T38 usa cópia de sleep no Linux e link no macOS, sempre com o candidato seguinte apontando para outro programa. Acompanha 12 acréscimos no histórico em cerca de 0,6 segundo. T03 isola HOME e TMPDIR. T02 usa America/Sao_Paulo, com 01h UTC no dia anterior local. |
| 6, achado 15 | `test_copiador.py, T05` | A resposta nada_relevante cita somente M1 a M3. Também confere que o texto inteiro com títulos chegou ao redator, para detectar a perda que a comparação dos bytes do documento 2 não detectava. |
| 6, achado 16 | `ocultacao.json e test_copiador.py, T07` | Acrescenta os 4 JSON aninhados do clone de leitura. Confere segredo oculto, JSON decodificável e campo note preservado. Os 8 textos de tempo da classe Masking passam pela cópia, cada um em menos de 2 segundos. Essa medição inclui inicialização e gravação, além da ocultação. |
| 7 | `conferir.py, F5 e F7; test_conferidor.py` | F5 exige as 9 seções em ordem e aceita títulos extras. F7 exclui somente os rótulos de metadados do Anexo E, conta listas de texto e calcula os 90% sobre todos os documentos 3 a 7 juntos, conforme D-18 (g). Mantém os limites por frase e parágrafo. |
| 8 | `valida-roteiro, invalida-F9 e verificar.yml` | Casos escritos sem executar o programa. A pasta válida contém os 6 pedidos do roteiro, a senha oculta e a linha Write, com D de origem M1, F de M4 e PD de M6. Inclui conversa migrada sem documentos 2 e 3 e decisão substituída por item existente. A inválida troca somente a origem de F para M3. O fluxo usa --roteiro nas 2 pastas. |
| 9 | `verificar.yml, Testes do executor` | Acrescenta if: always(). |
| 10 | `logs autorizados em execucao/avaliacoes/u2` | Executa os critérios finais contra 8dbb40b e T05 contra 7bcdf5d. Registra também a prova no commit anterior à correção de T05, descrita abaixo. Nenhum manifesto ou tag foi criado. |

Foram acrescentados 6 testes de aceite para os casos de borda e 4 testes do conferidor. O total passou de 32 para 42 por pacote. Os demais complementos entraram nos testes dos respectivos requisitos.

Os 4 testes do conferidor cobrem F2 sem comentário, F5 com título extra e ordem incorreta, F7 com limite global e lista longa, e F9 com conversa migrada. Também conferem F4 quando a decisão substituta não existe.

### Provas de G04

Os critérios finais foram copiados para a extração local de `8dbb40b`, criada com `git archive 8dbb40b | tar -x -C /tmp/versao-atual`. A execução foi feita em português, com UTC e saída completa no [log da versão atual](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/execucao/avaliacoes/u2/aceite-versao-atual-final-pt-br.log).

```text
Ran 42 tests in 3.782s

FAILED (failures=35, errors=5)
```

As contagens são de falhas e erros de subverificações. O erro de T32 ocorre porque a extração por `git archive` não contém `.git`. Esse erro não prova uma falha do programa. Os 4 testes do conferidor passam nessa extração, pois exercitam os critérios copiados, e não o programa antigo.

Existe uma divergência no commit indicado para T05. `7bcdf5d` vem depois de `eae5c9e` e já contém a correção de leitura do documento 2. Por isso T05 passa nele. A ordem foi confirmada por `git log` e pelo conteúdo de `Documento2.mensagens`.

A comparação adicional usou `eae5c9e^`, commit `5868b164b48ae88dd05b5d6a91c41aa9f776b8c0`. A asserção que confere o texto inteiro enviado ao redator reprova nesse programa anterior. A saída de `7bcdf5d`, seguida da saída de `5868b16`, está no [log de T05](/Users/jonathan/Library/CloudStorage/Dropbox/5-ai/5-claude/hopper-documentation-anth/execucao/avaliacoes/u2/t05-antes-da-correcao.log).

| Código avaliado em T05 | Resultado com o critério final |
| --- | --- |
| Código final desta tarefa | 1 teste aprovado |
| `7bcdf5d`, indicado na tarefa | 1 teste aprovado, pois já contém a correção |
| `5868b16`, imediatamente anterior à correção | 1 teste reprovado por texto cortado na entrada do redator |

Não alterei os commits nem provoquei uma falha artificial em `7bcdf5d`. Antes de acrescentar a asserção da entrada do redator, T05 também passava no commit anterior. Essa lacuna do teste foi corrigida no critério final.

### Conferência local do fluxo

```text
Lista completa de critérios versionados: aprovada.
Arquivo versionado ausente do manifesto temporário: CRITÉRIO ALTERADO, retorno 1.
Testes do executor: if: always() conferido no fluxo.
Nenhum manifesto do repositório ou tag foi criado.
```

## Parte 3. Condutor fora do repositório

- `roteiro.py` guarda o instante do envio da mensagem 6 e exige registro `pedido`, etapa `escrita`, resultado final e `data` posterior ao envio.
- Nas 2 passagens, a espera exige `gatilho-escrita`, etapa `escrita`, resultado final e data posterior ao início da compactação correspondente. Uma escrita da passagem 1 não encerra a espera da passagem 2.
- `driver.registro_posterior` compara os instantes completos, com fuso, e rejeita data ausente, inválida ou sem fuso.
- O teste rápido usa um `rodadas.jsonl` falso. Ele começa com linhas antigas e iguais ao marco e acrescenta a escrita posterior durante a espera. Também executa os próprios predicados extraídos de `main` para confirmar sua ligação aos marcos corretos.
- Nenhuma sessão do Claude Code foi aberta.

```text
pedido: ignorou registros antigos e iguais ao marco; aceitou só a nova escrita
gatilho-escrita: ignorou registros antigos e iguais ao marco; aceitou só a nova escrita
datas completas: fusos equivalentes, igualdade e datas inválidas conferidos
leitura do código: os 2 predicados reais de main exigem data posterior ao marco correto
nenhuma sessão do Claude Code foi aberta
```

## Saída dos 3 comandos pedidos

A ordem é português e depois inglês. Os comandos são os da tarefa 01 e foram executados após a última alteração.

### 1. Testes de aceite

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
```

```text
Ran 42 tests in 28.939s

FAILED (failures=1)
Ran 42 tests in 28.208s

FAILED (failures=1)
```

O código final do comando com `tail` e `cd` não comprova a aprovação. Os resultados acima são reprovações. A consulta por `CLAUDE_PID` de T38 falha nos 2 pacotes. Os cenários de `PATH` e de `~/.local/bin/claude` passam; os subtestes permitem executá-los mesmo após a falha do primeiro cenário.

### 2. Testes do executor

```sh
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
```

```text
Ran 31 tests in 0.301s

OK
Ran 31 tests in 0.296s

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

O retorno 1 do `diff` corresponde à única diferença esperada.

## Conferidor em todas as pastas

`valida-roteiro` e `invalida-F9` foram executadas com `--roteiro aceite/roteiro.json`. As demais foram executadas sem esse argumento.

| Pasta | Retorno | Verificações | Reprovações observadas |
| --- | --- | --- | --- |
| `invalida-F1` | 1 | 9 | F1, F5 |
| `invalida-F10` | 1 | 9 | F10 |
| `invalida-F2` | 1 | 9 | F2, F8 |
| `invalida-F2-sem-registros` | 1 | 9 | F2 |
| `invalida-F3` | 1 | 9 | F3 |
| `invalida-F4` | 1 | 9 | F4 |
| `invalida-F5` | 1 | 9 | F5 |
| `invalida-F6` | 1 | 9 | F6 |
| `invalida-F7` | 1 | 9 | F7 |
| `invalida-F8` | 1 | 9 | F8 |
| `invalida-F9` | 1 | 10 | F9 |
| `valida` | 0 | 9 | nenhuma |
| `valida-roteiro` | 0 | 10 | nenhuma |

Os 13 resultados são os esperados. As reprovações adicionais de `invalida-F1` e `invalida-F2` decorrem da falta do mesmo objeto usado por outras verificações.

## Limitações e conferências finais

- `/bin/ps -o comm= -p <pid>` foi recusado com `operation not permitted`. A função `executavel_do_claude` não foi alterada. T38 usa candidatos diferentes e mantém a prova de precedência, sem transformar o bloqueio do sandbox em aprovação.
- Os arquivos Python foram analisados com `ast.parse(..., feature_version=(3, 9))`. Isso confere a sintaxe, sem substituir uma execução real com Python 3.9.
- `git diff --check` passou. `SPEC.md`, `.claude/` e as instruções das tarefas não foram alterados. Em `.github/`, somente `workflows/verificar.yml` mudou.
- Não foram criados `aceite/MANIFESTO.sha256`, tags ou commits. Não foi executado o fluxo no GitHub nem a matriz real de Ubuntu e macOS.
- As alterações ficaram no disco para o verificador. Os temporários desta execução foram removidos depois de gravar os resultados. Os arquivos e caches anteriores foram preservados.

## Pendência

1. Falta comprovar o aceite integral em um ambiente que permita a consulta do processo por `ps`, além da matriz real de Ubuntu e macOS. Recomendo que o verificador execute T38 e o fluxo antes do congelamento e da instalação. Não preciso de nova decisão do proprietário para as mudanças já autorizadas. A restrição deste sandbox impede concluir essa prova local.
