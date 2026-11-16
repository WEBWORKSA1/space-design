#!/usr/bin/env python3
"""Space.Design static site generator. Run: python3 src/build.py  (outputs to repo root)."""
import os, json, datetime, html
from guides import GUIDES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://space.design"
NAME = "Space.Design"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
TODAY = datetime.date.today().isoformat()
PAGES = []

NAV = [("tools.html", "Tools"), ("planner.html", "Room Planner"), ("quiz.html", "Style Quiz"), ("styles.html", "Styles"),
       ("guides/index.html", "Guides"), ("videos.html", "Videos"), ("news.html", "News"), ("contests.html", "Contests")]


def layout(path, title, desc, body, js=(), schema=None, noindex=False):
    depth = path.count("/")
    b = "../" * depth
    cur = path
    cur_attr = ' aria-current="page"'
    nav = "".join(f'<li><a href="{b}{h}"{cur_attr if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    nav += f'<li class="mobile-only"><a href="{b}get-quote.html">Get Free Quotes</a></li>'
    canon = SITE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    full_title = title if title.startswith(NAME) else f"{title} | {NAME}"
    sch = ""
    base_schema = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/",
                   "potentialAction": {"@type": "SearchAction", "target": SITE + "/guides/?q={search_term_string}", "query-input": "required name=search_term_string"}}
    for s in ([base_schema] if path == "index.html" else []) + ([schema] if schema else []):
        sch += f'<script type="application/ld+json">{json.dumps(s)}</script>'
    scripts = "".join(f'<script src="{b}assets/js/{j}" defer></script>' for j in js)
    if not noindex:
        PAGES.append(path)
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
{robots}
<meta name="theme-color" content="#18181B">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(full_title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{b}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/css/style.css">
<link rel="manifest" href="{b}manifest.webmanifest">
{ADS}
{sch}
<script>try{{var t=localStorage.getItem('sd-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
</head>
<body data-base="{b}">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="https://web.works/contact" target="_blank" rel="noopener"><strong>Contact</strong>, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership →</a></div>
<header class="site-header"><div class="wrap nav">
<a class="logo" href="{b}index.html" aria-label="{NAME} home"><span class="logo-mark" aria-hidden="true"></span><span class="wordmark">Space<b>.</b>Design</span></a>
<nav aria-label="Main"><ul class="menu" id="menu">{nav}</ul></nav>
<div class="nav-actions"><a class="btn btn-accent btn-sm" href="{b}get-quote.html">Get Free Quotes</a>
<button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode">🌓</button>
<button class="icon-btn burger" data-burger aria-label="Open menu" aria-controls="menu" aria-expanded="false">☰</button></div>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="{b}index.html"><span class="logo-mark" aria-hidden="true"></span><span class="wordmark">Space<b>.</b>Design</span></a>
<p class="mt">Free tools, honest guides and vetted professionals to plan, measure and design any space — from a studio corner to a whole home.</p>
<p><a href="https://web.works/contact" target="_blank" rel="noopener">Sponsorship, advertising, partnership or domain inquiry →</a></p></div>
<div><h4>Plan</h4><ul><li><a href="{b}tools.html">All calculators</a></li><li><a href="{b}planner.html">2D room planner</a></li><li><a href="{b}tools.html#palette">Colour palettes</a></li><li><a href="{b}quiz.html">Style quiz</a></li></ul></div>
<div><h4>Learn</h4><ul><li><a href="{b}guides/index.html">Guides</a></li><li><a href="{b}styles.html">Design styles</a></li><li><a href="{b}videos.html">Video library</a></li><li><a href="{b}news.html">Design news</a></li></ul></div>
<div><h4>Get involved</h4><ul><li><a href="{b}get-quote.html">Get matched with a pro</a></li><li><a href="{b}pros.html">Join as a professional</a></li><li><a href="{b}contests.html">Design contests</a></li><li><a href="{b}careers.html">Careers</a></li><li><a href="{b}donate.html">Support us</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{b}about.html">About</a></li><li><a href="{b}advertise.html">Advertise</a></li><li><a href="{b}contact.html">Contact</a></li><li><a href="{b}privacy.html">Privacy</a></li><li><a href="{b}terms.html">Terms</a></li><li><a href="{b}disclaimer.html">Disclaimer &amp; trademarks</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>{datetime.date.today().year}</span> {NAME}. All rights reserved. Independent website — not affiliated with any company named “Space Design”. <a href="{b}disclaimer.html">Trademark notice</a>.</span><span>Ads by Google · <a href="{b}privacy.html#cookies">Cookie settings</a></span></div>
</div></footer>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie notice"><strong>We value your privacy.</strong> We use cookies to run this site and, with Google AdSense, to show and measure ads. See our <a href="{b}privacy.html">Privacy Policy</a>.
<div class="btns"><button class="btn btn-sm" data-consent="all">Accept all</button><button class="btn btn-sm btn-ghost" data-consent="essential">Essential only</button></div></div>
<script src="{b}assets/js/main.js" defer></script>{scripts}
</body></html>"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def hp():  # honeypot
    return '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'


def unit_radio(name, a="ft", b="m"):
    return f'<div class="chip-row" style="margin:0 0 6px"><label class="check"><input type="radio" name="{name}-unit" value="{a}" checked> {a}</label><label class="check"><input type="radio" name="{name}-unit" value="{b}"> {b}</label></div>'


def field(id_, label, val, step="0.1"):
    return f'<div><label for="{id_}">{label}</label><input id="{id_}" type="number" min="0" step="{step}" value="{val}" inputmode="decimal"></div>'


# ---------------------------------------------------------------- Lead form (reused)
PROJECTS = [("living", "🛋️", "Living room"), ("kitchen", "🍳", "Kitchen"), ("bathroom", "🛁", "Bathroom"), ("bedroom", "🛏️", "Bedroom"),
            ("office", "💻", "Home office"), ("small-space", "📐", "Small space"), ("full-home", "🏠", "Whole home"), ("commercial", "🏢", "Office / retail"),
            ("outdoor", "🌿", "Outdoor"), ("lighting", "💡", "Lighting"), ("flooring", "🪵", "Flooring"), ("painting", "🎨", "Painting")]


def lead_form(compact=False):
    choices = "".join(f'<label class="choice"><input type="radio" name="project" value="{v}" required><span><em>{e}</em>{t}</span></label>' for v, e, t in PROJECTS)
    return f"""<form class="form" data-form="Lead — Get Matched" data-success="You're in! A matching specialist will email you within 1 business day with next steps and designer options.">
{hp()}
<div class="steps"><span class="on"></span><span></span><span></span><span></span></div>
<div class="step active"><h3>1. What space are you designing?</h3><div class="choice-grid">{choices}</div>
<div class="step-nav"><span></span><button type="button" class="btn btn-accent" data-step="next">Next →</button></div></div>
<div class="step"><h3>2. Scope & style</h3>
<div class="row"><div><label>Service you need</label><select name="service" required><option value="">Choose…</option><option>Full-service interior designer</option><option>Online e-design (per room)</option><option>Contractor / renovation quote</option><option>Space planning & layout only</option><option>Colour & styling consult</option><option>Not sure — advise me</option></select></div>
<div><label>Approx. size</label><select name="size"><option>Under 150 sq ft / 14 m²</option><option>150–300 sq ft / 14–28 m²</option><option>300–600 sq ft / 28–56 m²</option><option>600–1,500 sq ft / 56–140 m²</option><option>1,500+ sq ft / 140+ m²</option></select></div></div>
<div class="row"><div><label>Style</label><select name="style"><option>Not sure yet</option><option>Japandi</option><option>Modern Minimal</option><option>Mid-Century Modern</option><option>Warm Industrial</option><option>Modern Farmhouse</option><option>Bohemian</option><option>Coastal</option><option>Art Deco Glam</option><option>Traditional</option><option>Scandinavian</option></select></div>
<div><label>Property</label><select name="property"><option>I own it</option><option>I rent it</option><option>Business / commercial</option><option>Investment / short-term rental</option></select></div></div>
<div class="step-nav"><button type="button" class="btn btn-ghost" data-step="back">← Back</button><button type="button" class="btn btn-accent" data-step="next">Next →</button></div></div>
<div class="step"><h3>3. Budget & timing</h3>
<div class="row"><div><label>Budget</label><select name="budget" required><option value="">Choose…</option><option>Under $2,500</option><option>$2,500–$10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$150,000</option><option>$150,000+</option></select></div>
<div><label>When do you want to start?</label><select name="timeline" required><option value="">Choose…</option><option>ASAP</option><option>Within 1 month</option><option>1–3 months</option><option>3–6 months</option><option>Just researching</option></select></div></div>
<div><label>City / region & country</label><input name="location" required placeholder="e.g. Toronto, Canada"></div>
<div class="step-nav"><button type="button" class="btn btn-ghost" data-step="back">← Back</button><button type="button" class="btn btn-accent" data-step="next">Next →</button></div></div>
<div class="step"><h3>4. Where should we send your matches?</h3>
<div class="row"><div><label>Full name</label><input name="name" required autocomplete="name"></div><div><label>Email</label><input type="email" name="email" required autocomplete="email"></div></div>
<div class="row"><div><label>Phone (optional)</label><input type="tel" name="phone" autocomplete="tel"></div><div><label>Best way to reach you</label><select name="contact_pref"><option>Email</option><option>Phone</option><option>WhatsApp</option></select></div></div>
<div><label>Anything else? (optional)</label><textarea name="details" placeholder="Room dimensions, must-keep pieces, links to inspiration…"></textarea></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted about my project and accept the <a href="privacy.html">Privacy Policy</a>. Free, no obligation.</label>
<div class="step-nav"><button type="button" class="btn btn-ghost" data-step="back">← Back</button><button type="submit" class="btn btn-accent">Get my free matches</button></div>
<div class="form-msg" role="status"></div></div>
</form>"""


def guide_cards(limit=None, b=""):
    gs = GUIDES[:limit] if limit else GUIDES
    return "".join(f'<a class="card reveal" href="{b}guides/{g["slug"]}.html"><span class="tag">{g["cat"]} · {g["read"]} min</span><h3>{g["title"]}</h3><p>{g["desc"]}</p></a>' for g in gs)


TOOLS = [("paint", "🎨", "Paint calculator", "Gallons & litres for walls and ceilings."), ("flooring", "🪵", "Flooring calculator", "Area, waste and boxes to buy."),
         ("rug", "🟫", "Rug size finder", "The right rug for every room layout."), ("lighting", "💡", "Lumens calculator", "How much light each room needs."),
         ("budget", "💰", "Renovation budget", "Realistic cost ranges by room."), ("palette", "🌈", "Palette generator", "60-30-10 schemes from any colour."),
         ("clearance", "📏", "Furniture fit check", "Will it fit with walkways clear?"), ("wallpaper", "🧻", "Wallpaper rolls", "Rolls needed incl. pattern repeat."),
         ("art", "🖼️", "Art hanging height", "Exact nail height, gallery standard.")]


def tool_cards(b=""):
    return "".join(f'<a class="card reveal" href="{b}tools.html#{a}"><div class="ico">{i}</div><h3>{t}</h3><p>{d}</p></a>' for a, i, t, d in TOOLS)


BLUEPRINT = """<svg viewBox="0 0 400 400" role="img" aria-label="Illustrated floor plan">
<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="var(--line)" stroke-width="1"/></pattern></defs>
<rect width="400" height="400" fill="url(#g)"/>
<rect x="40" y="40" width="320" height="320" fill="none" stroke="var(--ink)" stroke-width="6"/>
<line x1="220" y1="40" x2="220" y2="200" stroke="var(--ink)" stroke-width="4"/><line x1="220" y1="250" x2="220" y2="360" stroke="var(--ink)" stroke-width="4"/>
<path d="M220 200 A50 50 0 0 1 270 250" fill="none" stroke="var(--muted)" stroke-dasharray="4 4"/>
<rect x="60" y="60" width="140" height="56" rx="8" fill="var(--accent)"/><rect x="85" y="140" width="90" height="50" rx="6" fill="var(--brass)"/>
<rect x="60" y="230" width="140" height="110" rx="4" fill="var(--paper-2)" stroke="var(--line)"/>
<circle cx="130" cy="285" r="34" fill="var(--sage)"/>
<rect x="245" y="60" width="95" height="120" rx="8" fill="var(--sage)" opacity=".85"/><rect x="255" y="70" width="34" height="22" rx="4" fill="var(--paper)"/><rect x="296" y="70" width="34" height="22" rx="4" fill="var(--paper)"/>
<rect x="250" y="290" width="90" height="50" rx="4" fill="var(--blue)"/><circle cx="295" cy="270" r="14" fill="var(--blue)" opacity=".6"/>
<text x="200" y="30" font-size="12" text-anchor="middle" fill="var(--muted)" font-family="Inter">16'-0"</text>
</svg>"""

# ================================================================== HOME
home = f"""
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Plan · Measure · Design</span>
<h1>Design any space with confidence.</h1>
<p class="lead">Free room planner, 9 pro-grade calculators, a 2-minute style quiz and honest guides — plus free matching with vetted interior designers and contractors when you want it done for you.</p>
<div class="hero-cta"><a class="btn btn-accent" href="get-quote.html">Get matched with a designer — free</a><a class="btn btn-ghost" href="planner.html">Open the room planner</a></div>
<div class="stats"><div class="stat"><b>9</b><span>free design tools</span></div><div class="stat"><b>{len(GUIDES)}</b><span>in-depth guides</span></div><div class="stat"><b>Daily</b><span>auto-updated news & videos</span></div></div>
</div>
<div class="blueprint reveal">{BLUEPRINT}</div>
</div></section>

<section class="block" style="padding-top:0"><div class="wrap"><div class="tipbox"><div class="ico">💡</div><div><strong>Designer tip of the day</strong><br><span id="tip-of-day">Leave 36" of clearance for main walkways.</span></div></div></div></section>

<section class="block"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Free tools</span><h2>Measure twice, buy once.</h2></div><p>Every calculator works in feet or metres, runs in your browser and never asks for sign-up.</p></div>
<div class="grid g3">{tool_cards()}</div>
</div></section>

<section class="block"><div class="wrap"><div class="band split">
<div><span class="eyebrow" style="color:var(--brass)">Free matching service</span><h2>Tell us about your space. Get matched with the right pro.</h2>
<p>Designers, decorators, e-designers and renovation contractors — matched to your room, style, budget and city. One short form, no obligation, no spam.</p>
<ul style="line-height:2"><li>✓ Vetted professionals only</li><li>✓ Compare up to 3 proposals</li><li>✓ Online e-design from a few hundred dollars per room, or full service</li><li>✓ 100% free for homeowners</li></ul></div>
<div class="card" style="color:var(--ink)">{lead_form()}</div>
</div></div></section>

<section class="block"><div class="wrap split">
<div class="reveal"><span class="eyebrow">2-minute quiz</span><h2>What's your interior style?</h2><p>Seven visual questions reveal your style, a matching colour palette and the designers who specialise in it.</p><a class="btn" href="quiz.html">Take the style quiz</a></div>
<div class="reveal"><span class="eyebrow">Room planner</span><h2>Drag, drop, rotate — at real scale.</h2><p>Set your room size, add true-to-size furniture and see your walkway space and floor coverage update live. Save and export to PNG.</p><a class="btn" href="planner.html">Plan a room</a></div>
</div></section>

<section class="block"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Guides</span><h2>Learn from the people who measure for a living.</h2></div><a class="btn btn-ghost" href="guides/index.html">All guides</a></div>
<div class="grid g3">{guide_cards(6)}</div>
</div></section>

<section class="block"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Watch</span><h2>Fresh design videos, updated daily.</h2></div><a class="btn btn-ghost" href="videos.html">Video library</a></div>
<div class="grid g3" id="video-feed" data-limit="6"><p class="muted">Loading the latest videos…</p></div>
</div></section>

<section class="block"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Design news</span><h2>What's new in architecture & interiors.</h2></div><span class="muted" id="news-updated"></span></div>
<div class="feed-list" id="news-feed" data-limit="6"><p class="muted">Loading headlines…</p></div>
</div></section>

<section class="block"><div class="wrap grid g3">
<a class="card reveal" href="contests.html"><span class="tag hot">Monthly</span><h3>Small Space Challenge</h3><p>Share your best small-space makeover. Winners get prizes and a featured spotlight.</p></a>
<a class="card reveal" href="pros.html"><span class="tag">For pros</span><h3>Get design clients</h3><p>Designers, architects and contractors: join our network and receive matched project requests.</p></a>
<a class="card reveal" href="donate.html"><span class="tag">Support</span><h3>Keep the tools free</h3><p>Help fund new tools, contests, prizes and the talent who build them.</p></a>
</div></section>

<section class="block"><div class="wrap"><div class="section-head"><h2>Frequently asked questions</h2></div>
<details><summary>Is Space.Design really free?</summary><p>Yes. All tools, guides and the matching service are free for homeowners and renters. We're supported by advertising, sponsors and voluntary donations.</p></details>
<details><summary>How does designer matching work?</summary><p>You describe your space, style, budget and location. We review it and introduce you to professionals who fit. You decide whether to work with anyone — there's no obligation.</p></details>
<details><summary>Do the calculators work in metric?</summary><p>Every calculator has a feet/metres switch.</p></details>
<details><summary>Is my room plan saved?</summary><p>Your plan is stored only in your own browser. Nothing is uploaded unless you export it.</p></details>
</div></section>
"""
FAQ_SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in [
        ("Is Space.Design really free?", "Yes. All tools, guides and the matching service are free for homeowners and renters."),
        ("How does designer matching work?", "You describe your space, style, budget and location and we introduce professionals who fit, with no obligation."),
        ("Do the calculators work in metric?", "Every calculator has a feet/metres switch.")]]}
write("index.html", layout("index.html", "Space.Design — Free Room Planner, Interior Design Tools & Designer Matching",
      "Plan and design any room: free 2D room planner, paint, flooring, rug and lighting calculators, style quiz, expert guides and free matching with vetted interior designers.",
      home, schema=FAQ_SCHEMA))

# ================================================================== TOOLS
tools_body = f"""
<section class="block"><div class="wrap">
<span class="eyebrow">Free calculators</span><h1>Interior design calculators</h1>
<p class="lead muted" style="max-width:65ch">Nine fast, accurate tools for planning paint, floors, rugs, lighting, budgets, colour and furniture fit. Results update as you type.</p>
<div class="tool-nav">{''.join(f'<a href="#{a}">{i} {t}</a>' for a, i, t, d in TOOLS)}</div>
<div class="grid g2">

<div class="tool" id="paint"><h3>🎨 Paint calculator</h3><form id="paint-form" onsubmit="return false">{unit_radio('paint')}
<div class="form"><div class="row">{field('p-l','Room length',14)}{field('p-w','Room width',12)}</div><div class="row">{field('p-h','Wall height',8)}{field('p-coats','Coats',2,'1')}</div>
<div class="row">{field('p-doors','Doors',1,'1')}{field('p-wins','Windows',2,'1')}</div><label class="check"><input type="checkbox" id="p-ceil"> Include ceiling</label></div></form>
<div class="result" id="paint-out"></div></div>

<div class="tool" id="flooring"><h3>🪵 Flooring calculator</h3><form id="floor-form" onsubmit="return false">{unit_radio('floor')}
<div class="form"><div class="row">{field('f-l','Room length',14)}{field('f-w','Room width',12)}</div>
<div class="row"><div><label for="f-waste">Waste allowance</label><select id="f-waste"><option value="5">5% (straight lay, simple room)</option><option value="10" selected>10% (standard)</option><option value="15">15% (diagonal / herringbone)</option></select></div>{field('f-box','Coverage per box',20)}</div>
{field('f-price','Price per unit area (optional)',0,'0.01')}</div></form>
<div class="result" id="floor-out"></div></div>

<div class="tool" id="rug"><h3>🟫 Rug size finder</h3><form id="rug-form" onsubmit="return false">{unit_radio('rug')}
<div class="form"><div class="row">{field('r-l','Room length',14)}{field('r-w','Room width',12)}</div>
<div><label for="r-room">Room</label><select id="r-room"><option value="living">Living room</option><option value="bedroom">Bedroom</option><option value="dining">Dining room</option><option value="entry">Entry / hallway</option></select></div></div></form>
<div class="result" id="rug-out"></div></div>

<div class="tool" id="lighting"><h3>💡 Lumens calculator</h3><form id="light-form" onsubmit="return false">{unit_radio('light')}
<div class="form"><div class="row">{field('l-l','Room length',14)}{field('l-w','Room width',12)}</div>
<div><label for="l-type">Room type</label><select id="l-type"><option value="living">Living room</option><option value="bedroom">Bedroom</option><option value="kitchen">Kitchen</option><option value="dining">Dining</option><option value="bathroom">Bathroom</option><option value="office">Home office</option><option value="hallway">Hallway</option></select></div></div></form>
<div class="result" id="light-out"></div></div>

<div class="tool" id="budget"><h3>💰 Renovation budget estimator</h3><form id="budget-form" onsubmit="return false">{unit_radio('budget')}
<div class="form"><div class="row">{field('b-area','Floor area',120,'1')}<div><label for="b-room">Room</label><select id="b-room"><option value="kitchen">Kitchen</option><option value="bathroom">Bathroom</option><option value="living">Living room</option><option value="bedroom">Bedroom</option><option value="basement">Basement</option><option value="office">Home office</option></select></div></div>
<div class="row"><div><label for="b-level">Finish level</label><select id="b-level"><option value="basic">Basic</option><option value="mid" selected>Mid-range</option><option value="luxury">High-end</option></select></div>
<div><label for="b-region">Cost of living</label><select id="b-region"><option value="0.8">Lower-cost area</option><option value="1" selected>Average</option><option value="1.3">High-cost city</option></select></div></div></div></form>
<div class="result" id="budget-out"></div></div>

<div class="tool" id="palette"><h3>🌈 Colour palette generator</h3><form id="palette-form" onsubmit="return false"><div class="form"><div class="row">
<div><label for="pal-base">Base colour</label><input type="color" id="pal-base" value="#5F7A65" style="height:48px;padding:4px"></div>
<div><label for="pal-mode">Harmony</label><select id="pal-mode"><option value="mono">Monochrome</option><option value="analogous">Analogous</option><option value="complementary">Complementary</option><option value="triadic">Triadic</option></select></div></div>
<button type="button" class="btn btn-sm btn-ghost" id="pal-random">🎲 Surprise me</button></div></form>
<div class="swatches" id="pal-out"></div><p class="muted" style="font-size:.85rem;margin-top:8px">Click a swatch to copy its hex code.</p></div>

<div class="tool" id="clearance"><h3>📏 Furniture fit checker</h3><form id="fit-form" onsubmit="return false">{unit_radio('fit')}
<div class="form"><div class="row">{field('c-rl','Room length',14)}{field('c-rw','Room width',12)}</div><div class="row">{field('c-fl','Furniture length',7)}{field('c-fw','Furniture depth',3)}</div></div></form>
<div class="result" id="fit-out"></div></div>

<div class="tool" id="wallpaper"><h3>🧻 Wallpaper roll calculator</h3><form id="paper-form" onsubmit="return false">{unit_radio('paper')}
<div class="form"><div class="row">{field('w-perim','Wall width to cover',40)}{field('w-h','Wall height',8)}</div>{field('w-rep','Pattern repeat (in / cm)',21,'1')}
<p class="muted" style="font-size:.85rem;margin:0">Assumes a standard roll ≈ 21&quot; × 33 ft (0.53 × 10.05 m).</p></div></form>
<div class="result" id="paper-out"></div></div>

<div class="tool" id="art"><h3>🖼️ Art hanging height</h3><form id="art-form" onsubmit="return false">{unit_radio('art','in','cm')}
<div class="form"><div class="row">{field('a-h','Frame height',24)}{field('a-hook','Hook to top of frame (wire drop)',3)}</div></div></form>
<div class="result" id="art-out"></div></div>

</div>
<div class="ad-wrap"></div>
<div class="band mt center"><h2>Rather have a pro do the maths?</h2><p>Get matched with vetted designers and contractors near you — free.</p><a class="btn btn-accent" href="get-quote.html">Get free quotes</a></div>
</div></section>"""
write("tools.html", layout("tools.html", "Free Interior Design Calculators — Paint, Flooring, Rug, Lighting & Budget",
      "Free interior design calculators: paint, flooring, rug size, lumens, renovation budget, wallpaper, furniture fit, art height and colour palette generator. Feet or metres.",
      tools_body, js=["tools.js"], schema={"@context": "https://schema.org", "@type": "WebApplication", "name": "Space.Design calculators", "applicationCategory": "DesignApplication", "offers": {"@type": "Offer", "price": "0"}}))

# ================================================================== PLANNER
planner = """
<section class="block"><div class="wrap">
<span class="eyebrow">Free tool</span><h1>2D room planner</h1>
<p class="muted" style="max-width:70ch">Set your room size, add true-to-scale furniture, drag to arrange and press <span class="kbd">R</span> to rotate or <span class="kbd">Delete</span> to remove. Your plan saves automatically in this browser.</p>
<div class="form" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr));display:grid;gap:12px;margin:18px 0">
<div><label for="pl-w">Room width (ft)</label><input id="pl-w" type="number" min="4" step="0.5"></div>
<div><label for="pl-l">Room length (ft)</label><input id="pl-l" type="number" min="4" step="0.5"></div>
<div style="display:flex;align-items:end"><label class="check"><input type="checkbox" id="pl-snap" checked> Snap to 6"</label></div></div>
<div class="planner"><div class="palette" id="pl-palette"></div>
<div><canvas id="room" aria-label="Room plan canvas"></canvas>
<div class="result" id="pl-stats"></div>
<div class="hero-cta"><button class="btn btn-sm" id="pl-rot" type="button">↻ Rotate</button><button class="btn btn-sm btn-ghost" id="pl-del" type="button">Delete</button><button class="btn btn-sm btn-ghost" id="pl-clear" type="button">Clear all</button><button class="btn btn-sm btn-accent" id="pl-png" type="button">Download PNG</button></div></div></div>
<div class="grid g3 mt">
<div class="card"><h3>Walkways</h3><p>Keep 36" (3 ft) for main paths and 30" minimum elsewhere. Each grid square is 1 ft.</p></div>
<div class="card"><h3>Footprint</h3><p>Aim to keep furniture under 50–60% of the floor. The live stat turns orange when a room is crowded.</p></div>
<div class="card"><h3>Next step</h3><p>Happy with the layout? <a href="get-quote.html">Send it to a designer</a> for finishes, lighting and a shopping list.</p></div></div>
</div></section>"""
write("planner.html", layout("planner.html", "Free 2D Room Planner — Drag & Drop Furniture at Real Scale",
      "Plan any room online for free: set dimensions, drag true-to-scale furniture, rotate, check walkway space and export your floor plan as an image.", planner, js=["planner.js"]))

# ================================================================== QUIZ
quiz = """<section class="block"><div class="wrap" style="max-width:820px">
<span class="eyebrow">2-minute quiz</span><h1>What's your interior design style?</h1>
<p class="muted">Seven quick questions. Get your style, a palette to match and designers who specialise in it.</p>
<div class="card mt" id="quiz"></div>
<p class="muted mt">Explore all <a href="styles.html">design styles</a> or try the <a href="tools.html#palette">palette generator</a>.</p>
</div></section>"""
write("quiz.html", layout("quiz.html", "Interior Design Style Quiz — Find Your Style in 2 Minutes",
      "Take the free interior design style quiz: discover whether you're Japandi, Mid-Century, Industrial, Boho, Coastal or more, with a matching colour palette.", quiz, js=["quiz.js"]))

# ================================================================== STYLES
STYLES = [
    ("japandi", "Japandi", "A blend of Japanese minimalism and Scandinavian comfort. Low furniture, pale and mid-tone woods, linen, paper and stone. Every object earns its place.", "Light oak, ash, linen, washi paper, ceramic, matte black accents", "Clutter, glossy finishes, loud patterns"),
    ("modern-minimal", "Modern Minimal", "Clean planes, flush storage and a restrained palette. The architecture is the decoration, and negative space is a feature.", "Lacquer, plaster, glass, steel, wool", "Ornate trims, visible cables, too many accessories"),
    ("mid-century-modern", "Mid-Century Modern", "Born in the 1940s–60s: tapered legs, organic curves, teak and walnut, and confident colour like mustard, teal and burnt orange.", "Walnut, teak, moulded plywood, brass, bouclé", "Heavy, skirted furniture"),
    ("industrial", "Warm Industrial", "Loft character — brick, concrete, black steel and reclaimed wood — warmed with leather, rugs and plants.", "Brick, steel, reclaimed timber, leather, Edison bulbs", "Overly cold, all-grey schemes"),
    ("modern-farmhouse", "Modern Farmhouse", "Rustic comfort with modern restraint: white walls, shiplap, oak, matte-black fixtures and practical, family-friendly pieces.", "White oak, shiplap, linen slipcovers, stoneware", "Kitschy signage overload"),
    ("bohemian", "Bohemian", "Collected, layered and personal: global textiles, rattan, vintage finds and abundant greenery.", "Rattan, jute, kilims, macramé, terracotta", "Matching furniture sets"),
    ("coastal", "Coastal", "Light, breezy and relaxed with washed whites, soft blues and sandy textures — no nautical clichés required.", "Linen, rattan, whitewashed wood, seagrass", "Anchors and themed décor everywhere"),
    ("art-deco", "Art Deco Glam", "1920s-inspired drama: geometric patterns, brass, lacquer, velvet and jewel tones.", "Brass, marble, velvet, lacquer, fluted glass", "Timid scale — Deco needs confidence"),
    ("scandinavian", "Scandinavian", "Bright, functional and cosy (hygge). Pale woods, white walls, soft textiles and simple forms.", "Birch, pine, wool, sheepskin", "Dark, heavy furniture"),
    ("traditional", "Traditional / Classic", "Symmetry, moulding, rich woods and timeless patterns like damask and stripes, updated with lighter palettes.", "Mahogany, silk, damask, crystal", "Mixing too many eras at once"),
]
styles_body = '<section class="block"><div class="wrap"><span class="eyebrow">Style library</span><h1>Interior design styles explained</h1><p class="muted" style="max-width:70ch">Definitions, signature materials and the mistakes to avoid for ten popular styles. Not sure which is yours? <a href="quiz.html">Take the quiz</a>.</p><div class="grid g2 mt">'
for slug, n, d, m, avoid in STYLES:
    styles_body += f'<article class="card reveal" id="{slug}" style="scroll-margin-top:90px"><h2 style="font-size:1.6rem">{n}</h2><p>{d}</p><p><strong>Signature materials:</strong> {m}</p><p><strong>Avoid:</strong> {avoid}</p><a class="btn btn-sm btn-ghost" href="get-quote.html?style={html.escape(n)}">Find a {n} designer</a></article>'
styles_body += '</div></div></section>'
write("styles.html", layout("styles.html", "Interior Design Styles Explained — Japandi, Mid-Century, Industrial & More",
      "A clear guide to 10 interior design styles with signature materials and mistakes to avoid: Japandi, Minimal, Mid-Century, Industrial, Farmhouse, Boho, Coastal, Deco.", styles_body))

# ================================================================== GUIDES
gindex = f"""<section class="block"><div class="wrap"><span class="eyebrow">Guides</span><h1>Interior design & renovation guides</h1>
<p class="muted" style="max-width:70ch">Practical, measurement-first advice written to help you plan better and spend smarter.</p>
<input id="gsearch" type="search" placeholder="Search guides…" style="max-width:420px;margin:16px 0 24px" aria-label="Search guides">
<div class="grid g3" id="glist">{guide_cards(b="../")}</div></div></section>
<script>(function(){{var q=document.getElementById('gsearch'),cards=[].slice.call(document.querySelectorAll('#glist .card'));
var p=new URLSearchParams(location.search).get('q');if(p)q.value=p;function f(){{var v=q.value.toLowerCase();cards.forEach(function(c){{c.style.display=c.textContent.toLowerCase().indexOf(v)>-1?'':'none';}});}}q.addEventListener('input',f);f();}})();</script>"""
write("guides/index.html", layout("guides/index.html", "Interior Design & Renovation Guides",
      "Expert interior design guides: small living room layouts, kitchen remodel costs, hiring a designer, home offices, bathrooms, lighting, colour and storage.", gindex))
for i, g in enumerate(GUIDES):
    nxt = GUIDES[(i + 1) % len(GUIDES)]
    related = "".join(f'<a class="card" href="{x["slug"]}.html"><span class="tag">{x["cat"]}</span><h3 style="font-size:1.05rem">{x["title"]}</h3></a>' for x in [y for y in GUIDES if y is not g][:3])
    body = f"""<div class="wrap"><div class="article"><nav class="breadcrumb"><a href="../index.html">Home</a> › <a href="index.html">Guides</a> › {g['cat']}</nav>
<span class="tag">{g['cat']}</span><h1 style="font-size:clamp(2rem,4vw,3rem)">{g['title']}</h1>
<p class="meta">By the Space.Design editorial team · {g['read']} min read · Updated {TODAY}</p>
<p class="lead" style="font-size:1.15rem;color:var(--ink-2)">{g['desc']}</p>
{g['body']}
<div class="ad-wrap"></div>
<div class="band mt"><h2 style="font-size:1.6rem">Get a pro's eyes on your project</h2><p>Free matching with vetted designers and contractors. No obligation.</p><a class="btn btn-accent" href="../get-quote.html?project={g['project']}">Get free quotes</a></div>
<h2 class="mt">Keep reading</h2><div class="grid g3">{related}</div>
<p class="mt">Next: <a href="{nxt['slug']}.html">{nxt['title']} →</a></p>
</div></div>"""
    sch = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "dateModified": TODAY, "datePublished": "2026-11-16",
           "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME}, "mainEntityOfPage": f"{SITE}/guides/{g['slug']}.html"}
    write(f"guides/{g['slug']}.html", layout(f"guides/{g['slug']}.html", g["title"], g["desc"], body, schema=sch))

# ================================================================== VIDEOS & NEWS
videos = """<section class="block"><div class="wrap"><span class="eyebrow">Video library</span><h1>Interior design videos</h1>
<p class="muted" style="max-width:70ch">Home tours, small-space ideas, renovation how-tos and design inspiration from leading channels — refreshed automatically every day. Videos are embedded with YouTube's official player; all rights remain with their creators.</p>
<div class="chip-row" id="video-chips"></div>
<div class="grid g3" id="video-feed" data-limit="60"><p class="muted">Loading the latest videos…</p></div>
<div class="ad-wrap"></div></div></section>"""
write("videos.html", layout("videos.html", "Interior Design Videos — Home Tours, Small Spaces & Renovation",
      "Watch the latest interior design videos: home tours, small apartment ideas, renovation how-tos and architecture, updated daily.", videos))
news = """<section class="block"><div class="wrap"><span class="eyebrow">Design news</span><h1>Architecture & interior design news</h1>
<p class="muted">Headlines from respected design publications, refreshed automatically several times a day. Each link opens the original publisher. <span id="news-updated"></span></p>
<div class="feed-list mt" id="news-feed" data-limit="60"><p class="muted">Loading headlines…</p></div><div class="ad-wrap"></div></div></section>"""
write("news.html", layout("news.html", "Architecture & Interior Design News — Updated Daily",
      "The latest architecture, interior design and product design headlines from leading publications, updated automatically.", news))

# ================================================================== GET QUOTE (lead gen)
quote = f"""<section class="block"><div class="wrap split">
<div><span class="eyebrow">Free · No obligation</span><h1>Get matched with the right designer or contractor.</h1>
<p class="lead muted">Answer four quick steps. We'll introduce you to vetted professionals who fit your space, style, budget and location.</p>
<div class="grid" style="gap:14px;margin-top:24px">
<div class="card"><h3>1 · Describe your space</h3><p>Room, size, style and budget — about 60 seconds.</p></div>
<div class="card"><h3>2 · We match you</h3><p>We shortlist professionals who specialise in projects like yours.</p></div>
<div class="card"><h3>3 · Compare & choose</h3><p>Review proposals, portfolios and fees. Hire only if you want to.</p></div></div>
<div class="trust"><span>🔒 Your details are never sold</span><span>✓ Free for homeowners</span><span>⏱ Reply within 1 business day</span></div></div>
<div class="card" style="position:sticky;top:90px">{lead_form()}</div></div></section>
<section class="block"><div class="wrap"><h2>What can you get help with?</h2><div class="grid g4">
{''.join(f'<a class="card" href="get-quote.html?project={v}"><div class="ico">{e}</div><h3 style="font-size:1.05rem">{t}</h3></a>' for v, e, t in PROJECTS)}</div></div></section>"""
write("get-quote.html", layout("get-quote.html", "Get Free Interior Design & Renovation Quotes — Matched to You",
      "Get matched free with vetted interior designers, e-designers and renovation contractors for your room, style, budget and city. No obligation.", quote))

# ================================================================== PROS
pros = f"""<section class="block"><div class="wrap split">
<div><span class="eyebrow">For professionals</span><h1>Get matched with clients who are ready to design.</h1>
<p class="lead muted">Interior designers, decorators, architects, contractors, carpenters, lighting and landscape pros — join the Space.Design network.</p>
<ul style="line-height:2"><li>✓ Pre-qualified project requests by room, budget and location</li><li>✓ Featured profile and portfolio spotlight</li><li>✓ Guest articles and video features to build authority</li><li>✓ Contest judging and sponsorship opportunities</li></ul></div>
<div class="card"><form class="form" data-form="Pro Network Application" data-success="Thanks! We'll review your portfolio and reply within 3 business days.">{hp()}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Business name</label><input name="business"></div></div>
<div class="row"><div><label>Email</label><input type="email" name="email" required></div><div><label>Phone</label><input type="tel" name="phone"></div></div>
<div class="row"><div><label>Profession</label><select name="profession" required><option value="">Choose…</option><option>Interior designer</option><option>Interior decorator</option><option>E-designer</option><option>Architect</option><option>General contractor</option><option>Kitchen & bath specialist</option><option>Carpenter / millwork</option><option>Lighting designer</option><option>Landscape designer</option><option>Home stager</option><option>Other</option></select></div>
<div><label>Service area</label><input name="area" required placeholder="City, region, country / online"></div></div>
<div class="row"><div><label>Website / portfolio</label><input type="url" name="portfolio" placeholder="https://"></div><div><label>Typical project budget</label><select name="typical_budget"><option>Under $10k</option><option>$10k–$50k</option><option>$50k–$150k</option><option>$150k+</option></select></div></div>
<div><label>About your work</label><textarea name="about" required></textarea></div>
<label class="check"><input type="checkbox" required> I confirm I'm licensed/insured where required and agree to the <a href="terms.html">Terms</a>.</label>
<button class="btn btn-accent" type="submit">Apply to join</button><div class="form-msg" role="status"></div></form></div></div></section>"""
write("pros.html", layout("pros.html", "Join the Designer & Contractor Network — Get Matched Clients",
      "Interior designers, architects and contractors: join the Space.Design network to receive matched, pre-qualified project requests.", pros))

# ================================================================== CONTESTS
contests = f"""<section class="block"><div class="wrap">
<span class="eyebrow">Contests & prizes</span><h1>The Small Space Challenge</h1>
<p class="lead muted" style="max-width:70ch">Every month we celebrate the smartest, most beautiful small-space makeovers. Enter your room, get featured and win prizes.</p>
<div class="grid g3 mt">
<div class="card"><span class="tag hot">Now open</span><h3>Contest: <span id="contest-month"></span></h3><p>Closes in <strong id="countdown">—</strong></p></div>
<div class="card"><h3>🏆 Prizes</h3><p><strong>Grand prize:</strong> cash or gift-card prize + homepage feature.<br><strong>Runner-up:</strong> 1-hour e-design consult.<br><strong>Community pick:</strong> featured article + badge. Current prize values are confirmed in each month's announcement.</p></div>
<div class="card"><h3>🧑‍⚖️ Judging</h3><p>Function (40%), creativity (30%), budget smartness (20%), photography & story (10%). Judged by our editors and guest designers.</p></div></div>

<div class="split mt"><div class="card"><h2>Enter now</h2>
<form class="form" data-form="Contest Entry" data-success="Entry received! We'll confirm eligibility by email.">{hp()}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Room type</label><select name="room"><option>Studio</option><option>Living room</option><option>Bedroom</option><option>Kitchen</option><option>Bathroom</option><option>Home office</option><option>Balcony / outdoor</option></select></div><div><label>Size</label><input name="size" placeholder="e.g. 180 sq ft"></div></div>
<div><label>Link to photos (Google Drive, Dropbox, Instagram…)</label><input type="url" name="photos" required placeholder="https://"></div>
<div><label>Your story & budget</label><textarea name="story" required placeholder="What you changed, what it cost, what you learned."></textarea></div>
<label class="check"><input type="checkbox" required> I own the photos and the rights to them, I'm 18+ and I accept the official rules below.</label>
<button class="btn btn-accent" type="submit">Submit entry</button><div class="form-msg" role="status"></div></form></div>
<div><div class="card"><h2>Sponsor a contest</h2><p>Put your brand in front of an engaged design audience. Sponsors fund prizes and get logo placement, social mentions and a dedicated winners' article.</p><a class="btn" href="advertise.html#sponsor">Sponsorship options</a></div>
<div class="card mt"><h3>Upcoming themes</h3><ul><li>Rental-friendly makeovers</li><li>Home offices under 50 sq ft</li><li>Tiny kitchens</li><li>Kids' rooms that grow up</li><li>Balcony gardens</li></ul></div></div></div>

<h2 class="mt">Official rules (summary)</h2>
<details><summary>Eligibility</summary><p>Open to individuals aged 18+ where permitted by law. Void where prohibited. Employees of Space.Design and contest sponsors and their immediate families are not eligible.</p></details>
<details><summary>No purchase necessary</summary><p>No purchase or payment is required to enter or win. Donations to Space.Design do not improve your chances.</p></details>
<details><summary>Entries & rights</summary><p>One entry per person per month. You must own the photos. By entering you grant Space.Design a non-exclusive, royalty-free licence to display your entry with credit on this website and its social channels.</p></details>
<details><summary>Winners & prizes</summary><p>Winners are selected by the judging criteria above, notified by email within 14 days of the close, and must respond within 14 days or an alternate is chosen. Prizes are non-transferable; taxes are the winner's responsibility. Where required by law, a skill-testing question may apply.</p></details>
<details><summary>Privacy</summary><p>Entry information is used only to administer the contest, as described in our <a href="privacy.html">Privacy Policy</a>.</p></details>
</div></section>"""
write("contests.html", layout("contests.html", "Small Space Design Challenge — Monthly Contest & Prizes",
      "Enter the monthly Small Space Challenge: share your room makeover, get featured and win prizes. Official rules, judging criteria and sponsorship.", contests))

# ================================================================== DONATE
donate = f"""<section class="block"><div class="wrap">
<div class="center" style="max-width:760px;margin:0 auto"><span class="eyebrow">Support Space.Design</span><h1>Help keep great design tools free.</h1>
<p class="lead muted">Your support funds ongoing operations, new tools, promotion, hiring talented designers and developers, and the prizes for our community contests.</p></div>
<div class="grid g4 mt">
<div class="card tier"><h3>Supporter</h3><div class="price">$5</div><p class="muted">one-time</p><ul><li>Thank-you shout-out</li><li>Supporter newsletter</li></ul><button class="btn btn-ghost btn-sm" data-amount="5">Choose</button></div>
<div class="card tier featured"><span class="tag hot">Most popular</span><h3>Builder</h3><div class="price">$15</div><p class="muted">per month</p><ul><li>Name on supporters wall</li><li>Early access to new tools</li><li>Vote on contest themes</li></ul><button class="btn btn-accent btn-sm" data-amount="15/month">Choose</button></div>
<div class="card tier"><h3>Patron</h3><div class="price">$50</div><p class="muted">per month</p><ul><li>Everything in Builder</li><li>Quarterly design Q&A</li><li>Logo/link on supporters page</li></ul><button class="btn btn-ghost btn-sm" data-amount="50/month">Choose</button></div>
<div class="card tier"><h3>Prize Fund</h3><div class="price">Any</div><p class="muted">one-time</p><ul><li>100% goes to contest prizes</li><li>Credited in winners' article</li></ul><button class="btn btn-ghost btn-sm" data-amount="Prize fund">Choose</button></div></div>

<div class="split mt"><div><h2>Where your money goes</h2>
<p><strong>Operations & hosting</strong> — 30%</p><div class="progress"><span style="width:30%"></span></div>
<p><strong>New tools & content</strong> — 25%</p><div class="progress"><span style="width:25%"></span></div>
<p><strong>Promotion & marketing</strong> — 15%</p><div class="progress"><span style="width:15%"></span></div>
<p><strong>Hiring talent (writers, designers, developers)</strong> — 15%</p><div class="progress"><span style="width:15%"></span></div>
<p><strong>Contests & prizes</strong> — 15%</p><div class="progress"><span style="width:15%"></span></div>
<p class="muted">Planned allocation. Donations are voluntary and are not tax-deductible charitable gifts.</p>
<div id="donate-links" class="hero-cta"></div></div>
<div class="card"><h2 style="font-size:1.5rem">Pledge your support</h2><p class="muted">Tell us how you'd like to give and we'll send a secure payment link (card, PayPal, bank transfer or crypto).</p>
<form class="form" data-form="Donation Pledge" data-success="Thank you for your support! A secure payment link is on its way to your inbox.">{hp()}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Amount</label><input name="amount" id="don-amount" required placeholder="e.g. 25 or 15/month"></div><div><label>Currency</label><select name="currency"><option>USD</option><option>CAD</option><option>EUR</option><option>GBP</option><option>INR</option><option>AUD</option></select></div></div>
<div class="row"><div><label>Direct my gift to</label><select name="purpose"><option>Where it's needed most</option><option>Ongoing operations</option><option>New tools & content</option><option>Promotion & marketing</option><option>Hiring talent</option><option>Contests & prizes</option></select></div><div><label>Preferred method</label><select name="method"><option>Card</option><option>PayPal</option><option>Bank transfer</option><option>Crypto</option></select></div></div>
<label class="check"><input type="checkbox" name="public_credit" value="yes"> Show my name on the supporters wall</label>
<button class="btn btn-accent" type="submit">Send pledge</button><div class="form-msg" role="status"></div></form></div></div>
<div class="band mt center"><h2>Corporate supporter or sponsor?</h2><p>Brands can fund tools, guides or contests in exchange for tasteful recognition.</p><a class="btn btn-accent" href="advertise.html">See sponsorship options</a></div>
</div></section>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('[data-amount]');if(!b)return;var i=document.getElementById('don-amount');i.value=b.getAttribute('data-amount');i.focus();i.scrollIntoView({{behavior:'smooth',block:'center'}});}});
fetch('data/site.json').then(function(r){{return r.json()}}).then(function(s){{var el=document.getElementById('donate-links');(s.donate_links||[]).forEach(function(l){{if(!l.url)return;var a=document.createElement('a');a.className='btn btn-sm';a.href=l.url;a.target='_blank';a.rel='noopener';a.textContent=l.label;el.appendChild(a);}});}}).catch(function(){{}});</script>"""
write("donate.html", layout("donate.html", "Support Space.Design — Donate to Keep Design Tools Free",
      "Support Space.Design with a one-time or monthly donation to fund operations, new free tools, marketing, hiring talent and contest prizes.", donate))

# ================================================================== CAREERS
roles = [("Freelance interior design writer", "Remote · Contract", "Write measurement-first guides and buying advice. Portfolio of published home/design content required."),
         ("3D visualiser / renderer", "Remote · Per project", "Create room renders and before/after visuals for guides and contests."),
         ("Video editor (YouTube & Shorts)", "Remote · Part-time", "Edit tool walkthroughs, makeover stories and design explainers."),
         ("Front-end developer", "Remote · Contract", "Build new calculators and planner features in vanilla JS and canvas."),
         ("Partnerships & sponsorship lead", "Remote · Commission", "Bring on brand sponsors, affiliate partners and contest prize partners."),
         ("Community & contest moderator", "Remote · Part-time", "Run monthly contests, verify entries and manage social channels.")]
role_cards = "".join(f'<div class="card reveal"><span class="tag">{w}</span><h3>{t}</h3><p>{d}</p><a class="btn btn-sm btn-ghost mt" href="#apply" data-role="{html.escape(t)}">Apply</a></div>' for t, w, d in roles)
careers = f"""<section class="block"><div class="wrap"><span class="eyebrow">Careers</span><h1>Build the future of space design with us.</h1>
<p class="lead muted" style="max-width:70ch">We're a remote-first team hiring designers, writers, developers and creators. Don't see your role? Apply anyway.</p>
<div class="grid g3 mt">{role_cards}</div>
<div class="card mt" id="apply" style="scroll-margin-top:90px"><h2>Apply</h2><form class="form" data-form="Job Application" data-success="Application received — thank you! We'll be in touch if there's a fit.">{hp()}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Role</label><input id="role" name="role" required></div><div><label>Location / time zone</label><input name="location"></div></div>
<div class="row"><div><label>Portfolio / LinkedIn</label><input type="url" name="portfolio" required placeholder="https://"></div><div><label>Availability</label><select name="availability"><option>Immediately</option><option>2 weeks</option><option>1 month+</option></select></div></div>
<div><label>Why you?</label><textarea name="message" required></textarea></div>
<button class="btn btn-accent" type="submit">Submit application</button><div class="form-msg" role="status"></div></form></div></div></section>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('[data-role]');if(b)document.getElementById('role').value=b.getAttribute('data-role');}});</script>"""
write("careers.html", layout("careers.html", "Careers — Remote Design, Writing & Developer Jobs",
      "Join Space.Design: remote roles for interior design writers, 3D visualisers, video editors, developers, partnerships and community moderators.", careers))

# ================================================================== ADVERTISE
adv = f"""<section class="block"><div class="wrap"><span class="eyebrow">Advertise & partner</span><h1>Reach people actively planning their spaces.</h1>
<p class="lead muted" style="max-width:70ch">Our visitors are measuring rooms, setting budgets and looking for products and professionals — right now. Partner with us on placements that help them.</p>
<div class="grid g4 mt" id="sponsor">
<div class="card"><h3>Tool sponsorship</h3><p>Exclusive "presented by" placement on a calculator or the room planner.</p></div>
<div class="card"><h3>Sponsored guide</h3><p>Expert, clearly labelled content written with our editorial team.</p></div>
<div class="card"><h3>Contest sponsor</h3><p>Fund monthly prizes; get logo placement, social mentions and a winners' feature.</p></div>
<div class="card"><h3>Pro directory feature</h3><p>Priority placement for designers and contractors in matching and listings.</p></div>
<div class="card"><h3>Lead partnerships</h3><p>Receive consented, qualified project requests in your region and category.</p></div>
<div class="card"><h3>Affiliate & product</h3><p>Furniture, paint, flooring and lighting brands — product integrations in tools.</p></div>
<div class="card"><h3>Video features</h3><p>Brand-integrated walkthroughs and makeover stories.</p></div>
<div class="card"><h3>Domain & acquisition</h3><p>Interested in acquiring or partnering on Space.Design itself? <a href="https://web.works/contact" target="_blank" rel="noopener">Get in touch</a>.</p></div></div>
<div class="split mt"><div><h2>Why Space.Design</h2><ul style="line-height:2"><li>High-intent audience: home improvement, renovation and furnishing</li><li>Premium, memorable, brandable domain</li><li>Fast, mobile-first, privacy-respecting pages</li><li>All sponsored content is clearly labelled</li></ul></div>
<div class="card"><form class="form" data-form="Advertising / Partnership Inquiry" data-success="Thanks! Our partnerships team will send a media kit within 2 business days.">{hp()}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Company</label><input name="company" required></div></div>
<div class="row"><div><label>Email</label><input type="email" name="email" required></div><div><label>Website</label><input type="url" name="website" placeholder="https://"></div></div>
<div class="row"><div><label>Interest</label><select name="interest"><option>Tool sponsorship</option><option>Sponsored guide</option><option>Contest sponsorship</option><option>Lead partnership</option><option>Affiliate / product</option><option>Video feature</option><option>Domain / website acquisition</option><option>Other partnership</option></select></div>
<div><label>Monthly budget</label><select name="budget"><option>Under $500</option><option>$500–$2,000</option><option>$2,000–$10,000</option><option>$10,000+</option><option>Let's discuss</option></select></div></div>
<div><label>Message</label><textarea name="message"></textarea></div><button class="btn btn-accent" type="submit">Request media kit</button><div class="form-msg" role="status"></div></form></div></div></div></section>"""
write("advertise.html", layout("advertise.html", "Advertise, Sponsor & Partner with Space.Design",
      "Advertising, sponsorship, lead partnerships and domain acquisition inquiries for Space.Design — reach people actively planning and renovating their spaces.", adv))

# ================================================================== ABOUT / CONTACT
about = """<section class="block"><div class="wrap article"><span class="eyebrow">About</span><h1>Good design starts with a tape measure.</h1>
<p class="lead muted">Space.Design is an independent resource that helps people plan, measure and design the spaces they live and work in.</p>
<p>Most design mistakes aren't about taste — they're about size, light and flow: a sofa that blocks a doorway, a rug that's too small, a kitchen without enough task lighting. We build free tools and write practical guides that solve those problems before money is spent.</p>
<h2>What we offer</h2><ul><li><strong>Free tools:</strong> a 2D room planner and nine calculators for paint, flooring, rugs, lighting, budgets, wallpaper, furniture fit, art and colour.</li><li><strong>Guides:</strong> original, measurement-first articles reviewed and updated regularly.</li><li><strong>Matching:</strong> a free service connecting homeowners with suitable designers and contractors.</li><li><strong>Community:</strong> monthly design contests celebrating real homes.</li></ul>
<h2>Editorial standards</h2><p>Our guides are written to be practical and accurate. Figures such as clearances and cost ranges are general guidance — local codes, products and prices vary, and we always recommend confirming with qualified local professionals. Sponsored content is always labelled.</p>
<h2>How we're funded</h2><p>Space.Design is supported by advertising (including Google AdSense), sponsorships, partnerships and voluntary <a href="donate.html">donations</a>. Advertisers never influence our editorial recommendations.</p>
<p><a class="btn" href="contact.html">Contact us</a></p></div></section>"""
write("about.html", layout("about.html", "About Space.Design", "Space.Design is an independent resource with free room planning tools, practical interior design guides and free designer matching.", about))
contact = f"""<section class="block"><div class="wrap split"><div><span class="eyebrow">Contact</span><h1>Let's talk.</h1>
<p class="lead muted">Questions, feedback, corrections, press or partnership ideas — send us a message and we'll reply within 1–2 business days.</p>
<div class="grid" style="gap:12px"><a class="card" href="get-quote.html"><h3>Need a designer?</h3><p>Use the free matching form for the fastest response.</p></a>
<a class="card" href="https://web.works/contact" target="_blank" rel="noopener"><h3>Domain, sponsorship or acquisition</h3><p>Interested in this website, the domain name, sponsorship, advertising or partnership? Contact the owner directly.</p></a>
<a class="card" href="#" data-mail="General inquiry"><h3>Prefer email?</h3><p>Click to open a pre-addressed message in your email app.</p></a></div></div>
<div class="card"><form class="form" data-form="Contact" data-success="Message sent — thank you! We'll reply within 1–2 business days.">{hp()}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div><label>Topic</label><select name="topic"><option>General question</option><option>Feedback / correction</option><option>Press</option><option>Partnership / sponsorship</option><option>Domain / website acquisition</option><option>Privacy request</option></select></div>
<div><label>Message</label><textarea name="message" required></textarea></div>
<button class="btn btn-accent" type="submit">Send message</button><div class="form-msg" role="status"></div></form></div></div></section>"""
write("contact.html", layout("contact.html", "Contact Space.Design", "Contact Space.Design for questions, feedback, press, partnerships, sponsorship or domain inquiries.", contact))

# ================================================================== LEGAL
privacy = f"""<section class="block"><div class="wrap article"><h1>Privacy Policy</h1><p class="meta">Last updated {TODAY}</p>
<p>This policy explains what information Space.Design ("we", "us") collects and how it's used. By using this website you agree to this policy.</p>
<h2>Information you give us</h2><p>When you submit a form (quote request, contact, contest entry, application, pledge) we receive the details you enter, such as name, email, phone, location and project information. We use it only to respond to you and provide the service you asked for — for example, introducing you to suitable professionals when you request matching. We do not sell your personal information.</p>
<p>Forms are delivered to us by email through a third-party form-processing service (FormSubmit), which processes the submission solely to deliver it.</p>
<h2>Information stored in your browser</h2><p>Room plans, theme choice, quiz results and cookie preferences are stored in your browser's local storage and are never sent to us.</p>
<h2 id="cookies">Cookies and advertising</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the Internet.</p>
<p>You can opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" rel="noopener" target="_blank">Google Ads Settings</a>, or opt out of third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p>
<p>You can reset your cookie choice here: <button class="btn btn-sm btn-ghost" onclick="try{{localStorage.removeItem('sd-consent')}}catch(e){{}};location.reload()">Change cookie settings</button></p>
<h2>Embedded content</h2><p>Videos are embedded from YouTube using its privacy-enhanced mode and load only when you click play. Embedded content behaves as if you visited the other website and may collect data under that site's policy.</p>
<h2>Your rights</h2><p>Depending on where you live (including under GDPR, UK GDPR, PIPEDA, CCPA/CPRA and India's DPDP Act), you may request access to, correction of or deletion of your personal data. Use the <a href="contact.html">contact form</a> and choose "Privacy request".</p>
<h2>Retention & security</h2><p>We keep submissions only as long as needed for the purpose they were sent and to meet legal obligations. The site is served over HTTPS.</p>
<h2>Children</h2><p>This site is not directed to children under 13 (or 16 in the EEA), and we do not knowingly collect their data.</p>
<h2>Changes</h2><p>We may update this policy; the date above shows the latest version.</p></div></section>"""
write("privacy.html", layout("privacy.html", "Privacy Policy", "How Space.Design collects, uses and protects information, including cookies and Google AdSense advertising.", privacy))
terms = f"""<section class="block"><div class="wrap article"><h1>Terms of Use</h1><p class="meta">Last updated {TODAY}</p>
<h2>Use of the site</h2><p>Space.Design provides free tools, articles and a matching service for general information. You agree to use the site lawfully and not to misuse forms, scrape at abusive rates or attempt to disrupt the service.</p>
<h2>No professional advice</h2><p>Calculations, measurements, cost ranges and guidance are estimates for planning purposes only. They are not architectural, engineering, legal or financial advice. Always confirm with qualified local professionals and comply with local building codes.</p>
<h2>Professionals & matching</h2><p>Professionals introduced through Space.Design are independent businesses. We don't employ them and aren't party to your agreements with them. Check licences, insurance and references before hiring.</p>
<h2>User submissions</h2><p>By submitting content (e.g. contest entries) you confirm you own it and grant us a non-exclusive, royalty-free licence to display it with credit. We may remove any submission at our discretion.</p>
<h2>Third-party content</h2><p>News headlines link to their original publishers, and videos are embedded via YouTube's official player. All third-party content remains the property of its owners.</p>
<h2>Donations</h2><p>Donations are voluntary, generally non-refundable and are not tax-deductible charitable contributions unless stated otherwise.</p>
<h2>Liability</h2><p>The site is provided "as is" without warranties. To the fullest extent permitted by law, we are not liable for losses arising from use of the site or reliance on its content.</p>
<h2>Changes</h2><p>We may update these terms at any time. Continued use means you accept the current version.</p></div></section>"""
write("terms.html", layout("terms.html", "Terms of Use", "Terms of use for Space.Design tools, guides, matching service, contests and donations.", terms))
disc = f"""<section class="block"><div class="wrap article"><h1>Disclaimer, Trademark & Copyright Notice</h1><p class="meta">Last updated {TODAY}</p>
<h2>Trademark disclosure</h2><p>Space.Design is an independent website operating under the domain name <strong>space.design</strong>, which describes its subject matter: the design of spaces. The term "space design" is used here in its ordinary, descriptive sense.</p>
<p><strong>Space.Design is not affiliated with, endorsed by, sponsored by or connected to any company, studio, product, brand or registered trademark named "Space Design", "SpaceDesign", "Spacedesign", "Space Designs" or any similar name</strong>, in any country. Any such names are the property of their respective owners. If you believe any content on this site infringes your trademark, please <a href="contact.html">contact us</a> and we will respond promptly.</p>
<p>All other product names, logos and brands mentioned (including YouTube, Google and any publication names in our news feed) are property of their respective owners and are used for identification only. Their use does not imply endorsement.</p>
<h2>Copyright</h2><p>© {datetime.date.today().year} Space.Design. Original text, tools, code, illustrations and design on this website are protected by copyright. You may link to our pages and quote brief excerpts with attribution. Republishing full articles or copying the tools without permission is not allowed.</p>
<p>Third-party material — embedded YouTube videos and linked news headlines — remains the property of its creators and is shown via official embeds or links back to the source. We do not host copies of third-party articles or videos.</p>
<h2>Copyright complaints</h2><p>If you believe material on this site infringes your copyright, send a notice through our <a href="contact.html">contact form</a> including the work, the URL and your contact details. We will review and remove infringing material promptly.</p>
<h2>Advertising & affiliate disclosure</h2><p>This site displays ads served by Google AdSense and may contain sponsored content or affiliate links, which are always identified. This does not affect the price you pay or our editorial independence.</p>
<h2>Accuracy</h2><p>Content is provided for general information. Measurements, codes and costs vary by location and change over time; verify with qualified professionals before acting.</p></div></section>"""
write("disclaimer.html", layout("disclaimer.html", "Disclaimer, Trademark & Copyright Notice",
      "Space.Design trademark and copyright disclosure: independent website, not affiliated with any company named Space Design; advertising and accuracy disclaimers.", disc))

# ================================================================== 404
nf = """<section class="block"><div class="wrap center"><h1>404 — this room doesn't exist.</h1><p class="lead muted">The page may have moved. Try one of these:</p>
<div class="hero-cta" style="justify-content:center"><a class="btn" href="index.html">Home</a><a class="btn btn-ghost" href="tools.html">Tools</a><a class="btn btn-ghost" href="guides/index.html">Guides</a><a class="btn btn-accent" href="get-quote.html">Get free quotes</a></div></div></section>"""
page = layout("404.html", "Page not found", "Page not found.", nf, noindex=True)
page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8"><script>document.write(\'<base href="\'+(location.hostname.endsWith("github.io")?"/space-design/":"/")+\'">\')</script>', 1)
write("404.html", page)

# ================================================================== SEO / infra files
urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p.replace('index.html', '')}</loc><lastmod>{TODAY}</lastmod><changefreq>{'daily' if p in ('index.html','news.html','videos.html') else 'weekly'}</changefreq><priority>{'1.0' if p=='index.html' else '0.8' if p in ('tools.html','planner.html','get-quote.html') else '0.6'}</priority></url>" for p in PAGES)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
write("robots.txt", f"User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
write("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
write("manifest.webmanifest", json.dumps({"name": NAME, "short_name": NAME, "start_url": "./index.html", "display": "standalone", "background_color": "#F4F1EA", "theme_color": "#18181B", "icons": [{"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=1))
write(".nojekyll", "")
print("Built", len(PAGES), "indexable pages")
