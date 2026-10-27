#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-2-Quadratics.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders) is reused; only the content swaps.
All questions use original numbers."""
import json, re, sys

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(ROOT, 'catalog.js')):
    parent = os.path.dirname(ROOT)
    assert parent != ROOT, 'repo root with catalog.js not found above this script'
    ROOT = parent
SRC = ROOT + '/test-prep/sat/SAT-Math-1-Linear-Equations.html'
OUT = ROOT + '/test-prep/sat/SAT-Math-2-Quadratics.html'
LINEAR_URL = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/test-prep/sat/SAT-Math-1-Linear-Equations.html'

# ---------------------------------------------------------------- TAB 1: RULES
RULES = r'''
<p class="ref-intro">A quadratic is a parabola, and the SAT asks the same handful of questions about it: read the roots, the vertex, and the $y$-intercept from whichever form you are handed, factor or use the formula to solve, use the discriminant to count solutions, and find where a line meets the curve. Below, the quadratic is $y = ax^2 + bx + c$ with <span class="nw">$a \neq 0$,</span> its roots (the $x$-intercepts) are $r_1$ and <span class="nw">$r_2$,</span> and its vertex is <span class="nw">$(h, k)$.</span> Work every question the same way: recognize the type, choose the most efficient route, and sidestep the predictable trap.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules behind most SAT quadratic questions. Start here.</span><span><strong>Unstarred:</strong> shows up less often. Add it once the starred rules are automatic.</span></div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 1</span><span class="rname">Three forms of a parabola</span></div>
<p class="ref-lead">Different forms reveal different information. Recognize which form you have been given, and what it shows, before doing any algebra; the SAT asks outright which form displays which feature.</p>
<div class="tbl-wrap"><table class="forms"><thead><tr><th>Form</th><th>Formula</th><th>What it shows</th><th>Example</th></tr></thead><tbody>
<tr><td class="fname">Standard</td><td class="fmath">$y = ax^2 + bx + c$</td><td class="freads">$c$ is the $y$-intercept<br>$a > 0$ opens up, $a < 0$ opens down<br>axis of symmetry $x = -\dfrac{b}{2a}$</td><td class="fex"><span class="nw">$y = x^2 - 6x + 5$:</span> crosses the $y$-axis at <span class="nw">$5$,</span> opens up, axis $x = 3$</td></tr>
<tr><td class="fname">Factored</td><td class="fmath">$y = a(x - r_1)(x - r_2)$</td><td class="freads">the roots $r_1$ and $r_2$ are the $x$-intercepts<br>the vertex sits halfway between them</td><td class="fex"><span class="nw">$y = (x - 1)(x - 5)$:</span> $x$-intercepts $1$ and <span class="nw">$5$,</span> axis $x = 3$</td></tr>
<tr><td class="fname">Vertex</td><td class="fmath">$y = a(x - h)^2 + k$</td><td class="freads">vertex $(h, k)$<br>$k$ is the minimum value ($a > 0$) or the maximum value ($a < 0$)</td><td class="fex"><span class="nw">$y = (x - 3)^2 - 4$:</span> vertex <span class="nw">$(3, -4)$,</span> minimum value $-4$</td></tr>
</tbody></table></div>
<div class="fig-slot" data-fig="anatomy"></div>
<div class="ref-ex"><span class="exlab">Example A</span>all three are the same parabola: $(x - 1)(x - 5) = x^2 - 6x + 5 = (x - 3)^2 - 4$. Expand to move right in the table; factor or complete the square to move left</div>
<div class="ref-ex"><span class="exlab">Example B</span>“Which form displays the $x$-intercepts as constants?” is factored form. “The vertex” or “the minimum value” is vertex form. “The $y$-intercept” is standard form</div>
<div class="ref-ex"><span class="exlab">Example C</span>$a$ is the same number in every form and never moves the axis: $y = 2(x - 1)(x - 5)$ still has roots $1$ and $5$ and vertex at <span class="nw">$x = 3$,</span> but now $k = 2(3 - 1)(3 - 5) = -8$</div>
<div class="ref-note">The $y$-intercept of vertex or factored form is found by setting <span class="nw">$x = 0$:</span> for $y = 2(x - 3)^2 - 8$ it is <span class="nw">$2(9) - 8 = 10$,</span> not <span class="nw">$-8$.</span></div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 2</span><span class="rname">Factor, then set each factor to zero</span></div>
<p class="ref-lead">Factoring writes an expression as a product. A product is zero only when one of its factors is zero, so a factored equation hands you its solutions.</p>
<div class="tbl-wrap"><table class="forms"><thead><tr><th>Pattern</th><th>Expanded</th><th>Factored</th><th>Example</th></tr></thead><tbody>
<tr><td class="fname">Perfect square</td><td class="fmath">$a^2 + 2ab + b^2$</td><td class="freads">$(a + b)^2$</td><td class="fex">$x^2 + 6x + 9 = (x + 3)^2$: the middle term is twice the product of the two square roots</td></tr>
<tr><td class="fname">Perfect square</td><td class="fmath">$a^2 - 2ab + b^2$</td><td class="freads">$(a - b)^2$</td><td class="fex">$4x^2 - 12x + 9 = (2x - 3)^2$</td></tr>
<tr><td class="fname">Difference of squares</td><td class="fmath">$a^2 - b^2$</td><td class="freads">$(a + b)(a - b)$</td><td class="fex">no middle term: $x^2 - 49 = (x + 7)(x - 7)$, &nbsp; $9n^2 - 1 = (3n + 1)(3n - 1)$</td></tr>
<tr><td class="fname">Trinomial, $a = 1$</td><td class="fmath">$x^2 + bx + c$</td><td class="freads">$(x + p)(x + q)$ with <span class="nw">$p + q = b$,</span> $pq = c$</td><td class="fex">$x^2 - 2x - 3 = (x - 3)(x + 1)$: the numbers $-3$ and $1$ add to $-2$ and multiply to $-3$</td></tr>
<tr><td class="fname">Trinomial, $a \neq 1$</td><td class="fmath">$ax^2 + bx + c$</td><td class="freads">two numbers with product $ac$ and sum <span class="nw">$b$,</span> then group</td><td class="fex">$6x^2 + x - 1$: product <span class="nw">$-6$,</span> sum <span class="nw">$1$:</span> $3$ and <span class="nw">$-2$.</span> $6x^2 + 3x - 2x - 1 = (3x - 1)(2x + 1)$</td></tr>
<tr><td class="fname">Common factor first</td><td class="fmath">$12x^2 + 2x - 2$</td><td class="freads">$2(6x^2 + x - 1)$</td><td class="fex">$= 2(3x - 1)(2x + 1)$: pull the greatest common factor before anything else</td></tr>
</tbody></table></div>
<div class="fbox">
<div class="frow"><div class="flabel">zero product</div><div class="fmath">$(x - r_1)(x - r_2) = 0$ &nbsp;means&nbsp; $x = r_1$ &nbsp;or&nbsp; $x = r_2$</div></div>
<div class="frow"><div class="flabel">square root</div><div class="fmath">$x^2 = n$ gives $x = \pm\sqrt{n}$; &nbsp; $(x - h)^2 = n$ gives $x = h \pm \sqrt{n}$</div></div>
</div>
<div class="ref-ex"><span class="exlab">Example A</span><span class="nw">$x^2 - 7x + 12 = 0$:</span> $(x - 3)(x - 4) = 0$, so $x = 3$ or <span class="nw">$x = 4$.</span> The signs inside the factors are the opposite of the roots</div>
<div class="ref-ex"><span class="exlab">Example B</span><span class="nw">$2x^2 + 5x - 12 = 0$:</span> product <span class="nw">$ac = -24$,</span> sum <span class="nw">$5$:</span> $8$ and <span class="nw">$-3$.</span> $2x^2 + 8x - 3x - 12 = 2x(x + 4) - 3(x + 4) = (2x - 3)(x + 4)$, so $x = \tfrac{3}{2}$ or $x = -4$</div>
<div class="ref-ex"><span class="exlab">Example C</span>structure, not solving: if <span class="nw">$(x - 5)(x + 5) = a$,</span> then $(3x - 15)(x + 5) = 3(x - 5)(x + 5) = 3a$. Look for the piece you already know inside the new expression</div>
<div class="ref-ex"><span class="exlab">Example D</span>$x^2 - y^2 = 60$ with positive integers: $(x - y)(x + y) = 60$, and the two factors must be both even or both odd. $2 \cdot 30$ gives <span class="nw">$x = 16$,</span> <span class="nw">$y = 14$;</span> $6 \cdot 10$ gives <span class="nw">$x = 8$,</span> $y = 2$</div>
<div class="ref-note">Desmos factors for you: graph $y = 2x^2 + 5x - 12$ and click the $x$-intercepts. Use that to check. “Equivalent expression” questions have nothing to click, so the patterns above still have to be automatic. Want deeper reps on these patterns? The <a href="https://learningcurvecollective.github.io/learning-curve-collective-resources/algebra/factoring-worksheet.html" target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;">Factoring worksheet</a> drills every row of this table.</div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 3</span><span class="rname">Vertex, axis of symmetry, maximum and minimum</span></div>
<div class="fbox">
<div class="frow"><div class="flabel">axis of symmetry</div><div class="fmath">$h = -\dfrac{b}{2a} = \dfrac{r_1 + r_2}{2}$ &nbsp; (halfway between the roots, or between any two points with the same $y$)</div></div>
<div class="frow"><div class="flabel">vertex value</div><div class="fmath">$k = f(h)$: the minimum if <span class="nw">$a > 0$,</span> the maximum if $a < 0$</div></div>
<div class="frow"><div class="flabel">completing the square</div><div class="fmath">$x^2 + bx + c = \left(x + \dfrac{b}{2}\right)^2 - \dfrac{b^2}{4} + c$</div></div>
<div class="frow"><div class="flabel">symmetry</div><div class="fmath">$f(h - t) = f(h + t)$ for every $t$</div></div>
</div>
<div class="ref-ex"><span class="exlab">Example A</span><span class="nw">$y = x^2 - 6x + 5$:</span> $h = 3$ and <span class="nw">$k = 9 - 18 + 5 = -4$.</span> Completing the square agrees: $(x - 3)^2 - 9 + 5 = (x - 3)^2 - 4$</div>
<div class="ref-ex"><span class="exlab">Example B</span>in context, $h(t) = -16t^2 + 64t + 80$ is a ball's height. It starts at $80$ (set <span class="nw">$t = 0$),</span> peaks at $t = \dfrac{-64}{2(-16)} = 2$ with height <span class="nw">$h(2) = 144$,</span> and lands when <span class="nw">$h = 0$:</span> $-16(t - 5)(t + 1) = 0$, so $t = 5$</div>
<div class="ref-ex"><span class="exlab">Example C</span>if $f(2) = f(8)$ for a quadratic <span class="nw">$f$,</span> the vertex is at <span class="nw">$x = 5$,</span> whether those two outputs are $0$ or $7$</div>
<div class="ref-note">“The minimum value” is <span class="nw">$k$;</span> “the $x$ at which the minimum occurs” is <span class="nw">$h$.</span> Expect to see both among the answer choices.</div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 4</span><span class="rname">The quadratic formula and the discriminant</span></div>
<div class="fbox">
<div class="frow"><div class="flabel">quadratic formula</div><div class="fmath">$x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ &nbsp; (for $ax^2 + bx + c = 0$; set it equal to zero first)</div></div>
<div class="frow"><div class="flabel">discriminant</div><div class="fmath">$D = b^2 - 4ac$ &nbsp; (the part under the root; its sign counts the real solutions)</div></div>
<div class="frow"><div class="flabel">tangent</div><div class="fmath">a line is tangent to a parabola exactly when the combined equation has $D = 0$</div></div>
</div>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Discriminant</th><th>Real solutions</th><th>Graph of $y = ax^2 + bx + c$</th><th></th></tr></thead><tbody>
<tr><td class="fname">$D > 0$</td><td class="">two (rational if $D$ is a perfect square, irrational if not)</td><td class="">crosses the $x$-axis twice</td><td class=""><span class="fig-slot" data-fig="dpos"></span></td></tr>
<tr><td class="fname">$D = 0$</td><td class="">one, a double root at $x = -\dfrac{b}{2a}$</td><td class="">touches the $x$-axis at its vertex: the axis is tangent</td><td class=""><span class="fig-slot" data-fig="dzero"></span></td></tr>
<tr><td class="fname">$D < 0$</td><td class="">none</td><td class="">never meets the $x$-axis: entirely above it ($a > 0$) or entirely below it ($a < 0$)</td><td class=""><span class="fig-slot" data-fig="dneg"></span></td></tr>
</tbody></table></div>
<div class="ref-ex"><span class="exlab">Example A</span><span class="nw">$x^2 - 6x + 7 = 0$:</span> $D = 36 - 28 = 8$, two irrational solutions, $x = \dfrac{6 \pm \sqrt{8}}{2} = 3 \pm \sqrt{2}$</div>
<div class="ref-ex"><span class="exlab">Example B</span>$x^2 + 4x + k = 0$ has exactly one solution when <span class="nw">$16 - 4k = 0$,</span> so <span class="nw">$k = 4$.</span> &nbsp; $2x^2 + 3x + 5 = 0$ has <span class="nw">$D = 9 - 40 < 0$:</span> no real solutions</div>
<div class="ref-ex"><span class="exlab">Example C</span>$y = 2x + k$ is tangent to <span class="nw">$y = x^2 - 5$:</span> set them equal, <span class="nw">$x^2 - 2x - 5 - k = 0$.</span> Tangent means <span class="nw">$D = 0$:</span> $4 + 4(5 + k) = 24 + 4k = 0$, so $k = -6$</div>
<div class="ref-note">Set the equation equal to zero before you read <span class="nw">$a$,</span> <span class="nw">$b$,</span> and <span class="nw">$c$.</span> In <span class="nw">$x^2 - 2x = 2x + k$,</span> $b$ is <span class="nw">$-4$,</span> not <span class="nw">$-2$.</span></div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 5</span><span class="rname">A line meets a parabola</span></div>
<p class="ref-lead">Set the two $y$'s equal, move everything to one side, and solve the quadratic. Every solution $x$ is an intersection; plug it into the line, the easier equation, to get <span class="nw">$y$.</span></p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Outcome</th><th>Algebra test</th><th>Picture</th></tr></thead><tbody>
<tr><td class="fname">Two solutions</td><td class="">$D > 0$ for the combined equation</td><td class="">the line cuts through the parabola at two points</td></tr>
<tr><td class="fname">One solution</td><td class="">$D = 0$</td><td class="">the line is tangent to the parabola</td></tr>
<tr><td class="fname">No solution</td><td class="">$D < 0$</td><td class="">the line misses the parabola</td></tr>
</tbody></table></div>
<div class="fig-slot" data-fig="sys"></div>
<div class="ref-ex"><span class="exlab">Example A</span>$y = x + 1$ and <span class="nw">$y = x^2 - 3x + 4$:</span> $x^2 - 3x + 4 = x + 1$ gives <span class="nw">$x^2 - 4x + 3 = (x - 1)(x - 3) = 0$.</span> At $x = 1$, <span class="nw">$y = 2$;</span> at $x = 3$, <span class="nw">$y = 4$.</span> The solutions are $(1, 2)$ and $(3, 4)$</div>
<div class="ref-ex"><span class="exlab">Example B</span>$y = x^2 - 2x - 14$ and <span class="nw">$y = 3x$:</span> $x^2 - 5x - 14 = 0$ has <span class="nw">$D = 25 + 56 = 81 > 0$,</span> so the system has two solutions ($x = 7$ and $x = -2$)</div>
<div class="ref-ex"><span class="exlab">Example C</span>when a line and a parabola enclose a region, the intersections are the corners. From there it is the area rule from the <a href="''' + LINEAR_URL + r'''" target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;">linear sheet</a>: base on an axis, or split into triangles and trapezoids</div>
<div class="ref-note">In Desmos, graph both and click the intersection points. For a question with an unknown <span class="nw">$k$,</span> add a slider and drag it until the line just touches the curve; then confirm with $D = 0$.</div>
</div>
<div class="ref-rule"><div class="ref-rule-line"><span class="rtag">Rule 6</span><span class="rname">Sum and product of the roots</span></div>
<div class="fbox">
<div class="frow"><div class="flabel">sum</div><div class="fmath">$r_1 + r_2 = -\dfrac{b}{a}$</div></div>
<div class="frow"><div class="flabel">product</div><div class="fmath">$r_1 r_2 = \dfrac{c}{a}$</div></div>
<div class="frow"><div class="flabel">build from the roots</div><div class="fmath">$x^2 - (r_1 + r_2)\,x + r_1 r_2 = 0$</div></div>
<div class="frow"><div class="flabel">two useful rewrites</div><div class="fmath">$\dfrac{1}{r_1} + \dfrac{1}{r_2} = \dfrac{r_1 + r_2}{r_1 r_2}$, &nbsp; $r_1^2 + r_2^2 = (r_1 + r_2)^2 - 2 r_1 r_2$</div></div>
</div>
<div class="ref-ex"><span class="exlab">Example A</span>where it comes from: $a(x - r_1)(x - r_2) = ax^2 - a(r_1 + r_2)\,x + a\,r_1 r_2$. Match the coefficients with $ax^2 + bx + c$</div>
<div class="ref-ex"><span class="exlab">Example B</span>one root of $3x^2 + x - k = 0$ is <span class="nw">$1$.</span> The sum of the roots is <span class="nw">$-\tfrac{1}{3}$,</span> so the other root is <span class="nw">$-\tfrac{1}{3} - 1 = -\tfrac{4}{3}$.</span> ($k$ was never needed; it is $4$)</div>
<div class="ref-ex"><span class="exlab">Example C</span>if $\alpha$ and $\beta$ are the roots of <span class="nw">$x^2 + 6x - 16 = 0$,</span> then $\dfrac{1}{\alpha} + \dfrac{1}{\beta} = \dfrac{\alpha + \beta}{\alpha\beta} = \dfrac{-6}{-16} = \tfrac{3}{8}$. Check by factoring: $(x + 8)(x - 2)$ gives $-\tfrac{1}{8} + \tfrac{1}{2} = \tfrac{3}{8}$. ✓</div>
<div class="ref-note">Rare on the digital SAT, but it turns a two-minute factoring problem into a ten-second one, and a question with an unknown constant in the $c$ slot is built for it.</div>
</div>
<div class="ref-rule"><div class="ref-rule-line"><span class="rtag">Rule 7</span><span class="rname">Shifting and reflecting a parabola</span></div>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Move</th><th>New equation</th><th>Effect on the vertex $(h, k)$</th></tr></thead><tbody>
<tr><td class="fname">up $n$ units</td><td class="">$f(x) + n$</td><td class="">$(h, k + n)$</td></tr>
<tr><td class="fname">right $n$ units</td><td class="">$f(x - n)$</td><td class="">$(h + n, k)$</td></tr>
<tr><td class="fname">across the $x$-axis</td><td class="">$-f(x)$</td><td class=""><span class="nw">$(h, -k)$,</span> and $a \to -a$: a minimum becomes a maximum</td></tr>
<tr><td class="fname">across the $y$-axis</td><td class="">$f(-x)$</td><td class="">$(-h, k)$</td></tr>
</tbody></table></div>
<div class="ref-ex"><span class="exlab">Example A</span>$f(x) = (x - 2)^2 - 5$ shifted left $3$ and up <span class="nw">$4$:</span> <span class="nw">$g(x) = (x + 1)^2 - 1$,</span> vertex $(-1, -1)$</div>
<div class="ref-ex"><span class="exlab">Example B</span>the graph of $y = x^2 - 4x$ translated down <span class="nw">$3$:</span> <span class="nw">$y = x^2 - 4x - 3$.</span> Its new $x$-intercepts, <span class="nw">$2 \pm \sqrt{7}$,</span> come from the new equation, not from sliding the old ones</div>
<div class="ref-ex"><span class="exlab">Example C</span>$-f(x)$ flips the parabola: $y = -(x - 2)^2 + 5$ opens down with maximum <span class="nw">$5$.</span> The $x$-intercepts stay put, because they sit on the mirror line</div>
<div class="ref-note">Inside the parentheses the sign runs backwards: $(x - 2)^2$ is a shift to the <em>right</em> by <span class="nw">$2$.</span></div>
</div>
<hr class="ref-divider"><div class="ref-h">Common SAT traps and how to avoid them</div>
<p>Each move below looks reasonable, is wrong, and produces a wrong answer that sits waiting in the choices. Learn to recognize these now, so you can sidestep them under time pressure.</p>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 1</span><span class="rname">reading the roots with the signs as written</span></div><div class="ref-ex">$(x - 3)(x + 5) = 0$ has roots $3$ and <span class="nw">$-5$.</span> Set each factor to zero: $x - 3 = 0$ gives <span class="nw">$x = 3$.</span> The signs flip.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 2</span><span class="rname">dividing both sides by $x$</span></div><div class="ref-ex">$x^2 = 5x$ has two solutions, $0$ and <span class="nw">$5$.</span> Dividing by $x$ throws away <span class="nw">$x = 0$.</span> Move everything to one side and factor: $x(x - 5) = 0$.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 3</span><span class="rname">a square root with one sign</span></div><div class="ref-ex">$(x - 3)^2 = 16$ gives <span class="nw">$x - 3 = \pm 4$,</span> so $x = 7$ or <span class="nw">$x = -1$.</span> Half of the answer lives in the minus sign.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 4</span><span class="rname">$(x + 3)^2 = x^2 + 9$</span></div><div class="ref-ex">The middle term is <span class="nw">$2 \cdot 3 \cdot x$:</span> <span class="nw">$(x + 3)^2 = x^2 + 6x + 9$.</span> For the same reason $\sqrt{x^2 + 9}$ is not <span class="nw">$x + 3$.</span></div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 5</span><span class="rname">reading $a$, $b$, $c$ before the equation equals zero</span></div><div class="ref-ex">$x^2 - 2x = 2x + k$ becomes <span class="nw">$x^2 - 4x - k = 0$,</span> so $b = -4$ and <span class="nw">$c = -k$.</span> The discriminant uses the moved version, every time.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 6</span><span class="rname">copying the sign inside the parentheses into the vertex</span></div><div class="ref-ex">$y = 2(x + 1)^2 - 3$ has vertex <span class="nw">$(-1, -3)$:</span> $h$ flips sign, $k$ does not. Check by plugging in <span class="nw">$x = -1$,</span> which makes the square zero.</div></div>
'''

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Read the parabola in any form",
  "rule": r"$y = ax^2 + bx + c$ &nbsp;·&nbsp; $y = a(x - r_1)(x - r_2)$ &nbsp;·&nbsp; $y = a(x - h)^2 + k$",
  "say": r"Standard form shows the $y$-intercept, factored form shows the $x$-intercepts, vertex form shows the vertex. Every form is the same parabola, and the SAT's favorite version of this rule is a question that hands you one form and asks which <em>equivalent</em> form displays a particular feature as a constant.",
  "prob": r"The function $f$ is defined by <span class=\"nw\">$f(x) = x^2 - 6x + 5$.</span> Which equivalent form of $f(x)$ displays the $x$-intercepts of the graph as constants, and which displays the vertex as constants?",
  "sol": r"<strong>$x$-intercepts: factor.</strong> Two numbers with product $5$ and sum <span class=\"nw\">$-6$:</span> $-1$ and <span class=\"nw\">$-5$.</span> <span class=\"nw\">$f(x) = (x - 1)(x - 5)$,</span> so the intercepts are $1$ and <span class=\"nw\">$5$.</span><br><strong>Vertex: complete the square.</strong> $x^2 - 6x + 5 = (x - 3)^2 - 9 + 5 = (x - 3)^2 - 4$, vertex <span class=\"nw\">$(3, -4)$.</span> Check with the roots: the vertex sits halfway between $1$ and <span class=\"nw\">$5$,</span> at <span class=\"nw\">$x = 3$.</span> ✓",
  "trap": r"Picking $(x - 3)^2 + 5$ because it “keeps the $5$.” The $5$ is the $y$-intercept of standard form; it is not $k$. Expand your choice back out: $(x - 3)^2 + 5 = x^2 - 6x + 14$, which is a different parabola.",
  "micro": {"q": r"The $y$-intercept of $y = 2(x - 3)^2 - 8$ is $y =$", "accept": ["10"],
            "exp": r"Set <span class=\"nw\">$x = 0$:</span> <span class=\"nw\">$2(0 - 3)^2 - 8 = 18 - 8 = 10$.</span> The $-8$ is the minimum value, not the $y$-intercept."}},
 {"ess": True, "name": "Rule 2: Factor, then zero-product",
  "rule": r"$(x - r_1)(x - r_2) = 0$ &nbsp;means&nbsp; $x = r_1$ or $x = r_2$",
  "say": r"Move everything to one side so the equation equals zero, pull any common factor, then factor the trinomial: two numbers with product $ac$ and sum <span class=\"nw\">$b$.</span> When $a = 1$ they go straight into the parentheses; when $a \neq 1$, split the middle term and group. Each factor set to zero is one solution.",
  "prob": r"What are the solutions of the equation <span class=\"nw\">$2x^2 + 5x - 12 = 0$?</span>",
  "sol": r"<strong>Step 1: product and sum.</strong> $ac = -24$ and <span class=\"nw\">$b = 5$:</span> the numbers are $8$ and <span class=\"nw\">$-3$.</span><br><strong>Step 2: split and group.</strong> $2x^2 + 8x - 3x - 12 = 2x(x + 4) - 3(x + 4) = (2x - 3)(x + 4)$.<br><strong>Step 3: each factor to zero.</strong> $2x - 3 = 0$ gives <span class=\"nw\">$x = \tfrac{3}{2}$;</span> $x + 4 = 0$ gives <span class=\"nw\">$x = -4$.</span> Check: $2(16) - 20 - 12 = 0$. ✓",
  "trap": r"Reading the solutions off the factors with the signs as written: $(2x - 3)(x + 4)$ does not have roots $-3$ and <span class=\"nw\">$4$.</span> And on a student-produced response that asks for “the positive solution,” $\tfrac{3}{2}$ and $1.5$ both count; $3$ does not.",
  "micro": {"q": r"The positive solution of $x^2 - 2x - 15 = 0$ is $x =$", "accept": ["5"],
            "exp": r"$(x - 5)(x + 3) = 0$: product $-15$, sum <span class=\"nw\">$-2$.</span> The positive solution is <span class=\"nw\">$5$.</span>"}},
 {"ess": True, "name": "Rule 2, continued: Squares and structure",
  "rule": r"$a^2 - b^2 = (a + b)(a - b)$ &nbsp;·&nbsp; $a^2 \pm 2ab + b^2 = (a \pm b)^2$",
  "say": r"The SAT's “equivalent expression” questions run on two patterns: a difference of squares and a perfect square. Spot them by the missing middle term or by a middle term that is twice the product of two square roots. Often the move is to expand what you are given, regroup, and recognize a square, not to solve anything.",
  "prob": r"Which of the following is equivalent to <span class=\"nw\">$\left(n - \dfrac{2}{n}\right)^2 + 8$?</span> &nbsp; (A) $8$ &nbsp; (B) $\left(n + \dfrac{2}{n}\right)^2$ &nbsp; (C) $n^2 + \dfrac{4}{n^2}$ &nbsp; (D) $n^2 - \dfrac{4}{n^2}$",
  "sol": r"<strong>Step 1: expand the square.</strong> $\left(n - \tfrac{2}{n}\right)^2 = n^2 - 2 \cdot n \cdot \tfrac{2}{n} + \tfrac{4}{n^2} = n^2 - 4 + \tfrac{4}{n^2}$.<br><strong>Step 2: add the 8.</strong> $n^2 + 4 + \tfrac{4}{n^2}$.<br><strong>Step 3: recognize a perfect square.</strong> The middle term $4$ is $2 \cdot n \cdot \tfrac{2}{n}$, so this is <span class=\"nw\">$\left(n + \tfrac{2}{n}\right)^2$.</span> Choice B.",
  "trap": r"Choice C is the expansion with the middle term dropped: $(a + b)^2$ is never <span class=\"nw\">$a^2 + b^2$.</span> If the pattern is not obvious, plug in $n = 2$: the original is $(2 - 1)^2 + 8 = 9$, and only choice B gives <span class=\"nw\">$(2 + 1)^2 = 9$.</span>",
  "micro": {"q": r"If $x^2 - y^2 = 32$ and <span class=\"nw\">$x + y = 8$,</span> then $x - y =$", "accept": ["4"],
            "exp": r"$x^2 - y^2 = (x + y)(x - y)$, so <span class=\"nw\">$8(x - y) = 32$</span> and <span class=\"nw\">$x - y = 4$.</span>"}},
 {"ess": True, "name": "Rule 4: The discriminant counts the solutions",
  "rule": r"$D = b^2 - 4ac$ &nbsp;·&nbsp; $D > 0$: two &nbsp;·&nbsp; $D = 0$: one &nbsp;·&nbsp; $D < 0$: none",
  "say": r"The discriminant is the part under the root in the quadratic formula, and its sign is all the SAT usually wants: two real solutions, one (a double root, the graph tangent to the $x$-axis), or none (the graph never reaches the $x$-axis). Any question with “how many solutions,” “exactly one,” “no real solutions,” or “for what value of $k$” is a discriminant question.",
  "prob": r"Which of the following is true about the graph of $y = 2x^2 - 10x + 9$ in the $xy$-plane? &nbsp; (A) It is tangent to the $x$-axis. &nbsp; (B) It intersects the $x$-axis at two points. &nbsp; (C) It lies entirely above the $x$-axis. &nbsp; (D) It lies entirely below the $x$-axis.",
  "sol": r"<strong>Step 1: the discriminant.</strong> $D = (-10)^2 - 4(2)(9) = 100 - 72 = 28$.<br><strong>Step 2: read the sign.</strong> $D > 0$, so there are two real roots and the graph crosses the $x$-axis twice. Choice B.<br><strong>If $D$ had been negative:</strong> $a = 2 > 0$ opens up, so the graph would sit entirely above the axis (choice C). The sign of $a$ decides above versus below.",
  "trap": r"Reading $-10$ as $b$ but forgetting to square it, or a sign slip in $4ac$. Write $D$ out in full before simplifying; the arithmetic is the whole question. Desmos check: graph it and count the crossings.",
  "micro": {"q": r"For what value of $k$ are the two roots of $x^2 + 4x + k = 0$ equal? $k =$", "accept": ["4"],
            "exp": r"Equal roots means <span class=\"nw\">$D = 0$:</span> <span class=\"nw\">$16 - 4k = 0$,</span> so <span class=\"nw\">$k = 4$.</span> Then $x^2 + 4x + 4 = (x + 2)^2$, a double root at $-2$. ✓"}},
 {"ess": True, "name": "Rule 4, continued: Tangent means $D = 0$",
  "rule": r"set the equations equal, move to one side, then $b^2 - 4ac = 0$",
  "say": r"“Tangent,” “touches at exactly one point,” and “the system has exactly one solution” all say the same thing: the combined quadratic has a double root. Set the two expressions for $y$ equal, bring everything to one side (this is where the unknown $k$ lands in $c$), and solve <span class=\"nw\">$D = 0$</span> for <span class=\"nw\">$k$.</span>",
  "fig": "tangent",
  "prob": r"In the $xy$-plane above, the graph of $y = 2x + k$ is tangent to the graph of <span class=\"nw\">$y = x^2 - 5$,</span> where $k$ is a constant. What is the value of <span class=\"nw\">$k$?</span>",
  "sol": r"<strong>Step 1: set them equal and move to one side.</strong> $x^2 - 5 = 2x + k$ gives <span class=\"nw\">$x^2 - 2x - (5 + k) = 0$.</span> Now $a = 1$, <span class=\"nw\">$b = -2$,</span> <span class=\"nw\">$c = -5 - k$.</span><br><strong>Step 2: tangent means $D = 0$.</strong> $(-2)^2 - 4(1)(-5 - k) = 4 + 20 + 4k = 24 + 4k = 0$, so <span class=\"nw\">$k = -6$.</span><br><strong>Check:</strong> $x^2 - 2x + 1 = (x - 1)^2$, a double root at <span class=\"nw\">$x = 1$,</span> where both graphs give <span class=\"nw\">$y = -4$.</span> ✓",
  "trap": r"Using $b = -2$ with $c = -5$ and forgetting that $k$ moved to the left side with a minus sign. Rewrite the full equation set to zero and copy $a$, <span class=\"nw\">$b$,</span> $c$ from that line only.",
  "micro": {"q": r"The graph of $y = x^2 + 10x + k$ is tangent to the $x$-axis. Then $k =$", "accept": ["25"],
            "exp": r"Tangent to the $x$-axis means one root: <span class=\"nw\">$100 - 4k = 0$,</span> so <span class=\"nw\">$k = 25$.</span> Indeed $x^2 + 10x + 25 = (x + 5)^2$."}},
 {"ess": True, "name": "Rule 3: Vertex, maximum, minimum",
  "rule": r"$h = -\dfrac{b}{2a} = \dfrac{r_1 + r_2}{2}$ &nbsp;·&nbsp; $k = f(h)$",
  "say": r"The vertex is on the axis of symmetry, halfway between the roots or any two inputs with equal outputs, and $-\tfrac{b}{2a}$ finds it from standard form directly. Its $y$-value is the maximum (opens down) or minimum (opens up). In a word problem, the vertex is the highest point of a throw or the price that maximizes revenue, and the roots are when it lands or when revenue is zero.",
  "prob": r"A ball is thrown upward from the top of a building. Its height above the ground, in feet, $t$ seconds after the throw is given by <span class=\"nw\">$h(t) = -16t^2 + 64t + 80$.</span> What is the maximum height of the ball, and at what time does the ball hit the ground?",
  "sol": r"<strong>Step 1: the vertex.</strong> $t = -\dfrac{b}{2a} = -\dfrac{64}{2(-16)} = 2$ seconds. $h(2) = -64 + 128 + 80 = 144$ feet, the maximum since $a < 0$.<br><strong>Step 2: the ground is $h = 0$.</strong> $-16t^2 + 64t + 80 = 0$, divide by <span class=\"nw\">$-16$:</span> $t^2 - 4t - 5 = (t - 5)(t + 1) = 0$. The ball lands at <span class=\"nw\">$t = 5$</span> (the root $t = -1$ is before the throw).<br><strong>Read the rest for free:</strong> $h(0) = 80$ is the building's height, and the vertex at $t = 2$ with landing at $t = 5$ is not symmetric only because the ball starts $80$ feet up.",
  "trap": r"Answering $2$ when the question asks for the maximum height, or $144$ when it asks when the maximum occurs. The vertex is a pair, $(h, k)$: one coordinate is a time, the other is a height, and the question picks one.",
  "micro": {"mc": True, "q": r"Which form of $f(x) = x^2 - 8x + 10$ displays the minimum value of $f$ as a constant?",
            "opts": [r"$f(x) = x(x - 8) + 10$", r"$f(x) = (x - 4)^2 - 6$", r"$f(x) = (x - 4)^2 + 10$", r"$f(x) = (x - 2)(x - 6) - 2$"], "correct": 1,
            "exp": r"Complete the square: $x^2 - 8x + 16 - 16 + 10 = (x - 4)^2 - 6$. The minimum value is <span class=\"nw\">$-6$,</span> at <span class=\"nw\">$x = 4$.</span>"}},
 {"ess": True, "name": "Rule 5: A line meets a parabola",
  "rule": r"set $y = y$, solve the quadratic &nbsp;·&nbsp; each root is an intersection",
  "say": r"A system of a line and a parabola is one quadratic equation in disguise: substitute the line into the parabola, move everything to one side, factor. Each root is the $x$ of an intersection; the line gives you the <span class=\"nw\">$y$.</span> To count the solutions without finding them, use the discriminant of that same equation.",
  "fig": "sys",
  "prob": r"$$y = x + 1$$ $$y = x^2 - 3x + 4$$ The graphs of the equations above intersect at two points in the $xy$-plane. What are the coordinates of the two points?",
  "sol": r"<strong>Step 1: set the right sides equal.</strong> $x^2 - 3x + 4 = x + 1$.<br><strong>Step 2: one side, then factor.</strong> $x^2 - 4x + 3 = 0$ gives <span class=\"nw\">$(x - 1)(x - 3) = 0$,</span> so $x = 1$ or <span class=\"nw\">$x = 3$.</span><br><strong>Step 3: the line gives $y$.</strong> $y = 1 + 1 = 2$ and <span class=\"nw\">$y = 3 + 1 = 4$.</span> The points are $(1, 2)$ and <span class=\"nw\">$(3, 4)$.</span><br><strong>Desmos:</strong> graph both, click each intersection. Same answer in ten seconds.",
  "trap": r"Stopping at $x = 1$ and <span class=\"nw\">$x = 3$</span> when the question asks for points, or for the <em>sum of the $y$-coordinates</em> ($2 + 4 = 6$). Read the last sentence of the question again before you type anything.",
  "micro": {"mc": True, "q": r"How many solutions does the system $y = x^2 - 2x - 14$, $y = 3x$ have?",
            "opts": ["$0$", "$1$", "$2$", "Infinitely many"], "correct": 2,
            "exp": r"$x^2 - 2x - 14 = 3x$ gives <span class=\"nw\">$x^2 - 5x - 14 = 0$,</span> with <span class=\"nw\">$D = 25 + 56 = 81 > 0$:</span> two solutions. (They are $x = 7$ and <span class=\"nw\">$x = -2$.)</span>"}},
 {"ess": False, "name": "Rule 6: Sum and product of the roots",
  "rule": r"$r_1 + r_2 = -\dfrac{b}{a}$ &nbsp;·&nbsp; $r_1 r_2 = \dfrac{c}{a}$",
  "say": r"Expand $a(x - r_1)(x - r_2)$ and match it with <span class=\"nw\">$ax^2 + bx + c$:</span> the sum of the roots is $-\tfrac{b}{a}$ and the product is <span class=\"nw\">$\tfrac{c}{a}$,</span> with no solving required. It shines when one root is known and the constant is not, or when the question asks for a combination of the roots such as $\tfrac{1}{r_1} + \tfrac{1}{r_2}$ rather than the roots themselves.",
  "prob": r"If one root of the quadratic equation $3x^2 + x - k = 0$ is <span class=\"nw\">$1$,</span> what is the other root of the equation? &nbsp; (A) $-\tfrac{7}{3}$ &nbsp; (B) $-\tfrac{4}{3}$ &nbsp; (C) $-\tfrac{1}{3}$ &nbsp; (D) $\tfrac{4}{3}$",
  "sol": r"<strong>The sum route (no $k$ needed).</strong> The roots add to <span class=\"nw\">$-\tfrac{b}{a} = -\tfrac{1}{3}$.</span> One root is <span class=\"nw\">$1$,</span> so the other is <span class=\"nw\">$-\tfrac{1}{3} - 1 = -\tfrac{4}{3}$.</span> Choice B.<br><strong>The long route agrees.</strong> Plug in $x = 1$: $3 + 1 - k = 0$ gives <span class=\"nw\">$k = 4$,</span> and $3x^2 + x - 4 = (3x + 4)(x - 1)$ has roots $1$ and <span class=\"nw\">$-\tfrac{4}{3}$.</span> ✓<br><strong>Bonus check:</strong> when one root is $1$, the product of the roots <em>is</em> the other root: $\tfrac{c}{a} = -\tfrac{4}{3}$. ✓",
  "trap": r"Using $-b$ instead of $-\tfrac{b}{a}$ when $a \neq 1$: the sum here is <span class=\"nw\">$-\tfrac{1}{3}$,</span> not <span class=\"nw\">$-1$.</span> The product route also works, but it needs $k$ first.",
  "micro": {"mc": True, "q": r"If $\alpha$ and $\beta$ are the roots of <span class=\"nw\">$x^2 + 6x - 16 = 0$,</span> what is $\dfrac{1}{\alpha} + \dfrac{1}{\beta}$?",
            "opts": [r"$-\tfrac{3}{8}$", r"$\tfrac{3}{8}$", r"$\tfrac{8}{3}$", r"$\tfrac{3}{4}$"], "correct": 1,
            "exp": r"$\dfrac{1}{\alpha} + \dfrac{1}{\beta} = \dfrac{\alpha + \beta}{\alpha\beta} = \dfrac{-6}{-16} = \tfrac{3}{8}$. Factoring agrees: the roots are $-8$ and <span class=\"nw\">$2$,</span> and $-\tfrac{1}{8} + \tfrac{1}{2} = \tfrac{3}{8}$."}},
 {"ess": False, "name": "Rule 7: Shifting and reflecting a parabola",
  "rule": r"$f(x) + n$: up $n$ &nbsp;·&nbsp; $f(x - n)$: right $n$ &nbsp;·&nbsp; $-f(x)$: flip over the $x$-axis",
  "say": r"Transformations move the vertex and nothing else about the shape: adding outside the function shifts up or down, subtracting inside shifts right (backwards from what it looks like), and a leading minus sign flips the parabola so a minimum becomes a maximum. Track the vertex and the sign of <span class=\"nw\">$a$;</span> everything else follows.",
  "prob": r"The graph of $f(x) = (x - 2)^2 - 5$ is translated $3$ units to the left and $4$ units up to produce the graph of <span class=\"nw\">$g$.</span> What is the vertex of the graph of <span class=\"nw\">$g$,</span> and what is the minimum value of <span class=\"nw\">$g$?</span>",
  "sol": r"<strong>Step 1: the original vertex.</strong> $(2, -5)$.<br><strong>Step 2: move it.</strong> Left $3$: $x = 2 - 3 = -1$. Up $4$: $y = -5 + 4 = -1$. Vertex <span class=\"nw\">$(-1, -1)$.</span><br><strong>Step 3: write $g$ if asked.</strong> $g(x) = f(x + 3) + 4 = (x + 1)^2 - 1$. The minimum value of $g$ is <span class=\"nw\">$-1$,</span> since $a = 1 > 0$.",
  "trap": r"Shifting left by writing $(x - 3)$: left is <span class=\"nw\">$f(x + 3)$.</span> Check with the vertex: $(x + 1)^2$ is zero at <span class=\"nw\">$x = -1$,</span> which is where the new vertex should be.",
  "micro": {"q": r"If $f(x) = x^2 - 6x + 11$ and <span class=\"nw\">$g(x) = f(x) + 4$,</span> the minimum value of $g$ is", "accept": ["6"],
            "exp": r"$f$ has its minimum at $x = 3$: <span class=\"nw\">$f(3) = 9 - 18 + 11 = 2$.</span> Shifting up $4$ makes the minimum <span class=\"nw\">$6$.</span>"}},
]
STEPS = [STEPS[i] for i in [0, 1, 2, 5, 3, 4, 6, 7, 8]]  # forms, factor, squares, vertex, discriminant, tangent, systems, sum/product, transforms
LAST_STARRED_STEP_INDEX = 6  # 0-based index of the last starred step (Rule 5)

# ---------------------------------------------------------------- TAB 3: FLUENCY
FLUENCY = [
 {"sec": "A. Read the parabola", "items": [
   {"q": r"The $y$-intercept of $y = 3(x - 2)^2 - 7$ is $y =$", "accept": ["5"], "exp": r"Set <span class=\"nw\">$x = 0$:</span> <span class=\"nw\">$3(4) - 7 = 5$.</span>"},
   {"q": r"The $x$-coordinate of the vertex of $y = x^2 + 8x - 3$ is $x =$", "accept": ["-4"], "exp": r"$-\dfrac{b}{2a} = -\dfrac{8}{2} = -4$."},
   {"q": r"The larger $x$-intercept of $y = (x + 2)(x - 7)$ is $x =$", "accept": ["7"], "exp": r"The roots are $-2$ and <span class=\"nw\">$7$</span> (signs flipped from the factors)."},
   {"mc": True, "q": r"The parabola with vertex $(3, -2)$ and $a = 1$ is", "opts": [r"$y = (x + 3)^2 - 2$", r"$y = (x - 3)^2 - 2$", r"$y = (x - 3)^2 + 2$", r"$y = (x - 2)^2 + 3$"], "correct": 1, "exp": r"Vertex form $y = a(x - h)^2 + k$ with $h = 3$ and <span class=\"nw\">$k = -2$:</span> <span class=\"nw\">$y = (x - 3)^2 - 2$.</span>"},
 ]},
 {"sec": "B. Factor and solve", "items": [
   {"q": r"The positive solution of $x^2 - 5x - 14 = 0$ is $x =$", "accept": ["7"], "exp": r"$(x - 7)(x + 2) = 0$: product $-14$, sum <span class=\"nw\">$-5$.</span>"},
   {"q": r"The nonzero solution of $3x^2 - 12x = 0$ is $x =$", "accept": ["4"], "exp": r"Factor, don't divide: $3x(x - 4) = 0$, so $x = 0$ or <span class=\"nw\">$x = 4$.</span>"},
   {"mc": True, "q": r"$4x^2 - 25$ is equivalent to", "opts": [r"$(2x - 5)(2x + 5)$", r"$(2x - 5)^2$", r"$(4x - 5)(x + 5)$", r"$(2x - 25)(2x + 1)$"], "correct": 0, "exp": r"A difference of squares: $(2x)^2 - 5^2 = (2x - 5)(2x + 5)$."},
   {"q": r"The only solution of $x^2 - 10x + 25 = 0$ is $x =$", "accept": ["5"], "exp": r"A perfect square: $(x - 5)^2 = 0$, a double root at <span class=\"nw\">$5$.</span>"},
 ]},
 {"sec": "C. The discriminant", "items": [
   {"q": r"The discriminant of $x^2 - 6x + 7 = 0$ is", "accept": ["8"], "exp": r"$b^2 - 4ac = 36 - 28 = 8$. Two irrational solutions."},
   {"q": r"The number of real solutions of $2x^2 + 3x + 5 = 0$ is", "accept": ["0"], "exp": r"$D = 9 - 40 = -31 < 0$: no real solutions."},
   {"q": r"If $x^2 - 8x + k = 0$ has exactly one solution, then $k =$", "accept": ["16"], "exp": r"$D = 64 - 4k = 0$ gives <span class=\"nw\">$k = 16$,</span> and $(x - 4)^2 = 0$. ✓"},
   {"mc": True, "q": r"The graph of $y = x^2 + 4x + 7$", "opts": ["is tangent to the $x$-axis", "crosses the $x$-axis at two points", "lies entirely above the $x$-axis", "lies entirely below the $x$-axis"], "correct": 2, "exp": r"$D = 16 - 28 < 0$, so no $x$-intercepts; $a = 1 > 0$ opens up, so the graph is entirely above the axis."},
 ]},
 {"sec": "D. Systems, sums, products", "items": [
   {"q": r"The graphs of $y = x^2$ and $y = 2x + 3$ meet at two points. The larger $x$-coordinate is $x =$", "accept": ["3"], "exp": r"$x^2 - 2x - 3 = (x - 3)(x + 1) = 0$: <span class=\"nw\">$x = 3$</span> or <span class=\"nw\">$x = -1$.</span>"},
   {"q": r"The number of solutions of the system $y = x^2 + 1$, $y = -x - 2$ is", "accept": ["0"], "exp": r"$x^2 + x + 3 = 0$ has <span class=\"nw\">$D = 1 - 12 < 0$:</span> the line misses the parabola."},
   {"q": r"The sum of the solutions of $3x^2 - 12x + 5 = 0$ is", "accept": ["4"], "exp": r"$-\dfrac{b}{a} = -\dfrac{-12}{3} = 4$. No need to solve."},
   {"q": r"The product of the solutions of $2x^2 + 7x - 6 = 0$ is", "accept": ["-3"], "exp": r"$\dfrac{c}{a} = \dfrac{-6}{2} = -3$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: GAUNTLET
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"The function $f$ is defined by <span class=\"nw\">$f(x) = (x - 3)(x + 5)$.</span> Which of the following are the $x$-intercepts of the graph of $y = f(x)$ in the $xy$-plane?",
  "options": [r"$(-3, 0)$ and $(5, 0)$", r"$(0, -15)$ only", r"$(3, 0)$ and $(-5, 0)$", r"$(0, 3)$ and $(0, -5)$"], "correct": 2,
  "desmos": ["y=(x-3)(x+5)"],
  "sol": r"<strong>Given:</strong> factored form.<br><br>Each factor set to zero: $x - 3 = 0$ gives <span class=\"nw\">$x = 3$,</span> $x + 5 = 0$ gives <span class=\"nw\">$x = -5$.</span> The $x$-intercepts are $(3, 0)$ and <span class=\"nw\">$(-5, 0)$.</span>",
  "trap": r"Choice A copies the signs from inside the parentheses. Choice D swaps the coordinates: $x$-intercepts have <span class=\"nw\">$y = 0$.</span> Choice B is the $y$-intercept, $f(0) = -15$."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"What is the sum of the solutions to the equation <span class=\"nw\">$x^2 - 7x + 12 = 0$?</span>",
  "label": "Sum $=$", "accept": ["7"], "desmos": ["y=x^2-7x+12"],
  "sol": r"<strong>Given:</strong> a trinomial with $a = 1$.<br><br>$(x - 3)(x - 4) = 0$, so the solutions are $3$ and <span class=\"nw\">$4$,</span> with sum <span class=\"nw\">$7$.</span> Rule 6 says the same thing in one step: the sum is <span class=\"nw\">$-\tfrac{b}{a} = 7$.</span>",
  "trap": r"Typing one solution instead of the sum. Easy items are lost to the last three words of the question."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"The function $h(t) = -16t^2 + 48t + 160$ gives the height <span class=\"nw\">$h$,</span> in feet, of a ball $t$ seconds after it is thrown upward from the top of a building. Which of the following is the best interpretation of $160$ in this context?",
  "options": ["The maximum height of the ball, in feet", "The height of the building, in feet", "The number of seconds the ball is in the air", "The speed at which the ball is thrown, in feet per second"], "correct": 1,
  "desmos": ["y=-16x^2+48x+160\\left\\{0\\le x\\le 5\\right\\}", "(0,160)"],
  "sol": r"<strong>Given:</strong> standard form, with $c = 160$.<br><br>$h(0) = 160$: the height at the moment of the throw, which is the top of the building. The maximum height is at the vertex, $t = \tfrac{48}{32} = 1.5$, where $h = 196$, so choice A is a different number.",
  "trap": r"The constant term of a quadratic model is the starting value, exactly as the intercept was in the linear sheet. The maximum lives at the vertex, not in any single coefficient."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"$$y = x^2 - 6x + 5$$ Which of the following is an equivalent form of the equation above that displays the coordinates of the vertex of the parabola as constants?",
  "options": [r"$y = (x - 1)(x - 5)$", r"$y = x(x - 6) + 5$", r"$y = (x - 3)^2 + 5$", r"$y = (x - 3)^2 - 4$"], "correct": 3,
  "desmos": ["y=x^2-6x+5", "(3,-4)"],
  "sol": r"<strong>Given:</strong> standard form; wanted: vertex form.<br><br>Complete the square: $x^2 - 6x + 9 - 9 + 5 = (x - 3)^2 - 4$. The vertex is <span class=\"nw\">$(3, -4)$.</span> Check: $-\tfrac{b}{2a} = 3$ and $y(3) = 9 - 18 + 5 = -4$. ✓",
  "trap": r"Choice C has the right $h$ and the wrong <span class=\"nw\">$k$:</span> it expands to <span class=\"nw\">$x^2 - 6x + 14$,</span> a different parabola. Choice A displays the $x$-intercepts; a companion question usually asks for those instead."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"$$y = x^2 - 2x - 8$$ $$y = x + 2$$ The graphs of the equations above intersect at two points in the $xy$-plane. What is the $x$-coordinate of the point of intersection with the greater $x$-coordinate?",
  "label": "$x =$", "accept": ["5"], "desmos": ["y=x^2-2x-8", "y=x+2"],
  "sol": r"<strong>Given:</strong> a line and a parabola.<br><br>$x^2 - 2x - 8 = x + 2$ gives <span class=\"nw\">$x^2 - 3x - 10 = 0$,</span> so <span class=\"nw\">$(x - 5)(x + 2) = 0$</span> and <span class=\"nw\">$x = 5$</span> or <span class=\"nw\">$x = -2$.</span> The greater is <span class=\"nw\">$5$</span> (the point is $(5, 7)$).",
  "trap": r"Forgetting to move the $x + 2$ across: $x^2 - 2x - 8 = 0$ has roots $4$ and <span class=\"nw\">$-2$,</span> and $4$ is the standard wrong answer. Desmos: graph both, click the right-hand intersection."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"Which of the following is true about the graph of $y = 3x^2 - 2x + 4$ in the $xy$-plane?",
  "options": ["It is tangent to the $x$-axis.", "It intersects the $x$-axis at two points.", "It lies entirely above the $x$-axis.", "It lies entirely below the $x$-axis."], "correct": 2,
  "desmos": ["y=3x^2-2x+4"],
  "sol": r"<strong>Given:</strong> standard form; asked: how many $x$-intercepts.<br><br>$D = (-2)^2 - 4(3)(4) = 4 - 48 = -44 < 0$, so no $x$-intercepts. $a = 3 > 0$ opens up, so the whole graph is above the axis.",
  "trap": r"A negative discriminant says the graph never reaches the axis, but not which side it is on. That is the sign of <span class=\"nw\">$a$.</span> Choice D would need $a < 0$."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"The function $f$ is defined by <span class=\"nw\">$f(x) = 2x^2 + 12x + k$,</span> where $k$ is a constant. If the minimum value of $f$ is <span class=\"nw\">$-5$,</span> what is the value of <span class=\"nw\">$k$?</span>",
  "label": "$k =$", "accept": ["13"], "desmos": ["y=2x^2+12x+13", "(-3,-5)"],
  "sol": r"<strong>Given:</strong> the minimum value, which is $k$ in vertex form, is <span class=\"nw\">$-5$.</span><br><br>The vertex is at $x = -\tfrac{12}{4} = -3$, and $f(-3) = 18 - 36 + k = k - 18$. Set that equal to the minimum: <span class=\"nw\">$k - 18 = -5$,</span> so <span class=\"nw\">$k = 13$.</span> Check by completing the square: $2(x + 3)^2 - 18 + 13 = 2(x + 3)^2 - 5$. ✓",
  "trap": r"Factoring out the $2$ changes what you subtract: $2(x^2 + 6x) + k = 2(x + 3)^2 - 2 \cdot 9 + k$. Forgetting that factor gives $k = 4$. Finding the vertex with $-\tfrac{b}{2a}$ and evaluating avoids the slip."},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"$$y = x^2 + 2x + 5$$ $$y = -2x + 1$$ How many solutions does the system of equations above have?",
  "options": ["Zero", "Exactly one", "Exactly two", "Infinitely many"], "correct": 1,
  "desmos": ["y=x^2+2x+5", "y=-2x+1"],
  "sol": r"<strong>Given:</strong> a line and a parabola; asked only how many times they meet.<br><br>$x^2 + 2x + 5 = -2x + 1$ gives <span class=\"nw\">$x^2 + 4x + 4 = 0$,</span> which is <span class=\"nw\">$(x + 2)^2 = 0$:</span> $D = 16 - 16 = 0$. One solution, at <span class=\"nw\">$(-2, 5)$,</span> where the line is tangent to the parabola.",
  "trap": r"“Infinitely many” never happens for a line and a parabola; they are different shapes. The real choice is between zero, one, and two, and the discriminant of the combined equation decides."},
 {"ess": True, "type": "mc", "diff": "Medium-hard", "fig": "g9",
  "stem": r"In the $xy$-plane above, the graphs of $f(x) = x + k$ and $g(x) = x^2 - 2x + 3$ are tangent to each other, where $k$ is a constant. What is the value of <span class=\"nw\">$k$?</span>",
  "options": [r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$", r"$\dfrac{3}{4}$", r"$\dfrac{5}{4}$"], "correct": 2,
  "desmos": ["y=x^2-2x+3", "y=x+k", "k=0.75"],
  "sol": r"<strong>Given:</strong> tangent, so the combined equation has <span class=\"nw\">$D = 0$.</span><br><br>$x^2 - 2x + 3 = x + k$ gives <span class=\"nw\">$x^2 - 3x + (3 - k) = 0$.</span> Then $D = 9 - 4(3 - k) = 9 - 12 + 4k = 4k - 3 = 0$, so <span class=\"nw\">$k = \tfrac{3}{4}$.</span> The point of tangency is at $x = \tfrac{3}{2}$, where both give <span class=\"nw\">$y = \tfrac{9}{4}$.</span>",
  "trap": r"The constant is $3 - k$, not <span class=\"nw\">$3$:</span> the unknown has to cross to the left side before you read <span class=\"nw\">$c$.</span> In Desmos, the load adds a slider for $k$; drag it and watch the line lift off the curve on either side of $0.75$."},
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "g10",
  "stem": r"The graphs of the functions $f(x) = x + 3$ and $g(x) = -x^2 + 9$ are shown in the $xy$-plane above. Points $A$ and $C$ are the $x$-intercepts of $f$ and <span class=\"nw\">$g$,</span> respectively, and $B$ is a point of intersection of the two graphs. What is the area of triangle <span class=\"nw\">$ABC$?</span>",
  "label": "Area $=$", "accept": ["15"], "desmos": ["y=x+3", "y=-x^2+9", "(-3,0),(2,5),(3,0)"],
  "sol": r"<strong>Given:</strong> three vertices to find, then base on the $x$-axis.<br><br>$A$: $x + 3 = 0$, so <span class=\"nw\">$A = (-3, 0)$.</span> $C$: $-x^2 + 9 = 0$ with $x > 0$, so <span class=\"nw\">$C = (3, 0)$.</span> $B$: $x + 3 = -x^2 + 9$ gives $x^2 + x - 6 = (x + 3)(x - 2) = 0$; the intersection above the axis is <span class=\"nw\">$B = (2, 5)$.</span> Base $AC = 6$, height <span class=\"nw\">$5$:</span> area $= \tfrac{1}{2}(6)(5) = 15$.",
  "trap": r"The other intersection, $x = -3$, is point $A$ itself: the line and the parabola share that $x$-intercept. The height is the $y$-coordinate of <span class=\"nw\">$B$,</span> not the distance along the line."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "c1",
  "stem": r"In the $xy$-plane above, the graphs of $y = x^2 - 5x + 10$ and $y = 2x$ intersect at points $B$ and <span class=\"nw\">$C$.</span> Points $A$ and $D$ lie on the $x$-axis directly below $B$ and <span class=\"nw\">$C$.</span> What is the area of quadrilateral <span class=\"nw\">$ABCD$?</span>",
  "label": "Area $=$", "accept": ["21"], "desmos": ["y=x^2-5x+10", "y=2x", "(2,4),(5,10),(2,0),(5,0)"],
  "sol": r"<strong>Given:</strong> the corners are the intersections and their feet on the $x$-axis.<br><br>$x^2 - 5x + 10 = 2x$ gives <span class=\"nw\">$x^2 - 7x + 10 = (x - 2)(x - 5) = 0$.</span> From the line, <span class=\"nw\">$B = (2, 4)$</span> and <span class=\"nw\">$C = (5, 10)$,</span> so $A = (2, 0)$ and <span class=\"nw\">$D = (5, 0)$.</span> $ABCD$ is a trapezoid with parallel vertical sides $AB = 4$ and $DC = 10$ and width <span class=\"nw\">$AD = 3$:</span> area $= \tfrac{1}{2}(4 + 10)(3) = 21$.",
  "trap": r"The parabola is scenery once the corners are found; the region is bounded by the line and the axis. If the trapezoid formula is not automatic, split it: a $3 \times 4$ rectangle plus a triangle with legs $3$ and <span class=\"nw\">$6$,</span> $12 + 9 = 21$."},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"If <span class=\"nw\">$(x - 5)(x + 5) = a$,</span> then $(3x - 15)(x + 5) =$",
  "options": ["$2a$", "$3a$", "$5a$", "$15a$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a known product inside a new one.<br><br>$3x - 15 = 3(x - 5)$, so $(3x - 15)(x + 5) = 3(x - 5)(x + 5) = 3a$.",
  "trap": r"Expanding both sides ($x^2 - 25 = a$, and $(3x - 15)(x + 5) = 3x^2 - 75 = 3(x^2 - 25)$) works too and lands on the same <span class=\"nw\">$3a$,</span> but it costs a minute. Factor the new expression until the old one appears; these questions are built so that it does.",
  "extrasIntro": r"Structure questions hide a known expression inside a new one. Factor, expand, or complete the square until the known piece shows up. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"If <span class=\"nw\">$x^2 - 16 = 9$,</span> then $(x - 4)(x + 4) =$", "label": "$=$", "accept": ["9"], "exp": r"$(x - 4)(x + 4) = x^2 - 16$, which is given as <span class=\"nw\">$9$.</span> No solving."},
   {"type": "ne", "q": r"If <span class=\"nw\">$(x + 3)^2 = 17$,</span> then $x^2 + 6x =$", "label": "$=$", "accept": ["8"], "exp": r"$(x + 3)^2 = x^2 + 6x + 9 = 17$, so <span class=\"nw\">$x^2 + 6x = 8$.</span>"},
   {"type": "ne", "q": r"If <span class=\"nw\">$x^2 + 10x = 39$,</span> then $(x + 5)^2 =$", "label": "$=$", "accept": ["64"], "exp": r"Complete the square: $(x + 5)^2 = x^2 + 10x + 25 = 39 + 25 = 64$."},
  ]},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"Which of the following is equivalent to <span class=\"nw\">$\left(n - \dfrac{3}{n}\right)^2 + 12$?</span>",
  "options": ["$12$", r"$\left(n + \dfrac{3}{n}\right)^2$", r"$n^2 + \dfrac{9}{n^2}$", r"$n^2 - \dfrac{9}{n^2}$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a perfect square in disguise.<br><br>$\left(n - \tfrac{3}{n}\right)^2 = n^2 - 6 + \tfrac{9}{n^2}$. Adding $12$: <span class=\"nw\">$n^2 + 6 + \tfrac{9}{n^2}$,</span> and the middle term $6 = 2 \cdot n \cdot \tfrac{3}{n}$ makes this <span class=\"nw\">$\left(n + \tfrac{3}{n}\right)^2$.</span>",
  "trap": r"Choice C drops the middle term. When the algebra is not obvious, test a number: with $n = 3$ the original is $(3 - 1)^2 + 12 = 16$, and only choice B gives <span class=\"nw\">$(3 + 1)^2 = 16$.</span>"},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"The equation $3x^2 - 7x + c = 0$, where $c$ is a constant, has $x = 2$ as one of its solutions. What is the other solution?",
  "label": "$x =$", "accept": ["1/3", "0.333", ".333", "0.3333", ".3333", "0.33", ".33"],
  "desmos": ["y=3x^2-7x+2"],
  "sol": r"<strong>Given:</strong> one root and no constant.<br><br>Sum of the roots $= -\tfrac{b}{a} = \tfrac{7}{3}$, so the other root is <span class=\"nw\">$\tfrac{7}{3} - 2 = \tfrac{1}{3}$.</span> The long route agrees: $x = 2$ gives $12 - 14 + c = 0$, so <span class=\"nw\">$c = 2$,</span> and $3x^2 - 7x + 2 = (3x - 1)(x - 2)$.",
  "trap": r"On a student-produced response, $1/3$ and $.333$ both count; $0.3$ does not. Solving for $c$ first is fine but doubles the work; the sum of the roots skips it.",
  "extrasIntro": r"Sum and product questions ask about a combination of the roots, never the roots themselves. Write the combination in terms of $r_1 + r_2$ and <span class=\"nw\">$r_1 r_2$,</span> then read those off the coefficients. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"If $\alpha$ and $\beta$ are the roots of <span class=\"nw\">$x^2 + 5x - 10 = 0$,</span> then $\dfrac{1}{\alpha} + \dfrac{1}{\beta} =$", "label": "$=$", "accept": ["1/2", "0.5", ".5"], "exp": r"$\dfrac{\alpha + \beta}{\alpha\beta} = \dfrac{-5}{-10} = \tfrac{1}{2}$. No need to find the roots themselves."},
   {"type": "ne", "q": r"If $r$ and $s$ are the solutions of <span class=\"nw\">$x^2 - 5x + 6 = 0$,</span> then $r^2 + s^2 =$", "label": "$=$", "accept": ["13"], "exp": r"$(r + s)^2 - 2rs = 25 - 12 = 13$. (The roots are $2$ and <span class=\"nw\">$3$:</span> $4 + 9 = 13$. ✓)"},
   {"type": "ne", "q": r"The equation $x^2 + bx + c = 0$ has solutions $2$ and <span class=\"nw\">$-5$.</span> Then $b =$", "label": "$b =$", "accept": ["3"], "exp": r"Sum $= 2 + (-5) = -3 = -b$, so <span class=\"nw\">$b = 3$.</span> (And $c = -10$: the equation is $(x - 2)(x + 5) = 0$.)"},
  ]},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"If <span class=\"nw\">$x^2 - y^2 = 40$,</span> where $x$ and $y$ are positive integers with <span class=\"nw\">$x > y$,</span> what is one possible value of <span class=\"nw\">$x$?</span>",
  "label": "$x =$", "accept": ["7", "11"],
  "sol": r"<strong>Given:</strong> a difference of squares equal to a number, with integer unknowns.<br><br>$(x - y)(x + y) = 40$. Since $x + y$ and $x - y$ differ by <span class=\"nw\">$2y$,</span> an even number, both factors are even or both are odd; $40$ has no odd-by-odd factorization, so both are even: $2 \cdot 20$ or <span class=\"nw\">$4 \cdot 10$.</span> From $x - y = 2$, <span class=\"nw\">$x + y = 20$:</span> $x = 11$, <span class=\"nw\">$y = 9$.</span> From $x - y = 4$, <span class=\"nw\">$x + y = 10$:</span> $x = 7$, <span class=\"nw\">$y = 3$.</span> Either $7$ or $11$ is accepted.",
  "trap": r"$1 \cdot 40$ and $5 \cdot 8$ look available, but they give fractions for $x$ (the two factors must add to an even number, $2x$). Check: $121 - 81 = 40$ and $49 - 9 = 40$. ✓"},
 {"ess": True, "type": "mc", "diff": "Hard",
  "stem": r"In the $xy$-plane, the graph of a quadratic function $f$ has $x$-intercepts at $(-2, 0)$ and $(6, 0)$ and passes through the point <span class=\"nw\">$(0, -6)$.</span> What is the minimum value of <span class=\"nw\">$f$?</span>",
  "options": ["$-8$", "$-6$", "$-16$", "$-4$"], "correct": 0,
  "desmos": ["y=\\frac{1}{2}(x+2)(x-6)", "(0,-6),(2,-8)"],
  "sol": r"<strong>Given:</strong> two roots and one more point, so factored form with an unknown <span class=\"nw\">$a$.</span><br><br>$f(x) = a(x + 2)(x - 6)$. At $x = 0$: $a(2)(-6) = -12a = -6$, so <span class=\"nw\">$a = \tfrac{1}{2}$.</span> The vertex is halfway between the roots, at <span class=\"nw\">$x = 2$:</span> $f(2) = \tfrac{1}{2}(4)(-4) = -8$. Since $a > 0$ this is the minimum.",
  "trap": r"$-6$ is the $y$-intercept, not the minimum: the vertex is at $x = 2$, not <span class=\"nw\">$x = 0$.</span> $-16$ is what you get with $a = 1$, before using the third point. Two roots pin down the axis; the extra point pins down <span class=\"nw\">$a$.</span>",
  "extrasIntro": r"Roots pin down the axis of symmetry: the vertex is always at their average. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The $x$-coordinate of the vertex of $y = (x - 1)(x - 9)$ is $x =$", "label": "$x =$", "accept": ["5"], "exp": r"Halfway between the roots $1$ and <span class=\"nw\">$9$:</span> <span class=\"nw\">$x = 5$.</span>"},
   {"type": "ne", "q": r"The function $f(x) = x^2 + bx + 12$ has <span class=\"nw\">$f(2) = 0$.</span> The other zero of $f$ is $x =$", "label": "$x =$", "accept": ["6"], "exp": r"<strong>Product of the roots</strong> $= \tfrac{c}{a} = 12$, so the other root is <span class=\"nw\">$\tfrac{12}{2} = 6$.</span> (Then $b = -8$: $x^2 - 8x + 12 = (x - 2)(x - 6)$.)"},
   {"type": "ne", "q": r"A parabola has $x$-intercepts $-3$ and $5$ and passes through <span class=\"nw\">$(0, 30)$.</span> Its maximum value is", "label": "Max $=$", "accept": ["32"], "exp": r"<strong>Step 1: $a$.</strong> $y = a(x + 3)(x - 5)$; at $x = 0$, $-15a = 30$, so <span class=\"nw\">$a = -2$.</span><br><strong>Step 2: vertex at $x = 1$.</strong> $y = -2(4)(-4) = 32$."},
  ]},
]

_area = GAUNTLET.pop()  # the geometry-blend area question moves to the challenge tab
_area["diff"] = "Medium-hard · geometry blend"
CHALLENGE.insert(1, _area)
CHALLENGE[0]["diff"] = "Medium-hard · geometry blend"
GAUNTLET.insert(6,  {"ess": True, "type": "ne", "diff": "Medium", "fig": "g7",
  "stem": r"The graph of <span class=\"nw\">$y = x^2 + bx + c$,</span> where $b$ and $c$ are constants, is shown in the $xy$-plane above. The graph has $x$-intercepts at $(-6, 0)$ and <span class=\"nw\">$(2, 0)$.</span> What is the value of <span class=\"nw\">$b$?</span>",
  "label": "$b =$", "accept": ["4"], "desmos": ["y=x^2+4x-12", "(-6,0),(2,0)"],
  "sol": r"<strong>Given:</strong> both roots, so factored form is free.<br><br>$y = (x + 6)(x - 2)$, and expanding gives <span class=\"nw\">$x^2 + 4x - 12$:</span> <span class=\"nw\">$b = 4$</span> (and <span class=\"nw\">$c = -12$).</span> Rule 6 agrees in one step: the sum of the roots is <span class=\"nw\">$-6 + 2 = -4$,</span> and $b$ is its opposite.",
  "trap": r"The sign: roots $-6$ and $2$ give factors $(x + 6)$ and <span class=\"nw\">$(x - 2)$,</span> flipped from the roots. A ten-second expansion settles $b$ and its sign for good."})

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"The $x$-intercepts of the graph of $y = (x + 4)(x - 2)$ are at $x =$", "opts": ["$-4$ and $2$", "$4$ and $-2$", "$-4$ and $-2$", "$4$ and $2$"], "correct": 0,
  "exp": r"Set each factor to zero: $x + 4 = 0$ gives <span class=\"nw\">$-4$,</span> $x - 2 = 0$ gives <span class=\"nw\">$2$.</span> The signs flip."},
 {"q": r"The number of real solutions of $x^2 + 3x + 5 = 0$ is", "opts": ["$2$", "$1$", "$0$", "Infinitely many"], "correct": 2,
  "exp": r"$D = 9 - 20 = -11 < 0$: the graph never reaches the $x$-axis."},
 {"q": r"The vertex of the graph of $y = 2(x - 1)^2 + 3$ is", "opts": ["$(-1, 3)$", "$(1, 3)$", "$(1, -3)$", "$(-1, -3)$"], "correct": 1,
  "exp": r"Vertex form $a(x - h)^2 + k$ with $h = 1$ and <span class=\"nw\">$k = 3$:</span> the sign inside the parentheses flips, the one outside does not."},
]

# ---------------------------------------------------------------- FIGURES
FIGS_JS = r'''var FIGS = {
    anatomy: { xmin: -2, xmax: 8, ymin: -6, ymax: 8, w: 340, h: 260, alt: 'the parabola y = x squared minus 6x plus 5 with its y-intercept, x-intercepts, vertex, and axis of symmetry labeled',
        curves: [{ a: 1, b: -6, c: 5 }],
        segs: [{ x1: 3, y1: -6, x2: 3, y2: 8 }],
        points: [{ x: 1, y: 0, label: '(1, 0)', dx: 5, dy: -8 }, { x: 5, y: 0, label: '(5, 0)', dx: 8, dy: 16 }, { x: 0, y: 5, label: '(0, 5)', dx: -44, dy: -2 }, { x: 3, y: -4, label: '(3, −4)', dx: 8, dy: 14 }],
        labels: [{ x: 3, y: 7.2, text: 'x = 3', dx: 6, dy: 0 }] },
    g7: { xmin: -9, xmax: 5, ymin: -18, ymax: 8, w: 330, h: 260, alt: 'an upward parabola with x-intercepts at (-6, 0) and (2, 0)',
        curves: [{ a: 1, b: 4, c: -12, label: 'y = x² + bx + c', lx: -5.4, ly: 6.5, dx: 0, dy: 0 }],
        points: [{ x: -6, y: 0, label: '(−6, 0)', dx: -24, dy: -10 }, { x: 2, y: 0, label: '(2, 0)', dx: 8, dy: -10 }] },
    sys: { xmin: -2, xmax: 6, ymin: -1, ymax: 9, w: 340, h: 260, alt: 'the parabola y = x squared minus 3x plus 4 and the line y = x plus 1 meeting at (1, 2) and (3, 4)',
        curves: [{ a: 1, b: -3, c: 4, label: 'y = x² − 3x + 4', lx: 0.62, ly: 8.3, dx: 0, dy: 0 }],
        lines: [{ m: 1, b: 1, label: 'y = x + 1', lx: 4.55, ly: 5.55, dx: 8, dy: 12 }],
        points: [{ x: 1, y: 2, label: '(1, 2)', dx: -52, dy: 6 }, { x: 3, y: 4, label: '(3, 4)', dx: 10, dy: 12 }] },
    tangent: { xmin: -4, xmax: 5, ymin: -7, ymax: 6, w: 320, h: 250, alt: 'the parabola y = x squared minus 5 with the line y = 2x minus 6 tangent to it at (1, negative 4)',
        curves: [{ a: 1, b: 0, c: -5, label: 'y = x² − 5', lx: 3.15, ly: 4.9, dx: 6, dy: 2 }],
        lines: [{ m: 2, b: -6, cls: 'ln2', label: 'y = 2x + k', lx: 3.3, ly: -1.9, dx: 8, dy: 4 }],
        points: [{ x: 1, y: -4, label: '(1, −4)', dx: 8, dy: 12 }] },
    g9: { xmin: -3, xmax: 5, ymin: -2, ymax: 12, w: 340, h: 260, alt: 'the parabola g(x) = x squared minus 2x plus 3 and the line f(x) = x + k tangent to it',
        curves: [{ a: 1, b: -2, c: 3, label: 'g', lx: 3.65, ly: 11.2, dx: 8, dy: 0 }],
        lines: [{ m: 1, b: 0.75, cls: 'ln2', label: 'f', lx: 4.35, ly: 5.1, dx: 6, dy: 2 }] },
    g10: { xmin: -5, xmax: 5, ymin: -3, ymax: 11, w: 330, h: 250, alt: 'the line f(x) = x + 3 and the downward parabola g(x) = 9 minus x squared, with triangle ABC shaded between their x-intercepts and their intersection',
        poly: [[-3, 0], [2, 5], [3, 0]],
        curves: [{ a: -1, b: 0, c: 9, label: 'g', lx: -3.35, ly: -2.2, dx: -14, dy: 4 }],
        lines: [{ m: 1, b: 3, cls: 'ln2', label: 'f', lx: 4.3, ly: 7.3, dx: 6, dy: 0 }],
        points: [{ x: -3, y: 0, label: 'A', dx: -16, dy: 17 }, { x: 2, y: 5, label: 'B', dx: 8, dy: -4 }, { x: 3, y: 0, label: 'C', dx: 6, dy: 16 }] },
    c1: { xmin: -1, xmax: 8, ymin: -2, ymax: 13, w: 330, h: 270, alt: 'the parabola y = x squared minus 5x plus 10 and the line y = 2x meeting at B and C, with the quadrilateral ABCD shaded down to the x-axis',
        poly: [[2, 0], [2, 4], [5, 10], [5, 0]],
        curves: [{ a: 1, b: -5, c: 10, label: 'y = x² − 5x + 10', lx: 5.55, ly: 12.3, dx: 6, dy: 0 }],
        lines: [{ m: 2, b: 0, cls: 'ln2', label: 'y = 2x', lx: 2.75, ly: 5.5, dx: -56, dy: 0 }],
        segs: [{ x1: 2, y1: 0, x2: 2, y2: 4 }, { x1: 5, y1: 0, x2: 5, y2: 10 }],
        squares: [{ x: 2, y: 0, u: [1, 0], v: [0, 1], size: 8 }, { x: 5, y: 0, u: [-1, 0], v: [0, 1], size: 8 }],
        points: [{ x: 2, y: 4, label: 'B', dx: -16, dy: -4 }, { x: 5, y: 10, label: 'C', dx: 10, dy: 2 }],
        labels: [{ x: 2, y: 0, text: 'A', dx: -4, dy: 17 }, { x: 5, y: 0, text: 'D', dx: -4, dy: 17 }] }
};
/* Small discriminant pictures for the Rule 3 table: a parabola below, on, or above the x-axis. */
function miniParab(vy) {
    var axis = 46, y0 = 6, cy = 2 * vy - y0;
    return '<svg class="fig" viewBox="0 0 120 64" width="120" height="64" style="margin:0;" role="img" aria-label="parabola and x-axis">' +
        '<line class="ax" x1="6" y1="' + axis + '" x2="114" y2="' + axis + '"/>' +
        '<text class="it" x="104" y="' + (axis + 13) + '">x</text>' +
        '<path class="ln" d="M22,' + y0 + ' Q60,' + cy + ' 98,' + y0 + '"/></svg>';
}
var MINI = { dpos: function() { return miniParab(60); }, dzero: function() { return miniParab(46); }, dneg: function() { return miniParab(30); } };
function fig(name) { if (MINI[name]) return MINI[name](); return FIGS[name] ? graphSVG(FIGS[name]) : ''; }'''

CURVES_JS = r'''    (o.curves || []).forEach(function(c) {
        // y = a x^2 + b x + c, sampled across the window and clipped to the plot box
        var n = 160, pts = [];
        for (var i = 0; i <= n; i++) {
            var x = xmin + (xmax - xmin) * i / n;
            pts.push(X(x).toFixed(1) + ',' + Y(c.a * x * x + c.b * x + c.c).toFixed(1));
        }
        s += '<polyline class="' + (c.cls || 'ln') + '" clip-path="url(#clip' + id + ')" points="' + pts.join(' ') + '"/>';
        if (c.label) s += '<text class="it" x="' + (X(c.lx) + (c.dx || 0)) + '" y="' + (Y(c.ly) + (c.dy || 0)) + '">' + c.label + '</text>';
    });
'''

def _clean(o):
    """The literals above are r-strings, so \" arrives as backslash+quote; drop the backslash."""
    if isinstance(o, str): return o.replace('\\"', '"')
    if isinstance(o, list): return [_clean(v) for v in o]
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    return o

