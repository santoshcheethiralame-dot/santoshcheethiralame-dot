#!/usr/bin/env python3
"""Write README.md from the same content tables that drive the SVGs."""
from build_assets import PROJECTS, LINKS, MORE
from svgkit import ROOT

U = "santoshcheethiralame-dot"
RAW = f"https://raw.githubusercontent.com/{U}/{U}"
HREF = {
    "portfolio": "https://santoshcheethirala.vercel.app",
    "linkedin": "https://www.linkedin.com/in/santoshcheethirala/",
    "github": f"https://github.com/{U}?tab=repositories",
}
REPO = {"highwater": "HighWater", "tessera": "TESSERA", "injunct": "INJUNCT", "precedent": "PRECEDENT",
        "glassbox": "GlassBox", "missingmass": "MissingMass", "lift": "LIFT", "conrag": "ConRAG",
        "gradient": "GRADIENT", "baoli": "BAOLI", "smudge": "SMUDGE", "ember": "EMBER-BOOK"}

LAB = [
    ("DRAGNET", "distribution-free, set-valued causal attribution for RAG, using conformal prediction"),
    ("LINEUP", "a controlled benchmark for causal chunk-role attribution in RAG"),
    ("FORGE", "an agent that writes, safety-checks and keeps its own tools"),
    ("HEMLOCK", "grounded discharge-medication safety review"),
    ("CHRONOS", "a time-travel debugger for Python"),
]


def pic(base, alt, width=None, attrs=""):
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="{base}-light.svg">'
            f'<img alt="{alt}" src="{base}-dark.svg"{w}{attrs}></picture>')


def head(sid, alt):
    return f'\n<br>\n\n{pic(f"assets/h-{sid}", alt, "100%")}\n'


out = []
A = out.append
A(f"<!-- Every graphic is generated: python scripts/build_assets.py && python scripts/write_readme.py -->")
A(f"<!-- TELEMETRY is rebuilt daily by .github/workflows/stats.yml onto the output-stats branch. -->\n")
A(pic("assets/hero", "Santosh Cheethirala. Systems, AI safety, agents and graphics. CS at PES University, class of 2028.", "100%"))
A("\n<p align=\"center\">")
for slug, label, value in LINKS:
    A(f'  <a href="{HREF[slug]}">{pic(f"assets/btn-{slug}", f"{label}: {value}", None, " height=\"40\"")}</a>')
A("</p>\n")

A(head("about", "01 / whoami"))
A('<p align="center"><img alt="A neofetch-style terminal card: an ASCII cat, plus OS, editor, languages, university, current research, honours, hackathons and hobbies" src="assets/neofetch.svg" width="880"></p>\n')
A("<p align=\"center\">I like problems where the answer has to be <b>shown</b>, not asserted: lost writes "
  "reproduced under a linearizability checker, agent rules proven against git history, and safety audits "
  "that come with an estimate of what they missed.</p>\n")

A(head("work", "02 / selected work"))
for i in range(0, len(PROJECTS), 2):
    A('<p align="center">')
    for p in PROJECTS[i:i + 2]:
        slug, name, *_ , tag = p[:6]
        A(f'  <a href="https://github.com/{U}/{REPO[slug]}">{pic(f"assets/cards/{slug}", f"{name}: {p[5]}", "49%")}</a>')
    A("</p>")

A(head("more", "03 / also shipped"))
A('<p align="center">')
for name, lang, demo, desc in MORE:
    A(f'  <a href="https://github.com/{U}/{name}">{pic(f"assets/rows/{name.lower()}", f"{name}: {desc}", "100%")}</a>')
A("</p>")
A("\n<details>\n<summary><b>In the lab</b> &nbsp;·&nbsp; research and works in progress, in private repos for now</summary>\n<br>\n")
for name, desc in LAB:
    A(f"- **{name}**: {desc}")
A("\n</details>\n")

A(head("stack", "04 / toolbox"))
A(pic("assets/toolbox", "Toolbox: Python, Rust, Go, TypeScript, C, WGSL; Raft, LSM-trees, MVCC; PyTorch, TransformerLens; React, Next.js, Three.js, WebGPU; PostgreSQL, Docker, Grafana; Claude Code, MCP", "100%"))

A(head("stats", "05 / telemetry"))
A(f'<picture><source media="(prefers-color-scheme: dark)" srcset="{RAW}/output-stats/stats-dark.svg">'
  f'<source media="(prefers-color-scheme: light)" srcset="{RAW}/output-stats/stats-light.svg">'
  f'<img alt="GitHub activity: contributions in the last year, streaks, commits, repositories, weekly activity and top languages" src="{RAW}/output-stats/stats-dark.svg" width="100%"></picture>')

A(head("arcade", "06 / the year, eaten"))
A(f'<picture><source media="(prefers-color-scheme: dark)" srcset="{RAW}/output/snake-dark.svg">'
  f'<source media="(prefers-color-scheme: light)" srcset="{RAW}/output/snake.svg">'
  f'<img alt="A snake eating my GitHub contribution graph" src="{RAW}/output/snake-dark.svg" width="100%"></picture>')
A("\n<details>\n<summary>&nbsp;or watch pac-man do it</summary>\n<br>\n")
A(f'<img alt="Pac-Man eating my GitHub contribution graph" src="{RAW}/output-arcade/pacman-contribution-graph.svg" width="100%">')
A("\n</details>\n")

A("\n<br>\n")
A(pic("assets/footer", "santosh@github:~$ exit  # thanks for scrolling", "100%"))
A(f'\n<p align="right"><img alt="profile views" src="https://komarev.com/ghpvc/?username={U}&label=visitors&color=FFB454&style=flat-square&labelColor=111115"></p>')

(ROOT / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("README.md written")
