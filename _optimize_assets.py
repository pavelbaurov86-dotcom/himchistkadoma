# -*- coding: utf-8 -*-
"""Generate responsive hero images and self-hosted font files."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
FONTS_DIR = ROOT / "assets" / "fonts"
IMG_DIR = ROOT / "assets" / "img"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
FONTS_CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Source+Sans+3:wght@400;500;600;700&"
    "family=Space+Grotesk:wght@500;600;700&display=swap"
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def slug_from_url(url: str) -> str:
    name = url.rsplit("/", 1)[-1].split("?")[0]
    if name.endswith(".woff2"):
        return name
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name)


def download_fonts() -> None:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    css = fetch(FONTS_CSS_URL).decode("utf-8")
    cache: dict[str, str] = {}

    def local_url(match: re.Match[str]) -> str:
        remote = match.group(1)
        if remote not in cache:
            filename = slug_from_url(remote)
            path = FONTS_DIR / filename
            if not path.exists():
                path.write_bytes(fetch(remote))
            cache[remote] = f"../fonts/{filename}"
        return f"url({cache[remote]})"

    local_css = re.sub(
        r"url\((https://fonts\.gstatic\.com/[^)]+)\)",
        local_url,
        css,
    )
    (ROOT / "assets" / "css" / "fonts.css").write_text(
        "/* Self-hosted fonts — no render-blocking third-party requests */\n" + local_css,
        encoding="utf-8",
    )
    print(f"fonts: {len(cache)} files -> assets/css/fonts.css")


def resize_hero() -> None:
    src = IMG_DIR / "title-image.webp"
    if not src.exists():
        src = IMG_DIR / "title-image.png"
    img = Image.open(src).convert("RGB")
    widths = (480, 768, 1280)
    for w in widths:
        ratio = w / img.width
        h = max(1, round(img.height * ratio))
        out = IMG_DIR / f"title-image-{w}.webp"
        resized = img.resize((w, h), Image.Resampling.LANCZOS)
        resized.save(out, "WEBP", quality=78, method=6)
        print(f"image: {out.name} -> {out.stat().st_size // 1024} KiB")


def build_critical_css() -> None:
    main = (ROOT / "assets" / "css" / "main.css").read_text(encoding="utf-8")
    markers = [
        ("/* ---------- Header:", "/* ---------- Sections ---------- */"),
        ("/* ---------- Buttons ---------- */", "/* ---------- Sections ---------- */"),
        ("/* ---------- Full-bleed hero", "/* Compact page hero"),
        ("/* ---------- Trust strip ---------- */", "/* ---------- Cards / grids ---------- */"),
        ("/* Compact page hero", "/* ---------- Trust strip ---------- */"),
    ]
    chunks = [main.split("/* ---------- Header:")[0]]
    for start, end in markers:
        if start not in main:
            continue
        part = main.split(start, 1)[1]
        if end in part:
            part = part.split(end, 1)[0]
        chunks.append(start + part)
    critical = "".join(chunks)
    critical = re.sub(r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/", "", critical)
    critical = re.sub(r"\n\s+\n", "\n", critical)
    critical = re.sub(r"  +", " ", critical)
    critical = re.sub(r"\n{3,}", "\n\n", critical)
    (ROOT / "assets" / "css" / "critical.css").write_text(
        "/* Above-the-fold styles */\n" + critical.strip() + "\n",
        encoding="utf-8",
    )
    size = (ROOT / "assets" / "css" / "critical.css").stat().st_size
    print(f"critical.css -> {size // 1024} KiB")


if __name__ == "__main__":
    download_fonts()
    resize_hero()
