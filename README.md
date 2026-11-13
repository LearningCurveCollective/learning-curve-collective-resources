# Learning Curve Collective: Open Learning Resources

Welcome to the open learning resource library from **Learning Curve Collective**.

This repository contains free mathematics and STEM learning materials designed to help students develop deep conceptual understanding, strong analytical thinking, and lasting academic confidence.

## What you'll find here

- Interactive HTML lessons and worksheets
- Conceptual mathematics guides
- Visual explanations that build intuition
- Structured practice materials for high school and college topics
- Standardized test preparation resources (SAT / ACT / AP)

Every resource is thoughtfully designed by experienced educators to make complex ideas more approachable, engaging, and meaningful.

## Our educational philosophy

At **Learning Curve Collective**, we believe meaningful learning happens when students are encouraged to:

- understand ideas deeply rather than memorize procedures
- develop clear, step-by-step reasoning skills
- connect visual intuition with formal mathematical thinking
- build confidence through consistent, structured practice
- discover connections and patterns across mathematical concepts

Our goal is to help every learner become more curious, capable, and confident, not just in mathematics, but in how they approach learning itself.

## Using these resources

Students, families, educators, and lifelong learners are welcome to explore and use these materials for independent study, classroom enrichment, and academic growth.

This library is freely available as part of Learning Curve Collective's mission to make exceptional educational resources more accessible to everyone.

## Looking ahead

This repository is an evolving project. Planned additions include:

- complete topic learning pathways
- advanced challenge problem sets
- interactive mathematical simulations
- machine learning and data science resources
- AI-powered educational tools

We hope these resources continue to grow into a valuable collection for students and educators around the world.

## How the site is organized

The hub at [learningcurvecollective.github.io/learning-curve-collective-resources](https://learningcurvecollective.github.io/learning-curve-collective-resources/) renders from `catalog.js`, which has one record per sheet (title, description, subject, topic, course order, academic levels, tags).

- `index.html` is the home page: the hero, a search box that looks inside every sheet, the subject pills, and featured resources.
- `math.html`, `test-prep.html`, `economics.html`, `science.html`, `machine-learning.html` and `social-science.html` are the subject pages: one card per course with every sheet listed in course order. They are written by `_build/build_pages.py` from the areas in `catalog.js`.
- `sheet-index.html` is the Index: every sheet grouped by subject in course order, a table of contents. It is also written by `_build/build_pages.py`.
- `assets/site.css` and `assets/site.js` are shared by all of those pages.
- `search-index.js` is written by `_build/build_search_index.py` and holds the searchable words from each sheet.

To add a sheet: drop the .html file in its subject folder, add a record to `catalog.js`, and run `00 Publish.command` (it rebuilds the search index and subject pages, then pushes). `python3 _build/check_catalog.py` lists any sheet that is missing a catalog entry.

To take a sheet off the site without deleting it, add `"hidden": true` to its record in `catalog.js`; remove the flag to bring it back.

To retire a sheet for good, move it into `retired-sheets/` (the README there has the steps). Nothing in that folder is listed on the site, and `check_catalog.py` skips it.

The test-day playbook (`test-prep/Test-Day-Playbook-SAT-PSAT-ACT.html`) is one sheet for all three tests: it opens on whichever test its link names (`?test=sat`, `?test=psat` or `?test=act`), and the reader can switch inside. Its catalog record carries a `variants` entry per section so the SAT & PSAT and ACT sections each link to it with the right default. `test-prep/Final-48-Hours-SAT-PSAT-ACT.html`, the short checklist for the two days before the test, works the same way and closes both sections.

A subject page can use the plain course list or the guided walkthrough (`"layout": "guided"` on the area in `catalog.js`; every subject page uses it now, and the Index keeps the plain list). The guided page opens with a tile per subject (skipped when the area has a single subject, like Economics, where the jump bar lists the steps instead), then lists each subject's sheets as cards under numbered steps taken from that subject's `steps` list; a sheet's `topic` names the step it sits in, and each card shows the sheet's schooling level.

---

© Learning Curve Collective

Resources are provided to support education and academic growth.

Commercial redistribution or resale of these materials is not permitted without the written permission of Learning Curve Collective.
