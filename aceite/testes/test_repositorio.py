"""Testes de aceite T32, T35, T37, T38 e T41 (repositório, idiomas e instalação). Critério congelado da spec, seções 5.5 e 5.6."""
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from apoio import CODIGO_B1, PACOTE, PROGRAMA, RAIZ, SESSAO_B1, SKILL, CasoDeAceite, TEXTO, le

INVENTARIO = [
    ".claude-plugin/marketplace.json",
    ".github/ISSUE_TEMPLATE/bug-report.yml",
    ".github/ISSUE_TEMPLATE/change-proposal.yml",
    ".github/pull_request_template.md",
    ".github/workflows/verificar.yml",
    ".gitignore", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "LICENSE", "README.md", "SECURITY.md", "SPEC.md", "index.md",
    "aceite/conferir.py", "aceite/MANIFESTO.sha256", "aceite/roteiro.json", "aceite/casos/*", "aceite/testes/*",
    "hopper-documentation-anth-pt-br/CODE_OF_CONDUCT.md", "hopper-documentation-anth-pt-br/CONTRIBUTING.md",
    "hopper-documentation-anth-pt-br/SECURITY.md", "hopper-documentation-anth-pt-br/.github/*",
]
for pacote, regras, modelos in (("hopper-documentation-anth-pt-br", "regras-de-escrita.md", "modelos.md"),
                                ("hopper-documentation-anth-en", "writing-rules.md", "templates.md")):
    INVENTARIO += [
        f"{pacote}/.claude-plugin/plugin.json", f"{pacote}/.claude-plugin/marketplace.json", f"{pacote}/hooks/hooks.json",
        f"{pacote}/scripts/hopper_documentation_anth.py", f"{pacote}/skills/hopper-documentation-anth/SKILL.md",
        f"{pacote}/skills/hopper-documentation-anth/LICENSE", f"{pacote}/skills/hopper-documentation-anth/{regras}",
        f"{pacote}/skills/hopper-documentation-anth/{modelos}", f"{pacote}/tests/*", f"{pacote}/evals/*",
        f"{pacote}/.gitignore", f"{pacote}/LICENSE", f"{pacote}/README.md", f"{pacote}/index.md",
    ]
PROIBIDOS = ("claude_agent" + "_sdk", "get_session" + "_messages", "unverified" + "_quotes")


def arquivos_versionados():
    saida = subprocess.run(["git", "ls-files"], cwd=str(RAIZ), capture_output=True, text=True, check=True).stdout
    return [l for l in saida.splitlines() if l.strip()]


def branch_atual():
    return os.environ.get("GITHUB_REF_NAME") or subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(RAIZ),
                                                                capture_output=True, text=True).stdout.strip()


class Repositorio(unittest.TestCase):
    def test_R32_inventario_da_main(self):
        """T32: só os caminhos do Anexo C, e nenhum arquivo com as cadeias proibidas (exceto SPEC.md e este teste)."""
        fora_da_main = branch_atual() != "main"
        permitidos = lambda caminho: any(fnmatch.fnmatch(caminho, p) or (p.endswith("/*") and caminho.startswith(p[:-1])) for p in INVENTARIO)  # noqa: E731
        indevidos = [c for c in arquivos_versionados() if not permitidos(c) and not (fora_da_main and c.startswith("execucao/"))]
        self.assertEqual(indevidos, [])
        proprio = str(Path(__file__).resolve().relative_to(RAIZ))
        com_proibidos = []
        for caminho in arquivos_versionados():
            if caminho in ("SPEC.md", proprio) or (fora_da_main and caminho.startswith("execucao/")):
                continue
            try:
                texto = (RAIZ / caminho).read_text(encoding="utf-8")
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            if any(p in texto for p in PROIBIDOS):
                com_proibidos.append(caminho)
        self.assertEqual(com_proibidos, [])
        for pacote in ("hopper-documentation-anth-pt-br", "hopper-documentation-anth-en"):
            manifesto = json.loads(le(RAIZ / pacote / ".claude-plugin" / "plugin.json"))
            self.assertEqual(manifesto["version"], "2.0.0", pacote)

    def test_R35_dois_pacotes_com_o_mesmo_programa(self):
        """T35: os 2 programas diferem só na linha LANGUAGE; os 2 pacotes têm os arquivos de plugin."""
        a = le(RAIZ / "hopper-documentation-anth-pt-br" / "scripts" / "hopper_documentation_anth.py").splitlines()
        b = le(RAIZ / "hopper-documentation-anth-en" / "scripts" / "hopper_documentation_anth.py").splitlines()
        self.assertEqual(len(a), len(b))
        diferentes = [(x, y) for x, y in zip(a, b) if x != y]
        self.assertEqual(len(diferentes), 1, diferentes[:3])
        self.assertTrue(diferentes[0][0].startswith("LANGUAGE = ") and diferentes[0][1].startswith("LANGUAGE = "), diferentes)
        for pacote, regras, modelos in (("hopper-documentation-anth-pt-br", "regras-de-escrita.md", "modelos.md"),
                                        ("hopper-documentation-anth-en", "writing-rules.md", "templates.md")):
            for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "hooks/hooks.json",
                        "scripts/hopper_documentation_anth.py", "skills/hopper-documentation-anth/SKILL.md",
                        f"skills/hopper-documentation-anth/{regras}", f"skills/hopper-documentation-anth/{modelos}"):
                self.assertTrue((RAIZ / pacote / rel).exists(), f"{pacote}/{rel}")
            self.assertTrue(any((RAIZ / pacote / "tests").glob("test_*.py")), pacote)
            self.assertTrue(any((RAIZ / pacote / "evals").rglob("prompt.md")), pacote)

    def test_R41_skill_md_com_as_secoes_e_menos_de_500_linhas(self):
        """T41: as 2 seções de R41 e menos de 500 linhas, nos 2 pacotes."""
        for pacote, secoes in (("hopper-documentation-anth-pt-br", ["O que a skill produz", "Como a skill roda"]),
                               ("hopper-documentation-anth-en", ["What the skill produces", "How the skill runs"])):
            texto = le(RAIZ / pacote / "skills" / "hopper-documentation-anth" / "SKILL.md")
            self.assertLess(len(texto.splitlines()), 500, pacote)
            titulos = [l.lstrip("#").strip() for l in texto.splitlines() if l.startswith("#")]
            for s in secoes:
                self.assertIn(s, titulos, pacote)
            self.assertIn("name: hopper-documentation-anth", texto)
            self.assertNotIn("disable-model-invocation: true", texto)


