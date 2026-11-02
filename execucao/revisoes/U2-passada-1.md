# Revisão independente de U2, passada 1

- Revisor: subagente sem o contexto do executor (G09, C22). A revisão começou no Claude Fable 5.1 e terminou no Claude Opus 5.5, depois da troca de modelo da sessão.
- Data: 2026-11-02.
- Estado avaliado: commit `eae5c9e` da branch `versao-2`. Os critérios ainda não têm manifesto nem tag `criterios-congelados`.
- Material lido: `SPEC.md` (seções 5, 6 e 7, Anexos B a G, decisões C03 a C07, C09 a C13, C17 e C18, glossário e garantias G03, G04 e G09); `execucao/decisoes.md` (D-09 e D-13); `aceite/testes/*.py`, `aceite/conferir.py`, `aceite/roteiro.json`, `aceite/casos/**` e `.github/workflows/verificar.yml`; `execucao/avaliacoes/u2/aceite-versao-atual-pt-br.log`; `execucao/verificacoes.md` (V-U2-01, V-U2-02, V-U8-02 e V-U8-02 correção); `git diff fb208df..HEAD` e `git diff c25a8be..HEAD` dos critérios; o clone de leitura no commit `8c2e438`, só para conferir os casos herdados.
- Comandos rodados: `python3 -m py_compile` nos 8 arquivos Python dos critérios (sem erro); `python3 aceite/conferir.py <pasta> --idioma pt-br` em cada pasta de `aceite/casos/conferidor/` (`valida` aprova 9 de 9; cada `invalida-F<n>` reprova em F<n>; `invalida-F1` também em F5 e `invalida-F2` também em F8, por falta do mesmo objeto); `conferir.py` com `--roteiro` em `valida` (F9 reprova, o esperado, porque `valida` é o caso B1); 5 cópias de `valida` na pasta temporária da sessão, alteradas para provar comportamentos do conferidor e apagadas depois; comparação do caso B1 com o texto literal do Anexo B. Os testes de aceite não rodaram. Nenhum arquivo do repositório foi alterado, exceto este.

## Achados que bloqueiam o congelamento

1. **Respostas simuladas em português no pacote em inglês (T13 e os testes que usam `rodada-b1`).**
   - Arquivo: `aceite/testes/apoio.py`, linhas 167 a 177 (`Ambiente.resposta`); `aceite/casos/redator/rodada-b1.json`, `rodada-m7.json`, `rodada-mudanca-inexistente.json` e `rodada-modelo-errado.json`.
   - Problema: no pacote em inglês, a tradução troca só o campo `situacao`, e o campo `conversa_simplificada` continua começando por `**Assunto: `. Um programa que confere a regra do Anexo D rejeita a resposta, e um programa que grava o texto como veio reprova em T13 no inglês.
   - Evidência: Anexo D, regras que o programa confere além do esquema: "A cadeia `conversa_simplificada` começa na linha de assunto." Anexo E, textos fixos, linha de assunto em inglês: `**Subject: <text>.**`. T13 (`test_redator.py`, linha 91) exige que o bloco comece por `TEXTO["assunto"]`. T13 passa hoje no inglês só porque o programa acrescenta uma linha de assunto feita do `resumo` quando ela falta (`bloco_do_documento_3`, `if not corpo.startswith(T["assunto"])`), comportamento que a spec não prevê. O bloco gravado fica com um parágrafo `**Assunto: …**` sem origem, que F3 reprova.
   - Correção: em `resposta()`, traduzir também `**Assunto: ` para `**Subject: ` no campo `conversa_simplificada`.

