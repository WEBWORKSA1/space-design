/* Space.Design — core behaviour */
(function () {
  'use strict';
  var d = document, root = d.documentElement;

  /* ---------- Theme ---------- */
  try { var t = localStorage.getItem('sd-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) {}
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-theme-toggle]');
    if (!b) return;
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('sd-theme', next); } catch (e) {}
  });

  /* ---------- Mobile nav ---------- */
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-burger]');
    if (!b) return;
    var m = d.getElementById('menu');
    var open = m.classList.toggle('open');
    b.setAttribute('aria-expanded', open);
  });

  /* ---------- Reveal on scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12 });
    d.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else d.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });

  /* ---------- Cookie notice ---------- */
  var ck = d.getElementById('cookie');
  try {
    if (ck && !localStorage.getItem('sd-consent')) ck.classList.add('show');
  } catch (e) {}
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-consent]');
    if (!b) return;
    try { localStorage.setItem('sd-consent', b.getAttribute('data-consent')); } catch (e) {}
    if (b.getAttribute('data-consent') === 'essential') { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; }
    ck.classList.remove('show');
  });

  /* ---------- Secure routing (address never appears in page source) ---------- */
  var R = [122,104,101,122,114,117,110,118,100,52,67,106,112,100,108,111,49,102,114,112];
  function route() { return R.map(function (c) { return String.fromCharCode(c - 3); }).join(''); }
  window.SD_route = route;

  function serialize(form) {
    var data = {};
    new FormData(form).forEach(function (v, k) {
      if (k === '_honey') return;
      data[k] = data[k] ? data[k] + ', ' + v : v;
    });
    return data;
  }

  function submitForm(form) {
    var msg = form.querySelector('.form-msg');
    var btn = form.querySelector('[type="submit"]');
    if (form.querySelector('[name="_honey"]') && form.querySelector('[name="_honey"]').value) return; // bot
    var data = serialize(form);
    data._subject = '[Space.Design] ' + (form.getAttribute('data-form') || 'Form') + ' — ' + (data.name || data.email || 'New submission');
    data._template = 'table';
    data._captcha = 'false';
    data.page = location.href;
    data.submitted = new Date().toISOString();
    if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Sending…'; }
    fetch('https://formsubmit.co/ajax/' + route(), {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data)
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (j && (j.success === 'true' || j.success === true)) done(true); else throw new Error('fail');
    }).catch(function () {
      // Fallback: open the visitor's mail app with the details pre-filled
      var body = Object.keys(data).filter(function (k) { return k[0] !== '_'; }).map(function (k) { return k + ': ' + data[k]; }).join('\n');
      location.href = 'mailto:' + route() + '?subject=' + encodeURIComponent(data._subject) + '&body=' + encodeURIComponent(body);
      done(true, true);
    });
    function done(ok, viaMail) {
      if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
      if (msg) {
        msg.className = 'form-msg ' + (ok ? 'ok' : 'err');
        msg.textContent = viaMail ? 'Your email app has opened with your details — just press send.' : (form.getAttribute('data-success') || 'Thank you! We received your message and will reply within 1–2 business days.');
      }
      if (ok && !viaMail) { form.reset(); resetSteps(form); }
      try { if (window.gtag) gtag('event', 'generate_lead', { form: form.getAttribute('data-form') }); } catch (e) {}
    }
  }

  d.addEventListener('submit', function (e) {
    var f = e.target.closest('form[data-form]');
    if (!f) return;
    e.preventDefault();
    if (!f.checkValidity()) { f.reportValidity(); return; }
    submitForm(f);
  });

  /* Any element with data-mail opens a pre-addressed email without exposing it */
  d.addEventListener('click', function (e) {
    var a = e.target.closest('[data-mail]');
    if (!a) return;
    e.preventDefault();
    location.href = 'mailto:' + route() + '?subject=' + encodeURIComponent('[Space.Design] ' + a.getAttribute('data-mail'));
  });

  /* ---------- Multi-step forms ---------- */
  function resetSteps(form) {
    var steps = form.querySelectorAll('.step');
    if (!steps.length) return;
    steps.forEach(function (s, i) { s.classList.toggle('active', i === 0); });
    paintBar(form, 0);
  }
  function paintBar(form, i) {
    form.querySelectorAll('.steps span').forEach(function (s, j) { s.classList.toggle('on', j <= i); });
  }
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-step]');
    if (!b) return;
    var form = b.closest('form'), steps = [].slice.call(form.querySelectorAll('.step'));
    var cur = steps.findIndex(function (s) { return s.classList.contains('active'); });
    var dir = b.getAttribute('data-step') === 'next' ? 1 : -1;
    if (dir === 1) {
      var bad = [].slice.call(steps[cur].querySelectorAll('input,select,textarea')).find(function (el) { return !el.checkValidity(); });
      if (bad) { bad.reportValidity(); return; }
    }
    var n = Math.max(0, Math.min(steps.length - 1, cur + dir));
    steps[cur].classList.remove('active'); steps[n].classList.add('active'); paintBar(form, n);
  });

  /* Prefill lead form from query (?project=kitchen) */
  try {
    var qp = new URLSearchParams(location.search);
    ['project', 'style', 'budget'].forEach(function (k) {
      var v = qp.get(k); if (!v) return;
      var el = d.querySelector('form [name="' + k + '"][value="' + v + '"]') || d.querySelector('form [name="' + k + '"]');
      if (el) { if (el.type === 'radio') el.checked = true; else el.value = v; }
    });
  } catch (e) {}

  /* ---------- Tip of the day (self-rotating) ---------- */
  var TIPS = [
    'Leave 36" (91 cm) of clearance for main walkways and 18" (46 cm) between a sofa and coffee table.',
    'Hang curtains 4–6" above the window frame and 8–10" past each side to make windows look larger.',
    'A rug should be large enough that at least the front legs of every seat sit on it.',
    'Use the 60-30-10 rule: 60% dominant colour, 30% secondary, 10% accent.',
    'Art over a sofa should span roughly two-thirds of the sofa width, centred about 57" from the floor.',
    'Layer three kinds of light in every room: ambient, task and accent.',
    'In small rooms, leggy furniture shows more floor and makes the space feel bigger.',
    'Dining chairs need about 24" (61 cm) of table width per person and 36" behind for pull-out.',
    'Paint the ceiling a shade lighter than the walls to add perceived height.',
    'Mirrors opposite windows bounce daylight deeper into a room.',
    'Kitchen work triangle: each leg between sink, stove and fridge should be 4–9 ft.',
    'Pick warm 2700–3000K bulbs for living areas and 3500–4000K for kitchens and workspaces.',
    'Vertical storage — wall shelves, tall cabinets — frees floor area in compact homes.',
    'Bedside tables look best within 2" of mattress height.',
    'Leave 30–36" between a dining table edge and the wall or other furniture.'
  ];
  var tipEl = d.getElementById('tip-of-day');
  if (tipEl) {
    var day = Math.floor(Date.now() / 864e5);
    tipEl.textContent = TIPS[day % TIPS.length];
  }

  /* ---------- Year ---------- */
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Self-updating news & video feeds ----------
     1) data/*.json is refreshed server-side by the GitHub Action.
     2) If it is empty, feeds are pulled live in the browser (cached per session). */
  function esc(s) { return String(s || '').replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function base() { return d.body.getAttribute('data-base') || ''; }
  function getJSON(u) { return fetch(u, { cache: 'no-cache' }).then(function (r) { return r.json(); }); }
  function rss(url) {
    return fetch('https://api.rss2json.com/v1/api.json?rss_url=' + encodeURIComponent(url)).then(function (r) { return r.json(); })
      .then(function (j) { return j && j.status === 'ok' ? j.items || [] : []; }).catch(function () { return []; });
  }
  function cached(key, maker) {
    try { var c = JSON.parse(sessionStorage.getItem(key) || 'null'); if (c && c.length) return Promise.resolve(c); } catch (e) {}
    return maker().then(function (v) { try { if (v.length) sessionStorage.setItem(key, JSON.stringify(v)); } catch (e) {} return v; });
  }
  function byDate(a, b) { return String(b.date || '').localeCompare(String(a.date || '')); }
  function liveNews() {
    return cached('sd-live-news', function () {
      return getJSON(base() + 'data/site.json').then(function (cfg) {
        return Promise.all((cfg.news_feeds || []).slice(0, 8).map(function (f) {
          return rss(f.url).then(function (items) { return items.slice(0, 6).map(function (i) { return { title: i.title, link: i.link, date: String(i.pubDate || '').replace(' ', 'T'), source: f.name }; }); });
        }));
      }).then(function (lists) { return [].concat.apply([], lists).sort(byDate); });
    });
  }
  function liveVideos() {
    return cached('sd-live-videos', function () {
      return getJSON(base() + 'data/site.json').then(function (cfg) {
        return Promise.all((cfg.youtube_channels || []).filter(function (c) { return c.id; }).map(function (c) {
          return rss('https://www.youtube.com/feeds/videos.xml?channel_id=' + c.id).then(function (items) {
            return items.slice(0, 6).map(function (i) {
              var m = String(i.link || i.guid || '').match(/(?:v=|video:)([\w-]{11})/);
              return m ? { id: m[1], title: i.title, channel: i.author || c.handle, date: String(i.pubDate || '').replace(' ', 'T'), category: c.category } : null;
            }).filter(Boolean);
          });
        }));
      }).then(function (lists) { return [].concat.apply([], lists).sort(byDate); });
    });
  }

  var newsEl = d.getElementById('news-feed');
  function renderNews(items, updated) {
    items = items.slice(0, parseInt(newsEl.getAttribute('data-limit') || '12', 10));
    if (!items.length) { newsEl.innerHTML = '<p class="muted">Fresh headlines are being collected — check back shortly.</p>'; return; }
    newsEl.innerHTML = items.map(function (it) {
      return '<a class="feed-item" href="' + esc(it.link) + '" target="_blank" rel="noopener nofollow"><div><span class="feed-src">' + esc(it.source) + '</span><div><strong>' + esc(it.title) + '</strong></div><small>' + esc((it.date || '').slice(0, 10)) + '</small></div></a>';
    }).join('');
    var up = d.getElementById('news-updated'); if (up) up.textContent = updated ? 'Auto-updated ' + updated.slice(0, 16).replace('T', ' ') + ' UTC' : 'Live feed';
  }
  if (newsEl) {
    getJSON(base() + 'data/news.json').then(function (j) {
      if (j.items && j.items.length) return renderNews(j.items, j.updated);
      return liveNews().then(function (items) { renderNews(items); });
    }).catch(function () { liveNews().then(function (items) { renderNews(items); }); });
  }

  var vidEl = d.getElementById('video-feed');
  function renderVideos(all) {
    if (!all.length) { vidEl.innerHTML = '<p class="muted">New videos are being collected — check back shortly.</p>'; return; }
    var limit = parseInt(vidEl.getAttribute('data-limit') || '60', 10);
    var chips = d.getElementById('video-chips');
    function render(cat) {
      var list = all.filter(function (v) { return !cat || cat === 'all' || v.category === cat; }).slice(0, limit);
      vidEl.innerHTML = list.map(function (v) {
        return '<div class="video"><div class="frame" data-yt="' + esc(v.id) + '"><img loading="lazy" src="https://i.ytimg.com/vi/' + esc(v.id) + '/hqdefault.jpg" alt="' + esc(v.title) + '"></div><div class="cap"><strong>' + esc(v.title) + '</strong><small>' + esc(v.channel) + ' · ' + esc((v.date || '').slice(0, 10)) + '</small></div></div>';
      }).join('');
    }
    if (chips) {
      var cats = ['all'].concat(Array.from(new Set(all.map(function (v) { return v.category; }))));
      chips.innerHTML = cats.map(function (c, i) { return '<button class="chip' + (i ? '' : ' on') + '" data-cat="' + esc(c) + '">' + esc(c === 'all' ? 'All videos' : c) + '</button>'; }).join('');
      chips.onclick = function (e) {
        var b = e.target.closest('[data-cat]'); if (!b) return;
        chips.querySelectorAll('.chip').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on');
        render(b.getAttribute('data-cat'));
      };
    }
    render('all');
  }
  if (vidEl) {
    getJSON(base() + 'data/videos.json').then(function (j) {
      if (j.items && j.items.length) return renderVideos(j.items);
      return liveVideos().then(renderVideos);
    }).catch(function () { liveVideos().then(renderVideos); });
  }
  d.addEventListener('click', function (e) {
    var f = e.target.closest('[data-yt]');
    if (!f || f.classList.contains('playing')) return;
    f.classList.add('playing');
    f.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(f.getAttribute('data-yt')) + '?autoplay=1&rel=0" title="YouTube video" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
  });

  /* ---------- Contest countdown ---------- */
  var cd = d.getElementById('countdown');
  if (cd) {
    var now = new Date();
    var end = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1)); // closes at month end, auto-rolls
    var tick = function () {
      var s = Math.max(0, (end - new Date()) / 1000);
      cd.textContent = Math.floor(s / 86400) + 'd ' + Math.floor(s % 86400 / 3600) + 'h ' + Math.floor(s % 3600 / 60) + 'm';
    };
    tick(); setInterval(tick, 30000);
    var cn = d.getElementById('contest-month');
    if (cn) cn.textContent = now.toLocaleString('en', { month: 'long', year: 'numeric' });
  }
})();
