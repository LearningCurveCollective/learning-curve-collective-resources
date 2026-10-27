---
name: sat-math-topic-sheet
description: Build or revise a sheet in the Learning Curve Collective SAT Math topic series (the six-tab Learn/Drill/Check format of SAT-Math-1-Linear-Equations and SAT-Math-2-Quadratics, with a Rules tab, worked-example stepper, fluency drills, SAT-Style Practice set, challenge questions, and exit ticket). Use this whenever the user asks for the next SAT math sheet or topic sheet (exponents, percentages, geometry, trig, systems, etc.), says "like the linear sheet" or "like the quadratics one", pastes prep-book pages to turn into a topic sheet, or asks to audit, renumber, or restyle an existing sheet in the series. Do NOT use for the four-tab interactive worksheet format (that is the sat-math-worksheet skill) or for Reading & Writing content.
---

# SAT Math Topic Sheet Builder

This skill encodes every convention agreed for the Learning Curve Collective SAT Math
topic series, so a new sheet comes out right the first time instead of needing rounds
of auditing. Read this whole file before building; the conventions below are the audit.

## The series so far

| # | File (in `test-prep/sat/`) | Topic |
|---|---|---|
| 0 | `SAT-Desmos-Strategies.html` | Calculator techniques |
| 1 | `SAT-Math-1-Linear-Equations.html` | Linear equations (this file is the SHELL SOURCE) |
| 2 | `SAT-Math-2-Quadratics.html` | Quadratics |

Live URLs follow `https://learningcurvecollective.github.io/learning-curve-collective-resources/<path>`.
The site serves from `main`; work on the session's designated branch and merge to
`main` only when the user says to publish.

## How a sheet is built

Do not hand-write the HTML. Copy `scripts/build_quadratics.py` (the complete worked
example that produced sheet 2), rename it for the new topic, and rewrite only its
content blocks. The script reads the linear sheet as the shell (CSS, tabs, graders,
Desmos panel, the agreed voice) and swaps in content:

- `RULES` - the Rules tab HTML (rule cards, tables, examples, traps section).
- `STEPS` - the worked-example stepper (one dict per step, each with a micro check).
- `FLUENCY`, `GAUNTLET`, `CHALLENGE`, `EXIT` - the drill and practice data.
- `FIGS_JS` - figure specs for the SVG renderer (lines, parabolas via `curves`, points,
  shaded polygons). The builder injects a quadratic-curve renderer; reuse it.
- A block of `replace_once` calls for topic strings: title, subtitle, tab-1 name,
  intro cards, exit-ticket links, the Desmos-guidance examples, the practice-ramp tail,
  and the localStorage key.

The builder strips the shell's "Ready for the next topic?" forward link so a copied
sheet never links to itself; keep that guard. Every `replace_once` asserts exactly one
match, so a drifted shell fails loudly instead of silently producing a broken page.

String literals in the content dicts are r-strings, so `\"` inside them arrives as
backslash-quote; the `_clean` pass in `js_data` strips it. Keep that pass.

## Content conventions (the audit checklist)

