#!/usr/bin/env python3
"""staging/v2/properties/ and staging/v2/journal/ — the two cross-page links from the
v2 nav, rebuilt in the ERA v2 design language.

Content is ported verbatim from the production pages (available-properties.html and
building-my-life-in-spain.html on origin/main). FIGURES ARE VERBATIM — prices, m2,
plot sizes, yields and dates must not be altered.

Reuses the CSS/JS from gen_era_v2.py so the three pages stay visually identical;
run that generator's module import, not a copy of its stylesheet.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_era_v2 as V2

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "staging", "v2")

# ---------------------------------------------------------------- shared chrome
NAV = """<nav class="nav"><a class="brand" href="/v2/"><b>Spanish</b> AfterLife</a>
<div class="nav-links"><a href="/v2/#life">The Life</a><a href="/v2/#numbers">The Numbers</a><a href="/v2/#places">Where</a><a href="/v2/#how">How It Works</a><a href="/v2/properties/">Properties</a><a href="/v2/journal/">Journal</a><a class="nav-cta" href="/v2/#contact">Start Here</a></div>
<button class="burger" aria-label="Menu"><span></span><span></span><span></span></button></nav>
<div class="menu" id="menu"><a href="/v2/#life">The Life</a><a href="/v2/#numbers">The Numbers</a><a href="/v2/#places">Where</a><a href="/v2/#how">How It Works</a><a href="/v2/properties/">Properties</a><a href="/v2/journal/">Journal</a><a href="/v2/#contact">Start Here</a><div class="menu-sig">Why wait for the AfterLife?</div>
</div>"""

FOOT = """<footer class="foot"><div class="foot-top"><div class="foot-sig">Why wait for the AfterLife?</div>
<div class="foot-nav"><a href="/v2/#life">The Life</a><a href="/v2/#numbers">The Numbers</a><a href="/v2/#places">Where</a><a href="/v2/#how">How It Works</a><a href="/v2/properties/">Properties</a><a href="/v2/journal/">Journal</a><a href="/v2/#contact">Start Here</a></div></div>
<div class="foot-bot"><span>&copy; 2025 LJ Koch Group Inc. &middot; Spanish AfterLife</span><span>Valencia Community, Spain</span></div></footer>"""

# page-specific CSS layered on top of the shared v2 stylesheet
EXTRA = """
/* --- cross-page: shared --- */
.subhero{position:relative;min-height:74vh;display:flex;align-items:flex-end;padding:0 var(--pad) clamp(3rem,8vh,6rem);overflow:hidden;background:var(--ink);color:var(--cream)}
.subhero .media{position:absolute;inset:0;z-index:0}
.subhero::after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(23,35,59,.5) 0%,rgba(23,35,59,.2) 35%,rgba(23,35,59,.88) 100%)}
.subhero-in{position:relative;z-index:2;width:100%;max-width:1440px;margin:0 auto}
.subhero h1{font-size:clamp(2.6rem,6.4vw,5.2rem);max-width:15ch;line-height:1.02;font-weight:360}
.subhero .ovl{color:var(--cream-soft);display:block;margin-bottom:1.4rem}
.subhero .lead{max-width:58ch;margin-top:1.6rem;color:rgba(243,243,236,.82)}
.pnote{font-size:.78rem;letter-spacing:.02em;color:var(--ink-soft);max-width:70ch}
.dark .pnote{color:var(--cream-soft)}

