"""Generate the small copies of the ernster- category icons the pages serve.

Each master `assets/ernster-<name>.png` is large artwork (hundreds of pixels,
up to 190KB) shown at 22 to 38px. Serving it as is costs every page load, so
this script writes `assets/ernster-<name>-76.png` beside it: twice the largest
display size, so it stays sharp on a high-density screen. The masters are
only ever read.

The masters arrive with differing transparent margins, so a straight resize
would draw some icons visibly smaller than their neighbours. Each copy is
therefore cropped to its artwork, padded square with one shared margin and
only then scaled down. A master smaller than the copy is refused rather than
enlarged.

    python generate_icons.py           write any copy that is missing or stale
    python generate_icons.py --check   change nothing; exit 1 if a copy is

Idempotent: a copy already matching its master is left untouched.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
PREFIX = "ernster-"
SIZE = 76
SUFFIX = f"-{SIZE}.png"
# Share of the copy's side the artwork spans, matching the tightest masters.
ARTWORK_FILL = 0.9
# Alpha at or below this counts as empty margin rather than artwork: soft
# glows fade into near-transparent pixels that should not widen the crop.
ALPHA_FLOOR = 8


def masters() -> list[Path]:
    return sorted(
        path for path in ASSETS.glob(f"{PREFIX}*.png") if not path.name.endswith(SUFFIX)
    )


def copy_path(master: Path) -> Path:
    return master.with_name(master.stem + SUFFIX)


def render(master: Path) -> Image.Image:
    """Return the square copy of `master`: cropped, padded, then scaled down."""
    with Image.open(master) as image:
        art = image.convert("RGBA")
    mask = art.getchannel("A").point(lambda a: 255 if a > ALPHA_FLOOR else 0)
    box = mask.getbbox()
    if box is None:
        raise SystemExit(f"{master.name}: no artwork, every pixel is transparent")
    art = art.crop(box)
    side = round(max(art.size) / ARTWORK_FILL)
    if side < SIZE:
        raise SystemExit(f"{master.name}: artwork too small to scale down to {SIZE}")
    canvas = Image.new("RGBA", (side, side))
    canvas.paste(art, ((side - art.width) // 2, (side - art.height) // 2))
    return canvas.resize((SIZE, SIZE), Image.LANCZOS)


def is_current(copy: Path, rendered: Image.Image) -> bool:
    if not copy.exists():
        return False
    with Image.open(copy) as image:
        existing = image.convert("RGBA")
    if existing.size != rendered.size:
        return False
    return ImageChops.difference(existing, rendered).getbbox() is None


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    stale = []
    for master in masters():
        copy = copy_path(master)
        rendered = render(master)
        if is_current(copy, rendered):
            continue
        stale.append(copy.name)
        if not check_only:
            rendered.save(copy, optimize=True)
    verb = "stale" if check_only else "wrote"
    for name in stale:
        print(f"{verb}: {name}")
    return 1 if check_only and stale else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