2. **T14 reaproveita uma resposta com origem fora do trecho novo.**
   - Arquivo: `aceite/testes/test_redator.py`, linha 114 (`test_R14_numera_com_o_proximo_numero_livre`, 3ª rodada).
   - Problema: a 3ª rodada tem o trecho novo M8, e a resposta usada é `rodada-m7`, com o item N1 e a mudança de PD1 de origem M7. Um programa que aplica a regra do Anexo D rejeita a resposta, e T14 reprova. Congelado assim, T14 impede que o programa passe a cumprir a regra.
   - Evidência: Anexo D: "`origem` cita mensagens do trecho novo ou itens existentes." `rodada-m7.json`: `"origem": ["M7-3f9c2a71"]` no item e na mudança. T14 passa hoje porque o programa aceita qualquer mensagem já gravada (`mensagens_validas = {f"M{m['n']}-{codigo}" for m in gravadas}`, linha 1248 do programa em português), regra mais frouxa que a do Anexo D.
   - Correção: montar a 3ª resposta no próprio teste a partir de `rodada-m7`, com M8 no lugar de M7, como T16 faz com `outra-conversa.json`.

3. **A conferência do manifesto não detecta arquivo novo em `aceite/`.**
   - Arquivo: `.github/workflows/verificar.yml`, linhas 21 a 27.
   - Problema: `sha256sum --check` confere só os arquivos listados no manifesto, então um arquivo acrescentado em `aceite/` passa sem "CRITÉRIO ALTERADO". Por exemplo, um `aceite/testes/unittest.py` substitui o executor de testes, porque `python3 -m unittest` põe a pasta atual no início do `sys.path` e a linha 51 roda dentro de `aceite/testes`. O passo dos testes de aceite passaria sem rodar nenhum teste, com o manifesto conferindo.
   - Evidência: glossário, "Critérios congelados": "Os arquivos de `aceite/`, o arquivo `.github/workflows/verificar.yml` e o `SPEC.md`". C18: a verificação falha "quando um critério congelado não confere com o manifesto". `verificar.yml`, linha 22: `sha256sum --check --strict aceite/MANIFESTO.sha256`.
   - Correção: comparar também a lista de `git ls-files aceite .github/workflows/verificar.yml SPEC.md`, sem o manifesto, com os caminhos do manifesto, e falhar com "CRITÉRIO ALTERADO" quando as 2 listas diferirem.

4. **F2 deixou de detectar mensagem sem o comentário de registros (regressão do commit `eae5c9e`).**
   - Arquivo: `aceite/conferir.py`, linhas 86 a 89 (`Conferencia.mensagens`).
   - Problema: um cabeçalho só conta como mensagem quando a linha seguinte é o comentário de registros. Fora o 1º cabeçalho, uma mensagem sem o comentário vira texto da mensagem anterior, e F2 aprova.
   - Evidência: Anexo F, F2: "cada mensagem tem o comentário de registros". Em uma cópia de `valida` sem a linha `<!-- registros: u8 u8 -->` de M6, o conferidor deu `F2: aprovada`. Só F8 reprovou, porque outros documentos citam M6. Uma mensagem sem o comentário e sem citação passa em todas as verificações.
   - Correção: reconhecer o cabeçalho pelo padrão completo `RE_MENSAGEM` (`## M<n>-<código> · <data> · <autor>`), que `## Plano` não satisfaz, e reprovar em F2 o cabeçalho sem o comentário na linha seguinte.

5. **O caso de borda de R11, trecho novo acima de 300 mil caracteres, não tem verificador.**
   - Arquivo: `aceite/testes/test_redator.py`, `test_R11_envia_so_o_trecho_novo_e_os_documentos_atuais` (linhas 16 a 46).
   - Problema: T11 usa só o caso B1, com poucas centenas de caracteres. A divisão em partes, com 1 chamada e 1 bloco por parte, não tem teste, e o roteiro de aceite não a alcança, porque a conversa de teste é curta. Depois do congelamento, acrescentar o teste exige o "sim" do proprietário (C18).
   - Evidência: seção 6, R11: "O programa divide o trecho em partes consecutivas, sem dividir uma mensagem, e faz 1 chamada ao redator por parte, em ordem. Cada parte vira 1 bloco do documento 3." K09: "1 compactação perto de 967 mil tokens pode gerar vários trechos de 300 mil caracteres". A busca por `300` em `aceite/testes/` só encontra um corte de mensagem de erro em `test_copiador.py`.
   - Correção: acrescentar a T11 um caso com, por exemplo, 4 mensagens de 100 mil caracteres, e conferir 2 chamadas ou mais, em ordem, nenhuma mensagem dividida e 1 bloco do documento 3 por chamada.

