/* ============================================================
   MOTHERLAND GROUP — motion layer
   lenis      → smooth scrolling
   motion.dev → reveals, springs, magnetic buttons
   anime.js   → the load sequence, counters, the wash wipe
   vanilla    → parallax, marquees, tilt, cursor, demo, tabs
   Every library loads dynamically, so a CDN failure degrades
   to a visible, static, fully readable site.
   ============================================================ */

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE    = matchMedia('(hover:hover) and (pointer:fine)').matches;

let motion = null, anime = null, Lenis = null, lenis = null;

const load = () => Promise.all([
  import('https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm')
    .then(m => { motion = m; }).catch(() => {}),
  import('https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.es.js')
    .then(m => { anime = m.default || m; }).catch(() => {}),
  import('https://cdn.jsdelivr.net/npm/lenis@1.1.14/+esm')
    .then(m => { Lenis = m.default || m.Lenis; }).catch(() => {})
]);

/* ------------------------------------------------------------
   Smooth scroll. Everything else reads window.scrollY, which
   Lenis keeps in sync, so nothing downstream needs to know.
   ------------------------------------------------------------ */
function smooth() {
  if (REDUCED || !Lenis) return;
  lenis = new Lenis({ duration: 1.15, smoothWheel: true, lerp: 0.1 });
  const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);

  $$('a[href^="#"]').forEach(a => {
    const id = a.getAttribute('href');
    if (id.length < 2) return;
    a.addEventListener('click', e => {
      const t = $(id);
      if (!t) return;
      e.preventDefault();
      lenis.scrollTo(t, { offset: -92 });
    });
  });

  // Lenis owns the scroll position, so a #hash arriving from another
  // page never lands. Take it there once the page has settled.
  if (location.hash.length > 1) {
    const t = $(location.hash);
    if (t) setTimeout(() => lenis.scrollTo(t, { offset: -92, immediate: true }), 120);
  }
}

/* ------------------------------------------------------------
   Split headings into lines of words, so they can rise in
   sequence from behind a mask. One device, used on every H2.
   ------------------------------------------------------------ */
function splitHeads() {
  $$('[data-split]').forEach(h => {
    if (h.dataset.done) return;
    h.dataset.done = '1';

    // <br> already tells us where the author wanted a line break
    const lines = h.innerHTML.split(/<br\s*\/?>/i);
    h.innerHTML = lines.map(line => {
      const words = line.trim().split(/\s+/).filter(Boolean)
        .map(w => `<span class="sp-w">${w}</span>`).join(' ');
      return `<span class="sp-line">${words}</span>`;
    }).join('');

    if (REDUCED) return;
    $$('.sp-w', h).forEach(w => {
      w.style.transform = 'translateY(105%) rotate(3deg)';
      w.style.opacity = '0';
    });
  });

  if (REDUCED) return;

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const words = $$('.sp-w', e.target);
      // drop the inline transforms afterwards so the words stop
      // holding a composited layer each
      const settle = () => words.forEach(w => w.removeAttribute('style'));
      if (anime) {
        anime({
          targets: words, translateY: ['105%', '0%'], rotate: [3, 0], opacity: [0, 1],
          delay: anime.stagger(48), duration: 950, easing: 'easeOutExpo', complete: settle
        });
      } else {
        words.forEach((w, i) => {
          w.style.transition = `transform .85s cubic-bezier(.2,.9,.25,1) ${i * 48}ms, opacity .6s ease ${i * 48}ms`;
          w.style.transform = 'none'; w.style.opacity = '1';
        });
        setTimeout(settle, 1000 + words.length * 48);
      }
      io.unobserve(e.target);
    });
  }, { threshold: .2, rootMargin: '0px 0px -8% 0px' });

  $$('[data-split]').forEach(h => io.observe(h));
}

/* ------------------------------------------------------------
   Reveals + the rules that draw themselves
   ------------------------------------------------------------ */