/* --- properties --- */
.feat{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4.5rem);align-items:center}
.feat-media{position:relative;overflow:hidden;aspect-ratio:4/3}
.pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(1.2rem,2.5vw,2.4rem);margin-top:clamp(2.5rem,6vh,4rem)}
.pillar{border-top:1px solid var(--line-d);padding-top:1.1rem}
.pillar h4{font-family:var(--sans);font-size:.68rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--cream-soft);margin-bottom:.7rem}
.pillar p{font-size:.95rem;color:rgba(243,243,236,.8)}
.gal{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:clamp(2.5rem,6vh,4rem)}
.gal figure{position:relative;overflow:hidden;margin:0;aspect-ratio:4/3}
.gal figure:nth-child(1),.gal figure:nth-child(2){grid-column:span 3;aspect-ratio:16/10}
.gal figure:nth-child(n+3){grid-column:span 2}
.gal img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 1.2s var(--ease)}
.gal figure:hover img{transform:scale(1.04)}
.gal figcaption{position:absolute;left:0;bottom:0;right:0;padding:1.4rem 1.1rem .8rem;font-size:.62rem;text-transform:uppercase;letter-spacing:.18em;font-weight:600;color:#fff;background:linear-gradient(180deg,transparent,rgba(0,0,0,.6))}
.awards{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:clamp(2rem,5vh,3rem)}
.award{border:1px solid var(--line-d);border-radius:100px;padding:.6rem 1.1rem;font-size:.7rem;letter-spacing:.06em;color:var(--cream)}
.coll{border-top:1px solid var(--line);padding:clamp(2.5rem,6vh,4.5rem) 0}
.coll-head{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4rem);align-items:end;margin-bottom:clamp(1.6rem,4vh,2.6rem)}
.coll-media{position:relative;overflow:hidden;aspect-ratio:16/9}
.coll-media img{width:100%;height:100%;object-fit:cover;display:block}
.coll h3{margin-bottom:.5rem}
.coll-meta{font-family:var(--sans);font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;color:var(--stone)}
.coll-desc{margin-top:1rem;color:var(--stone)}
.ptable{width:100%;border-collapse:collapse;margin-top:.4rem}
.ptable th{font-family:var(--sans);font-size:.62rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--ink-soft);text-align:left;padding:.7rem 1rem .7rem 0;border-bottom:1px solid var(--line)}
.ptable td{font-family:var(--serif);font-size:1rem;padding:.9rem 1rem .9rem 0;border-bottom:1px solid var(--line);vertical-align:baseline}
.ptable td:first-child{font-weight:500}
.ptable td:last-child,.ptable th:last-child{text-align:right;padding-right:0;white-space:nowrap}
.ptable tr:last-child td{border-bottom:0}
.tscroll{overflow-x:auto}
.wow{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4.5rem);align-items:center}
.wow-media{position:relative;overflow:hidden;aspect-ratio:4/3}
.stats{display:flex;gap:clamp(1.5rem,4vw,3.5rem);margin-top:2rem;flex-wrap:wrap}
.stat b{display:block;font-family:var(--serif);font-size:clamp(2.2rem,4.5vw,3.4rem);font-weight:340;line-height:1}
.stat span{font-size:.66rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--cream-soft)}

/* --- journal --- */
.cats{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(1.5rem,3vw,3rem)}
.cat{border-top:1px solid var(--line);padding-top:1.2rem}
.cat-n{font-family:var(--serif);font-size:.95rem;color:var(--stone);display:block;margin-bottom:.8rem}
.cat h3{font-size:clamp(1.15rem,1.8vw,1.5rem);margin-bottom:.6rem}
.cat p{font-size:.95rem;color:var(--stone)}
/* the categories grid sits on a .dark section: stone-on-navy is unreadable */
.dark .cat{border-top-color:var(--line-d)}
.dark .cat-n{color:var(--cream-soft)}
.dark .cat p{color:rgba(243,243,236,.8)}
.arts{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(1.2rem,2.5vw,2rem);margin-top:clamp(2rem,5vh,3rem)}
.art{display:block;border:1px solid var(--line);padding:clamp(1.4rem,2.5vw,2rem);transition:background .5s var(--ease),border-color .5s var(--ease)}
a.art:hover{background:rgba(23,35,59,.035);border-color:rgba(23,35,59,.3)}
.art-meta{display:flex;justify-content:space-between;gap:1rem;font-size:.62rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--ink-soft);margin-bottom:1.1rem}
.art h3{font-size:clamp(1.2rem,2vw,1.7rem);margin-bottom:.7rem}
.art p{font-size:.95rem;color:var(--stone)}
.art-more{display:inline-block;margin-top:1rem;font-family:var(--sans);font-size:.68rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;border-bottom:1px solid var(--line);padding-bottom:.25rem}
.sig{font-family:var(--sans);font-size:.68rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--ink-soft);margin-top:2rem}
.founder p{margin-bottom:1.1rem}

