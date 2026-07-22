# ernster.dev

The hand-built static profile hub at [ernster.dev](https://ernster.dev): the entry point to my (Oliver Ernster) public work, grouped by category (Decision Architecture, applications, libraries and tooling, protocol and standards, gaming, 3D printing and the long tail).

## Who this is for

Anyone arriving from GitHub, a CV or a search result who wants the full catalogue in one place. It links out to each project's own site or repository.

**Not for:** project documentation. Each project documents itself in its own repository; this hub only routes you there.

## What it is

- Plain hand-written HTML and CSS. No framework, no build step, no site generator (`.nojekyll`).
- One page per category plus the home page, sharing a single stylesheet.
- Served by GitHub Pages from this repository's root at the custom domain `ernster.dev` (the `CNAME` file). The old `oernster.github.io` URLs 301-redirect here, project sites included.

## SEO infrastructure

This repository owns the host root, so it carries the crawler surface for every project site served under `ernster.dev/<repo>/`:

- `robots.txt`: the single robots file for the host (crawlers read it only at the root).
- `sitemap.xml`: the single sitemap listing the hub pages and every page of every project site on the host. Project repositories ship no sitemap or robots of their own; when a project site gains a page, its URL is added here.
- Every page carries a canonical URL, Open Graph and Twitter card metadata; the home page carries Person and WebSite JSON-LD and the Google site verification tag.

## Licence

No licence is granted. The content and design are copyright Oliver Ernster; the linked projects carry their own licences.
