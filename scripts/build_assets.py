#!/usr/bin/env python3
"""Build every static SVG on the profile README, in dark and light.

    pip install fonttools brotli
    python scripts/build_assets.py

Outputs to assets/. Edit the content blocks below (HERO, PROJECTS, STACK,
NEOFETCH) and re-run; the README only references the generated files.
"""
from __future__ import annotations

from svgkit import (DARK, LIGHT, REDUCED_MOTION, ROOT, SVG, THEMES, esc,
                    measure, wrap)

OUT = ROOT / "assets"

# ════════════════════════════════════════════════════════════════════════════
# content
# ════════════════════════════════════════════════════════════════════════════
NAME_1, NAME_2 = "Santosh", "Cheethirala"

TYPED = [
    "building a sharded KV store in std-only Rust",
    "making Couchbase lose acknowledged writes",
    "turning AGENTS.md into rules agents can't skip",
    "estimating what safety audits miss",
    "training neural nets inside WebGPU shaders",
]

BUILD_LOG = [
    ("ok", "tessera",     "raft · lsm · 0 crates"),
    ("ok", "highwater",   "56 acked writes lost"),
    ("ok", "injunct",     "446 tests passing"),
    ("ok", "precedent",   "53% → 70% first try"),
    ("ok", "lift",        "+24.4pp causal lift"),
    ("ok", "conrag",      "F1 0.92 on conflicts"),
    ("..", "missingmass", "pre-registering v0.1"),
]

PILLARS = [("SYSTEMS", "amber"), ("AI SAFETY", "cyan"), ("AGENTS", "green"), ("GRAPHICS", "pink")]

# category -> accent key
CAT = {
    "SYSTEMS": "amber", "AGENTS": "green", "AI SAFETY": "cyan", "RETRIEVAL": "blue",
    "GPU · ML": "pink", "GRAPHICS": "pink", "GAMES · EDU": "violet", "EDUCATION": "violet",
}

# slug, name, category, language, live?, tagline, metric, metric label, stack
PROJECTS = [
    ("highwater", "HighWater", "SYSTEMS", "Go", False,
     "Couchbase is one of the few major databases with no published Jepsen analysis, "
     "so I ran one: kill the majority before the flush and watch acknowledged writes vanish.",
     "56", "acknowledged writes lost at “majority” durability, confirmed by Porcupine",
     "Go · gocbcore patch · Porcupine · fault injection"),
    ("tessera", "TESSERA", "SYSTEMS", "Rust", False,
     "A distributed, sharded, replicated key-value store on a from-scratch LSM engine. "
     "Raft per shard, the CockroachDB shape, scaled down.",
     "0", "external crates; deterministic simulation caught a real split-brain on seed 99",
     "Rust · Raft · LSM-tree · MVCC · simulation testing"),
    ("injunct", "Injunct", "AGENTS", "Python", False,
     "Your AGENTS.md is a suggestion; Injunct makes it a rule. It proves each instruction "
     "against your git history, then blocks the agent edit that breaks one.",
     "446", "tests passing, zero dependencies, runs on open-weight Gemma 4",
     "Python · Claude Code + opencode hooks · git hooks · CI"),
    ("precedent", "PRECEDENT", "AGENTS", "Python", False,
     "Your coding agent forgot the migration again. Precedent turns a confirmed failure "
     "into a binding, executable check, cited to the run that proved it.",
     "53→70%", "first-try pass rate across 300 measured agent runs",
     "Python · standard library · one SQLite file"),
    ("glassbox", "GlassBox", "AI SAFETY", "Python", True,
     "A live microscope for transformer LLMs. Watch attention heads and sparse features, "
     "then ablate one and watch the answer move.",
     "2.6B", "parameter Gemma-2 probed and edited causally, live in a browser",
     "PyTorch · FastAPI · React · sparse autoencoders"),
    ("missingmass", "MissingMass", "AI SAFETY", "Python", False,
     "How complete was the audit? Capture-recapture statistics that estimate how many "
     "failure modes red teams and interpretability tools missed.",
     "Chao2", "coverage estimator, validated on testbeds with planted failures",
     "Python · statistics · open-weight LLMs · pre-registered"),
    ("lift", "LIFT", "AGENTS", "Node.js", False,
     "Every dunning tool reports how much it recovered. LIFT subtracts the money that was "
     "arriving anyway, measured against a control arm left completely alone.",
     "+24.4pp", "mean causal lift across 30 batches, Razorpay AI Buildathon",
     "Node.js · causal inference · zero runtime deps"),
    ("conrag", "ConRAG", "RETRIEVAL", "TypeScript", False,
     "Retrieval-augmented generation that notices when its sources disagree, and answers "
     "with both sides, their sources and the way the evidence leans.",
     "0.92", "F1 on pair-level contradiction detection, at 1.00 recall",
     "Next.js · PostgreSQL 17 · pgvector · triggers"),
    ("gradient", "GRADIENT", "GPU · ML", "TypeScript", True,
     "A from-scratch deep-learning stack where every FLOP is a WebGPU compute shader: "
     "forward pass, hand-derived backward pass and optimizer.",
     "100%", "in-browser on your GPU: no Python, no server, no WASM",
     "TypeScript · WebGPU · hand-written WGSL"),
    ("baoli", "BAOLI", "GRAPHICS", "JavaScript", True,
     "A real-time cinematic descent into Toorji Ka Jhalra, an 18th-century Jodhpur "
     "stepwell, from a god's-eye view down to the shrine in the water.",
     "60fps", "live in the browser, with no pre-rendered video and no build step",
     "Three.js · WebGL2 · GLSL"),
    ("smudge", "Smudge", "GAMES · EDU", "TypeScript", False,
     "A detective game inside a living textbook. AI suspects talk freely, and only the "
     "science can catch the liar. Built for Class 9–10 physics and chemistry.",
     "₹0", "running cost, with 403 server tests passing",
     "Phaser 3 · TypeScript · FastAPI · LLM agents"),
    ("ember", "Ember", "EDUCATION", "Python", False,
     "A DSA textbook that assumes you are five, have unlimited time, and refuse to "
     "memorise anything you do not understand. Eight volumes, 152 chapters.",
     "1,075,998", "assertions, 0 failures; 149 mutants, 0 escaped",
     "Python · 520 problems · offline reader app"),
]

