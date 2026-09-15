#!/usr/bin/env python3
"""Generate a static SVG that mimics GitHub's native profile 'Activity overview'
panel (Contributed-to list + Code review/Commits/Issues/Pull requests radar),
computed from the real contributionsCollection data for the given user.
Runs with stdlib only so it needs no extra pip installs in CI.
"""
import json
import math
import os
import sys
import urllib.request

API_URL = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
    repositoriesContributedTo(first: 20, includeUserRepositories: true, orderBy: {field: PUSHED_AT, direction: DESC}, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
      totalCount
      nodes { nameWithOwner }
    }
  }
}
"""

def fetch(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "activity-overview-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)

def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

def build_svg(login: str, data: dict) -> str:
    user = data["data"]["user"]
    cc = user["contributionsCollection"]
    commits = cc["totalCommitContributions"]
    issues = cc["totalIssueContributions"]
    prs = cc["totalPullRequestContributions"]
    reviews = cc["totalPullRequestReviewContributions"]
    total = commits + issues + prs + reviews

    def pct(x: int) -> int:
        return round(x / total * 100) if total else 0

    p_commits, p_issues, p_prs, p_review = pct(commits), pct(issues), pct(prs), pct(reviews)

    contributed = user["repositoriesContributedTo"]
    names = [n["nameWithOwner"] for n in contributed["nodes"]]
    total_repos = contributed["totalCount"]
    shown = names[:3]
    extra = total_repos - len(shown)

    W, H = 780, 330
    bg = "#0d1117"
    border = "#30363d"
    text_muted = "#8b949e"
    text_main = "#c9d1d9"
    link_color = "#58a6ff"
    green = "#3fb950"
    axis_color = "#30363d"

    cx, cy, R = 580, 185, 86

    def pt(angle_deg: float, value_pct: float):
        a = math.radians(angle_deg)
        r = R * value_pct / 100
        return cx + r * math.sin(a), cy - r * math.cos(a)

    top = pt(0, p_review)
    right = pt(90, p_issues)
    bottom = pt(180, p_prs)
    left = pt(270, p_commits)

    axis_top_end = pt(0, 100)
    axis_right_end = pt(90, 100)
    axis_bottom_end = pt(180, 100)
    axis_left_end = pt(270, 100)

    polygon_pts = f"{top[0]:.1f},{top[1]:.1f} {right[0]:.1f},{right[1]:.1f} {bottom[0]:.1f},{bottom[1]:.1f} {left[0]:.1f},{left[1]:.1f}"

    dots = "".join(
        f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="4" fill="{green}" />'
        for p in (top, right, bottom, left)
    )

    axis_lines = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{e[0]:.1f}" y2="{e[1]:.1f}" stroke="{axis_color}" stroke-width="1.5" />'
        for e in (axis_top_end, axis_right_end, axis_bottom_end, axis_left_end)
    )

    def axis_label(x, y, lines, anchor="middle"):
        tspans = "".join(
            f'<tspan x="{x}" dy="{"0" if i == 0 else "16"}">{esc(line)}</tspan>'
            for i, line in enumerate(lines)
        )
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="13" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{tspans}</text>'

    top_lines = [f"{p_review}%", "Code review"] if p_review else ["Code review"]
    right_lines = [f"{p_issues}%", "Issues"]
    bottom_lines = [f"{p_prs}%", "Pull requests"]
    left_lines = [f"{p_commits}%", "Commits"]

    labels = (
        f'<g fill="{link_color}">{axis_label(axis_top_end[0], axis_top_end[1] - 26, top_lines)}</g>'
        f'<g fill="{text_main}">{axis_label(axis_right_end[0] + 34, axis_right_end[1] - 4, right_lines, "start")}</g>'
        f'<g fill="{text_main}">{axis_label(axis_bottom_end[0], axis_bottom_end[1] + 24, bottom_lines)}</g>'
        f'<g fill="{link_color}">{axis_label(axis_left_end[0] - 34, axis_left_end[1] - 4, left_lines, "end")}</g>'
    )
    if not p_review:
        labels = labels.replace(f'fill="{link_color}">{axis_label(axis_top_end[0], axis_top_end[1] - 26, top_lines)}', f'fill="{text_main}">{axis_label(axis_top_end[0], axis_top_end[1] - 26, top_lines)}')

    repo_link_y = 84
    rows = []
    rows.append(f'<tspan x="46" dy="0" fill="{text_main}">Contributed to</tspan>')
    for i, name in enumerate(shown):
        suffix = "," if i < len(shown) - 1 else ""
        rows.append(f'<tspan x="46" dy="20" fill="{link_color}">{esc(name)}</tspan><tspan fill="{text_main}">{suffix}</tspan>')
    if extra > 0:
        word = "repository" if extra == 1 else "repositories"
        rows.append(f'<tspan x="46" dy="20" fill="{text_main}">and {extra} other {word}</tspan>')

    repo_text = f'<text y="{repo_link_y}" font-size="14" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{"".join(rows)}</text>'

    repo_icon = (
        '<path transform="translate(18,72) scale(0.9)" fill="'
        + text_muted
        + '" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 1 1 0-1.5h1.75v-2H4.5a1 1 0 0 0-.968 1.246.75.75 0 1 1-1.453.375A2.5 2.5 0 0 1 2 11.5Zm10.5-1H4.5a1 1 0 0 0-1 1v6.708A2.5 2.5 0 0 1 4.5 9h8Z" />'
    )

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Activity overview for {esc(login)}">
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{bg}" stroke="{border}" />
<text x="20" y="34" font-size="16" font-weight="600" fill="{text_main}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">Activity overview</text>
<line x1="20" y1="50" x2="{W - 20}" y2="50" stroke="{border}" />
{repo_icon}
{repo_text}
<line x1="400" y1="24" x2="400" y2="{H - 24}" stroke="{border}" />
{axis_lines}
<polygon points="{polygon_pts}" fill="{green}" fill-opacity="0.18" stroke="{green}" stroke-width="2" />
{dots}
{labels}
</svg>'''
    return svg

def main():
    login = os.environ.get("LOGIN") or (sys.argv[1] if len(sys.argv) > 1 else None)
    token = os.environ.get("GH_TOKEN")
    out_path = os.environ.get("OUT_PATH", "profile/activity-overview.svg")
    if not login or not token:
        print("LOGIN and GH_TOKEN env vars are required", file=sys.stderr)
        sys.exit(1)

    data = fetch(login, token)
    if data.get("errors"):
        print(json.dumps(data["errors"]), file=sys.stderr)
        sys.exit(1)

    svg = build_svg(login, data)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out_path} ({len(svg)} bytes)")

if __name__ == "__main__":
    main()
