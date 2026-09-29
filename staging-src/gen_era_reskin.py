#!/usr/bin/env python3
"""Re-skin the production pages that were not hand-rebuilt into the ERA v2 language.

Copy is NEVER retyped: each page's <head> (title, description, canonical, og, JSON-LD,
Google tag) and its content markup are lifted verbatim from origin/main. Only the chrome
(nav, footer), the hero treatment and the stylesheet change.

    build(slug) -> full HTML string for the production path of that page
"""
import os, re, io, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import era_seo as SEO
import gen_era_v2 as V2
import gen_era_pages as P

PAGES = {  # slug (= production path without .html) : hero image
    "about": "/media/xabia-1.webp",
    "privacy": "/media/valencia-1.webp",
    "canada-quality-of-life": "/media/oliva-1.webp",
    "us-cash-out": "/media/home-2.webp",
    "us-sun-seekers": "/media/oliva-2.webp",
    "thank-you": "/media/oliva-3.webp",
    "message-received": "/media/oliva-3.webp",
    "subscribed": "/media/oliva-3.webp",
    "building-my-life-in-spain/non-lucrative-vs-digital-nomad-visa-spain": "/media/valencia-2.webp",
    "guide": "/guide-cover.png",
    "find-your-spain": "/media/oliva-5.webp",
}

def prod(slug):
    return subprocess.run(["git", "show", f"{SEO.SRC_REF}:{slug}.html"], cwd=HERE,
                          capture_output=True, text=True, check=True).stdout

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..460;1,9..144,300..400&family=Archivo:wght@400;500;600&family=Ephesis&display=swap" rel="stylesheet">"""

