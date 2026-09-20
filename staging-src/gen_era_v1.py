#!/usr/bin/env python3
# Generates staging/index.html — spanishafterlife.com homepage re-dressed in the
# visual language of era-residence.com. STAGING / throwaway prototype.
import html, os, json

import os as _os
OUT = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),"staging","index.html")

def ph(w, h, label="", cls="", img=None):
    if img:
        return (f'<div class="ph has-img {cls}" style="aspect-ratio:{w}/{h};'
                f"background-image:url('{img}')\" role=\"img\" aria-label=\"{label or 'Photograph'}\"></div>")
    return (f'<div class="ph {cls}" style="aspect-ratio:{w}/{h}" '
            f'role="img" aria-label="Image placeholder {w} by {h}">'
            f'<span class="ph-dim">{w} &times; {h}</span>'
            f'{f"<span class=ph-tag>{label}</span>" if label else ""}</div>')

PILLARS = [
 ("The Property","Fincas with olive groves, or beachfront access. At prices unavailable in the market you're leaving."),
 ("The Table","Food culture, markets, bodegas, the three-hour lunch. Valencia is the birthplace of paella."),
 ("The Course","Golf 300 days a year. Mediterranean landscape. A fraction of what you pay at home."),
 ("The Paddle","Padel as social infrastructure. Spain's own sport. How community is built here."),
 ("The Club","Beach clubs, Mediterranean sea, the long unhurried afternoon. This is Tuesday now."),
 ("The Horses","Equestrian estates, Andalusian horse culture, trail riding, polo. The working finca."),
 ("The Continent","Two hours to Paris, Madrid, Rome, Lisbon. Spain is not a country — it's a base."),
 ("The Canvas","Picasso, Dalí, Goya, Velázquez. Gaudí to the Alhambra. Beauty as infrastructure."),
 ("The Land","Pyrenees to Andalusia. National parks, dramatic coastline, serious hiking."),
 ("The Sail","Mediterranean sailing at its most refined. Palma, the Balearics, unspoiled harbours."),
 ("The Rhythm","Flamenco, jazz in Barcelona, live music in every plaza. The culture doesn't perform — it lives."),
 ("The Ride","Coll de Rates at sunrise, gravel through the inland sierras, the climbs pro teams winter on. Road, gravel, mountain — straight from the door."),
]

PLACES = [
 ("Costa Blanca North","Jávea &amp; Denia","From €280,000","The most sophisticated stretch of coastline in Spain. Sailing culture, serious restaurants, deep community. Where people who've done the research end up."),
 ("City Life","Valencia City","From €180,000","Spain's third city. Birthplace of paella. World-class food scene, extraordinary architecture, beach tram from the centre. Europe's most underrated city."),
 ("Unspoiled Coast","Oliva &amp; Cullera","From €180,000","Where the coastline hasn't been overdeveloped. Extraordinary beaches, local pace, genuine value — and where our founder lives, in Oliva Nova."),
 ("Finca Country","Inland — Ontinyent","From €120,000","The best-kept secret in European real estate. Fincas with olive groves at prices that bear no relation to the coast. Real Spain, for buyers seeking space and quiet."),
]

# The Numbers — Spain side is constant; the "leaving" side + intro switch CA/US.
WAITING = [
 ("Property","€400K buys a beachfront villa with a pool. €280K buys a finca with two hectares of olive groves. Your equity goes further than you think."),
 ("Cost of living","Dinner for two with wine: €40. Fresh produce markets that make the supermarket obsolete. Utilities at a fraction of what you pay now."),
 ("Healthcare","Spain ranks among the top healthcare systems in the world. Private cover for a couple: €200 – €400 per month. English-speaking providers throughout the Valencia Community."),
 ("Tax","On the Non-Lucrative Visa you become a Spanish resident, taxed on investment income at the savings-base rates — 19% on the first €6,000, 21% to €50,000, then 23%. Double-taxation treaties with the US and Canada keep the same income from being taxed twice."),
 ("Weather","300 days of sun. Mild winters. Sea swimming from April to November. The kind of January that makes the move feel obvious in retrospect."),
]
LEAVING = {
 "ca": ("The client selling a $1.5M Toronto semi or a $2M Vancouver townhouse arrives in Spain with genuinely transformative purchasing power.", [
   ("Property","$1.5M buys a semi-detached on a street of 50 neighbours. No land. No pool. Maintenance that costs more every year."),
   ("Cost of living","Groceries, restaurants, utilities, services — priced for a market that decided affordability was someone else's problem."),
   ("Healthcare","Public system under strain. Private insurance that costs more and covers less every renewal cycle."),
   ("Tax rate","Up to 53% marginal in Ontario and B.C. More every budget cycle."),
   ("Weather","Five tolerable months. Seven months of something you've stopped pretending to enjoy."),
 ]),
 "us": ("The client selling a $1.5M Bay Area bungalow or a $1.3M Seattle craftsman arrives in Spain with genuinely transformative purchasing power.", [
   ("Property","$1.5M buys a mid-century ranch a long drive from the coast. No land. No pool. Property tax that climbs with every assessment."),
   ("Cost of living","Groceries, restaurants, utilities, services — priced for a market that decided affordability was someone else's problem."),
   ("Healthcare","Premiums, deductibles, and a network you check before every appointment. Coverage that costs more the year you'll lean on it."),
   ("Tax rate","Up to 37% federal — plus 13.3% in California or 10.9% in New York. More every cycle."),
   ("Weather","Five tolerable months. Seven months of something you've stopped pretending to enjoy."),
 ]),
}

