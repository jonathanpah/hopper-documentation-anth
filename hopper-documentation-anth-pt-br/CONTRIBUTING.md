# Como contribuir

A versão 2 deste plugin foi construída a partir do `SPEC.md` da raiz do repositório. As mudanças seguem as regras da spec.

## Antes de abrir um pedido de alteração

1. Rode os testes de aceite dos 2 pacotes, a partir da raiz do repositório:

   ```sh
   HOPPER_DOCUMENTATION_ANTH_PACOTE=hopper-documentation-anth-pt-br TZ=UTC python3 -m unittest discover -s aceite/testes
   HOPPER_DOCUMENTATION_ANTH_PACOTE=hopper-documentation-anth-en TZ=UTC python3 -m unittest discover -s aceite/testes
   ```

2. Rode os testes do executor de cada pacote: `python3 -m unittest discover -s tests`, dentro da pasta do pacote.
3. Rode o conferidor nos casos dele: `python3 aceite/conferir.py aceite/casos/conferidor/valida --idioma pt-br`.
4. Valide os plugins: `claude plugin validate --strict hopper-documentation-anth-pt-br` e o mesmo para `-en`.
5. Mantenha o programa igual nos 2 pacotes, exceto a linha `LANGUAGE`.

A verificação do GitHub (`.github/workflows/verificar.yml`) roda os testes de aceite em Ubuntu e macOS com Python 3.9 e 3.13, os casos do conferidor e o teste de inventário.

## Critérios congelados

Os arquivos de `aceite/`, o fluxo de verificação e o `SPEC.md` são congelados: `aceite/MANIFESTO.sha256` guarda o SHA-256 deles, e a tag `criterios-congelados-2-1` marca o commit (a tag `criterios-congelados` guarda os critérios da versão 2.0). A verificação falha com "CRITÉRIO ALTERADO" quando um arquivo congelado difere do manifesto ou o manifesto difere da tag. Mudar um critério exige a aprovação do proprietário, em commit próprio, com uma tag nova e o fluxo de verificação apontando para ela, porque envios forçados não são permitidos.

## Relatar e corrigir um defeito

1. Abra uma issue com o trecho do histórico (com os segredos ocultos) e as linhas de `rodadas.jsonl` da pasta de dados.
2. A correção começa por um teste de aceite que falha na `main` atual.
3. A correção vai em uma branch nova, revisada por alguém sem o contexto do autor.
4. Com a aprovação do proprietário, o teste novo entra nos critérios congelados e a correção é incorporada.
5. Se o defeito escapou dos verificadores, registre a prevenção aqui.

## Prevenções conhecidas

- O formato do histórico é interno do Claude Code: mantenha em `aceite/casos/` históricos de teste vindos de sessões reais.
- A pasta de dados é a que o Claude Code reserva ao plugin (`<plugin>-<catálogo>`); nunca crie uma pasta paralela.
- Um processo separado precisa de fork duplo com `setsid`; `Popen(start_new_session=True)` morre junto com o Claude Code.
- `claude plugin uninstall` sem `--keep-data` apaga a pasta de dados do plugin, inclusive o `config.json`. Use `--keep-data` para preservar os dados e a configuração (D-14).
- Com a mesma versão do plugin, `claude plugin update` não atualiza a cópia instalada. Depois de atualizar a cópia de origem, rode `claude plugin uninstall --keep-data hopper-documentation-anth@hopper-documentation-anth` seguido de `claude plugin install hopper-documentation-anth@hopper-documentation-anth` (D-15).
