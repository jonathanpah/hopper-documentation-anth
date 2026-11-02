# Revisão independente de U3, U4 e U6, passada 1

Data: 2026-11-02 (UTC). Revisor: subagente sem o contexto do executor (G09, C22), retomado depois de uma interrupção.

Estado revisado: o programa do commit `eae5c9e`, igual ao do HEAD `62ce2d5` da branch `versao-2`. Os 2 pacotes diferem só na linha `LANGUAGE`. As linhas citadas são as desse commit.

Material lido: `SPEC.md` (seções 5, 6 e 7, Anexos B, D e E, decisões C01 a C13 e C23), o programa, `execucao/verificacoes.md` (V-U2-02, V-U3-U7, V-U8-02 e a correção), `execucao/decisoes.md`, os testes de aceite, o redator simulado e as respostas dele, os casos B1 e B3, e o aceite real de A3 em `execucao/aceite/a3/`.

Verificações feitas: `py_compile` nos 2 programas. Testes de aceite em uma cópia extraída do commit, com 31 aprovados em cada pacote (T32 não roda fora de um repositório git). 17 cenários próprios, com o apoio dos testes de aceite e o redator simulado, em pastas temporárias. Nenhum arquivo do repositório foi alterado por esta revisão, além deste.

## Achados

1. **`gravar_itens`, linhas 1040 a 1064: 2 itens novos do mesmo tipo recebem o mesmo número.** O 1º laço calcula todos os números com `proximo_numero` antes de gravar qualquer item, então N1 e N2 do tipo D viram os 2 `D1`. O 2º laço pula o N2 porque `### D1-…` já existe, e as referências a N2 nos documentos 3 e 7 passam a apontar para o D1.
   - Evidência da spec: R14, "numera cada item novo com o próximo número livre"; N03, "Reaproveitar um número de mensagem ou de item"; C05, "grava os arquivos e confere a gravação".
   - Evidência do código: linha 1053, `mapa[item["ref"]] = f"{tipo}{proximo_numero(pasta_doc, tipo, codigo_do_item)}-{codigo_do_item}"`, sem gravação entre as iterações; no 2º laço, `if f"### {item_id}\n" in texto: continue`.
   - Cenário C1 (rodada com 2 decisões): o documento 4 fica só com `D1-3f9c2a71`, e o documento 7 diz "D1-3f9c2a71 e D1-3f9c2a71 vigentes". Cenário C13 (migração com 2 decisões da mesma conversa): só a 1ª é gravada, a linha final é "Migração concluída", e os 3 arquivos antigos são apagados.
   - Os testes passam porque `rodada-b1`, `rodada-m7` e `migracao-b3-*` trazem no máximo 1 item de cada tipo por código. Em A3 o redator real também devolveu 1 item por tipo em cada rodada.
   - Gravidade: reprova R14 e R30. Viola N03 e, na migração, N06 (ver achado 7).

2. **`copiar`, linhas 743 a 785: a parte nova da última mensagem do Claude já copiada se perde.** A cópia procura o ponto de retomada pelos limites das mensagens extraídas de novo, e não pelo registro seguinte ao último identificador gravado. Quando a última mensagem do Claude cresce depois da cópia, o acréscimo some por 1 de 2 caminhos.
   - Mensagem de 1 registro: a âncora casa pelo campo `primeiro`, e a continuação é pulada sem aviso.
   - Mensagem de vários registros: a âncora falha, a cópia segue pela data com precisão de minuto (linha 771), grava o aviso falso "o registro da última mensagem copiada não existe mais" e perde as mensagens do mesmo minuto.
   - Evidência da spec: C10, "A cópia seguinte começa no registro depois do último identificador da última mensagem"; R04, "acrescenta ao documento 2 só as mensagens posteriores à última mensagem já copiada"; R08, "as respostas do Claude"; R29, "sem mensagem perdida".
   - Evidência do código: linha 762, `posicoes = [i for i, m in enumerate(mensagens) if m["ultimo"] == ultimo or m["primeiro"] == ultimo]`.
   - Cenário C11 (padrão da skill): a cópia acontece logo depois do Bash. A fala que fecha o turno e o relato do resultado depois da notificação somem, e o registro da cópia não traz aviso. Cenário C2 (compactação no meio de um turno): a continuação do Claude e uma mensagem do usuário do mesmo minuto somem, com o aviso falso.
   - Dado real de A3: M4 e M13 são o Bash da skill, com 1 registro cada. O documento 2 não tem nenhuma fala do Claude entre M4 e M5 nem entre M13 e M14, e o registro de rodadas não traz aviso. O turno do Claude só termina com uma resposta depois do resultado do Bash, então a fala existiu e se perdeu. Isso é inferência: o histórico real fica na VPS e não foi lido nesta revisão.
   - A skill sempre roda assim (SKILL.md, passos 1 e 2), então toda rodada a pedido perde a fala de fechamento do turno.
   - Gravidade: reprova R04, R08 e R29. Contraria C10.

