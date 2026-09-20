# HANDOFF — Spanish AfterLife "ERA" homepage redesign (staging prototype)

> For a fresh session picking up the ERA-style redesign. Self-contained. This is
> a **throwaway evaluation prototype**, NOT production. The live production site
> (spanishafterlife.com) is untouched and must stay that way.

## Project state & timeline (whole picture)

Work happened on **two tracks**: the **production site** (live on
spanishafterlife.com) and the **ERA redesign prototype** (staging only — the main
subject of this doc). Keep them straight: production ships by pushing/merging to
`main` (auto-deploys live); the redesign ships only to the `era-staging` preview.

**Timeline:**
1. **www→root 301 redirect** created at Cloudflare — live.
2. **SEO foundation** — created the GitHub repo from production; PR #1 (self-ref
   non-www extension-less canonicals, per-page titles/meta ≤60/≤155,
   Organization + Person JSON-LD, OG/Twitter, 13-URL sitemap, robots) → merged +
   deployed. Kept the designed hero H1s.
3. **GitHub Actions auto-deploy** — push to `main` → `wrangler pages deploy _site`
   (a clean copy dir; `.assetsignore` proved unsupported so we exclude repo/docs
   files via rsync). Secret `CLOUDFLARE_API_TOKEN` = the reused
   `spanishafterlife-redirect-fix` token (Zone Single-Redirect/DNS/SSL **plus**
   Account · Cloudflare Pages · Edit).
4. **Homepage features** — PR #2: 12-pillar dim-until-hover + click-through modals
   (~200-word overviews), 4 place-card dimming, **mobile touch fix** (hover gated
   behind `@media (hover:hover)` so tiles open on first tap), region-coverage line
   (Alicante/Murcia named without cards) → merged + deployed.
5. **Main-site handoff** written → `HANDOFF.md`.
6. **ERA redesign** — v1 → v2 (image-led, sparse text, cinematic), real owner
   photography + Ronda video, desktop/mobile video fixes → **staging only**. (This doc.)

**Where each thing lives:**

| LIVE in production (spanishafterlife.com) | STAGING only (era-staging.*.pages.dev · noindex) | Repo only (never served) |
|---|---|---|
| www→root 301 · SEO foundation · pillar/place dim + modals · mobile touch fix · region line · auto-deploy pipeline | v1 (`staging/index.html`) + v2 (`staging/v2/index.html`) ERA prototype · real Spain media · Ronda video | `HANDOFF.md` · `HANDOFF-ERA.md` · `staging-src/` generators |

**Open items — PRODUCTION track:**
- **AI-crawler robots.txt (unfinished):** owner chose to *allow* AI crawlers, but
  Cloudflare's zone-managed robots.txt still prepends AI-bot blocks (GPTBot,
  ClaudeBot, Google-Extended…). Fix = disable Cloudflare's managed robots.txt /
  **AI Crawl Control** in the dashboard (a toggle, not an API change). Was
  mid-navigation to that page when the redesign work began.
- **Place photos:** production Valencia City + Inland–Ontinyent cards still use
  unverified stock; Jávea & Denia and Oliva & Cullera are the owner's real photos.
- **Do NOT revoke** the `spanishafterlife-redirect-fix` API token — it now doubles
  as the CI deploy token.
- Owner has submitted the sitemap to Google Search Console.

**Open items — REDESIGN track** (details later in this doc): video ~19MB needs
ffmpeg compression; pillar switcher uses thematic stock for activity pillars;
Ontinyent staging card is stock; and the whole thing is **awaiting the owner's
decision on whether v2 is the approved direction** before any production build.

## What this is

A homepage redesign of spanishafterlife.com in the visual language of
**era-residence.com** (cinematic, image-led scroll; big Didone display type;
warm cream + navy palette). Built to decide whether the direction works before
committing to a production build.

Two versions exist, both in the repo, both live:
- **v1** — `staging/index.html` — first pass (ERA components, but text-heavy).
- **v2** — `staging/v2/index.html` — **the current direction**: image-led, sparse
  text, cinematic full-bleed "chapter" moments between sections, real owner
  photography + a Ronda background video. **Work continues on v2.**

## Where everything lives

- **Repo:** `github.com/ljkoch4321/spanishafterlife-site`, branch **`redesign-era`** (NOT `main`).
- **Local clone (this Mac):** `~/spanishafterlife-site`
- **v2 page:** `staging/v2/index.html` — self-contained (inline CSS + JS).
- **Media (committed):** `staging/media/` — real Spain photos + video:
  - `valencia-1/2/3.jpg` (Calatrava architecture), `oliva-1..5.jpg` (beaches/sunsets;
    oliva-4 = horses on beach), `home-1/2/3.jpg` (beach sunset / dark terrace / villa garden),
    `xabia-1/2.jpg` (founder portraits — NOT used on the homepage), `ronda.mp4` (video),
    `ronda-poster.jpg` (video poster).
  - Also at `staging/` root: `hero.png`, `javea-denia.jpg`, `oliva-cullera.jpg`, `guide-cover.png`.
