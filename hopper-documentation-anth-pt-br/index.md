# Índice documental

- [README](README.md): finalidade, o que roda e envia, requisitos, instalação, uso, limites, testes e atualizações.
- [Skill](skills/hopper-documentation-anth/SKILL.md): o que a conversa faz quando o usuário pede o registro ou chega um aviso da compactação.
- [Regras do redator](skills/hopper-documentation-anth/regras-do-redator.md): as regras de conteúdo que o programa envia ao modelo que escreve o handoff.
- [Exemplo](skills/hopper-documentation-anth/exemplo.md): um handoff completo.
- [Programa](scripts/hopper_documentation_anth.py): lê a conversa, oculta segredos, chama o redator, confere as citações, grava o handoff e refaz o índice.
- [Gatilho](hooks/hooks.json): roda o programa antes de cada compactação.
- [Testes](tests/test_hopper_documentation_anth.py) e [suíte de avaliação](evals/): testes do programa e casos de comportamento para `claude plugin eval`.
- [Contribuição](CONTRIBUTING.md): propostas, pull requests, verificações e revisão.
- [Política de Segurança](SECURITY.md): escopo, expectativas de segurança e relato privado de vulnerabilidades.
- [Código de Conduta](CODE_OF_CONDUCT.md): participação e moderação.
- [Licença](LICENSE): termos MIT e copyright, preservados no texto original em inglês.
- [Relato de bug](.github/ISSUE_TEMPLATE/bug-report.yml), [proposta de alteração](.github/ISSUE_TEMPLATE/change-proposal.yml) e [modelo de pull request](.github/pull_request_template.md): modelos do GitHub.

- [English](../hopper-documentation-anth-en/index.md): skill e documentação equivalentes, publicadas na mesma versão.

- [Plugin do Claude](.claude-plugin/plugin.json) · [Marketplace do Claude](.claude-plugin/marketplace.json).
