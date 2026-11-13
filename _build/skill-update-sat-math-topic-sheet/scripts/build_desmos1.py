#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Desmos-1-Core-Moves.html. Content only; desmos_common.build() does the assembly.
Every Desmos behavior described here was checked in the College Board version of the
Desmos graphing calculator (desmos.com/testing/collegeboard/graphing) on 2026-11-11."""
import os
from desmos_common import build, dz, kbd, table, window, slider, SITE, SAT_DIR

LINEAR_URL = SITE + 'test-prep/sat/SAT-Math-1-Linear-Equations.html'
QUAD_URL = SITE + 'test-prep/sat/SAT-Math-2-Quadratics.html'
CB_DESMOS = 'https://www.desmos.com/testing/collegeboard/graphing'
A_STYLE = 'target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;"'

STAR = '<span class="star">&#9733;</span>'


def move(n, name, ess, body):
    tag = (STAR if ess else '') + 'Move ' + str(n)
    return ('<div class="ref-rule' + (' ess' if ess else '') + '"><div class="ref-rule-line"><span class="rtag">' + tag +
            '</span><span class="rname">' + name + '</span></div>\n' + body.strip('\n') + '\n</div>\n')


def frow(label, math):
    return '<div class="frow"><div class="flabel">' + label + '</div><div class="fmath">' + math + '</div></div>\n'


def ex(letter, text):
    return '<div class="ref-ex"><span class="exlab">Example ' + letter + '</span>' + text + '</div>\n'


def note(text):
    return '<div class="ref-note">' + text + '</div>\n'


def trap(n, name, text):
    return ('<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Common mistake ' + str(n) + '</span><span class="rname">' +
            name + '</span></div><div class="ref-ex">' + text + '</div></div>\n')


# ---------------------------------------------------------------- TAB 1: MOVES
RULES = r'''
<p class="ref-intro">Desmos is available throughout the SAT Math section in Bluebook. The goal is to recognize when a graph can help, enter the equation accurately, and understand what the result tells you. This guide introduces nine useful skills with examples and the exact entries to practice. The examples were checked in the College Board version of Desmos. As you practice, start by identifying the question type. Then decide whether Desmos or algebra makes more sense, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the Desmos skills you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred skills.</span></div>
''' + move(1, 'Type it the way the test prints it', True, r'''
<p class="ref-lead">Desmos can graph equations in many forms, so you often do not need to rearrange first. Standard form, a circle, an equation with $x$ on both sides: type it as printed. A few entry habits help Desmos read what you meant.</p>
<div class="tbl-wrap"><table class="forms"><thead><tr><th>You want</th><th>Type</th><th>What to watch</th></tr></thead><tbody>
<tr><td class="fname">a fraction, &nbsp;$\dfrac{3}{4}x - 2$</td><td class="fmath">''' + kbd('3', '/', '4', '&rarr;', 'x', '&minus;', '2') + r'''</td><td class="freads">everything you type after the slash lands in the denominator until you press the right arrow</td></tr>
<tr><td class="fname">a power, &nbsp;$x^2 - 4$</td><td class="fmath">''' + kbd('x', '^', '2', '&minus;', '4') + r'''</td><td class="freads">a plus or minus sign closes the exponent by itself; for $2^{x+1}$ type ''' + kbd('2^(x+1)') + r'''</td></tr>
<tr><td class="fname">a root, &nbsp;$\sqrt{x + 9}$</td><td class="fmath">''' + kbd('sqrt', 'x+9', '&rarr;') + r'''</td><td class="freads">the right arrow steps back out of the root</td></tr>
<tr><td class="fname">an absolute value, &nbsp;$|x - 5|$</td><td class="fmath">''' + kbd('abs(', 'x&minus;5') + r'''</td><td class="freads">or use the $|a|$ key on the Desmos keypad</td></tr>
<tr><td class="fname">$\leq$ &nbsp;or&nbsp; $\geq$</td><td class="fmath">''' + kbd('&lt;=') + ' &nbsp;or&nbsp; ' + kbd('&gt;=') + r'''</td><td class="freads">Desmos joins the two characters into one symbol</td></tr>
<tr><td class="fname">$\pi$</td><td class="fmath">''' + kbd('pi') + r'''</td><td class="freads">more precise than typing $3.14$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('letters', r'Desmos graphs equations in $x$ and $y$. Retype any other pair of letters as $x$ and $y$') +
    frow('window', r'nothing on screen? zoom out with the minus button, or open the wrench and set the $x$ and $y$ ranges') +
    frow('fractions', r'a decimal result has a small round button on its left that turns it into a fraction') + r'''</div>
''' + ex('A', r'$2x + 5y = 9$ can be typed as printed. So can a circle such as $(x - 1)^2 + (y - 5)^2 = 16$. You do not need to solve for $y$ first.') +
    ex('B', r'The test writes $3a - 2b = 12$ and $a + b = 9$. Type $3x - 2y = 12$ and $x + y = 9$. The lines cross at $(6, 3)$, so $a = 6$ and $b = 3$.') +
    ex('C', r'Typing ' + kbd('y=3/4x&minus;2') + r' with no right arrow graphs $y = \dfrac{3}{4x - 2}$, a curve where you expected a line. When a picture surprises you, reread the line you typed before you reread the question.') +
    note(r'If the graph looks unexpected, check your entry and graph window before changing your approach.')) + \
move(2, 'Read the gray dots', True, r'''
<p class="ref-lead">Click a curve and Desmos marks points that SAT questions often ask about: where the curve crosses each axis, and where it reaches a high or low point. Click a dot to see its coordinates. Zeros, roots, $x$-intercepts and the solutions of $f(x) = 0$ are four names for the same dots.</p>
''' + dz([{'x': r'y = x^2 - 2x - 8', 'see': 'click the curve: dots at (&minus;2, 0) and (4, 0) on the x-axis, (0, &minus;8) on the y-axis, and the vertex (1, &minus;9)'}]) + r'''
<div class="fig-slot" data-fig="dots"></div>
<div class="fbox">
''' + frow('zeros, roots', r'the dots on the $x$-axis') +
    frow('$y$-intercept', r'the dot on the $y$-axis') +
    frow('max or min', r'the dot at the vertex: its $x$ says where, its $y$ is the value') +
    frow('a circle', r'dots at the top and the bottom: the center is halfway between them, and the radius is half the distance') + r'''</div>
''' + ex('A', r'$y = 2x^2 - 9$: the right-hand dot reads $(2.121, 0)$. Algebra agrees: $x = \sqrt{4.5} \approx 2.121$.') +
    ex('B', r'$h(x) = -2(x - 1)(x - 7)$: the vertex dot reads $(4, 18)$. The maximum value is $18$, and it happens at $x = 4$. Reread the question to see which of the two it wants.') +
    ex('C', r'$(x - 3)^2 + (y + 2)^2 = 25$: the top dot is $(3, 3)$ and the bottom dot is $(3, -7)$. Halfway between is the center, $(3, -2)$, and half the distance is the radius, $5$.') + r'''
<div class="fig-slot" data-fig="circle"></div>
''' + note(r'Desmos rounds what it shows. When a dot reads $2.121$, the exact answer may be $\sqrt{4.5}$ or $\tfrac{3\sqrt{2}}{2}$. Match it to the choices by typing each choice and comparing decimals.')) + \
move(3, 'Intersections solve systems, and many single equations', True, r'''
<p class="ref-lead">The solution of a system is the point where its graphs cross. The same idea works for a single equation: graph the left side and the right side as two curves, and the $x$-coordinates of the crossings are the solutions.</p>
''' + dz([{'x': r'3x + 2y = 16'}, {'x': r'y = x - 2', 'see': 'click the crossing: (4, 2)'}]) + r'''
<div class="fig-slot" data-fig="cross"></div>
<div class="fbox">
''' + frow('a system', r'one equation per line, then click the crossing') +
    frow('a single equation', r'$y =$ left side on one line, $y =$ right side on the next; read the $x$ of each crossing') +
    frow('one variable', r'or type the equation itself, such as $3(x - 2) + 5 = 2x + 7$: a vertical line appears at each solution') +
    frow('finish the question', r'it may want $x$, $y$, $x + y$, or the sum of the solutions') + r'''</div>
''' + ex('A', r'$|2x - 3| = 11$: graph $y = |2x - 3|$ and $y = 11$. They cross at $x = -4$ and $x = 7$, so the sum of the solutions is $3$.') +
    ex('B', r'$3(x - 2) + 5 = 2x + 7$, typed as printed, draws a vertical line at $x = 8$.') +
    ex('C', r'$\sqrt{x + 9} = x - 3$: the two graphs cross once, at $x = 7$. Squaring both sides by hand also produces $x = 0$, which does not satisfy the original equation. The graphs do not cross there, so the picture shows only $x = 7$.') +
    note(r'This is one of the most useful Desmos skills for the SAT. In many cases, two equations and an intersection give you the information you need.')) + \
move(4, 'Count the solutions', True, r'''
<p class="ref-lead">Some questions ask how many solutions there are rather than what the solutions are. A graph can help you see the number of intersections, as long as you interpret it carefully.</p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>What you see</th><th>Solutions</th><th>Why</th></tr></thead><tbody>
<tr><td class="fname">two lines that cross</td><td class="">exactly one</td><td class="">different slopes</td></tr>
<tr><td class="fname">two parallel lines</td><td class="">none</td><td class="">same slope, different intercepts</td></tr>
<tr><td class="fname">one line, though you typed two</td><td class="">infinitely many</td><td class="">both equations describe the same line</td></tr>
<tr><td class="fname">a line and a parabola</td><td class="">none, one, or two</td><td class="">count the crossings; a line that just touches counts once</td></tr>
</tbody></table></div>
<div class="fig-row"><div class="fig-slot" data-fig="c_one"></div><div class="fig-slot" data-fig="c_none"></div><div class="fig-slot" data-fig="c_same"></div></div>
''' + ex('A', r'$4x - 6y = 8$ and $2x - 3y = 4$: only one line appears, because the first equation is the second one doubled. Infinitely many solutions.') +
    ex('B', r'$x - 2y = 3$ and $3x - 6y = 4$: two parallel lines. No solution.') +
    ex('C', r'$y = x^2 - 4x + 7$ and $y = 2x - 2$: the line touches the parabola at $(3, 4)$ and nowhere else. Exactly one solution.') + r'''
<div class="fig-slot" data-fig="tangent"></div>
''' + note(r'Zoom out before you decide that two lines never meet. Lines with close slopes can look parallel in the default window and still cross off screen.')) + \
move(5, 'Slide an unknown constant', True, r'''
<p class="ref-lead">When an equation contains a constant such as $k$ or $c$, Desmos offers a slider for it. Drag the slider and watch the graph until it does what the question describes.</p>
''' + dz([{'x': r'2x - 5y = 7'}, {'x': r'6x + ky = 4', 'see': 'click <em>add slider: k</em>'}, {'x': r'k = -15', 'see': 'drag until the two lines are parallel'}]) + r'''
<div class="fig-slot" data-fig="slider"></div>
<div class="fbox">
''' + frow('no solution', r'slide until the lines are parallel') +
    frow('infinitely many', r'slide until one line sits on top of the other') +
    frow('exactly one', r'with a parabola: slide until the curve just touches') +
    frow('set the slider', r'it starts with a range of $-10$ to $10$. Click the numbers at its ends to widen the range, and set the step to $1$ to land on whole numbers') + r'''</div>
''' + ex('A', r'$y = x^2 + 6x + c$ touches the $x$-axis exactly once when $c = 9$.') +
    ex('B', r'$3x + 4y = 10$ and $kx + 12y = 30$ become the same line at $k = 9$: infinitely many solutions.') +
    ex('C', r'Confirm the system above with algebra: the slopes are $\tfrac{2}{5}$ and $-\tfrac{6}{k}$, and they match when $k = -15$.') +
    note(r'A slider finds whole-number answers quickly. When the answer could be a fraction, use the slider to see roughly where it is, then finish with algebra: equal slopes, or a discriminant of zero.')) + \
move(6, 'Name the function, then reuse it and test the choices', True, r'''
<p class="ref-lead">Type a function once with a name, and Desmos lets you reuse it on later lines: evaluate it, shift it, or compare it with every answer choice.</p>
''' + dz([{'x': r'f(x) = x^2 - 6x + 5'}, {'x': r'f(3)', 'val': '-4'}, {'x': r'y = f(x) + 4', 'see': 'the same parabola moved up 4: its vertex now sits on the x-axis'}]) + r'''
<div class="fbox">
''' + frow('evaluate', r'$f(3)$ on its own line') +
    frow('shift', r'$y = f(x) + 4$ &nbsp;or&nbsp; $y = f(x - 2)$') +
    frow('equivalent', r'graph the original and each choice: an equivalent expression has the same graph as the original') +
    frow('which equation', r'graph all four choices and keep the one with the right intercepts') + r'''</div>
''' + ex('A', r'Which expression is equivalent to $(2x + 3)(x - 4)$? Graph $y = (2x + 3)(x - 4)$, then $y = 2x^2 - 5x - 12$. The second curve sits on top of the first, so the two expressions match.') +
    ex('B', r'A line has $x$-intercept $2$ and $y$-intercept $8$. Of $2x + 8y = 16$ and $4x + y = 8$, only the second passes through both $(2, 0)$ and $(0, 8)$. The first has the intercepts swapped.') +
    ex('C', r'To see many values at once, press the plus button, add a table, and type $f(x)$ as the heading of the second column.') +
    note(r'Two curves that match look like one. Click the colored circle beside a line to hide and show that curve, so you can be sure both are there.')) + \
move(7, 'Shade the inequalities', False, r'''
<p class="ref-lead">Type an inequality and Desmos shades every point that satisfies it. With two inequalities, the solutions are the points shaded twice.</p>
''' + dz([{'x': r'y \leq 2x + 1'}, {'x': r'y > -x + 4', 'see': 'the solutions are where the two shadings overlap'}]) + r'''
<div class="fig-slot" data-fig="shade"></div>
<div class="fbox">
''' + frow('solid edge', r'$\leq$ or $\geq$: points on the line are solutions') +
    frow('dashed edge', r'$<$ or $>$: points on the line are not solutions') +
    frow('test a point', r'type the point, such as $(3, 5)$, and see whether it lands in the overlap') + r'''</div>
''' + ex('A', r'$(3, 5)$ lands in the overlap, and the arithmetic agrees: $5 \leq 7$ and $5 > 1$. A solution.') +
    ex('B', r'$(3, 1)$ sits on the dashed line $y = -x + 4$. Not a solution.') +
    ex('C', r'For a point $(3, b)$, the overlap runs from just above $b = 1$ up to and including $b = 7$.') +
    note(r'Pay attention to dashed boundaries, especially on greatest- or least-integer questions. A dashed boundary is not included in the solution set.')) + \
move(8, 'Let lists do the statistics', False, r'''
<p class="ref-lead">Desmos has the statistics functions built in. Type the numbers in any order: it sorts and counts for you.</p>
''' + dz([{'x': r'\operatorname{mean}(4, 9, 9, 13, 20, 23)', 'val': '13'}, {'x': r'\operatorname{median}(4, 9, 9, 13, 20, 23)', 'val': '11'}, {'x': r'15\%\ \operatorname{of}\ 80', 'val': '12'}]) + r'''
<div class="fbox">
''' + frow('mean', kbd('mean(') + r' then the values, separated by commas') +
    frow('median', kbd('median(') + r': no sorting, and it averages the middle two when the count is even') +
    frow('percent', r'type ' + kbd('15%') + r' and Desmos writes the word “of” for you') +
    frow('also there', r'min, max, total, count, and stdev (standard deviation)') + r'''</div>
''' + ex('A', r'One large value pulls the mean and leaves the median alone: $\text{mean}(2, 3, 3, 8, 34) = 10$, while $\text{median}(2, 3, 3, 8, 34) = 3$.') +
    ex('B', r'$18\%$ of $250$: type ' + kbd('18%', '250') + r' and read $45$.') +
    note(r'A frequency table needs one more idea, weighting each value by its count. That is covered in SAT Desmos 2: Next Steps.')) + \
move(9, 'A table and a tilde: the line of best fit', False, r'''
<p class="ref-lead">Given data points, Desmos can fit a line to them. Put the points in a table, then type the model with a tilde ($\sim$) where the equals sign would go. The tilde means “find the constants that fit best.”</p>
''' + dz([{'x': r'\text{table: }\ x_1 = 1, 3, 6, 8 \quad y_1 = 4, 9, 14, 19', 'see': 'the plus button, then <em>table</em>'},
          {'x': r'y_1 \sim m x_1 + b', 'out': ['m = 2.06897', 'b = 2.18966'], 'stat': 'R^2 = 0.9931'}]) + r'''
<div class="fig-slot" data-fig="fit"></div>
<div class="fbox">
''' + frow('the tilde', r'Shift plus the key to the left of $1$ on most keyboards') +
    frow('subscripts', r'typing ' + kbd('x1') + r' makes $x_1$ by itself') +
    frow('read it', r'$m$ is the slope and $b$ is the $y$-intercept') + r'''</div>
''' + ex('A', r'Desmos reports $m \approx 2.07$ and $b \approx 2.19$, so the line of best fit is about $y = 2.1x + 2.2$.') +
    ex('B', r'A choice with the two numbers swapped, such as $y = 2.2x + 2.1$, is a common wrong answer. The slope is the number multiplying $x$.') +
    ex('C', r'To predict, type $m \cdot 10 + b$ on a new line: Desmos uses the fitted values and shows about $22.9$.') +
    note(r'The tilde is useful for more than best-fit lines. It can also find unknown constants in many equations, which is where SAT Desmos 2: Next Steps begins.')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common entry and interpretation mistakes. Review them so you know what to check when an answer seems off. Practice spotting these now so they are easier to catch on test day.</p>
''' + trap(1, r'leaving the test’s letters in', r'Type $3a - 2b = 12$ and Desmos offers sliders for $a$ and $b$ where you wanted a graph. Retype the system with $x$ and $y$.') + \
      trap(2, r'forgetting the right arrow after a fraction', kbd('y=3/4x&minus;2') + r' graphs $y = \dfrac{3}{4x - 2}$. Press the right arrow to leave the denominator, and read your line back before you rely on the graph.') + \
      trap(3, r'answering $x$ when the question asks for something else', r'The crossing is $(4, 2)$ and the question wants $y$, or $x + y$, or the sum of two solutions. Finding the point is only one step. Check what the question asks you to do with it.') + \
      trap(4, r'calling it “no solution” from a zoomed-in window', r'Two lines with close slopes can look parallel near the origin. Zoom out, or compare the slopes, before you choose “zero.”') + \
      trap(5, r'picking a point on a dashed edge', r'With $<$ or $>$, the boundary line is dashed and its points are not solutions. If $b < 6$, the greatest integer is $5$, not $6$.') + \
      trap(6, r'rounding a decimal the answer box will not take', r'When Desmos shows a rounded decimal such as $0.6667$, enter $2/3$ or $.6667$ rather than $.67$. The Bluebook Tools tab on this sheet has practice with the entry rules.') + \
      trap(7, r'graphing what a glance would answer', r'The $y$-intercept of $y = 3x^2 - 12x + 7$ is $7$: read the constant directly. Use Desmos when it helps; for simpler questions, algebra may be quicker.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Move 1: Type it as printed",
  "rule": r"type the equation the way it is written &nbsp;·&nbsp; $x$ and $y$ are the only letters Desmos graphs",
  "say": r"Desmos accepts standard form, so you do not need to solve a system for $y$ before you graph it. What it does need is the right letters. If the test uses $a$ and $b$, or $p$ and $q$, retype the same equations with $x$ and $y$. The crossing point is the same; only the names change.",
  "prob": r"$$3a - 2b = 12$$ $$a + b = 9$$ The solution to the system of equations above is $(a, b)$. What is the value of $a$?",
  "sol": r"<strong>Step 1: retype with $x$ and $y$.</strong>" + dz([{'x': r'3x - 2y = 12'}, {'x': r'x + y = 9', 'see': 'click the crossing: (6, 3)'}]) +
         r"<strong>Step 2: translate back.</strong> $x$ stood for $a$, so $a = 6$ (and $b = 3$).<br><strong>Check:</strong> $3(6) - 2(3) = 12$ and $6 + 3 = 9$. ✓",
  "trap": r"Typing the system with $a$ and $b$. Desmos does not treat those letters as the variables, so it offers a slider for each one and does not draw the lines you need. Change the two letters to $x$ and $y$, then click the crossing.",
  "desmos": ["3x-2y=12", "x+y=9"],
  "micro": {"q": r"$$2a + b = 13$$ $$a - b = 2$$ Retype the system with $x$ and $y$ and graph it. The value of $a$ is", "accept": ["5"],
            "exp": r"Type $2x + y = 13$ and $x - y = 2$. The lines cross at $(5, 3)$, so $a = 5$."}},
 {"ess": True, "name": "Move 2: Read the gray dots",
  "rule": r"zeros are the dots on the $x$-axis &nbsp;·&nbsp; the max or min is the dot at the vertex",
  "say": r"A maximum or minimum question is a vertex question, and Desmos marks the vertex for you. Graph the function, click the curve, click the dot at the top. Its $x$-coordinate is <em>where</em> the maximum happens and its $y$-coordinate is the maximum <em>value</em>. A question may ask for either one, so read its last line again before you answer.",
  "fig": "hmax",
  "prob": r"$$h(x) = -2(x - 1)(x - 7)$$ The function $h$ is defined above. For what value of $x$ does $h(x)$ reach its maximum, and what is that maximum value?",
  "sol": r"<strong>Step 1: graph it.</strong>" + dz([{'x': r'h(x) = -2(x - 1)(x - 7)', 'see': 'zoom out until the top is visible, then click the vertex: (4, 18)'}]) +
         r"<strong>Step 2: read both coordinates.</strong> The maximum happens at $x = 4$, and the maximum value is $18$.<br><strong>Check:</strong> the zeros are $1$ and $7$, the vertex sits halfway between at $x = 4$, and $h(4) = -2(3)(-3) = 18$. ✓",
  "trap": r"Answering $18$ when the question asks “for what value of $x$,” or $4$ when it asks for the maximum. Both numbers come from the same dot, and both may appear among the choices.",
  "desmos": ["h(x)=-2(x-1)(x-7)", window(-3, 11, -8, 22)],
  "micro": {"q": r"Graph $y = x^2 + 4x - 1$ and click its lowest point. The $y$-coordinate of that point is", "accept": ["-5"],
            "exp": r"The vertex dot reads $(-2, -5)$. The lowest value of $y$ is $-5$, reached at $x = -2$."}},
 {"ess": True, "name": "Move 3: Intersections",
  "rule": r"a system: click the crossing &nbsp;·&nbsp; a single equation: graph each side and read the $x$ of each crossing",
  "say": r"An absolute value equation often has two solutions, and by hand you find them by splitting into two cases. On a graph the two cases are the two arms of the V. Put the left side on one line and the right side on the next, and each solution shows up as a crossing.",
  "prob": r"What is the sum of the solutions to the equation $|2x - 3| = 11$?",
  "sol": r"<strong>Step 1: graph each side.</strong>" + dz([{'x': r'y = |2x - 3|'}, {'x': r'y = 11', 'see': 'two crossings: (&minus;4, 11) and (7, 11)'}]) +
         r"<strong>Step 2: finish the question.</strong> The solutions are $x = -4$ and $x = 7$, and their sum is $3$.<br><strong>Check:</strong> $2x - 3 = 11$ gives $x = 7$; $2x - 3 = -11$ gives $x = -4$. ✓",
  "trap": r"Stopping at the first crossing and entering $7$. The question asks for the sum, and this equation has a second solution on the other arm of the V. If you see only one crossing, drag the graph or zoom out.",
  "desmos": [r"y=\left|2x-3\right|", "y=11", window(-10, 13, -3, 16)],
  "micro": {"q": r"$$3x + 2y = 16$$ $$y = x - 2$$ The solution to the system above is $(x, y)$. The value of $x$ is", "accept": ["4"],
            "exp": r"The lines cross at $(4, 2)$. Check: $3(4) + 2(2) = 16$ and $2 = 4 - 2$. ✓"}},
 {"ess": True, "name": "Move 4: Count the solutions",
  "rule": r"count the crossings &nbsp;·&nbsp; a line that just touches a curve counts once",
  "say": r"“How many solutions” is a counting question, and a graph can help you count. Two lines are usually quick to read. A line and a parabola need a second look, because a line that just touches the curve gives exactly one solution, and from far away a touch can look like a near miss or like two crossings close together. Zoom in on that spot before you decide.",
  "prob": r"$$y = x^2 - 4x + 7$$ $$y = 2x - 2$$ How many solutions does the system of equations above have?",
  "sol": r"<strong>Step 1: graph both.</strong>" + dz([{'x': r'y = x^2 - 4x + 7'}, {'x': r'y = 2x - 2', 'see': 'one dot where they meet: (3, 4)'}]) +
         r"<strong>Step 2: zoom in on the contact.</strong> The line touches the parabola at $(3, 4)$ and stays below it everywhere else. Exactly one solution.<br><strong>Check:</strong> setting the two equal gives $x^2 - 6x + 9 = 0$, which is $(x - 3)^2 = 0$: one value of $x$. ✓",
  "trap": r"Deciding from the default window. At that zoom the line and the curve seem to run together for a stretch. Zoom in until you can see whether there is one dot or two, and use algebra to confirm: a perfect square means one solution.",
  "desmos": ["y=x^2-4x+7", "y=2x-2", window(-2, 8, -2, 12)],
  "micro": {"mc": True, "q": r"$$x - 2y = 3$$ $$3x - 6y = 4$$ How many solutions does the system above have?",
            "opts": ["Zero", "Exactly one", "Exactly two", "Infinitely many"], "correct": 0,
            "exp": r"The two lines are parallel: both have slope $\tfrac{1}{2}$, with different intercepts. Tripling the first equation gives $3x - 6y = 9$, not $4$, so they are not the same line."}},
 {"ess": True, "name": "Move 5: Slide an unknown constant",
  "rule": r"no solution: slide to parallel &nbsp;·&nbsp; infinitely many: slide to the same line &nbsp;·&nbsp; exactly one: slide to a touch",
  "say": r"A constant in an equation is a dial. Type the system with the $k$ still in it, accept the slider Desmos offers, and turn the dial until the picture matches the words of the question. “No solution” for two lines means parallel. Then confirm the value with one line of algebra, because a slider only stops on the values its step allows.",
  "prob": r"$$2x - 5y = 7$$ $$6x + ky = 4$$ In the system of equations above, $k$ is a constant. For what value of $k$ does the system have no solution?",
  "sol": r"<strong>Step 1: type it with the $k$.</strong>" + dz([{'x': r'2x - 5y = 7'}, {'x': r'6x + ky = 4', 'see': 'click <em>add slider: k</em>, then widen its range to &minus;20 through 20'}, {'x': r'k = -15', 'see': 'the lines are parallel here'}]) +
         r"<strong>Step 2: confirm with slopes.</strong> The first line has slope $\tfrac{2}{5}$ and the second has slope $-\tfrac{6}{k}$. They match when $-\tfrac{6}{k} = \tfrac{2}{5}$, so $k = -15$.<br><strong>Check they are different lines:</strong> tripling the first equation gives $6x - 15y = 21$, not $4$. Parallel and distinct: no solution. ✓",
  "trap": r"The slider starts with a range of $-10$ to $10$, and the answer here is $-15$. If you drag to the end and the lines do not become parallel, the answer may be outside the range: click the number at the end of the slider and widen it.",
  "desmos": ["2x-5y=7", "6x+ky=4", slider('k', 5, -20, 20, 1)],
  "micro": {"q": r"The graph of $y = x^2 + 6x + c$, where $c$ is a constant, touches the $x$-axis at exactly one point. The value of $c$ is", "accept": ["9"],
            "exp": r"Slide $c$ until the vertex rests on the axis: $c = 9$. The equation becomes $y = (x + 3)^2$, a perfect square."}},
 {"ess": True, "name": "Move 6: Name it, reuse it, test the choices",
  "rule": r"equivalent expressions have the same graph &nbsp;·&nbsp; the matching choice sits on top of the original",
  "say": r"When the answer choices are four expressions, you can check each one against the original. Graph the original, then graph each choice. Three of them separate from the original somewhere, and one sits on top of it. That one is equivalent. Multiplying it out is a good way to confirm.",
  "prob": r"Which of the following expressions is equivalent to $(2x + 3)(x - 4)$?<br>A) $2x^2 - 12$<br>B) $2x^2 - 5x - 12$<br>C) $2x^2 + 5x - 12$<br>D) $2x^2 - 11x - 12$",
  "sol": r"<strong>Step 1: graph the original and the choices.</strong>" + dz([{'x': r'y = (2x + 3)(x - 4)'}, {'x': r'y = 2x^2 - 5x - 12', 'see': 'choice B sits on top of the original; hide and show it with the colored circle to check'}]) +
         r"<strong>Step 2: confirm.</strong> Multiply it out: $2x^2 - 8x + 3x - 12 = 2x^2 - 5x - 12$. Choice B. ✓",
  "trap": r"Choice A multiplies only first by first and last by last. Choice C has the middle sign backwards. All four parabolas open the same way and share the $y$-intercept $-12$, so look along the whole curve, not at one point.",
  "desmos": ["y=(2x+3)(x-4)", "y=2x^2-12", "y=2x^2-5x-12", "y=2x^2+5x-12", "y=2x^2-11x-12", window(-6, 9, -30, 14)],
  "micro": {"q": r"Type $f(x) = x^2 - 6x + 5$ into Desmos. On new lines, evaluate $f(3)$ and $f(0)$. Then $f(3) + f(0) =$", "accept": ["1"],
            "exp": r"$f(3) = -4$ and $f(0) = 5$, so the sum is $1$. Once $f$ is named, any input is one short line."}},
 {"ess": False, "name": "Move 7: Shade the inequalities",
  "rule": r"solutions are the points shaded twice &nbsp;·&nbsp; a dashed edge is not included",
  "say": r"A system of inequalities has a whole region of solutions, and a question usually asks about one part of it: a point with a given $x$, or the largest or smallest value a coordinate can take. Graph both inequalities, add the vertical line for the given $x$, and read where that line passes through the overlap. Then check whether each end of that stretch is solid or dashed.",
  "prob": r"$$y \leq 2x + 1$$ $$y > -x + 4$$ The point $(3, b)$ is a solution to the system of inequalities above. What is the least possible integer value of $b$?",
  "sol": r"<strong>Step 1: graph the system and the line $x = 3$.</strong>" + dz([{'x': r'y \leq 2x + 1'}, {'x': r'y > -x + 4'}, {'x': r'x = 3', 'see': 'inside the overlap from just above y = 1 up to y = 7'}]) +
         r"<strong>Step 2: read the ends.</strong> At $x = 3$ the conditions are $b \leq 7$ (solid, included) and $b > 1$ (dashed, not included). The least integer greater than $1$ is $2$.",
  "trap": r"Answering $1$. The point $(3, 1)$ sits on the dashed line $y = -x + 4$, and a dashed edge is not part of the solution. Check the boundary type on “least integer” and “greatest integer” questions.",
  "desmos": [r"y\le 2x+1", "y>-x+4", "x=3"],
  "micro": {"mc": True, "q": r"$$y > x - 1$$ $$y < -x + 7$$ Which point is a solution to the system above?",
            "opts": ["$(4, 1)$", "$(2, 3)$", "$(5, 3)$", "$(1, 7)$"], "correct": 1,
            "exp": r"Type the four points on top of the shading: only $(2, 3)$ lands in the overlap. Check: $3 > 1$ and $3 < 5$. ✓"}},
 {"ess": False, "name": "Move 8: Lists do the statistics",
  "rule": r"$\text{mean}(\ldots)$ &nbsp;·&nbsp; $\text{median}(\ldots)$ &nbsp;·&nbsp; any order, no sorting",
  "say": r"Mean and median questions involve several small arithmetic steps, and small slips are easy to make when you are working quickly. Type the list once inside $\text{mean}$ and once inside $\text{median}$, and Desmos sorts, counts and divides. You still need to read what the question does with those two numbers.",
  "prob": r"The data set $\{4, 9, 9, 13, 20, 23\}$ has mean $m$ and median $d$. What is the value of $m - d$?",
  "sol": r"<strong>Step 1: two lines.</strong>" + dz([{'x': r'\operatorname{mean}(4, 9, 9, 13, 20, 23)', 'val': '13'}, {'x': r'\operatorname{median}(4, 9, 9, 13, 20, 23)', 'val': '11'}]) +
         r"<strong>Step 2: finish the question.</strong> $m - d = 13 - 11 = 2$.<br><strong>Check:</strong> the sum is $78$ and $78 \div 6 = 13$; with six values the median averages the third and fourth, $\tfrac{9 + 13}{2} = 11$. ✓",
  "trap": r"By hand, a common slip is taking $9$ or $13$ as the median, a single middle value, when an even count needs the average of the two middle values. Desmos averages the two middle values for you.",
  "desmos": [r"\operatorname{mean}(4,9,9,13,20,23)", r"\operatorname{median}(4,9,9,13,20,23)"],
  "micro": {"q": r"In Desmos, $\text{median}(6, 2, 11, 7, 4) =$", "accept": ["6"],
            "exp": r"Sorted, the list is $2, 4, 6, 7, 11$ and the middle value is $6$. Desmos did the sorting for you."}},
 {"ess": False, "name": "Move 9: A table and a tilde",
  "rule": r"points in a table &nbsp;·&nbsp; then $y_1 \sim m x_1 + b$ &nbsp;·&nbsp; $m$ is the slope, $b$ is the intercept",
  "say": r"When the answer choices are close, estimating a line of best fit by eye is unreliable. Enter the points in a table, type the model with a tilde where the equals sign would go, and Desmos reports a fitted slope and intercept. Then compare them with the choices, slope first.",
  "prob": r"Which of the following best approximates the line of best fit for the points $(1, 4)$, $(3, 9)$, $(6, 14)$, and $(8, 19)$?<br>A) $y = 2.1x + 2.2$<br>B) $y = 2.2x + 2.1$<br>C) $y = -2.1x + 2.2$<br>D) $y = 0.5x + 9.3$",
  "sol": r"<strong>Step 1: table, then tilde.</strong>" + dz([{'x': r'\text{table: }\ x_1 = 1, 3, 6, 8 \quad y_1 = 4, 9, 14, 19'}, {'x': r'y_1 \sim m x_1 + b', 'out': ['m = 2.06897', 'b = 2.18966'], 'stat': 'R^2 = 0.9931'}]) +
         r"<strong>Step 2: match, slope first.</strong> Slope about $2.1$, intercept about $2.2$: choice A.",
  "trap": r"Choice B has the same two numbers in the wrong places. The slope is the number multiplying $x$; the intercept stands alone. Choice C has the right size and the wrong direction: these points rise.",
  "desmos": [table([1, 3, 6, 8], [4, 9, 14, 19]), r"y_{1}\sim mx_{1}+b", window(-1, 10, -2, 24)],
  "micro": {"q": r"Enter the points $(0, 3)$, $(2, 8)$, $(4, 11)$ and $(6, 18)$ in a table and type $y_1 \sim m x_1 + b$. Desmos reports $m =$", "accept": ["2.4", "12/5"],
            "exp": r"$m = 2.4$ and $b = 2.8$: the line of best fit is $y = 2.4x + 2.8$."}},
]
LAST_STARRED_STEP_INDEX = 5

# ---------------------------------------------------------------- TAB 3: FLUENCY
COUNT4 = ["Zero", "Exactly one", "Exactly two", "Infinitely many"]
FLUENCY = [
 {"sec": "A. Type it right", "items": [
   {"mc": True, "q": r"The test prints $4a + 3b = 24$. To graph it in Desmos, you type", "opts": [r"$4a + 3b = 24$, exactly as printed", r"$4x + 3y = 24$", r"$y = 4a + 3b$", r"$a = 24 - 3b$"], "correct": 1,
    "exp": r"Desmos graphs in $x$ and $y$ and offers sliders for other letters, so retype $a$ as $x$ and $b$ as $y$."},
   {"mc": True, "q": r"You type " + kbd('y=3/4x&minus;2') + r" and never press the right arrow. Desmos graphs", "opts": [r"$y = \dfrac{3}{4}x - 2$", r"$y = \dfrac{3}{4x - 2}$", r"$y = \dfrac{3}{4x} - 2$", "nothing: it shows an error"], "correct": 1,
    "exp": r"Everything after the slash stays in the denominator until you press the right arrow. Type 3 / 4, then the arrow, then $x - 2$."},
   {"q": r"Type $\sqrt{50} + |-7|$ using " + kbd('sqrt') + " and " + kbd('abs(') + r". To the nearest hundredth, Desmos shows", "accept": ["14.07", "14.071"],
    "exp": r"$\sqrt{50} \approx 7.071$ and $|-7| = 7$, so the total is about $14.07$. Press the right arrow to leave the root before you type the plus sign."},
   {"mc": True, "q": r"Which entry graphs $y = 2^{x + 1}$?", "opts": [kbd('y=2^x+1'), kbd('y=2^(x+1)'), kbd('y=2x+1'), kbd('y=2^x^1')], "correct": 1,
    "exp": r"A plus sign closes the exponent, so the first entry graphs $y = 2^x + 1$. Parentheses keep $x + 1$ together in the exponent."},
 ]},
 {"sec": "B. Read the dots", "items": [
   {"q": r"Graph $y = x^2 - 2x - 15$. Its positive $x$-intercept is $x =$", "accept": ["5"], "exp": r"The dots on the $x$-axis are $(-3, 0)$ and $(5, 0)$. Check: $(x - 5)(x + 3)$."},
   {"q": r"Graph $y = -x^2 + 8x - 7$. The maximum value of $y$ is", "accept": ["9"], "exp": r"The vertex dot reads $(4, 9)$. The maximum value is the $y$-coordinate, $9$."},
   {"q": r"Graph $y = 3x^2 - 20$. To the nearest hundredth, its positive $x$-intercept is $x =$", "accept": ["2.58", "2.582"], "exp": r"The right-hand dot reads $(2.582, 0)$. Exactly, $x = \sqrt{\tfrac{20}{3}}$."},
   {"q": r"Graph the circle $(x + 1)^2 + (y - 4)^2 = 9$ and click it. The $y$-coordinate of its highest point is", "accept": ["7"], "exp": r"The top dot is $(-1, 7)$: the center's height, $4$, plus the radius, $3$."},
 ]},
 {"sec": "C. Crossings and counts", "items": [
   {"q": r"The lines $y = 3x - 5$ and $y = -x + 7$ cross at $(x, y)$. The value of $y$ is", "accept": ["4"], "exp": r"They cross at $(3, 4)$. The question asks for $y$."},
   {"q": r"Graph $y = |x - 4|$ and $y = 9$. The smaller solution of $|x - 4| = 9$ is $x =$", "accept": ["-5"], "exp": r"The crossings are at $x = -5$ and $x = 13$. The smaller one is $-5$."},
   {"mc": True, "q": r"How many solutions does the system $2x + y = 5$ and $4x + 2y = 10$ have?", "opts": COUNT4, "correct": 3,
    "exp": r"Only one line appears: the second equation is the first one doubled. Every point on the line is a solution."},
   {"mc": True, "q": r"How many times does the parabola $y = x^2 - 4x + 1$ meet the line $y = -5$?", "opts": ["Zero", "Once", "Twice", "Three times"], "correct": 0,
    "exp": r"The vertex of the parabola is $(2, -3)$, and it opens upward, so it does not reach $y = -5$."},
 ]},
 {"sec": "D. Sliders, lists, shading", "items": [
   {"q": r"Type $y = 2x + 3$ and $y = kx - 1$ and add the slider. The lines never meet when $k =$", "accept": ["2"], "exp": r"At $k = 2$ the slopes match and the intercepts differ: parallel lines."},
   {"q": r"In Desmos, $\text{mean}(12, 15, 15, 18, 25) =$", "accept": ["17"], "exp": r"The sum is $85$, and $85 \div 5 = 17$."},
   {"q": r"In Desmos, $\text{median}(31, 8, 19, 24, 8, 12) =$", "accept": ["15.5", "31/2"], "exp": r"Sorted: $8, 8, 12, 19, 24, 31$. The median averages the middle two: $\tfrac{12 + 19}{2} = 15.5$."},
   {"mc": True, "q": r"On the graph of $y < 3x - 2$, the boundary line is", "opts": ["solid, and its points are solutions", "dashed, and its points are solutions", "dashed, and its points are not solutions", "solid, and its points are not solutions"], "correct": 2,
    "exp": r"A strict inequality ($<$ or $>$) draws a dashed edge, and points on that edge do not satisfy it."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE
GAUNTLET = [
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"The function $f$ is defined by $f(x) = x^2 - 10x + 16$. What is the minimum value of $f$?",
  "label": "Minimum $=$", "accept": ["-9"], "desmos": ["f(x)=x^2-10x+16", window(-3, 13, -12, 20)],
  "sol": r"<strong>Given:</strong> a quadratic; the minimum is at its vertex.<br><br>" + dz([{'x': r'f(x) = x^2 - 10x + 16', 'see': 'click the lowest point: (5, &minus;9)'}]) + r"The minimum value is the $y$-coordinate, $-9$. Check: $f(5) = 25 - 50 + 16 = -9$. ✓",
  "trap": r"Entering $5$. That is where the minimum happens; the question asks for the minimum value itself."},
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"$$y = 2x + 1$$ $$3x + y = 16$$ The solution to the system of equations above is $(x, y)$. What is the value of $y$?",
  "options": ["$3$", "$5$", "$7$", "$10$"], "correct": 2, "desmos": ["y=2x+1", "3x+y=16"],
  "sol": r"<strong>Given:</strong> two lines; the solution is their crossing.<br><br>" + dz([{'x': r'y = 2x + 1'}, {'x': r'3x + y = 16', 'see': 'click the crossing: (3, 7)'}]) + r"The question asks for $y$: choice C. Check: $2(3) + 1 = 7$ and $3(3) + 7 = 16$. ✓",
  "trap": r"Choice A is $x$. Read which coordinate the question wants after you click the dot."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"$$5x - 2y = 8$$ $$10x - 4y = 3$$ How many solutions does the system of equations above have?",
  "options": ["Zero", "Exactly one", "Exactly two", "Infinitely many"], "correct": 0, "desmos": ["5x-2y=8", "10x-4y=3"],
  "sol": r"<strong>Given:</strong> two equations in standard form; the question is a count.<br><br>Type both as printed. Two parallel lines appear: both have slope $\tfrac{5}{2}$, and they cross the $y$-axis at $-4$ and at $-0.75$. Parallel lines never meet, so there is no solution.",
  "trap": r"“Infinitely many” needs the two equations to be the same line. Doubling the first gives $10x - 4y = 16$, not $3$, so the lines are parallel, not identical. For two linear equations, two parallel lines on screen mean no solution; a single line means infinitely many."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"What is the positive solution to the equation $|3x + 2| = 13$?",
  "label": "$x =$", "accept": ["11/3", "3.666", "3.667"], "desmos": [r"y=\left|3x+2\right|", "y=13", window(-10, 10, -3, 18)],
  "sol": r"<strong>Given:</strong> an absolute value equation; graph each side.<br><br>" + dz([{'x': r'y = |3x + 2|'}, {'x': r'y = 13', 'see': 'crossings at x = &minus;5 and x = 3.667'}]) + r"The positive solution is $x = \tfrac{11}{3}$. Check: $3x + 2 = 13$ gives $x = \tfrac{11}{3}$. ✓",
  "trap": r"Entering $3.67$. A decimal that does not end needs to fill the answer box: $3.666$ or $3.667$, or the fraction $11/3$. An entry rounded to two places is not accepted."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"Which of the following expressions is equivalent to $(3x - 2)^2 - (x + 4)(x - 4)$?",
  "options": [r"$8x^2 - 12x - 12$", r"$8x^2 - 12x + 20$", r"$8x^2 + 20$", r"$10x^2 - 12x + 20$"], "correct": 1,
  "desmos": ["y=(3x-2)^2-(x+4)(x-4)", "y=8x^2-12x-12", "y=8x^2-12x+20", "y=8x^2+20", "y=10x^2-12x+20", window(-4, 5, -20, 60)],
  "sol": r"<strong>Given:</strong> four candidate expressions; equivalent expressions have identical graphs.<br><br>Graph $y = (3x - 2)^2 - (x + 4)(x - 4)$, then each choice. Choice B sits on top of it.<br>Algebra: $(9x^2 - 12x + 4) - (x^2 - 16) = 8x^2 - 12x + 20$. ✓",
  "trap": r"Choice A subtracts the $16$ when it should add it: $-(x^2 - 16)$ is $-x^2 + 16$. Choice C squares $3x - 2$ without the middle term."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"$$4x - 3y = 6$$ $$kx + 9y = 5$$ In the system of equations above, $k$ is a constant. If the system has no solution, what is the value of $k$?",
  "label": "$k =$", "accept": ["-12"], "desmos": ["4x-3y=6", "kx+9y=5", slider('k', 3, -20, 20, 1)],
  "sol": r"<strong>Given:</strong> a system with a constant; no solution means parallel lines.<br><br>Type both equations, add the slider for $k$, and widen its range. The lines are parallel at $k = -12$.<br>Algebra: the slopes are $\tfrac{4}{3}$ and $-\tfrac{k}{9}$, and $-\tfrac{k}{9} = \tfrac{4}{3}$ gives $k = -12$. ✓",
  "trap": r"The slider's starting range stops at $-10$. If nothing looks parallel, the answer may be beyond the end of the slider: widen it, or compare the slopes."},
 {"ess": False, "type": "mc", "diff": "Medium", "fig": "g7",
  "stem": r"The scatterplot above shows the points $(2, 3)$, $(4, 8)$, $(7, 12)$, and $(9, 17)$. Which of the following is closest to the equation of the line of best fit for these points?",
  "options": [r"$y = -0.4x + 1.9$", r"$y = 1.9x + 0.4$", r"$y = 0.5x + 7.3$", r"$y = 1.9x - 0.4$"], "correct": 3,
  "desmos": [table([2, 4, 7, 9], [3, 8, 12, 17]), r"y_{1}\sim mx_{1}+b", window(-1, 11, -3, 20)],
  "sol": r"<strong>Given:</strong> four data points; a best-fit line is a table and a tilde.<br><br>" + dz([{'x': r'\text{table: }\ x_1 = 2, 4, 7, 9 \quad y_1 = 3, 8, 12, 17'}, {'x': r'y_1 \sim m x_1 + b', 'out': ['m = 1.89655', 'b = -0.431034']}]) + r"Slope about $1.9$, intercept about $-0.4$: choice D.",
  "trap": r"Choice B has the right slope and the wrong sign on the intercept: the fitted line crosses the $y$-axis just below zero. Choice A swaps the two numbers."},
 {"ess": False, "type": "ne", "diff": "Medium",
  "stem": r"$$y \geq 2x - 3$$ $$y < -x + 9$$ The point $(3, b)$ is a solution to the system of inequalities above. What is the greatest possible integer value of $b$?",
  "label": "$b =$", "accept": ["5"], "desmos": [r"y\ge 2x-3", "y<-x+9", "x=3"],
  "sol": r"<strong>Given:</strong> two inequalities and a fixed $x$.<br><br>Graph both and add $x = 3$. Along that line the overlap runs from $b = 3$ (solid, included) up to $b = 6$ (dashed, not included). The greatest integer below $6$ is $5$.<br>Check: $5 \geq 3$ and $5 < 6$. ✓",
  "trap": r"Answering $6$. The point $(3, 6)$ is on the dashed line $y = -x + 9$, and a dashed edge is not part of the solution."},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"$$f(x) = 2x^2 - 8x + 3$$ The function $g$ is defined by $g(x) = f(x) + 5$. How many $x$-intercepts does the graph of $y = g(x)$ have?",
  "options": ["Zero", "Exactly one", "Exactly two", "Infinitely many"], "correct": 1, "desmos": ["f(x)=2x^2-8x+3", "g(x)=f(x)+5", window(-3, 7, -7, 12)],
  "sol": r"<strong>Given:</strong> a parabola moved up $5$.<br><br>" + dz([{'x': r'f(x) = 2x^2 - 8x + 3', 'see': 'vertex (2, &minus;5)'}, {'x': r'g(x) = f(x) + 5', 'see': 'vertex (2, 0): resting on the x-axis'}]) + r"The graph of $g$ touches the $x$-axis at one point. Check: $g(x) = 2x^2 - 8x + 8 = 2(x - 2)^2$. ✓",
  "trap": r"Counting the intercepts of $f$, which has two. The question is about $g$, and the shift of $5$ lifts the vertex onto the axis."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$y = x^2 - 6x + c$$ $$y = 2x - 9$$ In the system of equations above, $c$ is a constant. The graphs of the two equations intersect at exactly one point. What is the value of $c$?",
  "label": "$c =$", "accept": ["7"], "desmos": ["y=x^2-6x+c", "y=2x-9", slider('c', 0, -10, 10, 1)],
  "sol": r"<strong>Given:</strong> a parabola with a constant and a line; exactly one intersection means the line just touches.<br><br>Type both, add the slider for $c$, and slide until the two crossings merge into one: $c = 7$, touching at $(4, -1)$.<br>Algebra: $x^2 - 8x + (c + 9) = 0$ has one solution when $64 - 4(c + 9) = 0$, so $c = 7$. ✓",
  "trap": r"Stopping one notch early. At $c = 6$ the two crossings sit very close together and can pass for one. Zoom in on the contact point, or use the discriminant to confirm."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$\tfrac{2}{3}x - \tfrac{1}{4}y = 5$$ $$\tfrac{1}{2}x + \tfrac{3}{8}y = 6$$ The solution to the system of equations above is $(x, y)$. What is the value of $x + y$?",
  "label": "$x + y =$", "accept": ["13"], "desmos": [r"\frac{2}{3}x-\frac{1}{4}y=5", r"\frac{1}{2}x+\frac{3}{8}y=6", window(-2, 16, -4, 12)],
  "sol": r"<strong>Given:</strong> a system with a fraction on every term. By hand this is two rounds of clearing denominators; in Desmos it is two lines.<br><br>" + dz([{'x': r'\tfrac{2}{3}x - \tfrac{1}{4}y = 5'}, {'x': r'\tfrac{1}{2}x + \tfrac{3}{8}y = 6', 'see': 'click the crossing: (9, 4)'}]) + r"$x + y = 13$. Check: $\tfrac{2}{3}(9) - \tfrac{1}{4}(4) = 6 - 1 = 5$ and $\tfrac{1}{2}(9) + \tfrac{3}{8}(4) = 4.5 + 1.5 = 6$. ✓",
  "trap": r"Give each fraction its own right arrow: type 2 / 3, arrow, then $x$. If you skip the arrow, the $x$ goes into the denominator and the graph changes shape without any warning. Read each line back before you click the crossing.",
  "extrasIntro": r"Graphing is especially helpful when a system has fraction or decimal coefficients. Three more to try: type each system as printed.",
  "extras": [
   {"type": "ne", "q": r"$0.5x + 0.25y = 4$ and $x - y = 2$. The value of $x$ is", "label": "$x =$", "accept": ["6"], "exp": r"The lines cross at $(6, 4)$."},
   {"type": "ne", "q": r"$\tfrac{1}{3}x + \tfrac{1}{2}y = 7$ and $x - y = 1$. The value of $y$ is", "label": "$y =$", "accept": ["8"], "exp": r"The lines cross at $(9, 8)$. Check: $3 + 4 = 7$."},
   {"type": "ne", "q": r"$1.2x - 0.4y = 2$ and $0.3x + 0.2y = 0.8$. The value of $x + y$ is", "label": "$x + y =$", "accept": ["3"], "exp": r"The lines cross at $(2, 1)$, so $x + y = 3$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"What is the sum of the solutions to the equation $|2x - 5| = x + 2$?",
  "label": "Sum $=$", "accept": ["8"], "desmos": [r"y=\left|2x-5\right|", "y=x+2", window(-4, 12, -3, 14)],
  "sol": r"<strong>Given:</strong> an absolute value with a variable on the other side, so the right side is a slanted line.<br><br>" + dz([{'x': r'y = |2x - 5|'}, {'x': r'y = x + 2', 'see': 'crossings at (1, 3) and (7, 9)'}]) + r"The solutions are $x = 1$ and $x = 7$, and their sum is $8$.<br>Algebra: $2x - 5 = x + 2$ gives $x = 7$; $-(2x - 5) = x + 2$ gives $x = 1$. ✓",
  "trap": r"When a variable sits on both sides of an absolute value equation, graph both sides and count the crossings. A case solved by hand can produce a value that fails the original equation and has to be tested; the graph shows only true solutions."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"$$f(x) = (x - 3)^2 - 4$$ The function $g$ is defined by $g(x) = f(x + 2)$. What is the sum of the $x$-intercepts of the graph of $y = g(x)$?",
  "label": "Sum $=$", "accept": ["2"], "desmos": ["f(x)=(x-3)^2-4", "g(x)=f(x+2)"],
  "sol": r"<strong>Given:</strong> a parabola shifted sideways through function notation.<br><br>" + dz([{'x': r'f(x) = (x - 3)^2 - 4', 'see': 'x-intercepts 1 and 5'}, {'x': r'g(x) = f(x + 2)', 'see': 'the same curve moved 2 to the left: x-intercepts &minus;1 and 3'}]) + r"The sum is $-1 + 3 = 2$.",
  "trap": r"You can check the direction of a shift in Desmos: type $g(x) = f(x + 2)$ and look. $f(x + 2)$ moves the graph to the left, so the intercepts $1$ and $5$ become $-1$ and $3$, not $3$ and $7$."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"What is the solution to the equation $\sqrt{2x + 7} = x - 4$?",
  "label": "$x =$", "accept": ["9"], "desmos": [r"y=\sqrt{2x+7}", "y=x-4", window(-5, 14, -6, 9)],
  "sol": r"<strong>Given:</strong> a radical equation. Squaring both sides by hand can create an extra value that does not satisfy the original equation.<br><br>" + dz([{'x': r'y = \sqrt{2x + 7}'}, {'x': r'y = x - 4', 'see': 'one crossing: (9, 5)'}]) + r"The only solution is $x = 9$. Check: $\sqrt{25} = 5$ and $9 - 4 = 5$. ✓",
  "trap": r"Graphing a radical equation is a good check on the algebra. Squaring gives $x^2 - 10x + 9 = 0$, so $x = 1$ or $x = 9$, but $x = 1$ makes the left side $3$ and the right side $-3$. The curve and the line do not meet there, so the graph shows only $x = 9$."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"In the $xy$-plane, the line $y = kx - 4$, where $k$ is a positive constant, intersects the parabola $y = x^2$ at exactly one point. What is the value of $k$?",
  "label": "$k =$", "accept": ["4"], "desmos": ["y=x^2", "y=kx-4", slider('k', 1, -10, 10, 0.5)],
  "sol": r"<strong>Given:</strong> a line through $(0, -4)$ whose slope is the unknown; exactly one intersection means it just touches the parabola.<br><br>Type both, add the slider, and turn the line until it touches the curve: $k = 4$, touching at $(2, 4)$.<br>Algebra: $x^2 - kx + 4 = 0$ has one solution when $k^2 - 16 = 0$, so $k = 4$ or $k = -4$. The question says positive. ✓",
  "trap": r"“Exactly one point” for a line and a parabola means the line just touches. The slider finds two touching positions here, $k = 4$ and $k = -4$, and the word “positive” in the question chooses between them."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"$$y \leq 2x + 3$$ $$y \leq -x + 12$$ For all points $(x, y)$ that satisfy the system of inequalities above, what is the maximum possible value of $y$?",
  "label": "Maximum $y =$", "accept": ["9"], "desmos": [r"y\le 2x+3", r"y\le -x+12", window(-4, 14, -4, 14)],
  "sol": r"<strong>Given:</strong> a region under two lines; its highest point is the corner where the lines cross.<br><br>" + dz([{'x': r'y \leq 2x + 3'}, {'x': r'y \leq -x + 12', 'see': 'the overlap comes to a peak where the lines cross: (3, 9)'}]) + r"Both edges are solid, so the corner is included: the maximum value of $y$ is $9$.",
  "trap": r"In a region like this one, the largest value of $y$ is at a corner of the overlap. Reading $12$, the $y$-intercept of the second line, picks a point outside the first region. A corner has to satisfy both inequalities."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"A system is printed with the variables $p$ and $q$. Before you graph it in Desmos, you", "opts": [r"retype it with $x$ and $y$", r"solve each equation for $p$", r"add a slider for $q$", "switch to degree mode"], "correct": 0,
  "exp": r"Desmos graphs in $x$ and $y$ and offers sliders for other letters."},
 {"q": r"The positive $x$-intercept of the graph of $y = x^2 - 4x - 12$ is", "opts": ["$2$", "$4$", "$6$", "$12$"], "correct": 2,
  "exp": r"The dots on the $x$-axis are $(-2, 0)$ and $(6, 0)$: $(x - 6)(x + 2) = 0$."},
 {"q": r"You type two different linear equations and only one line appears. The system has", "opts": ["no solution", "exactly one solution", "exactly two solutions", "infinitely many solutions"], "correct": 3,
  "exp": r"One line for two equations means they are the same line, and every point on it is a solution."},
]

# ---------------------------------------------------------------- FIGURES
FIGS_JS = r'''var FIGS = {
    dots: { xmin: -5, xmax: 10, ymin: -10.5, ymax: 6, w: 360, h: 250, alt: 'the parabola y = x squared minus 2x minus 8 with gray dots at its x-intercepts (negative 2, 0) and (4, 0), its y-intercept (0, negative 8), and its vertex (1, negative 9)',
        curves: [{ a: 1, b: -2, c: -8, label: 'y = x² − 2x − 8', lx: 4.6, ly: 3.4, dx: 12, dy: 0 }],
        gdots: [{ x: -2, y: 0, label: '(−2, 0)', dx: -50, dy: -8 }, { x: 4, y: 0, label: '(4, 0)', dx: 8, dy: 16 }, { x: 0, y: -8, label: '(0, −8)', dx: -50, dy: 4 }, { x: 1, y: -9, label: 'vertex (1, −9)', dx: 10, dy: 12 }] },
    hmax: { xmin: -2, xmax: 10, ymin: -7, ymax: 22, w: 320, h: 260, alt: 'a downward parabola crossing the x-axis at 1 and 7 with its highest point marked',
        curves: [{ a: -2, b: 16, c: -14, label: 'y = h(x)', lx: 6.6, ly: 12, dx: 8, dy: 0 }],
        gdots: [{ x: 1, y: 0, label: '(1, 0)', dx: 9, dy: 16 }, { x: 7, y: 0, label: '(7, 0)', dx: 9, dy: -8 }, { x: 4, y: 18, label: 'highest point', dx: 10, dy: 0 }] },
    circle: { xmin: -4, xmax: 10, ymin: -8.5, ymax: 4.5, w: 324, h: 304, alt: 'a circle with gray dots at its top (3, 3) and bottom (3, negative 7); the center (3, negative 2) is halfway between',
        circles: [{ x: 3, y: -2, r: 5 }],
        segs: [{ x1: 3, y1: 3, x2: 3, y2: -7 }],
        points: [{ x: 3, y: -2, label: 'center (3, −2)', dx: 8, dy: 4 }],
        gdots: [{ x: 3, y: 3, label: 'top (3, 3)', dx: 9, dy: -6 }, { x: 3, y: -7, label: 'bottom (3, −7)', dx: 9, dy: 15 }],
        labels: [{ x: 3, y: 1.4, text: 'radius 5', dx: 8, dy: 4, cls: 'sm' }] },
    cross: { xmin: -2, xmax: 8, ymin: -4, ymax: 9.5, w: 320, h: 250, alt: 'the lines 3x + 2y = 16 and y = x minus 2 crossing at the point (4, 2)',
        lines: [{ m: -1.5, b: 8, label: '3x + 2y = 16', lx: 0.3, ly: 8.4, dx: 16, dy: 2 }, { m: 1, b: -2, cls: 'ln2', label: 'y = x − 2', lx: 6.2, ly: 4.2, dx: -10, dy: 26 }],
        gdots: [{ x: 4, y: 2, label: '(4, 2)', dx: -8, dy: -12 }] },
    c_one: { xmin: -3, xmax: 4, ymin: -2, ymax: 5, w: 190, h: 160, alt: 'two lines crossing at one point',
        lines: [{ m: 1, b: 1 }, { m: -1, b: 3, cls: 'ln2' }], gdots: [{ x: 1, y: 2 }],
        labels: [{ x: -3, y: -2, text: 'cross once: one solution', dx: 4, dy: 12, cls: 'sm' }] },
    c_none: { xmin: -3, xmax: 4, ymin: -2, ymax: 5, w: 190, h: 160, alt: 'two parallel lines',
        lines: [{ m: 0.5, b: 2.4 }, { m: 0.5, b: 0.2, cls: 'ln2' }],
        labels: [{ x: -3, y: -2, text: 'parallel: no solution', dx: 4, dy: 12, cls: 'sm' }] },
    c_same: { xmin: -3, xmax: 4, ymin: -2, ymax: 5, w: 190, h: 160, alt: 'a single line, drawn for two equations that describe the same line',
        lines: [{ m: 0.5, b: 1.3 }],
        labels: [{ x: -3, y: -2, text: 'one line: infinitely many', dx: 4, dy: 12, cls: 'sm' }] },
    tangent: { xmin: -1.5, xmax: 7, ymin: -3, ymax: 11, w: 320, h: 260, alt: 'the parabola y = x squared minus 4x + 7 and the line y = 2x minus 2 touching at the single point (3, 4)',
        curves: [{ a: 1, b: -4, c: 7, label: 'y = x² − 4x + 7', lx: 0, ly: 9.8, dx: 30, dy: 0 }],
        lines: [{ m: 2, b: -2, cls: 'ln2', label: 'y = 2x − 2', lx: 5.2, ly: 5.6, dx: 6, dy: 0 }],
        gdots: [{ x: 3, y: 4, label: '(3, 4)', dx: -46, dy: -4 }] },
    slider: { xmin: -4, xmax: 8, ymin: -5, ymax: 5, w: 330, h: 240, alt: 'the line 2x minus 5y = 7 with the second line shown dashed at k = 5, where the two lines cross, and solid at k = negative 15, where they are parallel',
        lines: [{ m: 0.4, b: -1.4, label: '2x − 5y = 7', lx: 4.4, ly: -0.6, dx: 0, dy: 22 }, { m: -1.2, b: 0.8, cls: 'dash', label: 'k = 5', lx: -3.8, ly: 3.0, dx: 0, dy: 0 }, { m: 0.4, b: -0.2667, cls: 'ln2', label: 'k = −15: parallel', lx: 3.4, ly: 3.1, dx: 0, dy: 0 }] },
    shade: { xmin: -2, xmax: 7, ymin: -2, ymax: 9, w: 320, h: 260, alt: 'the solid line y = 2x + 1 and the dashed line y = negative x + 4, with the overlap of the two shaded regions to the right of their crossing',
        poly: [[1, 3], [4, 9], [7, 9], [7, -2], [6, -2]],
        lines: [{ m: 2, b: 1, label: 'y ≤ 2x + 1', lx: 0.4, ly: 6.8, dx: 0, dy: 0 }, { m: -1, b: 4, cls: 'dash', label: 'y > −x + 4', lx: 1.2, ly: -1.3, dx: 0, dy: 0 }],
        segs: [{ x1: 3, y1: 1, x2: 3, y2: 7 }],
        points: [{ x: 3, y: 7, label: '(3, 7) counts', dx: 8, dy: 4 }],
        gdots: [{ x: 3, y: 1, label: '(3, 1) does not', dx: 10, dy: -6 }],
        labels: [{ x: 4.6, y: 4.4, text: 'solutions', dx: 0, dy: 0, cls: 'sm' }] },
    fit: { xmin: -1, xmax: 10, ymin: -2, ymax: 23, w: 320, h: 240, alt: 'four data points rising from (1, 4) to (8, 19) with the line of best fit drawn through them',
        lines: [{ m: 2.069, b: 2.19, cls: 'ln2', label: 'y ≈ 2.07x + 2.19', lx: 4.2, ly: 6.6, dx: 8, dy: 4 }],
        points: [{ x: 1, y: 4 }, { x: 3, y: 9 }, { x: 6, y: 14 }, { x: 8, y: 19 }] },
    g7: { xmin: -1, xmax: 11, ymin: -2, ymax: 20, w: 330, h: 250, grid: { step: 2, label: 4 }, alt: 'a scatterplot of the four points (2, 3), (4, 8), (7, 12), and (9, 17)',
        points: [{ x: 2, y: 3 }, { x: 4, y: 8 }, { x: 7, y: 12 }, { x: 9, y: 17 }] }
};
function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }'''

CONFIG = dict(
    out=os.path.join(SAT_DIR, 'SAT-Desmos-1-Core-Moves.html'),
    title='SAT Desmos 1: Core Moves',
    subtitle='CALCULATOR SKILLS &bull; CORE MOVES',
    footer='SAT Desmos Series: Core Moves',
    tab1='1. Core Moves', tab1_h2='Core moves',
    key='sat-desmos-1-sheet',
    RULES=RULES, STEPS=STEPS, FLUENCY=FLUENCY, GAUNTLET=GAUNTLET, CHALLENGE=CHALLENGE, EXIT=EXIT, FIGS_JS=FIGS_JS,
    LAST_STARRED_STEP_INDEX=LAST_STARRED_STEP_INDEX,
    last_hint='That was the last starred step. The next three cover skills that come up less often.',
    bluebook_tools=True,
    tab2_intro=r'The main idea behind these skills is simple: <strong>a graph is a picture of every solution, and Desmos marks the points that matter.</strong> An intercept, a vertex, a crossing: each of these questions asks you to read one of those points, or to count them.',
    fluency_bar='There is no time limit here. Open the calculator and practice entering each expression yourself. Building comfort with the input is part of the goal. You can enter fractions as 7/3 or 2.333; both are accepted.',
    tab4_intro=r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and one includes a scatterplot to read. A <strong>&#9733; starred move</strong> chip means the question uses one of the starred moves from tab 1. Before you compute, identify the question type, then decide whether Desmos or algebra makes more sense. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. The calculator starts blank, as it will on test day, so type each line yourself. After you finish and score the set, each solution shows the lines to type, with a <em>Load into Desmos</em> button so you can compare them with your own.',
    tab5_intro=r'These six questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each is a move you already have, paired with a second idea (a fraction on every term, a variable on both sides of an absolute value, a sideways shift, a solution that algebra invents and the graph never shows, a line that just touches, a region with a corner). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred move</strong> use the essential moves; the one marked <em>extra</em> leans on an unstarred move.',
    exit_prompt='Write one sentence you can use the next time you open the calculator. Make it an if-then. (Shape: “When a question gives me two equations, I ______ before I do any algebra.”)',
    exit_links=('<p style="font-size:14px; margin-top:10px;"><strong>Practice in the College Board version of Desmos.</strong> Desmos publishes this version of its graphing calculator, and the examples on this sheet were checked there. <a href="' + CB_DESMOS + '" ' + A_STYLE + '>Open the College Board version of Desmos &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">For skill-by-skill practice, <strong>Khan Academy\'s Official Digital SAT Prep</strong> sorts questions by topic: the units on <em>systems of linear equations</em>, <em>linear inequalities</em>, and <em>nonlinear functions</em> are good places to use these moves. <a href="https://www.khanacademy.org/digital-sat" ' + A_STYLE + '>Open Khan Academy &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">The algebra behind these moves is in <a href="' + LINEAR_URL + '" ' + A_STYLE + '>SAT Math 1: Linear Equations &#8594;</a> and <a href="' + QUAD_URL + '" ' + A_STYLE + '>SAT Math 2: Quadratics &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">Ready for the tilde? Continue the series with <a href="' + SITE + 'test-prep/sat/SAT-Desmos-2-Next-Steps.html" ' + A_STYLE + '>SAT Desmos 2: Next Steps &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">For mixed practice on the moves from both guides, including a timed set, go to <a href="' + SITE + 'test-prep/sat/SAT-Desmos-3-Mixed-Practice.html" ' + A_STYLE + '>SAT Desmos 3: Mixed Practice &#8594;</a></p>'),
)

if __name__ == '__main__':
    build(CONFIG)