STACK = [
    ("LANGUAGES", "amber", ["Python", "Rust", "Go", "TypeScript", "C", "WGSL", "SQL", "GLSL"]),
    ("SYSTEMS",   "cyan",  ["Raft", "LSM-trees", "MVCC", "simulation testing", "linearizability", "fault injection"]),
    ("ML · SAFETY", "green", ["PyTorch", "TransformerLens", "sparse autoencoders", "conformal prediction", "causal inference", "RAG"]),
    ("WEB · GPU", "pink",  ["React", "Next.js", "Vite", "Tailwind", "Three.js", "WebGPU", "Phaser"]),
    ("DATA · OPS", "violet", ["PostgreSQL", "pgvector", "SQLite", "Docker", "Grafana", "OpenTelemetry", "FastAPI"]),
    ("AGENTS",    "blue",  ["Claude Code", "opencode", "MCP", "Gemini", "Gemma", "agent hooks"]),
]

# name, language, live demo, one-liner (must fit one line)
MORE = [
    ("ShowMe", "TypeScript", "https://showme-sandy.vercel.app",
     "Ask any question and an LLM draws you a custom animation, live: real running code for your exact confusion"),
    ("CallSheet", "Python", None,
     "A render farm that reports to Grafana, and an agent that decides which shots to sacrifice before review"),
    ("UNTANGLE", "Python", None,
     "Graph-native detection of mule-account fraud rings in UPI-style payments. Scores the network, not the hop"),
    ("ATTEST", "TypeScript", None,
     "Proof a human understood this: turns any written assignment into a short, adaptive oral defense"),
    ("ATLAS", "JavaScript", "https://atlas-eight-azure.vercel.app",
     "A personal ML study map with written notes across eight tracks, from the maths up to AI safety"),
    ("ORBIT", "TypeScript", "https://orbit-virid-gamma.vercel.app",
     "A local-first focus engine that plans a student's day around energy, deadlines and exam readiness"),
    ("CRUX", "TypeScript", None,
     "An exam-tuned study app: deeply explained notes, MCQ quizzes, flashcards and past-year questions"),
    ("TERRACREST", "TypeScript", "https://terracrest.vercel.app",
     "An invitation-only deal platform for high-value Bengaluru real estate, every parcel ground-verified"),
    ("skills", "Markdown", None,
     "33 portable Claude Code skills for craft, design, motion and engineering practice"),
]

