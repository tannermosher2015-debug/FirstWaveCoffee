"""First Wave Coffee — self-host the Google Fonts (Fraunces + Hanken Grotesk).
Fetches the exact variable woff2 files Google serves (all subsets, so the Hawaiian
okina and macrons keep the brand font), downloads them to assets/fonts/, and emits a
local @font-face block to assets/fonts/_fontface.css for inlining. Re-run to refresh."""
import os, re, urllib.request

OUT = r"C:\Users\Tanne\first-wave-coffee\assets\fonts"
os.makedirs(OUT, exist_ok=True)

# Variable ranges so we get ONE file per (family, style, subset) covering all weights used.
CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600"
           "&family=Hanken+Grotesk:wght@400..700&display=swap")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

req = urllib.request.Request(CSS_URL, headers={"User-Agent": UA})
css = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")

# Each face is preceded by a /* subset */ comment.
blocks = re.findall(r"/\*\s*([\w\[\]-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
print("faces found:", len(blocks))

local_faces = []
preload = []
counter = {}
for subset, face in blocks:
    fam = re.search(r"font-family:\s*'([^']+)'", face).group(1)
    style = re.search(r"font-style:\s*(\w+)", face).group(1)
    url = re.search(r"url\((https://[^)]+\.woff2)\)", face).group(1)
    slug = fam.lower().replace(" ", "") + "-" + style + "-" + subset
    counter[slug] = counter.get(slug, 0) + 1
    if counter[slug] > 1:
        slug += "-%d" % counter[slug]
    fname = slug + ".woff2"
    fpath = os.path.join(OUT, fname)
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
    with open(fpath, "wb") as f:
        f.write(data)
    print("downloaded %-40s %5d KB  [%s]" % (fname, round(len(data) / 1024), subset))
    local = face.replace(url, "assets/fonts/" + fname)
    local = re.sub(r"format\('woff2'\)", "format('woff2')", local)
    local_faces.append(local.strip())
    if subset == "latin":   # preload the primary (English + okina) subsets
        preload.append(fname)

with open(os.path.join(OUT, "_fontface.css"), "w", encoding="utf-8") as f:
    f.write("\n".join(local_faces))

print("\n=== PRELOAD THESE (latin subset) ===")
for p in preload:
    print(p)
print("\ntotal woff2 bytes:",
      round(sum(os.path.getsize(os.path.join(OUT, x)) for x in os.listdir(OUT) if x.endswith('.woff2')) / 1024), "KB")
print("wrote", os.path.join(OUT, "_fontface.css"))
