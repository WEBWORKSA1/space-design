/* Space.Design — 2D room planner (canvas). Units: inches internally. */
(function () {
  'use strict';
  var cv = document.getElementById('room'); if (!cv) return;
  var ctx = cv.getContext('2d');
  var CAT = {
    'Sofa (3-seat)': [84, 36, '#C4532F'], 'Loveseat': [60, 34, '#C4532F'], 'Armchair': [32, 34, '#D9825F'], 'Coffee table': [48, 24, '#B08D57'],
    'TV console': [60, 18, '#5C4A3A'], 'Queen bed': [60, 80, '#5F7A65'], 'King bed': [76, 80, '#5F7A65'], 'Twin bed': [38, 75, '#7E9A84'],
    'Nightstand': [22, 18, '#B08D57'], 'Dresser': [60, 20, '#5C4A3A'], 'Dining table (6)': [72, 38, '#8A6A45'], 'Dining chair': [18, 20, '#B08D57'],
    'Desk': [48, 24, '#2F4B6E'], 'Office chair': [24, 24, '#4A6A8E'], 'Bookshelf': [36, 12, '#5C4A3A'], 'Rug 8×10': [96, 120, '#E8D9C0'],
    'Plant': [16, 16, '#5F7A65'], 'Kitchen island': [72, 36, '#8A6A45']
  };
  var items = [], sel = -1, drag = null, roomW = 144, roomL = 168, scale = 1, pad = 30;
  try { var saved = JSON.parse(localStorage.getItem('sd-plan') || 'null'); if (saved) { items = saved.items || []; roomW = saved.w; roomL = saved.l; } } catch (e) {}
  var wIn = document.getElementById('pl-w'), lIn = document.getElementById('pl-l');
  wIn.value = roomW / 12; lIn.value = roomL / 12;

  function size() {
    var maxW = cv.parentElement.clientWidth;
    cv.width = maxW * devicePixelRatio; cv.height = Math.min(640, maxW * 0.8) * devicePixelRatio;
    cv.style.height = (cv.height / devicePixelRatio) + 'px';
    scale = Math.min((cv.width / devicePixelRatio - pad * 2) / roomW, (cv.height / devicePixelRatio - pad * 2) / roomL);
    draw();
  }
  function save() { try { localStorage.setItem('sd-plan', JSON.stringify({ items: items, w: roomW, l: roomL })); } catch (e) {} stats(); }
  function draw() {
    var css = getComputedStyle(document.documentElement);
    ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.save(); ctx.translate(pad, pad);
    // grid (1 ft)
    ctx.strokeStyle = css.getPropertyValue('--line'); ctx.lineWidth = 1;
    for (var x = 0; x <= roomW; x += 12) { ctx.beginPath(); ctx.moveTo(x * scale, 0); ctx.lineTo(x * scale, roomL * scale); ctx.stroke(); }
    for (var y = 0; y <= roomL; y += 12) { ctx.beginPath(); ctx.moveTo(0, y * scale); ctx.lineTo(roomW * scale, y * scale); ctx.stroke(); }
    ctx.strokeStyle = css.getPropertyValue('--ink'); ctx.lineWidth = 4; ctx.strokeRect(0, 0, roomW * scale, roomL * scale);
    ctx.fillStyle = css.getPropertyValue('--muted'); ctx.font = '12px Inter, sans-serif';
    ctx.fillText((roomW / 12).toFixed(1) + ' ft', roomW * scale / 2 - 16, -10);
    ctx.save(); ctx.translate(-12, roomL * scale / 2 + 16); ctx.rotate(-Math.PI / 2); ctx.fillText((roomL / 12).toFixed(1) + ' ft', 0, 0); ctx.restore();
    items.forEach(function (it, i) {
      ctx.globalAlpha = it.n.indexOf('Rug') === 0 ? 0.55 : 0.92;
      ctx.fillStyle = it.c; ctx.fillRect(it.x * scale, it.y * scale, it.w * scale, it.h * scale);
      ctx.globalAlpha = 1;
      ctx.strokeStyle = i === sel ? '#C4532F' : 'rgba(0,0,0,.35)'; ctx.lineWidth = i === sel ? 3 : 1;
      ctx.strokeRect(it.x * scale, it.y * scale, it.w * scale, it.h * scale);
      ctx.fillStyle = '#fff'; ctx.font = '600 11px Inter, sans-serif';
      if (it.w * scale > 50) ctx.fillText(it.n, it.x * scale + 5, it.y * scale + 15);
    });
    ctx.restore();
  }
  function stats() {
    var used = items.filter(function (i) { return i.n.indexOf('Rug') !== 0; }).reduce(function (a, i) { return a + i.w * i.h; }, 0);
    var pct = used / (roomW * roomL) * 100;
    document.getElementById('pl-stats').innerHTML = 'Room: <strong>' + (roomW * roomL / 144).toFixed(0) + ' sq ft</strong> · Furniture footprint: <strong>' + pct.toFixed(0) + '%</strong> ' + (pct > 60 ? '<span style="color:var(--accent)">(crowded — aim ≤ 50–60%)</span>' : '<span style="color:var(--sage)">(balanced)</span>') + ' · Items: ' + items.length;
  }
  function pos(e) {
    var r = cv.getBoundingClientRect(), p = e.touches ? e.touches[0] : e;
    return { x: (p.clientX - r.left - pad) / scale, y: (p.clientY - r.top - pad) / scale };
  }
  function hit(p) { for (var i = items.length - 1; i >= 0; i--) { var it = items[i]; if (p.x >= it.x && p.x <= it.x + it.w && p.y >= it.y && p.y <= it.y + it.h) return i; } return -1; }
  function down(e) { var p = pos(e); sel = hit(p); if (sel > -1) { drag = { dx: p.x - items[sel].x, dy: p.y - items[sel].y }; e.preventDefault(); } draw(); }
  function move(e) {
    if (!drag || sel < 0) return; e.preventDefault();
    var p = pos(e), it = items[sel], snap = document.getElementById('pl-snap').checked ? 6 : 1;
    it.x = Math.round(Math.max(0, Math.min(roomW - it.w, p.x - drag.dx)) / snap) * snap;
    it.y = Math.round(Math.max(0, Math.min(roomL - it.h, p.y - drag.dy)) / snap) * snap;
    draw();
  }
  function up() { if (drag) save(); drag = null; }
  cv.addEventListener('mousedown', down); cv.addEventListener('touchstart', down, { passive: false });
  window.addEventListener('mousemove', move); cv.addEventListener('touchmove', move, { passive: false });
  window.addEventListener('mouseup', up); window.addEventListener('touchend', up);

  var pal = document.getElementById('pl-palette');
  pal.innerHTML = Object.keys(CAT).map(function (k) { return '<button type="button" data-add="' + k + '">＋ ' + k + ' <small class="muted">' + CAT[k][0] + '×' + CAT[k][1] + '"</small></button>'; }).join('');
  pal.addEventListener('click', function (e) {
    var b = e.target.closest('[data-add]'); if (!b) return;
    var c = CAT[b.getAttribute('data-add')];
    items.push({ n: b.getAttribute('data-add'), w: c[0], h: c[1], c: c[2], x: Math.min(Math.max(0, roomW - c[0]), 6 + (items.length * 12) % Math.max(12, roomW - c[0])), y: Math.min(Math.max(0, roomL - c[1]), 6 + (items.length * 12) % Math.max(12, roomL - c[1])) });
    sel = items.length - 1; if (items[sel].n.indexOf('Rug') === 0) { items.unshift(items.pop()); sel = 0; }
    save(); draw();
  });
  function rotate() { if (sel < 0) return; var it = items[sel], t = it.w; it.w = it.h; it.h = t; it.x = Math.min(it.x, roomW - it.w); it.y = Math.min(it.y, roomL - it.h); save(); draw(); }
  function del() { if (sel < 0) return; items.splice(sel, 1); sel = -1; save(); draw(); }
  document.getElementById('pl-rot').onclick = rotate;
  document.getElementById('pl-del').onclick = del;
  document.getElementById('pl-clear').onclick = function () { items = []; sel = -1; save(); draw(); };
  document.getElementById('pl-png').onclick = function () { var a = document.createElement('a'); a.download = 'space-design-plan.png'; a.href = cv.toDataURL('image/png'); a.click(); };
  window.addEventListener('keydown', function (e) {
    if (['INPUT', 'TEXTAREA', 'SELECT'].indexOf(document.activeElement.tagName) > -1) return;
    if (e.key === 'r' || e.key === 'R') rotate();
    if (e.key === 'Delete' || e.key === 'Backspace') { if (sel > -1) { e.preventDefault(); del(); } }
  });
  function resizeRoom() { roomW = Math.max(4, parseFloat(wIn.value) || 12) * 12; roomL = Math.max(4, parseFloat(lIn.value) || 14) * 12; save(); size(); }
  wIn.addEventListener('change', resizeRoom); lIn.addEventListener('change', resizeRoom);
  window.addEventListener('resize', size);
  size(); stats();
})();