SERVICES = [
 ("Immigration Concierge","Your legal right to live here, handled. NLV, NIE, empadronamiento, CaixaBank, Beckham Law, tax registration. Managed through our vetted legal partner — you deal with us throughout.","Fixed fee from €3,500","Single applicant / €5,500 couple","See how immigration works","/immigration"),
 ("Real Estate — Buyer's Agency","The market you don't know yet. We do. Full buyer's representation across the Valencia Community. Fincas, beach apartments, equestrian estates, city properties. We know what locals know.","Transaction range €200K – €1.5M+","Buyer representation costs you nothing extra","See how property works","/real-estate"),
 ("The Full AfterLife","Most people want both — residency and property, run as one engagement, start to finish. That is The Full AfterLife.","","","See the whole move","/fullafterlife"),
 ("The Private Client","And some want the founder personally embedded from day one — every call, every decision, two years of advisory beside you. A different mode of engagement.","","","Meet The Private Client","/private-client"),
]

STEPS = [
 ("01","Strategy Call","Visa eligibility, financial structure, property goals, timeline. Free. No obligation. Just clarity."),
 ("02","Immigration","Non-Lucrative Visa, NIE, empadronamiento, CaixaBank, Beckham Law. Done properly the first time."),
 ("03","Property","Full buyer's agency. We represent you, not the seller. Commission paid by the seller's agent."),
 ("04","Settlement","Keys in hand. Utilities connected. Neighbours introduced. Your AfterLife begins."),
]


U="https://images.unsplash.com/"
PILLAR_IMGS=[U+p+"?w=1400&q=80" for p in [
 "photo-1564013799919-ab600027ffc6","photo-1515443961218-a51367888e4b","photo-1535131749006-b7f58c99034b",
 "photo-1554068865-24cecd4e34b8","photo-1507525428034-b723cf961d3e","photo-1553284965-83fd3e82fa5a",
 "photo-1499856871958-5b9627545d1a","photo-1583422409516-2895a77efded","photo-1464822759023-fed622ff2c3b",
 "photo-1534190760961-74e8c1c5c3da","photo-1516450360452-9312f5e86fc7","photo-1517649763962-0c623066013b"]]
PLACE_IMGS={
 "Jávea &amp; Denia":"/javea-denia.jpg",
 "Valencia City":U+"photo-1539037116277-4db20889f2d4?w=1400&q=85",
 "Oliva &amp; Cullera":"/oliva-cullera.jpg",
 "Inland — Ontinyent":U+"photo-1474979266404-7eaacbcd87c5?w=1400&q=85",
}
HERO_IMG="/hero.png"
JOURNAL_IMG=U+"photo-1512753360435-329c4535a9a7?w=1400&q=80"
GUIDE_IMG="/guide-cover.png"
LOCATIONS = ["Select country / province / state","Ontario","British Columbia","Alberta","Quebec","Other Canadian province","California","New York","Washington","Illinois","Texas","Florida","Other US state"]

# ---- build fragments ----
pillar_tabs = "\n".join(
  f'<button class="sw-tab" data-i="{i}" type="button"><span class="sw-idx">{i+1:02d}</span>'
  f'<span class="sw-name">{t}</span></button>' for i,(t,_) in enumerate(PILLARS))
pillar_panels = "\n".join(
  f'<div class="sw-panel" data-i="{i}">{ph(1200,1500,t,img=PILLAR_IMGS[i])}'
  f'<div class="sw-copy"><h3>{t}</h3><p>{d}</p></div></div>'
  for i,(t,d) in enumerate(PILLARS))

places_html = "\n".join(
  f'''<article class="place reveal">
    <div class="place-media">{ph(1600,1100,name,img=PLACE_IMGS.get(name))}</div>
    <div class="place-body">
      <span class="ovl">{tag}</span>
      <h3>{name}</h3>
      <p>{desc}</p>
      <span class="place-price">{price}</span>
    </div>
  </article>''' for tag,name,price,desc in PLACES)

def num_rows(rows):
    return "\n".join(
      f'<div class="num-row"><div class="num-k">{k}</div><div class="num-v">{v}</div></div>'
      for k,v in rows)

services_html = "\n".join(
  f'''<article class="svc reveal">
    <div class="svc-head"><h3>{name}</h3>{f'<span class="svc-fee">{fee}</span>' if fee else ''}</div>
    <p class="svc-desc">{desc}</p>
    {f'<p class="svc-sub">{sub}</p>' if sub else ''}
    <a class="svc-link" href="{href}">{link} <span aria-hidden="true">&rarr;</span></a>
  </article>''' for name,desc,fee,sub,link,href in SERVICES)

steps_html = "\n".join(
  f'<div class="step reveal"><div class="step-n">{n}</div><div class="step-b"><h3>{t}</h3><p>{d}</p></div></div>'
  for n,t,d in STEPS)

def _opt(i,o):
    attr=' value=""' if i==0 else ''
    return '<option'+attr+'>'+o+'</option>'
loc_opts = "\n".join(_opt(i,o) for i,o in enumerate(LOCATIONS))

