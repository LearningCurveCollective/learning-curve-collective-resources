#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-4B-Special-Right-Triangles.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the content
swaps. This sheet is the companion to SAT Math 4: Triangles. It goes deeper on one rule from that
sheet: the 45-45-90 and 30-60-90 triangles, knowing both patterns from memory, and noticing them
inside squares, circles and equilateral triangles. All questions use original numbers and figures.

It was copied from build_triangles.py and keeps that file's geoSVG figure renderer. Two things are
new here: Skill Practice items can carry a figure (the `fig` key on a FLUENCY item), and tri_fig()
draws a labeled special right triangle at any rotation, for the reps on matching sides to angles.
Answer key: verify_special_right_triangles.py (same folder) recomputes every answer."""
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
OUT = ROOT + '/test-prep/sat/SAT-Math-4B-Special-Right-Triangles.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
TRI_URL = SITE + 'test-prep/sat/SAT-Math-4-Triangles.html'
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


def memo(tag, name, body):
    """A starred block that is not a numbered rule: a memory aid that covers more than one rule."""
    return ('<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag">' + STAR + tag +
            '</span><span class="rname">' + name + '</span></div>\n' + body.strip('\n') + '\n</div>\n')


def memo_table(name, angles, roots, sides):
    """Angles, roots and sides in matching columns, so each side sits under the angle it is across from."""
    def row(label, cells):
        return '<tr><td class="fname">' + label + '</td>' + ''.join('<td>' + c + '</td>' for c in cells) + '</tr>\n'
    return ('<div class="tbl-wrap"><table class="cases memo"><thead><tr><th>' + name + '</th><th colspan="3">small to tall</th></tr></thead><tbody>\n' +
            row('Angles', angles) + row('Root them all', roots) + row('Simplify, times $x$', sides) + '</tbody></table></div>\n')


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
<p class="ref-intro">Two right triangles have fixed side ratios: the $45$-$45$-$90$ triangle and the $30$-$60$-$90$ triangle. Once you know one side of either triangle, the pattern gives you the other two. This sheet has two goals. The first is to know both patterns from memory, including which side is across from which angle. The second is to notice these triangles when a question does not name them: inside a square, a circle or an equilateral triangle. As you practice, start by identifying which special triangle the figure contains. Then decide which side you were given, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''' + rule(1, r'The $45$-$45$-$90$ triangle', True, r'''
<p class="ref-lead">A right triangle with two $45^\circ$ angles has two equal legs, so it is an isosceles right triangle. It is also half of a square, cut along the diagonal. If each leg is $x$, the hypotenuse is $x\sqrt{2}$.</p>
''' + figslot('r_45') + r'''<div class="fbox">
''' + frow('the pattern', r'$x : x : x\sqrt{2}$ &nbsp; (leg, leg, hypotenuse)') +
      frow('leg to hypotenuse', r'multiply by $\sqrt{2}$') +
      frow('hypotenuse to leg', r'divide by $\sqrt{2}$') +
      frow('why it works', r'$x^2 + x^2 = 2x^2$, and $\sqrt{2x^2} = x\sqrt{2}$') +
      frow('the order of the sides', r'$\sqrt{2}$ is about $1.41$, which is between $1$ and $2$, so $x < x\sqrt{2} < 2x$. The hypotenuse is longer than a leg, but it is not double a leg') +
      frow('how to remember it', r'<strong>Small to tall, root them all.</strong> List the angles from smallest to largest: $45^\circ$, $45^\circ$, $90^\circ$. Across from them, the sides are $x$ times $\sqrt{1}$, $\sqrt{1}$, $\sqrt{2}$. Since $\sqrt{1} = 1$, that is $x$, $x$, $x\sqrt{2}$') + r'''</div>
''' + ex('A', r'Each leg is $8$: the hypotenuse is $8\sqrt{2}$.') +
    ex('B', r'The hypotenuse is $9\sqrt{2}$: each leg is $9$.') +
    ex('C', r'The hypotenuse is $20$: each leg is $\dfrac{20}{\sqrt{2}} = 10\sqrt{2}$. Rule 3 shows that division one step at a time.') +
    note(r'The hypotenuse is across from the right angle, and it is the longest side. If a leg comes out longer than the hypotenuse, check which side you gave the $\sqrt{2}$.')) + \
rule(2, r'The $30$-$60$-$90$ triangle', True, r'''
<p class="ref-lead">A right triangle with a $30^\circ$ angle and a $60^\circ$ angle has three different side lengths. It is half of an equilateral triangle, cut along the height. Call the shortest side $x$. The hypotenuse is $2x$, and the longer leg is $x\sqrt{3}$.</p>
''' + figslot('r_30') + r'''<div class="tbl-wrap"><table class="cases"><thead><tr><th>Angle</th><th>Side across from it</th><th>Length</th></tr></thead><tbody>
<tr><td class="fname">$30^\circ$ &nbsp;(the smallest angle)</td><td>short leg</td><td>$x$</td></tr>
<tr><td class="fname">$60^\circ$</td><td>long leg</td><td>$x\sqrt{3}$</td></tr>
<tr><td class="fname">$90^\circ$ &nbsp;(the largest angle)</td><td>hypotenuse</td><td>$2x$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('the pattern', r'$x : x\sqrt{3} : 2x$ &nbsp; (short leg, long leg, hypotenuse)') +
      frow('sides follow angles', r'the smallest angle is across from the shortest side, and the largest angle is across from the longest side') +
      frow('the order of the sides', r'$\sqrt{3}$ is about $1.73$, which is between $1$ and $2$, so $x < x\sqrt{3} < 2x$') +
      frow('why it works', r'$(2x)^2 - x^2 = 3x^2$, and $\sqrt{3x^2} = x\sqrt{3}$') +
      frow('how to remember it', r'<strong>Small to tall, root them all.</strong> List the angles from smallest to largest: $30^\circ$, $60^\circ$, $90^\circ$. Across from them, the sides are $x$ times $\sqrt{1}$, $\sqrt{3}$, $\sqrt{4}$. Since $\sqrt{4} = 2$, that is $x$, $x\sqrt{3}$, $2x$') + r'''</div>
''' + ex('A', r'The short leg is $3$: the long leg is $3\sqrt{3}$ and the hypotenuse is $6$.') +
    ex('B', r'The hypotenuse is $50$: the short leg is $25$ and the long leg is $25\sqrt{3}$.') +
    ex('C', r'A right triangle has a $60^\circ$ angle, and the leg that touches that angle has length $13$. The third angle is $30^\circ$, and this leg is across from it, so it is the short leg. The other leg is $13\sqrt{3}$ and the hypotenuse is $26$.') +
    note(r'Before you write $x$ on a side, find the $30^\circ$ angle. If the figure marks only the $60^\circ$ angle, the third angle is $30^\circ$. The side across from the $30^\circ$ angle is $x$.')) + \
memo('Memory aid', 'Small to tall, root them all', r'''
<p class="ref-lead">One rhyme holds both patterns. List the angles from smallest to largest, write a square root across from each one, then simplify. The numbers under the roots are $1$, $1$, $2$ for the <span class="nw">$45$-$45$-$90$</span> triangle and $1$, $3$, $4$ for the <span class="nw">$30$-$60$-$90$</span> triangle.</p>
<div class="memo-pair">
''' + memo_table('45-45-90', [r'$45^\circ$', r'$45^\circ$', r'$90^\circ$'], [r'$\sqrt{1}$', r'$\sqrt{1}$', r'$\sqrt{2}$'], ['$x$', '$x$', r'$x\sqrt{2}$']) +
      memo_table('30-60-90', [r'$30^\circ$', r'$60^\circ$', r'$90^\circ$'], [r'$\sqrt{1}$', r'$\sqrt{3}$', r'$\sqrt{4}$'], ['$x$', r'$x\sqrt{3}$', '$2x$']) + r'''</div>
<div class="fbox">
''' + frow('say it', r'&ldquo;one, one, two&rdquo; for the <span class="nw">$45$-$45$-$90$</span> triangle, and &ldquo;one, three, four&rdquo; for the <span class="nw">$30$-$60$-$90$</span> triangle') +
      frow('recall the numbers', r'both lists start at $1$. Two equal angles repeat the $1$, and three different angles skip to $3$. The last number is the first two added: $1 + 1 = 2$ and $1 + 3 = 4$') +
      frow('why adding works', r'squaring a square root gives the number under it, so $1 + 1 = 2$ and $1 + 3 = 4$ are the Pythagorean theorem for these two triangles. If your three numbers do not add up, check the pattern') +
      frow('where each side goes', r'each side is across from the angle above it. The smallest angle is across from the shortest side, however the triangle is turned') + r'''</div>
''' + note(r'The roots belong to the pattern, not to the lengths in the question. If the hypotenuse of a <span class="nw">$30$-$60$-$90$</span> triangle is $10$, it stays $10$. It matches $2x$, so $x = 5$. Rule 3 shows how to find $x$ from any side.')) + \
rule(3, r'Find $x$ first', True, r'''
<p class="ref-lead">Each side of a special right triangle is $x$ times a fixed number. Write the pattern on the figure, set the side you know equal to its piece of the pattern, and solve for $x$. Then build the side the question asks for.</p>
<div class="tbl-wrap"><table class="forms"><thead><tr><th>Triangle</th><th>You are given</th><th>Write</th><th>Then</th></tr></thead><tbody>
<tr><td class="fname">$45$-$45$-$90$</td><td class="freads">a leg</td><td class="fmath">$x = \text{leg}$</td><td class="fex">hypotenuse $= x\sqrt{2}$</td></tr>
<tr><td class="fname">$45$-$45$-$90$</td><td class="freads">the hypotenuse</td><td class="fmath">$x\sqrt{2} = \text{hypotenuse}$</td><td class="fex">divide by $\sqrt{2}$</td></tr>
<tr><td class="fname">$30$-$60$-$90$</td><td class="freads">the short leg</td><td class="fmath">$x = \text{short leg}$</td><td class="fex">long leg $= x\sqrt{3}$, hypotenuse $= 2x$</td></tr>
<tr><td class="fname">$30$-$60$-$90$</td><td class="freads">the hypotenuse</td><td class="fmath">$2x = \text{hypotenuse}$</td><td class="fex">divide by $2$</td></tr>
<tr><td class="fname">$30$-$60$-$90$</td><td class="freads">the long leg</td><td class="fmath">$x\sqrt{3} = \text{long leg}$</td><td class="fex">divide by $\sqrt{3}$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('dividing by a root', r'multiply the top and the bottom by the root: $\dfrac{24}{\sqrt{3}} = \dfrac{24\sqrt{3}}{3} = 8\sqrt{3}$ &nbsp; and &nbsp; $\dfrac{20}{\sqrt{2}} = \dfrac{20\sqrt{2}}{2} = 10\sqrt{2}$') +
      frow('in words', r'dividing by $\sqrt{2}$ gives half of the number, times $\sqrt{2}$. Dividing by $\sqrt{3}$ gives a third of the number, times $\sqrt{3}$') +
      frow('squaring a root', r'$(5\sqrt{2})^2 = 25 \cdot 2 = 50$ &nbsp; and &nbsp; $(4\sqrt{3})^2 = 16 \cdot 3 = 48$') +
      frow('size check', r'moving to a longer side makes the number larger, and moving to a shorter side makes it smaller') + r'''</div>
''' + ex('A', r'A $30$-$60$-$90$ triangle with long leg $24$: $x\sqrt{3} = 24$, so $x = 8\sqrt{3}$. The hypotenuse is $2x = 16\sqrt{3}$.') +
    ex('B', r'A $45$-$45$-$90$ triangle with hypotenuse $30$: $x\sqrt{2} = 30$, so each leg is $15\sqrt{2}$.') +
    ex('C', r'A $30$-$60$-$90$ triangle with long leg $5$: $x = \dfrac{5}{\sqrt{3}} = \dfrac{5\sqrt{3}}{3}$. The numbers do not have to come out as whole numbers for the pattern to work.') +
    ex('D', r'A $45$-$45$-$90$ triangle with hypotenuse $6$: each leg is $3\sqrt{2}$, and the area is $\tfrac{1}{2}(3\sqrt{2})(3\sqrt{2}) = \tfrac{1}{2}(18) = 9$.') +
    note(r'Get $x$ by itself before you do anything else. To undo a multiplication by $\sqrt{3}$, divide by $\sqrt{3}$. Desmos can confirm a simplified radical: $24/\sqrt{3}$ and $8\sqrt{3}$ both show about $13.86$.')) + \
rule(4, r'Squares and circles: where the $45$-$45$-$90$ triangle appears', True, r'''
<p class="ref-lead">The diagonal of a square cuts it into two $45$-$45$-$90$ triangles, so the side and the diagonal of a square follow the pattern $s : s\sqrt{2}$. Circles bring in the same triangle when a square is drawn inside a circle or around one. A rectangle that is not a square is different: its diagonal does not make $45^\circ$ angles.</p>
<div class="fig-row">''' + figslot('r_sqd').strip('\n') + figslot('r_sqin').strip('\n') + figslot('r_cin').strip('\n') + r'''</div>
<div class="fbox">
''' + frow('square with side $s$', r'diagonal $= s\sqrt{2}$') +
      frow('square with diagonal $d$', r'side $= \dfrac{d}{\sqrt{2}}$, &nbsp; area $= \dfrac{d^2}{2}$') +
      frow('square inscribed in a circle', r'the corners of the square are on the circle, so the diagonal of the square is a diameter of the circle') +
      frow('circle inscribed in a square', r'the circle touches all four sides, so the side of the square equals the diameter of the circle') +
      frow('isosceles right triangle', r'a right triangle with two equal legs is a $45$-$45$-$90$ triangle, whether or not the angles are marked') + r'''</div>
''' + ex('A', r'A square with side $15$ has a diagonal of $15\sqrt{2}$.') +
    ex('B', r'A square with diagonal $22$ has area $\dfrac{22^2}{2} = 242$. Each side is $11\sqrt{2}$, and $(11\sqrt{2})^2 = 242$ agrees.') +
    ex('C', r'A square is inscribed in a circle of radius $3$. The diagonal of the square is the diameter, $6$. Each side is $\dfrac{6}{\sqrt{2}} = 3\sqrt{2}$, and the area is $18$.') +
    ex('D', r'A circle is inscribed in a square whose diagonal is $8\sqrt{2}$. The side of the square is $8$, so the diameter of the circle is $8$ and the radius is $4$.') +
    note(r'If the diagonal of the square is not drawn, draw it. Then decide what matches the diameter of the circle: the diagonal when the square is inside the circle, the side when the circle is inside the square.')) + \
rule(5, r'Equilateral triangles: where the $30$-$60$-$90$ triangle appears', True, r'''
<p class="ref-lead">An equilateral triangle has three equal sides and three $60^\circ$ angles. Its height cuts it into two $30$-$60$-$90$ triangles. In each one, the hypotenuse is a side of the equilateral triangle, the short leg is half of the base, and the long leg is the height. The height and area formulas come from that picture, so you can rebuild them whenever you need them.</p>
''' + figslot('r_eq') + r'''<div class="fbox">
''' + frow('short leg', r'half of the base: $\dfrac{s}{2}$') +
      frow('height (the long leg)', r'$\dfrac{s}{2} \cdot \sqrt{3} = \dfrac{s\sqrt{3}}{2}$') +
      frow('area', r'$\dfrac{1}{2} \cdot \text{base} \cdot \text{height}$ $= \dfrac{1}{2} \cdot s \cdot \dfrac{s\sqrt{3}}{2}$ $= \dfrac{s^2\sqrt{3}}{4}$') +
      frow('from the area to the side', r'set $\dfrac{s^2\sqrt{3}}{4}$ equal to the area, divide both sides by $\sqrt{3}$, and solve for $s$') +
      frow('from the height to the side', r'the height is $x\sqrt{3}$: solve for $x$, then double it') + r'''</div>
''' + ex('A', r'Side $6$: the short leg is $3$, the height is $3\sqrt{3}$, and the area is $\tfrac{1}{2}(6)(3\sqrt{3}) = 9\sqrt{3}$. The formula agrees: $\dfrac{6^2\sqrt{3}}{4} = 9\sqrt{3}$.') +
    ex('B', r'Area $64\sqrt{3}$: $\dfrac{s^2\sqrt{3}}{4} = 64\sqrt{3}$, so $\dfrac{s^2}{4} = 64$. Then $s^2 = 256$ and $s = 16$.') +
    ex('C', r'Height $9\sqrt{3}$: the short leg is $9$, so each side is $18$.') +
    ex('D', r'Height $6$: $x\sqrt{3} = 6$, so $x = 2\sqrt{3}$ and each side is $4\sqrt{3}$. The area is $\tfrac{1}{2}(4\sqrt{3})(6) = 12\sqrt{3}$.') +
    note(r'The Bluebook reference sheet shows both special right triangles, but it does not list the height or the area of an equilateral triangle. If you forget $\dfrac{s^2\sqrt{3}}{4}$, draw the height and use $\tfrac{1}{2} \cdot \text{base} \cdot \text{height}$. The Bluebook Tools tab of <a href="' + DESMOS1_URL + r'" target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;">SAT Desmos 1: Core Moves</a> has a copy of the reference sheet.')) + \
rule(6, 'More figures built from these triangles', False, r'''
<p class="ref-lead">A few other figures contain the same two triangles. In each one, add a height, a radius or a diagonal, and a $30$-$60$-$90$ or $45$-$45$-$90$ triangle appears.</p>
<div class="fig-row">''' + figslot('r_hex').strip('\n') + figslot('r_iso').strip('\n') + r'''</div>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Figure</th><th>What to draw</th><th>What you get</th></tr></thead><tbody>
<tr><td class="fname">Regular hexagon with side $s$</td><td>segments from the center to each corner</td><td>six equilateral triangles with side $s$, so the area is $6 \cdot \dfrac{s^2\sqrt{3}}{4}$</td></tr>
<tr><td class="fname">Isosceles triangle with a $120^\circ$ angle</td><td>the height from the $120^\circ$ angle</td><td>two $30$-$60$-$90$ triangles; the third side is an equal side times $\sqrt{3}$</td></tr>
<tr><td class="fname">Two radii that are $60^\circ$ apart</td><td>the chord between their endpoints</td><td>an equilateral triangle, so the chord equals the radius</td></tr>
<tr><td class="fname">Two radii that are $90^\circ$ apart</td><td>the chord between their endpoints</td><td>a $45$-$45$-$90$ triangle, so the chord is $r\sqrt{2}$</td></tr>
<tr><td class="fname">Rhombus with a $60^\circ$ angle</td><td>the shorter diagonal</td><td>two equilateral triangles</td></tr>
</tbody></table></div>
''' + ex('A', r'A regular hexagon with side $2$: each of the six triangles has area $\dfrac{2^2\sqrt{3}}{4} = \sqrt{3}$, so the hexagon has area $6\sqrt{3}$.') +
    ex('B', r'An isosceles triangle has two sides of length $8$ with a $120^\circ$ angle between them. The height from that angle is the short leg of each $30$-$60$-$90$ triangle: $4$. Each long leg is $4\sqrt{3}$, so the third side is $8\sqrt{3}$ and the area is $\tfrac{1}{2}(8\sqrt{3})(4) = 16\sqrt{3}$.') +
    ex('C', r'In a circle of radius $9$, two radii that are $60^\circ$ apart have a chord of $9$ between their endpoints. Two radii that are $90^\circ$ apart have a chord of $9\sqrt{2}$.') +
    note(r'These figures come up less often than squares and equilateral triangles. The approach is the same: find the $30^\circ$, $45^\circ$ or $60^\circ$ angle, add the segment that makes a right angle, and use the pattern.')) + \
rule(7, r'Sine, cosine and tangent of $30^\circ$, $45^\circ$ and $60^\circ$', False, r'''
<p class="ref-lead">If you have studied right triangle trigonometry, the two patterns also give exact values of sine, cosine and tangent at $30^\circ$, $45^\circ$ and $60^\circ$. Sketch the triangle with $x = 1$, find the sides opposite and adjacent to the angle you are using, and read the ratio. The size of the triangle does not matter, because $x$ cancels.</p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Angle</th><th>sine</th><th>cosine</th><th>tangent</th></tr></thead><tbody>
<tr><td class="fname">$30^\circ$</td><td>$\dfrac{1}{2}$</td><td>$\dfrac{\sqrt{3}}{2}$</td><td>$\dfrac{1}{\sqrt{3}} = \dfrac{\sqrt{3}}{3}$</td></tr>
<tr><td class="fname">$45^\circ$</td><td>$\dfrac{1}{\sqrt{2}} = \dfrac{\sqrt{2}}{2}$</td><td>$\dfrac{\sqrt{2}}{2}$</td><td>$1$</td></tr>
<tr><td class="fname">$60^\circ$</td><td>$\dfrac{\sqrt{3}}{2}$</td><td>$\dfrac{1}{2}$</td><td>$\sqrt{3}$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('the three ratios', r'$\sin = \dfrac{\text{opposite}}{\text{hypotenuse}}$, &nbsp; $\cos = \dfrac{\text{adjacent}}{\text{hypotenuse}}$, &nbsp; $\tan = \dfrac{\text{opposite}}{\text{adjacent}}$') +
      frow('a pattern to notice', r'$\sin 30^\circ = \cos 60^\circ$ and $\sin 60^\circ = \cos 30^\circ$, because the two angles belong to the same triangle') +
      frow('small to tall again', r'for $30^\circ$, $45^\circ$, $60^\circ$, sine is $\dfrac{\sqrt{1}}{2}$, $\dfrac{\sqrt{2}}{2}$, $\dfrac{\sqrt{3}}{2}$. Cosine is the same list in reverse') +
      frow('in radians', r'$30^\circ = \dfrac{\pi}{6}$, &nbsp; $45^\circ = \dfrac{\pi}{4}$, &nbsp; $60^\circ = \dfrac{\pi}{3}$') + r'''</div>
''' + ex('A', r'In a $30$-$60$-$90$ triangle with sides $1$, $\sqrt{3}$ and $2$, the side opposite the $30^\circ$ angle is $1$ and the hypotenuse is $2$, so $\sin 30^\circ = \dfrac{1}{2}$.') +
    ex('B', r'A right triangle has a hypotenuse of $10$ and a $30^\circ$ angle. The side opposite that angle is $10 \cdot \sin 30^\circ = 5$. That is the short leg, half of the hypotenuse, as the pattern says.') +
    note(r'There is no separate list to memorize here. Sketch the triangle, label it $1$, $\sqrt{3}$, $2$ or $1$, $1$, $\sqrt{2}$, and read the ratio.')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common setup and interpretation mistakes. Review them so you know what to check when an answer seems off.</p>
''' + mistake(1, r'putting $x\sqrt{3}$ on the hypotenuse', r'In a $30$-$60$-$90$ triangle the hypotenuse is $2x$. Since $\sqrt{3}$ is about $1.73$, the side $x\sqrt{3}$ is shorter than $2x$, so it is the longer leg.') + \
      mistake(2, r'doubling a leg of a $45$-$45$-$90$ triangle', r'The hypotenuse of a $45$-$45$-$90$ triangle is $x\sqrt{2}$, which is about $1.41x$. The side that doubles belongs to the $30$-$60$-$90$ triangle.') + \
      mistake(3, r'calling the given side $x$ without checking', r'The given side might be the long leg or the hypotenuse. Find the $30^\circ$ angle first: the side across from it is $x$. Then decide whether the given length is $x$, $x\sqrt{3}$ or $2x$.') + \
      mistake(4, 'multiplying by the root when the side should get shorter', r'With a long leg of $24$, the short leg is $\dfrac{24}{\sqrt{3}} = 8\sqrt{3}$, which is about $13.9$. Multiplying gives $24\sqrt{3}$, about $41.6$, which is longer than the long leg. Compare sizes after each step.') + \
      mistake(5, 'using half of the base as the height of an equilateral triangle', r'With a side of $30$, half of the base is $15$, but the height is the long leg, $15\sqrt{3}$. The area is $\tfrac{1}{2}(30)(15\sqrt{3}) = 225\sqrt{3}$, not $\tfrac{1}{2}(30)(15)$.') + \
      mistake(6, 'treating a rectangle like a square', r'A square is the only rectangle whose diagonal makes $45^\circ$ angles with its sides. For another rectangle, use the Pythagorean theorem, unless the question gives a $30^\circ$ or $60^\circ$ angle.') + \
      mistake(7, 'using the diameter as the side of an inscribed square', r'When a square is inscribed in a circle, the diameter is the diagonal of the square. The side is the diameter divided by $\sqrt{2}$.') + \
      mistake(8, r'stopping at $x$', r'After you find $x$, reread the question. It may ask for the hypotenuse, a perimeter, an area or a radius.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: The 45-45-90 triangle",
  "rule": r"$x : x : x\sqrt{2}$ &nbsp;·&nbsp; two equal legs, and the hypotenuse is a leg times $\sqrt{2}$",
  "say": r"A right triangle with one $45^\circ$ angle has a second $45^\circ$ angle, because the two acute angles add to $90^\circ$. Equal angles are across from equal sides, so the two legs match. Write $x$ on both legs and $x\sqrt{2}$ on the hypotenuse, then fill in what you know.",
  "fig": "s1",
  "prob": r"In the figure above, triangle $ABC$ has a right angle at $C$, and the measure of angle $A$ is $45^\circ$. If $AC = 9$, what is the length of $\overline{BC}$? What is the length of $\overline{AB}$?",
  "sol": r"<strong>Step 1: find the third angle.</strong> Angle $B$ measures $90 - 45 = 45$ degrees.<br><strong>Step 2: equal angles, equal sides.</strong> $\overline{BC}$ is across from angle $A$, and $\overline{AC}$ is across from angle $B$. The angles are equal, so $BC = AC = 9$.<br><strong>Step 3: the hypotenuse.</strong> $AB = 9\sqrt{2}$.<br><strong>Check:</strong> $9^2 + 9^2 = 162$, and $(9\sqrt{2})^2 = 81 \cdot 2 = 162$. ✓",
  "trap": r"Writing $AB = 18$. Doubling belongs to the $30$-$60$-$90$ triangle. Here the hypotenuse is a leg times $\sqrt{2}$, which is about $12.7$.",
  "micro": {"q": r"The hypotenuse of a $45$-$45$-$90$ triangle has length $17\sqrt{2}$. The length of each leg is", "accept": ["17"],
            "exp": r"The hypotenuse is $x\sqrt{2}$, so $x\sqrt{2} = 17\sqrt{2}$ and $x = 17$."}},
 {"ess": True, "name": "Rule 2: The 30-60-90 triangle",
  "rule": r"$x : x\sqrt{3} : 2x$ &nbsp;·&nbsp; $30^\circ$ is across from $x$, $60^\circ$ is across from $x\sqrt{3}$, $90^\circ$ is across from $2x$",
  "say": r"Sides follow angles: the smallest angle is across from the shortest side. Find the $30^\circ$ angle first, even when the figure marks only the $60^\circ$ angle. The side across from the $30^\circ$ angle is $x$, the hypotenuse is $2x$, and the remaining leg is $x\sqrt{3}$.",
  "fig": "s2",
  "prob": r"In the figure above, triangle $DEF$ has a right angle at $E$, and the measure of angle $D$ is $60^\circ$. If $DE = 15$, what is the length of $\overline{DF}$? What is the length of $\overline{EF}$?",
  "sol": r"<strong>Step 1: find the $30^\circ$ angle.</strong> Angle $F$ measures $90 - 60 = 30$ degrees.<br><strong>Step 2: match each side to the angle across from it.</strong> $\overline{DE}$ is across from angle $F$, so it is the short leg: $x = 15$.<br><strong>Step 3: build the other sides.</strong> $\overline{DF}$ is across from the right angle, so it is the hypotenuse: $2x = 30$. $\overline{EF}$ is across from the $60^\circ$ angle, so it is the long leg: $15\sqrt{3}$.<br><strong>Check:</strong> $15^2 + (15\sqrt{3})^2 = 225 + 675 = 900 = 30^2$. ✓",
  "trap": r"Treating $\overline{DE}$ as the long leg because it touches the marked $60^\circ$ angle. A side goes with the angle across from it, not the angle beside it. $\overline{DE}$ is across from the $30^\circ$ angle at $F$.",
  "micro": {"q": r"In a $30$-$60$-$90$ triangle, the hypotenuse has length $46$. The leg across from the $60^\circ$ angle has length $k\sqrt{3}$. Then $k =$", "accept": ["23"],
            "exp": r"The short leg is half of the hypotenuse: $x = 23$. The leg across from the $60^\circ$ angle is the long leg, $23\sqrt{3}$."}},
 {"ess": True, "name": "Rule 3: Find x first",
  "rule": r"write the pattern &nbsp;·&nbsp; set the known side equal to its piece &nbsp;·&nbsp; solve for $x$ &nbsp;·&nbsp; build the side you need",
  "say": r"When the given side is the long leg or the hypotenuse, it is $x$ times a number. Write that as an equation and divide to get $x$ by itself. To divide by a root, multiply the top and the bottom by that root.",
  "fig": "s3",
  "prob": r"In the figure above, triangle $JKL$ has a right angle at $K$, and the measure of angle $L$ is $30^\circ$. If $KL = 21$, what is the length of $\overline{JK}$? What is the length of $\overline{JL}$?",
  "sol": r"<strong>Step 1: write the pattern on the figure.</strong> $\overline{JK}$ is across from the $30^\circ$ angle, so it is $x$. $\overline{KL}$ is across from angle $J$, which measures $60^\circ$, so it is $x\sqrt{3}$. $\overline{JL}$ is the hypotenuse, $2x$.<br><strong>Step 2: write the equation and solve.</strong> $x\sqrt{3} = 21$, so $x = \dfrac{21}{\sqrt{3}} = \dfrac{21\sqrt{3}}{3} = 7\sqrt{3}$. That is $JK$.<br><strong>Step 3: the hypotenuse.</strong> $JL = 2x = 14\sqrt{3}$.<br><strong>Check:</strong> $(7\sqrt{3})^2 + 21^2 = 147 + 441 = 588$, and $(14\sqrt{3})^2 = 196 \cdot 3 = 588$. ✓",
  "trap": r"Multiplying $21$ by $\sqrt{3}$. The long leg is already $x\sqrt{3}$, so getting back to $x$ means dividing. A size check helps: the short leg has to come out shorter than $21$, and $7\sqrt{3}$ is about $12.1$.",
  "micro": {"q": r"A $45$-$45$-$90$ triangle has a hypotenuse of length $22$. Each leg has length $k\sqrt{2}$. Then $k =$", "accept": ["11"],
            "exp": r"$x\sqrt{2} = 22$, so $x = \dfrac{22}{\sqrt{2}} = \dfrac{22\sqrt{2}}{2} = 11\sqrt{2}$."}},
 {"ess": True, "name": "Rule 4: Squares and circles",
  "rule": r"square: diagonal $= s\sqrt{2}$ &nbsp;·&nbsp; square inside a circle: diagonal $=$ diameter &nbsp;·&nbsp; circle inside a square: side $=$ diameter",
  "say": r"A square cut along its diagonal gives two $45$-$45$-$90$ triangles. When a figure pairs a square with a circle, decide which part of the square matches the diameter. If the corners of the square are on the circle, the diagonal is a diameter. If the circle touches the sides of the square from the inside, the side equals the diameter.",
  "fig": "s4",
  "prob": r"In the figure above, square $ABCD$ is inscribed in a circle with center $O$, and the radius of the circle is $5$. What is the side length of the square? What is the area of the square?",
  "sol": r"<strong>Step 1: the diagonal.</strong> Diagonal $\overline{AC}$ passes through $O$, so it is a diameter: $AC = 10$.<br><strong>Step 2: the side.</strong> Triangle $ABC$ is a $45$-$45$-$90$ triangle with hypotenuse $10$. So $x\sqrt{2} = 10$, and $x = \dfrac{10}{\sqrt{2}} = 5\sqrt{2}$.<br><strong>Step 3: the area.</strong> $(5\sqrt{2})^2 = 25 \cdot 2 = 50$.<br><strong>A shorter path to the area:</strong> the area of a square is half the square of its diagonal, $\dfrac{10^2}{2} = 50$.",
  "trap": r"Using the diameter as the side of the square, which gives an area of $100$. The diameter runs from corner to corner, so it is the diagonal. The side is shorter: $5\sqrt{2}$ is about $7.1$.",
  "micro": {"q": r"A circle is inscribed in a square. The diagonal of the square has length $12\sqrt{2}$. The radius of the circle is", "accept": ["6"],
            "exp": r"The side of the square is $12$. The circle touches all four sides, so its diameter is $12$ and its radius is $6$."}},
 {"ess": True, "name": "Rule 5: Equilateral triangles",
  "rule": r"height $= \dfrac{s\sqrt{3}}{2}$ &nbsp;·&nbsp; area $= \dfrac{s^2\sqrt{3}}{4}$ &nbsp;·&nbsp; both come from the $30$-$60$-$90$ triangle",
  "say": r"Draw the height of an equilateral triangle and you have two $30$-$60$-$90$ triangles. The hypotenuse of each one is a full side, the short leg is half of the base, and the height is the long leg. The area is then $\tfrac{1}{2} \cdot \text{base} \cdot \text{height}$, with a full side as the base.",
  "fig": "s5",
  "prob": r"In the figure above, triangle $PQR$ is equilateral, each side has length $8$, and $\overline{PM}$ is perpendicular to $\overline{QR}$. What is the length of $\overline{PM}$? What is the area of triangle $PQR$?",
  "sol": r"<strong>Step 1: find the $30$-$60$-$90$ triangle.</strong> In triangle $PMQ$, the hypotenuse is $PQ = 8$ and the short leg is $QM = 4$, half of the base.<br><strong>Step 2: the height.</strong> $\overline{PM}$ is the long leg: $4\sqrt{3}$.<br><strong>Step 3: the area.</strong> $\tfrac{1}{2} \cdot 8 \cdot 4\sqrt{3} = 16\sqrt{3}$.<br><strong>Check with the formula:</strong> $\dfrac{8^2\sqrt{3}}{4} = \dfrac{64\sqrt{3}}{4} = 16\sqrt{3}$. ✓",
  "trap": r"Using $4$ or $8$ as the height. Half of the base is the short leg, and a full side is the hypotenuse. The height is the long leg, $4\sqrt{3}$, which is about $6.9$: longer than half of the base and shorter than a side.",
  "micro": {"q": r"The area of an equilateral triangle is $100\sqrt{3}$. The length of each side is", "accept": ["20"],
            "exp": r"$\dfrac{s^2\sqrt{3}}{4} = 100\sqrt{3}$. Divide both sides by $\sqrt{3}$ to get $\dfrac{s^2}{4} = 100$. Then $s^2 = 400$ and $s = 20$."}},
 {"ess": False, "name": "Rule 6: More figures built from these triangles",
  "rule": r"regular hexagon $=$ six equilateral triangles &nbsp;·&nbsp; a $120^\circ$ isosceles triangle $=$ two $30$-$60$-$90$ triangles",
  "say": r"A regular hexagon has six equal sides. Segments from its center to its corners make six triangles. Each has a $60^\circ$ angle at the center between two equal sides, so each one is equilateral. Whatever you find for one of the triangles, the hexagon has six of them.",
  "fig": "s6",
  "prob": r"The figure above shows a regular hexagon with sides of length $4$. What is the area of the hexagon? What is the distance between two opposite sides?",
  "sol": r"<strong>Step 1: one triangle.</strong> Each of the six equilateral triangles has side $4$, so its area is $\dfrac{4^2\sqrt{3}}{4} = 4\sqrt{3}$.<br><strong>Step 2: six of them.</strong> The hexagon has area $6 \cdot 4\sqrt{3} = 24\sqrt{3}$.<br><strong>Step 3: side to side.</strong> The distance between two opposite sides is two heights of the small triangles. Each height is $2\sqrt{3}$, so the distance is $4\sqrt{3}$.",
  "trap": r"Using $8$ for the distance between opposite sides. From corner to opposite corner is two sides of the small triangles, which is $8$. From side to opposite side is two heights, $4\sqrt{3}$, which is about $6.9$.",
  "micro": {"q": r"An isosceles triangle has two sides of length $10$ and an angle of $120^\circ$ between them. The length of the third side is $k\sqrt{3}$. Then $k =$", "accept": ["10"],
            "exp": r"The height from the $120^\circ$ angle makes two $30$-$60$-$90$ triangles, each with a hypotenuse of $10$. The short leg is $5$ and the long leg is $5\sqrt{3}$. The third side is two long legs: $10\sqrt{3}$."}},
 {"ess": False, "name": "Rule 7: Sine, cosine and tangent from the two triangles",
  "rule": r"$\sin = \dfrac{\text{opposite}}{\text{hypotenuse}}$ &nbsp;·&nbsp; $\cos = \dfrac{\text{adjacent}}{\text{hypotenuse}}$ &nbsp;·&nbsp; $\tan = \dfrac{\text{opposite}}{\text{adjacent}}$",
  "say": r"This step is for students who have studied right triangle trigonometry. The exact values at $30^\circ$, $45^\circ$ and $60^\circ$ are ratios of sides in the two special triangles. Sketch the triangle, write the pattern on it with $x = 1$, and read the ratio from the angle you are using.",
  "prob": r"In triangle $ABC$, angle $C$ is a right angle and the measure of angle $A$ is $60^\circ$. What are the values of $\sin A$, $\cos A$ and $\tan A$?",
  "sol": r"<strong>Step 1: sketch and label.</strong> Angle $B$ measures $30^\circ$. $\overline{AC}$ is across from it, so $AC = 1$. $\overline{BC}$ is across from the $60^\circ$ angle, so $BC = \sqrt{3}$. The hypotenuse is $AB = 2$.<br><strong>Step 2: name the sides from angle $A$.</strong> The opposite side is $\overline{BC}$, and the adjacent side is $\overline{AC}$.<br><strong>Step 3: read the ratios.</strong> $\sin A = \dfrac{\sqrt{3}}{2}$, $\cos A = \dfrac{1}{2}$, and $\tan A = \dfrac{\sqrt{3}}{1} = \sqrt{3}$.",
  "trap": r"Naming opposite and adjacent from the other acute angle. From the $60^\circ$ angle, the opposite side is the long leg. From the $30^\circ$ angle, the opposite side is the short leg, which is why $\sin 30^\circ = \dfrac{1}{2}$ and $\sin 60^\circ = \dfrac{\sqrt{3}}{2}$.",
  "micro": {"q": r"The value of $\sin 30^\circ$ is", "accept": ["1/2", "0.5", ".5"],
            "exp": r"In a $30$-$60$-$90$ triangle, the side opposite the $30^\circ$ angle is $x$ and the hypotenuse is $2x$: $\dfrac{x}{2x} = \dfrac{1}{2}$."}},
]
LAST_STARRED_STEP_INDEX = 4  # 0-based index of the last starred step (Rule 5)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
RATIOS = [r"$\sqrt{2}$", r"$\sqrt{3}$", "$2$", "$3$"]
FLUENCY = [
 {"sec": "A. The two patterns, from memory", "items": [
   {"mc": True, "q": r"The side lengths of a $45$-$45$-$90$ triangle, from shortest to longest, are in the ratio", "opts": [r"$x : x : x\sqrt{2}$", r"$x : x\sqrt{3} : 2x$", r"$x : x : 2x$", r"$x : x\sqrt{2} : 2x$"], "correct": 0, "exp": r"Small to tall, root them all: $\sqrt{1}$, $\sqrt{1}$, $\sqrt{2}$. That is two equal legs of $x$ and a hypotenuse of $x\sqrt{2}$."},
   {"mc": True, "q": r"The side lengths of a $30$-$60$-$90$ triangle, from shortest to longest, are in the ratio", "opts": [r"$x : x : x\sqrt{2}$", r"$x : 2x : x\sqrt{3}$", r"$x : x\sqrt{3} : 2x$", r"$x : x\sqrt{2} : x\sqrt{3}$"], "correct": 2, "exp": r"Small to tall, root them all: $\sqrt{1}$, $\sqrt{3}$, $\sqrt{4}$. That is short leg $x$, long leg $x\sqrt{3}$, hypotenuse $2x$. Since $\sqrt{3}$ is less than $\sqrt{4}$, the long leg is shorter than the hypotenuse."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle, the side across from the $30^\circ$ angle is", "opts": [r"the long leg, $x\sqrt{3}$", "the short leg, $x$", "the hypotenuse, $2x$", "either leg, depending on the figure"], "correct": 1, "exp": r"The smallest angle is across from the shortest side, however the triangle is turned."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle with short leg $x$, the side across from the $60^\circ$ angle has length", "opts": ["$x$", r"$x\sqrt{2}$", r"$x\sqrt{3}$", "$2x$"], "correct": 2, "exp": r"The $60^\circ$ angle is the middle angle, so it is across from the middle side: the long leg, $x\sqrt{3}$."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle, the hypotenuse is how many times as long as the short leg?", "opts": RATIOS, "correct": 2, "exp": r"The hypotenuse is $2x$ and the short leg is $x$."},
   {"mc": True, "q": r"In a $45$-$45$-$90$ triangle, the hypotenuse is how many times as long as a leg?", "opts": RATIOS, "correct": 0, "exp": r"The hypotenuse is $x\sqrt{2}$ and each leg is $x$. Doubling belongs to the $30$-$60$-$90$ triangle."},
   {"mc": True, "q": r"A square is cut along its diagonal, and an equilateral triangle is cut along its height. In that order, the pieces are", "opts": [r"$30$-$60$-$90$ triangles, then $45$-$45$-$90$ triangles", r"$45$-$45$-$90$ triangles, then $30$-$60$-$90$ triangles", r"$45$-$45$-$90$ triangles both times", r"$30$-$60$-$90$ triangles both times"], "correct": 1, "exp": r"The diagonal of a square splits a $90^\circ$ corner into two $45^\circ$ angles. The height of an equilateral triangle splits a $60^\circ$ corner into two $30^\circ$ angles."},
 ]},
 {"sec": "B. 45-45-90: one side gives the others", "items": [
   {"mc": True, "q": r"Each leg of a $45$-$45$-$90$ triangle has length $12$. The length of the hypotenuse is", "opts": [r"$6\sqrt{2}$", r"$12\sqrt{2}$", r"$12\sqrt{3}$", "$24$"], "correct": 1, "exp": r"From a leg to the hypotenuse, multiply by $\sqrt{2}$."},
   {"q": r"The hypotenuse of a $45$-$45$-$90$ triangle has length $19\sqrt{2}$. The length of each leg is", "accept": ["19"], "exp": r"$x\sqrt{2} = 19\sqrt{2}$, so $x = 19$."},
   {"mc": True, "q": r"The hypotenuse of a $45$-$45$-$90$ triangle has length $8$. The length of each leg is", "opts": ["$4$", r"$4\sqrt{2}$", r"$4\sqrt{3}$", r"$8\sqrt{2}$"], "correct": 1, "exp": r"$x\sqrt{2} = 8$, so $x = \dfrac{8}{\sqrt{2}} = \dfrac{8\sqrt{2}}{2} = 4\sqrt{2}$. A leg is shorter than the hypotenuse, and $4\sqrt{2}$ is about $5.7$."},
   {"q": r"Each leg of a $45$-$45$-$90$ triangle has length $3\sqrt{2}$. The length of the hypotenuse is", "accept": ["6"], "exp": r"$3\sqrt{2} \cdot \sqrt{2} = 3 \cdot 2 = 6$."},
   {"q": r"The hypotenuse of a $45$-$45$-$90$ triangle has length $26$. Each leg has length $k\sqrt{2}$. Then $k =$", "accept": ["13"], "exp": r"$\dfrac{26}{\sqrt{2}} = \dfrac{26\sqrt{2}}{2} = 13\sqrt{2}$."},
   {"q": r"The hypotenuse of a $45$-$45$-$90$ triangle has length $10$. The area of the triangle is", "accept": ["25"], "exp": r"Each leg is $\dfrac{10}{\sqrt{2}} = 5\sqrt{2}$. The legs are the base and the height: $\tfrac{1}{2}(5\sqrt{2})(5\sqrt{2}) = \tfrac{1}{2}(50) = 25$."},
 ]},
 {"sec": "C. 30-60-90: find x first", "items": [
   {"q": r"In a $30$-$60$-$90$ triangle, the shorter leg has length $16$. The length of the hypotenuse is", "accept": ["32"], "exp": r"The hypotenuse is twice the short leg."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle, the shorter leg has length $10$. The length of the longer leg is", "opts": [r"$5\sqrt{3}$", r"$10\sqrt{2}$", r"$10\sqrt{3}$", "$20$"], "correct": 2, "exp": r"The long leg is the short leg times $\sqrt{3}$. The side that doubles is the hypotenuse, $20$."},
   {"q": r"In a $30$-$60$-$90$ triangle, the hypotenuse has length $28$. The length of the shorter leg is", "accept": ["14"], "exp": r"$2x = 28$, so $x = 14$."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle, the hypotenuse has length $12$. The length of the longer leg is", "opts": ["$6$", r"$6\sqrt{2}$", r"$6\sqrt{3}$", r"$12\sqrt{3}$"], "correct": 2, "exp": r"Find $x$ first: $2x = 12$, so $x = 6$. The long leg is $6\sqrt{3}$."},
   {"q": r"In a $30$-$60$-$90$ triangle, the longer leg has length $4\sqrt{3}$. The length of the shorter leg is", "accept": ["4"], "exp": r"$x\sqrt{3} = 4\sqrt{3}$, so $x = 4$."},
   {"q": r"In a $30$-$60$-$90$ triangle, the longer leg has length $17\sqrt{3}$. The length of the hypotenuse is", "accept": ["34"], "exp": r"$x = 17$, and the hypotenuse is $2x = 34$."},
   {"mc": True, "q": r"In a $30$-$60$-$90$ triangle, the longer leg has length $6$. The length of the shorter leg is", "opts": ["$3$", r"$2\sqrt{3}$", r"$3\sqrt{3}$", r"$6\sqrt{3}$"], "correct": 1, "exp": r"$x\sqrt{3} = 6$, so $x = \dfrac{6}{\sqrt{3}} = \dfrac{6\sqrt{3}}{3} = 2\sqrt{3}$. That is about $3.5$, which is shorter than the long leg."},
   {"q": r"In a $30$-$60$-$90$ triangle, the longer leg has length $27$. The hypotenuse has length $k\sqrt{3}$. Then $k =$", "accept": ["18"], "exp": r"$x = \dfrac{27}{\sqrt{3}} = 9\sqrt{3}$, and the hypotenuse is $2x = 18\sqrt{3}$."},
 ]},
 {"sec": "D. Match each side to its angle", "items": [
   {"fig": "d1", "q": r"In the right triangle shown, $y =$", "accept": ["12"], "exp": r"The side marked $y$ is across from the $30^\circ$ angle, so it is the short leg: half of the hypotenuse."},
   {"fig": "d2", "q": r"In the right triangle shown, $y =$", "accept": ["18"], "exp": r"The third angle measures $30^\circ$, and the side of length $9$ is across from it. That makes $9$ the short leg. The side marked $y$ is the hypotenuse: $2 \cdot 9 = 18$."},
   {"fig": "d3", "q": r"In the right triangle shown, $y =$", "accept": ["40"], "exp": r"The side of length $20\sqrt{3}$ touches the $30^\circ$ angle, so it is across from the $60^\circ$ angle: it is the long leg. Then $x = 20$, and the hypotenuse is $2x = 40$."},
   {"fig": "d4", "q": r"In the right triangle shown, $y =$", "accept": ["5"], "exp": r"The other acute angle also measures $45^\circ$, so this is a $45$-$45$-$90$ triangle: $x\sqrt{2} = 5\sqrt{2}$, and $x = 5$."},
   {"fig": "d5", "mc": True, "q": r"In the right triangle shown, $y =$", "opts": [r"$11\sqrt{3}$", "$16.5$", r"$33\sqrt{3}$", "$66$"], "correct": 0, "exp": r"The side of length $33$ is across from the $60^\circ$ angle, so it is the long leg: $x\sqrt{3} = 33$, and $x = \dfrac{33}{\sqrt{3}} = 11\sqrt{3}$. The side marked $y$ is across from the $30^\circ$ angle, so $y = x$."},
   {"fig": "d6", "q": r"In the right triangle shown, $y =$", "accept": ["6"], "exp": r"The side across from the $30^\circ$ angle is the short leg, so $x = 2\sqrt{3}$. The side marked $y$ is the long leg: $2\sqrt{3} \cdot \sqrt{3} = 2 \cdot 3 = 6$."},
 ]},
 {"sec": "E. Find the triangle inside the figure", "items": [
   {"q": r"A square has a perimeter of $44$. Its diagonal has length $k\sqrt{2}$. Then $k =$", "accept": ["11"], "exp": r"Each side is $44 \div 4 = 11$, and the diagonal of a square is its side times $\sqrt{2}$."},
   {"q": r"A square has a diagonal of length $6$. The area of the square is", "accept": ["18"], "exp": r"Each side is $\dfrac{6}{\sqrt{2}} = 3\sqrt{2}$, and $(3\sqrt{2})^2 = 9 \cdot 2 = 18$. A shorter path: the area of a square is half the square of its diagonal, $\dfrac{6^2}{2}$."},
   {"mc": True, "q": r"An equilateral triangle has sides of length $18$. The height of the triangle is", "opts": ["$9$", r"$9\sqrt{2}$", r"$9\sqrt{3}$", r"$18\sqrt{3}$"], "correct": 2, "exp": r"The height makes a $30$-$60$-$90$ triangle with a hypotenuse of $18$ and a short leg of $9$. The height is the long leg, $9\sqrt{3}$."},
   {"q": r"The area of an equilateral triangle with sides of length $14$ is $k\sqrt{3}$. Then $k =$", "accept": ["49"], "exp": r"The height is $7\sqrt{3}$, so the area is $\tfrac{1}{2}(14)(7\sqrt{3}) = 49\sqrt{3}$. The formula agrees: $\dfrac{14^2\sqrt{3}}{4} = 49\sqrt{3}$."},
   {"q": r"A square is inscribed in a circle of radius $8$. The area of the square is", "accept": ["128"], "exp": r"The diagonal of the square is the diameter, $16$. The area is $\dfrac{16^2}{2} = 128$. Each side is $8\sqrt{2}$, and $(8\sqrt{2})^2 = 128$ agrees."},
   {"q": r"A circle is inscribed in a square. The diagonal of the square has length $30\sqrt{2}$. The radius of the circle is", "accept": ["15"], "exp": r"The side of the square is $30$. That equals the diameter of the circle, so the radius is $15$."},
   {"q": r"The height of an equilateral triangle is $10\sqrt{3}$. The perimeter of the triangle is", "accept": ["60"], "exp": r"The height is the long leg, $x\sqrt{3}$, so $x = 10$. The short leg is half of a side, so each side is $20$ and the perimeter is $60$."},
   {"q": r"An equilateral triangle has a perimeter of $12$. Its area is $k\sqrt{3}$. Then $k =$", "accept": ["4"], "exp": r"Each side is $4$: $\dfrac{4^2\sqrt{3}}{4} = 4\sqrt{3}$."},
 ]},
 {"sec": "F. Less common figures and trig values", "items": [
   {"q": r"A regular hexagon has sides of length $10$. Its area is $k\sqrt{3}$. Then $k =$", "accept": ["150"], "exp": r"The hexagon is six equilateral triangles with side $10$. Each has area $\dfrac{10^2\sqrt{3}}{4} = 25\sqrt{3}$, and $6 \cdot 25\sqrt{3} = 150\sqrt{3}$."},
   {"q": r"In a circle with radius $12$, two radii form a $60^\circ$ angle. The length of the chord that joins their endpoints is", "accept": ["12"], "exp": r"The two radii are equal, so the other two angles of the triangle are equal: $\dfrac{180 - 60}{2} = 60$ degrees each. The triangle is equilateral, and the chord equals the radius."},
   {"mc": True, "q": r"An isosceles triangle has two sides of length $6$ and an angle of $120^\circ$ between them. The length of the third side is", "opts": ["$6$", r"$6\sqrt{2}$", r"$6\sqrt{3}$", "$12$"], "correct": 2, "exp": r"The height from the $120^\circ$ angle makes two $30$-$60$-$90$ triangles with a hypotenuse of $6$. Each long leg is $3\sqrt{3}$, and the third side is two of them."},
   {"mc": True, "q": r"What is the value of $\tan 60^\circ$?", "opts": [r"$\dfrac{1}{2}$", r"$\dfrac{\sqrt{3}}{3}$", r"$\dfrac{\sqrt{3}}{2}$", r"$\sqrt{3}$"], "correct": 3, "exp": r"From the $60^\circ$ angle, the opposite side is $x\sqrt{3}$ and the adjacent side is $x$: $\dfrac{x\sqrt{3}}{x} = \sqrt{3}$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"The two legs of a right triangle each have length $25$. What is the length of the hypotenuse?",
  "options": ["$25$", r"$25\sqrt{2}$", r"$25\sqrt{3}$", "$50$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a right triangle with two equal legs.<br><br>Equal legs are across from equal angles, so each acute angle measures $45^\circ$. In a $45$-$45$-$90$ triangle the hypotenuse is a leg times $\sqrt{2}$: $25\sqrt{2}$.",
  "trap": r"Choice D doubles the leg, which is the $30$-$60$-$90$ pattern. Choice C uses $\sqrt{3}$, which also belongs to that triangle. The $45$-$45$-$90$ roots are $\sqrt{1}$, $\sqrt{1}$, $\sqrt{2}$."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"In a right triangle, one angle measures $30^\circ$ and the hypotenuse has length $38$. What is the length of the side across from the $30^\circ$ angle?",
  "label": "Length $=$", "accept": ["19"],
  "sol": r"<strong>Given:</strong> a $30$-$60$-$90$ triangle and its hypotenuse.<br><br>The side across from the $30^\circ$ angle is the short leg, $x$. The hypotenuse is $2x = 38$, so $x = 19$.",
  "trap": r"Mixing up the two legs. The long leg, $19\sqrt{3}$, is across from the $60^\circ$ angle. Match each side to the angle across from it before you answer."},
 {"ess": True, "type": "mc", "diff": "Easy to medium", "fig": "p3",
  "stem": r"In the right triangle above, what is the value of $y$?",
  "options": ["$5$", "$10$", r"$10\sqrt{3}$", "$15$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a right triangle with a $60^\circ$ angle. The side across from that angle has length $5\sqrt{3}$, and $y$ is the hypotenuse.<br><br>The side across from the $60^\circ$ angle is the long leg, $x\sqrt{3}$. So $x\sqrt{3} = 5\sqrt{3}$, and $x = 5$. The hypotenuse is $2x = 10$.",
  "trap": r"Choice C doubles the long leg. The hypotenuse is twice the short leg, so find $x$ first. Choice A is $x$ itself: check which side the question asks for."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"A square has an area of $50$. What is the length of its diagonal?",
  "label": "Diagonal $=$", "accept": ["10"],
  "sol": r"<strong>Given:</strong> the area of a square.<br><br>Each side is $\sqrt{50} = 5\sqrt{2}$. The diagonal is the side times $\sqrt{2}$: $5\sqrt{2} \cdot \sqrt{2} = 10$.<br><strong>A shorter path:</strong> the area of a square is $\dfrac{d^2}{2}$, so $d^2 = 100$ and $d = 10$.",
  "trap": r"Stopping at the side, $5\sqrt{2}$, which is about $7.07$. The question asks for the diagonal, which is one more step."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"An equilateral triangle has an area of $121\sqrt{3}$. What is the perimeter of the triangle?",
  "options": ["$22$", "$44$", "$66$", "$121$"], "correct": 2,
  "sol": r"<strong>Given:</strong> the area of an equilateral triangle.<br><br>Set the area formula equal to the given area: $\dfrac{s^2\sqrt{3}}{4} = 121\sqrt{3}$. Divide both sides by $\sqrt{3}$ to get $\dfrac{s^2}{4} = 121$. Then $s^2 = 484$ and $s = 22$. The perimeter is $3 \cdot 22 = 66$.",
  "trap": r"Choice A is the side length. The question asks for the perimeter, so multiply by $3$. Choice D is $s^2 \div 4$, a step along the way."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p6",
  "stem": r"In the figure above, a square is inscribed in a circle with center $O$. The radius of the circle is $6$. What is the area of the square?",
  "options": ["$36$", "$72$", "$144$", r"$36\pi$"], "correct": 1,
  "sol": r"<strong>Given:</strong> the corners of the square are on the circle.<br><br>The diagonal of the square passes through $O$, so it is a diameter: $12$. The diagonal cuts the square into two $45$-$45$-$90$ triangles, so each side is $\dfrac{12}{\sqrt{2}} = 6\sqrt{2}$. The area is $(6\sqrt{2})^2 = 72$.",
  "trap": r"Choice C uses the diameter as the side of the square. The diameter runs from corner to corner, so it is the diagonal. Choice A uses the radius as the side, and choice D is the area of the circle."},
 {"ess": True, "type": "ne", "diff": "Medium", "fig": "p7",
  "stem": r"In the figure above, a circle is inscribed in a square. The diagonal of the square has length $18\sqrt{2}$. The area of the circle is $k\pi$. What is the value of $k$?",
  "label": "$k =$", "accept": ["81"],
  "sol": r"<strong>Given:</strong> the circle touches all four sides of the square.<br><br>The diagonal of a square is its side times $\sqrt{2}$, so the side is $18$. The side equals the diameter of the circle, so the radius is $9$. The area is $\pi(9)^2 = 81\pi$, and $k = 81$.",
  "trap": r"Using $18$ as the radius, which gives $324$. The side of the square matches the diameter. Take half of it before you square."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p8",
  "stem": r"In rectangle $ABCD$ above, diagonal $\overline{AC}$ has length $20$, and the measure of angle $CAB$ is $30^\circ$. What is the area of the rectangle?",
  "options": [r"$50\sqrt{3}$", "$100$", r"$100\sqrt{3}$", r"$200\sqrt{3}$"], "correct": 2,
  "sol": r"<strong>Given:</strong> triangle $ABC$ has a right angle at $B$ and a $30^\circ$ angle at $A$, so it is a $30$-$60$-$90$ triangle with a hypotenuse of $20$.<br><br>$\overline{BC}$ is across from the $30^\circ$ angle, so it is the short leg: $10$. $\overline{AB}$ is the long leg: $10\sqrt{3}$. The area of the rectangle is $10\sqrt{3} \cdot 10 = 100\sqrt{3}$.",
  "trap": r"Choice A is the area of triangle $ABC$, which is half of the rectangle. Choice D multiplies the long leg by the diagonal. The area of the rectangle uses its two sides, which are the two legs of the triangle."},
 {"ess": False, "type": "ne", "diff": "Medium-hard", "fig": "p9",
  "stem": r"The figure above shows a regular hexagon with sides of length $6$. The area of the hexagon is $k\sqrt{3}$. What is the value of $k$?",
  "label": "$k =$", "accept": ["54"],
  "sol": r"<strong>Given:</strong> a regular hexagon, which splits into six equilateral triangles when you connect the center to each corner.<br><br>Each triangle has side $6$, so its area is $\dfrac{6^2\sqrt{3}}{4} = 9\sqrt{3}$. Six of them make $54\sqrt{3}$, so $k = 54$.",
  "trap": r"Answering $9$, the area of one of the six triangles. Reread the question after the first step: it asks for the whole hexagon."},
 {"ess": True, "type": "mc", "diff": "Medium-hard", "fig": "p10",
  "stem": r"In the figure above, $\overline{BD}$ is perpendicular to $\overline{AC}$, the measure of angle $A$ is $45^\circ$, the measure of angle $C$ is $30^\circ$, and $AB = 8\sqrt{2}$. What is the length of $\overline{BC}$?",
  "options": ["$8$", r"$8\sqrt{3}$", "$16$", r"$16\sqrt{2}$"], "correct": 2,
  "sol": r"<strong>Given:</strong> a height that splits triangle $ABC$ into a $45$-$45$-$90$ triangle and a $30$-$60$-$90$ triangle. $\overline{BD}$ belongs to both.<br><br><strong>Triangle $ABD$.</strong> It is a $45$-$45$-$90$ triangle with a hypotenuse of $8\sqrt{2}$, so each leg is $8$: $BD = 8$.<br><strong>Triangle $BDC$.</strong> $\overline{BD}$ is across from the $30^\circ$ angle at $C$, so it is the short leg. $\overline{BC}$ is across from the right angle, so it is the hypotenuse: $2 \cdot 8 = 16$.",
  "trap": r"Choice A stops at the shared side, $\overline{BD}$. Choice B is $DC$, the long leg of the second triangle. When two special triangles share a side, find that side first. Then decide which role it plays in the second triangle."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "c1",
  "stem": r"In the figure above, a circle is inscribed in a square with sides of length $20$, and a smaller square is inscribed in the circle. What is the area of the smaller square?",
  "label": "Area $=$", "accept": ["200"],
  "sol": r"<strong>Given:</strong> the circle touches the sides of the larger square, and the corners of the smaller square are on the circle.<br><br><strong>Larger square to circle.</strong> The side of the larger square equals the diameter: $20$.<br><strong>Circle to smaller square.</strong> The diagonal of the smaller square is a diameter: $20$. The area of a square is half the square of its diagonal: $\dfrac{20^2}{2} = 200$. Each side of the smaller square is $\dfrac{20}{\sqrt{2}} = 10\sqrt{2}$, and $(10\sqrt{2})^2 = 200$ agrees.",
  "trap": r"The diameter links the two squares. It matches the side of the outer square and the diagonal of the inner square, so the inner square has half the area of the outer one.",
  "extrasIntro": r"Squares and circles, one inside another: decide whether the diameter matches a side or a diagonal. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"A square is inscribed in a circle, and the circle is inscribed in a larger square. The larger square has an area of $64$. The area of the smaller square is", "label": "$=$", "accept": ["32"], "exp": r"The larger square has side $8$, so the diameter is $8$. That is the diagonal of the smaller square, whose area is $\dfrac{8^2}{2} = 32$."},
   {"type": "ne", "q": r"A circle has an area of $81\pi$. A square is inscribed in the circle. The area of the square is", "label": "$=$", "accept": ["162"], "exp": r"The radius is $9$ and the diameter is $18$. The diameter is the diagonal of the square: $\dfrac{18^2}{2} = 162$."},
   {"type": "ne", "q": r"A square is inscribed in a circle of radius $5\sqrt{2}$, and a smaller circle is inscribed in the square. The radius of the smaller circle is", "label": "$=$", "accept": ["5"], "exp": r"The diagonal of the square is the larger diameter, $10\sqrt{2}$, so its side is $10$. The side equals the diameter of the smaller circle, so the smaller radius is $5$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "c2",
  "stem": r"In the figure above, the height of the equilateral triangle is $30$. The area of the triangle is $k\sqrt{3}$. What is the value of $k$?",
  "label": "$k =$", "accept": ["300"],
  "sol": r"<strong>Given:</strong> the height, which is the long leg of a $30$-$60$-$90$ triangle.<br><br><strong>Find $x$.</strong> $x\sqrt{3} = 30$, so $x = \dfrac{30}{\sqrt{3}} = 10\sqrt{3}$. That is half of the base.<br><strong>The side.</strong> Each side is $2x = 20\sqrt{3}$.<br><strong>The area.</strong> $\tfrac{1}{2} \cdot 20\sqrt{3} \cdot 30 = 300\sqrt{3}$, so $k = 300$.",
  "trap": r"The height is not the side. Work back from the long leg to $x$ by dividing by $\sqrt{3}$, double $x$ for the side, and then use $\tfrac{1}{2} \cdot \text{base} \cdot \text{height}$ with the height you were given.",
  "extrasIntro": r"Equilateral triangles from different starting points: a height, an area, a perimeter. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The height of an equilateral triangle is $6$. Each side has length $k\sqrt{3}$. Then $k =$", "label": "$k =$", "accept": ["4"], "exp": r"$x\sqrt{3} = 6$, so $x = 2\sqrt{3}$. Each side is $2x = 4\sqrt{3}$."},
   {"type": "ne", "q": r"The area of an equilateral triangle is $9\sqrt{3}$. Its height is $k\sqrt{3}$. Then $k =$", "label": "$k =$", "accept": ["3"], "exp": r"$\dfrac{s^2\sqrt{3}}{4} = 9\sqrt{3}$ gives $s^2 = 36$ and $s = 6$. The height is half of the side, times $\sqrt{3}$: $3\sqrt{3}$."},
   {"type": "ne", "q": r"An equilateral triangle has a perimeter of $54$. Its area is $k\sqrt{3}$. Then $k =$", "label": "$k =$", "accept": ["81"], "exp": r"Each side is $18$: $\dfrac{18^2\sqrt{3}}{4} = \dfrac{324\sqrt{3}}{4} = 81\sqrt{3}$."},
  ]},
 {"ess": False, "type": "ne", "diff": "Medium-hard", "fig": "c3",
  "stem": r"In the figure above, rhombus $ABCD$ has sides of length $6$, and the measure of angle $A$ is $60^\circ$. The area of the rhombus is $k\sqrt{3}$. What is the value of $k$?",
  "label": "$k =$", "accept": ["18"],
  "sol": r"<strong>Given:</strong> four equal sides and a $60^\circ$ angle.<br><br>Draw diagonal $\overline{BD}$. Triangle $ABD$ has two sides of length $6$ with a $60^\circ$ angle between them, so its other two angles also measure $60^\circ$: it is equilateral. Triangle $CBD$ has the same three side lengths. Each triangle has area $\dfrac{6^2\sqrt{3}}{4} = 9\sqrt{3}$, so the rhombus has area $18\sqrt{3}$ and $k = 18$.",
  "trap": r"A $60^\circ$ angle between two equal sides makes an equilateral triangle. Draw the segment that closes the triangle, and the area formula does the rest."},
 {"ess": True, "type": "mc", "diff": "Hard", "fig": "c4",
  "stem": r"In the figure above, equilateral triangle $ABE$ is drawn inside square $ABCD$, which has sides of length $8$. What is the distance from point $E$ to side $\overline{CD}$?",
  "options": [r"$8 - 4\sqrt{3}$", r"$8 - 4\sqrt{2}$", "$4$", r"$4\sqrt{3}$"], "correct": 0,
  "sol": r"<strong>Given:</strong> the triangle and the square share side $\overline{AB}$, so the triangle has sides of length $8$.<br><br>The height of the triangle from $E$ to $\overline{AB}$ is the long leg of a $30$-$60$-$90$ triangle with a short leg of $4$: $4\sqrt{3}$. The square is $8$ units tall, so the distance from $E$ to $\overline{CD}$ is what is left: $8 - 4\sqrt{3}$, which is about $1.07$.",
  "trap": r"Choice D is the height of the triangle, which is the distance from $E$ to $\overline{AB}$. The question asks for the gap on the other side, so subtract that height from the side of the square."},
 {"ess": False, "type": "mc", "diff": "Hard", "fig": "c5",
  "stem": r"In the figure above, equilateral triangle $ABC$ is inscribed in a circle with center $O$, and the radius of the circle is $10$. What is the length of each side of the triangle?",
  "options": ["$10$", r"$10\sqrt{2}$", r"$10\sqrt{3}$", "$20$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $\overline{OB}$ and $\overline{OC}$ are radii, so triangle $OBC$ is isosceles with two sides of length $10$.<br><br>The three radii to the corners divide the $360^\circ$ at the center into three equal angles, so angle $BOC$ measures $120^\circ$. Draw the height from $O$ to $\overline{BC}$. It makes two $30$-$60$-$90$ triangles with a hypotenuse of $10$: the short leg is $5$, and the long leg is $5\sqrt{3}$. $\overline{BC}$ is two long legs: $10\sqrt{3}$.",
  "trap": r"The radius is not half of a side. Connect the center to two corners, and the $120^\circ$ isosceles triangle from Rule 6 appears: its third side is an equal side times $\sqrt{3}$."},
 {"ess": False, "type": "ne", "diff": "Hard · trig blend",
  "stem": r"In right triangle $ABC$, angle $C$ is the right angle and $\sin A = \dfrac{\sqrt{3}}{2}$. If $AB = 24$, what is the length of $\overline{AC}$?",
  "label": "$AC =$", "accept": ["12"],
  "sol": r"<strong>Given:</strong> a sine value that belongs to one of the special triangles.<br><br>$\sin 60^\circ = \dfrac{\sqrt{3}}{2}$, so angle $A$ measures $60^\circ$ and angle $B$ measures $30^\circ$. $\overline{AB}$ is the hypotenuse: $2x = 24$, so $x = 12$. $\overline{AC}$ is across from the $30^\circ$ angle at $B$, so it is the short leg: $12$.<br><strong>Another route:</strong> $\overline{BC}$ is opposite angle $A$, so $BC = 24 \cdot \dfrac{\sqrt{3}}{2} = 12\sqrt{3}$. Then $AC^2 = 24^2 - (12\sqrt{3})^2 = 576 - 432 = 144$, and $AC = 12$.",
  "trap": r"A sine of $\dfrac{1}{2}$, $\dfrac{\sqrt{2}}{2}$ or $\dfrac{\sqrt{3}}{2}$ points to an angle of $30^\circ$, $45^\circ$ or $60^\circ$. Once you know the angle, the side pattern gives the lengths."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"Each leg of a $45$-$45$-$90$ triangle has length $13$. What is the length of the hypotenuse?", "opts": ["$13$", r"$13\sqrt{2}$", r"$13\sqrt{3}$", "$26$"], "correct": 1,
  "exp": r"The hypotenuse is a leg times $\sqrt{2}$. Doubling belongs to the $30$-$60$-$90$ triangle."},
 {"q": r"In a $30$-$60$-$90$ triangle, the hypotenuse has length $60$. What is the length of the longer leg?", "opts": ["$30$", r"$30\sqrt{2}$", r"$30\sqrt{3}$", r"$60\sqrt{3}$"], "correct": 2,
  "exp": r"$2x = 60$, so $x = 30$. The longer leg is $x\sqrt{3} = 30\sqrt{3}$."},
 {"q": r"What is the area of an equilateral triangle with sides of length $2$?", "opts": [r"$\sqrt{3}$", "$2$", r"$2\sqrt{3}$", r"$4\sqrt{3}$"], "correct": 0,
  "exp": r"The height is $\sqrt{3}$, so the area is $\tfrac{1}{2}(2)(\sqrt{3}) = \sqrt{3}$. The formula agrees: $\dfrac{2^2\sqrt{3}}{4} = \sqrt{3}$."},
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
FIGS = {}


def turn(p, deg=0, flip=False):
    """Rotate the point p by deg degrees about the origin, after an optional mirror in the y-axis."""
    x, y = (-p[0] if flip else p[0]), p[1]
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return pt(x * c - y * s, x * s + y * c)


def bbox(points, m=1.0, mx=None, my=None):
    mx = m if mx is None else mx
    my = m if my is None else my
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    return [round(min(xs) - mx, 3), round(min(ys) - my, 3), round(max(xs) + mx, 3), round(max(ys) + my, 3)]


def oside(a, b, t, G, off=13, **k):
    """A label beside segment a-b, on the side away from the point G (usually the centroid)."""
    cross = (b[0] - a[0]) * (G[1] - a[1]) - (b[1] - a[1]) * (G[0] - a[0])
    return side(a, b, t, -off if cross > 0 else off, **k)


def tri_fig(kind, deg=0, flip=False, show=(), labels=None, alt='', size=4.4, m=0.8, offs=None, scale=38, pad=12):
    """A special right triangle at any rotation, for the reps on matching sides to angles.
    kind 30: vertices R (right angle), S (the 60 degree corner), L (the 30 degree corner); sides 'short' (R-S),
    'long' (R-L) and 'hyp' (S-L). kind 45: R, S, L with both acute angles 45; sides 'leg1' (R-S), 'leg2' (R-L), 'hyp'.
    show lists the angle marks to draw ('30', '60', '45'); labels maps a side name to its text."""
    labels = labels or {}; offs = offs or {}
    if kind == 30:
        x = size / 2.0
        R, S, L = (0, 0), (x, 0), (0, x * R3)
        names = {'short': (0, 1), 'long': (0, 2), 'hyp': (1, 2)}
    else:
        x = size / R2
        R, S, L = (0, 0), (x, 0), (0, x)
        names = {'leg1': (0, 1), 'leg2': (0, 2), 'hyp': (1, 2)}
    P = [turn(p, deg, flip) for p in (R, S, L)]
    R, S, L = P
    G = cen(R, S, L)
    arcs = []
    if kind == 30:
        if '30' in show: arcs.append(ang3(L, R, S, '30°', r=34, lr=53))
        if '60' in show: arcs.append(ang3(S, R, L, '60°', r=17, lr=33))
    else:
        if '45' in show: arcs.append(ang3(S, R, L, '45°', r=24, lr=42))
    sides = [oside(P[i], P[j], labels[k], G, offs.get(k, 14)) for k, (i, j) in names.items() if k in labels]
    box = bbox(P, m)                                  # the figure is sized to the triangle, at `scale` px per unit
    w, h = int(round((box[2] - box[0]) * scale + 2 * pad)), int(round((box[3] - box[1]) * scale + 2 * pad))
    return dict(box=box, w=w, h=h, pad=pad, alt=alt, segs=[seg(R, S), seg(R, L), seg(S, L)],
                rights=[dict(at=R, a=S, b=L)], arcs=arcs, sides=sides)


def square_in_circle(r, deg=45):
    """Corners of a square whose corners are on the circle of radius r about the origin, starting at angle deg."""
    return [pol(pt(0, 0), deg + 90 * i, r) for i in range(4)]


def hexagon(r, deg=0):
    return [pol(pt(0, 0), deg + 60 * i, r) for i in range(6)]


# --- Rule 1 and Rule 2: the two patterns (as in SAT Math 4, so the pictures match)
A, B, C = pt(0, 0), pt(4, 0), pt(4, 4)
FIGS['r_45'] = dict(box=[-0.5, -0.7, 5.2, 4.3], w=250, h=250, alt='a 45-45-90 triangle drawn as half of a square: legs x and x, hypotenuse x times the square root of 2',
    segs=[seg(A, pt(0, 4), 'dash'), seg(pt(0, 4), C, 'dash'), seg(A, B), seg(B, C), seg(A, C)],
    rights=[dict(at=B, a=A, b=C)],
    sides=[side(A, B, 'x', -13), side(B, C, 'x', -12), side(A, C, 'x√2', 17)],
    arcs=[ang3(A, B, C, '45°', r=24, lr=42), ang3(C, A, B, '45°', r=24, lr=42)])
D, B, A = pt(2, 0), pt(4, 0), pt(2, 2 * R3)
FIGS['r_30'] = dict(box=[-0.3, -0.6, 5.0, 3.8], w=270, h=250, alt='a 30-60-90 triangle drawn as half of an equilateral triangle: short leg x across from the 30 degree angle, long leg x times the square root of 3, hypotenuse 2x',
    segs=[seg(pt(0, 0), D, 'dash'), seg(pt(0, 0), A, 'dash'), seg(D, B), seg(B, A), seg(A, D)],
    rights=[dict(at=D, a=B, b=A)],
    sides=[side(D, B, 'x', -13), side(D, A, 'x√3', 21), side(B, A, '2x', -15)],
    arcs=[ang3(A, D, B, '30°', r=38, lr=64, dx=1), ang3(B, A, D, '60°', r=17, lr=32)])

# --- Rule 4: a square and its diagonal, a square inside a circle, a circle inside a square
A, B, C, D = pt(0, 0), pt(4, 0), pt(4, 4), pt(0, 4)
FIGS['r_sqd'] = dict(box=[-0.7, -1.7, 4.9, 4.6], w=205, h=235, alt='a square with side s and its diagonal, which has length s times the square root of 2 and makes 45 degree angles with the sides',
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, A), seg(A, C)],
    rights=[dict(at=B, a=A, b=C, s=8)],
    sides=[side(A, B, 's', -13), side(B, C, 's', -12), side(A, C, 's√2', 16)],
    arcs=[ang3(A, B, C, '45°', r=24, lr=42)],
    texts=[txt(pt(2, -1.45), 'diagonal = side × √2', cls='note')])
O = pt(0, 0); Q = square_in_circle(2.7)
FIGS['r_sqin'] = dict(box=[-3.0, -3.75, 3.0, 3.0], w=205, h=235, alt='a square inscribed in a circle: the corners of the square are on the circle, and the diagonal of the square is a diameter of the circle',
    circles=[dict(c=O, r=2.7)],
    segs=[seg(Q[0], Q[1]), seg(Q[1], Q[2]), seg(Q[2], Q[3]), seg(Q[3], Q[0]), seg(Q[2], Q[0], 'dash')],
    dots=[O],
    texts=[txt(pt(0, -3.5), 'diagonal of the square = diameter', cls='note')])
FIGS['r_cin'] = dict(box=[-3.0, -3.75, 3.0, 3.0], w=205, h=235, alt='a circle inscribed in a square: the circle touches all four sides, and the side of the square equals the diameter of the circle',
    circles=[dict(c=O, r=2.7)],
    segs=[seg(pt(-2.7, -2.7), pt(2.7, -2.7)), seg(pt(2.7, -2.7), pt(2.7, 2.7)), seg(pt(2.7, 2.7), pt(-2.7, 2.7)), seg(pt(-2.7, 2.7), pt(-2.7, -2.7)), seg(pt(-2.7, 0), pt(2.7, 0), 'dash')],
    dots=[O],
    texts=[txt(pt(0, -3.5), 'side of the square = diameter', cls='note')])

# --- Rule 5: an equilateral triangle and its height
Q, R, P, M = pt(0, 0), pt(4, 0), pt(2, 2 * R3), pt(2, 0)
FIGS['r_eq'] = dict(box=[-0.9, -1.5, 4.9, 3.9], w=300, h=285, alt='an equilateral triangle with side s; its height splits it into two 30-60-90 triangles, each with hypotenuse s, short leg s over 2, and the height as its long leg',
    polys=[dict(pts=[P, Q, M], cls='shade')],
    segs=[seg(P, Q), seg(P, R), seg(Q, R), seg(P, M, 'dash')],
    rights=[dict(at=M, a=P, b=R, s=8)],
    sides=[side(Q, P, 's', 13), side(P, R, 's', 13), side(Q, M, 's/2', -14), side(M, R, 's/2', -14)],
    arcs=[ang3(Q, M, P, '60°', r=17, lr=33), ang3(P, Q, M, '30°', r=38, lr=62, dx=-2)],
    texts=[txt(pt(2, 1.45), 'h', dx=11), txt(pt(2, -1.2), 'height h = (s/2) × √3', cls='note')])

# --- Rule 6: a regular hexagon and a 120 degree isosceles triangle
O = pt(0, 0); V = hexagon(2.7)
FIGS['r_hex'] = dict(box=[-3.2, -3.0, 3.2, 3.0], w=240, h=230, alt='a regular hexagon with side s, divided by three dashed diagonals into six equilateral triangles that meet at the center; one triangle is shaded and its angle at the center is 60 degrees',
    polys=[dict(pts=[O, V[0], V[1]], cls='shade')],
    segs=[seg(V[i], V[(i + 1) % 6]) for i in range(6)] + [seg(V[i], V[i + 3], 'dash') for i in range(3)],
    sides=[side(V[0], V[1], 's', -13), side(O, V[0], 's', -12, f=0.6)],
    arcs=[ang3(O, V[0], V[1], '60°', r=15, lr=31)])
A, B, C, F = pt(0, 2), pt(-2 * R3, 0), pt(2 * R3, 0), pt(0, 0)
FIGS['r_iso'] = dict(box=[-4.2, -1.3, 4.2, 3.0], w=300, h=200, alt='an isosceles triangle with two sides of length a and a 120 degree angle between them; the height from that angle splits it into two 30-60-90 triangles, and the third side has length a times the square root of 3',
    segs=[seg(A, B), seg(A, C), seg(B, C), seg(A, F, 'dash')],
    rights=[dict(at=F, a=A, b=C, s=8)],
    sides=[side(B, A, 'a', 13), side(A, C, 'a', 13), side(B, C, 'a√3', -15)],
    arcs=[ang3(B, C, A, '30°', r=36, lr=58), ang3(C, A, B, '30°', r=36, lr=58)],
    texts=[txt(A, '120°', dy=-13, cls='g')])

# --- Step 1: a 45-45-90 triangle with one leg given
C, A, B = pt(0, 0), pt(4.2, 0), pt(0, 4.2)
FIGS['s1'] = dict(box=[-0.9, -1.1, 5.1, 4.9], w=290, h=250, alt='right triangle ABC with the right angle at C; the angle at A is 45 degrees and side AC is 9',
    segs=[seg(C, A), seg(C, B), seg(A, B)],
    rights=[dict(at=C, a=A, b=B)],
    arcs=[ang3(A, C, B, '45°', r=24, lr=42)],
    sides=[side(C, A, '9', -13)],
    pts=[lab(A, 'A', -20), lab(B, 'B', 90), lab(C, 'C', 225)])

# --- Step 2: a 30-60-90 triangle with only the 60 degree angle marked (short leg vertical)
E, D, F = pt(0, 0), pt(0, 3.1), pt(3.1 * R3, 0)
FIGS['s2'] = dict(box=[-1.2, -0.9, 6.3, 3.9], w=330, h=215, alt='right triangle DEF with the right angle at E; the angle at D is 60 degrees and side DE is 15',
    segs=[seg(E, D), seg(E, F), seg(D, F)],
    rights=[dict(at=E, a=D, b=F)],
    arcs=[ang3(D, E, F, '60°', r=17, lr=33)],
    sides=[side(E, D, '15', 14)],
    pts=[lab(D, 'D', 90), lab(E, 'E', 225), lab(F, 'F', -15)])

# --- Step 3: a 30-60-90 triangle resting on its hypotenuse, long leg given
L, J = pt(0, 0), pt(8, 0); K = pol(L, 30, 4 * R3)
FIGS['s3'] = dict(box=[-0.9, -0.9, 8.9, 4.4], w=340, h=215, alt='right triangle JKL with the right angle at K, drawn with hypotenuse JL along the bottom; the angle at L is 30 degrees and side KL is 21',
    segs=[seg(L, J), seg(L, K), seg(K, J)],
    rights=[dict(at=K, a=L, b=J)],
    arcs=[ang3(L, J, K, '30°', r=36, lr=56)],
    sides=[side(L, K, '21', 14)],
    pts=[lab(L, 'L', 200), lab(J, 'J', -20), lab(K, 'K', 80)])

# --- Step 4: a square inscribed in a circle of radius 5
O = pt(0, 0); B, A, D, C = square_in_circle(3.0)
FIGS['s4'] = dict(box=[-3.7, -3.7, 3.7, 3.7], w=270, h=270, pad=16, alt='square ABCD inscribed in a circle with center O; the dashed diagonal AC passes through O, and radius OB is 5',
    circles=[dict(c=O, r=3.0)],
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, A), seg(A, C, 'dash'), seg(O, B, 'thin')],
    sides=[side(O, B, '5', 12)],
    dots=[O],
    pts=[lab(A, 'A', 135), lab(B, 'B', 45), lab(C, 'C', -45), lab(D, 'D', 225), lab(O, 'O', 250, d=15)])

# --- Step 5: an equilateral triangle with side 8 and its height
Q, R, P, M = pt(0, 0), pt(5, 0), pt(2.5, 2.5 * R3), pt(2.5, 0)
FIGS['s5'] = dict(box=[-0.9, -1.0, 5.9, 5.0], w=290, h=255, alt='equilateral triangle PQR with sides of length 8; the dashed height PM meets side QR at a right angle at M',
    segs=[seg(P, Q), seg(P, R), seg(Q, R), seg(P, M, 'dash')],
    rights=[dict(at=M, a=P, b=R, s=8)],
    sides=[side(Q, P, '8', 13), side(P, R, '8', 13)],
    pts=[lab(P, 'P', 90), lab(Q, 'Q', 200), lab(R, 'R', -20), lab(M, 'M', 270)])

# --- Step 6: a regular hexagon with side 4
O = pt(0, 0); V = hexagon(2.8)
FIGS['s6'] = dict(box=[-3.4, -3.1, 3.4, 3.2], w=260, h=240, alt='a regular hexagon with sides of length 4; three dashed diagonals through the center divide it into six triangles',
    segs=[seg(V[i], V[(i + 1) % 6]) for i in range(6)] + [seg(V[i], V[i + 3], 'dash') for i in range(3)],
    sides=[side(V[1], V[2], '4', -13)],
    dots=[O])

# --- Skill Practice D: the same two triangles, turned
FIGS['d1'] = tri_fig(30, 205, False, show=('30',), labels={'hyp': '24', 'short': 'y'},
    alt='a right triangle with a 30 degree angle; the hypotenuse is 24, and the side across from the 30 degree angle is marked y')
FIGS['d2'] = tri_fig(30, 90, True, show=('60',), labels={'short': '9', 'hyp': 'y'},
    alt='a right triangle with a 60 degree angle; the leg that touches the 60 degree angle is 9, and the hypotenuse is marked y')
FIGS['d3'] = tri_fig(30, -30, False, show=('30',), labels={'long': '20√3', 'hyp': 'y'}, offs={'long': 24},
    alt='a right triangle with a 30 degree angle; the leg that touches the 30 degree angle is 20 times the square root of 3, and the hypotenuse is marked y')
FIGS['d4'] = tri_fig(45, -135, False, show=('45',), labels={'hyp': '5√2', 'leg2': 'y'},
    alt='a right triangle with a 45 degree angle, drawn with the hypotenuse along the bottom; the hypotenuse is 5 times the square root of 2, and one leg is marked y')
FIGS['d5'] = tri_fig(30, 180, True, show=('60',), labels={'long': '33', 'short': 'y'},
    alt='a right triangle with a 60 degree angle; the side across from the 60 degree angle is 33, and the other leg is marked y')
FIGS['d6'] = tri_fig(30, 60, False, show=('30',), labels={'short': '2√3', 'long': 'y'}, offs={'short': 17},
    alt='a right triangle with a 30 degree angle; the side across from the 30 degree angle is 2 times the square root of 3, and the other leg is marked y')

# --- Practice 3: a turned 30-60-90 triangle, long leg given
FIGS['p3'] = tri_fig(30, 150, True, show=('60',), labels={'long': '5√3', 'hyp': 'y'}, offs={'long': 18}, size=4.8, scale=42,
    alt='a right triangle with a 60 degree angle; the side across from the 60 degree angle is 5 times the square root of 3, and the hypotenuse is marked y')

# --- Practice 6: a square inscribed in a circle of radius 6
O = pt(0, 0); Q = square_in_circle(3.0)
FIGS['p6'] = dict(box=[-3.6, -3.6, 3.6, 3.6], w=260, h=260, pad=16, alt='a square inscribed in a circle with center O; a radius of length 6 is drawn from O to one corner of the square',
    circles=[dict(c=O, r=3.0)],
    segs=[seg(Q[0], Q[1]), seg(Q[1], Q[2]), seg(Q[2], Q[3]), seg(Q[3], Q[0]), seg(O, Q[0], 'thin')],
    sides=[side(O, Q[0], '6', 12)],
    dots=[O],
    pts=[lab(O, 'O', 225, d=14)])

# --- Practice 7: a circle inscribed in a square, with the square's diagonal
FIGS['p7'] = dict(box=[-3.3, -3.3, 3.3, 3.3], w=250, h=250, pad=16, alt='a circle inscribed in a square; the dashed diagonal of the square has length 18 times the square root of 2',
    circles=[dict(c=O, r=2.8)],
    segs=[seg(pt(-2.8, -2.8), pt(2.8, -2.8)), seg(pt(2.8, -2.8), pt(2.8, 2.8)), seg(pt(2.8, 2.8), pt(-2.8, 2.8)), seg(pt(-2.8, 2.8), pt(-2.8, -2.8)), seg(pt(-2.8, -2.8), pt(2.8, 2.8), 'dash')],
    sides=[side(pt(-2.8, -2.8), pt(2.8, 2.8), '18√2', 17, f=0.62)])

# --- Practice 8: a rectangle whose diagonal makes a 30 degree angle (drawn to scale: 10 root 3 by 10)
A, B, C, D = pt(0, 0), pt(4 * R3, 0), pt(4 * R3, 4), pt(0, 4)
FIGS['p8'] = dict(box=[-0.9, -0.9, 4 * R3 + 0.9, 4.9], w=330, h=235, alt='rectangle ABCD with diagonal AC; the diagonal has length 20 and the angle CAB is 30 degrees',
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, A), seg(A, C)],
    arcs=[ang3(A, B, C, '30°', r=38, lr=58)],
    sides=[side(A, C, '20', 14)],
    pts=[lab(A, 'A', 225), lab(B, 'B', -45), lab(C, 'C', 45), lab(D, 'D', 135)])

# --- Practice 9: a regular hexagon with side 6 (no segments drawn inside)
V = hexagon(2.8)
FIGS['p9'] = dict(box=[-3.4, -3.1, 3.4, 3.2], w=250, h=232, alt='a regular hexagon with sides of length 6',
    segs=[seg(V[i], V[(i + 1) % 6]) for i in range(6)],
    sides=[side(V[1], V[2], '6', -13)])

# --- Practice 10: a 45-45-90 triangle and a 30-60-90 triangle that share a height (BD = 3 units)
A, D, B, C = pt(0, 0), pt(3, 0), pt(3, 3), pt(3 + 3 * R3, 0)
FIGS['p10'] = dict(box=[-0.9, -1.0, 3 + 3 * R3 + 0.9, 3.9], w=340, h=205, alt='triangle ABC with the height BD drawn to side AC, meeting it at a right angle at D; the angle at A is 45 degrees, the angle at C is 30 degrees, and side AB is 8 times the square root of 2',
    segs=[seg(A, B), seg(B, C), seg(A, C), seg(B, D, 'thin')],
    rights=[dict(at=D, a=B, b=C, s=8)],
    arcs=[ang3(A, D, B, '45°', r=24, lr=42), ang3(C, B, D, '30°', r=38, lr=58)],
    sides=[side(A, B, '8√2', 17)],
    pts=[lab(A, 'A', 200), lab(B, 'B', 90), lab(C, 'C', -20), lab(D, 'D', 270)])

# --- Challenge 1: a square, the circle inscribed in it, and a square inscribed in the circle
O = pt(0, 0); Q = square_in_circle(3.0)
FIGS['c1'] = dict(box=[-3.6, -4.2, 3.6, 3.6], w=260, h=282, pad=16, alt='a square with sides of length 20, a circle inscribed in it, and a smaller shaded square inscribed in the circle with its sides parallel to the larger square',
    polys=[dict(pts=Q, cls='shade')],
    circles=[dict(c=O, r=3.0)],
    segs=[seg(pt(-3, -3), pt(3, -3)), seg(pt(3, -3), pt(3, 3)), seg(pt(3, 3), pt(-3, 3)), seg(pt(-3, 3), pt(-3, -3)),
          seg(Q[0], Q[1]), seg(Q[1], Q[2]), seg(Q[2], Q[3]), seg(Q[3], Q[0])],
    sides=[side(pt(-3, -3), pt(3, -3), '20', -14)])

# --- Challenge 2: an equilateral triangle with its height given
Q, R, P, M = pt(0, 0), pt(5, 0), pt(2.5, 2.5 * R3), pt(2.5, 0)
FIGS['c2'] = dict(box=[-0.9, -0.8, 5.9, 5.0], w=280, h=240, alt='an equilateral triangle with its dashed height drawn from the top corner to the base, meeting it at a right angle; the height is 30',
    segs=[seg(P, Q), seg(P, R), seg(Q, R), seg(P, M, 'dash')],
    rights=[dict(at=M, a=P, b=R, s=8)],
    ticks=[dict(a=P, b=Q, n=1), dict(a=P, b=R, n=1)],
    texts=[txt(pt(2.5, 1.9), '30', dx=14)])

# --- Challenge 3: a rhombus with a 60 degree angle
A, B = pt(0, 0), pt(4.2, 0); D = pol(A, 60, 4.2); C = pt(B[0] + D[0], D[1])
FIGS['c3'] = dict(box=[-0.9, -1.0, C[0] + 0.9, D[1] + 0.9], w=320, h=215, alt='rhombus ABCD with sides of length 6; tick marks show the four sides are equal, and the angle at A is 60 degrees',
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, A)],
    ticks=[dict(a=A, b=D, n=1), dict(a=B, b=C, n=1), dict(a=D, b=C, n=1), dict(a=A, b=B, n=1)],
    arcs=[ang3(A, B, D, '60°', r=17, lr=33)],
    sides=[side(A, B, '6', -14, f=0.62)],
    pts=[lab(A, 'A', 225), lab(B, 'B', -45), lab(C, 'C', 45), lab(D, 'D', 135)])

# --- Challenge 4: an equilateral triangle inside a square (side 8 drawn as 4 units)
A, B, C, D = pt(0, 0), pt(4, 0), pt(4, 4), pt(0, 4); E = pt(2, 2 * R3)
FIGS['c4'] = dict(box=[-0.9, -1.1, 4.9, 4.9], w=270, h=280, alt='square ABCD with sides of length 8; equilateral triangle ABE is drawn inside it on side AB, with E near the top side CD',
    polys=[dict(pts=[A, B, E], cls='shade')],
    segs=[seg(A, B), seg(B, C), seg(C, D), seg(D, A), seg(A, E), seg(B, E)],
    sides=[side(A, B, '8', -14)],
    pts=[lab(A, 'A', 225), lab(B, 'B', -45), lab(C, 'C', 45), lab(D, 'D', 135), lab(E, 'E', 180, d=14, dy=-3)])

# --- Challenge 5: an equilateral triangle inscribed in a circle of radius 10
O = pt(0, 0); A, B, C = pol(O, 90, 3.0), pol(O, 210, 3.0), pol(O, 330, 3.0)
FIGS['c5'] = dict(box=[-3.7, -3.7, 3.7, 3.7], w=265, h=265, pad=16, alt='equilateral triangle ABC inscribed in a circle with center O; radius OC is drawn and has length 10',
    circles=[dict(c=O, r=3.0)],
    segs=[seg(A, B), seg(B, C), seg(C, A), seg(O, C, 'thin')],
    sides=[side(O, C, '10', 12)],
    dots=[O],
    pts=[lab(A, 'A', 90), lab(B, 'B', 210), lab(C, 'C', 330), lab(O, 'O', 150, d=14)])

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
@media (max-width: 768px) { .ref-page .fig-row { margin-left: 0; } }
.memo-pair { display: flex; flex-wrap: wrap; gap: 0 16px; }
.memo-pair .tbl-wrap { flex: 1 1 290px; }
table.cases.memo td, table.cases.memo th[colspan] { text-align: center; }
table.cases.memo td.fname { text-align: left; }
table.cases.memo td:not(.fname) { font-size: 18px; }
@media (max-width: 768px) { table.cases.memo td:not(.fname) { font-size: 16px; } }'''
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
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Special Right Triangles</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Special Right Triangles</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; SPECIAL RIGHT TRIANGLES')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Special Right Triangles')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Pattern Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Special right triangle rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>one side and one pattern give you the whole triangle.</strong> A $45$-$45$-$90$ triangle is $x$, $x$, $x\sqrt{2}$. A $30$-$60$-$90$ triangle is $x$, $x\sqrt{3}$, $2x$. Each question asks you to notice which triangle the figure contains, decide which side you were given, and build the side you need.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. Try section A from memory before you look back at the rules. Sections A to E use the starred rules, and section F covers the unstarred ones. Once you feel comfortable, try responding without pausing for long.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and six include a figure. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type: which special triangle does the figure contain, and which of its sides were you given? Sketch a figure if none is provided. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. For these questions it works mostly as a calculator, for example to compare $\dfrac{24}{\sqrt{3}}$ with $8\sqrt{3}$. When the choices contain radicals, an exact answer from the side pattern is usually quicker than a decimal.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These six questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each one places a special right triangle inside another figure (a square and a circle nested together, an equilateral triangle known only by its height, a rhombus, a triangle inside a square, a triangle inside a circle) or reaches it through a trig value. Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the ones marked <em>extra</em> lean on the unstarred rules. One is tagged <em>trig blend</em>: it uses sine, so treat it as stretch practice if you have not studied trigonometry yet.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time a special right triangle shows up. Make it an if-then. (Shape: “When a figure has a square or an equilateral triangle, I ______ before I compute anything.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">For skill-by-skill practice, <strong>Khan Academy\'s Official Digital SAT Prep</strong> sorts questions by topic: the lessons on <em>right triangle trigonometry</em> are a good place to practice both patterns. <a href="https://www.khanacademy.org/digital-sat" ' + A_STYLE + '>Open Khan Academy &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">This sheet goes deeper on one rule from SAT Math 4, which also covers parallel lines, the angles of a triangle and the Pythagorean theorem: <a href="' + TRI_URL + '" ' + A_STYLE + '>SAT Math 4: Triangles &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, and for a copy of the Bluebook reference sheet with both special right triangles, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>',
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

    # --- Skill Practice items can carry a figure (section D); it sits between the question and the answer row
    html = replace_once(html, """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>';""",
                        """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>' + (it.fig ? fig(it.fig) : '');""")

    # --- results kit: carry each question's figure into the tutor report (practice, challenge and the Skill Practice reps that have one)
    html = replace_n(html, "stem: p.stem, trap: p.trap });", "stem: p.stem, fig: p.fig ? fig(p.fig) : '', trap: p.trap });", 2)
    html = replace_once(html, """'</b></span></div><div class="stem">' + r.i.stem + '</div>""", """'</b></span></div><div class="stem">' + (r.i.fig || '') + r.i.stem + '</div>""")
    html = replace_once(html, ": it.accept[0], q: it.q }); }", ": it.accept[0], q: it.q + (it.fig ? fig(it.fig) : '') }); }")
    html = replace_once(html, "'.nw{white-space:nowrap}table.vtab{", "'" + REPORT_FIG_CSS.replace('\\', '\\\\').replace("'", "\\'") + "' +\n        '.nw{white-space:nowrap}table.vtab{")

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', 'sat-special-right-triangles-sheet:rule')
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
