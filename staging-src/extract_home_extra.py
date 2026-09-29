#!/usr/bin/env python3
"""Lift the homepage copy the v2 prototype dropped, VERBATIM, from production (origin/main:index.html)
into content/home_extra.json. Never retype copy - re-run this if production changes."""
import re, json, subprocess, os, io, html as H
HERE=os.path.dirname(os.path.abspath(__file__))
src=subprocess.run(["git","show","origin/main:index.html"],cwd=HERE,capture_output=True,text=True).stdout
def inner(s):  # keep inline markup (em, br, a) but drop presentational spans
    s=re.sub(r'<span class="cur"[^>]*>(.*?)</span>',r'\1',s,flags=re.S)
    return re.sub(r'\s+',' ',s).strip()
def txt(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s)).strip()
def sect(cls):
    i=src.find(f'<section class="{cls}'); return src[i:src.find('</section>',i)]
out={}
# hero stats
h=sect("hero")
out["hero_stats"]=[(inner(n),inner(l)) for n,l in re.findall(r'<div class="hstat-n">(.*?)</div>\s*<div class="hstat-l">(.*?)</div>',h,re.S)]
out["hero_lede"]=inner(re.search(r'<h1.*?</h1>\s*<p[^>]*>(.*?)</p>',h,re.S).group(1))
# the calculation
s=sect("statement")
out["calc"]={"ovl":txt(re.search(r'eyebrow">(.*?)<',s).group(1)),
  "h2":inner(re.search(r'<h2>(.*?)</h2>',s,re.S).group(1)),
  "paras":[inner(p) for p in re.findall(r'<p[^>]*>(.*?)</p>',s,re.S)],
  "stats":[(inner(n),inner(l)) for n,l in re.findall(r'<div class="sq-n">(.*?)</div>\s*<div class="sq-l">(.*?)</div>',s,re.S)]}
# numbers
s=sect("reality")
intros=re.findall(r'<p[^>]*class="[^"]*geo-(ca|us)[^"]*"[^>]*>(.*?)</p>',s,re.S)
if not intros: intros=list(zip(["ca","us"],re.findall(r'<p[^>]*>(.*?)</p>',s,re.S)[:2]))
out["num_intro"]={k:inner(v) for k,v in intros}
def items(card):
    res=[]
    for cls,body in re.findall(r'<div class="compare-item([^"]*)"[^>]*>(.*?)</div>\s*</div>',card,re.S):
        m=re.search(r'<div class="ci-text">\s*<strong>(.*?)</strong>(.*)',body,re.S)
        if not m: m=re.search(r'<div class="ci-text">\s*<b>(.*?)</b>(.*)',body,re.S)
        geo="ca" if "geo-ca" in cls else "us" if "geo-us" in cls else "both"
        res.append((geo,inner(m.group(1)) if m else "",inner(m.group(2)) if m else inner(body)))
    return res
sp=s[s.find('compare-card spain'):s.find('compare-card home')]; hm=s[s.find('compare-card home'):]
out["num_spain"]=items(sp); out["num_home"]=items(hm)
# places - full text per place
s=sect("places")
out["places_full"]={txt(n):[inner(p) for p in re.findall(r'<p>(.*?)</p>',full,re.S)]
  for n,full in re.findall(r'<div class="place-name">(.*?)</div>.*?<div class="place-full">(.*?)</div>',s,re.S)}
out["places_intro"]=inner(re.search(r'<h2>.*?</h2>\s*<p[^>]*>(.*?)</p>',s,re.S).group(1))
# is this you
s=sect("decision")
out["decision"]={"ovl":txt(re.search(r'eyebrow">(.*?)<',s).group(1)),"h2":inner(re.search(r'<h2>(.*?)</h2>',s,re.S).group(1)),
 "deck":inner(re.search(r'decision-deck">(.*?)</p>',s,re.S).group(1)),
 "traits":[inner(t) for t in re.findall(r'<div class="trait">.*?<p>(.*?)</p>',s,re.S)],
 "ctas":[(a,inner(t)) for a,t in re.findall(r'<a href="([^"]+)" class="btn[^"]*">(.*?)</a>',s,re.S)]}
