#!/usr/bin/env python3
"""Render the TELEMETRY card from live GitHub data (dark + light).

Run by .github/workflows/stats.yml every day; output lands on the
`output-stats` branch so main's history stays clean.

    GITHUB_TOKEN=... python scripts/build_stats.py --user <login> --out dist
    python scripts/build_stats.py --sample --out dist     # offline preview

With the default Actions token only public activity is counted. Add a
classic PAT (read:user, repo) as the STATS_TOKEN secret to include private
contributions and languages from private repos.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import urllib.request

from svgkit import DARK, THEMES, SVG, measure

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""

SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS", "Makefile", "Dockerfile", "Shell",
              "PowerShell", "Batchfile", "ShaderLab", "HLSL"}


def gql(token: str, variables: dict) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def fetch(login: str, token: str) -> dict:
    user, after, repos = None, None, []
    while True:
        u = gql(token, {"login": login, "after": after})
        user = user or u
        repos += u["repositories"]["nodes"]
        pi = u["repositories"]["pageInfo"]
        if not pi["hasNextPage"]:
            break
        after = pi["endCursor"]

    days = [d for w in user["contributionsCollection"]["contributionCalendar"]["weeks"]
            for d in w["contributionDays"]]
    langs: dict[str, int] = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n not in SKIP_LANGS:
                langs[n] = langs.get(n, 0) + e["size"]
    cc = user["contributionsCollection"]
    return dict(
        days=[(d["date"], d["contributionCount"]) for d in days],
        total=cc["contributionCalendar"]["totalContributions"],
        commits=cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        prs=cc["totalPullRequestContributions"],
        repos=user["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in repos),
        langs=langs,
    )


def sample() -> dict:
    rnd = random.Random(7)
    today = dt.date(2026, 11, 4)
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    days = []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        boost = 3 if d.month in (7, 8, 10) else 1
        c = 0 if rnd.random() < 0.25 else int(rnd.expovariate(0.25) * boost)
        days.append((d.isoformat(), c))
    return dict(days=days, total=sum(c for _, c in days), commits=1460, prs=38, repos=51, stars=1,
                langs={"Python": 5_200_000, "TypeScript": 4_100_000, "JavaScript": 1_900_000,
                       "Rust": 640_000, "Go": 420_000, "C": 210_000, "C#": 120_000, "WGSL": 60_000})


def streaks(days: list[tuple[str, int]]) -> tuple[int, int]:
    longest = cur = 0
    for _, c in days:
        cur = cur + 1 if c else 0
        longest = max(longest, cur)
    # today may still be empty — don't break the streak on it
    run, seq = 0, list(days)
    if seq and seq[-1][1] == 0:
        seq = seq[:-1]
    for _, c in reversed(seq):
        if not c:
            break
        run += 1
    return run, longest


def fmt(n: int) -> str:
    return f"{n:,}"


def render(t: dict, data: dict, out: str):
    W, H = 1200, 340
    s = SVG(W, H, f"{fmt(data['total'])} contributions in the last year")
    s.rect(0.5, 0.5, W - 1, H - 1, fill=t["panel"], rx=14, stroke=t["line"])
    cur, best = streaks(data["days"])

    # ── tiles
    tiles = [
        (fmt(data["total"]), "CONTRIBUTIONS", "last 12 months", "amber"),
        (f"{cur}d", "CURRENT STREAK", f"best {best} days", "cyan"),
        (fmt(data["commits"]), "COMMITS", f"{fmt(data['prs'])} pull requests", "green"),
        (fmt(data["repos"]), "REPOSITORIES", f"{fmt(data['stars'])} stars", "pink"),
    ]
    x0, tw = 32, 176
    for i, (v, lab, sub, key) in enumerate(tiles):
        x = x0 + i * (tw + 8)
        if i:
            s.line(x - 4, 36, x - 4, 112, t["line"])
        pad = 0 if i == 0 else 16
        s.rect(x + pad, 38, 8, 8, fill=t[key], rx=1.5)
        s.text(x + pad + 16, 46, lab, alias="mono-b", size=10.5, fill=t["muted"], ls=1.6)
        s.text(x + pad - 1, 88, v, alias="mono-b", size=32, fill=t["ink"])
        s.text(x + pad, 110, sub, alias="mono", size=11.5, fill=t["faint"])

    # ── weekly bars
    days = data["days"]
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)][-52:]
    totals = [sum(c for _, c in w) for w in weeks]
    mx = max(totals) or 1
    bx, by, bw, bh = 32, 146, 712, 128
    gap = 3
    cw = (bw - gap * (len(weeks) - 1)) / len(weeks)
    s.text(bx, by - 4, "PER WEEK", alias="mono-b", size=10, fill=t["faint"], ls=1.6)
    s.text(bx + bw, by - 4, f"peak {mx}", alias="mono", size=10.5, fill=t["faint"], anchor="end")
    base = by + 14 + bh
    for k in range(4):
        yy = base - k * bh / 3
        s.line(bx, yy, bx + bw, yy, t["line"], extra='stroke-dasharray="1 4"' if k else "")
    for i, v in enumerate(totals):
        h = max(2.0, v / mx * bh) if v else 1.5
        last = i == len(totals) - 1
        col = t["cyan"] if last else t["amber"]
        op = 1 if last else 0.35 + 0.65 * (v / mx)
        s.rect(bx + i * (cw + gap), base - h, cw, h, fill=col, rx=1.5, extra=f'opacity="{op:.2f}"')
    seen = None
    for i, w in enumerate(weeks):
        m = dt.date.fromisoformat(w[0][0]).strftime("%b").lower()
        if m != seen and i < len(weeks) - 2:
            s.text(bx + i * (cw + gap), base + 18, m, alias="mono", size=10.5, fill=t["faint"])
            seen = m

    # ── languages
    lx, lw = 788, 380
    s.line(lx - 20, 36, lx - 20, 304, t["line"])
    s.text(lx, 46, "LANGUAGES", alias="mono-b", size=10.5, fill=t["muted"], ls=1.6)
    s.text(lx + lw, 46, "by bytes · own repos", alias="mono", size=11, fill=t["faint"], anchor="end")
    total = sum(data["langs"].values()) or 1
    top = sorted(data["langs"].items(), key=lambda kv: -kv[1])[:7]
    rest = total - sum(v for _, v in top)
    if rest > 0:
        top.append(("other", rest))
    cols = ["amber", "cyan", "green", "pink", "violet", "blue", "red", "faint"]
    x = lx
    s.defs.append(f'<clipPath id="lb"><rect x="{lx}" y="66" width="{lw}" height="12" rx="6"/></clipPath>')
    s.add('<g clip-path="url(#lb)">')
    for i, (n, v) in enumerate(top):
        w = v / total * lw
        s.rect(x, 66, max(w - 2, 0.5) if i < len(top) - 1 else w, 12, fill=t[cols[i]])
        x += w
    s.add("</g>")
    for i, (n, v) in enumerate(top):
        col, row = i % 2, i // 2
        xx = lx + col * (lw / 2 + 10)
        yy = 112 + row * 34
        s.rect(xx, yy - 9, 9, 9, fill=t[cols[i]], rx=2)
        s.text(xx + 18, yy, n, alias="mono-m", size=13, fill=t["ink"])
        s.text(xx + lw / 2 - 10, yy, f"{v / total * 100:.1f}%", alias="mono", size=12.5,
               fill=t["muted"], anchor="end")

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    s.text(lx, 316, f"updated {stamp}", alias="mono", size=10.5, fill=t["faint"])
    s.text(lx + lw, 316, "scripts/build_stats.py", alias="mono", size=10.5, fill=t["faint"], anchor="end")
    s.save(__import__("pathlib").Path(out) / f"stats-{t['name']}.svg")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="santoshcheethiralame-dot")
    ap.add_argument("--out", default="dist")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()
    if a.sample:
        data = sample()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("set GITHUB_TOKEN (or pass --sample)")
        data = fetch(a.user, token)
    for t in THEMES:
        render(t, data, a.out)
    print(f"{data['total']} contributions · {data['repos']} repos · {len(data['langs'])} languages")


if __name__ == "__main__":
    main()