3. **`mensagem_de_usuario`, linhas 558 a 591: registros `isMeta` entram como mensagem do "Usuário".** A expansão do SKILL.md que o Claude Code injeta quando a skill roda vira mensagem do usuário no documento 2 e vai ao redator como fala do usuário.
   - Evidência da spec: R09 exclui "lembretes do sistema, saídas de gatilhos, … ecos de comandos"; R08 inclui "as mensagens do usuário".
   - Dado real de A3: M3 tem o autor "Usuário" e cerca de 50 linhas que começam com "Base directory for this skill: /opt/hopper-documentation-anth/…" e seguem com o SKILL.md inteiro, inclusive o comando com o identificador da sessão. Cenário C12 reproduz.
   - V-U8-02 atribui a reprovação de F2 a "uma resposta do Claude" com títulos do SKILL.md. As linhas estão em M3, uma mensagem do "Usuário". A correção de `eae5c9e` tornou a leitura tolerante a essas linhas, mas o conteúdo continua no documento 2, e o conferidor aprovou 10 de 10 com ele.
   - Gravidade: reprova R09 em parte e a autoria de R08.

4. **`aplicar_mudancas`, linhas 1076 a 1107, com `validar_resposta`, linhas 867 a 914: mudança com situação inválida bloqueia a conversa e duplica itens.** A situação das mudanças só é conferida na gravação (linha 1093), depois do bloco do documento 3 e dos itens novos. A falha deixa o diário com a resposta inválida. Toda rodada seguinte reaplica o diário antes de chamar o redator e falha de novo, até alguém apagar o diário à mão.
   - Duplicação: a busca de item já gravado (linha 1048) compara o texto bruto da resposta com a 1ª linha gravada, que já tem `N1` trocado pelo identificador final. Um item com `N1` no texto ganha 1 cópia nova a cada reaplicação.
   - Evidência da spec: R12, "descarta a resposta que não cumpre o esquema do Anexo D"; Anexo D, "`situacao` precisa ser um valor do Anexo E"; caso de borda de R12, "Nada é gravado nos documentos 3 a 7 … A rodada seguinte repete a chamada"; R29, "sem item duplicado"; C05, "valida o JSON contra o esquema e as situações contra o Anexo E".
   - Cenário C4 (mudança com a situação "encerrada", sem "em M-ID"): a rodada 2 falha com o bloco M7 e o item D2 já gravados, e o diário `3f9c2a71-M7-M7.json` fica. A rodada 3, com trecho novo, falha com o mesmo motivo sem chamar o redator.
   - Cenário C15 (item F "Painel ajustado conforme N1."): F2, F3 e F4 são gravados nas rodadas 2, 3 e 4.
   - Gravidade: reprova R12 e R29. "encerrada" sem a mensagem é um erro plausível do redator real.

5. **`comando_escrita`, linha 1479: o gatilho de escrita usa outra pasta do projeto.** Ele passa à rodada o `cwd` do evento, e o gatilho de cópia e a skill usam o `cwd` do 1º registro. Quando os 2 diferem, a rodada do gatilho cria outra pasta de documentação, com o documento 2 copiado de novo desde M1.
   - Evidência da spec: C11, "A pasta do projeto é o `cwd` do primeiro registro … o primeiro registro dá a mesma pasta ao gatilho e à skill"; glossário, "Pasta de documentação: `<pasta do projeto>/docs-by-hopper-documentation/`"; R03 e N02.
   - Evidência do código: `projeto = evento.get("cwd")` e `"--pasta-do-projeto", projeto`.
   - Cenário C5: ficam 2 pastas, `outra-pasta/docs-by-hopper-documentation` (cópia) e `projeto/docs-by-hopper-documentation` (escrita).
   - Hipótese: a frequência depende de o `cwd` do evento acompanhar a mudança de pasta da sessão. Isso não foi verificado com o Claude Code real.
   - Gravidade: reprova R03 em parte. Contraria C11.