CSS = r"""
:root{
  --cream:#F3F3EC; --ink:#17233B; --white:#FFFFFF;
  --sand:#E6DDCE; --sand-2:#D6C9B4; --stone:#5C5648;
  --ink-soft:rgba(23,35,59,.62); --line:rgba(23,35,59,.16);
  --cream-soft:rgba(243,243,236,.66); --line-d:rgba(243,243,236,.18);
  --serif:"Fraunces",Georgia,serif; --sans:"Archivo","Helvetica Neue",Arial,sans-serif;
  --script:"Ephesis",cursive;
  --ease:cubic-bezier(.16,1,.3,1); --pad:clamp(1.25rem,5vw,5.5rem);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:var(--sans);background:var(--cream);color:var(--ink);
  font-size:clamp(1rem,.95rem + .3vw,1.12rem);line-height:1.72;-webkit-font-smoothing:antialiased;
  font-weight:400;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
h1,h2,h3{font-family:var(--serif);font-weight:360;letter-spacing:-.02em;line-height:1.04}
h1{font-size:clamp(2.7rem,7.6vw,6rem)}
h2{font-size:clamp(2rem,5vw,3.7rem);line-height:1.06}
h3{font-size:clamp(1.35rem,2.4vw,2.05rem);letter-spacing:-.015em}
p{max-width:64ch}
.ovl{font-family:var(--sans);font-size:.68rem;font-weight:600;text-transform:uppercase;
  letter-spacing:.24em;color:var(--ink-soft)}
.script{font-family:var(--script);font-weight:400;letter-spacing:0}

/* ---- shell / rhythm ---- */
section{padding:clamp(4.5rem,11vh,10rem) var(--pad);position:relative}
.wrap{max-width:1440px;margin:0 auto}
.theme-dark{background:var(--ink);color:var(--cream)}
.theme-dark .ovl{color:var(--cream-soft)}
.theme-dark p{color:var(--cream-soft)}
.lede{font-family:var(--serif);font-weight:340;font-size:clamp(1.35rem,2.6vw,2.05rem);
  line-height:1.32;letter-spacing:-.01em;max-width:24ch;color:var(--ink)}
.body-muted{color:var(--stone)}

/* ---- placeholders ---- */
.ph{width:100%;background:
   linear-gradient(135deg,var(--sand) 0%,var(--sand-2) 100%);
  position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph::after{content:"";position:absolute;inset:0;
  background-image:repeating-linear-gradient(45deg,rgba(23,35,59,.05) 0 1px,transparent 1px 22px);
  mix-blend-mode:multiply}
.ph-dim{font-size:.72rem;font-weight:600;letter-spacing:.16em;color:rgba(23,35,59,.5);
  font-variant-numeric:tabular-nums;z-index:1}
.ph.has-img{background-size:cover;background-position:center}
.ph.has-img::after{content:none}
.ph-tag{position:absolute;top:.9rem;left:.9rem;font-size:.6rem;letter-spacing:.2em;
  text-transform:uppercase;color:rgba(23,35,59,.42);z-index:1}

/* ---- reveal ---- */
.js .reveal{opacity:0;transform:translateY(26px);filter:blur(6px);
  transition:opacity 1.1s var(--ease),transform 1.1s var(--ease),filter 1.1s var(--ease)}
.reveal.in{opacity:1;transform:none;filter:none}
.rline{display:block;overflow:hidden}
.rline > span{display:block}
.js .rline > span{display:block;transform:translateY(105%);transition:transform 1s var(--ease)}
.in .rline > span,.rline.in > span{transform:none}
@media (prefers-reduced-motion:reduce){
  .reveal,.rline>span{opacity:1!important;transform:none!important;filter:none!important;transition:none}
}

/* ---- nav ---- */
.nav{position:fixed;top:0;left:0;right:0;z-index:60;display:flex;align-items:center;
  justify-content:space-between;padding:1.15rem var(--pad);
  mix-blend-mode:difference;color:#fff}
.brand{font-family:var(--serif);font-size:1.15rem;letter-spacing:-.01em;line-height:1}
.brand b{font-weight:400}
.nav-links{display:flex;gap:2.1rem;align-items:center}
.nav-links a{font-size:.72rem;text-transform:uppercase;letter-spacing:.18em;font-weight:500;
  opacity:.9;transition:opacity .4s var(--ease)}
.nav-links a:hover{opacity:.55}
.nav-cta{border:1px solid rgba(255,255,255,.5);padding:.55rem 1.1rem;border-radius:100px}
.burger{display:none;flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:6px}
.burger span{width:26px;height:1.5px;background:#fff;transition:transform .5s var(--ease),opacity .3s}

/* ---- mobile menu modal ---- */
.menu{position:fixed;inset:0;z-index:55;background:var(--ink);color:var(--cream);
  display:flex;flex-direction:column;justify-content:center;padding:var(--pad);
  clip-path:inset(0 0 100% 0);transition:clip-path .8s var(--ease);pointer-events:none}
.menu.open{clip-path:inset(0 0 0 0);pointer-events:auto}
.menu a{font-family:var(--serif);font-size:clamp(2rem,9vw,3.4rem);font-weight:340;
  padding:.35rem 0;opacity:0;transform:translateY(20px);transition:opacity .6s var(--ease),transform .6s var(--ease)}
.menu.open a{opacity:1;transform:none}
.menu.open a:nth-child(1){transition-delay:.15s}.menu.open a:nth-child(2){transition-delay:.21s}
.menu.open a:nth-child(3){transition-delay:.27s}.menu.open a:nth-child(4){transition-delay:.33s}
.menu.open a:nth-child(5){transition-delay:.39s}.menu.open a:nth-child(6){transition-delay:.45s}
.menu-sig{font-family:var(--script);font-size:2rem;margin-top:2rem;opacity:.7}

/* ---- hero ---- */
.hero{position:relative;min-height:100svh;display:flex;align-items:flex-end;
  padding-bottom:clamp(2.5rem,7vh,5rem);color:var(--cream);overflow:hidden}
.hero-bg{position:absolute;inset:0;z-index:-2}
.hero-bg .ph{height:118%;border-radius:0}
.hero-bg .ph::before{content:"";position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(23,35,59,.35),rgba(23,35,59,.66));z-index:1}
.hero-inner{width:100%;max-width:1440px;margin:0 auto;position:relative;z-index:1}
.hero h1{max-width:15ch;text-shadow:0 2px 40px rgba(23,35,59,.3)}
.hero h1 em{font-style:italic;font-weight:300}
.hero-deck{max-width:46ch;margin-top:1.6rem;color:rgba(243,243,236,.9);font-size:clamp(1rem,1.4vw,1.2rem)}
.hero-actions{display:flex;gap:1rem;margin-top:2.2rem;flex-wrap:wrap}
.btn{font-family:var(--sans);font-size:.74rem;text-transform:uppercase;letter-spacing:.16em;
  font-weight:600;padding:1rem 1.9rem;border-radius:100px;cursor:pointer;border:1px solid transparent;
  transition:background .5s var(--ease),color .5s var(--ease),border-color .5s var(--ease);display:inline-flex;gap:.6rem}
.btn-solid{background:var(--cream);color:var(--ink)}
.btn-solid:hover{background:transparent;color:var(--cream);border-color:var(--cream)}
.btn-ghost{border-color:rgba(243,243,236,.5);color:var(--cream)}
.btn-ghost:hover{background:var(--cream);color:var(--ink)}
.hero-facts{display:flex;gap:clamp(1.5rem,4vw,3.4rem);margin-top:3rem;flex-wrap:wrap;
  border-top:1px solid rgba(243,243,236,.22);padding-top:1.5rem}
.fact{max-width:16ch}
.fact b{font-family:var(--serif);font-weight:340;font-size:clamp(1.5rem,2.4vw,2.1rem);display:block;line-height:1}
.fact span{font-size:.72rem;text-transform:uppercase;letter-spacing:.16em;color:rgba(243,243,236,.66);margin-top:.5rem;display:block}
.hero-sig{position:absolute;right:0;bottom:.2rem;font-family:var(--script);
  font-size:clamp(1.4rem,2.6vw,2.2rem);color:rgba(243,243,236,.78);z-index:1}

/* ---- section intro ---- */
.intro{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,5vw,5rem);align-items:end;
  margin-bottom:clamp(2.5rem,6vh,5rem)}
.intro .idx{font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-soft);
  display:block;margin-bottom:1.4rem}
.theme-dark .intro .idx{color:var(--cream-soft)}
.intro-lede{align-self:end}

/* ---- switcher (12 pillars) ---- */
.switch{padding:0}
.switch-track{height:calc(12 * 46vh + 100vh)}
.switch-sticky{position:sticky;top:0;height:100svh;display:grid;
  grid-template-columns:minmax(280px,34%) 1fr;gap:0;align-items:stretch;overflow:hidden}
.sw-list{align-self:center;padding:0 clamp(1.25rem,4vw,4rem);display:flex;flex-direction:column;gap:.1rem}
.sw-head{font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;color:var(--cream-soft);margin-bottom:1.6rem}
.sw-tab{background:none;border:0;text-align:left;cursor:pointer;display:flex;gap:1rem;align-items:baseline;
  padding:.5rem 0;color:var(--cream);opacity:.4;transition:opacity .5s var(--ease);font-family:var(--serif)}
.sw-tab .sw-idx{font-family:var(--sans);font-size:.7rem;letter-spacing:.1em;color:var(--cream-soft);
  font-variant-numeric:tabular-nums}
.sw-tab .sw-name{font-size:clamp(1.15rem,2vw,1.7rem);line-height:1.1;transition:transform .5s var(--ease)}
.sw-tab.active{opacity:1}
.sw-tab.active .sw-name{transform:translateX(10px)}
.sw-tab:hover{opacity:.8}
.sw-stage{position:relative;background:#141d31}
.sw-panel{position:absolute;inset:0;display:grid;grid-template-rows:1fr auto;
  opacity:0;transition:opacity .7s var(--ease);pointer-events:none}
.sw-panel.active{opacity:1;pointer-events:auto}
.sw-panel .ph{height:100%;position:absolute;inset:0}
.sw-panel .ph::before{content:"";position:absolute;inset:0;
  background:linear-gradient(180deg,transparent 40%,rgba(20,29,49,.85));z-index:1}
.sw-copy{position:relative;z-index:2;align-self:end;padding:clamp(1.5rem,4vw,3.5rem);color:var(--cream)}
.sw-copy h3{font-size:clamp(1.8rem,3.4vw,3rem)}
.sw-copy p{max-width:44ch;margin-top:.9rem;color:rgba(243,243,236,.82)}

/* ---- the numbers / toggle ---- */
.toggle{display:inline-flex;position:relative;border:1px solid var(--line-d);border-radius:100px;
  padding:4px;margin-top:1.6rem;background:rgba(243,243,236,.04)}
.toggle button{position:relative;z-index:1;background:none;border:0;cursor:pointer;
  font-family:var(--sans);font-size:.72rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;
  color:var(--cream-soft);padding:.7rem 1.5rem;border-radius:100px;transition:color .5s var(--ease)}
.toggle button.on{color:var(--ink)}
.toggle .knob{position:absolute;top:4px;bottom:4px;left:4px;width:calc(50% - 4px);
  background:var(--cream);border-radius:100px;transition:transform .55s var(--ease);z-index:0}
.toggle.us .knob{transform:translateX(100%)}
.num-intro{font-family:var(--serif);font-weight:340;font-size:clamp(1.3rem,2.4vw,1.95rem);
  line-height:1.34;max-width:30ch;margin-top:2.2rem;min-height:4.2em}
.num-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,5vw,5rem);margin-top:3rem}
.num-col > .ovl{display:block;margin-bottom:.4rem}
.num-col h3{font-size:clamp(1.5rem,2.4vw,2rem);margin-bottom:1.6rem;font-weight:360}
.num-row{display:grid;grid-template-columns:minmax(90px,26%) 1fr;gap:1.2rem;
  padding:1.15rem 0;border-top:1px solid var(--line-d)}
.num-k{font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:var(--cream-soft);padding-top:.2rem}
.num-v{color:rgba(243,243,236,.9);font-size:1rem;line-height:1.6}
.num-col.leaving .num-v{color:rgba(243,243,236,.62)}

/* ---- places ---- */
.place{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4rem);align-items:center;
  padding:clamp(2rem,5vh,4.5rem) 0;border-top:1px solid var(--line)}
.place:nth-child(even) .place-media{order:2}
.place-body h3{margin:.7rem 0 1rem}
.place-body p{color:var(--stone);max-width:40ch}
.place-price{font-family:var(--serif);font-size:1.15rem;margin-top:1.6rem;display:inline-block;
  padding-bottom:.3rem;border-bottom:1px solid var(--line)}

/* ---- services ---- */
.svc-list{display:grid;gap:0}
.svc{padding:clamp(2rem,4vh,3.4rem) 0;border-top:1px solid var(--line);
  display:grid;grid-template-columns:1fr 1.2fr;gap:clamp(1rem,4vw,4rem);align-items:start}
.svc-head{display:flex;flex-direction:column;gap:.9rem}
.svc-fee{font-family:var(--sans);font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;
  font-weight:600;color:var(--ink-soft)}
.svc-desc{color:var(--stone)}
.svc-sub{font-size:.85rem;color:var(--ink-soft);margin-top:.7rem}
.svc-link{font-size:.74rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;
  margin-top:1.4rem;display:inline-flex;gap:.5rem;align-items:center;
  border-bottom:1px solid var(--line);padding-bottom:.3rem;transition:gap .4s var(--ease)}
.svc-link:hover{gap:1rem}
.founder-note{margin-top:3.5rem;max-width:60ch;color:var(--stone);font-style:italic;
  font-family:var(--serif);font-size:1.15rem;line-height:1.6}

/* ---- how (steps) ---- */
.steps{display:grid;gap:0;margin-top:1rem}
.step{display:grid;grid-template-columns:auto 1fr;gap:clamp(1.2rem,4vw,3.5rem);
  padding:clamp(1.6rem,3.5vh,2.8rem) 0;border-top:1px solid var(--line-d);align-items:baseline}
.step-n{font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.4rem);color:var(--cream-soft);font-weight:340}
.step-b h3{margin-bottom:.6rem}
.step-b p{color:rgba(243,243,236,.72);max-width:52ch}

/* ---- journal ---- */
.journal{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(1.5rem,5vw,5rem);align-items:center}
.journal .ph{width:100%}
.journal-body h2{margin-bottom:1.2rem}
.journal-body p{color:var(--stone)}
.journal-link{margin-top:1.8rem;display:inline-flex;gap:.5rem;font-size:.74rem;text-transform:uppercase;
  letter-spacing:.14em;font-weight:600;border-bottom:1px solid var(--line);padding-bottom:.3rem}

/* ---- guide ---- */
.guide{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(1.5rem,5vw,5rem);align-items:center}
.guide-media .ph{width:100%}
.guide-body h2{margin-bottom:1.2rem}
.guide-body p{color:rgba(243,243,236,.82)}
.gform{margin-top:2rem;display:flex;flex-wrap:wrap;gap:.8rem;max-width:520px}
.gform input[type=email]{flex:1;min-width:220px;background:transparent;border:0;border-bottom:1px solid var(--line-d);
  color:var(--cream);padding:.9rem .2rem;font-family:var(--sans);font-size:1rem}
.gform input::placeholder{color:var(--cream-soft)}
.gform input:focus{outline:none;border-color:var(--cream)}
.consent{display:flex;gap:.7rem;font-size:.8rem;color:var(--cream-soft);margin-top:1rem;max-width:52ch;align-items:flex-start}
.consent input{margin-top:.25rem}
.microcopy{font-size:.78rem;color:var(--cream-soft);margin-top:1.2rem;letter-spacing:.02em}

/* ---- contact ---- */
.contact-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(2rem,5vw,5rem);align-items:start}
.agenda{list-style:none;margin-top:2rem;display:grid;gap:0}
.agenda li{display:grid;grid-template-columns:auto 1fr;gap:1.2rem;padding:1.1rem 0;
  border-top:1px solid var(--line);align-items:baseline}
.agenda .an{font-family:var(--serif);color:var(--ink-soft)}
.agenda p{color:var(--stone);font-size:.95rem}
.cform{display:grid;gap:1.3rem}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:1.3rem}
.field{display:flex;flex-direction:column;gap:.5rem}
.field label{font-size:.68rem;text-transform:uppercase;letter-spacing:.16em;color:var(--ink-soft);font-weight:600}
.field input,.field select,.field textarea{background:transparent;border:0;border-bottom:1px solid var(--line);
  padding:.7rem 0;font-family:var(--sans);font-size:1rem;color:var(--ink);border-radius:0}
.field textarea{resize:vertical;min-height:90px}
.field input:focus,.field select,.field textarea:focus{outline:none;border-color:var(--ink)}
.cform .btn{align-self:start;margin-top:.5rem;background:var(--ink);color:var(--cream)}
.cform .btn:hover{background:transparent;color:var(--ink);border-color:var(--ink)}

/* ---- footer ---- */
.foot{padding:clamp(3rem,7vh,6rem) var(--pad) 2.5rem;background:var(--ink);color:var(--cream)}
.foot-top{display:flex;justify-content:space-between;gap:2rem;flex-wrap:wrap;
  padding-bottom:2.5rem;border-bottom:1px solid var(--line-d)}
.foot-sig{font-family:var(--script);font-size:clamp(2rem,5vw,3.2rem)}
.foot-nav{display:flex;gap:1.6rem;flex-wrap:wrap}
.foot-nav a{font-size:.72rem;text-transform:uppercase;letter-spacing:.16em;color:var(--cream-soft)}
.foot-bot{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:1.6rem;
  font-size:.72rem;color:var(--cream-soft);letter-spacing:.04em}

/* ---- staging badge ---- */
#staging-badge{position:fixed;left:1rem;bottom:1rem;z-index:90;background:#B4643C;color:#fff;
  font-family:var(--sans);font-size:.62rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
  padding:.5rem .8rem;border-radius:4px;box-shadow:0 6px 20px rgba(23,35,59,.3)}

/* ---- responsive ---- */
@media (max-width:900px){
  .nav-links{display:none}
  .burger{display:flex}
  .intro,.num-grid,.place,.place:nth-child(even) .place-media,.svc,.journal,.guide,.contact-grid,.frow{
    grid-template-columns:1fr}
  .place:nth-child(even) .place-media{order:0}
  .switch-sticky{grid-template-columns:1fr;grid-template-rows:auto 1fr}
  .switch-track{height:calc(12 * 30vh + 100vh)}
  .sw-list{flex-direction:row;overflow-x:auto;gap:1.2rem;padding:1.1rem var(--pad);align-self:start;
    background:#141d31;-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .sw-list::-webkit-scrollbar{display:none}
  .sw-head{display:none}
  .sw-tab{flex:0 0 auto;padding:.3rem 0}
  .sw-tab .sw-name{font-size:1.05rem}
  .sw-tab.active .sw-name{transform:none}
  .num-intro{min-height:auto}
  .hero-facts{gap:1.5rem}
  .hero-sig{display:none}
}
"""

