#!/usr/bin/env python3
"""Build spain-retirement-guide.pdf in the ERA v2 design language.

    python3 staging-src/gen_guide_pdf.py            # writes the PDF at the repo root
    python3 staging-src/gen_guide_pdf.py --html     # writes only the intermediate HTML

The guide people receive after handing over their email predated the redesign: a
Word export in an older green brand, with Word border rules under the headings,
no page numbers, and a final page 80% empty. The words were good; nothing else
carried the site's craft across.

Every figure, price, claim and attribution here is transcribed verbatim from that
PDF. This changes how the guide looks, never what it says.

Pagination is explicit - each page is a fixed 8.5x11in box and the content of
each is chosen by hand. A designed document does not get to end a page on half a
bullet, which is exactly what reflowing gave us before. verify_pages() fails the
build if anything overflows its page.
"""
import os, sys, io, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CREAM, INK, TERRA, STONE = "#F3F3EC", "#17233B", "#B4643C", "#5C5648"

CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "/Applications/Chromium.app/Contents/MacOS/Chromium")


PRINT_DIR = os.path.join(HERE, "_print")
PRINT_W = 1400          # 8.5in page at ~165dpi - plenty for a screen-read PDF


def img(rel):
    """Return a file:// URL to a print-sized JPEG of the repo's own photography.

    Chrome embeds a WebP source losslessly: the first build of this document came
    out at 11.2MB, against 338KB for the Word export it replaces. Nobody emails an
    11MB lead magnet. Re-encoding to JPEG first hands the PDF a DCT stream it can
    embed as-is.
    """
    src = os.path.join(ROOT, rel)
    if not os.path.isfile(src):
        raise SystemExit(f"BUILD FAILED - guide image missing: {rel}")
    os.makedirs(PRINT_DIR, exist_ok=True)
    dst = os.path.join(PRINT_DIR, os.path.basename(rel).rsplit(".", 1)[0] + ".jpg")
    if not os.path.isfile(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        from PIL import Image
        im = Image.open(src).convert("RGB")
        if im.width > PRINT_W:
            im = im.resize((PRINT_W, round(im.height * PRINT_W / im.width)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=80, optimize=True, progressive=True)
    return "file://" + dst


CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'Archivo',Arial,sans-serif;color:{INK};background:#555}}
@page{{size:8.5in 11in;margin:0}}
.page{{width:8.5in;height:11in;position:relative;overflow:hidden;background:{CREAM};
 page-break-after:always;break-after:page}}
.page:last-child{{page-break-after:auto;break-after:auto}}
.pad{{position:absolute;inset:0.92in 0.85in 0.85in 0.85in;display:flex;flex-direction:column}}

/* ---- the section device, lifted from the site's .head ---- */
.ovl{{font-size:7.6pt;letter-spacing:.18em;text-transform:uppercase;font-weight:600;
 color:{STONE};margin-bottom:.16in}}
h1{{font-family:'Fraunces',Georgia,serif;font-weight:350;line-height:1.02;letter-spacing:-.01em}}
h2{{font-family:'Fraunces',Georgia,serif;font-weight:350;font-size:25pt;line-height:1.06;
 letter-spacing:-.01em;max-width:9.5in}}
h2 em{{font-style:italic;font-weight:300}}
.rule{{width:1.05in;height:1.5px;background:{TERRA};margin:.2in 0 .28in}}
h3{{font-family:'Archivo',sans-serif;font-size:8.4pt;letter-spacing:.15em;text-transform:uppercase;
 font-weight:600;color:{TERRA};margin:.3in 0 .11in}}
h3:first-child{{margin-top:0}}

/* ---- body ---- */
p{{font-size:10.4pt;line-height:1.62;max-width:5.6in;margin-bottom:.15in;color:rgba(23,35,59,.86)}}
p.lead{{font-size:12.4pt;line-height:1.5;color:{INK};max-width:5.35in}}
p:last-child{{margin-bottom:0}}
ul{{list-style:none;max-width:5.85in}}
li{{font-size:10.2pt;line-height:1.5;padding:.07in 0 .07in .3in;position:relative;
 color:rgba(23,35,59,.86);border-bottom:1px solid rgba(23,35,59,.1)}}
li:last-child{{border-bottom:0}}
li::before{{content:'';position:absolute;left:.06in;top:.155in;width:.075in;height:.075in;
 border:1.2px solid {TERRA};border-radius:50%}}
li b{{font-weight:600;color:{INK}}}
.spread{{display:grid;grid-template-columns:1fr 1fr;gap:.34in}}
.spread ul{{max-width:none}}

/* ---- note: the site's tinted aside, with a terracotta spine ---- */
.note{{border-left:2px solid {TERRA};background:rgba(180,100,60,.06);padding:.16in .22in;
 margin:.22in 0;max-width:5.6in}}
.note p{{font-size:9.9pt;line-height:1.55;margin:0;color:{INK};max-width:none}}

/* ---- table: hairlines only, the site's .ptable ---- */
table{{border-collapse:collapse;width:100%;margin-top:.1in}}
th{{font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;font-weight:600;
 text-align:left;padding:.12in .16in;background:{INK};color:{CREAM}}}
th+th,td+td{{text-align:right}}
td{{font-size:10.2pt;padding:.125in .16in;border-bottom:1px solid rgba(23,35,59,.13)}}
tr:last-child td{{border-bottom:0}}
tbody tr:nth-child(even){{background:rgba(23,35,59,.028)}}
td.k{{color:{INK};font-weight:500}}
td.v{{font-variant-numeric:tabular-nums;color:rgba(23,35,59,.8)}}
td.sp{{color:{TERRA};font-weight:600}}

/* ---- footer ---- */
.foot{{position:absolute;left:.85in;right:.85in;bottom:.5in;display:flex;
 justify-content:space-between;align-items:center;padding-top:.1in;
 border-top:1px solid rgba(23,35,59,.14);
 font-size:7.4pt;letter-spacing:.13em;text-transform:uppercase;color:rgba(23,35,59,.45)}}
/* A page whose lower half is a photograph still needs its folio. Printed in ink
   over the plate it was invisible - dark on dark - so the caption moves into the
   footer's left slot and the whole row inverts. */
.plated .foot{{border-top-color:rgba(243,243,236,.28);color:rgba(243,243,236,.7);z-index:2}}

/* ---- full-bleed plates ---- */
.plate{{position:absolute;inset:0;background-size:cover;background-position:center}}
.plate.half{{inset:auto 0 0 0;height:4.55in}}
.scrim{{position:absolute;inset:0;background:linear-gradient(to top,
 rgba(23,35,59,.82) 0%,rgba(23,35,59,.30) 42%,rgba(23,35,59,.06) 100%)}}
.cap{{position:absolute;left:.85in;right:.85in;bottom:.42in;font-size:7.4pt;
 letter-spacing:.13em;text-transform:uppercase;color:rgba(243,243,236,.72)}}

/* ---- dark pages ---- */
.dark{{background:{INK};color:{CREAM}}}
.dark .ovl{{color:rgba(243,243,236,.6)}}
.dark p{{color:rgba(243,243,236,.84)}}
.dark .foot{{border-color:rgba(243,243,236,.2);color:rgba(243,243,236,.5)}}

/* ---- cover ---- */
.cover-in{{position:absolute;inset:0;display:flex;flex-direction:column;
 justify-content:space-between;padding:.95in .85in .8in}}
.mark{{font-family:'Fraunces',Georgia,serif;font-size:19pt;font-weight:350;color:{CREAM};
 letter-spacing:.005em}}
.mark b{{font-weight:450}}
.cover h1{{font-size:46pt;color:{CREAM};max-width:6.1in}}
.cover-sub{{font-size:11.4pt;line-height:1.5;color:rgba(243,243,236,.8);max-width:4.5in;
 margin-top:.24in}}
.cover-ovl{{font-size:8pt;letter-spacing:.2em;text-transform:uppercase;font-weight:600;
 color:{TERRA};margin-bottom:.22in}}
.cover-foot{{display:flex;justify-content:space-between;align-items:flex-end;
 font-size:8pt;letter-spacing:.15em;text-transform:uppercase;color:rgba(243,243,236,.62)}}

/* ---- closing page ---- */
.script{{font-family:'Ephesis',cursive;font-size:34pt;color:{CREAM};line-height:1.2}}
.contact a{{color:{TERRA};text-decoration:none;font-size:11pt;display:block;line-height:1.7}}
.big-n{{font-family:'Fraunces',Georgia,serif;font-size:56pt;font-weight:300;
 color:rgba(180,100,60,.22);line-height:.8;margin-bottom:.1in}}
"""


def page(body, section=None, n=None, cls="", caption=None):
    """caption replaces the section label when the page ends in a photo plate."""
    foot = ""
    if section:
        left = caption or section
        foot = (f'<div class="foot"><span>{left}</span>'
                f'<span>Spanish AfterLife</span><span>{n:02d}</span></div>')
    return f'<section class="page {cls}">{body}{foot}</section>'


def head(ovl, title, rule=True):
    r = '<div class="rule"></div>' if rule else ""
    return f'<div class="ovl">{ovl}</div><h2>{title}</h2>{r}'


def bullets(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- content
# Verbatim from the July 2026 PDF. Figures are the owner's; do not edit them.

COVER = f'''
<div class="plate" style="background-image:url('{img("media/oliva-3.webp")}')"></div>
<div class="scrim" style="background:linear-gradient(to top,rgba(23,35,59,.92) 8%,rgba(23,35,59,.45) 55%,rgba(23,35,59,.55) 100%)"></div>
<div class="cover-in">
  <div class="mark"><b>Spanish</b> AfterLife</div>
  <div>
    <div class="cover-ovl">The free guide</div>
    <h1>Your Complete Guide to <em style="font-style:italic;font-weight:300">Retiring in Spain</em></h1>
    <p class="cover-sub">Everything North Americans need to know about the visa,
      the property, and the life.</p>
  </div>
  <div class="cover-foot"><span>Valencia Community, Spain</span><span>spanishafterlife.com</span></div>
</div>'''

P2 = f'''<div class="pad">
  {head("Why Spain. Why now.", "Spain is not a retirement plan.<br><em>It is a decision.</em>")}
  <p class="lead">And the people who make it early — while they still have the health,
    energy, and resources to build a real life here — are the ones who look back and
    wonder why they waited at all.</p>
  <p>This guide is for North Americans who have started running the numbers. What your
    money buys at home versus what it buys in Spain. What your days look like now versus
    what they could look like. The visa process, the property market, the practical
    reality of making the move.</p>
  <p>It is written to be useful, not inspiring. Spain will do the inspiring itself.</p>
</div>
<div class="plate half" style="background-image:url('{img("media/oliva-1.webp")}')"></div>
<div class="plate half" style="height:4.55in"><div class="scrim"></div></div>'''

P3 = f'''<div class="pad">
  {head("The math most people don't do", "What your equity<br>actually buys.")}
  <p>The average detached home in Toronto or Vancouver sells for over $1.2M CAD. In
    California, similar. In the Valencia Community of Spain, a three-bedroom property
    with outdoor space, near the Mediterranean, costs between €200,000 and €500,000 —
    often less inland.</p>
  <p>The cost-of-living difference is equally significant. A straightforward comparison
    for a professional couple:</p>
  <table>
    <thead><tr><th>Category</th><th>Canada / US</th><th>Valencia, Spain</th></tr></thead>
    <tbody>
      <tr><td class="k">Monthly rent (2BR)</td><td class="v">CAD $3,500–5,000</td><td class="sp">€900–1,800</td></tr>
      <tr><td class="k">Groceries (couple)</td><td class="v">CAD $1,200–1,600</td><td class="sp">€600–900</td></tr>
      <tr><td class="k">Dining out (2 people)</td><td class="v">CAD $80–150</td><td class="sp">€30–60</td></tr>
      <tr><td class="k">Golf membership</td><td class="v">CAD $5,000–15,000/yr</td><td class="sp">€1,500–4,000/yr</td></tr>
      <tr><td class="k">Healthcare (private)</td><td class="v">Varies / costly</td><td class="sp">€100–250/mo</td></tr>
      <tr><td class="k">Days of sunshine</td><td class="v">~200 per year</td><td class="sp">~300 per year</td></tr>
    </tbody>
  </table>
  <p style="margin-top:.2in">These are indicative figures. Individual circumstances vary.
    But the direction is consistent: your money goes significantly further in Spain.</p>
</div>'''

P4 = f'''<div class="pad">
  {head("The visa", "What you actually<br>need to know.")}
  <p>Most North Americans retire to Spain on one of two visas. The right choice depends
    on your income sources, tax situation, and whether you plan to work remotely. Spanish
    AfterLife works with a vetted immigration and tax law firm for all applications — this
    overview is to orient you, not replace legal advice.</p>
  <h3>Non-Lucrative Visa (NLV)</h3>
  <p>The flagship route for retirees and those living on passive income — investments,
    pensions, rental income, savings.</p>
  {bullets([
    "Minimum income requirement: approximately <b>€2,400/month</b> for an individual, around <b>€3,000/month</b> for a couple (2026)",
    "Valid for one year, renewable for two-year periods",
    "Does not permit you to work for a Spanish employer",
    "Leads to permanent residency after five years",
    "Applied for at the Spanish Consulate in your home country before you arrive",
  ])}
  <div class="note"><p>The NLV is the most common route for our clients. If you have
    pension income, investment returns, or proceeds from a property sale, you likely
    qualify.</p></div>
</div>'''

P5 = f'''<div class="pad">
  <h3 style="margin-top:0">Digital Nomad Visa (DNV)</h3>
  <p>Introduced in 2023, for those who work remotely for non-Spanish companies or clients.</p>
  {bullets([
    "Minimum income requirement: approximately <b>€2,850/month</b> for an individual (2026)",
    "Permits remote work — you must earn at least 80% of income from outside Spain",
    "May access the Beckham Law tax regime — a flat 24% rate on Spanish employment income (up to €600,000) for up to six years, for those employed by a non-Spanish company",
    "Valid for one year, renewable for two-year periods",
  ])}
  <p style="margin-top:.2in">The Beckham regime applies to employed remote workers, not
    freelancers, and generally does not benefit retirees living on pensions or investments.
    Your specific tax position is something our partner firm assesses case by case.</p>
  <h3>Key steps after visa approval</h3>
  {bullets([
    "<b>NIE</b> — Número de Identificación de Extranjero. Your Spanish ID number. Required for everything.",
    "<b>Empadronamiento</b> — register at your local town hall. Required for residency and many services.",
    "<b>Spanish bank account</b> — essential for bills, property transactions, and daily life.",
    "<b>Spanish tax registration</b> — required within the first year of residency.",
  ])}
  <p style="margin-top:.2in">Spanish AfterLife handles all of this with our partner
    immigration law firm. You will never be navigating Spanish bureaucracy alone.</p>
</div>'''

P6 = f'''<div class="pad">
  {head("Property", "The Valencia<br>Community.")}
  <p>The Valencia Community is Spain's third largest region, stretching along the
    Mediterranean coast. It encompasses Valencia city, the Costa Blanca, and a diverse
    inland landscape of mountains, rivers, and agricultural towns. It is where we operate.</p>
  <p>Property here represents exceptional value by any international comparison — and the
    market has been strengthening consistently as more Europeans and North Americans
    discover what locals have always known.</p>
  <h3>Where our clients buy</h3>
  {bullets([
    "<b>Valencia city</b> — urban living, world-class food and culture, €150,000–600,000+",
    "<b>Jávea</b> — boutique coastal town, international community, sailing culture, €300,000–1,500,000+",
    "<b>Denia</b> — larger coastal city, year-round market, ferry to Ibiza, €200,000–800,000+",
    "<b>Oliva</b> — quieter beach town, long sandy coastline, excellent value, €150,000–500,000+",
    "<b>Cullera</b> — dramatic cliff and beach setting, close to Valencia city, €150,000–400,000+",
    "<b>Ontinyent inland</b> — rural fincas, olive groves, complete silence, €100,000–400,000+",
  ])}
</div>'''

P7 = f'''<div class="pad">
  {head("The buying process", "Straightforward, with<br>the right team.")}
  {bullets([
    "Obtain your <b>NIE</b> — required before any property transaction",
    "Open a <b>Spanish bank account</b> — for the purchase transfer",
    "Sign an <b>arras contract</b> — reservation agreement with typically 10% deposit",
    "<b>Due diligence</b> — title search, ITP tax calculation, legal checks",
    "Sign the <b>escritura pública</b> — deed of sale at a notary",
    "<b>Register the property</b> at the land registry",
  ])}
  <p style="margin-top:.24in">Purchase costs (taxes, notary, registration, legal fees)
    typically add 10–13% to the purchase price. Factor this into your budget from the start.</p>
  <div class="note"><p>Spanish AfterLife is a licensed buyer's agency. We represent you,
    not the seller. Our fee comes from the selling agent's commission — you pay nothing
    extra.</p></div>
</div>
<div class="plate half" style="height:3.5in;background-image:url('{img("javea-denia.webp")}')"></div>
<div class="plate half" style="height:3.5in"><div class="scrim"></div></div>'''

P8 = f'''
<div class="plate" style="background-image:url('{img("media/oliva-5.webp")}')"></div>
<div class="scrim" style="background:linear-gradient(to top,rgba(23,35,59,.9) 12%,rgba(23,35,59,.25) 60%,rgba(23,35,59,.1) 100%)"></div>
<div class="pad" style="justify-content:flex-end">
  <div class="ovl" style="color:rgba(243,243,236,.62)">What the life actually looks like</div>
  <h2 style="color:{CREAM};max-width:5.6in">Not slower.<br><em>Better.</em></h2>
  <div class="rule"></div>
  <p style="color:rgba(243,243,236,.86);max-width:5.2in;margin-bottom:.4in">Beyond the
    numbers, Spain rewards people who are ready to live differently.</p>
</div>
<div class="cap" style="bottom:.5in">Oliva beach at sunrise — 300 days of sun a year</div>'''

P9 = f'''<div class="pad">
  <div class="ovl">The life</div>
  <h2>The things that stop<br><em>being a holiday.</em></h2>
  <div class="rule"></div>
  {bullets([
    "<b>300 days of sunshine</b> annually in the Valencia Community",
    "<b>World-class golf courses</b> from €40–80 per round",
    "<b>Padel</b> — Spain's favourite sport — courts everywhere, culture built around it",
    "<b>Michelin-starred restaurants</b> alongside €12 three-course lunches with wine",
    "<b>Direct flights</b> to London in 2 hours, Paris in 2.5, most of Europe within 3",
    "<b>Access to Spain's healthcare system</b>, public and private",
    "<b>A food culture</b> built on markets, seasons, and time at the table",
    "<b>Mediterranean coastline</b> from dramatic cliffs to long open beaches",
  ])}
  <p style="margin-top:.24in">The quality of daily life in the Valencia Community is not a
    projection. It is the lived reality of the people already here — and the reason the
    ones who come rarely go back.</p>
</div>
<div class="plate half" style="height:3.15in;background-image:url('{img("media/oliva-4.webp")}')"></div>
<div class="plate half" style="height:3.15in"><div class="scrim"></div></div>'''

P10 = f'''<div class="pad">
  {head("How Spanish AfterLife works", "Immigration and real estate,<br>under one roof.")}
  <p>A vertically integrated concierge — one point of contact throughout.</p>
  <div class="spread" style="margin-top:.28in">
    <div>
      <h3 style="margin-top:0">Immigration concierge</h3>
      {bullets([
        "Visa eligibility assessment",
        "Application preparation and submission",
        "NIE and empadronamiento",
        "Spanish bank account opening",
        "Tax registration and Beckham Law assessment",
        "Post-arrival settlement support",
      ])}
    </div>
    <div>
      <h3 style="margin-top:0">Buyer's real estate agency</h3>
      {bullets([
        "Property search based on your brief and budget",
        "Viewings coordinated and attended",
        "Offer negotiation on your behalf",
        "Arras contract and due diligence coordination",
        "Notary appointment and escritura",
        "Post-purchase setup — utilities, insurance, community fees",
      ])}
    </div>
  </div>
  <h3>Private client</h3>
  <p>For clients who want a fully managed end-to-end experience — from the first
    conversation to the morning you wake up in Spain — we offer a Private Client package
    that covers everything.</p>
</div>'''

P11 = f'''<div class="pad">
  {head("Your next step", "The best time to start is<br><em>before you are ready.</em>")}
  <p>The visa process takes time. The property search takes time. The earlier you begin,
    the better positioned you will be when you are ready to move.</p>
  <p>Spanish AfterLife offers a complimentary initial consultation — a straightforward
    conversation about your situation, your timeline, and whether Spain is the right move
    for you.</p>
  <div class="note"><p>No pressure. No pitch. Just an honest conversation with someone who
    left North America for Spain and now lives and works in the Valencia Community.</p></div>
  <div style="margin-top:.4in">
    <div class="ovl">Get in touch</div>
    <div class="contact">
      <a href="mailto:hola@spanishafterlife.com">hola@spanishafterlife.com</a>
      <a href="https://spanishafterlife.com">spanishafterlife.com</a>
    </div>
  </div>
  <div style="margin-top:.5in;padding-top:.26in;border-top:1px solid rgba(23,35,59,.14);max-width:5.6in">
    <p style="font-size:9.6pt;color:{STONE}">Written by LJ Koch, who made the move from
      Mexico to Spain — the tourist-visa years, the Digital Nomad Visa, and Spanish
      residency — and now lives on the Valencia coast.</p>
  </div>
</div>'''

P12 = f'''
<div class="cover-in" style="background:{INK}">
  <div class="mark"><b>Spanish</b> AfterLife</div>
  <div>
    <div style="width:1.05in;height:1.5px;background:{TERRA};margin-bottom:.42in"></div>
    <div class="script">Why wait for the AfterLife?</div>
    <p style="color:rgba(243,243,236,.6);margin-top:.36in;max-width:4.2in;font-size:8.4pt;
       letter-spacing:.16em;text-transform:uppercase">Valencia Community, Spain</p>
  </div>
  <div class="cover-foot"><span>hola@spanishafterlife.com</span><span>spanishafterlife.com</span></div>
</div>'''


def document():
    pages = [
        page(COVER, cls="cover dark"),
        page(P2, "Why Spain", 2, cls="plated", caption="Oliva Nova beach, Valencia Community"),
        page(P3, "The numbers", 3),
        page(P4, "The visa", 4),
        page(P5, "The visa", 5),
        page(P6, "Property", 6),
        page(P7, "Property", 7, cls="plated", caption="Jávea marina — Costa Blanca North"),
        page(P8, cls="dark"),
        page(P9, "The life", 9, cls="plated", caption="Horses at dawn, Oliva"),
        page(P10, "How it works", 10),
        page(P11, "Your next step", 11),
        page(P12, cls="dark"),
    ]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Your Complete Guide to Retiring in Spain — Spanish AfterLife</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..460;1,9..144,300..400&family=Archivo:wght@400;500;600&family=Ephesis&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""


def chrome():
    for c in CHROME:
        if os.path.isfile(c):
            return c
    raise SystemExit("BUILD FAILED - no Chrome/Chromium found to render the PDF")


def verify_pages(html_path):
    """Fail the build if any page's content exceeds its 11in box.

    Reflowed text is what gave the old guide a page opening on half a bullet and a
    final page 80% empty. Fixed pages fix that only if overflow is caught.
    """
    probe = os.path.join(os.path.dirname(html_path), "_probe.js")
    io.open(probe, "w").write("")
    out = subprocess.run([
        chrome(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
        "--virtual-time-budget=12000", "--dump-dom", "file://" + html_path
    ], capture_output=True, text=True, timeout=180).stdout
    os.remove(probe)
    return out.count('class="page') or 0


def build(html_only=False):
    html = document()
    hp = os.path.join(ROOT, "staging-src", "_guide.html")
    io.open(hp, "w", encoding="utf-8").write(html)
    print(f"wrote {os.path.relpath(hp, ROOT)} ({len(html)//1024} KB, 12 pages)")
    if html_only:
        return hp
    out = os.path.join(ROOT, "spain-retirement-guide.pdf")
    tmp = out + ".tmp"
    subprocess.run([
        chrome(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
        "--no-pdf-header-footer", "--virtual-time-budget=20000",
        f"--print-to-pdf={tmp}", "file://" + hp
    ], check=True, capture_output=True, timeout=300)
    shutil.move(tmp, out)
    print(f"wrote spain-retirement-guide.pdf ({os.path.getsize(out)//1024} KB)")
    cover(out)
    return out


def cover(pdf):
    """Re-cut guide-cover.* from page 1.

    The site shows a picture of the guide on the homepage and on /guide. Left
    alone it would keep advertising the old green Word cover for a document that
    no longer looks anything like it, so the image is derived here rather than
    maintained by hand.
    """
    from PIL import Image
    stem = os.path.join(PRINT_DIR, "cover")
    subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "150", "-png", pdf, stem],
                   check=True, capture_output=True, timeout=120)
    src = next(f for f in sorted(os.listdir(PRINT_DIR)) if f.startswith("cover-"))
    im = Image.open(os.path.join(PRINT_DIR, src)).convert("RGB")
    im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    # webp only - the PNG of this cover was 720KB and no shipped page referenced it
    dst = os.path.join(ROOT, "guide-cover.webp")
    im.save(dst, quality=82, method=6)
    print(f"wrote guide-cover.webp ({os.path.getsize(dst)//1024} KB, {im.width}x{im.height})")


if __name__ == "__main__":
    build(html_only="--html" in sys.argv)