## Achados menores

6. **Outros casos de borda da seção 6 sem teste.**
   - Arquivo: `test_estrutura.py` (T01 e T02), `test_copiador.py` (T04 e T05), `test_execucao.py` (T22) e `test_redator.py` (T12).
   - Problema: estes comportamentos não têm asserção. R01, pasta do projeto sem permissão de gravação (falha só no registro e documento 1 não gravado). R02, 2 conversas com os mesmos 8 caracteres (código de 12 caracteres e fato no registro). R04, registro da última mensagem copiada que sumiu (a cópia continua pela data e hora e anota o fato). R04, histórico apagado (T22 confere só que `motivo` não está vazio, e não o texto "arquivo de histórico não encontrado"). R05, registro do usuário vazio depois de retirar os lembretes. R12, a rodada seguinte repete a chamada depois de uma falha.
   - Evidência: seção 6, linhas de R01, R02, R04, R05 e R12. A busca em `aceite/testes/` por `chmod`, `3f9c2a715b8e` e "não encontrado" não encontra nada.
   - Correção: acrescentar 1 caso de cada no teste do requisito, antes da tag.

7. **T12 cobre só a rejeição de C04 e não confere a instrução do redator.**
   - Arquivo: `test_redator.py`, linhas 48 a 82; `aceite/casos/redator/rodada-modelo-errado.json`.
   - Problema: o único caso de modelo é a rejeição com 10% de Sonnet. Um programa que rejeita qualquer modelo auxiliar passa, e C04 foi decidida para evitar isso. O registro dos outros modelos no campo `modelos` não é conferido, e `--system-prompt` é conferido só como não vazio (linha 65).
   - Evidência: C04: "aceita a resposta só quando `modelUsage` contém `claude-sonnet-5-5` e esse modelo responde por no mínimo 90% dos tokens de saída. Outros modelos listados entram no registro de rodadas." O Anexo D traz o texto literal da instrução em português.
   - Correção: acrescentar uma resposta com 95% de Sonnet e 5% de outro modelo, aceita e com os 2 modelos em `modelos`, e comparar a instrução com o texto do Anexo D no pacote em português.

8. **Asserção de T27 que sempre passa.**
   - Arquivo: `test_execucao.py`, linha 110, e linha 108.
   - Problema: `assertEqual(X if cond else "falhou", "falhou")` vale "falhou" nos 2 ramos, então só confere que o registro não está vazio. A linha 108 aceita qualquer linha final.
   - Evidência: seção 6, R27: "A segunda rodada desiste e informa o motivo."
   - Correção: `self.assertTrue(any(x["acionamento"] == "pedido" and x["resultado"] == "falhou" and x["motivo"] for x in registro))`.

9. **T37 confere `~/.claude` por um arquivo que o próprio teste copiou para lá.**
   - Arquivo: `test_repositorio.py`, linhas 107 a 117.
   - Problema: `shutil.copytree` copia para `casa/.claude` a pasta de dados em que a 1ª cópia já gravou `rodadas.jsonl`, então a asserção da linha 117 passa mesmo que o programa ignore `~/.claude`. O evento traz o `transcript_path` da pasta original, então o caminho sem `CLAUDE_CONFIG_DIR` nunca procura o histórico.
   - Evidência: docstring do teste: "sem ela, de ~/.claude". R37 e C11 (busca por `<pasta de configuração>/projects/*/<identificador>.jsonl`).
   - Correção: copiar só `projects/` para `casa/.claude` e rodar `rodada --sessao` com `HOME` apontando para `casa`, conferindo a linha nova em `casa/.claude/plugins/data/hopper-documentation-anth-hopper-documentation-anth/rodadas.jsonl`.