JS = r"""
/* ---------- mobile menu ---------- */
const burger=document.querySelector('.burger'), menu=document.getElementById('menu');
burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o);
  document.body.style.overflow=o?'hidden':'';});
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');
  burger.setAttribute('aria-expanded','false');document.body.style.overflow='';}));

/* ---------- eased smooth scroll (mini-Lenis: real document scroll, so position:sticky still works) ---------- */
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
let smooth=fine&&!reduce, target=window.scrollY, current=window.scrollY, raf=null;
function maxScroll(){return document.documentElement.scrollHeight-window.innerHeight;}
function loop(){
  current+=(target-current)*0.09;
  if(Math.abs(target-current)<0.4){current=target;}
  window.scrollTo(0,current);
  onScroll();
  if(current!==target){raf=requestAnimationFrame(loop);}else{raf=null;}
}
function kick(){if(raf===null)raf=requestAnimationFrame(loop);}
if(smooth){
  window.addEventListener('wheel',e=>{
    // let inner scrollable areas (mobile tab strip) scroll natively
    if(e.target.closest('.sw-list,.menu')) return;
    e.preventDefault();
    target=Math.max(0,Math.min(maxScroll(),target+e.deltaY));
    kick();
  },{passive:false});
  window.addEventListener('keydown',e=>{
    const k=e.key; const step=window.innerHeight;
    const map={PageDown:step*.9,PageUp:-step*.9,ArrowDown:120,ArrowUp:-120,' ':step*.9,Home:-1e9,End:1e9};
    if(!(k in map)) return; if(document.activeElement&&/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) return;
    e.preventDefault(); target=Math.max(0,Math.min(maxScroll(),(k==='Home'?0:k==='End'?maxScroll():target+map[k]))); kick();
  });
  // keep target synced if the user drags the native scrollbar
  window.addEventListener('scroll',()=>{ if(raf===null){current=target=window.scrollY;onScroll();} },{passive:true});
}else{
  window.addEventListener('scroll',onScroll,{passive:true});
}
function scrollToY(y){ if(smooth){target=Math.max(0,Math.min(maxScroll(),y));kick();} else window.scrollTo({top:y,behavior:'smooth'}); }
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{
  const el=document.querySelector(a.getAttribute('href')); if(!el)return; e.preventDefault();
  scrollToY(el.getBoundingClientRect().top+window.scrollY);
}));

/* ---------- reveals ---------- */
const io=new IntersectionObserver((es)=>{es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:.14,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal,.rline').forEach(el=>io.observe(el));

/* ---------- parallax + switcher (driven each scroll frame) ---------- */
const parEls=[...document.querySelectorAll('[data-par]')];
const track=document.querySelector('.switch-track'), tabs=[...document.querySelectorAll('.sw-tab')],
      panels=[...document.querySelectorAll('.sw-panel')];
let activePillar=-1;
function setPillar(i){ if(i===activePillar)return; activePillar=i;
  tabs.forEach((t,n)=>t.classList.toggle('active',n===i));
  panels.forEach((p,n)=>p.classList.toggle('active',n===i));
}
setPillar(0);
function onScroll(){
  const y=window.scrollY;
  for(const el of parEls){
    const r=el.getBoundingClientRect(); const speed=parseFloat(el.dataset.par);
    const off=(r.top+r.height/2-window.innerHeight/2);
    el.style.transform='translate3d(0,'+(-off*speed).toFixed(1)+'px,0)';
  }
  if(track){
    const r=track.getBoundingClientRect(); const total=track.offsetHeight-window.innerHeight;
    const prog=Math.min(1,Math.max(0,(-r.top)/total));
    setPillar(Math.min(tabs.length-1,Math.floor(prog*tabs.length)));
  }
}
tabs.forEach((t,i)=>t.addEventListener('click',()=>{
  const total=track.offsetHeight-window.innerHeight;
  const y=track.getBoundingClientRect().top+window.scrollY + (i+0.5)/tabs.length*total;
  scrollToY(y);
}));
onScroll();
window.addEventListener('resize',onScroll);

/* ---------- US / Canada toggle ---------- */
const tg=document.getElementById('toggle'), numIntro=document.getElementById('num-intro'),
      leaving=document.getElementById('leaving');
const DATA=window.__NUM__;
function setCountry(c){
  tg.classList.toggle('us',c==='us');
  tg.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.c===c));
  numIntro.textContent=DATA[c].intro;
  leaving.innerHTML=DATA[c].rows.map(r=>`<div class="num-row"><div class="num-k">${r[0]}</div><div class="num-v">${r[1]}</div></div>`).join('');
}
tg.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>setCountry(b.dataset.c)));
setCountry('ca');

/* ---------- forms: stubbed to console (STAGING) ---------- */
document.getElementById('gform').addEventListener('submit',e=>{
  e.preventDefault();
  // TODO(real endpoint): Mailchimp list-manage subscribe — POST https://<dc>.list-manage.com/subscribe/post?u=<U>&id=<ID>
  console.log('[STAGING] guide signup — TODO wire to Mailchimp list-manage endpoint', {email:e.target.EMAIL.value});
  alert('STAGING — guide form logged to console (not sent).');
});
document.getElementById('cform').addEventListener('submit',e=>{
  e.preventDefault();
  // TODO(real endpoint): Formspree — POST https://formspree.io/f/<FORM_ID>
  const d=Object.fromEntries(new FormData(e.target).entries());
  console.log('[STAGING] consultation request — TODO wire to Formspree endpoint', d);
  alert('STAGING — contact form logged to console (not sent).');
});
"""

