#!/usr/bin/env python3
"""Generate a self-hosted 'Top Languages' card computed from the languages the
user *actually wrote code in* — based on their own authored commits (matched by
GitHub login, which correctly follows username renames), not raw repo-wide
language byte totals. This avoids crediting a user with languages that only
exist in files written by other contributors in a shared/forked repo.
Stdlib only, so it needs no extra pip installs in CI.
"""
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

API = "https://api.github.com"

EXT_LANG = {
    ".py": "Python", ".ipynb": "Jupyter Notebook",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".html": "HTML", ".htm": "HTML",
    ".css": "CSS", ".scss": "SCSS", ".sass": "SCSS",
    ".php": "PHP", ".dart": "Dart", ".java": "Java", ".kt": "Kotlin",
    ".swift": "Swift", ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".cxx": "C++",
    ".c": "C", ".go": "Go", ".rb": "Ruby", ".rs": "Rust", ".sh": "Shell",
    ".vue": "Vue", ".sql": "SQL",
}

LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "HTML": "#e34c26", "CSS": "#563d7c", "Jupyter Notebook": "#DA5B0B",
    "PHP": "#4F5D95", "Dart": "#00B4AB", "C#": "#178600", "Shell": "#89e051",
    "Java": "#b07219", "C++": "#f34b7d", "C": "#555555", "Go": "#00ADD8",
    "Ruby": "#701516", "Rust": "#dea584", "Vue": "#41b883", "SCSS": "#c6538c",
    "Kotlin": "#A97BFF", "Swift": "#F05138", "SQL": "#e38c00",
}
FALLBACK_COLOR = "#8b949e"


def api_get(url: str, token: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "top-languages-generator",
    }
    if token:
        headers["Authorization"] = f"bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def list_all_commits(full_name: str, token: str) -> list:
    commits = []
    page = 1
    while True:
        try:
            batch = api_get(f"{API}/repos/{full_name}/commits?per_page=100&page={page}", token)
        except Exception:
            break
        if not batch or not isinstance(batch, list):
            break
        commits.extend(batch)
        if len(batch) < 100 or page >= 10:  # cap at 1000 commits/repo, plenty for a profile
            break
        page += 1
    return commits


def ext_of(filename: str) -> str:
    i = filename.rfind(".")
    return filename[i:].lower() if i != -1 else ""


def commit_language_additions(full_name: str, sha: str, token: str) -> dict:
    try:
        detail = api_get(f"{API}/repos/{full_name}/commits/{sha}", token)
    except Exception:
        return {}
    out = {}
    for f in detail.get("files", []) or []:
        lang = EXT_LANG.get(ext_of(f.get("filename", "")))
        if not lang:
            continue
        out[lang] = out.get(lang, 0) + f.get("additions", 0)
    return out


def fetch_user_language_totals(login: str, token: str) -> dict:
    totals = {}
    page = 1
    repos = []
    while True:
        batch = api_get(f"{API}/users/{login}/repos?type=owner&per_page=100&page={page}", token)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    my_commits = []  # (full_name, sha)
    for repo in repos:
        if repo.get("archived"):
            continue
        commits = list_all_commits(repo["full_name"], token)
        for c in commits:
            author = c.get("author")
            if not (author and author.get("login") == login):
                continue
            # Skip merge commits: GitHub's per-commit diff for a merge includes
            # everything the merge brought in from the other branch, which would
            # wrongly credit the person who ran `git merge` with code they never
            # personally wrote (e.g. pulling in a teammate's Dart/mobile changes).
            if len(c.get("parents") or []) > 1:
                continue
            my_commits.append((repo["full_name"], c["sha"]))

    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = [
            ex.submit(commit_language_additions, full_name, sha, token)
            for full_name, sha in my_commits
        ]
        for fut in as_completed(futures):
            for lang, add in fut.result().items():
                totals[lang] = totals.get(lang, 0) + add

    return totals


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_svg(login: str, totals: dict) -> str:
    grand_total = sum(totals.values())
    items = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:6]

    W = 420
    row_h = 40
    top_pad = 56
    bottom_pad = 18
    H = top_pad + max(len(items), 1) * row_h + bottom_pad

    bg = "#0d1117"
    border = "#30363d"
    track = "#21262d"
    text_main = "#c9d1d9"
    text_muted = "#8b949e"

    track_x = 20
    track_w = W - 40
    track_h = 8

    rows = []
    for i, (lang, count) in enumerate(items):
        pct = (count / grand_total * 100) if grand_total else 0
        color = LANG_COLORS.get(lang, FALLBACK_COLOR)
        y_label = top_pad + i * row_h
        y_track = y_label + 10
        fill_w = max(track_w * pct / 100, 3) if pct > 0 else 0
        rows.append(
            f'<text x="{track_x}" y="{y_label}" font-size="13" fill="{text_main}" '
            f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{esc(lang)}</text>'
            f'<text x="{W - 20}" y="{y_label}" text-anchor="end" font-size="13" fill="{text_muted}" '
            f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{pct:.1f}%</text>'
            f'<rect x="{track_x}" y="{y_track}" width="{track_w}" height="{track_h}" rx="4" fill="{track}" />'
            f'<rect x="{track_x}" y="{y_track}" width="{fill_w:.1f}" height="{track_h}" rx="4" fill="{color}" />'
        )

    if not items:
        rows.append(
            f'<text x="{W/2}" y="{top_pad + 20}" text-anchor="middle" font-size="13" fill="{text_muted}" '
            f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">No authored commits found yet</text>'
        )

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Most used languages for {esc(login)}">
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{bg}" stroke="{border}" />
<text x="20" y="30" font-size="16" font-weight="600" fill="{text_main}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">Most Used Languages</text>
<line x1="20" y1="42" x2="{W - 20}" y2="42" stroke="{border}" />
{"".join(rows)}
</svg>'''
    return svg


def main():
    login = os.environ.get("LOGIN") or (sys.argv[1] if len(sys.argv) > 1 else None)
    token = os.environ.get("GH_TOKEN", "")
    out_path = os.environ.get("OUT_PATH", "profile/top-languages.svg")
    if not login:
        print("LOGIN env var is required", file=sys.stderr)
        sys.exit(1)

    totals = fetch_user_language_totals(login, token)
    svg = build_svg(login, totals)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out_path} ({len(svg)} bytes), {len(totals)} languages: {totals}")


if __name__ == "__main__":
    main()