10. **T38 não prova a ordem de C12 fora da máquina do executor.**
    - Arquivo: `test_repositorio.py`, linhas 124 a 149.
    - Problema: depois da troca por links simbólicos (V-U2-02, item 4), os 3 executáveis falsos resolvem para o mesmo `sleep`, e nenhum cenário tem 2 candidatos ao mesmo tempo. A precedência de `CLAUDE_PID` sobre o `PATH` só é testada quando a máquina tem um `claude` real no `PATH`, o que não acontece no GitHub.
    - Evidência: C12: "usa o executável indicado por `CLAUDE_PID` […] Depois, o `claude` do `PATH`. Depois, `~/.local/bin/claude`." Linhas 129, 137, 141 e 146.
    - Correção: em cada cenário, pôr também o candidato seguinte, apontando para outro programa (por exemplo, um link para `true`), para que o resultado esperado se distinga pelo `resolve()`.

11. **T04 (C09) pode passar sem nenhuma espera.**
    - Arquivo: `test_copiador.py`, linhas 29 a 43.
    - Problema: o registro novo entra 0,15 s depois do início. Se o programa leva mais de 0,15 s até a 1ª leitura, o que é comum em um executor lento do GitHub, o registro já está no arquivo, e o teste passa sem a espera de C09.
    - Evidência: C09: "A leitura começa quando o tamanho fica igual por 1 segundo, ou depois de 5 segundos." Prova de C09: "T04, com um arquivo que cresce durante a cópia".
    - Correção: acrescentar registros durante cerca de 0,6 s, 1 a cada 0,05 s, e exigir o último no documento 2.

12. **T03 não olha fora da pasta temporária.**
    - Arquivo: `test_estrutura.py`, linha 52.
    - Problema: o inventário cobre só a raiz temporária, e o programa roda com o `HOME` real e a pasta temporária do sistema. Uma gravação nesses lugares passa.
    - Evidência: T03, na seção 5: "A lista de arquivos criados ou alterados fora dessas 2 pastas fica vazia." N02.
    - Correção: em T03, apontar `HOME` e `TMPDIR` para pastas dentro da raiz temporária, como T37 já faz com `HOME`.

13. **Com `TZ=UTC`, nenhum teste distingue o fuso da máquina do UTC.**
    - Arquivo: `test_estrutura.py` (T02) e `test_copiador.py` (T05).
    - Problema: um programa que usa sempre o UTC passa em T02 e T05. No fuso de São Paulo, uma conversa iniciada às 22h de 14/03 receberia a pasta com a data de 15/03.
    - Evidência: R02: "com a data da primeira mensagem no fuso da máquina". Anexo B: "Os testes rodam com `TZ=UTC`."
    - Correção: acrescentar a T02 1 caso com `TZ=America/Sao_Paulo` (1ª mensagem às 2026-03-15T01:00Z e pasta `2026-03-14`), com registro em `decisoes.md` por complementar o Anexo B, ou registrar que o fuso da máquina só é provado em U8.

14. **Escolhas que a spec não fixa e que os testes fixam sem registro.**
    - Arquivo: (a) `aceite/casos/b1/esperado-en.md` e `conferir.py`, linha 86, com o comentário `<!-- registros: … -->` em português no pacote em inglês; (b) `test_redator.py`, linha 22, com a 1ª linha da entrada ("Conversa: … Código: … Intervalo:") e os nomes das tags em português nos 2 pacotes, enquanto "Task:" é aceito (V-U2-02, item 5); (c) `test_execucao.py`, linha 122, e T12, T22, T24 e T31, com `resultado` "nada novo" e "falhou" no registro de rodadas nos 2 pacotes; (d) `test_copiador.py`, linhas 181 e 182, com o corpo da resposta a perguntas e do plano aprovado sem a linha de rótulo do clone de leitura; (e) `test_migracao.py`, linha 68, com o código `antigo-a2f1` exigido na entrada da migração; (f) `test_migracao.py`, linha 115, com a chamada de migração antes da chamada da rodada, porque o redator simulado responde pela ordem das chamadas.
    - Problema: cada escolha é razoável, mas uma implementação que segue a outra leitura possível da spec reprova.
    - Evidência: Anexo E: "O pacote em inglês usa a tradução fiel de todo o texto fixo deste anexo". A linha "Resultados" dos textos fixos traz "nothing new" e "failed", e o mesmo anexo diz que "nada novo" e "em andamento" "ficam só no registro de rodadas". Anexo B, B1: "o corpo da mensagem segue o formato do clone de leitura"; no clone, o corpo é `TEXT["answers"] + "\n" + …`, com `TEXT["answers"]` igual a "O usuário respondeu às perguntas da IA:". O Anexo D diz só que cada arquivo antigo vem "precedido do nome dele" e não fixa a ordem entre migração e rodada.
    - Correção: registrar as 6 escolhas como complemento de D-13 antes da tag.

