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
- `assets/site.css` and `assets/site.js` are shared by all of those pages.
- `search-index.js` is written by `_build/build_search_index.py` and holds the searchable words from each sheet.

To add a sheet: drop the .html file in its subject folder, add a record to `catalog.js`, and run `00 Publish.command` (it rebuilds the search index and subject pages, then pushes). `python3 _build/check_catalog.py` lists any sheet that is missing a catalog entry.

---

© Learning Curve Collective

Resources are provided to support education and academic growth.

Commercial redistribution or resale of these materials is not permitted without the written permission of Learning Curve Collective.