function reveals() {
  const items = [...$$('.rv'), ...$$('.rule')];
  if (REDUCED) { items.forEach(el => el.classList.add('seen')); return; }

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      if (el.classList.contains('rule')) { el.classList.add('seen'); io.unobserve(el); return; }
      if (motion) {
        motion.animate(el,
          { opacity: [0, 1], transform: ['translateY(28px)', 'translateY(0px)'] },
          { duration: .9, easing: [.2, .85, .25, 1] });
      } else {
        el.style.transition = 'opacity .8s ease, transform .8s cubic-bezier(.2,.85,.25,1)';
      }
      el.classList.add('seen');
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: .1 });

  items.forEach(el => io.observe(el));
}

/* Grids arrive as a group, not one card at a time. */
function staggerGroups() {
  if (REDUCED) return;
  const sel = ['.divs', '.certs', '.grid-3', '.alt-grid', '.stores',
               '.team-grid', '.rail-track', '.counters', '.showcase', '.team-lead', '.pillars'];

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      [...e.target.children].forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(24px) scale(.985)';
        el.style.transition =
          `opacity .75s ease ${i * 55}ms, transform .75s cubic-bezier(.2,.85,.25,1) ${i * 55}ms`;
        requestAnimationFrame(() => requestAnimationFrame(() => {
          el.style.opacity = '1';
          el.style.transform = '';
        }));
      });
      io.unobserve(e.target);
    });
  }, { threshold: .06, rootMargin: '0px 0px -6% 0px' });

  sel.forEach(s => $$(s).forEach(g => io.observe(g)));
}

/* ------------------------------------------------------------
   Boot + hero: the one orchestrated page-load moment.
   The wordmark is washed down by an indigo→bleach gradient,
   which is exactly what this company does to a garment.
   ------------------------------------------------------------ */
function bootAndHero() {
  const boot = $('#boot'), bar = $('#boot .boot-bar i'), mark = $('#boot .boot-mark');

  const finish = () => {
    if (!boot || boot.dataset.done) return;
    boot.dataset.done = '1';
    boot.style.transition = 'opacity .55s ease, transform .9s cubic-bezier(.7,0,.3,1)';
    boot.style.transform = 'translateY(-101%)';
    boot.style.opacity = '0';
    setTimeout(() => boot.remove(), 950);
    heroIn();
  };

  if (REDUCED || !anime || !boot) {
    if (mark) mark.style.backgroundPosition = '100% 50%';
    setTimeout(finish, REDUCED ? 60 : 600);
    return;
  }

  anime.timeline({ easing: 'easeOutExpo' })
    .add({ targets: mark, opacity: [0, 1], scale: [.94, 1], duration: 620 })
    .add({ targets: mark, backgroundPosition: ['0% 50%', '100% 50%'], duration: 1050, easing: 'easeInOutQuart' }, '-=400')
    .add({ targets: bar, width: ['0%', '100%'], duration: 950, easing: 'easeInOutQuart' }, '-=1000')
    .add({ targets: mark, opacity: 0, translateY: -14, duration: 400, easing: 'easeInQuad', complete: finish }, '-=110');

  setTimeout(finish, 3400); // failsafe
}

