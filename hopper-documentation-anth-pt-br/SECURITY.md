# Segurança

## O que o plugin faz com os seus dados

- Ele lê o histórico do Claude Code da conversa atual e grava arquivos Markdown dentro da pasta `docs-by-hopper-documentation/` do projeto e da pasta de dados do plugin (`~/.claude/plugins/data/hopper-documentation-anth-hopper-documentation-anth/`). Não grava em nenhum outro lugar, exceto os arquivos que o próprio Claude Code grava na pasta de configuração quando o redator roda.
- Senhas, tokens, chaves e códigos de acesso viram `[oculto]` na conversa integral antes de qualquer envio ao redator ou gravação em disco. As regras de ocultação são testadas contra os casos de `aceite/casos/b2/`.
- O redator (Claude Sonnet 5.5) roda sem janela, em modo seguro, sem ferramentas, plugins, gatilhos, servidores MCP ou arquivos `CLAUDE.md`. Ele recebe só o trecho novo, os documentos atuais, as regras de escrita e os modelos, e devolve um objeto JSON que o programa valida antes de gravar.
- O programa aceita uma resposta só quando o Claude Sonnet 5.5 produziu no mínimo 90% dos tokens de saída dela.
- Resultados de ferramentas, raciocínio interno, lembretes do sistema e saídas de gatilhos nunca entram nos documentos.

## Do que ele não protege

- Segredos escritos em uma forma que as regras de ocultação não reconhecem. Revise o documento 2 antes de compartilhá-lo.
- Segredos na saída do redator que vieram do texto da conversa em forma não reconhecida.

## Relatar uma vulnerabilidade

Abra um aviso de segurança privado no GitHub ou uma issue sem o conteúdo sensível. Inclua a versão do plugin (`claude plugin details hopper-documentation-anth@hopper-documentation-anth`), a versão do Claude Code e as linhas de `rodadas.jsonl` envolvidas.