# how
s=sect("how")
out["how"]={"h2":inner(re.search(r'<h2>(.*?)</h2>',s,re.S).group(1)),"lede":inner(re.search(r'</h2>\s*<p[^>]*>(.*?)</p>',s,re.S).group(1)),
 "steps":[(inner(n),inner(t),inner(p)) for n,t,p in re.findall(r'<div class="how-n">(.*?)</div>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',s,re.S)],
 "fees":[(txt(l),inner(a),inner(n)) for l,a,n in re.findall(r'svc-price-lbl">(.*?)</span>\s*<div class="svc-price-amt">(.*?)</div>\s*<p[^>]*>(.*?)</p>',s,re.S)],
 "fa_line":inner(re.search(r'fa-line[^>]*>\s*<p>(.*?)</p>',s,re.S).group(1)),
 "pc_line":inner(re.search(r'pc-line[^>]*>\s*<p>(.*?)</p>',s,re.S).group(1))}
fn=re.search(r'<strong[^>]*>Why we built this.</strong>(.*?)</p>',s,re.S)
out["how"]["founder"]=inner(fn.group(1))
# journal feature
s=sect("journal")
out["journal"]={"ovl":txt(re.search(r'eyebrow">(.*?)<',s).group(1)),"h2":inner(re.search(r'<h2>(.*?)</h2>',s,re.S).group(1)),
 "deck":inner(re.search(r'class="deck">(.*?)</p>',s,re.S).group(1)),
 "href":re.search(r'journal-feature[^"]*" href="([^"]+)"|href="([^"]+)"[^>]*journal-feature',s).group(0),
 "cat":txt(re.search(r'jf-cat">(.*?)<',s).group(1)),"date":txt(re.search(r'jf-date">(.*?)<',s).group(1)),
 "h3":inner(re.search(r'<h3>(.*?)</h3>',s,re.S).group(1)),"p":inner(re.search(r'</h3>\s*<p>(.*?)</p>',s,re.S).group(1))}
# contact
s=sect("contact")
out["contact"]={"paras":[inner(p) for p in re.findall(r'<p>(.*?)</p>',s[:s.find('contact-list')],re.S)],
 "list":[inner(p) for p in re.findall(r'<span class="cl-n">.*?</span>\s*<p>(.*?)</p>',s,re.S)],
 "box_h3":inner(re.search(r'form-box">\s*<h3>(.*?)</h3>',s,re.S).group(1)),
 "box_p":inner(re.search(r'form-box">\s*<h3>.*?</h3>\s*<p[^>]*>(.*?)</p>',s,re.S).group(1)),
 "note":inner(re.search(r'form-note">(.*?)</p>',s,re.S).group(1))}
# round 2: the remaining short copy the copy-gate flagged
s=sect("places")
out["places_short"]={txt(n):inner(p) for n,p in re.findall(r'<div class="place-name">(.*?)</div>\s*<p class="place-desc">(.*?)</p>',s,re.S)}
s=sect("life-essay"); out["life_deck"]=inner(re.search(r'class="deck">(.*?)</p>',s,re.S).group(1))
s=sect("reality"); out["num_h3"]=[inner(x) for x in re.findall(r'<h3>(.*?)</h3>',s,re.S)]
s=sect("how"); out["svc"]=[(txt(e),inner(h),inner(p)) for e,h,p in re.findall(r'<div class="svc-body">\s*<span class="eyebrow">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',s,re.S)]
s=sect("guide-cta"); out["guide"]={"ovl":txt(re.search(r'guide-eyebrow">(.*?)<',s).group(1)),"h2":inner(re.search(r'<h2>(.*?)</h2>',s,re.S).group(1)),"p":inner(re.search(r'</h2>\s*<p>(.*?)</p>',s,re.S).group(1)),"note":inner(re.search(r'guide-note">(.*?)</p>',s,re.S).group(1))}
io.open(os.path.join(HERE,"content","home_extra.json"),"w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=1))
print(json.dumps(out,ensure_ascii=False,indent=1)[:9000])
