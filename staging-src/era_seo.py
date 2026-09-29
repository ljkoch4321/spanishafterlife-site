#!/usr/bin/env python3
"""Shared head/SEO block for every ERA v2 page.

ONE switch controls staging vs production:

    STAGING = True   -> noindex,nofollow + the staging badge, pages served under /v2/
    STAGING = False  -> indexable, badge removed, pages served at their production paths

Canonicals always point at the PRODUCTION url, so the indexed URL set never changes.
Slugs deliberately match production (/available-properties, /building-my-life-in-spain)
so no indexed URL needs a 301 when this replaces the live site.
"""

STAGING = True
BASE = "https://spanishafterlife.com"

# Titles / descriptions / og images are the PRODUCTION ones, verbatim, so the indexed
# snippets do not change. staging-src/content/prod_meta.json is extracted from
# origin/main — never hand-write these.
import os as _os, io as _io, json as _json
_META = _json.load(_io.open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                          "content", "prod_meta.json"), encoding="utf-8"))
_PATHS = {
    "home": "/", "immigration": "/immigration", "real-estate": "/real-estate",
    "available-properties": "/available-properties", "fullafterlife": "/fullafterlife",
    "private-client": "/private-client",
    "building-my-life-in-spain": "/building-my-life-in-spain",
}
PAGES = {k: (_PATHS[k], _META[k]["title"], _META[k]["desc"],
             _META[k]["og"].replace("https://spanishafterlife.com", "")) for k in _PATHS}
PAGES["404"] = ("/404", "Page not found (404) | Spanish AfterLife",
                "That page does not exist. Find your way back to Spanish AfterLife.", "/hero.png")

ORG_LD = """{
"@context":"https://schema.org","@type":"Organization",
"@id":"https://spanishafterlife.com/#organization",
"name":"Spanish AfterLife","legalName":"LJ Koch Group Inc.",
"url":"https://spanishafterlife.com","logo":"https://spanishafterlife.com/logo.png",
"description":"Concierge immigration and real estate for North Americans retiring to Spain's Valencia Community.",
"areaServed":"Valencia Community, Spain",
"founder":{"@type":"Person","@id":"https://spanishafterlife.com/#ljkoch","name":"LJ Koch"}
}"""


def href(slug):
    """in-prototype link for a page (staging keeps everything under /v2/)"""
    path = PAGES[slug][0]
    return ("/v2" + ("/" if path == "/" else path + "/")) if STAGING else path


def head(slug, jsonld=False):
    path, title, desc, img = PAGES[slug]
    canonical = BASE + path
    robots = ('<meta name="robots" content="noindex,nofollow">' if STAGING
              else '<meta name="robots" content="index,follow,max-image-preview:large">')
    t = title + (" — STAGING v2" if STAGING else "")
    ld = f'\n<script type="application/ld+json">{ORG_LD}</script>' if jsonld else ""
    return f"""<title>{t}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spanish AfterLife">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}{img}">{ld}"""


def badge():
    return '<div id="badge">Staging v2 &middot; ERA flow</div>' if STAGING else ""


def sitemap():
    """Production sitemap: the 7 rebuilt pages plus the 8 that keep their current design,
    so the indexed URL set is unchanged."""
    keep = ["/building-my-life-in-spain/non-lucrative-vs-digital-nomad-visa-spain", "/about",
            "/find-your-spain", "/guide", "/canada-quality-of-life", "/us-cash-out",
            "/us-sun-seekers", "/privacy"]
    paths = [PAGES[s][0] for s in PAGES if s != "404"] + keep
    urls = "".join(f"\n <url><loc>{BASE}{p}</loc></url>" for p in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}\n</urlset>\n'