@media(max-width:900px){
 .feat,.wow,.coll-head,.cats,.arts,.pillars{grid-template-columns:1fr}
 .gal{grid-template-columns:1fr 1fr}
 .gal figure:nth-child(1),.gal figure:nth-child(2),.gal figure:nth-child(n+3){grid-column:span 1;aspect-ratio:4/3}
 .subhero{min-height:64vh}
}
"""

# JS: only the burger + reveal observer are relevant here (no sticky switcher / numbers toggle)
JS = r"""
const burger=document.querySelector('.burger'),menu=document.getElementById('menu');
burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');document.body.style.overflow=o?'hidden':'';});
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');document.body.style.overflow='';}));
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.reveal,.rline,.img-reveal').forEach(el=>io.observe(el));
"""


def shell(title, desc, body, favicon_note=""):
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><script>document.documentElement.className='js';</script>
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..460;1,9..144,300..400&family=Archivo:wght@400;500;600&family=Ephesis&display=swap" rel="stylesheet">
<style>{V2.CSS}{EXTRA}</style></head><body>
<div id="badge">Staging v2 &middot; ERA flow</div>
{NAV}
{body}
{FOOT}
<script>{JS}</script>
</body></html>"""


def rlines(text):
    return "".join(f'<span class="rline"><span>{p}</span></span>' for p in text.split("|"))


# ============================================================ PROPERTIES
COLLECTIONS = [
 ("Oasis Altaona", "From &euro;443,500 &middot; 2&ndash;4 bed &middot; delivery Q2&ndash;Q3 2026",
  "/media/altaona/altaona-oasis.webp",
  "Light-filled contemporary villas in the heart of the resort &mdash; bright two- to four-bedroom homes, each with a private pool, terrace and premium finishes. The accessible entry into resort life.",
  [("Arin","2 / 2","143.6","470&ndash;498","&euro;443,500"),
   ("Arin L","2&ndash;4 / 2&ndash;3","167.6&ndash;174","583&ndash;596","&euro;614,000"),
   ("Nara","3 / 3","204","525","&euro;646,000"),
   ("Nara XL","3 / 3","213.3","551","&euro;689,000"),
   ("Arava","4 / 3","231.1","561","&euro;744,000")]),
 ("Las Vistas Altaona", "From &euro;513,500 &middot; 3 bed &middot; final Phase II release",
  "/media/altaona/altaona-las-vistas.webp",
  "Elevated plots on the final Phase II release, looking out over the resort and the open country beyond.",
  [("Serenity","3 / 2","211.5","359&ndash;432","&euro;513,500"),
   ("Balance","3 / 2","222.1","434&ndash;454","&euro;544,000")]),
 ("Villas Santolina", "&euro;1,052,000&ndash;&euro;1,692,000 &middot; 3&ndash;6 bed &middot; bespoke",
  "/media/altaona/altaona-santolina.webp",
  "Larger plots and bespoke architecture for buyers who want the house designed around them rather than chosen from a catalogue.",
  [("Campo","4 / 4","246","1,000","from &euro;1,052,000"),
   ("Horizon","3 / 3","294","1,000","on request"),
   ("Aqua","4 / 4","305","1,000&ndash;1,115","on request"),
   ("Bespoke","3&ndash;6 / 4&ndash;5","up to 500","1,000+","to &euro;1,692,000")]),
 ("Villas Fairway", "From &euro;816,000 &middot; 3&ndash;5 bed &middot; frontline golf",
  "/media/altaona/altaona-fairway.webp",
  "The resort's signature collection: larger, architect-led villas on the most exclusive frontline-golf plots, up to 770 m&sup2;.",
  [("Breeze","3 / 3","200","793","&euro;816,000"),
   ("Swing","4 / 4","300","1,000","&euro;1,007,000"),
   ("Drive","4 / 4","435","1,000","&euro;1,103,000"),
   ("Eagle","4 / 4","575","1,900","&euro;1,690,500"),
   ("Woods","4 / 4","645","2,100","&euro;1,991,000"),
   ("Birdie","5 / 5","770","2,500","&euro;3,625,000")]),
 ("Villas Retama", "Under construction &middot; 3&ndash;4 bed", None,
  "The newest Altaona collection, currently under construction &mdash; three- and four-bedroom villas with private pools on plots of 400&ndash;671 m&sup2;. Prices on release; ask us to be told first.",
  [("Retama","3&ndash;4 / 3","151&ndash;223","400&ndash;671","on release")]),
]

