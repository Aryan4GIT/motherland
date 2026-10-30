#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates the Motherland Group site into the repo root.
Pages live at the root so static hosts (Vercel, GitHub Pages, Netlify)
serve them with no configuration.
One source of truth for the chrome; each page supplies only its body.
Run:  python build.py
"""
import os, io

OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ('index.html',               'Home'),
    ('about.html',               'About Group'),
    ('motherland-garments.html', 'Garment Washing'),
    ('mdenim.html',              'mDenim'),
    ('msquare.html',             'mSquare'),
    ('team.html',                'Team'),
    ('testimonials.html',        'Testimonials'),
]

PHONE_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')
MAIL_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
            '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>')


def head(title, desc, keywords=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Sora:wght@200..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/premium.css">
</head>
<body>

<div class="aura" aria-hidden="true"><b></b><b></b><b></b></div>
<div class="grain" aria-hidden="true"></div>
<div id="prog" aria-hidden="true"></div>
<div class="cur" aria-hidden="true"></div>
<div class="cur-d" aria-hidden="true"></div>

<div id="boot">
  <div>
    <div class="boot-mark">MOTHERLAND</div>
    <div class="boot-bar"><i></i></div>
  </div>
</div>
'''


def topbar(current):
    def item(href, label):
        cls = ' class="on"' if href == current else ''
        return '<a href="%s"%s>%s</a>' % (href, cls, label)

    blog = '<a href="http://blog.motherlandgroup.com/" target="_blank" rel="noopener">Blog</a>'
    links = ''.join(item(h, l) for h, l in NAV) + blog
    drawer = ''.join(item(h, l) for h, l in NAV) + blog
    drawer += '<a href="contact.html">Contact</a>'

    return f'''
<div class="topbar" id="topbar">
<div class="strip">
  <div class="shell">
    <a href="tel:+919342250766">{PHONE_SVG} +91 93422 50766 / +91 97400 44100</a>
    <a href="mailto:blr@motherlandgroup.com">{MAIL_SVG} blr@motherlandgroup.com</a>
  </div>
</div>

<header class="nav" id="nav">
  <div class="shell nav-in">
    <a class="brand" href="index.html">
      <img src="assets/img/mark.png" alt="Motherland Group">
      <b>MOTHERLAND<span>GROUP &middot; SINCE 1995</span></b>
    </a>
    <nav class="nav-links" id="navLinks">{links}</nav>
    <a class="btn btn--house nav-cta" href="contact.html"><span class="dot"></span>Talk to us</a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><i></i><i></i><i></i></button>
  </div>
</header>
</div>

<aside class="drawer" id="drawer">
  {drawer}
  <a class="btn btn--house" href="contact.html"><span class="dot"></span>Talk to us</a>
</aside>
'''


FOOT = '''
<footer class="foot">
  <div class="shell">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/mark.png" alt="Motherland Group"><b>MOTHERLAND<span>GROUP &middot; SINCE 1995</span></b></a>
        <p class="about">In 1995 three young textile chemistry graduates, along with a mechanical engineer, started a small garment processing unit in a makeshift shed with a capacity of 1000 garments per day. They worked hard with missionary zeal and nurtured the fledgling unit into a reliable supplier.</p>
        <div class="socials">
          <a href="https://www.facebook.com/motherlandgarments/" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1Z"/></svg></a>
          <a href="https://www.linkedin.com/in/motherland-group-76b9b1184/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm7 0h3.8v1.7h.05c.53-1 1.82-2.05 3.75-2.05C21.6 8.65 23 10.9 23 14.2V21h-4v-6c0-1.43-.03-3.27-2-3.27-2 0-2.3 1.56-2.3 3.17V21h-4V9Z"/></svg></a>
          <a href="mailto:blr@motherlandgroup.com" aria-label="Email"><svg viewBox="0 0 24 24"><path d="M2 5h20v14H2V5Zm2 2v.5l8 5 8-5V7H4Z"/></svg></a>
        </div>
      </div>

      <div>
        <h5>QUICK LINKS</h5>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="about.html#history">Our history</a></li>
          <li><a href="team.html">Our team</a></li>
          <li><a href="testimonials.html">Testimonials</a></li>
          <li><a href="contact.html">Contact us</a></li>
        </ul>
      </div>

      <div>
        <h5>SERVICES</h5>
        <ul>
          <li><a href="motherland-garments.html">Garment washing</a></li>
          <li><a href="motherland-garments.html#finishes">Functional finishes</a></li>
          <li><a href="mdenim.html">Denim manufacturing</a></li>
          <li><a href="mdenim.html#custom">Denim customisation</a></li>
          <li><a href="mdenim.html#alterations">Alteration &amp; refashion</a></li>
          <li><a href="msquare.html">Retail &amp; wholesale</a></li>
        </ul>
      </div>

      <div>
        <h5>GET IN TOUCH</h5>
        <p class="about" style="margin-bottom:14px">#40-B, 2nd Phase, Peenya Industrial Area, Bengaluru, Karnataka 560058</p>
        <ul>
          <li><a href="tel:+919342250766">+91 93422 50766</a></li>
          <li><a href="tel:+919740044100">+91 97400 44100</a></li>
          <li><a href="mailto:blr@motherlandgroup.com">blr@motherlandgroup.com</a></li>
          <li><a href="http://blog.motherlandgroup.com/" target="_blank" rel="noopener">Blog</a></li>
        </ul>
      </div>
    </div>

    <div class="foot-mark" aria-hidden="true">MOTHERLAND</div>

    <div class="foot-base">
      <span>Copyright &copy; 2021 All rights reserved by motherlandgroup.com</span>
      <span class="lnks"><a href="terms.html">Terms &amp; Conditions</a><a href="privacy.html">Privacy Policy</a></span>
    </div>
  </div>
</footer>

<div class="fab">
  <a href="tel:+919342250766" aria-label="Call Motherland Group">''' + PHONE_SVG + '''</a>
  <a class="up" id="toTop" href="#top" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m18 15-6-6-6 6"/></svg></a>
</div>

<script type="module" src="assets/js/app.js"></script>
</body>
</html>
'''


def page(fname, title, desc, body, keywords=''):
    html = head(title, desc, keywords) + topbar(fname) + '<main id="top">' + body + '</main>' + FOOT
    with io.open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        f.write(html)
    return fname


# ---------------------------------------------------------------- partials

# The banners range from a near-white flat-lay to a dim factory floor
# (measured mean luminance in brackets). On the light ground they all have
# to carry the same weight under the veil, so each is pulled toward ~112.
BANNER_DIM = {
    'banner/alter-01.jpg':     .53,   # [208] threads on white
    'motherland-01.jpg':       .58,   # [189] drier line, bright
    'banner/md-banner-01.jpg': .60,   # [184] studio shot on white
    'team.jpg':                .80,   # [140]
    'about-mdl.jpg':          1.08,   # [101]
    'denim-repair-01.jpg':    1.10,   # [94]
    'banner/ms-01.jpg':       1.60,   # [66]  dark store interior
}


def phero(img, crumb, h1, lede, pos='center', dim=''):
    """Compact banner for inner pages. `dim` overrides the normalised grade."""
    if not dim and img in BANNER_DIM:
        dim = 'saturate(.7) contrast(1.06) brightness(%s)' % BANNER_DIM[img]
    extra = (';filter:' + dim) if dim else ''
    return f'''
<section class="phero">
  <div class="phero-bg" style="background-image:url('assets/img/{img}');background-position:{pos}{extra}"></div>
  <div class="phero-veil"></div>
  <div class="shell">
    <nav class="crumb"><a href="index.html">Home</a><span>&rsaquo;</span><b>{crumb}</b></nav>
    <h1 data-split>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>'''


def sec_head(kicker, h2, lede):
    return f'''
    <div class="sec-head">
      <div>
        <p class="kicker rv">{kicker}</p>
        <h2 class="h-sec" data-split>{h2}</h2>
      </div>
      <p class="lede rv">{lede}</p>
    </div>'''


def wash_card(title, icon, text):
    return (f'<article class="wash glass spot tilt"><div class="top"><h4>{title}</h4>'
            f'<img src="assets/img/icons/{icon}.png" alt=""></div><p>{text}</p></article>')


def voice(head, text, name, co, img=None):
    av = (f'<img src="assets/img/customers/{img}" alt="">' if img else
          f'<span class="ini">{name[0]}</span>')
    return f'''<article class="voice glass spot rv">
          <span class="q">&ldquo;</span>
          <h5>{head}</h5>
          <p>{text}</p>
          <div class="who">{av}<div><div class="nm">{name}</div><div class="cp">{co}</div></div></div>
        </article>'''


APPROVALS = ['INDITEX', 'MARKS AND SPENCER', 'LACOSTE', 'BESTSELLER', 'VARNER',
             'AMERICAN EAGLE OUTFITTERS', 'NEXT']

APPROVE_MQ = ('<div class="mq approve" aria-label="Brands that have approved Motherland Garments">'
              '<div class="mq-row" data-mq="-0.45">'
              + ''.join(f'<span class="mq-item">{b}</span>' for b in APPROVALS) * 2
              + '</div></div>')

CLIENT_LOGOS = [('Aditya.jpg', 'Aditya Birla'), ('Arvind.jpg', 'Arvind'), ('Derby.jpg', 'Derby'),
                ('HHEC.jpg', 'HHEC'), ('Hasbro.jpg', 'Hasbro'), ('Indus.jpg', 'Indus'),
                ('Lawernce.jpg', 'Lawrence &amp; Mayo'), ('Pearl.jpg', 'Pearl Global')]

CLIENTS_BAND = '''
<section class="band band--tight">
  <div class="shell">
    <p class="kicker rv">OUR CLIENTS</p>
    <h2 class="h-sub" data-split>Exporters and brands who send us their garments</h2>
  </div>
  <div class="mq logo-row">
    <div class="mq-row" data-mq="0.35">''' + ''.join(
    f'<span class="mq-item"><img src="assets/img/clients/{f}" alt="{a}"></span>'
    for f, a in CLIENT_LOGOS) * 2 + '''</div>
  </div>
</section>'''


def cta(line, sub, label='Talk to us', href='contact.html'):
    return f'''
<section class="band band--tight">
  <div class="shell">
    <div class="cta-band glass rv">
      <div>
        <h2 class="h-sub" data-split>{line}</h2>
        <p class="lede" style="margin-top:12px">{sub}</p>
      </div>
      <a class="btn btn--house" href="{href}"><span class="dot"></span>{label}</a>
    </div>
  </div>
</section>'''


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
    ('Thejaswini', 'MARKETING', None), ('Mamatha', 'ACCOUNTANT', None),
    ('Bindushree', 'HUMAN RESOURCES', None), ('Asha', 'ADMIN', None),
    ('Manjunatha R', 'ADMIN', 'Manjunatha R.jpg'), ('Andiswamy', 'SALES', None),
    ('Mahesh S', 'OPERATION', None), ('Myliraj R', 'OPERATION', 'Myliraj R.jpg'),
    ('Gowda BL', 'SALES', None),
]

# testimonials: (heading, body, name, company, photo)
T_WASH = [
    ('Innovative techniques', 'Motherland have a separate R&amp;D team and very nice wash effects by them, and innovative techniques. We would like to explore more with Motherland.', 'Leena Anand', 'HOD DESIGNS &middot; K. MOHAN &amp; CO', 'leena.png'),
    ('Happy with Motherland', 'We are happy with the samples &mdash; they came out good enough as per the originals, and we got them within the targeted date.', 'Sharika', 'DESIGNER &middot; RIVERA CREATION', 'sharika.png'),
    ('Especially the SQUMA effect', 'Motherland R&amp;D new development samples are simply splendid, especially the SQUMA effect. These days designers look forward to innovative and SQUMA contrast looks in denim.', 'Babul Arya', 'DESIGNER &middot; YA APPARELS', 'arya.png'),
    ('Great products', 'Really, I&rsquo;m going to have to leave &ldquo;awesome&rdquo; on every order. I&rsquo;d like to thank all the staff at Motherland Garments for their help &mdash; from the owner to customer service, sales, shipping and receiving. Great products. My clients love them.', 'Anjibabu', 'E-LAND GROUP', None),
    ('Prompt on every commitment', 'We came to know about Motherland Laundry of Bangalore through a reliable source. We were looking for a good laundry in Bangalore and found it in Motherland. They are very prompt in their pick-up and delivery commitments, with a sincere, hardworking and dedicated team. All the best to your team going forward.', 'Thomas Malakkaran', 'USHA GARMENTS', None),
]

T_DENIM = [
    ('Everyone asks me where I got it', 'I am thankful to mDenim for the bag I bought last month. I am so happy with it and all my colleagues ask me where I got it &mdash; because it&rsquo;s a beautiful design at a reasonable price. Trust me, the bag designs are marvellous; you&rsquo;ll know once it&rsquo;s on your shoulder.', 'Alankrita Chordia', 'mDENIM BAGS', None),
    ('Now the fitting is excellent', 'My waist size reduced from 42&Prime; to 36&Prime;. I had three jeans that needed re-altering to my fit. I found mDenim through a Google search, contacted Anisha, explained what I needed, went in person, and the tailor took measurements and re-altered the jeans. Now the fitting is excellent. Their service is excellent and they did amazing work.', 'Vijayanagaram Srihari', 'mDENIM ALTERATION', None),
    ('The bag is mind blowing', 'mDenim team, you amazed me with the bag. I especially appreciate the person who guided me through all the fabric work that went into it. At home my sister and mum use the one-sided bag for everything. Everyone should try these bags &mdash; the design is very good, it&rsquo;s unisex, the stitching is finely done, and the price is reasonable.', 'Anamika Varshney', 'mDENIM BAGS', None),
    ('Still using it for my laptop', 'Thank you so much mDenim. You gave me really good service for my clothes washing, and the bag I bought recently is very usable for daily purposes. I am still using it for my laptop and other things and have not found a single fault in the stitching. A very unique and marvellous design.', 'Sridhar Yerimgere', 'mDENIM BAGS', None),
]

T_RETAIL = [
    ('Never seen these prices anywhere else', 'High quality products at the lowest prices, never seen anywhere else. I have shopped many times and the family members I referred are also happily shopping.', 'Vijay Kumar', 'mSQUARE RETAIL', None),
    ('Such lovely selections', 'What a beautiful store and such lovely selections. I bought gifts to take home at reasonable prices and couldn&rsquo;t resist a few items for myself. I&rsquo;m so glad to have experienced this store and this style of India &mdash; highly recommend.', 'Yathiraju GN', 'mSQUARE RETAIL', None),
    ('Every purchase has been perfect', 'Every purchase I have made has been perfect. The items are quality and well made. I have also bought my daughter a couple of outfits and she loves them. I highly recommend this awesome business.', 'Mohan Sarangapani', 'mSQUARE RETAIL', None),
    ('Worth the purchase', 'Purchased a few shirts and jeans. The products are of good quality, affordable and worth the purchase.', 'Shahin Sukumar', 'mSQUARE RETAIL', None),
]

T_LAUNDRY = [
    ('Great service', 'Had a suit dry cleaned here along with a water repellent finish &mdash; looked great. I brought some silk shirts with spots that needed extra finish and they redid them and brought them back to life.', 'Amit Raj Singh', 'INSTRUCTIONAL DESIGNER AT SIMPLILEARN', 'Amit Raj Singh.png'),
    ('The service was unbelievable', 'The stain on my kid&rsquo;s uniform was stubborn. I was surprised and 100% satisfied with my clothes. One of the few things I truly enjoyed was the detail in which they fold everything, even my socks. I highly recommend them for great customer service and delivery.', 'Pramila D&rsquo;Souza', 'HOME MAKER', "Pramila D'Souza.png"),
    ('They know how to process', 'Blazers, coats, suits &mdash; they handled them perfectly. I gave them my fungus-infected leather jacket to treat and finish, and they absolutely solved the issue with an anti-fungus finish and restoration. Great job.', 'Rishal Rupert Tauro', 'HEALTH &amp; SAFETY OFFICER', 'Rishal rupert tauro.png'),
    ('Still no odour after two days', '&ldquo;Here comes another new laundry&rdquo; was my first thought. I still gave it a try. Now I&rsquo;m happy with the quality of the wash and the ironing. I normally change my shirt every day, but I&rsquo;ve worn this one for two days and there&rsquo;s still no odour from sweating. Super happy.', 'Nagesh', 'ENTREPRENEUR', 'Nagesh.png'),
]


def voices_grid(items, cols=3):
    cells = [[] for _ in range(cols)]
    for i, t in enumerate(items):
        cells[i % cols].append(voice(*t))
    return ('<div class="voices">' +
            ''.join('<div class="vcol">' + ''.join(c) + '</div>' for c in cells) +
            '</div>')


WASH_DEMO = '''
    <div class="demo rv" id="demo">
      <div class="demo-l demo-raw"><img src="assets/img/denim.jpg" alt="Raw indigo denim before washing"></div>
      <div class="demo-l demo-wash" id="demoWash"><img src="assets/img/denim.jpg" alt="The same denim after a wash-down"></div>
      <span class="demo-bar" id="demoBar"><span class="demo-knob">
        <svg viewBox="0 0 24 24"><path d="m9 6-6 6 6 6"/><path d="m15 6 6 6-6 6"/></svg>
      </span></span>
      <span class="demo-tag l">RAW FROM THE LINE</span>
      <span class="demo-tag r">AFTER THE WASH</span>
      <span class="demo-hint">DRAG TO WASH IT DOWN</span>
    </div>'''


# ================================================================ PAGES

def build():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    # ------------------------------------------------------------ HOME
    home = '''
<section class="hero">
  <div class="hero-bg" id="heroBg"></div>
  <div class="hero-veil"></div>
  <div class="shell">
    <div class="hero-grid">
      <div class="hero-copy">
        <div class="hero-tag" id="heroTag"><em>SINCE 1995</em> Bangalore &middot; Chennai &middot; 4 units</div>
        <h1>
          <span class="solid" id="h1a">We wash</span>
          <span class="wash" id="h1b">1,00,000</span>
          <span class="solid" id="h1c">garments a day</span>
        </h1>
        <div class="hero-line" id="heroLine"></div>
        <p class="lede" id="heroLede">Three textile chemistry graduates started in a makeshift shed with 1000 garments a day. Thirty years on, Motherland finishes denim for Inditex, Marks and Spencer, Lacoste and Bestseller &mdash; and customises a single pair of jeans for whoever walks in.</p>
        <div class="hero-acts" id="heroActs">
          <a class="btn btn--house" href="motherland-garments.html"><span class="dot"></span>See what we can do to a garment</a>
          <a class="btn btn--ghost" href="about.html">Our story</a>
        </div>
      </div>
    </div>

    <div class="counters" id="counters">
      <div class="ctr glass spot"><span class="r"></span><div class="n" data-to="100000" data-fmt="in">0</div><div class="l">Garments washed every day</div></div>
      <div class="ctr glass spot"><span class="r"></span><div class="n" data-to="1000">0</div><div class="l">Customers visit our stores every day</div></div>
      <div class="ctr glass spot"><span class="r"></span><div class="n" data-to="200">0</div><div class="l">Denim alterations &amp; refashions every day</div></div>
      <div class="ctr glass spot"><span class="r"></span><div class="n" data-to="100">0</div><div class="l">Customised jeans every day</div></div>
    </div>
  </div>
  <div class="scroll-hint" id="scrollHint">SCROLL<i></i></div>
</section>
''' + APPROVE_MQ + '''
<section class="band" id="group">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'THE GROUP', 'One supply chain,<br>three ways in',
        'Motherland Group is a B2B and B2C apparel solution provider. We manufacture denim and denim accessories, add value with garment washing, sell factory-fresh garments at retail, and customise, alter and refashion denim one pair at a time.') + '''
    <div class="showcase" id="showcase">
      <article class="sc open" tabindex="0">
        <img src="assets/img/motherland-01.jpg" alt="Industrial tumble driers on the Motherland washing line">
        <span class="veil"></span><span class="tagi">B2B</span>
        <div class="sc-body">
          <span class="sc-no">UNIT 01</span>
          <h3>Motherland Garments</h3>
          <div class="sub">Washing &middot; Finishing &middot; Value addition</div>
          <div class="sc-more">
            <p>Four units across Bangalore and Chennai serving almost every leading garment exporter and domestic brand. From 1000 garments a day in 1995 to a 60,000-a-day capacity.</p>
            <a class="sc-link" href="motherland-garments.html">Explore washing <i>&rarr;</i></a>
          </div>
        </div>
      </article>
      <article class="sc" tabindex="0">
        <img src="assets/img/denim.jpg" alt="Hand-finishing raw denim at mDenim">
        <span class="veil"></span><span class="tagi">B2C &amp; B2B</span>
        <div class="sc-body">
          <span class="sc-no">UNIT 02</span>
          <h3>mDenim</h3>
          <div class="sub">Manufacturing &middot; Customisation &middot; Alterations</div>
          <div class="sc-more">
            <p>Not only your suits and coats can be tailored &mdash; your denim can too, in a variety of designs and washes. We also repair, alter and refashion old denim professionally.</p>
            <a class="sc-link" href="mdenim.html">Explore mDenim <i>&rarr;</i></a>
          </div>
        </div>
      </article>
      <article class="sc" tabindex="0">
        <img src="assets/img/retails-showroom.jpg" alt="mSquare retail store interior">
        <span class="veil"></span><span class="tagi">RETAIL</span>
        <div class="sc-body">
          <span class="sc-no">UNIT 03</span>
          <h3>mSquare</h3>
          <div class="sub">Retail &middot; Wholesale</div>
          <div class="sc-more">
            <p>Five stores across Bangalore stocked with factory-fresh denims, chinos, casual shirts, knits, tees, tracks, joggers, kids and ladies wear in the latest fabrics, fits and washes.</p>
            <a class="sc-link" href="msquare.html">Explore mSquare <i>&rarr;</i></a>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">''' + sec_head(
        'WHAT A WASH DOES', 'Raw indigo in,<br>finished denim out',
        'Every effect you see on a pair of jeans &mdash; the fade down the thigh, the contrast at the seam, the softness in the hand &mdash; is put there on purpose, in a machine, by us. Drag the handle.') + WASH_DEMO + '''
    <div style="margin-top:34px"><a class="btn btn--ghost" href="motherland-garments.html">See all 20 washes and finishes</a></div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'PEOPLE', 'Promoted by technocrats',
        'Thirty years of expertise in the garment supply chain. Behind the group is a team that grew with the business and has delivered the right quality at the right time, every time.') + '''
    <div class="dirs">
      <article class="dir glass spot rv">
        <img src="assets/img/Photos/pandiyan.jpg" alt="A. J. Pandian, Managing Director">
        <div>
          <h4>A. J. Pandian</h4>
          <div class="role">MANAGING DIRECTOR</div>
          <blockquote>Motherland believes in the philosophy of WIN WIN WIN &mdash; for a successful business all the stakeholders, customer, employees and the business owner, should win. It is happy employees who ensure customer satisfaction and thereby guarantee a successful business.</blockquote>
        </div>
      </article>
      <article class="dir glass spot rv">
        <img src="assets/img/Photos/selvamani.jpg" alt="S. A. Selvamani, Technical Director">
        <div>
          <h4>S. A. Selvamani</h4>
          <div class="role">TECHNICAL DIRECTOR</div>
          <blockquote>Sustainability is the core of all our beliefs and it is reflected in the way we work &mdash; from sourcing non-hazardous chemicals and auxiliaries, to less water and energy consuming equipment, to investing in new technologies that reduce our impact on the environment.</blockquote>
        </div>
      </article>
    </div>
    <div style="margin-top:28px"><a class="btn btn--ghost" href="team.html">Meet the whole team</a></div>
  </div>
</section>
''' + CLIENTS_BAND + '''
<section class="band">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'WHAT THEY SAY', 'Designers, exporters<br>and people who love<br>their jeans',
        'From brand design heads who test our R&amp;D samples, to a customer whose waist went from 42&Prime; to 36&Prime; and wanted three jeans to fit again.') + voices_grid(
        [T_WASH[0], T_DENIM[1], T_RETAIL[0], T_WASH[2], T_LAUNDRY[3], T_DENIM[0]]) + '''
    <div style="margin-top:30px"><a class="btn btn--ghost" href="testimonials.html">Read all testimonials</a></div>
  </div>
</section>
''' + cta('Tell us what you need done',
          'Whether it&rsquo;s 60,000 garments a day or one pair of jeans that doesn&rsquo;t fit any more.')

    page('index.html',
         'Motherland Group | Garment Washing, Denim Manufacturing &amp; Retail since 1995',
         'Motherland Group washes 1,00,000 garments a day across four units in Bangalore and Chennai. Sustainable garment finishing for Inditex, Marks and Spencer, Lacoste and Bestseller, plus mDenim customisation and mSquare retail.',
         home, 'garment washing bangalore, denim manufacturers, motherland group')

    # ------------------------------------------------------------ ABOUT
    about = phero('motherland-01.jpg', 'About Group',
                  'A makeshift shed<br>in Chennai, 1995',
                  'Three young textile chemistry graduates &mdash; first generation entrepreneurs, fresh from college &mdash; started a tiny washing unit called Jaihind Garments in Guindy, Chennai. A single set of machinery on loan from a chemical supplier. One customer. Five hundred shirts a day.') + '''
<section class="band">
  <div class="shell">
    <div class="split-img rv">
      <div class="si-txt">
        <p class="kicker">KNOW MORE ABOUT US</p>
        <h2 class="h-sub" data-split>They worked hard with missionary zeal</h2>
        <p class="lede">In 1995 three young textile chemistry graduates, along with a mechanical engineer, started a small garment processing unit in a makeshift shed with a capacity of 1000 garments per day. They nurtured the fledgling unit into a reliable supplier.</p>
        <p class="lede">With sheer hard work and commitment the business started to make a name for itself in Chennai. A lot has changed since. With over 25 years of a customer-focused approach and a continuous quest for quality, Motherland Group today processes over 60,000 garments a day and has diversified into many garment-based B2B and B2C solutions.</p>
      </div>
      <div class="si-ph"><img src="assets/img/about-mdl.jpg" alt="The washing floor at Motherland Garments"></div>
    </div>
  </div>
</section>

<section class="band" id="history">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'OUR HISTORY', 'Thirty years,<br>one line at a time',
        'From one loaned machine in Guindy to four units, a denim-only washing plant and a retail chain. Drag the line to move through it.') + '''
    <div class="rail" id="rail">
      <div class="rail-track">''' + ''.join(
        f'<article class="stop glass spot"><div class="yr">{y}</div><p>{t}</p></article>'
        for y, t in TIMELINE) + '''</div>
    </div>

    <div class="vm">
      <article class="vm-card glass spot rv">
        <span class="glow" style="background:var(--crimson)"></span>
        <h3>Vision</h3>
        <p class="lede">To be the best apparel solution provider to garment manufacturers, brands, exporters and retail customers &mdash; with the least impact on the planet.</p>
      </article>
      <article class="vm-card glass spot rv">
        <span class="glow" style="background:var(--indigo)"></span>
        <h3>Mission</h3>
        <ul>
          <li>Provide a wide variety of garment solutions to garment exporters, brand manufacturers and retail customers.</li>
          <li>Help exporters, brands and manufacturers stay above their competition with sustainable garment washing and manufacturing services.</li>
          <li>Help retail customers get international quality and value for money with a unique product line and denim customisation.</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'OUR SERVICES', 'A B2B and B2C<br>apparel solution provider',
        'We manufacture denims and denim accessories, add value with our garment washing services, sell at retail, make customised jeans, and alter and refashion old denim.') + '''
    <div class="divs">
      <article class="div-card rv">
        <div class="ph"><img src="assets/img/motherland-01.jpg" alt="Motherland Garments washing line"></div>
        <div class="div-body">
          <span class="tagi">B2B</span>
          <h3>Motherland Garments</h3>
          <div class="sub">Washing &middot; Finishing</div>
          <p>Four units in Bangalore and Chennai serving almost all leading garment exporters and domestic brands. From a humble 1000 garments per day in 1995 to a 60,000-per-day capacity.</p>
          <a class="div-link" href="motherland-garments.html">Know more <i>&rarr;</i></a>
        </div>
      </article>
      <article class="div-card rv">
        <div class="ph"><img src="assets/img/denim.jpg" alt="mDenim customisation"></div>
        <div class="div-body">
          <span class="tagi">B2C &amp; B2B</span>
          <h3>mDenim</h3>
          <div class="sub">Customisation &middot; Alterations</div>
          <p>Good news to all denim lovers and haters. It is not only your suits and coats that can be custom tailored &mdash; your denim can be too, in a variety of designs and washes. We also repair, alter and refashion your denims professionally.</p>
          <a class="div-link" href="mdenim.html">Know more <i>&rarr;</i></a>
        </div>
      </article>
      <article class="div-card rv">
        <div class="ph"><img src="assets/img/retails-showroom.jpg" alt="mSquare retail store"></div>
        <div class="div-body">
          <span class="tagi">RETAIL</span>
          <h3>mSquare</h3>
          <div class="sub">Retail store</div>
          <p>Apparel retail with locations across Bangalore, offering the best of factory-fresh garments in the latest fabrics, fits, designs and washes &mdash; denims, chinos, casual cotton shirts, knits, t-shirts, tracks, joggers, kids and ladies wear.</p>
          <a class="div-link" href="msquare.html">Know more <i>&rarr;</i></a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">''' + sec_head(
        'DIRECTORS&rsquo; MESSAGE', 'In their words',
        'Promoted by technocrats with 30 years of expertise in the garment supply chain.') + '''
    <div class="dirs">
      <article class="dir glass spot rv">
        <img src="assets/img/Photos/pandiyan.jpg" alt="A. J. Pandian">
        <div>
          <h4>A. J. Pandian</h4>
          <div class="role">MANAGING DIRECTOR</div>
          <blockquote>Motherland believes in the philosophy of WIN WIN WIN &mdash; for a successful business all the stakeholders, customer, employees and the business owner, should win. It is happy employees who ensure customer satisfaction and thereby guarantee a successful business.</blockquote>
        </div>
      </article>
      <article class="dir glass spot rv">
        <img src="assets/img/Photos/selvamani.jpg" alt="S. A. Selvamani">
        <div>
          <h4>S. A. Selvamani</h4>
          <div class="role">TECHNICAL DIRECTOR</div>
          <blockquote>Sustainability is the core of all our beliefs and it is reflected in the way we work &mdash; from sourcing non-hazardous chemicals and auxiliaries, to less water and energy consuming equipment, to investing in new technologies that reduce our impact on the environment.</blockquote>
        </div>
      </article>
    </div>
  </div>
</section>
''' + cta('Want to see the plant?', 'We are at Peenya, Magadi Road, Harohalli and Chennai.', 'Arrange a visit')

    page('about.html', 'About Motherland Group | Our story since 1995',
         'From a makeshift shed in Chennai in 1995 to four units processing 60,000 garments a day. The history, vision and mission of Motherland Group.',
         about, 'about motherland group, garment processing history bangalore')

    # ------------------------------------------------ MOTHERLAND GARMENTS
    mg = phero('denim-repair-01.jpg', 'Motherland Garments',
               'Sustainability in<br>garment washing',
               'Adding value to apparel since 1995. Multiple locations at Magadi Road, Peenya, Harohalli and Chennai, with an exclusive denim washing unit at Peenya.') + APPROVE_MQ + '''
<section class="band">
  <div class="shell">
    <div class="certs">
      <div class="cert glass spot rv"><div class="t">APPROVED BY</div><div class="v">''' + ''.join(
        f'<span>{b.title() if b != "INDITEX" else "Inditex"}</span>' for b in
        ['Inditex', 'Marks and Spencer', 'Lacoste', 'Bestseller', 'Varner', 'American Eagle', 'Next']
    ) + '''</div></div>
      <div class="cert glass spot rv"><div class="t">SUSTAINABILITY</div><div class="v"><span>ZDHC</span><span>GOTS</span><span>INCHECK</span><span>Clearstream</span><span>EIM</span><span>Higgs FEM</span><span>BV E3</span></div></div>
      <div class="cert glass spot rv"><div class="t">CERTIFIED IN</div><div class="v"><span>ISO 9001</span><span>ISO 14001</span><span>OEKO-TEX</span></div></div>
      <div class="cert glass spot rv"><div class="t">FUNCTIONAL FINISH</div><div class="v"><span>Antimicrobial</span><span>Antiviral</span><span>Moisture wicking</span><span>Water &amp; oil repellent</span><span>Stain guard</span><span>UV protection</span><span>Fragrance</span><span>Cool finish</span></div></div>
    </div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'WHAT A WASH DOES', 'Raw indigo in,<br>finished denim out',
        'Every effect on a finished pair of jeans is put there on purpose, in a machine, by us. Drag the handle to take the indigo down.') + WASH_DEMO + '''
  </div>
</section>

<section class="band" id="finishes">
  <div class="shell">''' + sec_head(
        'THE CATALOGUE', 'Twenty washes<br>and finishes',
        'We carry out different washes based on customer requirements. These are the ones we are asked for most.') + '''
    <div class="tabs" role="tablist" id="washTabs">
      <button class="tab on" role="tab" aria-selected="true" aria-controls="p-basic" data-panel="p-basic">Basic washes<b>8</b></button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p-func" data-panel="p-func">Functional finishes<b>6</b></button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p-corr" data-panel="p-corr">Correctional finishes<b>6</b></button>
    </div>
    <div class="panel" id="p-basic" role="tabpanel"><div class="grid-3">''' + ''.join(
        wash_card(*w) for w in BASIC) + '''</div></div>
    <div class="panel" id="p-func" role="tabpanel" hidden><div class="grid-3">''' + ''.join(
        wash_card(*w) for w in FUNC) + '''</div></div>
    <div class="panel" id="p-corr" role="tabpanel" hidden><div class="grid-3">''' + ''.join(
        wash_card(*w) for w in CORR) + '''</div></div>

    <div class="tech rv">
      <div class="tech-txt">
        <p class="kicker">TECHNOLOGY</p>
        <h3 data-split>The science of finishing</h3>
        <p class="lede">The depletion of natural resources affects every one of us. We are committed to doing our bit in changing how we use the planet&rsquo;s fast-depleting resources &mdash; especially water. For sustainable technology in garment finishing and washing we work with the award-winning team at Jeanologia from Spain.</p>
        <span class="jean">Jeanologia Corporative &middot; Spain</span>
      </div>
      <div class="tech-ph"><img src="assets/img/about-mdl.jpg" alt="The washing floor at Motherland Garments"></div>
    </div>
  </div>
</section>
''' + CLIENTS_BAND + '''
<section class="band">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'WHAT THEY SAY', 'Design heads and<br>sourcing teams',
        'The people who send us their samples and their bulk.') + voices_grid(T_WASH) + '''
  </div>
</section>
''' + cta('Send us a sample', 'Tell us the garment, the fabric and the look you are after.', 'Start an enquiry')

    page('motherland-garments.html',
         'Motherland Garments | Sustainable garment washing &amp; finishing, Bangalore',
         'Garment washing and finishing for exporters and brands. 20 washes and finishes, ZDHC and OEKO-TEX certified, approved by Inditex, M&S, Lacoste, Bestseller, Varner, American Eagle and Next.',
         mg, 'garment washing, denim washing bangalore, functional finishes, stone wash, enzyme wash')

    # ------------------------------------------------------------ mDENIM
    md = phero('banner/md-banner-01.jpg', 'mDenim',
               'Don&rsquo;t ever throw<br>away a jean',
               'Alter, re-design, customise. Motherland Group, with over three decades across the apparel value chain, is now into denim alteration, customised denim and denim bag retail &mdash; a denim solution provider across B2C and B2B.') + '''
<section class="band">
  <div class="shell">
    <div class="vm">
      <article class="vm-card glass spot rv">
        <span class="glow" style="background:var(--crimson)"></span>
        <h3>Our Mission</h3>
        <p class="lede">To help people wear premium denim &mdash; by customising a new jean to the right fabric, fit, size and wash, redesigning and altering old denim into new fashion, and creating a unique identity.</p>
      </article>
      <article class="vm-card glass spot rv">
        <span class="glow" style="background:var(--indigo)"></span>
        <h3>Our Message</h3>
        <p class="lede">We make unique denim garments individually, to each customer&rsquo;s fabric, fit and look. The customers who love our work are passionate about their denim. Unlike others, we offer our own production facility for handcrafting custom denim and a process house for every wash and finish.</p>
      </article>
    </div>
  </div>
</section>

<section class="band band--tight" id="custom">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'FOUR THINGS WE DO', 'Make it, fit it,<br>fade it, fix it',
        'In-house sewing, washing and finishing means a single pair gets the same equipment as a 60,000-piece order.') + '''
    <div class="pillars">
      <article class="pillar glass spot rv"><span class="edge"></span>
        <h4>Denim Manufacturing</h4>
        <p>Niche products like denim bags and denim accessories. Our design team works a step ahead of the competition, and in-house sewing, washing and finishing deliver quality denims at the right price. We manufacture denim trousers, shorts and other bottom wear &mdash; and we specialise in denim bags, our core product. But we can do anything that is denim.</p>
      </article>
      <article class="pillar glass spot rv"><span class="edge"></span>
        <h4>Denim Customisation</h4>
        <p>Custom-fit trousers and suits are easy to find. A custom denim service is not &mdash; because it isn&rsquo;t just cut, sew and finish. It&rsquo;s choosing the right denim fabric, designing the garment, understanding the shrinkage pattern, sewing on heavy-duty specialised machinery, processing for the right look and feel, then finishing it as you want. Denim is an art and a science, rightly blended.</p>
      </article>
      <article class="pillar glass spot rv"><span class="edge"></span>
        <h4>Denim Re-Designing</h4>
        <p>Your seldom-worn jean can become your favourite. We restore old, worn jeans into a different pair altogether &mdash; packages that refresh the jean, take away stains, make it bright as new, add new looks, wash-downs, overdyes and more. There are exciting possibilities in your old denim.</p>
      </article>
      <article class="pillar glass spot rv" id="alterations"><span class="edge"></span>
        <h4>Denim Alterations</h4>
        <p>You buy a brand-new jean, aren&rsquo;t happy with the store&rsquo;s alteration service, find a tailor with great difficulty and still get below-par work, because they aren&rsquo;t equipped for it. mDenim offers professional, technical alteration &mdash; from a length reduction with the original hem to anything else you want done &mdash; on specialised heavy-duty factory equipment, by tailors who understand denim.</p>
      </article>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">''' + sec_head(
        'ALSO ALTER THIS WAY', 'Fifteen ways we can<br>change a denim',
        'One-stop solutions for everything you wear.') + '''
    <div class="alt-grid">''' + ''.join(
        f'<article class="alt glass spot"><img src="assets/img/icons/{icon}.png" alt="">'
        f'<h5>{name}</h5><p>{desc}</p></article>'
        for name, icon, desc in ALTERATIONS) + '''</div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="split-img rv">
      <div class="si-ph"><img src="assets/img/denim-repair-01.jpg" alt="Denim repair work at mDenim"></div>
      <div class="si-txt">
        <p class="kicker">DENIMS IN LATEST FASHION</p>
        <h2 class="h-sub" data-split>And washes, because we have in-house manufacturing</h2>
        <p class="lede">Give a new life to your old denim. Professional alteration with the original hem, the fit you want, and many more. Alterations are done on specialised, heavy-duty factory equipment by skilled tailors who understand the nuances of denim.</p>
        <a class="btn btn--house" href="contact.html"><span class="dot"></span>Get started now</a>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'WHAT THEY SAY', 'People who are<br>passionate about<br>their denim',
        'Bags, alterations and jeans that fit again.') + voices_grid(T_DENIM) + '''
  </div>
</section>
''' + cta('Bring us your denim', 'Length, waist, taper, rips, patches, a whole new wash &mdash; or a jean built from scratch.', 'Book an alteration')

    page('mdenim.html', 'mDenim | Denim customisation, alteration &amp; refashioning in Bangalore',
         'mDenim customises new jeans to your fabric, fit, size and wash, and alters, repairs and refashions old denim on heavy-duty factory equipment. Denim bags and accessories too.',
         md, 'denim manufacturers in bangalore, denim customisation, denim refashioning, denim alterations')

    # ----------------------------------------------------------- mSQUARE
    ms = phero('banner/ms-01.jpg', 'mSquare',
               'Factory fresh,<br>five stores, one city',
               'Motherland Group, with its strong presence in garment manufacturing, is also into garment retail under the brand mSquare &mdash; with the expertise of working with top Indian and international brands across menswear, womenswear, kids and babies.') + '''
<section class="band">
  <div class="shell">
    <div class="retail-split">
      <article class="retail-card glass spot rv">
        <h4>Retail</h4>
        <p>mSquare stores sit at prime locations across Bangalore. In the first year of operations there are already five, well stocked with apparel for every occasion &mdash; formals, semi-casuals and casuals.</p>
        <div class="chips">
          <span>Denims</span><span>Chinos</span><span>Casual cotton shirts</span><span>Knits</span><span>T-shirts</span><span>Sweatshirts</span><span>Tracks</span><span>Joggers</span><span>Kids</span><span>Ladies wear</span><span>100% cotton</span><span>Prewashed</span>
        </div>
      </article>
      <article class="retail-card glass spot rv">
        <h4>Wholesale</h4>
        <p>mSquare also runs a B2B model, offering garments to other retailers with stock in every category at attractive prices.</p>
        <p class="muted" style="margin-top:16px;font-size:14px">A lot has changed since 1995. With over 25 years of a customer-focused approach and a continuous quest for quality, Motherland Group today processes over 60,000 garments a day and has diversified into many garment-based B2B and B2C solutions.</p>
        <a class="btn btn--ghost" href="contact.html" style="margin-top:22px">Talk wholesale</a>
      </article>
    </div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'WHERE TO FIND US', 'Five stores,<br>and counting',
        'mSquare plans at least 25 stores across Bangalore.') + '''
    <div class="stores">''' + ''.join(
        f'<article class="store glass spot"><span class="ix">STORE {i+1:02d}</span><p>{s}</p></article>'
        for i, s in enumerate(STORES)) + '''</div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="split-img rv">
      <div class="si-ph"><img src="assets/img/retails-showroom.jpg" alt="Inside an mSquare store"></div>
      <div class="si-txt">
        <p class="kicker">EXPORT QUALITY</p>
        <h2 class="h-sub" data-split>Knits, t-shirts, sweatshirts, tracks, joggers</h2>
        <p class="lede">100% cotton. Prewashed garments. The stores are well stocked with variety for all occasions, and because the garments come off our own finishing lines, the quality is the same one our export customers buy.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="shell">''' + sec_head(
        'WHAT THEY SAY', 'Shoppers who<br>came back',
        'And brought the family.') + voices_grid(T_RETAIL) + '''
  </div>
</section>
''' + cta('Stocking up for your store?', 'We have stock in every category at wholesale prices.', 'Talk wholesale')

    page('msquare.html', 'mSquare | Factory outlet &amp; wholesale garments in Bangalore',
         'mSquare sells factory-fresh garments across five Bangalore stores — denims, chinos, shirts, knits, t-shirts, tracks, joggers, kids and ladies wear — and supplies other retailers wholesale.',
         ms, 'best factory outlet in bangalore, factory outlet near me, msquare factory outlet')

    # -------------------------------------------------------------- TEAM
    stars = ''.join(
        '<div class="mini glass spot"><div class="av">' +
        (f'<img src="assets/img/Photos/{ph}" alt="{n}">' if ph else n[0]) +
        f'</div><div><h5>{n}</h5><span>{r}</span></div></div>'
        for n, r, ph in SUPERSTARS)

    team = phero('team.jpg', 'Our Team',
                 'Take care of your people<br>and they take care<br>of your customers',
                 'A 200-strong team focused entirely on giving the customer the best. Creative freedom, continuous learning, personal career growth and employee empowerment are guaranteed in the organisation.',
                 'center 30%') + '''
<section class="band">
  <div class="shell">''' + sec_head(
        'OUR MANAGEMENT', 'The people who<br>built the place',
        'Promoted by technocrats with 30 years of expertise in the garment supply chain.') + '''
    <div class="team-lead">
      <article class="person spot rv"><div class="pf"><img src="assets/img/Photos/a-j-Pandian-Managing-Director.jpg" alt="A. J. Pandian"></div><div class="meta"><h4>A. J. Pandian</h4><div class="role">MANAGING DIRECTOR</div></div></article>
      <article class="person spot rv"><div class="pf"><img src="assets/img/Photos/s-a-Selvamani-Technical-Director.jpg" alt="S. A. Selvamani"></div><div class="meta"><h4>S. A. Selvamani</h4><div class="role">TECHNICAL DIRECTOR</div></div></article>
      <article class="person spot rv"><div class="pf"><img src="assets/img/Photos/G.Ramesh Kanna - Director.jpg" alt="G. Ramesh Kanna"></div><div class="meta"><h4>G. Ramesh Kanna</h4><div class="role">EXECUTIVE DIRECTOR</div></div></article>
    </div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'OUR SUPER STARS', 'The team that<br>runs the day',
        'Marketing, accounts, HR, admin, sales and operations.') + f'''
    <div class="team-grid">{stars}</div>
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="dirs">
      <article class="dir glass spot rv">
        <img src="assets/img/Photos/pandiyan.jpg" alt="A. J. Pandian">
        <div>
          <h4>A. J. Pandian</h4>
          <div class="role">MANAGING DIRECTOR</div>
          <blockquote>Motherland believes in the philosophy of WIN WIN WIN &mdash; for a successful business all the stakeholders, customer, employees and the business owner, should win. It is happy employees who ensure customer satisfaction and thereby guarantee a successful business.</blockquote>
        </div>
      </article>
      <article class="dir glass spot rv">
        <img src="assets/img/Photos/selvamani.jpg" alt="S. A. Selvamani">
        <div>
          <h4>S. A. Selvamani</h4>
          <div class="role">TECHNICAL DIRECTOR</div>
          <blockquote>Sustainability is the core of all our beliefs and it is reflected in the way we work &mdash; from sourcing non-hazardous chemicals and auxiliaries, to less water and energy consuming equipment, to investing in new technologies that reduce our impact on the environment.</blockquote>
        </div>
      </article>
    </div>
  </div>
</section>
''' + cta('Want to work here?', 'Creative freedom, continuous learning and career growth are guaranteed.', 'Write to us')

    page('team.html', 'Our Team | Motherland Group',
         'A 200-strong team. Meet the management and the people who run the day at Motherland Group.',
         team, 'motherland group team, garment manufacturing management bangalore')

    # ------------------------------------------------------ TESTIMONIALS
    tst = phero('banner/alter-01.jpg', 'Testimonials',
                'What they say<br>when we are<br>not in the room',
                'Design heads, sourcing teams, shoppers and people who just wanted their jeans to fit again.') + f'''
<section class="band">
  <div class="shell">''' + sec_head(
        'MOTHERLAND GARMENTS', 'Exporters and<br>design teams',
        'The people who send us their samples and their bulk.') + voices_grid(T_WASH) + '''
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'mDENIM', 'Denim people',
        'Bags, alterations and jeans that fit again.') + voices_grid(T_DENIM) + '''
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'mSQUARE', 'Shoppers',
        'Who came back, and brought the family.') + voices_grid(T_RETAIL) + '''
  </div>
</section>

<section class="band band--tight">
  <div class="shell">
    <div class="rule"></div>''' + sec_head(
        'LAUNDRY &amp; CARE', 'Garment care',
        'Dry cleaning, finishes and restoration.') + voices_grid(T_LAUNDRY) + '''
  </div>
</section>
''' + cta('Want to be the next one?', 'Tell us what you need and we will come back within a working day.')

    page('testimonials.html', 'Testimonials | Motherland Group',
         'What exporters, designers, shoppers and denim customers say about Motherland Garments, mDenim and mSquare.',
         tst, 'motherland group reviews, testimonials')

    # ----------------------------------------------------------- CONTACT
    contact = phero('about-mdl.jpg', 'Contact Us',
                    'Tell us what<br>you need done',
                    'Whether it&rsquo;s 60,000 garments a day or one pair of jeans that doesn&rsquo;t fit any more &mdash; send us the details and our team will come back to you.') + '''
<section class="band contact">
  <div class="shell">
    <div class="c-grid">
      <div class="c-info glass spot rv">
        <div class="c-line">
          <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg></span>
          <div><div class="lb">HEAD OFFICE</div><div class="vl">#40-B, 2nd Phase, Peenya Industrial Area,<br>Bengaluru, Karnataka 560058</div></div>
        </div>
        <div class="c-line">
          <span class="ic">''' + PHONE_SVG.replace('stroke="currentColor"', '') + '''</span>
          <div><div class="lb">PHONE</div><div class="vl"><a href="tel:+919342250766">+91 93422 50766</a><br><a href="tel:+919740044100">+91 97400 44100</a></div></div>
        </div>
        <div class="c-line">
          <span class="ic">''' + MAIL_SVG.replace('stroke="currentColor"', '') + '''</span>
          <div><div class="lb">EMAIL</div><div class="vl"><a href="mailto:blr@motherlandgroup.com">blr@motherlandgroup.com</a></div></div>
        </div>
        <div class="c-line">
          <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M3 21V8l9-5 9 5v13"/><path d="M9 21v-7h6v7"/></svg></span>
          <div><div class="lb">UNITS</div><div class="vl">Magadi Road &middot; Peenya &middot; Harohalli &middot; Chennai<br><span class="muted" style="font-size:13.4px">Exclusive denim washing unit at Peenya</span></div></div>
        </div>
        <div class="c-line">
          <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M3 3h18v18H3z"/><path d="M3 9h18M9 21V9"/></svg></span>
          <div><div class="lb">mSQUARE STORES</div><div class="vl" style="font-size:13.6px">''' + '<br>'.join(STORES) + '''</div></div>
        </div>
      </div>

      <form class="c-form glass spot rv" id="enquiry" novalidate>
        <div class="fields">
          <div class="field"><label for="f-name">YOUR NAME</label><input id="f-name" name="name" type="text" placeholder="Full name" required></div>
          <div class="field"><label for="f-company">COMPANY</label><input id="f-company" name="company" type="text" placeholder="Optional"></div>
          <div class="field"><label for="f-email">EMAIL</label><input id="f-email" name="email" type="email" placeholder="you@company.com" required></div>
          <div class="field"><label for="f-phone">PHONE</label><input id="f-phone" name="phone" type="tel" placeholder="+91" required></div>
          <div class="field wide"><label for="f-int">WHAT DO YOU NEED</label>
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
          <div class="field wide"><label for="f-msg">TELL US WHAT YOU NEED</label><textarea id="f-msg" name="message" placeholder="Garment type, quantity, finish, timeline — whatever you already know." required></textarea></div>
        </div>
        <button class="btn btn--house" type="submit"><span class="dot"></span>Send enquiry</button>
        <p class="form-note" id="formNote">We reply within one working day.</p>
      </form>
    </div>
  </div>
</section>'''

    page('contact.html', 'Contact Motherland Group | Peenya, Bengaluru',
         'Get in touch with Motherland Group for garment washing, denim manufacturing, customisation, alteration, retail and wholesale. Peenya, Bengaluru.',
         contact, 'contact motherland group, garment washing enquiry bangalore')

    # ------------------------------------------------------ LEGAL PAGES
    def legal(fname, crumb, title, blocks, desc):
        body = phero('about-mdl.jpg', crumb, title, '') + '''
<section class="band">
  <div class="shell" style="max-width:min(820px,92vw)">''' + ''.join(
            f'<h3 class="h-sub" style="margin:40px 0 14px">{h}</h3><p class="lede">{b}</p>'
            for h, b in blocks) + '''
  </div>
</section>'''
        page(fname, f'{title.replace("<br>", " ")} | Motherland Group', desc, body)

    legal('terms.html', 'Terms', 'Terms &amp;<br>Conditions', [
        ('Use of this site', 'This website is operated by Motherland Garments Private Limited. By accessing it you agree to these terms. Content, images and marks on this site belong to Motherland Group and may not be reproduced without written permission.'),
        ('Services and quotations', 'Descriptions of washes, finishes and services on this site are indicative. Exact process routes, lead times and prices are confirmed in writing against each order, after sample approval.'),
        ('Liability', 'We take every care in processing garments entrusted to us. Liability for any garment is limited to the processing value of that garment, unless otherwise agreed in a signed contract.'),
        ('Contact', 'Questions about these terms can be sent to blr@motherlandgroup.com or by post to #40-B, 2nd Phase, Peenya Industrial Area, Bengaluru, Karnataka 560058.'),
    ], 'Terms and conditions for using the Motherland Group website and services.')

    legal('privacy.html', 'Privacy', 'Privacy<br>Policy', [
        ('What we collect', 'When you send an enquiry through this site we receive the name, company, email address, phone number and message you choose to give us. We do not collect anything else about you.'),
        ('How we use it', 'We use your details only to answer your enquiry and to follow up about the work you asked about. We do not sell or rent your information to anyone.'),
        ('Cookies', 'This site does not set tracking or advertising cookies. Fonts are loaded from Google Fonts, which may log the request.'),
        ('Your choices', 'Write to blr@motherlandgroup.com at any time to ask what we hold about you, to correct it, or to have it deleted.'),
    ], 'How Motherland Group handles the information you send through this website.')

    print('built:', ', '.join(sorted(f for f in os.listdir(OUT) if f.endswith('.html'))))


if __name__ == '__main__':
    build()