function heroIn() {
  const hero = $('.hero');
  if (!hero) { pheroIn(); return; }

  const parts = ['#heroTag', '#h1a', '#h1b', '#h1c', '#heroLine', '#heroLede', '#heroActs', '#scrollHint']
    .map(s => $(s)).filter(Boolean);

  if (REDUCED || !anime) { counters(); return; }

  const cards = $$('#counters .ctr');
  parts.forEach(el => { el.style.opacity = '0'; });
  cards.forEach(el => { el.style.opacity = '0'; });

  // once the entrance is done, drop the leftover transforms so the
  // hero stops holding a composited layer per element
  const settle = () => [...parts, ...cards].forEach(el => {
    el.style.transform = '';
    el.style.opacity = '1';
  });

  anime.timeline({ easing: 'easeOutExpo', duration: 1000, complete: settle })
    .add({ targets: '#heroTag', opacity: [0, 1], translateY: [18, 0], duration: 680 })
    .add({ targets: ['#h1a', '#h1b', '#h1c'], opacity: [0, 1], translateY: [56, 0], rotate: [1.5, 0], delay: anime.stagger(110) }, '-=400')
    .add({ targets: '#h1b', backgroundPosition: ['0% 50%', '62% 50%'], duration: 1500, easing: 'easeInOutQuart' }, '-=900')
    .add({ targets: '#heroLine', opacity: [0, 1], scaleX: [0, 1], duration: 760 }, '-=1150')
    .add({ targets: '#heroLede', opacity: [0, 1], translateY: [22, 0], duration: 760 }, '-=620')
    .add({ targets: '#heroActs', opacity: [0, 1], translateY: [22, 0], duration: 700 }, '-=560')
    .add({ targets: '#counters .ctr', opacity: [0, 1], translateY: [34, 0], scale: [.95, 1],
           delay: anime.stagger(90), duration: 820, begin: counters }, '-=620')
    .add({ targets: '#scrollHint', opacity: [0, 1], duration: 600 }, '-=400');

  // the wash keeps breathing afterwards, very slowly
  anime({ targets: '#h1b', backgroundPosition: ['62% 50%', '38% 50%'],
          duration: 6500, direction: 'alternate', loop: true,
          easing: 'easeInOutSine', delay: 2600 });
}

/* Inner pages get a quieter version of the same entrance. */
function pheroIn() {
  const p = $('.phero');
  if (!p || REDUCED || !anime) return;
  const bits = [$('.crumb', p), $('.lede', p)].filter(Boolean);
  anime({ targets: bits, opacity: [0, 1], translateY: [20, 0],
          delay: anime.stagger(120, { start: 140 }), duration: 900, easing: 'easeOutExpo' });
}

/* Indian digit grouping: 100000 → 1,00,000 */
const inGroup = n => {
  const s = String(n);
  if (s.length <= 3) return s;
  return s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + s.slice(-3);
};

let counted = false;
function counters() {
  if (counted) return; counted = true;
  $$('#counters .n').forEach(el => {
    const to = +el.dataset.to;
    const fmt = el.dataset.fmt === 'in' ? inGroup
      : v => String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    if (REDUCED || !anime) { el.textContent = fmt(to) + '+'; return; }
    const o = { v: 0 };
    anime({
      targets: o, v: to, duration: 2200, easing: 'easeOutExpo',
      update: () => { el.textContent = fmt(Math.round(o.v)); },
      complete: () => { el.textContent = fmt(to) + '+'; }
    });
  });
}

/* ------------------------------------------------------------
   Parallax on both hero kinds
   ------------------------------------------------------------ */
function parallax() {
  if (REDUCED) return;
  const layers = [
    [$('#heroBg'), $('.hero'), 96, .1],
    [$('.phero-bg'), $('.phero'), 70, .08]
  ].filter(([el, host]) => el && host);
  const blobs = $$('.aura b');
  if (!layers.length && !blobs.length) return;

  let t = false;
  const run = () => {
    const y = window.scrollY;
    layers.forEach(([el, host, dist, sc]) => {
      const h = host.offsetHeight;
      if (y > h + 240) return;
      const p = Math.min(y / h, 1);
      el.style.transform = `translate3d(0,${p * dist}px,0) scale(${1 + p * sc})`;
    });
    blobs.forEach((b, i) => {
      const k = (i + 1) * .045 * (i % 2 ? -1 : 1);
      b.style.transform = `translate3d(0,${y * k}px,0)`;
    });
    t = false;
  };
  addEventListener('scroll', () => { if (!t) { t = true; requestAnimationFrame(run); } }, { passive: true });
  run();
}

