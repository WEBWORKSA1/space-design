#!/usr/bin/env python3
"""Convert the generated full HTML pages into Jekyll pages (front matter + body) sharing _layouts/default.html,
so GitHub Pages' built-in Jekyll assembles them. Run after build.py:  python3 src/jekyllify.py
Verifies that every page renders byte-identical to the original before writing."""
import os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
pages = sorted(glob.glob("*.html") + glob.glob("guides/*.html"))
FIELDS = ["pre", "t", "d", "canon", "robots", "b", "sch", "nav", "js"]


def split(s):
    v = {}
    m = re.search(r'<meta charset="utf-8">(.*?)\n<meta name="viewport"', s, re.S); v["pre"] = m.group(1)
    v["t"] = re.search(r"<title>(.*?)</title>", s).group(1)
    v["d"] = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
    v["canon"] = re.search(r'<link rel="canonical" href="(.*?)">', s).group(1)
    v["robots"] = re.search(r'\n(<meta name="robots"[^>]*>)\n', s).group(1)
    v["b"] = re.search(r'<body data-base="(.*?)">', s).group(1)
    v["sch"] = re.search(r'adsbygoogle\.js\?client=[^\n]*\n(.*?)\n<script>try', s, re.S).group(1)
    v["nav"] = re.search(r'<ul class="menu" id="menu">(.*?)</ul>', s).group(1)
    v["js"] = re.search(r'assets/js/main\.js" defer></script>(.*?)\n</body>', s, re.S).group(1)
    body = re.search(r'<main id="main">\n(.*)\n</main>', s, re.S).group(1)
    return v, body


def template(s, v):
    """Turn one page into the layout by replacing its variable parts with Liquid tags."""
    lay = s
    i, j = lay.index('<main id="main">\n') + len('<main id="main">\n'), lay.index("\n</main>")
    lay = lay[:i] + "{{ content }}" + lay[j:]
    reps = [
        ('<meta charset="utf-8">' + v["pre"] + "\n", '<meta charset="utf-8">{{ page.pre }}\n'),
        ("<title>" + v["t"] + "</title>", "<title>{{ page.t }}</title>"),
        ('<meta name="description" content="' + v["d"] + '">', '<meta name="description" content="{{ page.d }}">'),
        ('<meta property="og:title" content="' + v["t"] + '">', '<meta property="og:title" content="{{ page.t }}">'),
        ('<meta property="og:description" content="' + v["d"] + '">', '<meta property="og:description" content="{{ page.d }}">'),
        ('href="' + v["canon"] + '">', 'href="{{ page.canon }}">'),
        ('<meta property="og:url" content="' + v["canon"] + '">', '<meta property="og:url" content="{{ page.canon }}">'),
        ("\n" + v["robots"] + "\n", "\n{{ page.robots }}\n"),
        ('crossorigin="anonymous"></script>\n' + v["sch"] + "\n<script>try", 'crossorigin="anonymous"></script>\n{{ page.sch }}\n<script>try'),
        ('<ul class="menu" id="menu">' + v["nav"] + "</ul>", '<ul class="menu" id="menu">{{ page.nav }}</ul>'),
        ('assets/js/main.js" defer></script>' + v["js"] + "\n</body>", 'assets/js/main.js" defer></script>{{ page.js }}\n</body>'),
    ]
    for a, b in reps:
        assert a in lay, a[:60]
        lay = lay.replace(a, b, 1)
    # base path prefix appears in many hrefs: href="../x" / src="../x"
    if v["b"]:
        lay = lay.replace('href="' + v["b"], 'href="{{ page.b }}').replace('src="' + v["b"], 'src="{{ page.b }}')
    else:
        lay = re.sub(r'(href|src)="(?!https?:|#|\{\{)', r'\1="{{ page.b }}', lay)
    lay = lay.replace('<body data-base="' + v["b"] + '">', '<body data-base="{{ page.b }}">')
    return lay


def render(lay, v, body):
    out = lay.replace("{{ content }}", body)
    for k in FIELDS:
        out = out.replace("{{ page.%s }}" % k, v[k])
    return out


def yaml_block(k, val):
    return f"{k}: |-\n" + "\n".join("  " + line for line in val.split("\n")) + "\n" if val else f'{k}: ""\n'


src = {p: open(p, encoding="utf-8").read() for p in pages}
v0, _ = split(src["about.html"])
layout = template(src["about.html"], v0)
bad = []
out = {}
for p, s in src.items():
    v, body = split(s)
    if render(layout, v, body) != s:
        bad.append(p)
    fm = "---\nlayout: default\n" + "".join(yaml_block(k, v[k]) for k in FIELDS) + "---\n"
    out[p] = fm + body
if bad:
    sys.exit("Mismatch: " + ", ".join(bad))
os.makedirs("_layouts", exist_ok=True)
open("_layouts/default.html", "w", encoding="utf-8").write(layout)
for p, s in out.items():
    open(p, "w", encoding="utf-8").write(s)
open("_config.yml", "w").write("# GitHub Pages (Jekyll) wraps each page in _layouts/default.html\nexclude: [src, scripts, README.md]\n")
if os.path.exists(".nojekyll"):
    os.remove(".nojekyll")
print("Jekyll pages:", len(out), "- all render byte-identical")
