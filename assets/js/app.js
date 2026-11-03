/* ============================================================
   MOTHERLAND GROUP
   Interactions and live visuals. No libraries and no network calls,
   so nothing here can fail to load. If this file never runs, every
   word on the site is still visible and only the canvases stay blank.

   Everything that moves forever goes through live(): it draws only
   while its element is on screen, stops when motion is paused, and
   gives up on a device that cannot keep the frame rate.
   ============================================================ */
(() => {
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const CALM  = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const PHONE = matchMedia('(max-width:639px)').matches;
  const MOUSE = matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* ---------- the pause switch ---------- */
  const loops = [];
  let still = CALM || root.classList.contains('still');
  const motionButtons = $$('[data-motion]');
  const labelMotion = () => motionButtons.forEach(b => {
    const text = still ? 'Play motion' : 'Pause motion';
    if (b.dataset.motion === 'icon') b.setAttribute('aria-label', text);
    else b.textContent = text;
  });
  motionButtons.forEach(b => b.addEventListener('click', () => {
    still = !still;
    root.classList.toggle('still', still);
    try { localStorage.setItem('motion', still ? 'off' : 'on'); } catch (e) { /* private mode: it just won't be remembered */ }
    labelMotion();
    loops.forEach(l => l.sync());
  }));
  labelMotion();

  function live(el, draw) {
    const loop = { seen: false, raf: 0, slow: false, skip: false, avg: 16, frames: 0, prev: 0 };
    const tick = now => {
      loop.raf = requestAnimationFrame(tick);
      if (PHONE && (loop.skip = !loop.skip)) return;    // 30fps is plenty on a phone
      const dt = now - loop.prev;
      loop.prev = now;
      if (dt < 250) loop.avg += (dt - loop.avg) * .05;
      if (++loop.frames > 90 && loop.avg > (PHONE ? 80 : 50)) { loop.slow = true; loop.sync(); return; }
      draw(now / 1000);
    };
    loop.sync = () => {
      const run = loop.seen && !still && !loop.slow;
      if (run && !loop.raf) { loop.prev = performance.now(); loop.raf = requestAnimationFrame(tick); }
      if (!run && loop.raf) { cancelAnimationFrame(loop.raf); loop.raf = 0; }
    };
    new IntersectionObserver(([e]) => { loop.seen = e.isIntersecting; loop.sync(); }, { rootMargin: '60px' }).observe(el);
    loops.push(loop);
    draw(performance.now() / 1000);   // always one frame, so a paused page still shows the visual
    return loop;
  }

  /* ---------- menu: a modal <dialog> gives focus trapping and Esc for free ---------- */
  const menu = $('#menu');
  $$('[data-menu]').forEach(b => b.addEventListener('click', () => menu.showModal()));
  $$('[data-menu-close], a', menu).forEach(el => el.addEventListener('click', () => menu.close()));

  /* ---------- tabs ---------- */
  $$('[role=tablist]').forEach(list => {
    const tabs = $$('[role=tab]', list);
    const select = (tab, focus) => tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      $('#' + t.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) t.focus();
    });
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', e => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (!step) return;
        e.preventDefault();
        select(tabs[(i + step + tabs.length) % tabs.length], true);
      });
    });
    select(tabs[0]); // panels start visible in the markup, so they read fine without JS
  });

  /* ---------- lists: an accordion on phones, all open on anything wider ---------- */
  const wide = matchMedia('(min-width:640px)');
  const syncRows = () => $$('.row').forEach(d => {
    d.open = wide.matches;
    $('summary', d).tabIndex = wide.matches ? -1 : 0;
  });
  wide.addEventListener('change', syncRows);
  syncRows();

  /* ---------- hero numbers count up. The markup holds the real value,
     so a frame that never runs leaves the right number on screen. ---------- */
  if (!still) $$('[data-to]').forEach(el => {
    const to = +el.dataset.to, final = el.textContent, t0 = performance.now();
    const tick = now => {
      const p = Math.min((now - t0 - 400) / 1500, 1);
      if (p >= 1) { el.textContent = final; return; }
      el.textContent = Math.round(to * (1 - Math.pow(2, -10 * Math.max(p, 0)))).toLocaleString('en-IN');
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });

  /* ---------- plain arithmetic at the published rate, and the sentence says so ---------- */
  const ticker = $('#ticker');
  if (ticker) {
    const n = $('b', ticker), word = $('[data-word]', ticker), t0 = performance.now();
    const show = () => {
      const v = Math.floor((performance.now() - t0) / 1000 * 100000 / 86400);
      n.textContent = v.toLocaleString('en-IN');
      word.textContent = v === 1 ? 'garment' : 'garments';
    };
    ticker.hidden = false;
    show();
    setInterval(show, 250);
  }

  /* ---------- the hero has depth: figure and drum shift apart under the pointer ---------- */
  const fig = $('.hero-fig');
  if (fig && MOUSE && !CALM) $('.hero').addEventListener('pointermove', e => {
    const r = fig.getBoundingClientRect();
    const clamp = v => Math.max(-1, Math.min(1, v)).toFixed(3);
    fig.style.setProperty('--px', clamp((e.clientX - r.left) / r.width - .5));
    fig.style.setProperty('--py', clamp((e.clientY - r.top) / r.height - .5));
  }, { passive: true });

  /* ---------- division panels take turns. Each one's progress bar is a CSS animation,
     so when hover, the pause switch or scrolling away stops the bar, the turn-taking stops with it. ---------- */
  const inView = el => new IntersectionObserver(([e]) => el.classList.toggle('in-view', e.isIntersecting), { threshold: .25 }).observe(el);
  $$('.showcase').forEach(wrap => {
    inView(wrap);
    const panels = $$('.sc', wrap);
    const open = p => panels.forEach(x => x.classList.toggle('is-open', x === p));
    panels.forEach((p, i) => {
      $('.sc-bar', p).addEventListener('animationend', () => open(panels[(i + 1) % panels.length]));
      p.addEventListener('pointerenter', () => { if (MOUSE) open(p); });
      p.addEventListener('focus', () => open(p));
    });
  });

  /* ---------- the quote stage works the same way ---------- */
  $$('.stage').forEach(stage => {
    inView(stage);
    const quotes = $$('.sq', stage), who = $$('.who', stage);
    const show = n => {
      quotes.forEach((q, i) => q.classList.toggle('is-on', i === n));
      who.forEach((w, i) => { w.classList.toggle('is-on', i === n); w.setAttribute('aria-pressed', i === n); });
    };
    who.forEach((w, i) => {
      w.addEventListener('click', () => show(i));
      $('.who-bar', w).addEventListener('animationend', () => show((i + 1) % who.length));
    });
  });

  /* ---------- enquiry: no backend is wired, so hand it to the visitor's mail app ---------- */
  const form = $('#enquiry');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    const body = [
      `Name: ${d.get('name')}`,
      `Company: ${d.get('company') || '-'}`,
      `Email: ${d.get('email')}`,
      `Phone: ${d.get('phone')}`,
      `Interest: ${d.get('interest')}`, '', d.get('message')
    ].join('\n');
    location.href = 'mailto:blr@motherlandgroup.com'
      + '?subject=' + encodeURIComponent(`Enquiry: ${d.get('interest')}`)
      + '&body=' + encodeURIComponent(body);
    $('#formNote').innerHTML = 'Your mail app should open with the enquiry ready to send. '
      + 'If it doesn&rsquo;t, write to <a href="mailto:blr@motherlandgroup.com">blr@motherlandgroup.com</a>.';
  });

  /* ============================================================
     SHADERS
     ============================================================ */
  const HEAD = `#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
    #else
    precision mediump float;
    #endif
    `;

  /* Returns null when WebGL is unavailable; the CSS background behind the canvas then stays. */
  function shader(canvas, frag, names, scale) {
    const gl = canvas.getContext('webgl', { antialias: false, alpha: false, depth: false, stencil: false, powerPreference: 'low-power' });
    if (!gl) return null;
    const part = (type, src) => {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    };
    const prog = gl.createProgram();
    gl.attachShader(prog, part(gl.VERTEX_SHADER, 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}'));
    gl.attachShader(prog, part(gl.FRAGMENT_SHADER, HEAD + frag));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
    gl.useProgram(prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'p');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    const u = {};
    names.forEach(n => { u[n] = gl.getUniformLocation(prog, n); });
    canvas.addEventListener('webglcontextlost', () => { canvas.style.display = 'none'; });
    return {
      gl, u,
      draw() {
        const w = Math.max(1, Math.round(canvas.clientWidth * scale));
        const h = Math.max(1, Math.round(canvas.clientHeight * scale));
        if (canvas.width !== w || canvas.height !== h) {
          canvas.width = w;
          canvas.height = h;
          gl.viewport(0, 0, w, h);
          if (u.R) gl.uniform2f(u.R, w, h);
          if (u.D) gl.uniform1f(u.D, scale);
        }
        gl.drawArrays(gl.TRIANGLES, 0, 3);
      }
    };
  }

  /* ---------- flowing cloth and dye: a few layers of sines bending each other's
     coordinates. Far cheaper than noise, and it folds like silk. ---------- */
  const FLOW = `
    uniform vec2 R, P; uniform float T, K; uniform vec3 A, B, C;
    void main(){
      vec2 uv = (gl_FragCoord.xy - .5*R) / R.y;
      vec2 p = uv * K;
      float t = T * .16;
      vec2 d = uv - P;
      p += d * exp(-dot(d, d) * 7.) * 1.5;
      for (int i = 0; i < 5; i++) {
        float f = float(i);
        p += vec2(sin(p.y*1.25 + t*(1. + f*.13) + f*1.7), cos(p.x*1.1 - t*(.8 + f*.11) + f*2.3)) * .42;
      }
      float fold = .5 + .5*sin(p.x*1.15 + p.y*.85 + t*.4);
      vec3 col = mix(A, B, smoothstep(0., .8, fold));
      col = mix(col, C, pow(fold, 5.));
      col += (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - .5) / 120.;
      gl_FragColor = vec4(col, 1.);
    }`;

  const PALETTES = {
    silk: { A: [.36, .012, .135], B: [.72, .004, .185], C: [.98, .16, .32], K: 2.7 },
    cta:  { A: [.33, .018, .14],  B: [.60, .010, .17],  C: [.80, .004, .19], K: 1.5 },
    dye:  { A: [.035, .055, .16], B: [.065, .10, .28],  C: [.15, .23, .53],  K: 1.7 }
  };

  $$('[data-flow]').forEach(canvas => {
    const pal = PALETTES[canvas.dataset.flow];
    const s = shader(canvas, FLOW, ['R', 'T', 'P', 'K', 'A', 'B', 'C'], PHONE ? 1 : .7);
    if (!s) return;
    const { gl, u } = s;
    gl.uniform3fv(u.A, pal.A);
    gl.uniform3fv(u.B, pal.B);
    gl.uniform3fv(u.C, pal.C);
    gl.uniform1f(u.K, pal.K);

    // the flow parts around the pointer
    let px = 9, py = 9, tx = 9, ty = 9;
    if (MOUSE) {
      const host = canvas.parentElement;
      host.addEventListener('pointermove', e => {
        const r = canvas.getBoundingClientRect();
        tx = (e.clientX - r.left - r.width / 2) / r.height;
        ty = -(e.clientY - r.top - r.height / 2) / r.height;
        if (px === 9) { px = tx; py = ty; }
      }, { passive: true });
      host.addEventListener('pointerleave', () => { tx = 9; ty = 9; px = 9; py = 9; });
    }
    live(canvas, t => {
      px += (tx - px) * .06;
      py += (ty - py) * .06;
      gl.uniform2f(u.P, px, py);
      gl.uniform1f(u.T, t);
      s.draw();
    });
  });

  /* ---------- denim drawn from its structure: a 3x1 twill of dyed warp over white weft.
     Washing takes the dye off the warp, the raised ribs and the slubs first, in clouds,
     which is why it reads as cloth rather than a colour fade. Light slides across it,
     and the cloth breathes a little. ---------- */
  const CLOTH = `
    uniform vec2 R; uniform float X, D, T;
    float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.-2.*f);
      return mix(mix(h(i), h(i+vec2(1,0)), f.x), mix(h(i+vec2(0,1)), h(i+vec2(1,1)), f.x), f.y); }
    float fbm(vec2 p){ return .5*n(p) + .3*n(p*2.1+7.) + .2*n(p*4.3+13.); }
    void main(){
      vec2 px = gl_FragCoord.xy / D;
      float u = gl_FragCoord.x / R.x;
      vec2 sag = vec2(sin(px.y*.011 + T*.5), cos(px.x*.009 - T*.4)) * 3.;

      float rib  = .5 + .5*sin(((px.x+sag.x)*.89 - (px.y+sag.y)*.454) * 1.2);
      float warp = .5 + .5*sin((px.x+sag.x) * 2.1);
      float slub = n(vec2(px.x*.5, px.y*.016));
      float fine = n(px*.8);
      float cloud = fbm(px*.008);
      float marble = fbm(px*.055);
      vec2 q = vec2(px.x*.96 + px.y*.28, px.y*.96 - px.x*.28);
      float crease = n(vec2(q.x*.004, q.y*.035));

      float w = smoothstep(X-.26, X+.26, u + (cloud-.5)*.16);
      float local = .74 + .55*(cloud-.5) + .6*(marble-.5) + .3*(crease-.5);
      float threadv = (rib-.5)*.3 + (slub-.5)*.3 + (warp-.5)*.1;
      float take = clamp(w*(local + threadv), 0., 1.);

      vec3 raw  = vec3(.040, .070, .205);
      vec3 mid  = vec3(.165, .265, .530);
      vec3 pale = vec3(.650, .745, .880);
      vec3 dye  = mix(mix(raw, mid, smoothstep(0., .55, take)), pale, smoothstep(.45, 1., take));
      dye *= .80 + .40*rib;
      dye *= .95 + .10*slub;

      float fleck = smoothstep(.55, .95, (1.-rib)*warp + fine*.25);
      vec3 col = mix(dye, vec3(.93, .95, .985), fleck*(.07 + .34*take));
      col += (fine-.5)*.03;

      float light = sin(px.x*.0065 + px.y*.0045 - T*.42);
      col *= 1. + .13*smoothstep(.2, 1., light);
      gl_FragColor = vec4(col, 1.);
    }`;

  $$('.swatch').forEach(swatch => {
    const input = $('input', swatch), canvas = $('canvas', swatch);
    const s = shader(canvas, CLOTH, ['R', 'X', 'D', 'T'], Math.min(devicePixelRatio || 1, PHONE ? 1.5 : 2));
    let x = 50, touched = false, down = false, t0 = null, now = 0;

    const paint = () => {
      swatch.style.setProperty('--x', x);
      input.value = Math.round(x);
      if (!s) return;
      s.gl.uniform1f(s.u.X, x / 100);
      s.gl.uniform1f(s.u.T, now);
      s.draw();
    };
    const fromEvent = e => {
      const r = swatch.getBoundingClientRect();
      touched = true;
      x = Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100));
      paint();
    };
    swatch.addEventListener('pointerdown', e => { down = true; swatch.setPointerCapture(e.pointerId); fromEvent(e); });
    swatch.addEventListener('pointermove', e => { if (down || e.pointerType === 'mouse') fromEvent(e); });
    swatch.addEventListener('pointerup', () => { down = false; });
    swatch.addEventListener('pointercancel', () => { down = false; });
    input.addEventListener('focus', () => { touched = true; });
    input.addEventListener('input', () => { touched = true; x = +input.value; paint(); });

    // Left alone, it shows what it does in one wide sweep, then keeps breathing.
    let started = false;
    live(swatch, t => {
      now = t;
      if (!touched && started) {
        if (t0 === null) t0 = t;
        const a = t - t0;
        x = 50 + Math.sin(a * .9) * (11 + 22 * Math.exp(-a * .22));
      }
      started = true;
      paint();
    });
    if (s) new ResizeObserver(paint).observe(swatch);
  });

  /* ============================================================
     THE LINE: garments on an overhead rail, the way a finishing floor
     moves them. On the wash line their colour is tied to where they are
     on screen, so each one fades from raw to bleached as it passes the
     spray bar. On the rack variant they simply keep their own colours.
     ============================================================ */
  const GARMENTS = {
    jeans: {
      h: 178,
      body: 'M-30 22H30L33 40Q38 70 40 178H14L3 84Q0 78-3 84L-14 178H-40Q-38 70-33 40Z',
      lines: 'M-31 32H31M0 32V80M-32 44Q-20 44-14 33M32 44Q20 44 14 33M-39.6 170H-14.6M39.6 170H14.6M-22 22v10M22 22v10M-8 22v10M8 22v10',
      stitch: 'M5 33Q7 58 1 74M-31 47Q-18 47-11 33M31 47Q18 47 11 33M-39.8 173H-14.4M39.8 173H14.4M-30 24.5H30',
      dots: [[-13.5, 34], [13.5, 34], [0, 27]],
      hanger: 'M0 3V19M-27 20H27'
    },
    jacket: {
      h: 126,
      body: 'M-12 16C-6 24 6 24 12 16L40 26Q48 30 50 40L60 118L46 122L36 66V126H-36V66L-46 122L-60 118L-50 40Q-48 30-40 26Z',
      lines: 'M-12 16L-20 31L-2 35L0 27L2 35L20 31L12 16M0 35V126M-36 52H36M-36 114H36M-36 66L-40 34M36 66L40 34M-47.5 114L-60 111M47.5 114L60 111M-28 60h17v14l-8.5 4-8.5-4zM11 60h17v14l-8.5 4-8.5-4z',
      stitch: 'M-36 55H36M-4 36V114M4 36V114M-36 111H36',
      dots: [[0, 44], [0, 62], [0, 80], [0, 98], [-19.5, 66], [19.5, 66]],
      hanger: 'M0 3V13M-40 28L0 13L40 28'
    },
    shirt: {
      h: 138,
      body: 'M-10 16C-5 22 5 22 10 16L36 24Q44 28 46 38L54 112L42 114L33 62L34 132Q0 140-34 132L-33 62L-42 114L-54 112L-46 38Q-44 28-36 24Z',
      lines: 'M-10 16L-15 28L-1 31L0 24L1 31L15 28L10 16M-3 31V136M3 31V136M-33 62L-37 32M33 62L37 32M9 50h16v16l-8 4-8-4z',
      stitch: 'M-42.5 108L-54 106M42.5 108L54 106M-33 128Q0 136 33 128',
      dots: [[0, 42], [0, 60], [0, 78], [0, 96], [0, 114]],
      hanger: 'M0 3V13M-36 26L0 13L36 26'
    },
    tee: {
      h: 118,
      body: 'M-11 16Q0 28 11 16L34 22L54 46L40 58L30 46L31 118H-31L-30 46L-40 58L-54 46L-34 22Z',
      lines: 'M-14 18Q0 34 14 18M-30 46L-34 22M30 46L34 22',
      stitch: 'M-31 112H31M-50 49L-37 60M50 49L37 60',
      dots: [],
      hanger: 'M0 3V13M-32 24L0 13L32 24'
    }
  };
  Object.values(GARMENTS).forEach(g => {
    ['body', 'lines', 'stitch', 'hanger'].forEach(k => { g[k] = new Path2D(g[k]); });
  });

  const WASH_ORDER = ['jeans', 'jacket', 'jeans', 'shirt', 'jeans', 'tee', 'jeans', 'jacket'];
  const RACK_ORDER = ['shirt', 'jeans', 'tee', 'jacket', 'jeans', 'shirt', 'tee', 'jeans'];
  const RACK_COLOURS = ['#2E3F9E', '#10173A', '#DA0133', '#5C73C8', '#2B3355', '#82073A', '#C9893B', '#3F54B8'];
  const rand = i => { const v = Math.sin(i * 12.9898) * 43758.5453; return v - Math.floor(v); };

  $$('[data-line]').forEach(canvas => {
    const ctx = canvas.getContext('2d');
    const rack = canvas.dataset.line === 'rack';
    const order = rack ? RACK_ORDER : WASH_ORDER;
    let W = 0, H = 0, s = 1, railY = 0, gap = 0, span = 0, margin = 0, count = 0, curtain = null;

    const fit = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      W = canvas.clientWidth;
      H = canvas.clientHeight;
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      railY = Math.round(H * .1);
      s = (H - railY - 10) / 178;
      gap = 138 * s;
      margin = 80 * s;
      count = Math.ceil((W + margin * 2) / gap) + 1;
      span = count * gap;
      curtain = ctx.createLinearGradient(W * .36, 0, W * .64, 0);
      curtain.addColorStop(0, 'rgba(92,115,200,0)');
      curtain.addColorStop(.5, 'rgba(92,115,200,.1)');
      curtain.addColorStop(1, 'rgba(92,115,200,0)');
    };

    const garment = (i, x, t) => {
      const g = GARMENTS[order[i % order.length]];
      const u = x / W;
      const inWash = rack ? 0 : Math.exp(-Math.pow((u - .5) / .13, 2));
      const sway = Math.sin(t * 1.25 + i * 1.9) * .022 + Math.sin(t * 5.3 + i) * .04 * inWash;

      ctx.save();
      ctx.translate(x, railY);

      // the trolley riding the rail stays on the rail; only the garment swings
      ctx.fillStyle = '#10173A';
      ctx.beginPath();
      ctx.arc(0, 0, 3.4 * s, 0, Math.PI * 2);
      ctx.fill();

      ctx.rotate(sway);
      ctx.scale(s, s);

      ctx.strokeStyle = '#5F6888';
      ctx.lineWidth = 1.6;
      ctx.stroke(g.hanger);

      ctx.save();
      ctx.translate(3, 5);
      ctx.fillStyle = 'rgba(16,23,58,.07)';
      ctx.fill(g.body);
      ctx.restore();

      if (rack) {
        ctx.fillStyle = RACK_COLOURS[i % RACK_COLOURS.length];
      } else {
        // gradient coordinates are local, so offset them to stay fixed to the screen
        const fade = ctx.createLinearGradient(-x / s, 0, (W - x) / s, 0);
        fade.addColorStop(.34, '#10173A');
        fade.addColorStop(.48, '#2E3F9E');
        fade.addColorStop(.62, '#6B83D2');
        fade.addColorStop(.8, '#A9BCE6');
        ctx.fillStyle = fade;
      }
      ctx.fill(g.body);

      ctx.lineWidth = .8;
      ctx.strokeStyle = rack || u < .56 ? 'rgba(255,255,255,.26)' : 'rgba(16,23,58,.24)';
      ctx.stroke(g.lines);

      ctx.setLineDash([2.6, 2.2]);
      ctx.strokeStyle = '#D9A15C';
      ctx.stroke(g.stitch);
      ctx.setLineDash([]);

      ctx.fillStyle = '#E3B071';
      g.dots.forEach(d => {
        ctx.beginPath();
        ctx.arc(d[0], d[1], 1.25, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.restore();
    };

    const spray = t => {
      const c = W / 2, half = W * .1;
      ctx.fillStyle = curtain;
      ctx.fillRect(W * .36, railY, W * .28, H - railY);

      // the spray bar, with water falling from it
      ctx.fillStyle = '#10173A';
      ctx.fillRect(c - half, railY + 6 * s, half * 2, 4 * s);

      ctx.lineCap = 'round';
      ctx.lineWidth = 1.3;
      const drops = PHONE ? 26 : 54;
      for (let i = 0; i < drops; i++) {
        const y = (rand(i) + t * (.34 + rand(i + 50) * .3)) % 1;
        const dx = c - half + rand(i + 99) * half * 2;
        const dy = railY + 12 * s + y * (H - railY - 12 * s);
        ctx.strokeStyle = `rgba(62,88,190,${(.5 * (1 - y)).toFixed(3)})`;
        ctx.beginPath();
        ctx.moveTo(dx, dy);
        ctx.lineTo(dx, dy + 7 + rand(i + 7) * 7);
        ctx.stroke();
      }

      // suds rising off the floor
      ctx.lineWidth = 1;
      for (let i = 0; i < 16; i++) {
        const y = (rand(i + 200) + t * (.05 + rand(i + 300) * .07)) % 1;
        const bx = c - half * 1.5 + rand(i + 400) * half * 3 + Math.sin(t * 1.4 + i) * 6;
        const by = H - y * H * .5;
        ctx.strokeStyle = `rgba(62,88,190,${(.42 * (1 - y)).toFixed(3)})`;
        ctx.beginPath();
        ctx.arc(bx, by, 1.6 + rand(i + 500) * 3.4, 0, Math.PI * 2);
        ctx.stroke();
      }
    };

    let off = 0, prev = null, lastY = scrollY, boost = 0;
    const speed = rack ? 22 : 34;
    const frame = t => {
      if (!W) fit();
      const dt = prev === null ? 0 : Math.min(t - prev, .1);
      prev = t;
      // scrolling leans on the line a little
      boost += (Math.min(Math.abs(scrollY - lastY), 120) * 1.5 - boost) * .08;
      lastY = scrollY;
      off += (speed + boost) * s * dt;

      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#10173A';
      ctx.fillRect(0, railY - 1, W, 2);
      for (let i = 0; i < count; i++) {
        garment(i, ((i * gap + off) % span) - margin, t);
      }
      if (!rack) spray(t);
    };
    new ResizeObserver(() => { fit(); frame(performance.now() / 1000); }).observe(canvas);
    fit();
    live(canvas, frame);
  });
})();