/* ------------------------------------------------------------
   Marquees — constant drift, nudged by scroll velocity
   ------------------------------------------------------------ */
function marquees() {
  const rows = $$('.mq-row');
  if (!rows.length || REDUCED) return;

  const st = rows.map(r => ({ el: r, x: 0, base: +r.dataset.mq || -.4, w: 0 }));
  const measure = () => st.forEach(s => { s.w = s.el.scrollWidth / 2; });
  measure();
  addEventListener('resize', measure);
  addEventListener('load', measure);

  let vel = 0, last = window.scrollY;
  addEventListener('scroll', () => {
    vel += (window.scrollY - last) * .035;
    last = window.scrollY;
  }, { passive: true });

  (function tick() {
    vel *= .92;
    st.forEach(s => {
      s.x += s.base + vel * Math.sign(s.base || 1);
      if (s.w) {
        if (s.x <= -s.w) s.x += s.w;
        if (s.x > 0) s.x -= s.w;
      }
      s.el.style.transform = `translate3d(${s.x}px,0,0)`;
    });
    requestAnimationFrame(tick);
  })();
}

/* ------------------------------------------------------------
   Nav: stuck state, scroll progress, drawer
   ------------------------------------------------------------ */
function nav() {
  const bar = $('#topbar'), up = $('#toTop'), prog = $('#prog');

  const run = () => {
    const y = window.scrollY;
    if (bar) bar.classList.toggle('is-stuck', y > 40);
    if (up) up.classList.toggle('on', y > 700);
    if (prog) {
      const max = document.documentElement.scrollHeight - innerHeight;
      prog.style.transform = `scaleX(${max > 0 ? Math.min(y / max, 1) : 0})`;
    }
  };
  addEventListener('scroll', run, { passive: true });
  addEventListener('resize', run);
  run();

  const burger = $('#burger'), drawer = $('#drawer');
  if (!burger || !drawer) return;
  const toggle = on => {
    burger.classList.toggle('on', on);
    drawer.classList.toggle('on', on);
    burger.setAttribute('aria-expanded', String(on));
    if (lenis) on ? lenis.stop() : lenis.start();
    document.body.style.overflow = on ? 'hidden' : '';
  };
  burger.addEventListener('click', () => toggle(!drawer.classList.contains('on')));
  $$('#drawer a').forEach(a => a.addEventListener('click', () => toggle(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
}

/* ------------------------------------------------------------
   Wash tabs
   ------------------------------------------------------------ */
function tabs() {
  const btns = $$('#washTabs .tab');
  if (!btns.length) return;

  btns.forEach(btn => btn.addEventListener('click', () => {
    if (btn.classList.contains('on')) return;
    btns.forEach(b => { b.classList.remove('on'); b.setAttribute('aria-selected', 'false'); });
    btn.classList.add('on'); btn.setAttribute('aria-selected', 'true');

    $$('.panel').forEach(p => { p.hidden = true; });
    const panel = $('#' + btn.dataset.panel);
    panel.hidden = false;
    const cards = $$('.wash', panel);
    if (REDUCED) return;

    if (anime) {
      anime({ targets: cards, opacity: [0, 1], translateY: [28, 0], scale: [.97, 1],
              delay: anime.stagger(45), duration: 640, easing: 'easeOutExpo' });
    } else {
      cards.forEach((c, i) => {
        c.style.opacity = '0'; c.style.transform = 'translateY(26px)';
        c.style.transition = `opacity .5s ease ${i * 45}ms, transform .5s ease ${i * 45}ms`;
        requestAnimationFrame(() => { c.style.opacity = '1'; c.style.transform = 'none'; });
      });
    }
  }));
}

/* ------------------------------------------------------------
   Cursor-tracked spotlight border + 3D tilt
   ------------------------------------------------------------ */
function pointerFX() {
  if (REDUCED || !FINE) return;

  $$('.spot').forEach(el => {
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    });
  });

  $$('.tilt').forEach(el => {
    el.style.transition = 'transform .5s cubic-bezier(.2,.9,.25,1)';
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - .5;
      const py = (e.clientY - r.top) / r.height - .5;
      el.style.transition = 'transform .12s linear';
      el.style.transform =
        `perspective(900px) rotateY(${px * 9}deg) rotateX(${-py * 9}deg) translateZ(14px)`;
    });
    el.addEventListener('pointerleave', () => {
      el.style.transition = 'transform .6s cubic-bezier(.2,.9,.25,1)';
      el.style.transform = '';
    });
  });
}

