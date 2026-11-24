#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-4C-Similar-Figures.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the content
swaps. This sheet is a companion to SAT Math 4: Triangles. It covers similar figures: matching sides
and the scale factor, the similar triangles that parallel lines create, and how the scale factor
acts on lengths (k), areas (k squared) and volumes (k cubed). Source: Tip 28 of the class book, as
question types only. All questions use original numbers and figures.

It was copied from build_special_right_triangles.py and keeps that file's geoSVG figure renderer,
with one addition: a `regions` key that shades a circle with circular holes (a ring, or the space
around circles inside a larger circle). nested() and bowtie() draw the two parallel-line pictures.
Answer key: verify_similar_figures.py (same folder) recomputes every answer."""
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
OUT = ROOT + '/test-prep/sat/SAT-Math-4C-Similar-Figures.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
TRI_URL = SITE + 'test-prep/sat/SAT-Math-4-Triangles.html'
RATIOS_URL = SITE + 'test-prep/sat/SAT-Math-5-Ratios-Rates-Proportions.html'
DESMOS1_URL = SITE + 'test-prep/sat/SAT-Desmos-1-Core-Moves.html'
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
<p class="ref-intro">Two figures are similar when one is a scaled copy of the other: the same shape at a different size. Matching angles are equal, and every pair of matching lengths has the same ratio, called the scale factor. This sheet has two goals. The first is to match the parts correctly and set up the proportion. The second is to know what the scale factor does to lengths, areas and volumes. As you practice, start by identifying which figures are similar and which parts match. Then decide whether the question is about a length, an area or a volume, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''' + rule(1, 'Matching sides and the scale factor', True, r'''
<p class="ref-lead">Similar figures have equal matching angles and proportional matching sides. The similarity statement tells you which parts match: in $\triangle ABC \sim \triangle DEF$, vertex $A$ matches $D$, $B$ matches $E$, and $C$ matches $F$. Divide a length in one figure by the matching length in the other to get the scale factor $k$.</p>
''' + figslot('r_sim') + r'''<div class="fbox">
''' + frow('the proportion', r'$\dfrac{AB}{DE} = \dfrac{BC}{EF} = \dfrac{AC}{DF}$') +
      frow('scale factor', r'$k = \dfrac{\text{a length in the second figure}}{\text{the matching length in the first figure}}$') +
      frow('a missing side', r'multiply its matching side by $k$, or solve the proportion') +
      frow('two angles are enough', r'if two angles of one triangle equal two angles of another, the triangles are similar') + r'''</div>
''' + ex('A', r'In the figure, $\overline{AB}$ matches $\overline{DE}$, so $k = \dfrac{12}{8} = 1.5$. The other sides follow: $EF = 1.5 \cdot 10 = 15$ and $DF = 1.5 \cdot 12 = 18$.') +
    ex('B', r'A triangle has sides of $9$, $12$ and $18$. A similar triangle has a shortest side of $6$. The scale factor is $\dfrac{6}{9} = \dfrac{2}{3}$, so its other sides are $8$ and $12$.') +
    note(r'Match sides by the order of the letters, or by the angle each side is across from, not by where they sit on the page. One of the figures may be turned or flipped.')) + \
rule(2, 'Parallel lines make similar triangles', True, r'''
<p class="ref-lead">Parallel lines create equal angles, and two pairs of equal angles make two triangles similar. Two pictures come up most often. In the nested picture, a segment parallel to one side cuts off a smaller triangle that shares an angle with the whole triangle. In the bowtie picture, two segments cross between parallel lines.</p>
<div class="fig-row">''' + figslot('r_nest').strip('\n') + figslot('r_bow').strip('\n') + r'''</div>
<div class="fbox">
''' + frow('nested', r'if $\overline{DE} \parallel \overline{BC}$, then $\triangle ADE \sim \triangle ABC$ and $\dfrac{AD}{AB} = \dfrac{AE}{AC} = \dfrac{DE}{BC}$') +
      frow('use the whole side', r'the side of the large triangle is $AB = AD + DB$, not $DB$') +
      frow('bowtie', r'if $\overline{PQ} \parallel \overline{RS}$ and the segments cross at $M$, then $\triangle PQM \sim \triangle SRM$ and $\dfrac{PQ}{SR} = \dfrac{PM}{SM} = \dfrac{QM}{RM}$') +
      frow('which vertices match', r'$P$ matches $S$, and $Q$ matches $R$: matching vertices sit at opposite ends of each crossing segment') +
      frow('right triangles', r'two right triangles that share an acute angle are similar') + r'''</div>
''' + ex('A', r'In $\triangle ABC$, $\overline{DE} \parallel \overline{BC}$, $AD = 6$, $DB = 3$ and $BC = 12$. The whole side is $AB = 9$, so $\dfrac{DE}{12} = \dfrac{6}{9}$ and $DE = 8$.') +
    ex('B', r'Segments $\overline{PS}$ and $\overline{QR}$ cross at $M$, with $\overline{PQ} \parallel \overline{RS}$. If $PQ = 4$, $RS = 10$ and $PM = 6$, then $\dfrac{SM}{6} = \dfrac{10}{4}$ and $SM = 15$.') +
    note(r'The equal angles come from the parallel lines: corresponding angles in the nested picture, alternate interior angles and vertical angles in the bowtie. For a review of those angle facts, see <a href="' + TRI_URL + r'" target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;">SAT Math 4: Triangles</a>.')) + \
rule(3, r'Every length scales by $k$', True, r'''
<p class="ref-lead">The scale factor applies to every length in the figure, not only to the sides. Heights, diagonals, radii and perimeters all grow or shrink by the same factor $k$. Angles do not change.</p>
<div class="fbox">
''' + frow('perimeters', r'$\dfrac{\text{perimeter of the second figure}}{\text{perimeter of the first figure}} = k$') +
      frow('heights and diagonals', r'matching heights, medians and diagonals have the ratio $k$') +
      frow('circles', r'any two circles are similar: radius, diameter and circumference share one ratio') +
      frow('angles', r'matching angles stay equal: they are not multiplied by $k$') + r'''</div>
''' + ex('A', r'Two similar triangles have a pair of matching sides of $6$ and $10$, so $k = \dfrac{10}{6} = \dfrac{5}{3}$. If the smaller triangle has a perimeter of $24$, the larger has a perimeter of $24 \cdot \dfrac{5}{3} = 40$.') +
    ex('B', r'Circles with radii of $4$ and $10$ have circumferences of $8\pi$ and $20\pi$. Both ratios reduce to $2 : 5$.') +
    ex('C', r'A $5$ by $12$ rectangle has a diagonal of $13$. A similar rectangle with a diagonal of $39$ has $k = 3$, so its sides are $15$ and $36$.') +
    note(r'A ratio of any two matching lengths is the scale factor. If the perimeters are in the ratio $3 : 4$, each pair of matching sides is in the ratio $3 : 4$ too.')) + \
rule(4, r'Areas scale by $k^2$', True, r'''
<p class="ref-lead">An area is built from two lengths multiplied together, and each one is multiplied by $k$. So areas are multiplied by $k^2$. If matching lengths are in the ratio $a : b$, the areas are in the ratio $a^2 : b^2$.</p>
''' + figslot('r_sq') + r'''<div class="fbox">
''' + frow('the rule', r'$\dfrac{\text{area of the second figure}}{\text{area of the first figure}} = k^2$') +
      frow('as a ratio', r'lengths $a : b$ &nbsp;give&nbsp; areas $a^2 : b^2$') +
      frow('why it works', r'for a triangle, $\tfrac{1}{2}(kb)(kh) = k^2 \cdot \tfrac{1}{2}bh$') +
      frow('going back', r'take a square root: areas in the ratio $16 : 25$ mean lengths in the ratio $4 : 5$') +
      frow('circles', r'the ratio of the areas is the square of the ratio of the radii') + r'''</div>
''' + ex('A', r'Two similar triangles have matching sides in the ratio $2 : 5$. If the smaller has an area of $12$, the larger has an area of $12 \cdot \dfrac{25}{4} = 75$.') +
    ex('B', r'The circumferences of two circles are in the ratio $3 : 4$, so their areas are in the ratio $9 : 16$. If the smaller circle has an area of $54$, the larger has an area of $54 \cdot \dfrac{16}{9} = 96$.') +
    ex('C', r'Two similar pentagons have areas of $49$ and $100$, so their matching sides are in the ratio $7 : 10$. If a side of the smaller pentagon is $21$, the matching side of the larger is $30$.') +
    note(r'Decide what kind of quantity each number is before you set up a ratio. A ratio of sides, perimeters or radii is $k$. A ratio of areas is $k^2$.')) + \
rule(5, 'Regions between similar figures', False, r'''
<p class="ref-lead">When one figure sits inside a similar one, the region between them is the larger area minus the smaller area. Write each area as a number of equal parts using the squared ratio, subtract the parts, and then find the size of one part.</p>
<div class="fig-row">''' + figslot('r_ring').strip('\n') + figslot('r_slice').strip('\n') + r'''</div>
<div class="fbox">
''' + frow('a ring', r'radii $a : b$ &nbsp;give&nbsp; circle areas of $a^2$ and $b^2$ parts, so the ring is $b^2 - a^2$ parts') +
      frow('a slice of a triangle', r'matching sides $a : b$ &nbsp;give&nbsp; triangle areas of $a^2$ and $b^2$ parts, so the slice is $b^2 - a^2$ parts') +
      frow('one part', r'divide a known area by its number of parts') +
      frow('ratios along one side', r'measure both triangles from the vertex they share before you square') +
      frow('tangent circles', r'when circles sit in a row along a diameter of a larger circle, their diameters add up to the large diameter') + r'''</div>
''' + ex('A', r'Two circles have the same center, and the radius of the larger is $\dfrac{4}{3}$ times the radius of the smaller. The radii are in the ratio $3 : 4$, so the areas are $9$ parts and $16$ parts, and the ring is $7$ parts. If the smaller circle has an area of $18$, one part is $2$ and the ring has an area of $14$.') +
    ex('B', r'In $\triangle ABC$, $\overline{DE} \parallel \overline{BC}$ and $AD : DB = 1 : 2$. Measured from $A$, the matching sides are $AD : AB = 1 : 3$, so the areas are $1$ part and $9$ parts. Quadrilateral $DBCE$ is $8$ parts. If its area is $88$, one part is $11$ and $\triangle ABC$ has an area of $99$.') +
    note(r'Square first, then subtract. For radii in the ratio $3 : 4$, the ring is $16 - 9 = 7$ parts, not $(4 - 3)^2 = 1$ part.')) + \
rule(6, r'Volumes scale by $k^3$', False, r'''
<p class="ref-lead">A volume is built from three lengths, so volumes are multiplied by $k^3$. A surface area is still an area, so it is multiplied by $k^2$.</p>
''' + figslot('r_cubes') + r'''<div class="tbl-wrap"><table class="cases"><thead><tr><th>Quantity</th><th>Multiplied by</th><th>With $k = 3$</th></tr></thead><tbody>
<tr><td class="fname">lengths (edges, heights, radii)</td><td>$k$</td><td>$3$</td></tr>
<tr><td class="fname">areas (faces, surface area)</td><td>$k^2$</td><td>$9$</td></tr>
<tr><td class="fname">volumes</td><td>$k^3$</td><td>$27$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('as a ratio', r'lengths $a : b$ &nbsp;give&nbsp; volumes $a^3 : b^3$') +
      frow('going back', r'take a cube root: volumes in the ratio $8 : 125$ mean lengths in the ratio $2 : 5$') + r'''</div>
''' + ex('A', r'Two similar cylinders have heights of $4$ and $6$, so $k = \dfrac{3}{2}$ and $k^3 = \dfrac{27}{8}$. If the smaller holds $40$ cubic inches, the larger holds $40 \cdot \dfrac{27}{8} = 135$ cubic inches.') +
    ex('B', r'Two similar cones have volumes in the ratio $8 : 125$. Their heights are in the ratio $2 : 5$, and their surface areas are in the ratio $4 : 25$.') +
    note(r'A scale model works the same way. If each length of the model is $\dfrac{1}{10}$ of the original, its volume is $\dfrac{1}{1{,}000}$ of the original.')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common setup and interpretation mistakes. Review them so you know what to check when an answer seems off.</p>
''' + mistake(1, 'matching sides by where they sit on the page', r'A side matches the side across from the equal angle, which is not necessarily the side in the same position on the page. Use the order of the letters in the similarity statement, or mark the equal angles first.') + \
      mistake(2, 'using a piece of a side where the whole side belongs', r'In the nested picture with $AD = 6$ and $DB = 3$, the triangles compare $AD$ with $AB = 9$. The ratio $\dfrac{6}{3}$ compares two pieces of one side, and it is not the scale factor.') + \
      mistake(3, 'adding where you should multiply', r'If matching sides are $8$ and $12$, a side of $10$ does not match $10 + 4 = 14$. Similar figures keep ratios equal, so it matches $10 \cdot 1.5 = 15$.') + \
      mistake(4, 'flipping the ratio', r'Decide first whether the answer should be larger or smaller than the number you start with. If the result moves the other way, the scale factor is upside down.') + \
      mistake(5, r'scaling an area by $k$', r'If each side of a figure is doubled, an area of $10$ does not become $20$. Areas use the squared ratio: $10 \cdot 2^2 = 40$.') + \
      mistake(6, 'using an area ratio on a length', r'If two areas are in the ratio $16 : 25$, the perimeters are not in that ratio. Take the square root first: lengths are in the ratio $4 : 5$.') + \
      mistake(7, 'subtracting before squaring', r'For a ring whose radii are in the ratio $2 : 5$, the areas are $4$ parts and $25$ parts, so the ring is $21$ parts. Computing $(5 - 2)^2 = 9$ gives a different number.') + \
      mistake(8, 'answering for a different figure', r'After you find one part or one area, reread the question. It may ask for the larger figure, the smaller figure, or the region between them.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Matching sides and the scale factor",
  "rule": r"$\triangle ABC \sim \triangle DEF$ &nbsp;·&nbsp; $\dfrac{AB}{DE} = \dfrac{BC}{EF} = \dfrac{AC}{DF}$ &nbsp;·&nbsp; one scale factor $k$ for all three",
  "say": r"Read the similarity statement in order: first letter with first letter, second with second, third with third. Find one pair of matching sides where you know both lengths. Their ratio is the scale factor, and it carries each of the other sides across.",
  "fig": "s1",
  "prob": r"In the figure above, triangle $ABC$ is similar to triangle $DEF$, where $A$, $B$ and $C$ correspond to $D$, $E$ and $F$. If $AB = 10$, $BC = 14$ and $DE = 15$, what is the length of $\overline{EF}$?",
  "sol": r"<strong>Step 1: match the sides.</strong> $\overline{AB}$ matches $\overline{DE}$, and $\overline{BC}$ matches $\overline{EF}$.<br><strong>Step 2: find the scale factor.</strong> $k = \dfrac{DE}{AB} = \dfrac{15}{10} = 1.5$.<br><strong>Step 3: scale the side you need.</strong> $EF = 1.5 \cdot 14 = 21$.<br><strong>Check:</strong> $\dfrac{10}{15}$ and $\dfrac{14}{21}$ both reduce to $\dfrac{2}{3}$. ✓",
  "trap": r"Adding where the figure calls for multiplying. $\overline{DE}$ is $5$ longer than $\overline{AB}$, but $EF$ is not $14 + 5 = 19$. Similar figures keep ratios equal, not differences.",
  "micro": {"q": r"Triangle $JKL$ is similar to triangle $MNP$, in that order. If $JK = 8$, $MN = 20$ and $KL = 12$, then $NP =$", "accept": ["30"],
            "exp": r"$\overline{JK}$ matches $\overline{MN}$, so $k = \dfrac{20}{8} = 2.5$. Then $NP = 2.5 \cdot 12 = 30$."}},
 {"ess": True, "name": "Rule 2: Parallel lines make similar triangles",
  "rule": r"nested: $\dfrac{AD}{AB} = \dfrac{DE}{BC}$ &nbsp;·&nbsp; bowtie: $\dfrac{PQ}{SR} = \dfrac{PM}{SM}$ &nbsp;·&nbsp; use whole sides",
  "say": r"In the nested picture, the small triangle and the large triangle share the angle at $A$, and the parallel segment makes the other angles equal. Compare the small triangle with the whole triangle, so that both sides you use start at the shared vertex.",
  "fig": "s2",
  "prob": r"In the figure above, $\overline{DE}$ is parallel to $\overline{BC}$. If $AD = 8$, $DB = 4$ and $DE = 10$, what is the length of $\overline{BC}$?",
  "sol": r"<strong>Step 1: name the similar triangles.</strong> $\triangle ADE \sim \triangle ABC$.<br><strong>Step 2: use the whole side.</strong> $AB = 8 + 4 = 12$.<br><strong>Step 3: write the proportion.</strong> $\dfrac{BC}{10} = \dfrac{12}{8}$, so $BC = 15$.<br><strong>Check:</strong> $\dfrac{8}{12}$ and $\dfrac{10}{15}$ both reduce to $\dfrac{2}{3}$. ✓",
  "trap": r"Using $DB$ where $AB$ belongs. The ratio $\dfrac{8}{4}$ compares two pieces of one side and would give $BC = 5$, which is shorter than $\overline{DE}$. The matching sides are $\overline{AD}$ and the whole side $\overline{AB}$.",
  "micro": {"q": r"Segments $\overline{PS}$ and $\overline{QR}$ cross at $M$, and $\overline{PQ}$ is parallel to $\overline{RS}$. If $PQ = 6$, $RS = 15$ and $QM = 8$, then $RM =$", "accept": ["20"],
            "exp": r"$\triangle PQM \sim \triangle SRM$, so $\dfrac{RM}{QM} = \dfrac{RS}{PQ} = \dfrac{15}{6} = 2.5$. Then $RM = 2.5 \cdot 8 = 20$."}},
 {"ess": True, "name": "Rule 3: Every length scales by k",
  "rule": r"sides, heights, diagonals, radii and perimeters are all multiplied by $k$ &nbsp;·&nbsp; angles stay the same",
  "say": r"A perimeter is a sum of lengths, so it scales the way each side does. You do not need all three sides of the second triangle: find $k$ from one matching pair and apply it to the perimeter.",
  "prob": r"Triangle $ABC$ has sides of length $9$, $12$ and $15$. Triangle $DEF$ is similar to triangle $ABC$, and its shortest side has length $15$. What is the perimeter of triangle $DEF$?",
  "sol": r"<strong>Step 1: find the scale factor.</strong> Shortest side matches shortest side: $k = \dfrac{15}{9} = \dfrac{5}{3}$.<br><strong>Step 2: find the first perimeter.</strong> $9 + 12 + 15 = 36$.<br><strong>Step 3: scale it.</strong> $36 \cdot \dfrac{5}{3} = 60$.<br><strong>Check:</strong> the sides of triangle $DEF$ are $15$, $20$ and $25$, and $15 + 20 + 25 = 60$. ✓",
  "trap": r"Matching the $15$ in one triangle with the $15$ in the other. The shortest side of triangle $DEF$ matches the shortest side of triangle $ABC$, which is $9$.",
  "micro": {"q": r"The circumference of circle $X$ is $3$ times the circumference of circle $Y$. If the radius of circle $Y$ is $7$, the radius of circle $X$ is", "accept": ["21"],
            "exp": r"A radius and a circumference are both lengths, so they share the scale factor: $3 \cdot 7 = 21$."}},
 {"ess": True, "name": "Rule 4: Areas scale by k squared",
  "rule": r"lengths $a : b$ &nbsp;·&nbsp; areas $a^2 : b^2$ &nbsp;·&nbsp; going back, take a square root",
  "say": r"All equilateral triangles are similar to each other, and so are all squares and all circles. Once you know the ratio of one pair of lengths, square it to compare areas. You do not need an area formula.",
  "fig": "s4",
  "prob": r"Two equilateral triangles are shown above. The longer side length is $a$, the shorter side length is $b$, and $\dfrac{a}{b} = \dfrac{4}{3}$. If the smaller triangle has an area of $27$, what is the area of the larger triangle?",
  "sol": r"<strong>Step 1: find the ratio of lengths.</strong> From the smaller triangle to the larger, $k = \dfrac{4}{3}$.<br><strong>Step 2: square it.</strong> $k^2 = \dfrac{16}{9}$.<br><strong>Step 3: scale the area.</strong> $27 \cdot \dfrac{16}{9} = 48$.<br><strong>Check:</strong> $27 : 48$ reduces to $9 : 16$, which is the square of $3 : 4$. ✓",
  "trap": r"Multiplying the area by $\dfrac{4}{3}$, which gives $36$. That treats the area as a length. An area needs the squared ratio.",
  "micro": {"q": r"Two similar rectangles have areas of $50$ and $72$. The ratio of their matching sides, smaller to larger, is $5 : n$. Then $n =$", "accept": ["6"],
            "exp": r"$50 : 72$ reduces to $25 : 36$. Take the square root of each: $5 : 6$."}},
 {"ess": False, "name": "Rule 5: Regions between similar figures",
  "rule": r"write each area in parts using the squared ratio &nbsp;·&nbsp; subtract the parts &nbsp;·&nbsp; find one part",
  "say": r"The two circles are similar, so their areas follow the squared ratio of their radii. Counting in parts keeps the arithmetic small: you do not need $\pi$ or the radii themselves.",
  "fig": "s5",
  "prob": r"In the figure above, two circles share a center, and the radius of the larger circle is $\dfrac{7}{4}$ of the radius of the smaller circle. The smaller circle has an area of $32$. What is the area of the shaded ring?",
  "sol": r"<strong>Step 1: write the ratio of the radii.</strong> Smaller to larger, $4 : 7$.<br><strong>Step 2: write the areas in parts.</strong> $16$ parts and $49$ parts.<br><strong>Step 3: find one part.</strong> $32 \div 16 = 2$.<br><strong>Step 4: find the shaded ring.</strong> It is $49 - 16 = 33$ parts, and $33 \cdot 2 = 66$.<br><strong>Check:</strong> the larger circle has an area of $49 \cdot 2 = 98$, and $98 - 32 = 66$. ✓",
  "trap": r"Stopping at $98$, the area of the larger circle, or scaling $32$ by $\dfrac{7}{4}$ to get $56$. The shaded ring is the larger area minus the smaller one, and areas use the squared ratio.",
  "micro": {"q": r"In triangle $ABC$, $\overline{DE}$ is parallel to $\overline{BC}$, with $D$ on $\overline{AB}$ and $E$ on $\overline{AC}$. If $AD = 2$, $DB = 3$ and the area of triangle $ADE$ is $8$, the area of quadrilateral $DBCE$ is", "accept": ["42"],
            "exp": r"$AD : AB = 2 : 5$, so the areas are $4$ parts and $25$ parts. One part is $8 \div 4 = 2$, and the quadrilateral is $25 - 4 = 21$ parts: $42$."}},
 {"ess": False, "name": "Rule 6: Volumes scale by k cubed",
  "rule": r"lengths $k$ &nbsp;·&nbsp; areas $k^2$ &nbsp;·&nbsp; volumes $k^3$",
  "say": r"Similar solids are scaled copies in each direction: height, radius and width all use the same $k$. A volume multiplies three of those lengths, so it picks up $k$ three times.",
  "prob": r"Two jars are similar cylinders with heights of $6$ inches and $9$ inches. If the smaller jar holds $80$ cubic inches, how many cubic inches does the larger jar hold?",
  "sol": r"<strong>Step 1: find the scale factor.</strong> $k = \dfrac{9}{6} = \dfrac{3}{2}$.<br><strong>Step 2: cube it.</strong> $k^3 = \dfrac{27}{8}$.<br><strong>Step 3: scale the volume.</strong> $80 \cdot \dfrac{27}{8} = 270$.<br><strong>Check:</strong> $80 : 270$ reduces to $8 : 27$, which is the cube of $2 : 3$. ✓",
  "trap": r"Using $k$ or $k^2$. $80 \cdot \dfrac{3}{2} = 120$ treats the volume as a length, and $80 \cdot \dfrac{9}{4} = 180$ treats it as an area.",
  "micro": {"q": r"Each length of a solid is multiplied by $4$. Its volume is multiplied by", "accept": ["64"],
            "exp": r"$4^3 = 64$."}},
]
LAST_STARRED_STEP_INDEX = 3  # 0-based index of the last starred step (Rule 4)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
NESTED_Q = r"In triangle $ABC$, $\overline{DE}$ is parallel to $\overline{BC}$, with $D$ on $\overline{AB}$ and $E$ on $\overline{AC}$."
FLUENCY = [
 {"sec": "A. Matching sides and the scale factor", "items": [
   {"q": r"Triangle $ABC$ is similar to triangle $DEF$, in that order. If $AB = 6$ and $DE = 9$, the scale factor from triangle $ABC$ to triangle $DEF$ is", "accept": ["3/2", "1.5"], "exp": r"Divide the new length by the matching original length: $\dfrac{9}{6} = \dfrac{3}{2}$."},
   {"mc": True, "q": r"Triangle $ABC$ is similar to triangle $XYZ$, in that order. Which side of triangle $XYZ$ matches $\overline{BC}$?", "opts": [r"$\overline{XY}$", r"$\overline{YZ}$", r"$\overline{XZ}$", "It depends on how the figure is drawn."], "correct": 1, "exp": r"$B$ and $C$ are the second and third letters, so they match $Y$ and $Z$. The statement decides the matching, however the figure is turned."},
   {"q": r"Triangle $ABC$ is similar to triangle $DEF$, in that order. If $AB = 4$, $BC = 9$ and $DE = 12$, then $EF =$", "accept": ["27"], "exp": r"$k = \dfrac{12}{4} = 3$, and $3 \cdot 9 = 27$."},
   {"q": r"A triangle has sides of length $10$, $16$ and $20$. A similar triangle has a longest side of length $15$. Its shortest side has length", "accept": ["7.5", "15/2"], "exp": r"Longest matches longest: $k = \dfrac{15}{20} = \dfrac{3}{4}$. The shortest side is $\dfrac{3}{4} \cdot 10 = 7.5$."},
   {"fig": "fa5", "q": r"The two triangles shown are similar, and equal angles are marked the same way. $x =$", "accept": ["15"], "exp": r"The side between the single mark and the double mark is $6$ in one triangle and $10$ in the other, so $k = \dfrac{10}{6} = \dfrac{5}{3}$. The side marked $x$ matches the side of length $9$: $9 \cdot \dfrac{5}{3} = 15$."},
 ]},
 {"sec": "B. Parallel lines: nested and bowtie", "items": [
   {"fig": "fb1", "q": r"In the figure, $\overline{DE}$ is parallel to $\overline{BC}$. $BC =$", "accept": ["16"], "exp": r"$AB = 3 + 9 = 12$, so $k = \dfrac{12}{3} = 4$ from the small triangle to the large one. $BC = 4 \cdot 4 = 16$."},
   {"fig": "fb2", "q": r"In the figure, $\overline{DE}$ is parallel to $\overline{BC}$. $DE =$", "accept": ["14"], "exp": r"$AB = 10 + 15 = 25$, so $\dfrac{DE}{35} = \dfrac{10}{25}$ and $DE = 14$."},
   {"fig": "fb3", "q": r"In the figure, $\overline{PQ}$ is parallel to $\overline{RS}$. $SM =$", "accept": ["9"], "exp": r"$\triangle PQM \sim \triangle SRM$, and $\overline{PM}$ matches $\overline{SM}$. $k = \dfrac{12}{8} = 1.5$, so $SM = 1.5 \cdot 6 = 9$."},
   {"fig": "fb4", "q": r"In the figure, $\overline{PQ}$ is parallel to $\overline{RS}$, and $QR = 24$. $QM =$", "accept": ["6"], "exp": r"$QM : RM = PQ : RS = 5 : 15 = 1 : 3$. Split $24$ into $4$ equal parts of $6$: $QM = 6$ and $RM = 18$."},
   {"mc": True, "q": NESTED_Q + r" If $AD = 5$ and $DB = 10$, the ratio $DE : BC$ is", "opts": ["$1 : 2$", "$1 : 3$", "$2 : 3$", "$1 : 4$"], "correct": 1, "exp": r"The whole side is $AB = 15$, so $DE : BC = AD : AB = 5 : 15 = 1 : 3$. The ratio $1 : 2$ compares the two pieces of $\overline{AB}$."},
 ]},
 {"sec": "C. Every length scales by k", "items": [
   {"q": r"Two similar triangles have a pair of matching sides of $8$ and $12$. The smaller triangle has a perimeter of $26$. The perimeter of the larger triangle is", "accept": ["39"], "exp": r"$k = \dfrac{12}{8} = 1.5$, and $1.5 \cdot 26 = 39$."},
   {"q": r"Two circles have radii of $6$ and $15$. In simplest form, the ratio of their circumferences is $2 : n$. Then $n =$", "accept": ["5"], "exp": r"Circumferences have the same ratio as radii: $6 : 15 = 2 : 5$."},
   {"q": r"Two similar triangles have perimeters of $28$ and $42$. A side of the smaller triangle has length $8$. The matching side of the larger triangle has length", "accept": ["12"], "exp": r"$k = \dfrac{42}{28} = 1.5$, and $1.5 \cdot 8 = 12$."},
   {"q": r"Matching heights of two similar triangles are $9$ and $6$. The larger triangle has a base of $33$. The matching base of the smaller triangle is", "accept": ["22"], "exp": r"From larger to smaller, $k = \dfrac{6}{9} = \dfrac{2}{3}$, and $\dfrac{2}{3} \cdot 33 = 22$."},
 ]},
 {"sec": "D. Areas scale by k squared", "items": [
   {"mc": True, "q": r"Each side length of a figure is tripled. Its area is multiplied by", "opts": ["$3$", "$6$", "$9$", "$27$"], "correct": 2, "exp": r"Areas are multiplied by $k^2 = 3^2 = 9$."},
   {"q": r"Two similar triangles have a pair of matching sides of $3$ and $5$. The smaller triangle has an area of $18$. The area of the larger triangle is", "accept": ["50"], "exp": r"Areas are in the ratio $9 : 25$, and $18 \cdot \dfrac{25}{9} = 50$."},
   {"q": r"The radii of two circles are in the ratio $1 : 4$. The smaller circle has an area of $5$. The area of the larger circle is", "accept": ["80"], "exp": r"Areas are in the ratio $1 : 16$, and $5 \cdot 16 = 80$."},
   {"q": r"Two similar polygons have areas of $36$ and $121$. The ratio of their matching sides is $6 : n$. Then $n =$", "accept": ["11"], "exp": r"Take square roots: $\sqrt{36} : \sqrt{121} = 6 : 11$."},
   {"q": r"Two similar triangles have areas of $32$ and $50$. A side of the smaller triangle has length $12$. The matching side of the larger triangle has length", "accept": ["15"], "exp": r"$32 : 50$ reduces to $16 : 25$, so lengths are in the ratio $4 : 5$. Then $12 \cdot \dfrac{5}{4} = 15$."},
 ]},
 {"sec": "E. Regions and volumes", "items": [
   {"q": r"Two circles have the same center, and their radii are in the ratio $1 : 2$. The smaller circle has an area of $13$. The area of the ring between the circles is", "accept": ["39"], "exp": r"The areas are $1$ part and $4$ parts, so the ring is $3$ parts: $3 \cdot 13 = 39$."},
   {"q": NESTED_Q + r" If $AD : AB = 1 : 2$ and the area of triangle $ABC$ is $80$, the area of quadrilateral $DBCE$ is", "accept": ["60"], "exp": r"The areas are $1$ part and $4$ parts. One part is $80 \div 4 = 20$, and the quadrilateral is $3$ parts: $60$."},
   {"mc": True, "q": r"Each edge of a box is doubled. Its volume is multiplied by", "opts": ["$2$", "$4$", "$6$", "$8$"], "correct": 3, "exp": r"Volumes are multiplied by $k^3 = 2^3 = 8$."},
   {"q": r"Two similar pyramids have a pair of matching edges of $2$ and $5$. The smaller pyramid has a volume of $16$. The volume of the larger pyramid is", "accept": ["250"], "exp": r"Volumes are in the ratio $8 : 125$, and $16 \cdot \dfrac{125}{8} = 250$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy", "fig": "p1",
  "stem": r"In the figure above, triangle $ABC$ is similar to triangle $DEF$, where $A$, $B$ and $C$ correspond to $D$, $E$ and $F$. What is the length of $\overline{DF}$?",
  "options": ["$7.2$", "$18$", "$20$", "$24$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $AB = 9$, $AC = 12$ and $DE = 15$. $\overline{AB}$ matches $\overline{DE}$, and $\overline{AC}$ matches $\overline{DF}$.<br><br><strong>Scale factor.</strong> $k = \dfrac{15}{9} = \dfrac{5}{3}$.<br><strong>Scale the side.</strong> $DF = 12 \cdot \dfrac{5}{3} = 20$.<br><strong>Check:</strong> $\dfrac{9}{15}$ and $\dfrac{12}{20}$ both reduce to $\dfrac{3}{5}$. ✓",
  "trap": r"Choice B adds $6$ to $12$ because $\overline{DE}$ is $6$ longer than $\overline{AB}$. Choice A multiplies by $\dfrac{9}{15}$, which makes a side of the larger triangle shorter than its match."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"Triangle $RST$ is similar to triangle $UVW$. The shortest side of triangle $RST$ has length $8$, and the shortest side of triangle $UVW$ has length $20$. If the perimeter of triangle $RST$ is $34$, what is the perimeter of triangle $UVW$?",
  "label": "Perimeter $=$", "accept": ["85"],
  "sol": r"<strong>Given:</strong> one pair of matching sides, $8$ and $20$, and the smaller perimeter, $34$.<br><br><strong>Scale factor.</strong> $k = \dfrac{20}{8} = 2.5$.<br><strong>Scale the perimeter.</strong> A perimeter is a length, so it is multiplied by $k$: $34 \cdot 2.5 = 85$.",
  "trap": r"Adding $12$ to the perimeter because the shortest side grew by $12$. Each side is multiplied by $2.5$, so the perimeter is too."},
 {"ess": True, "type": "mc", "diff": "Easy to medium", "fig": "p3",
  "stem": r"In the figure above, $\overline{DE}$ is parallel to $\overline{BC}$. What is the length of $\overline{BC}$?",
  "options": ["$9$", "$21$", "$24$", "$25$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $AD = 10$, $DB = 6$, $DE = 15$ and $\overline{DE} \parallel \overline{BC}$, so $\triangle ADE \sim \triangle ABC$.<br><br><strong>Whole side.</strong> $AB = 10 + 6 = 16$.<br><strong>Proportion.</strong> $\dfrac{BC}{15} = \dfrac{16}{10}$, so $BC = 24$.<br><strong>Check:</strong> $\dfrac{10}{16}$ and $\dfrac{15}{24}$ both reduce to $\dfrac{5}{8}$. ✓",
  "trap": r"Choice D multiplies $15$ by $\dfrac{10}{6}$, which compares the two pieces of $\overline{AB}$. Choice A uses $\dfrac{6}{10}$, and choice B adds $6$. The matching sides are $\overline{AD}$ and the whole side $\overline{AB}$."},
 {"ess": True, "type": "ne", "diff": "Medium", "fig": "p4",
  "stem": r"The two circles shown above have centers $A$ and $B$. The circumference of circle $A$ is $\dfrac{3}{5}$ of the circumference of circle $B$. If circle $A$ has an area of $36$, what is the area of circle $B$?",
  "label": "Area $=$", "accept": ["100"],
  "sol": r"<strong>Given:</strong> circumferences in the ratio $3 : 5$, and the smaller area.<br><br><strong>Lengths to areas.</strong> A circumference is a length, so $k = \dfrac{5}{3}$ and the areas are in the ratio $9 : 25$.<br><strong>Scale the area.</strong> $36 \cdot \dfrac{25}{9} = 100$.<br><strong>Check:</strong> $36 : 100$ reduces to $9 : 25$. ✓",
  "trap": r"Scaling the area by $\dfrac{5}{3}$, which gives $60$. The ratio of the circumferences must be squared before it is used on an area."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"At the same time of day, a $5$-foot post casts a $3$-foot shadow, and a nearby tree casts a $21$-foot shadow. The post and the tree both stand straight up on level ground. What is the height of the tree, in feet?",
  "options": ["$12.6$", "$23$", "$35$", "$105$"], "correct": 2,
  "sol": r"<strong>Given:</strong> two heights and two shadows. Key: $h$ is the height of the tree.<br><br>The sun's rays meet the ground at the same angle for both, and each object makes a right angle with the ground. The two right triangles share an acute angle, so they are similar.<br><strong>Proportion.</strong> $\dfrac{h}{21} = \dfrac{5}{3}$, so $h = 35$.",
  "trap": r"Choice A flips one ratio: $21 \cdot \dfrac{3}{5}$. The tree has the longer shadow, so it must be taller than the post. Choice B adds the $18$-foot difference in the shadows to the post."},
 {"ess": True, "type": "ne", "diff": "Medium", "fig": "p6",
  "stem": r"Equilateral triangles $ABC$ and $DEF$ are shown above. Each side of triangle $ABC$ has length $a$, and each side of triangle $DEF$ has length $b$. If $\dfrac{a}{b} = \dfrac{7}{4}$ and triangle $ABC$ has an area of $98$, what is the area of triangle $DEF$?",
  "label": "Area $=$", "accept": ["32"],
  "sol": r"<strong>Given:</strong> two equilateral triangles, which are similar, with sides in the ratio $7 : 4$.<br><br><strong>Lengths to areas.</strong> The areas are in the ratio $49 : 16$.<br><strong>Scale the area.</strong> Triangle $DEF$ is the smaller one: $98 \cdot \dfrac{16}{49} = 32$.<br><strong>Check:</strong> $98 : 32$ reduces to $49 : 16$. ✓",
  "trap": r"Multiplying $98$ by $\dfrac{4}{7}$, which gives $56$. The side ratio must be squared before it is used on an area."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p7",
  "stem": r"In the figure above, $\overline{PQ}$ is parallel to $\overline{RS}$, and segments $\overline{PS}$ and $\overline{QR}$ cross at $M$. Triangle $PQM$ has an area of $6$, and triangle $SRM$ has an area of $54$. If the perimeter of triangle $PQM$ is $14$, what is the perimeter of triangle $SRM$?",
  "options": ["$28$", "$42$", "$62$", "$126$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $\overline{PQ} \parallel \overline{RS}$, so $\triangle PQM \sim \triangle SRM$. The areas are $6$ and $54$.<br><br><strong>Ratio of areas.</strong> $6 : 54$ reduces to $1 : 9$.<br><strong>Areas to lengths.</strong> Take square roots: lengths are in the ratio $1 : 3$.<br><strong>Scale the perimeter.</strong> $14 \cdot 3 = 42$.",
  "trap": r"Choice D multiplies $14$ by $9$, which uses the area ratio on a length. Choice C adds the difference of the areas. A perimeter is a length, so take the square root of the area ratio first."},
 {"ess": False, "type": "ne", "diff": "Medium", "fig": "p8",
  "stem": r"The two circles shown above have the same center. The radius of the smaller circle is $\dfrac{3}{5}$ of the radius of the larger circle, and the smaller circle has an area of $63$. What is the area of the shaded ring?",
  "label": "Area $=$", "accept": ["112"],
  "sol": r"<strong>Given:</strong> radii in the ratio $3 : 5$, and the smaller area.<br><br><strong>Areas in parts.</strong> $9$ parts and $25$ parts.<br><strong>One part.</strong> $63 \div 9 = 7$.<br><strong>Shaded ring.</strong> $25 - 9 = 16$ parts, and $16 \cdot 7 = 112$.<br><strong>Check:</strong> the larger circle has an area of $25 \cdot 7 = 175$, and $175 - 63 = 112$. ✓",
  "trap": r"Answering $175$, the area of the larger circle, or scaling $63$ by $\dfrac{5}{3}$. The shaded ring is the larger circle minus the smaller one."},
 {"ess": False, "type": "mc", "diff": "Medium-hard", "fig": "p9",
  "stem": r"In the figure above, angle $BAC$ is a right angle, $\overline{KM}$ and $\overline{LN}$ are perpendicular to $\overline{AC}$, and $AM : MN : NC = 1 : 2 : 2$. If the area of quadrilateral $KMNL$ is $60$, what is the area of triangle $ABC$?",
  "options": ["$100$", "$125$", "$150$", "$300$"], "correct": 1,
  "sol": r"<strong>Given:</strong> three right triangles that share the angle at $C$: $LNC$, $KMC$ and $BAC$. They are similar.<br><br><strong>Measure from $C$.</strong> $NC : MC : AC = 2 : 4 : 5$.<br><strong>Areas in parts.</strong> $4$, $16$ and $25$ parts.<br><strong>One part.</strong> Quadrilateral $KMNL$ is $16 - 4 = 12$ parts, so one part is $60 \div 12 = 5$.<br><strong>Whole triangle.</strong> $25 \cdot 5 = 125$.",
  "trap": r"Using $1 : 2 : 2$ as the ratio of the triangles. Those numbers are pieces of one side. The matching sides of the three triangles are $\overline{NC}$, $\overline{MC}$ and $\overline{AC}$, all measured from $C$. Choice C multiplies $60$ by $2.5$, the ratio of $AC$ to $NC$, without squaring."},
 {"ess": False, "type": "ne", "diff": "Medium-hard", "fig": "p10",
  "stem": r"In the figure above, the circles with centers $S$ and $T$ touch each other at one point, and each touches the largest circle from the inside. The centers of all three circles lie on one diameter of the largest circle. The radius of circle $S$ is $2$ times the radius of circle $T$. If the area of the shaded region is $36\pi$, what is the radius of circle $T$?",
  "label": "Radius $=$", "accept": ["3"],
  "sol": r"<strong>Given:</strong> key: $r$ is the radius of circle $T$, so the radius of circle $S$ is $2r$.<br><br><strong>Largest circle.</strong> The two diameters, $4r$ and $2r$, add up to the large diameter, $6r$. Its radius is $3r$.<br><strong>Areas in parts.</strong> Radii $r : 2r : 3r$ give areas of $1$, $4$ and $9$ parts, where one part is $\pi r^2$.<br><strong>Shaded region.</strong> $9 - 4 - 1 = 4$ parts: $4\pi r^2 = 36\pi$, so $r^2 = 9$ and $r = 3$.",
  "trap": r"Subtracting only one of the inner circles, or answering with $r^2 = 9$. The shaded region is the largest circle minus both inner circles, and the question asks for a radius."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "c1",
  "stem": r"In the figure above, $\overline{DE}$ is parallel to $\overline{BC}$. If $AD = x$, $DB = 6$, $DE = 10$ and $BC = 25$, what is the value of $x$?",
  "label": "$x =$", "accept": ["4"],
  "sol": r"<strong>Given:</strong> $\overline{DE} \parallel \overline{BC}$, so $\triangle ADE \sim \triangle ABC$. The whole side is $AB = x + 6$.<br><br><strong>Proportion.</strong> $\dfrac{x}{x + 6} = \dfrac{10}{25} = \dfrac{2}{5}$.<br><strong>Solve.</strong> $5x = 2x + 12$, so $x = 4$.<br><strong>Check:</strong> $\dfrac{4}{10} = \dfrac{2}{5}$. ✓",
  "trap": r"Build the whole side before you write the proportion: the side of the large triangle is $x + 6$. Writing $\dfrac{x}{6} = \dfrac{10}{25}$ compares $AD$ with $DB$ and gives $x = 2.4$.",
  "extrasIntro": r"Nested triangles with a variable in a side: build the whole side first. Three more reps.",
  "extras": [
   {"type": "ne", "q": NESTED_Q + r" If $AD = x$, $DB = 5$, $DE = 6$ and $BC = 9$, then $x =$", "label": "$=$", "accept": ["10"], "exp": r"$\dfrac{x}{x + 5} = \dfrac{6}{9} = \dfrac{2}{3}$, so $3x = 2x + 10$ and $x = 10$."},
   {"type": "ne", "q": NESTED_Q + r" If $AD = 6$, $DB = x$, $DE = 8$ and $BC = 20$, then $x =$", "label": "$=$", "accept": ["9"], "exp": r"$\dfrac{6}{6 + x} = \dfrac{8}{20} = \dfrac{2}{5}$, so $30 = 12 + 2x$ and $x = 9$."},
   {"type": "ne", "q": NESTED_Q + r" If $AD = x$, $AB = 3x - 4$, $DE = 4$ and $BC = 10$, then $x =$", "label": "$=$", "accept": ["8"], "exp": r"$\dfrac{x}{3x - 4} = \dfrac{4}{10} = \dfrac{2}{5}$, so $5x = 6x - 8$ and $x = 8$. Then $AB = 20$, and $\dfrac{8}{20} = \dfrac{2}{5}$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "c2",
  "stem": r"In the figure above, $\overline{PQ}$ is parallel to $\overline{RS}$, $PQ = 12$ and $RS = 21$. If the area of triangle $PQM$ is $32$, what is the area of triangle $SRM$?",
  "label": "Area $=$", "accept": ["98"],
  "sol": r"<strong>Given:</strong> $\overline{PQ} \parallel \overline{RS}$, so $\triangle PQM \sim \triangle SRM$, and $\overline{PQ}$ matches $\overline{SR}$.<br><br><strong>Ratio of lengths.</strong> $12 : 21 = 4 : 7$.<br><strong>Ratio of areas.</strong> $16 : 49$.<br><strong>Scale the area.</strong> $32 \cdot \dfrac{49}{16} = 98$.",
  "trap": r"The sides give $k$, and the areas need $k^2$. Scaling $32$ by $\dfrac{7}{4}$ gives $56$, which treats the area as a length."},
 {"ess": True, "type": "ne", "diff": "Medium-hard · trig blend",
  "stem": r"Right triangle $ABC$ is similar to right triangle $DEF$, where $A$, $B$ and $C$ correspond to $D$, $E$ and $F$, and the right angles are at $C$ and $F$. In triangle $ABC$, $AC = 16$ and $BC = 12$. Each side of triangle $DEF$ is $2.5$ times as long as the matching side of triangle $ABC$. What is the value of $\cos D$?",
  "label": r"$\cos D =$", "accept": ["4/5", "0.8", ".8"],
  "sol": r"<strong>Given:</strong> similar triangles have equal matching angles, so angle $D$ equals angle $A$ and $\cos D = \cos A$.<br><br><strong>Hypotenuse.</strong> $AB = \sqrt{16^2 + 12^2} = \sqrt{400} = 20$.<br><strong>Cosine.</strong> $\cos A = \dfrac{AC}{AB} = \dfrac{16}{20} = \dfrac{4}{5}$.<br><strong>Check in the larger triangle:</strong> $DF = 40$ and $DE = 50$, and $\dfrac{40}{50} = \dfrac{4}{5}$. ✓",
  "trap": r"A trig ratio compares two sides of the same triangle. Both sides are multiplied by the same $k$, so the ratio is the same in the larger triangle. The cosine is not multiplied by $2.5$."},
 {"ess": True, "type": "mc", "diff": "Hard · percent blend",
  "stem": r"Each side of a triangle is increased by $20\%$ to make a larger, similar triangle. By what percent does the area of the triangle increase?",
  "options": [r"$20\%$", r"$40\%$", r"$44\%$", r"$144\%$"], "correct": 2,
  "sol": r"<strong>Given:</strong> each length is multiplied by $1.2$, so $k = 1.2$.<br><br><strong>Area.</strong> The area is multiplied by $k^2 = 1.2^2 = 1.44$.<br><strong>Percent increase.</strong> A multiplier of $1.44$ is an increase of $44\%$.",
  "trap": r"Turn the percent into a multiplier, then square it: $1.2^2 = 1.44$. Choice A scales the area as if it were a length, and choice B doubles the percent. Choice D is the new area as a percent of the old area, which is not the increase."},
 {"ess": False, "type": "ne", "diff": "Hard", "fig": "c5",
  "stem": r"In the figure above, $\overline{DE}$ and $\overline{FG}$ are parallel to $\overline{BC}$, and $AD = DF = FB$. If the area of quadrilateral $FBCG$ is $45$, what is the area of quadrilateral $DFGE$?",
  "label": "Area $=$", "accept": ["27"],
  "sol": r"<strong>Given:</strong> three nested triangles that share the angle at $A$: $ADE$, $AFG$ and $ABC$.<br><br><strong>Measure from $A$.</strong> $AD : AF : AB = 1 : 2 : 3$.<br><strong>Areas in parts.</strong> $1$, $4$ and $9$ parts. From the top, the three bands are $1$, $4 - 1 = 3$ and $9 - 4 = 5$ parts.<br><strong>One part.</strong> $FBCG$ is $5$ parts, so one part is $45 \div 5 = 9$.<br><strong>Middle band.</strong> $DFGE$ is $3$ parts: $27$.",
  "trap": r"Measure each triangle from the shared vertex, square, and then subtract. Equal pieces along $\overline{AB}$ do not make equal bands: the bands are $1$, $3$ and $5$ parts.",
  "extrasIntro": r"Regions in parts: square the ratio from the shared vertex or the shared center, then subtract. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"Two circles have the same center, and their radii are in the ratio $3 : 5$. If the ring between the circles has an area of $80$, the area of the smaller circle is", "label": "$=$", "accept": ["45"], "exp": r"The areas are $9$ parts and $25$ parts, so the ring is $16$ parts. One part is $80 \div 16 = 5$, and the smaller circle is $9 \cdot 5 = 45$."},
   {"type": "ne", "q": NESTED_Q + r" If $AD : DB = 1 : 3$ and the area of triangle $ABC$ is $96$, the area of quadrilateral $DBCE$ is", "label": "$=$", "accept": ["90"], "exp": r"$AD : AB = 1 : 4$, so the areas are $1$ part and $16$ parts. One part is $96 \div 16 = 6$, and the quadrilateral is $15$ parts: $90$."},
   {"type": "ne", "q": r"Circles $X$ and $Y$ are tangent to each other, and each is tangent to a larger circle from the inside, with all three centers on one diameter. The radii of circles $X$ and $Y$ are $2$ and $3$. The area inside the larger circle and outside both smaller circles is $k\pi$. Then $k =$", "label": "$=$", "accept": ["12"], "exp": r"The diameters $4$ and $6$ add up to the large diameter, $10$, so the large radius is $5$. The areas are $25\pi$, $4\pi$ and $9\pi$: $25 - 4 - 9 = 12$."},
  ]},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"Two similar cones have surface areas of $90$ square centimeters and $160$ square centimeters. If the volume of the smaller cone is $54$ cubic centimeters, what is the volume of the larger cone, in cubic centimeters?",
  "label": "Volume $=$", "accept": ["128"],
  "sol": r"<strong>Given:</strong> two surface areas and the smaller volume.<br><br><strong>Areas to lengths.</strong> $90 : 160$ reduces to $9 : 16$, so lengths are in the ratio $3 : 4$.<br><strong>Lengths to volumes.</strong> $27 : 64$.<br><strong>Scale the volume.</strong> $54 \cdot \dfrac{64}{27} = 128$.",
  "trap": r"Go through the lengths. An area ratio is $k^2$, so take its square root to get $k = \dfrac{4}{3}$, then cube it. Scaling the volume by $\dfrac{16}{9}$ gives $96$."},
 {"ess": False, "type": "ne", "diff": "Hard", "fig": "c7",
  "stem": r"In the figure above, $\overline{DE}$ is parallel to $\overline{BC}$, and $\overline{DE}$ divides triangle $ABC$ into two regions of equal area. If $AB = 12$, the length of $\overline{AD}$ is $k\sqrt{2}$. What is the value of $k$?",
  "label": "$k =$", "accept": ["6"],
  "sol": r"<strong>Given:</strong> triangle $ADE$ has half the area of triangle $ABC$, and the two triangles are similar.<br><br><strong>Areas to lengths.</strong> Areas in the ratio $1 : 2$ mean lengths in the ratio $1 : \sqrt{2}$.<br><strong>Scale the side.</strong> $AD = \dfrac{12}{\sqrt{2}} = 6\sqrt{2}$, so $k = 6$.<br><strong>Check:</strong> $\left(\dfrac{6\sqrt{2}}{12}\right)^2 = \dfrac{72}{144} = \dfrac{1}{2}$. ✓",
  "trap": r"Half of the area needs a side ratio of $\dfrac{1}{\sqrt{2}}$, which is about $0.71$. Halving the side gives $AD = 6$, and that triangle has only one fourth of the area."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"Triangle $ABC$ is similar to triangle $DEF$, in that order. If $AB = 12$, $DE = 18$ and $AC = 20$, what is the length of $\overline{DF}$?", "opts": ["$24$", "$26$", "$30$", "$45$"], "correct": 2,
  "exp": r"$k = \dfrac{18}{12} = 1.5$, and $1.5 \cdot 20 = 30$. Adding $6$ gives $26$, but similar figures keep ratios equal, not differences."},
 {"q": NESTED_Q + r" If $AD = 6$, $DB = 12$ and $BC = 27$, what is the length of $\overline{DE}$?", "opts": ["$9$", "$13.5$", "$18$", "$81$"], "correct": 0,
  "exp": r"The whole side is $AB = 18$, so $\dfrac{DE}{27} = \dfrac{6}{18}$ and $DE = 9$. Using $\dfrac{6}{12}$ compares two pieces of one side."},
 {"q": r"Two similar triangles have a pair of matching sides of $5$ and $15$. If the smaller triangle has an area of $7$, what is the area of the larger triangle?", "opts": ["$21$", "$42$", "$63$", "$189$"], "correct": 2,
  "exp": r"Lengths are in the ratio $1 : 3$, so areas are in the ratio $1 : 9$: $7 \cdot 9 = 63$. Multiplying by $3$ gives $21$, which treats the area as a length."},
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

R3 = math.sqrt(3)
R2 = math.sqrt(2)
NOTE = 'Note: Figure not drawn to scale.'
FIGS = {}


def turn(p, deg=0, flip=False):
    """Rotate the point p by deg degrees about the origin, after an optional mirror in the y-axis."""
    x, y = (-p[0] if flip else p[0]), p[1]
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return pt(x * c - y * s, x * s + y * c)


def place(P, k=1.0, deg=0, flip=False, at=(0, 0)):
    """Scale, mirror, rotate and then shift a list of points."""
    out = []
    for p in P:
        q = turn(pt(p[0] * k, p[1] * k), deg, flip)
        out.append(pt(q[0] + at[0], q[1] + at[1]))
    return out


def bbox(points, m=1.0, mx=None, my=None):
    mx = m if mx is None else mx
    my = m if my is None else my
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    return [round(min(xs) - mx, 3), round(min(ys) - my, 3), round(max(xs) + mx, 3), round(max(ys) + my, 3)]


def oside(a, b, t, G, off=13, **k):
    """A label beside segment a-b, on the side away from the point G (usually the centroid)."""
    cross = (b[0] - a[0]) * (G[1] - a[1]) - (b[1] - a[1]) * (G[0] - a[0])
    return side(a, b, t, -off if cross > 0 else off, **k)


def tri_parts(P, names=None, sides=None, off=13, d=13):
    """Segments, corner letters and side labels for the triangle with corners P. `sides` labels P0P1, P1P2, P2P0."""
    G = cen(*P)
    o = dict(segs=[seg(P[i], P[(i + 1) % 3]) for i in range(3)], pts=[], sides=[])
    if names:
        o['pts'] = [lab(P[i], names[i], away=G, d=d) for i in range(3) if names[i] != ' ']
    if sides:
        o['sides'] = [oside(P[i], P[(i + 1) % 3], sides[i], G, off) for i in range(3) if sides[i]]
    return o


def merge(*parts, **extra):
    o = {}
    for p in parts:
        for k, v in p.items():
            o.setdefault(k, []).extend(v)
    o.update(extra)
    return o


def nested(f, sides=None, names='ABCDE', A=None, B=None, C=None, **kw):
    """Triangle ABC with D on AB and E on AC, where DE is parallel to BC. f is AD / AB as drawn.
    `sides` labels segments by name: AD, DB, AE, EC, DE, BC."""
    A = A or pt(2.3, 4.3); B = B or pt(0, 0); C = C or pt(5.6, 0)
    D, E = mid(A, B, f), mid(A, C, f); G = cen(A, B, C); s = sides or {}
    o = dict(segs=[seg(A, B), seg(B, C), seg(C, A), seg(D, E)], sides=[],
             pts=[lab(A, names[0], 90), lab(B, names[1], 215), lab(C, names[2], -35), lab(D, names[3], 172, d=14), lab(E, names[4], 8, d=14)])
    for key, (a, b) in {'AD': (A, D), 'DB': (D, B), 'AE': (A, E), 'EC': (E, C)}.items():
        if key in s:
            o['sides'].append(oside(a, b, s[key], G, 14))
    if 'DE' in s: o['sides'].append(side(D, E, s['DE'], -12))
    if 'BC' in s: o['sides'].append(side(B, C, s['BC'], -13))
    o.update(box=[-1.0, -0.75, 6.6, 5.0], w=265, h=225, pad=12)
    o.update(kw)
    o['_pts'] = dict(A=A, B=B, C=C, D=D, E=E)
    return o


def bowtie(sides=None, kk=1.8, names='PQRSM', **kw):
    """Segments PS and QR crossing at M, with PQ parallel to RS (PQ on top). kk is RS / PQ as drawn.
    `sides` labels segments by name: PQ, RS, PM, QM, MS, MR."""
    M = pt(0, 0); P = pt(-1.2, 1.25); Q = pt(1.0, 1.25)
    S = pt(-kk * P[0], -kk * P[1]); R = pt(-kk * Q[0], -kk * Q[1]); s = sides or {}
    o = dict(segs=[seg(P, Q), seg(R, S), seg(P, S), seg(Q, R)], sides=[],
             pts=[lab(P, names[0], 150), lab(Q, names[1], 30), lab(R, names[2], 210), lab(S, names[3], -30), lab(M, names[4], 0, d=17)])
    for key, (a, b, off) in {'PQ': (P, Q, 12), 'RS': (R, S, -13), 'PM': (P, M, -12), 'QM': (Q, M, 12), 'MS': (M, S, 12), 'MR': (M, R, -12)}.items():
        if key in s:
            o['sides'].append(side(a, b, s[key], off))
    o.update(box=bbox([P, Q, R, S], 0.75), w=250, h=235, pad=12)
    o.update(kw)
    return o


def clean(o):
    """Drop helper keys before a spec goes to the page."""
    return {k: v for k, v in o.items() if not k.startswith('_')}


# --- Rule 1: two similar triangles with sides 8, 10, 12 and 12, 15, 18 (drawn to scale)
T = [pt(0, 0), pt(1.5, 2.205), pt(4, 0)]
T2 = place(T, 1.5, at=(5.9, 0))
FIGS['r_sim'] = merge(tri_parts(T, 'ABC', ['8', '10', '12']), tri_parts(T2, 'DEF', ['12', '15', '18']),
    box=[-0.7, -1.35, 12.6, 3.95], w=440, h=205, pad=12,
    alt='triangle ABC with sides AB 8, BC 10 and AC 12, and a larger similar triangle DEF with sides DE 12, EF 15 and DF 18',
    texts=[txt(pt(5.95, -1.1), 'each side of DEF is 1.5 times the matching side of ABC', cls='note')])

# --- Rule 2: the nested picture and the bowtie picture
FIGS['r_nest'] = clean(nested(0.58, alt='triangle ABC with D on side AB and E on side AC; segment DE is parallel to side BC, so triangle ADE is a smaller copy of triangle ABC',
    box=[-1.0, -1.25, 6.6, 5.0], w=255, h=240, texts=[txt(pt(2.8, -1.0), 'nested: DE is parallel to BC', cls='note')]))
FIGS['r_bow'] = bowtie(alt='segments PS and QR cross at M; segment PQ at the top is parallel to the longer segment RS at the bottom, forming triangles PQM and SRM',
    box=[-2.6, -3.5, 2.95, 2.0], w=255, h=240, texts=[txt(pt(0.18, -3.2), 'bowtie: PQ is parallel to RS', cls='note')])

# --- Rule 4: a square of side s and a square of side 3s cut into nine copies of the small one
u = 0.9
def tile(x, y): return dict(pts=[pt(x, y), pt(x + u, y), pt(x + u, y + u), pt(x, y + u)], cls='tile')
FIGS['r_sq'] = dict(box=[-0.5, -0.95, 5.6, 3.3], w=310, h=215,
    alt='a small square with side s beside a large square with side 3 s; the large square is cut into a 3 by 3 grid of 9 squares, each the size of the small one',
    polys=[tile(0, 0)] + [tile(2.3 + i * u, j * u) for i in range(3) for j in range(3)],
    sides=[side(pt(0, 0), pt(u, 0), 's', -13), side(pt(2.3, 0), pt(2.3 + 3 * u, 0), '3s', -13)],
    texts=[txt(pt(u / 2, u + 0.3), 'area: 1 tile', cls='note'), txt(pt(2.3 + 1.5 * u, 3 * u + 0.3), 'area: 9 tiles', cls='note')])

# --- Rule 5: a ring between two circles, and a slice between nested triangles
O = pt(0, 0)
def ring(r, R, **kw):
    o = dict(box=[-R - 0.25, -R - 0.25, R + 0.25, R + 0.25], w=215, h=215, regions=[dict(outer=dict(c=O, r=R), holes=[dict(c=O, r=r)])],
             circles=[dict(c=O, r=R), dict(c=O, r=r)], dots=[O])
    o.update(kw)
    return o
FIGS['r_ring'] = ring(1.65, 2.2, box=[-2.5, -3.1, 2.5, 2.5], w=225, h=240,
    alt='two circles with the same center; the ring between the smaller circle and the larger circle is shaded',
    texts=[txt(pt(0, -2.85), 'ring = large circle − small circle', cls='note')])
n5 = nested(0.5, box=[-1.0, -1.25, 6.6, 5.0], w=255, h=240,
    alt='triangle ABC with segment DE parallel to side BC; the quadrilateral DBCE between the segment and the side is shaded',
    texts=[txt(pt(2.8, -1.0), 'slice = large triangle − small triangle', cls='note')])
n5['polys'] = [dict(pts=[n5['_pts'][c] for c in 'DBCE'])]
FIGS['r_slice'] = clean(n5)

# --- Rule 6: a cube and a cube with edges twice as long, cut into eight copies of the small one
def cube(x, y, s, d, cut=False):
    F = [pt(x, y), pt(x + s, y), pt(x + s, y + s), pt(x, y + s)]
    K = [pt(p[0] + d, p[1] + d) for p in F]
    g = [seg(F[0], F[1]), seg(F[1], F[2]), seg(F[2], F[3]), seg(F[3], F[0]), seg(F[3], K[3]), seg(K[3], K[2]), seg(K[2], F[2]), seg(F[1], K[1]), seg(K[1], K[2])]
    if cut:
        g += [seg(mid(F[0], F[1]), mid(F[3], F[2]), 'thin'), seg(mid(F[0], F[3]), mid(F[1], F[2]), 'thin'),
              seg(mid(F[3], F[2]), mid(K[3], K[2]), 'thin'), seg(mid(F[3], K[3]), mid(F[2], K[2]), 'thin'),
              seg(mid(F[1], F[2]), mid(K[1], K[2]), 'thin'), seg(mid(F[1], K[1]), mid(F[2], K[2]), 'thin')]
    return g
FIGS['r_cubes'] = dict(box=[-0.5, -1.0, 6.2, 3.5], w=320, h=220,
    alt='a small cube with edge s beside a large cube with edge 2 s; the large cube is cut into 8 cubes, each the size of the small one',
    segs=cube(0, 0, 1.1, 0.42) + cube(2.6, 0, 2.2, 0.84, cut=True),
    sides=[side(pt(0, 0), pt(1.1, 0), 's', -13), side(pt(2.6, 0), pt(4.8, 0), '2s', -13)],
    texts=[txt(pt(0.75, 1.9), 'volume: 1 cube', cls='note'), txt(pt(4.1, 3.3), 'volume: 8 cubes', cls='note')])

# --- Step 1: triangle ABC and a larger similar triangle DEF, turned (AB 10, BC 14, DE 15)
T = [pt(0, 0), pt(1.0, 2.3), pt(3.6, 0)]
T2 = place(T, 1.5, deg=-18, at=(4.9, 0.9))
FIGS['s1'] = merge(tri_parts(T, 'ABC', ['10', '14', None]), tri_parts(T2, 'DEF', ['15', None, None]),
    box=bbox(T + T2, 0.8), w=400, h=215, pad=12, note=NOTE,
    alt='triangle ABC with AB 10 and BC 14, and a larger similar triangle DEF, turned slightly, with DE 15')

# --- Step 2: the nested picture with AD 8, DB 4, DE 10
FIGS['s2'] = clean(nested(0.6, {'AD': '8', 'DB': '4', 'DE': '10'}, note=NOTE,
    alt='triangle ABC with D on AB and E on AC; DE is parallel to BC; AD is 8, DB is 4 and DE is 10'))

# --- Step 4: two equilateral triangles with sides a and b (a is the longer one)
def equi(x, s): return [pt(x, 0), pt(x + s / 2, s * R3 / 2), pt(x + s, 0)]
FIGS['s4'] = merge(tri_parts(equi(0, 3.4), None, [None, None, 'a']), tri_parts(equi(4.4, 2.55), None, [None, None, 'b']),
    box=[-0.5, -0.8, 7.45, 3.3], w=330, h=190,
    alt='two equilateral triangles side by side; the larger has sides of length a and the smaller has sides of length b')

# --- Step 5: a ring (radius of the larger circle is 7/4 of the smaller)
FIGS['s5'] = ring(1.3, 2.275, alt='two circles with the same center; the region between the smaller circle and the larger circle is shaded')

# --- Skill Practice A5: two similar triangles, one turned and flipped, with equal angles marked alike
T = [pt(0, 0), pt(2, 0), pt(0.153, 2.364)]                       # U, V, W: UV = 2 (stands for 6), VW = 3 (stands for 9)
T2 = place(T, 1.3, deg=200, flip=True, at=(7.6, 2.9))
def marks(P):
    return [ang3(P[0], P[1], P[2], None, r=15), ang3(P[1], P[2], P[0], None, r=12), ang3(P[1], P[2], P[0], None, r=17)]
FIGS['fa5'] = merge(tri_parts(T, None, ['6', '9', None]), tri_parts(T2, None, ['10', 'x', None]),
    box=bbox(T + T2, 0.7), w=360, h=215, pad=12, note=NOTE, arcs=marks(T) + marks(T2),
    alt='two triangles; in each, one angle has a single arc and a second angle has a double arc. In the first triangle, the side between the marked angles is 6 and the side from the double arc to the unmarked angle is 9. In the second triangle, which is turned and flipped, the matching sides are 10 and x')

# --- Skill Practice B: nested and bowtie pictures with different numbers
FIGS['fb1'] = clean(nested(0.4, {'AD': '3', 'DB': '9', 'DE': '4'}, note=NOTE, w=240, h=210,
    alt='triangle ABC with D on AB and E on AC; DE is parallel to BC; AD is 3, DB is 9 and DE is 4'))
FIGS['fb2'] = clean(nested(0.45, {'AD': '10', 'DB': '15', 'BC': '35'}, note=NOTE, w=240, h=210,
    alt='triangle ABC with D on AB and E on AC; DE is parallel to BC; AD is 10, DB is 15 and BC is 35'))
FIGS['fb3'] = bowtie({'PQ': '8', 'RS': '12', 'PM': '6'}, kk=1.5, note=NOTE, w=235, h=220,
    alt='segments PS and QR cross at M, with PQ parallel to RS; PQ is 8, RS is 12 and PM is 6')
FIGS['fb4'] = bowtie({'PQ': '5', 'RS': '15'}, kk=2.1, note=NOTE, w=235, h=230,
    alt='segments PS and QR cross at M, with PQ parallel to RS; PQ is 5 and RS is 15')

# --- Practice 1: triangle ABC (AB 9, AC 12) and a larger similar triangle DEF (DE 15)
T = [pt(0, 0), pt(0.9, 2.1), pt(3.0, 0)]
T2 = place(T, 1.6, at=(4.9, 0))
FIGS['p1'] = merge(tri_parts(T, 'ABC', ['9', None, '12']), tri_parts(T2, 'DEF', ['15', None, None]),
    box=bbox(T + T2, 0.8), w=400, h=205, pad=12, note=NOTE,
    alt='triangle ABC with AB 9 and AC 12, and a larger similar triangle DEF with DE 15')

# --- Practice 3: the nested picture with AD 10, DB 6, DE 15
FIGS['p3'] = clean(nested(0.62, {'AD': '10', 'DB': '6', 'DE': '15'}, note=NOTE,
    alt='triangle ABC with D on AB and E on AC; DE is parallel to BC; AD is 10, DB is 6 and DE is 15'))

# --- Practice 4: two circles with centers A and B
A, B = pt(0, 0), pt(4.1, 0)
FIGS['p4'] = dict(box=[-1.6, -2.3, 6.5, 2.3], w=330, h=200, circles=[dict(c=A, r=1.26), dict(c=B, r=2.1)], dots=[A, B],
    pts=[lab(A, 'A', 0, d=12), lab(B, 'B', 0, d=12)], note=NOTE,
    alt='two separate circles: a smaller circle with center A and a larger circle with center B')

# --- Practice 6: equilateral triangles ABC (side a) and RST (side b), a is the longer one
FIGS['p6'] = merge(tri_parts(equi(0, 3.5), 'ABC', [None, None, 'a'], off=15), tri_parts(equi(5.3, 2.0), 'DEF', [None, None, 'b'], off=15),
    box=[-0.7, -0.9, 8.0, 3.75], w=350, h=200, pad=12,
    alt='equilateral triangle ABC with base AC of length a, beside a smaller equilateral triangle DEF with base DF of length b')

# --- Practice 7 and Challenge 2: the bowtie picture
FIGS['p7'] = bowtie(kk=2.0, note=NOTE, alt='segments PS and QR cross at M; PQ at the top is parallel to the longer segment RS at the bottom')
FIGS['c2'] = bowtie({'PQ': '12', 'RS': '21'}, kk=1.75, note=NOTE, alt='segments PS and QR cross at M, with PQ parallel to RS; PQ is 12 and RS is 21')

# --- Practice 8: a ring (radius of the larger circle is 5/3 of the smaller)
FIGS['p8'] = ring(1.35, 2.25, alt='two circles with the same center; the region between the smaller circle and the larger circle is shaded')

# --- Practice 9: right triangle ABC with two segments perpendicular to AC; AM : MN : NC = 1 : 2 : 2 (K above M, L above N)
A, B, C = pt(0, 0), pt(0, 3.4), pt(6.5, 0)
Q, R = pt(1.3, 0), pt(3.9, 0)
P, S = pt(1.3, 3.4 * (1 - 1.3 / 6.5)), pt(3.9, 3.4 * (1 - 3.9 / 6.5))
FIGS['p9'] = dict(box=[-0.8, -0.75, 7.2, 3.95], w=350, h=225, note=NOTE,
    polys=[dict(pts=[P, Q, R, S])],
    segs=[seg(A, B), seg(B, C), seg(C, A), seg(P, Q), seg(S, R)],
    rights=[dict(at=A, a=C, b=B, s=8), dict(at=Q, a=C, b=P, s=8), dict(at=R, a=C, b=S, s=8)],
    pts=[lab(A, 'A', 225), lab(B, 'B', 110), lab(C, 'C', 0), lab(Q, 'M', -90), lab(R, 'N', -90), lab(P, 'K', 60), lab(S, 'L', 60)],
    alt='right triangle ABC with the right angle at A, AB vertical and AC horizontal; M and N are on AC, K and L are on BC, and segments KM and LN are perpendicular to AC; quadrilateral KMNL is shaded')

# --- Practice 10: circles S and T tangent to each other inside a larger circle (radii 2, 1 and 3 as drawn)
Pc, Qc = pt(-1, 0), pt(2, 0)
FIGS['p10'] = dict(box=[-3.25, -3.25, 3.25, 3.25], w=230, h=230,
    regions=[dict(outer=dict(c=O, r=3), holes=[dict(c=Pc, r=2), dict(c=Qc, r=1)])],
    circles=[dict(c=O, r=3), dict(c=Pc, r=2), dict(c=Qc, r=1)],
    segs=[seg(pt(-3, 0), pt(3, 0), 'thin')], dots=[Pc, Qc],
    pts=[lab(Pc, 'S', 90, d=14), lab(Qc, 'T', 90, d=14)],
    alt='a large circle containing two smaller circles with centers S and T on one diameter; the smaller circles touch each other and each touches the large circle from the inside; the part of the large circle outside both smaller circles is shaded')

# --- Challenge 1: the nested picture with AD x, DB 6, DE 10, BC 25
FIGS['c1'] = clean(nested(0.42, {'AD': 'x', 'DB': '6', 'DE': '10', 'BC': '25'}, note=NOTE,
    alt='triangle ABC with D on AB and E on AC; DE is parallel to BC; AD is x, DB is 6, DE is 10 and BC is 25'))

# --- Challenge 5: two segments parallel to BC that cut AB into three equal pieces
A, B, C = pt(2.3, 4.5), pt(0, 0), pt(5.6, 0)
D, F, E, G = mid(A, B, 1 / 3), mid(A, B, 2 / 3), mid(A, C, 1 / 3), mid(A, C, 2 / 3)
FIGS['c5'] = dict(box=[-1.0, -0.75, 6.6, 5.2], w=265, h=240,
    segs=[seg(A, B), seg(B, C), seg(C, A), seg(D, E), seg(F, G)],
    ticks=[dict(a=A, b=D, n=1), dict(a=D, b=F, n=1), dict(a=F, b=B, n=1)],
    pts=[lab(A, 'A', 90), lab(B, 'B', 215), lab(C, 'C', -35), lab(D, 'D', 172, d=14), lab(F, 'F', 172, d=14), lab(E, 'E', 8, d=14), lab(G, 'G', 8, d=14)],
    alt='triangle ABC with D and F on side AB and E and G on side AC; segments DE and FG are parallel to BC, and marks show that AD, DF and FB are equal')

# --- Challenge 7: a segment parallel to BC that cuts the triangle into two regions of equal area (AD / AB is 1 over root 2)
n7 = nested(1 / R2, alt='triangle ABC with D on AB and E on AC; DE is parallel to BC; triangle ADE and quadrilateral DBCE are shaded differently to show the two regions')
n7['polys'] = [dict(pts=[n7['_pts'][c] for c in 'ADE'], cls='shade2'), dict(pts=[n7['_pts'][c] for c in 'DBCE'])]
FIGS['c7'] = clean(n7)


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
    (o.regions || []).forEach(function(g) {     // a shaded circle with circular holes (even-odd fill): a ring, or the space around inner circles
        function C(c) {
            var cx = X(c.c[0]), cy = Y(c.c[1]), r = (c.r * sc).toFixed(1);
            return 'M' + (cx - c.r * sc).toFixed(1) + ',' + cy.toFixed(1) + ' a' + r + ',' + r + ' 0 1,0 ' + (2 * c.r * sc).toFixed(1) + ',0 a' + r + ',' + r + ' 0 1,0 ' + (-2 * c.r * sc).toFixed(1) + ',0 Z';
        }
        s += '<path class="' + (g.cls || 'shade') + '" fill-rule="evenodd" d="' + [g.outer].concat(g.holes || []).map(C).join(' ') + '"/>';
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
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Similar Figures</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Similar Figures</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; SIMILAR FIGURES')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Similar Figures')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Similarity Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Similar figure rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>one scale factor runs the whole figure.</strong> Each length is multiplied by $k$, each area by $k^2$, and each volume by $k^3$. Each question asks you to find the similar figures, match their parts, and decide which power of $k$ applies.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. Sections A to D use the starred rules, and section E covers the unstarred ones. You can enter fractions as 3/2 or 1.5; both are accepted. Once you feel comfortable, try responding without pausing for long.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and eight include a figure. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type: which figures are similar, which parts match, and is the question about a length or an area? Sketch a figure if none is provided. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. For these questions it works mostly as a calculator, for example to compute $98 \cdot \dfrac{16}{49}$. You still need to set up the proportion yourself.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These seven questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each is a rule you already have, paired with a second idea (a side with a variable in it, areas inside a bowtie, a trig ratio, a percent change, a triangle cut into three bands, a volume found from a surface area, a triangle cut into two equal areas). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the ones marked <em>extra</em> lean on the unstarred rules. Two are tagged as blends, <em>trig blend</em> and <em>percent blend</em>: those pairings appear less often, so treat them as stretch practice.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time two similar figures show up. Make it an if-then. (Shape: “When a question compares the areas of two similar figures, I ______ before I multiply.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">This sheet is a companion to SAT Math 4, which covers parallel lines and the angle facts that make triangles similar: <a href="' + TRI_URL + '" ' + A_STYLE + '>SAT Math 4: Triangles &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">Most questions on this sheet start with a proportion. For practice setting one up and solving it, see <a href="' + RATIOS_URL + '" ' + A_STYLE + '>SAT Math 5: Ratios, Rates and Proportions &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>',
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

    # --- Skill Practice items can carry a figure (sections A and B); it sits between the question and the answer row
    html = replace_once(html, """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>';""",
                        """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>' + (it.fig ? fig(it.fig) : '');""")

    # --- results kit: carry each question's figure into the tutor report (practice, challenge and the Skill Practice reps that have one)
    html = replace_n(html, "stem: p.stem, trap: p.trap });", "stem: p.stem, fig: p.fig ? fig(p.fig) : '', trap: p.trap });", 2)
    html = replace_once(html, """'</b></span></div><div class="stem">' + r.i.stem + '</div>""", """'</b></span></div><div class="stem">' + (r.i.fig || '') + r.i.stem + '</div>""")
    html = replace_once(html, ": it.accept[0], q: it.q }); }", ": it.accept[0], q: it.q + (it.fig ? fig(it.fig) : '') }); }")
    html = replace_once(html, "'.nw{white-space:nowrap}table.vtab{", "'" + REPORT_FIG_CSS.replace('\\', '\\\\').replace("'", "\\'") + "' +\n        '.nw{white-space:nowrap}table.vtab{")

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', 'sat-similar-figures-sheet:rule')
    html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                        "(i === %d ? 'That was the last starred step. The next two cover ideas that come up less often.' : '')" % LAST_STARRED_STEP_INDEX)
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