def js_data(name, data):
    return 'var ' + name + ' = ' + json.dumps(_clean(data), ensure_ascii=False).replace('</', '<\\/') + ';\n'

def sub1(src, pattern, repl, flags=0, count=1):
    new, n = re.subn(pattern, lambda m: repl, src, count=count, flags=flags)
    if n != count:
        sys.exit('pattern not found (%d of %d): %r' % (n, count, pattern[:80]))
    return new

def replace_once(src, old, new):
    if src.count(old) != 1:
        sys.exit('expected exactly one occurrence (%d): %r' % (src.count(old), old[:100]))
    return src.replace(old, new)

html = open(SRC, encoding='utf-8').read()
html = re.sub(r'\s*<p style="font-size:14px; margin-top:10px;">Ready for the next topic\?.*?</p>', '', html, flags=re.S)

# --- header / titles / footer
html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Quadratics</title>')
html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Quadratics</h1>')
html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; QUADRATICS')
html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Quadratics')
html = replace_once(html, '>1. Linear Rules</button>', '>1. Quadratic Rules</button>')
html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Quadratic rules</h2>')

# --- tab 1 body
start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
html = html[:start] + RULES.rstrip('\n') + '\n' + html[end:]

# --- tab 2 intro card
html = replace_once(html,
    '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
    '<p>Everything on the rules tab runs on one idea: <strong>a quadratic is a product of two linear factors, and its graph is symmetric about its vertex.</strong> The factors hand you the roots, the symmetry hands you the vertex, and every SAT question about a parabola is asking for one of those, for how many roots there are, or for where a line meets the curve.</p>')

