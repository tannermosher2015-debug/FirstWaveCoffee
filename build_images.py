"""First Wave Coffee — image pipeline.
Reads the owner-supplied photos, auto-orients, optimizes to web sizes (webp + jpg
fallbacks for hero/og), and composes an Open Graph share card.
Re-run after dropping new/updated source photos into SRC."""
from PIL import Image, ImageOps, ImageDraw, ImageFont
import os

SRC = r"C:\Users\Tanne\frontline-web-design\FirstWaveCoffee"
OUT = r"C:\Users\Tanne\first-wave-coffee\assets"
os.makedirs(OUT, exist_ok=True)

# source file -> output basename, longest-edge px, also-jpg?
JOBS = [
    ("unnamed (2).webp",      "hero-trailer",      1600, True),   # trailer + drink + Maui sky
    ("unnamed (3).webp",      "golden-logo",       1600, True),   # carved logo, golden hour
    ("1.webp",                "latte-art",         1600, True),   # top-down latte art (landscape)
    ("ownerstoryphoto.webp",  "story-owner",       1400, False),  # barista shaka
    ("Firstwavefamily.png",   "story-family",      1400, False),  # family at the trailer
    ("logo.webp",             "logo-sign",         1400, False),  # carved wood sign
    ("FWCmenu.webp",          "menu-board",        1400, False),  # real menu board
    ("unnamed (1).webp",      "drinks-signature",  1400, False),  # Hapa / Shore Break / Up Country cups
    ("unnamed.webp",          "drink-mango-matcha",1200, False),
    ("unnamed (7).webp",      "drink-guava-chai",  1200, False),
    ("unnamed (4).webp",      "candid-window",     1200, False),
    ("unnamed (6).webp",      "community-line",    1400, False),
]

def load(name):
    img = Image.open(os.path.join(SRC, name))
    img = ImageOps.exif_transpose(img)
    return img

def fit(img, longest):
    w, h = img.size
    if max(w, h) <= longest:
        return img
    s = longest / max(w, h)
    return img.resize((round(w * s), round(h * s)), Image.LANCZOS)

for src, base, longest, also_jpg in JOBS:
    img = fit(load(src), longest)
    rgb = img.convert("RGB")
    rgb.save(os.path.join(OUT, base + ".webp"), "WEBP", quality=82, method=6)
    if also_jpg:
        rgb.save(os.path.join(OUT, base + ".jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    print("ok", base, img.size)

def cover(img, tw, th):
    w, h = img.size
    s = max(tw / w, th / h)
    img = img.resize((round(w * s), round(h * s)), Image.LANCZOS)
    w, h = img.size
    return img.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))

# ---- Open Graph card 1200x630 from the latte-art shot ----
og = cover(load("1.webp").convert("RGB"), 1200, 630)
shade = Image.new("L", (1200, 630), 0)
ds = ImageDraw.Draw(shade)
for y in range(630):
    ds.line([(0, y), (1200, y)], fill=int(200 * (y / 630) ** 1.5))  # darker toward bottom
black = Image.new("RGB", (1200, 630), (10, 30, 28))
og = Image.composite(black, og, shade)
draw = ImageDraw.Draw(og)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

f_big = font(r"C:\Windows\Fonts\georgiab.ttf", 92)
f_small = font(r"C:\Windows\Fonts\georgia.ttf", 38)
mark = Image.open(os.path.join(OUT, "logo-mark.png")).convert("RGBA")
mw = 150
mark = mark.resize((mw, round(mark.size[1] * mw / mark.size[0])), Image.LANCZOS)
og.paste(mark, (70, 70), mark)
draw.text((72, 430), "First Wave Coffee", font=f_big, fill=(247, 241, 230))
draw.text((76, 540), "Signature lattes · Kahului, Maui", font=f_small, fill=(242, 166, 90))
og.save(os.path.join(OUT, "og.jpg"), "JPEG", quality=88, optimize=True)
print("ok og 1200x630")
print("DONE")
