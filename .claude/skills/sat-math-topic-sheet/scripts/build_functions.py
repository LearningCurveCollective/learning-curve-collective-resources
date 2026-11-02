#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-3-Functions.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the
content swaps. All questions use original numbers (the DSAT Tips 13, 14, 15, 16 and 43 pages
were the source of the question TYPES only)."""
import json, re, sys

import os
ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(ROOT, 'catalog.js')):
    parent = os.path.dirname(ROOT)
    assert parent != ROOT, 'repo root with catalog.js not found above this script'
    ROOT = parent
SRC = ROOT + '/test-prep/sat/SAT-Math-1-Linear-Equations.html'
OUT = ROOT + '/test-prep/sat/SAT-Math-3-Functions.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
LINEAR_URL = SITE + 'test-prep/sat/SAT-Math-1-Linear-Equations.html'
QUAD_URL = SITE + 'test-prep/sat/SAT-Math-2-Quadratics.html'

# ---------------------------------------------------------------- TAB 1: RULES
RULES = r'''
<p class="ref-intro">A function is a rule that turns each input into exactly one output, and the SAT asks the same handful of questions about one: evaluate it, read it off a graph or a table, say where it is undefined, feed one function into another, decide when an equation holds for every <span class="nw">$x$,</span> and recognize a graph that has been shifted. Below, $f$ and $g$ are functions, $x$ is the input, and $f(x)$ is the output. Work every question the same way: recognize the type, choose the most efficient route, and sidestep the predictable trap.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules behind most SAT function questions. Start here.</span><span><strong>Unstarred:</strong> shows up less often. Add it once the starred rules are automatic.</span></div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 1</span><span class="rname">Function notation: input, output, point</span></div>
<p class="ref-lead">$f(x)$ is a name for the output that goes with the input <span class="nw">$x$.</span> Read $f(4) = 2$ as “put in <span class="nw">$4$,</span> get out <span class="nw">$2$,”</span> which is the point $(4, 2)$ on the graph. Everything else about functions is built on that one translation.</p>
<div class="fig-slot" data-fig="machine"></div>
<div class="fbox">
<div class="frow"><div class="flabel">evaluate</div><div class="fmath">replace every <span class="nw">$x$:</span> for <span class="nw">$f(x) = x^2 - 4x$,</span> $f(-2) = (-2)^2 - 4(-2) = 12$</div></div>
<div class="frow"><div class="flabel">solve</div><div class="fmath">$f(a) = c$ is an equation in <span class="nw">$a$:</span> $a^2 - 4a = 12$ gives $a = 6$ or $a = -2$</div></div>
<div class="frow"><div class="flabel">on a graph</div><div class="fmath">$f(a) = c$ means the point $(a, c)$ is on the graph; &nbsp; $f(x) = c$ has one solution for each time the graph meets the line $y = c$</div></div>
<div class="frow"><div class="flabel">in a table</div><div class="fmath">each column is one point $(x, f(x))$; the input row and the output row are never interchangeable</div></div>
</div>
<div class="fig-slot" data-fig="notation"></div>
<div class="ref-ex"><span class="exlab">Example A</span><span class="nw">$f(x) = 3x^2 - 2$:</span> $f(-2) = 3(4) - 2 = 10$. Square first, then multiply: $(-2)^2$ is <span class="nw">$4$,</span> not $-4$</div>
<div class="ref-ex"><span class="exlab">Example B</span>$f(x + 1)$ means replace every $x$ with <span class="nw">$x + 1$:</span> for <span class="nw">$f(x) = x^2 - 4x$,</span> $f(x + 1) = (x + 1)^2 - 4(x + 1) = x^2 - 2x - 3$. It is not $f(x) + 1$</div>
<div class="ref-ex"><span class="exlab">Example C</span>reading the graph below: $f(x) = 1$ has three solutions because the graph meets the line $y = 1$ three times (near <span class="nw">$x = -3.2$,</span> near <span class="nw">$x = 0.3$,</span> and at <span class="nw">$x = 2$),</span> and $f(3) = 0$ because $(3, 0)$ is on the graph</div>
<div class="fig-slot" data-fig="crossings"></div>
<div class="ref-note">In Desmos, type $f(x) = x^2 - 4x$ on one line and $f(-2)$ on the next: it evaluates. Add $y = 1$ to see every solution of $f(x) = 1$ as an intersection you can click.</div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 2</span><span class="rname">Domain: where a function is undefined</span></div>
<p class="ref-lead">The domain is every input the rule can accept. Two things break a rule on the SAT: dividing by zero and taking the square root of a negative number. Set the denominator equal to zero and solve; set the radicand greater than or equal to zero and solve.</p>
<div class="tbl-wrap"><table class="forms"><thead><tr><th>Form</th><th>Restriction</th><th>How to find it</th><th>Example</th></tr></thead><tbody>
<tr><td class="fname">Fraction &nbsp;$\dfrac{P(x)}{Q(x)}$<span class="fig-slot" data-fig="m_frac"></span></td><td class="fmath">$Q(x) \neq 0$</td><td class="freads">set $Q(x) = 0$, factor, solve; every solution is a value where the function is undefined</td><td class="fex"><span class="nw">$\dfrac{x + 5}{x^2 - 5x + 6}$:</span> $(x - 2)(x - 3) = 0$, undefined at $x = 2$ and $x = 3$</td></tr>
<tr><td class="fname">Square root &nbsp;$\sqrt{R(x)}$<span class="fig-slot" data-fig="m_root"></span></td><td class="fmath">$R(x) \geq 0$</td><td class="freads">solve the inequality; the domain starts at the value that makes the radicand zero</td><td class="fex"><span class="nw">$\sqrt{2x - 6}$:</span> $2x - 6 \geq 0$, so $x \geq 3$</td></tr>
<tr><td class="fname">Root underneath &nbsp;$\dfrac{1}{\sqrt{R(x)}}$</td><td class="fmath">$R(x) > 0$</td><td class="freads">both rules at once, so zero is excluded too and the inequality turns strict</td><td class="fex"><span class="nw">$\dfrac{4}{\sqrt{x - 3}}$:</span> $x > 3$</td></tr>
<tr><td class="fname">Root over a fraction &nbsp;$\dfrac{\sqrt{R(x)}}{Q(x)}$</td><td class="fmath">$R(x) \geq 0$, &nbsp;$Q(x) \neq 0$</td><td class="freads">the answer choice that states <em>both</em> conditions</td><td class="fex"><span class="nw">$\dfrac{\sqrt{x + 4}}{x - 1}$:</span> $x \geq -4$ and $x \neq 1$</td></tr>
</tbody></table></div>
<div class="fig-row"><div class="fig-slot" data-fig="undefined"></div><div class="fig-slot" data-fig="sqrtdom"></div></div>
<div class="ref-ex"><span class="exlab">Example A</span>a repeated chunk: <span class="nw">$h(x) = \dfrac{3}{(x - 2)^2 - 3(x - 2) - 10}$.</span> Let <span class="nw">$u = x - 2$:</span> $u^2 - 3u - 10 = (u - 5)(u + 2) = 0$, so $u = 5$ or <span class="nw">$u = -2$,</span> which is $x = 7$ or <span class="nw">$x = 0$.</span> The substitution saves expanding</div>
<div class="ref-ex"><span class="exlab">Example B</span>do not cancel first: $g(x) = \dfrac{x^2 - 9}{x^2 - x - 6} = \dfrac{(x - 3)(x + 3)}{(x - 3)(x + 2)}$ is undefined at $x = 3$ <em>and</em> at <span class="nw">$x = -2$.</span> Canceling the $(x - 3)$ hides one of the two answers</div>
<div class="ref-ex"><span class="exlab">Example C</span>a polynomial has no restrictions: $f(x) = x^2 - 4x$ accepts every real number. “All real numbers” is a legitimate answer when nothing divides and nothing sits under a root</div>
<div class="ref-note">In Desmos, graph the function and look for the gap: a vertical asymptote or a hole for a fraction, a left or right edge for a root. Then confirm with the algebra; the test wants the exact value.</div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 3</span><span class="rname">Composition: one function feeds another</span></div>
<p class="ref-lead">$g(f(x))$ means evaluate $f$ first, then send its output into <span class="nw">$g$.</span> Work from the inside out. The SAT writes composition three ways: as nested parentheses, as a new function defined from an old one <span class="nw">($g(x) = 3f(x) - 2$),</span> and as a graph of $f$ with a question about <span class="nw">$g$.</span></p>
<div class="fig-slot" data-fig="compose"></div>
<div class="fbox">
<div class="frow"><div class="flabel">inside first</div><div class="fmath"><span class="nw">$g(f(2))$:</span> find <span class="nw">$f(2)$,</span> then plug that number into $g$</div></div>
<div class="frow"><div class="flabel">with a formula</div><div class="fmath">$g(f(x))$ is $g$ with every $x$ replaced by $f(x)$</div></div>
<div class="frow"><div class="flabel">defined from another</div><div class="fmath">$g(x) = 3f(x) - 2$ means <span class="nw">$g(5) = 3f(5) - 2$:</span> the input passes straight through to $f$</div></div>
<div class="frow"><div class="flabel">order matters</div><div class="fmath">$g(f(x))$ and $f(g(x))$ are usually different functions</div></div>
</div>
<div class="ref-ex"><span class="exlab">Example A</span>$f(x) = 2x + 1$ and <span class="nw">$g(x) = x^2 - 3$:</span> $g(f(2)) = g(5) = 22$, but <span class="nw">$f(g(2)) = f(1) = 3$</span></div>
<div class="ref-ex"><span class="exlab">Example B</span>$f(x) = 4x - 3$ and <span class="nw">$g(x) = 2f(x) + 5$.</span> If <span class="nw">$g(k) = 0$:</span> $2(4k - 3) + 5 = 8k - 1 = 0$, so <span class="nw">$k = \tfrac{1}{8}$.</span> Write $g$ out in terms of $x$ first: $g(x) = 8x - 1$</div>
<div class="ref-ex"><span class="exlab">Example C</span>from a graph: if $g(x) = 2f(x) - 1$ and the question asks how many $k$ have <span class="nw">$g(k) = 5$,</span> translate it into $f(k) = 3$ and count how many times the graph of $f$ meets the line $y = 3$</div>
<div class="ref-note">The trap is direction: $g(f(2))$ starts with <span class="nw">$f$.</span> Say it as “$g$ of $f$ of <span class="nw">$2$,”</span> and do the innermost thing first, every time.</div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 4</span><span class="rname">Equations that are true for every $x$</span></div>
<p class="ref-lead">Most equations are true for one or two values of <span class="nw">$x$.</span> An identity is true for all of them, which means the two sides are the same expression in disguise. Match the coefficients term by term: the $x^2$ terms agree, the $x$ terms agree, the constants agree. Each match is a small equation in the unknown constants.</p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>What the question says</th><th>What it means</th><th>The move</th></tr></thead><tbody>
<tr><td class="fname">“true for all values of $x$”</td><td class="">the two sides are identical expressions</td><td class="">match the coefficients</td></tr>
<tr><td class="fname">“infinitely many solutions”</td><td class="">the same thing, phrased as a solution count (Rule 5 of the linear sheet)</td><td class="">match the coefficients, constants included</td></tr>
<tr><td class="fname">“for what value of $x$”</td><td class="">an ordinary equation, true for one input</td><td class="">solve for <span class="nw">$x$;</span> this is not an identity</td></tr>
</tbody></table></div>
<div class="fbox">
<div class="frow"><div class="flabel">linear identity</div><div class="fmath">$ax + b = cx + d$ for all $x$ &nbsp;means&nbsp; $a = c$ and $b = d$</div></div>
<div class="frow"><div class="flabel">quadratic identity</div><div class="fmath">$ax^2 + bx + c = 0$ for all $x$ &nbsp;means&nbsp; $a = b = c = 0$</div></div>
<div class="frow"><div class="flabel">expand first</div><div class="fmath">$a(x + 2) + b(x - 1) = (a + b)\,x + (2a - b)$</div></div>
<div class="frow"><div class="flabel">shortcut</div><div class="fmath">plug in two easy values of $x$ (the ones that zero out a factor) to get two equations in the constants</div></div>
</div>
<div class="ref-ex"><span class="exlab">Example A</span>$(k - 3)x + 2 = 4x + m$ for all <span class="nw">$x$:</span> $k - 3 = 4$ and <span class="nw">$2 = m$,</span> so $k = 7$ and $m = 2$</div>
<div class="ref-ex"><span class="exlab">Example B</span>$a(x + 2) + b(x - 1) = 5x + 1$ for all <span class="nw">$x$:</span> expand to <span class="nw">$(a + b)x + (2a - b) = 5x + 1$.</span> Then $a + b = 5$ and <span class="nw">$2a - b = 1$;</span> add them: <span class="nw">$3a = 6$,</span> so $a = 2$ and $b = 3$</div>
<div class="ref-ex"><span class="exlab">Example C</span>the shortcut on Example B: $x = 1$ makes the $b$ term vanish and gives $3a = 6$ at once; $x = -2$ makes the $a$ term vanish and gives <span class="nw">$-3b = -9$</span></div>
<div class="ref-note">If a question says “true for all $x$” and you find yourself solving for <span class="nw">$x$,</span> stop. $x$ is not the unknown; the constants are.</div>
</div>
<div class="ref-rule ess"><div class="ref-rule-line"><span class="rtag"><span class="star">&#9733;</span>Rule 5</span><span class="rname">Shifting a graph: translations</span></div>
<p class="ref-lead">Adding outside the function moves the graph up or down. Adding inside the parentheses moves it left or right, and the direction runs backwards from the sign: $f(x - 3)$ is the graph of $f$ moved $3$ to the <em>right</em>. The shape never changes; every point slides by the same amount.</p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Move</th><th>New function</th><th>Effect on a point $(a, b)$</th><th>From $f(x) = x^2$</th></tr></thead><tbody>
<tr><td class="fname">up $k$</td><td class="">$f(x) + k$</td><td class="">$(a, b + k)$</td><td class="">$x^2 + 2$</td></tr>
<tr><td class="fname">down $k$</td><td class="">$f(x) - k$</td><td class="">$(a, b - k)$</td><td class="">$x^2 - 2$</td></tr>
<tr><td class="fname">right $h$</td><td class="">$f(x - h)$</td><td class="">$(a + h, b)$</td><td class="">$(x - 3)^2$</td></tr>
<tr><td class="fname">left $h$</td><td class="">$f(x + h)$</td><td class="">$(a - h, b)$</td><td class="">$(x + 3)^2$</td></tr>
<tr><td class="fname">both</td><td class="">$f(x - h) + k$</td><td class="">$(a + h, b + k)$</td><td class=""><span class="nw">$(x - 3)^2 + 2$:</span> right <span class="nw">$3$,</span> up $2$</td></tr>
</tbody></table></div>
<div class="fig-slot" data-fig="shift"></div>
<div class="ref-ex"><span class="exlab">Example A</span>$y = 4x - 1$ shifted $2$ left and $3$ up: replace $x$ with <span class="nw">$x + 2$,</span> then add <span class="nw">$3$:</span> $y = 4(x + 2) - 1 + 3 = 4x + 10$. The slope never changes; a shifted line is a parallel line</div>
<div class="ref-ex"><span class="exlab">Example B</span>“Which transformation turns $y = x^2$ into <span class="nw">$y = x^2 + 6x + 2$?”</span> Complete the square: <span class="nw">$(x + 3)^2 - 7$.</span> Left <span class="nw">$3$,</span> down $7$</div>
<div class="ref-ex"><span class="exlab">Example C</span>if $(3, 7)$ is on the graph of <span class="nw">$f$,</span> then $(5, 8)$ is on the graph of <span class="nw">$f(x - 2) + 1$:</span> add $2$ to the input and $1$ to the output. A table of $f$ shifts the same way, one column at a time</div>
<div class="ref-note">Desmos checks this directly: define $f(x) = x^2$ on one line, type $g(x) = f(x - 3) + 2$ on the next, and compare the two graphs. Function notation works in Desmos exactly as it does on paper.</div>
</div>
<div class="ref-rule"><div class="ref-rule-line"><span class="rtag">Rule 6</span><span class="rname">Range: the outputs a function can reach</span></div>
<p class="ref-lead">The domain is the set of inputs; the range is the set of outputs, read up the $y$-axis. Find the lowest or highest value the rule can produce. A square root starts at zero, a square starts at zero, and whatever is added afterward shifts the whole range by that much.</p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Function</th><th>Range</th><th>Why</th><th></th></tr></thead><tbody>
<tr><td class="fname">$f(x) = mx + b$, &nbsp;$m \neq 0$</td><td class="">all real numbers</td><td class="">a line keeps going in both directions</td><td class=""><span class="fig-slot" data-fig="rng_line"></span></td></tr>
<tr><td class="fname">$f(x) = a(x - h)^2 + k$, &nbsp;$a > 0$</td><td class="">$y \geq k$</td><td class="">the vertex is the lowest point</td><td class=""><span class="fig-slot" data-fig="rng_up"></span></td></tr>
<tr><td class="fname">$f(x) = a(x - h)^2 + k$, &nbsp;$a < 0$</td><td class="">$y \leq k$</td><td class="">the vertex is the highest point</td><td class=""><span class="fig-slot" data-fig="rng_down"></span></td></tr>
<tr><td class="fname">$f(x) = \sqrt{x - h} + k$</td><td class="">$y \geq k$</td><td class="">the root is $0$ or more, so the output is $k$ or more</td><td class=""><span class="fig-slot" data-fig="rng_root"></span></td></tr>
</tbody></table></div>
<div class="fig-slot" data-fig="range"></div>
<div class="ref-ex"><span class="exlab">Example A</span><span class="nw">$f(x) = \sqrt{x + 1} - 4$:</span> domain $x \geq -1$ (the radicand), range $y \geq -4$ (the smallest root is <span class="nw">$0$,</span> at <span class="nw">$x = -1$).</span> The $1$ belongs to the domain and the $4$ to the range</div>
<div class="ref-ex"><span class="exlab">Example B</span>$f(x) = -(x - 1)^2 + 4$ opens down with vertex <span class="nw">$(1, 4)$:</span> range <span class="nw">$y \leq 4$.</span> The maximum value is $4$ (the <span class="nw">$k$),</span> and it occurs at $x = 1$ (the $h$)</div>
<div class="ref-ex"><span class="exlab">Example C</span>from a graph with endpoints, the range runs from the lowest point drawn to the highest, ends included: the graph in Rule 1 runs from $y = -2$ up to <span class="nw">$y = 3$,</span> so its range is $-2 \leq y \leq 3$</div>
<div class="ref-note">Rare as a question on its own, but it hides inside others: “the minimum value of $f$” and “$f(x) = c$ has no solution” are both range questions.</div>
</div>
<hr class="ref-divider"><div class="ref-h">Common SAT traps and how to avoid them</div>
<p>Each move below looks reasonable, is wrong, and produces a wrong answer that sits waiting in the choices. Learn to recognize these now, so you can sidestep them under time pressure.</p>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 1</span><span class="rname">canceling a common factor before reading the domain</span></div><div class="ref-ex">$\dfrac{(x - 3)(x + 3)}{(x - 3)(x + 2)}$ is undefined at $3$ <em>and</em> at <span class="nw">$-2$.</span> List the restrictions first; cancel afterward, never before.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 2</span><span class="rname">composing in the wrong order</span></div><div class="ref-ex">$g(f(2))$ means $f$ first. With $f(x) = 2x + 1$ and <span class="nw">$g(x) = x^2 - 3$,</span> $g(f(2)) = 22$ and <span class="nw">$f(g(2)) = 3$.</span> Both numbers are in the choices.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 3</span><span class="rname">shifting left by writing $(x - 3)$</span></div><div class="ref-ex">Left $3$ is <span class="nw">$f(x + 3)$.</span> Check with one point: $(x + 3)^2$ is zero at <span class="nw">$x = -3$,</span> which is where the vertex of $x^2$ lands after a move to the left.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 4</span><span class="rname">solving an identity for $x$</span></div><div class="ref-ex">“True for all values of $x$” means match the coefficients. A single value of $x$ is never the answer to that question; the constants are.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 5</span><span class="rname">reading the domain off the numerator only</span></div><div class="ref-ex">$\dfrac{\sqrt{x}}{x - 7}$ needs $x \geq 0$ from the root <em>and</em> $x \neq 7$ from the denominator. The choice that states only one of the two conditions is the trap.</div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 6</span><span class="rname">$f(x + 1)$ is not $f(x) + 1$</span></div><div class="ref-ex">Inside the parentheses means replace every <span class="nw">$x$.</span> For <span class="nw">$f(x) = x^2$,</span> $f(x + 1) = x^2 + 2x + 1$ while <span class="nw">$f(x) + 1 = x^2 + 1$.</span></div></div>
<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Trap 7</span><span class="rname">putting the horizontal shift into the range</span></div><div class="ref-ex">$\sqrt{x - 6} - 3$ has range <span class="nw">$y \geq -3$.</span> The $6$ sets where the domain starts; the $-3$ sets where the range starts.</div></div>
'''

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Input, output, point",
  "rule": r"$f(a) = c$ &nbsp;means the point&nbsp; $(a, c)$ &nbsp;·&nbsp; evaluate by replacing every $x$",
  "say": r"Function notation is a translation exercise. $f(-2)$ says replace every $x$ with $-2$ and compute. $f(a) = 12$ says the output is $12$ and the input is the unknown, so it is an equation to solve. On a graph those are the same fact seen two ways: the point $(a, 12)$ is on the curve.",
  "prob": r"The function $f$ is defined by <span class=\"nw\">$f(x) = x^2 - 4x$.</span> What is the value of <span class=\"nw\">$f(-2)$?</span> For what positive value of $a$ is <span class=\"nw\">$f(a) = 12$?</span>",
  "sol": r"<strong>Step 1: evaluate.</strong> $f(-2) = (-2)^2 - 4(-2) = 4 + 8 = 12$.<br><strong>Step 2: solve.</strong> $a^2 - 4a = 12$ gives <span class=\"nw\">$a^2 - 4a - 12 = 0$,</span> so <span class=\"nw\">$(a - 6)(a + 2) = 0$</span> and the positive value is <span class=\"nw\">$a = 6$.</span><br><strong>Read the rest for free:</strong> $f(-2) = 12$ and $f(6) = 12$ are two points at the same height, symmetric about <span class=\"nw\">$x = 2$,</span> the axis of this parabola.",
  "trap": r"Squaring the sign away. $(-2)^2 = 4$, and then $-4(-2) = +8$. Two sign slips produce $-4$ or <span class=\"nw\">$4$,</span> and both sit in the choices. Write the substitution with parentheses around every $-2$.",
  "micro": {"q": r"If <span class=\"nw\">$f(x) = 3x^2 - 2$,</span> then $f(-2) =$", "accept": ["10"],
            "exp": r"$3(-2)^2 - 2 = 3(4) - 2 = 10$. Square before multiplying by the <span class=\"nw\">$3$.</span>"}},
 {"ess": True, "name": "Rule 1, continued: Read the graph",
  "rule": r"$f(a) = c$ is the point $(a, c)$ &nbsp;·&nbsp; the solutions of $f(x) = c$ are the crossings of $y = c$",
  "say": r"A graph is a picture of every input-output pair. To find <span class=\"nw\">$f(1)$,</span> go to $x = 1$ and read the height. To solve <span class=\"nw\">$f(x) = 1$,</span> draw the horizontal line $y = 1$ and count the points where it meets the graph; each one is a solution. The SAT asks for the count more often than for the values.",
  "fig": "g_read",
  "prob": r"The graph of $y = f(x)$ is shown in the $xy$-plane above for <span class=\"nw\">$-4 \leq x \leq 5$.</span> What is the value of <span class=\"nw\">$f(1)$?</span> For how many values of $x$ does <span class=\"nw\">$f(x) = 1$?</span>",
  "sol": r"<strong>Step 1: read $f(1)$.</strong> At $x = 1$ the graph is at height <span class=\"nw\">$2$:</span> <span class=\"nw\">$f(1) = 2$.</span><br><strong>Step 2: count the crossings of $y = 1$.</strong> The line meets the graph three times: on the way down (near <span class=\"nw\">$x = -3.2$),</span> on the way up (near <span class=\"nw\">$x = 0.3$),</span> and on the way down again (at <span class=\"nw\">$x = 2$).</span> The last piece, from $(3, 0)$ to <span class=\"nw\">$(5, 0.5)$,</span> never climbs back to <span class=\"nw\">$1$.</span> Three values.",
  "trap": r"Reading $f(1)$ as “the $x$ where the graph is at height <span class=\"nw\">$1$,”</span> which is the reverse question. Input is horizontal, output is vertical, always.",
  "micro": {"mc": True, "q": r"Using the same graph, for how many values of $x$ is <span class=\"nw\">$f(x) = 2$?</span>",
            "opts": ["One", "Two", "Three", "Four"], "correct": 1,
            "exp": r"The line $y = 2$ crosses the first piece once (between $x = -4$ and <span class=\"nw\">$x = -2$)</span> and touches the peak at <span class=\"nw\">$(1, 2)$:</span> two values. A peak that just touches the line counts once."}},
 {"ess": True, "name": "Rule 2: Where a fraction is undefined",
  "rule": r"$\dfrac{P(x)}{Q(x)}$ is undefined wherever $Q(x) = 0$",
  "say": r"Set the denominator equal to zero and solve; every solution is a value where the function is undefined. When the denominator repeats a chunk like <span class=\"nw\">$(x - 2)$,</span> substitute one letter for the chunk, factor the simpler quadratic, then translate back to <span class=\"nw\">$x$.</span>",
  "prob": r"$$h(x) = \dfrac{3}{(x - 2)^2 - 3(x - 2) - 10}$$ For what values of $x$ is the function $h$ above undefined?",
  "sol": r"<strong>Step 1: substitute.</strong> Let <span class=\"nw\">$u = x - 2$,</span> so the denominator is <span class=\"nw\">$u^2 - 3u - 10$.</span><br><strong>Step 2: factor.</strong> $(u - 5)(u + 2) = 0$, so $u = 5$ or <span class=\"nw\">$u = -2$.</span><br><strong>Step 3: back to $x$.</strong> $x - 2 = 5$ gives <span class=\"nw\">$x = 7$;</span> $x - 2 = -2$ gives <span class=\"nw\">$x = 0$.</span> Check: at $x = 0$ the denominator is $4 + 6 - 10 = 0$. ✓",
  "trap": r"Stopping at $u = 5$ and <span class=\"nw\">$u = -2$.</span> Those are values of <span class=\"nw\">$x - 2$,</span> not of <span class=\"nw\">$x$.</span> The last step, adding the $2$ back, is where the point is lost.",
  "micro": {"q": r"The largest value of $x$ at which $\dfrac{1}{x^2 - 5x + 6}$ is undefined is $x =$", "accept": ["3"],
            "exp": r"$x^2 - 5x + 6 = (x - 2)(x - 3) = 0$ at $x = 2$ and <span class=\"nw\">$x = 3$.</span> The larger is <span class=\"nw\">$3$.</span>"}},
 {"ess": True, "name": "Rule 2, continued: Roots and combined domains",
  "rule": r"$\sqrt{R(x)}$ needs $R(x) \geq 0$ &nbsp;·&nbsp; a fraction needs $Q(x) \neq 0$ &nbsp;·&nbsp; both can apply at once",
  "say": r"A square root needs a radicand of zero or more; solve that inequality. When a root sits over a denominator, both rules apply, and the correct choice is the one that states both conditions. When the root <em>is</em> the denominator, zero is excluded too, so the inequality becomes strict.",
  "prob": r"$$f(x) = \dfrac{\sqrt{x + 4}}{x - 1}$$ Which of the following represents the domain of the function $f$ above? &nbsp; (A) $x \geq -4$ &nbsp; (B) $x \neq 1$ &nbsp; (C) $x \geq -4$ and $x \neq 1$ &nbsp; (D) $x > -4$ and $x \neq 1$",
  "sol": r"<strong>The root:</strong> $x + 4 \geq 0$, so <span class=\"nw\">$x \geq -4$.</span><br><strong>The denominator:</strong> $x - 1 \neq 0$, so <span class=\"nw\">$x \neq 1$.</span><br><strong>Both:</strong> choice C. Choice D throws out $x = -4$ for no reason: $\sqrt{0} = 0$ is a perfectly good numerator.",
  "trap": r"Choices A and B each state one true condition, and a true condition is not the domain. Scan every choice for the word “and” before you commit.",
  "micro": {"mc": True, "q": r"The domain of $\dfrac{\sqrt{3x - 9}}{x - 5}$ is",
            "opts": [r"$x \geq 3$", r"$x \neq 5$", r"$x \geq 3$ and $x \neq 5$", r"$x > 3$ and $x \neq 5$"], "correct": 2,
            "exp": r"$3x - 9 \geq 0$ gives <span class=\"nw\">$x \geq 3$;</span> the denominator adds <span class=\"nw\">$x \neq 5$.</span> The root is in the numerator, so $x = 3$ stays in."}},
 {"ess": True, "name": "Rule 3: Composition, inside out",
  "rule": r"$g(f(x))$: do $f$ first &nbsp;·&nbsp; $g(x) = 2f(x) + k$: the input passes through to $f$",
  "say": r"When one function is defined in terms of another, write the new one out in terms of $x$ before plugging anything in. $g(x) = 2f(x) + k$ with $f(x) = 4x - 3$ is <span class=\"nw\">$g(x) = 8x - 6 + k$,</span> a line with an unknown intercept. One given value of $g$ pins the unknown down.",
  "prob": r"The functions $f$ and $g$ are defined by $f(x) = 4x - 3$ and <span class=\"nw\">$g(x) = 2f(x) + k$,</span> where $k$ is a constant. If <span class=\"nw\">$g(3) = 25$,</span> what is the value of <span class=\"nw\">$k$?</span>",
  "sol": r"<strong>Step 1: $f$ first.</strong> $f(3) = 12 - 3 = 9$.<br><strong>Step 2: then $g$.</strong> $g(3) = 2 \cdot 9 + k = 18 + k$.<br><strong>Step 3: use the given value.</strong> $18 + k = 25$, so <span class=\"nw\">$k = 7$.</span><br><strong>Same thing with the formula:</strong> $g(x) = 8x - 6 + k$, and $g(3) = 24 - 6 + k = 18 + k$. ✓",
  "trap": r"Plugging $3$ into $g$ as if $g(x) = 2x + k$. The $f$ in the definition is not decoration: $2(3) + k = 25$ gives <span class=\"nw\">$k = 19$,</span> which is sitting in the choices.",
  "micro": {"q": r"If $f(x) = 2x + 1$ and <span class=\"nw\">$g(x) = x^2 - 3$,</span> then $g(f(2)) =$", "accept": ["22"],
            "exp": r"$f(2) = 5$, then <span class=\"nw\">$g(5) = 25 - 3 = 22$.</span> (The other order, <span class=\"nw\">$f(g(2)) = f(1) = 3$.)</span>"}},
 {"ess": True, "name": "Rule 3, continued: Composition on a graph",
  "rule": r"translate $g(k) = c$ into $f(k) = $ a number &nbsp;·&nbsp; then count the crossings",
  "say": r"When $g$ is defined from $f$ and only $f$ is graphed, rewrite the question about $g$ as a question about <span class=\"nw\">$f$.</span> $g(k) = 5$ with $g(x) = 2f(x) - 1$ becomes <span class=\"nw\">$2f(k) - 1 = 5$,</span> so <span class=\"nw\">$f(k) = 3$.</span> Now it is Rule 1: count how many times the graph of $f$ meets the line <span class=\"nw\">$y = 3$.</span>",
  "fig": "g_comp",
  "prob": r"The graph of $y = f(x)$ is shown in the $xy$-plane above for <span class=\"nw\">$-4 \leq x \leq 6$.</span> The function $g$ is defined by <span class=\"nw\">$g(x) = 2f(x) - 1$.</span> For how many values of $k$ is <span class=\"nw\">$g(k) = 5$?</span> &nbsp; (A) Two &nbsp; (B) Three &nbsp; (C) Four &nbsp; (D) Five",
  "sol": r"<strong>Step 1: translate.</strong> $2f(k) - 1 = 5$ gives <span class=\"nw\">$f(k) = 3$.</span><br><strong>Step 2: count.</strong> The line $y = 3$ meets the graph four times: on the way up to <span class=\"nw\">$(-1, 4)$,</span> on the way down to <span class=\"nw\">$(1, 2)$,</span> on the way up to <span class=\"nw\">$(3, 5)$,</span> and on the way down to <span class=\"nw\">$(6, 1)$.</span> Choice C.",
  "trap": r"Counting the crossings of $y = 5$ (the number in the question) instead of $y = 3$ (the number after the translation). The graph only reaches $5$ once, and “One” is not even offered; that missing choice is the test's hint that a step was skipped.",
  "micro": {"mc": True, "q": r"Using the same graph, for how many values of $x$ is <span class=\"nw\">$f(x) = 4$?</span>",
            "opts": ["One", "Two", "Three", "Four"], "correct": 2,
            "exp": r"$y = 4$ touches the peak at <span class=\"nw\">$(-1, 4)$,</span> then crosses on the way up to $(3, 5)$ and again on the way down: three values."}},
 {"ess": True, "name": "Rule 4: True for all values of $x$",
  "rule": r"$ax + b = cx + d$ for all $x$ &nbsp;means&nbsp; $a = c$ and $b = d$",
  "say": r"An equation that holds for every $x$ has identical sides. Expand both sides, collect like terms, and set the matching coefficients equal: the $x$ terms give one equation and the constants give another. Two unknown constants need two matches, and the result is a small system.",
  "prob": r"$$a(x + 2) + b(x - 1) = 5x + 1$$ In the equation above, $a$ and $b$ are constants. If the equation is true for all values of <span class=\"nw\">$x$,</span> what is the value of <span class=\"nw\">$a$?</span>",
  "sol": r"<strong>Step 1: expand.</strong> $ax + 2a + bx - b = (a + b)\,x + (2a - b)$.<br><strong>Step 2: match.</strong> $x$ terms: <span class=\"nw\">$a + b = 5$.</span> Constants: <span class=\"nw\">$2a - b = 1$.</span><br><strong>Step 3: solve.</strong> Add the two equations: <span class=\"nw\">$3a = 6$,</span> so $a = 2$ (and <span class=\"nw\">$b = 3$).</span> Check: $2(x + 2) + 3(x - 1) = 5x + 1$. ✓<br><strong>Shortcut:</strong> set $x = 1$ to kill the $b$ term: $3a = 6$ in one line.",
  "trap": r"Treating it as an equation in $x$ and “solving” to get $x$ in terms of $a$ and <span class=\"nw\">$b$.</span> The phrase “for all values of $x$” is the signal: $x$ is not the unknown.",
  "micro": {"q": r"If $(k + 2)x = 7x$ for all values of <span class=\"nw\">$x$,</span> then $k =$", "accept": ["5"],
            "exp": r"The $x$ coefficients must match: <span class=\"nw\">$k + 2 = 7$,</span> so <span class=\"nw\">$k = 5$.</span> Dividing both sides by $x$ gets there too, but only because this one has no constant term."}},
 {"ess": True, "name": "Rule 5: Shift the graph",
  "rule": r"$f(x - h) + k$: right $h$, up $k$ &nbsp;·&nbsp; every point $(a, b)$ moves to $(a + h, b + k)$",
  "say": r"Inside the parentheses moves the graph sideways, backwards from the sign; outside moves it vertically, with the sign. To write the shifted function, replace $x$ with $x - h$ and add <span class=\"nw\">$k$.</span> To shift a point or a table, add $h$ to the input and $k$ to the output.",
  "fig": "shift",
  "prob": r"The graph of $g$ is the graph of $f(x) = x^2$ shifted $3$ units to the right and $2$ units up, as shown above. What is the equation of <span class=\"nw\">$g$,</span> and what is the $y$-intercept of its graph?",
  "sol": r"<strong>Step 1: write $g$.</strong> $g(x) = f(x - 3) + 2 = (x - 3)^2 + 2$.<br><strong>Step 2: expand if the choices are in standard form.</strong> $x^2 - 6x + 9 + 2 = x^2 - 6x + 11$.<br><strong>Step 3: the $y$-intercept.</strong> $g(0) = 9 + 2 = 11$.<br><strong>Check with the vertex:</strong> $(0, 0)$ moved to <span class=\"nw\">$(3, 2)$,</span> and $(x - 3)^2 + 2$ is smallest at $x = 3$ with value <span class=\"nw\">$2$.</span> ✓",
  "trap": r"Writing $(x + 3)^2 + 2$ for a shift to the right. Test it with the vertex: $(x + 3)^2$ is zero at <span class=\"nw\">$x = -3$,</span> which is a shift to the left. One substitution settles the direction.",
  "micro": {"q": r"The graph of $y = f(x)$ passes through <span class=\"nw\">$(3, 7)$.</span> The graph of $y = f(x - 2) + 1$ passes through <span class=\"nw\">$(a, b)$.</span> Then $a + b =$", "accept": ["13"],
            "exp": r"Right $2$ and up <span class=\"nw\">$1$:</span> $(3, 7)$ becomes <span class=\"nw\">$(5, 8)$,</span> so <span class=\"nw\">$a + b = 13$.</span>"}},
 {"ess": False, "name": "Rule 6: Range",
  "rule": r"range $=$ the outputs &nbsp;·&nbsp; a root or a square starts at $0$; the constant added outside moves the start",
  "say": r"The range is read up the $y$-axis: the lowest output to the highest. A square root and a square can never be negative, so the least they contribute is <span class=\"nw\">$0$;</span> whatever is added outside sets the floor (or, with a leading minus sign, the ceiling). The horizontal shift has no effect on the range.",
  "fig": "range",
  "prob": r"The function $f$ is defined by <span class=\"nw\">$f(x) = \sqrt{x + 1} - 4$.</span> What are the domain and the range of <span class=\"nw\">$f$?</span>",
  "sol": r"<strong>Domain:</strong> $x + 1 \geq 0$, so <span class=\"nw\">$x \geq -1$.</span><br><strong>Range:</strong> $\sqrt{x + 1}$ is $0$ or more, so $f(x)$ is $-4$ or more: <span class=\"nw\">$y \geq -4$.</span><br><strong>The picture:</strong> the graph starts at $(-1, -4)$ and rises forever. Domain to the right of <span class=\"nw\">$-1$,</span> range above <span class=\"nw\">$-4$.</span>",
  "trap": r"Mixing the two numbers up. The $1$ is a domain number (it moves the start to the left) and the $4$ is a range number (it moves the start down). $y \geq -1$ is the standard wrong answer.",
  "micro": {"q": r"The range of $f(x) = \sqrt{x + 3} - 7$ is $y \geq$", "accept": ["-7"],
            "exp": r"The root is $0$ at <span class=\"nw\">$x = -3$,</span> so the smallest output is <span class=\"nw\">$0 - 7 = -7$.</span>"}},
]
LAST_STARRED_STEP_INDEX = 7  # 0-based index of the last starred step (Rule 5)

# ---------------------------------------------------------------- TAB 3: FLUENCY
FLUENCY = [
 {"sec": "A. Evaluate and read", "items": [
   {"q": r"If <span class=\"nw\">$f(x) = x^2 - 4x$,</span> then $f(-3) =$", "accept": ["21"], "exp": r"$(-3)^2 - 4(-3) = 9 + 12 = 21$."},
   {"q": r"If $f(x) = 2x + 5$ and <span class=\"nw\">$f(a) = 17$,</span> then $a =$", "accept": ["6"], "exp": r"$2a + 5 = 17$, so <span class=\"nw\">$a = 6$.</span> The $17$ is the output; the input is the unknown."},
   {"q": r"The table gives four values of the function <span class=\"nw\">$f$.</span><table class='vtab'><tr><th>$x$</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$3$</td></tr><tr><th>$f(x)$</th><td>$5$</td><td>$3$</td><td>$8$</td><td>$1$</td></tr></table>The value of $x$ for which $f(x) = 3$ is $x =$", "accept": ["1"], "exp": r"Find $3$ in the output row; its input is <span class=\"nw\">$1$.</span> ($f(1) = 3$ is the point <span class=\"nw\">$(1, 3)$.)</span>"},
   {"q": r"If $f(4) = 2$ and <span class=\"nw\">$g(x) = 3f(x) - 1$,</span> then $g(4) =$", "accept": ["5"], "exp": r"$g(4) = 3f(4) - 1 = 3(2) - 1 = 5$."},
 ]},
 {"sec": "B. Domain and undefined", "items": [
   {"q": r"The larger value of $x$ at which $\dfrac{5}{x^2 - 9}$ is undefined is $x =$", "accept": ["3"], "exp": r"$x^2 - 9 = (x - 3)(x + 3) = 0$ at $x = 3$ and <span class=\"nw\">$x = -3$.</span>"},
   {"q": r"The smallest value of $x$ in the domain of $f(x) = \sqrt{x - 7}$ is $x =$", "accept": ["7"], "exp": r"$x - 7 \geq 0$. At $x = 7$ the root is <span class=\"nw\">$\sqrt{0} = 0$,</span> which is allowed."},
   {"mc": True, "q": r"The domain of $f(x) = \dfrac{\sqrt{x + 1}}{x - 4}$ is", "opts": [r"$x \geq -1$", r"$x \neq 4$", r"$x \geq -1$ and $x \neq 4$", r"$x > -1$ and $x \neq 4$"], "correct": 2, "exp": r"Root: <span class=\"nw\">$x \geq -1$.</span> Denominator: <span class=\"nw\">$x \neq 4$.</span> Both conditions, and $x = -1$ stays in because the root is upstairs."},
   {"q": r"The negative value of $x$ at which $\dfrac{x - 2}{(x - 2)(x + 5)}$ is undefined is $x =$", "accept": ["-5"], "exp": r"Both factors of the denominator count, even the one that would cancel: undefined at $x = 2$ and <span class=\"nw\">$x = -5$.</span>"},
 ]},
 {"sec": "C. Composition and identities", "items": [
   {"q": r"If $f(x) = x - 3$ and <span class=\"nw\">$g(x) = x^2$,</span> then $g(f(5)) =$", "accept": ["4"], "exp": r"$f(5) = 2$, then <span class=\"nw\">$g(2) = 4$.</span> (The other order: <span class=\"nw\">$f(g(5)) = 25 - 3 = 22$.)</span>"},
   {"q": r"If $f(x) = 4x - 1$ and <span class=\"nw\">$g(x) = 2f(x) + 3$,</span> then $g(2) =$", "accept": ["17"], "exp": r"$f(2) = 7$, so <span class=\"nw\">$g(2) = 2(7) + 3 = 17$.</span>"},
   {"q": r"If $(a - 1)x + 6 = 5x + b$ for all values of <span class=\"nw\">$x$,</span> then $a + b =$", "accept": ["12"], "exp": r"Match: $a - 1 = 5$ gives <span class=\"nw\">$a = 6$;</span> the constants give <span class=\"nw\">$b = 6$.</span> Sum <span class=\"nw\">$12$.</span>"},
   {"q": r"If $2(x + 3) = ax + b$ for all values of <span class=\"nw\">$x$,</span> then $a + b =$", "accept": ["8"], "exp": r"$2x + 6 = ax + b$: $a = 2$ and <span class=\"nw\">$b = 6$.</span>"},
 ]},
 {"sec": "D. Shifts and range", "items": [
   {"q": r"The graph of $y = 3x - 5$ is shifted $2$ units to the left and $4$ units up. The $y$-intercept of the new graph is $y =$", "accept": ["5"], "exp": r"$y = 3(x + 2) - 5 + 4 = 3x + 5$. Left means $x + 2$ inside."},
   {"q": r"The graph of $y = x^2$ is shifted $5$ units to the right. The vertex of the new graph is at $x =$", "accept": ["5"], "exp": r"$y = (x - 5)^2$, vertex <span class=\"nw\">$(5, 0)$.</span> Right means minus inside."},
   {"mc": True, "q": r"The graph of $y = x^2 + 2x + 7$ is the graph of $y = x^2$ shifted", "opts": ["$1$ unit left and $6$ units up", "$1$ unit right and $6$ units up", "$2$ units left and $7$ units up", "$1$ unit left and $7$ units up"], "correct": 0, "exp": r"Complete the square: $x^2 + 2x + 1 + 6 = (x + 1)^2 + 6$. The $7$ is the $y$-intercept, not the vertical shift."},
   {"q": r"The minimum value of $f(x) = \sqrt{x - 1} + 4$ is", "accept": ["4"], "exp": r"The root is $0$ at <span class=\"nw\">$x = 1$,</span> so the smallest output is <span class=\"nw\">$0 + 4 = 4$.</span> Range <span class=\"nw\">$y \geq 4$.</span>"},
 ]},
]

# ---------------------------------------------------------------- TAB 4: GAUNTLET
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"The function $f$ is defined by <span class=\"nw\">$f(x) = 2x^2 - 3x + 1$.</span> What is the value of <span class=\"nw\">$f(-2)$?</span>",
  "options": ["$-9$", "$3$", "$11$", "$15$"], "correct": 3,
  "desmos": ["f(x)=2x^2-3x+1", "f(-2)"],
  "sol": r"<strong>Given:</strong> a rule and an input.<br><br>Replace every $x$ with <span class=\"nw\">$(-2)$:</span> $2(-2)^2 - 3(-2) + 1 = 2(4) + 6 + 1 = 15$.",
  "trap": r"Choice B is <span class=\"nw\">$8 - 6 + 1$,</span> the sign of the middle term lost. Choice A squares before the sign, $-(2 \cdot 2)^2 + 6 + 1$. Parentheses around the $-2$ prevent both."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"The function $f$ is defined by <span class=\"nw\">$f(x) = 5x + 2$.</span> For what value of $a$ is <span class=\"nw\">$f(a) = 37$?</span>",
  "label": "$a =$", "accept": ["7"], "desmos": ["y=5x+2", "y=37"],
  "sol": r"<strong>Given:</strong> the output; the input is the unknown.<br><br>$5a + 2 = 37$, so $5a = 35$ and <span class=\"nw\">$a = 7$.</span>",
  "trap": r"Computing $f(37) = 187$ answers the reverse question. $f(a) = 37$ puts the $37$ on the output side; the input is what you solve for."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"$$f(x) = \dfrac{\sqrt{x + 6}}{x - 2}$$ Which of the following represents the domain of the function $f$ above?",
  "options": [r"$x \geq -6$", r"$x \neq 2$", r"$x \geq -6$ and $x \neq 2$", r"$x > -6$ and $x \neq 2$"], "correct": 2,
  "desmos": ["y=\\frac{\\sqrt{x+6}}{x-2}"],
  "sol": r"<strong>Given:</strong> a root over a denominator, so two conditions.<br><br>Root: $x + 6 \geq 0$, so <span class=\"nw\">$x \geq -6$.</span> Denominator: <span class=\"nw\">$x \neq 2$.</span> Both together: choice C.",
  "trap": r"Choice D drops <span class=\"nw\">$x = -6$,</span> but $\sqrt{0} = 0$ is a perfectly good numerator. The strict inequality belongs only to a root in the denominator."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"$$h(x) = \dfrac{5}{(x - 2)^2 - 6(x - 2) + 8}$$ What is the greatest value of $x$ for which the function $h$ above is undefined?",
  "label": "$x =$", "accept": ["6"], "desmos": ["y=\\frac{5}{(x-2)^2-6(x-2)+8}"],
  "sol": r"<strong>Given:</strong> a repeated chunk in the denominator.<br><br>Let <span class=\"nw\">$u = x - 2$:</span> $u^2 - 6u + 8 = (u - 2)(u - 4) = 0$, so $u = 2$ or <span class=\"nw\">$u = 4$,</span> which is $x = 4$ or <span class=\"nw\">$x = 6$.</span> The greatest is <span class=\"nw\">$6$.</span> Check: $(6 - 2)^2 - 6(4) + 8 = 16 - 24 + 8 = 0$. ✓",
  "trap": r"Answering <span class=\"nw\">$4$,</span> the larger value of <span class=\"nw\">$u$.</span> The substitution has to be undone: $u = 4$ means <span class=\"nw\">$x - 2 = 4$.</span> In Desmos, the two vertical asymptotes sit at $4$ and <span class=\"nw\">$6$.</span>"},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"The functions $f$ and $g$ are defined by $f(x) = 4x + 1$ and <span class=\"nw\">$g(x) = 2f(x) - k$,</span> where $k$ is a constant. If <span class=\"nw\">$g(3) = 19$,</span> what is the value of <span class=\"nw\">$k$?</span>",
  "options": ["$7$", "$13$", "$26$", "$45$"], "correct": 0,
  "sol": r"<strong>Given:</strong> $g$ defined through <span class=\"nw\">$f$,</span> one value of $g$ known.<br><br>$f(3) = 13$, so <span class=\"nw\">$g(3) = 2(13) - k = 26 - k$.</span> Then $26 - k = 19$ gives <span class=\"nw\">$k = 7$.</span>",
  "trap": r"Choice B is $f(3)$ and choice C is <span class=\"nw\">$2f(3)$:</span> each a stop on the way, not the destination. Choice D adds the $19$ instead of subtracting."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"$$a(x + 2) + b(x - 3) = 7x + 4$$ In the equation above, $a$ and $b$ are constants. If the equation is true for all values of <span class=\"nw\">$x$,</span> what is the value of <span class=\"nw\">$a$?</span>",
  "label": "$a =$", "accept": ["5"],
  "sol": r"<strong>Given:</strong> true for all <span class=\"nw\">$x$,</span> so match coefficients.<br><br>Expand: <span class=\"nw\">$(a + b)\,x + (2a - 3b) = 7x + 4$.</span> So $a + b = 7$ and <span class=\"nw\">$2a - 3b = 4$.</span> From the first, <span class=\"nw\">$b = 7 - a$;</span> substitute: $2a - 21 + 3a = 4$, so $5a = 25$ and $a = 5$ (and <span class=\"nw\">$b = 2$).</span><br><strong>Shortcut:</strong> $x = 3$ kills the $b$ term: $5a = 25$.",
  "trap": r"Solving for <span class=\"nw\">$x$.</span> Two constants, two matches: the $x$ coefficients and the constants give the two equations you need, and $x$ never gets a value."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "g7",
  "stem": r"The graph of $y = f(x)$ is shown in the $xy$-plane above for <span class=\"nw\">$-4 \leq x \leq 6$.</span> The function $g$ is defined by <span class=\"nw\">$g(x) = 2f(x) - 1$.</span> For how many values of $k$ is <span class=\"nw\">$g(k) = 7$?</span>",
  "options": ["One", "Two", "Three", "Four"], "correct": 2,
  "sol": r"<strong>Given:</strong> only $f$ is graphed, so translate the question about <span class=\"nw\">$g$.</span><br><br>$2f(k) - 1 = 7$ gives <span class=\"nw\">$f(k) = 4$.</span> The line $y = 4$ meets the graph three times: coming down from <span class=\"nw\">$(-4, 5)$,</span> going up to <span class=\"nw\">$(1, 6)$,</span> and coming down to <span class=\"nw\">$(4, 2)$.</span> The last piece, from $(4, 2)$ to <span class=\"nw\">$(6, 3)$,</span> stays below <span class=\"nw\">$4$.</span> Three values.",
  "trap": r"Counting where the graph meets $y = 7$ (never, so the count is zero) and answering from the wrong line. The number in the question is a value of <span class=\"nw\">$g$;</span> it has to be converted before it touches the graph."},
 {"ess": True, "type": "mc", "diff": "Medium-hard", "fig": "g8",
  "stem": r"The graphs of $y = f(x)$ and $y = g(x)$ are shown in the $xy$-plane above. The vertex of the graph of $f$ is at $(0, -3)$ and the vertex of the graph of $g$ is at <span class=\"nw\">$(3, -1)$.</span> Which of the following defines $g$ in terms of <span class=\"nw\">$f$?</span>",
  "options": [r"$g(x) = f(x - 3) + 2$", r"$g(x) = f(x + 3) + 2$", r"$g(x) = f(x - 3) - 2$", r"$g(x) = f(x + 3) - 2$"], "correct": 0,
  "desmos": ["f(x)=x^2-3", "g(x)=f(x-3)+2"],
  "sol": r"<strong>Given:</strong> the same shape in two places, so track one point.<br><br>The vertex moved from $(0, -3)$ to <span class=\"nw\">$(3, -1)$:</span> $3$ to the right and $2$ up. Right $3$ is <span class=\"nw\">$f(x - 3)$;</span> up $2$ is <span class=\"nw\">$+\,2$.</span> $g(x) = f(x - 3) + 2$.",
  "trap": r"Choice B uses the sign inside the parentheses as written. A shift to the right subtracts inside; check with the vertex: $f(x - 3)$ is at its lowest when <span class=\"nw\">$x - 3 = 0$,</span> at <span class=\"nw\">$x = 3$.</span> ✓"},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"In the $xy$-plane, which of the following transformations of the graph of $y = x^2$ produces the graph of <span class=\"nw\">$y = x^2 - 6x + 11$?</span>",
  "options": ["Shift $3$ units to the right and $2$ units up", "Shift $3$ units to the left and $2$ units up", "Shift $3$ units to the right and $11$ units up", "Shift $6$ units to the left and $11$ units up"], "correct": 0,
  "desmos": ["y=x^2", "y=x^2-6x+11"],
  "sol": r"<strong>Given:</strong> standard form hides the shift; vertex form shows it.<br><br>Complete the square: $x^2 - 6x + 11 = (x - 3)^2 - 9 + 11 = (x - 3)^2 + 2$. That is <span class=\"nw\">$f(x - 3) + 2$:</span> right <span class=\"nw\">$3$,</span> up <span class=\"nw\">$2$.</span>",
  "trap": r"Reading the $11$ as the vertical shift. The $11$ is the $y$-intercept; the vertical shift is what is left after completing the square. In Desmos, graph both and watch the vertex move from $(0, 0)$ to <span class=\"nw\">$(3, 2)$.</span>"},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$(2x + a)(x - 3) = 2x^2 + bx - 15$$ In the equation above, $a$ and $b$ are constants. If the equation is true for all values of <span class=\"nw\">$x$,</span> what is the value of <span class=\"nw\">$b$?</span>",
  "label": "$b =$", "accept": ["-1"],
  "sol": r"<strong>Given:</strong> an identity with two unknown constants.<br><br>Expand: $2x^2 - 6x + ax - 3a = 2x^2 + (a - 6)\,x - 3a$. Match the constants: <span class=\"nw\">$-3a = -15$,</span> so <span class=\"nw\">$a = 5$.</span> Match the $x$ terms: <span class=\"nw\">$b = a - 6 = -1$.</span> Check: $(2x + 5)(x - 3) = 2x^2 - x - 15$. ✓",
  "trap": r"Reporting <span class=\"nw\">$a = 5$.</span> The question asks for <span class=\"nw\">$b$,</span> which needs the second match. Also tempting: $b = -6$ from the first cross-product alone, forgetting the $ax$ term."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"$$f(x) = \dfrac{x + 2}{\sqrt{x - 3}}$$ Which of the following represents the domain of the function $f$ above?",
  "options": [r"$x \geq 3$", r"$x > 3$", r"$x \neq 3$", r"$x \geq -2$ and $x \neq 3$"], "correct": 1,
  "desmos": ["y=\\frac{x+2}{\\sqrt{x-3}}"],
  "sol": r"<strong>Given:</strong> the root is in the denominator.<br><br>The radicand must be $0$ or more <em>and</em> the denominator must not be <span class=\"nw\">$0$,</span> and $\sqrt{x - 3} = 0$ exactly at <span class=\"nw\">$x = 3$.</span> Both rules together: <span class=\"nw\">$x - 3 > 0$,</span> so <span class=\"nw\">$x > 3$.</span>",
  "trap": r"Choice A is the domain of $\sqrt{x - 3}$ by itself. Moving the root downstairs turns $\geq$ into <span class=\"nw\">$>$.</span> Choice D treats the numerator as if it restricted anything; $x + 2$ accepts every number."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$g(x) = \dfrac{x^2 - 9}{2x^2 - 7x + 3}$$ What is the sum of all values of $x$ for which the function $g$ above is undefined?",
  "label": "Sum $=$", "accept": ["7/2", "3.5"], "desmos": ["y=\\frac{x^2-9}{2x^2-7x+3}"],
  "sol": r"<strong>Given:</strong> a denominator with <span class=\"nw\">$a \neq 1$,</span> and a numerator that shares a factor with it.<br><br>$2x^2 - 7x + 3 = (2x - 1)(x - 3)$, so $g$ is undefined at $x = \tfrac{1}{2}$ and <span class=\"nw\">$x = 3$.</span> Sum: <span class=\"nw\">$\tfrac{7}{2}$.</span> The numerator $(x - 3)(x + 3)$ also contains <span class=\"nw\">$(x - 3)$,</span> but a shared factor does not rescue the point: $x = 3$ still makes the denominator zero.",
  "trap": r"Canceling the $(x - 3)$ first leaves $\dfrac{x + 3}{2x - 1}$ and the answer $\tfrac{1}{2}$ alone. List the restrictions before any simplifying. On a student-produced response, $7/2$ and $3.5$ both count.",
  "extrasIntro": r"Domain questions come in three flavors: a denominator to set to zero, a radicand to keep at zero or more, and both at once. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The positive value of $x$ at which $\dfrac{1}{x^2 + 2x - 15}$ is undefined is $x =$", "label": "$x =$", "accept": ["3"], "exp": r"$(x + 5)(x - 3) = 0$ at $x = -5$ or <span class=\"nw\">$x = 3$.</span>"},
   {"type": "ne", "q": r"The largest value of $x$ in the domain of $f(x) = \sqrt{10 - 2x}$ is $x =$", "label": "$x =$", "accept": ["5"], "exp": r"$10 - 2x \geq 0$ gives <span class=\"nw\">$x \leq 5$:</span> the domain runs to the <em>left</em> this time, and $5$ is its right edge."},
   {"type": "ne", "q": r"At how many values of $x$ is $g(x) = \dfrac{x + 4}{x^2 - 16}$ undefined?", "label": "Number $=$", "accept": ["2"], "exp": r"$x^2 - 16 = (x - 4)(x + 4)$: two values, $4$ and <span class=\"nw\">$-4$,</span> even though the $(x + 4)$ would cancel."},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"The function $f$ is defined by <span class=\"nw\">$f(x) = (x - 5)(x + 1)$,</span> and the function $g$ is defined by <span class=\"nw\">$g(x) = f(x + 2)$.</span> What is the $x$-coordinate of the $x$-intercept of the graph of $g$ with the greater $x$-coordinate?",
  "label": "$x =$", "accept": ["3"], "desmos": ["f(x)=(x-5)(x+1)", "g(x)=f(x+2)"],
  "sol": r"<strong>Given:</strong> a shift of a function whose zeros are known.<br><br>$g(x) = f(x + 2) = (x + 2 - 5)(x + 2 + 1) = (x - 3)(x + 3)$: zeros at $3$ and <span class=\"nw\">$-3$.</span> The greater is <span class=\"nw\">$3$.</span><br><strong>Without algebra:</strong> $f(x + 2)$ is $f$ shifted $2$ to the <em>left</em>, so the zeros $5$ and $-1$ become $3$ and <span class=\"nw\">$-3$.</span>",
  "trap": r"Shifting the zeros to the right ($7$ and <span class=\"nw\">$1$)</span> because of the plus sign. Inside the parentheses, plus means left. Check one: $g(3) = f(5) = 0$. ✓",
  "extrasIntro": r"A shift moves every point by the same amount, zeros and vertices included: add $h$ to the input and $k$ to the output. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"The function $f$ has a zero at <span class=\"nw\">$x = 4$.</span> The function $g(x) = f(x - 3)$ has a zero at $x =$", "label": "$x =$", "accept": ["7"], "exp": r"$g(7) = f(4) = 0$. Minus inside is a shift to the right."},
   {"type": "ne", "q": r"If $f(2) = 9$ and <span class=\"nw\">$g(x) = f(x) + 4$,</span> then $g(2) =$", "label": "$=$", "accept": ["13"], "exp": r"Outside the function: add $4$ to the output. $g(2) = 9 + 4 = 13$."},
   {"type": "ne", "q": r"The minimum point of the graph of $f$ is <span class=\"nw\">$(2, -3)$.</span> The minimum point of the graph of $g(x) = f(x + 1) - 5$ is <span class=\"nw\">$(a, b)$.</span> Then $a + b =$", "label": "$=$", "accept": ["-7"], "exp": r"Left $1$ and down <span class=\"nw\">$5$:</span> <span class=\"nw\">$(1, -8)$,</span> so <span class=\"nw\">$a + b = -7$.</span>"},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$$f(x) = ax + b$$ $$g(x) = 3f(x) - 2$$ In the functions above, $a$ and $b$ are constants. If $g(1) = 4$ and <span class=\"nw\">$g(2) = 13$,</span> what is the value of <span class=\"nw\">$b$?</span>",
  "label": "$b =$", "accept": ["-1"],
  "sol": r"<strong>Given:</strong> two values of <span class=\"nw\">$g$,</span> two unknowns inside <span class=\"nw\">$f$.</span><br><br>$g(1) = 3(a + b) - 2 = 4$ gives <span class=\"nw\">$a + b = 2$.</span> $g(2) = 3(2a + b) - 2 = 13$ gives <span class=\"nw\">$2a + b = 5$.</span> Subtract: <span class=\"nw\">$a = 3$,</span> so <span class=\"nw\">$b = -1$.</span> Check: $f(x) = 3x - 1$ and $g(2) = 3(5) - 2 = 13$. ✓",
  "trap": r"Treating $g(1) = 4$ as if it said <span class=\"nw\">$f(1) = 4$.</span> Peel $g$ back to $f$ first: $f(1) = 2$ and $f(2) = 5$ is a two-point line, Rule 2 of the linear sheet, and its intercept is <span class=\"nw\">$b$.</span>"},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"The functions $f$ and $g$ are defined by $f(x) = x^2$ and <span class=\"nw\">$g(x) = x + 2$.</span> For what value of $x$ is <span class=\"nw\">$f(g(x)) = g(f(x))$?</span>",
  "label": "$x =$", "accept": ["-1/2", "-0.5", "-.5"], "desmos": ["y=(x+2)^2", "y=x^2+2"],
  "sol": r"<strong>Given:</strong> both compositions, set equal.<br><br>$f(g(x)) = (x + 2)^2 = x^2 + 4x + 4$. $g(f(x)) = x^2 + 2$. They agree when <span class=\"nw\">$x^2 + 4x + 4 = x^2 + 2$,</span> so $4x = -2$ and <span class=\"nw\">$x = -\tfrac{1}{2}$.</span>",
  "trap": r"Assuming the two orders are the same function and answering “all real numbers.” They agree at exactly one input. The $x^2$ terms cancel, so this is a linear equation in disguise; in Desmos the two parabolas cross once."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"$$(ax + 3)(bx - 4) = 10x^2 + cx - 12$$ In the equation above, $a$, $b$, and $c$ are constants and <span class=\"nw\">$a + b = 7$.</span> If the equation is true for all values of <span class=\"nw\">$x$,</span> what is one possible value of <span class=\"nw\">$c$?</span>",
  "label": "$c =$", "accept": ["7", "-14"],
  "sol": r"<strong>Given:</strong> an identity with three unknown constants and one extra fact.<br><br>Expand: $abx^2 + (3b - 4a)\,x - 12$. Match the $x^2$ terms: <span class=\"nw\">$ab = 10$,</span> and with $a + b = 7$ the pair is $2$ and $5$ in some order. If $a = 2$ and <span class=\"nw\">$b = 5$:</span> <span class=\"nw\">$c = 15 - 8 = 7$.</span> If $a = 5$ and <span class=\"nw\">$b = 2$:</span> <span class=\"nw\">$c = 6 - 20 = -14$.</span> Either value is accepted. Check: $(2x + 3)(5x - 4) = 10x^2 + 7x - 12$. ✓",
  "trap": r"The constant term, $3 \cdot (-4) = -12$, matches automatically and tells you nothing. The information is in $ab = 10$ together with <span class=\"nw\">$a + b = 7$:</span> a sum-and-product pair, the same idea as the quadratics sheet's Rule 6.",
  "extrasIntro": r"Identities built from a product: expand, then match the coefficient of each power of <span class=\"nw\">$x$.</span> Three more reps.",
  "extras": [
   {"type": "ne", "q": r"If $(x + a)(x + 3) = x^2 + 7x + b$ for all <span class=\"nw\">$x$,</span> then $b =$", "label": "$b =$", "accept": ["12"], "exp": r"$x^2 + (a + 3)\,x + 3a$: $a + 3 = 7$ gives <span class=\"nw\">$a = 4$,</span> so <span class=\"nw\">$b = 3a = 12$.</span>"},
   {"type": "ne", "q": r"If $3(x - k) = 3x - 12$ for all <span class=\"nw\">$x$,</span> then $k =$", "label": "$k =$", "accept": ["4"], "exp": r"$3x - 3k = 3x - 12$, so <span class=\"nw\">$-3k = -12$</span> and <span class=\"nw\">$k = 4$.</span>"},
   {"type": "ne", "q": r"If $(x + 2)(x + m) = x^2 + 9x + 14$ for all <span class=\"nw\">$x$,</span> then $m =$", "label": "$m =$", "accept": ["7"], "exp": r"$m + 2 = 9$ gives <span class=\"nw\">$m = 7$</span> (and $2m = 14$ agrees)."},
  ]},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"$$x^2 + 10x + 23 = (x + a)^2 + b$$ In the equation above, $a$ and $b$ are constants. If the equation is true for all values of <span class=\"nw\">$x$,</span> what is the value of <span class=\"nw\">$a - b$?</span>",
  "label": "$a - b =$", "accept": ["7"], "desmos": ["y=x^2+10x+23", "(-5,-2)"],
  "sol": r"<strong>Given:</strong> an identity whose right side is vertex form, so this is completing the square.<br><br>$(x + a)^2 + b = x^2 + 2ax + a^2 + b$. Match: <span class=\"nw\">$2a = 10$,</span> so <span class=\"nw\">$a = 5$;</span> <span class=\"nw\">$a^2 + b = 23$,</span> so <span class=\"nw\">$b = -2$.</span> Then <span class=\"nw\">$a - b = 5 - (-2) = 7$.</span> The vertex, <span class=\"nw\">$(-5, -2)$,</span> is the shift of $y = x^2$ that this identity describes.",
  "trap": r"$b = 23 - 10 = 13$, subtracting $2a$ instead of <span class=\"nw\">$a^2$.</span> The constant that comes with $(x + a)^2$ is <span class=\"nw\">$a^2$.</span> And watch the final subtraction: $5 - (-2)$ is <span class=\"nw\">$7$,</span> not $3$."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"The function $f$ is defined by <span class=\"nw\">$f(x) = \sqrt{x + a} + b$,</span> where $a$ and $b$ are constants. The domain of $f$ is $x \geq -3$ and the range of $f$ is <span class=\"nw\">$y \geq 5$.</span> What is the value of <span class=\"nw\">$a + b$?</span>",
  "label": "$a + b =$", "accept": ["8"], "desmos": ["y=\\sqrt{x+3}+5", "(-3,5)"],
  "sol": r"<strong>Given:</strong> the domain pins <span class=\"nw\">$a$,</span> the range pins <span class=\"nw\">$b$.</span><br><br>Domain: $x + a \geq 0$ means <span class=\"nw\">$x \geq -a$,</span> and that is <span class=\"nw\">$x \geq -3$,</span> so <span class=\"nw\">$a = 3$.</span> Range: the root contributes $0$ or more, so the outputs start at <span class=\"nw\">$b$,</span> and that is <span class=\"nw\">$5$:</span> <span class=\"nw\">$b = 5$.</span> $a + b = 8$.",
  "trap": r"Reading $a = -3$ off the domain. The domain starts at <span class=\"nw\">$-a$,</span> so <span class=\"nw\">$-a = -3$.</span> Inside the root the sign runs backwards, exactly as it does for a horizontal shift."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"If <span class=\"nw\">$f(x) = x^2 + 3x$,</span> then $f(-2) =$", "opts": ["$-2$", "$10$", "$2$", "$-10$"], "correct": 0,
  "exp": r"$(-2)^2 + 3(-2) = 4 - 6 = -2$."},
 {"q": r"The function $h(x) = \dfrac{7}{x^2 - 16}$ is undefined at", "opts": ["$x = 4$ only", "$x = 4$ and $x = -4$", "$x = 16$", "$x = 7$"], "correct": 1,
  "exp": r"$x^2 - 16 = (x - 4)(x + 4) = 0$ at both $4$ and <span class=\"nw\">$-4$.</span>"},
 {"q": r"The graph of $y = f(x + 4)$ is the graph of $y = f(x)$ shifted", "opts": ["$4$ units to the left", "$4$ units to the right", "$4$ units up", "$4$ units down"], "correct": 0,
  "exp": r"Inside the parentheses, plus means left: the point that used to need input $4$ now needs input <span class=\"nw\">$0$.</span>"},
]

# ---------------------------------------------------------------- FIGURES
FIGS_JS = r'''var FIGS = {
    notation: { xmin: -1.8, xmax: 6.5, ymin: -1, ymax: 5.5, w: 340, h: 240, alt: 'the graph of a function f with the point (4, 2) marked; dashed lines show the input 4 on the x-axis and the output 2 on the y-axis',
        curves: [{ a: -0.5, b: 2, c: 2, label: 'y = f(x)', lx: 5.2, ly: 1.6, dx: 6, dy: 0 }],
        segs: [{ x1: 4, y1: 0, x2: 4, y2: 2 }, { x1: 0, y1: 2, x2: 4, y2: 2 }],
        points: [{ x: 4, y: 2, label: '(4, 2)', dx: 8, dy: -6 }],
        labels: [{ x: 4, y: 0, text: 'input 4', dx: -20, dy: 17, cls: 'sm' }, { x: 0, y: 2, text: 'output 2', dx: -60, dy: 4, cls: 'sm' }] },
    crossings: { xmin: -5, xmax: 6, ymin: -3, ymax: 4, w: 340, h: 250, grid: { step: 1, label: 2 }, alt: 'a zigzag graph of f on a grid from x = negative 4 to x = 5 with the horizontal line y = 1 meeting it at three points',
        polylines: [{ pts: [[-4, 3], [-2, -2], [1, 2], [3, 0], [5, 0.5]], label: 'y = f(x)', lx: 4.1, ly: 1.6 }],
        hlines: [{ y: 1, label: 'y = 1', lx: -4.9, dy: -5 }],
        points: [{ x: -3.2, y: 1 }, { x: 0.25, y: 1 }, { x: 2, y: 1 }, { x: 3, y: 0 }] },
    g_read: { xmin: -5, xmax: 6, ymin: -3, ymax: 4, w: 340, h: 250, grid: { step: 1, label: 2 }, alt: 'a zigzag graph of f on a grid from x = negative 4 to x = 5',
        polylines: [{ pts: [[-4, 3], [-2, -2], [1, 2], [3, 0], [5, 0.5]], label: 'y = f(x)', lx: 4.1, ly: 1.6 }] },
    undefined: { xmin: -3, xmax: 7, ymin: -4, ymax: 4, w: 300, h: 230, alt: 'the graph of y = 1 over (x minus 2) with a dashed vertical line at x = 2 where the function is undefined',
        curves: [{ f: function(x) { return 1 / (x - 2); }, label: 'y = 1/(x − 2)', lx: 3.6, ly: 1.6, dx: 0, dy: -4 }],
        vlines: [{ x: 2, label: 'x = 2', dx: -40, dy: 14 }],
        labels: [{ x: 2, y: -3.4, text: 'undefined here', dx: 6, dy: 0, cls: 'sm' }] },
    sqrtdom: { xmin: -1.5, xmax: 9, ymin: -1.2, ymax: 3.5, w: 300, h: 210, alt: 'the graph of y = the square root of (x minus 3), starting at (3, 0), with the domain x greater than or equal to 3 highlighted on the x-axis',
        curves: [{ f: function(x) { return Math.sqrt(x - 3); }, from: 3, label: 'y = √(x − 3)', lx: 5.4, ly: 2.3, dx: -6, dy: -6 }],
        thick: [{ x1: 3, y1: 0, x2: 9, y2: 0 }],
        points: [{ x: 3, y: 0, label: '(3, 0)', dx: -42, dy: 16 }],
        labels: [{ x: 4.3, y: 0, text: 'domain: x ≥ 3', dx: 0, dy: 18, cls: 'sm' }] },
    g_comp: { xmin: -5, xmax: 7, ymin: -1, ymax: 6, w: 340, h: 250, grid: { step: 1, label: 2 }, alt: 'a zigzag graph of f on a grid from x = negative 4 to x = 6 with peaks at (negative 1, 4) and (3, 5)',
        polylines: [{ pts: [[-4, 1], [-1, 4], [1, 2], [3, 5], [6, 1]], label: 'y = f(x)', lx: 4.4, ly: 4.6 }] },
    shift: { xmin: -3.2, xmax: 7, ymin: -1, ymax: 9, w: 340, h: 260, alt: 'the parabola f(x) = x squared and the parabola g, the same shape moved 3 to the right and 2 up, with dashed arrows showing the move from vertex (0, 0) to vertex (3, 2)',
        curves: [{ a: 1, b: 0, c: 0, label: 'f', lx: -2.3, ly: 3.5, dx: -13, dy: 0 }, { a: 1, b: -6, c: 11, cls: 'ln2', label: 'g', lx: 5.75, ly: 8.6, dx: 8, dy: 0 }],
        segs: [{ x1: 0, y1: 0, x2: 3, y2: 0 }, { x1: 3, y1: 0, x2: 3, y2: 2 }],
        points: [{ x: 0, y: 0 }, { x: 3, y: 2, label: '(3, 2)', dx: 9, dy: 14 }],
        labels: [{ x: 1.5, y: 0, text: 'right 3', dx: -20, dy: 17, cls: 'sm' }, { x: 3, y: 1, text: 'up 2', dx: -34, dy: 4, cls: 'sm' }] },
    range: { xmin: -4.4, xmax: 9, ymin: -5.6, ymax: 1.2, w: 350, h: 240, alt: 'the graph of y = the square root of (x plus 1) minus 4, starting at (negative 1, negative 4), with the domain highlighted on the x-axis and the range highlighted on the y-axis',
        curves: [{ f: function(x) { return Math.sqrt(x + 1) - 4; }, from: -1, label: 'y = √(x + 1) − 4', lx: 4.6, ly: -2.9, dx: 0, dy: 12 }],
        thick: [{ x1: -1, y1: 0, x2: 9, y2: 0 }, { x1: 0, y1: -4, x2: 0, y2: 1.2 }],
        points: [{ x: -1, y: -4, label: '(−1, −4)', dx: -58, dy: 5 }],
        labels: [{ x: 4.2, y: 0, text: 'domain: x ≥ −1', dx: -4, dy: -8, cls: 'sm' }, { x: 0, y: -2.2, text: 'range: y ≥ −4', dx: -92, dy: 4, cls: 'sm' }] },
    g7: { xmin: -5, xmax: 7, ymin: -1, ymax: 7, w: 340, h: 260, grid: { step: 1, label: 2 }, alt: 'a zigzag graph of f on a grid from x = negative 4 to x = 6 with a peak at (1, 6)',
        polylines: [{ pts: [[-4, 5], [-2, 1], [1, 6], [4, 2], [6, 3]], label: 'y = f(x)', lx: 4.7, ly: 5.6 }] },
    g8: { xmin: -4, xmax: 7, ymin: -4, ymax: 6, w: 340, h: 260, alt: 'two parabolas of the same shape: f with vertex (0, negative 3) and g with vertex (3, negative 1)',
        curves: [{ a: 1, b: 0, c: -3, label: 'f', lx: -3.1, ly: 5.4, dx: -8, dy: 0 }, { a: 1, b: -6, c: 8, cls: 'ln2', label: 'g', lx: 6.05, ly: 5.4, dx: 6, dy: 0 }],
        points: [{ x: 0, y: -3, label: '(0, −3)', dx: 8, dy: 14 }, { x: 3, y: -1, label: '(3, −1)', dx: 8, dy: 14 }] }
};
/* Function-machine pictures (Rule 1 and Rule 3). */
function arrowDefs(id) {
    return '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';
}
function mBox(x, y, w, h, text, sub) {
    var s = '<rect class="box" x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="6"/>' +
        '<text class="it" text-anchor="middle" x="' + (x + w / 2) + '" y="' + (y + h / 2 + (sub ? 1 : 5)) + '">' + text + '</text>';
    if (sub) s += '<text class="sm" text-anchor="middle" x="' + (x + w / 2) + '" y="' + (y + h / 2 + 15) + '">' + sub + '</text>';
    return s;
}
function mArrow(id, x1, y, x2, text, above) {
    return '<line class="ax" x1="' + x1 + '" y1="' + y + '" x2="' + x2 + '" y2="' + y + '" marker-end="url(#' + id + ')"/>' +
        (text ? '<text class="it" text-anchor="middle" x="' + ((x1 + x2) / 2 - 3) + '" y="' + (y + (above ? -7 : 17)) + '">' + text + '</text>' : '');
}
function machineSVG() {
    var id = 'mk' + (++figCounter);
    var s = '<svg class="fig" viewBox="0 0 400 128" width="400" height="128" role="img" aria-label="a function machine: the input x enters the box f and the output f(x) leaves it; below it, the input negative 2 enters f(x) = x squared minus 4x and the output 12 leaves">' + arrowDefs(id);
    s += mArrow(id, 24, 34, 140, 'x', true) + mBox(146, 14, 108, 40, 'f') + mArrow(id, 258, 34, 374, 'f(x)', true);
    s += '<text class="sm" x="60" y="54">input</text><text class="sm" x="296" y="54">output</text>';
    s += mArrow(id, 24, 100, 140, '−2', true) + mBox(146, 80, 108, 40, 'x² − 4x') + mArrow(id, 258, 100, 374, '12', true);
    s += '<text class="sm" x="150" y="76">(−2)² − 4(−2) = 12</text>';
    return s + '</svg>';
}
function composeSVG() {
    var id = 'mk' + (++figCounter);
    var s = '<svg class="fig" viewBox="0 0 470 118" width="470" height="118" role="img" aria-label="composition as two machines in a row: the input 2 enters f(x) = 2x + 1 and 5 comes out; 5 enters g(x) = x squared minus 3 and 22 comes out, so g(f(2)) = 22">' + arrowDefs(id);
    s += mArrow(id, 14, 40, 94, '2', true) + mBox(100, 20, 112, 40, 'f(x) = 2x + 1') + mArrow(id, 216, 40, 290, '5', true) + mBox(296, 20, 112, 40, 'g(x) = x² − 3') + mArrow(id, 412, 40, 462, '22', true);
    s += '<text class="sm" x="118" y="76">f first: f(2) = 5</text><text class="sm" x="302" y="76">then g: g(5) = 25 − 3 = 22</text>';
    s += '<text class="it" x="150" y="104">g(f(2)) = g(5) = 22, &nbsp;read from the inside out</text>';
    return s + '</svg>';
}
/* Small pictures for the domain and range tables. */
function miniCurve(fn, x0, x1, o) {
    o = o || {};
    var w = 120, h = 64, xmin = o.xmin, xmax = o.xmax, ymin = o.ymin, ymax = o.ymax;
    function X(x) { return 6 + (x - xmin) / (xmax - xmin) * 108; }
    function Y(y) { return 58 - (y - ymin) / (ymax - ymin) * 52; }
    var s = '<svg class="fig" viewBox="0 0 120 64" width="120" height="64" style="margin:0;" role="img" aria-label="' + (o.alt || 'small graph') + '">';
    if (ymin <= 0 && ymax >= 0) s += '<line class="ax" x1="6" y1="' + Y(0) + '" x2="114" y2="' + Y(0) + '"/>';
    if (xmin <= 0 && xmax >= 0) s += '<line class="ax" x1="' + X(0) + '" y1="58" x2="' + X(0) + '" y2="4"/>';
    (o.vlines || []).forEach(function(v) { s += '<line class="dash" x1="' + X(v) + '" y1="4" x2="' + X(v) + '" y2="58"/>'; });
    var runs = [], run = [];
    for (var i = 0; i <= 120; i++) {
        var x = x0 + (x1 - x0) * i / 120, y = fn(x);
        if (!isFinite(y) || y < ymin - 3 || y > ymax + 3) { if (run.length) { runs.push(run); run = []; } continue; }
        run.push(X(x).toFixed(1) + ',' + Y(Math.max(ymin - 0.5, Math.min(ymax + 0.5, y))).toFixed(1));
    }
    if (run.length) runs.push(run);
    runs.forEach(function(r) { if (r.length > 1) s += '<polyline class="ln" points="' + r.join(' ') + '"/>'; });
    (o.thick || []).forEach(function(t) { s += '<line class="dom" x1="' + X(t[0]) + '" y1="' + Y(t[1]) + '" x2="' + X(t[2]) + '" y2="' + Y(t[3]) + '"/>'; });
    (o.pts || []).forEach(function(p) { s += '<circle class="pt" cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="2.8"/>'; });
    return s + '</svg>';
}
var MINI = {
    m_frac: function() { return miniCurve(function(x) { return 1 / (x - 1.5); }, -2, 5, { xmin: -2, xmax: 5, ymin: -3, ymax: 3, vlines: [1.5], alt: 'a fraction graph with a vertical gap where the denominator is zero' }); },
    m_root: function() { return miniCurve(function(x) { return Math.sqrt(x - 1); }, 1, 6, { xmin: -1, xmax: 6, ymin: -1, ymax: 2.6, thick: [[1, 0, 6, 0]], pts: [[1, 0]], alt: 'a square root graph starting at a point and going right' }); },
    rng_line: function() { return miniCurve(function(x) { return 0.8 * x + 0.4; }, -3, 3, { xmin: -3, xmax: 3, ymin: -2.6, ymax: 2.6, thick: [[0, -2.6, 0, 2.6]], alt: 'a line: every height is reached' }); },
    rng_up: function() { return miniCurve(function(x) { return 0.5 * (x - 0.6) * (x - 0.6) - 1; }, -3, 3.5, { xmin: -3, xmax: 3.5, ymin: -2.2, ymax: 2.6, thick: [[0, -1, 0, 2.6]], pts: [[0.6, -1]], alt: 'an upward parabola: heights from the vertex up' }); },
    rng_down: function() { return miniCurve(function(x) { return -0.5 * (x - 0.6) * (x - 0.6) + 1.2; }, -3, 3.5, { xmin: -3, xmax: 3.5, ymin: -2.4, ymax: 2.4, thick: [[0, -2.4, 0, 1.2]], pts: [[0.6, 1.2]], alt: 'a downward parabola: heights from the vertex down' }); },
    rng_root: function() { return miniCurve(function(x) { return Math.sqrt(x - 0.8) - 0.9; }, 0.8, 6, { xmin: -1, xmax: 6, ymin: -2, ymax: 2.2, thick: [[0, -0.9, 0, 2.2]], pts: [[0.8, -0.9]], alt: 'a square root graph: heights from its starting point up' }); },
    machine: machineSVG, compose: composeSVG
};
function fig(name) { if (MINI[name]) return MINI[name](); return FIGS[name] ? graphSVG(FIGS[name]) : ''; }'''

# The shell draws lines, dashed segments, points, polygons. This sheet adds: general
# function curves (with gaps), polylines, horizontal and vertical dashed lines, thick
# domain/range highlights on the axes, and an optional labeled grid.
CURVES_JS = r'''    (o.curves || []).forEach(function(c) {
        // y = a x^2 + b x + c, or any function c.f, sampled across [from, to] and split at gaps
        var fn = c.f || function(x) { return c.a * x * x + c.b * x + c.c; };
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

FIG_CSS = r'''.fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }
.fig .grid { stroke: rgba(45,45,45,0.13); stroke-width: 1; }
.fig .dom { stroke: #BC6C26; stroke-width: 6; stroke-linecap: round; opacity: 0.5; }
.fig .box { fill: white; stroke: #21442B; stroke-width: 1.6; }
.fig text.sm { font-family: 'Inter', sans-serif; font-size: 11px; font-style: normal; fill: #5A5A5A; }
.fig-row { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: flex-start; justify-content: center; margin: 4px 0 10px; }
.fig-row .fig { margin: 4px 0; }
.ref-page .fig-row { margin-left: 24px; }
table.forms td.fname .fig, table.cases td .fig { margin: 4px 0 0; }
@media (max-width: 768px) { .ref-page .fig-row { margin-left: 0; } }'''

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
html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Functions</title>')
html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Functions</h1>')
html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; FUNCTIONS')
html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Functions')
html = replace_once(html, '>1. Linear Rules</button>', '>1. Function Rules</button>')
html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Function rules</h2>')

# --- tab 1 body
start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
html = html[:start] + RULES.rstrip('\n') + '\n' + html[end:]

# --- tab 2 intro card
html = replace_once(html,
    '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
    '<p>Everything on the rules tab runs on one idea: <strong>a function is a rule that turns an input into an output, and $f(a) = b$ is the point $(a, b)$.</strong> Evaluating, reading a graph, composing two rules, matching an identity, and shifting a graph are all that one translation, applied in a different direction each time.</p>')

# --- tab 4 and tab 5 intro cards
html = replace_once(html,
    'from easy openers to the high-medium items near the end. A <strong>',
    'from easy openers through medium to medium-hard at the end, and two carry graphs to read. A <strong>')
html = replace_once(html,
    '<p>These six run from high-medium to hard: the linear questions that show up late in a module and separate a strong score from a perfect one. Each one is a rule you already have, paired with a second idea (an unknown that cancels, an area, a reflection, a translation, a pair of intercepts).',
    '<p>These eight pick up where the practice set stops, running from medium-hard to hard: late-module question types that separate a strong score from a perfect one. Each is a rule you already have, paired with a second idea (a root in the denominator, a factor that would cancel, a shift of a known zero, two compositions set equal, an identity with a sum-and-product pair, completing the square read as an identity, a domain and a range that each pin down a constant).')

# --- tab 6: rule prompt and extra reps
html = replace_once(html,
    'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
    'One sentence you will say to yourself the next time a function shows up. Make it an if-then. (Shape: “When a question says true for all values of $x$, I ______ before I solve for anything.”)')
# (Bluebook framing and voice renames are inherited from the shell)
html = replace_once(html,
    'the units <em>Linear equations in two variables</em>, <em>Linear functions</em>, and <em>Systems of two linear equations</em> are this sheet\'s Rules 1 through 5.',
    'the units <em>Linear functions</em>, <em>Nonlinear functions</em>, and <em>Equivalent expressions</em> cover this sheet\'s Rules 1 through 5.')
html = replace_once(html,
    'For the calculator side of these questions (graphing a system, a slider for $k$, reading an intersection), see',
    'For the calculator side of these questions (defining $f(x)$ and $g(x) = f(x - 3) + 2$ directly, clicking a crossing, spotting an asymptote), see')
html = replace_once(html,
    '<p style="font-size:14px; margin-top:10px;">For the calculator side',
    '<p style="font-size:14px; margin-top:10px;">The parabolas in these questions (vertex form, completing the square) are covered in <a href="' + QUAD_URL + '" target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;">SAT Math 2: Quadratics &#8594;</a>, and the lines in <a href="' + LINEAR_URL + '" target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;">SAT Math 1: Linear Equations &#8594;</a></p>\n            <p style="font-size:14px; margin-top:10px;">For the calculator side')

# --- Desmos guidance: swap the linear sheet's examples for function ones
html = replace_once(html,
    'finding an intersection, checking a slope, sliding a $k$. For a one-step slope read or a quick substitution, straight algebra is faster.',
    'counting how many times a graph crosses a height, checking a shift (Desmos understands $f(x - 3) + 2$), spotting where a denominator hits zero. For evaluating, composing, and matching coefficients, straight algebra is faster.')

# --- data arrays
for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
    html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

# --- figures: FIGS + fig(), a general curve renderer, a grid, and a clip path in graphSVG
start = html.index('var FIGS = {')
end = html.index("function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }") + len("function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }")
html = html[:start] + FIGS_JS + html[end:]
html = replace_once(html,
    """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';""",
    """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker>' +
        '<clipPath id="clip' + id + '"><rect x="' + X(xmin) + '" y="' + Y(ymax) + '" width="' + (X(xmax) - X(xmin)) + '" height="' + (Y(ymin) - Y(ymax)) + '"/></clipPath></defs>';""")
html = replace_once(html, "    if (o.poly) {\n", GRID_JS + "    if (o.poly) {\n")
html = replace_once(html, "    (o.lines || []).forEach(function(l) {\n", CURVES_JS + "    (o.lines || []).forEach(function(l) {\n")
html = replace_once(html, ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }", FIG_CSS)

# --- misc: storage key, last-starred-step hint
html = html.replace('sat-linear-sheet:rule', 'sat-functions-sheet:rule')
html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                    "(i === %d ? 'That was the last starred step. The last one is the extra.' : '')" % LAST_STARRED_STEP_INDEX)
html = replace_once(html, "Step 1 of 9", "Step 1 of %d" % len(STEPS))

open(OUT, 'w', encoding='utf-8').write(html)
print('wrote', OUT, len(html), 'bytes;', len(STEPS), 'steps,', sum(len(s['items']) for s in FLUENCY), 'fluency,', len(GAUNTLET), 'gauntlet,', len(CHALLENGE), 'challenge,', len(EXIT), 'exit')