# --- tab 4 and tab 5 intro cards
html = replace_once(html,
    'from easy openers to the high-medium items near the end. A <strong>',
    'from easy openers through medium to medium-hard at the end, and two carry figures. A <strong>')
html = replace_once(html,
    '<p>These six run from high-medium to hard: the linear questions that show up late in a module and separate a strong score from a perfect one. Each one is a rule you already have, paired with a second idea (an unknown that cancels, an area, a reflection, a translation, a pair of intercepts).',
    '<p>These seven pick up where the practice set stops, running from medium-hard to hard: late-module question types that separate a strong score from a perfect one. Each is a rule you already have, paired with a second idea (an area between two graphs, a known expression hidden inside a new one, a perfect square in disguise, a constant you never need, an integer constraint, a third point that fixes $a$). The first two blend coordinate geometry into the algebra; that pairing shows up less often than the pure algebra, so treat it as stretch practice once the rest is solid.')

# --- tab 6: rule prompt and extra reps
html = replace_once(html,
    'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
    'One sentence you will say to yourself the next time a parabola shows up. Make it an if-then. (Shape: “When a question says tangent or exactly one solution, I ______ before I solve anything.”)')
# (Bluebook framing and voice renames are inherited from the shell)
html = replace_once(html,
    'the units <em>Linear equations in two variables</em>, <em>Linear functions</em>, and <em>Systems of two linear equations</em> are this sheet\'s Rules 1 through 5.',
    'the units <em>Nonlinear equations in one variable and systems of equations in two variables</em>, <em>Nonlinear functions</em>, and <em>Equivalent expressions</em> are this sheet\'s Rules 1 through 5.')