/* ------------------------------------------------------------
   Custom cursor — a ring that reacts to what is under it
   ------------------------------------------------------------ */
function cursor() {
  const ring = $('.cur'), dot = $('.cur-d');
  if (!ring || !dot || !FINE || REDUCED) { ring?.remove(); dot?.remove(); return; }

  let x = innerWidth / 2, y = innerHeight / 2, rx = x, ry = y;
  addEventListener('pointermove', e => {
    x = e.clientX; y = e.clientY;
    dot.style.transform = `translate(${x}px,${y}px)`;

    const t = e.target.closest('a,button,.sc,.tab,.demo,.store,.alt,.mini,input,textarea,select');
    ring.classList.toggle('hot', !!t && !t.matches('input,textarea,select'));
    ring.classList.toggle('txt', !!t && t.matches('input,textarea,select'));
  }, { passive: true });

  (function loop() {
    rx += (x - rx) * .17;
    ry += (y - ry) * .17;
    ring.style.transform = `translate(${rx}px,${ry}px)`;
    requestAnimationFrame(loop);
  })();

  addEventListener('pointerdown', () => { ring.style.scale = '.82'; });
  addEventListener('pointerup',   () => { ring.style.scale = '1'; });
}

/* ------------------------------------------------------------
   Magnetic buttons (motion.dev spring)
   ------------------------------------------------------------ */
function magnetic() {
  if (REDUCED || !motion || !FINE) return;
  $$('.btn--house, .fab a, .socials a, .demo-knob').forEach(el => {
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      motion.animate(el, {
        x: (e.clientX - (r.left + r.width / 2)) * .2,
        y: (e.clientY - (r.top + r.height / 2)) * .28
      }, { type: 'spring', stiffness: 320, damping: 22 });
    });
    el.addEventListener('pointerleave', () => {
      motion.animate(el, { x: 0, y: 0 }, { type: 'spring', stiffness: 260, damping: 18 });
    });
  });
}

/* ------------------------------------------------------------
   Showcase panels
   ------------------------------------------------------------ */
function showcase() {
  const wrap = $('#showcase');
  if (!wrap) return;
  const panels = $$('.sc', wrap);

  const open = p => panels.forEach(x => x.classList.toggle('open', x === p));
  panels.forEach(p => {
    p.addEventListener('pointerenter', () => { if (FINE) open(p); });
    p.addEventListener('click', e => {
      if (e.target.closest('a')) return;
      open(p);
    });
    p.addEventListener('focus', () => open(p));
  });
}

/* ------------------------------------------------------------
   The wash demo. Drag the handle and the indigo comes down —
   the whole business in one gesture.
   ------------------------------------------------------------ */
