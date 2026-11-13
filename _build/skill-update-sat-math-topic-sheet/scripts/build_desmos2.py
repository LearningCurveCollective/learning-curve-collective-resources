#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Desmos-2-Next-Steps.html. Content only; desmos_common.build() does the assembly.
Every Desmos output quoted here (fitted constants, RMSE, error messages) was read from the
College Board version of the Desmos graphing calculator on 2026-11-11."""
import os
from desmos_common import build, dz, kbd, table, window, slider, DEGREES, SITE, SAT_DIR
from build_desmos1 import move, frow, ex, note, trap, A_STYLE, CB_DESMOS, QUAD_URL

FUNC_URL = SITE + 'test-prep/sat/SAT-Math-3-Functions.html'
RMSE0 = r'\text{RMSE} = 0'

# ---------------------------------------------------------------- TAB 1: MOVES
RULES = r'''
<p class="ref-intro">SAT Desmos 1 covered what a graph can show you. This guide is built around one symbol that works differently: the tilde. Type an equation with a tilde ($\sim$) where the equals sign would go, and Desmos looks for values of the unknown constants that make the two sides match as closely as possible. That can shorten several kinds of later-module questions (a function through given points, a system written in other letters, an identity that holds for all values of $x$) to two or three lines of typing. These skills also have limits, so this guide shows what to check under each tilde line before you use a result, and when algebra is the simpler choice. The outputs shown here were read from the College Board version of Desmos. As you practice, start by identifying the question type. Then decide whether Desmos or algebra makes more sense, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the tilde skills you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred skills.</span></div>
''' + move(1, 'Use a tilde to find the constants: a function through given points', True, r'''
<p class="ref-lead">An equals sign states that two expressions are equal. With a tilde, Desmos looks for values of the unknown constants that make the expressions match as closely as possible. Define your function with letters for the constants, then enter known inputs and outputs as matching lists in square brackets.</p>
''' + dz([{'x': r'f(x) = a \cdot b^{x}'}, {'x': r'f([2, 5]) \sim [12, 96]', 'out': ['a = 3', 'b = 2'], 'stat': RMSE0}, {'x': r'f(8)', 'val': '768'}]) + r'''
<div class="fig-slot" data-fig="fitexp"></div>
<div class="fbox">
''' + frow('a line', r'$f(x) = mx + b$, with two points') +
    frow('an exponential', r'$f(x) = a \cdot b^{x}$, with two points') +
    frow('a quadratic', r'$f(x) = ax^2 + bx + c$, with three points') +
    frow('the lists', r'inputs in the first brackets, their outputs in the same order in the second') +
    frow('the letters', r'$x$ and $y$ stay variables; Desmos treats most other letters as constants to find') + r'''</div>
''' + ex('A', r'A line with $f(2) = 5$ and $f(6) = 17$: define $f(x) = mx + b$ and type $f([2, 6]) \sim [5, 17]$. Desmos reports $m = 3$ and $b = -1$, and a new line $f(10)$ shows $29$.') +
    ex('B', r'A quadratic through $(-1, 10)$, $(2, 1)$ and $(3, 6)$: define $f(x) = ax^2 + bx + c$ and type $f([-1, 2, 3]) \sim [10, 1, 6]$. Desmos reports $a = 2$, $b = -5$, $c = 3$, and $f(5)$ shows $28$.') +
    ex('C', r'A table works the same way. Enter $x_1 = 0, 1, 2, 3$ and $y_1 = 5, 10, 20, 40$, then type $y_1 \sim a \cdot b^{x_1}$. Desmos reports $a = 5$ and $b = 2$.') +
    note(r'After a fit, the letters keep their fitted values. Type $f(8)$, or $a + b$, or $3m - b$ on a new line and Desmos evaluates it.')) + \
move(2, 'Read the report before you use the values', True, r'''
<p class="ref-lead">After a tilde calculation, check the fitted values and the error information underneath. RMSE measures how far the model is from the data; an RMSE of zero (or very close to zero from rounding) indicates an exact match. If the error is larger, the result may be only an approximation. A table fit may show $R^2$ instead, which needs to be interpreted differently.</p>
''' + dz([{'x': r'2p + 3 \sim 2p + 5', 'out': ['p = 0'], 'stat': r'\text{RMSE} = 2'}]) + r'''
<div class="tbl-wrap"><table class="cases"><thead><tr><th>What you see</th><th>What it means</th><th>What to do</th></tr></thead><tbody>
<tr><td class="fname">RMSE $= 0$, or $R^2 = 1$</td><td class="">the values match what you typed exactly</td><td class="">use the values</td></tr>
<tr><td class="fname">a tiny RMSE such as $8 \times 10^{-14}$</td><td class="">zero, apart from calculator rounding</td><td class="">use the values</td></tr>
<tr><td class="fname">RMSE clearly above $0$</td><td class="">Desmos did not find an exact match: there may be no solution, or the model may have the wrong form</td><td class="">reread the question and check your setup: “no solution” may be the answer</td></tr>
<tr><td class="fname">one value, where two are possible</td><td class="">the tilde reports one solution at a time</td><td class="">graph the equation and count the solutions</td></tr>
<tr><td class="fname">values that look arbitrary</td><td class="">more than one set of values may work, and Desmos reported one</td><td class="">check whether a condition from the question is missing, and type it in</td></tr>
<tr><td class="fname">“$x$ may not be used as a regression parameter”</td><td class="">$x$ cannot be the unknown in a tilde line</td><td class="">rename the unknown, or graph the equation</td></tr>
</tbody></table></div>
''' + ex('A', r'In our check, $2p + 3 \sim 2p + 5$ reported $p = 0$ with RMSE $= 2$. No value of $p$ makes those two sides equal: the equation has no solution.') +
    ex('B', r'In our check, $p^2 - p - 12 \sim 0$ reported $p = 4$ with RMSE $= 0$. That value is correct, but it is not the whole answer: $p = -3$ works too. For “the sum of the solutions,” type $x^2 - x - 12 = 0$ and read both vertical lines.') + r'''
<div class="fig-slot" data-fig="roots"></div>
''' +
    ex('C', r'$y_1 \sim e\,x_1 + d$ looks like a line with slope $e$. Desmos reads $e$ as the number $2.718\ldots$ and fits only $d$. Choose a different letter.') +
    note(r'Take a moment to review the output before using the fitted values.')) + \
move(3, 'Use square brackets for several equations at once', True, r'''
<p class="ref-lead">Put the left sides of several equations in one pair of brackets and the right sides in another, in the same order, with a tilde between them. Desmos then looks for values that satisfy all of the equations, using the letters from the question.</p>
''' + dz([{'x': r'[2a + 3b,\ a - b] \sim [12,\ 1]', 'out': ['a = 3', 'b = 2'], 'stat': RMSE0}, {'x': r'3a - b', 'val': '7'}]) + r'''
<div class="fbox">
''' + frow('word problems', r'keep the question’s own letters: no rewriting into $x$ and $y$') +
    frow('three unknowns', r'three expressions in each pair of brackets') +
    frow('the follow-up', r'type the combination the question asks for, such as $3a - b$, on the next line') + r'''</div>
''' + ex('A', r'Adult tickets cost $\$12$ and student tickets cost $\$8$. A total of $50$ tickets sold for $\$520$. $[a + s,\ 12a + 8s] \sim [50,\ 520]$ reports $a = 30$ and $s = 20$.') +
    ex('B', r'$[a + b + c,\ a - b,\ b + c] \sim [10,\ 1,\ 7]$ reports $a = 3$, $b = 2$, $c = 5$.') +
    ex('C', r'A system already printed in $x$ and $y$ is usually quicker to graph (SAT Desmos 1, Move 3). Brackets are most helpful when the letters are not $x$ and $y$, when there are three unknowns, or when the question wants a combination of the answers.') +
    note(r'You still need to translate the question into the right equations. Desmos can handle the calculation once you have set it up.')) + \
move(4, 'Match two expressions for every $x$', True, r'''
<p class="ref-lead">“Equivalent to,” “true for all values of $x$,” and “can be rewritten in the form” all say the same thing: two expressions agree at every input. Give Desmos a short list of inputs, write both expressions with that list in place of $x$, and use a tilde to look for constants that make them agree at those inputs.</p>
''' + dz([{'x': r'x_1 = [1, 2, 3, 4, 5]'}, {'x': r'(2x_1 + 3)(x_1 - 4) \sim a x_1^2 + b x_1 + c', 'out': ['a = 2', 'b = -5', 'c = -12'], 'stat': RMSE0}]) + r'''
<div class="fbox">
''' + frow('standard form', r'$\ldots \sim a x_1^2 + b x_1 + c$') +
    frow('vertex form', r'$\ldots \sim a(x_1 - h)^2 + k$') +
    frow('an identity', r'type both sides as printed, with $x_1$ wherever the question has $x$') +
    frow('the list', r'five different inputs are usually enough for the polynomial examples here') + r'''</div>
''' + ex('A', r'$2x_1^2 + 12x_1 + 7 \sim a(x_1 - h)^2 + k$ reports $a = 2$, $h = -3$, $k = -11$. The vertex form is $2(x + 3)^2 - 11$, and the vertex is $(-3, -11)$.') +
    ex('B', r'$a(x_1 + 2) + b(x_1 - 1) \sim 5x_1 + 1$ reports $a = 2$ and $b = 3$.') +
    ex('C', r'When the question adds a condition such as $a + b = 7$, the list does not include it. Use Move 3 for the conditions instead (see Common mistake 4).') +
    note(r'For a plain “which expression is equivalent” question with four choices, graphing the choices works just as well (SAT Desmos 1, Move 6). The list is most helpful when the question asks for the value of a constant.')) + \
move(5, 'One solution, no solution: the touching condition', True, r'''
<p class="ref-lead">“Exactly one solution,” “intersect at exactly one point,” and “no real solutions” are all statements about a discriminant, $b^2 - 4ac$. A slider can help you estimate where the answer is. The tilde may give a more precise value: type the discriminant with the unknown constant still in it, set it to zero with a tilde, and read the constant.</p>
''' + dz([{'x': r'y = x^2 - 4x + c'}, {'x': r'y = 2x - 3', 'see': 'slide c: the curve and the line touch near c = 6'}], cap='See it with a slider') +
      dz([{'x': r'(-6)^2 - 4(1)(c + 3) \sim 0', 'out': ['c = 6'], 'stat': RMSE0}], cap='Calculate it with a tilde, in a blank graph') + r'''
<div class="fig-slot" data-fig="touch"></div>
<div class="fbox">
''' + frow('set them equal', r'$x^2 - 4x + c = 2x - 3$ becomes $x^2 - 6x + (c + 3) = 0$') +
    frow('exactly one', r'discriminant $= 0$') +
    frow('two / none', r'discriminant $> 0$ &nbsp;/&nbsp; discriminant $< 0$') +
    frow('two lines', r'no solution when the slopes match and the lines are different') + r'''</div>
''' + ex('A', r'$x^2 + kx + 16 = 0$ has exactly one solution when $k^2 - 64 = 0$, so $k = 8$ or $k = -8$. Read the question for which one it wants.') +
    ex('B', r'$kx - 3y = 4$ and $4x - 5y = 7$ have no solution when the slopes match. $\dfrac{k}{3} \sim \dfrac{4}{5}$ reports $k = 2.4$, a value that a slider moving in whole steps would skip.') +
    ex('C', r'$2x^2 - 4x + c = 0$ has no real solutions when $16 - 8c < 0$, so $c > 2$. Slide $c$ and watch the parabola lift off the $x$-axis as it passes $2$.') +
    note(r'The slider and the tilde answer different questions. The slider helps you see how the graph changes; the tilde helps you calculate a candidate value. Use the picture to choose the condition and the tilde to finish.')) + \
move(6, 'Curves that cross: nonlinear systems and circles', False, r'''
<p class="ref-lead">A line and a parabola, a line and a circle, a circle written in expanded form: type each equation as printed and read the dots. You can do this without completing the square.</p>
''' + dz([{'x': r'x^2 + y^2 - 6x + 4y = 12', 'see': 'click the circle: top dot (3, 3), bottom dot (3, &minus;7)'}]) + r'''
<div class="fig-row"><div class="fig-slot" data-fig="circle"></div><div class="fig-slot" data-fig="circline"></div></div>
<div class="fbox">
''' + frow('center', r'halfway between the top and bottom dots: $(3, -2)$') +
    frow('radius', r'half the distance between them: $5$') +
    frow('line and curve', r'click each crossing; the question may want a coordinate, a sum, or a count') +
    frow('ovals', r'the default window can make a circle look like an oval. The dots still show the correct coordinates') + r'''</div>
''' + ex('A', r'$y = x + 1$ and $x^2 + y^2 = 25$ cross at $(3, 4)$ and $(-4, -3)$.') +
    ex('B', r'$y = x^2 - 3$ and $y = 2x$ cross at $x = -1$ and $x = 3$. The sum of the $x$-coordinates is $2$.') +
    ex('C', r'$x^2 + y^2 + 2x - 8y = 8$ has its top dot at $(-1, 9)$, so the horizontal line $y = 9$ touches the circle at exactly one point.') +
    note(r'In our check, a clicked circle showed dots at its top and bottom, not at its sides. If a question needs the leftmost or rightmost point, find the center first and move one radius left or right.')) + \
move(7, 'Lists for statistics', False, r'''
<p class="ref-lead">Name a list once and reuse it. A frequency table becomes two lists, the values and their counts, and one line of arithmetic.</p>
''' + dz([{'x': r'v = [1, 2, 3, 4]'}, {'x': r'n = [3, 5, 8, 4]'}, {'x': r'\dfrac{\operatorname{total}(v \cdot n)}{\operatorname{total}(n)}', 'val': '2.65'}]) + r'''
<div class="fbox">
''' + frow('weighted mean', r'total of value times count, divided by the total count') +
    frow('compare spread', r'$\text{stdev}(\ldots)$ for each data set: the larger number is the more spread-out set') +
    frow('a missing value', r'$\text{mean}(8, 11, 15, 20, k) \sim 14$ finds the $k$ that makes the mean $14$') + r'''</div>
''' + ex('A', r'$\text{stdev}(10, 12, 14, 16, 18) \approx 3.16$ and $\text{stdev}(6, 10, 14, 18, 22) \approx 6.32$. Both sets have mean $14$; the second is more spread out.') +
    ex('B', r'$\text{mean}(8, 11, 15, 20, k) \sim 14$ reports $k = 16$.') +
    note(r'For SAT questions that compare spread, focus on which data set is more variable rather than calculating standard deviation by hand. When the data are listed, Desmos can confirm the comparison. When they are drawn as dot plots, compare how far the dots sit from the center.')) + \
move(8, 'Degree mode for trigonometry', False, r'''
<p class="ref-lead">Desmos starts in radians, and many SAT triangle questions use degrees. Open the wrench at the top right of the graph and choose Degrees before you enter a trig expression in degrees.</p>
''' + dz([{'x': r'\sin(30)', 'see': 'radian mode (the default) shows &minus;0.988; degree mode shows 0.5'}]) + r'''
<div class="fbox">
''' + frow('switch', r'wrench, then Degrees, at the bottom of the menu') +
    frow('a side', r'$15 \sin(28)$ shows $7.042$') +
    frow('an angle', r'$\arcsin(0.5)$ shows $30$') +
    frow('radians', r'when a question is in radians, switch back and type ' + kbd('pi') + r' for $\pi$') + r'''</div>
''' + ex('A', r'A right triangle has a $28^\circ$ angle and a hypotenuse of $15$. The side opposite that angle is $15 \sin(28^\circ) \approx 7.04$.') +
    ex('B', r'$\sin(58^\circ)$ and $\cos(32^\circ)$ both show $0.848$: sine and cosine trade places at complementary angles. Knowing that relationship can be quicker than typing it.') +
    note(r'The current mode is shown only in the wrench menu. If a trig answer looks unexpected, check there first.')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These common mistakes can produce results that look reasonable at first. Practice spotting these now so they are easier to catch on test day.</p>
''' + trap(1, r'naming a constant $e$, or solving for $x$', r'Desmos reads $e$ as $2.718\ldots$ and does not fit it. It also does not accept $x$ as the unknown in a tilde line. Use letters such as $a$, $b$, $k$, $m$, $p$.') + \
      trap(2, r'taking the tilde’s one answer when there are two', r'In our check, $p^2 - p - 12 \sim 0$ reported only $p = 4$. When an equation could have two solutions, graph it and count.') + \
      trap(3, r'trusting a fit whose RMSE is not zero', r'$2p + 3 \sim 2p + 5$ still prints a value, $p = 0$. An RMSE of $2$ shows that the displayed value does not satisfy the equation.') + \
      trap(4, r'leaving out a condition', r'$(ax + 2)(bx + 5) = 12x^2 + cx + 10$ with $a + b = 7$: in our check, a list fit without $a + b = 7$ reported $a = 12$, $b = 1$, $c = 62$. Those values satisfy the identity but not the condition. Include each condition the question gives.') + \
      trap(5, r'radians when the question is in degrees', r'$\sin(30)$ is $0.5$ in degrees and $-0.988$ in radians. Check the mode in the wrench menu before you enter a trig expression.') + \
      trap(6, r'typing $=$ where the tilde belongs', r'$f([2, 5]) = [12, 96]$ with an equals sign answers “Too many variables.” Use the tilde to ask Desmos to fit the unknown constants.') + \
      trap(7, r'using Desmos when a short algebra solution is simpler', r'$3x + 7 = 22$ is two steps by hand. And no calculator move can say what a number means: “what does $1.04$ represent in $P = 250(1.04)^t$” is answered by reading the structure.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Move 1: Use a tilde to find the constants",
  "rule": r"define $f$ with letters for its constants &nbsp;·&nbsp; $f([\text{inputs}]) \sim [\text{outputs}]$ &nbsp;·&nbsp; then evaluate",
  "say": r"A tilde fits this question type well: the form of a function is given, its constants are unknown, and you know two points. By hand you would divide two equations to find $b$, substitute back to find $a$, and then evaluate. In Desmos you define the function, enter the points, and evaluate. That takes three lines.",
  "prob": r"The function $f$ is defined by $f(x) = a \cdot b^{x}$, where $a$ and $b$ are positive constants. If $f(2) = 12$ and $f(5) = 96$, what is the value of $f(8)$?",
  "sol": r"<strong>Step 1: describe, fit, evaluate.</strong>" + dz([{'x': r'f(x) = a \cdot b^{x}'}, {'x': r'f([2, 5]) \sim [12, 96]', 'out': ['a = 3', 'b = 2'], 'stat': RMSE0}, {'x': r'f(8)', 'val': '768'}]) +
         r"<strong>Step 2: read the report.</strong> RMSE is $0$, so $a = 3$ and $b = 2$ fit both points exactly, and $f(8) = 768$.<br><strong>Check:</strong> $\tfrac{96}{12} = 8 = b^3$ gives $b = 2$; then $a \cdot 4 = 12$ gives $a = 3$; and $3 \cdot 2^8 = 768$. ✓",
  "trap": r"Typing an equals sign in line 2. Entered as $f([2, 5]) = [12, 96]$, Desmos answers “Too many variables.” Use the tilde to ask Desmos to fit the unknown constants.",
  "desmos": [r"f(x)=a\cdot b^{x}", r"f([2,5])\sim[12,96]", "f(8)"],
  "micro": {"q": r"The function $f$ is linear, with $f(3) = 7$ and $f(9) = 25$. Define $f(x) = mx + b$, fit it with a tilde, and evaluate: $f(12) =$", "accept": ["34"],
            "exp": r"$f([3, 9]) \sim [7, 25]$ reports $m = 3$ and $b = -2$, and $f(12)$ shows $34$."}},
 {"ess": True, "name": "Move 1, continued: Three points for a quadratic",
  "rule": r"$f(x) = ax^2 + bx + c$ &nbsp;·&nbsp; three points pin down three constants",
  "say": r"A quadratic has three constants, so it takes three points. The table in a question like this one gives you the two lists Desmos needs: the top row goes in the first brackets and the bottom row goes in the second, in the same order.",
  "prob": r"The table shows three values of the quadratic function $f$.<table class='vtab'><tr><th>$x$</th><td>$0$</td><td>$2$</td><td>$5$</td></tr><tr><th>$f(x)$</th><td>$7$</td><td>$-1$</td><td>$2$</td></tr></table>What is the value of $f(8)$?",
  "sol": r"<strong>Step 1: describe, fit, evaluate.</strong>" + dz([{'x': r'f(x) = ax^2 + bx + c'}, {'x': r'f([0, 2, 5]) \sim [7, -1, 2]', 'out': ['a = 1', 'b = -6', 'c = 7'], 'stat': RMSE0}, {'x': r'f(8)', 'val': '23'}]) +
         r"<strong>Step 2: confirm one row.</strong> $f(x) = x^2 - 6x + 7$, and $f(5) = 25 - 30 + 7 = 2$. ✓ So $f(8) = 64 - 48 + 7 = 23$.",
  "trap": r"Entering the lists out of order. The outputs need to be in the same positions as their inputs: $[0, 2, 5]$ pairs with $[7, -1, 2]$. If two outputs are swapped, Desmos fits a different parabola and shows no warning.",
  "desmos": ["f(x)=ax^2+bx+c", r"f([0,2,5])\sim[7,-1,2]", "f(8)"],
  "micro": {"q": r"A quadratic function $f$ passes through $(1, 2)$, $(2, 3)$ and $(4, 11)$. Fit $f(x) = ax^2 + bx + c$. Then $f(0) =$", "accept": ["3"],
            "exp": r"Desmos reports $a = 1$, $b = -2$, $c = 3$, so $f(0) = 3$. The $y$-intercept of a quadratic is its constant $c$."}},
 {"ess": True, "name": "Move 2: Read the report",
  "rule": r"RMSE $= 0$: an exact match &nbsp;·&nbsp; RMSE above $0$: not an exact match &nbsp;·&nbsp; the tilde reports one solution, even when there are two",
  "say": r"A tilde line usually reports a value, so it is worth checking what that value means. On a quadratic, the tilde reports one solution and does not indicate whether there is another. If an equation could have two solutions, graphing is the better choice: type the equation itself in $x$, and Desmos draws a vertical line at each solution.",
  "prob": r"What is the sum of the solutions to the equation $x^2 - x - 12 = 0$?",
  "sol": r"<strong>What the tilde does here.</strong>" + dz([{'x': r'p^2 - p - 12 \sim 0', 'out': ['p = 4'], 'stat': RMSE0}], cap='With a tilde') +
         r"One value, with no indication that another exists.<br><strong>A better choice: graph the equation.</strong>" + dz([{'x': r'x^2 - x - 12 = 0', 'see': 'vertical lines at x = &minus;3 and x = 4'}]) +
         r"The solutions are $-3$ and $4$, and their sum is $1$.<br><strong>Check:</strong> $(x - 4)(x + 3) = 0$. ✓",
  "trap": r"Entering $4$. It is a correct solution with an RMSE of $0$, and it is only one of the two. An RMSE of zero means “this value works,” not “this is the only value that works.”",
  "desmos": [r"p^2-p-12\sim 0", "x^2-x-12=0"],
  "micro": {"mc": True, "q": r"For the line $2p + 3 \sim 2p + 5$, Desmos reports $p = 0$ and RMSE $= 2$. The equation $2p + 3 = 2p + 5$ has",
            "opts": ["exactly one solution, $p = 0$", "no solution", "infinitely many solutions", "exactly two solutions"], "correct": 1,
            "exp": r"The RMSE is above zero, so the reported value does not make the two sides equal: $p = 0$ gives $3$ on the left and $5$ on the right. Subtracting $2p$ from both sides leaves $3 = 5$, which is false for every $p$. No solution."}},
 {"ess": True, "name": "Move 3: Square brackets for a system",
  "rule": r"$[\text{left sides}] \sim [\text{right sides}]$ &nbsp;·&nbsp; any letters, same order",
  "say": r"A word problem with two unknowns is a system in disguise, and its natural letters are rarely $x$ and $y$. Write one equation per fact, using letters that mean something, then stack the left sides in one pair of brackets and the right sides in another.",
  "prob": r"A theater sold $50$ tickets for a total of $\$520$. Adult tickets cost $\$12$ each and student tickets cost $\$8$ each. How many adult tickets were sold?",
  "sol": r"<strong>Step 1: one equation per fact.</strong> With $a$ adult tickets and $s$ student tickets: $a + s = 50$ and $12a + 8s = 520$.<br><strong>Step 2: brackets.</strong>" + dz([{'x': r'[a + s,\ 12a + 8s] \sim [50,\ 520]', 'out': ['a = 30', 's = 20'], 'stat': RMSE0}]) +
         r"<strong>Step 3: answer what was asked.</strong> $30$ adult tickets.<br><strong>Check:</strong> $30 + 20 = 50$ and $12(30) + 8(20) = 360 + 160 = 520$. ✓",
  "trap": r"Entering $20$, the number of student tickets. Desmos reports both values side by side; the question asked for one of them. Choosing letters that match the words, $a$ for adult, makes this slip easier to avoid.",
  "desmos": [r"[a+s,12a+8s]\sim[50,520]"],
  "micro": {"q": r"Type $[3a + 2b,\ a - b] \sim [19,\ 3]$, then $a + b$ on the next line. Desmos shows $a + b =$", "accept": ["7"],
            "exp": r"The fit reports $a = 5$ and $b = 2$, so $a + b = 7$."}},
 {"ess": True, "name": "Move 4: Match two expressions for every $x$",
  "rule": r"$x_1 = [1, 2, 3, 4, 5]$ &nbsp;·&nbsp; type both sides with $x_1$ for $x$ and a tilde between",
  "say": r"“True for all values of $x$” means the two sides are the same expression, so they agree at every input you try. That is something Desmos can test: give it five inputs at once, and ask which constants make the two sides agree at all five. Use $x_1$, not $x$, so Desmos treats the inputs as a list of numbers.",
  "prob": r"$$(ax + 3)(2x - 5) = 8x^2 + bx - 15$$ In the equation above, $a$ and $b$ are constants. If the equation is true for all values of $x$, what is the value of $a + b$?",
  "sol": r"<strong>Step 1: a list of inputs, then both sides.</strong>" + dz([{'x': r'x_1 = [1, 2, 3, 4, 5]'}, {'x': r'(a x_1 + 3)(2x_1 - 5) \sim 8x_1^2 + b x_1 - 15', 'out': ['a = 4', 'b = -14'], 'stat': RMSE0}, {'x': r'a + b', 'val': '-10'}]) +
         r"<strong>Step 2: confirm by expanding.</strong> $(ax + 3)(2x - 5) = 2a\,x^2 + (6 - 5a)\,x - 15$. Matching $x^2$ terms: $2a = 8$, so $a = 4$. Matching $x$ terms: $b = 6 - 20 = -14$. So $a + b = -10$. ✓",
  "trap": r"Typing the identity with $x$ in place of $x_1$. Desmos then answers “$x$ may not be used as a regression parameter.” The list $x_1$ is what turns “for all $x$” into something it can check.",
  "desmos": ["x_{1}=[1,2,3,4,5]", r"(ax_{1}+3)(2x_{1}-5)\sim 8x_{1}^{2}+bx_{1}-15", "a+b"],
  "micro": {"q": r"$x^2 + 8x + 3 = (x - h)^2 + k$ for all values of $x$. With the list $x_1$ and a tilde, Desmos reports $k =$", "accept": ["-13"],
            "exp": r"$x_1^2 + 8x_1 + 3 \sim (x_1 - h)^2 + k$ reports $h = -4$ and $k = -13$: the vertex form is $(x + 4)^2 - 13$."}},
 {"ess": True, "name": "Move 5: The touching condition",
  "rule": r"exactly one intersection &nbsp;means&nbsp; discriminant $= 0$ &nbsp;·&nbsp; slider to see it, tilde to calculate it",
  "say": r"When a line and a parabola meet at exactly one point, the line is just touching the curve. Set the two equations equal, collect everything on one side, and the resulting quadratic must have exactly one solution: its discriminant is zero. A slider lets you watch the two crossings merge. The tilde, applied to the discriminant, calculates the constant.",
  "prob": r"$$y = x^2 - 4x + c$$ $$y = 2x - 3$$ In the system of equations above, $c$ is a constant. The graphs of the two equations intersect at exactly one point. What is the value of $c$?",
  "sol": r"<strong>Step 1: see it.</strong> Type both equations, add the slider for $c$, and slide until the two crossings merge: near $c = 6$.<br><strong>Step 2: set them equal.</strong> $x^2 - 4x + c = 2x - 3$ becomes $x^2 - 6x + (c + 3) = 0$.<br><strong>Step 3: discriminant zero, with a tilde.</strong>" + dz([{'x': r'(-6)^2 - 4(1)(c + 3) \sim 0', 'out': ['c = 6'], 'stat': RMSE0}], cap='In a blank graph') +
         r"<strong>Check:</strong> with $c = 6$ the equation is $x^2 - 6x + 9 = (x - 3)^2 = 0$: one solution, at $(3, 3)$. ✓",
  "trap": r"Forgetting to move the line's terms across. The discriminant belongs to $x^2 - 6x + (c + 3)$, not to the original parabola. Using $(-4)^2 - 4c = 0$ gives $c = 4$, the value that makes the parabola touch the $x$-axis. That is a different question.",
  "desmos": ["y=x^2-4x+c", "y=2x-3", slider('c', 0, -10, 10, 1)],
  "micro": {"q": r"The equation $x^2 + kx + 16 = 0$ has exactly one real solution. The positive value of $k$ is", "accept": ["8"],
            "exp": r"$k^2 - 4(1)(16) = 0$ gives $k = 8$ or $k = -8$. The question asks for the positive one."}},
 {"ess": False, "name": "Move 6: A circle in expanded form",
  "rule": r"type the circle as printed &nbsp;·&nbsp; center: halfway between the top and bottom dots &nbsp;·&nbsp; radius: half the distance",
  "say": r"By hand, a circle in expanded form means completing the square twice. In Desmos it means typing the equation and clicking the curve. The dots at the top and bottom of the circle sit directly above and below the center, one radius away in each direction.",
  "prob": r"$$x^2 + y^2 - 6x + 4y = 12$$ The equation above defines a circle in the $xy$-plane. What is the radius of the circle?",
  "sol": r"<strong>Step 1: type it and click the circle.</strong>" + dz([{'x': r'x^2 + y^2 - 6x + 4y = 12', 'see': 'top dot (3, 3), bottom dot (3, &minus;7)'}]) +
         r"<strong>Step 2: halve the distance.</strong> From $y = -7$ up to $y = 3$ is $10$, so the radius is $5$ (and the center is $(3, -2)$).<br><strong>Check:</strong> completing the square gives $(x - 3)^2 + (y + 2)^2 = 25$. ✓",
  "trap": r"Answering $10$, the full distance from bottom to top, which is the diameter. A second common mistake: taking $\sqrt{12}$ straight from the right side. In expanded form the $12$ is not $r^2$.",
  "desmos": ["x^2+y^2-6x+4y=12", window(-9, 15, -9, 5)],
  "micro": {"q": r"The line $y = x + 1$ and the circle $x^2 + y^2 = 25$ cross at two points. The larger of the two $x$-coordinates is", "accept": ["3"],
            "exp": r"The crossings are $(3, 4)$ and $(-4, -3)$. Check: $3^2 + 4^2 = 25$. ✓"}},
 {"ess": False, "name": "Move 7: A frequency table",
  "rule": r"two lists, values and counts &nbsp;·&nbsp; mean $= \dfrac{\text{total}(v \cdot n)}{\text{total}(n)}$",
  "say": r"A frequency table hides a long list: the value $1$ three times, the value $2$ five times, and so on. You could type all twenty numbers into $\text{mean}$. It is quicker, and safer, to type the two rows of the table as two lists and let Desmos weight each value by its count.",
  "prob": r"The table shows how many books each of $20$ students read last month.<table class='vtab'><tr><th>Books</th><td>$1$</td><td>$2$</td><td>$3$</td><td>$4$</td></tr><tr><th>Students</th><td>$3$</td><td>$5$</td><td>$8$</td><td>$4$</td></tr></table>What is the mean number of books read per student?",
  "sol": r"<strong>Step 1: two lists and one line.</strong>" + dz([{'x': r'v = [1, 2, 3, 4]'}, {'x': r'n = [3, 5, 8, 4]'}, {'x': r'\dfrac{\operatorname{total}(v \cdot n)}{\operatorname{total}(n)}', 'val': '2.65'}]) +
         r"<strong>Check:</strong> $1(3) + 2(5) + 3(8) + 4(4) = 53$ books among $20$ students, and $53 \div 20 = 2.65$. ✓",
  "trap": r"Averaging the four values, $\tfrac{1 + 2 + 3 + 4}{4} = 2.5$, as if each appeared once. The counts tell you how much weight each value gets.",
  "desmos": ["v=[1,2,3,4]", "n=[3,5,8,4]", r"\frac{\operatorname{total}(v\cdot n)}{\operatorname{total}(n)}"],
  "micro": {"q": r"The mean of the five numbers $8$, $11$, $15$, $20$ and $k$ is $14$. Type $\text{mean}(8, 11, 15, 20, k) \sim 14$. Desmos reports $k =$", "accept": ["16"],
            "exp": r"$k = 16$. Check: $8 + 11 + 15 + 20 + 16 = 70$, and $70 \div 5 = 14$. ✓"}},
 {"ess": False, "name": "Move 8: Degree mode",
  "rule": r"wrench, then Degrees &nbsp;·&nbsp; then $\sin$, $\cos$, $\tan$ as written",
  "say": r"A right-triangle question may give an angle in degrees and one side, and ask for another side. Start with the setup: decide which ratio connects the side you know to the side you want. The calculation is one line in Desmos, as long as the calculator is in degree mode. It starts in radians.",
  "prob": r"In right triangle $ABC$, angle $C$ is the right angle, the measure of angle $A$ is $28^\circ$, and the length of hypotenuse $AB$ is $15$. To the nearest tenth, what is the length of side $BC$?",
  "sol": r"<strong>Step 1: choose the ratio.</strong> $BC$ is opposite angle $A$, and $AB$ is the hypotenuse: $\sin(28^\circ) = \dfrac{BC}{15}$, so $BC = 15 \sin(28^\circ)$.<br><strong>Step 2: degree mode, then one line.</strong>" + dz([{'x': r'15 \sin(28)', 'val': '7.042'}], cap='In degree mode') +
         r"To the nearest tenth, $BC = 7.0$.",
  "trap": r"Leaving the calculator in radian mode. The same line shows $4.06$ in radians, a plausible-looking length that is not correct. If the angle in the question has a degree symbol, set the wrench menu to Degrees.",
  "desmos": [DEGREES, r"15\sin(28)"],
  "micro": {"mc": True, "q": r"You type $\sin(30)$ and Desmos shows $-0.988$. What happened?",
            "opts": ["The sine of $30^\\circ$ is negative", "The calculator is in radian mode", "Sine needs two inputs", "The keypad is set to scientific"], "correct": 1,
            "exp": r"$-0.988$ is the sine of $30$ radians. Open the wrench and switch to Degrees: the same line then shows $0.5$."}},
]
LAST_STARRED_STEP_INDEX = 5

# ---------------------------------------------------------------- TAB 3: FLUENCY
FLUENCY = [
 {"sec": "A. The tilde with points", "items": [
   {"q": r"$f(x) = mx + b$ with $f(1) = 4$ and $f(5) = 16$. Desmos reports $m =$", "accept": ["3"], "exp": r"$f([1, 5]) \sim [4, 16]$ reports $m = 3$ and $b = 1$."},
   {"q": r"$f(x) = a \cdot b^{x}$ with $f(1) = 6$ and $f(3) = 54$. Then $f(4) =$", "accept": ["162"], "exp": r"The fit reports $a = 2$ and $b = 3$, and $f(4) = 2 \cdot 81 = 162$."},
   {"q": r"$f(x) = ax^2 + bx + c$ passes through $(0, 1)$, $(1, 0)$ and $(3, 10)$. Desmos reports $a =$", "accept": ["2"], "exp": r"$f([0, 1, 3]) \sim [1, 0, 10]$ reports $a = 2$, $b = -3$, $c = 1$."},
   {"q": r"A table has $x_1 = 0, 1, 2, 3$ and $y_1 = 4, 12, 36, 108$. Type $y_1 \sim a \cdot b^{x_1}$. Desmos reports $b =$", "accept": ["3"], "exp": r"$a = 4$ and $b = 3$: each step multiplies the output by $3$."},
 ]},
 {"sec": "B. Brackets and identities", "items": [
   {"q": r"$[2a + b,\ a - b] \sim [11,\ 1]$ reports $a =$", "accept": ["4"], "exp": r"$a = 4$ and $b = 3$. Check: $8 + 3 = 11$ and $4 - 3 = 1$."},
   {"q": r"Five pencils and two notebooks cost $\$9.50$. Three pencils and four notebooks cost $\$13.40$. In dollars, one notebook costs", "accept": ["2.75", "11/4"], "exp": r"$[5p + 2n,\ 3p + 4n] \sim [9.5,\ 13.4]$ reports $p = 0.8$ and $n = 2.75$."},
   {"q": r"$(3x - 2)(x + 5) = ax^2 + bx + c$ for all values of $x$. The value of $b$ is", "accept": ["13"], "exp": r"With $x_1 = [1, 2, 3, 4, 5]$, the fit reports $a = 3$, $b = 13$, $c = -10$."},
   {"q": r"$x^2 - 10x + 31 = (x - h)^2 + k$ for all values of $x$. The value of $k$ is", "accept": ["6"], "exp": r"The fit reports $h = 5$ and $k = 6$: the vertex form is $(x - 5)^2 + 6$."},
 ]},
 {"sec": "C. Touching, circles, lists", "items": [
   {"q": r"$x^2 + 10x + c = 0$ has exactly one real solution when $c =$", "accept": ["25"], "exp": r"$10^2 - 4c \sim 0$ reports $c = 25$: the equation is $(x + 5)^2 = 0$."},
   {"q": r"Graph $x^2 + y^2 + 8x - 2y = 19$ and click the circle. Its radius is", "accept": ["6"], "exp": r"Top dot $(-4, 7)$, bottom dot $(-4, -5)$: the distance is $12$, so the radius is $6$."},
   {"q": r"The parabola $y = x^2 - 5$ and the line $y = x + 1$ cross at two points. The sum of the $x$-coordinates of those points is", "accept": ["1"], "exp": r"They cross at $x = -2$ and $x = 3$. The sum is $1$."},
   {"q": r"The values $2$, $4$ and $6$ occur $5$, $3$ and $2$ times. The mean of the data is", "accept": ["3.4", "17/5"], "exp": r"$\dfrac{2(5) + 4(3) + 6(2)}{10} = \dfrac{34}{10} = 3.4$."},
 ]},
 {"sec": "D. Desmos or algebra? Choose an approach", "items": [
   {"mc": True, "q": r"Solve $3x + 7 = 22$.", "opts": ["A tilde with square brackets", "A table and a tilde", "Algebra: subtract, then divide", "A slider"], "correct": 2,
    "exp": r"Two short steps by hand give $x = 5$. Algebra is the simpler choice here."},
   {"mc": True, "q": r"A quadratic function passes through $(0, 4)$, $(2, 6)$ and $(5, 39)$. Find $f(3)$.", "opts": ["Algebra: guess and check", r"Define $f(x) = ax^2 + bx + c$, then a tilde with lists", "A slider for each constant", "Degree mode"], "correct": 1,
    "exp": r"Three unknown constants by hand is a three-equation system. The tilde reports $a = 2$, $b = -3$, $c = 4$, and $f(3)$ shows $13$."},
   {"mc": True, "q": r"For what value of $k$ does the system $3x + ky = 8$ and $6x - 10y = 5$ have no solution?", "opts": [r"Match the coefficients: $\tfrac{3}{6} = \tfrac{k}{-10}$", "A table and a tilde", "Square brackets with three unknowns", "Degree mode"], "correct": 0,
    "exp": r"One proportion gives $k = -5$. A slider works too, but the ratio is a single line of algebra."},
   {"mc": True, "q": r"In the model $P = 250(1.04)^t$, what does the number $1.04$ represent?", "opts": ["Graph it and click the $y$-intercept", "A tilde with lists", "A slider for $t$", "Read the structure: no calculator move interprets a constant"], "correct": 3,
    "exp": r"$1.04$ is the growth factor: the quantity grows by $4\%$ each time $t$ increases by $1$. Desmos can draw the curve, but meaning comes from reading the form."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE
GAUNTLET = [
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"The function $f$ is linear, with $f(2) = 9$ and $f(6) = 21$. What is the value of $f(10)$?",
  "label": "$f(10) =$", "accept": ["33"], "desmos": ["f(x)=mx+b", r"f([2,6])\sim[9,21]", "f(10)"],
  "sol": r"<strong>Given:</strong> a linear function and two of its points.<br><br>" + dz([{'x': r'f(x) = mx + b'}, {'x': r'f([2, 6]) \sim [9, 21]', 'out': ['m = 3', 'b = 3'], 'stat': RMSE0}, {'x': r'f(10)', 'val': '33'}]) + r"Algebra is just as quick here: the output rises $12$ for every $4$ units of input, so $f(10) = 21 + 12 = 33$. ✓",
  "trap": r"Pairing the lists the wrong way round. Inputs go in the first brackets, outputs in the second: $f([2, 6]) \sim [9, 21]$."},
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"At a bakery, $3$ muffins and $2$ coffees cost $\$16.50$, and $1$ muffin and $4$ coffees cost $\$15.50$. What is the price of one muffin?",
  "options": [r"$\$3.00$", r"$\$3.25$", r"$\$3.50$", r"$\$4.00$"], "correct": 2, "desmos": [r"[3m+2c,m+4c]\sim[16.5,15.5]"],
  "sol": r"<strong>Given:</strong> two purchases, two unknown prices.<br><br>" + dz([{'x': r'[3m + 2c,\ m + 4c] \sim [16.5,\ 15.5]', 'out': ['m = 3.5', 'c = 3'], 'stat': RMSE0}]) + r"A muffin costs $\$3.50$: choice C. Check: $3(3.50) + 2(3) = 16.50$ and $3.50 + 4(3) = 15.50$. ✓",
  "trap": r"Choice A is the price of a coffee. Desmos reports both values; the question asks for the muffin."},
 {"ess": True, "type": "ne", "diff": "Easy to medium",
  "stem": r"The function $f$ is defined by $f(x) = a \cdot b^{x}$, where $a$ and $b$ are positive constants. If $f(1) = 10$ and $f(3) = 40$, what is the value of $f(6)$?",
  "label": "$f(6) =$", "accept": ["320"], "desmos": [r"f(x)=a\cdot b^{x}", r"f([1,3])\sim[10,40]", "f(6)"],
  "sol": r"<strong>Given:</strong> an exponential form and two points.<br><br>" + dz([{'x': r'f(x) = a \cdot b^{x}'}, {'x': r'f([1, 3]) \sim [10, 40]', 'out': ['a = 5', 'b = 2'], 'stat': RMSE0}, {'x': r'f(6)', 'val': '320'}]) + r"Check: $b^2 = \tfrac{40}{10} = 4$, so $b = 2$ and $a = 5$; $5 \cdot 2^6 = 320$. ✓",
  "trap": r"Treating the function as linear. From $x = 1$ to $x = 3$ the output multiplied by $4$; it did not rise by a fixed amount. A line through the same two points would give $f(6) = 85$."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"Which of the following is equivalent to $2x^2 - 12x + 7$?",
  "options": [r"$2(x - 3)^2 - 11$", r"$2(x - 3)^2 + 7$", r"$2(x - 6)^2 - 11$", r"$2(x - 3)^2 - 2$"], "correct": 0,
  "desmos": ["x_{1}=[1,2,3,4,5]", r"2x_{1}^{2}-12x_{1}+7\sim a(x_{1}-h)^{2}+k"],
  "sol": r"<strong>Given:</strong> a quadratic to rewrite in vertex form.<br><br>" + dz([{'x': r'x_1 = [1, 2, 3, 4, 5]'}, {'x': r'2x_1^2 - 12x_1 + 7 \sim a(x_1 - h)^2 + k', 'out': ['a = 2', 'h = 3', 'k = -11'], 'stat': RMSE0}]) + r"Vertex form: $2(x - 3)^2 - 11$, choice A. Check: $2(x^2 - 6x + 9) - 11 = 2x^2 - 12x + 7$. ✓ Graphing the original with each choice works just as well.",
  "trap": r"Choice B keeps the $7$ and forgets that completing the square pulls $2 \cdot 9 = 18$ out of it. Choice C halves nothing: the $-12$ must be divided by the leading $2$ before it is halved."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"$$(2x + a)(3x - 4) = 6x^2 + bx - 20$$ In the equation above, $a$ and $b$ are constants. If the equation is true for all values of $x$, what is the value of $b$?",
  "label": "$b =$", "accept": ["7"], "desmos": ["x_{1}=[1,2,3,4,5]", r"(2x_{1}+a)(3x_{1}-4)\sim 6x_{1}^{2}+bx_{1}-20"],
  "sol": r"<strong>Given:</strong> an identity with two unknown constants.<br><br>" + dz([{'x': r'x_1 = [1, 2, 3, 4, 5]'}, {'x': r'(2x_1 + a)(3x_1 - 4) \sim 6x_1^2 + b x_1 - 20', 'out': ['a = 5', 'b = 7'], 'stat': RMSE0}]) + r"Check by expanding: the constant term is $-4a = -20$, so $a = 5$; the $x$ term is $(-8 + 3a)x = 7x$. ✓",
  "trap": r"Stopping at $a = 5$. The question asks for $b$, the coefficient of $x$, which needs both the outer and the inner products: $-8 + 15$."},
 {"ess": False, "type": "mc", "diff": "Medium",
  "stem": r"$$x^2 + y^2 + 4x - 10y = 20$$ The equation above defines a circle in the $xy$-plane. What are the coordinates of the center of the circle?",
  "options": [r"$(2, -5)$", r"$(-2, 5)$", r"$(4, -10)$", r"$(-4, 10)$"], "correct": 1, "desmos": ["x^2+y^2+4x-10y=20", window(-16, 12, -4, 14)],
  "sol": r"<strong>Given:</strong> a circle in expanded form.<br><br>" + dz([{'x': r'x^2 + y^2 + 4x - 10y = 20', 'see': 'top dot (&minus;2, 12), bottom dot (&minus;2, &minus;2)'}]) + r"The center is halfway between: $(-2, 5)$, choice B. Check: completing the square gives $(x + 2)^2 + (y - 5)^2 = 49$. ✓",
  "trap": r"Choice A has both signs backwards: $(x + 2)^2$ puts the center at $x = -2$. Choices C and D read the coefficients $4$ and $-10$ without halving them."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"The table shows three values of the quadratic function $f$.<table class='vtab'><tr><th>$x$</th><td>$-1$</td><td>$1$</td><td>$3$</td></tr><tr><th>$f(x)$</th><td>$12$</td><td>$2$</td><td>$8$</td></tr></table>What is the value of $f(0)$?",
  "label": "$f(0) =$", "accept": ["5"], "desmos": ["f(x)=ax^2+bx+c", r"f([-1,1,3])\sim[12,2,8]", "f(0)"],
  "sol": r"<strong>Given:</strong> three points of a quadratic.<br><br>" + dz([{'x': r'f(x) = ax^2 + bx + c'}, {'x': r'f([-1, 1, 3]) \sim [12, 2, 8]', 'out': ['a = 2', 'b = -5', 'c = 5'], 'stat': RMSE0}, {'x': r'f(0)', 'val': '5'}]) + r"Check one row: $f(3) = 18 - 15 + 5 = 8$. ✓",
  "trap": r"Guessing $7$, the average of $12$ and $2$, because $0$ is halfway between $-1$ and $1$. Halfway inputs give halfway outputs only on a line. This function curves."},
 {"ess": False, "type": "mc", "diff": "Medium",
  "stem": r"Data set A consists of the values $10$, $12$, $14$, $16$, $18$. Data set B consists of the values $6$, $10$, $14$, $18$, $22$. Which of the following statements is true?",
  "options": ["The means are equal, and the standard deviations are equal.", "The mean of A is greater, and the standard deviations are equal.", "The means are equal, and the standard deviation of A is greater.", "The means are equal, and the standard deviation of B is greater."], "correct": 3,
  "desmos": [r"\operatorname{mean}(10,12,14,16,18)", r"\operatorname{mean}(6,10,14,18,22)", r"\operatorname{stdev}(10,12,14,16,18)", r"\operatorname{stdev}(6,10,14,18,22)"],
  "sol": r"<strong>Given:</strong> two small data sets to compare.<br><br>" + dz([{'x': r'\operatorname{mean}(10, 12, 14, 16, 18)', 'val': '14'}, {'x': r'\operatorname{mean}(6, 10, 14, 18, 22)', 'val': '14'}, {'x': r'\operatorname{stdev}(10, 12, 14, 16, 18)', 'val': '3.162'}, {'x': r'\operatorname{stdev}(6, 10, 14, 18, 22)', 'val': '6.325'}]) + r"Equal means; B is more spread out. Choice D. You can also see it without a calculator: both sets are centered on $14$, and B's values sit twice as far from it.",
  "trap": r"Reading “same number of values and same center” as “same spread.” Standard deviation measures distance from the mean, and B's values are farther out."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$y = 2x^2 - 4x + c$$ $$y = 4x - 3$$ In the system of equations above, $c$ is a constant. The graphs of the two equations intersect at exactly one point. What is the value of $c$?",
  "label": "$c =$", "accept": ["5"], "desmos": ["y=2x^2-4x+c", "y=4x-3", slider('c', 0, -10, 10, 1)],
  "sol": r"<strong>Given:</strong> a parabola with a constant and a line that just touches it.<br><br>Set them equal: $2x^2 - 4x + c = 4x - 3$ becomes $2x^2 - 8x + (c + 3) = 0$. One solution means the discriminant is zero." + dz([{'x': r'(-8)^2 - 4(2)(c + 3) \sim 0', 'out': ['c = 5'], 'stat': RMSE0}]) + r"Check: $2x^2 - 8x + 8 = 2(x - 2)^2$, one solution at $x = 2$. ✓",
  "trap": r"Using $a = 1$ in the discriminant. The leading coefficient here is $2$, and it multiplies the whole $4ac$ term: $4(2)(c + 3)$."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$(ax + 2)(bx + 5) = 12x^2 + cx + 10$$ In the equation above, $a$, $b$, and $c$ are constants and $a + b = 7$. If the equation is true for all values of $x$, what is one possible value of $c$?",
  "label": "$c =$", "accept": ["26", "23"], "desmos": [r"[ab,a+b]\sim[12,7]", "5a+2b"],
  "sol": r"<strong>Given:</strong> an identity plus one extra condition.<br><br>Expanding the left side gives $ab\,x^2 + (5a + 2b)\,x + 10$, so $ab = 12$ and $c = 5a + 2b$. Together with $a + b = 7$, that is a system for Move 3:" + dz([{'x': r'[ab,\ a + b] \sim [12,\ 7]', 'out': ['a = 4', 'b = 3'], 'stat': RMSE0}, {'x': r'5a + 2b', 'val': '26'}]) + r"Desmos may report the pair in either order. The other order, $a = 3$ and $b = 4$, gives $c = 15 + 8 = 23$. Either $26$ or $23$ is accepted.",
  "trap": r"Fitting the identity with a list and leaving out the condition. In our check, Desmos then reported $a = 12$, $b = 1$, $c = 62$: values that satisfy the identity but not $a + b = 7$. The tilde uses only what you type."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"The sum of three numbers is $27$. The largest number is twice the smallest, and the middle number is $3$ more than the smallest. What is the largest number?",
  "label": "Largest $=$", "accept": ["12"], "desmos": [r"[s+m+l,l-2s,m-s]\sim[27,0,3]"],
  "sol": r"<strong>Given:</strong> three facts about three unknowns.<br><br>Write each fact with everything on the left: $s + m + l = 27$, $l - 2s = 0$, $m - s = 3$." + dz([{'x': r'[s + m + l,\ l - 2s,\ m - s] \sim [27,\ 0,\ 3]', 'out': ['s = 6', 'm = 9', 'l = 12'], 'stat': RMSE0}]) + r"The largest number is $12$. Check: $6 + 9 + 12 = 27$. ✓",
  "trap": r"Say each equation aloud with numbers in mind before you type it. “The largest is twice the smallest” is $l = 2s$, because the largest is the bigger one. If it is typed backwards as $s = 2l$, Desmos solves that system instead and shows no warning."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"The function $P$ is defined by $P(t) = a \cdot b^{t}$, where $a$ and $b$ are positive constants. If $P(2) = 450$ and $P(4) = 648$, what is the value of $P(0)$?",
  "label": "$P(0) =$", "accept": ["312.5", "625/2"], "desmos": [r"f(x)=a\cdot b^{x}", r"f([2,4])\sim[450,648]", "f(0)"],
  "sol": r"<strong>Given:</strong> an exponential model and two points; the question asks for the starting value.<br><br>" + dz([{'x': r'f(x) = a \cdot b^{x}'}, {'x': r'f([2, 4]) \sim [450, 648]', 'out': ['a = 312.5', 'b = 1.2'], 'stat': RMSE0}, {'x': r'f(0)', 'val': '312.5'}]) + r"$P(0) = a = 312.5$. Check: $b^2 = \tfrac{648}{450} = 1.44$, so $b = 1.2$, and $a = \tfrac{450}{1.44} = 312.5$. ✓",
  "trap": r"An exponential function changes by a constant factor, not a constant amount. Stepping back by subtraction ($648 - 450 = 198$, then $450 - 198 = 252$) treats it as a line. Use the tilde to find $a$ and $b$, and read $P(0)$ as $a$.",
  "extrasIntro": r"Two points are enough to determine an exponential function of this form. Three more to try: define $f(x) = a \cdot b^{x}$ and use the tilde to find the constants.",
  "extras": [
   {"type": "ne", "q": r"$f(1) = 12$ and $f(2) = 18$. Then $f(3) =$", "label": "$f(3) =$", "accept": ["27"], "exp": r"The fit reports $a = 8$ and $b = 1.5$, and $f(3) = 27$."},
   {"type": "ne", "q": r"$f(0) = 80$ and $f(2) = 20$, with $b > 0$. The value of $b$ is", "label": "$b =$", "accept": ["0.5", ".5", "1/2"], "exp": r"$a = 80$ and $b = 0.5$: the output is cut in half at each step."},
   {"type": "ne", "q": r"$f(2) = 50$ and $f(5) = 400$. The value of $a$ is", "label": "$a =$", "accept": ["12.5", "25/2"], "exp": r"The fit reports $a = 12.5$ and $b = 2$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"In the $xy$-plane, the graph of the quadratic function $f$ has its vertex at $(3, -4)$ and passes through the point $(5, 8)$. What is the value of $f(0)$?",
  "label": "$f(0) =$", "accept": ["23"], "desmos": ["f(x)=a(x-3)^2-4", r"f(5)\sim 8", "f(0)"],
  "sol": r"<strong>Given:</strong> a vertex and one more point. Vertex form already holds two of the three constants.<br><br>" + dz([{'x': r'f(x) = a(x - 3)^2 - 4'}, {'x': r'f(5) \sim 8', 'out': ['a = 3'], 'stat': RMSE0}, {'x': r'f(0)', 'val': '23'}]) + r"Check: $a(5 - 3)^2 - 4 = 8$ gives $4a = 12$, so $a = 3$; $f(0) = 3(9) - 4 = 23$. ✓",
  "trap": r"Build what you know into the form before you fit. A known vertex means vertex form, which leaves one constant for one point. Starting from $ax^2 + bx + c$ with only two facts leaves Desmos free to report one of many parabolas."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"$$kx + 4y = 9$$ $$5x + 6y = 2$$ In the system of equations above, $k$ is a constant. If the system has no solution, what is the value of $k$?",
  "label": "$k =$", "accept": ["10/3", "3.333"], "desmos": ["kx+4y=9", "5x+6y=2", slider('k', 1, -10, 10, 0.5)],
  "sol": r"<strong>Given:</strong> two lines; no solution means equal slopes.<br><br>The slopes are $-\tfrac{k}{4}$ and $-\tfrac{5}{6}$. Set the ratios equal with a tilde:" + dz([{'x': r'\dfrac{k}{4} \sim \dfrac{5}{6}', 'out': ['k = 3.33333'], 'stat': RMSE0}]) + r"$k = \tfrac{10}{3}$. The lines are different (their constants do not match the same ratio), so they are parallel. Enter $10/3$ or $3.333$.",
  "trap": r"When a slider suggests the answer is between two steps, it may be a fraction, and a tilde on the slopes can calculate it. A slider moving in whole or half steps passes from $3$ to $3.5$ without stopping where the lines are parallel."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"In the $xy$-plane, the line $y = k$ is tangent to the circle $x^2 + y^2 - 4x - 6y = 12$. What is the greater of the two possible values of $k$?",
  "label": "$k =$", "accept": ["8"], "desmos": ["x^2+y^2-4x-6y=12", "y=8", window(-10, 14, -4, 10)],
  "sol": r"<strong>Given:</strong> a circle in expanded form and a horizontal tangent line.<br><br>A horizontal line touches a circle only at its very top or its very bottom, and those are the two dots Desmos marks." + dz([{'x': r'x^2 + y^2 - 4x - 6y = 12', 'see': 'top dot (2, 8), bottom dot (2, &minus;2)'}]) + r"The two tangent lines are $y = 8$ and $y = -2$. The greater value is $8$. Check: the circle is $(x - 2)^2 + (y - 3)^2 = 25$, and $3 + 5 = 8$. ✓",
  "trap": r"A horizontal tangent line touches a circle at its top or bottom point, where Desmos marks the dots. The line sits one radius above the center, at $3 + 5$, not at the radius $5$ and not at the center's height $3$."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"In right triangle $ABC$, angle $C$ is the right angle, the length of side $AC$ is $9$, and the measure of angle $A$ is $40^\circ$. To the nearest tenth, what is the length of side $BC$?",
  "label": "$BC =$", "accept": ["7.6", "7.55", "7.552"], "desmos": [DEGREES, r"9\tan(40)"],
  "sol": r"<strong>Given:</strong> an angle and the side next to it; the side across from it is wanted.<br><br>Opposite over adjacent is tangent: $\tan(40^\circ) = \dfrac{BC}{9}$, so $BC = 9 \tan(40^\circ)$." + dz([{'x': r'9 \tan(40)', 'val': '7.552'}], cap='In degree mode') + r"To the nearest tenth, $BC = 7.6$.",
  "trap": r"Choose the ratio before you open the calculator: opposite over adjacent is tangent, and $AC$ here is a leg, not the hypotenuse. Then confirm degree mode. In radians the same line shows $-10.05$, a negative length."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"Under a tilde line, Desmos shows RMSE $= 0$. That means", "opts": ["the reported values satisfy every equation exactly", "the equation has no solution", "the calculator is in radian mode", "there is exactly one solution and no other"], "correct": 0,
  "exp": r"An RMSE of zero means the reported values match exactly. It does not tell you whether they are the only values that work."},
 {"q": r"$[3a + b,\ a - b] \sim [14,\ 2]$ reports $a =$", "opts": ["$2$", "$3$", "$4$", "$6$"], "correct": 2,
  "exp": r"$a = 4$ and $b = 2$. Check: $12 + 2 = 14$ and $4 - 2 = 2$."},
 {"q": r"A question asks what the number $1.5$ means in the model $h = 1.5t + 20$. The best tool is", "opts": ["a tilde with lists", "a slider for $t$", "degree mode", "reading the equation: no calculator move interprets a constant"], "correct": 3,
  "exp": r"$1.5$ is the rate of change: $h$ rises $1.5$ for each unit of $t$. That is reading, not calculating."},
]

# ---------------------------------------------------------------- FIGURES
FIGS_JS = r'''var FIGS = {
    fitexp: { xmin: -1, xmax: 7, ymin: -12, ymax: 130, w: 330, h: 240, alt: 'the exponential curve f(x) = 3 times 2 to the x passing through the two given points (2, 12) and (5, 96)',
        curves: [{ f: function(x) { return 3 * Math.pow(2, x); }, label: 'f(x) = 3 · 2ˣ', lx: 5.2, ly: 118, dx: -100, dy: 0 }],
        points: [{ x: 2, y: 12, label: '(2, 12)', dx: -8, dy: -12 }, { x: 5, y: 96, label: '(5, 96)', dx: 10, dy: 6 }] },
    roots: { xmin: -6, xmax: 7, ymin: -3, ymax: 3, w: 320, h: 170, alt: 'two vertical lines, at x = negative 3 and x = 4, drawn by typing the equation x squared minus x minus 12 = 0',
        vlines: [{ x: -3, cls: 'ln', label: 'x = −3', dx: -46, dy: 14 }, { x: 4, cls: 'ln', label: 'x = 4', dx: 8, dy: 14 }],
        gdots: [{ x: -3, y: 0 }, { x: 4, y: 0 }] },
    touch: { xmin: -1.5, xmax: 7.5, ymin: -5, ymax: 12, w: 330, h: 270, alt: 'the line y = 2x minus 3 with two parabolas: a dashed one, for c = 3, crossing the line twice, and a solid one, for c = 6, touching it at (3, 3)',
        curves: [{ a: 1, b: -4, c: 3, cls: 'dash', label: 'c = 3: two crossings', lx: 3.3, ly: -2.4, dx: 0, dy: 0 }, { a: 1, b: -4, c: 6, label: 'c = 6: one touch', lx: 0.5, ly: 10.6, dx: 0, dy: 0 }],
        lines: [{ m: 2, b: -3, cls: 'ln2', label: 'y = 2x − 3', lx: 5.6, ly: 7.2, dx: 10, dy: 0 }],
        gdots: [{ x: 3, y: 3, label: '(3, 3)', dx: -46, dy: -4 }] },
    circle: { xmin: -4, xmax: 10, ymin: -8.5, ymax: 4.5, w: 304, h: 286, alt: 'a circle with gray dots at its top (3, 3) and bottom (3, negative 7); the center (3, negative 2) is halfway between',
        circles: [{ x: 3, y: -2, r: 5 }],
        segs: [{ x1: 3, y1: 3, x2: 3, y2: -7 }],
        points: [{ x: 3, y: -2, label: 'center (3, −2)', dx: 8, dy: 4 }],
        gdots: [{ x: 3, y: 3, label: 'top (3, 3)', dx: 9, dy: -6 }, { x: 3, y: -7, label: 'bottom (3, −7)', dx: 9, dy: 15 }],
        labels: [{ x: 3, y: 1.4, text: 'radius 5', dx: 8, dy: 4, cls: 'sm' }] },
    circline: { xmin: -7, xmax: 8.5, ymin: -6.5, ymax: 6.5, w: 354, h: 304, alt: 'the circle x squared + y squared = 25 and the line y = x + 1 crossing at (3, 4) and (negative 4, negative 3)',
        circles: [{ x: 0, y: 0, r: 5 }],
        lines: [{ m: 1, b: 1, cls: 'ln2', label: 'y = x + 1', lx: 5.2, ly: 5.2, dx: 6, dy: 4 }],
        gdots: [{ x: 3, y: 4, label: '(3, 4)', dx: 16, dy: 6 }, { x: -4, y: -3, label: '(−4, −3)', dx: -58, dy: -12 }] }
};
function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }'''

CONFIG = dict(
    out=os.path.join(SAT_DIR, 'SAT-Desmos-2-Next-Steps.html'),
    title='SAT Desmos 2: Next Steps',
    subtitle='CALCULATOR SKILLS &bull; NEXT STEPS',
    footer='SAT Desmos Series: Next Steps',
    tab1='1. Next Steps', tab1_h2='Next steps',
    key='sat-desmos-2-sheet',
    RULES=RULES, STEPS=STEPS, FLUENCY=FLUENCY, GAUNTLET=GAUNTLET, CHALLENGE=CHALLENGE, EXIT=EXIT, FIGS_JS=FIGS_JS,
    LAST_STARRED_STEP_INDEX=LAST_STARRED_STEP_INDEX,
    last_hint='That was the last starred step. The next three cover skills that come up less often.',
    bluebook_tools=False,
    tab2_intro=r'The central idea for these skills is: <strong>a tilde asks Desmos to find the constants, and the report underneath tells you whether to believe them.</strong> A function through given points, a system in any letters, an identity, a discriminant: each is the same request with different lines above it.',
    fluency_bar='There is no time limit here. Open the calculator and practice entering each expression yourself. Building comfort with the input is part of the goal. You can enter fractions as 7/3 or 2.333; both are accepted.',
    tab4_intro=r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and one includes a table to read. A <strong>&#9733; starred move</strong> chip means the question uses one of the starred moves from tab 1. Before you compute, identify the question type and decide whether Desmos or algebra makes more sense; on two or three of these, algebra may be quicker. The calculator starts blank, as it will on test day, so type each line yourself, and read the report under each tilde line. After you finish and score the set, each solution shows the lines to type, with a <em>Load into Desmos</em> button so you can compare them with your own.',
    tab5_intro=r'These six questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each is a move you already have, paired with a second idea (three unknowns from a paragraph of words, an exponential model traced back to its starting value, a vertex built into the form, an answer that is not a whole number, a tangent line read from a circle, a ratio to choose before any typing). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred move</strong> use the essential moves; the ones marked <em>extra</em> lean on the unstarred moves.',
    exit_prompt='Write one sentence you can use the next time you reach for the tilde. Make it an if-then. (Shape: “When Desmos reports a value under a tilde, I ______ before I enter it.”)',
    exit_links=('<p style="font-size:14px; margin-top:10px;"><strong>Practice in the College Board version of Desmos.</strong> Desmos publishes this version of its graphing calculator, and the outputs on this sheet were read there. <a href="' + CB_DESMOS + '" ' + A_STYLE + '>Open the College Board version of Desmos &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">For skill-by-skill practice, <strong>Khan Academy\'s Official Digital SAT Prep</strong> sorts questions by topic: the units on <em>nonlinear functions</em>, <em>equivalent expressions</em>, and <em>circles</em> are good places to use these moves. <a href="https://www.khanacademy.org/digital-sat" ' + A_STYLE + '>Open Khan Academy &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">The algebra behind these moves is in <a href="' + QUAD_URL + '" ' + A_STYLE + '>SAT Math 2: Quadratics &#8594;</a> and <a href="' + FUNC_URL + '" ' + A_STYLE + '>SAT Math 3: Functions &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">New to Desmos, or want to review the basics? Start with <a href="' + SITE + 'test-prep/sat/SAT-Desmos-1-Core-Moves.html" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>'),
)

if __name__ == '__main__':
    build(CONFIG)