PILLARS = [
 ("Residential homes", "Four villa collections, from two-bed Oasis homes to frontline-golf Fairway villas."),
 ("Longevity &amp; wellness", "World-class wellness centre and medical spa, built around preventative health."),
 ("Sport &amp; golf", "18-hole golf course, tennis and paddle academy, trails through open country."),
 ("The location", "~20 min to Murcia city, ~30 min to Corvera airport, Mar Menor beaches nearby."),
]

GALLERY = [
 ("/media/altaona/altaona-resort.webp", "18-hole Golf Resort"),
 ("/media/altaona/altaona-las-vistas.webp", "New-Build Villas with Pool"),
 ("/media/altaona/altaona-aerial.webp", "Aerial View"),
 ("/media/altaona/altaona-interior.webp", "Contemporary Interiors"),
 ("/media/altaona/altaona-golf-sunset.webp", "Golf at Sunset"),
]

AWARDS = ["Best Leisure Development in Spain",
          "Best Marketing Development Strategy in Spain",
          "Best Real Estate Website in Spain"]


def collection(name, meta, img, desc, rows):
    media = (f'<div class="coll-media img-reveal"><img src="{img}" alt="{name}, Altaona Golf &amp; Wellness Resort, Murcia" loading="lazy"></div>'
             if img else '')
    head = (f'<div class="coll-head"><div class="reveal"><h3>{name}</h3><span class="coll-meta">{meta}</span>'
            f'<p class="coll-desc">{desc}</p></div>{media}</div>') if img else \
           (f'<div class="reveal" style="max-width:62ch"><h3>{name}</h3><span class="coll-meta">{meta}</span>'
            f'<p class="coll-desc">{desc}</p></div>')
    body = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a,b,c,d,e in rows)
    return (f'<div class="coll">{head}<div class="tscroll reveal"><table class="ptable">'
            f'<thead><tr><th>Villa</th><th>Beds / Baths</th><th>Built m&sup2;</th><th>Plot m&sup2;</th><th>From</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div></div>')


