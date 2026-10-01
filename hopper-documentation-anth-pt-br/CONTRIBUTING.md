# Contribuindo com hopper-documentation-anth

Contribuições podem melhorar as regras do redator, encontrar falhas no registro, verificar o comportamento no Claude Code ou melhorar a documentação. A documentação fica em inglês em `hopper-documentation-anth-en/` e em português brasileiro em `hopper-documentation-anth-pt-br/`. As políticas e os modelos compartilhados do GitHub permanecem na raiz do repositório. Cada pasta de idioma é um plugin completo: a skill, as regras do redator, o exemplo, o programa, o gatilho, os testes e a suíte de avaliação. Mantenha as duas versões equivalentes; cada release inclui os dois idiomas.

## Comece pelo problema

Para suspeitas de vulnerabilidade, siga a [Política de Segurança](SECURITY.md) e relate de forma privada. Não inclua detalhes sensíveis de segurança em issues, discussões ou pull requests públicos antes de coordenar a divulgação.

Use um relato de bug para uma falha reproduzível e uma proposta para uma alteração específica. Use [Discussions](https://github.com/jonathanpah/hopper-documentation-anth/discussions) para dúvidas ou ideias iniciais. Pesquise as issues existentes antes de abrir outro relato sobre o mesmo comportamento.

Para mudanças nas regras do registro ou no que o programa lê, envia ou grava, explique o comportamento atual, o problema que ele causa, o comportamento desejado, as evidências e as consequências das alternativas. Uma proposta não é aprovação para alterar o desenho do projeto. Pequenas correções documentais podem ir diretamente para um pull request.

## Preserve o desenho da skill

- O programa faz o trabalho mecânico, e o modelo só escreve o conteúdo. Mantenha no programa a leitura, a ocultação de segredos, a conferência das citações, os nomes, a trava, a gravação e o índice.
- Leia as conversas só pelo Agent SDK da Anthropic. Não leia diretamente os arquivos internos de conversa do Claude Code.
- O redator é fixo: Claude Sonnet 5.5 com esforço medium, e nada é gravado se o Claude Code usar outro modelo. Mudá-lo é uma mudança de desenho, não uma edição incidental.
- Nunca sobrescreva nem apague um handoff. Mantenha estáveis o nome da pasta, os nomes dos arquivos, os campos do cabeçalho e o formato do índice, porque pessoas e ferramentas dependem deles.
- Mantenha o plugin completo por si só. A skill e as regras do redator não devem depender de um `AGENTS.md` separado nem deste guia.
- Mantenha os dois idiomas equivalentes. O programa é o mesmo arquivo nas duas pastas, exceto pela linha `LANGUAGE`. Atualize os dois idiomas juntos.
- Diferencie comportamento observado de afirmações da documentação, suposições e comportamentos propostos. Não alegue melhorias de qualidade ou custo sem medições comparáveis.
- Use linguagem clara em português e em inglês.

## Abra um pull request

1. Crie um fork do repositório na sua conta do GitHub. Um fork é uma cópia sua, que você pode editar.
2. Crie uma branch no seu fork para uma alteração coerente.
3. Edite os arquivos e registre a alteração em um commit com mensagem descritiva.
4. Abra um pull request da sua branch para a branch `main` deste repositório. Vincule a issue pertinente, se houver.
5. Explique o problema, o comportamento resultante, as verificações e as limitações. Responda à revisão na mesma branch.

Um pull request propõe uma mudança; ele não altera este repositório até que o mantenedor o integre. Você também pode contribuir revisando propostas, reproduzindo falhas relatadas ou fornecendo evidências sem alterar arquivos.

## Verifique de forma proporcional

Na pasta de idioma alterada, execute `python3 -m unittest discover -s tests` e `claude plugin validate --strict .claude-plugin/plugin.json`. Confira se os links funcionam e se YAML e JSON têm sintaxe válida. Para uma tradução ou mudança de redação, compare o significado e as obrigações antes e depois.

Para mudanças na descrição da skill ou nos passos da conversa, rode os casos afetados da suíte de avaliação com `claude plugin eval . --allow-tools Write Edit Bash`. As avaliações chamam modelos pela sua conta.

Para mudanças nas regras do redator ou no programa, grave também um handoff real de uma conversa descartável e confira-o contra a conversa: decisões, autorizações, restrições, pendências e citações.

Para alegar compatibilidade, identifique a versão do Claude Code (CLI ou aplicativo), o sistema operacional, o que você observou e as limitações. Use recursos descartáveis e conversas sintéticas. Nunca envie senhas, tokens de acesso, chaves privadas, dados pessoais, histórico privado de conversas ou handoffs sem remoção de informações sensíveis.

## Revisão e releases

Jonathan Honorio mantém o projeto e decide se uma alteração será aceita. As revisões consideram o problema descrito, as evidências, a consistência com o desenho da skill e o custo de manutenção. A revisão não implica promessa de prazo de resposta ou de aceite.

As alterações aceitas são integradas à `main`. Uma release identifica uma versão selecionada do repositório e descreve suas mudanças e limitações conhecidas. Instalar ou atualizar continua sendo uma decisão do usuário; um pull request ou uma discussão em aberto não é uma alteração lançada.

Ao enviar uma contribuição, você concorda em fornecê-la sob a [Licença MIT](LICENSE) deste repositório. Siga o [Código de Conduta](CODE_OF_CONDUCT.md).
