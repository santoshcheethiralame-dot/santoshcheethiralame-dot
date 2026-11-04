#!/usr/bin/env python3
"""Build the coloured terminal bits of the README (dark + light).

    pip install -r scripts/requirements.txt
    python scripts/build.py

Everything else in README.md is plain text; edit it directly.
"""
from __future__ import annotations

from svgkit import REDUCED_MOTION, ROOT, SVG, THEMES, measure

OUT = ROOT / "assets"
SITE = "https://santoshcheethirala.vercel.app"

BANNER = """\
  █████████    █████████   ██████   █████ ███████████    ███████     █████████  █████   █████
 ███░░░░░███  ███░░░░░███ ░░██████ ░░███ ░█░░░███░░░█  ███░░░░░███  ███░░░░░███░░███   ░░███
░███    ░░░  ░███    ░███  ░███░███ ░███ ░   ░███  ░  ███     ░░███░███    ░░░  ░███    ░███
░░█████████  ░███████████  ░███░░███░███     ░███    ░███      ░███░░█████████  ░███████████
 ░░░░░░░░███ ░███░░░░░███  ░███ ░░██████     ░███    ░███      ░███ ░░░░░░░░███ ░███░░░░░███
 ███    ░███ ░███    ░███  ░███  ░░█████     ░███    ░░███     ███  ███    ░███ ░███    ░███
░░█████████  █████   █████ █████  ░░█████    █████    ░░░███████░  ░░█████████  █████   █████
 ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░    ░░░░░    ░░░░░       ░░░░░░░     ░░░░░░░░░  ░░░░░   ░░░░░""".split("\n")

# what goes after "❯ building " — each phrase gets its own colour
TYPED = [
    ("distributed databases in std-only rust", "amber"),
    ("microscopes for language models", "cyan"),
    ("agents that actually follow the rules", "green"),
    ("neural nets out of webgpu shaders", "pink"),
    ("ways to break couchbase on purpose", "violet"),
]

# tmux status bar: (file, label, colour, link)
BAR = [
    ("session",   "[santosh]",      "amber",  "https://github.com/santoshcheethiralame-dot"),
    ("portfolio", "1:portfolio*",   "cyan",   SITE),
    ("linkedin",  "2:linkedin",     "blue",   "https://www.linkedin.com/in/santoshcheethirala/"),
    ("resume",    "3:resume",       "pink",   f"{SITE}/resume"),
    ("email",     "4:mail",         "green",  "mailto:santoshcheethirala.me@gmail.com"),
]

# git branch --list 'resume/*'   (branch, pdf, note)
RESUMES = [
    ("swe-backend",   "SWE_Backend",   "the general read · tessera, GlassBox, BATCH"),
    ("ml-research",   "ML_Research",   "interpretability, RAG reliability · DRAGNET, GlassBox"),
    ("systems-infra", "Systems_Infra", "storage, consensus · highwater, tessera"),
    ("fintech-data",  "Fintech_Data",  "payments, fraud, causal measurement · Untangle, LIFT"),
    ("sdet-quality",  "SDET_Quality",  "testing, fault injection · highwater, tessera"),
    ("security",      "Security",      "correctness, assurance · highwater, Untangle"),
]
BRANCH_COLOURS = ["green", "cyan", "amber", "pink", "violet", "blue"]

# section prompts: (file, cwd, command)
PROMPTS = [
    ("about",     "~",          "cat santosh.py"),
    ("projects",  "~/projects", "tree -L 2"),
    ("now",       "~",          "git diff HEAD~1 -- now.md"),
    ("resume",    "~/resume",   "git branch --list 'resume/*'"),
    ("loop",      "~/life",     "cat src/main.rs"),
    ("telemetry", "~",          "./telemetry --since 1y"),
    ("snake",     "~",          "snake --eat ~/.contributions"),
    ("exit",      "~",          "exit"),
]

ON_ACCENT = {"dark": "#0B0B0D", "light": "#FFFFFF"}


