# hopper-documentation-anth

[English](../hopper-documentation-anth-en/README.md) | **Português (Brasil)**

Um plugin do Claude Code que registra a conversa em **handoffs**: arquivos Markdown que dizem a quem não viu a conversa onde o trabalho está, o que foi decidido e como continuar. Outra pessoa, outra sessão do Claude ou outra IA retoma o trabalho lendo o handoff mais recente e conferindo o estado real, sem abrir a conversa.

## Como funciona

O registro acontece em dois momentos:

- **A pedido:** quando você pede para documentar ou registrar a conversa, a skill roda o programa do plugin em segundo plano, e você continua trabalhando.
- **Antes de cada compactação:** um gatilho (hook `PreCompact`) roda o mesmo programa em segundo plano, manual ou automático. Se ele falhar, a conversa é avisada; a compactação não é afetada.

O programa faz o trabalho mecânico e deixa ao modelo só a escrita:

1. lê as mensagens novas da conversa desde o último handoff pela biblioteca oficial da Anthropic, o Agent SDK, sem depender do formato interno dos arquivos de conversa;
2. mantém só as mensagens do usuário, as respostas do assistente, as respostas a perguntas e os planos aprovados, e oculta senhas, tokens e chaves;
3. pede ao Claude Sonnet 5.5, com esforço medium e sem ferramentas, que escreva o conteúdo seguindo as regras do redator; se o Claude Code usar outro modelo, nada é gravado;
4. confere, letra por letra, cada trecho que o handoff cita entre aspas; se um deles não estiver na conversa, pede a correção uma vez e, se continuar errado, não grava nada. Frases que atribuem fala ou autorização ao usuário sem citá-lo também recebem uma segunda chance; se persistirem, o handoff as lista em Lacunas como interpretação do redator;
5. grava o handoff sem nunca sobrescrever um arquivo, sob uma trava que impede duas gravações ao mesmo tempo na mesma pasta, e refaz o índice.

Conversas muito longas são divididas em partes, cada uma num handoff que continua o anterior. Quando não há nada novo, o programa não chama o modelo.

## O que ele grava

Na raiz do diretório de trabalho, a pasta `docs-by-hopper-documentation/` recebe:

- `handoff-AAAAMMDD-HHMMSS-<conversa>.md`, um arquivo por registro, nunca alterado depois de gravado;
- `index.md`, com todos os handoffs da pasta, inclusive os de outros formatos, do mais recente ao mais antigo.

Cada handoff tem um cabeçalho (data com fuso, conversa, diretório, handoff anterior, acionamento, modelo e esforço usados e a última mensagem registrada) e nove seções: objetivo, pautas e estado atual, próximo passo, decisões e autorizações, restrições vigentes, descobertas e tentativas descartadas, pendências e compromissos, lacunas e como retomar.

## O que ele roda, envia e busca

- **Roda:** `python3` com o programa do plugin; o executável do próprio Claude Code, em modo não interativo, sem ferramentas e sem carregar plugins, para escrever o conteúdo; `git` só para ler o estado do diretório.
- **Envia:** as mensagens novas da conversa, com segredos ocultados, ao Claude Sonnet 5.5, pela sua conta do Claude.
- **Busca:** na primeira execução, instala o Agent SDK (`claude-agent-sdk`, versão fixa) do PyPI num ambiente Python próprio, na pasta de dados do plugin (`${CLAUDE_PLUGIN_DATA}`), com cerca de 55 MB.
- **Grava:** só na pasta de handoffs e na pasta de dados do plugin, onde ficam o ambiente Python, as travas e um registro de execuções.

## Requisitos

- Claude Code, na CLI ou no aplicativo, em macOS ou Linux.
- Python 3.9 ou mais novo para o programa, e Python 3.10 ou mais novo, com o módulo `venv`, para a biblioteca da Anthropic. O programa procura sozinho um Python 3.10 ou mais novo: o do sistema, um `python3.1x` no PATH ou em `~/.local/bin`, o do Homebrew ou o do instalador do python.org. Em Debian e Ubuntu, o módulo `venv` exige o pacote `python3-venv` (por exemplo, `python3.13-venv`). O macOS traz só o Python 3.9; instale um mais novo antes.
- Acesso ao PyPI na primeira execução.

