#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-7-Exponents-and-Exponential-Models.html from the linear-equations
sheet's shell. Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only
the content swaps. This sheet covers the exponent laws, negative and fractional exponents, rewriting
in one base, growth and decay factors, reading an exponential model, and two less common model
questions (a constant to find, and average rate of change). All questions use original numbers.

It was copied from build_special_right_triangles.py (the voice pass, figures carried into the tutor
report) and takes the curve and grid extensions for coordinate graphs from build_functions.py. Every
figure here is a coordinate graph, so the geometry renderer is not carried. One small addition: a
figure can name its axes with `xl` and `yl` (for example t and N in place of x and y).
Answer key: verify_exponents.py (same folder) recomputes every answer."""
import json, os, re, sys

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
OUT = ROOT + '/test-prep/sat/SAT-Math-7-Exponents-and-Exponential-Models.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
PCT_URL = SITE + 'test-prep/sat/SAT-Math-6-Percentages.html'
FUNC_URL = SITE + 'test-prep/sat/SAT-Math-3-Functions.html'
CIRCLES_URL = SITE + 'test-prep/sat/SAT-Math-8-Circle-Equations.html'
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


def lead(text):
    return '<p class="ref-lead">' + text + '</p>\n'


def fbox(*rows):
    return '<div class="fbox">\n' + ''.join(rows) + '</div>\n'


def table(head, rows):
    """A `cases` table: the first cell of each row is the bold name cell."""
    return ('<div class="tbl-wrap"><table class="cases"><thead><tr>' + ''.join('<th>' + h + '</th>' for h in head) + '</tr></thead><tbody>\n' +
            ''.join('<tr><td class="fname">' + r[0] + '</td>' + ''.join('<td>' + c + '</td>' for c in r[1:]) + '</tr>\n' for r in rows) +
            '</tbody></table></div>\n')


def vtab(xname, xs, yname, ys):
    """A small table of values, the way the SAT prints one inside a question."""
    return ("<table class='vtab'><tr><th>" + xname + "</th>" + ''.join('<td>' + v + '</td>' for v in xs) + "</tr><tr><th>" + yname + "</th>" +
            ''.join('<td>' + v + '</td>' for v in ys) + "</tr></table>")


# ---------------------------------------------------------------- TAB 1: RULES
PCT_LINK = '<a href="' + PCT_URL + '" target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;">SAT Math 6: Percentages</a>'

RULES = ''.join([
    r'''
<p class="ref-intro">An exponent counts repeated multiplication. That idea is behind two kinds of SAT questions. In the first kind, you rewrite an expression: combine powers, move a negative exponent, or turn a root into a fractional exponent. In the second kind, a quantity is multiplied by the same factor again and again, and you build or read the model that describes it. Rules 1 to 4 cover the expressions. Rules 5 and 6 cover the models, and Rule 7 adds two model questions that come up less often. Different forms reveal different information, so notice what you have been given before you start the algebra. As you practice, start by identifying the question type. Then decide whether Desmos or algebra makes more sense, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''',
    rule(1, 'The exponent laws', True,
         lead(r'An exponent tells you how many times the base is used as a factor: $5^3 = 5 \cdot 5 \cdot 5$. Each law below comes from counting factors. If you forget one, write out a small case and count.') +
         fbox(frow('multiply, same base', r'$a^m \cdot a^n = a^{m+n}$ &nbsp; (add the exponents)'),
              frow('divide, same base', r'$\dfrac{a^m}{a^n} = a^{m-n}$ &nbsp; (subtract the exponents)'),
              frow('power of a power', r'$\left(a^m\right)^n = a^{mn}$ &nbsp; (multiply the exponents)'),
              frow('power of a product', r'$(ab)^n = a^n b^n$'),
              frow('power of a quotient', r'$\left(\dfrac{a}{b}\right)^n = \dfrac{a^n}{b^n}$'),
              frow('why it works', r'$x^2 \cdot x^3 = (x \cdot x)(x \cdot x \cdot x) = x^5$, and $\left(x^2\right)^3 = x^2 \cdot x^2 \cdot x^2 = x^6$')) +
         ex('A', r'$x^7 \cdot x^5 = x^{12}$. The bases match, so add the exponents.') +
         ex('B', r'$\left(3x^4\right)^2 = 3^2 \cdot \left(x^4\right)^2 = 9x^8$. The power applies to the coefficient too.') +
         ex('C', r'$\dfrac{12x^9}{4x^3} = 3x^6$. Divide the coefficients and subtract the exponents.') +
         note(r'These laws need a shared base or a shared exponent. There is no law for a sum: $x^2 + x^3$ does not combine, and $(a + b)^2$ is not $a^2 + b^2$.')),
    rule(2, 'Negative and zero exponents', True,
         lead(r'A negative exponent means divide by the factor instead of multiplying by it. The power moves to the other side of the fraction bar, and its exponent turns positive. A negative exponent does not make the value negative.') +
         fbox(frow('negative exponent', r'$a^{-n} = \dfrac{1}{a^n}$'),
              frow('in a denominator', r'$\dfrac{1}{a^{-n}} = a^n$'),
              frow('a fraction', r'$\left(\dfrac{a}{b}\right)^{-n} = \left(\dfrac{b}{a}\right)^n$ &nbsp; (flip, then raise)'),
              frow('zero exponent', r'$a^0 = 1$ for $a \neq 0$'),
              frow('why it works', r'$2^3 = 8$, &nbsp; $2^2 = 4$, &nbsp; $2^1 = 2$, &nbsp; $2^0 = 1$, &nbsp; $2^{-1} = \dfrac{1}{2}$, &nbsp; $2^{-2} = \dfrac{1}{4}$. Each step down divides by $2$'),
              frow('negative bases', r'$(-2)^4 = 16$ and $(-2)^3 = -8$: an even power is positive, and an odd power is negative. Without parentheses, $-2^4 = -16$')) +
         ex('A', r'$4^{-2} = \dfrac{1}{4^2} = \dfrac{1}{16}$.') +
         ex('B', r'$\dfrac{x^3 y^{-2}}{x^{-1}} = \dfrac{x^3 \cdot x^1}{y^2} = \dfrac{x^4}{y^2}$. Each negative power crosses the fraction bar.') +
         ex('C', r'$\left(\dfrac{2}{5}\right)^{-2} = \left(\dfrac{5}{2}\right)^2 = \dfrac{25}{4}$.') +
         note(r'The subtraction law still works with negative exponents: $\dfrac{x^3}{x^{-1}} = x^{3-(-1)} = x^4$. Use whichever view is easier for you to keep track of.')),
    rule(3, 'Fractional exponents and roots', True,
         lead(r'A fractional exponent is a power and a root written together. The numerator is the power, and the denominator is the root. Rewriting a radical this way lets you use the laws from Rule 1.') +
         fbox(frow('one over $n$', r'$a^{\frac{1}{n}} = \sqrt[n]{a}$, so $a^{\frac{1}{2}} = \sqrt{a}$ and $a^{\frac{1}{3}} = \sqrt[3]{a}$'),
              frow('$m$ over $n$', r'$a^{\frac{m}{n}} = \sqrt[n]{a^m} = \left(\sqrt[n]{a}\right)^m$'),
              frow('how to remember it', r'<strong>Power over root.</strong> In $a^{\frac{m}{n}}$, the top number is the power and the bottom number is the root'),
              frow('why it works', r'$\left(a^{\frac{1}{2}}\right)^2 = a^1$, so $a^{\frac{1}{2}}$ is the number whose square is $a$')) +
         ex('A', r'$27^{\frac{2}{3}} = \left(\sqrt[3]{27}\right)^2 = 3^2 = 9$. Taking the root first keeps the numbers small.') +
         ex('B', r'$\sqrt[4]{x^3} = x^{\frac{3}{4}}$, and $\sqrt{x^5} = x^{\frac{5}{2}}$.') +
         ex('C', r'$\left(x^6 y^{10}\right)^{\frac{1}{2}} = x^3 y^5$. A power of $\tfrac{1}{2}$ halves each exponent.') +
         ex('D', r'$16^{-\frac{3}{4}} = \dfrac{1}{16^{3/4}} = \dfrac{1}{2^3} = \dfrac{1}{8}$. Handle the negative sign with Rule 2, then the fraction.') +
         note(r'When a question asks which expression is equivalent to one with radicals, rewrite each radical as a fractional exponent first. Then add, subtract or multiply the exponents as in Rule 1.')),
    rule(4, 'One base, then compare exponents', True,
         lead(r'If two powers of the same base are equal, their exponents are equal. When an equation mixes bases such as $4$, $8$ and $2$, rewrite each number as a power of one base before you do anything else.') +
         fbox(frow('the idea', r'if $b^x = b^y$, then $x = y$ &nbsp; (for $b > 0$ and $b \neq 1$)'),
              frow('powers of $2$', r'$4 = 2^2$, &nbsp; $8 = 2^3$, &nbsp; $16 = 2^4$, &nbsp; $32 = 2^5$, &nbsp; $64 = 2^6$'),
              frow('powers of $3$ and $5$', r'$9 = 3^2$, &nbsp; $27 = 3^3$, &nbsp; $81 = 3^4$, &nbsp; $25 = 5^2$, &nbsp; $125 = 5^3$'),
              frow('adding equal powers', r'$3^5 + 3^5 + 3^5 = 3 \cdot 3^5 = 3^6$ &nbsp; (count the copies, then multiply)'),
              frow('same exponent instead', r'if $p^n = q^n$ and both bases are positive, then $p = q$')) +
         ex('A', r'$9^x = 27^4$. Write both sides in base $3$: $3^{2x} = 3^{12}$, so $2x = 12$ and $x = 6$.') +
         ex('B', r'$5^4 + 5^4 + 5^4 + 5^4 + 5^4 = 5 \cdot 5^4 = 5^5$. Five copies of $5^4$ make a product, so the exponents add.') +
         ex('C', r'$p^{-2} = 3^{-4}$ with $p > 0$. Rewrite the right side with an exponent of $-2$: $3^{-4} = \left(3^2\right)^{-2} = 9^{-2}$, so $p = 9$.') +
         note(r'Adding powers and multiplying powers are different operations. $2^3 \cdot 2^3 = 2^6$, but $2^3 + 2^3 = 2 \cdot 2^3 = 2^4$.')),
    rule(5, 'Growth and decay factors', True,
         lead(r'When a quantity changes by the same percent each period, it is multiplied by the same number each period. That number is the multiplier from ' + PCT_LINK + r'. In a model it is called the growth factor or the decay factor. Multiply by it once for each period, and the exponent counts the periods.') +
         '<div class="fig-row">' + figslot('r_growth').strip() + figslot('r_decay').strip() + '</div>\n' +
         fbox(frow('growth', r'$P(t) = P_0(1 + r)^t$ &nbsp; the growth factor $1 + r$ is greater than $1$'),
              frow('decay', r'$P(t) = P_0(1 - r)^t$ &nbsp; the decay factor $1 - r$ is between $0$ and $1$'),
              frow('the starting amount', r'$P_0$ is the value when $t = 0$, because a factor raised to the power $0$ is $1$'),
              frow('the rate', r'$r$ is the percent rate written as a decimal: $4\%$ is $0.04$, and $0.4\%$ is $0.004$'),
              frow('factors without a percent', r'doubling is a factor of $2$, tripling is a factor of $3$, and halving is a factor of $\dfrac{1}{2}$')) +
         ex('A', r'A deposit of $\$800$ grows by $3\%$ each year. The growth factor is $1.03$, so the model is $A(t) = 800(1.03)^t$.') +
         ex('B', r'A sample with a mass of $250$ grams loses $12\%$ of its mass each hour. The decay factor is $1 - 0.12 = 0.88$, so the model is $M(t) = 250(0.88)^t$.') +
         ex('C', r'After $2$ years, the deposit in Example A is worth $800(1.03)^2 = 800(1.0609) = 848.72$ dollars.') +
         note(r'Rates below $1\%$ need care with the decimal point. A rate of $0.6\%$ is $0.006$, so the growth factor is $1.006$ and the decay factor is $0.994$.')),
    rule(6, 'Reading a model', True,
         lead(r'A model written as $y = a \cdot b^t$ shows its starting value and its factor directly. Different parts of the model answer different questions, so identify which part a question asks about before you compute.') +
         table(['Part', 'Where it sits', 'What it tells you'], [
             [r'$a$', 'in front', r'the initial value: the amount when $t = 0$, and the $y$-intercept of the graph'],
             [r'$b$', 'the base', r'the factor for one period: greater than $1$ is growth, between $0$ and $1$ is decay'],
             [r'$b - 1$ or $1 - b$', 'from the base', r'the percent rate as a decimal: $1.03$ is $3\%$ growth, and $0.97$ is $3\%$ decay'],
             [r'$t$', 'the exponent', 'the number of periods, so check the unit: years, months, hours'],
         ]) +
         figslot('r_read') +
         fbox(frow('factor to rate', r'$1.03 \to 3\%$ increase, &nbsp; $1.3 \to 30\%$ increase, &nbsp; $1.003 \to 0.3\%$ increase, &nbsp; $0.97 \to 3\%$ decrease'),
              frow('from a table', r'divide one output by the output before it. If the ratio stays the same, that ratio is $b$'),
              frow('a time unit in the exponent', r'$b^{\frac{t}{3}}$ means one factor of $b$ for each $3$ units of time'),
              frow('linear or exponential', r'adding the same amount each period is linear. Multiplying by the same factor, or changing by the same percent, is exponential')) +
         figslot('r_linexp') +
         ex('A', r'$y = 2{,}400(1.035)^t$: the initial value is $2{,}400$, and the quantity grows by $3.5\%$ each period.') +
         ex('B', r'$y = 760(0.91)^t$, with $t$ in years: the quantity decreases by $9\%$ each year, because $1 - 0.91 = 0.09$.') +
         ex('C', vtab('$x$', ['$0$', '$1$', '$2$', '$3$'], '$y$', ['$80$', '$120$', '$180$', '$270$']) + r'Each output is $1.5$ times the one before it, and the output at $x = 0$ is $80$, so $y = 80(1.5)^x$.') +
         ex('D', r'$N(t) = 50(2)^{\frac{t}{4}}$, with $t$ in hours: the quantity doubles once for each $4$ hours. After $12$ hours, $N = 50(2)^3 = 400$.') +
         note(r'The factor and the rate are different numbers. In $y = 760(0.91)^t$ the factor is $0.91$, and the percent decrease is $9\%$. Check which one the question asks for.')),
    rule(7, 'A constant to find, and average rate of change', False,
         lead(r'Two more model questions come up less often, and neither needs a new formula. In the first, a model contains an unknown constant, and the question gives one input with its output. In the second, the question asks how fast a function changes, on average, between two inputs.') +
         fbox(frow('a constant to find', 'substitute the known input and output, then solve for the constant'),
              frow('average rate of change', r'$\dfrac{f(b) - f(a)}{b - a}$ &nbsp; the slope of the line through the two points on the graph')) +
         ex('A', r'$C(x) = \dfrac{150x - 600}{x} + k$ and $C(30) = 310$. Substitute: $\dfrac{150(30) - 600}{30} + k = 310$, so $130 + k = 310$ and $k = 180$.') +
         ex('B', r'For $f(x) = x^2$, the average rate of change from $x = -1$ to $x = 4$ is $\dfrac{f(4) - f(-1)}{4 - (-1)} = \dfrac{16 - 1}{5} = 3$.') +
         ex('C', r'For $g(t) = 100(2)^t$, the average rate of change from $t = 1$ to $t = 3$ is $\dfrac{800 - 200}{3 - 1} = 300$. From $t = 3$ to $t = 5$ it is $\dfrac{3{,}200 - 800}{2} = 1{,}200$. An exponential model does not change at a constant rate.') +
         note(r'Evaluate the function at each input first, then subtract. $f(4) - f(-1)$ is not the same as $f(5)$ or $f(3)$.')),
    r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common setup and interpretation mistakes. Review them so you know what to check when an answer seems off.</p>
''',
    mistake(1, 'multiplying the exponents in a product', r'$x^3 \cdot x^4 = x^7$, not $x^{12}$. Exponents multiply only for a power of a power, such as $\left(x^3\right)^4 = x^{12}$.'),
    mistake(2, 'leaving the coefficient out of the power', r'$\left(2x^3\right)^4 = 2^4 \cdot x^{12} = 16x^{12}$. The exponent outside the parentheses applies to each factor inside.'),
    mistake(3, 'reading a negative exponent as a negative number', r'$5^{-2} = \dfrac{1}{25}$, which is positive. The negative sign in the exponent means a reciprocal.'),
    mistake(4, 'adding powers as if they were multiplied', r'$2^5 + 2^5 = 2 \cdot 2^5 = 2^6$, not $2^{10}$. Count how many copies are added, then multiply.'),
    mistake(5, 'swapping the root and the power', r'In $8^{\frac{2}{3}}$ the $3$ is the root and the $2$ is the power: $\left(\sqrt[3]{8}\right)^2 = 4$. Reading it the other way gives $\sqrt{8^3}$, which is about $22.6$.'),
    mistake(6, 'using the rate as the factor', r'Growth of $4\%$ per year means multiplying by $1.04$ each year, not by $0.04$ or by $4$. For a decrease of $4\%$, the factor is $0.96$.'),
    mistake(7, 'misplacing the decimal point in a small rate', r'$0.2\%$ is $0.002$, so a decrease of $0.2\%$ gives a factor of $0.998$. A factor of $0.98$ would be a $2\%$ decrease.'),
    mistake(8, 'answering with the factor when the question asks for the rate', r'In $y = 3{,}000(0.82)^t$ the factor is $0.82$, and the percent decrease is $18\%$. Reread the question to see which number it asks for.'),
    mistake(9, 'treating a repeated percent change as one subtraction', r'A value that falls $10\%$ a year for $3$ years is multiplied by $0.9^3 = 0.729$. That is a decrease of $27.1\%$, not $30\%$.'),
])

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: The exponent laws",
  "rule": r"multiply: add the exponents &nbsp;·&nbsp; divide: subtract the exponents &nbsp;·&nbsp; power of a power: multiply the exponents",
  "say": r"Work from the inside out. Clear the parentheses first, applying the outside power to the coefficient and to each variable. Then combine the powers of the same base, one base at a time.",
  "prob": r"Simplify $\dfrac{\left(2x^3\right)^4 \cdot x^5}{8x^9}$. Write the result in the form $cx^n$.",
  "sol": r"<strong>Step 1: clear the parentheses.</strong> $\left(2x^3\right)^4 = 2^4 \cdot x^{12} = 16x^{12}$.<br><strong>Step 2: multiply across the top.</strong> $16x^{12} \cdot x^5 = 16x^{17}$.<br><strong>Step 3: divide.</strong> $\dfrac{16x^{17}}{8x^9} = 2x^8$.<br><strong>Check:</strong> try $x = 2$. The original is $\dfrac{16^4 \cdot 32}{8 \cdot 512} = 512$, and $2 \cdot 2^8 = 512$. ✓",
  "trap": r"Writing $\left(2x^3\right)^4$ as $2x^{12}$ or as $16x^7$. The outside exponent multiplies the exponent on $x$, and it also applies to the $2$: $2^4 = 16$.",
  "micro": {"q": r"$\dfrac{\left(x^4\right)^3}{x^5} = x^n$. Then $n =$", "accept": ["7"],
            "exp": r"$\left(x^4\right)^3 = x^{12}$, and $\dfrac{x^{12}}{x^5} = x^{12-5} = x^7$."}},
 {"ess": True, "name": "Rule 2: Negative and zero exponents",
  "rule": r"$a^{-n} = \dfrac{1}{a^n}$ &nbsp;·&nbsp; a negative power crosses the fraction bar &nbsp;·&nbsp; $a^0 = 1$",
  "say": r"When an equation has the same variables on both sides, divide to collect each variable in one place. Then clear the negative exponent by multiplying both sides by the matching positive power. Take a root at the end if the question asks for the variable itself.",
  "prob": r"If $m$ and $n$ are positive and $6m^4n^{-2} = 54m^2n^2$, what is $m$ in terms of $n$?",
  "sol": r"<strong>Step 1: divide both sides by $6m^2$.</strong> $m^2n^{-2} = 9n^2$.<br><strong>Step 2: clear the $n^{-2}$.</strong> Multiply both sides by $n^2$: $m^2 = 9n^4$.<br><strong>Step 3: take the square root.</strong> Since $m$ and $n$ are positive, $m = 3n^2$.<br><strong>Check:</strong> let $n = 2$, so $m = 12$. Left side: $6 \cdot 12^4 \cdot \dfrac{1}{4} = 31{,}104$. Right side: $54 \cdot 144 \cdot 4 = 31{,}104$. ✓",
  "trap": r"Stopping at $m^2 = 9n^4$, or taking the root of only one part. The square root of $9n^4$ is $3n^2$: take the root of the $9$ and halve the exponent.",
  "micro": {"q": r"If $k$ is positive and $k^{-2} = 49$, then $k =$", "accept": ["1/7", "0.142", ".142", "0.143", ".143", "0.1428", ".1428", "0.1429", ".1429"],
            "exp": r"$k^{-2} = \dfrac{1}{k^2} = 49$, so $k^2 = \dfrac{1}{49}$ and $k = \dfrac{1}{7}$."}},
 {"ess": True, "name": "Rule 3: Fractional exponents and roots",
  "rule": r"$a^{\frac{m}{n}} = \left(\sqrt[n]{a}\right)^m$ &nbsp;·&nbsp; the power is on top, and the root is on the bottom",
  "say": r"Apply the fractional exponent to each factor inside the parentheses. A power of $\tfrac{1}{2}$ halves each exponent. If the result has to equal a whole number, break that number into prime factors and match the pieces.",
  "prob": r"If $a$ and $b$ are positive integers and $\left(a^4b^6\right)^{\frac{1}{2}} = 392$, what is the value of $a + b$?",
  "sol": r"<strong>Step 1: apply the exponent.</strong> $\left(a^4b^6\right)^{\frac{1}{2}} = a^2b^3$, so $a^2b^3 = 392$.<br><strong>Step 2: factor $392$.</strong> $392 = 8 \cdot 49 = 2^3 \cdot 7^2$.<br><strong>Step 3: match.</strong> $a^2 = 7^2$ and $b^3 = 2^3$, so $a = 7$ and $b = 2$. Then $a + b = 9$.<br><strong>Check:</strong> $7^4 \cdot 2^6 = 2{,}401 \cdot 64 = 153{,}664$, and $392^2 = 153{,}664$. ✓",
  "trap": r"Giving each factor to the other letter. The squared factor goes with $a$, and the cubed factor goes with $b$, so $a = 7$ and $b = 2$.",
  "micro": {"q": r"$81^{\frac{3}{4}} =$", "accept": ["27"],
            "exp": r"Root first: $\sqrt[4]{81} = 3$. Then the power: $3^3 = 27$."}},
 {"ess": True, "name": "Rule 4: One base, then compare exponents",
  "rule": r"rewrite each number as a power of one base &nbsp;·&nbsp; if $b^x = b^y$, then $x = y$",
  "say": r"Look for the smallest base that fits each number in the equation. Rewrite each power in that base, simplify each side to a single power, and set the exponents equal. For a negative base, decide the sign first: an even power is positive.",
  "prob": r"If $\left((-3)^3 \cdot 9^2\right)^2 = \left(3^2\right)^n$, what is the value of $n$?",
  "sol": r"<strong>Step 1: one base inside.</strong> $(-3)^3 = -3^3$ and $9^2 = \left(3^2\right)^2 = 3^4$, so the inside is $-3^3 \cdot 3^4 = -3^7$.<br><strong>Step 2: the outside power.</strong> Squaring removes the negative sign: $\left(-3^7\right)^2 = 3^{14}$.<br><strong>Step 3: the right side.</strong> $\left(3^2\right)^n = 3^{2n}$.<br><strong>Step 4: compare exponents.</strong> $2n = 14$, so $n = 7$.<br><strong>Check:</strong> the left side is $(-27 \cdot 81)^2 = (-2{,}187)^2 = 4{,}782{,}969$, and $9^7 = 4{,}782{,}969$. ✓",
  "trap": r"Adding $3 + 2$ to get $3^5$ inside the parentheses. The $9^2$ has to be rewritten in base $3$ first: $9^2 = 3^4$.",
  "micro": {"q": r"$9^2 + 9^2 + 9^2 = 3^n$. Then $n =$", "accept": ["5"],
            "exp": r"Three copies of $9^2$ is $3 \cdot 9^2 = 3 \cdot 3^4 = 3^5$."}},
 {"ess": True, "name": "Rule 5: Growth and decay factors",
  "rule": r"growth: $P_0(1 + r)^t$ &nbsp;·&nbsp; decay: $P_0(1 - r)^t$ &nbsp;·&nbsp; $r$ is the percent written as a decimal",
  "say": r"Pull three things out of the words: the starting amount, the percent rate, and whether the quantity rises or falls. Turn the rate into a factor, and put the number of periods in the exponent.",
  "prob": r"A lab buys a microscope for $\$6{,}400$. Its resale value falls by $25\%$ each year. Write a model for the value $V(t)$, in dollars, after $t$ years. What is the value after $3$ years?",
  "sol": r"<strong>Given:</strong> a starting value of $6{,}400$, a decrease of $25\%$ per year, and $t = 3$.<br><strong>Step 1: the factor.</strong> A decrease of $25\%$ leaves $75\%$, so the decay factor is $1 - 0.25 = 0.75$.<br><strong>Step 2: the model.</strong> $V(t) = 6{,}400(0.75)^t$.<br><strong>Step 3: evaluate.</strong> $V(3) = 6{,}400(0.75)^3 = 6{,}400(0.421875) = 2{,}700$.<br><strong>Check:</strong> year by year, $6{,}400 \to 4{,}800 \to 3{,}600 \to 2{,}700$. ✓",
  "trap": r"Subtracting $25\%$ of the original price three times: $6{,}400 - 3(1{,}600) = 1{,}600$. Each year's decrease is $25\%$ of that year's value, so the amounts shrink: $1{,}600$, then $1{,}200$, then $900$.",
  "micro": {"q": r"An account opens with $\$900$ and grows by $3.5\%$ each year. In the model $900(b)^t$, $b =$", "accept": ["1.035"],
            "exp": r"$3.5\%$ is $0.035$, so the growth factor is $1 + 0.035 = 1.035$."}},
 {"ess": True, "name": "Rule 6: Reading a model",
  "rule": r"in $y = a \cdot b^t$: $a$ is the value at $t = 0$ &nbsp;·&nbsp; $b$ is the factor per period &nbsp;·&nbsp; the rate is $b - 1$ or $1 - b$",
  "say": r"Name each part before you answer. The number in front is the starting value. The base tells you growth or decay, and its distance from $1$ is the rate. The exponent tells you what one period is.",
  "fig": "s6",
  "prob": r"The function $N(t) = 5{,}200(0.96)^t$ models the number of trees in a forest $t$ years after a survey. Its graph is shown above. What does $5{,}200$ represent? By what percent does the number of trees change each year?",
  "sol": r"<strong>The number in front.</strong> $N(0) = 5{,}200(0.96)^0 = 5{,}200$, so there were $5{,}200$ trees at the time of the survey. On the graph, that is the point on the vertical axis.<br><strong>The base.</strong> $0.96$ is less than $1$, so the number of trees decreases. The rate is $1 - 0.96 = 0.04$.<br><strong>Answer:</strong> the number of trees decreases by $4\%$ each year.<br><strong>Check:</strong> after one year, $5{,}200(0.96) = 4{,}992$. That is a drop of $208$ trees, and $\dfrac{208}{5{,}200} = 0.04$. ✓",
  "trap": r"Answering $96\%$. The base $0.96$ is the part that remains each year. The percent decrease is the part that is removed: $4\%$.",
  "micro": {"q": r"$y = 310(1.008)^t$. Each period, $y$ increases by what percent? (Enter the number without the percent sign.)", "accept": ["0.8", ".8", "0.80", ".80"],
            "exp": r"$1.008 - 1 = 0.008$, which is $0.8\%$."}},
 {"ess": False, "name": "Rule 7: A constant to find, and average rate of change",
  "rule": r"substitute the known pair, then solve for the constant &nbsp;·&nbsp; average rate of change $= \dfrac{f(b) - f(a)}{b - a}$",
  "say": r"A model with an unknown constant becomes a one-variable equation once you substitute the input and the output that the question gives. Write the substitution out in full before you simplify.",
  "prob": r"The function $h(x) = \dfrac{120x - 360}{x} + k$ gives the cost per guest, in dollars, of a banquet for $x$ guests, where $k$ is a constant. If the cost per guest is $\$136$ when $40$ guests attend, what is the value of $k$?",
  "sol": r"<strong>Given:</strong> $h(40) = 136$.<br><strong>Step 1: substitute.</strong> $\dfrac{120(40) - 360}{40} + k = 136$.<br><strong>Step 2: simplify the fraction.</strong> $\dfrac{4{,}800 - 360}{40} = \dfrac{4{,}440}{40} = 111$.<br><strong>Step 3: solve.</strong> $111 + k = 136$, so $k = 25$.<br><strong>Check:</strong> $h(40) = 111 + 25 = 136$. ✓",
  "trap": r"Substituting $136$ for $x$. The number of guests is the input, and the cost is the output: $x = 40$ and $h(x) = 136$.",
  "micro": {"q": r"For $f(x) = x^2 + 1$, the average rate of change from $x = -1$ to $x = 5$ is", "accept": ["4"],
            "exp": r"$f(5) = 26$ and $f(-1) = 2$, so the average rate of change is $\dfrac{26 - 2}{5 - (-1)} = \dfrac{24}{6} = 4$."}},
]
LAST_STARRED_STEP_INDEX = 5  # 0-based index of the last starred step (Rule 6)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
NO_PCT = " (Enter the number without the percent sign.)"
FLUENCY = [
 {"sec": "A. The exponent laws", "items": [
   {"q": r"$x^6 \cdot x^3 = x^n$. Then $n =$", "accept": ["9"], "exp": r"Same base, multiplied: add the exponents. $6 + 3 = 9$."},
   {"q": r"$\left(x^5\right)^4 = x^n$. Then $n =$", "accept": ["20"], "exp": r"A power of a power: multiply the exponents. $5 \cdot 4 = 20$."},
   {"q": r"$\dfrac{x^{11}}{x^4} = x^n$. Then $n =$", "accept": ["7"], "exp": r"Same base, divided: subtract the exponents. $11 - 4 = 7$."},
   {"mc": True, "q": r"$\left(3x^2\right)^3 =$", "opts": ["$3x^5$", "$3x^6$", "$9x^6$", "$27x^6$"], "correct": 3, "exp": r"The power applies to both factors: $3^3 = 27$ and $\left(x^2\right)^3 = x^6$."},
   {"q": r"$\dfrac{\left(x^3\right)^2 \cdot x^4}{x^5} = x^n$. Then $n =$", "accept": ["5"], "exp": r"$\left(x^3\right)^2 = x^6$, then $x^6 \cdot x^4 = x^{10}$, then $\dfrac{x^{10}}{x^5} = x^5$."},
 ]},
 {"sec": "B. Negative and fractional exponents", "items": [
   {"q": r"$2^{-3} =$", "accept": ["1/8", "0.125", ".125"], "exp": r"$2^{-3} = \dfrac{1}{2^3} = \dfrac{1}{8}$."},
   {"q": r"$\left(\dfrac{1}{3}\right)^{-2} =$", "accept": ["9"], "exp": r"Flip the fraction, then square: $3^2 = 9$."},
   {"q": r"$7^0 + 7^1 =$", "accept": ["8"], "exp": r"$7^0 = 1$ and $7^1 = 7$."},
   {"mc": True, "q": r"$\dfrac{1}{x^{-4}} =$", "opts": ["$-x^4$", "$x^{-4}$", "$x^4$", r"$\dfrac{1}{x^4}$"], "correct": 2, "exp": r"A negative power in the denominator moves to the numerator, and its exponent turns positive."},
   {"q": r"$49^{\frac{1}{2}} =$", "accept": ["7"], "exp": r"An exponent of $\tfrac{1}{2}$ is a square root: $\sqrt{49} = 7$."},
   {"q": r"$8^{\frac{4}{3}} =$", "accept": ["16"], "exp": r"Root first: $\sqrt[3]{8} = 2$. Then the power: $2^4 = 16$."},
   {"mc": True, "q": r"$\sqrt[3]{x^5} =$", "opts": [r"$x^{\frac{3}{5}}$", r"$x^{\frac{5}{3}}$", "$x^{15}$", "$x^2$"], "correct": 1, "exp": r"Power over root: the power $5$ goes on top, and the root $3$ goes on the bottom."},
 ]},
 {"sec": "C. One base, then compare exponents", "items": [
   {"q": r"$4^5 = 2^n$. Then $n =$", "accept": ["10"], "exp": r"$4 = 2^2$, so $4^5 = \left(2^2\right)^5 = 2^{10}$."},
   {"q": r"$27^x = 3^{12}$. Then $x =$", "accept": ["4"], "exp": r"$27 = 3^3$, so $3^{3x} = 3^{12}$ and $x = 4$."},
   {"q": r"$2^7 + 2^7 = 2^n$. Then $n =$", "accept": ["8"], "exp": r"Two copies of $2^7$ is $2 \cdot 2^7 = 2^8$."},
   {"q": r"Six copies of $6^4$ are added together. The sum equals $6^n$. Then $n =$", "accept": ["5"], "exp": r"$6 \cdot 6^4 = 6^5$."},
   {"q": r"If $p$ is positive and $p^3 = 5^6$, then $p =$", "accept": ["25"], "exp": r"$5^6 = \left(5^2\right)^3 = 25^3$. The exponents match, so $p = 25$."},
 ]},
 {"sec": "D. Growth and decay factors", "items": [
   {"q": r"A quantity grows by $6\%$ each year. Each year it is multiplied by", "accept": ["1.06"], "exp": r"$1 + 0.06 = 1.06$."},
   {"q": r"A quantity loses $30\%$ of its value each month. Each month it is multiplied by", "accept": ["0.7", ".7", "0.70", ".70", "7/10"], "exp": r"$1 - 0.30 = 0.70$. What remains is $70\%$."},
   {"q": r"A population increases by $0.9\%$ each year. The growth factor is", "accept": ["1.009"], "exp": r"$0.9\%$ is $0.009$, so the factor is $1.009$."},
   {"q": r"$y = 40(1.25)^t$. Each period, $y$ increases by what percent?" + NO_PCT, "accept": ["25"], "exp": r"$1.25 - 1 = 0.25$, which is $25\%$."},
   {"q": r"$y = 900(0.985)^t$. Each period, $y$ decreases by what percent?" + NO_PCT, "accept": ["1.5"], "exp": r"$1 - 0.985 = 0.015$, which is $1.5\%$."},
   {"q": r"$y = 75(3)^t$. The value of $y$ when $t = 0$ is", "accept": ["75"], "exp": r"$3^0 = 1$, so $y = 75$. The number in front is the starting value."},
   {"mc": True, "q": r"A quantity doubles each year. Each year it increases by", "opts": [r"$2\%$", r"$50\%$", r"$100\%$", r"$200\%$"], "correct": 2, "exp": r"A factor of $2$ is $1 + 1.00$, so the increase is $100\%$ of the current amount."},
 ]},
 {"sec": "E. Less common: a constant to find, and average rate of change", "items": [
   {"q": r"$g(x) = \dfrac{60}{x} + k$ and $g(5) = 20$. Then $k =$", "accept": ["8"], "exp": r"$\dfrac{60}{5} + k = 20$, so $12 + k = 20$ and $k = 8$."},
   {"q": r"For $f(x) = x^2$, the average rate of change from $x = 2$ to $x = 6$ is", "accept": ["8"], "exp": r"$\dfrac{36 - 4}{6 - 2} = \dfrac{32}{4} = 8$."},
   {"q": r"For $f(x) = 3^x$, the average rate of change from $x = 0$ to $x = 2$ is", "accept": ["4"], "exp": r"$\dfrac{9 - 1}{2 - 0} = 4$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"Which expression is equivalent to $\left(2x^3\right)\left(5x^4\right)$?",
  "options": ["$7x^7$", "$7x^{12}$", "$10x^7$", "$10x^{12}$"], "correct": 2,
  "sol": r"<strong>Given:</strong> a product of two terms with the same base.<br><br>Multiply the coefficients: $2 \cdot 5 = 10$. Add the exponents: $x^3 \cdot x^4 = x^7$. The product is $10x^7$.<br><strong>Check:</strong> with $x = 2$, the original is $16 \cdot 80 = 1{,}280$, and $10 \cdot 2^7 = 1{,}280$. ✓",
  "trap": r"Choice D multiplies the exponents, which belongs to a power of a power. Choices A and B add the coefficients instead of multiplying them."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"If $8^x = 2^{15}$, what is the value of $x$?",
  "label": "$x =$", "accept": ["5"],
  "sol": r"<strong>Given:</strong> two powers with different bases.<br><br>Rewrite the left side in base $2$: $8^x = \left(2^3\right)^x = 2^{3x}$. Then $2^{3x} = 2^{15}$, so $3x = 15$ and $x = 5$.<br><strong>Check:</strong> $8^5 = 32{,}768$ and $2^{15} = 32{,}768$. ✓",
  "trap": r"Dividing $15$ by $8$, or subtracting $3$ from $15$. The $3$ in $2^3$ multiplies the exponent $x$, so the equation is $3x = 15$."},
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"A savings account opens with a deposit of $\$750$ and earns $4.5\%$ interest each year, added once a year. Which function gives the amount $S$, in dollars, in the account after $t$ years?",
  "options": [r"$S = 750(4.5)^t$", r"$S = 750(1.045)^t$", r"$S = 750(1.45)^t$", r"$S = 750 + (1.045)^t$"], "correct": 1,
  "sol": r"<strong>Given:</strong> a starting amount of $750$ and growth of $4.5\%$ per year.<br><br>$4.5\%$ is $0.045$, so the growth factor is $1.045$. The starting amount is multiplied by that factor once per year: $S = 750(1.045)^t$.<br><strong>Check:</strong> after one year the model gives $750(1.045) = 783.75$. That is $750$ plus $4.5\%$ of $750$, which is $33.75$. ✓",
  "trap": r"Choice C moves the decimal point one place instead of two: a factor of $1.45$ would be growth of $45\%$. Choice A uses the rate as the factor. Choice D adds to the starting amount instead of multiplying it."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"The resale value of a printer decreases by $1.8\%$ each month. This month the printer is worth $\$640$. Its value $p$, in dollars, $n$ months from now is given by $p(n) = 640c^n$, where $c$ is a constant. What is the value of $c$?",
  "label": "$c =$", "accept": ["0.982", ".982"],
  "sol": r"<strong>Given:</strong> a decrease of $1.8\%$ per month, and a model in which $640$ is multiplied by $c$ once per month.<br><br>$c$ is the decay factor. $1.8\%$ is $0.018$, so $c = 1 - 0.018 = 0.982$.<br><strong>Check:</strong> after one month, $640(0.982) = 628.48$. That is a drop of $11.52$, and $\dfrac{11.52}{640} = 0.018$. ✓",
  "trap": r"Entering $0.018$, which is the rate, or $0.82$, which would be a decrease of $18\%$. The factor is the part that remains each month: $98.2\%$ of the value."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"If $k$ is positive and $k^{-2} \cdot 3^2 = 3^6$, what is the value of $k$?",
  "label": "$k =$", "accept": ["1/9", "0.111", ".111", "0.1111", ".1111"],
  "sol": r"<strong>Given:</strong> an equation with a negative exponent on the unknown.<br><br>Divide both sides by $3^2$: $k^{-2} = 3^4 = 81$. A negative exponent is a reciprocal, so $\dfrac{1}{k^2} = 81$ and $k^2 = \dfrac{1}{81}$. Since $k$ is positive, $k = \dfrac{1}{9}$.<br><strong>Check:</strong> $\left(\dfrac{1}{9}\right)^{-2} = 9^2 = 81$, and $81 \cdot 9 = 729 = 3^6$. ✓",
  "trap": r"Answering $9$. That solves $k^2 = 81$, but the exponent is $-2$, so $k$ is the reciprocal: $\dfrac{1}{9}$."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"For $x > 0$, which expression is equivalent to $\sqrt[3]{x^2} \cdot \sqrt{x}$?",
  "options": [r"$x^{\frac{1}{3}}$", r"$x^{\frac{3}{5}}$", r"$x^{\frac{6}{7}}$", r"$x^{\frac{7}{6}}$"], "correct": 3,
  "sol": r"<strong>Given:</strong> a product of two radicals with the same base.<br><br>Rewrite each radical: $\sqrt[3]{x^2} = x^{\frac{2}{3}}$ and $\sqrt{x} = x^{\frac{1}{2}}$. Same base, multiplied, so add the exponents: $\dfrac{2}{3} + \dfrac{1}{2} = \dfrac{4}{6} + \dfrac{3}{6} = \dfrac{7}{6}$.<br><strong>Check:</strong> with $x = 64$, $\sqrt[3]{64^2} = 16$ and $\sqrt{64} = 8$, a product of $128$. And $64^{\frac{7}{6}} = 2^7 = 128$. ✓",
  "trap": r"Choice A multiplies the exponents. Choice B adds the numerators and the denominators separately. Adding fractions needs a common denominator."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": vtab('$x$', ['$0$', '$1$', '$2$', '$3$'], '$f(x)$', ['$96$', '$72$', '$54$', '$40.5$']) + r"The table shows four values of the exponential function $f$. Which equation defines $f$?",
  "options": [r"$f(x) = 96(0.25)^x$", r"$f(x) = 96(0.75)^x$", r"$f(x) = 72(0.75)^x$", r"$f(x) = 96 - 24x$"], "correct": 1,
  "desmos": ["(0,96)", "(1,72)", "(2,54)", "(3,40.5)"],
  "sol": r"<strong>Given:</strong> the outputs at $x = 0$, $1$, $2$ and $3$.<br><br><strong>Starting value.</strong> $f(0) = 96$, so the number in front is $96$.<br><strong>Factor.</strong> $\dfrac{72}{96} = 0.75$, $\dfrac{54}{72} = 0.75$ and $\dfrac{40.5}{54} = 0.75$. The ratio stays the same, so the base is $0.75$.<br>The equation is $f(x) = 96(0.75)^x$.",
  "trap": r"Choice D fits the first two columns, since $96 - 24 = 72$, but it gives $48$ at $x = 2$. Choice A uses the part that is removed ($25\%$) as the base, instead of the part that remains."},
 {"ess": False, "type": "ne", "diff": "Medium",
  "stem": r"The function $c(x) = \dfrac{180x - 540}{x} + k$ gives the cost per person, in dollars, of a guided tour for a group of $x$ people, where $k$ is a constant. If the cost per person for a group of $60$ is $\$250$, what is the value of $k$?",
  "label": "$k =$", "accept": ["79"],
  "sol": r"<strong>Given:</strong> $c(60) = 250$.<br><br>Substitute $x = 60$: $\dfrac{180(60) - 540}{60} + k = 250$. The fraction is $\dfrac{10{,}800 - 540}{60} = \dfrac{10{,}260}{60} = 171$. Then $171 + k = 250$, so $k = 79$.<br><strong>Check:</strong> $171 + 79 = 250$. ✓",
  "trap": r"Dividing only the $180x$ by $x$ and leaving the $540$ whole. The entire numerator is divided by $60$: $180 - 9 = 171$."},
 {"ess": True, "type": "ne", "diff": "Medium-hard", "fig": "p9",
  "stem": r"The graph of the exponential function $f(x) = a \cdot b^x$ is shown above, where $a$ and $b$ are positive constants. The graph passes through the points $(0, 20)$ and $(2, 45)$. What is the value of $b$?",
  "label": "$b =$", "accept": ["1.5", "3/2"],
  "sol": r"<strong>Given:</strong> $f(0) = 20$ and $f(2) = 45$.<br><br><strong>Find $a$.</strong> $f(0) = a \cdot b^0 = a$, so $a = 20$.<br><strong>Find $b$.</strong> $f(2) = 20b^2 = 45$, so $b^2 = \dfrac{45}{20} = 2.25$. Since $b$ is positive, $b = 1.5$.<br><strong>Check:</strong> $20(1.5)^2 = 20(2.25) = 45$. ✓",
  "trap": r"Stopping at $2.25$. The two points are two steps apart, so $2.25$ is the factor for two steps, which is $b^2$. One step is its square root."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"If $a$ and $b$ are positive numbers, $\left(a^{-5}b\right)^{-2} = 81$, and $b = a^3$, what is the value of $a$?",
  "label": "$a =$", "accept": ["3"],
  "sol": r"<strong>Given:</strong> $b = a^3$, so the expression can be written with $a$ alone.<br><br><strong>Substitute.</strong> $a^{-5}b = a^{-5} \cdot a^3 = a^{-2}$.<br><strong>Apply the outside power.</strong> $\left(a^{-2}\right)^{-2} = a^4$.<br><strong>Solve.</strong> $a^4 = 81 = 3^4$, and $a$ is positive, so $a = 3$.<br><strong>Check:</strong> $b = 27$, and $a^{-5}b = \dfrac{27}{243} = \dfrac{1}{9}$. Then $\left(\dfrac{1}{9}\right)^{-2} = 81$. ✓",
  "trap": r"Adding $-2$ and $-2$ on the outside step. A power of a power multiplies: $(-2)(-2) = 4$. Two negative exponents give a positive one here."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"If $p$ and $q$ are positive numbers, $p^{-2} = 6^{-4}$, and $q^{-2} = 9^2$, what is the value of $pq$?",
  "label": "$pq =$", "accept": ["4"],
  "sol": r"<strong>Given:</strong> two equations, each with an exponent of $-2$ on the unknown.<br><br><strong>Find $p$.</strong> Rewrite the right side with an exponent of $-2$: $6^{-4} = \left(6^2\right)^{-2} = 36^{-2}$. So $p = 36$.<br><strong>Find $q$.</strong> $q^{-2} = 81$ means $\dfrac{1}{q^2} = 81$, so $q^2 = \dfrac{1}{81}$ and $q = \dfrac{1}{9}$.<br><strong>Multiply.</strong> $pq = 36 \cdot \dfrac{1}{9} = 4$.<br><strong>Check:</strong> $36^{-2} = \dfrac{1}{1{,}296} = 6^{-4}$, and $\left(\dfrac{1}{9}\right)^{-2} = 81 = 9^2$. ✓",
  "trap": r"Taking $q = 9$. The exponent on $q$ is negative and the exponent on the right is positive, so $q$ is the reciprocal of $9$.",
  "extrasIntro": r"Rewriting one side so the exponents match, then comparing bases. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"If $p$ is positive and $p^{-3} = 4^{-6}$, then $p =$", "label": "$=$", "accept": ["16"], "exp": r"$4^{-6} = \left(4^2\right)^{-3} = 16^{-3}$, so $p = 16$."},
   {"type": "ne", "q": r"If $q$ is positive and $q^{-2} = 25$, then $q =$", "label": "$=$", "accept": ["1/5", "0.2", ".2", "0.20", ".20"], "exp": r"$\dfrac{1}{q^2} = 25$, so $q^2 = \dfrac{1}{25}$ and $q = \dfrac{1}{5}$."},
   {"type": "ne", "q": r"If $m^{-\frac{1}{2}} = 3$, then $m =$", "label": "$=$", "accept": ["1/9", "0.111", ".111", "0.1111", ".1111"], "exp": r"$\dfrac{1}{\sqrt{m}} = 3$, so $\sqrt{m} = \dfrac{1}{3}$ and $m = \dfrac{1}{9}$."},
  ]},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"If $x$ and $y$ are positive and $5x^6y^{-1} = 80x^4y^5$, which of the following gives $x$ in terms of $y$?",
  "options": [r"$x = 4y^3$", r"$x = 16y^3$", r"$x = 4y^6$", r"$x = \dfrac{4}{y^3}$"], "correct": 0,
  "sol": r"<strong>Given:</strong> the same two variables on both sides.<br><br><strong>Divide both sides by $5x^4$.</strong> $x^2y^{-1} = 16y^5$.<br><strong>Multiply both sides by $y$.</strong> $x^2 = 16y^6$.<br><strong>Take the square root.</strong> Both variables are positive, so $x = 4y^3$.<br><strong>Check:</strong> let $y = 2$, so $x = 32 = 2^5$. Left side: $5 \cdot 2^{30} \cdot 2^{-1} = 5 \cdot 2^{29}$. Right side: $80 \cdot 2^{20} \cdot 2^5 = 5 \cdot 2^4 \cdot 2^{25} = 5 \cdot 2^{29}$. ✓",
  "trap": r"Choice C takes the root of $16$ but leaves $y^6$ as it is. Choice B halves the exponent but leaves the $16$. The square root applies to both parts: $\sqrt{16y^6} = 4y^3$."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"If $a$ and $b$ are positive integers and $\left(a^9b^6\right)^{\frac{1}{3}} = 500$, what is the value of $a + b$?",
  "label": "$a + b =$", "accept": ["7"],
  "sol": r"<strong>Given:</strong> a power of $\tfrac{1}{3}$ on a product, equal to a whole number.<br><br><strong>Apply the exponent.</strong> A power of $\tfrac{1}{3}$ divides each exponent by $3$: $a^3b^2 = 500$.<br><strong>Factor $500$.</strong> $500 = 125 \cdot 4 = 5^3 \cdot 2^2$.<br><strong>Match.</strong> $a = 5$ and $b = 2$, so $a + b = 7$.<br><strong>Check:</strong> $5^3 \cdot 2^2 = 125 \cdot 4 = 500$. ✓",
  "trap": r"Halving the exponents out of habit. The exponent here is $\tfrac{1}{3}$, a cube root, so $a^9$ becomes $a^3$ and $b^6$ becomes $b^2$."},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"The value of a boat is modeled by $v(t) = a\left(1 - \dfrac{d}{100}\right)^t$, where $a$ is the purchase price in dollars, $d$ is the percent by which the value falls each year, and $t$ is the number of years since the purchase. A boat is bought for $\$12{,}500$, and its value falls by $20\%$ each year. What is the value of the boat, in dollars, $4$ years after the purchase?",
  "label": "Value $=$", "accept": ["5120", "5120.00"], "desmos": ["12500(1-\\frac{20}{100})^4"],
  "sol": r"<strong>Given:</strong> $a = 12{,}500$, $d = 20$ and $t = 4$.<br><br><strong>The factor.</strong> $1 - \dfrac{20}{100} = 0.8$.<br><strong>Evaluate.</strong> $v(4) = 12{,}500(0.8)^4$. Since $0.8^4 = 0.4096$, that is $12{,}500(0.4096) = 5{,}120$.<br><strong>Check:</strong> year by year, the value is $10{,}000$, then $8{,}000$, then $6{,}400$, then $5{,}120$. ✓",
  "trap": r"Taking $80\%$ off the purchase price, which gives $2{,}500$. Each year's $20\%$ is taken from a smaller value, so the total decrease is less than $80\%$.",
  "extrasIntro": r"Evaluating a model at a given time. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"An amount of $\$8{,}000$ grows by $5\%$ each year. After $2$ years, the amount in dollars is", "label": "$=$", "accept": ["8820", "8820.00"], "exp": r"$8{,}000(1.05)^2 = 8{,}000(1.1025) = 8{,}820$."},
   {"type": "ne", "q": r"A sample of $2{,}000$ bacteria is cut in half each hour. After $4$ hours, the number of bacteria is", "label": "$=$", "accept": ["125"], "exp": r"$2{,}000\left(\dfrac{1}{2}\right)^4 = \dfrac{2{,}000}{16} = 125$."},
   {"type": "ne", "q": r"$f(t) = 10{,}000(1.1)^t$. Then $f(3) =$", "label": "$=$", "accept": ["13310", "13310.0"], "exp": r"$1.1^3 = 1.331$, so $f(3) = 13{,}310$."},
  ]},
 {"ess": True, "type": "mc", "diff": "Hard",
  "stem": r"A culture starts with $400$ bacteria, and the number of bacteria triples every $5$ hours. Which function gives the number of bacteria $P$ after $t$ hours?",
  "options": [r"$P(t) = 400(3)^{5t}$", r"$P(t) = 400(3)^{\frac{t}{5}}$", r"$P(t) = 400(5)^{\frac{t}{3}}$", r"$P(t) = 400(1.6)^{t}$"], "correct": 1,
  "desmos": ["(0,400)", "(5,1200)", "(10,3600)"],
  "sol": r"<strong>Given:</strong> a starting value of $400$ and a factor of $3$ for each $5$ hours.<br><br>The exponent has to count how many $5$-hour periods have passed. After $t$ hours, that count is $\dfrac{t}{5}$, so $P(t) = 400(3)^{\frac{t}{5}}$.<br><strong>Check:</strong> at $t = 5$ the model gives $400(3)^1 = 1{,}200$, three times the start. At $t = 10$ it gives $400(3)^2 = 3{,}600$. ✓",
  "trap": r"Choice A triples the count five times each hour. Test a choice with a time you understand: at $t = 5$ the count should be $1{,}200$, and choice A gives $400(3)^{25}$."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"The function $f(t) = 1{,}500(1.04)^t$ models the value, in dollars, of an investment $t$ years after it was made. By what percent does the value increase over a $2$-year period? (Enter the number without the percent sign.)",
  "label": "Percent $=$", "accept": ["8.16"],
  "sol": r"<strong>Given:</strong> a growth factor of $1.04$ per year.<br><br>Over $2$ years the value is multiplied by $1.04$ twice: $1.04^2 = 1.0816$. A factor of $1.0816$ is an increase of $8.16\%$.<br><strong>Check:</strong> $f(0) = 1{,}500$ and $f(2) = 1{,}500(1.0816) = 1{,}622.40$. The increase is $122.40$, and $\dfrac{122.40}{1{,}500} = 0.0816$. ✓",
  "trap": r"Doubling $4\%$ to get $8\%$. The second year's $4\%$ applies to a larger amount, so two years of growth is a little more than $8\%$."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"For the function $f(x) = x^2 + kx$, where $k$ is a constant, the average rate of change from $x = 1$ to $x = 5$ is $13$. What is the value of $k$?",
  "label": "$k =$", "accept": ["7"],
  "sol": r"<strong>Given:</strong> $\dfrac{f(5) - f(1)}{5 - 1} = 13$.<br><br><strong>Evaluate.</strong> $f(5) = 25 + 5k$ and $f(1) = 1 + k$.<br><strong>Set up.</strong> $\dfrac{(25 + 5k) - (1 + k)}{4} = \dfrac{24 + 4k}{4} = 6 + k$.<br><strong>Solve.</strong> $6 + k = 13$, so $k = 7$.<br><strong>Check:</strong> with $k = 7$, $f(5) = 60$ and $f(1) = 8$, and $\dfrac{60 - 8}{4} = 13$. ✓",
  "trap": r"Evaluating $f(4)$ because $5 - 1 = 4$. The average rate of change uses the value of the function at each endpoint: $f(5) - f(1)$ on top and $5 - 1$ on the bottom."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"Which expression is equivalent to $\dfrac{x^{-2}y^5}{x^3y^2}$?", "opts": [r"$\dfrac{y^3}{x^5}$", r"$\dfrac{y^7}{x}$", r"$xy^3$", r"$x^5y^3$"], "correct": 0,
  "exp": r"Subtract the exponents for each base: $x^{-2-3} = x^{-5}$ and $y^{5-2} = y^3$. The negative power moves to the denominator."},
 {"q": r"A substance decays at a rate of $0.4\%$ per hour. Which function could model the amount of the substance after $t$ hours?", "opts": [r"$60(0.4)^t$", r"$60(0.96)^t$", r"$60(0.996)^t$", r"$60(1.004)^t$"], "correct": 2,
  "exp": r"$0.4\%$ is $0.004$, so the decay factor is $1 - 0.004 = 0.996$. A factor of $0.96$ would be a decrease of $4\%$."},
 {"q": r"What is the value of $16^{\frac{3}{4}}$?", "opts": ["$6$", "$8$", "$12$", "$64$"], "correct": 1,
  "exp": r"Root first: $\sqrt[4]{16} = 2$. Then the power: $2^3 = 8$."},
]

# ---------------------------------------------------------------- FIGURES (coordinate graphs, drawn by the shell's graphSVG)
# A label can carry a raised letter with SUP, since figure text is plain SVG and not MathJax.
FIGS_JS = r'''var SUP_T = '<tspan dy="-5" font-size="10">t</tspan>', SUP_X = '<tspan dy="-5" font-size="10">x</tspan>';
var FIGS = {
    r_growth: { xmin: -0.8, xmax: 5.2, ymin: -1.4, ymax: 11.5, w: 250, h: 200, xl: 't', yl: 'P', alt: 'a growth curve: it starts at the starting amount on the vertical axis and rises faster and faster',
        curves: [{ f: function(x) { return 2 * Math.pow(1.45, x); }, from: 0, to: 4.6 }],
        points: [{ x: 0, y: 2, label: 'starting amount', dx: 8, dy: 16 }],
        labels: [{ x: 0.7, y: 10.1, text: 'growth: factor &gt; 1', dx: 0, dy: 0, cls: 'sm' }] },
    r_decay: { xmin: -0.8, xmax: 5.2, ymin: -1.4, ymax: 11.5, w: 250, h: 200, xl: 't', yl: 'P', alt: 'a decay curve: it starts at the starting amount on the vertical axis and falls, quickly at first and then more slowly',
        curves: [{ f: function(x) { return 9 * Math.pow(0.62, x); }, from: 0, to: 4.8 }],
        points: [{ x: 0, y: 9, label: 'starting amount', dx: 8, dy: 3 }],
        labels: [{ x: 1.25, y: 6.6, text: 'decay: 0 &lt; factor &lt; 1', dx: 0, dy: 0, cls: 'sm' }] },
    r_read: { xmin: -0.8, xmax: 3.6, ymin: -80, ymax: 620, w: 330, h: 250, alt: 'the graph of y = 200 times 1.5 to the power x, passing through (0, 200), (1, 300) and (2, 450); each step to the right multiplies the height by 1.5',
        curves: [{ f: function(x) { return 200 * Math.pow(1.5, x); }, from: -0.6, to: 2.7, label: 'y = 200(1.5)' + SUP_X, lx: 0.32, ly: 545 }],
        points: [{ x: 0, y: 200, label: '(0, 200)', dx: 8, dy: 15 }, { x: 1, y: 300, label: '(1, 300)', dx: 8, dy: 15 }, { x: 2, y: 450, label: '(2, 450)', dx: 8, dy: 15 }],
        ticks: [{ x: 1, label: '1' }, { x: 2, label: '2' }, { x: 3, label: '3' }, { y: 400, label: '400' }],
        labels: [{ x: 0.28, y: 300, text: '× 1.5', dx: 0, dy: 0, cls: 'sm' }, { x: 1.2, y: 440, text: '× 1.5', dx: 0, dy: 0, cls: 'sm' }] },
    r_linexp: { xmin: -0.8, xmax: 5.8, ymin: -100, ymax: 860, w: 330, h: 250, alt: 'a line and an exponential curve that both start at (0, 100): the line adds 50 each step, the curve multiplies by 1.5 each step, and the curve ends far above the line',
        lines: [{ m: 50, b: 100 }],
        curves: [{ f: function(x) { return 100 * Math.pow(1.5, x); }, from: 0, to: 5.25 }],
        points: [{ x: 0, y: 100 }],
        ticks: [{ x: 1, label: '1' }, { x: 2, label: '2' }, { x: 3, label: '3' }, { x: 4, label: '4' }, { x: 5, label: '5' }, { y: 400, label: '400' }, { y: 800, label: '800' }],
        labels: [{ x: 0.3, y: 770, text: 'exponential:', dx: 0, dy: 0, cls: 'sm' }, { x: 0.3, y: 700, text: 'multiply by 1.5 each step', dx: 0, dy: 0, cls: 'sm' },
                 { x: 2.9, y: 150, text: 'linear: add 50 each step', dx: 0, dy: 0, cls: 'sm' }] },
    s6: { xmin: -5, xmax: 45, ymin: -700, ymax: 6300, w: 330, h: 240, xl: 't', yl: 'N', alt: 'the graph of N(t) = 5,200 times 0.96 to the power t: it starts at (0, 5,200) and falls, more slowly as t increases',
        curves: [{ f: function(x) { return 5200 * Math.pow(0.96, x); }, from: 0, to: 42, label: 'N(t) = 5,200(0.96)' + SUP_T, lx: 15, ly: 4300 }],
        points: [{ x: 0, y: 5200, label: '(0, 5,200)', dx: 8, dy: 3 }],
        ticks: [{ x: 10, label: '10' }, { x: 20, label: '20' }, { x: 30, label: '30' }, { x: 40, label: '40' }, { y: 2000, label: '2,000' }, { y: 4000, label: '4,000' }] },
    p9: { xmin: -0.8, xmax: 3.5, ymin: -10, ymax: 80, w: 320, h: 240, alt: 'the graph of an increasing exponential function f with the points (0, 20) and (2, 45) marked',
        curves: [{ f: function(x) { return 20 * Math.pow(1.5, x); }, from: -0.7, to: 3.25, label: 'y = f(x)', lx: 1.7, ly: 68 }],
        points: [{ x: 0, y: 20, label: '(0, 20)', dx: 8, dy: 15 }, { x: 2, y: 45, label: '(2, 45)', dx: 8, dy: 15 }] }
};
function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }'''

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

# figure classes on top of the shell's figure styles; the fig-row rules match sheet 3
FIG_RULES = [
    ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }",
    ".fig .grid { stroke: rgba(45,45,45,0.13); stroke-width: 1; }",
    ".fig .dom { stroke: #BC6C26; stroke-width: 6; stroke-linecap: round; opacity: 0.5; }",
    ".fig text.sm { font-family: 'Inter', sans-serif; font-size: 11px; font-style: normal; fill: #5A5A5A; }",
]
FIG_CSS = '\n'.join(FIG_RULES) + r'''
.fig-row { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: flex-start; justify-content: center; margin: 4px 0 10px; }
.fig-row .fig { margin: 4px 0; }
.ref-page .fig-row { margin-left: 24px; }
.ref-ex .vtab { margin: 2px 0 8px; }
@media (max-width: 768px) { .ref-page .fig-row { margin-left: 0; } }'''
# the same figure styles, on one line, for the downloaded results report (which has its own style block)
REPORT_FIG_CSS = (".fig{display:block;margin:4px 0 10px;max-width:100%;height:auto}.fig .ax{stroke:#2D2D2D;stroke-width:1.4}.fig .ln{stroke:#21442B;stroke-width:2;fill:none}"
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
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Exponents and Exponential Models</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Exponents and Exponential Models</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; EXPONENTS AND EXPONENTIAL MODELS')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Exponents and Exponential Models')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Exponent Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Exponent rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>an exponent counts repeated multiplication.</strong> The laws in Rules 1 to 4 are ways of counting factors. The models in Rules 5 and 6 multiply a starting amount by the same factor once per period. Each question asks you to notice which of these you are looking at, and then to count with care.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. You can enter fractions as 1/8 or 0.125; both are accepted. Sections A to D use the starred rules, and section E covers the unstarred one. Once you feel comfortable, try responding without pausing for long.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end. One includes a table, and one includes a graph. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type: are you rewriting an expression, or building or reading a model? Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it, and <em>Load into Desmos</em> places a question&#39;s points in the graph when it has some. Use Desmos when it helps: evaluating a model at a given time, seeing whether a model rises or falls, or testing answer choices against a table. For the exponent laws and equivalent expressions, working by hand is usually quicker.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These seven questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each one pairs a rule you already have with a second idea (two unknowns with negative exponents, one variable written in terms of another, a cube root on a product, a model written with letters, a time unit in the exponent, growth over two periods, an average rate of change with a constant in it). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the one marked <em>extra</em> leans on the unstarred rule.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time an exponent or an exponential model shows up. Make it an if-then. (Shape: “When a model gives a percent rate, I ______ before I write the base.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">The growth factor in Rule 5 is the multiplier from the percentages sheet: <a href="' + PCT_URL + '" ' + A_STYLE + '>SAT Math 6: Percentages &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For function notation such as $f(3)$ and for reading values from a graph, see <a href="' + FUNC_URL + '" ' + A_STYLE + '>SAT Math 3: Functions &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">Ready for the next topic? Continue the series with <a href="' + CIRCLES_URL + '" ' + A_STYLE + '>SAT Math 8: Circle Equations &#8594;</a></p>',
        flags=re.S)

    # --- data arrays
    for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
        html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

    # --- figures: FIGS and fig(), then the curve renderer, the grid and a clip path inside the shell's graphSVG
    start = html.index('var FIGS = {')
    tail = "function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }"
    end = html.index(tail) + len(tail)
    html = html[:start] + FIGS_JS + html[end:]
    html = replace_once(html,
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';""",
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker>' +
        '<clipPath id="clip' + id + '"><rect x="' + X(xmin) + '" y="' + Y(ymax) + '" width="' + (X(xmax) - X(xmin)) + '" height="' + (Y(ymin) - Y(ymax)) + '"/></clipPath></defs>';""")
    html = replace_once(html, "    if (o.poly) {\n", GRID_JS + "    if (o.poly) {\n")
    html = replace_once(html, "    (o.lines || []).forEach(function(l) {\n", CURVES_JS + "    (o.lines || []).forEach(function(l) {\n")
    # axis names other than x and y (a model in t, for example)
    html = replace_once(html, """(Y(0) + 15) + '">x</text>';""", """(Y(0) + 15) + '">' + (o.xl || 'x') + '</text>';""")
    html = replace_once(html, """(Y(ymax) + 6) + '">y</text>';""", """(Y(ymax) + 6) + '">' + (o.yl || 'y') + '</text>';""")
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
    html = html.replace('sat-linear-sheet:rule', 'sat-exponents-sheet:rule')
    html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                        "(i === %d ? 'That was the last starred step. The last one covers ideas that come up less often.' : '')" % LAST_STARRED_STEP_INDEX)
    html = replace_once(html, "Step 1 of 9", "Step 1 of %d" % len(STEPS))

    # --- LCC voice pass: visible shell and results-kit copy (the last entry renames a column for the Desmos sheets only)
    html = voice.apply(html, voice.SHELL[:-1], 'shell')

    dash = chr(8212)                                  # the em dash, written this way so this file contains none
    if dash in html:
        i = html.index(dash)
        sys.exit('em dash found: ' + html[max(0, i - 80):i + 40])
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out, len(html), 'bytes;', len(STEPS), 'steps,', sum(len(s['items']) for s in FLUENCY), 'skill practice,',
          len(GAUNTLET), 'practice,', len(CHALLENGE), 'challenge,', len(EXIT), 'exit, 6 figures')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else OUT)
