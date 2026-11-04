#!/usr/bin/env python3
"""Build assets/neofetch.svg: the ascii cat + info panel.

    pip install -r scripts/requirements.txt
    python scripts/neofetch.py

Edit NEOFETCH below and re-run. Fonts are subset and embedded so the card
renders the same everywhere GitHub shows it.
"""
from svgkit import DARK, REDUCED_MOTION, ROOT, SVG

OUT = ROOT / "assets"

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


if __name__ == "__main__":
    neofetch()
    print("wrote assets/neofetch.svg")
