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
                "That page couldn't be found. Head back to Spanish AfterLife — immigration and property help for North Americans moving to Spain.", "/hero.png")

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
    if slug == "404" and not STAGING:  # production's 404: noindex, follow, no canonical
        robots = '<meta name="robots" content="noindex, follow">'

    t = title + (" — STAGING v2" if STAGING else "")
    ld = f'\n<script type="application/ld+json">{ORG_LD}</script>' if jsonld else ""
    return f"""{ga()}<title>{t}</title>
<meta name="description" content="{desc}">
{robots}
{'' if slug == "404" else f'<link rel="canonical" href="{canonical}">'}
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
<meta name="twitter:image" content="{BASE}{img}">{ld}
<style>{CHROME_CSS}</style>"""


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


# ------------------------------------------------------------------ analytics
# Production's Google tag, verbatim (origin/main has GA4 G-0D870F788P on all 21 pages and
# NO Plausible / Clarity). Emitted only in the production build so staging traffic never
# pollutes the property.
GA_ID = "G-0D870F788P"
def ga():
    if STAGING:
        return ""
    return f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>
"""


def home(anchor=""):
    """link to a homepage section from any page"""
    return href("home") + anchor


# ------------------------------------------------------------------ forms (production markup)
LOC_CA = ["Ontario", "British Columbia", "Alberta", "Quebec", "Other Canadian province"]
LOC_US = ["California", "New York", "Washington", "Illinois", "Texas", "Florida", "Other US state"]
INTEREST = ["Ready to move — need visa + property help",
            "Serious about it — want to understand the process",
            "Property only — already have residency sorted",
            "Visa only — property sorted",
            "Early stages — still doing the research"]


def contact_form():
    """production's Formspree consultation form, field for field (index.html #cform on origin/main)"""
    ca = "".join(f"<option>{o}</option>" for o in LOC_CA)
    us = "".join(f"<option>{o}</option>" for o in LOC_US)
    it = "".join(f"<option>{o}</option>" for o in INTEREST)
    return f"""<form class="cform" id="cform" action="https://formspree.io/f/xvzeevnb" method="POST">
    <input type="hidden" name="_subject" value="New enquiry — spanishafterlife.com">
    <input type="hidden" name="_next" value="https://spanishafterlife.com/message-received">
    <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-5000px">
    <div class="frow"><div class="field"><label for="cf-first">First Name</label><input id="cf-first" type="text" name="first_name" required></div><div class="field"><label for="cf-last">Last Name</label><input id="cf-last" type="text" name="last_name" required></div></div>
    <div class="field"><label for="cf-email">Email Address</label><input id="cf-email" type="email" name="email" required></div>
    <div class="field"><label for="cf-loc">Where are you based?</label><select id="cf-loc" name="location" required><option value="">Select country / province / state</option><optgroup label="Canada">{ca}</optgroup><optgroup label="United States">{us}</optgroup></select></div>
    <div class="field"><label for="cf-int">What's driving the move?</label><select id="cf-int" name="interest" required><option value="">Select one</option>{it}</select></div>
    <div class="field"><label for="cf-msg">Anything that would help us prepare</label><textarea id="cf-msg" name="message" placeholder="Budget, timeline, areas of interest, questions you already have..."></textarea></div>
    <button class="cbtn" type="submit">Book My Free Consultation</button>
    <p class="form-note">No sales pitch. No obligation. Just an honest conversation.</p>
  </form>"""


