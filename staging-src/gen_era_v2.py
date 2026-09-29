#!/usr/bin/env python3
# staging/v2/index.html — ERA-flow v2: image-led, sparse text, cinematic scroll.
import os, json, io as _io, sys as _sys
import os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import era_seo as SEO
OUT=_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),"staging","v2","index.html")
PILLAR_FULL=json.load(_io.open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"content","pillars.json"),encoding="utf-8"))
HX=json.load(_io.open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"content","home_extra.json"),encoding="utf-8"))
REGION_LINE=_io.open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"content","region.txt"),encoding="utf-8").read().strip()
U="https://images.unsplash.com/"
def uimg(id,w=1600,q=80): return f"{U}{id}?w={w}&q={q}"

# proven-loading image ids (from the live site)
PILLAR_IDS=["photo-1564013799919-ab600027ffc6","photo-1515443961218-a51367888e4b","photo-1535131749006-b7f58c99034b",
 "photo-1554068865-24cecd4e34b8","photo-1507525428034-b723cf961d3e","photo-1553284965-83fd3e82fa5a",
 "photo-1499856871958-5b9627545d1a","photo-1583422409516-2895a77efded","photo-1464822759023-fed622ff2c3b",
 "photo-1534190760961-74e8c1c5c3da","photo-1516450360452-9312f5e86fc7","photo-1517649763962-0c623066013b"]

# --- SIMPLIFIED copy (trimmed from existing, figures preserved) ---
PILLARS=[  # (title, ~6-word essence)
 ("The Property","Fincas and beachfront, at impossible prices."),
 ("The Table","Markets, bodegas, the three-hour lunch."),
 ("The Course","Golf, three hundred days a year."),
 ("The Paddle","Padel — how community is built here."),
 ("The Club","The long, unhurried afternoon."),
 ("The Horses","Equestrian estates and working fincas."),
 ("The Continent","Two hours to Paris, Rome, Lisbon."),
 ("The Canvas","Picasso to Gaudí. Beauty everywhere."),
 ("The Land","Mountains, coast, serious hiking."),
 ("The Sail","The Balearics, unspoiled harbours."),
 ("The Rhythm","Flamenco, jazz, music in every plaza."),
 ("The Ride","Road, gravel, mountain — from your door."),
]
PLACES=[  # tag, name, price, short line, image
 ("Costa Blanca North","Jávea &amp; Denia","From €280,000","The most sophisticated stretch of the coast.","/javea-denia.webp"),
 ("City Life","Valencia City","From €180,000","Europe's most underrated city.","/media/valencia-3.webp"),
 ("Unspoiled Coast","Oliva &amp; Cullera","From €180,000","The coast that never got overbuilt.","/media/oliva-2.webp"),
 ("Finca Country","Inland — Ontinyent","From €120,000","Olive groves at inland prices.",uimg("photo-1474979266404-7eaacbcd87c5",1600,85)),
]
# Numbers — lean: 3 contrasts. Spain constant; home switches. Figures verbatim.
# Numbers — production's rows, verbatim (content/home_extra.json). Spain constant; home switches.
WAIT=[(k,v) for g,k,v in HX["num_spain"]]
LEAVE={c:(HX["num_intro"][c],[(k,v) for g,k,v in HX["num_home"] if g in (c,"both")]) for c in ("ca","us")}
SERVICES=[
 ("Immigration Concierge","Your legal right to live in Spain, handled end to end — visa, NIE, banking, tax registration.","Fixed fee from &euro;3,500<small>Single applicant / &euro;5,500 couple</small>","/v2/immigration/"),
 ("Real Estate","Full buyer's agency across the Valencia Community. We represent you, never the seller.","&euro;200K – &euro;1.5M+<small>Buyer representation costs you nothing extra</small>","/v2/real-estate/"),
 ("The Full AfterLife","Residency and property run as a single engagement — from the first call to the keys.","","/v2/fullafterlife/"),
 ("The Private Client","The founder personally embedded from day one. Every call, every decision, beside you.","","/v2/private-client/"),
]
SVC_IMGS=["/media/valencia-2.webp","/media/valencia-1.webp","/oliva-cullera.webp","/media/home-3.webp"]
SVC_TAGS=["Residency","Property","Everything","Bespoke"]
STEPS=[tuple(x) for x in HX["how"]["steps"]]

# Cross-page links. These pages are NOT part of the redesign and do not exist on the
# era-staging preview, so they point at the live site to keep the prototype clickable.
# AT PRODUCTION BUILD: set SITE="" so they resolve relative (/available-properties).
SITE=""   # in-prototype pages live at /v2/available-properties/ and /v2/building-my-life-in-spain/
LOCS=["Select country / province / state","Ontario","British Columbia","Alberta","Quebec","Other Canadian province","California","New York","Washington","Illinois","Texas","Florida","Other US state"]

def bg(img,cls="",par="0.06"):
    return f'<div class="media {cls}"><div class="media-img" data-par="{par}" style="{SEO.bgv(img)}"></div></div>'

def vbg(mp4,poster,par="0.08",webm=None):
    """Full-bleed background video. Poster doubles as a CSS background so the still
    always shows even when iOS blocks autoplay; the <video> fades in on 'playing'.

    Media recipe. The source is HDR — 10-bit, BT.2020, HLG (arib-std-b67), Dolby Vision
    profile 8. Feeding it straight to ffmpeg gives washed-out, flat colour: this ffmpeg
    build has no zscale/libplacebo, so it cannot tone-map. Do the HDR->SDR conversion with
    macOS avconvert (AVFoundation tone-maps DV/HLG correctly), then grade/cut in ffmpeg.

      1. tone-map + trim (source = Ronda IMG_0486.mov, 1080x1920 HLG, 23.1s):
         avconvert -s IMG_0486.mov -p Preset1920x1080 --start 13.6 --duration 9.0 -o sdr.mov --replace
      2. filter: scale=864:1536 -> vibrance=intensity=0.18,eq=contrast=1.05:saturation=1.06
         -> 1.5s self-crossfade at t=6.0 (head dissolved over tail) = seamless 7.5s loop
      3. mp4:    -c:v libx264 -crf 26 -preset veryslow -profile:v main -level 4.0 \
                 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart
      4. webm:   -c:v libvpx-vp9 -crf 42 -b:v 0 -row-mt 1 -cpu-used 2
      5. poster: -ss 5.8 -i sdr.mov -frames:v 1 -vf "scale=675:1200,<same grade>" -q:v 4
    """
    src = (f'<source src="{webm}" type="video/webm">' if webm else "") + \
          f'<source src="{mp4}" type="video/mp4">'
    return (f'<div class="media vid" style="background:#141d31 url(&#39;{poster}&#39;) 50% 30%/cover">'
            f'<video class="media-img" autoplay muted loop playsinline preload="metadata" '
            f'poster="{poster}">{src}</video></div>')

