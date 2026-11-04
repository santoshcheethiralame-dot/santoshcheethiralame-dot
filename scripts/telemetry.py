#!/usr/bin/env python3
"""Rewrite the telemetry block in README.md as plain ascii.

Everything between <!-- telemetry:start --> and <!-- telemetry:end --> is
replaced. Run daily by .github/workflows/telemetry.yml.

    GITHUB_TOKEN=... python scripts/telemetry.py
    python scripts/telemetry.py --sample      # fake data, prints only

stdlib only. With the default Actions token only public activity counts;
add a PAT (read:user, repo) as the STATS_TOKEN secret for private too.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import urllib.request
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- telemetry:start -->", "<!-- telemetry:end -->"

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
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

SKIP = {"Jupyter Notebook", "HTML", "CSS", "Makefile", "Dockerfile", "Shell",
        "PowerShell", "Batchfile", "ShaderLab", "HLSL", "Mermaid"}


def fetch(login: str, token: str) -> dict:
    after, repos, user = None, [], None
    while True:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": QUERY, "variables": {"login": login, "after": after}}).encode(),
            headers={"Authorization": f"bearer {token}", "User-Agent": "profile-telemetry"})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.load(r)
        if body.get("errors"):
            raise SystemExit(f"GraphQL error: {body['errors']}")
        u = body["data"]["user"]
        user = user or u
        repos += u["repositories"]["nodes"]
        pi = u["repositories"]["pageInfo"]
        if not pi["hasNextPage"]:
            break
        after = pi["endCursor"]
    cc = user["contributionsCollection"]
    langs: dict[str, int] = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            if e["node"]["name"] not in SKIP:
                langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return dict(
        days=[(d["date"], d["contributionCount"])
              for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]],
        total=cc["contributionCalendar"]["totalContributions"],
        commits=cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        prs=cc["totalPullRequestContributions"],
        repos=user["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in repos),
        langs=langs,
    )


def sample() -> dict:
    rnd = random.Random(7)
    today = dt.date.today()
    days = []
    for i in range(371):
        d = today - dt.timedelta(days=370 - i)
        c = 0 if rnd.random() < .3 else int(rnd.expovariate(.25) * (3 if d.month in (7, 8, 10) else 1))
        days.append((d.isoformat(), c))
    return dict(days=days, total=sum(c for _, c in days), commits=1460, prs=38, repos=51, stars=1,
                langs={"Python": 52, "TypeScript": 41, "JavaScript": 19, "Rust": 6, "Go": 4, "C": 2, "C#": 1})


def streaks(days):
    best = cur = 0
    for _, c in days:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    seq = days[:-1] if days and days[-1][1] == 0 else days   # today isn't over yet
    run = 0
    for _, c in reversed(seq):
        if not c:
            break
        run += 1
    return run, best


def render(d: dict) -> str:
    # one horizontal bar per month: survives GitHub's line-height, and any
    # monospace font has full blocks and light shade
    months: dict[str, int] = {}
    for date, c in d["days"][-365:]:
        key = date[:7]
        months[key] = months.get(key, 0) + c
    keys = sorted(months)[-12:]
    mx = max(months[k] for k in keys) or 1
    W = 28
    chart = []
    for k in keys:
        v = months[k]
        n = round(v / mx * W)
        if v and not n:
            n = 1
        name = dt.date.fromisoformat(k + "-01").strftime("%b %y").lower()
        chart.append(f"  {name:<12}{'█' * n}{'░' * (W - n)}  {v:>6,}")
    cur, best = streaks(d["days"])
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
    lang_lines = []
    for name, v in top:
        f = v / total
        n = round(f * W)
        lang_lines.append(f"  {name:<12}{'█' * n}{'░' * (W - n)}  {f * 100:5.1f}%")

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = [
        "```text",
        f"  contributions   {d['total']:,}",
        f"  commits         {d['commits']:,}   ·   pull requests {d['prs']:,}",
        f"  streak          {cur}d now   ·   best {best}d",
        f"  repos           {d['repos']:,}   ·   stars {d['stars']:,}",
        "",
        "  contributions by month",
        *chart,
        "",
        "  languages (bytes, own repos)",
        *lang_lines,
        "",
        f"  # regenerated {stamp} by .github/workflows/telemetry.yml",
        "```",
    ]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="santoshcheethiralame-dot")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()
    if a.sample:
        print(render(sample()))
        return
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("set GITHUB_TOKEN (or pass --sample)")
    block = render(fetch(a.user, token))
    text = README.read_text(encoding="utf-8")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 lambda _: f"{START}\n{block}\n{END}", text, flags=re.S)
    if new == text:
        raise SystemExit("telemetry markers not found in README.md")
    README.write_text(new, encoding="utf-8")
    print("README telemetry updated")


if __name__ == "__main__":
    main()
