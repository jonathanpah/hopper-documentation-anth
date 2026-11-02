# Tarefa 01 para o Codex: correções da revisão de U5 e U7

Você é o executor do trabalho braçal desta execução de spec. O Claude, na sessão que abriu esta tarefa, verifica o seu trabalho, faz o commit e cuida da instalação nos ambientes. Decisão do proprietário em `execucao/decisoes.md`, D-16.

## Contexto em 5 linhas

- Repositório `hopper-documentation-anth`, branch `versao-2`, na pasta atual. A spec é `SPEC.md`; o estado da execução está em `execucao/estado.md`.
- O plugin tem 2 pacotes: `hopper-documentation-anth-pt-br/` e `hopper-documentation-anth-en/`. O programa é `scripts/hopper_documentation_anth.py`, igual nos 2 exceto a linha `LANGUAGE`.
- Os testes de aceite ficam em `aceite/testes/` e passam hoje (32 de 32 em cada pacote).
- A revisão independente de U5 e U7 está em `execucao/revisoes/U5-U7-passada-1.md`. Leia os achados citados abaixo nela.
- Responda e escreva em português brasileiro.

## O que corrigir

Edite só o pacote em português e, no fim, regenere o programa em inglês com:

```sh
sed 's/^LANGUAGE = "pt-br"$/LANGUAGE = "en"/' hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py > hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

Textos que existem nos 2 idiomas (SKILL.md, README, graders das avaliações, textos fixos do programa) mudam nos 2, com tradução fiel.

1. **Achado 3.** `comando_escrita` não passa mais `--pasta-do-projeto` ao processo separado. A pasta do projeto vem do 1º registro do histórico que traz `cwd` (glossário da spec e C11), igual ao gatilho de cópia e à skill.
2. **Achado 4.** No registro de rodadas, a linha `inicio-compactacao` grava `motivo` vazio e o `trigger` do evento em um campo extra `trigger`. As linhas `copia` gravam em `intervalo` o intervalo das mensagens copiadas (`M<a>-<código> a M<b>-<código>`), ou vazio quando nada foi copiado.
3. **Achado 5.** A soma das esperas do comando `copia` fica abaixo de 60 segundos: trava de cópia 20 s, espera do histórico 5 s (C09) e trava de pasta no máximo 25 s quando o chamador é o gatilho de cópia.
4. **Achado 6.** O motivo de falha de trava diz o tempo real esperado, por exemplo "outra rodada da conversa ou da pasta em andamento; a espera de 20 segundos acabou". Nos 2 idiomas.
5. **Achado 7.** Em `main`, o comando `rodada` captura qualquer exceção: grava a falha no registro de rodadas, grava o marcador com código 1 e a linha de falha, imprime a linha e sai com 1.
6. **Fora do escopo 1 (R09).** O copiador ignora registros do usuário com `isMeta` verdadeiro (o Claude Code injeta assim o texto de uma skill carregada, com "Base directory for this skill: …").
7. **Fora do escopo 3.** Quando a conversa ainda não tem mensagens, a linha final não cita "M0". Use, por exemplo, "Documentação: nada novo." nos 2 idiomas.
8. **Achado 8.** Os 2 SKILL.md dizem que a migração automática acontece na 1ª rodada "quando a configuração `migracao_automatica` está ligada, como no padrão".
9. **Achado 9.** O SECURITY.md da raiz e o do pacote em português registram a exceção de R03: o próprio Claude Code grava os arquivos dele na pasta de configuração quando o redator roda.
10. **Achado 10 e D-15.** As 2 listas "Prevenções conhecidas" (CONTRIBUTING da raiz e do pacote em português) ganham 2 itens: `claude plugin uninstall` sem `--keep-data` apaga a pasta de dados e o `config.json` (D-14); com a mesma versão, `claude plugin update` não atualiza a cópia instalada, e a atualização é `uninstall --keep-data` seguido de `install` (D-15). Os 2 README dos pacotes trocam a frase de atualização por esse procedimento.
11. **Achado 11.** Os graders `evals/registra-pedido/graders/relato-fiel.md` (pt-br) e `evals/record-request/graders/faithful-report.md` (en) descrevem a versão 2: o programa grava 7 documentos e imprime "Documentação concluída: …", "Documentação: nada novo …" ou "Documentação falhou: …". O critério de aprovação continua o mesmo.

Para cada correção de código (itens 1 a 7), acrescente em `hopper-documentation-anth-pt-br/tests/test_hopper_documentation_anth.py` um teste do executor que falha sem a correção e passa com ela. Copie o arquivo de testes para o pacote em inglês no fim.

## O que você não pode fazer

- Alterar `SPEC.md`, `aceite/`, `.github/`, `.claude/` ou `execucao/`, exceto o relatório abaixo.
- Fazer commit, push, merge ou qualquer comando `git` que grave. Deixe as mudanças no disco; o Claude confere e faz o commit.
- Acessar a VPS, instalar plugins ou rodar `claude -p`.

## Como verificar antes de entregar

Rode e deixe a saída no relatório:

```sh
cd aceite/testes && for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do HOPPER_DOCUMENTATION_ANTH_PACOTE=$p TZ=UTC python3 -m unittest discover -s . -p 'test_*.py' 2>&1 | tail -3; done; cd ../..
for p in hopper-documentation-anth-pt-br hopper-documentation-anth-en; do (cd $p && python3 -m unittest discover -s tests 2>&1 | tail -3); done
diff hopper-documentation-anth-pt-br/scripts/hopper_documentation_anth.py hopper-documentation-anth-en/scripts/hopper_documentation_anth.py
```

O trabalho termina quando os testes de aceite passam nos 2 pacotes, os testes do executor passam (com os novos), e o `diff` mostra só a linha `LANGUAGE`.

## Relatório

Grave `execucao/codex/tarefa-01-relatorio.md` com: o que mudou em cada item (arquivo e função), os testes novos, a saída dos 3 comandos acima e o que ficou sem fazer, com o motivo.
