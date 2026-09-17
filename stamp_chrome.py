"""Stamp the shared site chrome (top bar and footer) into every hub page.

The hub is hand-written HTML served straight from this directory, so there is
no include mechanism at render time. Eleven pages each carried their own copy
of the navigation and the copies drifted. This script is the one home for that
markup: it rewrites the `<header class="topbar">` and `<footer>` blocks of
every root `*.html` from the definitions below, marking the current page.

    python stamp_chrome.py           rewrite any page that has drifted
    python stamp_chrome.py --check   change nothing; exit 1 if a page drifted

Idempotent: stamping a page that is already current changes nothing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME_PAGE = "index.html"
HOME_HREF = "./"
# Pages whose footer names the hub rather than offering a way back: the home
# page itself, plus the SmartScreen page, which is reached from product sites on
# other domains rather than from inside the hub.
PROFILE_HUB_FOOTER_PAGES = frozenset({HOME_PAGE, "windows-smartscreen.html"})
LINKEDIN_URL = "https://www.linkedin.com/in/oliverernster"
CRANK_URL = "https://www.crankthecode.com"
GITHUB_URL = "https://github.com/oernster"

SECTIONS = (
    (HOME_HREF, "Home"),
    ("applications.html", "Applications"),
    ("decision-architecture.html", "Decision Architecture"),
    ("tooling.html", "Tooling"),
    ("workshop.html", "Workshop"),
    ("commercial-licensing.html", "Licensing"),
)

LINKEDIN_ICON_PATH = (
    "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 "
    "1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 "
    "3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 "
    "0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 "
    "2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 "
    ".774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 "
    "22.271V1.729C24 .774 23.2 0 22.225 0z"
)

UTILITY_LINKS = (
    (
        '<a class="util" href="assets/CV-OliverErnster.pdf" title="Two-page CV (PDF)">'
        '<img src="assets/download-arrow-76.png" alt="" width="16" height="16">CV</a>'
    ),
    (
        f'<a class="util" href="{CRANK_URL}" title="Crank the Code, the Decision '
        'Architecture thesis in long form"><img src="assets/crankthecode.png" alt="" '
        'width="16" height="16">Crank the Code</a>'
    ),
    (
        f'<a class="util" href="{GITHUB_URL}" title="github.com/oernster, the full '
        'collection of source"><img src="assets/github.svg" alt="" width="16" '
        'height="16">GitHub</a>'
    ),
    (
        f'<a class="util icon-only" href="{LINKEDIN_URL}" target="_blank" '
        'rel="noopener" aria-label="LinkedIn (opens in a new tab)" title="LinkedIn">'
        '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
        f'focusable="false"><path d="{LINKEDIN_ICON_PATH}"/></svg></a>'
    ),
)

HEADER_RE = re.compile(r'<header class="topbar">.*?</header>', re.DOTALL)
FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.DOTALL)


def _page_href(page: str) -> str:
    return HOME_HREF if page == HOME_PAGE else page


def render_header(page: str) -> str:
    current = _page_href(page)
    lines = [
        '<header class="topbar">',
        '    <div class="inner">',
        f'      <a class="brand" href="{HOME_HREF}">ernster.dev</a>',
        '      <nav class="nav" aria-label="Sections">',
    ]
    for href, label in SECTIONS:
        marker = ' aria-current="page"' if href == current else ""
        lines.append(f'        <a href="{href}"{marker}>{label}</a>')
    lines.append('        <span class="sep" aria-hidden="true"></span>')
    lines.extend(f"        {link}" for link in UTILITY_LINKS)
    lines.extend(["      </nav>", "    </div>", "  </header>"])
    return "\n".join(lines)


def render_footer(page: str) -> str:
    if page in PROFILE_HUB_FOOTER_PAGES:
        first = '<a href="https://ernster.dev">Profile hub</a>'
    else:
        first = f'<a href="{HOME_HREF}">Back to home</a>'
    return "\n".join(
        [
            "<footer>",
            '    <div class="row">',
            f"      {first}",
            f'      <a href="{CRANK_URL}">crankthecode.com</a>',
            f'      <a href="{GITHUB_URL}">github.com/oernster</a>',
            (
                f'      <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">'
                "LinkedIn</a>"
            ),
            "    </div>",
            "  </footer>",
        ]
    )


def stamp(text: str, page: str) -> str:
    """Return `text` with its header and footer replaced by the shared chrome."""
    for pattern, rendered in (
        (HEADER_RE, render_header(page)),
        (FOOTER_RE, render_footer(page)),
    ):
        if len(pattern.findall(text)) != 1:
            raise ValueError(
                f"{page}: expected exactly one match for {pattern.pattern}"
            )
        text = pattern.sub(lambda _match, r=rendered: r, text)
    return text


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    drifted = []
    for path in sorted(ROOT.glob("*.html")):
        raw = path.read_bytes().decode("utf-8")
        newline = "\r\n" if "\r\n" in raw else "\n"
        text = raw.replace("\r\n", "\n")
        stamped = stamp(text, path.name)
        if stamped == text:
            continue
        drifted.append(path.name)
        if not check_only:
            path.write_bytes(stamped.replace("\n", newline).encode("utf-8"))
    verb = "drifted" if check_only else "stamped"
    for name in drifted:
        print(f"{verb}: {name}")
    return 1 if check_only and drifted else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