RS_CSS = r"""
/* --- re-skinned production pages --- */
.rs{padding:clamp(4rem,11vh,8rem) var(--pad)}
.rs .inner{max-width:880px;margin:0 auto}
.rs .inner.wide{max-width:1240px}
.rs-alt{background:#EAEAE0}
.rs .label,.rs .eyebrow{display:block;font-family:var(--sans);font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:.24em;color:var(--ink-soft);margin-bottom:1.2rem}
.dark .label,.dark .eyebrow,.rs-hero .eyebrow{color:var(--cream-soft)}
.rs h2,.rs .heading{font-family:var(--serif);font-weight:340;font-size:clamp(1.9rem,4vw,3.2rem);line-height:1.08;margin-bottom:1.6rem;max-width:22ch}
.rs h2 em,.rs-hero h1 em{font-style:italic;font-weight:300}
.rs h3{font-family:var(--serif);font-weight:360;font-size:clamp(1.3rem,2vw,1.7rem);margin:2rem 0 .8rem}
.rs h3.sub{font-family:var(--serif);font-weight:380;font-size:1.2rem;margin-bottom:.4rem;margin-top:0}
.rs p{color:var(--stone);margin-bottom:1rem;max-width:66ch}
.dark.rs p{color:var(--cream-soft)}
.rs p.lede{font-family:var(--serif);font-size:clamp(1.25rem,2vw,1.6rem);line-height:1.45;color:var(--ink)}
.rs a:not(.btn){text-decoration:underline;text-underline-offset:3px}
.rs ul,.rs ol{margin:0 0 1.2rem 1.2rem;color:var(--stone)}
.rs li{margin-bottom:.5rem;max-width:64ch}
.rs strong{color:var(--ink);font-weight:600}
.dark.rs strong{color:var(--cream)}
.rs table{width:100%;border-collapse:collapse;margin:1.4rem 0;font-size:.92rem}
.rs th,.rs td{text-align:left;padding:.8rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
.rs th{font-size:.66rem;text-transform:uppercase;letter-spacing:.14em;color:var(--ink-soft);font-weight:600}
.rs .prose{max-width:none}
.mirror{display:grid;grid-template-columns:1fr 1fr;gap:0 clamp(1.5rem,4vw,3.5rem);margin-top:1.5rem}
.m-item{display:flex;gap:1rem;padding:1.1rem 0;border-top:1px solid var(--line);align-items:baseline}
.m-item p{margin:0;font-family:var(--serif);font-size:clamp(1.02rem,1.5vw,1.25rem);line-height:1.4;color:var(--ink)}
.m-check{font-size:.9rem;color:var(--ink-soft)}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4rem);margin-top:1.5rem}
.compare .col{padding:clamp(1.4rem,3vw,2.4rem)}
.compare .col.leave{border:1px solid var(--line)}
.compare .col.spain{background:var(--ink);color:var(--cream)}
.compare .col h3{margin-top:0}
.compare .row{display:grid;grid-template-columns:120px 1fr;gap:1rem;padding:1rem 0;border-top:1px solid var(--line)}
.compare .col.spain .row{border-color:var(--line-d)}
.compare .row strong{font-family:var(--sans);font-size:.66rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;color:inherit;opacity:.75;padding-top:.2rem}
.compare .row span{font-family:var(--serif);font-size:1.05rem;line-height:1.45}
.compare .col.leave .row span{color:var(--stone)}
.steps{display:grid;gap:0;margin-top:1.5rem}
.rs .step{display:grid;grid-template-columns:3.2rem 1fr;gap:clamp(1rem,3vw,2rem);padding:1.4rem 0;border-top:1px solid var(--line);align-items:baseline}
.dark .step{border-color:var(--line-d)}
.rs .step .n{font-family:var(--serif);font-size:clamp(1.4rem,2.4vw,1.9rem);color:var(--ink-soft)}
.dark .step .n{color:var(--cream-soft)}
.rs .step p{margin:0}
.rs-note .inner{border-top:1px solid var(--line);padding-top:2rem}
.rs-note p{font-family:var(--serif);font-size:clamp(1.1rem,1.7vw,1.4rem);line-height:1.5;color:var(--ink);max-width:60ch}
.rs-cta{text-align:left}
.rs-cta .cta-inner{max-width:880px;margin:0 auto}
.rs-cta h2{color:var(--cream)}
.rs-cta .cta-inner>div:last-child{display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.8rem}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:.9rem 1.7rem;border-radius:100px;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;border:1px solid currentColor;text-decoration:none}
.btn-terra,.btn-white{background:var(--cream);color:var(--ink);border-color:var(--cream)}
.rs:not(.dark) .btn-terra{background:var(--ink);color:var(--cream);border-color:var(--ink)}
.btn-outline-white,.btn-ghost-white{color:var(--cream);border-color:var(--on-dark-quiet)}
.rs-hero{min-height:68vh;padding-top:clamp(7rem,16vh,10rem)}
.rs-hero .eyebrow{display:block;font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:.24em;margin-bottom:1.4rem}
.rs-hero h1{font-size:clamp(2.4rem,5.8vw,4.8rem);max-width:17ch;line-height:1.04;font-weight:340}
.rs-hero .ph-desc,.rs-hero p{max-width:60ch;margin-top:1.4rem;color:var(--on-dark);font-size:clamp(1rem,1.3vw,1.15rem)}
.rs-hero .ph-cta,.rs-hero p:has(.btn){display:flex;gap:1rem;flex-wrap:wrap;margin-top:2rem}
.rs-hero .post-meta{display:flex;gap:.8rem;align-items:center;margin-top:1.4rem;font-size:.72rem;text-transform:uppercase;letter-spacing:.16em;color:var(--cream-soft)}
.rs-hero .dot{width:4px;height:4px;border-radius:50%;background:currentColor;display:inline-block}
.post-wrap{padding:clamp(3.5rem,9vh,6rem) var(--pad)}
.post-body{max-width:720px;margin:0 auto}
.post-body p,.post-body li{font-size:1.08rem;line-height:1.8;color:#2d3548;max-width:none}
.post-body p{margin-bottom:1.3rem}
.post-body h2{font-family:var(--serif);font-weight:360;font-size:clamp(1.6rem,3vw,2.2rem);margin:2.8rem 0 1rem;line-height:1.15}
.post-body h3{font-family:var(--serif);font-weight:380;font-size:1.35rem;margin:2rem 0 .7rem}
.post-body ul,.post-body ol{margin:0 0 1.3rem 1.3rem}
.post-body a{text-decoration:underline;text-underline-offset:3px}
.post-body strong{color:var(--ink)}
.post-body table{width:100%;border-collapse:collapse;font-size:.94rem;margin:1.5rem 0}
.post-body th,.post-body td{text-align:left;padding:.75rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
.post-body th{font-size:.66rem;text-transform:uppercase;letter-spacing:.14em;color:var(--ink-soft)}
.post-table-wrap{overflow-x:auto}
.callout{border-left:2px solid var(--ink);padding:1rem 1.4rem;margin:1.8rem 0;background:#EAEAE0}
.post-end{max-width:720px;margin:0 auto;padding:0 var(--pad) clamp(3rem,8vh,5rem)}
.post-back{display:inline-block;font-size:.72rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;margin-bottom:2rem;min-height:44px}
.author-card{border-top:1px solid var(--line);padding-top:1.6rem}
.a-name{font-family:var(--serif);font-size:1.3rem;margin-bottom:.4rem}
.a-bio{color:var(--stone);font-size:.95rem}
.a-bio a{text-decoration:underline}
.news{background:var(--ink);color:var(--cream);padding:clamp(4rem,10vh,7rem) var(--pad)}
.news-inner{max-width:720px;margin:0 auto}
.news .eyebrow{display:block;font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:.24em;color:var(--cream-soft);margin-bottom:1.2rem}
.news h2{font-family:var(--serif);font-weight:340;font-size:clamp(1.9rem,4vw,3rem);margin-bottom:1rem}
.news p{color:var(--cream-soft)}
.news-form{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.6rem;position:relative}
.news-form input[type=email]{flex:1;min-width:220px;background:transparent;border:0;border-bottom:1px solid var(--line-d);color:var(--cream);padding:.85rem .2rem;font-size:1rem}
.news-form button{background:var(--cream);color:var(--ink);border:0;border-radius:100px;padding:.9rem 1.7rem;min-height:44px;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;cursor:pointer}
.news-consent{display:block;margin-top:1rem;font-size:.8rem;color:var(--cream-soft)}
.news-consent a{text-decoration:underline}
.news-note{font-size:.76rem;margin-top:.8rem}
/* guide landing page */
.lm{display:grid;grid-template-columns:1.1fr .9fr;min-height:100svh;padding-top:clamp(5rem,10vh,6rem)}
.lm-right{padding-top:clamp(6rem,12vh,8rem)!important}\n.lm-left{position:relative;background:var(--ink);color:var(--cream);padding:clamp(6rem,14vh,9rem) var(--pad) clamp(3rem,8vh,5rem);display:flex;align-items:center;overflow:hidden}
.lm-left .media{position:absolute;inset:0;opacity:.28}
.lm-left-inner{position:relative;z-index:1;max-width:560px}
.lm-eyebrow{font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:.24em;color:var(--cream-soft);margin-bottom:1.4rem}
.lm h1{font-size:clamp(2.4rem,5vw,4.2rem);line-height:1.04;font-weight:340;margin-bottom:1.4rem}
.lm h1 em{font-style:italic;font-weight:300}
.lm-left p{color:rgba(243,243,236,.84);max-width:52ch}
.lm-list{list-style:none;margin-top:1.8rem}
.lm-list li{padding:.8rem 0;border-top:1px solid var(--line-d);color:var(--on-dark);font-size:.98rem}
.lm-right{display:flex;align-items:center;padding:clamp(3rem,8vh,5rem) var(--pad)}
.lm-form-wrap{max-width:440px;width:100%}
.lm-form-wrap h2{font-family:var(--serif);font-weight:340;font-size:clamp(1.8rem,3vw,2.6rem);margin-bottom:.6rem}
.lm-form-wrap .sub{color:var(--stone);margin-bottom:1.6rem}
.lm-field input{width:100%;background:transparent;border:0;border-bottom:1px solid var(--line);padding:.8rem 0;font-size:1rem;margin-bottom:1rem;color:var(--ink)}
.lm-consent{display:block;font-size:.8rem;color:var(--stone);margin:.6rem 0 1.4rem}
.lm-consent a,.lm-trust a{text-decoration:underline}
.lm-submit{background:var(--ink);color:var(--cream);border:0;border-radius:100px;padding:1rem 1.8rem;min-height:44px;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;cursor:pointer}
.lm-trust{font-size:.8rem;color:var(--stone);margin-top:1.6rem;line-height:1.6}
@media(max-width:900px){.mirror,.compare,.lm{grid-template-columns:1fr}.compare .row{grid-template-columns:1fr;gap:.3rem}}
"""