- **Generators (source of truth):** `staging-src/gen_era_v2.py` (v2), `staging-src/gen_era_v1.py` (v1).
  Path-portable (compute output from their own location). **These live OUTSIDE
  `staging/` on purpose so they are not deployed to the public preview.**
- **Staging hygiene:** `staging/robots.txt` (disallow all), `staging/_headers` (`X-Robots-Tag: noindex`).

## Live preview (noindex, non-production)

- **v2:** https://era-staging.spanish-afterlife.pages.dev/v2/
- **v1:** https://era-staging.spanish-afterlife.pages.dev/

## Build / edit workflow

The v2 HTML is **generated** by `staging-src/gen_era_v2.py` — a single Python
file: copy + image maps at the top, then CSS, JS, and the HTML template. Two
ways to change it:
1. **Edit the generator** (`staging-src/gen_era_v2.py`) then run `python3 staging-src/gen_era_v2.py`. Preferred for content/image/copy changes (data-driven).
2. **Edit `staging/v2/index.html` directly** — it's self-contained. Fine for one-off CSS tweaks, but the generator will overwrite it on next run, so keep them in sync (or fold the change back into the generator).

Note: the generators also contain the `sips` image-processing and `avconvert`
video-transcode commands used to create `staging/media/*` — but that media is
already committed, so you only need those if you add NEW source photos/video
(which live only on this Mac, see "Source assets" below).

## Deploy (staging preview ONLY — never production)

```bash
cd ~/spanishafterlife-site
wrangler pages deploy staging --project-name=spanish-afterlife --branch=era-staging --commit-dirty=true
```
- Deploys the `staging/` dir to the **`era-staging` preview branch** of the
  Cloudflare Pages project `spanish-afterlife` → https://era-staging.spanish-afterlife.pages.dev
- The production custom domain (spanishafterlife.com) points only at the `main`
  branch deployment, so preview deploys **cannot** affect production.
- Requires `wrangler` authenticated (this Mac is). Account `d6d2d8b5a9f263c661f21fd9f50b7fc2`.
- **⚠️ Do NOT merge `redesign-era` into `main`, and do NOT deploy `staging/` to
  production.** The main pipeline rsyncs the repo into `_site` and would publish
  `staging/` on the live domain. Only `.git/.github/.gitignore/README.md/HANDOFF.md`
  are excluded there — `staging/`, `staging-src/`, and this file are NOT.

## v2 page structure (top → bottom)

1. **Hero** — real beach sunset (`home-1.jpg`); "Your best years. / Starting now."; one line; START HERE.
2. **Chapter (full-bleed VIDEO)** — Ronda (`ronda.mp4`); "A continent at your door."
3. **`#life`** — 12-pillar **sticky switcher** (scroll-driven + clickable). Mostly thematic Unsplash; real photos on The Property (`home-3`) and The Horses (`oliva-4`).
4. **Chapter** — `oliva-3.jpg`; "This is Tuesday now."
5. **`#numbers`** — US/Canada two-state toggle; 3 short contrasts. **Figures are verbatim — do not alter.**
6. **`#places`** — 4: Jávea & Denia (`javea-denia.jpg`), Valencia City (`valencia-3`), Oliva & Cullera (`oliva-2`), Inland–Ontinyent (Unsplash).
7. **Chapter** — `oliva-5.jpg`; "Why wait for the AfterLife?"
8. **`#how` (services)** — 4 alternating image rows (`valencia-2`, `valencia-1`, `oliva-cullera`, `home-3`).
9. **`#process`** — full-bleed split image (`hero.png`) + 4 numbered steps; "One relationship, start to finish."
10. **`#guide`** — `guide-cover.png` + email form.
11. **`#contact`** — `valencia-3` image + form.
12. **Footer.**

## Tech / behaviors