15. **O teste novo de T05 aceita um documento 7 que viola R20.**
    - Arquivo: `test_copiador.py`, linha 74 (`test_R05_titulo_no_texto_de_uma_mensagem_nao_e_cabecalho`).
    - Problema: a conversa tem 3 mensagens, e a resposta usada é `rodada-nada-relevante`, cujo `handoff` cita M4 a M7. Como o documento 7 ainda não existe, o programa o grava com esse campo (caso de borda de R17), e o teste aceita um documento 7 que cita mensagens inexistentes. Um programa que garante R20 na gravação reprova.
    - Evidência: R20: "Todo identificador de mensagem ou de item citado nos documentos 3 a 7 existe na pasta de documentação." `rodada-nada-relevante.json`: `"objetivo": "… (M1-3f9c2a71 a M4-3f9c2a71)"` e `"pautas_e_estado": "Sem mudança. (M1-3f9c2a71 a M7-3f9c2a71)"`.
    - Correção: usar no teste uma resposta `nada_relevante` cujo `handoff` cite só M1 a M3.

16. **T07 não usa todos os casos da classe `Masking`.**
    - Arquivo: `aceite/casos/b2/ocultacao.json` e `test_copiador.py`, `test_R07_oculta_senhas_tokens_e_chaves`.
    - Problema: o arquivo traz os 46 casos de `CASES` e os 3 de `test_whole_web_tokens`, mas não os de `test_nested_json` (senha em JSON aninhado de 1 a 4 níveis) nem os de `test_linear_time` (8 textos longos em menos de 2 s). Os testes do executor também não os têm.
    - Evidência: Anexo B, B2: "O teste T07 usa todos os casos da classe `Masking` do clone de leitura". No clone, commit `8c2e438`, a classe `Masking` tem 4 métodos de teste.
    - Correção: acrescentar os 4 casos de JSON aninhado ao arquivo e a T07, e os 8 de tempo com um limite.

17. **F5 e F7 aplicam regras diferentes das do Anexo F.**
    - Arquivo: `conferir.py`, linhas 235, 272 e 290.
    - Problema: (a) F5 exige exatamente as 9 linhas `## `, e uma linha `## ` no texto de uma seção reprova, o mesmo tipo de falha que V-U8-02 achou em F2; (b) F7 calcula os 90% por documento, e um documento de 1 frase com 26 palavras reprova; (c) F7 tira da contagem toda linha que começa por `- `, inclusive itens de lista com texto corrido, e uma frase de 45 palavras em lista passa.
    - Evidência: Anexo F, F5: "Cada documento 7 tem as 9 seções." F7: "Ficam fora da contagem os títulos, as linhas de assunto, as linhas de metadados, as tabelas, os blocos de código e os identificadores." R19: "Nos documentos 3 a 7 […], no mínimo 90% das frases têm até 25 palavras". Provas em cópias de `valida`: a seção extra `## Detalhe` no documento 7 deu `F5: reprovada`; 1 frase de 26 palavras no documento 4 deu "4-decisoes.md: 1 de 1 frases passam de 25 palavras"; um item de lista com 45 palavras no documento 7 deu `F7: aprovada`.
    - Correção: F5 confere as 9 seções em ordem e aceita outras linhas `## ` entre elas; F7 tira da contagem só as linhas `- <rótulo>: ` com os rótulos do Anexo E; e a leitura dos 90%, por documento ou no total, fica registrada em `decisoes.md`.

