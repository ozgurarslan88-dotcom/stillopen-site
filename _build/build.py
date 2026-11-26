"""Build Road File pages and sitemap.xml from roads_data.py.
Run from the repo root:  python3 _build/build.py
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from roads_data import ROADS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://stillopenroads.com"
e = html.escape

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_short} — Road File — Still Open</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://i.ytimg.com/vi/{id}/maxresdefault.jpg">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Overpass:wght@600;700;800&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230f6b3f'/%3E%3Cpath d='M6 26 C12 18 14 14 26 6' stroke='%23f2c230' stroke-width='4' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="../">
      <svg class="shield" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="#fff"/><path d="M6 26 C12 18 14 14 26 6" stroke="#d9481c" stroke-width="4" fill="none" stroke-linecap="round"/></svg>
      STILL OPEN
    </a>
    <nav>
      <a href="../#roads">Road Files</a>
      <a href="../map.html">Map</a>
      <a href="https://www.youtube.com/@StillOpenRoads?sub_confirmation=1">YouTube</a>
    </nav>
  </div>
</header>
"""

FOOT = """
<footer>
  <div class="wrap">
    <div><strong>Still Open</strong> · <a href="https://www.youtube.com/@StillOpenRoads">youtube.com/@StillOpenRoads</a></div>
    <div class="fine">For information only. Road conditions change; always check your state's 511 service before you drive.</div>
  </div>
</footer>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "84f2dbed3598475ca9df2ff686326174"}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""

def month(d):
    y, m, _ = d.split("-")
    return ["January","February","March","April","May","June","July","August","September","October","November","December"][int(m)-1] + " " + y

def page(r):
    url = f"{SITE}/roads/{r['slug']}.html"
    desc = r["summary"][0]
    if len(desc) > 300: desc = desc[:297].rsplit(" ", 1)[0] + "…"
    ld = {
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": r["title"], "description": " ".join(r["summary"]),
        "thumbnailUrl": [f"https://i.ytimg.com/vi/{r['id']}/maxresdefault.jpg"],
        "uploadDate": r["date"], "embedUrl": f"https://www.youtube.com/embed/{r['id']}",
        "contentUrl": f"https://www.youtube.com/watch?v={r['id']}",
        "publisher": {"@type": "Organization", "name": "Still Open", "url": SITE},
    }
    out = HEAD.format(title_short=e(r["plate"]), title=e(r["title"]), desc=e(desc), url=url, id=r["id"],
                      ld=json.dumps(ld).replace("</", "<\\/"))
    out += f"""
<section class="file-head">
  <div class="wrap">
    <div class="crumb"><a href="../#roads">← All Road Files</a></div>
    <div class="signplate">{e(r['plate'])}</div>
    <h1>{e(r['title'])}</h1>
    <div class="meta">Road File · Published {month(r['date'])} · Facts checked against the sources below</div>
  </div>
</section>

<div class="wrap file-body">
  <main>
    <div class="embed" style="border-radius:10px;overflow:hidden">
      <iframe src="https://www.youtube-nocookie.com/embed/{r['id']}" title="{e(r['title'])}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

    <h2>The short version</h2>
""" + "".join(f"    <p>{e(p)}</p>\n" for p in r["summary"])
    if r.get("timeline"):
        out += "\n    <h2>Timeline</h2>\n    <ul class=\"timeline\">\n"
        for when, what, alert in r["timeline"]:
            out += f"      <li{' class=\"alert\"' if alert else ''}><b>{e(when)}</b> — {e(what)}</li>\n"
        out += "    </ul>\n"
    out += "\n    <h2>Before you drive it</h2>\n    <ul class=\"tips\">\n"
    out += "".join(f"      <li>{e(t)}</li>\n" for t in r["tips"])
    out += "    </ul>\n\n    <h2>Sources</h2>\n    <ol class=\"sources\">\n"
    out += "".join(f"      <li><a href=\"{e(u)}\">{e(n)}</a></li>\n" for n, u in r["sources"])
    out += "    </ol>\n    <p class=\"note\">Crash victims are not named on this site.</p>\n  </main>\n"
    if r.get("facts"):
        out += "\n  <aside>\n    <div class=\"facts\">\n      <h2>By the numbers</h2>\n      <dl>\n"
        out += "".join(f"        <div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>\n" for a, b in r["facts"])
        out += "      </dl>\n    </div>\n  </aside>\n"
    out += "</div>\n" + FOOT
    return out

def main():
    os.makedirs(os.path.join(ROOT, "roads"), exist_ok=True)
    for r in ROADS:
        with open(os.path.join(ROOT, "roads", r["slug"] + ".html"), "w") as f:
            f.write(page(r))
        print("wrote roads/%s.html" % r["slug"])
    pages = ["", "map.html"] + sorted("roads/" + n for n in os.listdir(os.path.join(ROOT, "roads")) if n.endswith(".html"))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}/{p}</loc></url>\n" for p in pages)
    sm += "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt with", len(pages), "pages")

if __name__ == "__main__":
    main()
