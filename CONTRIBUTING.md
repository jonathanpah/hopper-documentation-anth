# Contributing

Version 2 of this plugin was built from `SPEC.md`. Changes follow the spec's rules.

## Before opening a pull request

1. Run the acceptance tests for both packages, from the repository root:

   ```sh
   HOPPER_DOCUMENTATION_ANTH_PACOTE=hopper-documentation-anth-pt-br TZ=UTC python3 -m unittest discover -s aceite/testes
   HOPPER_DOCUMENTATION_ANTH_PACOTE=hopper-documentation-anth-en TZ=UTC python3 -m unittest discover -s aceite/testes
   ```

2. Run the executor tests of each package: `python3 -m unittest discover -s tests`, inside the package folder.
3. Run the checker on its cases: `python3 aceite/conferir.py aceite/casos/conferidor/valida --idioma pt-br`.
4. Validate the plugins: `claude plugin validate --strict hopper-documentation-anth-pt-br` and the same for `-en`.
5. Keep the program identical in both packages except for the `LANGUAGE` line.

Run evaluations with `claude plugin eval ./<package> --ablation none --trust-plugin --model sonnet --allow-tools 'Bash(python3 *)'` because the skill runs the program through Bash, which evaluations allow only with `--allow-tools`.

The GitHub verification (`.github/workflows/verificar.yml`) runs the acceptance tests on Ubuntu and macOS with Python 3.9 and 3.13, the checker cases and the inventory test.

## Frozen criteria

The files in `aceite/`, the workflow and `SPEC.md` are frozen: `aceite/MANIFESTO.sha256` holds their SHA-256, and the tag `criterios-v<version>` of the current version marks the commit (`criterios-v2.1.0` now; `criterios-v2.0.0` keeps the criteria of version 2.0). The verification fails with "CRITÉRIO ALTERADO" when a frozen file differs from the manifest or the manifest differs from the tag. Changing a criterion needs the owner's approval, in its own commit, with a new tag `criterios-v<next version>` and the workflow pointing to it, because force pushes are not allowed.

## Reporting and fixing a defect

1. Open an issue with the transcript excerpt (with secrets hidden) and the lines of `rodadas.jsonl` from the data folder.
2. The fix starts with an acceptance test that fails on the current `main`.
3. The fix goes in a new branch, reviewed by someone without the author's context.
4. With the owner's approval, the new test enters the frozen criteria and the fix is merged.
5. If the defect escaped the verifiers, record the prevention here.

## Known prevention list

- The transcript format is internal to Claude Code: keep test transcripts from real sessions in `aceite/casos/`.
- The data folder is the one Claude Code reserves for the plugin (`<plugin>-<marketplace>`); never create a parallel folder.
- A detached process must be created with a double fork and `setsid`; `Popen(start_new_session=True)` dies with Claude Code.
- `claude plugin uninstall` without `--keep-data` deletes the plugin data folder, including `config.json`. Use `--keep-data` to preserve the data and configuration (D-14).
- With the same plugin version, `claude plugin update` does not refresh the installed copy. After updating the source copy, run `claude plugin uninstall --keep-data hopper-documentation-anth@hopper-documentation-anth` followed by `claude plugin install hopper-documentation-anth@hopper-documentation-anth` (D-15).
