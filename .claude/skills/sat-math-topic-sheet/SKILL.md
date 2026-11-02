---
name: sat-math-topic-sheet
description: Build or revise a sheet in the Learning Curve Collective SAT Math topic series (the six-tab Learn/Drill/Check format of SAT-Math-1-Linear-Equations, SAT-Math-2-Quadratics and SAT-Math-3-Functions, with a Rules tab, worked-example stepper, fluency drills, SAT-Style Practice set, challenge questions, exit ticket, and the results kit that autosaves answers and downloads a report for the tutor). Use this whenever the user asks for the next SAT math sheet or topic sheet (exponents, percentages, geometry, trig, systems, etc.), says "like the linear sheet" or "like the quadratics one", pastes prep-book pages to turn into a topic sheet, asks to audit, renumber, or restyle an existing sheet in the series, or asks how students send their results from a sheet. Do NOT use for the four-tab interactive worksheet format (that is the sat-math-worksheet skill) or for Reading & Writing content.
---

# SAT Math Topic Sheet Builder

This skill encodes every convention agreed for the Learning Curve Collective SAT Math
topic series, so a new sheet comes out right the first time instead of needing rounds
of auditing. Read this whole file before building; the conventions below are the audit.

## The series so far

| # | File (in `test-prep/sat/`) | Topic | Builder |
|---|---|---|---|
| 0 | `SAT-Desmos-Strategies.html` | Calculator techniques | (hand-built) |
| 1 | `SAT-Math-1-Linear-Equations.html` | Linear equations (this file is the SHELL SOURCE) | (hand-built; results kit injected) |
| 2 | `SAT-Math-2-Quadratics.html` | Quadratics | `scripts/build_quadratics.py` |
| 3 | `SAT-Math-3-Functions.html` | Functions: notation, domain, composition, identities, translations, range | `scripts/build_functions.py` |

Source material so far: Dr. Chung's "DSAT Math 63 Tips" (sheet 2 from the quadratics
tips; sheet 3 from Tips 13, 14, 15, 16 and 43). Torin assigns the book itself as the second
rep, so the sheets use the book's question TYPES with new numbers, never its questions.

Live URLs follow `https://learningcurvecollective.github.io/learning-curve-collective-resources/<path>`.
The site serves from `main`. Torin pushes from GitHub Desktop or `00 Publish.command`; when
a session has no git access (the desktop bridge cannot delete lock files), write the finished
files into the repo folder and tell him what to commit.

## How a sheet is built

Do not hand-write the HTML. Copy `scripts/build_functions.py` (the most complete worked
example; `build_quadratics.py` is the simpler one), rename it for the new topic, and rewrite
only its content blocks. The script reads the linear sheet as the shell (CSS, tabs, graders,
Desmos panel, results kit, the agreed voice) and swaps in content:

- `RULES` - the Rules tab HTML (rule cards, tables, examples, traps section).
- `STEPS` - the worked-example stepper (one dict per step, each with a micro check).
- `FLUENCY`, `GAUNTLET`, `CHALLENGE`, `EXIT` - the drill and practice data.
- `FIGS_JS` - figure specs for the SVG renderer, plus any custom SVG builders (`MINI`).
- A block of `replace_once` calls for topic strings: title, subtitle, tab-1 name,
  intro cards, exit-ticket links, the Desmos-guidance examples, the practice-ramp tail,
  the previous-sheet link, and the localStorage key.

The builder strips the shell's "Ready for the next topic?" forward link so a copied
sheet never links to itself; keep that guard. Every `replace_once` asserts exactly one
match, so a drifted shell fails loudly instead of silently producing a broken page.

String literals in the content dicts are r-strings, so `\"` inside them arrives as
backslash-quote; the `_clean` pass in `js_data` strips it. Keep that pass.

### The figure renderer

The shell's `graphSVG` draws axes, `lines` (y = mx + b), `segs` (dashed), `points`,
`labels`, `poly` (shaded region), `squares` (right-angle marks) and `ticks`. The builders
inject more, and `build_functions.py` carries the full set; copy its `CURVES_JS`,
`GRID_JS` and `FIG_CSS` blocks for any new sheet:

- `curves`: `{a, b, c}` for a parabola, or `{f: function(x) {...}, from, to}` for any
  function; sampled 240 times, split at gaps, clipped to the plot box (asymptotes and
  square roots render correctly).
