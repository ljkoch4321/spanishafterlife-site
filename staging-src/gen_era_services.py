#!/usr/bin/env python3
"""The four service pages, rebuilt in the ERA v2 language:

    staging/v2/immigration/      staging/v2/real-estate/
    staging/v2/fullafterlife/    staging/v2/private-client/

Content comes from staging-src/content/*.json, which extract_services.py lifts
verbatim out of the production pages on origin/main. Copy and figures are never
retyped here — this file only decides layout — so prices cannot drift.

Chrome (nav/menu/footer) and CSS are imported from gen_era_pages / gen_era_v2 so
all seven prototype pages stay visually identical.
"""
import os, sys, io, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_era_v2 as V2
import gen_era_pages as P
import era_seo as SEO

ROOT = os.path.join(os.path.dirname(HERE), "staging", "v2")
CONTENT = os.path.join(HERE, "content")

# hero image per page — the owner's own photography, one each so they read distinct
HERO = {
    "immigration":    "/media/valencia-2.webp",
    "real-estate":    "/media/home-3.webp",
    "fullafterlife":  "/media/oliva-2.webp",
    "private-client": "/media/valencia-3.webp",
}
CHAPTER = {
    "immigration":    ("/media/valencia-1.webp", "Your legal right|to live here."),
    "real-estate":    ("/media/oliva-2.webp",    "We represent you.|Never the seller."),
    "fullafterlife":  ("/media/home-1.webp",     "One relationship,|start to finish."),
    "private-client": ("/media/oliva-5.webp",    "The founder,|beside you."),
}