KEEP_STYLE = re.compile(r'-5000px')

def strip_styles(html):
    # production inline styles carry the old palette; keep only the honeypot hiders
    def f(m):
        st = m.group(1)
        if KEEP_STYLE.search(st):
            return m.group(0)
        cls = ' class="btn btn-terra"' if re.search(r'padding:[^;]*;.*background:#', st) else ""
        return cls
    return re.sub(r'\sstyle="([^"]*)"', f, html)

def head_of(src):
    h = src[src.find("<head>") + 6:src.find("</head>")]
    h = re.sub(r'<style.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<link[^>]*(fonts\.googleapis|fonts\.gstatic|rel="preload"|blog\.css)[^>]*>\s*', '', h)
    return h.strip()

def hero(open_tag_inner, img):
    return (f'<header class="subhero rs-hero" id="top"><div class="media"><div class="media-img" '
            f"style=\"{SEO.bgv(img)}\"></div></div><div class=\"subhero-in\">")

def body_standard(src, img):
    b = src[src.find("<body"):]
    start = min(i for i in (b.find('<header class="page-header"'), b.find('<header class="post-header"')) if i >= 0)
    end = b.rfind("<footer")
    c = b[start:end]
    c = re.sub(r'<script.*?</script>', '', c, flags=re.S)
    c = strip_styles(c)
    c = re.sub(r'<header class="page-header">\s*<div class="ph-inner">', hero(None, img), c, count=1)
    c = re.sub(r'<header class="post-header">\s*<div class="post-header-inner">', hero(None, img), c, count=1)
    alt = [0]
    def sec(m):
        cls = m.group(1)
        if cls in ("bg-linen-dark",):
            return '<section class="rs dark">'
        if cls == "founder-note":
            return '<section class="rs rs-note">'
        if cls == "cta-section":
            return '<section class="rs dark rs-cta">'
        if cls == "bg-linen":
            return '<section class="rs rs-alt">'
        return '<section class="rs">'
    c = re.sub(r'<section class="([^"]+)">', sec, c)
    return c



