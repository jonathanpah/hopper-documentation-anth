# Tarefa 04 para o Codex: roteiro de aceite em A1 e A3 e avaliações de acionamento (U8)

**Alcance revisto (D-22): esta tarefa cobre só A3.** O isolamento do Codex não lê o Chaves do macOS, onde fica o login do Claude Code do Terminal, então A1 e as avaliações rodam pelo verificador, no painel de Terminal. Ignore abaixo o que fala de A1 e das avaliações.

Você roda os testes reais da versão 2.0.0, já instalada pelo verificador nas 3 contas a partir do commit congelado `e737aca` (critérios congelados, tag `criterios-congelados`). Nesta tarefa você tem rede (para o SSH) e pode gravar também em `~/hopper-sonda`. Leia antes: `SPEC.md`, Anexo F (passos F-C, F-A, F-K e F-V) e decisão C27; `execucao/decisoes.md`, D-10, D-11, D-14, D-15, D-17 e D-18; `execucao/verificacoes.md`, V-U1-05 (calibração) e V-U8-02.

## Ambientes

- **A3:** VPS `hopper`, conta `jpah`, por `ssh -o BatchMode=yes hopper-jpah`. Claude Code em `~/.local/bin/claude`.
- **A1:** Terminal do MacBook, conta `jonathan`, no seu próprio shell (o Claude Code do Terminal tem login; confira com `claude auth status`).
- A2 (app) fica com o verificador.

## Passos, em cada ambiente

1. Confira que `~/.claude/plugins/data/hopper-documentation-anth-hopper-documentation-anth/config.json` tem `{"migracao_automatica": false}`. Se não tiver, pare e relate (N12).
2. Copie o condutor `~/hopper-sonda/roteiro.py` e `~/hopper-sonda/driver.py` e o roteiro `aceite/roteiro.json` para `~/hopper-sonda/` da VPS (em A1, já estão no lugar).
3. Meça o contexto inicial de uma sessão nova, com `driver.py --modo medir` em uma pasta nova (`~/hopper-teste-a1-medir` ou `~/hopper-teste-a3-medir`). Calcule o percentual pela regra de V-U1-05: `percentual = teto((contexto inicial + 6000) / 765)`, no máximo 100.
4. Rode o roteiro com `roteiro.py --pasta <pasta nova> --roteiro <roteiro.json> --pct <percentual> --modelo sonnet` em uma pasta nova: `~/hopper-teste-a1` em A1 e `~/hopper-teste-a3-2` em A3 (a `~/hopper-teste-a3` do 1º aceite fica como está). Em A3, use `--claude ~/.local/bin/claude`.
5. Ao fim, copie para o repositório, em `execucao/aceite/a1/` e `execucao/aceite/a3-2/`: a pasta `docs-by-hopper-documentation` gerada, o JSON de saída do roteiro e as linhas do `rodadas.jsonl` da conversa de teste.
6. Rode o conferidor com o roteiro na pasta copiada: `python3 aceite/conferir.py <pasta> --idioma pt-br --roteiro aceite/roteiro.json`.
7. Confira e registre no relatório, com as linhas do registro de rodadas e do histórico como evidência:
   - R22: em cada compactação, a linha `copia` do gatilho de cópia terminou antes do 1º registro `api-request` do histórico posterior ao início da compactação (marco de D-11).
   - R23: na 2ª passagem de F-K, a linha `escrita` `concluída` do gatilho de escrita tem data posterior ao fechamento do Claude Code.
   - R25: depois da mensagem 6, a resposta do Claude informa a linha final do programa ou diz que a documentação começou em segundo plano.
   - R39 em A1 e A3: saída de `claude plugin list`, de `claude plugin details hopper-documentation-anth@hopper-documentation-anth` e a lista de hooks com os 2 comandos (pelo `/hooks` na sessão do roteiro, ou pelo `hooks.json` instalado no cache, citando de onde veio).
8. Confira de novo o `config.json` (passo 1) depois do roteiro.

## Avaliações de acionamento (R25 e R26)

Rode 1 execução completa por pacote, no MacBook, com `claude plugin eval ./<pacote> --ablation none --trust-plugin --model sonnet --output-dir execucao/avaliacoes/u8-<pacote>`. Cada pacote conta 1 das 3 execuções completas de C20. Relate os casos reprovados e as notas por caso.

## O que você não pode fazer

- Alterar `SPEC.md`, `aceite/`, `.github/`, `.claude/`, o programa, as skills ou qualquer arquivo dos pacotes. Se o aceite revelar um defeito, pare aquela parte e relate com a evidência: o verificador decide a correção.
- Gravar em `execucao/` fora de `execucao/aceite/a1/`, `execucao/aceite/a3-2/`, `execucao/avaliacoes/u8-*` e do relatório.
- Qualquer comando `git` que grave, desinstalar ou instalar plugins, rodar o comando `migrar`, mudar o `config.json`, apagar arquivos fora das pastas de teste que você criar, ou rodar comandos com `sudo` na VPS.

## Limites

No máximo 2 tentativas por ambiente. O roteiro faz cerca de 5 chamadas reais ao redator por ambiente.

## Relatório

`execucao/codex/tarefa-04-relatorio.md`: o percentual usado e o contexto medido em cada ambiente, o resultado do conferidor, as 4 conferências do passo 7 com as evidências, as avaliações, e o que ficou sem fazer, com o motivo.