def build_properties():
    gal = "".join(f'<figure class="img-reveal"><img src="{s}" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>'
                  for s, c in GALLERY)
    pil = "".join(f'<div class="pillar"><h4>{t}</h4><p>{d}</p></div>' for t, d in PILLARS)
    awd = "".join(f'<span class="award">&#127942; {a}</span>' for a in AWARDS)
    colls = "".join(collection(*c) for c in COLLECTIONS)

    body = f"""
<header class="subhero" id="top">
  <div class="media"><div class="media-img" data-par="0.06" style="background-image:url('/media/altaona/altaona-aerial.webp')"></div></div>
  <div class="subhero-in">
    <span class="ovl">Available Properties</span>
    <h1>{rlines('Homes we can|get you into.')}</h1>
    <p class="lead">A curated look at the developments and homes we work with directly &mdash; from Spain's Valencia coast down into the Region of Murcia. We represent you through the whole purchase, and can make a direct introduction to the developers below.</p>
  </div>
</header>

<section class="pad dark" id="altaona"><div class="wrap">
  <div class="feat">
    <div class="reveal"><span class="ovl">Featured Development Partner</span>
      <h2 style="margin:1.2rem 0 1.2rem">Altaona Resort, Murcia</h2>
      <p style="color:rgba(243,243,236,.82)">Spain's first longevity-focused resort development. New-build villas, an 18-hole golf course, world-class wellness facilities, and the upcoming WOW Longevity Hotel &mdash; built around one idea: living better, for longer. A development we work with directly and can introduce you to.</p>
    </div>
    <div class="feat-media img-reveal"><div class="media-img" data-par="0.05" style="background-image:url('/media/altaona/altaona-resort.webp')"></div></div>
  </div>

  <div class="reveal" style="margin-top:clamp(3rem,8vh,5.5rem);max-width:62ch">
    <span class="ovl">Radiant lifestyle in Murcia, southern Spain</span>
    <h3 style="margin:1.1rem 0 1.1rem">The closest resort to Murcia centre &mdash; designed for wellbeing and longer living.</h3>
    <p style="color:rgba(243,243,236,.8)">Altaona is built around three pillars that put health and lifestyle at the centre of everyday life: exclusive residential homes, the WOW Longevity Hotel, and a resort core of an 18-hole golf course, sports facilities and a world-class wellness centre &mdash; so movement, nature and recovery are part of daily life. Whether you want a home, an investment, or simply to live better for longer, Altaona is built for people who value quality of life.</p>
  </div>
  <div class="pillars reveal">{pil}</div>
  <div class="gal">{gal}</div>
  <div class="reveal" style="margin-top:clamp(2.5rem,6vh,4rem)"><span class="ovl">European Property Awards 2025</span><div class="awards">{awd}</div></div>
</div></section>

<section class="pad" id="pricelist"><div class="wrap">
  <div class="head"><span class="ovl">The Altaona Price List</span><h2 class="reveal">Four villa collections, one resort</h2></div>
  <p class="pnote reveal">Every home is a new-build within the gated Altaona golf &amp; wellness resort, with a private pool, garden, aerothermal heating and air-conditioning, underfloor heating and an Italian kitchen (Energy Rating A). Figures are &ldquo;from&rdquo; starting prices &mdash; <strong>updated live and subject to availability</strong>. Ask us for the current plot list, floor plans and a branded brochure on any model below.</p>
  {colls}
</div></section>

<section class="pad dark" id="wow"><div class="wrap">
  <div class="wow">
    <div class="wow-media img-reveal"><div class="media-img" data-par="0.05" style="background-image:url('/media/altaona/altaona-wow-hotel.webp')"></div></div>
    <div class="reveal"><span class="ovl">Coming Soon &mdash; Investment Opportunity</span>
      <h2 style="margin:1.2rem 0 1.2rem">WOW Longevity Hotel</h2>
      <p style="color:rgba(243,243,236,.82)">Europe's first real estate project built around the science of longevity. Hotel suites from 54m&sup2; to 235m&sup2; with a fixed 7% net annual return under a long-term lease, plus 2% during construction. Investment backed by Altaona's award-winning resort infrastructure.</p>
      <div class="stats">
        <div class="stat"><b>7%</b><span>Fixed net annual rent</span></div>
        <div class="stat"><b>&euro;270K</b><span>Studio Suite entry &mdash; from</span></div>
      </div>
      <p style="margin-top:2rem"><a class="srow-link" href="/v2/#contact">Enquire via Spanish AfterLife <span aria-hidden="true">&rarr;</span></a></p>
    </div>
  </div>
  <p class="pnote reveal" style="margin-top:clamp(3rem,7vh,5rem)"><strong>Developer partner.</strong> Spanish AfterLife works directly with Taolis &mdash; The Art of Living in Spain on the Altaona development. We handle immigration concierge for clients purchasing here and can make a direct introduction to the Taolis team. If Altaona interests you, mention it when you book your strategy call.</p>
</div></section>

<section class="chapter">
  <div class="media"><div class="media-img" data-par="0.1" style="background-image:url('/media/altaona/altaona-golf-sunset.webp')"></div></div>
  <h2>{rlines('Ask us for the|full price list.')}</h2>
</section>

<section class="pad"><div class="wrap" style="text-align:left">
  <div class="head"><span class="ovl">Next step</span><h2 class="reveal">Request the full price list</h2></div>
  <p class="reveal" style="color:var(--stone)">A free 45-minute call. Your eligibility, what your money buys here, and whether the move is right for you &mdash; honestly.</p>
  <p class="reveal" style="margin-top:1.6rem"><a class="srow-link" href="/v2/#contact">Book your free call <span aria-hidden="true">&rarr;</span></a></p>
</div></section>
"""
    return shell("Available Properties &mdash; STAGING v2 (ERA flow)",
                 "A curated look at the developments and homes Spanish AfterLife works with directly, from the Valencia coast into the Region of Murcia.",
                 body)


