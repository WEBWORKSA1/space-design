#!/usr/bin/env python3
"""Refresh data/news.json and data/videos.json from public RSS feeds. Stdlib only; runs in GitHub Actions.
Only titles, dates and links are stored — every item links back to the original publisher/creator."""
import json, os, re, sys, datetime, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "data", "site.json")))
UA = {"User-Agent": "Mozilla/5.0 (compatible; SpaceDesignBot/1.0; +https://space.design)"}
NS = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def iso(s):
    if not s:
        return ""
    try:
        return parsedate_to_datetime(s).astimezone(datetime.timezone.utc).isoformat()
    except Exception:
        return s.strip()


def parse_feed(raw, source, limit):
    out = []
    root = ET.fromstring(raw)
    for it in root.iter("item"):
        t, l = it.findtext("title"), it.findtext("link")
        if t and l:
            out.append({"title": re.sub(r"\s+", " ", t).strip(), "link": l.strip(), "date": iso(it.findtext("pubDate")), "source": source})
    for e in root.findall("atom:entry", NS):
        t = e.findtext("atom:title", namespaces=NS)
        ln = e.find("atom:link", NS)
        if t and ln is not None:
            out.append({"title": t.strip(), "link": ln.get("href"), "date": e.findtext("atom:updated", namespaces=NS) or e.findtext("atom:published", namespaces=NS) or "", "source": source})
    return out[:limit]


def news():
    items = []
    for f in CFG["news_feeds"]:
        try:
            items += parse_feed(get(f["url"]), f["name"], 8)
            print("news ok", f["name"])
        except Exception as ex:
            print("news skip", f["name"], ex, file=sys.stderr)
    seen, uniq = set(), []
    for i in sorted(items, key=lambda x: x["date"], reverse=True):
        if i["link"] in seen:
            continue
        seen.add(i["link"]); uniq.append(i)
    return uniq[:80]


def channel_id(ch):
    if ch.get("id"):
        return ch["id"]
    html = get("https://www.youtube.com/@" + ch["handle"]).decode("utf-8", "ignore")
    m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', html) or re.search(r'channel/(UC[\w-]{22})', html)
    return m.group(1) if m else None


def videos():
    items = []
    for ch in CFG["youtube_channels"]:
        try:
            cid = channel_id(ch)
            if not cid:
                raise ValueError("no channel id")
            root = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
            cname = root.findtext("atom:title", namespaces=NS) or ch["handle"]
            for e in root.findall("atom:entry", NS)[:6]:
                vid = e.findtext("yt:videoId", namespaces=NS)
                title = e.findtext("atom:title", namespaces=NS)
                if not vid or "#shorts" in (title or "").lower():
                    continue
                items.append({"id": vid, "title": title, "channel": cname, "date": e.findtext("atom:published", namespaces=NS), "category": ch["category"]})
            print("yt ok", ch["handle"])
        except Exception as ex:
            print("yt skip", ch.get("handle"), ex, file=sys.stderr)
    items.sort(key=lambda x: x["date"] or "", reverse=True)
    return items[:120]


def save(name, items):
    path = os.path.join(ROOT, "data", name)
    old = []
    try:
        old = json.load(open(path)).get("items", [])
    except Exception:
        pass
    if not items:  # never wipe good data on a bad run
        print("keeping previous", name)
        return
    json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"), "items": items}, open(path, "w"), indent=1, ensure_ascii=False)
    print("saved", name, len(items), "(was", len(old), ")")


def touch_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p).read()
    today = datetime.date.today().isoformat()
    for page in ("space.design/</loc>", "news.html</loc>", "videos.html</loc>"):
        s = re.sub(r"(" + re.escape(page) + r"<lastmod>)[\d-]+", r"\g<1>" + today, s)
    open(p, "w").write(s)


if __name__ == "__main__":
    save("news.json", news())
    save("videos.json", videos())
    touch_sitemap()
