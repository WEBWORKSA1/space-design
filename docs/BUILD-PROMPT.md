# Space.Design — Phase-wise Build Prompt

**Concept:** Space.Design is a free "plan · measure · design" hub. It offers a 2D room planner, 9 calculators, a style quiz and practical guides. Those pull in organic traffic, which is monetized with Google AdSense. A multi-step "get matched with a designer/contractor" funnel turns visitors into leads you can sell or refer.

**Why this concept:** Interior design and home improvement are high-CPC AdSense verticals. Benchmarks show roughly 110K monthly searches for "interior design" at about a $7 CPC, and "home improvement services" at about a $9 CPC. Tools bring in repeat, linkable traffic. Every calculator result is a natural moment to offer a quote. Each lead from a designer or contractor can sell for far more than an ad click.

---

## Phase 1: Foundation and compliance
1. Build a static HTML/CSS/JS site with no framework, so it hosts free on GitHub Pages from the `main` branch root. Add `.nojekyll`.
2. Put the AdSense loader in the `<head>` of every page: `ca-pub-6620975821265271`. Add the `google-adsense-account` meta tag and `ads.txt`.
3. Add a top bar on every page that reads "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" and links to `https://web.works/contact`. Show the link text only. Never show the URL.
4. Create the policy pages: Privacy (with the AdSense cookie wording and opt-out links), Terms, a Disclaimer with a trademark and copyright notice ("not affiliated with any company named Space Design / SpaceDesign"), About and Contact.
5. Add a cookie notice with "Accept all" and "Essential only". The "Essential only" choice sets non-personalized ads.

## Phase 2: Design system
- Use a warm architectural palette: paper, ink, terracotta, sage and brass. Add a blueprint-grid motif.
- Type: Fraunces for display text and Inter for UI.
- Include dark mode, mobile-first layout, an accessible skip link, focus states and reduced-motion support.

## Phase 3: Traffic engines (tools)
- Build a 2D room planner on canvas with true-to-scale furniture. It should support drag, rotate, delete, snap, a live footprint percentage, saving to localStorage and PNG export.
- Build 9 calculators: paint, flooring, rug size, lumens, renovation budget, wallpaper, furniture fit, art height and a 60-30-10 palette generator. Each should work in feet or metres.
- Add a 7-question style quiz that returns a style, a palette and a link to a designer match.

## Phase 4: Content for AdSense approval and SEO
- Write 9 or more original long-form guides: layout, kitchen costs, hiring a designer, home office, bathroom, lighting, colour, storage and open-plan zoning. Use tables, a table of contents and internal links to the tools.
- Add a library of 10 design styles.
- Add structured data: WebSite, FAQPage, Article and WebApplication. Also add canonical tags, Open Graph tags, `sitemap.xml` and `robots.txt`.

## Phase 5: Lead generation (main revenue lever)
- Build a 4-step matching form: project, then scope and style, then budget, timing and location, then contact details and consent. Add a progress bar and prefill from URL parameters (`?project=kitchen`).
- Put the form on the home page and on a dedicated `/get-quote.html` page. Link a quote CTA from every tool result and every guide.
- Add a supply-side form at `/pros.html` so designers and contractors can apply to join the network. This opens the door to paid listings later.
- Send every form to one inbox. The address is assembled at runtime from encoded character codes and posted through the FormSubmit AJAX endpoint. If that fails, open a pre-filled mailto link. The address never appears in the HTML.

## Phase 6: Community and funding
- **Donate:** offer tiers ($5, $15 a month, $50 a month, and a prize fund) and show how the money is allocated (operations, tools, marketing, hiring, prizes). Include a pledge form. Payment buttons appear automatically from `data/site.json`.
- **Contests:** run a monthly Small Space Challenge with an auto-rolling countdown, an entry form, judging criteria, a prize structure, sponsor slots and official rules.
- **Careers:** list 6 remote roles and an application form.
- **Advertise:** offer 8 sponsorship and partnership products and a media-kit request form.

## Phase 7: Automation (self-updating)
- A GitHub Action runs every 6 hours, on push and on demand. It pulls headlines from 10 design publications' RSS feeds and the latest videos from 12 YouTube channels. Channel handles are resolved to IDs automatically.
- It writes `data/news.json` and `data/videos.json` and refreshes the `sitemap.xml` lastmod. It never wipes good data after a failed run.
- The client side adds a rotating designer tip of the day, a contest countdown that rolls over monthly, and click-to-load YouTube embeds in privacy-enhanced mode.

## Phase 8: Launch
1. Push to `WEBWORKSA1/space-design` on `main`.
2. Go to Settings, then Pages, choose "Deploy from a branch" with `main` and `/ (root)`.
3. Add a custom domain by putting a `CNAME` file containing `space.design` in the repo, then point DNS at GitHub Pages.
4. Activate FormSubmit by clicking the confirmation email that the first form submission sends.
5. Add the site in AdSense, verify `ads.txt`, and request review.