# ============================================================ JOURNAL
CATS = [
 ("01","Relocation Guides","The process, step by step, in the order it actually happens &mdash; from the first document request to the residency card in your hand."),
 ("02","Early Retirement","The arithmetic of going sooner. What your equity buys here, what it costs to stay, and why the timing question usually answers itself."),
 ("03","Visa &amp; Money","The Non-Lucrative Visa, Beckham Law, tax residency, and the unromantic business of moving money across a border without losing your mind."),
 ("04","Neighbourhood Profiles","Valencia city, J&aacute;vea, D&eacute;nia, Oliva, Cullera, Ontinyent &mdash; what each is really like to live in, off-season, when the visitors have gone home."),
 ("05","The Life","Food, padel, golf, bodegas, the long lunch, the rhythm of a Spanish week &mdash; the part you came for, once the paperwork is behind you."),
 ("06","Personal Stories","The things that went sideways, the things that went right, and the small daily proof that the decision was the correct one."),
]

ARTICLES = [
 ("Visa &amp; Money","Jul 2026","Non-Lucrative vs Digital Nomad Visa: which Spain route?",
  "The two routes onto Spanish residency, how they differ, and who each one really suits &mdash; the shape of the choice before the numbers.",
  "https://spanishafterlife.com/building-my-life-in-spain/non-lucrative-vs-digital-nomad-visa-spain"),
 ("Early Retirement","In production","The maths that made waiting feel reckless",
  "What a Toronto or Bay Area sale converts into on the Valencia coast &mdash; and what every extra year at home quietly costs you.", None),
 ("Neighbourhood Profiles","In production","J&aacute;vea vs. D&eacute;nia: choosing your stretch of coast",
  "Two towns, twenty minutes apart, completely different lives. Who each one suits, and what you give up either way.", None),
 ("Visa &amp; Money","In production","Beckham Law and the six-month window",
  "The flat-rate tax regime worth real money &mdash; and the deadline that closes it for good if you blink.", None),
 ("Relocation Guides","In production","Opening a Spanish bank account: the honest version",
  "What to bring, which bank, how many visits it really takes, and the order that keeps the whole thing from stalling.", None),
 ("Personal Stories","In production","Two years on the coast, by way of Mexico",
  "Tourist-visa limbo, a seasonal apartment in Oliva Nova, and what living here off-season teaches you that a holiday never will.", None),
]


