#!/usr/bin/env python3
"""Extract the four service pages' content from the PRODUCTION sources into JSON.

Reads immigration / real-estate / fullafterlife / private-client from `origin/main`
(they are not in the redesign-era tree) and writes staging-src/content/<slug>.json.

Copy is never retyped — it is lifted from the source — so prices and figures cannot
drift. Run this only if production copy changes; gen_era_services.py renders the JSON.
"""
import re, io, os, json, subprocess, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "content")
PAGES = ["immigration", "real-estate", "fullafterlife", "private-client"]


def txt(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', H.unescape(s)).strip()


def rich(s):
    """keep <strong>/<em>, drop everything else"""
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'</?(?!strong|em|b|i)[a-zA-Z][^>]*>', '', s)
    return re.sub(r'\s+', ' ', H.unescape(s)).strip()


def src(slug):
    return subprocess.run(["git", "-C", os.path.dirname(HERE), "show",
                           f"origin/main:{slug}.html"],
                          capture_output=True, text=True, check=True).stdout


def extract(slug):
    h = src(slug)
    h = re.sub(r'<(script|style|nav|footer)[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    d = {"slug": slug}

    m = re.search(r'<title>(.*?)</title>', h, re.S)
    d["title"] = txt(m.group(1)) if m else slug
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    d["meta"] = H.unescape(m.group(1)) if m else ""

    # hero
    m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    d["h1"] = txt(m.group(1)) if m else ""
    m = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<p[^>]*>(.*?)</p>)', h, re.S)
    d["lead"] = rich(m.group(1)) if m else ""
    m = re.search(r'class="eyebrow"[^>]*>(.*?)</div>', h, re.S)
    d["eyebrow"] = txt(m.group(1)) if m else ""

    # hero / header price chips
    d["prices"] = []
    for lab, amt in re.findall(r'(?:header|hero)-price-label"[^>]*>(.*?)</[^>]+>\s*'
                               r'<[^>]*(?:header|hero)-price-amount"[^>]*>(.*?)</', h, re.S):
        d["prices"].append([txt(lab), txt(amt)])

    # closing CTA (its own heading per page; it has no section-label so it is not a block)
    heads = re.findall(r'<h2[^>]*>(.*?)</h2>', h, re.S)
    d["cta"] = {"heading": txt(heads[-1]) if heads else "", "note": "", "lead": ""}
    tail = h[h.rfind("<h2"):] if heads else ""
    ps = [rich(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', tail, re.S)]
    if ps:
        d["cta"]["lead"] = ps[0]
    m2 = re.search(r'>([^<]*No charge[^<]*)<', tail)
    if m2:
        d["cta"]["note"] = txt(m2.group(1))

    # Blocks: every content block on these pages starts with a `section-label`
    # overline. <section> is not reliable (private-client uses divs), so chunk on
    # the label boundary and scope every component to its own chunk — that keeps
    # the rendered order identical to production.
    parts = re.split(r'(?=class="section-label(?:-dark|-light)?")', h)
    d["blocks"] = []
    for seg in parts[1:]:
        lab = re.search(r'class="section-label(?:-dark|-light)?"[^>]*>(.*?)</', seg, re.S)
        head = re.search(r'<h2[^>]*>(.*?)</h2>', seg, re.S)
        if not head:
            continue
        b = {"label": txt(lab.group(1)) if lab else "", "heading": txt(head.group(1))}
        after = seg[:head.start()] + seg[head.end():]

        b["steps"] = []
        for m in re.finditer(r'class="(?:process-step|seq-step)"[^>]*>(.*?)'
                             r'(?=class="(?:process-step|seq-step)"|</section>|\Z)', after, re.S):
            t = re.search(r'<h[34][^>]*>(.*?)</h[34]>', m.group(1), re.S)
            para = re.search(r'<p[^>]*>(.*?)</p>', m.group(1), re.S)
            if t:
                b["steps"].append([f"{len(b['steps'])+1:02d}", txt(t.group(1)),
                                   rich(para.group(1)) if para else ""])

        b["includes"] = []
        for m in re.finditer(r'class="includes-group"[^>]*>(.*?)(?=class="includes-group"|</section>|\Z)', after, re.S):
            lb = re.search(r'class="includes-group-label"[^>]*>(.*?)</div>', m.group(1), re.S)
            items = [txt(li) for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S)]
            if lb and items:
                b["includes"].append([txt(lb.group(1)), items])

        b["cards"] = []
        for cls, nk, dk in (("property-card", "property-name", "property-desc"),
                            ("geo-item", "geo-label", "geo-desc"),
                            ("feature-block", "feature-label", None),
                            ("whom-item", None, None),
                            ("combine-card", "combine-tag", None)):
            for m in re.finditer(rf'class="{cls}[^"]*"[^>]*>(.*?)(?=class="{cls}[^"]*"|</section>|\Z)', after, re.S):
                sg = m.group(1)
                name = re.search(rf'class="{nk}[^"]*"[^>]*>(.*?)</div>', sg, re.S) if nk else None
                t = re.search(r'<h[34][^>]*>(.*?)</h[34]>', sg, re.S)
                if cls == "geo-item" and not t:
                    t = re.search(r'class="geo-name"[^>]*>(.*?)</div>', sg, re.S)
                para = re.search(rf'class="{dk}[^"]*"[^>]*>(.*?)</p>', sg, re.S) if dk else re.search(r'<p[^>]*>(.*?)</p>', sg, re.S)
                title = txt(t.group(1)) if t else (txt(name.group(1)) if name else "")
                if not title:
                    continue
                # keep EVERY paragraph (a second <p> held "€500 per session") and the
                # feature-included line (which held "€2,500 per person value")
                if dk:
                    paras = [rich(para.group(1))] if para else []
                else:
                    paras = [rich(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', sg, re.S)]
                inc = re.search(r'class="feature-included"[^>]*>(.*?)</div>', sg, re.S)
                items = [txt(x) for x in re.findall(r'<li[^>]*>(.*?)</li>', sg, re.S)]
                b["cards"].append({"tag": txt(name.group(1)) if (name and t) else "",
                                   "title": title, "desc": " ".join(paras),
                                   "items": items,
                                   "note": txt(inc.group(1)) if inc else ""})

        # highlighted stat blocks (the Beckham 24% / 47% callout)
        b["stats"] = []
        for m in re.finditer(r'class="beckham-block"[^>]*>(.*?)\Z', after, re.S):
            sg = m.group(1)
            eb = re.search(r'class="eyebrow"[^>]*>(.*?)</div>', sg, re.S)
            st = re.search(r'class="beckham-stat"[^>]*>(.*?)</div>', sg, re.S)
            lb = re.search(r'class="beckham-stat-label"[^>]*>(.*?)</div>', sg, re.S)
            t3 = re.search(r'<h3[^>]*>(.*?)</h3>', sg, re.S)
            ps = [rich(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', sg, re.S)]
            if st:
                extra = [txt(x.group(1)) for x in
                         (re.search(r'class="beckham-price"[^>]*>(.*?)</div>', sg, re.S),
                          re.search(r'class="beckham-warning"[^>]*>(.*?)</div>', sg, re.S)) if x]
                ps = ps + extra
                b["stats"].append({"eyebrow": txt(eb.group(1)) if eb else "",
                                   "stat": txt(st.group(1)),
                                   "label": txt(lb.group(1)) if lb else "",
                                   "title": txt(t3.group(1)) if t3 else "",
                                   "paras": ps})

        # priced package cards (immigration)
        b["packages"] = []
        for m in re.finditer(r'class="package-card[^"]*"[^>]*>(.*?)(?=class="package-card|</div>\s*</div>\s*</section>|\Z)', after, re.S):
            sg = m.group(1)
            get = lambda k: (re.search(rf'class="{k}"[^>]*>(.*?)</', sg, re.S) or [None, ""])
            nm = re.search(r'class="package-name"[^>]*>(.*?)</div>', sg, re.S)
            if not nm:
                continue
            tg = re.search(r'class="package-tag"[^>]*>(.*?)</div>', sg, re.S)
            pr = re.search(r'class="package-price"[^>]*>(.*?)</div>', sg, re.S)
            ds = re.search(r'class="package-desc"[^>]*>(.*?)</p>', sg, re.S)
            nt = re.search(r'class="package-note"[^>]*>(.*?)</p>', sg, re.S)
            b["packages"].append({"tag": txt(tg.group(1)) if tg else "",
                                  "name": txt(nm.group(1)),
                                  "price": txt(pr.group(1)) if pr else "",
                                  "desc": rich(ds.group(1)) if ds else "",
                                  "note": txt(nt.group(1)) if nt else ""})

        # standalone callout blocks (commission / availability)
        b["callouts"] = []
        for cls in ("commission-block", "availability-block", "trust-note"):
            for m in re.finditer(rf'class="{cls}[^"]*"[^>]*>(.*?)(?=</section>|\Z)', after, re.S):
                sg = m.group(1)
                t = re.search(r'<h[345][^>]*>(.*?)</h[345]>', sg, re.S)
                ps = [rich(x) for x in re.findall(r'<p[^>]*>(.*?)</p>', sg, re.S)]
                lis = [txt(x) for x in re.findall(r'<li[^>]*>(.*?)</li>', sg, re.S)]
                if not ps and not lis:
                    raw = rich(sg.split("</div>")[0])
                    if len(raw) > 40:
                        ps = [raw]
                if ps or lis:
                    b["callouts"].append({"title": txt(t.group(1)) if t else "",
                                          "paras": ps, "items": lis})

        b["tables"] = []
        for m in re.finditer(r'<table[^>]*>(.*?)</table>', after, re.S):
            rows = [[rich(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)]
                    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.S)]
            rows = [r for r in rows if r]
            if rows:
                b["tables"].append({"head": rows[0], "rows": rows[1:]})

        b["money"] = []
        for m in re.finditer(r'class="money-col"[^>]*>(.*?)(?=class="money-col"|</section>|\Z)', after, re.S):
            t = re.search(r'<h3[^>]*>(.*?)</h3>', m.group(1), re.S)
            a = re.search(r'class="amt"[^>]*>(.*?)</', m.group(1), re.S)
            items = [txt(li) for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S)]
            if t:
                b["money"].append([txt(t.group(1)), txt(a.group(1)) if a else "", items])

        b["faq"] = []
        for m in re.finditer(r'class="faq-question"[^>]*>(.*?)</button>\s*'
                             r'<[^>]*class="faq-answer"[^>]*>(.*?)</div>', after, re.S):
            q = txt(re.sub(r'<span class="faq-icon".*?</span>', '', m.group(1), flags=re.S))
            ans = rich(m.group(2))
            if q and ans:
                b["faq"].append([q, ans])

        # prose = every paragraph in the block that a component did not already claim,
        # so trailing copy after a grid/table is never dropped
        used = set()
        for k in ("steps", "money"):
            for row in b[k]:
                used.add(row[2] if k == "steps" else " ".join(row[2]))
        for c in b["cards"]:
            used.add(c["desc"])
        for pk in b["packages"]:
            used.update([pk["desc"], pk["note"]])
        for co in b["callouts"]:
            used.update(co["paras"])
        for st in b["stats"]:
            used.update(st["paras"])
        b["paras"] = [x for x in (rich(y) for y in re.findall(r'<p[^>]*>(.*?)</p>', after, re.S))
                      if len(x) > 40 and x not in used]

        d["blocks"].append(b)

    return d


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug in PAGES:
        d = extract(slug)
        io.open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8").write(
            json.dumps(d, ensure_ascii=False, indent=1))
        kinds = lambda k: sum(len(b[k]) for b in d["blocks"])
        print(f"{slug:16} blocks={len(d['blocks'])} steps={kinds('steps')} "
              f"includes={kinds('includes')} cards={kinds('cards')} tables={kinds('tables')} "
              f"money={kinds('money')} faq={kinds('faq')} prices={len(d['prices'])}")