- `polylines`: `{pts: [[x, y], ...]}` for the zigzag "graph of f" the SAT draws.
- `grid: {step: 1, label: 2}`: light gridlines every step, tick labels every `label`
  units (needed whenever a student must read values off the graph).
- `hlines` / `vlines`: dashed horizontal and vertical lines with labels (y = c crossings,
  asymptotes).
- `thick`: copper highlight bars along an axis (domain and range pictures).
- `MINI`: named custom SVG builders for machine diagrams and small table pictures
  (`miniCurve` makes a 120x64 thumbnail of any function).
- `<div class="fig-row">` puts two `fig-slot`s side by side on the rules tab.

Every figure gets an `alt`. Label placement is checked by screenshot (below); plan on one
or two passes of nudging `dx`/`dy`.

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
expressions (functions, constants, answer values) to confirm none survive; the sweep in
the session that built sheet 3 caught two echoes. Never reuse the same numbers for two
questions in the sheet (echoes between a rules example and its own step are house style
and fine).

**Rule order.** Starred (essential) rules first, unstarred extras last. Order so
dependent ideas are adjacent: the rule a later rule leans on sits directly before it
(in quadratics, the discriminant sits immediately before line-meets-parabola because
tangency reuses it; in functions, range comes right after translations because the
range of a shifted function is read from the shift). A foundation the source skips can
still be Rule 1 (functions opens with notation even though the book starts at domain).

**Stars.** Star only the rules behind most SAT questions for the topic. Steps,
practice, and challenge items carry `ess: true` only when they run on a starred rule;
unstarred-rule challenge items show the "extra" chip instead. The stepper's
`LAST_STARRED_STEP_INDEX` drives the "last starred step" hint; update it and its
wording ("The next two are the extras" / "The last one is the extra").

**Difficulty ramps.** Practice set: Easy, then Medium, capped at Medium-hard, ending on
the hardest item, with the `diff` chips saying exactly that. Challenge: picks up at
Medium-hard, finishes Hard. Two or so practice items carry figures, like the real test.

**Visuals.** Anything best explained by a picture gets one: a function machine for
notation and composition, a graph with the input and output traced, crossings of y = c,
an asymptote, a square root's starting point, the before-and-after of a shift, domain
and range highlighted on the axes, thumbnails in the domain and range tables. Graph-
reading questions (count the crossings, read f(1)) always get a gridded figure.

**Cross-domain blends.** Questions that mix in another domain (coordinate-geometry
areas, for instance) never go in the practice set. They live in the challenge tab with
a chip like `"Medium-hard · geometry blend"` and a sentence in the intro saying the
pairing appears less often, so treat it as stretch practice.

**Desmos.** The shell carries the when-to-use-Desmos sentence; retarget its examples to
the topic (what to graph, what to click) and say when straight algebra is faster. Give
`desmos` load arrays only to questions where graphing genuinely helps; structure and
equivalent-expression questions get none. Desmos accepts function notation, so loads
like `["f(x)=x^2-3", "g(x)=f(x-3)+2"]` work and are worth teaching.

**Grid-ins.** `accept` lists every form a student might type: canonical fraction first,
then decimals (3-place truncations and roundings, with and without the leading zero).
The grader also matches numerically, but be generous. A question with two valid answers
("one possible value of c") lists both.