function washDemo() {
  const demo = $('#demo'), wash = $('#demoWash'), bar = $('#demoBar');
  if (!demo || !wash || !bar) return;

  let p = 50, target = 50, down = false, raf = null;

  const paint = () => {
    p += (target - p) * .18;
    wash.style.clipPath = `inset(0 0 0 ${p}%)`;
    bar.style.left = p + '%';
    if (Math.abs(target - p) > .1) raf = requestAnimationFrame(paint);
    else { raf = null; p = target; wash.style.clipPath = `inset(0 0 0 ${p}%)`; bar.style.left = p + '%'; }
  };
  const to = v => {
    target = Math.max(2, Math.min(98, v));
    if (!raf) raf = requestAnimationFrame(paint);
  };
  const fromEvent = e => {
    const r = demo.getBoundingClientRect();
    to((e.clientX - r.left) / r.width * 100);
  };

  demo.addEventListener('pointerdown', e => {
    down = true; demo.classList.add('touched');
    demo.setPointerCapture(e.pointerId); fromEvent(e);
  });
  demo.addEventListener('pointermove', e => {
    if (down) { fromEvent(e); return; }
    if (FINE) { demo.classList.add('touched'); fromEvent(e); }   // follow the cursor
  });
  const stop = () => { down = false; };
  demo.addEventListener('pointerup', stop);
  demo.addEventListener('pointercancel', stop);

  // Nudge it once on first view so people see what it does.
  if (!REDUCED) {
    const io = new IntersectionObserver(es => {
      es.forEach(e => {
        if (!e.isIntersecting) return;
        io.disconnect();
        setTimeout(() => to(74), 420);
        setTimeout(() => to(28), 1500);
        setTimeout(() => to(50), 2500);
      });
    }, { threshold: .45 });
    io.observe(demo);
  }
}

/* ------------------------------------------------------------
   History rail — drag to scroll
   ------------------------------------------------------------ */
function rail() {
  const r = $('#rail');
  if (!r) return;
  let down = false, sx = 0, sl = 0;

  r.addEventListener('pointerdown', e => {
    down = true; sx = e.clientX; sl = r.scrollLeft;
    r.setPointerCapture(e.pointerId); r.style.cursor = 'grabbing';
  });
  r.addEventListener('pointermove', e => { if (down) r.scrollLeft = sl - (e.clientX - sx); });
  const stop = () => { down = false; r.style.cursor = 'grab'; };
  r.addEventListener('pointerup', stop);
  r.addEventListener('pointercancel', stop);
  r.style.cursor = 'grab';

  r.addEventListener('wheel', e => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    const atStart = r.scrollLeft <= 0;
    const atEnd = r.scrollLeft >= r.scrollWidth - r.clientWidth - 1;
    if ((e.deltaY < 0 && atStart) || (e.deltaY > 0 && atEnd)) return;
    e.preventDefault();
    r.scrollLeft += e.deltaY;
  }, { passive: false });
}

/* ------------------------------------------------------------
   Enquiry form — no backend is wired, so hand it to email
   rather than pretend it was sent.
   ------------------------------------------------------------ */
function form() {
  const f = $('#enquiry'), note = $('#formNote');
  if (!f) return;

  f.addEventListener('submit', e => {
    e.preventDefault();
    if (!f.reportValidity()) return;
    const d = new FormData(f);
    const body = [
      `Name: ${d.get('name')}`,
      `Company: ${d.get('company') || '—'}`,
      `Email: ${d.get('email')}`,
      `Phone: ${d.get('phone')}`,
      `Interest: ${d.get('interest')}`, '', d.get('message')
    ].join('\n');

    location.href = 'mailto:blr@motherlandgroup.com'
      + '?subject=' + encodeURIComponent(`Enquiry — ${d.get('interest')}`)
      + '&body=' + encodeURIComponent(body);

    note.textContent = 'Opening your mail app with the enquiry ready to send.';
    note.style.color = 'var(--indigo-lt)';
  });
}

/* ------------------------------------------------------------ */
(async function init() {
  // Never let a slow CDN hold the page hostage.
  await Promise.race([load(), new Promise(r => setTimeout(r, 2500))]);

  smooth();
  splitHeads();
  bootAndHero();
  reveals();
  staggerGroups();
  parallax();
  marquees();
  nav();
  tabs();
  pointerFX();
  cursor();
  magnetic();
  showcase();
  washDemo();
  rail();
  form();
})();
