#!/usr/bin/env python3
"""Checks catalog.js against the .html files in this repo.
Run from the repo root:  python3 _build/check_catalog.py
Reports sheets on disk that have no catalog entry (they will show on the site only as
"Recently added" until you add them) and catalog entries whose file is missing or renamed.
"""
import json, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js = open(os.path.join(root, 'catalog.js'), encoding='utf-8').read()
cat = json.loads(js[js.index('{'):js.rindex('}') + 1])
known = {r['path'] for r in cat['resources']}
disk = set()
for d, dirs, files in os.walk(root):
    dirs[:] = [x for x in dirs if not x.startswith('.') and not x.startswith('_') and x != 'assets']
    for f in files:
        if f.endswith('.html'):
            p = os.path.relpath(os.path.join(d, f), root)
            # sheets live in subject folders; .html files at the root are the hub pages
            # (index.html and the subject pages written by build_pages.py)
            if '/' in p:
                disk.add(p)
ids = [r['id'] for r in cat['resources']]
dups = {i for i in ids if ids.count(i) > 1}
problems = 0
for p in sorted(disk - known):
    print('NOT IN CATALOG :', p); problems += 1
for p in sorted(known - disk):
    print('FILE MISSING   :', p); problems += 1
for i in sorted(dups):
    print('DUPLICATE ID   :', i); problems += 1
levels = set(cat['levels'])
for r in cat['resources']:
    for key in ('id', 'path', 'title', 'description', 'subject', 'topic', 'order', 'levels', 'format'):
        if key not in r:
            print('MISSING FIELD  :', r.get('path'), key); problems += 1
    for l in r.get('levels', []):
        if l not in levels:
            print('UNKNOWN LEVEL  :', r['path'], l); problems += 1
    if '—' in json.dumps(r, ensure_ascii=False):
        print('EM DASH        :', r['path']); problems += 1
    if r.get('subject') not in {s['key'] for s in cat['subjects']}:
        print('UNKNOWN SUBJECT:', r['path'], r.get('subject')); problems += 1
print(f"{len(cat['resources'])} catalog entries, {len(disk)} sheets on disk, {problems} problem(s)")
sys.exit(1 if problems else 0)
