#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-8-Circle-Equations.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the content
swaps. This sheet covers circles in the xy-plane: standard form, completing the square, area and
circumference from the equation, writing the equation from a center and a point or from a diameter,
circles tangent to an axis, and symmetry and semicircles. The question types follow Tip 24 of the
class book; all questions use original numbers.

It was copied from build_ratios.py and keeps that file's conventions (the voice pass, figures in the
tutor report, the curve and grid extensions to the shell's graphSVG). One thing is added here: a
`circles` key for the coordinate graph (a full circle or an upper semicircle), with the helper G() that
sizes each figure so both axes use the same scale. There is no Khan Academy line on this sheet.
Answer key: verify_circles.py (same folder) recomputes every answer."""
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
OUT = ROOT + '/test-prep/sat/SAT-Math-8-Circle-Equations.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
QUAD_URL = SITE + 'test-prep/sat/SAT-Math-2-Quadratics.html'
TRI_URL = SITE + 'test-prep/sat/SAT-Math-4-Triangles.html'
EXP_URL = SITE + 'test-prep/sat/SAT-Math-7-Exponents-and-Exponential-Models.html'
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
LINK_STYLE = 'target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;"'

RULES = r'''
<p class="ref-intro">A circle is every point at the same distance from one point, its center. That distance is the radius. In the $xy$-plane, the equation of a circle states that distance with the Pythagorean theorem, so one form of the equation shows the center and the radius at a glance. Most questions on this sheet come down to getting the equation into that form and reading it. As you practice, start by identifying the question type. Then decide whether Desmos or algebra makes more sense, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''' + rule(1, 'Standard form: read the center and the radius', True, r'''
<p class="ref-lead">Different forms reveal different information. Standard form shows the center and the radius directly, so recognize whether you have been given it before doing any algebra.</p>
''' + figslot('r_standard') + r'''<div class="fbox">
''' + frow('standard form', r"$(x - h)^2 + (y - k)^2 = r^2$") +
      frow('center', r"$(h, k)$ &nbsp; (each sign is the opposite of the one you see)") +
      frow('radius', r"$r$, the square root of the right side") +
      frow('center at the origin', r"$x^2 + y^2 = r^2$") +
      frow('why it works', r"the legs $x - h$ and $y - k$ and the radius $r$ form a right triangle, so the Pythagorean theorem gives the equation") + r'''</div>
''' + ex('A', r"$(x - 3)^2 + (y + 2)^2 = 25$ has center $(3, -2)$ and radius $5$. Read $y + 2$ as $y - (-2)$.") +
    ex('B', r"$x^2 + (y - 4)^2 = 12$ has center $(0, 4)$ and radius $\sqrt{12} = 2\sqrt{3}$. When $x$ is squared on its own, the center is on the $y$-axis.") +
    ex('C', r"A circle with center $(-1, 5)$ and radius $3$ has the equation $(x + 1)^2 + (y - 5)^2 = 9$.") +
    note(r"The diameter is $2r$. If a question asks for the diameter, find the radius first and double it.")) + \
rule(2, 'Completing the square to reach standard form', True, r'''
<p class="ref-lead">When the squares have been multiplied out, the center and the radius are hidden. Completing the square rebuilds standard form: group the $x$ terms, group the $y$ terms, and turn each group into a perfect square.</p>
<div class="fbox">
''' + frow('the pattern', r"$x^2 + bx + \left(\dfrac{b}{2}\right)^2 = \left(x + \dfrac{b}{2}\right)^2$") +
      frow('what to add', r"half of the coefficient of $x$, squared; then the same for $y$") +
      frow('keep it balanced', r"add the same numbers to the other side of the equation") +
      frow('a number in front of the squares', r"if the equation starts $2x^2 + 2y^2$, divide every term by $2$ first") + r'''</div>
''' + ex('A', r"$x^2 + y^2 - 6x + 4y = 12$. Group the terms: $(x^2 - 6x) + (y^2 + 4y) = 12$. Half of $-6$ is $-3$, and $(-3)^2 = 9$. Half of $4$ is $2$, and $2^2 = 4$. Add $9$ and $4$ to both sides: $(x - 3)^2 + (y + 2)^2 = 25$. The center is $(3, -2)$ and the radius is $5$.") +
    ex('B', r"$x^2 + 8x + y^2 = 20$. Only the $x$ terms need work. Add $16$ to both sides: $(x + 4)^2 + y^2 = 36$. The center is $(-4, 0)$ and the radius is $6$.") +
    ex('C', r"$2x^2 + 2y^2 - 12x + 4y = 78$. Divide by $2$: $x^2 + y^2 - 6x + 2y = 39$. Add $9$ and $1$ to both sides: $(x - 3)^2 + (y + 1)^2 = 49$. The radius is $7$.") +
    note(r'Desmos can graph a circle from either form of its equation, so typing the equation as it is written is a good way to check the center and radius you found. Want more practice with completing the square? It is covered in <a href="' + QUAD_URL + r'" ' + LINK_STYLE + r'>SAT Math 2: Quadratics &#8594;</a>')) + \
rule(3, 'Area and circumference from the equation', True, r'''
<p class="ref-lead">Once the equation is in standard form, the right side is $r^2$. The area uses that number as it stands. The circumference and the diameter need $r$, so take the square root first.</p>
<div class="fbox">
''' + frow('area', r"$\pi r^2$, which is $\pi$ times the right side of standard form") +
      frow('circumference', r"$2\pi r$") +
      frow('diameter', r"$2r$") +
      frow('working backward', r"an area of $49\pi$ means $r^2 = 49$, and a circumference of $14\pi$ means $r = 7$") + r'''</div>
''' + ex('A', r"$(x - 1)^2 + (y - 6)^2 = 49$: the area is $49\pi$. The radius is $7$, so the circumference is $14\pi$.") +
    ex('B', r"$x^2 + y^2 + 10y = 119$. Add $25$ to both sides: $x^2 + (y + 5)^2 = 144$. The area is $144\pi$, and the circumference is $2\pi(12) = 24\pi$.") +
    ex('C', r"$(x + 2)^2 + y^2 = 20$: the area is $20\pi$. The radius is $\sqrt{20} = 2\sqrt{5}$, so the circumference is $4\sqrt{5}\,\pi$.") +
    note(r"The right side is already $r^2$. In Example A the area is $49\pi$, not $49^2\pi$.")) + \
rule(4, 'Writing the equation from a center and a point, or from a diameter', True, r'''
<p class="ref-lead">To write the equation of a circle you need two things: the center and $r^2$. A question may give them indirectly, as the center and one point on the circle, or as the two ends of a diameter.</p>
''' + figslot('r_diam') + r'''<div class="fbox">
''' + frow('a center and a point', r"$r^2 = (x_1 - h)^2 + (y_1 - k)^2$, the squared distance from the center to the point") +
      frow('the ends of a diameter', r"the center is the midpoint: $\left(\dfrac{x_1 + x_2}{2}, \dfrac{y_1 + y_2}{2}\right)$") +
      frow('then the radius', r"the distance from the center to either end, which is half of the diameter") +
      frow('testing a point', r"substitute it into the left side: equal to $r^2$ means on the circle, less means inside, greater means outside") + r'''</div>
''' + ex('A', r"A circle has center $(2, -1)$ and passes through $(5, 3)$. Then $r^2 = (5 - 2)^2 + (3 + 1)^2 = 9 + 16 = 25$, and the equation is $(x - 2)^2 + (y + 1)^2 = 25$.") +
    ex('B', r"A diameter has endpoints $(0, 1)$ and $(6, 5)$. The center is the midpoint, $(3, 3)$. From the center to $(6, 5)$: $r^2 = 3^2 + 2^2 = 13$. The equation is $(x - 3)^2 + (y - 3)^2 = 13$.") +
    ex('C', r"Is $(5, 2)$ on the circle from Example A? $(5 - 2)^2 + (2 + 1)^2 = 9 + 9 = 18$, which is less than $25$, so the point is inside the circle. For $(6, 2)$ the left side is $16 + 9 = 25$, so that point is on the circle.") +
    note(r"You need $r^2$ to write the equation, not $r$. In Example B, leaving $r^2 = 13$ as it is avoids a square root.")) + \
rule(5, 'Circles that touch an axis', False, r'''
<p class="ref-lead">A circle is tangent to a line when it touches the line at one point. When that line is an axis, the radius drawn to the touching point is perpendicular to the axis, so the radius equals the distance from the center to that axis.</p>
<div class="fig-row">
<div class="figcap">''' + figslot('r_tanx').strip() + r'''<div class="cap">tangent to the $x$-axis: $r = 3$</div></div>
<div class="figcap">''' + figslot('r_tany').strip() + r'''<div class="cap">tangent to the $y$-axis: $r = 3$</div></div>
</div>
<div class="fbox">
''' + frow('tangent to the x-axis', r"$r = |k|$, and the circle touches the axis at $(h, 0)$") +
      frow('tangent to the y-axis', r"$r = |h|$, and the circle touches the axis at $(0, k)$") +
      frow('where a circle crosses an axis', r"set $y = 0$ to find $x$-intercepts, or $x = 0$ to find $y$-intercepts") + r'''</div>
''' + ex('A', r"A circle with center $(4, 3)$ is tangent to the $x$-axis. The center is $3$ units above the axis, so $r = 3$ and the equation is $(x - 4)^2 + (y - 3)^2 = 9$. The circle touches the axis at $(4, 0)$.") +
    ex('B', r"$\overline{AB}$ is a diameter parallel to the $x$-axis, $B$ is the point $(11, 4)$, and the circle is tangent to the $x$-axis at $P(k, 0)$. A diameter passes through the center, so the center is $4$ units above the axis and $r = 4$. The center is $4$ units to the left of $B$, at $(7, 4)$, so $k = 7$.") +
    ex('C', r"Where does $(x - 6)^2 + (y - 4)^2 = 25$ cross the $x$-axis? Set $y = 0$: $(x - 6)^2 + 16 = 25$, so $(x - 6)^2 = 9$ and $x = 3$ or $x = 9$.") +
    note(r"A quick sketch helps. Mark the center, draw a radius straight to the axis, and label its length.")) + \
rule(6, 'Symmetry and semicircles', False, r'''
<p class="ref-lead">A circle is symmetric about the vertical line and the horizontal line through its center. Two points on the circle at the same height sit the same distance to the left and to the right of the center. Semicircle questions lean on this.</p>
''' + figslot('r_semi') + r'''<div class="fbox">
''' + frow('equal y-coordinates', r"the $x$-coordinates average to $h$, so $x_1 + x_2 = 2h$") +
      frow('highest and lowest points', r"$(h, k + r)$ and $(h, k - r)$") +
      frow('leftmost and rightmost points', r"$(h - r, k)$ and $(h + r, k)$") +
      frow('a semicircle on the x-axis', r"the center is the midpoint of the two endpoints, and the highest point is $(h, r)$") + r'''</div>
''' + ex('A', r"A semicircle meets the $x$-axis at $(1, 0)$ and $(11, 0)$. The center is $(6, 0)$ and the radius is $5$. Two points with equal $y$-coordinates have $x$-coordinates that add to $12$, such as $3$ and $9$.") +
    ex('B', r"The highest point of a semicircle is $(-1, 6)$, and its diameter lies on the $x$-axis. The center is straight below the highest point, at $(-1, 0)$, and $r = 6$. The endpoints are $(-7, 0)$ and $(5, 0)$.") +
    ex('C', r"On the circle $(x - 4)^2 + (y - 9)^2 = 25$, the greatest $y$-coordinate is $9 + 5 = 14$ and the least is $9 - 5 = 4$.") +
    note(r"If two points on a circle have the same $x$-coordinate instead, their $y$-coordinates average to $k$.")) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common reading and setup mistakes. Review them so you know what to check when an answer seems off.</p>
''' + mistake(1, 'keeping the signs you see', r"$(x + 3)^2 + (y - 8)^2 = 4$ has center $(-3, 8)$, not $(3, -8)$. Standard form subtracts the coordinates of the center, so $x + 3$ means $h = -3$.") + \
      mistake(2, 'using the right side as the radius', r"In $(x - 1)^2 + (y - 6)^2 = 49$ the right side is $r^2$. The radius is $7$, not $49$.") + \
      mistake(3, 'squaring the right side again for the area', r"The area is $\pi r^2$, and the right side of standard form is already $r^2$. For $(x - 1)^2 + (y - 6)^2 = 49$ the area is $49\pi$.") + \
      mistake(4, 'adding to one side only', r"To complete the squares in $x^2 + y^2 - 6x + 4y = 12$ you add $9$ and $4$ on the left. Add them on the right as well: $12 + 9 + 4 = 25$.") + \
      mistake(5, 'completing the square with a number in front', r"In $2x^2 + 2y^2 - 12x + 4y = 78$, divide every term by $2$ before you complete the squares, including the $78$.") + \
      mistake(6, 'using the whole diameter as the radius', r"When two points are the ends of a diameter, the distance between them is $2r$. Measure from the midpoint to one end, or halve the distance, before you square it.") + \
      mistake(7, 'choosing the other coordinate for a tangent circle', r"A circle with center $(5, -4)$ that is tangent to the $x$-axis has radius $4$, its distance from the $x$-axis. The $5$ is its distance from the $y$-axis.") + \
      mistake(8, 'stopping one step early', r"After you find the center and the radius, reread the question. It may ask for the diameter, the area, the circumference, or one coordinate of the center.")

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Standard form, center and radius",
  "rule": r"$(x - h)^2 + (y - k)^2 = r^2$ &nbsp;·&nbsp; center $(h, k)$ &nbsp;·&nbsp; radius $r$",
  "say": r"Match the equation to the form one piece at a time. Rewrite a plus sign as subtracting a negative number, and take the square root of the right side.",
  "prob": r"The equation $(x + 4)^2 + (y - 7)^2 = 81$ represents a circle in the $xy$-plane. What are the center and the radius of the circle?",
  "sol": r"<strong>Given:</strong> $(x + 4)^2 + (y - 7)^2 = 81$, which is already in standard form.<br><strong>Step 1: the center.</strong> $x + 4 = x - (-4)$, so $h = -4$. From $y - 7$, $k = 7$. The center is $(-4, 7)$.<br><strong>Step 2: the radius.</strong> $r^2 = 81$, so $r = 9$.<br><strong>Check:</strong> the point $9$ units to the right of the center is $(5, 7)$, and $(5 + 4)^2 + (7 - 7)^2 = 81$. ✓",
  "trap": r"Reading the center as $(4, -7)$, or the radius as $81$. Each sign is the opposite of the one you see, and the right side is $r^2$.",
  "micro": {"q": r"For the circle $(x - 6)^2 + (y + 1)^2 = 64$, the radius is", "accept": ["8"],
            "exp": r"$r^2 = 64$, so $r = 8$. The center is $(6, -1)$."}},
 {"ess": True, "name": "Rule 2: Completing the square",
  "rule": r"group the $x$ terms and the $y$ terms &nbsp;·&nbsp; add $\left(\dfrac{b}{2}\right)^2$ for each group &nbsp;·&nbsp; add the same numbers to the other side",
  "say": r"Take half of each linear coefficient and square it. Those two numbers go on both sides of the equation.",
  "prob": r"In the $xy$-plane, a circle has the equation $x^2 + y^2 + 4x - 10y = 20$. What is the radius of the circle?",
  "sol": r"<strong>Given:</strong> $x^2 + y^2 + 4x - 10y = 20$.<br><strong>Step 1: group.</strong> $(x^2 + 4x) + (y^2 - 10y) = 20$<br><strong>Step 2: find the numbers to add.</strong> Half of $4$ is $2$, and $2^2 = 4$. Half of $-10$ is $-5$, and $(-5)^2 = 25$.<br><strong>Step 3: add them to both sides.</strong> $(x + 2)^2 + (y - 5)^2 = 20 + 4 + 25 = 49$<br><strong>Step 4: read the radius.</strong> $r = \sqrt{49} = 7$<br><strong>Check:</strong> the center is $(-2, 5)$, so $(5, 5)$ should be on the circle. In the original equation, $25 + 25 + 20 - 50 = 20$. ✓",
  "trap": r"Adding $4$ and $25$ on the left only, which leaves $r^2 = 20$. Whatever you add to complete the squares has to be added to the right side too.",
  "micro": {"q": r"The circle $x^2 + y^2 - 8x = 9$ has radius", "accept": ["5"],
            "exp": r"Add $16$ to both sides: $(x - 4)^2 + y^2 = 25$, so $r = 5$."}},
 {"ess": True, "name": "Rule 3: Area and circumference from the equation",
  "rule": r"area $= \pi r^2$ &nbsp;·&nbsp; circumference $= 2\pi r$ &nbsp;·&nbsp; the right side of standard form is $r^2$",
  "say": r"Get to standard form first. Then decide whether the question needs $r^2$ (area) or $r$ (circumference or diameter).",
  "prob": r"What is the area of the circle in the $xy$-plane with equation $x^2 - 6x + y^2 + 8y = 75$?",
  "sol": r"<strong>Given:</strong> $x^2 - 6x + y^2 + 8y = 75$.<br><strong>Step 1: complete the squares.</strong> Add $9$ and $16$ to both sides: $(x - 3)^2 + (y + 4)^2 = 100$<br><strong>Step 2: read $r^2$.</strong> $r^2 = 100$<br><strong>Step 3: area.</strong> $\pi r^2 = 100\pi$<br><strong>Check:</strong> $r = 10$, and $\pi(10)^2 = 100\pi$. ✓",
  "trap": r"Using $75$ as $r^2$ and answering $75\pi$. The constant on the right changes when you complete the squares. A second slip is squaring $100$ again: the right side of standard form is already $r^2$.",
  "micro": {"mc": True, "q": r"What is the circumference of the circle $x^2 + y^2 + 2y = 35$?", "opts": [r"$6\pi$", r"$12\pi$", r"$36\pi$", r"$72\pi$"], "correct": 1,
            "exp": r"Add $1$ to both sides: $x^2 + (y + 1)^2 = 36$, so $r = 6$ and the circumference is $2\pi(6) = 12\pi$. The area is $36\pi$."}},
 {"ess": True, "name": "Rule 4: Writing the equation",
  "rule": r"a center and a point: $r^2 = (x_1 - h)^2 + (y_1 - k)^2$ &nbsp;·&nbsp; the ends of a diameter: the center is the midpoint",
  "say": r"Find the center and $r^2$, then place them in standard form. You do not need the radius itself.",
  "prob": r"A circle in the $xy$-plane has its center at $(-3, 2)$ and passes through the point $(3, 10)$. What is an equation of the circle?",
  "sol": r"<strong>Given:</strong> center $(-3, 2)$, and the point $(3, 10)$ on the circle.<br><strong>Step 1: find $r^2$.</strong> $r^2 = (3 - (-3))^2 + (10 - 2)^2 = 36 + 64 = 100$<br><strong>Step 2: write standard form.</strong> $(x + 3)^2 + (y - 2)^2 = 100$<br><strong>Check:</strong> substitute $(3, 10)$: $6^2 + 8^2 = 100$. ✓",
  "trap": r"Writing $(x - 3)^2 + (y + 2)^2$ on the left, or $10$ on the right. The center $(-3, 2)$ gives $x + 3$ and $y - 2$, and the right side is $r^2 = 100$.",
  "micro": {"q": r"A diameter of a circle has endpoints $(2, 5)$ and $(10, 11)$. The radius of the circle is", "accept": ["5"],
            "exp": r"The center is the midpoint, $(6, 8)$. From there to $(10, 11)$ is $4$ across and $3$ up, so $r = 5$."}},
 {"ess": False, "name": "Rule 5: A circle that touches an axis", "fig": "s5",
  "rule": r"tangent to the $x$-axis: $r = |k|$ &nbsp;·&nbsp; tangent to the $y$-axis: $r = |h|$",
  "say": r"Find how far the center is from the axis the circle touches. That distance is the radius.",
  "prob": r"In the $xy$-plane above, $\overline{AB}$ is a diameter of the circle and is parallel to the $x$-axis. The circle is tangent to the $x$-axis at the point $P(k, 0)$, and $B$ is the point $(13, 5)$. What is the value of $k$?",
  "sol": r"<strong>Given:</strong> a horizontal diameter $\overline{AB}$ with $B = (13, 5)$, and a circle that touches the $x$-axis at $P(k, 0)$.<br><strong>Step 1: find the radius.</strong> A diameter passes through the center, so the center is at height $5$. The circle touches the $x$-axis, so $r = 5$.<br><strong>Step 2: find the center.</strong> The center is $5$ units to the left of $B$: $(8, 5)$.<br><strong>Step 3: find $P$.</strong> $P$ is straight below the center, so $k = 8$.<br><strong>Check:</strong> $A$ is $5$ units to the left of the center, at $(3, 5)$, and $AB = 13 - 3 = 10 = 2r$. ✓",
  "trap": r"Halving $13$ to get $k = 6.5$. That would be correct only if $A$ were on the $y$-axis. Use the height of the diameter to find the radius first.",
  "micro": {"q": r"A circle with center $(-6, 4)$ is tangent to the $y$-axis. Its radius is", "accept": ["6"],
            "exp": r"The center is $6$ units from the $y$-axis, so $r = 6$. The $4$ is its distance from the $x$-axis."}},
 {"ess": False, "name": "Rule 6: Symmetry and semicircles", "fig": "s6",
  "rule": r"equal heights: $x_1 + x_2 = 2h$ &nbsp;·&nbsp; highest point of a semicircle on the $x$-axis: $(h, r)$",
  "say": r"Locate the center first. On a semicircle whose diameter is on the $x$-axis, the center is straight below the highest point.",
  "prob": r"In the $xy$-plane above, the semicircle has its highest point at $P(6, 10)$, and its diameter lies on the $x$-axis. What are the coordinates of point $Q$?",
  "sol": r"<strong>Given:</strong> highest point $P(6, 10)$, diameter on the $x$-axis, and $Q$ at the left end of the diameter.<br><strong>Step 1: find the center.</strong> It is on the $x$-axis, straight below $P$: $(6, 0)$.<br><strong>Step 2: find the radius.</strong> $P$ is $10$ units above the center, so $r = 10$.<br><strong>Step 3: find $Q$.</strong> $Q$ is $10$ units to the left of the center: $(-4, 0)$.<br><strong>Check:</strong> the right end of the diameter is $(16, 0)$, and the midpoint of $-4$ and $16$ is $6$. ✓",
  "trap": r"Answering $(-6, 0)$ by reflecting the $6$ across the $y$-axis. The semicircle is symmetric about the vertical line through its center, $x = 6$, not about the $y$-axis.",
  "micro": {"q": r"A semicircle meets the $x$-axis at $(-5, 0)$ and $(9, 0)$. Two points on it have equal $y$-coordinates. One has $x$-coordinate $-1$. The other has $x$-coordinate", "accept": ["5"],
            "exp": r"The center is at $x = 2$, and $-1$ is $3$ units to its left. The matching point is $3$ units to its right, at $x = 5$."}},
]
LAST_STARRED_STEP_INDEX = 3  # 0-based index of the last starred step (Rule 4)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
FLUENCY = [
 {"sec": "A. Read the center and the radius", "items": [
   {"q": r"The radius of $(x - 5)^2 + (y - 2)^2 = 16$ is", "accept": ["4"], "exp": r"$r^2 = 16$, so $r = 4$."},
   {"q": r"The $x$-coordinate of the center of $(x + 7)^2 + (y - 3)^2 = 1$ is", "accept": ["-7"], "exp": r"$x + 7 = x - (-7)$, so $h = -7$."},
   {"q": r"The $y$-coordinate of the center of $x^2 + (y + 9)^2 = 121$ is", "accept": ["-9"], "exp": r"$y + 9 = y - (-9)$, so $k = -9$. The center is $(0, -9)$."},
   {"q": r"The diameter of $(x - 4)^2 + (y + 6)^2 = 400$ is", "accept": ["40"], "exp": r"$r = 20$, and the diameter is $2r = 40$."},
   {"q": r"A circle has center $(2, -8)$ and radius $3$. Its equation is $(x - 2)^2 + (y + 8)^2 = c$, where $c =$", "accept": ["9"], "exp": r"The right side is $r^2 = 9$."},
 ]},
 {"sec": "B. Complete the square", "items": [
   {"q": r"$x^2 + 12x + c$ is a perfect square when $c =$", "accept": ["36"], "exp": r"Half of $12$ is $6$, and $6^2 = 36$: $x^2 + 12x + 36 = (x + 6)^2$."},
   {"q": r"$y^2 - 5y + c$ is a perfect square when $c =$", "accept": ["25/4", "6.25"], "exp": r"Half of $-5$ is $-\dfrac{5}{2}$, and its square is $\dfrac{25}{4}$."},
   {"q": r"The radius of $x^2 + y^2 - 2x - 6y = 26$ is", "accept": ["6"], "exp": r"Add $1$ and $9$ to both sides: $(x - 1)^2 + (y - 3)^2 = 36$."},
   {"q": r"The radius of $x^2 + y^2 + 18x = 19$ is", "accept": ["10"], "exp": r"Add $81$ to both sides: $(x + 9)^2 + y^2 = 100$."},
   {"q": r"The radius of $3x^2 + 3y^2 - 12y = 36$ is", "accept": ["4"], "exp": r"Divide by $3$: $x^2 + y^2 - 4y = 12$. Add $4$ to both sides: $x^2 + (y - 2)^2 = 16$."},
 ]},
 {"sec": "C. Area and circumference", "items": [
   {"q": r"The area of $(x - 2)^2 + (y - 2)^2 = 64$ is $a\pi$, where $a =$", "accept": ["64"], "exp": r"The right side is $r^2$, so the area is $64\pi$."},
   {"q": r"The circumference of $(x + 1)^2 + y^2 = 81$ is $c\pi$, where $c =$", "accept": ["18"], "exp": r"$r = 9$, and $2\pi(9) = 18\pi$."},
   {"q": r"The area of $x^2 + y^2 = 30$ is $a\pi$, where $a =$", "accept": ["30"], "exp": r"$r^2 = 30$, so the area is $30\pi$. No square root is needed."},
   {"q": r"The circumference of $x^2 + y^2 - 14x = 0$ is $c\pi$, where $c =$", "accept": ["14"], "exp": r"Add $49$ to both sides: $(x - 7)^2 + y^2 = 49$. Then $r = 7$, and $2\pi(7) = 14\pi$."},
   {"q": r"A circle with center $(0, 3)$ has area $196\pi$. Its equation is $x^2 + (y - 3)^2 = c$, where $c =$", "accept": ["196"], "exp": r"An area of $196\pi$ means $r^2 = 196$."},
 ]},
 {"sec": "D. Write the equation", "items": [
   {"q": r"A circle centered at the origin passes through $(-2, 7)$. For this circle, $r^2 =$", "accept": ["53"], "exp": r"$(-2)^2 + 7^2 = 4 + 49 = 53$. The equation is $x^2 + y^2 = 53$."},
   {"q": r"A circle has center $(1, 4)$ and passes through $(7, 12)$. Its radius is", "accept": ["10"], "exp": r"$6$ across and $8$ up: $r^2 = 36 + 64 = 100$, so $r = 10$."},
   {"q": r"A diameter has endpoints $(-7, 0)$ and $(3, 0)$. The $x$-coordinate of the center is", "accept": ["-2"], "exp": r"The center is the midpoint: $\dfrac{-7 + 3}{2} = -2$."},
   {"q": r"A diameter has endpoints $(2, 1)$ and $(8, 9)$. The radius is", "accept": ["5"], "exp": r"The center is $(5, 5)$. From there to $(8, 9)$ is $3$ across and $4$ up, so $r = 5$."},
   {"mc": True, "q": r"Compared with the circle $(x - 3)^2 + (y - 1)^2 = 20$, the point $(5, 4)$ is", "opts": ["inside the circle", "on the circle", "outside the circle"], "correct": 0,
    "exp": r"$(5 - 3)^2 + (4 - 1)^2 = 4 + 9 = 13$, which is less than $20$."},
 ]},
 {"sec": "E. Tangent circles, symmetry and semicircles", "items": [
   {"q": r"A circle with center $(5, -3)$ is tangent to the $x$-axis. Its radius is", "accept": ["3"], "exp": r"The center is $3$ units from the $x$-axis."},
   {"q": r"A circle with center $(-8, 6)$ is tangent to the $y$-axis. Its radius is", "accept": ["8"], "exp": r"The center is $8$ units from the $y$-axis."},
   {"q": r"The greatest $y$-coordinate of a point on $(x + 1)^2 + (y - 7)^2 = 16$ is", "accept": ["11"], "exp": r"The highest point is one radius above the center: $7 + 4 = 11$."},
   {"q": r"Two points on $(x + 2)^2 + (y - 1)^2 = 49$ have the same $y$-coordinate. One has $x$-coordinate $3$. The other has $x$-coordinate", "accept": ["-7"], "exp": r"The center is at $x = -2$. The point at $x = 3$ is $5$ units to the right, so the other point is $5$ units to the left, at $x = -7$."},
   {"q": r"A semicircle above the $x$-axis has a diameter from $(2, 0)$ to $(14, 0)$. The $y$-coordinate of its highest point is", "accept": ["6"], "exp": r"The diameter is $12$, so $r = 6$. The highest point is $(8, 6)$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"The equation $(x - 9)^2 + (y + 4)^2 = 36$ represents a circle in the $xy$-plane. What are the coordinates of the center of the circle?",
  "options": [r"$(-9, 4)$", r"$(-9, -4)$", r"$(9, -4)$", r"$(9, 4)$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $(x - 9)^2 + (y + 4)^2 = 36$, in standard form $(x - h)^2 + (y - k)^2 = r^2$.<br><br><strong>Match $x$:</strong> $x - 9$ gives $h = 9$.<br><strong>Match $y$:</strong> $y + 4 = y - (-4)$ gives $k = -4$.<br>The center is $(9, -4)$.<br><strong>Check:</strong> at $(9, -4)$ both squares are $0$, which happens only at the center. ✓",
  "trap": r"Choice A reads the signs as they appear, $-9$ and $+4$. Standard form subtracts the coordinates of the center, so each sign is the opposite of the one you see."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"A circle in the $xy$-plane has the equation $(x + 2)^2 + (y - 11)^2 = 169$. What is the diameter of the circle?",
  "label": "Diameter $=$", "accept": ["26"],
  "sol": r"<strong>Given:</strong> $(x + 2)^2 + (y - 11)^2 = 169$.<br><br><strong>Radius:</strong> $r^2 = 169$, so $r = 13$.<br><strong>Diameter:</strong> $2r = 26$<br><strong>Check:</strong> half of $26$ is $13$, and $13^2 = 169$. ✓",
  "trap": r"Entering $13$, the radius, or $169$. The question asks for the diameter, which is twice the radius."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"Which equation represents a circle in the $xy$-plane with center $(5, -7)$ and radius $4$?",
  "options": [r"$(x - 5)^2 + (y + 7)^2 = 4$", r"$(x + 5)^2 + (y - 7)^2 = 16$", r"$(x - 5)^2 + (y + 7)^2 = 16$", r"$(x + 5)^2 + (y - 7)^2 = 4$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $h = 5$, $k = -7$ and $r = 4$.<br><br><strong>Left side:</strong> $x - 5$, and $y - (-7) = y + 7$.<br><strong>Right side:</strong> $r^2 = 16$<br>The equation is $(x - 5)^2 + (y + 7)^2 = 16$.<br><strong>Check:</strong> the point $4$ units to the right of the center is $(9, -7)$, and $(9 - 5)^2 + 0^2 = 16$. ✓",
  "trap": r"Choice A has the correct center but puts $r$ on the right side instead of $r^2$. Choice B squares the radius but keeps the signs of the center."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"What is the area of the circle in the $xy$-plane with equation $x^2 + 2x + y^2 - 12y = 12$?",
  "options": [r"$7\pi$", r"$12\pi$", r"$14\pi$", r"$49\pi$"], "correct": 3, "desmos": ["x^2+2x+y^2-12y=12"],
  "sol": r"<strong>Given:</strong> $x^2 + 2x + y^2 - 12y = 12$.<br><br><strong>Complete the squares:</strong> half of $2$ is $1$, and half of $-12$ is $-6$. Add $1$ and $36$ to both sides: $(x + 1)^2 + (y - 6)^2 = 49$<br><strong>Area:</strong> $\pi r^2 = 49\pi$<br><strong>Check:</strong> $r = 7$, and $\pi(7)^2 = 49\pi$. ✓",
  "trap": r"Choice B uses the $12$ from the original equation as $r^2$. Choice C is the circumference, $2\pi(7)$."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"The circle in the $xy$-plane with equation $x^2 + y^2 - 16y = 36$ has a circumference of $k\pi$. What is the value of $k$?",
  "label": "$k =$", "accept": ["20"], "desmos": ["x^2+y^2-16y=36"],
  "sol": r"<strong>Given:</strong> $x^2 + y^2 - 16y = 36$, and the circumference is $k\pi$.<br><br><strong>Complete the square:</strong> add $64$ to both sides: $x^2 + (y - 8)^2 = 100$<br><strong>Radius:</strong> $r = 10$<br><strong>Circumference:</strong> $2\pi(10) = 20\pi$, so $k = 20$.<br><strong>Check:</strong> the center is $(0, 8)$, so $(0, 18)$ should be on the circle. In the original equation, $0 + 324 - 288 = 36$. ✓",
  "trap": r"Reading $r^2 = 36$ from the original equation, which gives $r = 6$ and $k = 12$. Complete the square before you read the radius. Entering $100$ answers a question about the area instead."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p6",
  "stem": r"The circle shown in the $xy$-plane has its center at $(2, 1)$ and passes through the point $(6, 4)$. Which equation represents the circle?",
  "options": [r"$(x - 2)^2 + (y - 1)^2 = 5$", r"$(x + 2)^2 + (y + 1)^2 = 25$", r"$(x - 2)^2 + (y - 1)^2 = 25$", r"$(x - 6)^2 + (y - 4)^2 = 25$"], "correct": 2,
  "sol": r"<strong>Given:</strong> center $(2, 1)$, and the point $(6, 4)$ on the circle.<br><br><strong>Find $r^2$:</strong> $(6 - 2)^2 + (4 - 1)^2 = 16 + 9 = 25$<br><strong>Standard form:</strong> $(x - 2)^2 + (y - 1)^2 = 25$<br><strong>Check:</strong> the graph reaches $x = 7$ at the height of the center, which is $5$ units to the right, and $5^2 = 25$. ✓",
  "trap": r"Choice A puts the radius, $5$, on the right side instead of $r^2$. Choice D uses the point on the circle as the center."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"In the $xy$-plane, the points $(-1, -4)$ and $(3, 8)$ are the endpoints of a diameter of a circle. Which equation represents the circle?",
  "options": [r"$(x - 1)^2 + (y - 2)^2 = 40$", r"$(x - 1)^2 + (y - 2)^2 = 160$", r"$(x + 1)^2 + (y + 2)^2 = 40$", r"$(x - 2)^2 + (y - 6)^2 = 40$"], "correct": 0,
  "sol": r"<strong>Given:</strong> the ends of a diameter, $(-1, -4)$ and $(3, 8)$.<br><br><strong>Center:</strong> the midpoint is $\left(\dfrac{-1 + 3}{2}, \dfrac{-4 + 8}{2}\right) = (1, 2)$.<br><strong>Find $r^2$:</strong> from $(1, 2)$ to $(3, 8)$ is $2$ across and $6$ up, so $r^2 = 4 + 36 = 40$.<br><strong>Standard form:</strong> $(x - 1)^2 + (y - 2)^2 = 40$<br><strong>Check:</strong> the other end, $(-1, -4)$, gives $(-2)^2 + (-6)^2 = 40$. ✓",
  "trap": r"Choice B uses the whole diameter: $4^2 + 12^2 = 160$ is the diameter squared, not $r^2$. Choice D uses half of each difference, $2$ and $6$, as the center instead of the midpoint."},
 {"ess": False, "type": "ne", "diff": "Medium", "fig": "p8",
  "stem": r"In the $xy$-plane above, $\overline{AB}$ is a diameter of the circle and is parallel to the $x$-axis. The circle is tangent to the $x$-axis at the point $P(k, 0)$, and $B$ is the point $(17, 7)$. What is the value of $k$?",
  "label": "$k =$", "accept": ["10"],
  "sol": r"<strong>Given:</strong> a horizontal diameter $\overline{AB}$ with $B = (17, 7)$, and a circle that touches the $x$-axis at $P(k, 0)$.<br><br><strong>Radius:</strong> the center is on $\overline{AB}$, at height $7$. The circle touches the $x$-axis, so $r = 7$.<br><strong>Center:</strong> $7$ units to the left of $B$: $(10, 7)$.<br><strong>Point $P$:</strong> straight below the center, so $k = 10$.<br><strong>Check:</strong> $A$ is $(3, 7)$, and $AB = 17 - 3 = 14 = 2r$. ✓",
  "trap": r"Entering $8.5$, half of $17$. That assumes the circle also touches the $y$-axis. The radius comes from the height of the diameter, which is $7$."},
 {"ess": False, "type": "mc", "diff": "Medium-hard", "fig": "p9",
  "stem": r"The semicircle shown in the $xy$-plane meets the $x$-axis at $(-6, 0)$ and $(14, 0)$. Which of the following are the $x$-coordinates of two points on the semicircle whose $y$-coordinates are equal?",
  "options": [r"$-2$ and $9$", r"$0$ and $9$", r"$1$ and $7$", r"$3$ and $6$"], "correct": 2,
  "sol": r"<strong>Given:</strong> the ends of the diameter are $(-6, 0)$ and $(14, 0)$.<br><br><strong>Center:</strong> the midpoint has $x$-coordinate $\dfrac{-6 + 14}{2} = 4$.<br><strong>Symmetry:</strong> two points at the same height are mirror images across the line $x = 4$, so their $x$-coordinates add to $8$.<br><strong>Test the sums:</strong> $-2 + 9 = 7$, $0 + 9 = 9$, $1 + 7 = 8$, $3 + 6 = 9$. Only $1$ and $7$ work.<br><strong>Check:</strong> $1$ is $3$ units to the left of $4$, and $7$ is $3$ units to the right. ✓",
  "trap": r"Choosing a pair that looks balanced without finding the center. Choices A and D have sums of $7$ and $9$. Find the $x$-coordinate of the center first, then look for the pair centered on it."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"In the $xy$-plane, the graph of $2x^2 + 2y^2 + 12x - 20y = 94$ is a circle. What is the radius of the circle?",
  "label": "Radius $=$", "accept": ["9"], "desmos": ["2x^2+2y^2+12x-20y=94"],
  "sol": r"<strong>Given:</strong> $2x^2 + 2y^2 + 12x - 20y = 94$.<br><br><strong>Divide by $2$:</strong> $x^2 + y^2 + 6x - 10y = 47$<br><strong>Complete the squares:</strong> add $9$ and $25$ to both sides: $(x + 3)^2 + (y - 5)^2 = 81$<br><strong>Radius:</strong> $r = 9$<br><strong>Check:</strong> the center is $(-3, 5)$, so $(6, 5)$ should be on the circle. In the original equation, $72 + 50 + 72 - 100 = 94$. ✓",
  "trap": r"Completing the squares before dividing by $2$. Standard form needs $x^2$ and $y^2$ with a coefficient of $1$, so divide every term first, including the $94$."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"In the $xy$-plane, the circle with equation $x^2 + y^2 - 8x + 6y = c$ has a radius of $7$, where $c$ is a constant. What is the value of $c$?",
  "label": "$c =$", "accept": ["24"],
  "sol": r"<strong>Given:</strong> $x^2 + y^2 - 8x + 6y = c$ and $r = 7$.<br><br><strong>Complete the squares:</strong> add $16$ and $9$ to both sides: $(x - 4)^2 + (y + 3)^2 = c + 25$<br><strong>Use the radius:</strong> the right side is $r^2$, so $c + 25 = 49$ and $c = 24$.<br><strong>Check:</strong> with $c = 24$ the right side is $24 + 25 = 49 = 7^2$. ✓",
  "trap": r"Setting $c = 49$. The constant in the expanded equation is not $r^2$: the $16$ and the $9$ from completing the squares are added to it first.",
  "extrasIntro": r"A constant to find from the radius or the area: complete the squares, then set the right side equal to $r^2$. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The circle $x^2 + y^2 + 10x = c$ has radius $8$. The value of $c$ is", "label": "$c =$", "accept": ["39"], "exp": r"Add $25$ to both sides: $(x + 5)^2 + y^2 = c + 25$. Then $c + 25 = 64$."},
   {"type": "ne", "q": r"The circle $x^2 + y^2 - 4x - 12y = c$ has radius $9$. The value of $c$ is", "label": "$c =$", "accept": ["41"], "exp": r"Add $4$ and $36$ to both sides: the right side is $c + 40$, and $c + 40 = 81$."},
   {"type": "ne", "q": r"The circle $x^2 + y^2 + 2x + 2y = c$ has area $20\pi$. The value of $c$ is", "label": "$c =$", "accept": ["18"], "exp": r"Add $1$ and $1$ to both sides: the right side is $c + 2$. An area of $20\pi$ means $r^2 = 20$, so $c = 18$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"The point $(a, 5)$ lies on the circle with equation $(x - 3)^2 + (y + 1)^2 = 100$ in the $xy$-plane. If $a > 0$, what is the value of $a$?",
  "label": "$a =$", "accept": ["11"],
  "sol": r"<strong>Given:</strong> $(a, 5)$ is on $(x - 3)^2 + (y + 1)^2 = 100$, and $a > 0$.<br><br><strong>Substitute $y = 5$:</strong> $(a - 3)^2 + 36 = 100$, so $(a - 3)^2 = 64$.<br><strong>Solve:</strong> $a - 3 = 8$ or $a - 3 = -8$, so $a = 11$ or $a = -5$.<br><strong>Use the condition:</strong> $a > 0$, so $a = 11$.<br><strong>Check:</strong> $(11 - 3)^2 + (5 + 1)^2 = 64 + 36 = 100$. ✓",
  "trap": r"Solving $(a - 3)^2 = 64$ as $a - 3 = 64$, or forgetting that a square has two roots. A horizontal line crosses the circle at two points, here $(11, 5)$ and $(-5, 5)$, and the condition $a > 0$ chooses between them.",
  "extrasIntro": r"A point with one coordinate missing: substitute what you know, then solve the squared equation. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The point $(4, b)$ lies on the circle $x^2 + y^2 = 41$, and $b > 0$. The value of $b$ is", "label": "$b =$", "accept": ["5"], "exp": r"$16 + b^2 = 41$, so $b^2 = 25$ and $b = 5$."},
   {"type": "ne", "q": r"The point $(a, -2)$ lies on the circle $(x + 1)^2 + (y - 4)^2 = 45$, and $a > 0$. The value of $a$ is", "label": "$a =$", "accept": ["2"], "exp": r"$(a + 1)^2 + 36 = 45$, so $(a + 1)^2 = 9$ and $a = 2$ or $a = -4$."},
   {"type": "ne", "q": r"The point $(7, b)$ lies on the circle $(x - 2)^2 + (y - 3)^2 = 169$, and $b < 0$. The value of $b$ is", "label": "$b =$", "accept": ["-9"], "exp": r"$25 + (b - 3)^2 = 169$, so $(b - 3)^2 = 144$ and $b = 15$ or $b = -9$."},
  ]},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"A circle in the $xy$-plane has center $(-2, 3)$ and radius $5$. Which of the following points lies inside the circle?",
  "options": [r"$(3, 3)$", r"$(1, 7)$", r"$(2, 5)$", r"$(-2, -3)$"], "correct": 2,
  "sol": r"<strong>Given:</strong> center $(-2, 3)$ and $r = 5$, so the equation is $(x + 2)^2 + (y - 3)^2 = 25$.<br><br>Substitute each point into the left side and compare with $25$.<br><strong>$(3, 3)$:</strong> $25 + 0 = 25$, on the circle.<br><strong>$(1, 7)$:</strong> $9 + 16 = 25$, on the circle.<br><strong>$(2, 5)$:</strong> $16 + 4 = 20$, less than $25$, so inside.<br><strong>$(-2, -3)$:</strong> $0 + 36 = 36$, greater than $25$, so outside.",
  "trap": r"Choices A and B are on the circle, not inside it: their squared distances from the center equal $25$. A point is inside when the left side comes out less than $r^2$."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"In the $xy$-plane, the points $P(-4, 1)$ and $Q(8, 6)$ are the endpoints of a diameter of a circle. The area of the circle is $k\pi$. What is the value of $k$?",
  "label": "$k =$", "accept": ["42.25", "169/4"],
  "sol": r"<strong>Given:</strong> the ends of a diameter, $P(-4, 1)$ and $Q(8, 6)$. The area is $k\pi$.<br><br><strong>Diameter:</strong> from $P$ to $Q$ is $12$ across and $5$ up, so the diameter is $\sqrt{144 + 25} = 13$.<br><strong>Radius:</strong> $r = \dfrac{13}{2} = 6.5$<br><strong>Area:</strong> $\pi(6.5)^2 = 42.25\pi$, so $k = 42.25$.<br><strong>Check:</strong> the midpoint is $(2, 3.5)$, and from there to $Q$ is $6$ across and $2.5$ up: $36 + 6.25 = 42.25$. ✓",
  "trap": r"Entering $169$, the diameter squared. The radius is half of $13$, and halving a length divides its square by $4$: $\dfrac{169}{4} = 42.25$."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"A circle in the $xy$-plane has its center at $(5, -4)$ and is tangent to the $x$-axis. An equation of the circle is $x^2 + y^2 + ax + by + c = 0$, where $a$, $b$ and $c$ are constants. What is the value of $c$?",
  "label": "$c =$", "accept": ["25"],
  "sol": r"<strong>Given:</strong> center $(5, -4)$, tangent to the $x$-axis, and the form $x^2 + y^2 + ax + by + c = 0$.<br><br><strong>Radius:</strong> the center is $4$ units from the $x$-axis, so $r = 4$.<br><strong>Standard form:</strong> $(x - 5)^2 + (y + 4)^2 = 16$<br><strong>Expand:</strong> $x^2 - 10x + 25 + y^2 + 8y + 16 = 16$, which simplifies to $x^2 + y^2 - 10x + 8y + 25 = 0$.<br>So $c = 25$.<br><strong>Check:</strong> $a = -10$ and $b = 8$. Completing the squares in $x^2 + y^2 - 10x + 8y = -25$ gives a right side of $-25 + 25 + 16 = 16$. ✓",
  "trap": r"Using $r = 5$, the distance from the center to the $y$-axis, which leads to $c = 16$. The circle touches the $x$-axis, so the radius is the vertical distance, $4$."},
 {"ess": False, "type": "ne", "diff": "Hard", "fig": "c6",
  "stem": r"In the $xy$-plane above, the semicircle has its highest point at $P(1, 13)$, and its diameter lies on the $x$-axis. The point $(t, 5)$ lies on the semicircle, and $t > 1$. What is the value of $t$?",
  "label": "$t =$", "accept": ["13"],
  "sol": r"<strong>Given:</strong> highest point $P(1, 13)$, diameter on the $x$-axis, and the point $(t, 5)$ on the semicircle with $t > 1$.<br><br><strong>Center and radius:</strong> the center is straight below $P$, at $(1, 0)$, and $r = 13$.<br><strong>Equation:</strong> $(x - 1)^2 + y^2 = 169$<br><strong>Substitute $y = 5$:</strong> $(t - 1)^2 + 25 = 169$, so $(t - 1)^2 = 144$ and $t = 13$ or $t = -11$.<br><strong>Use the condition:</strong> $t > 1$, so $t = 13$.<br><strong>Check:</strong> $(13 - 1)^2 + 5^2 = 144 + 25 = 169$. ✓",
  "trap": r"Using $P$ as the center. $P$ is a point on the semicircle. The center is on the $x$-axis, straight below $P$, at $(1, 0)$."},
 {"ess": True, "type": "ne", "diff": "Hard · systems blend",
  "stem": r"In the $xy$-plane, the line $y = x + 1$ intersects the circle $x^2 + y^2 = 25$ at two points. What is the $x$-coordinate of the intersection point that lies in the first quadrant?",
  "label": "$x =$", "accept": ["3"], "desmos": ["y=x+1", "x^2+y^2=25"],
  "sol": r"<strong>Given:</strong> $y = x + 1$ and $x^2 + y^2 = 25$.<br><br><strong>Substitute:</strong> $x^2 + (x + 1)^2 = 25$<br><strong>Expand:</strong> $2x^2 + 2x + 1 = 25$, so $2x^2 + 2x - 24 = 0$ and $x^2 + x - 12 = 0$.<br><strong>Factor:</strong> $(x + 4)(x - 3) = 0$, so $x = -4$ or $x = 3$.<br><strong>Use the condition:</strong> in the first quadrant $x$ is positive, so $x = 3$, and $y = 4$.<br><strong>Check:</strong> $3^2 + 4^2 = 25$, and $4 = 3 + 1$. ✓",
  "trap": r"Entering $-4$. That value solves the equation, but the point $(-4, -3)$ is in the third quadrant. Use the condition in the question to choose between the two solutions."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"What is the radius of the circle $(x + 5)^2 + (y - 12)^2 = 9$?", "opts": ["$3$", "$6$", "$9$", "$81$"], "correct": 0,
  "exp": r"The right side is $r^2$, so $r = \sqrt{9} = 3$. $9$ is $r^2$, and $6$ is the diameter."},
 {"q": r"What is the center of the circle $x^2 + y^2 - 4x + 14y = 3$?", "opts": [r"$(-2, 7)$", r"$(2, -7)$", r"$(-4, 14)$", r"$(4, -14)$"], "correct": 1,
  "exp": r"Complete the squares: $(x - 2)^2 + (y + 7)^2 = 56$. The center is $(2, -7)$: half of each linear coefficient, with the sign changed."},
 {"q": r"A circle has center $(1, -2)$ and passes through $(9, 13)$. What is its area?", "opts": [r"$17\pi$", r"$34\pi$", r"$289\pi$", r"$578\pi$"], "correct": 2,
  "exp": r"$r^2 = 8^2 + 15^2 = 289$, so the area is $289\pi$. $34\pi$ is the circumference."},
]

# ---------------------------------------------------------------- FIGURES
# Specs are Python dicts dumped to JS. Every figure on this sheet is a coordinate graph, drawn by the shell's
# graphSVG. This builder extends it with curves, a labelled grid and a clip path (as SAT Math 3 and 5 do) and with
# `circles`: a full circle, or with half=True the upper semicircle. G() sizes each figure so that one unit is the
# same number of pixels on both axes, which keeps the circles round.
def G(xmin, xmax, ymin, ymax, u=18, **k):
    return dict(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, w=int(round(44 + u * (xmax - xmin))), h=int(round(44 + u * (ymax - ymin))), **k)

MINUS = chr(8722)
FIGS = {}

# --- Rule 1: the radius as the hypotenuse of a right triangle
FIGS['r_standard'] = G(-3.5, 9.5, -4.5, 8.5, u=18,
    alt='a circle in the xy-plane with a radius drawn from the center (h, k) to a point (x, y) on the circle; the radius is the hypotenuse of a right triangle with legs x minus h and y minus k',
    circles=[dict(x=3, y=2, r=5)],
    segs=[dict(x1=3, y1=2, x2=7, y2=5, cls='ln'), dict(x1=3, y1=2, x2=7, y2=2), dict(x1=7, y1=2, x2=7, y2=5)],
    squares=[dict(x=7, y=2, u=[-1, 0], v=[0, 1])],
    points=[dict(x=3, y=2, label='(h, k)', dx=-44, dy=5), dict(x=7, y=5, label='(x, y)', dx=8, dy=-5)],
    labels=[dict(x=5, y=3.5, text='r', dx=-9, dy=-4), dict(x=5, y=2, text='x ' + MINUS + ' h', dx=-16, dy=16), dict(x=7, y=3.5, text='y ' + MINUS + ' k', dx=7, dy=5)])

# --- Rule 4: the ends of a diameter and the midpoint
FIGS['r_diam'] = G(-2.5, 9, -2.5, 8.5, u=20, grid=dict(step=1, label=2),
    alt='a circle on a grid with a diameter drawn from (0, 1) to (6, 5); the center (3, 3) is the midpoint of the diameter',
    circles=[dict(x=3, y=3, r=round(math.sqrt(13), 4))],
    segs=[dict(x1=0, y1=1, x2=6, y2=5, cls='ln')],
    points=[dict(x=0, y=1, label='(0, 1)', dx=-46, dy=14), dict(x=6, y=5, label='(6, 5)', dx=8, dy=-6), dict(x=3, y=3, label='(3, 3)', dx=4, dy=18)])

# --- Rule 5: tangent to the x-axis, tangent to the y-axis
FIGS['r_tanx'] = G(-1.5, 9, -1.5, 8, u=20, grid=dict(step=1, label=2),
    alt='a circle with center (4, 3) and radius 3 that touches the x-axis at (4, 0)',
    circles=[dict(x=4, y=3, r=3)], segs=[dict(x1=4, y1=3, x2=4, y2=0, cls='ln')],
    points=[dict(x=4, y=3, label='(4, 3)', dx=8, dy=-5), dict(x=4, y=0)],
    labels=[dict(x=4, y=1.5, text='r = 3', dx=8, dy=5)])
FIGS['r_tany'] = G(-1.5, 9, -1.5, 8, u=20, grid=dict(step=1, label=2),
    alt='a circle with center (3, 4) and radius 3 that touches the y-axis at (0, 4)',
    circles=[dict(x=3, y=4, r=3)], segs=[dict(x1=3, y1=4, x2=0, y2=4, cls='ln')],
    points=[dict(x=3, y=4, label='(3, 4)', dx=8, dy=-5), dict(x=0, y=4)],
    labels=[dict(x=1.5, y=4, text='r = 3', dx=-16, dy=17)])

# --- Rule 6: a semicircle on the x-axis, with two points at the same height
FIGS['r_semi'] = G(-1.5, 13.5, -1.5, 6.5, u=20, grid=dict(step=1, label=2),
    alt='a semicircle above the x-axis from (1, 0) to (11, 0); its highest point is (6, 5), and the points (3, 4) and (9, 4) are at the same height on either side of the vertical line through the center',
    circles=[dict(x=6, y=0, r=5, half=True)],
    segs=[dict(x1=3, y1=4, x2=9, y2=4), dict(x1=6, y1=0, x2=6, y2=5)],
    points=[dict(x=3, y=4, label='(3, 4)', dx=-46, dy=-3), dict(x=9, y=4, label='(9, 4)', dx=9, dy=-3), dict(x=6, y=5, label='(6, 5)', dx=8, dy=-6), dict(x=6, y=0)])

# --- Step 5: a horizontal diameter and a circle that touches the x-axis (center (8, 5), radius 5)
FIGS['s5'] = G(-2, 19, -2, 12, u=15,
    alt='a circle above the x-axis that touches the x-axis at the point P(k, 0); its horizontal diameter runs from A to B(13, 5)',
    circles=[dict(x=8, y=5, r=5)], segs=[dict(x1=3, y1=5, x2=13, y2=5, cls='ln')],
    points=[dict(x=3, y=5, label='A', dx=-17, dy=5), dict(x=13, y=5, label='B(13, 5)', dx=8, dy=5), dict(x=8, y=0, label='P(k, 0)', dx=-24, dy=19)])

# --- Step 6: a semicircle with its highest point marked (center (6, 0), radius 10)
FIGS['s6'] = G(-7, 19, -2.5, 13.5, u=11,
    alt='a semicircle above the x-axis with its highest point at P(6, 10); Q is the left end of its diameter on the x-axis',
    circles=[dict(x=6, y=0, r=10, half=True)],
    points=[dict(x=6, y=10, label='P(6, 10)', dx=8, dy=-7), dict(x=-4, y=0, label='Q', dx=-6, dy=19)])

# --- Practice 6: a circle on a grid with its center and one point marked
FIGS['p6'] = G(-4.5, 9, -5.5, 7.5, u=20, grid=dict(step=1, label=2),
    alt='a circle on a grid with center (2, 1) that passes through the point (6, 4)',
    circles=[dict(x=2, y=1, r=5)],
    points=[dict(x=2, y=1, label='(2, 1)', dx=8, dy=-6), dict(x=6, y=4, label='(6, 4)', dx=8, dy=-6)])

# --- Practice 8: the tangent picture again (center (10, 7), radius 7)
FIGS['p8'] = G(-2, 24, -2.5, 16, u=12,
    alt='a circle above the x-axis that touches the x-axis at the point P(k, 0); its horizontal diameter runs from A to B(17, 7)',
    circles=[dict(x=10, y=7, r=7)], segs=[dict(x1=3, y1=7, x2=17, y2=7, cls='ln')],
    points=[dict(x=3, y=7, label='A', dx=-17, dy=5), dict(x=17, y=7, label='B(17, 7)', dx=8, dy=5), dict(x=10, y=0, label='P(k, 0)', dx=-24, dy=19)])

# --- Practice 9: a semicircle with its two endpoints labelled (center (4, 0), radius 10)
FIGS['p9'] = G(-10, 18, -3, 13, u=11,
    alt='a semicircle above the x-axis that meets the x-axis at (-6, 0) and (14, 0)',
    circles=[dict(x=4, y=0, r=10, half=True)],
    points=[dict(x=-6, y=0, label='(' + MINUS + '6, 0)', dx=-34, dy=19), dict(x=14, y=0, label='(14, 0)', dx=-12, dy=19)])

# --- Challenge 6: a semicircle with its highest point marked (center (1, 0), radius 13)
FIGS['c6'] = G(-15, 17, -3, 16, u=9,
    alt='a semicircle above the x-axis with its highest point at P(1, 13)',
    circles=[dict(x=1, y=0, r=13, half=True)],
    points=[dict(x=1, y=13, label='P(1, 13)', dx=9, dy=-7)])

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
function fig(name) {
    var f = FIGS[name];
    if (!f) return '';
    if (f.panels) return '<div class="fig-row panels" role="group" aria-label="' + (f.alt || 'graphs') + '">' + f.panels.map(function(p) { return '<div class="panel"><div class="plab">' + p.t + '</div>' + fig(p.fig) + '</div>'; }).join('') + '</div>';
    return f.box ? geoSVG(f) : graphSVG(f);
}'''

FIGS_JS = 'var FIGS = {\n' + ',\n'.join('    ' + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in FIGS.items()) + '\n};' + GEO_JS

# figure classes on top of the shell's figure styles; the fig-row rules match sheets 3, 4 and 4B
FIG_RULES = [
    ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }",
    ".fig text.g { font-size: 15px; }",
    ".fig .thin { stroke: #21442B; stroke-width: 1.3; fill: none; }",
    ".fig .arc { stroke: #BC6C26; stroke-width: 1.4; fill: none; }",
    ".fig .tick { stroke: #21442B; stroke-width: 1.5; }",
    ".fig .circ { fill: none; stroke: #21442B; stroke-width: 2; }",
    ".fig .shade2 { fill: rgba(57,134,78,0.16); stroke: none; }",
    ".fig .tile { fill: rgba(221,162,94,0.12); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .tileR { fill: rgba(192,57,43,0.24); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .tileB { fill: rgba(52,101,164,0.20); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .fillg { fill: #21442B; stroke: none; }",
    ".fig .grid { stroke: rgba(45,45,45,0.13); stroke-width: 1; }",
    ".fig text.sm { font-family: 'Inter', sans-serif; font-size: 11px; font-style: normal; fill: #5A5A5A; }",
    ".fig text.lbl { font-family: 'Inter', sans-serif; font-size: 12.5px; font-style: normal; fill: #2D2D2D; }",
    ".fig text.note { font-family: 'Inter', sans-serif; font-size: 11.5px; font-style: normal; fill: #5A5A5A; }",
]
PANEL_RULES = [
    ".fig-row { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: flex-start; justify-content: center; margin: 4px 0 10px; }",
    ".fig-row .fig { margin: 4px 0; }",
    ".panel { text-align: center; }",
    ".panel .plab { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 700; color: #21442B; }",
]
FIG_CSS = '\n'.join(FIG_RULES + PANEL_RULES) + r'''
.ref-page .fig-row { margin-left: 24px; }
@media (max-width: 768px) { .ref-page .fig-row { margin-left: 0; } }
.figcap { text-align: center; }
.figcap .cap { font-family: 'Inter', sans-serif; font-size: 12.5px; color: #5A5A5A; margin: -2px 0 8px; }'''
# the same figure styles, on one line, for the downloaded results report (which has its own style block)
REPORT_FIG_CSS = (".fig{display:block;margin:4px 0 10px;max-width:100%;height:auto}.fig .ax{stroke:#2D2D2D;stroke-width:1.4}.fig .ln{stroke:#21442B;stroke-width:2;fill:none}"
                  ".fig .dash{stroke:#8B6914;stroke-width:1.4;stroke-dasharray:5 4;fill:none}.fig .pt{fill:#21442B}.fig .shade{fill:rgba(221,162,94,0.25);stroke:none}"
                  ".fig text{font-family:\"Times New Roman\",Georgia,serif;font-size:13px;fill:#2D2D2D}.fig text.it{font-style:italic}" +
                  ''.join(re.sub(r'\s*([{};:,])\s*', r'\1', r).replace(';}', '}') for r in FIG_RULES + PANEL_RULES))


# The shell draws lines, dashed segments, points, polygons. This sheet adds: general
# function curves (with gaps), polylines, horizontal and vertical dashed lines, thick
# domain/range highlights on the axes, and an optional labeled grid.
CURVES_JS = r'''    (o.curves || []).forEach(function(c) {
        // y = a x^2 + b x + c, or y = inv / x, or any function c.f, sampled across [from, to] and split at gaps
        var fn = c.f || (c.inv != null ? function(x) { return c.inv / x; } : function(x) { return c.a * x * x + c.b * x + c.c; });
        var x0 = (c.from != null ? c.from : xmin), x1 = (c.to != null ? c.to : xmax);
        var n = 240, run = [], runs = [], band = 2 * (ymax - ymin);
        for (var i = 0; i <= n; i++) {
            var x = x0 + (x1 - x0) * i / n, y = fn(x);
            if (!isFinite(y) || y < ymin - band || y > ymax + band) { if (run.length) { runs.push(run); run = []; } continue; }
            run.push(X(x).toFixed(1) + ',' + Y(y).toFixed(1));
        }
        if (run.length) runs.push(run);
        runs.forEach(function(r) { if (r.length > 1) s += '<polyline class="' + (c.cls || 'ln') + '" clip-path="url(#clip' + id + ')" points="' + r.join(' ') + '"/>'; });
        if (c.label) s += '<text class="it" x="' + (X(c.lx) + (c.dx || 0)) + '" y="' + (Y(c.ly) + (c.dy || 0)) + '">' + c.label + '</text>';
    });
    (o.polylines || []).forEach(function(c) {
        s += '<polyline class="' + (c.cls || 'ln') + '" points="' + c.pts.map(function(p) { return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }).join(' ') + '"/>';
        if (c.label) s += '<text class="it" x="' + (X(c.lx) + (c.dx || 0)) + '" y="' + (Y(c.ly) + (c.dy || 0)) + '">' + c.label + '</text>';
    });
    (o.hlines || []).forEach(function(l) {
        s += '<line class="' + (l.cls || 'dash') + '" x1="' + X(xmin) + '" y1="' + Y(l.y) + '" x2="' + X(xmax) + '" y2="' + Y(l.y) + '"/>';
        if (l.label) s += '<text class="it" x="' + (X(l.lx != null ? l.lx : xmin) + (l.dx || 0)) + '" y="' + (Y(l.y) + (l.dy || -5)) + '">' + l.label + '</text>';
    });
    (o.vlines || []).forEach(function(l) {
        s += '<line class="' + (l.cls || 'dash') + '" x1="' + X(l.x) + '" y1="' + Y(ymin) + '" x2="' + X(l.x) + '" y2="' + Y(ymax) + '"/>';
        if (l.label) s += '<text class="it" x="' + (X(l.x) + (l.dx || 5)) + '" y="' + (Y(l.ly != null ? l.ly : ymax) + (l.dy || 12)) + '">' + l.label + '</text>';
    });
    (o.thick || []).forEach(function(t) {
        s += '<line class="dom" x1="' + X(t.x1) + '" y1="' + Y(t.y1) + '" x2="' + X(t.x2) + '" y2="' + Y(t.y2) + '"/>';
    });
'''

GRID_JS = r'''    if (o.grid) {
        var gs = o.grid.step || 1, gl = o.grid.label || 0, k;
        for (k = Math.ceil(xmin / gs); k * gs <= xmax + 1e-9; k++) s += '<line class="grid" x1="' + X(k * gs) + '" y1="' + Y(ymin) + '" x2="' + X(k * gs) + '" y2="' + Y(ymax) + '"/>';
        for (k = Math.ceil(ymin / gs); k * gs <= ymax + 1e-9; k++) s += '<line class="grid" x1="' + X(xmin) + '" y1="' + Y(k * gs) + '" x2="' + X(xmax) + '" y2="' + Y(k * gs) + '"/>';
        if (gl && ymin <= 0 && ymax >= 0) for (k = Math.ceil(xmin / gl); k * gl <= xmax - 0.5; k++) if (k !== 0) s += '<text class="sm" text-anchor="middle" x="' + X(k * gl) + '" y="' + (Y(0) + 14) + '">' + (k * gl < 0 ? '−' + (-k * gl) : k * gl) + '</text>';
        if (gl && xmin <= 0 && xmax >= 0) for (k = Math.ceil(ymin / gl); k * gl <= ymax - 0.5; k++) if (k !== 0) s += '<text class="sm" text-anchor="end" x="' + (X(0) - 5) + '" y="' + (Y(k * gl) + 4) + '">' + (k * gl < 0 ? '−' + (-k * gl) : k * gl) + '</text>';
    }
'''

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




# Circles on the coordinate graph: {x, y, r} is a full circle; half: true draws only the upper semicircle.
# The radius is scaled with the x-axis, so a figure needs equal x and y scales (see G above).
CIRCLES_JS = r'''    (o.circles || []).forEach(function(c) {
        var rr = (c.r * (X(1) - X(0))).toFixed(1);
        if (c.half) s += '<path class="' + (c.cls || 'circ') + '" d="M' + X(c.x - c.r).toFixed(1) + ',' + Y(c.y).toFixed(1) + ' A' + rr + ',' + rr + ' 0 0 1 ' + X(c.x + c.r).toFixed(1) + ',' + Y(c.y).toFixed(1) + '"/>';
        else s += '<circle class="' + (c.cls || 'circ') + '" cx="' + X(c.x).toFixed(1) + '" cy="' + Y(c.y).toFixed(1) + '" r="' + rr + '"/>';
    });
'''


def build(out=OUT):
    html = open(SRC, encoding='utf-8').read()
    html = re.sub(r'\s*<p style="font-size:14px; margin-top:10px;">Ready for the next topic\?.*?</p>', '', html, flags=re.S)

    # --- header / titles / footer
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Circle Equations</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Circle Equations</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; CIRCLE EQUATIONS')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Circle Equations')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Circle Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Circle equation rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>a circle is every point at one fixed distance from its center.</strong> Standard form states that distance with the Pythagorean theorem, so the center and the radius can be read from it. Each question asks you to get the equation into that form, read what it shows, and answer what was asked.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. You can enter fractions as 25/4 or 6.25; both are accepted. Negative coordinates need the minus sign. Sections A to D use the starred rules, and section E covers the unstarred ones. Once you feel comfortable, try responding without pausing for long.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and three include a figure. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type: is the equation already in standard form, does it need completing the square, or do you have to build it from a center and a point? Then check what the question asks for: the center, the radius, the diameter, the area or the circumference. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. Desmos can graph a circle from either form of its equation, so typing an equation as it is written is a good way to check the center and radius you found. When the equation is already in standard form, reading it directly is usually quicker.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These seven questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each one adds a second idea to a rule you already have (a constant to find from the radius, a point with one coordinate missing, points inside and outside a circle, a diameter that leads to an area, a tangent circle written in expanded form, a point at a given height on a semicircle, a line that crosses a circle). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the ones marked <em>extra</em> lean on the unstarred rules. One is tagged <em>systems blend</em>: it pairs a circle with substitution and factoring from SAT Math 1 and SAT Math 2, and that pairing appears less often, so treat it as stretch practice.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card (no Khan Academy line: removed across the series on 2026-11-23)
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time a circle equation shows up. Make it an if-then. (Shape: “When a circle equation is not in standard form, I ______ before I read the radius.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">Completing the square comes from <a href="' + QUAD_URL + '" ' + A_STYLE + '>SAT Math 2: Quadratics &#8594;</a>, and the distance from the center to a point comes from the Pythagorean theorem in <a href="' + TRI_URL + '" ' + A_STYLE + '>SAT Math 4: Triangles &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">The previous sheet in the series is <a href="' + EXP_URL + '" ' + A_STYLE + '>SAT Math 7: Exponents and Exponential Models &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>',
        flags=re.S)

    # --- data arrays
    for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
        html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

    # --- figures: FIGS, the geometry renderer and fig(); the shell's graphSVG gains circles, curves, a grid and a clip path
    start = html.index('var FIGS = {')
    tail = "function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }"
    end = html.index(tail) + len(tail)
    html = html[:start] + FIGS_JS + html[end:]
    html = replace_once(html,
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';""",
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker>' +
        '<clipPath id="clip' + id + '"><rect x="' + X(xmin) + '" y="' + Y(ymax) + '" width="' + (X(xmax) - X(xmin)) + '" height="' + (Y(ymin) - Y(ymax)) + '"/></clipPath></defs>';""")
    html = replace_once(html, """s += '<text class="it" x="' + (X(0) - 12) + '" y="' + (Y(0) + 14) + '">O</text>';""",
                        """s += '<text class="it" x="' + (X(0) + (o.ox == null ? -12 : o.ox)) + '" y="' + (Y(0) + (o.oy == null ? 14 : o.oy)) + '">O</text>';""")   # ox, oy: move the O when a curve runs through its usual spot
    html = replace_once(html, "    if (o.poly) {\n", GRID_JS + "    if (o.poly) {\n")
    html = replace_once(html, "    (o.lines || []).forEach(function(l) {\n", CURVES_JS + CIRCLES_JS + "    (o.lines || []).forEach(function(l) {\n")
    html = replace_once(html, ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }", FIG_CSS)

    # --- Skill Practice items can carry a figure; it sits between the question and the answer row
    html = replace_once(html, """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>';""",
                        """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>' + (it.fig ? fig(it.fig) : '');""")

    # --- results kit: carry each question's figure into the tutor report (practice, challenge and any Skill Practice rep that has one)
    html = replace_n(html, "stem: p.stem, trap: p.trap });", "stem: p.stem, fig: p.fig ? fig(p.fig) : '', trap: p.trap });", 2)
    html = replace_once(html, """'</b></span></div><div class="stem">' + r.i.stem + '</div>""", """'</b></span></div><div class="stem">' + (r.i.fig || '') + r.i.stem + '</div>""")
    html = replace_once(html, ": it.accept[0], q: it.q }); }", ": it.accept[0], q: it.q + (it.fig ? fig(it.fig) : '') }); }")
    html = replace_once(html, "'.nw{white-space:nowrap}table.vtab{", "'" + REPORT_FIG_CSS.replace('\\', '\\\\').replace("'", "\\'") + "' +\n        '.nw{white-space:nowrap}table.vtab{")

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', 'sat-circle-equations-sheet:rule')
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