def footer(slug="home"):
    """production's full footer (three link columns, guide signup, legal line) in the v2 language"""
    return f"""<footer class="foot"><div class="foot-top"><div class="foot-sig">Why wait for the AfterLife?</div></div>
<div class="foot-grid">
  <div class="foot-brand"><div class="foot-mark"><b>Spanish</b> AfterLife</div>
    <p>Early retirement in Spain. Immigration concierge and buyer's agency for North Americans. Based in the Valencia Community. Operated by LJ Koch Group Inc.</p></div>
  <div class="foot-col"><h4>The Life</h4>
    <a href="{home('#life')}">The 12 Pillars</a><a href="{home('#places')}">The Places</a><a href="{home('#numbers')}">The Numbers</a><a href="{href('building-my-life-in-spain')}">Journal</a></div>
  <div class="foot-col"><h4>How We Help</h4>
    <a href="{href('fullafterlife')}">The Full AfterLife</a><a href="{href('immigration')}">Immigration Concierge</a><a href="{href('real-estate')}">Real Estate</a><a href="{href('available-properties')}">Properties</a><a href="{href('private-client')}">Private Client</a><a href="{home('#contact')}">Free Consultation</a></div>
  <div class="foot-col"><h4>Company</h4>
    <a href="/find-your-spain">Find Your Spain</a><a href="/about">About</a><a href="{home('#contact')}">Contact</a><a href="/privacy">Privacy Policy</a><a href="/guide">Free guide: the cost of moving to Spain</a><a href="/canada-quality-of-life">Retire in Spain from Canada</a><a href="/us-cash-out">Cash out &amp; retire in Spain (US)</a><a href="/us-sun-seekers">Retire somewhere warm (US)</a></div>
</div>
<div class="foot-signup">
  <div><h4>Your Complete Guide to Retiring in Spain</h4><p>The visa, the property, and the honest cost of the life &mdash; free, straight to your inbox.</p></div>
  <form class="gform foot-form" action="/api/subscribe" method="post">
    <input type="email" name="EMAIL" placeholder="Your email address" required aria-label="Email address">
    <button class="gbtn" type="submit">Send me the guide</button>
    <label class="consent"><input type="checkbox" name="consent" required><span>Email me the guide and the occasional honest update. I accept the <a href="/privacy">Privacy Policy</a> and can unsubscribe anytime.</span></label>
    <div aria-hidden="true" style="position:absolute;left:-5000px"><input type="text" name="website" tabindex="-1" autocomplete="off" value=""></div>
    <input type="hidden" name="intent" value="guide">
    <input type="hidden" name="source" value="{'index:hs-form' if slug=='home' else slug.split('/')[-1]+':fs-form'}">
  </form>
</div>
<div class="foot-bot"><span>&copy; 2026 Spanish AfterLife / LJ Koch Group Inc. All rights reserved.</span><span><a href="/privacy">Privacy Policy</a> &middot; Valencia Community, Spain</span></div></footer>"""


CHROME_CSS = """
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.3fr;gap:clamp(1.6rem,4vw,4rem);padding:clamp(2.2rem,5vh,3.5rem) 0;border-bottom:1px solid var(--line-d)}
.foot-mark{font-family:var(--serif);font-size:1.5rem;font-weight:360;margin-bottom:1rem}
.foot-brand p{font-size:.86rem;line-height:1.7;color:var(--cream-soft);max-width:36ch}
.foot-col{display:flex;flex-direction:column;gap:.55rem}
.foot-col h4{font-family:var(--sans);font-size:.64rem;font-weight:600;text-transform:uppercase;letter-spacing:.2em;color:var(--cream-soft);margin-bottom:.5rem}
.foot-col a{font-size:.9rem;color:var(--cream);opacity:.86;transition:opacity .3s}
.foot-col a:hover{opacity:1;text-decoration:underline}
.foot-signup{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4rem);align-items:start;padding:clamp(2rem,5vh,3rem) 0;border-bottom:1px solid var(--line-d)}
.foot-signup h4{font-family:var(--serif);font-size:clamp(1.2rem,2vw,1.6rem);font-weight:360;margin-bottom:.6rem}
.foot-signup p{font-size:.88rem;color:var(--cream-soft)}
.foot-form{margin-top:0}
.foot-bot a{text-decoration:underline}
.form-note{font-size:.8rem;color:var(--stone);margin-top:.2rem}
@media(max-width:900px){.foot-grid{grid-template-columns:1fr 1fr}.foot-brand{grid-column:1/-1}.foot-signup{grid-template-columns:1fr}}
@media(max-width:520px){.foot-grid{grid-template-columns:1fr}}
"""