6. **`codigo_do_identificador`, linhas 1070 a 1073, com `migrar`, linhas 1366 a 1369: gravação fora da pasta de documentação.** Na migração, o campo `conversa` da resposta que começa com `antigo-` entra no caminho sem conferência. O documento 7 é gravado antes da verificação interna.
   - Evidência do código: `if identificador.startswith("antigo-"): return identificador`, depois `pasta.mkdir(parents=True, exist_ok=True)` e `gravar_documento_7(...)`.
   - Cenário C14 (`conversa` igual a `antigo-x/../../../../FORA`): `FORA/7-handoff.md` aparece ao lado da pasta do projeto. A verificação interna reprova depois, e o arquivo fica.
   - Gravidade: menor quanto à chance, porque exige resposta malformada ou um arquivo antigo que induza o redator. É um caminho de gravação fora das pastas permitidas (N02).

7. **`verificacao_interna`, linhas 1319 a 1345: a condição 1 confere a resposta, e não a gravação.** As origens vêm de `resposta["itens_novos"]` (linha 1324), e não dos documentos 4, 5 e 6 gravados. Uma perda de gravação passa pela verificação, e os arquivos antigos são apagados.
   - Evidência da spec: R31, "apaga os arquivos do formato antigo só depois de gravar a migração e de a verificação interna aprovar"; Anexo E, condição 1, "Cada arquivo antigo aparece como origem de pelo menos 1 item"; N06.
   - Cenário C13: verificação aprovada e exclusão feita com a 2ª decisão não gravada (achado 1). Se o item perdido fosse o único a citar um arquivo, o arquivo ainda contaria como migrado.
   - Gravidade: reprova R31 em parte. Com o achado 1, viola N06.

8. **`migrar`, linhas 1348 a 1383: a retomada de uma migração interrompida chama o redator de novo.** A execução seguinte regrava os itens a partir de uma resposta nova. A busca de item já gravado compara o texto exato, e o redator real reescreve com outras palavras, então os itens saem em dobro. A função `migracao_pendente` (linha 1395), descrita como a que refaz a verificação, não é chamada em nenhum lugar.
   - Evidência da spec: caso de borda de R31, "A rodada seguinte refaz a verificação interna e apaga os arquivos antigos que restaram"; R30.
   - Cenário C6 (2ª resposta com o texto levemente diferente): ficam D1 e D2, F1 e F2, PD1 e PD2 da mesma conversa, com 2 chamadas ao redator. T31 passa porque o redator simulado devolve o mesmo texto.
   - Gravidade: reprova o caso de borda de R31. É comportamento do redator real que o simulado não exercita (categoria d).

9. **`rodada`, linhas 1407 a 1417: a falha da migração automática encerra a rodada antes da cópia e sem o documento 1.** O `return` fica dentro do `try` externo, que é o único que grava o documento 1. Enquanto a migração falhar, a rodada a pedido não copia nem escreve nada, e cada rodada gasta 1 chamada ao redator na migração.
   - Evidência da spec: R18, "depois de toda falha de rodada, o programa reescreve o documento 1".
   - Cenário C16 (redator fora do esquema na migração): código 1, sem documento 1 e sem documento 2.
   - Gravidade: reprova R18 em parte.

10. **`rodada` e `main`, linhas 1403 a 1437 e 1543: só a exceção `Falha` é tratada.** Outra exceção encerra o processo sem linha de falha no registro de rodadas, sem documento 1 e sem o arquivo marcador. Exemplos: `OSError` ao gravar os documentos 1, 3 a 7, ou um valor inesperado na resposta. O gatilho de escrita espera 3.500 segundos (linha 1493) e informa um motivo falso.
   - Evidência da spec: R18; R24, "a falha fica no registro de rodadas e no documento 1, e a conversa recebe 1 aviso com o motivo".
   - Cenário C9 (`outputTokens` igual a "n/d"): a rodada termina com `ValueError`, o registro fica só com a linha da cópia, o documento 1 não existe, e `escrita` sai com 2 e "o redator não respondeu em 58 minutos".
   - Gravidade: reprova R18 em parte. Afeta também R24, que é de U5.

