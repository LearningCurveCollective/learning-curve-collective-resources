#!/usr/bin/env python3
"""
build_pages.py: write one subject page per area in catalog.js (math.html, test-prep.html, ...).

    python3 _build/build_pages.py          # writes the pages at the repo root
    python3 _build/build_pages.py --check  # report only, write nothing

Each page is a small shell: the title, description and heading are baked in (so search
engines and bookmarks see them), and assets/site.js fills in the course cards from
catalog.js when the page loads. Re-run this after adding or renaming an area; adding or
retitling a sheet only needs catalog.js.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}: Open Learning by Learning Curve Collective</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/lcc-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body data-page="area" data-area="{key}">

<header class="topbar">
    <div class="wrap">
        <a class="brand" href="index.html">
            <span class="logo"><img src="assets/lcc-logo.png" alt=""></span>
            <span>
                <span class="brand-name">Open Learning</span><br>
                <span class="brand-by">by Learning Curve Collective</span>
            </span>
        </a>
        <nav class="topnav" aria-label="Site">
            <a class="hide-sm" href="index.html#explore">Subjects</a>
            <a class="hide-sm" href="index.html#featured">Featured</a>
            <a class="hide-sm" href="https://learningcurvecollective.com" target="_blank" rel="noopener">Learning Curve Collective</a>
            <a class="btn btn-gold btn-sm" href="index.html#all">All resources</a>
        </nav>
    </div>
</header>

<main id="top">
<section class="band">
    <div class="wrap">
        <div>
            <p class="crumb"><a href="index.html">Open Learning</a> / {name}</p>
            <h1>{name}</h1>
            <p class="lede">{description}</p>
            <p class="meta" id="band-meta"></p>
        </div>
        <form class="hero-search" id="band-search" role="search">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
            <label class="sr-only" for="bq">Search all resources</label>
            <input id="bq" type="search" placeholder="Search every resource" autocomplete="off">
            <button class="btn btn-gold btn-sm" type="submit">Search</button>
        </form>
    </div>
</section>

<nav class="subnav" aria-label="On this page">
    <div class="wrap"><span class="label">Jump to</span><span id="subnav-links"></span></div>
</nav>

<section class="block" style="padding-top: 32px;">
    <div class="wrap">
        <div id="courses"></div>
        <p class="key" id="key"></p>
    </div>
</section>

<section class="more-areas">
    <div class="wrap">
        <h2>Explore more subjects</h2>
        <ul class="pills" data-pills data-current="{key}"></ul>
    </div>
</section>
</main>

<footer>
    <div class="wrap">
        <div>
            <h3>Open Learning</h3>
            <p>Free, interactive study sheets from the educators at Learning Curve Collective, a tutoring and academic coaching practice in Los Angeles.</p>
            <p>These resources are free for independent study, classroom enrichment, and academic growth.</p>
        </div>
        <div>
            <h3>Learning Curve Collective</h3>
            <ul>
                <li><a href="https://learningcurvecollective.com" target="_blank" rel="noopener">Home</a></li>
                <li><a href="https://learningcurvecollective.com" target="_blank" rel="noopener">Test prep</a></li>
                <li><a href="https://learningcurvecollective.com" target="_blank" rel="noopener">Subject tutoring</a></li>
                <li><a href="https://learningcurvecollective.com" target="_blank" rel="noopener">Book a free consultation</a></li>
            </ul>
        </div>
        <div>
            <h3>This library</h3>
            <ul>
                <li><a href="index.html#explore">Browse by subject</a></li>
                <li><a href="index.html#featured">Featured resources</a></li>
                <li><a href="index.html#all">All resources</a></li>
                <li><a href="https://github.com/LearningCurveCollective/learning-curve-collective-resources" target="_blank" rel="noopener">Source on GitHub</a></li>
            </ul>
        </div>
        <p class="fine">&copy; Learning Curve Collective. Commercial redistribution or resale of these materials is not permitted without written permission.</p>
    </div>
</footer>

<script src="catalog.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""


def load_catalog():
    js = open(os.path.join(ROOT, "catalog.js"), encoding="utf-8").read()
    return json.loads(js[js.index("{"):js.rindex("}") + 1])


def main():
    check = "--check" in sys.argv
    cat = load_catalog()
    problems = 0
    for a in cat["areas"]:
        page = a.get("page")
        if not page or "/" in page or not page.endswith(".html"):
            print(f"AREA {a['key']}: needs a \"page\" like \"{a['key']}.html\" in catalog.js")
            problems += 1
            continue
        out = TEMPLATE.format(key=html.escape(a["key"]), name=html.escape(a["name"]),
                              description=html.escape(a.get("blurb", cat["site"]["description"])))
        dest = os.path.join(ROOT, page)
        current = open(dest, encoding="utf-8").read() if os.path.isfile(dest) else None
        if current == out:
            print(f"unchanged  {page}")
        elif check:
            print(f"would write {page}")
        else:
            open(dest, "w", encoding="utf-8").write(out)
            print(f"wrote      {page}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