def rlines(text):  # split a heading into animated lines by <br>
    return "".join(f'<span class="rline"><span>{p}</span></span>' for p in text.split("|"))

pillar_tabs="\n".join(f'<button type="button" class="sw-tab" data-i="{i}" aria-pressed="false"><span class="sw-idx">{i+1:02d}</span><span class="sw-name">{t}</span></button>' for i,(t,_) in enumerate(PILLARS))
PILLAR_IMG=[uimg(x,1400) for x in PILLAR_IDS]
PILLAR_IMG[0]="/media/home-3.webp"; PILLAR_IMG[5]="/media/oliva-4.webp"
pillar_panels="\n".join(
 f'<div class="sw-panel" data-i="{i}" aria-hidden="true"><div class="media-img" style="{SEO.bgv(PILLAR_IMG[i])}"></div>'
 f'<div class="sw-copy"><span class="sw-c-idx">{i+1:02d} / 12</span><h3>{t}</h3><p class="sw-lede">{d}</p></div></div>'
 for i,(t,d) in enumerate(PILLARS))

def place_more(name):
    ps=HX["places_full"].get(name)
    if not ps: return ""
    return '<details class="place-more"><summary>What it gives, what it asks</summary>'+"".join(f"<p>{x}</p>" for x in ps)+'</details>'
places_html="\n".join(
 f'''<article class="place">
   <div class="place-media img-reveal"><div class="media-img" data-par="0.05" style="{SEO.bgv(img)}"></div></div>
   <div class="place-body reveal"><span class="ovl">{tag}</span><h3>{name}</h3><p>{HX["places_short"].get(name,line)}</p><span class="place-price">{price}</span>{place_more(name)}</div>
 </article>''' for tag,name,price,line,img in PLACES)

def rows(rs): return "\n".join(f'<div class="nrow"><span class="nk">{k}</span><span class="nv">{v}</span></div>' for k,v in rs)
SVC_COPY=[tuple(HX["svc"][0]),tuple(HX["svc"][1]),
  ("The Full AfterLife","The Full AfterLife",HX["how"]["fa_line"]),
  ("The Private Client","The Private Client",HX["how"]["pc_line"])]
services_html="\n".join(
 f'''<article class="srow">
   <div class="srow-media img-reveal"><div class="media-img" data-par="0.05" style="{SEO.bgv(SVC_IMGS[i])}"></div></div>
   <div class="srow-body reveal"><span class="ovl">{SVC_COPY[i][0]}</span><h3>{SVC_COPY[i][1]}</h3><p>{SVC_COPY[i][2]}</p><div class="srow-foot">{f'<span class="srow-fee">{fee}</span>' if fee else ''}<a class="srow-link" href="{href}">Explore <span aria-hidden="true">&rarr;</span></a></div></div>
 </article>''' for i,(n,d,fee,href) in enumerate(SERVICES))