class Localizacao(CasoDeAceite):
    def test_R37_encontra_o_historico_pela_pasta_de_configuracao(self):
        """T37: com CLAUDE_CONFIG_DIR definida, o histórico vem dela; sem ela, de ~/.claude."""
        self.amb.historico_b1()
        r = self.amb.copia()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.amb.d(2).exists())
        casa = Path(tempfile.mkdtemp(prefix="casa-"))
        self.addCleanup(shutil.rmtree, casa, True)
        shutil.copytree(self.amb.config / "projects", casa / ".claude" / "projects")
        shutil.rmtree(self.amb.doc)
        env = self.amb.ambiente(("rodada-b1",))
        env.pop("CLAUDE_CONFIG_DIR")
        env["HOME"] = str(casa)
        r = subprocess.run([sys.executable, str(PROGRAMA), "rodada", "--sessao", SESSAO_B1], capture_output=True, text=True, env=env, cwd=str(self.amb.raiz))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.amb.d(2).exists())
        registro = casa / ".claude" / "plugins" / "data" / "hopper-documentation-anth-hopper-documentation-anth" / "rodadas.jsonl"
        linhas = [json.loads(l) for l in le(registro).splitlines()]
        self.assertTrue(any(l["conversa"] == SESSAO_B1 and l["etapa"] == "escrita" and l["resultado"] == "concluída" for l in linhas))
        # a skill localiza pelo identificador, sem transcript_path
        shutil.rmtree(self.amb.doc)
        r = self.amb.roda("rodada", "--sessao", SESSAO_B1, respostas=("rodada-b1",))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.amb.d(3).exists())

    def test_R38_encontra_o_executavel_do_claude_code(self):
        """T38: CLAUDE_PID aponta para o executável que iniciou o gatilho; depois o PATH; depois ~/.local/bin/claude."""
        pasta = Path(tempfile.mkdtemp(prefix="claude-falso-"))
        self.addCleanup(shutil.rmtree, pasta, True)
        falso = pasta / "claude-pid"
        sleep = shutil.which("sleep") or "/bin/sleep"
        outro = shutil.which("true") or "/usr/bin/true"
        if sys.platform.startswith("linux"):
            shutil.copy2(sleep, falso)  # /proc/<pid>/exe resolve links simbólicos.
        else:
            os.symlink(sleep, falso)  # cópias de binários do sistema são mortas no macOS.
        processo = subprocess.Popen([str(falso), "30"])
        def terminar():
            if processo.poll() is None:
                processo.kill()
            processo.wait()
        self.addCleanup(terminar)
        candidato_path = pasta / "claude"
        os.symlink(outro, candidato_path)
        casa = pasta / "casa"
        (casa / ".local" / "bin").mkdir(parents=True)
        candidato_local = casa / ".local" / "bin" / "claude"
        os.symlink(sleep, candidato_local)
        env = self.amb.ambiente()
        env.pop("HOPPER_DOCUMENTATION_ANTH_CLAUDE")
        env.update(CLAUDE_PID=str(processo.pid), PATH=str(pasta) + os.pathsep + env.get("PATH", ""), HOME=str(casa))
        with self.subTest(candidato="CLAUDE_PID antes do PATH"):
            r = subprocess.run([sys.executable, str(PROGRAMA), "executavel"], capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotEqual(falso.resolve(), candidato_path.resolve())
            self.assertEqual(Path(r.stdout.strip()).resolve(), falso.resolve())
        env.pop("CLAUDE_PID")
        with self.subTest(candidato="PATH antes de ~/.local/bin/claude"):
            r = subprocess.run([sys.executable, str(PROGRAMA), "executavel"], capture_output=True, text=True, env=env)
            self.assertNotEqual(candidato_path.resolve(), candidato_local.resolve())
            self.assertEqual(Path(r.stdout.strip()).resolve(), candidato_path.resolve())
        env["PATH"] = "/nonexistent"
        with self.subTest(candidato="~/.local/bin/claude"):
            r = subprocess.run([sys.executable, str(PROGRAMA), "executavel"], capture_output=True, text=True, env=env)
            self.assertEqual(Path(r.stdout.strip()).resolve(), candidato_local.resolve())



if __name__ == "__main__":
    unittest.main()
