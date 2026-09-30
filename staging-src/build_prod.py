#!/usr/bin/env python3
"""Build the ERA v2 site at PRODUCTION paths into a checkout of main.

    python3 staging-src/build_prod.py <main-worktree>

Writes every page as <slug>.html (Cloudflare Pages serves /immigration from immigration.html
with no redirect, so every live URL is unchanged), copies staging/media -> media/, and leaves
main's robots.txt, sitemap.xml, _headers, functions/, favicons and assets untouched.
"""
import os, sys, io, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import era_seo as SEO
SEO.STAGING = False                      # must be set before the generators import
import gen_era_v2 as V2
import gen_era_pages as P
import gen_era_services as S
import gen_era_reskin as R
import build_css as CSS

OUT = os.path.abspath(sys.argv[1])
ROOTS = ["available-properties", "building-my-life-in-spain", "immigration", "real-estate",
         "fullafterlife", "private-client"] + list(R.PAGES)

def prodlinks(html):
    # /v2/<slug>/  -> /<slug>   ;  /v2/#x -> /#x  ;  /v2/ -> /
    for slug in sorted(ROOTS, key=len, reverse=True):
        html = html.replace(f'"/v2/{slug}/"', f'"/{slug}"').replace(f'"/v2/{slug}/#', f'"/{slug}#')
    html = html.replace('"/v2/#', '"/#').replace('"/v2/"', '"/"')
    assert "/v2/" not in html, re.findall(r'.{40}/v2/.{40}', html)[:3]
    return html

WROTE = []


def write(rel, html):
    WROTE.append(rel)
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    html = prodlinks(html).replace('href="/era.css"', f'href="/era.css?v={_CSS_V}"')
    io.open(p, "w", encoding="utf-8").write(html)
    print("wrote", rel, len(html) // 1024, "KB")

_p, _n = CSS.write(OUT)
# era.css is not content-hashed, so a returning visitor can get NEW html with an
# OLD stylesheet until their cache expires (Pages serves it max-age=14400). Stamp
# the link with a hash of the file so every change is a new URL.
import hashlib
_CSS_V = hashlib.sha1(io.open(_p, "rb").read()).hexdigest()[:8]
print("wrote era.css", _n // 1024, "KB  version", _CSS_V)

write("index.html", V2.HTML)
write("available-properties.html", P.build_properties())
write("building-my-life-in-spain.html", P.build_journal())
write("404.html", P.build_404())
for slug in ("immigration", "real-estate", "fullafterlife", "private-client"):
    write(slug + ".html", S.build(slug))
for slug in R.PAGES:
    write(slug + ".html", R.build(slug))

src = os.path.join(os.path.dirname(HERE), "staging", "media")
dst = os.path.join(OUT, "media")
for dp, dn, fn in os.walk(src):
    for f in fn:
        a = os.path.join(dp, f); b = os.path.join(dst, os.path.relpath(a, src))
        os.makedirs(os.path.dirname(b), exist_ok=True)
        if f != "ronda.mp4" or True:
            shutil.copy2(a, b)
print("copied media/")

# A missing image does not fail loudly - it paints an empty box, and only on the
# viewport whose variant is absent, so it survives every desktop review. Four of
# these reached production. Fail the build instead.
_IMG = re.compile(r"url\('(/[^']+)'\)")
_missing, _seen = [], set()
for _rel in WROTE:                       # only what THIS build produced
        _html = io.open(os.path.join(OUT, _rel), encoding="utf-8").read()
        for _u in _IMG.findall(_html) + re.findall(r'src="(/media/[^"]+)"', _html):
            if _u in _seen:
                continue
            _seen.add(_u)
            if not os.path.isfile(os.path.join(OUT, _u.lstrip("/"))):
                _missing.append(_u)
if _missing:
    raise SystemExit("BUILD FAILED - referenced but not on disk:\n  " + "\n  ".join(sorted(_missing)))
print(f"verified {len(_seen)} image references, all present")