18. **F9 não tem caso do conferidor, e a verificação do GitHub nunca roda F9.**
    - Arquivo: `aceite/casos/conferidor/` e `verificar.yml`, linhas 72 a 82.
    - Problema: nenhuma pasta passa em F9, não existe `invalida-F9`, e o laço do GitHub roda o conferidor sem `--roteiro`. A parte das conversas migradas em F1 a F3 e a regra "substituída por" de F4 também não têm caso. A leitura usada por F9 já falhou uma vez, no aceite de A3 (V-U8-02).
    - Evidência: Anexo F: "Ele também escreve as pastas `aceite/casos/conferidor/invalida-F<n>/`, cada uma com 1 defeito". `conferir.py aceite/casos/conferidor/valida --idioma pt-br --roteiro aceite/roteiro.json` dá "F9: reprovada" com as mensagens "[1, 2, 4, 6]" não encontradas, o esperado para o caso B1.
    - Correção: escrever à mão uma pasta válida com as 6 mensagens do passo F-C e uma `invalida-F9`, e rodar as 2 com `--roteiro` no GitHub.

19. **Os testes do executor não rodam quando um teste de aceite reprova.**
    - Arquivo: `verificar.yml`, linhas 52 a 55.
    - Problema: o passo "Testes do executor" não tem `if: always()`, então fica de fora sempre que o passo anterior reprova.
    - Evidência: C17: "Ela roda os testes de aceite e os testes do executor dos 2 pacotes". A linha 57 já usa `if: always()` no passo da lista de reprovações.
    - Correção: acrescentar `if: always()` ao passo "Testes do executor".

20. **O registro de G04 não corresponde aos critérios atuais.**
    - Arquivo: `execucao/avaliacoes/u2/aceite-versao-atual-pt-br.log`; `execucao/verificacoes.md`, V-U2-01, V-U2-02 e V-U8-02 (correção).
    - Problema: a saída bruta é do commit `fb208df`, anterior às correções de V-U2-02 e de `eae5c9e`, e tem 31 testes. O 32º teste (`test_R05_titulo_no_texto_de_uma_mensagem_nao_e_cabecalho`) não tem saída bruta da falha sem a mudança, e o registro só afirma que ele "falha sem a correção".
    - Evidência: G04: "Cada verificação nova falha sem a mudança que ela cobre" e "a falha sem a mudança fica registrada".
    - Correção: rodar de novo os testes de aceite na versão final contra a versão atual (`8dbb40b`), e o teste novo de T05 contra o programa anterior a `eae5c9e`, com as saídas brutas em `execucao/avaliacoes/u2/`.

## O que está pronto e o que não está

Considero prontos para congelar a interface dos testes (D-09 e D-13), o caso B1 (os arquivos `historico.jsonl`, `esperado-pt-br.md` e `esperado-m7-pt-br.md` são iguais ao texto literal do Anexo B; o registro `summary` traz só um campo `leafUuid` a mais, sem efeito), os casos B2 tirados de `CASES` e de `test_whole_web_tokens`, os casos B3 (formatos iguais ao `exemplo.md` da versão atual e ao do clone, e o código `antigo-a2f1` confere com o SHA-256 do nome do arquivo), as respostas simuladas no pacote em português, as verificações F1, F3, F4, F6, F8 e F10, os 6 textos do roteiro, iguais aos do passo F-C, a matriz da verificação do GitHub e o inventário de T32, igual ao Anexo C. Todo verificador citado na seção 5 tem teste ou verificação correspondente, e não encontrei dependência do clone de leitura, da rede ou de caminho fixo da máquina nos critérios. Não estão prontos os achados 1 a 5, que bloqueiam o congelamento, porque deixariam congelado um teste que uma implementação correta não satisfaz, uma brecha na detecção de mudanças, uma regressão de F2 e um comportamento sem verificador. Recomendo corrigir também os achados 6 a 20 antes da tag, porque depois dela cada mudança exige o "sim" do proprietário (C18). O manifesto e a tag ainda não existem, então o job "critérios congelados" reprova em todo envio até o congelamento, como esperado. O registro de execução não mostra nenhuma execução de `verificar.yml` no GitHub, e por isso o Python 3.9 no `macos-latest` e o comportamento dos 3 jobs continuam sem prova; recomendo 1 execução registrada antes de criar a tag.