SECTIONS = [
    ("about",  "01", "WHOAMI",          "~/santosh"),
    ("work",   "02", "SELECTED WORK",   "12 projects · click a card"),
    ("more",   "03", "ALSO SHIPPED",    "the rest of the workbench"),
    ("stack",  "04", "TOOLBOX",         "what I reach for"),
    ("stats",  "05", "TELEMETRY",       "regenerated daily"),
    ("arcade", "06", "THE YEAR, EATEN", "contribution graph"),
]

LINKS = [
    ("portfolio", "portfolio", "santoshcheethirala.vercel.app"),
    ("linkedin",  "linkedin",  "in/santoshcheethirala"),
    ("github",    "github",    "@santoshcheethiralame-dot"),
]


# ════════════════════════════════════════════════════════════════════════════
# shared bits
# ════════════════════════════════════════════════════════════════════════════
def frame(s: SVG, t: dict, rx=16):
    s.rect(0.5, 0.5, s.w - 1, s.h - 1, fill=t["bg"], rx=rx, stroke=t["line"])


def dot_grid(s: SVG, t: dict, pid="dots", gap=22, r=1.0, op=1.0):
    s.defs.append(
        f'<pattern id="{pid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{gap/2}" cy="{gap/2}" r="{r}" fill="{t["line2"]}" opacity="{op}"/></pattern>')