# Moves focus to the new screen when the quiz advances. Additive: it observes the
# class change rather than touching the quiz's own logic.
FYS_A11Y = """
<script>
(function(){
  var seen=null;
  function focusActive(){
    var a=document.querySelector('.screen.active'); if(!a||a===seen) return; seen=a;
    var t=a.querySelector('#q-prompt,h1,h2')||a;
    if(!t.hasAttribute('tabindex')) t.setAttribute('tabindex','-1');
    try{ t.focus({preventScroll:true}); }catch(e){ t.focus(); }
  }
  var mo=new MutationObserver(focusActive);
  document.querySelectorAll('.screen').forEach(function(s){
    mo.observe(s,{attributes:true,attributeFilter:['class']});
  });
})();
</script>"""


def demote_h4(html):
    """production nests h4 directly under h2 on these pages; promote to h3 (same look via .sub)"""
    def op(m):
        attrs = m.group(1) or ""
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="sub ', 1)
        else:
            attrs += ' class="sub"'
        return "<h3" + attrs + ">"
    html = re.sub(r'<h4([^>]*)>', op, html)
    return html.replace("</h4>", "</h3>")


def build(slug):
    src = prod(slug)
    img = PAGES[slug]
    head = head_of(src)
    if slug == "guide":
        b = src[src.find('<div class="lm-main">'):src.find('<div class="lm-foot">')]
        b = strip_styles(b).replace('<div class="lm-main">', '<main class="lm" id="main">', 1)
        b = b.replace('<div class="lm-left">', f'<div class="lm-left"><div class="media"><div class="media-img" style="{SEO.bgv("/media/oliva-3.webp")}"></div></div>', 1)
        b = b[:b.rfind("</div>")] + "</main>"
        body = b
    elif slug == "find-your-spain":
        # the quiz keeps its own markup + script; only palette/typography change (see FYS_CSS)
        b = src[src.find('<div class="stage">'):src.rfind("</body>")]
        # the quiz swaps .screen elements with display:none/block, so a screen reader
        # gets no announcement when the question changes, and focus is left on the
        # option button that just disappeared.
        b = b.replace('<div class="screen" id="screen-q">',
                      '<div class="screen" id="screen-q" role="group" aria-live="polite" aria-atomic="true">')
        b = b.replace('<div class="screen result" id="screen-result">',
                      '<div class="screen result" id="screen-result" role="group" aria-live="polite">')
        # the question text is the screen's heading; swap the whole element so the
        # closing tag matches (it is empty in the source - the quiz fills it)
        b = b.replace('<div class="q-prompt" id="q-prompt"></div>',
                      '<h2 class="q-prompt" id="q-prompt" tabindex="-1"></h2>')
        body = f'<main id="main" class="fys">{b}</main>' + FYS_A11Y
        orig_css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
        head += "\n<style>" + fys_css(orig_css) + "</style>"
    else:
        body = body_standard(src, img)
    body = demote_h4(body)
    if "<main" not in body:                       # every page needs the landmark the skip link targets
        body = f'<main id="main">\n{body}\n</main>'
    html = f"""<!doctype html><html lang="en"><head>
{head}
<script>document.documentElement.className='js';</script>
{FONTS}
{SEO.css_link()}</head><body>
{SEO.badge()}
<a class="skip" href="#main">Skip to content</a>
{P.NAV}
{body}
{SEO.footer(slug)}
<script>{P.JS}</script>
</body></html>"""
    if slug == "guide":  # a standalone ad landing page in production: brand bar only, no site nav
        html = html.replace(P.NAV, '<nav class="nav"><a class="brand" href="/"><b>Spanish</b> AfterLife</a></nav>')
        html = html.replace(SEO.footer(slug), '<footer class="foot"><div class="foot-bot"><span>&copy; 2026 LJ Koch Group Inc. &middot; Spanish AfterLife &middot; <a href="/privacy">Privacy</a></span><span>Valencia Community, Spain</span></div></footer>')
    if SEO.STAGING:
        html = re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com[^"]*"></script>\s*<script>.*?</script>', '', html, flags=re.S)
        html = re.sub(r'<meta name="robots"[^>]*>', '', html)
        html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex,nofollow">', 1)
    return html

def _rules(css):
    """split top-level CSS into (prelude, block) pairs, keeping @media/@keyframes blocks whole"""
    out, i, n = [], 0, len(css)
    while i < n:
        a = css.find("{", i)
        if a < 0: break
        depth, k = 1, a + 1
        while depth and k < n:
            depth += (css[k] == "{") - (css[k] == "}"); k += 1
        out.append((css[i:a].strip(), css[a:k])); i = k
    return out

DROP = re.compile(r'^(\*|:root|html|body|h1|nav|\.nav-|\.hamburger|\.mobile-menu|footer|\.footer|@font-face)')

def fys_css(css):
    """The quiz keeps its own layout CSS; palette, fonts and the site chrome come from v2."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    keep = []
    for pre, blk in _rules(css):
        if DROP.search(pre):
            continue
        if pre.startswith("@media"):
            inner = [f"{p}{b}" for p, b in _rules(blk[1:-1]) if not DROP.search(p)]
            blk = "{" + "".join(inner) + "}"
        keep.append(pre + blk)
    css = "".join(keep)
    for a, b in {"'Cormorant Garamond', serif": "var(--serif)", "'Cormorant Garamond'": "var(--serif)",
                 "'DM Sans', sans-serif": "var(--sans)", "'DM Sans'": "var(--sans)",
                 "#b05a30": "#ffffff", "rgba(196,105,58,": "rgba(243,243,236,", "rgba(74,108,130,": "rgba(243,243,236,"}.items():
        css = css.replace(a, b)
    return (".fys{--terracotta:#F3F3EC;--linen:#F3F3EC;--olive:#17233B;--saffron:#d9cda9;--slate:#9aa3b5;"
            "--stone:#aab1bf;--white:#17233B;--linen-dark:#EAEAE0}\n.fys h1,.fys h2,.fys h3{font-family:var(--serif);font-weight:340}\n"
            + css + "\n.fys .stage{padding-top:5.5rem}\n")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "staging", "v2")
    for slug in PAGES:
        html = build(slug)
        p = os.path.join(out, slug, "index.html") if SEO.STAGING else os.path.join(out, slug + ".html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, "w", encoding="utf-8").write(html)
        print("wrote", p, len(html)//1024, "KB")
