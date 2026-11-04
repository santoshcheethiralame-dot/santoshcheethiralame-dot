"""Tiny SVG toolkit for the neofetch card.

Fonts are subset to the glyphs the file actually uses and embedded as WOFF2,
because an SVG shown through an <img> tag cannot load anything from the
network.

Requires: fonttools, brotli   (pip install fonttools brotli)
"""
from __future__ import annotations

import base64
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"

# ── type ────────────────────────────────────────────────────────────────────
# family alias -> (file, generic fallback)
FONTS = {
    "mono":   ("JetBrainsMono-Regular.ttf", "monospace"),
    "mono-b": ("JetBrainsMono-Bold.ttf",    "monospace"),
}
FALLBACK = {
    "monospace": "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
    "sans-serif": "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif",
}

_tt: dict[str, TTFont] = {}


def _font(alias: str) -> TTFont:
    if alias not in _tt:
        _tt[alias] = TTFont(FONT_DIR / FONTS[alias][0])
    return _tt[alias]


def measure(s: str, alias: str, size: float, ls: float = 0.0) -> float:
    """Advance width of `s` in px at `size`, plus letter-spacing `ls` per glyph."""
    f = _font(alias)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    w = 0
    for ch in s:
        g = cmap.get(ord(ch)) or cmap.get(ord("?"))
        w += hmtx[g][0]
    return w * size / upm + ls * len(s)


def wrap(s: str, alias: str, size: float, max_w: float) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if measure(trial, alias, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


# ── palette ─────────────────────────────────────────────────────────────────
# One warm-terminal identity: amber + cyan on near-black, ink on paper.
DARK = dict(
    name="dark",
    bg="#0B0B0D", panel="#111115", raise_="#17171C", line="#24242B", line2="#2E2E36",
    ink="#ECE7DC", body="#B9B4AA", muted="#8A8A93", faint="#55555E", ghost="#1C1C22",
    amber="#FFB454", cyan="#4FD6E5", green="#7FD962", pink="#F27FB1",
    violet="#B58CF2", red="#F25C54", blue="#6CA8FF",
)
LIGHT = dict(
    name="light",
    bg="#FBF8F2", panel="#F4EFE5", raise_="#FFFFFF", line="#E4DDCF", line2="#D6CDBC",
    ink="#17171B", body="#45444A", muted="#6E6C72", faint="#A29D92", ghost="#EDE7DB",
    amber="#B4630B", cyan="#0A7886", green="#3C8527", pink="#B5386F",
    violet="#6C49C2", red="#C23B33", blue="#2F64C8",
)
THEMES = (DARK, LIGHT)


# ── canvas ──────────────────────────────────────────────────────────────────
class SVG:
    """Collects elements, tracks which glyphs each font needs, emits one file."""

    def __init__(self, w: int, h: int, title: str = ""):
        self.w, self.h, self.title = w, h, title
        self.defs: list[str] = []
        self.css: list[str] = []
        self.body: list[str] = []
        self.used: dict[str, set[str]] = {}

    # raw
    def add(self, s: str):
        self.body.append(s)

    def rect(self, x, y, w, h, fill="none", rx=0, stroke=None, sw=1, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" '
                 f'fill="{fill}"{st} {extra}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=1, extra=""):
        self.add(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
                 f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    # text — runs is either a str or a list of (str, fill[, alias]) spans
    def text(self, x, y, runs, alias="mono", size=14, fill="#fff", anchor="start",
             ls=0.0, extra="", cls=""):
        if isinstance(runs, str):
            runs = [(runs, fill)]
        spans = []
        for r in runs:
            s, f = r[0], r[1]
            a = r[2] if len(r) > 2 else alias
            self.used.setdefault(a, set()).update(s)
            fam = "" if a == alias else f' font-family="{self.family(a)}"'
            spans.append(f'<tspan fill="{f}"{fam}>{esc(s)}</tspan>')
        ls_attr = f' letter-spacing="{ls:g}"' if ls else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<text x="{x:g}" y="{y:g}" font-family="{self.family(alias)}" '
                 f'font-size="{size:g}" text-anchor="{anchor}"{ls_attr}{c} '
                 f'xml:space="preserve" {extra}>{"".join(spans)}</text>')

    @staticmethod
    def family(alias: str) -> str:
        return f"{alias},{FALLBACK[FONTS[alias][1]]}".replace('"', "'")

    # output
    def _font_css(self) -> str:
        out = []
        for alias, chars in sorted(self.used.items()):
            chars = set(chars) | {" "}
            opts = subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["kern", "liga", "calt", "tnum"]
            opts.name_IDs = []
            opts.notdef_outline = True
            ft = TTFont(FONT_DIR / FONTS[alias][0])
            sub = subset.Subsetter(opts)
            sub.populate(text="".join(sorted(chars)))
            sub.subset(ft)
            buf = io.BytesIO()
            ft.flavor = "woff2"
            ft.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            out.append(f"@font-face{{font-family:{alias};"
                       f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        return "".join(out)

    def render(self) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img"'
                + (f' aria-label="{esc(self.title)}"' if self.title else "") + ">")
        parts = [head]
        if self.title:
            parts.append(f"<title>{esc(self.title)}</title>")
        css = self._font_css() + "text{font-kerning:normal}" + "".join(self.css)
        parts.append(f"<style>{css}</style>")
        if self.defs:
            parts.append("<defs>" + "".join(self.defs) + "</defs>")
        parts += self.body
        parts.append("</svg>")
        return "\n".join(parts)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.render(), encoding="utf-8")


REDUCED_MOTION = ("@media (prefers-reduced-motion:reduce){*{animation:none!important}"
                  ".rm-show{opacity:1!important}}")
