#!/usr/bin/env python3
"""Generate a self-hosted 'Top Languages' donut SVG computed from the real,
current language breakdown of a GitHub user's own (non-fork) repositories.
Replaces the public github-readme-stats.vercel.app widget, which is prone to
503 DEPLOYMENT_PAUSED outages. Stdlib only.
"""
import json
import math
import os
import sys
import urllib.request

API = "https://api.github.com"

# A reasonably broad subset of GitHub's linguist language colors.
LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "HTML": "#e34c26", "CSS": "#563d7c", "Jupyter Notebook": "#DA5B0B",
    "PHP": "#4F5D95", "Dart": "#00B4AB", "C#": "#178600", "Shell": "#89e051",
    "Java": "#b07219", "C++": "#f34b7d", "C": "#555555", "Go": "#00ADD8",
    "Ruby": "#701516", "Rust": "#dea584", "Vue": "#41b883", "SCSS": "#c6538c",
    "Blade": "#f7523f", "Jinja": "#a52a22", "Dockerfile": "#384d54",
    "Kotlin": "#A97BFF", "Swift": "#F05138", "Lua": "#000080",
}
FALLBACK_COLOR = "#8b949e"


def api_get(url: str, token: str):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"bearer {token}" if token else "",
            "Accept": "application/vnd.github+json",
            "User-Agent": "top-languages-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_language_bytes(login: str, token: str) -> dict:
    totals = {}
    page = 1
    while True:
        repos = api_get(
            f"{API}/users/{login}/repos?type=owner&per_page=100&page={page}", token
        )
        if not repos:
            break
        for repo in repos:
            if repo.get("archived"):
                continue
            langs = api_get(
                f"{API}/repos/{repo['full_name']}/languages", token
            )
            for lang, count in langs.items():
                totals[lang] = totals.get(lang, 0) + count
        if len(repos) < 100:
            break
        page += 1
    return totals


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def build_svg(login: str, totals: dict) -> str:
    grand_total = sum(totals.values())
    items = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    top = items[:6]
    other = sum(v for _, v in items[6:])
    if other > 0:
        top.append(("Other", other))

    W, H = 460, 260
    bg = "#0d1117"
    border = "#30363d"
    text_main = "#c9d1d9"
    text_muted = "#8b949e"

    cx, cy = 140, 130
    R, r = 92, 56

    def pt(angle_deg: float, radius: float):
        a = math.radians(angle_deg)
        return cx + radius * math.sin(a), cy - radius * math.cos(a)

    segments = []
    legend_rows = []
    angle = 0.0
    for i, (lang, count) in enumerate(top):
        pct = (count / grand_total * 100) if grand_total else 0
        sweep = pct / 100 * 360
        a0, a1 = angle, angle + sweep
        color = LANG_COLORS.get(lang, FALLBACK_COLOR)
        if pct > 0.05:
            o0 = pt(a0, R)
            o1 = pt(a1, R)
            i1 = pt(a1, r)
            i0 = pt(a0, r)
            large = 1 if (a1 - a0) > 180 else 0
            d = (
                f"M {o0[0]:.2f},{o0[1]:.2f} "
                f"A {R},{R} 0 {large} 1 {o1[0]:.2f},{o1[1]:.2f} "
                f"L {i1[0]:.2f},{i1[1]:.2f} "
                f"A {r},{r} 0 {large} 0 {i0[0]:.2f},{i0[1]:.2f} Z"
            )
            segments.append(f'<path d="{d}" fill="{color}" stroke="{bg}" stroke-width="1.5" />')
        angle = a1

        ly = 34 + i * 30
        legend_rows.append(
            f'<circle cx="298" cy="{ly - 5}" r="6" fill="{color}" />'
            f'<text x="314" y="{ly}" font-size="13" fill="{text_main}" '
            f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">'
            f'{esc(lang)} <tspan fill="{text_muted}">{pct:.1f}%</tspan></text>'
        )

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Most used languages for {esc(login)}">
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{bg}" stroke="{border}" />
<text x="20" y="34" font-size="16" font-weight="600" fill="{text_main}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">Most Used Languages</text>
<line x1="20" y1="50" x2="{W - 20}" y2="50" stroke="{border}" />
{"".join(segments)}
{"".join(legend_rows)}
</svg>'''
    return svg


def main():
    login = os.environ.get("LOGIN") or (sys.argv[1] if len(sys.argv) > 1 else None)
    token = os.environ.get("GH_TOKEN", "")
    out_path = os.environ.get("OUT_PATH", "profile/top-languages.svg")
    if not login:
        print("LOGIN env var is required", file=sys.stderr)
        sys.exit(1)

    totals = fetch_language_bytes(login, token)
    svg = build_svg(login, totals)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out_path} ({len(svg)} bytes), {len(totals)} languages found")


if __name__ == "__main__":
    main()
