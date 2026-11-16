/* Space.Design — calculators & generators */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var num = function (id) { var v = parseFloat(($(id) || {}).value); return isNaN(v) ? 0 : v; };
  var fmt = function (n, d) { return Number(n).toLocaleString('en', { maximumFractionDigits: d == null ? 1 : d }); };
  var SQM = 10.7639;
  function unit(form) { var u = document.querySelector('[name="' + form + '-unit"]:checked'); return u ? u.value : 'ft'; }
  function bind(id, fn) { var f = $(id); if (!f) return; f.addEventListener('input', fn); f.addEventListener('change', fn); fn(); }
  function cta(project) { return '<div class="mt"><a class="btn btn-sm btn-accent" href="get-quote.html?project=' + project + '">Get free quotes from vetted pros →</a></div>'; }

  /* 1. Paint */
  bind('paint-form', function () {
    var u = unit('paint'), L = num('p-l'), W = num('p-w'), H = num('p-h');
    var doors = num('p-doors'), wins = num('p-wins'), coats = num('p-coats') || 2, ceil = $('p-ceil').checked;
    var wall = 2 * (L + W) * H;
    var dArea = u === 'ft' ? 21 : 1.95, wArea = u === 'ft' ? 15 : 1.4;
    var area = Math.max(0, wall - doors * dArea - wins * wArea) + (ceil ? L * W : 0);
    var cover = u === 'ft' ? 350 : 32.5; // sq ft per US gal / m² per 3.785 L
    var cans = area * coats / cover;
    var liters = cans * 3.785;
    $('paint-out').innerHTML = 'Paintable area: <strong>' + fmt(area) + ' ' + (u === 'ft' ? 'sq ft' : 'm²') + '</strong><br>You need about <b>' + fmt(Math.ceil(cans * 10) / 10) + ' gal</b> (' + fmt(liters) + ' L) for ' + coats + ' coat(s). Buy ' + Math.ceil(cans) + ' gallon(s) plus a quart for touch-ups.' + cta('painting');
  });

  /* 2. Flooring */
  bind('floor-form', function () {
    var u = unit('floor'), L = num('f-l'), W = num('f-w'), waste = num('f-waste'), box = num('f-box'), price = num('f-price');
    var area = L * W, total = area * (1 + waste / 100);
    var boxes = box ? Math.ceil(total / box) : 0;
    var unitLbl = u === 'ft' ? 'sq ft' : 'm²';
    $('floor-out').innerHTML = 'Room area: <strong>' + fmt(area) + ' ' + unitLbl + '</strong> · with ' + waste + '% waste: <b>' + fmt(total) + ' ' + unitLbl + '</b>' + (boxes ? '<br>Boxes needed: <strong>' + boxes + '</strong>' : '') + (price ? '<br>Material cost: <strong>$' + fmt(total * price, 2) + '</strong>' : '') + cta('flooring');
  });

  /* 3. Rug size */
  bind('rug-form', function () {
    var u = unit('rug'), L = num('r-l'), W = num('r-w'), room = $('r-room').value;
    var border = u === 'ft' ? 1.5 : 0.45; // leave ~18" floor border
    var rl = Math.max(0, L - 2 * border), rw = Math.max(0, W - 2 * border);
    var std = u === 'ft' ? [[3, 5], [4, 6], [5, 8], [6, 9], [8, 10], [9, 12], [10, 14], [12, 15]] : [[0.9, 1.5], [1.2, 1.8], [1.6, 2.3], [2, 2.9], [2.4, 3], [2.7, 3.7], [3, 4.3], [3.7, 4.6]];
    var best = std.filter(function (s) { return s[0] <= Math.min(rl, rw) && s[1] <= Math.max(rl, rw); }).pop() || std[0];
    var advice = { living: 'Front legs of all seating should sit on the rug.', bedroom: 'Extend the rug 18–24" beyond each side of the bed; start it just in front of the nightstands.', dining: 'Add 24" (60 cm) on every side of the table so chairs stay on the rug when pulled out.', entry: 'Leave 6–12" of floor visible on all sides; runners suit narrow halls.' }[room];
    $('rug-out').innerHTML = 'Recommended standard size: <b>' + best[0] + ' × ' + best[1] + ' ' + (u === 'ft' ? 'ft' : 'm') + '</b><br>Maximum that still leaves a floor border: ' + fmt(rw) + ' × ' + fmt(rl) + '<br><span class="muted">' + advice + '</span>';
  });

  /* 4. Lighting (lumens) */
  bind('light-form', function () {
    var u = unit('light'), L = num('l-l'), W = num('l-w'), type = $('l-type').value;
    var sqft = u === 'ft' ? L * W : L * W * SQM;
    var fc = { living: [10, 20], bedroom: [10, 20], kitchen: [30, 40], bathroom: [70, 80], office: [30, 50], dining: [30, 40], hallway: [5, 10] }[type];
    var lo = sqft * fc[0], hi = sqft * fc[1];
    $('light-out').innerHTML = 'Target: <b>' + fmt(lo, 0) + '–' + fmt(hi, 0) + ' lumens</b> total<br>≈ ' + Math.ceil(lo / 800) + '–' + Math.ceil(hi / 800) + ' standard 800-lm (60 W-equivalent) LED bulbs, split across ambient, task and accent sources.' + cta('lighting');
  });

  /* 5. Renovation budget */
  bind('budget-form', function () {
    var u = unit('budget'), area = num('b-area'), room = $('b-room').value, level = $('b-level').value, region = parseFloat($('b-region').value);
    var sqft = u === 'ft' ? area : area * SQM;
    var rates = { kitchen: [150, 300, 550], bathroom: [200, 400, 700], living: [40, 90, 180], bedroom: [35, 80, 160], basement: [50, 100, 175], office: [40, 85, 170] }[room];
    var r = rates[{ basic: 0, mid: 1, luxury: 2 }[level]] * region;
    var lo = sqft * r * 0.8, hi = sqft * r * 1.2;
    $('budget-out').innerHTML = 'Estimated range: <b>$' + fmt(lo, 0) + ' – $' + fmt(hi, 0) + '</b><br><span class="muted">Planning estimate only (USD, materials + labour). Add a 10–20% contingency. Real quotes vary by site conditions.</span>' + cta(room);
  });

  /* 6. Wallpaper rolls */
  bind('paper-form', function () {
    var u = unit('paper'), P = num('w-perim'), H = num('w-h'), rep = num('w-rep');
    var rollW = u === 'ft' ? 1.75 : 0.53, rollL = u === 'ft' ? 33 : 10.05;
    var dropH = H + (rep ? rep / (u === 'ft' ? 12 : 100) : 0) + (u === 'ft' ? 0.33 : 0.1);
    var strips = Math.ceil(P / rollW), perRoll = Math.floor(rollL / dropH) || 1;
    var rolls = Math.ceil(strips / perRoll);
    $('paper-out').innerHTML = 'Strips needed: <strong>' + strips + '</strong> · Strips per roll: <strong>' + perRoll + '</strong><br>Buy <b>' + (rolls + 1) + ' rolls</b> (includes one spare from the same batch).';
  });

  /* 7. Furniture clearance */
  bind('fit-form', function () {
    var u = unit('fit'), RL = num('c-rl'), RW = num('c-rw'), FL = num('c-fl'), FW = num('c-fw');
    var need = u === 'ft' ? 3 : 0.91;
    var leftL = RL - FL, leftW = RW - FW;
    var ok = leftL >= need && leftW >= need;
    $('fit-out').innerHTML = 'Free space: <strong>' + fmt(leftL, 2) + '</strong> lengthwise, <strong>' + fmt(leftW, 2) + '</strong> widthwise.<br>' + (ok ? '<b>✓ Fits comfortably</b> — at least ' + need + ' ' + u + ' walkway remains.' : '<b style="color:var(--accent)">⚠ Tight fit</b> — main walkways should be ' + need + ' ' + u + ' or more.') + '<br>Coverage: ' + fmt(FL * FW / (RL * RW || 1) * 100, 0) + '% of the floor (aim for ≤ 50–60%).';
  });

  /* 8. Art hanging height */
  bind('art-form', function () {
    var u = unit('art'), h = num('a-h'), hook = num('a-hook'), eye = u === 'in' ? 57 : 145;
    var nail = eye + h / 2 - hook;
    $('art-out').innerHTML = 'Put the nail <b>' + fmt(nail) + ' ' + u + '</b> above the floor (gallery standard: art centre at ' + eye + ' ' + u + ').';
  });

  /* 9. Colour palette generator */
  function hexToHsl(hex) {
    hex = hex.replace('#', ''); var r = parseInt(hex.substr(0, 2), 16) / 255, g = parseInt(hex.substr(2, 2), 16) / 255, b = parseInt(hex.substr(4, 2), 16) / 255;
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), h, s, l = (mx + mn) / 2;
    if (mx === mn) h = s = 0; else { var dd = mx - mn; s = l > .5 ? dd / (2 - mx - mn) : dd / (mx + mn); h = mx === r ? (g - b) / dd + (g < b ? 6 : 0) : mx === g ? (b - r) / dd + 2 : (r - g) / dd + 4; h *= 60; }
    return [h, s * 100, l * 100];
  }
  function hsl(h, s, l) {
    h = ((h % 360) + 360) % 360; s /= 100; l /= 100;
    var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l);
    var f = function (n) { return l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))); };
    return '#' + [f(0), f(8), f(4)].map(function (x) { return Math.round(x * 255).toString(16).padStart(2, '0'); }).join('').toUpperCase();
  }
  function genPalette() {
    var base = $('pal-base').value, mode = $('pal-mode').value, c = hexToHsl(base), h = c[0], s = c[1], l = c[2], out;
    if (mode === 'analogous') out = [hsl(h - 30, s, l), hsl(h - 15, s, l + 8), base, hsl(h + 15, s, l + 8), hsl(h + 30, s, l)];
    else if (mode === 'complementary') out = [hsl(h, s * .4, 92), hsl(h, s, l), base, hsl(h + 180, s * .8, l), hsl(h + 180, s * .4, 25)];
    else if (mode === 'triadic') out = [hsl(h, s * .2, 94), base, hsl(h + 120, s * .7, l), hsl(h + 240, s * .7, l), hsl(h, s * .3, 18)];
    else out = [hsl(h, s * .15, 95), hsl(h, s * .3, 80), base, hsl(h, s, Math.max(10, l - 20)), hsl(h, s * .4, 15)];
    out = out.map(function (x) { return x.length === 7 ? x.toUpperCase() : x; });
    $('pal-out').innerHTML = out.map(function (c, i) {
      var light = hexToHsl(c)[2] > 60;
      return '<div class="swatch" title="Click to copy" data-copy="' + c + '" style="background:' + c + ';color:' + (light ? '#111' : '#fff') + '">' + c + '<br>' + ['60% walls', '30% textiles', 'Base', '10% accent', 'Anchor'][i] + '</div>';
    }).join('');
  }
  if ($('palette-form')) {
    $('palette-form').addEventListener('input', genPalette);
    $('palette-form').addEventListener('change', genPalette);
    $('pal-random') && $('pal-random').addEventListener('click', function () { $('pal-base').value = hsl(Math.random() * 360, 35 + Math.random() * 40, 35 + Math.random() * 30); genPalette(); });
    genPalette();
    document.addEventListener('click', function (e) {
      var s = e.target.closest('[data-copy]'); if (!s) return;
      try { navigator.clipboard.writeText(s.getAttribute('data-copy')); s.style.outline = '3px solid var(--accent)'; setTimeout(function () { s.style.outline = ''; }, 600); } catch (er) {}
    });
  }
})();
