# Space.Design

Space.Design is a free "plan · measure · design" platform. It includes a 2D room planner, 9 calculators, a style quiz, original guides, a design news and video feed that updates itself, a designer and contractor matching funnel, donations, contests, careers and advertising pages.

It is a static site with no build step needed at deploy time. It is ready for GitHub Pages on the free plan, served from the `main` branch at `/ (root)`.

## Monetization
- **Google AdSense:** the `ca-pub-6620975821265271` loader is on every page, along with `ads.txt` and the policy pages.
- **Lead generation:** `/get-quote.html` plus an inline 4-step form, and `/pros.html` for professionals who want to join the network.
- **Sponsorship and advertising:** `/advertise.html`, plus the top bar that links to the owner's contact page.
- **Donations:** `/donate.html`. Add your PayPal, Stripe or Buy Me a Coffee links in `data/site.json` and the buttons appear automatically.

## Forms
All forms post through FormSubmit's AJAX endpoint. The destination address is assembled at runtime from encoded character codes in `assets/js/main.js`, so it never appears in the HTML. The **first** submission sends a one-time activation email, and you need to click it once to activate.

## Self-updating
`.github/workflows/build.yml` regenerates every page whenever `src/` or `assets/` changes. Every 6 hours it also runs `scripts/update_feeds.py`, which refreshes `data/news.json` from 10 design RSS feeds and `data/videos.json` from 12 YouTube channels. The feed lists live in `data/site.json`.

## Editing pages
Page HTML is generated from `src/build.py`, and guide articles are in `src/guides.py`. Edit either one and push: the workflow rebuilds the site. To build locally, run:

```
cd src && python3 build.py
```

## Go live on space.design
1. Turn on Pages: Settings, then Pages, then Deploy from branch, then `main`, then `/ (root)`.
2. Add a `CNAME` file containing `space.design`. At your registrar, point the domain at GitHub Pages with A records for 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153.
3. Turn on "Enforce HTTPS", then submit the site in AdSense.

See `docs/BUILD-PROMPT.md` for the phase-by-phase build prompt and `docs/BENCHMARK.md` for the 35-site competitive benchmark.

© Space.Design. Independent website. Not affiliated with any company named "Space Design". See `disclaimer.html`.