def glow(s: SVG, gid: str, color: str, op: float):
    s.defs.append(
        f'<radialGradient id="{gid}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def pct(x: float) -> str:
    return f"{max(0.0, min(100.0, x)):.3f}%"


# ════════════════════════════════════════════════════════════════════════════
# hero
# ════════════════════════════════════════════════════════════════════════════
def hero(t: dict):
    W, H = 1200, 440
    s = SVG(W, H, "Santosh Cheethirala — systems, AI safety and agents. CS at PES University.")
    dark = t is DARK
    dot_grid(s, t, op=0.55 if dark else 0.8)
    glow(s, "g1", t["amber"], 0.16 if dark else 0.10)
    glow(s, "g2", t["cyan"], 0.10 if dark else 0.07)
    s.defs.append(
        '<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff"/>'
        '<stop offset=".55" stop-color="#fff" stop-opacity=".25"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<mask id="m"><rect width="1200" height="440" fill="url(#fade)"/></mask>'
        '<clipPath id="card"><rect x="1" y="1" width="1198" height="438" rx="16"/></clipPath>')
    frame(s, t)
    s.add('<g clip-path="url(#card)">')
    s.rect(0, 0, W, H, fill="url(#dots)", extra='mask="url(#m)"')
    s.add(f'<ellipse cx="230" cy="150" rx="430" ry="260" fill="url(#g1)"/>')
    s.add(f'<ellipse cx="1040" cy="430" rx="420" ry="220" fill="url(#g2)"/>')
    s.add("</g>")

    # top bar
    s.text(48, 50, [("santosh", t["cyan"]), ("@", t["faint"]), ("github", t["cyan"]),
                    (" : ", t["faint"]), ("~/readme", t["muted"])], alias="mono-m", size=13)
    s.text(W - 48, 50, [("bengaluru, in", t["muted"]), ("  ·  ", t["faint"]),
                        ("12.97°N 77.59°E", t["faint"])], alias="mono", size=12.5, anchor="end")
    s.line(48, 70, W - 48, 70, t["line"])

    # name
    s.text(44, 170, NAME_1, alias="disp-b", size=104, fill=t["ink"], ls=-3.5)
    w2 = measure(NAME_2, "disp-b", 104, -3.5)
    s.text(44, 272, NAME_2, alias="disp-b", size=104, fill=t["ink"], ls=-3.5)
    s.rect(44 + w2 + 6, 254, 18, 18, fill=t["amber"], rx=2)

    # typed line in a prompt pill
    px, py, pw, ph = 48, 304, 600, 46
    s.rect(px, py, pw, ph, fill=t["panel"], rx=10, stroke=t["line"])
    s.text(px + 18, py + 29, [("❯", t["amber"])], alias="mono-b", size=17)
    tx = px + 44
    s.defs.append(f'<clipPath id="pill"><rect x="{tx - 4}" y="{py + 2}" width="{pw - (tx - px) - 6}" height="{ph - 4}"/></clipPath>')
    N, slot = len(TYPED), 5.0
    T = N * slot
    s.css.append(f".blink{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}")
    s.add('<g clip-path="url(#pill)">')
    for i, phrase in enumerate(TYPED):
        w = measure(phrase, "mono", 17)
        st, L = i * 100 / N, 100 / N
        en = st + L
        # visibility: step-end holds each keyframe's value until the next
        vis = {0.0: 1 if i == 0 else 0}
        if i:
            vis[st] = 1
        vis[en] = 0
        vis[100.0] = 0
        s.css.append(f"@keyframes v{i}{{" + "".join(
            f"{pct(k)}{{opacity:{v}}}" for k, v in sorted(vis.items())) + "}")
        s.css.append(f".v{i}{{opacity:{1 if i == 0 else 0};animation:v{i} {T}s step-end infinite}}")
        n = len(phrase)
        s.css.append(
            f"@keyframes c{i}{{0%{{transform:translateX(0)}}"
            f"{pct(st)}{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{pct(st + L * .42)}{{transform:translateX({w:.1f}px);animation-timing-function:linear}}"
            f"{pct(st + L * .84)}{{transform:translateX({w:.1f}px);animation-timing-function:steps({max(1, n // 3)},end)}}"
            f"{pct(st + L * .96)}{{transform:translateX(0)}}100%{{transform:translateX(0)}}}}"
            f".c{i}{{animation:c{i} {T}s infinite}}")
        s.add(f'<g class="v{i}">')
        s.text(tx, py + 29, phrase, alias="mono", size=17, fill=t["ink"])
        s.add(f'<g class="c{i}">')
        s.rect(tx - 1, py + 3, 640, ph - 6, fill=t["panel"])
        s.rect(tx, py + 13, 9, 21, fill=t["amber"], extra='class="blink"')
        s.add("</g></g>")
    s.add("</g>")

    # build log panel
    lx, ly, lw, lh = 716, 100, 436, 250
    s.rect(lx, ly, lw, lh, fill=t["panel"], rx=12, stroke=t["line"])
    s.line(lx, ly + 38, lx + lw, ly + 38, t["line"])
    for k, c in enumerate(("red", "amber", "green")):
        s.add(f'<circle cx="{lx + 20 + k * 16}" cy="{ly + 19}" r="4.5" fill="{t[c]}" opacity=".85"/>')
    s.text(lx + lw / 2, ly + 24, "make -j projects", alias="mono", size=12, fill=t["muted"], anchor="middle")
    s.css.append("@keyframes show{to{opacity:1}}.rm-show{opacity:0;animation:show .01s step-end forwards}")
    for i, (stt, name, note) in enumerate(BUILD_LOG):
        y = ly + 66 + i * 24
        col = t["green"] if stt == "ok" else t["amber"]
        tag = " ok " if stt == "ok" else " .. "
        s.add(f'<g class="rm-show" style="animation-delay:{0.5 + i * 0.32:.2f}s">')
        s.text(lx + 20, y, [("[", t["faint"]), (tag, col), ("]", t["faint"]),
                            ("  " + name.ljust(13), t["ink"]), (note, t["muted"])],
               alias="mono", size=13)
        s.add("</g>")
    yc = ly + 66 + len(BUILD_LOG) * 24
    s.add(f'<g class="rm-show" style="animation-delay:{0.5 + len(BUILD_LOG) * 0.32:.2f}s">')
    s.text(lx + 20, yc, [("$ ", t["amber"])], alias="mono-b", size=13)
    s.rect(lx + 38, yc - 11, 8, 15, fill=t["amber"], extra='class="blink"')
    s.add("</g>")

    # footer strip
    s.line(48, 382, W - 48, 382, t["line"])
    x = 48
    for label, key in PILLARS:
        s.rect(x, 402, 8, 8, fill=t[key], rx=1.5)
        s.text(x + 16, 410, label, alias="mono-m", size=12, fill=t["body"], ls=2)
        x += 16 + measure(label, "mono-m", 12, 2) + 30
    s.text(W - 48, 410, [("CS @ PES University", t["body"]), ("  ·  ", t["faint"]), ("class of '28", t["muted"])],
           alias="mono", size=12.5, anchor="end")
    s.css.append(REDUCED_MOTION)
    s.save(OUT / f"hero-{t['name']}.svg")


# ════════════════════════════════════════════════════════════════════════════
# section headers
# ════════════════════════════════════════════════════════════════════════════
def section(t: dict, sid, num, title, note):
    W, H = 1200, 64
    s = SVG(W, H, title.title())
    y = 38
    s.text(2, y, num, alias="mono-b", size=13, fill=t["amber"])
    s.text(30, y, "/", alias="mono", size=13, fill=t["faint"])
    s.text(48, y, title, alias="mono-b", size=15, fill=t["ink"], ls=3)
    x1 = 48 + measure(title, "mono-b", 15, 3) + 20
    nw = measure(note, "mono", 12)
    x2 = W - 2 - nw - 20
    s.line(x1, y - 5, x2, y - 5, t["line2"], extra='stroke-dasharray="2 5"')
    s.text(W - 2, y, note, alias="mono", size=12, fill=t["muted"], anchor="end")
    s.save(OUT / f"h-{sid}-{t['name']}.svg")


# ════════════════════════════════════════════════════════════════════════════
# project cards
# ════════════════════════════════════════════════════════════════════════════
def card(t: dict, idx: int, p):
    slug, name, cat, lang, live, tag, metric, mlabel, stack = p
    W, H, P = 600, 340, 32
    acc = t[CAT[cat]]
    s = SVG(W, H, f"{name} — {tag}")
    glow(s, "cg", acc, 0.10 if t is DARK else 0.07)
    s.defs.append(f'<clipPath id="cc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath>')
    s.rect(0.5, 0.5, W - 1, H - 1, fill=t["panel"], rx=14, stroke=t["line"])
    s.add('<g clip-path="url(#cc)">')
    s.add(f'<ellipse cx="{W - 40}" cy="10" rx="300" ry="170" fill="url(#cg)"/>')
    s.rect(0, 0, W, 3, fill=acc, extra='opacity=".9"')
    s.add("</g>")

    # header row
    s.rect(P, 34, 8, 8, fill=acc, rx=1.5)
    s.text(P + 16, 42, cat, alias="mono-b", size=11, fill=acc, ls=2)
    s.text(W - P, 42, f"{idx:02d}", alias="mono", size=11, fill=t["faint"], anchor="end")
    rx = W - P - measure(f"{idx:02d}", "mono", 11) - 18
    s.text(rx, 42, lang, alias="mono", size=11.5, fill=t["muted"], anchor="end")
    if live:
        lw = measure(lang, "mono", 11.5)
        bx = rx - lw - 16 - 62
        s.rect(bx, 27, 62, 20, fill="none", rx=10, stroke=t["green"], extra='stroke-opacity=".5"')
        s.add(f'<circle cx="{bx + 13}" cy="37" r="3" fill="{t["green"]}"/>')
        s.text(bx + 22, 41, "LIVE", alias="mono-b", size=10, fill=t["green"], ls=1.5)

    # name + arrow
    s.text(P - 2, 100, name, alias="disp-b", size=38, fill=t["ink"], ls=-0.8)
    nw = measure(name, "disp-b", 38, -0.8)
    s.text(P + nw + 8, 98, "↗", alias="sans", size=22, fill=t["faint"])

    # tagline
    for k, ln in enumerate(wrap(tag, "sans", 15.5, W - 2 * P)[:3]):
        s.text(P, 136 + k * 24, ln, alias="sans", size=15.5, fill=t["body"])

    # metric
    s.line(P, 232, W - P, 232, t["line"])
    runs = []
    for ch in metric:
        a = "sans-sb" if ch == "₹" else "mono-b"
        if runs and runs[-1][2] == a:
            runs[-1] = (runs[-1][0] + ch, acc, a)
        else:
            runs.append((ch, acc, a))
    s.text(P - 1, 282, runs, alias="mono-b", size=34)
    mw = sum(measure(r[0], r[2], 34) for r in runs)
    lx = P + mw + 18
    ml = wrap(mlabel, "sans-m", 13, W - P - lx)[:2]
    base = 268 if len(ml) == 2 else 277
    for k, ln in enumerate(ml):
        s.text(lx, base + k * 18, ln, alias="sans-m", size=13, fill=t["muted"])
    s.text(P, 314, stack, alias="mono", size=11.5, fill=t["faint"])
    s.save(OUT / "cards" / f"{slug}-{t['name']}.svg")


# ════════════════════════════════════════════════════════════════════════════
# "also shipped" rows — one linkable image per row
# ════════════════════════════════════════════════════════════════════════════
def row(t: dict, idx: int, m):
    name, lang, demo, desc = m
    W, H = 1200, 58
    s = SVG(W, H, f"{name}: {desc}")
    s.rect(0.5, 0.5, W - 1, H - 1, fill=t["panel"], rx=10, stroke=t["line"])
    y = H / 2 + 5
    s.text(24, y, f"{idx:02d}", alias="mono", size=12, fill=t["faint"])
    s.text(60, y, name, alias="mono-b", size=15, fill=t["ink"])
    right = W - 24
    s.text(right, y, "↗", alias="sans", size=16, fill=t["faint"], anchor="end")
    right -= 28
    if demo:
        bw = 62
        s.rect(right - bw, H / 2 - 10, bw, 20, fill="none", rx=10, stroke=t["green"], extra='stroke-opacity=".5"')
        s.add(f'<circle cx="{right - bw + 13}" cy="{H / 2}" r="3" fill="{t["green"]}"/>')
        s.text(right - bw + 22, H / 2 + 4, "LIVE", alias="mono-b", size=10, fill=t["green"], ls=1.5)
        right -= bw + 14
    s.text(right, y - 0.5, lang, alias="mono", size=12, fill=t["muted"], anchor="end")
    maxw = right - measure(lang, "mono", 12) - 24 - 200
    line, words = desc, desc.split()
    while measure(line, "sans", 14.5) > maxw and len(words) > 1:
        words.pop()
        line = " ".join(words).rstrip(",:;") + "…"
    if line != desc:
        print(f"  note: '{name}' description truncated to fit")
    s.text(200, y, line, alias="sans", size=14.5, fill=t["body"])
    s.save(OUT / "rows" / f"{name.lower()}-{t['name']}.svg")


# ════════════════════════════════════════════════════════════════════════════
# toolbox
# ════════════════════════════════════════════════════════════════════════════
def toolbox(t: dict):
    W = 1200
    rowh = 52
    H = 24 + len(STACK) * rowh + 12
    s = SVG(W, H, "Toolbox: " + "; ".join(f"{c}: {', '.join(v)}" for c, _, v in STACK))
    s.rect(0.5, 0.5, W - 1, H - 1, fill=t["panel"], rx=14, stroke=t["line"])
    for i, (cat, key, items) in enumerate(STACK):
        y = 24 + i * rowh
        if i:
            s.line(28, y, W - 28, y, t["line"], extra='stroke-dasharray="2 5"')
        cy = y + rowh / 2
        s.rect(32, cy - 4, 8, 8, fill=t[key], rx=1.5)
        s.text(50, cy + 4.5, cat, alias="mono-b", size=11.5, fill=t[key], ls=2)
        x = 210
        for it in items:
            w = measure(it, "mono-m", 13) + 26
            s.rect(x, cy - 15, w, 30, fill=t["raise_"], rx=7, stroke=t["line"])
            s.text(x + 13, cy + 4.5, it, alias="mono-m", size=13, fill=t["ink"])
            x += w + 10
    s.save(OUT / f"toolbox-{t['name']}.svg")


# ════════════════════════════════════════════════════════════════════════════
# link buttons + footer
# ════════════════════════════════════════════════════════════════════════════
def button(t: dict, slug, label, value):
    lw = measure(label, "mono-b", 12, 1.5)
    vw = measure(value, "mono", 12.5)
    W, H = int(28 + lw + 18 + vw + 40), 44
    s = SVG(W, H, f"{label}: {value}")
    s.rect(0.5, 0.5, W - 1, H - 1, fill=t["panel"], rx=10, stroke=t["line"])
    s.text(16, 27, label.upper(), alias="mono-b", size=12, fill=t["amber"], ls=1.5)
    s.line(16 + lw + 10, 12, 16 + lw + 10, 32, t["line2"])
    s.text(16 + lw + 22, 27, value, alias="mono", size=12.5, fill=t["ink"])
    s.text(W - 16, 28, "↗", alias="sans", size=15, fill=t["muted"], anchor="end")
    s.save(OUT / f"btn-{slug}-{t['name']}.svg")


def footer(t: dict):
    W, H = 1200, 96
    s = SVG(W, H, "thanks for scrolling")
    s.line(0, 20, W, 20, t["line"])
    s.text(0, 62, [("santosh", t["cyan"]), ("@", t["faint"]), ("github", t["cyan"]),
                   (":", t["faint"]), ("~", t["muted"]), ("$ ", t["faint"]),
                   ("exit", t["ink"]), ("  # thanks for scrolling", t["faint"])], alias="mono", size=14)
    s.css.append(".blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}" + REDUCED_MOTION)
    x = measure("santosh@github:~$ exit  # thanks for scrolling", "mono", 14) + 8
    s.rect(x, 49, 9, 17, fill=t["amber"], extra='class="blink"')
    s.text(W, 62, "every graphic on this page is hand-built SVG · scripts/", alias="mono", size=12,
           fill=t["faint"], anchor="end")
    s.save(OUT / f"footer-{t['name']}.svg")


# ════════════════════════════════════════════════════════════════════════════
# neofetch card (dark terminal in both themes)
# ════════════════════════════════════════════════════════════════════════════
ART = """\
:::::::::::=++--=====================================
:::::::::-:==--:==============-::====-:..-===========
:::::::::::+=%*--=============-:---:.:-*+:-------:--:
:::::::-:::-%%%%#-========--==----:..:#%#:-----------
:::::::-::.+%%####+--=---=----::-:..:*%%%*-----------
:::::::-::=%%%######-:--------::....-#%%%#-----------
:::::::::.=%%%%%###*=:::::::::::...:##%%%%-----------
:::::::::.=#%%%+=:::::::-:::::::::::=*#%%%-----------
:::::::::.=##*#-::::::::-:::::-::::::::+**-::::::::-:
::::::::..=*=:::-:::::::::::::-::::::-:::+-::::::::::
:::::::...:::::::::::::::::::::::::::::::.:::::::::::
:::::::...::::::::::::::::::::::::::::::::.::::::::::
:::::.:...::::::=-....-===-:::::::+*:.:***-::::::::-:
:::::.::..::::::*%#---*%%%#:::::::=%*-=%%%#::::::::-:
.::::.::...:::::-%@@@@@@@#-::::::::-*%%%%*:::::::::::
..:::......::::::::::::::::::::===:::::::::::::::::::
..::::::::..:::::::::::::::::::-+=::::-::::::::.:::::
::::::::....:--::-::::::::::::::::::::-::::.:::::::::
::::::::..::..::::::::::::::::::::::::::::..:::::::::
::::::--:......::::::::::::::::::-:::::::..:::::-::::
:::::::::........::::::::::::::::::::::...::::::-::::
::::-:::............:::::::::::::::::....::::--::::::
::::-:::....::::..........................:::::::::::
::::::::...:::::::........................:::::::::::
::::::::....:::::::::::...................:::::::::::
:::::::......:::::::::::::................:::::::::::
:::::::.......::::::::::::::::::::.........::::::::::
:::::::.......:::::::::::::::::::::.........:::::::::
:::::::.......::::::::::::::::::::::........:::::::::
""".rstrip("\n").split("\n")

NEOFETCH = [
    ("user", "", ""),
    ("rule", "", ""),
    ("kv", "OS",       "Windows 11 · zsh + starship"),
    ("kv", "Editor",   "VSCode · Neovim"),
    ("kv", "Langs",    "Python · Rust · Go · TypeScript · C"),
    ("kv", "Systems",  "Raft · LSM-trees · WebGPU · Docker"),
    ("kv", "ML",       "PyTorch · TransformerLens · RAG"),
    ("kv", "Uni",      "PES University · CSE '28"),
    ("kv", "CGPA",     "7.95 / 10"),
    ("blank", "", ""),
    ("head", "", "NOW"),
    ("kv", "Research", "hallucination attribution @ PESU Labs"),
    ("kv", "Studying", "audit coverage for AI safety evals"),
    ("kv", "Asking",   "how models introspect, and break"),
    ("blank", "", ""),
    ("head", "", "HONOURS"),
    ("kv", "",         "Top 25% cohort scholarship · Sem 1"),
    ("kv", "",         "Academic Distinction · Sem 2 & 4"),
    ("blank", "", ""),
    ("head", "", "HACKATHONS"),
    ("kv", "Razorpay", "AI Buildathon · LIFT"),
    ("kv", "GCloud",   "Agentic Cinema · CallSheet"),
    ("blank", "", ""),
    ("head", "", "OFFLINE"),
    ("kv", "",         "10m air rifle · national level"),
    ("kv", "",         "filter coffee · non-negotiable"),
    ("blank", "", ""),
    ("palette", "", ""),
]


def neofetch():
    t = DARK
    FS, LH = 13.0, 17.2
    CH = FS * 0.6
    PADX, BAR, PADT, GAP = 30, 40, 22, 34
    LABW, RULE = 11, 46
    art_w = max(map(len, ART)) * CH
    ix = PADX + art_w + GAP
    W = round(ix + (LABW + 38) * CH + PADX)
    rows = max(len(ART), len(NEOFETCH))
    H = round(BAR + PADT + rows * LH + 18)
    s = SVG(W, H, "neofetch-style card: OS, editor, languages, university, current research, honours")
    s.rect(0.5, 0.5, W - 1, H - 1, fill=t["bg"], rx=14, stroke=t["line2"])
    s.line(1, BAR, W - 1, BAR, t["line2"])
    for k, c in enumerate(("red", "amber", "green")):
        s.add(f'<circle cx="{24 + k * 18}" cy="{BAR / 2}" r="5" fill="{t[c]}" opacity=".85"/>')
    s.text(W / 2, BAR / 2 + 4.5, "~/whoami — neofetch", alias="mono", size=12.5, fill=t["muted"], anchor="middle")
    s.css.append(".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}" + REDUCED_MOTION)

    y0 = BAR + PADT + FS
    fills = {"cat": t["amber"], "hi": "#34343C", "lo": "#1F1F26"}
    for i, ln in enumerate(ART):
        runs, buf, mode = [], "", None
        for c in ln:
            m = "cat" if c in "%#@*" else "hi" if c in "=-+" else "lo"
            if m != mode and buf:
                runs.append((buf, fills[mode]))
                buf = ""
            buf += c
            mode = m
        runs.append((buf, fills[mode]))
        s.text(PADX, y0 + i * LH, runs, alias="mono", size=FS)

    for i, (kind, lab, val) in enumerate(NEOFETCH):
        y = y0 + i * LH
        if kind == "user":
            s.text(ix, y, [("santosh", t["cyan"]), ("@", t["muted"]), ("github", t["cyan"])],
                   alias="mono-b", size=FS)
            s.rect(ix + 15 * CH, y - FS + 2, CH, FS, fill=t["ink"], extra='class="blink"')
        elif kind == "rule":
            s.text(ix, y, "─" * RULE, alias="mono", size=FS, fill=t["faint"])
        elif kind == "head":
            s.text(ix, y, [(val, t["cyan"], "mono-b"), (" " + "─" * (RULE - len(val) - 1), t["faint"])],
                   alias="mono", size=FS)
        elif kind == "kv":
            s.text(ix, y, [(lab.ljust(LABW) if lab else "", t["muted"]), (val, t["ink"])], alias="mono", size=FS)
        elif kind == "palette":
            cols = ["red", "amber", "green", "cyan", "blue", "violet", "pink", "ink"]
            for k, c in enumerate(cols):
                s.rect(ix + k * 3 * CH, y - FS + 1.5, 2 * CH, FS, fill=t[c], rx=1.5)
    s.save(OUT / "neofetch.svg")


# ════════════════════════════════════════════════════════════════════════════
def main():
    for t in THEMES:
        hero(t)
        for sid, num, title, note in SECTIONS:
            section(t, sid, num, title, note)
        for i, p in enumerate(PROJECTS, 1):
            card(t, i, p)
        for i, m in enumerate(MORE, 13):
            row(t, i, m)
        toolbox(t)
        for slug, label, value in LINKS:
            button(t, slug, label, value)
        footer(t)
    neofetch()
    n = len(list(OUT.rglob("*.svg")))
    size = sum(f.stat().st_size for f in OUT.rglob("*.svg"))
    print(f"wrote {n} svgs, {size / 1024:.0f} KiB total")


if __name__ == "__main__":
    main()