steps_html="\n".join(f'<div class="step reveal"><span class="step-n">{n}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for n,t,d in STEPS)
def _o(i,o): return '<option'+(' value=""' if i==0 else '')+'>'+o+'</option>'
locopts="\n".join(_o(i,o) for i,o in enumerate(LOCS))
hero_stats="".join(f'<div class="hstat"><span class="hstat-n">{n}</span><span class="hstat-l">{l}</span></div>' for n,l in HX["hero_stats"])
calc_stats="".join(f'<div class="cstat reveal"><span class="cstat-n">{n}</span><span class="cstat-l">{l}</span></div>' for n,l in HX["calc"]["stats"])
calc_paras="".join(f"<p>{x}</p>" for x in HX["calc"]["paras"])
D_=HX["decision"]
traits="".join(f'<li class="reveal"><span class="tick" aria-hidden="true">&check;</span>{t}</li>' for t in D_["traits"])
J_=HX["journal"]; J_HREF=J_["href"].split('href="')[1].rstrip('"')
C_=HX["contact"]
clist="".join(f'<li><span class="cl-n">{i+1:02d}</span><span>{x}</span></li>' for i,x in enumerate(C_["list"]))
NUM=json.dumps({"ca":{"intro":LEAVE["ca"][0],"rows":LEAVE["ca"][1]},"us":{"intro":LEAVE["us"][0],"rows":LEAVE["us"][1]}},ensure_ascii=False)

CSS=r"""
/* --- production-parity blocks --- */
html,body{overflow-x:clip}
.lm-consent input,.news-consent input{margin-right:.5rem;vertical-align:-2px}
.hstats{display:flex;gap:clamp(1.4rem,4vw,3.5rem);margin-top:clamp(2.2rem,6vh,3.4rem);flex-wrap:wrap}
.hstat{display:flex;flex-direction:column;gap:.3rem}
.hstat-n{font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.4rem);font-weight:340}
.hstat-l{font-size:.68rem;text-transform:uppercase;letter-spacing:.14em;color:var(--on-dark);max-width:18ch}
.calc-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(2rem,6vw,6rem);align-items:start}
.calc-copy h2{margin:1.2rem 0 1.6rem;max-width:14ch}
.calc-paras p{color:var(--stone);max-width:52ch;margin-bottom:1rem}
.calc-stats{display:grid;grid-template-columns:1fr 1fr;gap:0}
.cstat{padding:1.6rem 1.2rem 1.6rem 0;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:.5rem}
.cstat-n{font-family:var(--serif);font-size:clamp(2rem,3.6vw,3rem);font-weight:320;line-height:1}
.cstat-l{font-size:.86rem;color:var(--stone);max-width:24ch}
.place-more{margin-top:1.4rem;max-width:52ch}
.place-more summary{cursor:pointer;font-size:.7rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;list-style:none;display:inline-flex;gap:.5rem;align-items:center;min-height:44px}
.place-more summary::-webkit-details-marker{display:none}
.place-more summary::after{content:"+";font-size:1rem}
.place-more[open] summary::after{content:"\2212"}
.place-more p{color:var(--stone);font-size:.95rem;margin-top:.9rem}
.places-intro{color:var(--stone);max-width:52ch;margin-bottom:1rem}
.decision .lead{color:var(--stone);max-width:52ch}
.traits{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:0 clamp(1.5rem,4vw,4rem);margin:clamp(2rem,5vh,3rem) 0}
.traits li{display:flex;gap:1rem;padding:1.2rem 0;border-top:1px solid var(--line);font-family:var(--serif);font-size:clamp(1.05rem,1.5vw,1.3rem);line-height:1.4}
.tick{font-family:var(--sans);font-size:.9rem;color:var(--ink-soft);padding-top:.2rem}
.dec-ctas{display:flex;gap:1rem;flex-wrap:wrap}
.btn-ink,.btn-line{display:inline-flex;align-items:center;min-height:44px;padding:.9rem 1.7rem;border-radius:100px;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;border:1px solid var(--ink)}
.btn-ink{background:var(--ink);color:var(--cream)}
.btn-line{color:var(--ink)}
.srow-fee small{display:block;font-family:var(--sans);font-size:.74rem;color:var(--stone);margin-top:.3rem;letter-spacing:.02em}
.proc-lede{color:var(--on-dark);max-width:48ch;margin:-1rem 0 1.6rem}
.founder-note{margin-top:2rem;font-size:.9rem;color:var(--on-dark-quiet);max-width:60ch;border-top:1px solid var(--line-d);padding-top:1.4rem}
.founder-note strong{color:var(--cream)}
.journal-feat .lead{color:var(--stone);max-width:56ch}
.jfeat{display:block;margin-top:clamp(2rem,5vh,3rem);padding:clamp(1.6rem,3vw,2.6rem);border:1px solid var(--line);transition:background .5s var(--ease)}
.jfeat:hover{background:var(--tint)}
.jmeta{font-size:.66rem;text-transform:uppercase;letter-spacing:.2em;font-weight:600;color:var(--ink-soft)}
.jfeat h3{margin:.8rem 0;max-width:28ch}
.jfeat p{color:var(--stone);max-width:60ch;margin-bottom:1.2rem}
.jall{display:inline-block;margin-top:1.4rem;font-size:.72rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;min-height:44px}
.ccopy{margin-top:1.6rem}
.ccopy .lead{color:var(--stone);max-width:40ch;margin-bottom:.8rem}
.clist{list-style:none;margin-top:1.4rem}
.clist li{display:grid;grid-template-columns:2.4rem 1fr;gap:.6rem;padding:.9rem 0;border-top:1px solid var(--line);font-size:.95rem;color:var(--stone)}
.cl-n{font-family:var(--serif);color:var(--ink)}
.box-h{margin-bottom:.4rem}
.box-p{color:var(--stone);font-size:.9rem;margin-bottom:1.6rem}
@media(max-width:900px){.calc-grid,.traits{grid-template-columns:1fr}}

:root{--cream:#F3F3EC;--ink:#17233B;--stone:#5C5648;--ink-soft:rgba(23,35,59,.6);--cream-soft:rgba(243,243,236,.66);
--line:rgba(23,35,59,.15);--line-d:rgba(243,243,236,.18);
--on-dark:rgba(243,243,236,.84);--on-dark-quiet:rgba(243,243,236,.66);--tint:var(--tint);--tint-line:var(--tint-line);
--serif:"Fraunces",Georgia,serif;--sans:"Archivo",Arial,sans-serif;--script:"Ephesis",cursive;
--ease:cubic-bezier(.16,1,.3,1);--pad:clamp(1.25rem,5vw,6rem)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);background:var(--cream);color:var(--ink);line-height:1.7;overflow-x:clip;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--serif);font-weight:340;letter-spacing:-.02em;line-height:1.02}
h1{font-size:clamp(3rem,9vw,7rem)} h2{font-size:clamp(2.2rem,5.5vw,4.2rem);line-height:1.05}
h3{font-size:clamp(1.4rem,2.6vw,2.2rem);letter-spacing:-.015em}
p{max-width:58ch} a{color:inherit;text-decoration:none}
.ovl{font-family:var(--sans);font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:.24em;color:var(--ink-soft)}
.script{font-family:var(--script)}
section{position:relative}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:2px}
.dark :focus-visible,.nav :focus-visible,.menu :focus-visible,.chapter :focus-visible,.hero :focus-visible{outline-color:var(--cream)}
.gform input:focus-visible,.gform button:focus-visible{outline-color:var(--cream)}
.skip{position:absolute;left:-9999px;top:0;z-index:100;background:var(--ink);color:var(--cream);padding:.8rem 1.2rem;font-size:.75rem;letter-spacing:.14em;text-transform:uppercase}
.skip:focus{left:0}
.pad{padding:clamp(5rem,13vh,11rem) var(--pad)} .wrap{max-width:1440px;margin:0 auto}
.dark{background:var(--ink);color:var(--cream)} .dark .ovl{color:var(--cream-soft)} .dark p{color:var(--cream-soft)}
.rline{display:block;overflow:hidden} .rline>span{display:block}
.js .rline>span{transform:translateY(110%);transition:transform 1s var(--ease)}
.in .rline>span,.rline.in>span{transform:none}
.js .reveal{opacity:0;transform:translateY(24px);filter:blur(6px);transition:opacity 1s var(--ease),transform 1s var(--ease),filter 1s var(--ease)}
.reveal.in{opacity:1;transform:none;filter:none}
@media(prefers-reduced-motion:reduce){.js .reveal,.js .rline>span{opacity:1!important;transform:none!important;filter:none!important;transition:none}}

/* media + reveals */
.media,.place-media,.srow-media,.guide-media,.contact-media{position:relative;overflow:hidden}
.hero .media,.chapter .media{position:absolute;inset:0}
.media-img{position:absolute;inset:-8% 0;background-size:cover;background-position:center;will-change:transform;background-image:var(--bg)}
video.media-img{width:100%;height:100%;object-fit:cover}
.chapter video.media-img{inset:0;object-position:50% 30%;opacity:0;transition:opacity .9s var(--ease)}
.chapter video.media-img.on{opacity:1}
.js .img-reveal .media-img{clip-path:inset(0 0 100% 0);transition:clip-path 1.3s var(--ease)}
.img-reveal.in .media-img{clip-path:inset(0 0 0 0)}

/* nav */
.nav{position:fixed;top:0;left:0;right:0;z-index:60;display:flex;justify-content:space-between;align-items:center;
padding:1.15rem var(--pad);color:#fff;text-shadow:0 1px 14px rgba(11,17,30,.55)}
.nav::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
background:linear-gradient(180deg,rgba(11,17,30,.62) 0%,rgba(11,17,30,.34) 55%,transparent 100%)}
.brand{font-family:var(--serif);font-size:1.15rem;display:inline-flex;align-items:center;min-height:44px} .brand b{font-weight:400}
.nav-links{display:flex;gap:clamp(1rem,2.2vw,2rem);align-items:center}
.nav-links a{font-size:.7rem;text-transform:uppercase;letter-spacing:.18em;font-weight:500;opacity:.9}
.nav-links a:hover{opacity:.5}
.nav-cta{display:inline-flex;align-items:center;min-height:44px;border:1px solid rgba(255,255,255,.5);padding:.5rem 1.05rem;border-radius:100px}
.burger{display:none;flex-direction:column;justify-content:center;align-items:center;gap:5px;background:none;border:0;cursor:pointer;min-width:44px;min-height:44px;margin-right:-.5rem}
.burger span{width:26px;height:1.5px;background:#fff}
.menu{position:fixed;inset:0;z-index:55;background:var(--ink);color:var(--cream);display:flex;flex-direction:column;
justify-content:center;padding:var(--pad);clip-path:inset(0 0 100% 0);transition:clip-path .8s var(--ease);pointer-events:none}
.menu.open{clip-path:inset(0 0 0 0);pointer-events:auto}
.menu a{font-family:var(--serif);font-size:clamp(2rem,9vw,3.4rem);padding:.3rem 0}
.menu-sig{font-family:var(--script);font-size:2rem;margin-top:2rem;opacity:.7}

/* hero */
.hero{height:100svh;min-height:600px;position:relative;overflow:hidden;display:flex;align-items:center;color:var(--cream)}
.hero .media-img{inset:-6% 0}
.hero .media::after{content:"";position:absolute;inset:0;background:linear-gradient(105deg,rgba(23,35,59,.72) 0%,rgba(23,35,59,.42) 45%,rgba(23,35,59,.2) 100%)}
.hero-in{position:relative;z-index:2;width:100%;max-width:1440px;margin:0 auto;padding:0 var(--pad)}
.hero h1{max-width:14ch} .hero h1 em{font-style:italic;font-weight:300}
.hero-lede{margin-top:1rem;max-width:52ch;font-size:.95rem;color:var(--on-dark)}
.hero-sub{margin-top:1.4rem;font-size:clamp(1.05rem,1.5vw,1.3rem);color:rgba(243,243,236,.9);max-width:34ch}
.hero-cta{margin-top:2.2rem;display:inline-flex;gap:.6rem;align-items:center;background:var(--cream);color:var(--ink);
padding:1rem 1.9rem;border-radius:100px;font-size:.74rem;text-transform:uppercase;letter-spacing:.16em;font-weight:600;
transition:background .5s,color .5s;border:1px solid var(--cream)}
.hero-cta:hover{background:transparent;color:var(--cream)}
.scroll-cue{position:absolute;left:50%;bottom:2rem;transform:translateX(-50%);z-index:2;color:var(--cream-soft);
font-size:.62rem;letter-spacing:.24em;text-transform:uppercase;display:flex;flex-direction:column;align-items:center;gap:.6rem}
.scroll-cue::after{content:"";width:1px;height:38px;background:linear-gradient(var(--cream),transparent);animation:cue 2s var(--ease) infinite}
@keyframes cue{0%{opacity:0;transform:scaleY(0);transform-origin:top}40%{opacity:1;transform:scaleY(1)}100%{opacity:0;transform:scaleY(1);transform-origin:bottom}}

/* full-bleed chapter */
.chapter{height:100svh;min-height:540px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;color:var(--cream);text-align:center}
.chapter .media-img{inset:-12% 0}
.chapter::after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(23,35,59,.5) 0%,rgba(23,35,59,.7) 100%);z-index:1}
.chapter h2{position:relative;z-index:2;max-width:16ch;padding:0 var(--pad);font-weight:360;font-size:clamp(2.9rem,7.5vw,6rem);line-height:1.02;text-shadow:0 4px 44px rgba(0,0,0,.5)}

/* section intro */
.head{margin-bottom:clamp(2.5rem,6vh,4.5rem)}
.head h2{max-width:16ch}
.head .ovl{display:block;margin-bottom:1.2rem}

/* pillar switcher */
.switch-track{height:calc(12 * 40vh + 100vh)}
.switch-sticky{position:sticky;top:0;height:100svh;display:grid;grid-template-columns:38% 1fr;overflow:hidden}
.sw-list{align-self:center;padding:0 var(--pad);display:flex;flex-direction:column;gap:.05rem}
.sw-deck{display:block;margin-top:.8rem;font-family:var(--serif);font-size:1rem;letter-spacing:0;text-transform:none;color:var(--cream)}
.sw-head{margin-bottom:clamp(1.4rem,3vh,2.2rem)}
.sw-mhead{display:none}
.sw-title{font-family:var(--serif);font-weight:360;font-size:clamp(1.5rem,2.2vw,2.3rem);line-height:1.1;letter-spacing:-.02em;color:var(--cream);max-width:18ch}
.sw-deck{margin-top:.7rem;font-size:.92rem;line-height:1.6;color:var(--cream-soft);max-width:34ch}
.sw-tab{background:none;border:0;text-align:left;cursor:pointer;display:flex;gap:1rem;align-items:baseline;padding:.42rem 0;
color:var(--cream);opacity:.38;transition:opacity .5s var(--ease);font-family:var(--serif);min-height:44px;display:flex;align-items:center}
.sw-tab .sw-idx{font-family:var(--sans);font-size:.68rem;color:var(--cream-soft)}
.sw-tab .sw-name{font-size:clamp(1.2rem,2.1vw,1.9rem);transition:transform .5s var(--ease)}
.sw-tab.active{opacity:1}.sw-tab.active .sw-name{transform:translateX(12px)}
.sw-stage{position:relative;background:#111a2c}
.sw-panel{position:absolute;inset:0;opacity:0;transition:opacity .8s var(--ease)}
.sw-panel.active{opacity:1}
.sw-panel .media-img{inset:0;transition:transform 1.2s var(--ease)}
.sw-panel.active .media-img{transform:scale(1.05)}
.sw-panel::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(17,26,44,.9))}
.sw-copy{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:clamp(1.5rem,4vw,3.5rem);color:var(--cream);background:linear-gradient(180deg,transparent 0%,rgba(13,20,36,.55) 45%,rgba(13,20,36,.88) 100%)}
.sw-c-idx{font-size:.66rem;letter-spacing:.2em;color:var(--cream-soft)}
.sw-copy h3{font-size:clamp(2rem,3.6vw,3.2rem);margin:.5rem 0 .5rem} .sw-copy p{color:var(--on-dark)}

.region-line{max-width:70ch;color:var(--stone);margin-bottom:clamp(2rem,5vh,3rem)}
.sw-lede{font-family:var(--serif);font-size:clamp(1.05rem,1.7vw,1.35rem);line-height:1.4;color:var(--cream);max-width:46ch}
.sw-full{margin-top:1rem;max-height:min(30vh,15rem);overflow-y:auto;padding-right:1rem;scrollbar-width:thin;scrollbar-color:rgba(243,243,236,.35) transparent;-webkit-mask-image:linear-gradient(180deg,#000 78%,transparent 100%);mask-image:linear-gradient(180deg,#000 78%,transparent 100%)}
.sw-full::-webkit-scrollbar{width:3px}
.sw-full::-webkit-scrollbar-thumb{background:rgba(243,243,236,.35);border-radius:3px}
.sw-full:focus-visible{outline:2px solid var(--cream);outline-offset:4px}
.sw-full p{font-size:.92rem;line-height:1.7;color:var(--on-dark);max-width:54ch}
.sw-full p+p{margin-top:.7rem}
.gform .consent{display:flex;align-items:flex-start;gap:.65rem;flex:1 0 100%;margin-top:1rem;padding:.5rem 0;font-size:.78rem;line-height:1.6;color:var(--cream-soft);cursor:pointer;max-width:52ch}
.gform .consent>span{flex:1 1 auto;min-width:0}
.gform .consent input[type=checkbox]{flex:0 0 auto;width:18px;height:18px;min-width:0;margin:.15rem 0 0;accent-color:var(--cream);cursor:pointer}
.consent a{text-decoration:underline}
/* numbers */
.toggle{display:inline-grid;grid-template-columns:1fr 1fr;position:relative;border:1px solid var(--line-d);border-radius:100px;padding:4px;background:rgba(243,243,236,.04)}
.toggle button{position:relative;z-index:1;background:none;border:0;cursor:pointer;min-height:44px;font-family:var(--sans);font-size:.7rem;
text-transform:uppercase;letter-spacing:.16em;font-weight:600;color:var(--cream-soft);padding:.65rem 1.4rem;border-radius:100px;transition:color .5s}
.toggle button.on{color:var(--ink)} .toggle .knob{position:absolute;top:4px;bottom:4px;left:4px;width:calc(50% - 4px);background:var(--cream);border-radius:100px;transition:transform .55s var(--ease)}
.toggle.us .knob{transform:translateX(100%)}
.nhead{display:grid;grid-template-columns:1fr;gap:clamp(2rem,5vh,3.4rem);margin-bottom:clamp(3rem,8vh,5.5rem)}
#numbers .head{margin-bottom:0}
.nside{display:flex;flex-direction:column;align-items:flex-start}
.n-intro{font-family:var(--serif);font-weight:340;font-size:clamp(1.4rem,2.8vw,2.3rem);line-height:1.28;max-width:none;margin:1.4rem 0 0;min-height:2.6em}
.ncol-h{font-size:clamp(1.3rem,2vw,1.7rem);margin:-.4rem 0 1.2rem}
.ncols{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,5vw,5rem)}
.ncol .ovl{display:block;margin-bottom:1.4rem}
.nrow{display:grid;grid-template-columns:100px 1fr;gap:1rem;padding:1.15rem 0;border-top:1px solid var(--line-d);align-items:baseline}
.nk{font-size:.68rem;text-transform:uppercase;letter-spacing:.14em;color:var(--cream-soft)}
.nv{font-family:var(--serif);font-size:clamp(1.05rem,1.6vw,1.35rem);line-height:1.4;color:var(--cream)}
.ncol.leave .nv{color:var(--on-dark-quiet)}

/* places */
.place{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4.5rem);align-items:center;padding:clamp(2.5rem,6vh,5rem) 0;border-top:1px solid var(--line)}
.place:first-of-type{border-top:0}
.place:nth-child(even) .place-media{order:2}
.place-media{aspect-ratio:4/3}
.place-body h3{margin:.6rem 0 .9rem} .place-body p{color:var(--stone);max-width:34ch}
.place-price{font-family:var(--serif);font-size:1.2rem;margin-top:1.4rem;display:inline-block;padding-bottom:.3rem;border-bottom:1px solid var(--line)}

/* services — alternating image rows */
.srow{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,4.5rem);align-items:center;padding:clamp(2.5rem,6vh,5rem) 0;border-top:1px solid var(--line)}
.srow:first-of-type{border-top:0}
.srow:nth-child(even) .srow-media{order:2}
.srow-media{aspect-ratio:4/3}
.srow-body h3{font-size:clamp(1.9rem,3.4vw,3rem);margin:.7rem 0 1rem}
.srow-body p{color:var(--stone);max-width:40ch}
.srow-foot{display:flex;gap:1.6rem;align-items:center;margin-top:1.5rem;flex-wrap:wrap}
.srow-fee{font-size:.7rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;color:var(--ink-soft)}
.srow-link{display:inline-flex;gap:.5rem;align-items:center;min-height:44px;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;border-bottom:1px solid var(--line);padding-bottom:.3rem;transition:gap .4s var(--ease)}
.srow-link:hover{gap:1rem}
/* process — full-bleed split: image + steps */
.process{display:grid;grid-template-columns:1fr 1fr;min-height:100svh}
.process-media{position:relative;overflow:hidden}.process-media .media-img{inset:0}
.process-body{padding:clamp(3rem,8vh,7rem) var(--pad);display:flex;flex-direction:column;justify-content:center}
.process-body .head{margin-bottom:clamp(2rem,5vh,3.5rem)}
.process .step:first-child{border-top:0}
.contact-media{aspect-ratio:3/4}

/* steps */
.steps{display:grid;gap:0} .step{display:grid;grid-template-columns:auto 1fr;gap:clamp(1.2rem,4vw,3rem);padding:1.6rem 0;border-top:1px solid var(--line-d);align-items:baseline}
.step-n{font-family:var(--serif);font-size:clamp(1.4rem,2.6vw,2rem);color:var(--cream-soft)} .step p{color:var(--on-dark-quiet)}

/* guide + contact */
.guide{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(1.5rem,5vw,5rem);align-items:center}
.guide-media{aspect-ratio:4/5}
.guide-body h2{margin-bottom:1rem} .guide-body p{color:var(--on-dark)}
.gform{margin-top:1.8rem;display:flex;gap:.8rem;flex-wrap:wrap;max-width:480px}
.gform input{flex:1;min-width:200px;min-height:44px;background:transparent;border:0;border-bottom:1px solid var(--line-d);color:var(--cream);padding:.85rem .2rem;font-family:var(--sans);font-size:1rem}
.gform input::placeholder{color:var(--cream-soft)} .gform input:focus{outline:none;border-color:var(--cream)}
.gbtn{background:var(--cream);color:var(--ink);border:0;border-radius:100px;padding:.9rem 1.7rem;min-height:44px;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;cursor:pointer}
.micro{font-size:.76rem;color:var(--cream-soft);margin-top:1rem}
.contact{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(2rem,5vw,5rem);align-items:start}
.contact h2{margin-bottom:1.2rem} .contact .lead{color:var(--stone);max-width:32ch}
.cform{display:grid;gap:1.3rem}.frow{display:grid;grid-template-columns:1fr 1fr;gap:1.3rem}
.field{display:flex;flex-direction:column;gap:.5rem}
.field label{font-size:.66rem;text-transform:uppercase;letter-spacing:.16em;color:var(--ink-soft);font-weight:600}
.field input,.field select,.field textarea{background:transparent;border:0;border-bottom:1px solid var(--line);padding:.7rem 0;min-height:44px;font-family:var(--sans);font-size:1rem;color:var(--ink);border-radius:0}
.field textarea{resize:vertical;min-height:80px} .field input:focus,.field select:focus,.field textarea:focus{outline:none;border-color:var(--ink)}
.cbtn{justify-self:start;background:var(--ink);color:var(--cream);border:0;border-radius:100px;padding:1rem 1.9rem;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;font-weight:600;cursor:pointer}

/* footer + badge */
.foot{padding:clamp(3rem,7vh,6rem) var(--pad) 2.5rem;background:var(--ink);color:var(--cream)}
.foot-top{display:flex;justify-content:space-between;gap:2rem;flex-wrap:wrap;padding-bottom:2.5rem;border-bottom:1px solid var(--line-d)}
.foot-sig{font-family:var(--script);font-size:clamp(2rem,5vw,3.2rem)}
.foot-nav{display:flex;gap:1.5rem;flex-wrap:wrap} .foot-nav a{font-size:.7rem;text-transform:uppercase;letter-spacing:.16em;color:var(--cream-soft)}
.foot-bot{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:1.6rem;font-size:.7rem;color:var(--cream-soft)}
#badge{position:fixed;left:1rem;bottom:1rem;z-index:90;background:#B4643C;color:#fff;font-size:.6rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;padding:.5rem .8rem;border-radius:4px}

@media(max-width:1080px){.nav-links{display:none}.burger{display:flex}}
@media(max-width:900px){.media-img{background-image:var(--bg-sm,var(--bg))}}
@media(max-width:900px){
 .switch-sticky{grid-template-columns:1fr;grid-template-rows:auto 1fr}.switch-track{height:calc(12 * 26vh + 100vh)}
 .sw-list{flex-direction:row;overflow-x:auto;gap:1.1rem;padding:1rem var(--pad);background:#111a2c;scrollbar-width:none}
 .sw-list::-webkit-scrollbar{display:none}.sw-head{display:none}
 .switch-sticky{grid-template-rows:auto auto 1fr}
 .sw-mhead{display:block;padding:clamp(1.4rem,4vw,2rem) var(--pad) .2rem;background:#111a2c}.sw-tab{flex:0 0 auto}.sw-tab.active .sw-name{transform:none}
 .ncols,.place,.place:nth-child(even) .place-media,.guide,.contact,.frow,.srow,.process{grid-template-columns:1fr}
 .place:nth-child(even) .place-media{order:0}.srow:nth-child(even) .srow-media{order:0}.process-media{aspect-ratio:4/3;min-height:60vh}
 .nhead{grid-template-columns:1fr;gap:clamp(1.8rem,5vh,2.6rem);align-items:start}
 .ncols{gap:clamp(2.4rem,5vh,3.2rem)}
 .head h2{max-width:none}
 .n-intro{min-height:auto;max-width:34ch;margin-top:1.4rem}
 .toggle{width:100%;max-width:22rem}
}
"""

JS=r"""
const burger=document.querySelector('.burger'),menu=document.getElementById('menu');
burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');document.body.style.overflow=o?'hidden':'';});
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');document.body.style.overflow='';}));
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches,fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
let smooth=fine&&!reduce,target=scrollY,current=scrollY,raf=null;
const maxS=()=>document.documentElement.scrollHeight-innerHeight;
function loop(){current+=(target-current)*.09;if(Math.abs(target-current)<.4)current=target;scrollTo(0,current);tick();if(current!==target)raf=requestAnimationFrame(loop);else raf=null;}
const kick=()=>{if(raf===null)raf=requestAnimationFrame(loop);};
if(smooth){
 addEventListener('wheel',e=>{if(e.target.closest('.sw-list,.menu'))return;e.preventDefault();target=Math.max(0,Math.min(maxS(),target+e.deltaY));kick();},{passive:false});
 addEventListener('keydown',e=>{const m={PageDown:innerHeight*.9,PageUp:-innerHeight*.9,ArrowDown:120,ArrowUp:-120,' ':innerHeight*.9,Home:-1e9,End:1e9};if(!(e.key in m))return;if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName))return;e.preventDefault();target=Math.max(0,Math.min(maxS(),e.key==='Home'?0:e.key==='End'?maxS():target+m[e.key]));kick();});
 addEventListener('scroll',()=>{if(raf===null){current=target=scrollY;tick();}},{passive:true});
}else addEventListener('scroll',tick,{passive:true});
const goto=y=>{if(smooth){target=Math.max(0,Math.min(maxS(),y));kick();}else scrollTo({top:y,behavior:'smooth'});};
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const el=document.querySelector(a.getAttribute('href'));if(!el)return;e.preventDefault();goto(el.getBoundingClientRect().top+scrollY);}));
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.reveal,.rline,.img-reveal').forEach(el=>io.observe(el));
const par=[...document.querySelectorAll('[data-par]')];
const track=document.querySelector('.switch-track'),tabs=[...document.querySelectorAll('.sw-tab')],panels=[...document.querySelectorAll('.sw-panel')];
let cur=-1;const setP=i=>{if(i===cur)return;cur=i;tabs.forEach((t,n)=>{const on=n===i;t.classList.toggle('active',on);t.setAttribute('aria-pressed',on?'true':'false');});panels.forEach((p,n)=>{const on=n===i;p.classList.toggle('active',on);p.setAttribute('aria-hidden',on?'false':'true');});};setP(0);
function tick(){const y=scrollY;
 for(const el of par){const r=el.getBoundingClientRect();const s=parseFloat(el.dataset.par);el.style.transform='translate3d(0,'+(-(r.top+r.height/2-innerHeight/2)*s).toFixed(1)+'px,0)';}
 if(track){const r=track.getBoundingClientRect();const tot=track.offsetHeight-innerHeight;const p=Math.min(1,Math.max(0,-r.top/tot));setP(Math.min(tabs.length-1,Math.floor(p*tabs.length)));}}
tabs.forEach((t,i)=>t.addEventListener('click',()=>{const tot=track.offsetHeight-innerHeight;goto(track.getBoundingClientRect().top+scrollY+(i+.5)/tabs.length*tot);}));
tick();addEventListener('resize',tick);
const tg=document.getElementById('tg'),ni=document.getElementById('nintro'),lv=document.getElementById('leave'),D=NUMDATA;
function setC(c){tg.classList.toggle('us',c==='us');tg.querySelectorAll('button').forEach(b=>{const on=b.dataset.c===c;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');});ni.textContent=D[c].intro;lv.innerHTML=D[c].rows.map(r=>`<div class="nrow"><span class="nk">${r[0]}</span><span class="nv">${r[1]}</span></div>`).join('');}
tg.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>setC(b.dataset.c)));setC('ca');
const _vids=[...document.querySelectorAll('video')];
_vids.forEach(v=>v.addEventListener('playing',()=>v.classList.add('on')));
const _play=()=>_vids.forEach(v=>{try{v.muted=true;const p=v.play();if(p)p.catch(()=>{});}catch(e){}});
_play(); document.addEventListener('visibilitychange',()=>{if(!document.hidden)_play();});
['touchstart','pointerdown','click','scroll'].forEach(ev=>addEventListener(ev,_play,{once:true,passive:true}));
"""

HTML=f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.className='js';</script>
{SEO.head("home", jsonld=True)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..460;1,9..144,300..400&family=Archivo:wght@400;500;600&family=Ephesis&display=swap" rel="stylesheet">
{SEO.css_link()}</head><body>
{SEO.badge()}
<a class="skip" href="#main">Skip to content</a>
<nav class="nav"><a class="brand" href="#top"><b>Spanish</b> AfterLife</a>
<div class="nav-links"><a href="#life">The Life</a><a href="#numbers">The Numbers</a><a href="#places">Where</a><a href="#how">How It Works</a><a href="/v2/available-properties/">Properties</a><a href="/v2/building-my-life-in-spain/">Journal</a><a class="nav-cta" href="#contact">Start Here</a></div>
<button class="burger" aria-label="Menu"><span></span><span></span><span></span></button></nav>
<div class="menu" id="menu"><a href="#life">The Life</a><a href="#numbers">The Numbers</a><a href="#places">Where</a><a href="#how">How It Works</a><a href="/v2/available-properties/">Properties</a><a href="/v2/building-my-life-in-spain/">Journal</a><a href="#contact">Start Here</a><div class="menu-sig">Why wait for the AfterLife?</div></div>

<main id="main">
<header class="hero" id="top">
  <!-- OVERLAY ANCHOR: hero media/video layer mounts here -->
  {bg('/media/home-1.webp','','0.04')}
  <div class="hero-in">
    <h1>{rlines('Your best years.|<em>Starting now.</em>')}</h1>
    <p class="hero-sub reveal">Early retirement on Spain's Mediterranean coast.</p>
    <p class="hero-lede reveal">{HX["hero_lede"]}</p>
    <a class="hero-cta reveal" href="#contact">Start here <span aria-hidden="true">&rarr;</span></a>
    <div class="hstats reveal">{hero_stats}</div>
  </div>
  <div class="scroll-cue">Scroll</div>
</header>

<section class="chapter">{vbg('/media/ronda.mp4','/media/ronda-poster.jpg',webm='/media/ronda.webm')}<h2>{rlines('A continent|at your door.')}</h2></section>

<section class="pad calc" id="calc"><div class="wrap calc-grid">
  <div class="calc-copy"><span class="ovl">{HX["calc"]["ovl"]}</span><h2 class="reveal">{HX["calc"]["h2"]}</h2><div class="calc-paras reveal">{calc_paras}</div></div>
  <div class="calc-stats">{calc_stats}</div>
</div></section>

<section class="switch dark" id="life">
  <div class="switch-track"><div class="switch-sticky"><div class="sw-mhead"><h2 class="sw-title">Twelve reasons this is the right move</h2><p class="sw-deck">{HX["life_deck"]}</p></div>
    <div class="sw-list"><div class="sw-head"><h2 class="sw-title">Twelve reasons this is the right move</h2><p class="sw-deck">{HX["life_deck"]}</p></div>{pillar_tabs}</div>
    <div class="sw-stage">{pillar_panels}</div>
  </div></div>
</section>

<section class="chapter">{bg('/media/oliva-3.webp','','0.1')}<h2>{rlines('This is|every day now.')}</h2></section>

<section class="numbers dark pad" id="numbers"><div class="wrap">
  <div class="nhead">
    <div class="head"><span class="ovl">The Numbers</span><h2 class="reveal">What your equity actually buys</h2></div>
    <div class="nside reveal">
      <div class="toggle" id="tg" role="group" aria-label="Compare Spain with"><span class="knob" aria-hidden="true"></span><button type="button" data-c="ca" aria-pressed="true">Canada</button><button type="button" data-c="us" aria-pressed="false">United States</button></div>
      <p class="n-intro" id="nintro"></p>
    </div>
  </div>
  <div class="ncols">
    <div class="ncol reveal"><span class="ovl">What's waiting — Spain</span><h3 class="ncol-h">{HX["num_h3"][0]}</h3>{rows(WAIT)}</div>
    <div class="ncol leave reveal"><span class="ovl">What you're leaving</span><h3 class="ncol-h">{HX["num_h3"][1]}</h3><div id="leave"></div></div>
  </div>
</div></section>

<section class="places pad" id="places"><div class="wrap">
  <div class="head"><span class="ovl">Where We Work</span><h2 class="reveal">The Valencia Community</h2></div>
  <p class="lead places-intro reveal">{HX["places_intro"]}</p>
  <p class="region-line reveal">{REGION_LINE}</p>
  {places_html}
</div></section>

<section class="pad decision" id="decision"><div class="wrap">
  <div class="head"><span class="ovl">{D_["ovl"]}</span><h2 class="reveal">{D_["h2"]}</h2></div>
  <p class="lead reveal">{D_["deck"]}</p>
  <ul class="traits">{traits}</ul>
  <div class="dec-ctas reveal"><a class="btn-ink" href="{D_["ctas"][0][0]}">{D_["ctas"][0][1]}</a><a class="btn-line" href="#contact">{D_["ctas"][1][1]}</a></div>
</div></section>

<section class="chapter">{bg('/media/oliva-5.webp','','0.1')}<h2>{rlines('Why wait for|the AfterLife?')}</h2></section>

<section class="services pad" id="how"><div class="wrap">
  <div class="head"><span class="ovl">What we do</span><h2 class="reveal">The firm that makes<br>the move happen</h2></div>
  {services_html}
</div></section>

<section class="process dark" id="process">
  <div class="process-media img-reveal"><div class="media-img" data-par="0.06" style="{SEO.bgv('/hero.webp')}"></div></div>
  <div class="process-body">
    <div class="head"><span class="ovl">How We Work</span><h2 class="reveal">{HX["how"]["h2"]}</h2></div>
    <p class="proc-lede reveal">{HX["how"]["lede"]}</p>
    <div class="steps">{steps_html}</div>
    <p class="founder-note reveal"><strong>Why we built this.</strong> {HX["how"]["founder"]}</p>
  </div>
</section>

<section class="pad journal-feat" id="journal"><div class="wrap">
  <div class="head"><span class="ovl">{J_["ovl"]}</span><h2 class="reveal">{J_["h2"]}</h2></div>
  <p class="lead reveal">{J_["deck"]}</p>
  <a class="jfeat reveal" href="{J_HREF}"><span class="jmeta">{J_["cat"]} &middot; {J_["date"]}</span><h3>{J_["h3"]}</h3><p>{J_["p"]}</p><span class="srow-link">Read the piece <span aria-hidden="true">&rarr;</span></span></a>
  <a class="jall reveal" href="/v2/building-my-life-in-spain/">All journal entries &rarr;</a>
</div></section>

<section class="dark pad" id="guide"><div class="wrap guide">
  <div class="guide-media img-reveal"><div class="media-img" data-par="0.05" style="{SEO.bgv('/guide-cover.webp')}"></div></div>
  <div class="guide-body reveal">
    <span class="ovl">{HX["guide"]["ovl"]}</span>
    <h2>{HX["guide"]["h2"]}</h2>
    <p>{HX["guide"]["p"]}</p>
    <form class="gform" id="gform" action="/api/subscribe" method="post">
      <input type="email" name="EMAIL" placeholder="Your email address" required aria-label="Email address">
      <button class="gbtn" type="submit">Send me the guide</button>
      <label class="consent"><input type="checkbox" name="consent" required><span>Email me the guide and the occasional honest update. I accept the <a href="/privacy">Privacy Policy</a> and can unsubscribe anytime.</span></label>
      <div aria-hidden="true" style="position:absolute;left:-5000px"><input type="text" name="website" tabindex="-1" autocomplete="off" value=""></div>
      <input type="hidden" name="intent" value="guide">
      <input type="hidden" name="source" value="index:guide-form">
    </form>
    <p class="micro">{HX["guide"]["note"]}</p>
  </div>
</div></section>

<section class="pad" id="contact"><div class="wrap">
  <div class="head"><span class="ovl">Start Here</span><h2 class="reveal">Find out if Spain is right for you.</h2></div>
  <div class="contact">
  <div class="reveal"><div class="contact-media img-reveal"><div class="media-img" data-par="0.05" style="{SEO.bgv('/media/valencia-3.webp')}"></div></div>
  <div class="ccopy">{"".join(f'<p class="lead">{x}</p>' for x in C_["paras"])}<ol class="clist">{clist}</ol></div></div>
  <div><h3 class="box-h">{C_["box_h3"]}</h3><p class="box-p">{C_["box_p"]}</p>
  {SEO.contact_form()}</div>
</div></section>

</main>
{SEO.footer("home")}

<script>const NUMDATA={NUM};</script><script>{JS}</script>
</body></html>"""
if __name__=="__main__":
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    open(OUT,"w",encoding="utf-8").write(HTML)
    print("wrote",OUT,f"({len(HTML)//1024} KB)")