html = replace_once(html,
    'For the calculator side of these questions (graphing a system, a slider for $k$, reading an intersection), see',
    'For the calculator side of these questions (graphing a parabola, a slider for $k$, clicking a vertex or an intersection), see')
html = replace_once(html,
    '<p style="font-size:14px; margin-top:10px;">For the calculator side',
    '<p style="font-size:14px; margin-top:10px;">The lines in these questions (slope, intercepts, the area a line encloses) are covered in <a href="' + LINEAR_URL + '" target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;">SAT Math 1: Linear Equations &#8594;</a></p>\n            <p style="font-size:14px; margin-top:10px;">For the calculator side')

# --- Desmos guidance: swap the linear sheet's examples for quadratic ones
html = replace_once(html,
    'finding an intersection, checking a slope, sliding a $k$. For a one-step slope read or a quick substitution, straight algebra is faster.',
    'counting intersections, clicking a root or a vertex, sliding a $k$. For equivalent expressions and structure questions, straight algebra is faster.')

# --- data arrays
for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
    html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

# --- figures: FIGS + fig(), and a curve renderer plus clip path in graphSVG
start = html.index('var FIGS = {')
end = html.index("function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }") + len("function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }")
html = html[:start] + FIGS_JS + html[end:]
html = replace_once(html,
    """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';""",
    """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker>' +
        '<clipPath id="clip' + id + '"><rect x="' + X(xmin) + '" y="' + Y(ymax) + '" width="' + (X(xmax) - X(xmin)) + '" height="' + (Y(ymin) - Y(ymax)) + '"/></clipPath></defs>';""")
html = replace_once(html, "    (o.lines || []).forEach(function(l) {\n", CURVES_JS + "    (o.lines || []).forEach(function(l) {\n")

# --- misc: storage key, last-starred-step hint
html = html.replace('sat-linear-sheet:rule', 'sat-quadratics-sheet:rule')
html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                    "(i === %d ? 'That was the last starred step. The next two are the extras.' : '')" % LAST_STARRED_STEP_INDEX)
html = replace_once(html, "Step 1 of 9", "Step 1 of %d" % len(STEPS))

open(OUT, 'w', encoding='utf-8').write(html)
print('wrote', OUT, len(html), 'bytes;', len(STEPS), 'steps,', sum(len(s['items']) for s in FLUENCY), 'fluency,', len(GAUNTLET), 'gauntlet,', len(CHALLENGE), 'challenge,', len(EXIT), 'exit')