SVC_CSS = """
/* --- service pages --- */
.svc-p{max-width:62ch;color:var(--stone)}
.dark .svc-p{color:rgba(243,243,236,.82)}
.svc-p+.svc-p{margin-top:1rem}
.inc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:clamp(1.5rem,3vw,3rem);margin-top:clamp(2rem,5vh,3rem)}
.inc{border-top:1px solid var(--line);padding-top:1.1rem}
.dark .inc{border-top-color:var(--line-d)}
.inc h3{font-family:var(--sans);font-size:.66rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--ink-soft);margin-bottom:1rem}
.dark .inc h3{color:var(--cream-soft)}
.inc ul{list-style:none}
.inc li{font-size:.94rem;color:var(--stone);padding:.45rem 0 .45rem 1.1rem;position:relative;line-height:1.6}
.dark .inc li{color:rgba(243,243,236,.8)}
.inc li::before{content:"";position:absolute;left:0;top:.95rem;width:7px;height:1px;background:currentColor;opacity:.5}
.svc-steps{margin-top:clamp(2rem,5vh,3rem);border-top:1px solid var(--line)}
.dark .svc-steps{border-top-color:var(--line-d)}
.svc-step{display:grid;grid-template-columns:70px 1fr;gap:clamp(1rem,2.5vw,2.5rem);padding:1.5rem 0;border-bottom:1px solid var(--line);align-items:baseline}
.dark .svc-step{border-bottom-color:var(--line-d)}
.svc-step b{font-family:var(--serif);font-size:1rem;font-weight:400;color:var(--stone)}
.dark .svc-step b{color:var(--cream-soft)}
.svc-step h3{font-family:var(--serif);font-size:clamp(1.1rem,1.9vw,1.5rem);font-weight:360;letter-spacing:-.015em;margin-bottom:.45rem}
.svc-step p{font-size:.94rem;color:var(--stone);max-width:64ch}
.dark .svc-step p{color:rgba(243,243,236,.78)}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:clamp(1.2rem,2.5vw,2rem);margin-top:clamp(2rem,5vh,3rem)}
.svc-card{border:1px solid var(--line);padding:clamp(1.3rem,2.4vw,1.9rem)}
.dark .svc-card{border-color:var(--line-d)}
.svc-card .tag{display:block;font-family:var(--sans);font-size:.6rem;text-transform:uppercase;letter-spacing:.18em;font-weight:600;color:var(--ink-soft);margin-bottom:.9rem}
.dark .svc-card .tag{color:var(--cream-soft)}
.svc-card h3{font-family:var(--serif);font-size:clamp(1.15rem,1.9vw,1.5rem);font-weight:360;letter-spacing:-.015em;margin-bottom:.6rem}
.svc-card p{font-size:.94rem;color:var(--stone)}
.dark .svc-card p{color:rgba(243,243,236,.8)}
.money-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:clamp(1.5rem,4vw,4rem);margin-top:clamp(2rem,5vh,3rem)}
.money-col h3{font-family:var(--serif);font-size:clamp(1.2rem,2vw,1.6rem);font-weight:360;margin-bottom:.5rem}
.money-col .amt{display:block;font-family:var(--serif);font-size:clamp(1.8rem,3.4vw,2.6rem);font-weight:340;line-height:1;margin-bottom:1rem;color:var(--ink)}
.dark .money-col .amt{color:var(--cream)}
.faq-list{margin-top:clamp(2rem,5vh,3rem);border-top:1px solid var(--line)}
.dark .faq-list{border-top-color:var(--line-d)}
.faq-list details{border-bottom:1px solid var(--line)}
.dark .faq-list details{border-bottom-color:var(--line-d)}
.faq-list summary{list-style:none;cursor:pointer;padding:1.35rem 2.5rem 1.35rem 0;position:relative;font-family:var(--serif);font-size:clamp(1.05rem,1.7vw,1.35rem);font-weight:360;letter-spacing:-.01em}
.faq-list summary::-webkit-details-marker{display:none}
.faq-list summary::after{content:"+";position:absolute;right:.25rem;top:50%;transform:translateY(-50%);font-family:var(--sans);font-size:1.1rem;color:var(--ink-soft);transition:transform .4s var(--ease)}
.dark .faq-list summary::after{color:var(--cream-soft)}
.faq-list details[open] summary::after{content:"\\2013"}
.faq-list .a{padding:0 2.5rem 1.5rem 0;font-size:.96rem;color:var(--stone);max-width:72ch}
.dark .faq-list .a{color:rgba(243,243,236,.8)}
.chips{display:flex;flex-wrap:wrap;gap:clamp(1.5rem,4vw,3.5rem);margin-top:2.2rem}
.chip b{display:block;font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.4rem);font-weight:340;line-height:1;color:var(--cream)}
.chip span{font-size:.64rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--cream-soft)}
.pk-price{display:block;font-family:var(--serif);font-size:clamp(1.8rem,3.2vw,2.6rem);font-weight:340;line-height:1;margin:.2rem 0 .9rem}
.callout{margin-top:clamp(2rem,5vh,3rem);max-width:68ch;border-top:1px solid var(--line);padding-top:1.4rem}
.dark .callout{border-top-color:var(--line-d)}
.callout h3{font-family:var(--serif);font-size:clamp(1.2rem,2vw,1.6rem);font-weight:360;margin-bottom:.7rem}
.callout p{font-size:.95rem;color:var(--stone);max-width:64ch}
.dark .callout p{color:rgba(243,243,236,.8)}
.callout p+p{margin-top:.8rem}
.card-note{margin-top:.9rem;font-family:var(--sans);font-size:.66rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;color:var(--ink-soft)}
.dark .pk-price{display:block;font-family:var(--serif);font-size:clamp(1.8rem,3.2vw,2.6rem);font-weight:340;line-height:1;margin:.2rem 0 .9rem}
.callout{margin-top:clamp(2rem,5vh,3rem);max-width:68ch;border-top:1px solid var(--line);padding-top:1.4rem}
.dark .callout{border-top-color:var(--line-d)}
.callout h3{font-family:var(--serif);font-size:clamp(1.2rem,2vw,1.6rem);font-weight:360;margin-bottom:.7rem}
.callout p{font-size:.95rem;color:var(--stone);max-width:64ch}
.dark .callout p{color:rgba(243,243,236,.8)}
.callout p+p{margin-top:.8rem}
.card-note{color:var(--cream-soft)}
.statblock{margin-top:clamp(2rem,5vh,3rem);border-top:1px solid var(--line);padding-top:1.6rem;max-width:68ch}
.dark .statblock{border-top-color:var(--line-d)}
.statblock b{display:block;font-family:var(--serif);font-size:clamp(3rem,7vw,5rem);font-weight:340;line-height:1;margin:.8rem 0 .6rem}
.statblock .statlab{display:block;font-size:.9rem;color:var(--stone);max-width:52ch;margin-bottom:1.4rem}
.dark .statblock .statlab{color:rgba(243,243,236,.8)}
.statblock h3{margin-bottom:.8rem}
@media(max-width:900px){.svc-step{grid-template-columns:1fr;gap:.4rem}}
"""


