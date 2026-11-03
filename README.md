# Motherland Group website

Static site. No build step to deploy, no runtime dependencies. The pages sit at the
repo root so Vercel, GitHub Pages and Netlify all serve it with zero configuration.

## Run it locally

```bash
python -m http.server 4173
```

Then open http://localhost:4173. Opening `index.html` straight off disk also works.

## Pages

| File | Mirrors |
|---|---|
| `index.html` | Home |
| `about.html` | About: history, vision, mission, directors |
| `motherland-garments.html` | Garment washing: certifications, 20 washes, Jeanologia |
| `mdenim.html` | mDenim: 4 pillars, 15 alteration services |
| `msquare.html` | mSquare: retail, wholesale, 5 stores |
| `team.html` | Our team |
| `testimonials.html` | All testimonials, grouped by division |
| `contact.html` | Contact details + enquiry form |
| `terms.html`, `privacy.html` | Legal |

## Editing content

Pages are generated. Edit `build.py`, then:

```bash
python build.py
```

Content lives in plain Python lists near the top of `build.py`: `BASIC`, `FUNC`,
`CORR` (washes), `ALTERATIONS`, `TIMELINE`, `STORES`, `SUPERSTARS`, and the `T_*`
testimonial lists. The site chrome is defined once in `head()`, `topbar()` and `FOOT`,
so a nav change reaches every page.

The build fails if any page names a local file or `#anchor` that does not exist.

To hand the client plain HTML with no generator, give them everything except
`build.py`; the generated pages are self-contained.

## Deploying

Any static host works as-is, because every path in the HTML is relative.

- **Vercel**: import the repo, no settings to change.
- **GitHub Pages**: Settings, Pages, Source: *Deploy from a branch*, `main` / `root`.
  `.nojekyll` is present so Pages serves the files untouched.

`.vercelignore` keeps `build.py` and `README.md` out of the deployed bundle.

## Design

The palette is what a pair of jeans is made of: indigo at every stage of the wash
(`#10173A` raw to `#F4F6FB` bleached cotton), tan topstitch (`#C9893B`) and the house
crimson (`#DA0133`, `#82073A`) as the red tab. Tokens are at the top of
`assets/css/style.css`, which is written phone-first.

- **Type**: Archivo throughout, using its width axis (condensed for headlines and
  numbers, normal for reading). Instrument Serif is reserved for people's own words.
- **Words sit beside photographs, not on top of them.** The two exceptions, the division
  panels and the statement band, carry a scrim built for it.
- **Phones get their own layout**: an action bar under the thumb, a full-screen menu,
  cards that stack as you scroll, accordions for the long lists, and a swipe row for
  testimonials.

## Live visuals

| Visual | Where | How |
|---|---|---|
| Silk and turning wash drum, with the figure leaping past the frame | Home, Contact | WebGL + CSS |
| Dyed number with a fade moving through it | Home | CSS |
| Garment counter since the page opened | Home | JS |
| The line: garments fade from raw to bleached through a spray bar | Home, Garment Washing | Canvas |
| Division panels and quotes that take turns | Home, About | CSS + JS |
| Denim swatch: dye comes off under the handle | Home, Garment Washing | WebGL |
| Indigo dye moving behind dark bands | Home, Garment Washing | WebGL |
| Seam sewn by a moving needle | mDenim | CSS |
| Store rack of moving garments | mSquare | Canvas |
| Moving quotes | Testimonials | CSS |
| Self-stitching photo frames, spinning woven label, slow photo drift | Inner pages | CSS |
| Moving names and logos, footer wordmark, closing silk band | Across the site | CSS / WebGL |
| Reveals, opening photographs, history seam, progress bar | Across the site | CSS scroll timelines |

There are no libraries and no CDN scripts, so nothing can fail to load.

- `live()` in `assets/js/app.js` runs each perpetual canvas. It draws only while the
  element is on screen, runs at 30fps on phones, and stops on a device that cannot keep up.
- Nothing can leave content hidden. Load motion is plain CSS and scroll motion follows
  the scroll position, so browsers without scroll timelines just show everything.
- The **Pause motion** switch (on the hero and in every footer) stops all looping motion
  and is remembered between pages. `prefers-reduced-motion` turns it all off.
- Without WebGL the CSS background behind each canvas shows. Without JavaScript all the
  content is still there.

The swatch is drawn, not photographed, and says so on the page. The garment counter is
plain arithmetic at the published rate of 1,00,000 a day, and says that too.

## Known gaps

- **The enquiry form has no backend.** It validates, then opens the visitor's mail app
  with the enquiry pre-filled to `blr@motherlandgroup.com`. Wire it to a form handler
  before launch if you want submissions captured server-side.
- **The capacity figure is inconsistent in the client's copy**: the hero says 1,00,000
  garments a day; About, mDenim, the home closing band and the division text say 60,000.
- `terms.html` and `privacy.html` contain **drafted** text, not the client's legal copy.
- The Blog link was removed because `blog.motherlandgroup.com` no longer resolves.
- Six client logos in `assets/img/clients/` (`1.jpg` to `6.jpg`: H&M, Allen Solly,
  Jack & Jones, U.S. Polo Assn., Arrow, Blackberrys) are unused until confirmed as current.