**Links.** Deep-dive worksheets (e.g. the algebra factoring worksheet) are linked at
the point of need inside a rule note: "Want deeper reps on these patterns? ...". The
exit card links Bluebook, Khan Academy (name the topic's actual unit names), the Desmos
strategies sheet, and the previous sheet(s) in the series.

## The results kit (autosave + "Results for your tutor")

Students asked whether the sheets "save" (Cici, 2026-10-30: "I don't think it saved on my
end, did it save on yours?"). The answer is `scripts/results_kit.py`, which lives in the
shell, so every sheet in the series has it:

- **Autosave.** Every graded answer (quick checks, fluency drills, practice set with its
  timer, challenge questions and extras, exit ticket, takeaway sentence) is saved to
  `localStorage` under `<sheet-key>:progress` and restored on the next visit, with a
  "Welcome back" banner and a Start fresh button. Nothing leaves the browser.
- **Results for your tutor.** A button in the Check row of the tab bar, a card under the
  practice-set score, and a card on the exit ticket all open the same panel: the student
  types their name, then **Download results** (a self-contained HTML report: tiles per
  section, a review list of every miss with the question and its trap, full tables, the
  takeaway, and the raw data embedded as JSON in `<script id="lcc-results">` for a future
  hub import), **Copy summary** (a text-message-sized summary), or **Email summary**
  (`mailto:`; set `RK_TUTOR_EMAIL` in `results_kit.py` to pre-address it, left blank on
  the public sheets). The report renders its LaTeX through the MathJax CDN when opened.

Mechanics: the kit wraps the shell's `checkExp`, `checkMC`, `microExp`, `microMC`,
`renderStep`, `renderFluency`, `renderExit` and `renderGauntletResults` (JS function
bindings are reassigned, so the inline `onclick` handlers pick up the wrappers), records
each check, and replays the records after each render. State for the practice set and
challenge tab is the shell's own (`gState`, `chState`, `cxState`). The storage key is
derived at runtime from the literal `'sat-linear-sheet:rule'`, which every builder already
retargets (`html.replace('sat-linear-sheet:rule', 'sat-<topic>-sheet:rule')`), so a built
sheet gets its own key for free.

Every injected block sits between `rk:begin` / `rk:end` markers. `python3 results_kit.py
<sheet.html>` patches a sheet; re-running refreshes the blocks in place (byte-identical
when nothing changed) and `results_kit.strip(html)` restores the original exactly. To
change the kit: edit `results_kit.py`, re-run it on the linear sheet, rebuild sheets 2
and 3 from the builders (they copy the shell), and run the browser checks below on all
three. The private-hub sheets use a different, older panel (`claude/results-panel.md`
in the project: `_build/add_results.py`, a `.txt` report, recipients from `portal.json`);
this kit is the public-sheet equivalent and does not depend on a hub.

## Verification (mandatory, before showing the user)

1. **Math**: verify every answer, every rules example, and every accepted grid-in form
   with sympy. Any plausible arithmetic must be recomputed, not trusted.
2. **Markup**: `<div>`/`<table>`/`<tr>` open and close counts match (count `<\/tag>` as
   well as `</tag>`, since the JSON data escapes closing tags); zero em dashes; `\"`
   appears only inside `<script>` (that is JSON quoting, expected).
3. **Browser**: run the page in headless Playwright (preinstalled). Switch every tab,
   answer every practice and challenge item with its correct answer and confirm a
   perfect score, exercise one micro check, and screenshot every figure to inspect
   label placement. The MathJax and Desmos CDNs are blocked in the sandbox: for realistic
   screenshots, `npm install mathjax@3` once and test a copy of the sheet whose MathJax
   `src` points at `node_modules/mathjax/es5/tex-svg.js`. Also check a 390px viewport.
4. **Results kit**: on the built sheet, answer a mix of right and wrong items across the
   tabs, finish the practice set, download the report (Playwright `acceptDownloads`),
   reload and confirm the banner and every restored answer, then Start fresh. Render the
   downloaded report and check the review list and the embedded JSON. Run the same on
   sheets 1 and 2 whenever the kit or the shell changes.
   The session that built sheet 3 kept these as `test_sheet.js` and `test_kit.js`; they
   are short and easy to rewrite from this description.

## Publishing checklist

1. Add a `catalog.js` entry: next `order` in the SAT subject (bump the entries after
   it), `format: "Practice set"`, `difficulty: "Core"`, `builds_on` chain = previous
   sheet in the series plus any deep-dive prerequisite sheet. No em dashes.
2. Run `python3 _build/check_catalog.py` (must report 0 problems),
   `python3 _build/build_search_index.py`, and `python3 _build/build_pages.py` (the
   subject pages render from the catalog).
3. Cross-link the series: add the forward link to the PREVIOUS sheet's exit card, in its
   builder if it is a built sheet ("Ready for the next topic? Continue the series with
   ... &#8594;", after the Desmos Strategies paragraph), then rebuild the new sheet and
   confirm the guard stripped it from the copied shell.
4. Commit builder + kit + sheets + catalog + search index + pages, or hand the files to
   Torin to commit; the live site updates about a minute after the push to `main`.

## Files

- `scripts/build_functions.py` - the complete worked example with the full figure
  renderer. Copy it for a new topic; it is the source of truth for sheet 3 (fix content
  there and rebuild, never hand-edit the generated HTML).
- `scripts/build_quadratics.py` - the same for sheet 2 (carries the forward link to 3).
- `scripts/results_kit.py` - the autosave + tutor-report kit; patches the shell.