**Voice.** Premium LCC tone, not generic-worksheet tone. The shell already carries the
agreed names: "Common SAT traps and how to avoid them" (Trap 1..N tags), "SAT-Style
Practice: Apply Your Strategy", "Quick Check: Can You Apply It?", "Your Key Takeaway".
New prose must match that register. Never use em dashes anywhere, in any file,
including the catalog entry (the catalog checker flags them). Rule leads open with
what-the-form-reveals framing ("Different forms reveal different information.
Recognize what you have been given before doing any algebra"), never "costumes".

**The three-part frame.** Everything teaches: recognize the question type, choose the
most efficient strategy, avoid the predictable mistake. The rules intro ends with that
sentence; each step is rule, strategy, trap, quick check; the practice intro says
"Before you compute, name the question type."

**Honesty about the SAT.** Questions are "SAT-style", written to mirror released
questions, never claimed to match the official test. The practice set "ramps the way a
module tends to". Bluebook framing: "This sheet builds the strategies; Bluebook is
where you meet the real questions." Avoid "always in the choices"; say "usually".

**Originality.** Never copy questions from prep books or pasted sources verbatim. Keep
the structure and skill, change every number, and recompute the answer, solution, trap,
and figure. After building, sweep the output for the source's distinctive numbers and
expressions to confirm none survive. Never reuse the same numbers for two questions in
the sheet (echoes between a rules example and its own step are house style and fine).

**Rule order.** Starred (essential) rules first, unstarred extras last. Order so
dependent ideas are adjacent: the rule a later rule leans on sits directly before it
(in quadratics, the discriminant sits immediately before line-meets-parabola because
tangency reuses it).

**Stars.** Star only the rules behind most SAT questions for the topic. Steps,
practice, and challenge items carry `ess: true` only when they run on a starred rule;
unstarred-rule challenge items show the "extra" chip instead. The stepper's
`LAST_STARRED_STEP_INDEX` drives the "last starred step" hint; update it.

**Difficulty ramps.** Practice set: Easy, then Medium, capped at Medium-hard, ending on
the hardest item, with the `diff` chips saying exactly that. Challenge: picks up at
Medium-hard, finishes Hard. Two or so practice items carry figures, like the real test.

**Cross-domain blends.** Questions that mix in another domain (coordinate-geometry
areas, for instance) never go in the practice set. They live in the challenge tab with
a chip like `"Medium-hard · geometry blend"` and a sentence in the intro saying the
pairing appears less often, so treat it as stretch practice.

**Desmos.** The shell carries the when-to-use-Desmos sentence; retarget its examples to
the topic (what to graph, what to click) and say when straight algebra is faster. Give
`desmos` load arrays only to questions where graphing genuinely helps; structure and
equivalent-expression questions get none.

**Grid-ins.** `accept` lists every form a student might type: canonical fraction first,
then decimals (3-place truncations and roundings, with and without the leading zero).
The grader also matches numerically, but be generous.

**Links.** Deep-dive worksheets (e.g. the algebra factoring worksheet) are linked at
the point of need inside a rule note: "Want deeper reps on these patterns? ...". The
exit card links Bluebook, Khan Academy (name the topic's actual unit names), the Desmos
strategies sheet, and the previous sheet in the series.

## Verification (mandatory, before showing the user)

1. **Math**: verify every answer, every rules example, and every accepted grid-in form
   with sympy. Any plausible arithmetic must be recomputed, not trusted.
2. **Markup**: `<div>`/`<table>`/`<tr>` open and close counts match; zero em dashes;
   zero `\\"` artifacts in the output.
3. **Browser**: run the page in headless Playwright (preinstalled). Switch every tab,
   answer every practice and challenge item with its correct answer and confirm a
   perfect score, exercise one micro check, and screenshot every figure to inspect
   label placement (MathJax/Desmos CDNs are blocked in the sandbox; that is expected).
   Adapt `scripts/` test snippets from the session history or rewrite; they are short.

## Publishing checklist

1. Add a `catalog.js` entry: next `order` in the SAT subject (bump the entries after
   it), `format: "Practice set"`, `difficulty: "Core"`, `builds_on` chain = previous
   sheet in the series plus any deep-dive prerequisite sheet. No em dashes.
2. Run `python3 _build/check_catalog.py` (must report 0 problems) and
   `python3 _build/build_search_index.py`.
3. Cross-link the series: add the forward link to the PREVIOUS sheet's exit card
   ("Ready for the next topic? Continue the series with ... &#8594;"), then rebuild the
   new sheet and confirm the guard stripped it from the copied shell.
4. Commit builder + sheet + catalog + search index to the designated branch and push.
   Merge to `main` only when the user says to publish; the live site updates in about a
   minute.

## Files

- `scripts/build_quadratics.py` - the complete worked example. Copy it for a new topic;
  it also serves as the source of truth for sheet 2 (fix content there and rebuild,
  never hand-edit the generated HTML).
