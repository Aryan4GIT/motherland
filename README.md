# Motherland Group — website redesign

Static site. No build step, no dependencies. The pages sit at the repo root so
Vercel, GitHub Pages and Netlify all serve it with zero configuration.

## Run it locally

```bash
python -m http.server 4173
```

Then open http://localhost:4173. (Opening `index.html` straight off disk won't work —
the browser blocks ES modules on `file://`. Use the server.)

## Pages

| File | Mirrors |
|---|---|
| `index.html` | Home |
| `about.html` | About Group — history, vision, mission, directors |
| `motherland-garments.html` | Garment washing — certifications, 20 washes, Jeanologia |
| `mdenim.html` | mDenim — 4 pillars, 15 alteration services |
| `msquare.html` | mSquare — retail, wholesale, 5 stores |
| `team.html` | Our team |
| `testimonials.html` | All testimonials, grouped by division |
| `contact.html` | Contact details + enquiry form |
| `terms.html`, `privacy.html` | Legal |

## Editing content

Pages are generated. Edit `build.py`, then:

```bash
python build.py
```

Content lives in plain Python lists near the top of `build.py` — `BASIC`, `FUNC`,
`CORR` (washes), `ALTERATIONS`, `TIMELINE`, `STORES`, `SUPERSTARS`, and the
`T_*` testimonial lists. The site chrome (head, nav, footer) is defined once in
`head()`, `topbar()` and `FOOT`, so a nav change reaches every page.

To hand the client plain HTML with no generator, give them everything except
`build.py` — the generated pages are self-contained.

## Deploying

Any static host works as-is, because every path in the HTML is relative.

- **Vercel** — import the repo, no settings to change.
- **GitHub Pages** — Settings → Pages → Source: *Deploy from a branch*, `main` / `root`.
  `.nojekyll` is present so Pages serves the files untouched.

`.vercelignore` keeps `build.py` and `README.md` out of the deployed bundle.

## Design

Built on indigo, because the craft here is controlled fading of indigo — stone,
acid and enzyme washes are all ways of taking the dye down. The palette is the
bleached end of that wash: a washed-cotton ground (`#F1F4F9`) with indigo as the
ink (`#121833` text, `#2E3F9E` accent). The house crimson (`#82073A → #DA0133`)
is lifted from the original site's own CSS.

Text that sits over a photograph keeps a dark scrim and light type — those need
one regardless of the page around them, and the contrast gives the layout depth.
Banner photographs range from a near-white flat-lay to a dim factory floor, so
`BANNER_DIM` in `build.py` normalises each toward the same perceived weight.

- Display type: **Archivo** at expanded width (`wdth` 118–125)
- Body type: **Sora**
- Tokens are at the top of `assets/css/style.css`; `premium.css` holds the
  atmosphere, cursor, showcase and wash-demo layers.

## Motion

| Library | Used for |
|---|---|
| [Lenis](https://lenis.darkroom.engineering/) 1.1.14 | smooth scrolling |
| [motion.dev](https://motion.dev) 11.11.17 | scroll reveals, spring/magnetic buttons |
| [anime.js](https://animejs.com) 3.2.2 | load sequence, counters, split-heading reveals, tab swaps |

All three load from CDN **dynamically, inside `try/catch`**. If a CDN is blocked the
page still renders completely — it just loses the animation. `prefers-reduced-motion`
is respected throughout.

The signature moment is the **wash demo** (home page and the garment washing page):
drag the handle across a photo of raw denim being hand-finished and the indigo comes
down. Both halves are the same photograph under different CSS filters, so it is an
illustration of the effect, not a real before/after pair of the same garment.

## Known gaps

- **The enquiry form has no backend.** It validates, then opens the visitor's mail
  client with the enquiry pre-filled to `blr@motherlandgroup.com`. Wire it to a
  form handler or PHP endpoint before launch if you want submissions captured
  server-side.
- Footer legal links point at the new `terms.html` / `privacy.html`, which contain
  **drafted** text, not the client's existing legal copy. Replace before launch.
- The blog link still points at the live `blog.motherlandgroup.com`.
- Images are the originals pulled from motherlandgarments.com and are not
  optimised (no WebP, no responsive `srcset`). The two largest banners are ~500KB.
- Copyright line still reads 2021, matching the original site.
