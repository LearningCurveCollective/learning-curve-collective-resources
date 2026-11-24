#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-4-Triangles.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the
content swaps. All questions use original numbers, wording and figures (the DSAT Tips 37 to 42
pages were the source of the question TYPES only).

This sheet adds one thing to the shell: geoSVG, a figure renderer for plain geometry (no axes,
equal scale). A FIGS entry with a `box` key is drawn by geoSVG; the figure specs are written as
Python dicts below so the coordinates can be computed, then dumped to JS.
Answer key: verify_triangles.py (same folder) recomputes every answer."""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.exists(os.path.join(ROOT, 'catalog.js')):
    parent = os.path.dirname(ROOT)
    assert parent != ROOT, 'repo root with catalog.js not found above this script'
    ROOT = parent
sys.path.insert(0, HERE)
try:
    import desmos_voice as voice                      # the LCC voice table for shell and results-kit copy
except ImportError:                                   # e.g. when this file sits in the skill folder without it
    sys.path.insert(0, os.path.join(ROOT, '_build', 'skill-update-sat-math-topic-sheet', 'scripts'))
    import desmos_voice as voice

SRC = ROOT + '/test-prep/sat/SAT-Math-1-Linear-Equations.html'
OUT = ROOT + '/test-prep/sat/SAT-Math-4-Triangles.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
LINEAR_URL = SITE + 'test-prep/sat/SAT-Math-1-Linear-Equations.html'
QUAD_URL = SITE + 'test-prep/sat/SAT-Math-2-Quadratics.html'
FUNC_URL = SITE + 'test-prep/sat/SAT-Math-3-Functions.html'
DESMOS1_URL = SITE + 'test-prep/sat/SAT-Desmos-1-Core-Moves.html'
SRT_URL = SITE + 'test-prep/sat/SAT-Math-4B-Special-Right-Triangles.html'
RATIOS_URL = SITE + 'test-prep/sat/SAT-Math-5-Ratios-Rates-Proportions.html'
SIM_URL = SITE + 'test-prep/sat/SAT-Math-4C-Similar-Figures.html'
A_STYLE = 'target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;"'

# ---------------------------------------------------------------- text helpers
MATH_RE = re.compile(r'\$\$.*?\$\$|\$(?:\\.|[^$\\])+?\$', re.S)


def nw(s):
    """Keep inline math glued to the punctuation that follows it (house style)."""
    out, pos = [], 0
    for m in MATH_RE.finditer(s):
        out.append(s[pos:m.start()])
        seg, end = m.group(0), m.end()
        if not seg.startswith('$$'):
            pm = re.match(r'[.,:;?!]+(?=\s|<|$)', s[end:])
            if pm:
                out.append('<span class="nw">' + seg + pm.group(0) + '</span>')
                pos = end + pm.end()
                continue
        out.append(seg)
        pos = end
    out.append(s[pos:])
    return ''.join(out)


def nw_all(o):
    if isinstance(o, str):
        return nw(o)
    if isinstance(o, list):
        return [nw_all(v) for v in o]
    if isinstance(o, dict):
        return {k: (v if k in ('desmos', 'accept', 'fig', 'type', 'diff', 'sec') else nw_all(v)) for k, v in o.items()}
    return o


STAR = '<span class="star">&#9733;</span>'


def rule(n, name, ess, body):
    tag = (STAR if ess else '') + 'Rule ' + str(n)
    return ('<div class="ref-rule' + (' ess' if ess else '') + '"><div class="ref-rule-line"><span class="rtag">' + tag +
            '</span><span class="rname">' + name + '</span></div>\n' + body.strip('\n') + '\n</div>\n')


def frow(label, math_):
    return '<div class="frow"><div class="flabel">' + label + '</div><div class="fmath">' + math_ + '</div></div>\n'


def ex(letter, text):
    return '<div class="ref-ex"><span class="exlab">Example ' + letter + '</span>' + text + '</div>\n'


def note(text):
    return '<div class="ref-note">' + text + '</div>\n'


def mistake(n, name, text):
    return ('<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Common mistake ' + str(n) + '</span><span class="rname">' +
            name + '</span></div><div class="ref-ex">' + text + '</div></div>\n')


def figslot(name):
    return '<div class="fig-slot" data-fig="' + name + '"></div>\n'


# ---------------------------------------------------------------- TAB 1: RULES
RULES = r'''
<p class="ref-intro">Triangle questions on the SAT draw on a short list of facts: the angles that parallel lines make, the angles inside a triangle, the Pythagorean theorem, and the two special right triangles. Three less common ideas complete the list: which side lengths can form a triangle, how areas compare when triangles share a height, and what the altitude to the hypotenuse does. Most of these questions come with a figure, so mark what you know on the figure before you compute. As you practice, start by identifying the question type. Then decide which rule fits the figure, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''' + rule(1, 'Parallel lines and a transversal', True, r'''
<p class="ref-lead">When a line crosses two parallel lines at a slant, it forms eight angles but only two different measures. All the acute angles are equal, all the obtuse angles are equal, and one of each adds to $180^\circ$. Decide which kind of pair you have before you write an equation.</p>
''' + figslot('r_par') + r'''<div class="tbl-wrap"><table class="cases"><thead><tr><th>Pair</th><th>Where to find it</th><th>Relationship</th></tr></thead><tbody>
<tr><td class="fname">Vertical angles</td><td>across from each other at one crossing</td><td>equal</td></tr>
<tr><td class="fname">Corresponding angles</td><td>the same corner at each crossing</td><td>equal</td></tr>
<tr><td class="fname">Alternate interior angles</td><td>between the parallel lines, on opposite sides of the transversal</td><td>equal</td></tr>
<tr><td class="fname">Same-side interior angles</td><td>between the parallel lines, on the same side of the transversal</td><td>add to $180^\circ$</td></tr>
<tr><td class="fname">Linear pair</td><td>next to each other on a straight line</td><td>add to $180^\circ$</td></tr>
</tbody></table></div>
''' + ex('A', r'One of the eight angles measures $112^\circ$. Three others also measure $112^\circ$, and the remaining four measure $180^\circ - 112^\circ = 68^\circ$.') +
    ex('B', r'Same-side interior angles $(3x + 10)^\circ$ and $(2x + 20)^\circ$ add to $180^\circ$: $5x + 30 = 180$, so $x = 30$ and the angles are $100^\circ$ and $80^\circ$.') +
    ex('C', r'Alternate interior angles $(5x - 8)^\circ$ and $(3x + 26)^\circ$ are equal: $2x = 34$, so $x = 17$ and each angle is $77^\circ$.') +
    note(r'These relationships need parallel lines. Look for a statement such as $\ell \parallel m$ before you use them. After solving, put $x$ back in and confirm that the angle measures make sense.')) + \
rule(2, 'Angles in a triangle', True, r'''
<p class="ref-lead">The three interior angles of a triangle add to $180^\circ$. Two facts follow from that and come up often: an exterior angle equals the sum of the two interior angles that do not touch it, and equal sides are across from equal angles.</p>
''' + figslot('r_tri') + r'''<div class="fbox">
''' + frow('angle sum', r'$a + b + c = 180$') +
      frow('exterior angle', r'$d = a + b$ &nbsp; (the two interior angles that do not touch it)') +
      frow('isosceles', r'two equal sides, so the two angles across from them are equal') +
      frow('equilateral', r'three equal sides and three $60^\circ$ angles') +
      frow('right triangle', r'the two acute angles add to $90^\circ$') + r'''</div>
''' + ex('A', r'Two angles measure $47^\circ$ and $68^\circ$. The third is $180^\circ - 115^\circ = 65^\circ$, and the exterior angle at that vertex is $47^\circ + 68^\circ = 115^\circ$.') +
    ex('B', r'An isosceles triangle with a $40^\circ$ angle between its equal sides has two more angles of $\dfrac{180^\circ - 40^\circ}{2} = 70^\circ$. If the $40^\circ$ angle is one of the two equal angles instead, the angles are $40^\circ$, $40^\circ$ and $100^\circ$.') +
    ex('C', r'With parallel lines: in the figure below, $\ell \parallel m$. Draw a line through the bend that is parallel to both. Alternate interior angles carry the $35^\circ$ and the $50^\circ$ to the bend, so the angle there measures $35^\circ + 50^\circ = 85^\circ$.') +
    figslot('r_zig') +
    note(r'When a triangle or a bend sits between parallel lines, use Rule 1 to move an angle to where you need it. Then finish with the angle sum or the exterior angle.')) + \
rule(3, 'The Pythagorean theorem', True, r'''
<p class="ref-lead">In a right triangle, the squares of the two legs add up to the square of the hypotenuse, the side across from the right angle. Use it when you know two sides of a right triangle and need the third.</p>
''' + figslot('r_pyth') + r'''<div class="fbox">
''' + frow('the theorem', r'$a^2 + b^2 = c^2$ &nbsp; ($c$ is the hypotenuse)') +
      frow('a missing leg', r'$a^2 = c^2 - b^2$ &nbsp; (subtract when the missing side is a leg)') +
      frow('common triples', r'$3$-$4$-$5$, &nbsp; $5$-$12$-$13$, &nbsp; $8$-$15$-$17$, &nbsp; $7$-$24$-$25$') +
      frow('multiples work too', r'$6$-$8$-$10$, &nbsp; $9$-$12$-$15$, &nbsp; $10$-$24$-$26$') +
      frow('as areas', r'the squares built on the legs have areas $a^2$ and $b^2$; together they equal the area of the square built on the hypotenuse') + r'''</div>
''' + ex('A', r'Legs $9$ and $12$: $81 + 144 = 225$, so the hypotenuse is $15$. This is $3$-$4$-$5$ with each side tripled.') +
    ex('B', r'Hypotenuse $26$ and one leg $10$: $676 - 100 = 576$, so the other leg is $24$.') +
    ex('C', r'Legs $4$ and $6$: $16 + 36 = 52$, so the hypotenuse is $\sqrt{52} = 2\sqrt{13}$. Answer choices usually show the simplified radical.') +
    ex('D', r'Squares built on the legs have areas $15$ and $34$. The square on the hypotenuse has area $49$, so the hypotenuse is $7$. The leg lengths are not needed. The same addition works for any three similar shapes built on the sides, such as semicircles or equilateral triangles.') +
    note(r'Recognizing a triple can save the arithmetic. When the numbers are not a triple, Desmos can do the arithmetic: $\sqrt{4^2 + 6^2}$ is about $7.21$, which you can compare with the decimal value of each choice.')) + \
rule(4, 'Special right triangles', True, r'''
<p class="ref-lead">Two right triangles have fixed side ratios, so one side gives you the other two. A $45$-$45$-$90$ triangle is half of a square, cut along the diagonal. A $30$-$60$-$90$ triangle is half of an equilateral triangle, cut along the height.</p>
<div class="fig-row">''' + figslot('r_45').strip('\n') + figslot('r_30').strip('\n') + r'''</div>
<div class="tbl-wrap"><table class="forms"><thead><tr><th>Triangle</th><th>Sides</th><th>How to use it</th><th>Example</th></tr></thead><tbody>
<tr><td class="fname">$45$-$45$-$90$</td><td class="fmath">$x : x : x\sqrt{2}$</td><td class="freads">the legs are equal; multiply a leg by $\sqrt{2}$ for the hypotenuse; divide the hypotenuse by $\sqrt{2}$ for a leg</td><td class="fex">legs $5$: hypotenuse $5\sqrt{2}$</td></tr>
<tr><td class="fname">$30$-$60$-$90$</td><td class="fmath">$x : x\sqrt{3} : 2x$</td><td class="freads">the short leg $x$ is across from the $30^\circ$ angle; the hypotenuse is twice the short leg; the long leg is the short leg times $\sqrt{3}$</td><td class="fex">short leg $4$: long leg $4\sqrt{3}$, hypotenuse $8$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('start with $x$', r'find the short leg (or a leg of the $45$-$45$-$90$) first, then build the other sides from it') +
      frow('equilateral, side $s$', r'height $\dfrac{s\sqrt{3}}{2}$, &nbsp; area $\dfrac{s^2\sqrt{3}}{4}$') +
      frow('square, side $s$', r'diagonal $s\sqrt{2}$') +
      frow('dividing by a root', r'$\dfrac{12}{\sqrt{3}} = 4\sqrt{3}$ &nbsp; and &nbsp; $\dfrac{14}{\sqrt{2}} = 7\sqrt{2}$') + r'''</div>
''' + ex('A', r'A $45$-$45$-$90$ triangle with hypotenuse $14$: each leg is $\dfrac{14}{\sqrt{2}} = 7\sqrt{2}$.') +
    ex('B', r'A $30$-$60$-$90$ triangle with hypotenuse $18$: the short leg is $9$ and the long leg is $9\sqrt{3}$.') +
    ex('C', r'A $30$-$60$-$90$ triangle with long leg $12$: the short leg is $\dfrac{12}{\sqrt{3}} = 4\sqrt{3}$ and the hypotenuse is $8\sqrt{3}$.') +
    ex('D', r'An equilateral triangle with side $10$: the height is $5\sqrt{3}$ and the area is $\tfrac{1}{2}(10)(5\sqrt{3}) = 25\sqrt{3}$.') +
    note(r'A question may not name the triangle for you. Look for $30^\circ$, $45^\circ$ or $60^\circ$ angles, squares, and equilateral triangles. The Bluebook Tools tab of <a href="' + DESMOS1_URL + r'" target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;">SAT Desmos 1: Core Moves</a> has a copy of the reference sheet, which lists both of these triangles and the Pythagorean theorem. Want more practice with these two triangles? <a href="' + SRT_URL + r'" target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;">SAT Math 4B: Special Right Triangles</a> covers both patterns in depth, with quick reps and the figures where they appear.')) + \
rule(5, 'The triangle inequality', False, r'''
<p class="ref-lead">Three lengths form a triangle only when the two shorter ones add up to more than the longest. With two sides known, that limits the third side to a range. Inside a triangle, the longest side is across from the largest angle.</p>
''' + figslot('r_ineq') + r'''<div class="fbox">
''' + frow('the third side', r'$|a - b| < c < a + b$ &nbsp; (more than the difference, less than the sum)') +
      frow('quick test', r'add the two shortest lengths; the total has to be greater than the longest') +
      frow('equal is not enough', r'$4$, $5$, $9$ does not form a triangle: $4 + 5 = 9$, so the sides lie flat') +
      frow('side and angle order', r'longest side across from the largest angle; shortest side across from the smallest angle') + r'''</div>
''' + ex('A', r'Sides $5$ and $8$: the third side is between $3$ and $13$. If it is an integer, it can be $4$ through $12$, which is nine values.') +
    ex('B', r'$7$, $10$, $18$ is not a triangle, because $7 + 10 = 17$ is less than $18$. $7$, $10$, $16$ is a triangle, because $17$ is greater than $16$.') +
    ex('C', r'A triangle has angles of $50^\circ$, $60^\circ$ and $70^\circ$. The side across from the $70^\circ$ angle is the longest, and the side across from the $50^\circ$ angle is the shortest.') +
    note(r'When a side is written with a variable, such as $2x - 1$, write the range for the whole side first. Then solve for $x$.')) + \
rule(6, 'Triangles that share a height', False, r'''
<p class="ref-lead">The area of a triangle is $\tfrac{1}{2} \cdot \text{base} \cdot \text{height}$. When two triangles have the same height, the $\tfrac{1}{2}$ and the height are the same in both, so their areas compare the way their bases do.</p>
''' + figslot('r_share') + r'''<div class="fbox">
''' + frow('same height', r'$\dfrac{\text{area}_1}{\text{area}_2} = \dfrac{\text{base}_1}{\text{base}_2}$') +
      frow('where to look', r'triangles that share a vertex and have their bases on the same line') +
      frow('a median', r'equal bases, so the two triangles have equal areas') +
      frow('part of the whole', r'bases in the ratio $2 : 5$ give areas that are $\tfrac{2}{7}$ and $\tfrac{5}{7}$ of the whole triangle') + r'''</div>
''' + ex('A', r'In the figure, $QS = 4$ and $SR = 10$. If the area of triangle $PQS$ is $18$, each unit of base carries $18 \div 4 = 4.5$ units of area. The area of triangle $PSR$ is $45$, and the area of triangle $PQR$ is $63$.') +
    ex('B', r'A point on the diagonal of a rectangle: if $T$ divides diagonal $\overline{WY}$ of rectangle $WXYZ$ so that $WT : TY = 1 : 3$, then triangles $WXT$ and $TXY$ share the height from $X$, and their areas are in the ratio $1 : 3$.') +
    ex('C', r'The diagonal of a rectangle splits it into two triangles of equal area. Once you know the area of one of them, the rectangle is twice that.') +
    note(r'The ratio works because of the shared height. Before you use it, confirm that the two triangles have the same vertex across from bases on one line.')) + \
rule(7, 'The altitude to the hypotenuse', False, r'''
<p class="ref-lead">Draw the altitude from the right angle to the hypotenuse, and a right triangle splits into two smaller right triangles. Each one shares an angle with the original, so all three triangles are similar and their sides are proportional. Three relationships follow.</p>
''' + figslot('r_alt') + r'''<div class="fbox">
''' + frow('the altitude', r'$h^2 = p \cdot q$') +
      frow('each leg', r'$a^2 = p\,(p + q)$ &nbsp; and &nbsp; $b^2 = q\,(p + q)$ &nbsp; (the piece beside the leg, times the whole hypotenuse)') +
      frow('area two ways', r'$\tfrac{1}{2}ab = \tfrac{1}{2}(p + q)\,h$, &nbsp; so &nbsp; $h = \dfrac{ab}{p + q}$') + r'''</div>
''' + ex('A', r'The altitude splits the hypotenuse into pieces of $4$ and $9$: $h^2 = 36$, so $h = 6$.') +
    ex('B', r'Pieces of $2$ and $6$: the leg beside the $2$ has $a^2 = 2 \cdot 8 = 16$, so $a = 4$. The other leg has $b^2 = 6 \cdot 8 = 48$, so $b = 4\sqrt{3}$.') +
    ex('C', r'Legs $14$ and $48$: the hypotenuse is $50$, and the altitude to it is $\dfrac{14 \cdot 48}{50} = 13.44$.') +
    note(r'If you forget one of these, the Pythagorean theorem still works in each of the three right triangles. These relationships are a shorter path to the same result. Similar triangles have their own sheet, which covers the scale factor and how lengths and areas grow: <a href="' + SIM_URL + r'" ' + A_STYLE + r'>SAT Math 4C: Similar Figures &#8594;</a>')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common setup and interpretation mistakes. Review them so you know what to check when an answer seems off.</p>
''' + mistake(1, 'using a parallel-line pair when the lines are not parallel', r'Corresponding and alternate interior angles are equal only when the two lines are parallel. Look for $\ell \parallel m$ in the question before you set two angles equal.') + \
      mistake(2, 'setting same-side interior angles equal', r'They add to $180^\circ$. If one is $70^\circ$, the other is $110^\circ$. After solving, put $x$ back in: a negative angle measure means the setup needs another look.') + \
      mistake(3, 'adding in the angle beside an exterior angle', r'The exterior angle equals the two interior angles that do not touch it. The interior angle beside it is its supplement, and it is not part of that sum.') + \
      mistake(4, 'adding the squares when the missing side is a leg', r'Hypotenuse $13$ and leg $5$: the other leg is $\sqrt{169 - 25} = 12$, not $\sqrt{194}$. The hypotenuse is the longest side, so a leg that comes out longer than the hypotenuse signals a slip.') + \
      mistake(5, r'putting $x\sqrt{3}$ on the hypotenuse', r'In a $30$-$60$-$90$ triangle the hypotenuse is $2x$ and the long leg is $x\sqrt{3}$. Since $\sqrt{3}$ is about $1.73$, the hypotenuse is still the longest side.') + \
      mistake(6, r'calling the given side $x$ without checking', r'The given side might be the long leg or the hypotenuse. Mark which angle each side is across from, then decide whether the given length is $x$, $x\sqrt{3}$ or $2x$.') + \
      mistake(7, 'including the endpoints in the triangle inequality', r'With sides $5$ and $8$, the third side cannot be $3$ or $13$. At those lengths the three sides lie flat on one line.') + \
      mistake(8, 'stopping at a piece when the question asks for the whole', r'After a ratio gives you one triangle&rsquo;s area, reread the question. It may ask for the other piece, the whole triangle, or a rectangle that is twice the triangle.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Parallel lines and a transversal",
  "rule": r"equal: corresponding, alternate interior, vertical &nbsp;·&nbsp; add to $180^\circ$: same-side interior, linear pair",
  "say": r"A slanted transversal makes only two angle measures with a pair of parallel lines. First decide whether the two angles in the question have the same measure (set them equal) or different measures (add them to $180$). Then solve for $x$ and check the angles.",
  "fig": "s1",
  "prob": r"In the figure above, lines $\ell$ and $m$ are parallel. What is the value of $x$?",
  "sol": r"<strong>Step 1: name the pair.</strong> The angle vertical to the $(3x + 15)^\circ$ angle is between the parallel lines, on the same side of the transversal as the $(2x + 5)^\circ$ angle. Those two are same-side interior angles, so they add to $180^\circ$.<br><strong>Step 2: write the equation.</strong> $(3x + 15) + (2x + 5) = 180$, so $5x + 20 = 180$ and $x = 32$.<br><strong>Step 3: check the angles.</strong> $3(32) + 15 = 111$ and $2(32) + 5 = 69$, and $111 + 69 = 180$. ✓",
  "trap": r"Setting the two expressions equal. $3x + 15 = 2x + 5$ gives $x = -10$, which would make one angle measure $-15^\circ$. A negative angle is a signal to go back and name the pair again.",
  "micro": {"q": r"Lines $\ell$ and $m$ are parallel. Two alternate interior angles measure $(5x - 8)^\circ$ and $(3x + 26)^\circ$. Then $x =$", "accept": ["17"],
            "exp": r"Alternate interior angles are equal: $5x - 8 = 3x + 26$, so $2x = 34$ and $x = 17$. Each angle measures $77^\circ$."}},
 {"ess": True, "name": "Rule 2: Angles in a triangle",
  "rule": r"$a + b + c = 180$ &nbsp;·&nbsp; exterior angle $=$ the two interior angles that do not touch it",
  "say": r"An exterior angle and the interior angle beside it make a straight line. So the exterior angle equals the other two interior angles combined, and you can often skip finding the third angle.",
  "fig": "s2",
  "prob": r"In the figure above, point $C$ lies on $\overline{BD}$. What is the value of $x$? What is the measure of angle $ACB$?",
  "sol": r"<strong>Step 1: use the exterior angle.</strong> The $128^\circ$ angle is outside the triangle at $C$. The two interior angles that do not touch it are at $A$ and $B$: $3x + (2x + 8) = 128$, so $5x = 120$ and $x = 24$.<br><strong>Step 2: the two angles.</strong> Angle $A$ measures $72^\circ$ and angle $B$ measures $56^\circ$.<br><strong>Step 3: the angle at $C$.</strong> Angle $ACB$ and the $128^\circ$ angle form a straight line: $180 - 128 = 52$. Check: $72 + 56 + 52 = 180$. ✓",
  "trap": r"Including angle $ACB$ in the sum. The interior angle beside the exterior angle is its supplement, $52^\circ$ here. It is not one of the two angles that add to $128^\circ$.",
  "micro": {"q": r"Two angles of a triangle measure $47^\circ$ and $68^\circ$. The measure, in degrees, of the exterior angle at the third vertex is", "accept": ["115", "115°"],
            "exp": r"$47 + 68 = 115$. The third interior angle is $65^\circ$, and $180 - 65 = 115$ agrees."}},
 {"ess": True, "name": "Rule 2, continued: A triangle between parallel lines",
  "rule": r"use Rule 1 to move an angle into the triangle &nbsp;·&nbsp; then use the angle sum or the exterior angle",
  "say": r"When two segments cross between parallel lines, each one is a transversal. Alternate interior angles let you carry an angle from one parallel line to the other, so that two angles of the same triangle are known. Rule 2 finishes the question.",
  "fig": "s3",
  "prob": r"In the figure above, $\ell \parallel m$, and $\overline{PS}$ and $\overline{QR}$ intersect at $T$. What is the value of $k$?",
  "sol": r"<strong>Step 1: move an angle.</strong> $\overline{QR}$ is a transversal, so angle $TQP$ and the $57^\circ$ angle at $R$ are alternate interior angles. Angle $TQP$ measures $57^\circ$.<br><strong>Step 2: use the triangle.</strong> Triangle $PQT$ now has angles of $38^\circ$ at $P$ and $57^\circ$ at $Q$. The $k^\circ$ angle is an exterior angle of that triangle at $T$, so $k = 38 + 57 = 95$.<br><strong>Check:</strong> the angle inside the triangle at $T$ is $180 - 95 = 85$, and $38 + 57 + 85 = 180$. ✓",
  "trap": r"Answering $85$, the angle inside triangle $PQT$. Two different angles meet at $T$: the one inside the triangle, $85^\circ$, and the one beside it, $95^\circ$. Check which one the figure marks.",
  "micro": {"q": r"In an isosceles triangle, the angle between the two equal sides measures $40^\circ$. The measure, in degrees, of each of the other two angles is", "accept": ["70", "70°"],
            "exp": r"The other two angles are equal and share what is left: $\dfrac{180 - 40}{2} = 70$."}},
 {"ess": True, "name": "Rule 3: The Pythagorean theorem",
  "rule": r"$a^2 + b^2 = c^2$ &nbsp;·&nbsp; a square built on a side has an area equal to that side squared",
  "say": r"Find the hypotenuse first: it is across from the right angle. If the hypotenuse is the missing side, add the squares of the legs. If a leg is missing, subtract. When a question gives the areas of squares built on the sides, those areas are $a^2$, $b^2$ and $c^2$ already.",
  "fig": "s4",
  "prob": r"In the figure above, squares are drawn on leg $\overline{PQ}$ and on hypotenuse $\overline{PR}$ of right triangle $PQR$. The areas of the squares are $25$ and $74$. What is the length of $\overline{QR}$?",
  "sol": r"<strong>Step 1: read the areas as squares of sides.</strong> $PQ^2 = 25$ and $PR^2 = 74$.<br><strong>Step 2: place them in the theorem.</strong> $\overline{PR}$ is the hypotenuse, so $PQ^2 + QR^2 = PR^2$. That gives $25 + QR^2 = 74$, and $QR^2 = 49$.<br><strong>Step 3: take the root.</strong> $QR = 7$. The length $PR = \sqrt{74}$ was not needed.",
  "trap": r"Adding the two areas to get $99$. Add when both known sides are legs. Here one of them is the hypotenuse, so the missing leg comes from subtracting.",
  "micro": {"q": r"A right triangle has a hypotenuse of length $26$ and one leg of length $10$. The length of the other leg is", "accept": ["24"],
            "exp": r"$26^2 - 10^2 = 676 - 100 = 576$, and $\sqrt{576} = 24$. This is the $5$-$12$-$13$ triangle with each side doubled."}},
 {"ess": True, "name": "Rule 4: The 30-60-90 triangle",
  "rule": r"$x : x\sqrt{3} : 2x$ &nbsp;·&nbsp; the short leg $x$ is across from the $30^\circ$ angle",
  "say": r"Find the short leg first, because the other two sides are built from it. The short leg is across from the $30^\circ$ angle, the hypotenuse is twice the short leg, and the long leg is the short leg times $\sqrt{3}$.",
  "fig": "s5",
  "prob": r"In the figure above, triangle $ABC$ has a right angle at $C$, the measure of angle $A$ is $30^\circ$, and $AC = 12$. What is the length of $\overline{AB}$? What is the area of the triangle?",
  "sol": r"<strong>Step 1: match each side to its angle.</strong> $\overline{BC}$ is across from the $30^\circ$ angle, so it is the short leg, $x$. $\overline{AC}$ is across from the $60^\circ$ angle at $B$, so it is the long leg: $x\sqrt{3} = 12$.<br><strong>Step 2: find $x$.</strong> $x = \dfrac{12}{\sqrt{3}} = 4\sqrt{3}$.<br><strong>Step 3: build the rest.</strong> $AB = 2x = 8\sqrt{3}$. The area is $\tfrac{1}{2}(12)(4\sqrt{3}) = 24\sqrt{3}$.<br><strong>Check:</strong> $12^2 + (4\sqrt{3})^2 = 144 + 48 = 192 = (8\sqrt{3})^2$. ✓",
  "trap": r"Treating $12$ as the short leg and writing $AB = 24$. The leg that touches the $30^\circ$ angle is the long leg. Mark which angle each side is across from before you decide where $x$ goes.",
  "micro": {"q": r"In a $30$-$60$-$90$ triangle, the hypotenuse has length $18$. The length of the shorter leg is", "accept": ["9"],
            "exp": r"The hypotenuse is twice the short leg: $2x = 18$, so $x = 9$. The long leg is $9\sqrt{3}$."}},
 {"ess": True, "name": "Rule 4, continued: Squares and equilateral triangles",
  "rule": r"square: diagonal $= s\sqrt{2}$ &nbsp;·&nbsp; equilateral: height $= \dfrac{s\sqrt{3}}{2}$, area $= \dfrac{s^2\sqrt{3}}{4}$",
  "say": r"The diagonal of a square cuts it into two $45$-$45$-$90$ triangles. The height of an equilateral triangle cuts it into two $30$-$60$-$90$ triangles. When a figure contains a square or an equilateral triangle, picture that segment and the special triangle appears.",
  "fig": "s6",
  "prob": r"The figure above shows square $PQRS$ and equilateral triangle $QTR$, which share side $\overline{QR}$. The area of triangle $QTR$ is $25\sqrt{3}$. What is the length of diagonal $\overline{PR}$ of the square?",
  "sol": r"<strong>Step 1: find the side from the area.</strong> $\dfrac{s^2\sqrt{3}}{4} = 25\sqrt{3}$, so $s^2 = 100$ and $s = 10$.<br><strong>Step 2: carry it to the square.</strong> $\overline{QR}$ is also a side of the square, so the square has side $10$.<br><strong>Step 3: the diagonal.</strong> $\overline{PR}$ is the hypotenuse of a $45$-$45$-$90$ triangle with legs of $10$, so $PR = 10\sqrt{2}$.<br><strong>Where the area formula comes from:</strong> the height of the equilateral triangle is the long leg of a $30$-$60$-$90$ triangle with short leg $\tfrac{s}{2}$. The height is $\tfrac{s}{2}\sqrt{3}$, and the area is $\tfrac{1}{2} \cdot s \cdot \tfrac{s\sqrt{3}}{2}$.",
  "trap": r"Using $\tfrac{1}{2}s^2$ for the area of the equilateral triangle. Its height is $\dfrac{s\sqrt{3}}{2}$, which is shorter than the side $s$ because the sides slant.",
  "micro": {"q": r"A square has a diagonal of length $14$. The area of the square is", "accept": ["98"],
            "exp": r"The side is $\dfrac{14}{\sqrt{2}} = 7\sqrt{2}$, and $(7\sqrt{2})^2 = 98$. A shorter path: the area of a square is half the square of its diagonal, $\tfrac{1}{2}(14)^2$."}},
 {"ess": False, "name": "Rule 5: The triangle inequality",
  "rule": r"$|a - b| < c < a + b$ &nbsp;·&nbsp; the longest side is across from the largest angle",
  "say": r"Each side of a triangle is shorter than the other two combined. So when two sides are known, the third is between their difference and their sum. If a side is written with a variable, write the range for the whole side first, then solve for the variable.",
  "prob": r"The lengths of the sides of a triangle are $5$, $11$, and $2x - 1$. What is the greatest integer value of $x$? What is the least?",
  "sol": r"<strong>Step 1: the range for the whole side.</strong> $11 - 5 < 2x - 1 < 11 + 5$, so $6 < 2x - 1 < 16$.<br><strong>Step 2: solve for $x$.</strong> Add $1$ to get $7 < 2x < 17$. Divide by $2$ to get $3.5 < x < 8.5$.<br><strong>Step 3: the integers.</strong> $x$ can be $4$, $5$, $6$, $7$ or $8$. The greatest is $8$ and the least is $4$.<br><strong>Check $x = 8$:</strong> the sides are $5$, $11$ and $15$, and $5 + 11 = 16$ is greater than $15$. ✓ At $x = 9$ the third side would be $17$, which is longer than $5 + 11$.",
  "trap": r"Using $\leq$ in place of $<$. At $x = 8.5$ the third side would be $16$, which equals $5 + 11$, and the three sides would lie flat on one line. The endpoints of the range are not included.",
  "micro": {"mc": True, "q": r"Which of the following could be the side lengths of a triangle?",
            "opts": ["$4$, $5$, $9$", "$3$, $8$, $12$", "$7$, $9$, $15$", "$2$, $10$, $13$"], "correct": 2,
            "exp": r"Add the two shortest lengths and compare with the longest. $4 + 5 = 9$ is equal, not greater. $3 + 8 = 11$ is less than $12$. $7 + 9 = 16$ is greater than $15$, so this set works. $2 + 10 = 12$ is less than $13$."}},
 {"ess": False, "name": "Rule 6: Triangles that share a height",
  "rule": r"same height: &nbsp;$\dfrac{\text{area}_1}{\text{area}_2} = \dfrac{\text{base}_1}{\text{base}_2}$",
  "say": r"Triangles that share a vertex and have their bases on the same line have the same height. Their areas are then in the same ratio as their bases. Count how many parts of the base each triangle stands on.",
  "fig": "s8",
  "prob": r"In the figure above, points $S$ and $T$ lie on $\overline{QR}$, and $QS : ST : TR = 5 : 2 : 3$. If the area of triangle $PQT$ is $42$, what is the area of triangle $PTR$?",
  "sol": r"<strong>Step 1: same height.</strong> Triangles $PQS$, $PST$ and $PTR$ share vertex $P$, and their bases lie on $\overline{QR}$. They have the same height, so their areas are in the ratio $5 : 2 : 3$.<br><strong>Step 2: match the given triangle to its base.</strong> Triangle $PQT$ stands on $\overline{QS}$ and $\overline{ST}$ together, which is $5 + 2 = 7$ parts. So $7$ parts are $42$, and one part is $6$.<br><strong>Step 3: answer the question.</strong> Triangle $PTR$ stands on $3$ parts: $3 \cdot 6 = 18$. The whole triangle $PQR$ is $10$ parts, or $60$.",
  "trap": r"Matching $42$ to the $5$ because it is the first number in the ratio. Triangle $PQT$ covers two of the three pieces of the base. Trace each triangle on the figure and count the parts under it.",
  "micro": {"q": r"Point $M$ lies on side $\overline{KL}$ of triangle $JKL$, with $KM = 4$ and $ML = 10$. If the area of triangle $JKM$ is $18$, the area of triangle $JML$ is", "accept": ["45"],
            "exp": r"Both triangles have their vertex at $J$, so they share a height. Each unit of base carries $18 \div 4 = 4.5$ units of area, and $4.5 \cdot 10 = 45$."}},
 {"ess": False, "name": "Rule 7: The altitude to the hypotenuse",
  "rule": r"$h^2 = pq$ &nbsp;·&nbsp; $a^2 = p\,(p + q)$ &nbsp;·&nbsp; $b^2 = q\,(p + q)$",
  "say": r"The altitude from the right angle splits the hypotenuse into two pieces. The altitude squared equals the product of the pieces. Each leg squared equals the piece beside that leg times the whole hypotenuse.",
  "fig": "s9",
  "prob": r"In the figure above, triangle $JKL$ has a right angle at $K$, and $\overline{KN}$ is perpendicular to $\overline{JL}$. If $JN = 25$ and $NL = 144$, what is the length of $\overline{KN}$? What is the length of $\overline{JK}$?",
  "sol": r"<strong>Step 1: the altitude.</strong> $KN^2 = 25 \cdot 144 = 3600$, so $KN = 60$.<br><strong>Step 2: the leg beside the $25$.</strong> The whole hypotenuse is $25 + 144 = 169$. $JK^2 = 25 \cdot 169 = 4225$, so $JK = 65$.<br><strong>Step 3: the other leg, as a check.</strong> $KL^2 = 144 \cdot 169 = 24336$, so $KL = 156$, and $65^2 + 156^2 = 28561 = 169^2$. ✓ The area agrees both ways: $\tfrac{1}{2}(65)(156) = 5070 = \tfrac{1}{2}(169)(60)$.<br><strong>A shorter look:</strong> $25$ and $144$ are $5^2$ and $12^2$, so this is the $5$-$12$-$13$ triangle with each side multiplied by $13$.",
  "trap": r"Multiplying the two pieces to find a leg. $25 \cdot 144$ gives the altitude squared. For a leg, multiply the piece beside it by the whole hypotenuse, $169$.",
  "micro": {"q": r"The altitude to the hypotenuse of a right triangle divides the hypotenuse into segments of lengths $4$ and $9$. The length of the altitude is", "accept": ["6"],
            "exp": r"$h^2 = 4 \cdot 9 = 36$, so $h = 6$."}},
]
LAST_STARRED_STEP_INDEX = 5  # 0-based index of the last starred step (Rule 4, continued)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
FLUENCY = [
 {"sec": "A. Angles", "items": [
   {"q": r"Parallel lines $\ell$ and $m$ are cut by a transversal. One of the eight angles formed measures $133^\circ$. The measure, in degrees, of each acute angle formed is", "accept": ["47", "47°"], "exp": r"The acute angles are supplements of the obtuse ones: $180 - 133 = 47$."},
   {"q": r"A transversal crosses two parallel lines. Two same-side interior angles measure $(2x)^\circ$ and $(3x + 25)^\circ$. Then $x =$", "accept": ["31"], "exp": r"Same-side interior angles add to $180^\circ$, so $5x + 25 = 180$ and $x = 31$. The angles are $62^\circ$ and $118^\circ$."},
   {"q": r"Two angles of a triangle measure $38^\circ$ and $79^\circ$. The measure, in degrees, of the third angle is", "accept": ["63", "63°"], "exp": r"$180 - 38 - 79 = 63$."},
   {"q": r"In an isosceles triangle, the angle between the two equal sides measures $96^\circ$. The measure, in degrees, of each of the other two angles is", "accept": ["42", "42°"], "exp": r"The two remaining angles are equal: $\dfrac{180 - 96}{2} = 42$."},
 ]},
 {"sec": "B. The Pythagorean theorem", "items": [
   {"q": r"A right triangle has legs of lengths $8$ and $15$. The length of the hypotenuse is", "accept": ["17"], "exp": r"$64 + 225 = 289$, and $\sqrt{289} = 17$. This is one of the common triples."},
   {"q": r"A right triangle has a hypotenuse of length $39$ and one leg of length $15$. The length of the other leg is", "accept": ["36"], "exp": r"$39^2 - 15^2 = 1521 - 225 = 1296$, and $\sqrt{1296} = 36$. This is $5$-$12$-$13$ with each side tripled."},
   {"q": r"A rectangle is $20$ units long and $21$ units wide. The length of its diagonal is", "accept": ["29"], "exp": r"The diagonal is the hypotenuse of a right triangle with legs $20$ and $21$: $400 + 441 = 841$, and $\sqrt{841} = 29$."},
   {"q": r"Squares are drawn on the three sides of a right triangle. The squares on the legs have areas $17$ and $64$. The length of the hypotenuse is", "accept": ["9"], "exp": r"The areas are the squares of the legs, so the square on the hypotenuse has area $17 + 64 = 81$. The hypotenuse is $9$."},
 ]},
 {"sec": "C. Special right triangles", "items": [
   {"mc": True, "q": r"Each leg of a $45$-$45$-$90$ triangle has length $6$. The length of the hypotenuse is", "opts": [r"$6\sqrt{2}$", r"$6\sqrt{3}$", "$12$", r"$3\sqrt{2}$"], "correct": 0, "exp": r"In a $45$-$45$-$90$ triangle, the hypotenuse is a leg times $\sqrt{2}$."},
   {"q": r"In a $30$-$60$-$90$ triangle, the shorter leg has length $7$. The length of the hypotenuse is", "accept": ["14"], "exp": r"The hypotenuse is twice the short leg: $2 \cdot 7 = 14$."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle, the longer leg has length $9$. The length of the shorter leg is", "opts": [r"$3\sqrt{3}$", r"$9\sqrt{3}$", "$4.5$", "$18$"], "correct": 0, "exp": r"The long leg is $x\sqrt{3}$, so $x = \dfrac{9}{\sqrt{3}} = 3\sqrt{3}$. Divide by $\sqrt{3}$ to go from the long leg to the short leg."},
   {"q": r"The area of an equilateral triangle with side length $12$ is $k\sqrt{3}$. Then $k =$", "accept": ["36"], "exp": r"$\dfrac{12^2\sqrt{3}}{4} = 36\sqrt{3}$. To confirm: the height is $6\sqrt{3}$, and $\tfrac{1}{2}(12)(6\sqrt{3}) = 36\sqrt{3}$."},
 ]},
 {"sec": "D. Less common rules", "items": [
   {"q": r"Two sides of a triangle have lengths $6$ and $13$. The greatest possible integer length of the third side is", "accept": ["18"], "exp": r"The third side is less than $6 + 13 = 19$, so the greatest integer is $18$."},
   {"mc": True, "q": r"In triangle $ABC$, the measures of angles $A$, $B$ and $C$ are $48^\circ$, $61^\circ$ and $71^\circ$. Which side is the longest?", "opts": [r"$\overline{AB}$", r"$\overline{BC}$", r"$\overline{AC}$", "It cannot be determined."], "correct": 0, "exp": r"The longest side is across from the largest angle. Angle $C$ is the largest, and the side across from $C$ is $\overline{AB}$."},
   {"q": r"Point $D$ lies on side $\overline{QR}$ of triangle $PQR$, and $QD : DR = 2 : 7$. If the area of triangle $PQD$ is $8$, the area of triangle $PQR$ is", "accept": ["36"], "exp": r"The triangles share the height from $P$, so the areas follow the bases. Two parts are $8$, so one part is $4$, and the whole triangle is $9$ parts: $36$."},
   {"q": r"The altitude to the hypotenuse of a right triangle divides the hypotenuse into segments of lengths $5$ and $20$. The length of the altitude is", "accept": ["10"], "exp": r"$h^2 = 5 \cdot 20 = 100$, so $h = 10$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy", "fig": "p1",
  "stem": r"In the figure above, line $t$ intersects parallel lines $\ell$ and $m$. What is the value of $x$?",
  "options": ["$34$", "$56$", "$66$", "$124$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $\ell \parallel m$, a marked angle of $124^\circ$ at one crossing, and $x^\circ$ at the other.<br><br>The angle that corresponds to the $124^\circ$ angle is at the lower crossing in the same position: above $m$ and to the left of $t$. The $x^\circ$ angle is beside it on line $m$, so the two add to $180^\circ$. $x = 180 - 124 = 56$.",
  "trap": r"Choice D sets $x$ equal to $124$. The two marked angles are not a matching pair: both are above their lines, but one is to the left of the transversal and the other is to the right. Name the pair before you write the equation. Choice A is $124 - 90$, which uses $90$ where $180$ belongs."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"In triangle $ABC$, the measure of angle $A$ is $52^\circ$ and the measure of angle $B$ is $71^\circ$. What is the measure, in degrees, of angle $C$?",
  "label": "Angle $C =$", "accept": ["57", "57°"],
  "sol": r"<strong>Given:</strong> two of the three angles of a triangle.<br><br>The angles add to $180^\circ$. $52 + 71 = 123$, so angle $C$ measures $180 - 123 = 57$ degrees.",
  "trap": r"Answering $123$, the sum of the two given angles. That number is the exterior angle at $C$, not the angle inside the triangle. Check which one the question asks for."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"A support cable $37$ meters long runs from the top of a vertical tower to a point on level ground $12$ meters from the base of the tower. What is the height of the tower, in meters?",
  "options": ["$25$", "$35$", r"$\sqrt{1513}$", "$49$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a right triangle formed by the tower, the ground and the cable.<br><br>The cable is across from the right angle, so it is the hypotenuse, and the height $h$ is a leg. $h^2 = 37^2 - 12^2 = 1369 - 144 = 1225$, so $h = 35$.",
  "trap": r"Choice C adds the squares, $37^2 + 12^2 = 1513$, which treats the cable as a leg. Sketch the triangle and label the hypotenuse first. Choices A and D subtract or add the lengths without squaring."},
 {"ess": True, "type": "ne", "diff": "Medium", "fig": "p4",
  "stem": r"In the figure above, point $A$ lies on $\overline{BE}$. What is the value of $x$?",
  "label": "$x =$", "accept": ["25"],
  "sol": r"<strong>Given:</strong> an exterior angle of $(4x - 5)^\circ$ at $A$, and the two interior angles that do not touch it: $(x + 20)^\circ$ at $B$ and $(2x)^\circ$ at $C$.<br><br>The exterior angle equals the sum of those two: $4x - 5 = (x + 20) + 2x = 3x + 20$. So $x = 25$. Check: the angles at $B$ and $C$ are $45^\circ$ and $50^\circ$, and the exterior angle is $95^\circ$. ✓",
  "trap": r"Adding all three expressions and setting the total equal to $180$. The $(4x - 5)^\circ$ angle is outside the triangle, so it is not one of the three angles that add to $180^\circ$."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"An equilateral triangle has a perimeter of $42$. What is the height of the triangle?",
  "options": ["$7$", r"$7\sqrt{2}$", r"$7\sqrt{3}$", r"$14\sqrt{3}$"], "correct": 2,
  "sol": r"<strong>Given:</strong> a perimeter of $42$, so each side is $14$.<br><br>The height splits the equilateral triangle into two $30$-$60$-$90$ triangles. Each has a hypotenuse of $14$ (a side of the triangle) and a short leg of $7$ (half of the base). The height is the long leg: $7\sqrt{3}$.",
  "trap": r"Choice A is the short leg, half of the base. Choice D multiplies the full side by $\sqrt{3}$. The height is built from the short leg: half of the side, times $\sqrt{3}$."},
 {"ess": False, "type": "ne", "diff": "Medium",
  "stem": r"Two sides of a triangle have lengths $9$ and $14$. The length of the third side is an integer. What is the least possible perimeter of the triangle?",
  "label": "Perimeter $=$", "accept": ["29"],
  "sol": r"<strong>Given:</strong> two sides, and a third side that is an integer.<br><br>The third side is longer than the difference of the other two: $14 - 9 = 5$. The smallest integer greater than $5$ is $6$. The least perimeter is $9 + 14 + 6 = 29$. Check: $6 + 9 = 15$, which is greater than $14$. ✓",
  "trap": r"Using $5$ for the third side, which gives $28$. A side of $5$ makes $5 + 9 = 14$, and the three sides lie flat. The third side has to be greater than the difference, not equal to it. Also check what the question asks for: the perimeter, not the side."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p7",
  "stem": r"In the figure above, $\ell \parallel m$. What is the value of $x$?",
  "options": ["$13$", "$81$", "$99$", "$162$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $34^\circ$ at $A$ on line $\ell$, $47^\circ$ at $C$ on line $m$, and $x^\circ$ at the bend $B$ between the lines.<br><br>Draw a line through $B$ parallel to $\ell$ and $m$. It splits the angle at $B$ into two parts. The upper part and the $34^\circ$ angle are alternate interior angles, so the upper part is $34^\circ$. The lower part and the $47^\circ$ angle are alternate interior angles, so the lower part is $47^\circ$. $x = 34 + 47 = 81$.",
  "trap": r"Choice C is $180 - 81$, which comes from treating the three marked angles as the angles of a triangle. No triangle is drawn here, so add a line that connects the bend to the parallel lines. Choice A subtracts the two angles."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p8",
  "stem": r"In the figure above, angles $B$ and $D$ are right angles, $AB = 7$, $BC = 24$, and $AD = 15$. What is the length of $\overline{CD}$?",
  "options": ["$16$", "$20$", "$25$", r"$5\sqrt{34}$"], "correct": 1,
  "sol": r"<strong>Given:</strong> two right triangles that share side $\overline{AC}$.<br><br>In triangle $ABC$, $\overline{AC}$ is the hypotenuse: $AC^2 = 7^2 + 24^2 = 625$, so $AC = 25$. In triangle $ADC$, $\overline{AC}$ is the hypotenuse again and $\overline{CD}$ is a leg: $CD^2 = 25^2 - 15^2 = 400$, so $CD = 20$.",
  "trap": r"Choice C stops after the first triangle. Choice D adds in the second triangle, $625 + 225 = 850$, but $\overline{AC}$ is the hypotenuse there, so the squares are subtracted. In a figure with two right triangles, find the right angle in each one to locate its hypotenuse."},
 {"ess": False, "type": "mc", "diff": "Medium-hard", "fig": "p9",
  "stem": r"In rectangle $PQRS$ above, point $T$ lies on diagonal $\overline{PR}$, and $PT : TR = 2 : 3$. If the area of triangle $PTS$ is $14$, what is the area of rectangle $PQRS$?",
  "options": ["$35$", "$49$", "$56$", "$70$"], "correct": 3,
  "sol": r"<strong>Given:</strong> triangles $PTS$ and $TRS$ share vertex $S$, and their bases $\overline{PT}$ and $\overline{TR}$ lie on the same line.<br><br>They have the same height, so their areas follow their bases. The area of triangle $TRS$ is $14 \cdot \tfrac{3}{2} = 21$. Triangle $PRS$ is the two together: $14 + 21 = 35$. The diagonal cuts the rectangle into two triangles of equal area, so the rectangle has area $2 \cdot 35 = 70$.",
  "trap": r"Choice A is the area of triangle $PRS$, which is half of the rectangle. The question asks for the whole rectangle, so double it. Before you answer, check which shape the $2 : 3$ ratio divides (the triangle) and which shape the question asks about (the rectangle)."},
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "p10",
  "stem": r"In the figure above, $O$ is the center of the circle, the radius is $6$, and the measure of angle $POQ$ is $120^\circ$. The area of triangle $POQ$ is $k\sqrt{3}$. What is the value of $k$?",
  "label": "$k =$", "accept": ["9"],
  "sol": r"<strong>Given:</strong> an isosceles triangle with two sides of $6$ (both are radii) and a $120^\circ$ angle between them.<br><br>Draw the height from $O$ to $\overline{PQ}$. It splits the $120^\circ$ angle into two $60^\circ$ angles and makes two $30$-$60$-$90$ triangles, each with a hypotenuse of $6$. The short leg is the height: $3$. The long leg is half of $\overline{PQ}$: $3\sqrt{3}$, so $PQ = 6\sqrt{3}$. The area is $\tfrac{1}{2}(6\sqrt{3})(3) = 9\sqrt{3}$, so $k = 9$.",
  "trap": r"Using $\tfrac{1}{2}(6)(6) = 18$. That would be the area if the two radii met at a right angle. Here they are not a base and its height. Draw the height to $\overline{PQ}$ and use the $30$-$60$-$90$ ratios."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "mc", "diff": "Medium-hard", "fig": "c1",
  "stem": r"In the figure above, line $p$ is parallel to line $q$. Lines $s$ and $t$ each cross both of them. Which of the following must be true?<br><br>&nbsp;&nbsp;&nbsp;&nbsp;I. $w = y$<br>&nbsp;&nbsp;&nbsp;&nbsp;II. $w + x = 180$<br>&nbsp;&nbsp;&nbsp;&nbsp;III. $y = z$",
  "options": ["II only", "III only", "II and III only", "I, II, and III"], "correct": 2,
  "sol": r"<strong>Given:</strong> $p \parallel q$ and two transversals. Nothing says that $s$ and $t$ are parallel to each other.<br><br><strong>II is true.</strong> $w^\circ$ and $x^\circ$ are both on transversal $s$. The angle that corresponds to $w^\circ$ is at the lower crossing, above $q$ and to the right of $s$. The $x^\circ$ angle is beside it on line $q$, so $w + x = 180$.<br><strong>III is true.</strong> $y^\circ$ and $z^\circ$ are both on transversal $t$, between the parallel lines and on opposite sides of $t$. They are alternate interior angles, so $y = z$.<br><strong>I does not have to be true.</strong> $w^\circ$ and $y^\circ$ are on different transversals. They would be equal only if $s$ and $t$ were parallel, and that is not given.",
  "trap": r"Parallel lines relate the angles along one transversal. Angles on two different transversals are related only when the question says those transversals are parallel, however the figure looks."},
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "c2",
  "stem": r"In the figure above, $\ell \parallel m$. Points $P$ and $Q$ lie on $\ell$, points $S$ and $T$ lie on $m$, and point $R$ lies on $\overline{QS}$. $PQ = QR$ and $SR = ST$. If the measure of angle $PQR$ is $104^\circ$, what is the measure, in degrees, of angle $SRT$?",
  "label": "Angle $SRT =$", "accept": ["52", "52°"],
  "sol": r"<strong>Given:</strong> two isosceles triangles, $PQR$ and $SRT$, attached to a transversal between parallel lines.<br><br><strong>Step 1: cross to the other line.</strong> Angles $PQS$ and $QST$ are same-side interior angles, so angle $QST$ measures $180 - 104 = 76$ degrees.<br><strong>Step 2: use the isosceles triangle.</strong> In triangle $SRT$, $SR = ST$, so the angles across from those sides, at $T$ and at $R$, are equal. Each is $\dfrac{180 - 76}{2} = 52$ degrees.",
  "trap": r"Work from the parallel lines into the triangle. Rule 1 gives the angle at $S$, and then the isosceles triangle splits what is left of $180^\circ$ evenly between its other two angles.",
  "extrasIntro": r"The same figure has more to offer. Three more questions about it.",
  "extras": [
   {"type": "ne", "q": r"In the same figure, the measure, in degrees, of angle $QRP$ is", "label": "$=$", "accept": ["38", "38°"], "exp": r"Triangle $PQR$ is isosceles with a $104^\circ$ angle between its equal sides: $\dfrac{180 - 104}{2} = 38$."},
   {"type": "ne", "q": r"In the same figure, the measure, in degrees, of angle $PRT$ is", "label": "$=$", "accept": ["90", "90°"], "exp": r"Angles $QRP$, $PRT$ and $SRT$ meet along the straight segment $\overline{QS}$ at $R$, so they add to $180^\circ$: $180 - 38 - 52 = 90$."},
   {"type": "ne", "q": r"Suppose angle $PQR$ measured $130^\circ$ instead. The measure, in degrees, of angle $PRT$ would be", "label": "$=$", "accept": ["90", "90°"], "exp": r"The base angles become $25^\circ$ and $65^\circ$, and $180 - 25 - 65 = 90$ again. If angle $PQR$ measures $a^\circ$, the two base angles are $\dfrac{180 - a}{2}$ and $\dfrac{a}{2}$, which add to $90$ for every value of $a$."},
  ]},
 {"ess": True, "type": "mc", "diff": "Medium-hard", "fig": "c3",
  "stem": r"The figure above shows pentagon $ABCDE$, formed by rectangle $ABCE$ and isosceles triangle $CDE$. $AB = 12$, $BC = 5$, and angles $DEC$ and $DCE$ each measure $30^\circ$. What is the perimeter of the pentagon?",
  "options": [r"$22 + 4\sqrt{3}$", r"$22 + 8\sqrt{3}$", r"$22 + 12\sqrt{3}$", r"$34 + 8\sqrt{3}$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a rectangle $12$ wide and $5$ tall, topped by an isosceles triangle with $30^\circ$ base angles.<br><br>Draw the height from $D$ to $\overline{EC}$. It makes two $30$-$60$-$90$ triangles. In each one, the leg beside the $30^\circ$ angle is half of $EC = 12$, so the long leg is $6$. The short leg is $\dfrac{6}{\sqrt{3}} = 2\sqrt{3}$, and the hypotenuse is $4\sqrt{3}$. So $DE = DC = 4\sqrt{3}$.<br>Perimeter: $AB + BC + CD + DE + EA = 12 + 5 + 4\sqrt{3} + 4\sqrt{3} + 5 = 22 + 8\sqrt{3}$.",
  "trap": r"The $6$ is the long leg, so divide by $\sqrt{3}$ to reach the short leg before you double. Then count only the outside edges: $\overline{EC}$ is inside the pentagon, so it is not part of the perimeter (choice D includes it).",
  "extrasIntro": r"Special right triangles inside other shapes: find the square, the equilateral triangle or the $30^\circ$ angle, then build from the short leg. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"A square has a perimeter of $52$. The length of its diagonal is $k\sqrt{2}$. Then $k =$", "label": "$k =$", "accept": ["13"], "exp": r"Each side is $52 \div 4 = 13$, and the diagonal of a square is its side times $\sqrt{2}$."},
   {"type": "ne", "q": r"The height of an equilateral triangle is $11\sqrt{3}$. The length of each side is", "label": "Side $=$", "accept": ["22"], "exp": r"The height is the long leg of a $30$-$60$-$90$ triangle, so the short leg is $11$. The short leg is half of a side, so the side is $22$."},
   {"type": "ne", "q": r"In a $30$-$60$-$90$ triangle, the longer leg has length $15$. The length of the hypotenuse is $k\sqrt{3}$. Then $k =$", "label": "$k =$", "accept": ["10"], "exp": r"The short leg is $\dfrac{15}{\sqrt{3}} = 5\sqrt{3}$, and the hypotenuse is twice that: $10\sqrt{3}$."},
  ]},
 {"ess": False, "type": "mc", "diff": "Medium-hard", "fig": "c4",
  "stem": r"In quadrilateral $JKLM$ above, $JK = 5$, $JM = 9$, $KL = 6$, and $LM = 12$. Which of the following could be the length of diagonal $\overline{KM}$?",
  "options": ["$5$", "$6$", "$13$", "$14$"], "correct": 2,
  "sol": r"<strong>Given:</strong> the diagonal is a side of two triangles at once, so it has to fit both.<br><br>Triangle $JKM$ has sides $5$ and $9$: $4 < KM < 14$. Triangle $KLM$ has sides $6$ and $12$: $6 < KM < 18$. Both together: $6 < KM < 14$. Of the choices, only $13$ is in that range.",
  "trap": r"A shared side has to satisfy each triangle it belongs to. Write one range per triangle, then keep the overlap. The endpoints $6$ and $14$ are not included."},
 {"ess": True, "type": "ne", "diff": "Hard", "fig": "c5",
  "stem": r"In rectangle $PQRS$ above, $\overline{QT}$ is perpendicular to diagonal $\overline{PR}$, $QT = 6$, and the measure of angle $PQT$ is $60^\circ$. The area of the rectangle is $k\sqrt{3}$. What is the value of $k$?",
  "label": "$k =$", "accept": ["48"],
  "sol": r"<strong>Given:</strong> a height drawn inside a rectangle, which makes two $30$-$60$-$90$ triangles.<br><br><strong>Triangle $PQT$.</strong> The right angle is at $T$ and angle $PQT$ is $60^\circ$, so angle $QPT$ is $30^\circ$. $\overline{QT}$ is across from the $30^\circ$ angle, so it is the short leg, and the hypotenuse is $PQ = 12$.<br><strong>Triangle $QTR$.</strong> Angle $PQR$ is $90^\circ$, so angle $TQR$ is $30^\circ$. Here $\overline{QT}$ touches the $30^\circ$ angle, so it is the long leg. The short leg is $TR = \dfrac{6}{\sqrt{3}} = 2\sqrt{3}$, and the hypotenuse is $QR = 4\sqrt{3}$.<br><strong>Area.</strong> $PQ \cdot QR = 12 \cdot 4\sqrt{3} = 48\sqrt{3}$, so $k = 48$.",
  "trap": r"One segment can play different roles in different triangles. $\overline{QT}$ is the short leg of triangle $PQT$ and the long leg of triangle $QTR$. In each triangle, find the $30^\circ$ angle first: the side across from it is the short leg."},
 {"ess": False, "type": "ne", "diff": "Hard", "fig": "c6",
  "stem": r"In the figure above, triangle $FGH$ has a right angle at $G$, and $\overline{GK}$ is perpendicular to $\overline{FH}$. If $FG = 12$ and $FK = 9$, what is the length of $\overline{KH}$?",
  "label": "$KH =$", "accept": ["7"],
  "sol": r"<strong>Given:</strong> a leg and the piece of the hypotenuse beside it.<br><br>A leg squared equals the piece beside it times the whole hypotenuse: $12^2 = 9 \cdot FH$, so $FH = 16$. Then $KH = 16 - 9 = 7$.<br><strong>Another route:</strong> in right triangle $FKG$, $GK^2 = 144 - 81 = 63$. The altitude relationship $GK^2 = FK \cdot KH$ gives $63 = 9 \cdot KH$, so $KH = 7$ again.",
  "trap": r"The leg relationship gives the whole hypotenuse, not the missing piece. Subtract the piece you were given to finish.",
  "extrasIntro": r"The altitude squared is the product of the two pieces, and a leg squared is the piece beside it times the whole hypotenuse. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The altitude to the hypotenuse of a right triangle divides it into segments of lengths $3$ and $27$. The length of the altitude is", "label": "$h =$", "accept": ["9"], "exp": r"$h^2 = 3 \cdot 27 = 81$, so $h = 9$."},
   {"type": "ne", "q": r"The altitude to the hypotenuse of a right triangle divides it into segments of lengths $4$ and $5$. The length of the leg beside the segment of length $4$ is", "label": "Leg $=$", "accept": ["6"], "exp": r"The whole hypotenuse is $9$, so the leg squared is $4 \cdot 9 = 36$, and the leg is $6$."},
   {"type": "ne", "q": r"A right triangle has legs of lengths $5$ and $12$. The length of the altitude to the hypotenuse is", "label": "$h =$", "accept": ["60/13", "4.615", "4.616"], "exp": r"The hypotenuse is $13$. Write the area two ways: $\tfrac{1}{2}(5)(12) = \tfrac{1}{2}(13)\,h$, so $h = \dfrac{60}{13}$, which is about $4.615$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Hard · algebra blend",
  "stem": r"A right triangle has legs of lengths $a$ and $b$ and a hypotenuse of length $12$. If $a + b = 16$, what is the area of the triangle?",
  "label": "Area $=$", "accept": ["28"],
  "sol": r"<strong>Given:</strong> the hypotenuse and the sum of the legs, but neither leg.<br><br>The area is $\tfrac{1}{2}ab$, so the goal is the product $ab$. Square the sum: $(a + b)^2 = a^2 + 2ab + b^2$. By the Pythagorean theorem, $a^2 + b^2 = 12^2 = 144$. So $16^2 = 144 + 2ab$, which gives $2ab = 112$ and $ab = 56$. The area is $\tfrac{1}{2}(56) = 28$.",
  "trap": r"You do not need $a$ and $b$ separately (they are $8 + 2\sqrt{2}$ and $8 - 2\sqrt{2}$). When a question gives a sum and asks about a product, squaring the sum connects them: $(a + b)^2 = a^2 + b^2 + 2ab$."},
 {"ess": True, "type": "ne", "diff": "Hard", "fig": "c8",
  "stem": r"In the figure above, a semicircle is drawn on each side of right triangle $ABC$, and $AB : BC = 2 : 3$. If the area of the semicircle on hypotenuse $\overline{AC}$ is $78$, what is the area of the semicircle on $\overline{BC}$?",
  "label": "Area $=$", "accept": ["54"],
  "sol": r"<strong>Given:</strong> three similar shapes built on the sides of a right triangle, and the ratio of the legs.<br><br>The area of a semicircle is proportional to the square of its diameter. If $AB = 2x$ and $BC = 3x$, then $AC^2 = 4x^2 + 9x^2 = 13x^2$. The three areas are in the ratio $4 : 9 : 13$, the same as the squares of the sides. The semicircle on the hypotenuse is $13$ parts, so one part is $78 \div 13 = 6$. The semicircle on $\overline{BC}$ is $9$ parts: $54$.<br><strong>Check:</strong> the semicircle on $\overline{AB}$ is $4$ parts, or $24$, and $24 + 54 = 78$. ✓",
  "trap": r"Areas scale with the squares of the sides. A $2 : 3$ ratio of lengths becomes a $4 : 9$ ratio of areas, and the two areas on the legs add up to the area on the hypotenuse."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"Lines $\ell$ and $m$ are parallel. A transversal forms same-side interior angles that measure $x^\circ$ and $75^\circ$. What is the value of $x$?", "opts": ["$75$", "$105$", "$15$", "$285$"], "correct": 1,
  "exp": r"Same-side interior angles add to $180^\circ$: $x = 180 - 75 = 105$."},
 {"q": r"In a $30$-$60$-$90$ triangle, the shorter leg has length $11$. What is the length of the longer leg?", "opts": [r"$11\sqrt{2}$", r"$11\sqrt{3}$", "$22$", r"$\dfrac{11\sqrt{3}}{3}$"], "correct": 1,
  "exp": r"The long leg is the short leg times $\sqrt{3}$. The hypotenuse is the side that doubles: $22$."},
 {"q": r"A right triangle has legs of lengths $12$ and $16$. What is the length of the hypotenuse?", "opts": ["$20$", "$28$", r"$4\sqrt{7}$", "$400$"], "correct": 0,
  "exp": r"$144 + 256 = 400$, and $\sqrt{400} = 20$. This is $3$-$4$-$5$ with each side multiplied by $4$."},
]

# ---------------------------------------------------------------- FIGURES (specs in Python, drawn by geoSVG)
def pt(x, y): return [round(x, 3), round(y, 3)]
def pol(p, deg, r=1.0): return pt(p[0] + r * math.cos(math.radians(deg)), p[1] + r * math.sin(math.radians(deg)))
def mid(a, b, f=0.5): return pt(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
def cen(*ps): return pt(sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps))
def seg(a, b, cls=None):
    o = {'a': a, 'b': b}
    if cls: o['cls'] = cls
    return o
def ang(at, d1, d2, t=None, **k):
    """Angle at `at` between the directions d1 and d2 (degrees, counterclockwise from east)."""
    o = {'at': at, 'a': pol(at, d1), 'b': pol(at, d2)}
    if t: o['t'] = t
    o.update(k)
    return o
def ang3(at, a, b, t=None, **k):
    """Angle at `at` between the rays toward points a and b."""
    o = {'at': at, 'a': a, 'b': b}
    if t: o['t'] = t
    o.update(k)
    return o
def side(a, b, t, off=13, **k):
    """A label beside the middle of segment a-b; off > 0 is to the left of a->b."""
    o = {'a': a, 'b': b, 't': t, 'off': off}
    o.update(k)
    return o
def lab(p, t, deg=None, away=None, **k):
    """A letter beside point p, in direction deg (degrees) or pushed away from the point `away`; d= sets the distance in px."""
    o = {'p': p, 't': t}
    if away is not None: o['away'] = away
    else: o['dir'] = deg
    o.update(k)
    return o
def txt(at, t, **k):
    o = {'at': at, 't': t}
    o.update(k)
    return o
def transversal(th, px, yl, ym, up=1.4, down=1.3):
    """A transversal at th degrees through P on the upper line (y = yl); returns P, Q (on y = ym) and its two ends."""
    P = pt(px, yl); Q = pt(px - (yl - ym) / math.tan(math.radians(th)), ym)
    return P, Q, pol(P, th, up), pol(Q, th + 180, down)

NOTE = 'Note: Figure not drawn to scale.'
FIGS = {}

# --- Rule 1: eight angles, two measures
P, Q, top, bot = transversal(58, 5.7, 4.2, 1.6)
FIGS['r_par'] = dict(box=[0, 0, 10, 5.8], w=340, h=205, alt='two parallel lines crossed by a transversal; at each crossing the two acute angles are marked a and the two obtuse angles are marked b, with a + b = 180',
    segs=[seg(pt(0.5, 4.2), pt(9.1, 4.2)), seg(pt(0.5, 1.6), pt(9.1, 1.6)), seg(bot, top)],
    arcs=[a for X in (P, Q) for a in (ang(X, 0, 58, 'a°', r=0, lr=27), ang(X, 58, 180, 'b°', r=0, lr=17), ang(X, 180, 238, 'a°', r=0, lr=27), ang(X, 238, 360, 'b°', r=0, lr=17))],
    texts=[txt(pt(9.1, 4.2), 'ℓ', dx=11), txt(pt(9.1, 1.6), 'm', dx=11), txt(top, 't', dx=11, dy=4), txt(pt(7.7, 2.9), 'a + b = 180')])

# --- Rule 2: angle sum and exterior angle
A, B, C, D = pt(2.4, 4.2), pt(0.8, 0.8), pt(6.2, 0.8), pt(8.7, 0.8)
FIGS['r_tri'] = dict(box=[0, 0, 9.4, 5], w=330, h=190, alt='a triangle with interior angles a, b and c; one side is extended past the angle c to form the exterior angle d',
    segs=[seg(A, B), seg(A, C), seg(B, D)],
    arcs=[ang3(A, B, C, 'a°', r=16, lr=31), ang3(B, C, A, 'b°', r=18, lr=33), ang3(C, A, B, 'c°', r=16, lr=31), ang3(C, D, A, 'd°', r=13, lr=27)])

# --- Rule 2, Example C: a bend between parallel lines
A = pt(1.9, 4.0); B = pol(A, -35, (4.0 - 2.3) / math.sin(math.radians(35))); C = pol(B, 230, (2.3 - 0.8) / math.sin(math.radians(50)))
FIGS['r_zig'] = dict(box=[0, 0.2, 8, 4.7], w=330, h=200, alt='parallel lines l and m; a segment leaves line l at 35 degrees and a segment leaves line m at 50 degrees; they meet at a bend between the lines, where a dashed line parallel to both splits the angle into 35 degrees and 50 degrees',
    segs=[seg(pt(0.5, 4.0), pt(7.2, 4.0)), seg(pt(0.5, 0.8), pt(7.2, 0.8)), seg(A, B), seg(B, C), seg(pt(0.9, 2.3), pt(B[0] + 1.0, 2.3), 'dash')],
    arcs=[ang(A, 0, -35, '35°', r=26, lr=43), ang(C, 0, 50, '50°', r=22, lr=38), ang(B, 145, 180, '35°', r=30, lr=46), ang(B, 180, 230, '50°', r=24, lr=40)],
    texts=[txt(pt(7.2, 4.0), 'ℓ', dx=11), txt(pt(7.2, 0.8), 'm', dx=11)])

# --- Rule 3: the squares on a 3-4-5 triangle
FIGS['r_pyth'] = dict(box=[-3, -4, 7, 7], w=300, h=320, pad=14, alt='a right triangle with legs 3 and 4 and hypotenuse 5, with a square built on each side; the squares have areas 9, 16 and 25, and 9 + 16 = 25',
    polys=[dict(pts=[pt(0, 0), pt(0, 3), pt(-3, 3), pt(-3, 0)], cls='tile'), dict(pts=[pt(0, 0), pt(4, 0), pt(4, -4), pt(0, -4)], cls='tile'),
           dict(pts=[pt(0, 3), pt(4, 0), pt(7, 4), pt(3, 7)], cls='tile'), dict(pts=[pt(0, 0), pt(0, 3), pt(4, 0)], cls='shade')],
    segs=[seg(pt(0, 0), pt(0, 3)), seg(pt(0, 0), pt(4, 0)), seg(pt(0, 3), pt(4, 0))],
    rights=[dict(at=pt(0, 0), a=pt(0, 3), b=pt(4, 0), s=8)],
    texts=[txt(pt(-1.5, 1.5), '3² = 9'), txt(pt(2, -2), '4² = 16'), txt(pt(3.5, 3.5), '5² = 25'), txt(pt(5.6, -1.7), '9 + 16 = 25')])

# --- Rule 4: the two special right triangles
A, B, C = pt(0, 0), pt(4, 0), pt(4, 4)
FIGS['r_45'] = dict(box=[-0.5, -0.7, 5.2, 4.3], w=250, h=250, alt='a 45-45-90 triangle drawn as half of a square: legs x and x, hypotenuse x times the square root of 2',
    segs=[seg(A, pt(0, 4), 'dash'), seg(pt(0, 4), C, 'dash'), seg(A, B), seg(B, C), seg(A, C)],
    rights=[dict(at=B, a=A, b=C)],
    sides=[side(A, B, 'x', -13), side(B, C, 'x', -12), side(A, C, 'x√2', 17)],
    arcs=[ang3(A, B, C, '45°', r=24, lr=42), ang3(C, A, B, '45°', r=24, lr=42)])
D, B, A = pt(2, 0), pt(4, 0), pt(2, 2 * math.sqrt(3))
FIGS['r_30'] = dict(box=[-0.3, -0.6, 5.0, 3.8], w=270, h=250, alt='a 30-60-90 triangle drawn as half of an equilateral triangle: short leg x across from the 30 degree angle, long leg x times the square root of 3, hypotenuse 2x',
    segs=[seg(pt(0, 0), D, 'dash'), seg(pt(0, 0), A, 'dash'), seg(D, B), seg(B, A), seg(A, D)],
    rights=[dict(at=D, a=B, b=A)],
    sides=[side(D, B, 'x', -13), side(D, A, 'x√3', 21), side(B, A, '2x', -15)],
    arcs=[ang3(A, D, B, '30°', r=38, lr=64, dx=1), ang3(B, A, D, '60°', r=17, lr=32)])

# --- Rule 5: the third side
A, B = pt(0, 0), pt(8, 0); C = pol(A, 50, 5)
FIGS['r_ineq'] = dict(box=[-0.6, -1.5, 8.6, 4.2], w=300, h=205, alt='a triangle with sides 5, 8 and c; the third side c is greater than 8 minus 5 and less than 8 plus 5',
    segs=[seg(A, B), seg(A, C), seg(B, C)],
    sides=[side(A, B, '8', -13), side(A, C, '5', 13), side(B, C, 'c', -13)],
    texts=[txt(pt(4, -1.25), '8 − 5 < c < 8 + 5')])

# --- Rule 6: two triangles, one height
P, Q, R, S, F = pt(3.2, 4), pt(0, 0), pt(7, 0), pt(2, 0), pt(3.2, 0)
FIGS['r_share'] = dict(box=[-0.6, -1.0, 7.6, 4.6], w=320, h=235, alt='triangle PQR with point S on side QR; QS is 4 and SR is 10; triangles PQS and PSR are shaded differently and share the dashed height h from P',
    polys=[dict(pts=[P, Q, S], cls='shade'), dict(pts=[P, S, R], cls='shade2')],
    segs=[seg(P, Q), seg(P, R), seg(Q, R), seg(P, S), seg(P, F, 'dash')],
    rights=[dict(at=F, a=P, b=R, s=8)],
    sides=[side(Q, S, '4', -13), side(S, R, '10', -13, f=0.62)],
    pts=[lab(P, 'P', 90), lab(Q, 'Q', 200), lab(S, 'S', 270, dx=7), lab(R, 'R', -20)],
    texts=[txt(pt(3.2, 1.9), 'h', dx=10)])

# --- Rule 7: the altitude to the hypotenuse
J, L, N, K = pt(0, 0), pt(10, 0), pt(3.6, 0), pt(3.6, 4.8)
FIGS['r_alt'] = dict(box=[-0.5, -1.0, 10.5, 5.3], w=340, h=215, alt='a right triangle with legs a and b; the altitude h from the right angle meets the hypotenuse and splits it into the pieces p, beside leg a, and q, beside leg b',
    segs=[seg(J, K), seg(K, L), seg(J, L), seg(K, N, 'thin')],
    rights=[dict(at=K, a=J, b=L), dict(at=N, a=K, b=L, s=8)],
    sides=[side(J, K, 'a', 13), side(K, L, 'b', 13), side(J, N, 'p', -13), side(N, L, 'q', -13)],
    texts=[txt(pt(3.6, 2.3), 'h', dx=10)])

# --- Step 1
P, Q, top, bot = transversal(69, 5.5, 4.2, 1.5)
FIGS['s1'] = dict(box=[0, 0, 10, 5.8], w=340, h=210, alt='parallel lines l and m crossed by a transversal; the angle above line l on the left of the transversal is (3x + 15) degrees and the angle above line m on the right of the transversal is (2x + 5) degrees',
    segs=[seg(pt(0.5, 4.2), pt(9.1, 4.2)), seg(pt(0.5, 1.5), pt(9.1, 1.5)), seg(bot, top)],
    arcs=[ang(P, 69, 180, '(3x + 15)°', r=13, lr=40, dx=-22), ang(Q, 0, 69, '(2x + 5)°', r=15, lr=44, dx=22, dy=6)],
    texts=[txt(pt(9.1, 4.2), 'ℓ', dx=11), txt(pt(9.1, 1.5), 'm', dx=11)])

# --- Step 2: angles 72, 56, 52 drawn to scale
B, C, D = pt(0.8, 0.8), pt(6.4, 0.8), pt(8.9, 0.8); A = pol(B, 56, 5.6 * math.sin(math.radians(52)) / math.sin(math.radians(72)))
FIGS['s2'] = dict(box=[0, 0, 9.6, 5.3], w=340, h=200, alt='triangle ABC with side BC extended to D; the angle at A is 3x degrees, the angle at B is (2x + 8) degrees, and the exterior angle ACD is 128 degrees',
    segs=[seg(A, B), seg(A, C), seg(B, D)],
    arcs=[ang3(A, B, C, '3x°', r=15, lr=32), ang3(B, C, A, '(2x + 8)°', r=17, lr=52, dy=2), ang3(C, D, A, '128°', r=13, lr=29)],
    pts=[lab(A, 'A', 90), lab(B, 'B', 200), lab(C, 'C', 270, dx=-4), lab(D, 'D', 270)])

# --- Step 3: two segments crossing between parallel lines (38, 57, k = 95)
P, Q = pt(1.5, 4.0), pt(5.1, 4.0); T = pol(P, -38, 3.6 * math.sin(math.radians(57)) / math.sin(math.radians(85)))
S = pol(P, -38, (4.0 - 0.6) / math.sin(math.radians(38))); R = pol(Q, 237, (4.0 - 0.6) / math.sin(math.radians(57)))
FIGS['s3'] = dict(box=[0, 0, 7.8, 4.7], w=340, h=215, alt='parallel lines l and m; segment PS runs from P on l to S on m and segment QR runs from Q on l to R on m; they cross at T; the angle at P between line l and PS is 38 degrees, the angle at R between line m and RQ is 57 degrees, and the angle PTR is k degrees',
    segs=[seg(pt(0.5, 4.0), pt(7.0, 4.0)), seg(pt(0.5, 0.6), pt(7.0, 0.6)), seg(P, S), seg(Q, R)],
    arcs=[ang3(P, Q, T, '38°', r=26, lr=43), ang3(R, S, T, '57°', r=17, lr=33), ang3(T, P, R, 'k°', r=13, lr=28)],
    pts=[lab(P, 'P', 90), lab(Q, 'Q', 90), lab(R, 'R', 270), lab(S, 'S', 270), lab(T, 'T', 0, d=15)],
    texts=[txt(pt(7.0, 4.0), 'ℓ', dx=11), txt(pt(7.0, 0.6), 'm', dx=11)])

# --- Step 4: squares on a leg and on the hypotenuse
P, Q, R = pt(0, 5), pt(0, 0), pt(7, 0)
FIGS['s4'] = dict(box=[-5, -0.9, 12, 12], w=320, h=262, pad=14, alt='right triangle PQR with the right angle at Q; a square of area 25 is built on leg PQ and a square of area 74 is built on hypotenuse PR',
    polys=[dict(pts=[Q, P, pt(-5, 5), pt(-5, 0)], cls='tile'), dict(pts=[P, R, pt(12, 7), pt(5, 12)], cls='tile'), dict(pts=[P, Q, R], cls='shade')],
    segs=[seg(P, Q), seg(Q, R), seg(P, R)],
    rights=[dict(at=Q, a=P, b=R, s=8)],
    pts=[lab(P, 'P', 118), lab(Q, 'Q', 250), lab(R, 'R', -60)],
    texts=[txt(pt(-2.5, 2.5), '25'), txt(pt(6, 6), '74')])

# --- Step 5: 30-60-90 with the long leg given
A, C, B = pt(0, 0), pt(12, 0), pt(12, 4 * math.sqrt(3))
FIGS['s5'] = dict(box=[-0.9, -1.3, 13, 7.5], w=340, h=225, alt='right triangle ABC with the right angle at C; the angle at A is 30 degrees and side AC is 12',
    segs=[seg(A, C), seg(C, B), seg(A, B)],
    rights=[dict(at=C, a=A, b=B)],
    arcs=[ang3(A, C, B, '30°', r=34, lr=52)],
    sides=[side(A, C, '12', -13)],
    pts=[lab(A, 'A', 200), lab(B, 'B', 60), lab(C, 'C', -40)])

# --- Step 6: a square and an equilateral triangle on one of its sides
P, Q, R, S = pt(0, 4), pt(4, 4), pt(4, 0), pt(0, 0); T = pt(4 + 2 * math.sqrt(3), 2)
FIGS['s6'] = dict(box=[-0.6, -0.6, 8.1, 4.6], w=340, h=215, alt='square PQRS with equilateral triangle QTR built on side QR; the diagonal PR of the square is dashed',
    segs=[seg(P, Q), seg(Q, R), seg(R, S), seg(S, P), seg(Q, T), seg(T, R), seg(P, R, 'dash')],
    pts=[lab(P, 'P', 135), lab(Q, 'Q', 90), lab(R, 'R', 270), lab(S, 'S', 225), lab(T, 'T', 0)])

# --- Step 8: three triangles with one height
P, Q, R, S, T = pt(3.6, 4.2), pt(0, 0), pt(10, 0), pt(5, 0), pt(7, 0)
FIGS['s8'] = dict(box=[-0.6, -0.8, 10.6, 4.8], w=340, h=200, alt='triangle PQR with points S and T on side QR, in that order from Q; segments PS and PT divide the triangle into three smaller triangles',
    segs=[seg(P, Q), seg(P, R), seg(Q, R), seg(P, S), seg(P, T)],
    pts=[lab(P, 'P', 90), lab(Q, 'Q', 210), lab(S, 'S', 270), lab(T, 'T', 270), lab(R, 'R', -30)])

# --- Step 9: pieces 25 and 144, drawn to scale (hypotenuse 169 shown as 10 units)
J, L, N, K = pt(0, 0), pt(10, 0), pt(250 / 169, 0), pt(250 / 169, 600 / 169)
FIGS['s9'] = dict(box=[-0.5, -1.0, 10.5, 4.0], w=350, h=200, alt='right triangle JKL with the right angle at K; the altitude KN meets hypotenuse JL at N; JN is 25 and NL is 144',
    segs=[seg(J, K), seg(K, L), seg(J, L), seg(K, N, 'thin')],
    rights=[dict(at=K, a=J, b=L), dict(at=N, a=K, b=L, s=8)],
    sides=[side(J, N, '25', -14, f=0.4), side(N, L, '144', -14)],
    pts=[lab(J, 'J', 180), lab(K, 'K', 90), lab(L, 'L', -20), lab(N, 'N', 270, dx=2, d=14)])

# --- Practice 1
P, Q, top, bot = transversal(56, 5.9, 4.2, 1.5)
FIGS['p1'] = dict(box=[0, 0, 10, 5.8], w=340, h=210, alt='parallel lines l and m crossed by line t; the angle above line l on the left of t is 124 degrees and the angle above line m on the right of t is x degrees',
    segs=[seg(pt(0.5, 4.2), pt(9.1, 4.2)), seg(pt(0.5, 1.5), pt(9.1, 1.5)), seg(bot, top)],
    arcs=[ang(P, 56, 180, '124°', r=13, lr=30), ang(Q, 0, 56, 'x°', r=18, lr=33)],
    texts=[txt(pt(9.1, 4.2), 'ℓ', dx=11), txt(pt(9.1, 1.5), 'm', dx=11), txt(top, 't', dx=11, dy=4)])

# --- Practice 4: angles 45 and 50, exterior 95 at A, drawn to scale
B, C = pt(0.8, 0.8), pt(7.0, 0.8); A = pol(B, 45, 6.2 * math.sin(math.radians(50)) / math.sin(math.radians(85))); E = pol(A, 45, 1.7)
FIGS['p4'] = dict(box=[0, 0, 8.6, 6.3], w=340, h=250, alt='triangle ABC with side BA extended past A to E; the angle at B is (x + 20) degrees, the angle at C is 2x degrees, and the exterior angle EAC is (4x minus 5) degrees',
    segs=[seg(B, E), seg(A, C), seg(B, C)],
    arcs=[ang3(B, C, A, '(x + 20)°', r=19, lr=58, dy=3), ang3(C, B, A, '2x°', r=17, lr=36), ang3(A, E, C, '(4x − 5)°', r=13, lr=50, dx=6)],
    pts=[lab(A, 'A', 135), lab(B, 'B', 200), lab(C, 'C', -30), lab(E, 'E', 45, d=11)])

# --- Practice 7: a bend between parallel lines (34, 47, x = 81)
A = pt(1.6, 4.2); B = pol(A, -34, (4.2 - 2.3) / math.sin(math.radians(34))); C = pol(B, 227, (2.3 - 0.7) / math.sin(math.radians(47)))
FIGS['p7'] = dict(box=[0, 0, 7.8, 5], w=340, h=220, alt='parallel lines l and m; segment AB leaves point A on line l at 34 degrees and segment CB leaves point C on line m at 47 degrees; they meet at point B between the lines, where the angle ABC is x degrees',
    segs=[seg(pt(0.5, 4.2), pt(7.0, 4.2)), seg(pt(0.5, 0.7), pt(7.0, 0.7)), seg(A, B), seg(B, C)],
    arcs=[ang3(A, pt(3, 4.2), B, '34°', r=28, lr=45), ang3(C, pt(5, 0.7), B, '47°', r=20, lr=36), ang3(B, A, C, 'x°', r=14, lr=28)],
    pts=[lab(A, 'A', 90), lab(B, 'B', 0), lab(C, 'C', 270)],
    texts=[txt(pt(7.0, 4.2), 'ℓ', dx=11), txt(pt(7.0, 0.7), 'm', dx=11)])

# --- Practice 8: two right triangles on one hypotenuse (7-24-25 and 15-20-25)
A, C, B, D = pt(0, 0), pt(25, 0), pt(7 * 7 / 25, -7 * 24 / 25), pt(15 * 15 / 25, 15 * 20 / 25); G = cen(A, B, C, D)
FIGS['p8'] = dict(box=[-1.6, -8.2, 26.6, 13.4], w=340, h=262, alt='quadrilateral ABCD with right angles at B and D and a dashed diagonal AC; AB is 7, BC is 24 and AD is 15',
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, A), seg(A, C, 'dash')],
    rights=[dict(at=B, a=A, b=C, s=8), dict(at=D, a=A, b=C, s=8)],
    sides=[side(A, B, '7', -13), side(B, C, '24', -13), side(A, D, '15', 13)],
    pts=[lab(A, 'A', 180), lab(B, 'B', 250), lab(C, 'C', 0), lab(D, 'D', 100)])

# --- Practice 9: a point on the diagonal of a rectangle
P, Q, R, S = pt(0, 4), pt(7, 4), pt(7, 0), pt(0, 0); T = mid(P, R, 0.4)
FIGS['p9'] = dict(box=[-0.6, -0.6, 7.6, 4.6], w=320, h=215, alt='rectangle PQRS with diagonal PR; point T is on the diagonal, closer to P, and segment ST is drawn; triangle PTS is shaded',
    polys=[dict(pts=[P, T, S], cls='shade')],
    segs=[seg(P, Q), seg(Q, R), seg(R, S), seg(S, P), seg(P, R), seg(S, T)],
    pts=[lab(P, 'P', 135), lab(Q, 'Q', 45), lab(R, 'R', -45), lab(S, 'S', 225), lab(T, 'T', 50)])

# --- Practice 10: a 120 degree central angle
O = pt(0, 0); P, Q = pol(O, 210, 3), pol(O, 330, 3)
FIGS['p10'] = dict(box=[-3.3, -3.3, 3.3, 3.3], w=250, h=250, pad=16, alt='a circle with center O; radii OP and OQ and chord PQ form a triangle; angle POQ is 120 degrees and the radius is 6',
    circles=[dict(c=O, r=3)],
    segs=[seg(O, P), seg(O, Q), seg(P, Q)],
    arcs=[ang3(O, P, Q, '120°', r=12, lr=29)],
    sides=[side(O, Q, '6', 12)],
    dots=[O],
    pts=[lab(O, 'O', 90), lab(P, 'P', 210), lab(Q, 'Q', 330)])

# --- Challenge 1: two transversals that are not marked parallel
S1, S2, st, sb = transversal(62, 3.3, 4.0, 1.2)
T1, T2, tt, tb = transversal(68, 7.5, 4.0, 1.2)
FIGS['c1'] = dict(box=[0, 0, 9.8, 5.4], w=340, h=232, note=NOTE, alt='parallel lines p and q crossed by lines s and t; on line s, w degrees is above p to the right of s and x degrees is above q to the left of s; on line t, y degrees is below p to the left of t and z degrees is above q to the right of t',
    segs=[seg(pt(0.5, 4.0), pt(9.0, 4.0)), seg(pt(0.5, 1.2), pt(9.0, 1.2)), seg(sb, st), seg(tb, tt)],
    arcs=[ang(S1, 0, 62, 'w°', r=0, lr=27), ang(S2, 62, 180, 'x°', r=0, lr=18), ang(T1, 180, 248, 'y°', r=0, lr=26), ang(T2, 0, 68, 'z°', r=0, lr=27)],
    texts=[txt(pt(9.0, 4.0), 'p', dx=11), txt(pt(9.0, 1.2), 'q', dx=11, dy=-2), txt(st, 's', dx=11, dy=4), txt(tt, 't', dx=11, dy=4)])

# --- Challenge 2: two isosceles triangles on a transversal (104, 76, 52), drawn to scale
Q = pt(3.3, 4.2); S = pol(Q, -76, 3.6 / math.sin(math.radians(76))); R = pol(Q, -76, 2.1)
SR = math.hypot(S[0] - R[0], S[1] - R[1]); P = pt(Q[0] - 2.1, 4.2); T = pt(S[0] - SR, 0.6)
FIGS['c2'] = dict(box=[0.2, 0, 6.6, 4.9], w=340, h=262, alt='parallel lines l and m; P and Q are on l, S and T are on m, and R is on segment QS; tick marks show PQ = QR and SR = ST; segments PR and RT are drawn and angle PQR is 104 degrees',
    segs=[seg(pt(0.5, 4.2), pt(6.0, 4.2)), seg(pt(0.5, 0.6), pt(6.0, 0.6)), seg(Q, S), seg(P, R), seg(R, T)],
    ticks=[dict(a=P, b=Q, n=1), dict(a=Q, b=R, n=1), dict(a=R, b=S, n=2), dict(a=S, b=T, n=2)],
    arcs=[ang3(Q, P, R, '104°', r=12, lr=27)],
    pts=[lab(P, 'P', 90), lab(Q, 'Q', 75), lab(R, 'R', 0, d=14), lab(S, 'S', 285), lab(T, 'T', 250)],
    texts=[txt(pt(6.0, 4.2), 'ℓ', dx=11), txt(pt(6.0, 0.6), 'm', dx=11)])

# --- Challenge 3: a rectangle with a 30 degree roof
A, B, C, E = pt(0, 0), pt(12, 0), pt(12, 5), pt(0, 5); D = pt(6, 5 + 2 * math.sqrt(3))
FIGS['c3'] = dict(box=[-1.5, -1.4, 13.5, 9.4], w=340, h=262, alt='pentagon ABCDE: rectangle ABCE with AB equal to 12 and BC equal to 5, topped by triangle CDE; the dashed segment EC is the top of the rectangle, and the angles DEC and DCE are each 30 degrees',
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, E), seg(E, A), seg(E, C, 'dash')],
    arcs=[ang3(E, C, D, '30°', r=30, lr=48), ang3(C, D, E, '30°', r=30, lr=48)],
    sides=[side(A, B, '12', -13), side(B, C, '5', -12)],
    pts=[lab(A, 'A', 225), lab(B, 'B', -45), lab(C, 'C', 0), lab(D, 'D', 90), lab(E, 'E', 180)])

# --- Challenge 4: one diagonal, two triangles (drawn with KM = 12)
K, M = pt(0, 0), pt(12, 0)
jx = (25 - 81 + 144) / 24; J = pt(jx, math.sqrt(25 - jx * jx)); lx = (36 - 144 + 144) / 24; L = pt(lx, -math.sqrt(36 - lx * lx)); G = cen(J, K, L, M)
FIGS['c4'] = dict(box=[-1.1, -6.6, 13.1, 4.3], w=330, h=290, note=NOTE, alt='quadrilateral JKLM with a dashed diagonal KM; JK is 5, JM is 9, KL is 6 and LM is 12',
    segs=[seg(J, K), seg(J, M), seg(K, L), seg(L, M), seg(K, M, 'dash')],
    sides=[side(K, J, '5', 13), side(J, M, '9', 13), side(K, L, '6', -13), side(L, M, '12', -13)],
    pts=[lab(J, 'J', 100), lab(K, 'K', 180), lab(L, 'L', 255), lab(M, 'M', 0)])

# --- Challenge 5: a height inside a rectangle (PQ = 12, QR = 4 root 3, QT = 6), drawn to scale
P, Q, R, S = pt(0, 0), pt(12, 0), pt(12, 4 * math.sqrt(3)), pt(0, 4 * math.sqrt(3)); T = pol(P, 30, 12 * math.cos(math.radians(30)))
FIGS['c5'] = dict(box=[-0.9, -0.9, 12.9, 7.8], w=340, h=235, alt='rectangle PQRS with diagonal PR; segment QT is perpendicular to the diagonal at T; QT is 6 and angle PQT is 60 degrees',
    segs=[seg(P, Q), seg(Q, R), seg(R, S), seg(S, P), seg(P, R), seg(Q, T)],
    rights=[dict(at=T, a=Q, b=P, s=8)],
    arcs=[ang3(Q, P, T, '60°', r=20, lr=36)],
    sides=[side(Q, T, '6', -11)],
    pts=[lab(P, 'P', 225), lab(Q, 'Q', -45), lab(R, 'R', 45), lab(S, 'S', 135), lab(T, 'T', 100, d=14)])

# --- Challenge 6: a leg and the piece beside it
F, H, K, G = pt(0, 0), pt(16, 0), pt(9, 0), pt(9, math.sqrt(63))
FIGS['c6'] = dict(box=[-0.9, -1.4, 16.9, 8.7], w=340, h=225, alt='right triangle FGH with the right angle at G; the altitude GK meets hypotenuse FH at K; FG is 12 and FK is 9',
    segs=[seg(F, G), seg(G, H), seg(F, H), seg(G, K, 'thin')],
    rights=[dict(at=G, a=F, b=H), dict(at=K, a=G, b=H, s=8)],
    sides=[side(F, G, '12', 13), side(F, K, '9', -13)],
    pts=[lab(F, 'F', 200), lab(G, 'G', 90), lab(H, 'H', -20), lab(K, 'K', 270, dx=13, dy=-1)])

# --- Challenge 8: semicircles on the three sides (legs 2 and 3)
A, B, C = pt(0, 2), pt(0, 0), pt(3, 0)
FIGS['c8'] = dict(box=[-1.25, -1.75, 3.55, 3.05], w=300, h=300, pad=14, alt='right triangle ABC with the right angle at B and a semicircle built on each side; the semicircle on hypotenuse AC is labeled 78 and the semicircle on leg BC is labeled with a question mark',
    semis=[dict(a=B, b=A), dict(a=C, b=B), dict(a=A, b=C)],
    polys=[dict(pts=[A, B, C], cls='shade')],
    segs=[seg(A, B), seg(B, C), seg(A, C)],
    rights=[dict(at=B, a=A, b=C, s=8)],
    pts=[lab(A, 'A', 100, d=13), lab(B, 'B', 225, d=14), lab(C, 'C', -15, d=14)],
    texts=[txt(pt(1.95, 1.68), '78'), txt(pt(1.5, -0.68), '?')])

GEO_JS = r'''
/* Geometry figures: no axes, equal scale. Points are [x, y] with y up; `box` is [xmin, ymin, xmax, ymax]. */
function geoSVG(o) {
    var w = o.w || 300, h = o.h || 200, pad = o.pad == null ? 22 : o.pad, B = o.box, noteH = o.note ? 22 : 0;
    var sc = Math.min((w - 2 * pad) / (B[2] - B[0]), (h - noteH - 2 * pad) / (B[3] - B[1]));
    var ox = (w - sc * (B[2] - B[0])) / 2, oy = (h - noteH - sc * (B[3] - B[1])) / 2;
    function X(x) { return ox + (x - B[0]) * sc; }
    function Y(y) { return h - noteH - oy - (y - B[1]) * sc; }
    function P(p) { return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }
    function U(a, b) { var dx = b[0] - a[0], dy = b[1] - a[1], L = Math.sqrt(dx * dx + dy * dy) || 1; return [dx / L, dy / L]; }
    function T(x, y, t, c, anc) {
        var k = c || (/[A-Za-zℓ]/.test(t) ? 'g it' : 'g');
        return '<text class="' + k + '" text-anchor="' + (anc || 'middle') + '" x="' + x.toFixed(1) + '" y="' + (y + 5).toFixed(1) + '">' + t + '</text>';
    }
    var s = '<svg class="fig" viewBox="0 0 ' + w + ' ' + h + '" width="' + w + '" height="' + h + '" role="img" aria-label="' + (o.alt || 'geometry figure') + '">';
    (o.semis || []).forEach(function(m) {       // a semicircle on diameter a-b, on the left of a->b
        var r = Math.sqrt(Math.pow(X(m.b[0]) - X(m.a[0]), 2) + Math.pow(Y(m.b[1]) - Y(m.a[1]), 2)) / 2;
        s += '<path class="' + (m.cls || 'tile') + '" d="M' + P(m.a) + ' A' + r.toFixed(1) + ',' + r.toFixed(1) + ' 0 0 1 ' + P(m.b) + ' Z"/>';
    });
    (o.polys || []).forEach(function(pl) { s += '<polygon class="' + (pl.cls || 'shade') + '" points="' + pl.pts.map(P).join(' ') + '"/>'; });
    (o.circles || []).forEach(function(c) { s += '<circle class="circ" cx="' + X(c.c[0]).toFixed(1) + '" cy="' + Y(c.c[1]).toFixed(1) + '" r="' + (c.r * sc).toFixed(1) + '"/>'; });
    (o.segs || []).forEach(function(g) { s += '<line class="' + (g.cls || 'ln') + '" x1="' + X(g.a[0]).toFixed(1) + '" y1="' + Y(g.a[1]).toFixed(1) + '" x2="' + X(g.b[0]).toFixed(1) + '" y2="' + Y(g.b[1]).toFixed(1) + '"/>'; });
    (o.rights || []).forEach(function(q) {      // right-angle mark at q.at, opening toward the points q.a and q.b
        var k = q.s || 9, u = U(q.at, q.a), v = U(q.at, q.b), px = X(q.at[0]), py = Y(q.at[1]);
        s += '<path class="sq" d="M' + (px + u[0] * k).toFixed(1) + ',' + (py - u[1] * k).toFixed(1) + ' L' + (px + (u[0] + v[0]) * k).toFixed(1) + ',' + (py - (u[1] + v[1]) * k).toFixed(1) + ' L' + (px + v[0] * k).toFixed(1) + ',' + (py - v[1] * k).toFixed(1) + '"/>';
    });
    (o.arcs || []).forEach(function(c) {        // the angle at c.at between the rays toward c.a and c.b: an arc (r > 0) and a label on the bisector
        var a1 = Math.atan2(c.a[1] - c.at[1], c.a[0] - c.at[0]), a2 = Math.atan2(c.b[1] - c.at[1], c.b[0] - c.at[0]);
        var d = a2 - a1; while (d > Math.PI) d -= 2 * Math.PI; while (d <= -Math.PI) d += 2 * Math.PI;
        var px = X(c.at[0]), py = Y(c.at[1]), r = c.r == null ? 15 : c.r, am = a1 + d / 2;
        if (r > 0) s += '<path class="arc" d="M' + (px + r * Math.cos(a1)).toFixed(1) + ',' + (py - r * Math.sin(a1)).toFixed(1) + ' A' + r + ',' + r + ' 0 0 ' + (d > 0 ? 0 : 1) + ' ' + (px + r * Math.cos(a2)).toFixed(1) + ',' + (py - r * Math.sin(a2)).toFixed(1) + '"/>';
        if (c.t) { var lr = c.lr == null ? r + 14 : c.lr; s += T(px + lr * Math.cos(am) + (c.dx || 0), py - lr * Math.sin(am) + (c.dy || 0), c.t, c.cls); }
    });
    (o.ticks || []).forEach(function(k) {       // n short marks across the middle of segment a-b (equal lengths)
        var u = U(k.a, k.b), mx = (X(k.a[0]) + X(k.b[0])) / 2, my = (Y(k.a[1]) + Y(k.b[1])) / 2, n = k.n || 1;
        for (var i = 0; i < n; i++) {
            var off = (i - (n - 1) / 2) * 4, cx = mx + u[0] * off, cy = my - u[1] * off;
            s += '<line class="tick" x1="' + (cx - u[1] * 5).toFixed(1) + '" y1="' + (cy - u[0] * 5).toFixed(1) + '" x2="' + (cx + u[1] * 5).toFixed(1) + '" y2="' + (cy + u[0] * 5).toFixed(1) + '"/>';
        }
    });
    (o.sides || []).forEach(function(l) {       // a label beside segment a-b; off > 0 puts it on the left of a->b
        var u = U(l.a, l.b), off = l.off == null ? 13 : l.off, f = l.f == null ? 0.5 : l.f;
        s += T(X(l.a[0] + (l.b[0] - l.a[0]) * f) - u[1] * off + (l.dx || 0), Y(l.a[1] + (l.b[1] - l.a[1]) * f) - u[0] * off + (l.dy || 0), l.t, l.cls);
    });
    (o.dots || []).forEach(function(p) { s += '<circle class="pt" cx="' + X(p[0]).toFixed(1) + '" cy="' + Y(p[1]).toFixed(1) + '" r="3"/>'; });
    (o.pts || []).forEach(function(p) {         // a letter beside the point p.p: in direction p.dir (degrees), or pushed away from the point p.away
        var u = p.away ? U(p.away, p.p) : [Math.cos((p.dir || 0) * Math.PI / 180), Math.sin((p.dir || 0) * Math.PI / 180)], d = p.d == null ? 13 : p.d;
        s += T(X(p.p[0]) + u[0] * d + (p.dx || 0), Y(p.p[1]) - u[1] * d + (p.dy || 0), p.t, p.cls);
    });
    (o.texts || []).forEach(function(t) { s += T(X(t.at[0]) + (t.dx || 0), Y(t.at[1]) + (t.dy || 0), t.t, t.cls, t.anc); });
    if (o.note) s += '<text class="note" text-anchor="middle" x="' + (w / 2) + '" y="' + (h - 8) + '">' + o.note + '</text>';
    return s + '</svg>';
}
function fig(name) { var f = FIGS[name]; return f ? (f.box ? geoSVG(f) : graphSVG(f)) : ''; }'''

FIGS_JS = 'var FIGS = {\n' + ',\n'.join('    ' + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in FIGS.items()) + '\n};' + GEO_JS

# geometry classes on top of the shell's figure styles; the fig-row rules match sheet 3
FIG_RULES = [
    ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }",
    ".fig text.g { font-size: 15px; }",
    ".fig .thin { stroke: #21442B; stroke-width: 1.3; fill: none; }",
    ".fig .arc { stroke: #BC6C26; stroke-width: 1.4; fill: none; }",
    ".fig .tick { stroke: #21442B; stroke-width: 1.5; }",
    ".fig .circ { fill: none; stroke: #21442B; stroke-width: 2; }",
    ".fig .shade2 { fill: rgba(57,134,78,0.16); stroke: none; }",
    ".fig .tile { fill: rgba(221,162,94,0.12); stroke: #21442B; stroke-width: 1.4; }",
    ".fig text.note { font-family: 'Inter', sans-serif; font-size: 11.5px; font-style: normal; fill: #5A5A5A; }",
]
FIG_CSS = '\n'.join(FIG_RULES) + r'''
.fig-row { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: flex-start; justify-content: center; margin: 4px 0 10px; }
.fig-row .fig { margin: 4px 0; }
.ref-page .fig-row { margin-left: 24px; }
@media (max-width: 768px) { .ref-page .fig-row { margin-left: 0; } }'''
# the same figure styles, on one line, for the downloaded results report (which has its own style block)
REPORT_FIG_CSS = (".fig{display:block;margin:4px 0 10px;max-width:100%;height:auto}.fig .ln{stroke:#21442B;stroke-width:2;fill:none}"
                  ".fig .dash{stroke:#8B6914;stroke-width:1.4;stroke-dasharray:5 4;fill:none}.fig .pt{fill:#21442B}.fig .shade{fill:rgba(221,162,94,0.25);stroke:none}"
                  ".fig text{font-family:\"Times New Roman\",Georgia,serif;font-size:13px;fill:#2D2D2D}.fig text.it{font-style:italic}" +
                  ''.join(re.sub(r'\s*([{};:,])\s*', r'\1', r).replace(';}', '}') for r in FIG_RULES))


def _clean(o):
    """Content strings may arrive with backslash+quote from r-strings; drop the backslash."""
    if isinstance(o, str): return o.replace('\\"', '"')
    if isinstance(o, list): return [_clean(v) for v in o]
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    return o

def js_data(name, data):
    return 'var ' + name + ' = ' + json.dumps(_clean(nw_all(data)), ensure_ascii=False).replace('</', '<\\/') + ';\n'

def sub1(src, pattern, repl, flags=0, count=1):
    new, n = re.subn(pattern, (repl if callable(repl) else (lambda m: repl)), src, count=count, flags=flags)
    if n != count:
        sys.exit('pattern not found (%d of %d): %r' % (n, count, pattern[:80]))
    return new

def replace_once(src, old, new):
    if src.count(old) != 1:
        sys.exit('expected exactly one occurrence (%d): %r' % (src.count(old), old[:100]))
    return src.replace(old, new)

def replace_n(src, old, new, n):
    if src.count(old) != n:
        sys.exit('expected %d occurrences (%d): %r' % (n, src.count(old), old[:100]))
    return src.replace(old, new)


def build(out=OUT):
    html = open(SRC, encoding='utf-8').read()
    html = re.sub(r'\s*<p style="font-size:14px; margin-top:10px;">Ready for the next topic\?.*?</p>', '', html, flags=re.S)

    # --- header / titles / footer
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Triangles</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Triangles</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; TRIANGLES')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Triangles')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Triangle Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Triangle rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>a figure tells you more than it states.</strong> Parallel lines give you equal angles, a right angle gives you the Pythagorean theorem, and a $30^\circ$, $45^\circ$ or $60^\circ$ angle gives you a side ratio. Each question asks you to notice which of these the figure contains, then use it.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. Sketch a quick figure when a question does not give one. Enter angle measures as numbers, without the degree symbol.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and six include a figure. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type, then mark what you know on the figure, or sketch one if none is given. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. For these questions it works mostly as a calculator, for example to square, add and take a square root in one line. When the choices contain radicals such as $7\sqrt{3}$, an exact answer from the side ratios is usually quicker than a decimal.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These eight questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each is a rule you already have, paired with a second idea (two transversals in place of one, isosceles triangles attached to parallel lines, a roof on a rectangle, a diagonal shared by two triangles, a height drawn inside a rectangle, a leg and the piece of the hypotenuse beside it, a sum of two legs, shapes built on the three sides). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the ones marked <em>extra</em> lean on the unstarred rules. One is tagged <em>algebra blend</em>: that pairing appears less often, so treat it as stretch practice.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time a triangle shows up. Make it an if-then. (Shape: “When a right triangle has a $30^\circ$ or $60^\circ$ angle, I ______ before I compute anything.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">For skill-by-skill practice, <strong>Khan Academy\'s Official Digital SAT Prep</strong> sorts questions by topic: the lessons on <em>congruence, similarity, and angle relationships</em> and on <em>right triangle trigonometry</em> are good places to practice this sheet\'s starred rules. <a href="https://www.khanacademy.org/digital-sat" ' + A_STYLE + '>Open Khan Academy &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">The equations these figures lead to are usually linear. The earlier sheets in the series cover that algebra: <a href="' + LINEAR_URL + '" ' + A_STYLE + '>SAT Math 1: Linear Equations &#8594;</a>, <a href="' + QUAD_URL + '" ' + A_STYLE + '>SAT Math 2: Quadratics &#8594;</a> and <a href="' + FUNC_URL + '" ' + A_STYLE + '>SAT Math 3: Functions &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, and for a copy of the Bluebook reference sheet with the triangle formulas, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For similar triangles, and how lengths and areas scale, see the companion sheet <a href="' + SIM_URL + '" ' + A_STYLE + '>SAT Math 4C: Similar Figures &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">Ready for the next topic? Continue the series with <a href="' + RATIOS_URL + '" ' + A_STYLE + '>SAT Math 5: Ratios, Rates and Proportions &#8594;</a></p>',
        flags=re.S)

    # --- data arrays
    for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
        html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

    # --- figures: FIGS, the geometry renderer and fig(); the shell's graphSVG stays for any coordinate figure
    start = html.index('var FIGS = {')
    tail = "function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }"
    end = html.index(tail) + len(tail)
    html = html[:start] + FIGS_JS + html[end:]
    html = replace_once(html, ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }", FIG_CSS)

    # --- results kit: carry each question's figure into the tutor report (most of these questions depend on one)
    html = replace_n(html, "stem: p.stem, trap: p.trap });", "stem: p.stem, fig: p.fig ? fig(p.fig) : '', trap: p.trap });", 2)
    html = replace_once(html, """'</b></span></div><div class="stem">' + r.i.stem + '</div>""", """'</b></span></div><div class="stem">' + (r.i.fig || '') + r.i.stem + '</div>""")
    html = replace_once(html, "'.nw{white-space:nowrap}table.vtab{", "'" + REPORT_FIG_CSS.replace('\\', '\\\\').replace("'", "\\'") + "' +\n        '.nw{white-space:nowrap}table.vtab{")

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', 'sat-triangles-sheet:rule')
    html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                        "(i === %d ? 'That was the last starred step. The next three cover rules that come up less often.' : '')" % LAST_STARRED_STEP_INDEX)
    html = replace_once(html, "Step 1 of 9", "Step 1 of %d" % len(STEPS))

    # --- LCC voice pass: visible shell and results-kit copy (the last entry renames a column for the Desmos sheets only)
    html = voice.apply(html, voice.SHELL[:-1], 'shell')

    dash = chr(8212)                                  # the em dash, written this way so this file contains none
    if dash in html:
        i = html.index(dash)
        sys.exit('em dash found: ' + html[max(0, i - 80):i + 40])
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out, len(html), 'bytes;', len(STEPS), 'steps,', sum(len(s['items']) for s in FLUENCY), 'skill practice,',
          len(GAUNTLET), 'practice,', len(CHALLENGE), 'challenge,', len(EXIT), 'exit,', len(FIGS), 'figures')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else OUT)