NUM_JS_DATA = "window.__NUM__=" + json.dumps({
  "ca":{"intro":LEAVING["ca"][0],"rows":LEAVING["ca"][1]},
  "us":{"intro":LEAVING["us"][0],"rows":LEAVING["us"][1]},
}, ensure_ascii=False).replace("</","<\\/") + ";"

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<script>document.documentElement.className='js';</script>
<title>Spanish AfterLife — STAGING (ERA prototype)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..500;1,9..144,300..460&family=Archivo:wght@400;500;600&family=Ephesis&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<!-- STAGING badge — remove this one element (and #staging-badge CSS) to clear -->
<div id="staging-badge">Staging · ERA prototype</div>

<nav class="nav">
  <a class="brand" href="#top"><b>Spanish</b> AfterLife</a>
  <div class="nav-links">
    <a href="#life">The Life</a>
    <a href="#reality">The Numbers</a>
    <a href="#places">Where</a>
    <a href="#how">How It Works</a>
    <a href="#journal">Journal</a>
    <a class="nav-cta" href="#contact">Start Here</a>
  </div>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</nav>

<div class="menu" id="menu">
  <a href="#life">The Life</a>
  <a href="#reality">The Numbers</a>
  <a href="#places">Where</a>
  <a href="#how">How It Works</a>
  <a href="#journal">Journal</a>
  <a href="#contact">Start Here</a>
  <div class="menu-sig">Why wait for the AfterLife?</div>
</div>

<!-- ============ HERO ============ -->
<header class="hero" id="top">
  <div class="hero-bg">
    <!-- OVERLAY ANCHOR: hero video / media layer mounts here (skipped in this build) -->
    {ph(2400,1350,"Mediterranean coast",img=HERO_IMG)}
  </div>
  <div class="hero-inner">
    <h1 class="reveal"><span class="rline"><span>Your best years.</span></span><span class="rline"><span><em>Starting now.</em></span></span></h1>
    <p class="hero-deck reveal">Mediterranean weather. World-class food. A continent at your door. Property that makes your home market look like a bad joke. This is what the other side of the decision looks like.</p>
    <div class="hero-actions reveal">
      <a class="btn btn-solid" href="#life">Explore the Life</a>
      <a class="btn btn-ghost" href="#contact">Talk to Us</a>
    </div>
    <div class="hero-facts reveal">
      <div class="fact"><b>300</b><span>Days of sun per year</span></div>
      <div class="fact"><b>€200K</b><span>Beachfront entry, Valencia coast</span></div>
      <div class="fact"><b>2 hrs</b><span>To Paris, Madrid, Rome, Lisbon</span></div>
    </div>
    <div class="hero-sig">Why wait for the AfterLife?</div>
  </div>
</header>

<!-- ============ 12 PILLARS — sticky switcher ============ -->
<section class="switch theme-dark" id="life">
  <div class="switch-track">
    <div class="switch-sticky">
      <div class="sw-list">
        <div class="sw-head">Twelve reasons this is the right move</div>
        {pillar_tabs}
      </div>
      <div class="sw-stage">
        {pillar_panels}
      </div>
    </div>
  </div>
</section>

<!-- ============ THE NUMBERS — US/Canada two-state toggle ============ -->
<section class="theme-dark" id="reality">
  <div class="wrap">
    <div class="intro">
      <div><h2 class="reveal">What your equity actually buys</h2></div>
      <div class="intro-lede reveal">
        <div class="toggle" id="toggle" role="tablist" aria-label="Home market">
          <span class="knob" aria-hidden="true"></span>
          <button data-c="ca" role="tab">Canada</button>
          <button data-c="us" role="tab">United States</button>
        </div>
        <p class="num-intro" id="num-intro"></p>
      </div>
    </div>
    <div class="num-grid">
      <div class="num-col waiting reveal">
        <span class="ovl">What's waiting</span>
        <h3>The market you're moving to</h3>
        {num_rows(WAITING)}
      </div>
      <div class="num-col leaving reveal">
        <span class="ovl">What you're leaving</span>
        <h3>The market you know</h3>
        <div id="leaving"></div>
      </div>
    </div>
  </div>
</section>

<!-- ============ PLACES ============ -->
<section id="places">
  <div class="wrap">
    <div class="intro">
      <div><h2 class="reveal">The Valencia Community</h2></div>
      <p class="intro-lede body-muted reveal">We are based here. We know what each area gives you and what it asks of you. Our region runs the length of the Valencia Community and south into Murcia — Altea, Calpe, Benidorm and the smaller coastal and inland towns included.</p>
    </div>
    {places_html}
  </div>
</section>

<!-- ============ SERVICES ============ -->
<section id="services">
  <div class="wrap">
    <div class="intro">
      <div><h2 class="reveal">The firm that makes the move happen</h2></div>
      <p class="intro-lede body-muted reveal">Immigration, property, banking, settlement — one relationship, start to finish.</p>
    </div>
    <div class="svc-list">
      {services_html}
    </div>
    <p class="founder-note reveal">Our founder made the move personally — from Mexico to Spain, through the tourist-visa years, the Digital Nomad Visa, and Spanish residency — and lives on the Valencia coast today. Every piece of guidance comes from experience.</p>
  </div>
</section>

<!-- ============ HOW WE WORK ============ -->
<section class="theme-dark" id="how">
  <div class="wrap">
    <div class="intro">
      <div><h2 class="reveal">Everything between the decision and the first morning</h2></div>
      <p class="intro-lede reveal">Spanish AfterLife is the firm that makes the move happen. Immigration, property, banking, settlement — one relationship, start to finish.</p>
    </div>
    <div class="steps">
      {steps_html}
    </div>
  </div>
</section>

<!-- ============ JOURNAL ============ -->
<section id="journal">
  <div class="wrap journal">
    <div class="reveal" data-par="0.04">{ph(1200,800,"Journal",img=JOURNAL_IMG)}</div>
    <div class="journal-body reveal">
      <h2>Building My Life in Spain</h2>
      <p class="body-muted">Notes from the other side of the decision — guides, neighbourhood profiles, the money, and true stories of building a life in Spain's Valencia Community. Written from here, not from abroad.</p>
      <a class="journal-link" href="/building-my-life-in-spain">Read the journal <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
</section>

<!-- ============ GUIDE CAPTURE ============ -->
<section class="theme-dark" id="guide">
  <div class="wrap guide">
    <div class="guide-media reveal" data-par="0.05">{ph(1000,1250,"Guide cover",img=GUIDE_IMG)}</div>
    <div class="guide-body reveal">
      <h2>Your Complete Guide to Retiring in Spain</h2>
      <p>The visa, the property, and the honest cost of the life — the numbers most people never run. Written from the Valencia coast, not from abroad.</p>
      <form class="gform" id="gform" novalidate>
        <input type="email" name="EMAIL" placeholder="Your email address" required aria-label="Your email address">
        <button class="btn btn-solid" type="submit">Send me the guide</button>
      </form>
      <label class="consent"><input type="checkbox" name="consent" required> Email me the guide and the occasional honest update. I accept the <a href="/privacy" style="text-decoration:underline">Privacy Policy</a> and can unsubscribe anytime.</label>
      <p class="microcopy">Free. No obligation. Straight to your inbox.</p>
    </div>
  </div>
</section>

<!-- ============ CONTACT ============ -->
<section id="contact">
  <div class="wrap contact-grid">
    <div class="reveal">
      
      <h2>Find out if Spain is right for you.</h2>
      <p class="body-muted" style="margin-top:1.2rem">A free 45-minute call. We cover your visa eligibility, what your money buys here, the timeline, and whether Spain is actually the right move for your situation. If it isn't, we'll tell you that too.</p>
      <ul class="agenda">
        <li><span class="an">01</span><p>Visa eligibility — NLV income requirements, Beckham Law, what changes when you arrive</p></li>
        <li><span class="an">02</span><p>Financial picture — what your equity buys here and how to structure the move</p></li>
        <li><span class="an">03</span><p>Property goals — which area, which property type, which budget makes sense</p></li>
        <li><span class="an">04</span><p>Real talk — whether Spain is the right move for you, honestly</p></li>
      </ul>
    </div>
    <form class="cform" id="cform" novalidate>
      <div class="frow">
        <div class="field"><label>First Name</label><input name="first_name" required></div>
        <div class="field"><label>Last Name</label><input name="last_name" required></div>
      </div>
      <div class="field"><label>Email Address</label><input type="email" name="email" required></div>
      <div class="field"><label>Where are you based?</label><select name="location">{loc_opts}</select></div>
      <div class="field"><label>What's driving the move?</label><select name="interest"><option value="">Select one</option><option>Immigration / visa</option><option>Property purchase</option><option>The full move (both)</option><option>Private Client</option><option>Just exploring</option></select></div>
      <div class="field"><label>Anything that would help us prepare</label><textarea name="message" placeholder="Budget, timeline, areas of interest, questions you already have..."></textarea></div>
      <button class="btn" type="submit">Book My Free Consultation</button>
    </form>
  </div>
</section>

<footer class="foot">
  <div class="foot-top">
    <div class="foot-sig">Why wait for the AfterLife?</div>
    <div class="foot-nav">
      <a href="#life">The Life</a><a href="#reality">The Numbers</a><a href="#places">Where</a>
      <a href="#how">How It Works</a><a href="#journal">Journal</a><a href="#contact">Start Here</a>
    </div>
  </div>
  <div class="foot-bot">
    <span>© 2025 LJ Koch Group Inc. · Spanish AfterLife</span>
    <span>Valencia Community, Spain</span>
  </div>
</footer>

<script>{NUM_JS_DATA}</script>
<script>{JS}</script>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT,"w",encoding="utf-8").write(HTML)
print("wrote", OUT, f"({len(HTML)//1024} KB)")
print("pillars:", len(PILLARS), "places:", len(PLACES), "services:", len(SERVICES), "steps:", len(STEPS))
