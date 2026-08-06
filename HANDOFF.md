# HANDOFF — spanishafterlife.com maintenance

> Internal doc for whoever (human or agent) picks up work on this site. Lives in
> the repo but is NOT deployed — the deploy workflow copies the site into a clean
> `_site/` dir and excludes this file (see Deploy model). Assumes no prior context.

## The site / stack

Live production marketing site for a concierge immigration + real-estate
business helping North Americans (US & Canada) relocate/retire to Spain's
Valencia Community. Founder: **LJ Koch**; legal entity **LJ Koch Group Inc.**

- **Hand-authored static HTML.** One `.html` file per route. **No build step**,
  no framework, no `package.json`. The homepage is `index.html` (~520 KB — one
  large inline `<style>` block and small inline `<script>`s; it's all in that
  one file).
- **Routes:** `/` (index), `/immigration`, `/real-estate`, `/about`,
  `/fullafterlife`, `/private-client`, `/building-my-life-in-spain`,
  `/find-your-spain`, `/guide`, `/privacy`, `/canada-quality-of-life`,
  `/us-cash-out`, `/us-sun-seekers`, `/thank-you`.
- **Host:** Cloudflare Pages, project **`spanish-afterlife`** (direct-upload
  project). Custom domains `spanishafterlife.com` + `www` (www 301-redirects to
  root at the Cloudflare **zone** level — do **not** touch that).

## Deploy model — READ CAREFULLY

- Production branch is **`main`**. `.github/workflows/deploy.yml` runs on every
  push to `main`: it `rsync`s the repo into a clean `_site/` dir (excluding
  `.git`, `.github`, `.gitignore`, `README.md`, `HANDOFF.md`) then runs
  `wrangler pages deploy _site --project-name=spanish-afterlife --branch=main`.
  Repo secret `CLOUDFLARE_API_TOKEN` is already configured; the account ID is
  hardcoded in the workflow. (Note: `.assetsignore` is NOT honoured by this
  Pages project — that's why deploys go through the `_site` copy. If you add a
  new non-site file to the repo root that shouldn't be public, add it to the
  rsync `--exclude` list.)
- Cloudflare Pages serves `index.html` for unknown paths and returns **200**
  (a soft-404), so requesting a non-existent path shows the homepage rather than
  a real 404. Pre-existing behaviour; a `404.html` could be added if desired.
- **Therefore: pushing to `main` deploys straight to the LIVE site**,
  automatically, within ~1 minute. Treat `git push origin main` as "publish."
- **Preview without touching prod** (if `wrangler` is authenticated on this
  machine): `wrangler pages deploy . --project-name=spanish-afterlife
  --branch=<name>` → `https://<name>.spanish-afterlife.pages.dev`. Check whether
  wrangler is installed/authed first; if not, work via branch + PR and have the
  owner review the diff. **Never push experimental work to `main`.**
- **Default working style:** for anything non-trivial — branch → deploy a
  preview → verify → merge to `main`. For small fixes the owner may say "push to
  live," then push `main` directly.

## Access checklist (do this first)

1. Clone `https://github.com/ljkoch4321/spanishafterlife-site` (public).
2. `gh auth status` — confirm **push** access as `ljkoch4321`. Pushing is
   required to deploy; if you can't push, stop and tell the owner.
3. Check whether `wrangler` is installed + authenticated (for previews).

## Current state (all live in production as of this handoff)

- **Google Analytics (GA4) — active site-wide.** Property `G-0D870F788P`.
  The standard gtag snippet sits in `<head>` (right after `<meta charset>`) on
  all 14 pages. It replaced a dormant commented-out `GA_MEASUREMENT_ID`
  placeholder that had never fired. **Caveat the original author flagged and it
  still stands:** there is **no cookie-consent banner**, and GA4 drops
  cookies / sends data to Google on load — for EU/UK visitors that is a
  GDPR/ePrivacy consent gap. The business is Spain-based, so if you get EU
  traffic, add a consent gate (or GA Consent Mode) and a line in `privacy.html`.