def build_journal():
    cats = "".join(f'<div class="cat"><span class="cat-n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in CATS)
    arts = ""
    for cat, badge, title, desc, href in ARTICLES:
        more = '<span class="art-more">Read <span aria-hidden="true">&rarr;</span></span>' if href else ''
        tag = f'<a class="art" href="{href}">' if href else '<div class="art">'
        end = '</a>' if href else '</div>'
        arts += (f'{tag}<div class="art-meta"><span>{cat}</span><span>{badge}</span></div>'
                 f'<h3>{title}</h3><p>{desc}</p>{more}{end}')

    body = f"""
<header class="subhero" id="top">
  <div class="media"><div class="media-img" data-par="0.06" style="background-image:url('/media/oliva-5.jpg')"></div></div>
  <div class="subhero-in">
    <span class="ovl">Building My Life in Spain</span>
    <h1>{rlines('Notes from the other side|of the decision.')}</h1>
    <p class="lead">The guides, the money, the neighbourhoods, and the small true stories of building a life in the Valencia Community &mdash; written from here, not from abroad. For the people who have decided not to wait.</p>
  </div>
</header>

<section class="pad" id="founder"><div class="wrap">
  <div class="head"><span class="ovl">From the founder</span><h2 class="reveal">Why this exists, and what you'll find in it.</h2></div>
  <div class="founder reveal" style="max-width:66ch;color:var(--stone)">
    <p>Almost everything written about moving to Spain is written by someone who hasn't. It is researched, aggregated, and translated from a press release &mdash; accurate enough, and useless exactly when you need it, which is at four in the afternoon when the consulate portal won't load and nobody can tell you why.</p>
    <p>This is the other thing. I made the move myself &mdash; years on a tourist visa, then the Digital Nomad Visa, the NIE, the paperwork that never quite matches the checklist, and Spanish residency in 2025. I came to Spain by way of Mexico, where I'd lived since 2017. I wrote down what actually happened, where the official version and the real one diverged, and what I would tell a friend at my own kitchen table.</p>
    <p>So that is what this is. Relocation guides that match reality. Neighbourhood profiles written by someone who has eaten there on a wet Tuesday in February. The money explained without the hand-waving. And the unglamorous true bits nobody warns you about &mdash; because those are the ones that matter.</p>
    <p>No paradise. No promises. Just the move, honestly, from someone already on the far side of it.</p>
    <div class="sig">LJ Koch &middot; Founder &middot; Spanish AfterLife &middot; Oliva Nova</div>
  </div>
</div></section>

<section class="chapter">
  <div class="media"><div class="media-img" data-par="0.1" style="background-image:url('/media/oliva-3.jpg')"></div></div>
  <h2>{rlines('Written from here,|not from abroad.')}</h2>
</section>

<section class="pad dark" id="inside"><div class="wrap">
  <div class="head"><span class="ovl">What's inside</span><h2 class="reveal">Six things worth getting right.</h2></div>
  <div class="cats reveal">{cats}</div>
</div></section>

<section class="pad" id="first"><div class="wrap">
  <div class="head"><span class="ovl">First issues</span><h2 class="reveal">What's coming first.</h2></div>
  <p class="reveal" style="color:var(--stone);max-width:62ch">The inaugural lineup is in production now. Each piece is written from direct experience, not assembled from elsewhere. Join the list below and we'll send you the first one the day it goes up.</p>
  <div class="arts">{arts}</div>
</div></section>

<section class="guide pad dark" id="list"><div class="wrap">
  <div class="guide-body">
    <span class="ovl">The list</span>
    <h2 style="margin:1.1rem 0 1rem">Be the first to read them.</h2>
    <p>One email when something worth your time goes up. The guides, the profiles, the honest bits. Nothing else, and nothing sold.</p>
    <form class="gform" id="gform" novalidate style="margin-top:1.8rem">
      <input type="email" name="EMAIL" placeholder="Your email" required>
      <button class="gbtn" type="submit">Keep me posted</button>
    </form>
    <p class="pnote" style="margin-top:1rem">No spam. Unsubscribe whenever. We never share your address.</p>
  </div>
</div></section>

<section class="pad"><div class="wrap">
  <div class="head"><span class="ovl">Already decided?</span><h2 class="reveal">Then let's talk about the move.</h2></div>
  <p class="reveal" style="color:var(--stone);max-width:58ch">If you've read enough to know Spain is the next chapter, the next step is a free 45-minute call &mdash; eligibility, finances, property, timeline. No pitch, just clarity.</p>
  <p class="reveal" style="margin-top:1.6rem"><a class="srow-link" href="/v2/#contact">Book your free call <span aria-hidden="true">&rarr;</span></a></p>
</div></section>
"""
    html = shell("Building My Life in Spain &mdash; STAGING v2 (ERA flow)",
                 "The guides, the money, the neighbourhoods and the true stories of building a life in the Valencia Community.",
                 body)
    # the journal page has a signup form; stub it like the v2 index does
    html = html.replace("<script>" + JS,
        "<script>" + JS + """
const gf=document.getElementById('gform');
if(gf)gf.addEventListener('submit',e=>{e.preventDefault();/* TODO: Mailchimp list-manage subscribe endpoint */console.log('[STAGING v2] journal signup',{email:e.target.EMAIL.value});alert('STAGING — logged to console.');});
""")
    return html


if __name__ == "__main__":
    for sub, html in (("properties", build_properties()), ("journal", build_journal())):
        d = os.path.join(ROOT, sub)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "index.html")
        open(p, "w", encoding="utf-8").write(html)
        print(f"wrote {p} ({len(html)//1024} KB)")
