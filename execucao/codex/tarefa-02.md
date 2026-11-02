# Tarefa 02 para o Codex: correções da revisão de U3, U4 e U6

Mesmas regras, contexto e verificação da tarefa 01 (`execucao/codex/tarefa-01.md`): edite só o pacote em português, regenere o programa em inglês com o `sed` da tarefa 01, não altere `SPEC.md`, `aceite/`, `.github/`, `.claude/` nem `execucao/` (exceto o relatório), não faça nada com `git` que grave, não acesse a rede.

A revisão está em `execucao/revisoes/U3-U4-U6-passada-1.md`. Leia cada achado citado lá antes de corrigir. Alguns já podem estar resolvidos pela tarefa 01 (achados 3, 5, 10 e parte do 11); confira e diga no relatório.

## Correções, com a decisão de como já tomada pelo verificador

1. **Achado 1 (numeração).** Em `gravar_itens`, reserve os números em ordem, por tipo e código, com um contador que começa em `proximo_numero` e sobe a cada item novo, para que 2 itens do mesmo tipo recebam números diferentes.
2. **Achados 1, 4 e 8 (repetição sem efeito duplo, R29).** O diário de uma rodada e o de uma migração guardam, antes de qualquer gravação nos documentos, a resposta validada e o mapa `N<n>` → identificador final. A reaplicação usa o mapa guardado e pula um item cujo identificador já existe no documento; não compare texto. A migração passa a ter diário também (por pasta do projeto), e uma migração interrompida é concluída pela execução seguinte com o diário, sem chamar o redator de novo. Apague `migracao_pendente` se ficar sem uso.
3. **Achado 2 (C10).** A cópia seguinte começa no registro bruto que vem depois do registro cujo `uuid` é o último identificador da última mensagem gravada. Extraia as mensagens só dos registros depois desse ponto. Uma continuação da última fala do Claude vira uma mensagem nova (só acréscimos, N01). O caminho por data só vale quando o identificador sumiu do histórico, e compara a data e hora completas dos registros com a do último registro gravado (guarde-a no comentário de registros só se o formato do Anexo E permitir; senão, use o minuto do cabeçalho e registre o aviso).
4. **Achado 4 (validação antes de gravar).** `validar_resposta` confere também as mudanças antes de qualquer gravação: o identificador existe na pasta (senão vai para a lista de inexistentes, como hoje), e a situação é permitida para o tipo dele. Resposta inválida não grava nada e não deixa diário (caso de borda de R12).
5. **Achado 6 (N02).** O código de uma conversa antiga aceita só letras, dígitos e hífen. Qualquer outro caractere reprova a resposta de migração antes de gravar.
6. **Achado 7 (R31).** A verificação interna confere os documentos gravados (origens nos documentos 4, 5 e 6 e o documento 7 de cada conversa antiga no disco), e não a resposta.
7. **Achado 9 (R18).** Quando a migração automática falha dentro de uma rodada, a rodada registra a falha, continua com a cópia e a escrita, e grava o documento 1. A linha final informa as 2 coisas.
8. **Achado 10.** Dentro de `rodada`, qualquer exceção (não só `Falha`) registra a falha e grava o documento 1, como `Falha`.
9. **Achado 11 (C07).** A migração segura a trava de pasta só durante as gravações, e não durante a chamada ao redator.
10. **Achado 12.** Um cabeçalho do documento 2 só conta quando o número é o seguinte ao anterior (o 1º é M1) e o código é o da conversa, além do comentário de registros na linha seguinte.
11. **Achado 13 (C04).** `conferir_modelos` aceita `outputTokens` e `output_tokens`. Sem nenhuma contagem de tokens de saída, a resposta é rejeitada.
12. **Achado 14.** `validar_resposta` passa a conferir: `resumo` com até 80 caracteres; campos extras dentro dos itens, das mudanças e de `handoffs_antigos`; elementos de `mudancas[].origem` como texto; `data` no formato `AAAA-MM-DD`; origens das mudanças; origens da rodada só com mensagens do trecho novo, itens existentes ou `N<n>`; origens da migração só com nomes de arquivos antigos.
13. **Achado 15 (N05).** A migração aplica `ocultar` ao texto dos arquivos antigos antes de enviar e a cada campo de texto da resposta antes de gravar.
14. **Achado 16.** A colisão de códigos entra no registro de rodadas, em uma linha com o motivo. Mantenha a regra atual de qual conversa recebe o código de 12 caracteres e diga no relatório que o caso "a mais nova" não é tratado quando a mais antiga é documentada depois.
15. **Achado 17.** O resumo da rodada entra na própria linha de `registrar` (parâmetro opcional), e o programa nunca regrava o registro de rodadas inteiro. Apague `registrar_resumo` e a regravação em `registrar_escrita`.
16. **Achado 18 (N12).** Um `config.json` que não é um objeto JSON válido com `migracao_automatica` booleano vale como `migracao_automatica` falsa, e o fato entra no registro de rodadas.

