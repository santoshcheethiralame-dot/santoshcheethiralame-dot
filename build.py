#!/usr/bin/env python3
# builds neofetch.svg from the original ascii art + restructured info panel

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

#// palette
BG      = "#0B0B0D"
BORDER  = "#2E2E33"
DIM_HI  = "#33333B"   # texture: = - +
DIM_LO  = "#1F1F25"   # texture: : .
AMBER   = "#FFB454"   # the cat
CYAN    = "#4FD6E5"   # username + section headers
CREAM   = "#E8E3D8"   # values
GREY    = "#8A8A93"   # labels
FAINT   = "#55555E"   # rules / leaders
PALETTE = ["#F25C54", "#FFB454", "#7FD962", "#4FD6E5", "#6CA8FF", "#B58CF2", "#F27FB1", "#E8E3D8"]

ART_CHARS = set("%#@*")

#// info panel  (style, label, value) — label "" means full-line value
H, L, R, B, P = "header", "label", "rule", "blank", "palette"
RULE = "─" * 47

INFO = [
    ("user",  "", "santosh@github"),
    (R, "", RULE),
    (L, "OS",        "Windows 11 · zsh + starship"),
    (L, "Editor",    "VSCode · Neovim"),
    (L, "Langs",     "TypeScript · Python · C · WGSL"),
    (L, "Web",       "React · Astro · Tailwind · Vite"),
    (L, "ML",        "PyTorch · TransformerLens · RAG"),
    (L, "Systems",   "WebGPU · Docker"),
    (L, "Uni",       "PES University · CSE '28"),
    (L, "CGPA",      "7.95 / 10"),
    (B, "", ""),
    (H, "", "NOW"),
    (L, "Research",  "hallucination attribution @ PESU Labs"),
    (L, "Building",  "GlassBox · portfolio v2"),
    (B, "", ""),
    (H, "", "HONOURS"),
    (L, "", "Top 25% cohort scholarship · Sem 1"),
    (L, "", "Academic Distinction · Sem 2 & 4"),
    (B, "", ""),
    (H, "", "PROJECTS"),
    (L, "GlassBox",  "GPT-2 interpretability microscope"),
    (L, "Gradient",  "neural nets in-browser · WebGPU"),
    (L, "Orbit",     "local-first study PWA · shipped"),
    (B, "", ""),
    (H, "", "OFFLINE"),
    (L, "", "10m air rifle · national level"),
    (L, "", "filter coffee · non-negotiable"),
    (P, "", ""),
]

#// geometry
FS      = 12.5
CH      = FS * 0.6019      # monospace advance
LH      = 16.5
PAD_X   = 26
PAD_TOP = 18
BAR_H   = 36
GAP     = 30

art_w   = max(len(l) for l in ART) * CH
info_x  = PAD_X + art_w + GAP
label_w = 11                # chars reserved for label column
info_w  = max(
    (label_w if lab else 0) * CH + len(val) * CH
    for _, lab, val in [(s, l, v) for s, l, v in INFO]
)
rows    = max(len(ART), len(INFO))
width   = round(info_x + info_w + PAD_X)
height  = round(BAR_H + PAD_TOP + rows * LH + 20)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def art_line(line: str) -> str:
    # split into runs: cat chars amber, texture in two dim shades
    def cls(c):
        if c in ART_CHARS: return "cat"
        if c in "=-+":     return "hi"
        return "lo"
    out, buf, mode = [], [], None
    for c in line:
        m = cls(c)
        if m != mode and buf:
            out.append((mode, "".join(buf)))
            buf = []
        buf.append(c)
        mode = m
    if buf:
        out.append((mode, "".join(buf)))
    fills = {"cat": AMBER, "hi": DIM_HI, "lo": DIM_LO}
    return "".join(f'<tspan fill="{fills[m]}">{esc(run)}</tspan>' for m, run in out)


svg = []
svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}" font-family="\'SFMono-Regular\',Consolas,'
    f'\'Liberation Mono\',Menlo,\'DejaVu Sans Mono\',monospace" font-size="{FS}">'
)
svg.append(
    "<style>"
    "text{white-space:pre}"
    ".blink{animation:bl 1.1s steps(1) infinite}"
    "@keyframes bl{50%{opacity:0}}"
    "@media (prefers-reduced-motion: reduce){.blink{animation:none}}"
    "</style>"
)

#// card + title bar
svg.append(f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>')
svg.append(f'<line x1="1" y1="{BAR_H}" x2="{width-1}" y2="{BAR_H}" stroke="{BORDER}" stroke-width="2"/>')
for i, c in enumerate(["#F25C54", "#FFB454", "#7FD962"]):
    svg.append(f'<circle cx="{24 + i*20}" cy="{BAR_H/2 + 1}" r="5.5" fill="{c}" opacity="0.85"/>')
svg.append(f'<text x="{width/2}" y="{BAR_H/2 + 5}" text-anchor="middle" fill="{GREY}">~/whoami — neofetch</text>')

#// left column: the cat
y0 = BAR_H + PAD_TOP + FS
for i, line in enumerate(ART):
    svg.append(f'<text x="{PAD_X}" y="{y0 + i*LH:.1f}" xml:space="preserve">{art_line(line)}</text>')

#// right column: info
for i, (style, lab, val) in enumerate(INFO):
    y = y0 + i * LH
    if style == B:
        continue
    if style == "user":
        svg.append(
            f'<text x="{info_x:.1f}" y="{y:.1f}" font-weight="bold">'
            f'<tspan fill="{CYAN}">santosh</tspan><tspan fill="{GREY}">@</tspan>'
            f'<tspan fill="{CYAN}">github</tspan>'
            f'<tspan fill="{CREAM}" class="blink"> ▌</tspan></text>'
        )
    elif style == R:
        svg.append(f'<text x="{info_x:.1f}" y="{y:.1f}" fill="{FAINT}">{val}</text>')
    elif style == H:
        pad = "─" * (47 - len(val) - 4)
        svg.append(
            f'<text x="{info_x:.1f}" y="{y:.1f}" xml:space="preserve">'
            f'<tspan fill="{CYAN}" font-weight="bold">{esc(val)}</tspan>'
            f'<tspan fill="{FAINT}"> ── {pad}</tspan></text>'
        )
    elif style == P:
        blocks = "".join(f'<tspan fill="{c}">██ </tspan>' for c in PALETTE)
        svg.append(f'<text x="{info_x:.1f}" y="{y:.1f}" xml:space="preserve">{blocks}</text>')
    elif style == L:
        if lab:
            padded = lab.ljust(label_w)
            svg.append(
                f'<text x="{info_x:.1f}" y="{y:.1f}" xml:space="preserve">'
                f'<tspan fill="{GREY}">{esc(padded)}</tspan>'
                f'<tspan fill="{CREAM}">{esc(val)}</tspan></text>'
            )
        else:
            svg.append(f'<text x="{info_x:.1f}" y="{y:.1f}" fill="{CREAM}" xml:space="preserve">{esc(val)}</text>')

svg.append("</svg>")

with open("/home/claude/profile/neofetch.svg", "w") as f:
    f.write("\n".join(svg))

print(f"size {width}x{height}  art_lines {len(ART)}  info_lines {len(INFO)}")
print("art widths:", sorted(set(len(l) for l in ART)))