def shell(slug, body):
    """same as gen_era_pages.shell but with the service CSS appended"""
    return P.shell(slug, body)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rich(s):
    """content JSON keeps <strong>/<em>; re-allow just those after escaping"""
    s = esc(s)
    for t in ("strong", "em", "b", "i"):
        s = s.replace(f"&lt;{t}&gt;", f"<{t}>").replace(f"&lt;/{t}&gt;", f"</{t}>")
    return s


def render_block(b, dark, idx):
    out = [f'<section class="pad{" dark" if dark else ""}" id="s{idx}"><div class="wrap">']
    out.append(f'<div class="head"><span class="ovl">{esc(b["label"])}</span>'
               f'<h2 class="reveal">{esc(b["heading"])}</h2></div>')
    for p in b["paras"]:
        out.append(f'<p class="svc-p reveal">{rich(p)}</p>')

    if b["includes"]:
        out.append('<div class="inc-grid reveal">')
        for lab, items in b["includes"]:
            lis = "".join(f"<li>{esc(i)}</li>" for i in items)
            out.append(f'<div class="inc"><h3>{esc(lab)}</h3><ul>{lis}</ul></div>')
        out.append('</div>')

    if b.get("packages"):
        out.append('<div class="card-grid reveal">')
        for pk in b["packages"]:
            tag = f'<span class="tag">{esc(pk["tag"])}</span>' if pk["tag"] else ""
            price = f'<span class="pk-price">{esc(pk["price"])}</span>' if pk["price"] else ""
            desc = f'<p>{rich(pk["desc"])}</p>' if pk["desc"] else ""
            note = f'<p class="card-note">{esc(pk["note"])}</p>' if pk["note"] else ""
            out.append(f'<div class="svc-card pk">{tag}<h3>{esc(pk["name"])}</h3>{price}{desc}{note}</div>')
        out.append('</div>')

    for co in b.get("callouts", []):
        ti = f'<h3>{esc(co["title"])}</h3>' if co["title"] else ""
        ps = "".join(f'<p>{rich(x)}</p>' for x in co["paras"])
        lis = ("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in co["items"]) + "</ul>") if co["items"] else ""
        out.append(f'<div class="callout inc reveal">{ti}{ps}{lis}</div>')

    if b["cards"]:
        out.append('<div class="card-grid reveal">')
        for c in b["cards"]:
            tag = f'<span class="tag">{esc(c["tag"])}</span>' if c["tag"] else ""
            desc = f'<p>{rich(c["desc"])}</p>' if c.get("desc") else ""
            items = ("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in c["items"]) + "</ul>") if c.get("items") else ""
            note = f'<p class="card-note">{esc(c["note"])}</p>' if c.get("note") else ""
            out.append(f'<div class="svc-card inc">{tag}<h3>{esc(c["title"])}</h3>{desc}{items}{note}</div>')
        out.append('</div>')

    if b["money"]:
        out.append('<div class="money-grid reveal">')
        for title, amt, items in b["money"]:
            lis = "".join(f"<li>{esc(i)}</li>" for i in items)
            out.append(f'<div class="money-col inc"><h3>{esc(title)}</h3>'
                       f'<span class="amt">{esc(amt)}</span><ul>{lis}</ul></div>')
        out.append('</div>')

    for st in b.get("stats", []):
        ps = "".join(f'<p class="svc-p">{rich(x)}</p>' for x in st["paras"])
        eb = f'<span class="ovl">{esc(st["eyebrow"])}</span>' if st["eyebrow"] else ""
        ti = f'<h3>{esc(st["title"])}</h3>' if st["title"] else ""
        out.append(f'<div class="statblock reveal">{eb}<b>{esc(st["stat"])}</b>'
                   f'<span class="statlab">{esc(st["label"])}</span>{ti}{ps}</div>')

    for t in b["tables"]:
        head = "".join(f"<th>{rich(c)}</th>" for c in t["head"])
        rows = "".join("<tr>" + "".join(f"<td>{rich(c)}</td>" for c in r) + "</tr>"
                       for r in t["rows"])
        money_last = t["head"] and t["head"][-1].strip().lower() in ("from", "fee", "price", "amount", "total")
        cls = "ptable ralign" if money_last else "ptable"
        out.append(f'<div class="tscroll reveal"><table class="{cls}">'
                   f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')

    if b["steps"]:
        out.append('<div class="svc-steps reveal">')
        for n, title, desc in b["steps"]:
            p = f"<p>{rich(desc)}</p>" if desc else ""
            out.append(f'<div class="svc-step"><b>{esc(n)}</b><div><h3>{esc(title)}</h3>{p}</div></div>')
        out.append('</div>')

    if b["faq"]:
        out.append('<div class="faq-list reveal">')
        for q, a in b["faq"]:
            out.append(f'<details><summary>{esc(q)}</summary><div class="a">{rich(a)}</div></details>')
        out.append('</div>')

    out.append('</div></section>')
    return "".join(out)


def build(slug):
    d = json.load(io.open(os.path.join(CONTENT, slug + ".json"), encoding="utf-8"))
    chips = ""
    if d["prices"]:
        chips = '<div class="chips">' + "".join(
            f'<div class="chip"><b>{esc(a)}</b><span>{esc(l)}</span></div>'
            for l, a in d["prices"]) + '</div>'

    body = [f'''<header class="subhero" id="top">
  <div class="media"><div class="media-img" data-par="0.06" style="background-image:url('{HERO[slug]}')"></div></div>
  <div class="subhero-in">
    <span class="ovl">{esc(d["eyebrow"])}</span>
    <h1>{P.rlines(esc(d["h1"]))}</h1>
    <p class="lead">{rich(d["lead"])}</p>
    {chips}
  </div>
</header>''']

    chap_img, chap_text = CHAPTER[slug]
    half = max(1, len(d["blocks"]) // 2)
    for i, b in enumerate(d["blocks"]):
        body.append(render_block(b, dark=(i % 2 == 1), idx=i))
        if i == half - 1:
            body.append(f'''<section class="chapter">
  <div class="media"><div class="media-img" data-par="0.1" style="background-image:url('{chap_img}')"></div></div>
  <h2>{P.rlines(chap_text)}</h2>
</section>''')

    cta = d.get("cta") or {}
    head = esc(cta.get("heading") or "Find out if Spain is right for you.")
    lead = rich(cta.get("lead") or "A free 45-minute call. Your eligibility, what your money buys here, "
                                  "and whether the move is right for you &mdash; honestly.")
    note = f'<p class="card-note reveal" style="margin-top:1.2rem">{esc(cta["note"])}</p>' if cta.get("note") else ""
    body.append(f'''<section class="pad"><div class="wrap">
  <div class="head"><span class="ovl">Next step</span><h2 class="reveal">{head}</h2></div>
  <p class="svc-p reveal">{lead}</p>
  <p class="reveal" style="margin-top:1.6rem"><a class="srow-link" href="/v2/#contact">Book your free call <span aria-hidden="true">&rarr;</span></a></p>
  {note}
</div></section>

<section class="pad dark"><div class="wrap">
  <div class="head"><span class="ovl">The guide</span><h2 class="reveal">Your complete guide to retiring in Spain</h2></div>
  <p class="svc-p reveal" style="color:rgba(243,243,236,.82)">The visa, the property, and the honest cost of the life &mdash; free, straight to your inbox.</p>
  {P.guide_form("v2:" + slug)}
</div></section>''')

    return shell(slug, "\n".join(body))


if __name__ == "__main__":
    for slug in ("immigration", "real-estate", "fullafterlife", "private-client"):
        html = build(slug)
        dd = os.path.join(ROOT, slug)
        os.makedirs(dd, exist_ok=True)
        p = os.path.join(dd, "index.html")
        io.open(p, "w", encoding="utf-8").write(html)
        print(f"wrote {p} ({len(html)//1024} KB)")