Cada correção de código ganha 1 teste do executor em `hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py`, que falha sem a correção. Os cenários do revisor estão descritos no próprio relatório da revisão.

## Relatório

Grave `execucao/codex/tarefa-02-relatorio.md`, no mesmo formato da tarefa 01.

## Parte 2: correções dos critérios (revisão de U2)

Nesta tarefa, e só nela, você pode alterar `aceite/` e `.github/workflows/verificar.yml`, porque os critérios ainda não foram congelados. Não crie `aceite/MANIFESTO.sha256` nem tags: isso é do verificador. A revisão está em `execucao/revisoes/U2-passada-1.md`; as decisões de critério estão em `execucao/decisoes.md`, D-13 e D-18. Cada expectativa vem da spec (G04), e não do programa.

1. **Achado 1.** `apoio.resposta()` traduz também `**Assunto: ` para `**Subject: ` em `conversa_simplificada`. No programa, aplique D-18 (h): rejeitar a resposta sem a linha de assunto e não criá-la a partir do `resumo`.
2. **Achado 2.** A 3ª rodada de T14 usa uma resposta montada no teste, com M8 no lugar de M7.
3. **Achado 3.** O passo de critérios congelados do fluxo compara também a lista de `git ls-files aceite .github/workflows/verificar.yml SPEC.md` (sem o manifesto) com os caminhos do manifesto e falha com "CRITÉRIO ALTERADO" quando diferem.
4. **Achado 4.** O conferidor reconhece cabeçalho de mensagem pelo padrão completo `RE_MENSAGEM` e reprova em F2 o cabeçalho sem o comentário de registros na linha seguinte. Acrescente um caso `invalida-` que prove isso (por exemplo, `invalida-F2-sem-registros`) e ajuste o laço do fluxo, que hoje tira o número do nome da pasta.
5. **Achado 5.** T11 ganha o caso de borda de 300 mil caracteres: 4 mensagens de 100 mil caracteres, 2 chamadas ou mais ao redator, em ordem, nenhuma mensagem dividida e 1 bloco do documento 3 por chamada.
6. **Achados 6 a 13, 15 e 16.** Faça as correções que a revisão recomenda em cada um. Em T38 (achado 10), o teste precisa passar nos executores Ubuntu e macOS do GitHub: no Linux, `/proc/<pid>/exe` resolve links simbólicos, então use uma cópia do binário no Linux e um link simbólico no macOS (uma cópia de binário do sistema é morta no macOS), e ponha sempre o candidato seguinte apontando para outro programa. Em T02 (achado 13), acrescente o caso com `TZ=America/Sao_Paulo`.
7. **Achado 17.** F5 confere as 9 seções em ordem e aceita outras linhas `## ` entre elas. F7 tira da contagem só as linhas `- <rótulo>: ` com os rótulos do Anexo E e aplica D-18 (g).
8. **Achado 18.** Escreva à mão a pasta `aceite/casos/conferidor/valida-roteiro/`, com as 6 mensagens do passo F-C no documento 2 (a 2ª como gravada, com a senha oculta) e itens D, F e PD com as origens que F-A exige, e a pasta `invalida-F9/`. O fluxo roda as 2 com `--roteiro aceite/roteiro.json`.
9. **Achado 19.** `if: always()` no passo "Testes do executor".
10. **Achado 20 (G04).** Depois de tudo, rode os testes de aceite finais contra o código da versão atual, commit `8dbb40b` (extraia com `git archive 8dbb40b | tar -x -C /tmp/versao-atual` e copie para lá a pasta `aceite/` atual), e o teste novo de T05 contra o programa do commit `7bcdf5d`. Grave as saídas brutas em `execucao/avaliacoes/u2/aceite-versao-atual-final-pt-br.log` e `execucao/avaliacoes/u2/t05-antes-da-correcao.log` (essas 2 gravações em `execucao/` são permitidas).

## Parte 3: condutor do roteiro de aceite (fora do repositório)

O condutor fica em `~/hopper-sonda/roteiro.py` e `~/hopper-sonda/driver.py` (você tem permissão de gravar nessa pasta nesta tarefa). Revisão U5-U7, achados 15 e 16: a espera pela rodada a pedido deve aceitar só um registro `pedido` `escrita` com `data` posterior ao envio da mensagem 6, e a espera da passagem 2 só um registro `gatilho-escrita` `escrita` com `data` posterior ao início da 2ª compactação. Teste por leitura de código e por um teste rápido com um `rodadas.jsonl` falso, sem abrir o Claude Code.

## Verificação final

Os mesmos 3 comandos da tarefa 01, mais o conferidor em todas as pastas de `aceite/casos/conferidor/` (com `--roteiro` em `valida-roteiro` e `invalida-F9`). Tudo no relatório.
