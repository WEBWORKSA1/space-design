/* Space.Design — interior style quiz */
(function () {
  'use strict';
  var box = document.getElementById('quiz'); if (!box) return;
  var STYLES = {
    'Japandi': { d: 'Calm, low-slung, natural wood and linen with Japanese restraint and Scandinavian warmth.', c: ['#F1ECE2', '#D8CBB5', '#8C7B65', '#4E5B4C', '#2B2A28'], slug: 'japandi' },
    'Modern Minimal': { d: 'Clean lines, uncluttered surfaces, hidden storage and a tight, neutral palette.', c: ['#FAFAF8', '#E4E2DD', '#9A9894', '#3C3C3C', '#111111'], slug: 'modern-minimal' },
    'Mid-Century Modern': { d: 'Tapered legs, warm teak, organic curves and confident pops of mustard and teal.', c: ['#F3E9D7', '#D9A441', '#C2622D', '#2F6B6A', '#3B2A1E'], slug: 'mid-century-modern' },
    'Warm Industrial': { d: 'Exposed brick, black steel, reclaimed timber and leather softened with plants.', c: ['#E9E4DD', '#A7754F', '#6B4F3A', '#3A3A3A', '#1C1C1C'], slug: 'industrial' },
    'Modern Farmhouse': { d: 'Shiplap, white oak, matte-black hardware and lived-in comfort.', c: ['#FBF8F2', '#E7DDCB', '#A89F91', '#4B4B47', '#1F1F1F'], slug: 'modern-farmhouse' },
    'Bohemian': { d: 'Layered textiles, rattan, global patterns, vintage finds and lots of plants.', c: ['#F5E6D3', '#D88C5A', '#B5523B', '#6A7F4F', '#3D2B3B'], slug: 'bohemian' },
    'Coastal': { d: 'Airy whites, washed blues, sandy textures and breezy natural fibres.', c: ['#FBFBF7', '#E8E1D3', '#A9C3CF', '#4F7C93', '#22394A'], slug: 'coastal' },
    'Art Deco Glam': { d: 'Bold geometry, brass, velvet and jewel tones with a theatrical edge.', c: ['#F4EEE3', '#C9A35B', '#1F5C55', '#5B2340', '#121212'], slug: 'art-deco' }
  };
  var Q = [
    { q: 'Pick the sofa you\'d sink into.', a: [['Low linen sofa, oak base', { 'Japandi': 2, 'Modern Minimal': 1 }], ['Walnut frame, tapered legs', { 'Mid-Century Modern': 2 }], ['Cognac leather, metal frame', { 'Warm Industrial': 2 }], ['Emerald velvet, curved back', { 'Art Deco Glam': 2, 'Bohemian': 1 }]] },
    { q: 'Your ideal floor?', a: [['Wide white-oak planks', { 'Modern Farmhouse': 2, 'Japandi': 1 }], ['Polished concrete', { 'Warm Industrial': 2, 'Modern Minimal': 1 }], ['Layered vintage rugs', { 'Bohemian': 2 }], ['Bleached driftwood tones', { 'Coastal': 2 }]] },
    { q: 'Choose a colour mood.', a: [['Soft neutrals, no fuss', { 'Modern Minimal': 2, 'Japandi': 1 }], ['Mustard, teal, rust', { 'Mid-Century Modern': 2 }], ['Sea-glass blue and sand', { 'Coastal': 2 }], ['Black, gold and jewel tones', { 'Art Deco Glam': 2 }]] },
    { q: 'How much stuff is on display?', a: [['Almost nothing', { 'Modern Minimal': 2, 'Japandi': 1 }], ['A few curated pieces', { 'Mid-Century Modern': 1, 'Art Deco Glam': 1, 'Coastal': 1 }], ['Cosy, collected, practical', { 'Modern Farmhouse': 2 }], ['Everything I love, layered', { 'Bohemian': 2 }]] },
    { q: 'Pick a light fixture.', a: [['Paper lantern pendant', { 'Japandi': 2 }], ['Sputnik-style chandelier', { 'Mid-Century Modern': 1, 'Art Deco Glam': 2 }], ['Caged Edison bulbs', { 'Warm Industrial': 2, 'Modern Farmhouse': 1 }], ['Woven rattan shade', { 'Bohemian': 1, 'Coastal': 2 }]] },
    { q: 'Weekend vibe?', a: [['Tea, a book, quiet', { 'Japandi': 2 }], ['Hosting a dinner party', { 'Art Deco Glam': 1, 'Modern Farmhouse': 1, 'Mid-Century Modern': 1 }], ['Flea markets and record shops', { 'Bohemian': 1, 'Warm Industrial': 1, 'Mid-Century Modern': 1 }], ['Beach walk, open windows', { 'Coastal': 2 }]] },
    { q: 'Favourite material?', a: [['Linen and paper', { 'Japandi': 2 }], ['Lacquer and glass', { 'Modern Minimal': 1, 'Art Deco Glam': 1 }], ['Brick and steel', { 'Warm Industrial': 2 }], ['Shiplap and stoneware', { 'Modern Farmhouse': 2 }]] }
  ];
  var i = 0, score = {};
  function render() {
    if (i >= Q.length) return result();
    var q = Q[i];
    box.innerHTML = '<div class="steps">' + Q.map(function (_, j) { return '<span class="' + (j <= i ? 'on' : '') + '"></span>'; }).join('') + '</div><p class="muted">Question ' + (i + 1) + ' of ' + Q.length + '</p><h3>' + q.q + '</h3><div class="choice-grid">' + q.a.map(function (a, j) { return '<label class="choice"><input type="radio" name="qa" value="' + j + '"><span>' + a[0] + '</span></label>'; }).join('') + '</div>';
  }
  box.addEventListener('change', function (e) {
    if (e.target.name !== 'qa') return;
    var pts = Q[i].a[+e.target.value][1];
    Object.keys(pts).forEach(function (k) { score[k] = (score[k] || 0) + pts[k]; });
    i++; setTimeout(render, 220);
  });
  function result() {
    var top = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; });
    var s = STYLES[top[0]], second = top[1];
    try { localStorage.setItem('sd-style', top[0]); } catch (e) {}
    box.innerHTML = '<span class="tag hot">Your style</span><h2>' + top[0] + '</h2><p>' + s.d + '</p>' + (second ? '<p class="muted">With a touch of <strong>' + second + '</strong>.</p>' : '') +
      '<div class="swatches">' + s.c.map(function (c) { return '<div class="swatch" style="background:' + c + '"></div>'; }).join('') + '</div>' +
      '<div class="hero-cta"><a class="btn btn-accent" href="get-quote.html?style=' + encodeURIComponent(top[0]) + '">Get matched with a ' + top[0] + ' designer</a><a class="btn btn-ghost" href="styles.html#' + s.slug + '">Read the style guide</a><button class="btn btn-ghost" id="quiz-again" type="button">Retake</button></div>';
    document.getElementById('quiz-again').onclick = function () { i = 0; score = {}; render(); };
  }
  render();
})();
