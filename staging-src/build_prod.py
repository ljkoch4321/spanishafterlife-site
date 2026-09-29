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

def write(rel, html):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8").write(prodlinks(html))
    print("wrote", rel, len(html) // 1024, "KB")

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
