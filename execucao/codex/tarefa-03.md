# Tarefa 03 para o Codex: 2 testes de aceite que falham nos executores do GitHub

Mesmas regras da tarefa 01, com uma exceção: nesta tarefa você pode alterar `aceite/testes/test_repositorio.py` e `aceite/testes/test_copiador.py` (os critérios ainda não estão congelados). Não altere o programa.

A verificação do GitHub do commit `55ac502` (execução mais recente da branch `versao-2`) reprovou em 2 testes. Os 2 passam na máquina do verificador. Leia a saída com `gh` não é possível sem rede; os dados estão abaixo.

1. **T38, `test_R38_encontra_o_executavel_do_claude_code`, Ubuntu (Python 3.9 e 3.13).** Cenário "CLAUDE_PID antes do PATH": `AssertionError: PosixPath('/usr/bin/gnutrue') != PosixPath('/tmp/claude-falso-…/claude-pid')`. Causa provável: no Ubuntu do GitHub, `sleep` e `true` são links para um binário único (multicall) que escolhe o utilitário pelo nome com que foi chamado; a cópia chamada `claude-pid` não reconhece o próprio nome e sai na hora, então o PID não existe mais e o programa cai no candidato do `PATH`. Correção: no Linux, o processo de `CLAUDE_PID` é o próprio interpretador (`sys.executable`, rodando `import time; time.sleep(30)`), e o resultado esperado é `Path(sys.executable).resolve()`; no macOS, mantenha o link simbólico, que já passa. Os candidatos seguintes (`PATH` e `~/.local/bin/claude`) precisam continuar distinguíveis do esperado em cada cenário.
2. **T04, `test_R04_espera_o_arquivo_de_historico_parar_de_crescer`, macOS com Python 3.13.** O documento 2 terminou em "acréscimo 10", sem o "acréscimo 11". Causa provável: no executor lento, o teto de 5 s × escala da espera de C09 terminou antes do último acréscimo. Correção: use uma escala que deixe o teto bem acima da duração dos acréscimos (por exemplo, `escala="0.5"`, teto de 2,5 s, com os acréscimos durante cerca de 0,6 s) e mantenha a exigência do último acréscimo no documento 2.

## Verificação

Os 3 comandos da tarefa 01. Rode também `python3 -m unittest test_repositorio.Localizacao.test_R38_encontra_o_executavel_do_claude_code test_copiador.Copiador.test_R04_espera_o_arquivo_de_historico_parar_de_crescer` 5 vezes seguidas, em `aceite/testes`, e mostre que passa nas 5. Relatório em `execucao/codex/tarefa-03-relatorio.md`.
