#!/usr/bin/env python3
"""
build_search_index.py: read every sheet named in catalog.js and write search-index.js,
a per-resource bag of searchable words taken from the page itself (headings, tab labels,
bold terms, and the rest of the prose).

    python3 _build/build_search_index.py          # writes search-index.js
    python3 _build/build_search_index.py --check  # report only, write nothing

index.html loads search-index.js lazily the first time someone types in a search box, so
the page's first paint is unaffected. Re-run this whenever sheets are added or edited.
"""
import html as _html
import json
import os
import re
import sys

BODY_WORDS = 300          # distinctive prose words kept per sheet
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set("""a an and are as at be been but by can could did do does for from had has have how
if in into is it its may might must no not of on or our over should so some such than that the
their then there these they this those to too use used using was we were what when where which
while who will with would you your it's don't you'll we'll i e g etc vs via per each both all any
one two three four five first second next then also just more most other same very much many
here out up down off on only own too s t re ll ve d m o""".split())
KEEP_SHORT = {"ab", "bc", "ap", "sat", "act", "gre", "psat", "ib", "pv", "fv", "mr", "mc", "atc",
              "avc", "afc", "tr", "tc", "ad", "as", "ppf", "dwl", "cpi", "gdp", "ols", "iv", "dv",
              "ftc", "er", "dna", "rna", "atp", "ph", "pi", "e"}


def words(text):
    text = _html.unescape(text)
    text = re.sub(r"\$([A-Za-z0-9]{1,3})\$", r"\1", text)   # $u$-substitution -> u-substitution
    text = re.sub(r"\$\$?[^$]*\$\$?", " ", text)          # the rest of the LaTeX
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = re.sub(r"[^A-Za-z0-9'\- ]", " ", text)
    out = []
    for w in text.lower().split():
        w = w.strip("'-")
        if not w or w.isdigit():
            continue
        if len(w) < 3 and w not in KEEP_SHORT:
            continue
        if w in STOP:
            continue
        out.append(w)
    return out


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def extract(path):
    """Return (strong_terms, body_words) for one sheet."""
    t = open(path, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"<script\b[^>]*>.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<style\b[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"data:[a-z/+;,-]*base64,[A-Za-z0-9+/=]+", " ", t)

    strong_src = []
    for pat in (r"<h[1-4][^>]*>(.*?)</h[1-4]>",
                r'<button[^>]*class="tab-button[^"]*"[^>]*>(.*?)</button>',
                r"<strong[^>]*>(.*?)</strong>",
                r'<span[^>]*class="[^"]*(?:concept-label|step-label|q-tag|badge)[^"]*"[^>]*>(.*?)</span>',
                r'<div[^>]*class="[^"]*(?:concept-label|formula-note)[^"]*"[^>]*>(.*?)</div>'):
        strong_src += re.findall(pat, t, flags=re.S | re.I)
    strong = []
    seen = set()
    for w in words(" ".join(strip_tags(x) for x in strong_src)):
        if w not in seen:
            seen.add(w)
            strong.append(w)

    body = []
    seen_b = set(strong)
    for w in words(strip_tags(t)):
        if w not in seen_b:
            seen_b.add(w)
            body.append(w)
    return strong, body


def main():
    check = "--check" in sys.argv
    cat = open(os.path.join(ROOT, "catalog.js"), encoding="utf-8").read()
    records = re.findall(r'"id":\s*"([^"]+)",\s*\n\s*"path":\s*"([^"]+)"', cat)
    if not records:
        print("could not read records from catalog.js")
        sys.exit(1)

    raw, missing = {}, []
    for rid, path in records:
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full):
            missing.append(path)
            continue
        raw[rid] = extract(full)

    # A word that turns up in most sheets ("example", "answer", "step") tells a searcher
    # nothing, so drop it from the prose field. Headings and bold terms are kept as they are.
    df = {}
    for strong, body in raw.values():
        for w in set(body):
            df[w] = df.get(w, 0) + 1
    ceiling = max(3, int(len(raw) * 0.4))

    index, total = {}, 0
    for rid, (strong, body) in raw.items():
        body = [w for w in body if df.get(w, 0) <= ceiling]
        # Keep the most distinctive prose words (rarest across the collection) so a term like
        # "photosynthesis" survives while filler does not, and the file stays small enough to
        # fetch on the first keystroke.
        body.sort(key=lambda w: (df.get(w, 0), -len(w)))
        index[rid] = {"k": " ".join(strong), "b": " ".join(body[:BODY_WORDS])}
        total += len(index[rid]["k"]) + len(index[rid]["b"])

    print(f"{len(index)} resources indexed, {total/1024:.0f} KB of words"
          + (f", {len(missing)} missing file(s): {missing}" if missing else ""))
    if check:
        return
    out = ("/* Generated by _build/build_search_index.py: searchable words pulled from each\n"
           "   sheet (headings and bold terms in k, the rest of the prose in b).\n"
           "   Do not edit by hand; re-run the script after adding or editing sheets. */\n"
           "window.SEARCH_INDEX = " + json.dumps(index, separators=(",", ":"), ensure_ascii=False) + ";\n")
    dest = os.path.join(ROOT, "search-index.js")
    open(dest, "w", encoding="utf-8").write(out)
    print(f"wrote search-index.js ({len(out)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