- **SEO foundation — done & live.** Self-referencing non-www extension-less
  canonicals, per-page titles/meta, Organization + Person JSON-LD, OG/Twitter
  cards, `sitemap.xml` (13 non-www URLs), `robots.txt`. **Do not regress these.**
- **Homepage "Twelve reasons this is the right move"** (`id="life"`): 12
  `.pv-item` tiles. Photos **dimmed** (`brightness ~0.4`), brighten on hover;
  each tile is clickable and opens a modal (`#pvModal`) with a photo on top + a
  ~200-word overview. Overviews live as hidden `<div class="pv-full">` inside
  each tile (kept in the DOM for SEO, shown via JS).
- **Homepage "Where We Work / The Valencia Community"** (`id="places"`): 4
  `.place-card` tiles — Valencia City, Jávea & Dénia, Oliva & Cullera,
  Inland—Ontinyent. Same dim-until-hover + click-to-modal; overviews in
  `<div class="place-full">`. A `.places-region` line under the deck states
  coverage extends across Alicante towns and south into Murcia **without** giving
  them their own cards.
- **Mobile touch fix (most recent change).** iOS consumed the first tap applying
  `:hover`, so popups needed two taps. Fixed by gating **all** hover effects
  behind `@media (hover: hover) and (pointer: fine)`; under `@media (hover:
  none)` the `+` tap-cue is kept permanently visible + an `:active` press state.
  **⚠️ Any new hover-based interaction MUST follow this same pattern or it will
  re-break mobile.** Mobile is the majority of traffic — treat it as first-class
  and **test on a real phone**.

## Outstanding work (prioritize with the owner; nothing is urgent-broken)

1. **Popup copy review.** The 12 pillar + 4 area overviews (~3,000 words) are
   **AI-drafted** in the owner's voice, grounded only in claims the site already
   makes + general facts about Spain. Owner still needs to read/edit. Do not
   present as final.