11. **Travas, linhas 778 e 1354: o gatilho de cópia espera a chamada ao redator da migração.** `migrar` segura a trava de pasta durante a chamada ao redator, e `copiar` pede a mesma trava para gravar o documento 2, com espera de 60 segundos. Durante uma migração, a cópia de qualquer conversa da pasta passa do tempo-limite de 60 segundos do gatilho (até cerca de 5 segundos da espera de C09 mais 60 segundos da trava) e registra um motivo errado.
   - Evidência da spec: C07, "A trava de pasta … cobre a gravação dos documentos 1, 4, 5 e 6" e "o gatilho de cópia nunca espera uma chamada ao redator"; R22, "termina em até 60 segundos".
   - Cenário C17 (escala 0,01): a cópia falha em 0,7 segundo, que equivale a cerca de 65 segundos reais, com o motivo "outra rodada da conversa em andamento há mais de 15 minutos".
   - Gravidade: contraria C07. O efeito é menor, porque as mensagens entram na rodada seguinte, mas R22 fica em risco durante a migração de U9.

12. **`Documento2.mensagens`, linhas 716 a 735, depois de `eae5c9e`: uma citação do formato ainda vira cabeçalho.** A correção aceita como cabeçalho qualquer linha `## M<n>-… · … · …` seguida de `<!-- registros: … -->`. Uma mensagem que cita esse par, como o exemplo do Anexo E, gera uma mensagem falsa. Se a citação está na última mensagem, a cópia seguinte usa número e âncora errados.
   - Evidência da spec: R05, "n começando em 1 e crescendo de 1 em 1"; N01 e N03.
   - Cenário C10b (citação com data anterior à conversa): os cabeçalhos ficam `M1`, `M2`, `M1-e4bad083`, `M2`, `M3`, `M1-e4bad083`, `M4`. O número M2 se repete, e a mensagem M1 é copiada 2 vezes.
   - Cenário C10 (citação com data posterior): a cópia seguinte não copia nada, grava o aviso falso e continua parada enquanto a citação for a última mensagem.
   - Gravidade: menor quanto à chance. As conversas sobre esta skill citam esse formato.

13. **`conferir_modelos`, linhas 927 a 935: sem o campo `outputTokens`, a regra dos 90% passa sem conferir.** O total fica 0, e `if total and …` aceita a resposta.
   - Evidência da spec: C04, "esse modelo responde por no mínimo 90% dos tokens de saída"; N04.
   - Cenário C8 (campo `output_tokens`, Opus com 900 e Sonnet com 1): a resposta é aceita.
   - Dado real de A3: `modelos` traz 3.096, 4.556 e 5.093 tokens de `claude-sonnet-5-5`. O nome do modelo e o campo `outputTokens` da saída real batem com o programa.
   - Gravidade: menor. É dependência do formato da saída real (categoria d).

14. **`validar_resposta`, linhas 867 a 914: a conferência própria cobre só parte do Anexo D.** O programa não confere o limite de 80 caracteres de `resumo`, os campos extras dentro dos itens, das mudanças e de `handoffs_antigos`, o tipo dos elementos de `mudancas[].origem` nem o formato de `data`. A origem das mudanças e a dos itens da migração não são conferidas, e `mensagens_validas` aceita qualquer mensagem do documento 2, e não só as do trecho novo. O resto depende da validação do `--json-schema` pelo Claude Code.
   - Evidência da spec: R12; Anexo D, "`origem` cita mensagens do trecho novo ou itens existentes" e, na migração, "a `origem` cita nomes de arquivos antigos".
   - Dado real de A3: o `structured_output` veio dentro do esquema nas 4 rodadas.
   - Gravidade: menor.

15. **`entrada_da_migracao`, linhas 1304 a 1316: a migração não oculta segredos.** Os arquivos antigos vão ao redator sem `ocultar`, e a resposta é gravada sem `ocultar`. Um segredo que a ocultação das versões antigas deixou passar pode chegar aos documentos 4 a 7.
   - Evidência da spec: N05; C13 registra que a ocultação da versão atual tem menos casos de teste.
   - Gravidade: menor.

16. **`codigo_de`, linhas 681 a 692: a colisão de códigos não entra no registro.** O fato não é registrado, e o código de 12 caracteres vai para a conversa documentada depois, e não para a mais nova.
   - Evidência da spec: caso de borda de R02, "A conversa mais nova usa como código os 12 primeiros caracteres … O fato entra no registro de rodadas".
   - Gravidade: menor. Reprova esse caso de borda.