# ── banner + typed line ─────────────────────────────────────────────────────
def banner(t: dict):
    fs = 13.0
    cw, lh = fs * 0.6, fs * 1.32           # JetBrains Mono: block glyph is exactly 1.32em tall
    cols = max(map(len, BANNER))
    PADX, PADT = 4, 6
    bw = cols * cw
    W = int(PADX * 2 + bw)
    y_type = PADT + len(BANNER) * lh + 80
    H = int(y_type + 34)
    s = SVG(W, H, "SANTOSH, in ascii block letters. Sai Santosh Cheethirala, CS at PES University, Bengaluru.")
    stops = [t["amber"], t["pink"], t["violet"], t["cyan"], t["amber"]]
    s.defs.append(
        f'<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{bw * 1.6:.0f}" y2="0" '
        f'spreadMethod="repeat">'
        + "".join(f'<stop offset="{i / (len(stops) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
        + f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{bw * 1.6:.0f} 0" '
          f'dur="14s" repeatCount="indefinite"/></linearGradient>')
    shade = t["line2"]
    top = PADT
    for i, row in enumerate(BANNER):
        # full blocks as merged rects (text glyphs leave hairline seams),
        # shade characters stay as text so they keep their texture
        x = 0
        while x < len(row):
            if row[x] == "█":
                e = x
                while e < len(row) and row[e] == "█":
                    e += 1
                # whole-pixel rows overlapping by 1px, so no anti-aliased seam
                y0, y1_ = round(top + i * lh), round(top + (i + 1) * lh)
                s.rect(PADX + x * cw, y0, (e - x) * cw, y1_ - y0 + (1 if i < len(BANNER) - 1 else 0),
                       fill="url(#g)", extra='shape-rendering="crispEdges"')
                x = e
            else:
                x += 1
        shades = "".join(ch if ch == "░" else " " for ch in row)
        if shades.strip():
            s.text(PADX, top + i * lh + fs * 1.02, shades, alias="mono", size=fs, fill=shade)

    y1 = PADT + len(BANNER) * lh + 22
    s.text(PADX + 2, y1, [("sai santosh cheethirala", t["ink"], "mono-b"),
                          ("  ·  ", t["faint"]), ("cs @ pes university", t["body"]),
                          ("  ·  ", t["faint"]), ("bengaluru", t["body"])], alias="mono", size=13)
    y2 = y1 + 22
    s.text(PADX + 2, y2, [("● ", t["green"]), ("interning @ pesu i-labs", t["body"]),
                          ("  ·  ", t["faint"]), ("open to summer '27 internships", t["green"])],
           alias="mono", size=13)

    # line 2: ❯ building <typed phrase>
    x0 = PADX + 2
    s.text(x0, y_type, [("❯ ", t["amber"], "mono-b"), ("building ", t["muted"])], alias="mono", size=16)
    tx = x0 + measure("❯ building ", "mono", 16)
    N, slot = len(TYPED), 4.6
    T = N * slot
    s.defs.append(f'<clipPath id="tc"><rect x="{tx - 2:.1f}" y="{y_type - 20}" width="{W - tx}" height="30"/></clipPath>')
    s.add('<g clip-path="url(#tc)">')
    for i, (phrase, col) in enumerate(TYPED):
        w = measure(phrase, "mono", 16)
        st, L = i * 100 / N, 100 / N
        vis = {0.0: 1 if i == 0 else 0, st + L: 0, 100.0: 0}
        if i:
            vis[st] = 1
        p = lambda x: f"{max(0, min(100, x)):.3f}%"
        s.css.append(f"@keyframes v{i}{{" + "".join(f"{p(k)}{{opacity:{v}}}" for k, v in sorted(vis.items()))
                     + f"}}.v{i}{{opacity:{1 if i == 0 else 0};animation:v{i} {T}s step-end infinite}}")
        n = len(phrase)
        s.css.append(
            f"@keyframes c{i}{{0%{{transform:translateX(0)}}"
            f"{p(st)}{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{p(st + L * .45)}{{transform:translateX({w:.1f}px);animation-timing-function:linear}}"
            f"{p(st + L * .86)}{{transform:translateX({w:.1f}px);animation-timing-function:steps({max(1, n // 3)},end)}}"
            f"{p(st + L * .97)}{{transform:translateX(0)}}100%{{transform:translateX(0)}}}}"
            f".c{i}{{animation:c{i} {T}s infinite}}")
        # a mask slides right to "type" and back to "delete"; transparent, so
        # it works on every GitHub theme
        s.defs.append(f'<mask id="m{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                      f'<rect class="c{i}" x="{tx - 2000:.1f}" y="0" width="2000" height="{H}" fill="#fff"/></mask>')
        s.add(f'<g class="v{i}"><g mask="url(#m{i})">')
        s.text(tx, y_type, phrase, alias="mono", size=16, fill=t[col])
        s.add(f'</g><rect class="c{i}" x="{tx + 1:.1f}" y="{y_type - 14}" width="9" height="18" '
              f'fill="{t[col]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" '
              f'dur="1s" repeatCount="indefinite"/></rect></g>')
    s.add("</g>")
    s.css.append(REDUCED_MOTION)
    s.save(OUT / f"banner-{t['name']}.svg")


# ── tmux status bar (one image per segment so each is a link) ───────────────
def bar(t: dict):
    H, A, P = 30, 13, 14          # height, arrow width, text padding
    for i, (slug, label, col, _) in enumerate(BAR):
        nxt = t[BAR[i + 1][2]] if i + 1 < len(BAR) else None
        tw = measure(label, "mono-b", 13)
        W = int(P + tw + P + A)
        s = SVG(W, H, label)
        body = W - A
        if i == 0:
            s.rect(0, 0, body + 6, H, fill=t[col], rx=6)
        else:
            s.rect(0, 0, body, H, fill=t[col])
        if nxt:
            s.rect(body, 0, A, H, fill=nxt)
        s.add(f'<polygon points="{body},0 {W},{H / 2} {body},{H}" fill="{t[col]}"/>')
        s.text(P, H / 2 + 4.6, label, alias="mono-b", size=13, fill=ON_ACCENT[t["name"]])
        s.save(OUT / "bar" / f"{slug}-{t['name']}.svg")


# ── shell prompt used as a section heading ──────────────────────────────────
def prompt(t: dict, slug: str, cwd: str, cmd: str):
    H, A = 30, 11
    W = 980
    s = SVG(W, H, f"{cwd} $ {cmd}")
    fg = ON_ACCENT[t["name"]]
    w1 = measure("santosh", "mono-b", 12.5) + 24
    s.rect(0, 0, w1 + 6, H, fill=t["amber"], rx=6)
    s.text(12, H / 2 + 4.4, "santosh", alias="mono-b", size=12.5, fill=fg)
    w2 = measure(cwd, "mono-b", 12.5) + 30
    s.rect(w1, 0, w2, H, fill=t["violet"])
    s.add(f'<polygon points="{w1},0 {w1 + A},{H / 2} {w1},{H}" fill="{t["amber"]}"/>')
    s.text(w1 + A + 9, H / 2 + 4.4, cwd, alias="mono-b", size=12.5, fill=fg)
    x = w1 + w2
    s.add(f'<polygon points="{x},0 {x + A},{H / 2} {x},{H}" fill="{t["violet"]}"/>')
    x += A + 12
    # colour the command like a shell would: program, flags, args, strings
    runs = []
    for k, tok in enumerate(cmd.split(" ")):
        if k == 0:
            c = t["green"]
        elif tok.startswith("-"):
            c = t["cyan"]
        elif tok.startswith("'") or tok.startswith("~"):
            c = t["amber"]
        else:
            c = t["ink"]
        runs.append((("" if k == 0 else " ") + tok, c))
    s.text(x, H / 2 + 5, runs, alias="mono-b", size=14)
    s.save(OUT / "prompt" / f"{slug}-{t['name']}.svg")


# ── git branch rows (one image per résumé so each is a link) ────────────────
def branches(t: dict):
    W, H = 980, 30
    for i, (br, _, note) in enumerate(RESUMES):
        s = SVG(W, H, f"resume/{br}: {note}")
        y = H / 2 + 5
        col = t[BRANCH_COLOURS[i]]
        star = "* " if i == 0 else "  "
        s.text(14, y, [(star, t["green"], "mono-b"), ("resume/", t["muted"]),
                       (br, col, "mono-b")], alias="mono", size=14)
        s.text(14 + measure("* resume/systems-infra", "mono", 14) + 34, y,
               [("# ", t["faint"]), (note, t["body"])], alias="mono", size=13)
        s.text(W - 10, y, [("pdf ", t["faint"]), ("↗", col)], alias="mono", size=13, anchor="end")
        s.save(OUT / "resume" / f"{br}-{t['name']}.svg")


def main():
    for t in THEMES:
        banner(t)
        bar(t)
        for p in PROMPTS:
            prompt(t, *p)
        branches(t)
    n = len(list(OUT.rglob("*.svg")))
    print(f"wrote {n} svgs to assets/")


if __name__ == "__main__":
    main()