2. **Two place photos are unverified stock.** Valencia City (`.pc-1`) and
   Inland—Ontinyent (`.pc-4`) still use generic Unsplash images (2 of the other
   4 originally turned out to be the wrong location — that's why this matters).
   Jávea & Dénia (`.pc-2` → `/javea-denia.jpg`) and Oliva & Cullera (`.pc-3` →
   `/oliva-cullera.jpg`) already use real owner-provided photos. When new photos
   arrive: resize to ~1600px wide, strip EXIF, JPEG quality ~82, commit to repo
   root, reference as `/filename.jpg`. Crop out recognizable faces.
3. **Alicante + Murcia as their own area cards — DEFERRED** (owner wants later).
   Blockers first: (a) **photos** — the existing Altaona/taolis images already
   on-site are genuine Murcia imagery and usable; nothing sourced for Alicante —
   **do not guess stock image IDs**; (b) **heading** — Murcia is a *separate
   autonomous community*, so the "The Valencia Community" H2, the homepage meta
   ("Valencia Community specialists") and SEO titles would need rewording (e.g.
   "Valencia, Alicante & Murcia"). **Alicante is already inside the Valencia
   Community** (Jávea, Dénia, Altea, Calpe, Benidorm are all Alicante province),
   so an Alicante-province card overlaps the existing Jávea & Dénia card —
   clarify city-vs-province with the owner.
4. **robots.txt / AI crawlers.** Owner chose to **allow** AI crawlers, and the
   origin `robots.txt` allows them, but Cloudflare's zone-managed robots.txt
   still prepends a content-signals block that blocks GPTBot/ClaudeBot/
   Google-Extended etc. To truly allow them the owner must turn **off**
   Cloudflare's managed robots.txt / "AI Crawl Control" feature in the dashboard
   (a toggle, not an API change — cannot be flipped programmatically). Affects
   AI-answer visibility only, not normal Google/Bing SEO.
5. **Performance — first pass DONE & live.** See "Performance model" below for
   what changed and the rules that come with it. Still open, deliberately:
   (a) the 14 pillar/place tile photos are hot-linked from `images.unsplash.com`
   (third-party, uncached, unoptimised) — they go away as owner photos arrive;
   (b) ~~favicon~~ **done** — see Performance model;
   (c) CSS/JS are still inline and unminified — **leave it that way** unless a
   build step is introduced; minifying by hand saves a few KB gzipped and makes
   these hand-authored files much harder to edit.

## Email capture & automation (migrated OFF Mailchimp → MailerLite)

Mailchimp was dropped because automations moved behind its paid tier. All signup
forms now post to a Cloudflare Pages Function; capture + the nurture sequence run
on **MailerLite's free tier**.

- **Function:** `functions/api/subscribe.js` (Cloudflare Pages Function, served at
  `/api/subscribe`). Receives the form POST, adds/upserts the subscriber to a
  MailerLite group via `connect.mailerlite.com/api/subscribers` (joining the group
  fires the automation), then 303-redirects. Never blocks the visitor if MailerLite
  is unreachable. Honeypot field is `website`; bad emails are dropped silently.
- **Env vars (Cloudflare Pages → Settings → Environment variables, Prod + Preview):**
  `MAILERLITE_API_KEY`, `ML_GROUP_GUIDE`, `ML_GROUP_NEWSLETTER`. Until these are set,
  forms still work — they just redirect to the thank-you pages without capturing.
- **Forms (15 total):** each posts to `/api/subscribe` with hidden `intent`
  (`guide` | `newsletter`) + `source` fields. `intent=guide` → guide/prospect group
  → `/thank-you` (instant PDF download). `intent=newsletter` → newsletter group →
  `/subscribed`. The Formspree contact form (`#cform` on index) is unrelated and
  untouched (still needs its own `YOUR_FORM_ID` filled in).
- **Automation — BUILT AND ACTIVE** in MailerLite (trigger: joins guide group):
  Email 1 Guide Delivery (immediate) → 3-day delay → Email 2 Day-3 Lifestyle →
  4-day delay → Email 3 Day-7 Process → 7-day delay → Email 4 Day-14 Decision →
  exit. Verified end-to-end 2026-08-06: live form submit → subscriber lands in
  the guide group → Email 1 delivered.
- The Mailchimp connected-site tracking script (`chimpstatic.com/mcjs`) was removed
  from all 14 pages. Do not re-add it.
- Guide PDF lives at `/spain-retirement-guide.pdf` (repo root) and is linked from
  `/thank-you` and inside Email 1.

## Performance model (added in the perf pass — don't undo these)

- **No image may be base64-inlined into the HTML.** The hero used to be a 306 KB
  JPEG inside a `data:` URI in the homepage CSS, which alone made `index.html`
  524 KB raw / 340 KB gzipped, all of it render-blocking. It is now
  `/hero-bg.{webp,jpg}` with a 1100px mobile variant (`/hero-bg-1100.*`) behind
  `@media (max-width: 760px)`. `index.html` is 117 KB raw / 29 KB gzipped.
- **The WebP pattern.** For `<img>`, use `<picture>` with a WebP `<source>` and
  the original as the `<img>` fallback. For CSS backgrounds, write the plain
  `url()` fallback FIRST and an `image-set(... type('image/webp') ...)`
  immediately after — browsers too old for `image-set`/`type()` discard the
  second declaration and keep the JPEG. Always ship both files.
- **Keep the hero preloads in sync.** The two `rel="preload" as="image"` tags in
  `index.html`'s `<head>` are `media`-scoped so each viewport preloads exactly
  one variant. If you change the hero filenames or the 760px breakpoint, change
  them there too or the page silently downloads the wrong image twice.
- **`hero.png` is the `og:image`, not a page asset.** Nothing renders it. Leave
  it as PNG-named JPEG; social scrapers have that URL cached.
- **Fonts are self-hosted in `/fonts/` — do not re-add Google Fonts.** They are
  variable woff2s (one file per family+style, latin + latin-ext, unicode-range
  gated), with the `@font-face` blocks inlined in each page's `<style>`. To
  change a weight, widen the `font-weight` range — do not add a file. `_headers`
  pins `/fonts/*` to a one-year immutable cache; **do not extend that to
  images**, which get replaced at the same filename.
- **Favicon exists now — keep it that way.** Before, no page declared an icon,
  so every browser requested `/favicon.ico`, hit the soft-404, and was served
  the whole 120 KB homepage as the icon on every fresh visit. There is now a
  gold sun on an olive tile: `favicon.svg` (source of truth, hand-written),
  `favicon.ico` (16/32/48), `apple-touch-icon.png` (180px, deliberately
  **square** — iOS applies its own rounded mask, so a pre-rounded icon would
  get double-rounded). All 14 pages link all three. If you redraw it, redraw
  the SVG first and regenerate the raster sizes from the same geometry.
- New images: ~1600px wide, strip EXIF, JPEG q82 + a `cwebp -q 80` sibling.

## Blog / Journal

The blog is called **"Building My Life in Spain — A Founder's Journal."**

- **Index:** `building-my-life-in-spain.html` (route `/building-my-life-in-spain`,
  already linked in every nav + footer). It lists category cards and an
  "editorial slate" of article cards. Posts are written by an outside content
  writer and pasted in — **we build the machinery, not the copy.**
- **Posts live at `/building-my-life-in-spain/<slug>`** — file
  `building-my-life-in-spain/<slug>.html`, served extensionless by Cloudflare
  Pages, as a topic cluster nested under the journal hub. (The hub file
  `building-my-life-in-spain.html` and the same-named directory coexist fine:
  `/building-my-life-in-spain` serves the .html, `/building-my-life-in-spain/<slug>`
  serves from the directory. There is no `building-my-life-in-spain/index.html`.)
  Slugs are lowercase-hyphenated. First live post:
  `non-lucrative-vs-digital-nomad-visa-spain`. **NB:** an earlier draft of this
  doc said posts live at `/blog/<slug>` — that was superseded; only the shared
  CSS lives under `/blog/`.
- **Shared stylesheet `/blog/blog.css`** styles every post (fonts, nav, footer,
  long-form typography, comparison tables, callouts). Deliberate exception to
  the site's inline-CSS pattern: with many near-identical posts, one shared file
  means a restyle is a single edit. Kept at the `/blog/` path as a plain asset
  location even though posts now live under `/building-my-life-in-spain/`. The
  journal index keeps its own inline CSS.
- **Template `blog/_template.html`** — the starting point for every post. It is
  **excluded from deploy** (rsync `--exclude` in `deploy.yml`), so it is never
  public. Each post has its own `BlogPosting` JSON-LD, canonical, OG/Twitter
  tags, GA snippet, and the shared nav/footer.

### To add a post
1. `cp blog/_template.html building-my-life-in-spain/<slug>.html`.
2. Replace every `{{PLACEHOLDER}}` (search `{{`): title, meta description, slug,
   OG image, ISO + display dates, reading time, category, hero image/alt/caption.
3. Paste the writer's copy into `<article class="post-body">`, replacing the
   DEMO block, using the shown elements (`p`, `h2`, `h3`, `blockquote`,
   `ul`/`ol`, `<figure>`, `.callout`, `.post-lead`). Delete the hero `<figure>`
   if the post has no lead image.
4. On `building-my-life-in-spain.html`, flip that article's card from a
   `<div class="article">` to `<a class="article" href="/blog/<slug>">` and swap
   the "In production" badge for a date (there's a worked example in an HTML
   comment right above the `slate-grid`).
5. Add a `<url>` for `/blog/<slug>` to `sitemap.xml`.
6. **Do not invent visa/tax/price figures** — publish only the writer's numbers.

## Guardrails

- **Do not invent** prices, tax figures, visa thresholds, or property-market
  statistics. A wrong claim to a buyer is a real problem. Ground copy in what
  the site already says + general facts.
- **Do not touch** Cloudflare zone settings, DNS, nameservers, WAF, or the
  www→root redirect.
- **Don't regress the SEO** (canonicals, titles/meta, schema, sitemap, robots).
- **Verify before publishing:** check computed CSS/behavior; for anything
  interactive, test at a mobile viewport **and on a real phone**.
- Headless-browser **screenshots on this stack are flaky** (blank frames below
  the fold); verify functionally via computed styles + dispatched DOM events
  rather than trusting screenshots alone.