17. **`registrar_escrita`, linhas 1158 a 1168, e `registrar_resumo`, linhas 1386 a 1393: o resumo regrava o registro de rodadas inteiro.** O programa relê o arquivo, altera a última linha e regrava tudo, sem trava e sem gravação atômica, enquanto o gatilho de cópia acrescenta linhas em outro processo. Uma linha acrescentada nesse intervalo se perde, ou o resumo cai na linha de outro processo.
   - Evidência da spec: Anexo E, registro de rodadas; C07, "os 2 comandos do gatilho rodam em paralelo".
   - Gravidade: menor, porque a janela é curta. As provas de R22 e do passo F-K dependem dessas linhas.

18. **`configuracao`, linhas 221 a 227: arquivo inválido liga a migração.** Um `config.json` com JSON inválido, ou com `"false"` em texto, liga a migração automática. Um conteúdo que não é objeto encerra o programa com exceção.
   - Evidência da spec: C23, "Sem o arquivo, ela vale verdadeiro"; N12. A spec não trata o arquivo inválido.
   - Gravidade: menor. Com N12, um arquivo corrompido em U8 liberaria a exclusão em pasta real.

Decisões de como contrariadas: C05 (achados 1 e 4), C07 (achado 11), C10 (achado 2) e C11 (achado 5).

## Observações fora dos achados

- **Critérios congelados (C18).** O commit `eae5c9e` alterou `aceite/conferir.py`, `aceite/roteiro.json`, `aceite/testes/test_copiador.py` e os 10 casos do conferidor. O congelamento ainda não aconteceu (sem `aceite/MANIFESTO.sha256` e sem a tag `criterios-congelados`), e a mudança está registrada em V-U8-02 (correção). A nova leitura do documento 2 no conferidor acompanha a do programa e não detecta a causa do achado 3.
- **Edição simultânea do programa.** Durante esta passada, a cópia de trabalho recebeu alterações não commitadas no programa em português. Elas tratam `isMeta`, o `cwd` do gatilho de escrita, a espera da trava de pasta na cópia (25 segundos), exceções genéricas em `main`, o intervalo no registro da cópia e o texto de `motivo_trava`. As alterações sumiram e voltaram junto com mudanças em outros 13 arquivos, entre eles o programa em inglês, o SKILL.md e os testes do executor. Enquanto o pacote em inglês estava desatualizado, T35 reprovou nele. Essas alterações parecem atingir os achados 3, 5, 10 e 11 em parte e não foram revisadas.
- **Redator real (categoria d).** A3 confirmou que o programa lê o envelope do `claude -p` (1 objeto JSON na última linha), o nome `claude-sonnet-5-5` em `modelUsage` e o campo `outputTokens`. A3 não exercitou o trecho acima de 300 mil caracteres, a resposta com `is_error` verdadeiro nem a migração com o redator real (U9).
- **Cenários.** Os scripts dos cenários ficam em `/private/tmp/claude-501/-Users-jonathan--claude-spares-spare-egve4x/0f5ecff8-dcad-44a9-be90-0bad629caed5/scratchpad/cenarios_head.py` e `/private/tmp/claude-501/-Users-jonathan--claude-spares-spare-egve4x/0f5ecff8-dcad-44a9-be90-0bad629caed5/scratchpad/cenarios2_head.py`, com a cópia extraída do commit em `/private/tmp/claude-501/-Users-jonathan--claude-spares-spare-egve4x/0f5ecff8-dcad-44a9-be90-0bad629caed5/scratchpad/snap-head`. A pasta é temporária da sessão do revisor.

## Situação dos requisitos de U3, U4 e U6

| Situação | Requisitos |
| --- | --- |
| Aprovados | R01, R05 (com o risco do achado 12), R06, R07 no copiador (achado 15 vale para a migração), R10, R11 (com a ressalva menor do achado 14), R13, R15, R16, R17, R27, R28, R37 e R42 (com a ressalva do achado 18) |
| Reprovados ou reprovados em parte | R02 no caso de borda da colisão (16), R03 (5, e N02 em 5 e 6), R04 (2), R08 (2 e 3), R09 (3), R12 (4), R14 (1), R18 (9 e 10), R29 (2 e 4), R30 (1 e 8) e R31 (7 e 8) |
| Não verificáveis sem o redator real ou sem os outros ambientes | R19, R20 e R21, aprovados pelo conferidor só em A3 (F7, F8 e F9, 10 de 10 depois da correção), com A1 e A2 pendentes; R30 e R31 com o redator real, que dependem de U9 |

A parte de R12 que depende do redator real (envelope e `modelUsage`) foi confirmada em A3.
