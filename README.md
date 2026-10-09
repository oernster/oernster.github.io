# ernster.dev

The hand-built static profile hub at [ernster.dev](https://ernster.dev): the entry point to my (Oliver Ernster) public work. The home page leads with two deep dives (Decision Architecture, applications); the MMSP specification and Meridian sit on the Applications page alongside the shipped apps, libraries and tooling have their own page and the Workshop hub gathers the side interests (3D printing, gaming).

## Who this is for

Anyone arriving from GitHub, a CV or a search result who wants the full catalogue in one place. It links out to each project's own site or repository.

**Not for:** project documentation. Each project documents itself in its own repository; this hub only routes you there.

## What it is

- Plain hand-written HTML and CSS. No framework, no build step, no site generator (`.nojekyll`).
- One home for the shared chrome: `stamp_chrome.py` holds the top bar and footer and writes them into every root page, marking the current section. Edit the navigation there, never in a page, then run `python stamp_chrome.py`; `python stamp_chrome.py --check` changes nothing and exits 1 if any page has drifted.
- Small copies of the category icons: each master `assets/ernster-<name>.png` is large artwork, so the pages serve `assets/ernster-<name>-76.png`, written by `generate_icons.py` (it needs Pillow). After adding or replacing a master, run `python generate_icons.py`; `python generate_icons.py --check` changes nothing and exits 1 if a copy is missing or stale. The masters are only ever read.
- One page per category plus the home page, sharing a single stylesheet.
- Served by GitHub Pages from this repository's root at the custom domain `ernster.dev` (the `CNAME` file). The old GitHub Pages default URLs 301-redirect here, project sites included.

## SEO infrastructure

This repository owns the host root, so it carries the crawler surface for every project site served under `ernster.dev/<repo>/`:

- `robots.txt`: the single robots file for the host (crawlers read it only at the root).
- `sitemap.xml`: the hub sitemap listing the hub pages and every page of every project site on the host bar one. Project repositories ship no sitemap or robots of their own; when a project site gains a page, its URL is added here. The exception is 3D-printing-info, whose build generates its own `docs/sitemap.xml`; `robots.txt` names it beside the hub sitemap, so its URLs are not repeated here. `snarkapi/` is not listed either: it holds a copy of the SnarkAPI product pages, maintained here by hand, whose canonical home is snarkapi.com and whose own sitemap lists them.
- Every page carries a canonical URL. The content pages also carry Open Graph and Twitter card metadata; the two redirect stubs (`other.html`, `standards.html`) carry only a canonical pointing at their destination. The home page carries Person and WebSite JSON-LD and the Google site verification tag.

## Licence

No licence is granted. The content and design are copyright Oliver Ernster; the linked projects carry their own licences.
