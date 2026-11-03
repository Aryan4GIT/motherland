#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates the Motherland Group site into the repo root.
Pages live at the root so static hosts (Vercel, GitHub Pages, Netlify)
serve them with no configuration.
One source of truth for the chrome; each page supplies only its body.
Run:  python build.py
"""
import datetime, glob, io, math, os, re
from urllib.parse import quote, unquote

OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ('motherland-garments.html', 'Garment Washing'),
    ('mdenim.html',              'mDenim'),
    ('msquare.html',             'mSquare'),
    ('about.html',               'About'),
    ('team.html',                'Team'),
    ('testimonials.html',        'Testimonials'),
]

TEL = 'tel:+919342250766'
TEL_2 = 'tel:+919740044100'
EMAIL = 'blr@motherlandgroup.com'
ADDRESS = '#40-B, 2nd Phase, Peenya Industrial Area, Bengaluru, Karnataka 560058'

PHONE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')
MAIL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>'
PIN_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
PLANT_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21V8l9-5 9 5v13"/><path d="M9 21v-7h6v7"/></svg>'
STORE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h18v18H3z"/><path d="M3 9h18M9 21V9"/></svg>'
MENU_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
CLOSE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'


def asset(path):
    """Filenames here contain spaces and apostrophes, which must not reach the HTML raw."""
    return 'assets/img/' + quote(path)


BRAND = ('<a class="brand" href="index.html"><img alt="" src="assets/img/mark-sm.png" width="38" height="30">'
         '<span>Motherland <small>Group, since 1995</small></span></a>')


def head(title, desc, keywords=''):
    kw = f'<meta name="keywords" content="{keywords}">\n' if keywords else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{kw}<meta name="theme-color" content="#ffffff">
<link rel="icon" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=Instrument+Serif&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('motion')==='off')document.documentElement.classList.add('still')}}catch(e){{}}</script>
<script defer src="assets/js/app.js"></script>
</head>
<body>
<a class="skip" href="#top">Skip to content</a>
<div class="prog" aria-hidden="true"></div>
'''


def topbar(current):
    def item(href, label):
        cur = ' aria-current="page"' if href == current else ''
        return f'<a href="{href}"{cur}>{label}</a>'

    links = ''.join(item(h, l) for h, l in NAV)
    menu_links = item('index.html', 'Home') + links + item('contact.html', 'Contact')

    return f'''
<header class="head">
  <div class="shell head-in">
    {BRAND}
    <nav class="links" aria-label="Main">{links}</nav>
    <a class="tel" href="{TEL}">+91 93422 50766</a>
    <a class="btn btn--house" href="contact.html">Talk to us</a>
    <button class="burger" type="button" data-menu aria-label="Open menu" aria-haspopup="dialog">{MENU_SVG}</button>
  </div>
</header>

<dialog class="menu" id="menu" aria-label="Menu">
  <div class="menu-top">
    {BRAND}
    <button class="menu-x" type="button" data-menu-close aria-label="Close menu">{CLOSE_SVG}</button>
  </div>
  <nav aria-label="Menu">{menu_links}</nav>
  <div class="menu-end">
    <a class="contact-l" href="mailto:{EMAIL}">{EMAIL}</a>
    <a class="btn btn--house" href="{TEL}">Call +91 93422 50766</a>
  </div>
</dialog>
'''


FOOT = f'''
<footer class="foot">
  <div class="foot-word" aria-hidden="true"><div><span>Motherland Group</span><span>Motherland Group</span><span>Motherland Group</span><span>Motherland Group</span></div></div>
  <div class="shell">
    <div class="foot-grid">
      <div>
        {BRAND}
        <p class="foot-about">Garment washing, denim manufacturing and retail, from four units across Bangalore and Chennai.</p>
        <div class="socials">
          <a href="https://www.facebook.com/motherlandgarments/" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1Z"/></svg></a>
          <a href="https://www.linkedin.com/in/motherland-group-76b9b1184/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm7 0h3.8v1.7h.05c.53-1 1.82-2.05 3.75-2.05C21.6 8.65 23 10.9 23 14.2V21h-4v-6c0-1.43-.03-3.27-2-3.27-2 0-2.3 1.56-2.3 3.17V21h-4V9Z"/></svg></a>
        </div>
      </div>

      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="about.html#history">Our history</a></li>
          <li><a href="team.html">Our team</a></li>
          <li><a href="testimonials.html">Testimonials</a></li>
          <li><a href="contact.html">Contact us</a></li>
        </ul>
      </div>

      <div>
        <h2>Services</h2>
        <ul>
          <li><a href="motherland-garments.html">Garment washing</a></li>
          <li><a href="motherland-garments.html#finishes">Functional finishes</a></li>
          <li><a href="mdenim.html">Denim manufacturing</a></li>
          <li><a href="mdenim.html#custom">Denim customisation</a></li>
          <li><a href="mdenim.html#alterations">Alteration and refashion</a></li>
          <li><a href="msquare.html">Retail and wholesale</a></li>
        </ul>
      </div>

      <div>
        <h2>Get in touch</h2>
        <address>{ADDRESS}</address>
        <ul>
          <li><a href="{TEL}">+91 93422 50766</a></li>
          <li><a href="{TEL_2}">+91 97400 44100</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>

    <div class="foot-base">
      <span>&copy; {datetime.date.today().year} Motherland Group. All rights reserved.</span>
      <nav aria-label="Legal"><a href="terms.html">Terms &amp; Conditions</a><a href="privacy.html">Privacy Policy</a><button type="button" data-motion="text">Pause motion</button></nav>
    </div>
  </div>
</footer>

<nav class="dock" aria-label="Quick actions">
  <a href="{TEL}">{PHONE_SVG}Call</a>
  <a class="go" href="contact.html">Talk to us</a>
  <button type="button" data-menu aria-haspopup="dialog">{MENU_SVG}Menu</button>
</nav>
</body>
</html>
'''


def page(fname, title, desc, body, keywords=''):
    html = head(title, desc, keywords) + topbar(fname) + '<main id="top" tabindex="-1">' + body + '</main>' + FOOT
    # Images in the first screen are written as <img fetchpriority=...> or <img alt=...>, so only the rest go lazy.
    html = html.replace('<img src=', '<img loading="lazy" decoding="async" src=')
    with io.open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        f.write(html)
    return fname


# ---------------------------------------------------------------- partials

STAMP = (f'''<div class="stamp" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="stampPath" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs>'''
         '''<text><textPath href="#stampPath" textLength="283">Motherland Group, since 1995 &#10022; Bangalore, Chennai &#10022;</textPath></text></svg>'''
         '''<img alt="" src="assets/img/mark-sm.png" width="96" height="76"></div>''')


def stage_visual(palette='silk', extra=''):
    """A moving field with the turning drum over it. Decorative; the CSS gradient behind it is the fallback."""
    return (f'<canvas data-flow="{palette}" aria-hidden="true"></canvas>'
            f'<div class="drum-at" aria-hidden="true"><img alt="" class="drum" src="assets/img/drum.svg"></div>{extra}')


def phero(img, crumb, h1, lede='', pos='center', alt='', visual=''):
    """Page header. Words beside the photograph, never on top of it."""
    fig = (f'<div class="phero-fig"><figure class="phero-ph stitched"><img fetchpriority="high" src="{asset(img)}" alt="{alt}" '
           f'style="object-position:{pos}"></figure>{STAMP}</div>') if img else visual
    para = f'<p class="lede">{lede}</p>' if lede else ''
    cls = '' if img else (' phero--stage' if visual else ' phero--plain')
    return f'''
<section class="phero{cls}">
  <div class="shell phero-grid">
    <div>
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
      <h1>{h1}</h1>
      {para}
    </div>
    {fig}
  </div>
</section>'''


def sec_head(h2, lede=''):
    para = f'<p class="lede">{lede}</p>' if lede else ''
    return f'<div class="sec-head"><h2>{h2}</h2>{para}</div>'


def row(title, icon, text):
    return (f'<details class="row"><summary><span class="ico"><img src="{asset("icons/" + icon + ".png")}" alt=""></span>'
            f'{title}</summary><p>{text}</p></details>')


def rows(items):
    return '<div class="rows">' + ''.join(row(*i) for i in items) + '</div>'


def voice(head, text, name, co, img=None):
    av = (f'<img src="{asset("customers/" + img)}" alt="">' if img else
          f'<span class="ini" aria-hidden="true">{name[0]}</span>')
    return (f'<figure class="voice"><h3>{head}</h3><blockquote>{text}</blockquote>'
            f'<figcaption>{av}<span><b>{name}</b> <small>{co}</small></span></figcaption></figure>')


def voices_grid(items):
    return ('<div class="voices" role="group" aria-label="Testimonials" tabindex="0">'
            + ''.join(voice(*t) for t in items) + '</div>')


def stage(items):
    """One voice at a time, large. Without JS they simply stack, so nothing is lost."""
    quotes = who = ''
    for i, (head_, text, name, co, img) in enumerate(items):
        on = ' is-on' if i == 0 else ''
        av = (f'<img src="{asset("customers/" + img)}" alt="">' if img else
              f'<span class="ini" aria-hidden="true">{name[0]}</span>')
        quotes += (f'<figure class="sq{on}"><h3>{head_}</h3><blockquote>{text}</blockquote>'
                   f'<figcaption class="sq-by"><b>{name}</b>, {co}</figcaption></figure>')
        pressed = 'true' if i == 0 else 'false'
        who += (f'<button class="who{on}" type="button" aria-pressed="{pressed}">{av}<b>{name}</b>'
                f'<i class="who-bar"></i></button>')
    return (f'<div class="stage"><div class="stage-q">{quotes}</div>'
            f'<div class="stage-who" role="group" aria-label="Choose who to read">{who}</div></div>')


def tabset(label, items, extra=''):
    """items: (id, tab label, count, panel html).
    Every panel is visible in the markup and app.js hides the rest, so nothing is lost without JS."""
    tabs = panels = ''
    for pid, name, count, body in items:
        tabs += (f'<button class="tab" type="button" role="tab" id="t-{pid}" aria-controls="{pid}">'
                 f'{name} <small>{count}</small></button>')
        panels += f'<div class="panel" id="{pid}" role="tabpanel" aria-labelledby="t-{pid}" tabindex="0">{body}</div>'
    return f'<div class="tabs{extra}" role="tablist" aria-label="{label}">{tabs}</div>{panels}'


def split(img, alt, text):
    return f"""
    <div class="split">
      <div class="split-txt">{text}</div>
      <figure class="split-ph"><img src="{asset(img)}" alt="{alt}"></figure>
    </div>"""


def spec(term, items):
    return f'<div><dt>{term}</dt><dd><ul class="chips">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></dd></div>'


def cta(line, sub, label='Talk to us', href='contact.html'):
    return f'''
<section class="cta">
  <canvas data-flow="cta" aria-hidden="true"></canvas>
  <div class="shell cta-in">
    <div><h2>{line}</h2><p>{sub}</p></div>
    <div class="cta-acts">
      <a class="btn btn--white" href="{href}">{label}</a>
      <a class="cta-tel" href="{TEL}">Call +91 93422 50766</a>
    </div>
  </div>
</section>'''


APPROVALS = ['Inditex', 'Marks and Spencer', 'Lacoste', 'Bestseller', 'Varner',
             'American Eagle Outfitters', 'Next']

_approved = '<ul{}>' + ''.join(f'<li>{b}</li>' for b in APPROVALS) + '</ul>'
APPROVE_MQ = f'''
<section class="approve" aria-label="Brands that have approved Motherland Garments">
  <div class="shell approve-in">
    <p class="approve-l">Approved by</p>
    <div class="mq"><div class="mq-row">{_approved.format('')}{_approved.format(' aria-hidden="true"') * 3}</div></div>
  </div>
</section>'''

CLIENT_LOGOS = [('Aditya.jpg', 'Aditya Birla'), ('Arvind.jpg', 'Arvind'), ('Derby.jpg', 'Derby'),
                ('HHEC.jpg', 'HHEC'), ('Hasbro.jpg', 'Hasbro'), ('Indus.jpg', 'Indus League'),
                ('Lawernce.jpg', 'Lawrence &amp; Mayo'), ('Pearl.jpg', 'Pearl Global')]


def clients_band(tone=''):
    logos = ''.join(f'<li><img src="{asset("clients/" + f)}" alt="{a}"></li>' for f, a in CLIENT_LOGOS)
    twice = ''.join(f'<li><img src="{asset("clients/" + f)}" alt=""></li>' for f, a in CLIENT_LOGOS)
    return f'''
<section class="band{tone}">
  <div class="shell">
    {sec_head('Exporters and brands who send us their garments')}
    <div class="mq logo-mq"><div class="mq-row"><ul>{logos}</ul><ul aria-hidden="true">{twice}</ul><ul aria-hidden="true">{twice}</ul><ul aria-hidden="true">{twice}</ul></div></div>
  </div>
</section>'''


def _sc(href, img, alt, tag, name, text, more, is_open=False):
    return f'''
      <a class="sc{' is-open' if is_open else ''}" href="{href}">
        <div class="sc-ph"><img src="{asset(img)}" alt="{alt}"></div>
        <div class="sc-body">
          <p class="sc-tag">{tag}</p>
          <h3>{name}</h3>
          <div class="sc-more"><div>
            <p class="sc-txt">{text}</p>
            <span class="more">{more}</span>
          </div></div>
        </div>
        <i class="sc-bar"></i>
      </a>'''


SHOWCASE = '<div class="showcase">' + _sc(
    'motherland-garments.html', 'motherland-01.jpg', 'Industrial tumble driers on the Motherland washing line',
    'For exporters and brands', 'Motherland Garments',
    'Four units across Bangalore and Chennai serving almost every leading garment exporter and domestic brand. From 1000 garments a day in 1995 to a 60,000-a-day capacity.',
    'Explore washing', True) + _sc(
    'mdenim.html', 'denim.jpg', 'Hand-finishing denim at mDenim',
    'For brands and individuals', 'mDenim',
    'Not only your suits and coats can be tailored &mdash; your denim can too, in a variety of designs and washes. We also repair, alter and refashion old denim professionally.',
    'Explore mDenim') + _sc(
    'msquare.html', 'retails-showroom.jpg', 'Stacked denim inside an mSquare store',
    'For shoppers and retailers', 'mSquare',
    'Five stores across Bangalore stocked with factory-fresh denims, chinos, casual shirts, knits, tees, tracks, joggers, kids and ladies wear in the latest fabrics, fits and washes.',
    'Explore mSquare') + '''
    </div>'''

SWATCH = '''
    <div class="swatch stitched">
      <canvas aria-hidden="true"></canvas>
      <div class="sw-bar" aria-hidden="true"><span class="sw-knob"><svg viewBox="0 0 24 24"><path d="m9 6-6 6 6 6"/><path d="m15 6 6 6-6 6"/></svg></span></div>
      <span class="sw-tag l" aria-hidden="true">Raw</span>
      <span class="sw-tag r" aria-hidden="true">Washed</span>
      <label class="vh" for="swatchRange">Where the wash starts, from raw on the left to washed on the right</label>
      <input id="swatchRange" type="range" min="0" max="100" step="1" value="50">
    </div>
    <p class="sw-note">Drag across the cloth to wash it down. This is an illustration drawn live in your browser, not a photograph of a finished garment.</p>'''

_PANDIAN_QUOTE = 'Motherland believes in the philosophy of WIN WIN WIN &mdash; for a successful business all the stakeholders, customer, employees and the business owner, should win. It is happy employees who ensure customer satisfaction and thereby guarantee a successful business.'
_SELVAMANI_QUOTE = 'Sustainability is the core of all our beliefs and it is reflected in the way we work &mdash; from sourcing non-hazardous chemicals and auxiliaries, to less water and energy consuming equipment, to investing in new technologies that reduce our impact on the environment.'


def _dir(img, name, role, quote_text):
    return (f'<figure class="dir"><blockquote>{quote_text}</blockquote>'
            f'<figcaption><img src="{asset("Photos/" + img)}" alt=""><span><b>{name}</b> <small>{role}</small></span></figcaption></figure>')


DIRECTORS = ('<div class="dirs">'
             + _dir('a-j-Pandian-Managing-Director.jpg', 'A. J. Pandian', 'Managing Director', _PANDIAN_QUOTE)
             + _dir('s-a-Selvamani-Technical-Director.jpg', 'S. A. Selvamani', 'Technical Director', _SELVAMANI_QUOTE)
             + '</div>')


LINE = '''
<section class="liner" aria-label="How a garment moves through the wash">
  <canvas data-line="wash" aria-hidden="true"></canvas>
  <div class="shell liner-key"><span>Raw from the line</span><span>Through the wash</span><span>Finished denim</span></div>
</section>'''

RACK = '''
<div class="liner liner--rack" aria-hidden="true"><canvas data-line="rack"></canvas></div>'''

SEAM = '''
<div class="seam" aria-hidden="true">
  <div class="seam-cloth"></div>
  <div class="seam-stitch"></div>
  <div class="seam-wash"></div>
  <div class="needle"><i></i></div>
  <div class="foot-plate"></div>
</div>'''

# dark band with indigo dye moving behind whatever it holds
DYE = '<canvas data-flow="dye" aria-hidden="true"></canvas>'


def write_drum():
    """A wash drum seen from the front: staggered perforations, three lifter ribs, a heavy rim.
    The ribs matter: without them the rotation would be invisible."""
    dots = ''
    for k, r in enumerate(range(92, 22, -5)):
        n = int(r * 1.15)
        shift = (k % 2) * math.pi / n
        for i in range(n):
            a = shift + 2 * math.pi * i / n
            dots += f'<circle cx="{100 + r * math.cos(a):.1f}" cy="{100 + r * math.sin(a):.1f}" r=".85"/>'
    ribs = ''.join(f'<rect x="95.5" y="8" width="9" height="46" rx="4.5" transform="rotate({a} 100 100)"/>' for a in (0, 120, 240))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
           f'<g fill="#fff" fill-opacity=".34">{dots}</g><g fill="#fff" fill-opacity=".16">{ribs}</g>'
           '<g fill="none" stroke="#fff"><circle cx="100" cy="100" r="97" stroke-opacity=".3" stroke-width="3"/>'
           '<circle cx="100" cy="100" r="17" stroke-opacity=".3" stroke-width="2"/></g></svg>')
    with io.open(os.path.join(OUT, 'assets', 'img', 'drum.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)


# ---------------------------------------------------------------- wash data

BASIC = [
    ('Garment Wash', 'vintage', 'Fulfils the basic requirement of preshrinking the garment to arrest further shrinkage during home laundering.'),
    ('Stone Wash', 'bronze', 'Pronounced puckered effect on the seams, body breakage and a vintage look &mdash; preferably for heavier fabrics.'),
    ('Enzyme Wash', 'cleaning', 'Gives a puckered look on the seams, and enhances the brightness and body breakage.'),
    ('Acid Wash', 'flask', 'Multiple levels of washed-down effect with a grainy body and high-contrast puckering on the seams, for all types of dyed fabrics.'),
    ('Rubber / Silicon Ball Wash', 'medicine-ball', 'Garments are washed with emery, rubber, plastic and silicone-coated balls to give myriad finishes.'),
    ('Perlite Wash', 'shirt', 'Delicate lightweight garments that need a stone wash effect are washed with perlite powder in place of pumice stones, to avoid damage.'),
    ('Peach Wash', 'peach', 'Peaching or sueding is a mechanical finish done on fabrics &mdash; the same effect is replicated in garment form by chemical treatment.'),
    ('Silicon Softener', 'silicone', 'Enhances the touch and feel of the garment.'),
]

FUNC = [
    ('Antiviral Finish', 'anti-pilling-fabric', 'Gives antiviral characteristics to the garment and helps combat many virus strains, including Covid-19.'),
    ('Antimicrobial', 'germs', 'Imparts antimicrobial properties that inhibit the growth of odour-causing bacteria and disease-causing germs.'),
    ('Cool Finish', 'soil', 'Helps keep fabrics cool by up to 3&deg;C when in contact with sweat or moisture.'),
    ('Ultra Violet Protection', 'greenhouse-effect', 'Overexposure to invisible UV radiation leads to sunburn, accelerated skin ageing and skin cancer. Treated garments protect against it &mdash; especially needed for fair, sun-sensitive skin, children, and people who spend long hours outdoors.'),
    ('Water &amp; Oil Repellency', 'oil-bottle', 'Cotton has a higher surface tension than oil and water, so liquids soak in. This finish lowers the fabric&rsquo;s surface tension below that of the liquids &mdash; so the garment repels both.'),
    ('Moisture Management', 'moisturizer', 'Garments worn next to the skin transport sweat away and evaporate it quickly. They stay dry, don&rsquo;t cling, feel cooler, and the fabric breathes better.'),
]

CORR = [
    ('Backstain Removal', 'flames', 'Any kind of back staining on denims and indigos can be removed post-wash.'),
    ('Colour Fixing', 'color-wheel', 'Fastness parameters &mdash; colour fastness to washing, crocking and light &mdash; are improved with this wash.'),
    ('Colour Enhancing', 'rgb', 'Dark colours like blacks and navies are made deeper and brighter by this process.'),
    ('Anti Seam Slippage', 'seam-ripper', 'In some garments seams slip at the slightest force. A special auxiliary corrects it and increases strength at the same time.'),
    ('Anti Pilling', 'ozone-layer', 'Reduces pilling on fabrics and knits made from synthetic-content yarns, by suppressing the fibres&rsquo; ability to slacken and lowering their mechanical resistance.'),
    ('Optical Brightener Wash', 'brightness-and-contrast', 'Makes whites brighter by absorbing invisible ultraviolet light and re-emitting it as visible light in the blue range of the spectrum.'),
]

ALTERATIONS = [
    ('Embroidering', 'Emroidering', 'Embellishing denim with decorative stitching, colourful thread and a variety of stitch patterns to create unique designs.'),
    ('Washes', 'vintage', 'Treatments that alter the colour, texture and appearance of denim &mdash; stone, bleach, acid and other specialised washes.'),
    ('Hems', 'Hems', 'The finished edge of a denim garment &mdash; stitched, folded or cut for a clean, even edge that resists fraying.'),
    ('Length Alteration', 'lj', 'Adjusting the length through hemming or cutting, to a better fit and a style that suits the wearer.'),
    ('Tapering', 'tap', 'Narrowing the leg opening for a more modern or fitted look, using specialised sewing techniques.'),
    ('Waist Alteration', 'wai', 'Adjusting the waistline for a better fit, through resizing, adding darts or other sewing techniques.'),
    ('Holes &amp; Tears', 'Holes and Tears', 'Damage repaired and reinforced by darning, patching and other methods, to prolong the life of the garment.'),
    ('Patch Work', 'pocket', 'Decorative and functional &mdash; patches of contrasting denim or other fabric attached to repair, reinforce and design.'),
    ('Damaging', 'monogram', 'Deliberately distressed, worn or vintage looks, created by cutting, sanding or bleaching the fabric.'),
    ('Darning', 'yarn', 'Repairing holes and worn areas by weaving new threads through the existing fabric.'),
    ('Gathering', 'gather', 'Ruffles made with a longer stitch length and pulled threads, adding texture and volume to the fabric.'),
    ('Tailoring', 'sewing-machine', 'Altering denim to a better fit or style &mdash; hemming, tapering, waistband adjustments and more.'),
    ('Zips', 'zipper-tool', 'Zippers for denim, usually metal, built to be durable and long-lasting while adding a functional, stylish detail.'),
    ('Rips', 'riped', 'Intentional or unintentional tears that add a distressed or vintage look, often needing repair or reinforcement.'),
    ('Hardware', 'hadr', 'Buttons, rivets, zippers and other metal elements, functional and decorative, used in building a denim garment.'),
]

TIMELINE = [
    ('1995', 'The journey begins in a makeshift shed in Chennai. Jaihind Garments: one set of machinery on loan, one customer, 500 shirts a day.'),
    ('1997', 'A sick unit is taken over and starts serving customers in the Ambattur area under the name Jaihind Textile Processors.'),
    ('1998', 'Jaihind Garments moves from Guindy to its own premises at SIDCO Thirumudivakkam.'),
    ('2005', 'The milestone year. A big facility is taken over at Magadi Road, Bangalore. The existing companies merge and are named Motherland Garments Private Limited.'),
    ('2012', 'Second unit opens at KIADB Industrial Area, Kanakapura Road, Harohalli &amp; Peenya, Bangalore.'),
    ('2016', 'A new venture, mDenim, for alteration, refashion and customisation of denims.'),
    ('2020', 'Third unit, exclusive for denim washing, at Peenya. mSquare, the retail arm of Motherland Group, opens on Magadi Road and in Peenya.'),
]

STORES = [
    '75 Magadi Road, Opposite Metro Station, Bangalore 560023',
    '12th Cross, Magadi Main Road, Bangalore 560023',
    '40B, 2nd Phase, Peenya Industrial Area, Bangalore 560058',
    '6th Main, 3rd Phase, Rajagopalnagar Main Road, Bengaluru 560058',
    '3rd Stage, Peenya, Laggere Arch, Bangalore 560058',
]

SUPERSTARS = [
    ('Thejaswini', 'Marketing', None), ('Mamatha', 'Accountant', None),
    ('Bindushree', 'Human Resources', None), ('Asha', 'Admin', None),
    ('Manjunatha R', 'Admin', 'Manjunatha R.jpg'), ('Andiswamy', 'Sales', None),
    ('Mahesh S', 'Operation', None), ('Myliraj R', 'Operation', 'Myliraj R.jpg'),
    ('Gowda BL', 'Sales', None),
]

# testimonials: (heading, body, name, company, photo)
T_WASH = [
    ('Innovative techniques', 'Motherland have a separate R&amp;D team and very nice wash effects by them, and innovative techniques. We would like to explore more with Motherland.', 'Leena Anand', 'HOD Designs, K. Mohan &amp; Co', 'leena.png'),
    ('Happy with Motherland', 'We are happy with the samples &mdash; they came out good enough as per the originals, and we got them within the targeted date.', 'Sharika', 'Designer, Rivera Creation', 'sharika.png'),
    ('Especially the SQUMA effect', 'Motherland R&amp;D new development samples are simply splendid, especially the SQUMA effect. These days designers look forward to innovative and SQUMA contrast looks in denim.', 'Babul Arya', 'Designer, YA Apparels', 'arya.png'),
    ('Great products', 'Really, I&rsquo;m going to have to leave &ldquo;awesome&rdquo; on every order. I&rsquo;d like to thank all the staff at Motherland Garments for their help &mdash; from the owner to customer service, sales, shipping and receiving. Great products. My clients love them.', 'Anjibabu', 'E-Land Group', None),
    ('Prompt on every commitment', 'We came to know about Motherland Laundry of Bangalore through a reliable source. We were looking for a good laundry in Bangalore and found it in Motherland. They are very prompt in their pick-up and delivery commitments, with a sincere, hardworking and dedicated team. All the best to your team going forward.', 'Thomas Malakkaran', 'Usha Garments', None),
]

T_DENIM = [
    ('Everyone asks me where I got it', 'I am thankful to mDenim for the bag I bought last month. I am so happy with it and all my colleagues ask me where I got it &mdash; because it&rsquo;s a beautiful design at a reasonable price. Trust me, the bag designs are marvellous; you&rsquo;ll know once it&rsquo;s on your shoulder.', 'Alankrita Chordia', 'mDenim bags', None),
    ('Now the fitting is excellent', 'My waist size reduced from 42&Prime; to 36&Prime;. I had three jeans that needed re-altering to my fit. I found mDenim through a Google search, contacted Anisha, explained what I needed, went in person, and the tailor took measurements and re-altered the jeans. Now the fitting is excellent. Their service is excellent and they did amazing work.', 'Vijayanagaram Srihari', 'mDenim alteration', None),
    ('The bag is mind blowing', 'mDenim team, you amazed me with the bag. I especially appreciate the person who guided me through all the fabric work that went into it. At home my sister and mum use the one-sided bag for everything. Everyone should try these bags &mdash; the design is very good, it&rsquo;s unisex, the stitching is finely done, and the price is reasonable.', 'Anamika Varshney', 'mDenim bags', None),
    ('Still using it for my laptop', 'Thank you so much mDenim. You gave me really good service for my clothes washing, and the bag I bought recently is very usable for daily purposes. I am still using it for my laptop and other things and have not found a single fault in the stitching. A very unique and marvellous design.', 'Sridhar Yerimgere', 'mDenim bags', None),
]

T_RETAIL = [
    ('Never seen these prices anywhere else', 'High quality products at the lowest prices, never seen anywhere else. I have shopped many times and the family members I referred are also happily shopping.', 'Vijay Kumar', 'mSquare retail', None),
    ('Such lovely selections', 'What a beautiful store and such lovely selections. I bought gifts to take home at reasonable prices and couldn&rsquo;t resist a few items for myself. I&rsquo;m so glad to have experienced this store and this style of India &mdash; highly recommend.', 'Yathiraju GN', 'mSquare retail', None),
    ('Every purchase has been perfect', 'Every purchase I have made has been perfect. The items are quality and well made. I have also bought my daughter a couple of outfits and she loves them. I highly recommend this awesome business.', 'Mohan Sarangapani', 'mSquare retail', None),
    ('Worth the purchase', 'Purchased a few shirts and jeans. The products are of good quality, affordable and worth the purchase.', 'Shahin Sukumar', 'mSquare retail', None),
]

T_LAUNDRY = [
    ('Great service', 'Had a suit dry cleaned here along with a water repellent finish &mdash; looked great. I brought some silk shirts with spots that needed extra finish and they redid them and brought them back to life.', 'Amit Raj Singh', 'Instructional Designer, Simplilearn', 'Amit Raj Singh.png'),
    ('The service was unbelievable', 'The stain on my kid&rsquo;s uniform was stubborn. I was surprised and 100% satisfied with my clothes. One of the few things I truly enjoyed was the detail in which they fold everything, even my socks. I highly recommend them for great customer service and delivery.', 'Pramila D&rsquo;Souza', 'Home maker', "Pramila D'Souza.png"),
    ('They know how to process', 'Blazers, coats, suits &mdash; they handled them perfectly. I gave them my fungus-infected leather jacket to treat and finish, and they absolutely solved the issue with an anti-fungus finish and restoration. Great job.', 'Rishal Rupert Tauro', 'Health and Safety Officer', 'Rishal rupert tauro.png'),
    ('Still no odour after two days', '&ldquo;Here comes another new laundry&rdquo; was my first thought. I still gave it a try. Now I&rsquo;m happy with the quality of the wash and the ironing. I normally change my shirt every day, but I&rsquo;ve worn this one for two days and there&rsquo;s still no odour from sweating. Super happy.', 'Nagesh', 'Entrepreneur', 'Nagesh.png'),
]


# ================================================================ PAGES

def build():
    write_drum()

    # ------------------------------------------------------------ HOME
    home = f'''
<section class="hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="shell">
    <div class="hero-grid">
      <div>
        <h1>
          <span class="h1-a">We wash</span>
          <span class="h1-n">1,00,000</span>
          <span class="h1-c">garments a day</span>
        </h1>
        <p class="lede">Three textile chemistry graduates started in a makeshift shed with 1000 garments a day. Thirty years on, Motherland finishes denim for Inditex, Marks and Spencer, Lacoste and Bestseller &mdash; and customises a single pair of jeans for whoever walks in.</p>
        <div class="acts">
          <a class="btn btn--house" href="motherland-garments.html">See our washes</a>
          <a class="btn btn--line" href="about.html">Our story</a>
        </div>
      </div>
      <figure class="hero-fig">
        <div class="hero-stage stitched">{stage_visual()}</div>
        <div class="hero-leap"><div class="hero-leap-in"><img fetchpriority="high" src="assets/img/leap.webp" alt="A woman in a denim jacket and jeans leaping, arms flung wide" width="584" height="623"></div></div>
        <button class="motion-ico" type="button" data-motion="icon" aria-label="Pause motion"><svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg><svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7z"/></svg></button>
        <figcaption class="ticker" id="ticker" hidden><i aria-hidden="true"></i><span><b>0</b> <span data-word>garments</span> washed since you opened this page, at 1,00,000 a day</span></figcaption>
      </figure>
    </div>
    <ul class="stats">
      <li><b data-to="4">4</b><span>Units across Bangalore and Chennai</span></li>
      <li><b data-to="1000">1,000+</b><span>Customers visit our stores every day</span></li>
      <li><b data-to="200">200+</b><span>Denim alterations and refashions every day</span></li>
      <li><b data-to="100">100+</b><span>Customised jeans every day</span></li>
    </ul>
  </div>
</section>
{LINE}
{APPROVE_MQ}
<section class="band" id="group">
  <div class="shell">
    {sec_head('One supply chain, three ways in', 'Motherland Group is a B2B and B2C apparel solution provider. We manufacture denim and denim accessories, add value with garment washing, sell factory-fresh garments at retail, and customise, alter and refashion denim one pair at a time.')}
    {SHOWCASE}
  </div>
</section>

<section class="band band--raw">
  {DYE}
  <div class="shell">
    {sec_head('Raw indigo in, finished denim out', 'Every effect you see on a pair of jeans &mdash; the fade down the thigh, the contrast at the seam, the softness in the hand &mdash; is put there on purpose, in a machine, by us.')}
    {SWATCH}
    <div class="after"><a class="btn btn--line" href="motherland-garments.html">See all 20 washes and finishes</a></div>
  </div>
</section>

<section class="statement">
  <div class="statement-ph"><img src="{asset('denim-repair-01.jpg')}" alt="The washing floor, with a large industrial machine and a worker in an apron"></div>
  <div class="shell statement-txt">
    <h2>Thirty years of expertise in the garment supply chain</h2>
    <p>A 200-strong team across four units in Bangalore and Chennai, delivering the right quality at the right time, every time.</p>
    <a class="btn btn--white" href="team.html">Meet the whole team</a>
  </div>
</section>

<section class="band">
  <div class="shell">
    {sec_head('Promoted by technocrats')}
    {DIRECTORS}
  </div>
</section>
{clients_band(' band--cotton')}
<section class="band">
  <div class="shell">
    {sec_head('Designers, exporters and people who love their jeans', 'From brand design heads who test our R&amp;D samples, to a customer whose waist went from 42&Prime; to 36&Prime; and wanted three jeans to fit again.')}
    {stage([T_WASH[0], T_DENIM[1], T_RETAIL[0], T_WASH[2], T_LAUNDRY[3], T_DENIM[0]])}
    <div class="after"><a class="btn btn--line" href="testimonials.html">Read all testimonials</a></div>
  </div>
</section>
''' + cta('Tell us what you need done',
          'Whether it&rsquo;s 60,000 garments a day or one pair of jeans that doesn&rsquo;t fit any more.')

    page('index.html',
         'Motherland Group | Garment Washing, Denim Manufacturing &amp; Retail since 1995',
         'Motherland Group washes 1,00,000 garments a day across four units in Bangalore and Chennai. Sustainable garment finishing for Inditex, Marks and Spencer, Lacoste and Bestseller, plus mDenim customisation and mSquare retail.',
         home, 'garment washing bangalore, denim manufacturers, motherland group')

    # ------------------------------------------------------------ ABOUT
    timeline = ''.join(f'<li><b>{y}</b><p>{t}</p></li>' for y, t in TIMELINE)
    about = phero('motherland-01.jpg', 'About',
                  'A makeshift shed in Chennai, 1995',
                  'Three young textile chemistry graduates &mdash; first generation entrepreneurs, fresh from college &mdash; started a tiny washing unit called Jaihind Garments in Guindy, Chennai. A single set of machinery on loan from a chemical supplier. One customer. Five hundred shirts a day.',
                  alt='Industrial tumble driers on the Motherland washing line') + f'''
<section class="band">
  <div class="shell">
    {split('about-mdl.jpg', 'The washing floor at Motherland Garments', """
        <h2>They worked hard with missionary zeal</h2>
        <p class="lede">In 1995 three young textile chemistry graduates, along with a mechanical engineer, started a small garment processing unit in a makeshift shed with a capacity of 1000 garments per day. They nurtured the fledgling unit into a reliable supplier.</p>
        <p class="lede">With sheer hard work and commitment the business started to make a name for itself in Chennai. A lot has changed since. With over 25 years of a customer-focused approach and a continuous quest for quality, Motherland Group today processes over 60,000 garments a day and has diversified into many garment-based B2B and B2C solutions.</p>""")}
  </div>
</section>

<section class="band band--cotton" id="history">
  <div class="shell tl-wrap">
    {sec_head('Thirty years, one line at a time', 'From one loaned machine in Guindy to four units, a denim-only washing plant and a retail chain.')}
    <div class="tl">
      <span class="tl-thread" aria-hidden="true"></span>
      <ol>{timeline}</ol>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell cols2">
    <div>
      <h2>Vision</h2>
      <p class="lede">To be the best apparel solution provider to garment manufacturers, brands, exporters and retail customers &mdash; with the least impact on the planet.</p>
    </div>
    <div>
      <h2>Mission</h2>
      <ul class="ticks">
        <li>Provide a wide variety of garment solutions to garment exporters, brand manufacturers and retail customers.</li>
        <li>Help exporters, brands and manufacturers stay above their competition with sustainable garment washing and manufacturing services.</li>
        <li>Help retail customers get international quality and value for money with a unique product line and denim customisation.</li>
      </ul>
    </div>
  </div>
</section>

<section class="band band--cotton">
  <div class="shell">
    {sec_head('A B2B and B2C apparel solution provider', 'We manufacture denims and denim accessories, add value with our garment washing services, sell at retail, make customised jeans, and alter and refashion old denim.')}
    {SHOWCASE}
  </div>
</section>

<section class="band">
  <div class="shell">
    {sec_head("In their words", 'Promoted by technocrats with 30 years of expertise in the garment supply chain.')}
    {DIRECTORS}
  </div>
</section>
''' + cta('Want to see the plant?', 'We are at Peenya, Magadi Road, Harohalli and Chennai.', 'Arrange a visit')

    page('about.html', 'About Motherland Group | Our story since 1995',
         'From a makeshift shed in Chennai in 1995 to four units processing 60,000 garments a day. The history, vision and mission of Motherland Group.',
         about, 'about motherland group, garment processing history bangalore')

    # ------------------------------------------------ MOTHERLAND GARMENTS
    catalogue = tabset('Washes and finishes', [
        ('p-basic', 'Basic washes', 8, rows(BASIC)),
        ('p-func', 'Functional finishes', 6, rows(FUNC)),
        ('p-corr', 'Correctional finishes', 6, rows(CORR)),
    ])
    mg = phero('denim-repair-01.jpg', 'Garment Washing',
               'Sustainability in garment washing',
               'Adding value to apparel since 1995. Multiple locations at Magadi Road, Peenya, Harohalli and Chennai, with an exclusive denim washing unit at Peenya.',
               alt='The washing floor, with a large industrial machine and a worker in an apron') + f'''
{LINE}
<section class="band">
  <div class="shell">
    {sec_head('Who has approved us, and what we hold')}
    <dl class="spec">
      {spec('Approved by', ['Inditex', 'Marks and Spencer', 'Lacoste', 'Bestseller', 'Varner', 'American Eagle', 'Next'])}
      {spec('Sustainability', ['ZDHC', 'GOTS', 'INCHECK', 'Clearstream', 'EIM', 'Higgs FEM', 'BV E3'])}
      {spec('Certified in', ['ISO 9001', 'ISO 14001', 'OEKO-TEX'])}
      {spec('Functional finish', ['Antimicrobial', 'Antiviral', 'Moisture wicking', 'Water &amp; oil repellent', 'Stain guard', 'UV protection', 'Fragrance', 'Cool finish'])}
    </dl>
  </div>
</section>

<section class="band band--raw">
  {DYE}
  <div class="shell">
    {sec_head('Raw indigo in, finished denim out', 'Every effect on a finished pair of jeans is put there on purpose, in a machine, by us.')}
    {SWATCH}
  </div>
</section>

<section class="band" id="finishes">
  <div class="shell">
    {sec_head('Twenty washes and finishes', 'We carry out different washes based on customer requirements. These are the ones we are asked for most.')}
    {catalogue}
  </div>
</section>

<section class="band band--cotton">
  <div class="shell">
    {split('about-mdl.jpg', 'The washing floor at Motherland Garments', """
        <h2>The science of finishing</h2>
        <p class="lede">The depletion of natural resources affects every one of us. We are committed to doing our bit in changing how we use the planet&rsquo;s fast-depleting resources &mdash; especially water. For sustainable technology in garment finishing and washing we work with the award-winning team at Jeanologia from Spain.</p>
        <p class="tag">Jeanologia Corporative, Spain</p>""")}
  </div>
</section>
{clients_band()}
<section class="band band--cotton">
  <div class="shell">
    {sec_head('Design heads and sourcing teams', 'The people who send us their samples and their bulk.')}
    {voices_grid(T_WASH)}
  </div>
</section>
''' + cta('Send us a sample', 'Tell us the garment, the fabric and the look you are after.', 'Start an enquiry')

    page('motherland-garments.html',
         'Motherland Garments | Sustainable garment washing &amp; finishing, Bangalore',
         'Garment washing and finishing for exporters and brands. 20 washes and finishes, ZDHC and OEKO-TEX certified, approved by Inditex, M&amp;S, Lacoste, Bestseller, Varner, American Eagle and Next.',
         mg, 'garment washing, denim washing bangalore, functional finishes, stone wash, enzyme wash')

    # ------------------------------------------------------------ mDENIM
    md = phero('banner/md-banner-01.jpg', 'mDenim',
               'Don&rsquo;t ever throw away a jean',
               'Alter, re-design, customise. Motherland Group, with over three decades across the apparel value chain, is now into denim alteration, customised denim and denim bag retail &mdash; a denim solution provider across B2C and B2B.',
               '78% center', 'A mother and daughter in denim jackets and jeans, against a pink background') + f'''
<section class="band">
  <div class="shell cols2">
    <div>
      <h2>Our mission</h2>
      <p class="lede">To help people wear premium denim &mdash; by customising a new jean to the right fabric, fit, size and wash, redesigning and altering old denim into new fashion, and creating a unique identity.</p>
    </div>
    <div>
      <h2>Our message</h2>
      <p class="lede">We make unique denim garments individually, to each customer&rsquo;s fabric, fit and look. The customers who love our work are passionate about their denim. Unlike others, we offer our own production facility for handcrafting custom denim and a process house for every wash and finish.</p>
    </div>
  </div>
</section>

<section class="band band--cotton" id="custom">
  <div class="shell">
    {sec_head('Make it, fit it, fade it, fix it', 'In-house sewing, washing and finishing means a single pair gets the same equipment as a 60,000-piece order.')}
    <div class="cols2">
      <div>
        <h3>Denim manufacturing</h3>
        <p>Niche products like denim bags and denim accessories. Our design team works a step ahead of the competition, and in-house sewing, washing and finishing deliver quality denims at the right price. We manufacture denim trousers, shorts and other bottom wear &mdash; and we specialise in denim bags, our core product. But we can do anything that is denim.</p>
      </div>
      <div>
        <h3>Denim customisation</h3>
        <p>Custom-fit trousers and suits are easy to find. A custom denim service is not &mdash; because it isn&rsquo;t just cut, sew and finish. It&rsquo;s choosing the right denim fabric, designing the garment, understanding the shrinkage pattern, sewing on heavy-duty specialised machinery, processing for the right look and feel, then finishing it as you want. Denim is an art and a science, rightly blended.</p>
      </div>
      <div>
        <h3>Denim re-designing</h3>
        <p>Your seldom-worn jean can become your favourite. We restore old, worn jeans into a different pair altogether &mdash; packages that refresh the jean, take away stains, make it bright as new, add new looks, wash-downs, overdyes and more. There are exciting possibilities in your old denim.</p>
      </div>
      <div id="alterations">
        <h3>Denim alterations</h3>
        <p>You buy a brand-new jean, aren&rsquo;t happy with the store&rsquo;s alteration service, find a tailor with great difficulty and still get below-par work, because they aren&rsquo;t equipped for it. mDenim offers professional, technical alteration &mdash; from a length reduction with the original hem to anything else you want done &mdash; on specialised heavy-duty factory equipment, by tailors who understand denim.</p>
      </div>
    </div>
  </div>
</section>

{SEAM}
<section class="band">
  <div class="shell">
    {sec_head('Fifteen ways we can change a denim', 'One-stop solutions for everything you wear.')}
    {rows(ALTERATIONS)}
  </div>
</section>

<section class="band band--cotton">
  <div class="shell">
    {split('denim.jpg', 'Denim being finished by hand on a hanging line', """
        <h2>And washes, because we have in-house manufacturing</h2>
        <p class="lede">Give a new life to your old denim. Professional alteration with the original hem, the fit you want, and many more. Alterations are done on specialised, heavy-duty factory equipment by skilled tailors who understand the nuances of denim.</p>
        <a class="btn btn--house" href="contact.html">Get started now</a>""")}
  </div>
</section>

<section class="band">
  <div class="shell">
    {sec_head('People who are passionate about their denim', 'Bags, alterations and jeans that fit again.')}
    {voices_grid(T_DENIM)}
  </div>
</section>
''' + cta('Bring us your denim', 'Length, waist, taper, rips, patches, a whole new wash &mdash; or a jean built from scratch.', 'Book an alteration')

    page('mdenim.html', 'mDenim | Denim customisation, alteration &amp; refashioning in Bangalore',
         'mDenim customises new jeans to your fabric, fit, size and wash, and alters, repairs and refashions old denim on heavy-duty factory equipment. Denim bags and accessories too.',
         md, 'denim manufacturers in bangalore, denim customisation, denim refashioning, denim alterations')

    # ----------------------------------------------------------- mSQUARE
    stocked = ['Denims', 'Chinos', 'Casual cotton shirts', 'Knits', 'T-shirts', 'Sweatshirts', 'Tracks', 'Joggers', 'Kids', 'Ladies wear', '100% cotton', 'Prewashed']
    stores = ''.join(f'<li>{PIN_SVG}<address>{s}</address></li>' for s in STORES)
    ms = phero('banner/ms-01.jpg', 'mSquare',
               'Factory fresh, five stores, one city',
               'Motherland Group, with its strong presence in garment manufacturing, is also into garment retail under the brand mSquare &mdash; with the expertise of working with top Indian and international brands across menswear, womenswear, kids and babies.',
               '82% center', 'A man in a suit in a wood-panelled mSquare store') + f'''
<section class="band">
  <div class="shell cols2">
    <div>
      <h2>Retail</h2>
      <p>mSquare stores sit at prime locations across Bangalore. In the first year of operations there are already five, well stocked with apparel for every occasion &mdash; formals, semi-casuals and casuals.</p>
      <ul class="chips">{''.join(f'<li>{c}</li>' for c in stocked)}</ul>
    </div>
    <div>
      <h2>Wholesale</h2>
      <p>mSquare also runs a B2B model, offering garments to other retailers with stock in every category at attractive prices.</p>
      <a class="btn btn--line" href="contact.html">Talk wholesale</a>
    </div>
  </div>
</section>

{RACK}
<section class="band band--cotton">
  <div class="shell">
    {sec_head('Five stores, and counting', 'mSquare plans at least 25 stores across Bangalore.')}
    <ul class="stores">{stores}</ul>
  </div>
</section>

<section class="band">
  <div class="shell">
    {split('retails-showroom.jpg', 'Stacked denim inside an mSquare store', """
        <h2>Knits, t-shirts, sweatshirts, tracks, joggers</h2>
        <p class="lede">100% cotton. Prewashed garments. The stores are well stocked with variety for all occasions, and because the garments come off our own finishing lines, the quality is the same one our export customers buy.</p>""")}
  </div>
</section>

<section class="band band--cotton">
  <div class="shell">
    {sec_head('Shoppers who came back', 'And brought the family.')}
    {voices_grid(T_RETAIL)}
  </div>
</section>
''' + cta('Stocking up for your store?', 'We have stock in every category at wholesale prices.', 'Talk wholesale')

    page('msquare.html', 'mSquare | Factory outlet &amp; wholesale garments in Bangalore',
         'mSquare sells factory-fresh garments across five Bangalore stores &mdash; denims, chinos, shirts, knits, t-shirts, tracks, joggers, kids and ladies wear &mdash; and supplies other retailers wholesale.',
         ms, 'best factory outlet in bangalore, factory outlet near me, msquare factory outlet')

    # -------------------------------------------------------------- TEAM
    def person(img, name, role):
        return (f'<figure class="person"><div class="person-ph"><img src="{asset("Photos/" + img)}" alt=""></div>'
                f'<figcaption><b>{name}</b> <small>{role}</small></figcaption></figure>')

    stars = ''.join(
        '<li class="mini"><span class="av">' +
        (f'<img src="{asset("Photos/" + ph)}" alt="">' if ph else f'<span aria-hidden="true">{n[0]}</span>') +
        f'</span><span><b>{n}</b> <small>{r}</small></span></li>'
        for n, r, ph in SUPERSTARS)

    team = phero('team-indigo.jpg', 'Team',
                 'Take care of your people and they take care of your customers',
                 'A 200-strong team focused entirely on giving the customer the best. Creative freedom, continuous learning, personal career growth and employee empowerment are guaranteed in the organisation.',
                 alt='The Motherland Group team, standing together in rows') + f'''
<section class="band">
  <div class="shell">
    {sec_head('The people who built the place', 'Promoted by technocrats with 30 years of expertise in the garment supply chain.')}
    <div class="team-lead">
      {person('a-j-Pandian-Managing-Director.jpg', 'A. J. Pandian', 'Managing Director')}
      {person('s-a-Selvamani-Technical-Director.jpg', 'S. A. Selvamani', 'Technical Director')}
      {person('G.Ramesh Kanna - Director.jpg', 'G. Ramesh Kanna', 'Executive Director')}
    </div>
  </div>
</section>

<section class="band band--cotton">
  <div class="shell">
    {sec_head('The team that runs the day', 'Marketing, accounts, HR, admin, sales and operations.')}
    <ul class="team-grid">{stars}</ul>
  </div>
</section>

<section class="band">
  <div class="shell">
    {sec_head('In their words')}
    {DIRECTORS}
  </div>
</section>
''' + cta('Want to work here?', 'Creative freedom, continuous learning and career growth are guaranteed.', 'Write to us')

    page('team.html', 'Our Team | Motherland Group',
         'A 200-strong team. Meet the management and the people who run the day at Motherland Group.',
         team, 'motherland group team, garment manufacturing management bangalore')

    # ------------------------------------------------------ TESTIMONIALS
    def group(h2, lede, items):
        return sec_head(h2, lede) + voices_grid(items)

    said = [t[0] for t in T_DENIM + T_RETAIL + T_WASH + T_LAUNDRY]
    moving = ''.join(f'<span>{s}</span>' for s in said)

    tst = phero('banner/alter-01.jpg', 'Testimonials',
                'What they say when we are not in the room',
                'Design heads, sourcing teams, shoppers and people who just wanted their jeans to fit again.',
                '88% center', 'Frayed denim laid out with thread, scissors and a measuring tape') + f'''
<div class="mq mq-big" aria-hidden="true"><div class="mq-row">{moving}{moving}</div></div>
<section class="band">
  <div class="shell">
    {tabset('Testimonials by division', [
        ('v-wash', 'Garment washing', len(T_WASH), group('Exporters and design teams', 'The people who send us their samples and their bulk.', T_WASH)),
        ('v-denim', 'mDenim', len(T_DENIM), group('Denim people', 'Bags, alterations and jeans that fit again.', T_DENIM)),
        ('v-retail', 'mSquare', len(T_RETAIL), group('Shoppers', 'Who came back, and brought the family.', T_RETAIL)),
        ('v-care', 'Laundry and care', len(T_LAUNDRY), group('Garment care', 'Dry cleaning, finishes and restoration.', T_LAUNDRY)),
    ], ' tabs--4')}
  </div>
</section>
''' + cta('Want to be the next one?', 'Tell us what you need and we will come back within a working day.')

    page('testimonials.html', 'Testimonials | Motherland Group',
         'What exporters, designers, shoppers and denim customers say about Motherland Garments, mDenim and mSquare.',
         tst, 'motherland group reviews, testimonials')

    # ----------------------------------------------------------- CONTACT
    store_list = ''.join(f'<li>{s}</li>' for s in STORES)
    contact = phero(None, 'Contact',
                    'Tell us what you need done',
                    'Whether it&rsquo;s 60,000 garments a day or one pair of jeans that doesn&rsquo;t fit any more &mdash; send us the details and our team will come back to you.',
                    visual=f'<div class="phero-stage">{stage_visual()}</div>') + f'''
<section class="band c-band">
  <div class="shell c-grid">
    <form class="c-form" id="enquiry">
      <div class="fields">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="f-company">Company <small>(optional)</small></label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@company.com" required></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+91" required></div>
        <div class="field wide"><label for="f-int">What do you need?</label>
          <select id="f-int" name="interest">
            <option>Garment washing &amp; finishing (bulk)</option>
            <option>Denim manufacturing</option>
            <option>Denim customisation</option>
            <option>Denim alteration or refashion</option>
            <option>mSquare retail</option>
            <option>mSquare wholesale</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="field wide"><label for="f-msg">Details</label><textarea id="f-msg" name="message" placeholder="Garment type, quantity, finish, timeline: whatever you already know." required></textarea></div>
      </div>
      <button class="btn btn--house" type="submit">Send enquiry</button>
      <p class="form-note" id="formNote" role="status">We reply within one working day.</p>
    </form>

    <div class="c-info">
      <div class="c-line"><span class="c-ic">{PHONE_SVG}</span><div><h2>Phone</h2><a href="{TEL}">+91 93422 50766</a><a href="{TEL_2}">+91 97400 44100</a></div></div>
      <div class="c-line"><span class="c-ic">{MAIL_SVG}</span><div><h2>Email</h2><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
      <div class="c-line"><span class="c-ic">{PIN_SVG}</span><div><h2>Head office</h2><address>{ADDRESS}</address></div></div>
      <div class="c-line"><span class="c-ic">{PLANT_SVG}</span><div><h2>Units</h2><p>Magadi Road, Peenya, Harohalli and Chennai</p><small>Exclusive denim washing unit at Peenya</small></div></div>
      <div class="c-line"><span class="c-ic">{STORE_SVG}</span><div><h2>mSquare stores</h2><ul class="c-stores">{store_list}</ul></div></div>
    </div>
  </div>
</section>'''

    page('contact.html', 'Contact Motherland Group | Peenya, Bengaluru',
         'Get in touch with Motherland Group for garment washing, denim manufacturing, customisation, alteration, retail and wholesale. Peenya, Bengaluru.',
         contact, 'contact motherland group, garment washing enquiry bangalore')

    # ------------------------------------------------------ LEGAL PAGES
    def legal(fname, crumb, title, blocks, desc):
        body = phero(None, crumb, title) + '''
<section class="band">
  <div class="shell prose">''' + ''.join(f'<h2>{h}</h2><p>{b}</p>' for h, b in blocks) + '''
  </div>
</section>'''
        page(fname, f'{title} | Motherland Group', desc, body)

    legal('terms.html', 'Terms', 'Terms &amp; Conditions', [
        ('Use of this site', 'This website is operated by Motherland Garments Private Limited. By accessing it you agree to these terms. Content, images and marks on this site belong to Motherland Group and may not be reproduced without written permission.'),
        ('Services and quotations', 'Descriptions of washes, finishes and services on this site are indicative. Exact process routes, lead times and prices are confirmed in writing against each order, after sample approval.'),
        ('Liability', 'We take every care in processing garments entrusted to us. Liability for any garment is limited to the processing value of that garment, unless otherwise agreed in a signed contract.'),
        ('Contact', 'Questions about these terms can be sent to blr@motherlandgroup.com or by post to #40-B, 2nd Phase, Peenya Industrial Area, Bengaluru, Karnataka 560058.'),
    ], 'Terms and conditions for using the Motherland Group website and services.')

    legal('privacy.html', 'Privacy', 'Privacy Policy', [
        ('What we collect', 'When you send an enquiry through this site we receive the name, company, email address, phone number and message you choose to give us. We do not collect anything else about you.'),
        ('How we use it', 'We use your details only to answer your enquiry and to follow up about the work you asked about. We do not sell or rent your information to anyone.'),
        ('Cookies', 'This site does not set tracking or advertising cookies. Fonts are loaded from Google Fonts, which may log the request.'),
        ('Your choices', 'Write to blr@motherlandgroup.com at any time to ask what we hold about you, to correct it, or to have it deleted.'),
    ], 'How Motherland Group handles the information you send through this website.')

    check_links()
    print('built:', ', '.join(sorted(f for f in os.listdir(OUT) if f.endswith('.html'))))


def check_links():
    """Fail the build rather than ship a dead link: every local file and #anchor a page names must exist."""
    pages = {os.path.basename(p): io.open(p, encoding='utf-8').read() for p in glob.glob(os.path.join(OUT, '*.html'))}
    ids = {name: set(re.findall(r'\sid="([^"]+)"', html)) for name, html in pages.items()}
    broken = []
    for name, html in pages.items():
        for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
            if re.match(r'[a-z]+:', ref):
                continue
            path, _, anchor = ref.partition('#')
            target = path or name
            if path and not os.path.exists(os.path.join(OUT, unquote(path))):
                broken.append(f'{name}: {ref}')
            elif anchor and anchor not in ids.get(target, ()):
                broken.append(f'{name}: {ref} (no such anchor)')
    assert not broken, 'broken links:\n  ' + '\n  '.join(sorted(set(broken)))


if __name__ == '__main__':
    build()