- **Fonts (Google, open):** Fraunces (display serif), Archivo (body/labels), Ephesis (script accent).
- **Palette:** cream `#F3F3EC`, ink navy `#17233B`; dark sections invert.
- **Scroll:** custom eased smooth-scroll (mini-Lenis; drives real document scroll so `position:sticky` works), IntersectionObserver reveals (line + section, gated behind `html.js` so content shows if JS fails), scroll parallax, sticky pillar switcher. Native scroll on touch / reduced-motion.
- **Chapter titles:** big Fraunces over a center-weighted dark overlay (an earlier script-font title was unreadable — do not reintroduce script for titles).
- **Video (the fiddly bit):** original is HEVC portrait `.mov` → transcoded to H.264 mp4 with macOS `avconvert` (faststart OK). `object-position: 50% 30%` so the town/gorge shows (not sky). Poster is set as a **CSS background on the container** (always-visible fallback) and the `<video>` starts `opacity:0`, fading in only on the `playing` event; a play-nudge retries on first touch/scroll. So mobile always shows the Ronda still even when iOS blocks autoplay.
- **Media containers** must have `position:relative; overflow:hidden` or the absolutely-positioned `.media-img` escapes and blows up the layout (this bit us once — rule covers `.media, .place-media, .srow-media, .guide-media, .contact-media, .process-media`).
- **Forms** stubbed to `console` with TODO comments (Mailchimp guide / Formspree contact — both currently placeholder endpoints).
- **Removable `#badge`** (STAGING).

## Open items / TODO for production

1. ~~**Video weight (~19MB)**~~ — **DONE (2026-09-20).** Now **1.3MB** WebM (VP9 crf42) +
   **2.4MB** MP4 (H.264 crf26, `+faststart`), 864x1536, no audio, BT.709-tagged.
   **19MB -> 1.3MB** for browsers that take the WebM; older Safari gets the MP4.
   Trimmed to the Puente Nuevo reveal (**13.6s-22.6s** of the original) and built as a
   **seamless 7.5s loop** — a 1.5s self-crossfade at t=6.0 dissolves the head back over the
   tail, so it no longer jump-cuts on wrap. `ronda-poster.jpg` (149KB) re-pulled from
   **t=5.8 inside the loop**, so the still is a settled-bridge frame that actually occurs
   in the video. `vbg()` emits `<source>` WebM-before-MP4.

   **⚠️ THE HDR TRAP — read before re-encoding any of this footage.** The source
   `IMG_0486.mov` is **HDR**: 10-bit, BT.2020 primaries, **HLG** transfer (`arib-std-b67`),
   Dolby Vision profile 8. The Homebrew `ffmpeg` on this Mac has **no `zscale` and no
   `libplacebo`**, so it *cannot tone-map* — feeding the .mov straight to ffmpeg silently
   reads HLG values as plain SDR gamma and yields **washed-out, hazy, desaturated** colour
   (pale sky, grey-green foliage, flat stone). That is exactly what the first pass shipped
   and what had to be redone. **Fix: do the HDR->SDR step in macOS `avconvert`**
   (AVFoundation tone-maps DV/HLG correctly — it is why the old 19MB file looked right),
   then grade and cut in ffmpeg. Full recipe lives in the `vbg()` docstring in
   `staging-src/gen_era_v2.py`. Grade applied on top of the tone map:
   `vibrance=intensity=0.18,eq=contrast=1.05:saturation=1.06` (a stronger grade was tried
   and rejected — it crushed the gorge shadows and over-saturated the sky for this palette).
2. **Pillar switcher** still uses thematic Unsplash for activity pillars (golf, padel, cycling, art, food) — the owner's library is coast/city so there's no real match. Real photos used everywhere they fit.
3. **Ontinyent place** still Unsplash (no inland photo in the library).
4. **If v2 is approved:** rebuild for production with real Lenis + GSAP ScrollTrigger, the compressed video, proper photography, and have it **replace `index.html`** (not live in `staging/`). Then re-run the SEO pass (canonical/title/meta/schema) on the new markup — see `HANDOFF.md` for the main-site SEO + deploy setup.

## Content integrity rules (carry over)

- **Do not alter any figure** — property prices, tax rates (19–23% Spain savings base; up to 53% Ontario/B.C.; up to 37% federal + 13.3% California), €400K villa, 300 days of sun, service fees (€3,500 / €5,500), etc.
- Existing Spanish AfterLife copy is the source; v2 simplifies it but invents nothing.
- **No era-residence.com assets** were copied. Open fonts only.

## Source assets (this Mac only — for adding new photos/video)

`~/Desktop/Desktop - Morten's MacBook Pro/Spanish Afterlife/` — location shoots
(Valencia, Oliva, Xàbia, Ronda, "Home"). Already processed into `staging/media/`.
Ronda video original: `Social Media/Ronda, March 28, 2026/IMG_0486.mov` (HEVC).
Photos deliberately NOT used: `xabia-1/2` (founder portraits — belong on an About
page), `home-2` (too dark), `oliva-1` (feet selfie).
Processing recipe: `sips -Z 1800 -s format jpeg -s formatOptions 82 <in> --out <out>`;
video: `avconvert -p Preset1280x720 -s <in.mov> -o <out.mp4>`.

## Related

- `HANDOFF.md` (repo root) — the main production-site handoff (SEO, GitHub Actions
  auto-deploy on push to `main`, robots/Cloudflare notes). Read it before touching
  anything that could reach production.
