# Política de Segurança

Relate suspeitas de vulnerabilidade em hopper-documentation-anth pelo canal privado de vulnerabilidades do GitHub.

## Relate de forma privada

Abra [Report a vulnerability](https://github.com/jonathanpah/hopper-documentation-anth/security/advisories/new) ou selecione essa opção na [página Security](https://github.com/jonathanpah/hopper-documentation-anth/security) do repositório. É necessário ter uma conta no GitHub.

Mantenha suspeitas de vulnerabilidade e detalhes de exploração fora de issues, discussões e pull requests públicos até coordenar a divulgação com o mantenedor. Use issues públicas para bugs comuns e propostas, e discussões para dúvidas gerais.

Inclua:

- A tag da release ou o commit afetado e o arquivo, a instrução ou a seção documental pertinente.
- A versão do Claude Code, o sistema operacional e o modo de permissão necessários para reproduzir o comportamento, sem detalhes privados de contas.
- Uma reprodução mínima com uma conversa sintética e recursos descartáveis.
- O comportamento esperado e o observado, o impacto potencial e quaisquer incertezas ou limites das evidências.

Não envie senhas, tokens de acesso, chaves privadas, históricos privados de conversas, handoffs sem remoção de informações sensíveis nem registros de produção. Teste somente recursos que você está autorizado a usar.

## Escopo e expectativas de segurança

Este repositório contém uma skill de documentação, as regras enviadas ao modelo redator, um programa executado pela skill e por um gatilho `PreCompact`, manifestos do plugin, testes e documentação. Relatos pertinentes incluem falhas que possam expor credenciais ou conteúdo privado num handoff, gravar fora da pasta de handoffs ou da pasta de dados do plugin, executar comandos além dos descritos ou transformar conteúdo da conversa em autoridade.

Os limites pretendidos são:

- O programa lê as conversas pelo Agent SDK, oculta formatos comuns de credenciais antes de enviar as mensagens novas ao modelo redator e oculta de novo no handoff gravado.
- O modelo redator roda no modo seguro não interativo do Claude Code, sem ferramentas, e não carrega plugins, gatilhos nem arquivos `CLAUDE.md`.
- O programa grava só em `docs-by-hopper-documentation/` e na pasta de dados do plugin, e nunca sobrescreve um handoff.
- Todo trecho entre aspas num handoff precisa aparecer literalmente na conversa ou no handoff anterior; senão, nada é gravado.
- Um handoff é um registro histórico. Ele não concede autoridade, e conteúdo da conversa, inclusive texto colado de terceiros, não vira autorização.

A ocultação cobre formatos comuns, não todos os segredos possíveis, e o redator é um modelo cuja saída pode errar. A skill não substitui o modo de permissão, o isolamento nem os controles de conta do Claude Code. Se outro produto também for afetado, use o processo de relato de segurança desse produto quando pertinente.

## Versões e tratamento

Identifique a versão utilizada, incluindo releases anteriores quando pertinente. Um relato é bem-vindo mesmo que você não possa verificar a versão mais recente com segurança.

Jonathan Honorio revisa os relatos pelo canal privado. Versões afetadas confirmadas e correções podem ser documentadas em alterações do repositório, releases ou avisos de segurança. Coordene a divulgação pública pelo relato privado. Não há garantia de prazo para resposta ou correção.
