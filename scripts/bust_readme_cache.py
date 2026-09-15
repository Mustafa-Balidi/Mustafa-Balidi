#!/usr/bin/env python3
"""Append/refresh a cache-busting query string on the self-hosted card <img>
tags in README.md. GitHub renders README-embedded SVGs through its camo image
proxy, which caches by the exact URL (including query string) and can keep
serving a stale image on the profile page for a long time after the file in
the repo has actually changed -- even though the raw file itself is already
up to date. Changing the query string on every run forces a fresh fetch.
"""
import re
import sys
import time

README_PATH = "README.md"
CARD_PATTERNS = [
    r'profile/activity-overview\.svg',
    r'profile/top-languages\.svg',
]


def main():
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()

    cb = str(int(time.time()))
    changed = False
    for pattern in CARD_PATTERNS:
        new_content, n = re.subn(
            rf'(src="\./{pattern})(\?[^"]*)?"',
            rf'\1?cb={cb}"',
            content,
        )
        if n:
            content = new_content
            changed = True

    if changed:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"README.md cache-busted with cb={cb}")
    else:
        print("No matching <img> tags found in README.md", file=sys.stderr)


if __name__ == "__main__":
    main()
