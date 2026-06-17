# First Wave Coffee — website

A single-file, framework-free marketing site for **First Wave Coffee**, a two-brother
coffee trailer in Kahului, Maui. Warm-organic / surf-at-dawn direction — teal (ocean),
sunrise orange, and cedar tones pulled from the real trailer. WCAG 2.1 AA, reduced-motion
safe, optimized real photos. Built by Frontline Web Designs as a **concept / design preview**.

## Files
- `index.html` — the entire site (inline CSS + JS, a `CONFIG` block in the `<script>` at the bottom).
- `assets/` — optimized images (webp + jpg fallbacks for hero/og), transparent `logo-mark.png`, `favicon.png`, `og.jpg`.
- `build_images.py` — image pipeline. Re-run after dropping new/updated source photos into
  `C:\Users\Tanne\frontline-web-design\FirstWaveCoffee`: `python build_images.py`.
- `netlify.toml` — static deploy (`publish = "."`) + security/cache headers.
- `robots.txt` — **disallow-all** while this is an unofficial concept (see below).

## Editing
All links, hours, the contact email, and the optional contact-form key live in one
`CONFIG` object near the bottom of `index.html`. The live "Open now / Closed" pill and the
highlighted day in the hours list are computed from `CONFIG.hours` in Hawaii time.

## Contact form
The form posts to **Web3Forms** when `CONFIG.web3formsKey` is set; until then it gracefully
falls back to opening the visitor's email app addressed to `FrontlineWebDesigns@gmail.com`.
To enable AJAX submit, paste the Web3Forms access key for that inbox into `CONFIG.web3formsKey`.

## Confirm before going "official" (placeholders / to verify)
- [ ] **Exact street number** — using `214 Hoʻokele St` (Yelp); one source said 176. ZIP set to **96732** (Kahului; the brief's 96753 is Kīhei).
- [ ] **Hours** — Tue–Sat 7:30a–3p, Wed closes 1:30p, Sun/Mon closed (food-truck hours drift).
- [ ] **Menu + prices** — transcribed from the carved board photo; confirm still current.
- [ ] **Testimonials** — currently recurring review *themes*; swap in exact verbatim quotes + names.
- [ ] **Star rating** — shown qualitatively; add the real Yelp/Google number if desired.
- [ ] **Phone** — none shown (no public number found); add to `CONFIG`/Visit if they want one.
- [ ] **Social URLs** — Instagram/Yelp/Google/joe.coffee wired; add Facebook/TikTok if they exist.
- [ ] **robots.txt** — disallow-all because this is a concept. If First Wave adopts it as the
      official site, switch to `Allow: /`, add a sitemap, and remove the footer "concept" disclaimer.

## Deploy
Static site → push `main`, Netlify serves the repo root. **A push is a publish.**
Pull `--rebase` before working/pushing (two-machine sync).