## Modelo

Quem escreve é sempre o Claude Sonnet 5.5 com esforço medium. Não há opção para trocar. Se esse modelo não estiver disponível, o registro informa o impedimento e não usa outro.

## Instalação

O plugin e a skill se chamam `hopper-documentation-anth` nos dois idiomas. Escolha um idioma só. A pasta `hopper-documentation-anth-pt-br/` contém o plugin completo em português: a skill, o programa, o gatilho e os testes.

Clone o repositório uma vez:

```sh
mkdir -p "$HOME/.local/share"
git clone https://github.com/jonathanpah/hopper-documentation-anth.git "$HOME/.local/share/hopper-documentation-anth"
```

Se o destino já existir, confira sua origem e alterações locais antes de atualizá-lo.

No Claude Code:

```sh
claude plugin marketplace add "$HOME/.local/share/hopper-documentation-anth/hopper-documentation-anth-pt-br"
claude plugin install hopper-documentation-anth@hopper-documentation-anth
```

Numa sessão já aberta, envie `/reload-plugins` como mensagem separada. Confira com `claude plugin details hopper-documentation-anth@hopper-documentation-anth`: a skill e o gatilho devem aparecer. A instalação pela CLI não comprova presença no aplicativo: no aplicativo do Claude, confira **Personalização → Plugins → Meus** e **Habilidades → Meus**.

O identificador completo da skill é `hopper-documentation-anth:hopper-documentation-anth`: o primeiro trecho identifica o plugin, e o segundo, a skill.

## Uso

Peça em linguagem natural, por exemplo "documente esta conversa" ou "registre o que fizemos para eu continuar amanhã", ou acione `/hopper-documentation-anth:hopper-documentation-anth`. Explicar, revisar ou editar a skill não grava nada.

Para retomar numa sessão nova, peça ao Claude que leia o `index.md` da pasta e o handoff mais recente da conversa e siga a seção "Como retomar".

## Limites

- O handoff é escrito a partir das mensagens de texto da conversa, não das saídas de ferramentas. Um resultado que só apareceu na saída de um comando entra como relato do assistente, e o handoff diz isso. O estado do git no momento do registro é lido pelo programa.
- O Agent SDK lê a conversa desde a última compactação. O registro antes da compactação guarda o trecho que seria resumido; depois dela, o handoff seguinte parte do anterior e registra a limitação.
- A ocultação cobre formatos comuns de credenciais, não todos os segredos possíveis.
- Os modelos não são determinísticos. A conferência das citações prova que cada fala citada existe, não que o texto escrito a partir dela seja fiel.
- Um handoff é um registro histórico. Ele não substitui a conferência do estado real nem autoriza repetir operações concluídas.
- Não há suporte ao Windows.

## Testes

```sh
python3 -m unittest discover -s tests
```

Os testes não chamam modelo nem instalam nada. A suíte de comportamento fica em `evals/` e roda com a avaliação oficial do Claude Code, que chama modelos pela sua conta:

```sh
claude plugin eval . --allow-tools Write Edit Bash
```

## Atualizações e remoção

Confira as alterações locais e atualize o clone com `git pull --ff-only`. Depois, execute `claude plugin marketplace update hopper-documentation-anth` e `claude plugin update hopper-documentation-anth@hopper-documentation-anth`, e envie `/reload-plugins` nas sessões abertas.

Para remover, use `claude plugin uninstall hopper-documentation-anth@hopper-documentation-anth`. Os handoffs gravados nos projetos permanecem.

## Contribuição

Para suspeitas de vulnerabilidade, siga a [Política de Segurança](SECURITY.md) e relate de forma privada. Use [Issues](https://github.com/jonathanpah/hopper-documentation-anth/issues) para problemas reproduzíveis e propostas concretas, e [Discussions](https://github.com/jonathanpah/hopper-documentation-anth/discussions) para dúvidas e ideias. Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e o [Código de Conduta](CODE_OF_CONDUCT.md).

## Licença e mantenedor

Copyright (c) 2026 Jonathan Honorio. Publicado sob a [Licença MIT](LICENSE).

Mantido por [Jonathan Honorio (@jonathanpah)](https://github.com/jonathanpah). Este é um projeto independente, sem alegação de vínculo ou endosso da Anthropic.
