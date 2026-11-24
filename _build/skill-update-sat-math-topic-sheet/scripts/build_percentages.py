#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-6-Percentages.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the content
swaps. The sheet covers percent of, percent change, the multiplier, changes in a row, working
backward to an original value, percent sentences with letters, and mixtures. Its question types
follow Tips 26 and 29 of the class book, with original numbers and contexts throughout.

It was copied from build_special_right_triangles.py. The figures here are bar models, a multiplier
chain, mixing containers and one bar graph, drawn in Python as plain SVG (a FIGS entry with an
`svg` key); anything else in FIGS would still go to the shell's graphSVG.
Answer key: verify_percentages.py (same folder) recomputes every answer."""
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
OUT = ROOT + '/test-prep/sat/SAT-Math-6-Percentages.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
RATIOS_URL = SITE + 'test-prep/sat/SAT-Math-5-Ratios-Rates-Proportions.html'
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
RULES = r'''
<p class="ref-intro">A percent is a ratio out of $100$, and many percent questions come down to a single multiplication. This sheet covers the percent question types that come up most often on the SAT: taking a percent of a number, finding a percent change, applying a change with a multiplier, combining two changes, and working backward to an original value. Two less common types follow: percent sentences written with letters, and mixtures. As you practice, start by identifying the question type. Then decide whether to translate the sentence into an equation or use a multiplier, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''' + rule(1, 'Percent of: translate the sentence', True, r'''
<p class="ref-lead">Percent means out of $100$. In a percent sentence, <strong>of</strong> means times and <strong>is</strong> means equals. Translate the sentence one word at a time, then solve the equation you wrote.</p>
<div class="fbox">
''' + frow('percent to decimal', r'$p\% = \dfrac{p}{100}$, so $35\% = 0.35$, $4\% = 0.04$ and $150\% = 1.5$') +
      frow(r'$p\%$ of $n$', r'$\dfrac{p}{100} \cdot n$') +
      frow(r'what percent of $n$ is $a$?', r'$\dfrac{a}{n} \times 100$') +
      frow('a percent of a percent', r'multiply the decimals: $30\%$ of $50\%$ is $0.30 \times 0.50 = 0.15$, or $15\%$') + r'''</div>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>The sentence</th><th>The equation</th><th>The unknown</th></tr></thead><tbody>
<tr><td class="fname">What is $35\%$ of $80$?</td><td>$x = 0.35 \cdot 80$</td><td>the part</td></tr>
<tr><td class="fname">$28$ is what percent of $80$?</td><td>$28 = \dfrac{x}{100} \cdot 80$</td><td>the percent</td></tr>
<tr><td class="fname">$28$ is $35\%$ of what number?</td><td>$28 = 0.35 \cdot x$</td><td>the whole</td></tr>
</tbody></table></div>
''' + ex('A', r'What is $35\%$ of $80$? Multiply: $0.35 \times 80 = 28$.') +
    ex('B', r'$18$ is what percent of $72$? Divide the part by the whole: $\dfrac{18}{72} = 0.25$, so the answer is $25\%$.') +
    ex('C', r'$15\%$ of a number is $45$. Write $0.15n = 45$, so $n = \dfrac{45}{0.15} = 300$.') +
    ex('D', r'What is $30\%$ of $50\%$ of $240$? The two percents multiply to $0.15$, and $0.15 \times 240 = 36$.') +
    note(r'A percent can be greater than $100$. $150\%$ of a number is $1.5$ times the number, and $300\%$ of a number is $3$ times the number.')) + \
rule(2, 'Percent change: divide by the original', True, r'''
<p class="ref-lead">A percent change compares the amount of change with the starting value. The original value goes in the denominator, whether the value went up or down.</p>
''' + figslot('r_change') + r'''<div class="fbox">
''' + frow('percent change', r'$\dfrac{\text{new} - \text{original}}{\text{original}} \times 100$') +
      frow('which value is the original', r'the value before the change. In the phrase from $A$ to $B$, the original is $A$') +
      frow('the sign', r'a positive result is an increase, and a negative result is a decrease') +
      frow('doubling and tripling', r'a value that doubles has increased by $100\%$. A value that triples has increased by $200\%$') + r'''</div>
''' + ex('A', r'A price rises from $\$40$ to $\$52$. The change is $12$, and $\dfrac{12}{40} = 0.30$: a $30\%$ increase.') +
    ex('B', r'Attendance falls from $250$ to $210$. The change is $40$, and $\dfrac{40}{250} = 0.16$: a $16\%$ decrease.') +
    ex('C', r'A value goes from $50$ to $150$. The change is $100$, and $\dfrac{100}{50} = 2$: a $200\%$ increase.') +
    note(r'<strong>Percent of</strong> and <strong>percent greater than</strong> are different comparisons. In Example C, $150$ is $300\%$ of $50$, and $150$ is $200\%$ greater than $50$. The gap between the two is the original $100\%$.')) + \
rule(3, 'The multiplier', True, r'''
<p class="ref-lead">An increase of $p\%$ keeps the original $100\%$ and adds $p\%$ more, so the new value is $(100 + p)\%$ of the original. A decrease of $p\%$ leaves $(100 - p)\%$. Either way, the whole change is one multiplication. This sheet calls that number <strong>the multiplier</strong>.</p>
''' + figslot('r_mult') + r'''<div class="fbox">
''' + frow(r'increase by $p\%$', r'multiply by $1 + \dfrac{p}{100}$') +
      frow(r'decrease by $p\%$', r'multiply by $1 - \dfrac{p}{100}$') +
      frow('reading a multiplier', r'$1.3n$ is $30\%$ more than $n$. &nbsp; $0.82n$ is $18\%$ less than $n$. &nbsp; $2.1n$ is $110\%$ more than $n$') + r'''</div>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Increase</th><th>Multiplier</th><th>Decrease</th><th>Multiplier</th></tr></thead><tbody>
<tr><td class="fname">up $8\%$</td><td>$1.08$</td><td class="fname">down $8\%$</td><td>$0.92$</td></tr>
<tr><td class="fname">up $35\%$</td><td>$1.35$</td><td class="fname">down $35\%$</td><td>$0.65$</td></tr>
<tr><td class="fname">up $120\%$</td><td>$2.20$</td><td class="fname">down $60\%$</td><td>$0.40$</td></tr>
</tbody></table></div>
''' + ex('A', r'A $\$60$ item is marked up $35\%$. Multiply: $60 \times 1.35 = 81$, so the new price is $\$81$.') +
    ex('B', r'A population of $1{,}500$ falls by $12\%$. Multiply: $1{,}500 \times 0.88 = 1{,}320$.') +
    ex('C', r'An $8\%$ sales tax is added to a $\$45$ purchase. Multiply: $45 \times 1.08 = 48.60$, so the total is $\$48.60$.') +
    ex('D', r'The expression $0.7x$ gives a price after a discount, where $x$ is the original price. Since $0.7 = 1 - 0.30$, the discount is $30\%$.') +
    note(r'Repeating the same multiplier each period, such as $1.04$ every year, gives an exponential model. <a href="' + EXP_URL + '" ' + A_STYLE + r'>SAT Math 7: Exponents and Exponential Models</a> covers those.')) + \
rule(4, 'Changes in a row multiply', True, r'''
<p class="ref-lead">When one percent change follows another, the second change applies to the new value, not to the original. Multiply the multipliers. Adding or subtracting the percents gives a different result, and it is not the correct one.</p>
''' + figslot('r_chain') + r'''<div class="fbox">
''' + frow('two changes', r'$\text{new} = \text{original} \times m_1 \times m_2$') +
      frow('overall percent change', r'$(m_1 m_2 - 1) \times 100$') +
      frow('up, then down by the same percent', r'$1.2 \times 0.8 = 0.96$: a $4\%$ decrease overall, not a return to the start') +
      frow('the order of the changes', r'$m_1 m_2 = m_2 m_1$, so the order does not affect the final value') +
      frow('no starting value given', r'choose $100$. The final value is then the percent of the original') + r'''</div>
''' + ex('A', r'A price rises $20\%$ and then falls $25\%$. Multiply: $1.20 \times 0.75 = 0.90$. The price ends $10\%$ below where it started, not $5\%$ below.') +
    ex('B', r'A value rises $10\%$ and then rises $10\%$ again. Multiply: $1.1 \times 1.1 = 1.21$, a $21\%$ increase, not $20\%$.') +
    ex('C', r'An $\$80$ jacket is discounted $25\%$, and then a $5\%$ tax is added. Multiply: $80 \times 0.75 \times 1.05 = 63$, so the total is $\$63$.')) + \
rule(5, 'Working backward to the original', True, r'''
<p class="ref-lead">Some questions give the value after a change and ask for the value before it. Write the change as an equation, original times multiplier equals new, and divide by the multiplier. Taking the same percent off the new value does not undo the change, because the percent was a percent of the original.</p>
<div class="fbox">
''' + frow('the equation', r'$\text{original} \times m = \text{new}$') +
      frow('solve it', r'$\text{original} = \dfrac{\text{new}}{m}$') +
      frow(r'after an increase of $p\%$', r'divide by $1 + \dfrac{p}{100}$') +
      frow(r'after a decrease of $p\%$', r'divide by $1 - \dfrac{p}{100}$') +
      frow('a size check', r'after an increase, the original is smaller than the new value. After a decrease, it is larger') + r'''</div>
''' + ex('A', r'After a $25\%$ increase, a monthly rent is $\$1{,}500$. Write $1.25x = 1{,}500$, so $x = 1{,}200$. Check: $25\%$ of $1{,}200$ is $300$, and $1{,}200 + 300 = 1{,}500$.') +
    ex('B', r'After a $30\%$ discount, a coat costs $\$84$. Write $0.70x = 84$, so $x = 120$. The original price was $\$120$.') +
    ex('C', r'A total of $\$64.80$ includes an $8\%$ tax. Write $1.08x = 64.80$, so the price before tax is $\$60$.') +
    note(r'In Example A, taking $25\%$ off $\$1{,}500$ gives $\$1{,}125$, which is not the original rent. $25\%$ of the new value is more than $25\%$ of the original.')) + \
rule(6, 'Percent sentences with letters', False, r'''
<p class="ref-lead">When a percent sentence uses letters in place of numbers, translate it the same way. You get an equation that relates the letters. The question usually asks for a ratio, or for one letter as a percent of the other.</p>
<div class="fbox">
''' + frow(r'$a$ is $p\%$ of $b$', r'$a = \dfrac{p}{100} \cdot b$') +
      frow(r'$b$ is what percent of $a$?', r'$\dfrac{b}{a} \times 100$') +
      frow('flipping the comparison', r'if $a$ is $20\%$ of $b$, then $a = 0.2b$ and $b = 5a$, so $b$ is $500\%$ of $a$') +
      frow(r'$a$ is $p\%$ greater than $b$', r'$a = \left(1 + \dfrac{p}{100}\right) b$') + r'''</div>
''' + ex('A', r'$x$ is $40\%$ of $5y$. Then $x = 0.4 \cdot 5y = 2y$, so $y = \tfrac{1}{2}x$: $y$ is $50\%$ of $x$.') +
    ex('B', r'$3a + 2b$ is equal to $175\%$ of $8b$. Then $3a + 2b = 14b$, so $3a = 12b$ and $\dfrac{a}{b} = 4$.') +
    ex('C', r'$30\%$ of $n$ is $45$. What is $20\%$ of $3n$? Since $20\%$ of $3n$ is $0.6n$, it is twice $0.3n$: $90$. Finding $n = 150$ first also works: $0.20 \times 450 = 90$.') +
    note(r'If the letters are hard to follow, choose a number. In Example A, let $y = 10$. Then $x = 0.4 \times 50 = 20$, and $10$ is $50\%$ of $20$.')) + \
rule(7, 'Mixtures: track the pure amount', False, r'''
<p class="ref-lead">A $p\%$ solution is $p\%$ pure ingredient, and the rest is something else. When two amounts are combined, the pure amounts add and the total amounts add. One equation for the pure ingredient is usually enough.</p>
''' + figslot('r_mix') + r'''<div class="fbox">
''' + frow('pure amount', r'$\dfrac{p}{100} \times \text{total amount}$') +
      frow('the equation', r'pure in the first $+$ pure in the second $=$ pure in the mixture') +
      frow('adding water', r'water is a $0\%$ solution: the pure amount stays the same, and the total grows') +
      frow('adding the pure ingredient', r'it is a $100\%$ solution: the pure amount and the total grow by the same number') +
      frow('a size check', r'the final percent is between the two starting percents') + r'''</div>
''' + ex('A', r'How many liters of water must be added to $30$ liters of a $20\%$ bleach solution to make a $12\%$ bleach solution? The bleach is $0.20 \times 30 = 6$ liters, and adding water does not change it. Write $\dfrac{6}{30 + w} = 0.12$. Then $30 + w = 50$, so $w = 20$.') +
    ex('B', r'How many liters of a $10\%$ acid solution must be added to $12$ liters of a $40\%$ acid solution to make a $20\%$ acid solution? Write $0.10x + 0.40(12) = 0.20(x + 12)$. Then $0.10x + 4.8 = 0.20x + 2.4$, so $2.4 = 0.10x$ and $x = 24$.') +
    ex('C', r'How many ounces of pure juice must be added to $20$ ounces of a drink that is $40\%$ juice to make a drink that is $50\%$ juice? The drink starts with $8$ ounces of juice. Write $\dfrac{8 + x}{20 + x} = 0.50$. Then $8 + x = 10 + 0.5x$, so $x = 4$.') +
    note(r'The same equation works when the amounts are letters. Write the pure amount on each side, then solve for the letter the question asks about.')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common setup and interpretation mistakes. Review them so you know what to check when an answer seems off.</p>
''' + mistake(1, 'dividing by the new value', r'From $40$ to $52$, the change of $12$ is divided by the original, $40$, which gives $30\%$. Dividing by $52$ gives about $23\%$, which answers a different question.') + \
      mistake(2, 'adding the percents of two changes', r'Up $20\%$ and then down $25\%$ is $1.20 \times 0.75 = 0.90$, a $10\%$ decrease. Adding $20$ and $-25$ suggests a $5\%$ decrease, because it treats both percents as percents of the same value.') + \
      mistake(3, 'expecting an increase and an equal decrease to cancel', r'Up $20\%$ and then down $20\%$ is $1.2 \times 0.8 = 0.96$. The decrease is taken of a larger value, so it removes more than the increase added.') + \
      mistake(4, 'undoing a change by reversing the percent', r'If a value is $1{,}500$ after a $25\%$ increase, the original is $\dfrac{1{,}500}{1.25} = 1{,}200$. Taking $25\%$ off $1{,}500$ gives $1{,}125$.') + \
      mistake(5, 'reading percent of as percent greater than', r'$150$ is $300\%$ of $50$, and it is $200\%$ greater than $50$. Check which comparison the question uses.') + \
      mistake(6, 'placing the decimal point', r'$4\%$ is $0.04$, not $0.4$. $0.5\%$ is $0.005$. Divide the percent by $100$ each time.') + \
      mistake(7, 'averaging the percents in a mixture', r'Mixing a $10\%$ solution with a $40\%$ solution gives $25\%$ only when the two amounts are equal. Otherwise, track the pure amount and the total.') + \
      mistake(8, 'answering a different quantity', r'After you compute, reread the question. It may ask for the new value, the amount of change, the percent change or the original value.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Percent of",
  "rule": r"of means times &nbsp;·&nbsp; is means equals &nbsp;·&nbsp; $p\% = \dfrac{p}{100}$",
  "say": r"Read the sentence one word at a time and write what each word means. A percent of a percent is two multiplications in a row. When the same unknown number appears on both sides, it cancels.",
  "prob": r"$60\%$ of $40\%$ of a positive number is equal to $30\%$ of $k\%$ of the same number. What is the value of $k$?",
  "sol": r"<strong>Key:</strong> $n$ is the positive number.<br><strong>Step 1: translate each side.</strong> Left side: $0.60 \times 0.40 \times n = 0.24n$. Right side: $0.30 \times \dfrac{k}{100} \times n$.<br><strong>Step 2: set them equal and cancel $n$.</strong> $0.24 = 0.30 \cdot \dfrac{k}{100}$.<br><strong>Step 3: solve.</strong> $\dfrac{k}{100} = \dfrac{0.24}{0.30} = 0.8$, so $k = 80$.<br><strong>Check:</strong> with $n = 100$, the left side is $60\%$ of $40$, which is $24$. The right side is $30\%$ of $80$, which is $24$. ✓",
  "trap": r"Writing $k$ in place of $\dfrac{k}{100}$. The symbol $k\%$ means $k$ out of $100$, so $0.8$ is the decimal form of $k\%$, not the value of $k$.",
  "micro": {"q": r"$27$ is $18\%$ of what number?", "accept": ["150"],
            "exp": r"$0.18n = 27$, so $n = \dfrac{27}{0.18} = 150$."}},
 {"ess": True, "name": "Rule 2: Percent change",
  "rule": r"$\dfrac{\text{new} - \text{original}}{\text{original}} \times 100$ &nbsp;·&nbsp; the original is the value before the change",
  "say": r"Find the amount of change first. Then decide which value came first: that is the original, and it goes in the denominator.",
  "fig": "s2",
  "prob": r"Last year a club had $160$ members. This year it has $200$ members, as shown above. By what percent did the membership increase?",
  "sol": r"<strong>Given:</strong> original $= 160$, new $= 200$.<br><strong>Step 1: the change.</strong> $200 - 160 = 40$.<br><strong>Step 2: divide by the original.</strong> $\dfrac{40}{160} = 0.25$.<br><strong>Step 3: write it as a percent.</strong> The membership increased by $25\%$.<br><strong>Check:</strong> $25\%$ of $160$ is $40$, and $160 + 40 = 200$. ✓",
  "trap": r"Dividing by $200$. That gives $20\%$, which is the percent decrease from $200$ back to $160$. An increase is measured from the starting value.",
  "micro": {"q": r"A price drops from $\$80$ to $\$68$. The percent decrease is", "accept": ["15", "15%"],
            "exp": r"The change is $12$, and $\dfrac{12}{80} = 0.15$, or $15\%$."}},
 {"ess": True, "name": "Rule 3: The multiplier",
  "rule": r"up $p\%$: multiply by $1 + \dfrac{p}{100}$ &nbsp;·&nbsp; down $p\%$: multiply by $1 - \dfrac{p}{100}$",
  "say": r"Start from $100\%$ of the original. An increase adds to it, and a decrease takes away from it. Write the result as a decimal, and the change becomes one multiplication.",
  "prob": r"The price of a monthly transit pass is $\$75$. The price is going to increase by $12\%$. What number can you multiply $75$ by to get the new price, and what is the new price?",
  "sol": r"<strong>Given:</strong> original price $= 75$, increase $= 12\%$.<br><strong>Step 1: the multiplier.</strong> $100\% + 12\% = 112\%$, so the multiplier is $1.12$.<br><strong>Step 2: multiply.</strong> $75 \times 1.12 = 84$. The new price is $\$84$.<br><strong>Check:</strong> $12\%$ of $75$ is $9$, and $75 + 9 = 84$. ✓",
  "trap": r"Multiplying by $0.12$. That gives $9$, the amount of the increase. The new price also includes the original $100\%$, so the multiplier is $1.12$.",
  "micro": {"q": r"The expression $0.72p$ gives the price of an item after a discount, where $p$ is the original price. The percent discount is", "accept": ["28", "28%"],
            "exp": r"$0.72 = 1 - 0.28$, so the price was reduced by $28\%$."}},
 {"ess": True, "name": "Rule 4: Changes in a row",
  "rule": r"$\text{new} = \text{original} \times m_1 \times m_2$ &nbsp;·&nbsp; multiply the multipliers, do not add the percents",
  "say": r"Write a multiplier for each change. The second change acts on the value the first change produced, so the multipliers multiply. When no starting value is given, the product tells you the overall change.",
  "fig": "s4",
  "prob": r"The price of a ticket is increased by $25\%$, and then the new price is decreased by $40\%$, as shown above. What is the overall percent change in the price?",
  "sol": r"<strong>Given:</strong> first multiplier $= 1.25$, second multiplier $= 1 - 0.40 = 0.60$.<br><strong>Step 1: multiply.</strong> $1.25 \times 0.60 = 0.75$.<br><strong>Step 2: read the result.</strong> The final price is $75\%$ of the original, so the overall change is a $25\%$ decrease.<br><strong>Check with $100$:</strong> $100 \to 125 \to 75$. ✓",
  "trap": r"Adding $25$ and $-40$ to get a $15\%$ decrease. The $40\%$ is taken of the raised price, $125$, so it removes $50$, not $40$.",
  "micro": {"q": r"A value increases by $40\%$ and then decreases by $50\%$. The final value is what percent of the original?", "accept": ["70", "70%"],
            "exp": r"$1.4 \times 0.5 = 0.7$, so the final value is $70\%$ of the original."}},
 {"ess": True, "name": "Rule 5: Working backward to the original",
  "rule": r"$\text{original} \times m = \text{new}$ &nbsp;·&nbsp; $\text{original} = \dfrac{\text{new}}{m}$",
  "say": r"When a question gives the value after a change, call the original $x$ and write the change as an equation. Then divide by the multiplier. Compare sizes at the end: after a discount, the original should be larger than the sale price.",
  "prob": r"After a $20\%$ discount, a pair of shoes costs $\$68$. What was the original price?",
  "sol": r"<strong>Key:</strong> $x$ is the original price, and the multiplier is $1 - 0.20 = 0.80$.<br><strong>Step 1: write the equation.</strong> $0.80x = 68$.<br><strong>Step 2: divide.</strong> $x = \dfrac{68}{0.80} = 85$. The original price was $\$85$.<br><strong>Check:</strong> $20\%$ of $85$ is $17$, and $85 - 17 = 68$. ✓",
  "trap": r"Adding $20\%$ of $68$ back on. That gives $68 + 13.60 = 81.60$. The discount was $20\%$ of the original price, which is not known yet, so it has to come from the equation.",
  "micro": {"q": r"After a $10\%$ increase, a bill is $\$143$. The bill before the increase, in dollars, was", "accept": ["130", "$130", "130.00", "$130.00"],
            "exp": r"$1.10x = 143$, so $x = 130$."}},
 {"ess": False, "name": "Rule 6: Percent sentences with letters",
  "rule": r"$a$ is $p\%$ of $b$ means $a = \dfrac{p}{100} \cdot b$ &nbsp;·&nbsp; $b$ as a percent of $a$ is $\dfrac{b}{a} \times 100$",
  "say": r"Translate the sentence into an equation between the letters and simplify it. Then solve for the letter the question asks about, and write the multiplier as a percent.",
  "prob": r"If $p$ is $20\%$ of $4q$, then $q$ is what percent of $p$?",
  "sol": r"<strong>Step 1: translate.</strong> $p = 0.20 \cdot 4q = 0.8q$.<br><strong>Step 2: solve for $q$.</strong> $q = \dfrac{p}{0.8} = 1.25p$.<br><strong>Step 3: write it as a percent.</strong> $q$ is $125\%$ of $p$.<br><strong>Check with numbers:</strong> let $q = 10$. Then $p$ is $20\%$ of $40$, which is $8$, and $\dfrac{10}{8} = 1.25$. ✓",
  "trap": r"Answering $80\%$. That is $p$ as a percent of $q$. The question asks for the reverse comparison, so the two letters switch roles.",
  "micro": {"q": r"If $m$ is $25\%$ of $n$, then $n$ is what percent of $m$?", "accept": ["400", "400%"],
            "exp": r"$m = 0.25n$, so $n = 4m$, which is $400\%$ of $m$."}},
 {"ess": False, "name": "Rule 7: Mixtures",
  "rule": r"pure in the first $+$ pure in the second $=$ pure in the mixture &nbsp;·&nbsp; pure amount $= \dfrac{p}{100} \times$ total",
  "say": r"Name the unknown amount, then write the pure ingredient in each container. The totals add, and the pure amounts add. That gives one equation.",
  "fig": "s7",
  "prob": r"How many liters of a $15\%$ acid solution must be added to $8$ liters of a $45\%$ acid solution to produce a $25\%$ acid solution?",
  "sol": r"<strong>Key:</strong> $x$ is the number of liters of the $15\%$ solution. The mixture has $x + 8$ liters.<br><strong>Step 1: the acid in each part.</strong> $0.15x$ liters, and $0.45 \times 8 = 3.6$ liters.<br><strong>Step 2: write the equation.</strong> $0.15x + 3.6 = 0.25(x + 8)$.<br><strong>Step 3: solve.</strong> $0.15x + 3.6 = 0.25x + 2$, so $1.6 = 0.10x$ and $x = 16$.<br><strong>Check:</strong> the acid is $0.15 \times 16 + 3.6 = 6$ liters out of $24$ liters, and $\dfrac{6}{24} = 25\%$. ✓",
  "trap": r"Leaving the added liters out of the total. The mixture has $x + 8$ liters, not $8$. Averaging the two percents does not work either: $30\%$ would be correct only for equal amounts.",
  "micro": {"q": r"A $50$-liter solution is $30\%$ acid. The number of liters of acid in it is", "accept": ["15"],
            "exp": r"$0.30 \times 50 = 15$."}},
]
LAST_STARRED_STEP_INDEX = 4  # 0-based index of the last starred step (Rule 5)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
FLUENCY = [
 {"sec": "A. Percents, decimals and multipliers", "items": [
   {"q": r"Written as a decimal, $7\%$ is", "accept": ["0.07", ".07"], "exp": r"$7 \div 100 = 0.07$. Compare $70\%$, which is $0.7$."},
   {"q": r"The multiplier for a $30\%$ increase is", "accept": ["1.3", "1.30"], "exp": r"$100\% + 30\% = 130\%$, or $1.3$."},
   {"q": r"The multiplier for a $30\%$ decrease is", "accept": ["0.7", ".7", "0.70", ".70"], "exp": r"$100\% - 30\% = 70\%$, or $0.7$."},
   {"mc": True, "q": r"Multiplying a value by $0.45$ is the same as", "opts": [r"increasing it by $45\%$", r"decreasing it by $45\%$", r"decreasing it by $55\%$", r"decreasing it by $5.5\%$"], "correct": 2, "exp": r"$0.45 = 1 - 0.55$, so $55\%$ of the value is removed and $45\%$ remains."},
   {"q": r"The multiplier for a $140\%$ increase is", "accept": ["2.4", "2.40"], "exp": r"$100\% + 140\% = 240\%$, or $2.4$. The value more than doubles."},
 ]},
 {"sec": "B. Percent of", "items": [
   {"q": r"$20\%$ of $85$ is", "accept": ["17"], "exp": r"$0.20 \times 85 = 17$."},
   {"q": r"$9$ is what percent of $36$?", "accept": ["25", "25%"], "exp": r"$\dfrac{9}{36} = 0.25$, or $25\%$."},
   {"q": r"$40\%$ of a number is $32$. The number is", "accept": ["80"], "exp": r"$0.40n = 32$, so $n = 80$."},
   {"q": r"$125\%$ of $48$ is", "accept": ["60"], "exp": r"$1.25 \times 48 = 60$. More than $100\%$ of a number is more than the number."},
 ]},
 {"sec": "C. Percent change", "items": [
   {"q": r"A value goes from $50$ to $62$. The percent increase is", "accept": ["24", "24%"], "exp": r"The change is $12$, and $\dfrac{12}{50} = 0.24$."},
   {"q": r"A value goes from $120$ to $90$. The percent decrease is", "accept": ["25", "25%"], "exp": r"The change is $30$, and $\dfrac{30}{120} = 0.25$. The original, $120$, goes in the denominator."},
   {"q": r"A value goes from $40$ to $100$. The percent increase is", "accept": ["150", "150%"], "exp": r"The change is $60$, and $\dfrac{60}{40} = 1.5$, or $150\%$."},
   {"mc": True, "q": r"A value triples. The percent increase is", "opts": [r"$30\%$", r"$200\%$", r"$300\%$", r"$33\tfrac{1}{3}\%$"], "correct": 1, "exp": r"From $x$ to $3x$ the change is $2x$, and $\dfrac{2x}{x} = 2$, or $200\%$. The new value is $300\%$ of the original."},
 ]},
 {"sec": "D. Apply a change, and changes in a row", "items": [
   {"q": r"$\$40$ increased by $15\%$ is, in dollars,", "accept": ["46", "$46", "46.00", "$46.00"], "exp": r"$40 \times 1.15 = 46$."},
   {"q": r"A value goes up $10\%$ and then down $10\%$. The final value is what percent of the original?", "accept": ["99", "99%"], "exp": r"$1.1 \times 0.9 = 0.99$, or $99\%$."},
   {"mc": True, "q": r"A price rises $20\%$ and then rises $50\%$. The overall percent increase is", "opts": [r"$60\%$", r"$70\%$", r"$80\%$", r"$100\%$"], "correct": 2, "exp": r"$1.2 \times 1.5 = 1.8$, an $80\%$ increase. Adding the percents gives $70\%$, which leaves out the growth on the first increase."},
   {"q": r"A value goes down $50\%$ and then down $20\%$. The overall percent decrease is", "accept": ["60", "60%"], "exp": r"$0.5 \times 0.8 = 0.4$, so $40\%$ remains and the decrease is $60\%$."},
 ]},
 {"sec": "E. Working backward", "items": [
   {"q": r"After a $25\%$ increase, a value is $60$. The original value was", "accept": ["48"], "exp": r"$1.25x = 60$, so $x = 48$."},
   {"q": r"A total of $\$53$ includes a $6\%$ tax. The price before tax, in dollars, was", "accept": ["50", "$50", "50.00", "$50.00"], "exp": r"$1.06x = 53$, so $x = 50$."},
   {"mc": True, "q": r"After a $20\%$ discount, an item costs $d$ dollars. The original price, in dollars, was", "opts": [r"$0.8d$", r"$1.2d$", r"$\dfrac{d}{0.8}$", r"$\dfrac{d}{1.2}$"], "correct": 2, "exp": r"$0.8x = d$, so $x = \dfrac{d}{0.8}$, which is $1.25d$."},
 ]},
 {"sec": "F. Less common: letters and mixtures", "items": [
   {"q": r"If $c$ is $125\%$ of $d$, then $d$ is what percent of $c$?", "accept": ["80", "80%"], "exp": r"$c = 1.25d$, so $d = \dfrac{c}{1.25} = 0.8c$."},
   {"q": r"If $x$ is $75\%$ of $2y$, then $\dfrac{x}{y} =$", "accept": ["3/2", "1.5"], "exp": r"$x = 0.75 \cdot 2y = 1.5y$."},
   {"q": r"The number of liters of acid in $60$ liters of a $15\%$ acid solution is", "accept": ["9"], "exp": r"$0.15 \times 60 = 9$."},
   {"q": r"Five liters of water are added to $15$ liters of a drink that is $40\%$ juice. The new percent of juice is", "accept": ["30", "30%"], "exp": r"The juice is $0.40 \times 15 = 6$ liters, and the total is now $20$ liters: $\dfrac{6}{20} = 30\%$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"In a survey of $450$ people, $28\%$ said they commute by bicycle. How many of the people surveyed said they commute by bicycle?",
  "options": ["$28$", "$126$", "$324$", "$422$"], "correct": 1,
  "sol": r"<strong>Given:</strong> the whole is $450$ people, and the percent is $28\%$.<br><br>Of means times: $0.28 \times 450 = 126$.",
  "trap": r"Choice C is $72\%$ of $450$, the people who did not say bicycle. Choice A is the percent itself, and choice D subtracts it from $450$. A percent has to be multiplied by the whole before it counts people."},
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"The table shows the number of books of each type in a classroom library.<table class='vtab'><tr><th>Type</th><th>Number of books</th></tr><tr><td>Fiction</td><td>$84$</td></tr><tr><td>Biography</td><td>$36$</td></tr><tr><td>Science</td><td>$48$</td></tr><tr><td>History</td><td>$32$</td></tr></table>What percent of the books in the library are science books?",
  "options": [r"$16\%$", r"$24\%$", r"$42\%$", r"$48\%$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $48$ science books. The whole is the total: $84 + 36 + 48 + 32 = 200$.<br><br>Divide the part by the whole: $\dfrac{48}{200} = 0.24$, or $24\%$.",
  "trap": r"Choice D uses the count, $48$, as the percent. That would be correct only if the total were $100$. Add the four counts to find the whole first. Choices A and C are the percents for history and fiction."},
 {"ess": True, "type": "ne", "diff": "Easy to medium",
  "stem": r"A plant grew from $20$ inches tall to $27$ inches tall. Its height increased by $p\%$. What is the value of $p$?",
  "label": "$p =$", "accept": ["35", "35%"],
  "sol": r"<strong>Given:</strong> original $= 20$, new $= 27$.<br><br>The change is $27 - 20 = 7$. Divide by the original: $\dfrac{7}{20} = 0.35$, so $p = 35$.<br><strong>Check:</strong> $35\%$ of $20$ is $7$. ✓",
  "trap": r"Dividing by the new height. $\dfrac{7}{27}$ is about $0.26$, which compares the change with the ending value. A percent increase is taken of the starting value."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"The expression $1.24c$ gives the total cost, in dollars, of a meal after a tip is added, where $c$ is the cost of the meal before the tip. The tip is what percent of $c$?",
  "options": [r"$0.24\%$", r"$1.24\%$", r"$24\%$", r"$124\%$"], "correct": 2,
  "sol": r"<strong>Given:</strong> total $= 1.24c$.<br><br>Split the multiplier: $1.24c = c + 0.24c$. The first part is the meal, and the second part is the tip. As a percent, $0.24$ is $24\%$.",
  "trap": r"Choice D is the total as a percent of $c$. The tip is only the part beyond $100\%$. Choice A leaves the decimal unchanged: $0.24$ is $24\%$, since percent means out of $100$."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"After a $15\%$ discount, the price of a tablet is $\$272$. What was the price of the tablet, in dollars, before the discount?",
  "label": "Price $=$", "accept": ["320", "$320", "320.00", "$320.00"],
  "sol": r"<strong>Key:</strong> $x$ is the price before the discount. The multiplier is $1 - 0.15 = 0.85$.<br><br>$0.85x = 272$, so $x = \dfrac{272}{0.85} = 320$.<br><strong>Check:</strong> $15\%$ of $320$ is $48$, and $320 - 48 = 272$. ✓",
  "trap": r"Adding $15\%$ of $272$ to the sale price, which gives $312.80$. The discount was $15\%$ of the original price, so divide the sale price by $0.85$."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"The price of a concert ticket was increased by $10\%$, and then the new price was decreased by $30\%$. Which of the following is true about the price after these two changes?",
  "options": [r"It is $20\%$ less than the original price.", r"It is $23\%$ less than the original price.", r"It is $33\%$ less than the original price.", r"It is $40\%$ less than the original price."], "correct": 1,
  "sol": r"<strong>Given:</strong> the multipliers are $1.10$ and $0.70$.<br><br>$1.10 \times 0.70 = 0.77$. The final price is $77\%$ of the original, so it is $23\%$ less.<br><strong>Check with $100$:</strong> $100 \to 110 \to 77$. ✓",
  "trap": r"Choice A adds $10$ and $-30$. The $30\%$ decrease is taken of the raised price, $110$, so it removes $33$, not $30$. Choice C reports that $33$ without the $10$ that was added first."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"If $40$ percent of $w$ is $70$, what is $30$ percent of $2w$?",
  "options": ["$52.5$", "$105$", "$175$", "$210$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $0.40w = 70$.<br><br><strong>One way.</strong> $w = \dfrac{70}{0.40} = 175$, so $2w = 350$ and $0.30 \times 350 = 105$.<br><strong>Another way.</strong> $30\%$ of $2w$ is $0.6w$, which is $1.5$ times $0.4w$: $1.5 \times 70 = 105$.",
  "trap": r"Choice A is $30\%$ of $w$, not of $2w$, and choice C is $w$ itself. After you find $w$, reread the question: the last step uses $2w$."},
 {"ess": True, "type": "ne", "diff": "Medium", "fig": "p8",
  "stem": r"The bar graph above shows the number of visitors to a museum in each of four months. The number of visitors in March was $p\%$ greater than the number of visitors in February. What is the value of $p$?",
  "label": "$p =$", "accept": ["40", "40%"],
  "sol": r"<strong>Given:</strong> from the graph, February $= 250$ and March $= 350$.<br><br>The comparison is to February, so February is the original. The change is $350 - 250 = 100$, and $\dfrac{100}{250} = 0.40$, so $p = 40$.",
  "trap": r"Dividing by the March value. $\dfrac{100}{350}$ is about $0.29$. In the phrase $p\%$ greater than February, February is the base."},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"A store raised the price of a jacket by $25\%$. Later, during a sale, the store reduced the raised price by $20\%$, and the jacket sold for $\$96$. What was the price of the jacket before it was raised?",
  "options": [r"$\$86.40$", r"$\$91.43$", r"$\$96.00$", r"$\$100.80$"], "correct": 2,
  "sol": r"<strong>Key:</strong> $x$ is the price before it was raised. The multipliers are $1.25$ and $0.80$.<br><br>$x \times 1.25 \times 0.80 = 96$. Since $1.25 \times 0.80 = 1$, the two changes cancel here, and $x = 96$.<br><strong>Check:</strong> $96 \times 1.25 = 120$, and $120 \times 0.80 = 96$. ✓",
  "trap": r"Choice B treats the two changes as a net $5\%$ increase and divides $96$ by $1.05$. A $25\%$ increase is undone by a $20\%$ decrease, because the $20\%$ is taken of a larger value."},
 {"ess": False, "type": "ne", "diff": "Medium-hard",
  "stem": r"A fruit punch is $25\%$ juice. How many liters of water must be added to $18$ liters of the punch to make a punch that is $15\%$ juice?",
  "label": "Liters $=$", "accept": ["12"],
  "sol": r"<strong>Key:</strong> $w$ is the number of liters of water added.<br><br>The juice is $0.25 \times 18 = 4.5$ liters, and adding water does not change it. The new total is $18 + w$ liters, so $\dfrac{4.5}{18 + w} = 0.15$. Then $18 + w = \dfrac{4.5}{0.15} = 30$, and $w = 12$.<br><strong>Check:</strong> $\dfrac{4.5}{30} = 0.15$. ✓",
  "trap": r"Stopping at $30$. That is the total amount of punch after the water is added. The question asks for the water added, $30 - 18$."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"$35\%$ of $60\%$ of a positive number is equal to $14\%$ of $k\%$ of the same number. What is the value of $k$?",
  "label": "$k =$", "accept": ["150"],
  "sol": r"<strong>Key:</strong> $n$ is the positive number.<br><br><strong>Left side.</strong> $0.35 \times 0.60 \times n = 0.21n$.<br><strong>Right side.</strong> $0.14 \times \dfrac{k}{100} \times n$.<br><strong>Solve.</strong> The $n$ cancels: $0.21 = 0.14 \cdot \dfrac{k}{100}$, so $\dfrac{k}{100} = 1.5$ and $k = 150$.<br><strong>Check with $n = 100$:</strong> $35\%$ of $60$ is $21$, and $14\%$ of $150$ is $21$. ✓",
  "trap": r"Translate each side, then let the unknown number cancel. A percent can be greater than $100$, so $k = 150$ is a reasonable answer. Note that $1.5$ is the decimal form of $k\%$, not the value of $k$.",
  "extrasIntro": r"A percent of a percent: multiply the decimals, and let the number cancel. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"$20\%$ of $45\%$ of a number is equal to $k\%$ of the number. The value of $k$ is", "label": "$k =$", "accept": ["9"], "exp": r"$0.20 \times 0.45 = 0.09$, which is $9\%$."},
   {"type": "ne", "q": r"$50\%$ of $x\%$ of $80$ is $10$. The value of $x$ is", "label": "$x =$", "accept": ["25"], "exp": r"$0.50 \times \dfrac{x}{100} \times 80 = 0.4x$, and $0.4x = 10$ gives $x = 25$."},
   {"type": "ne", "q": r"$80\%$ of $25\%$ of a number is equal to $40\%$ of $k\%$ of the same number. The value of $k$ is", "label": "$k =$", "accept": ["50"], "exp": r"$0.80 \times 0.25 = 0.20$, and $0.20 = 0.40 \cdot \dfrac{k}{100}$ gives $k = 50$."},
  ]},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"The value of a collectible card rose by $8$ percent in one month and fell by $4$ percent the next month. Over the two months, the value of the card rose by what percent overall?",
  "options": [r"$3.68\%$", r"$4\%$", r"$4.32\%$", r"$12\%$"], "correct": 0,
  "sol": r"<strong>Given:</strong> the multipliers are $1.08$ and $0.96$.<br><br>$1.08 \times 0.96 = 1.0368$. The final value is $103.68\%$ of the starting value, so the card rose by $3.68\%$.<br><strong>Check with $100$:</strong> $100 \to 108 \to 103.68$. ✓",
  "trap": r"Two changes in a row multiply: $1.08 \times 0.96$. Subtracting the percents, as choice B does, misses that the $4\%$ is taken of the higher value, $108$, so the drop is $4.32$."},
 {"ess": False, "type": "mc", "diff": "Medium-hard",
  "stem": r"If $5a + 2b$ is equal to $140$ percent of $10b$, what is the value of $\dfrac{a}{b}$?",
  "options": [r"$\dfrac{5}{12}$", r"$\dfrac{12}{5}$", r"$\dfrac{14}{5}$", r"$\dfrac{16}{5}$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $5a + 2b = 1.40 \cdot 10b$.<br><br><strong>Simplify the right side.</strong> $1.40 \times 10b = 14b$.<br><strong>Solve for the ratio.</strong> $5a + 2b = 14b$, so $5a = 12b$ and $\dfrac{a}{b} = \dfrac{12}{5}$.<br><strong>Check with numbers:</strong> let $b = 5$, so $a = 12$. Then $5a + 2b = 70$, and $140\%$ of $50$ is $70$. ✓",
  "trap": r"Translate the percent first, then collect the $b$ terms on one side before you divide. Choice A is $\dfrac{b}{a}$, the reverse of the ratio the question asks for.",
  "extrasIntro": r"Letters in a percent sentence: translate, simplify, then solve for what is asked. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"If $r$ is $125\%$ of $4s$, then $s$ is what percent of $r$?", "label": "$=$", "accept": ["20", "20%"], "exp": r"$r = 1.25 \cdot 4s = 5s$, so $s = \dfrac{r}{5}$, which is $20\%$ of $r$."},
   {"type": "ne", "q": r"If $2u + v$ is equal to $120\%$ of $5v$, then $\dfrac{u}{v} =$", "label": "$=$", "accept": ["5/2", "2.5"], "exp": r"$2u + v = 6v$, so $2u = 5v$ and $\dfrac{u}{v} = \dfrac{5}{2}$."},
   {"type": "ne", "q": r"If $15\%$ of $t$ is $24$, then $45\%$ of $2t$ is", "label": "$=$", "accept": ["144"], "exp": r"$45\%$ of $2t$ is $0.9t$, which is $6$ times $0.15t$: $6 \times 24 = 144$. Finding $t = 160$ first also works."},
  ]},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"A furniture store sets the price of each item at $60\%$ above its wholesale cost. During a clearance sale, the store takes $25\%$ off that price and sells a chair for $\$144$. What was the wholesale cost of the chair, in dollars?",
  "label": "Cost $=$", "accept": ["120", "$120", "120.00", "$120.00"],
  "sol": r"<strong>Key:</strong> $c$ is the wholesale cost. The multipliers are $1.60$ and $0.75$.<br><br><strong>Write the equation.</strong> $c \times 1.60 \times 0.75 = 144$.<br><strong>Combine the multipliers.</strong> $1.60 \times 0.75 = 1.20$, so $1.20c = 144$.<br><strong>Solve.</strong> $c = \dfrac{144}{1.20} = 120$.<br><strong>Check:</strong> $120 \times 1.60 = 192$, and $192 \times 0.75 = 144$. ✓",
  "trap": r"Combine the multipliers first, then undo the combined change with one division. Adding the percents would suggest a net increase of $35\%$. The product, $1.20$, is the actual net change."},
 {"ess": True, "type": "mc", "diff": "Hard",
  "stem": r"The number $a$ is $60\%$ greater than the number $b$. The number $b$ is $50\%$ less than the number $c$. The number $a$ is what percent of $c$?",
  "options": [r"$10\%$", r"$80\%$", r"$110\%$", r"$120\%$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $a = 1.60b$ and $b = 0.50c$.<br><br>Substitute: $a = 1.60 \times 0.50c = 0.80c$. So $a$ is $80\%$ of $c$.<br><strong>Check with numbers:</strong> let $c = 100$. Then $b = 50$ and $a = 80$. ✓",
  "trap": r"The phrases greater than and less than each set a multiplier, $1.60$ and $0.50$, and the multipliers multiply. Adding $60$ and $-50$ to $100$, as choice C does, treats both percents as percents of the same number."},
 {"ess": False, "type": "mc", "diff": "Hard",
  "stem": r"How many liters of water must be added to $V$ liters of a $c\%$ acid solution to produce a $d\%$ acid solution, where $0 < d < c$?",
  "options": [r"$\dfrac{V(c - d)}{d}$", r"$\dfrac{V(c - d)}{c}$", r"$\dfrac{Vd}{c - d}$", r"$\dfrac{V(c - d)}{100}$"], "correct": 0,
  "sol": r"<strong>Key:</strong> $x$ is the number of liters of water added.<br><br><strong>The acid.</strong> It starts at $\dfrac{c}{100} \cdot V$ liters, and adding water does not change it.<br><strong>The equation.</strong> The new total is $V + x$ liters, so $\dfrac{cV}{100} = \dfrac{d}{100}(V + x)$.<br><strong>Solve.</strong> $cV = dV + dx$, so $dx = V(c - d)$ and $x = \dfrac{V(c - d)}{d}$.<br><strong>Check with numbers:</strong> $V = 30$, $c = 20$ and $d = 12$ give $\dfrac{30 \cdot 8}{12} = 20$, which matches Example A of Rule 7. ✓",
  "trap": r"Adding water leaves the amount of acid unchanged, so set the acid before equal to the acid after. When every choice is a formula, testing easy numbers is a good check.",
  "extrasIntro": r"Mixtures with numbers: one equation for the pure amount. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"How many liters of pure antifreeze must be added to $12$ liters of a $30\%$ antifreeze solution to make a $44\%$ antifreeze solution?", "label": "$=$", "accept": ["3"], "exp": r"$\dfrac{3.6 + x}{12 + x} = 0.44$, so $3.6 + x = 5.28 + 0.44x$. Then $0.56x = 1.68$ and $x = 3$."},
   {"type": "ne", "q": r"How many liters of water must be added to $24$ liters of a $50\%$ acid solution to make a $30\%$ acid solution?", "label": "$=$", "accept": ["16"], "exp": r"The acid is $12$ liters. $\dfrac{12}{24 + w} = 0.30$ gives $24 + w = 40$, so $w = 16$."},
   {"type": "ne", "q": r"How many liters of a $60\%$ acid solution must be added to $10$ liters of a $20\%$ acid solution to make a $44\%$ acid solution?", "label": "$=$", "accept": ["15"], "exp": r"$0.60x + 2 = 0.44(x + 10)$, so $0.16x = 2.4$ and $x = 15$."},
  ]},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"A tank holds $40$ liters of a $25\%$ acid solution. Some of the solution is drained and replaced with the same number of liters of pure acid, so the tank again holds $40$ liters. The new solution is $40\%$ acid. How many liters were drained?",
  "label": "Liters $=$", "accept": ["8"],
  "sol": r"<strong>Key:</strong> $x$ is the number of liters drained and replaced.<br><br><strong>Acid left after draining.</strong> $0.25(40 - x)$ liters.<br><strong>Acid added.</strong> $x$ liters, since pure acid is $100\%$ acid.<br><strong>The equation.</strong> $0.25(40 - x) + x = 0.40 \times 40$.<br><strong>Solve.</strong> $10 - 0.25x + x = 16$, so $0.75x = 6$ and $x = 8$.<br><strong>Check:</strong> $0.25 \times 32 = 8$ liters remain, and $8$ more are added. That is $16$ liters of acid, and $\dfrac{16}{40} = 40\%$. ✓",
  "trap": r"Draining removes solution, not pure acid: $x$ liters drained carry away only $0.25x$ liters of acid. Track the acid at each stage, and write $0.25(40 - x)$, not $10 - x$."},
 {"ess": True, "type": "ne", "diff": "Hard · exponent blend",
  "stem": r"The value of a machine decreases by $20\%$ each year. After $3$ years, the value of the machine is $p\%$ of its original value. What is the value of $p$?",
  "label": "$p =$", "accept": ["51.2", "51.2%"],
  "sol": r"<strong>Given:</strong> the multiplier for one year is $1 - 0.20 = 0.80$, and it is applied $3$ times.<br><br>$0.80 \times 0.80 \times 0.80 = 0.80^3 = 0.512$. The value is $51.2\%$ of the original, so $p = 51.2$.<br><strong>Check with $1{,}000$:</strong> $1{,}000 \to 800 \to 640 \to 512$. ✓",
  "trap": r"A repeated percent change is a repeated multiplier: $0.80^3$, not $1 - 3(0.20)$. Each year's decrease is $20\%$ of a smaller value, so the total drop is less than $60\%$. Repeating a multiplier this way is an exponential model, the subject of SAT Math 7."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"An item priced at $\$70$ is on sale for $30\%$ off. What is the sale price?", "opts": [r"$\$21$", r"$\$40$", r"$\$49$", r"$\$91$"], "correct": 2,
  "exp": r"The multiplier is $0.70$, and $70 \times 0.70 = 49$. The amount of the discount is $\$21$, which is not what the question asks for."},
 {"q": r"A value increases from $150$ to $174$. What is the percent increase?", "opts": [r"$13.8\%$", r"$16\%$", r"$24\%$", r"$116\%$"], "correct": 1,
  "exp": r"The change is $24$, and $\dfrac{24}{150} = 0.16$. Dividing by $174$ gives about $13.8\%$, which uses the new value as the base."},
 {"q": r"After a $20\%$ increase, a price is $\$90$. What was the price before the increase?", "opts": [r"$\$70$", r"$\$72$", r"$\$75$", r"$\$108$"], "correct": 2,
  "exp": r"$1.20x = 90$, so $x = 75$. Taking $20\%$ off $\$90$ gives $\$72$, which is not the original."},
]

# ---------------------------------------------------------------- FIGURES (plain SVG, drawn here in Python)
# Bar models, a multiplier chain, mixing containers and one bar graph. Figure text never uses a dollar
# sign, so MathJax has nothing to pick up inside an SVG.
MINUS, TIMES, DIVIDE = chr(8722), chr(215), chr(247)


def fmt(v):
    return ('%g' % v).replace('-', MINUS)

def svg(w, h, body, alt):
    return ('<svg class="fig" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">' % (w, h, w, h, alt)) + body + '</svg>'

def T(x, y, t, cls='lb', anc='middle'):
    return '<text class="%s" text-anchor="%s" x="%.1f" y="%.1f">%s</text>' % (cls, anc, x, y, t)

def R(x, y, w, h, cls):
    return '<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (cls, x, y, w, h)

def LN(x1, y1, x2, y2, cls):
    return '<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cls, x1, y1, x2, y2)


def change_bars(orig, new, alt, show_change=True, caption=None):
    """Two bars on one scale: the original value, and the new value with the change marked."""
    W, x0, span = 330, 12, 290.0
    sc = span / max(orig, new)
    lo, hi = min(orig, new), max(orig, new)
    b = T(x0, 15, 'Original value: ' + fmt(orig), 'lbb', 'start') + R(x0, 22, orig * sc, 26, 'bar')
    b += T(x0, 71, 'New value: ' + fmt(new), 'lbb', 'start') + R(x0, 78, lo * sc, 26, 'bar')
    b += R(x0 + lo * sc, 78, (hi - lo) * sc, 26, 'chg' if new > orig else 'cut')
    b += T(x0 + (lo + hi) / 2 * sc, 96, (('+' if new > orig else MINUS) + fmt(hi - lo)) if show_change else '?', 'lb')
    b += LN(x0 + orig * sc, 17, x0 + orig * sc, 110, 'dash')
    h = 116
    if caption:
        b += T(x0, 131, caption, 'lb', 'start')
        h = 142
    return svg(W, h, b, alt)


def mult_fig(alt):
    """100% of the original with the increase added on, and with the decrease taken off."""
    x0, full, hh = 12, 230.0, 28
    b = T(x0, 15, 'Increase by 35%', 'lbb', 'start')
    b += R(x0, 22, full, hh, 'bar') + T(x0 + full / 2, 41, '100%', 'lb')
    b += R(x0 + full, 22, full * 0.35, hh, 'chg') + T(x0 + full * 1.175, 41, '+35%', 'lb')
    b += T(x0, 67, '135% of the original: multiply by 1.35', 'lb', 'start')
    b += T(x0, 101, 'Decrease by 20%', 'lbb', 'start')
    b += R(x0, 108, full * 0.8, hh, 'bar') + T(x0 + full * 0.4, 127, '80%', 'lb')
    b += R(x0 + full * 0.8, 108, full * 0.2, hh, 'cut') + T(x0 + full * 0.9, 127, MINUS + '20%', 'lb')
    b += T(x0, 153, '80% of the original: multiply by 0.80', 'lb', 'start')
    return svg(336, 164, b, alt)


def chain(vals, mults, alt, caption=None):
    """Three value boxes joined by arrows; each arrow carries its multiplier."""
    W, bw, bh, y = 340, 74, 34, 28
    gap = (W - 20 - 3 * bw) / 2.0
    subs = ['original', 'after change 1', 'after change 2']
    b = ''
    for i, v in enumerate(vals):
        x = 10 + i * (bw + gap)
        b += R(x, y, bw, bh, 'bar' if i == 0 else 'chg') + T(x + bw / 2, y + 22, v, 'lb') + T(x + bw / 2, y + bh + 15, subs[i], 'lbs')
    for i, m in enumerate(mults):
        x1 = 10 + i * (bw + gap) + bw + 5
        x2 = x1 + gap - 10
        ym = y + bh / 2.0
        b += LN(x1, ym, x2 - 6, ym, 'arr') + '<polygon class="arrh" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (x2, ym, x2 - 8, ym - 4.5, x2 - 8, ym + 4.5)
        b += T((x1 + x2) / 2, ym - 8, TIMES + ' ' + m, 'lbb')
    h = y + bh + 26
    if caption:
        b += T(W / 2, y + bh + 40, caption, 'lb')
        h = y + bh + 50
    return svg(W, h, b, alt)


def mixture(parts, alt, note=None):
    """Three containers: first + second = mixture. Each part is (height in px, pure fraction, [three label lines])."""
    W, jw, base = 372, 62, 112
    cx = [56, 180, 304]
    b = ''
    for (hpx, frac, lines), c in zip(parts, cx):
        b += R(c - jw / 2, base - hpx, jw, hpx, 'jar')
        if frac:
            b += R(c - jw / 2 + 1, base - hpx * frac, jw - 2, hpx * frac - 1, 'pure')
        for k, t in enumerate(lines):
            b += T(c, base + 17 + 15 * k, t, 'lbb' if k == 0 else 'lb')
    b += T((cx[0] + cx[1]) / 2.0, base - 30, '+', 'op') + T((cx[1] + cx[2]) / 2.0, base - 30, '=', 'op')
    h = base + 56
    if note:
        b += T(W / 2, h + 10, note, 'lbs')
        h += 18
    return svg(W, h, b, alt)


def bar_chart(title, cats, vals, ymax, step, label_step, ytitle, xtitle, alt):
    W, H, L0, R0, T0, B0 = 340, 250, 54, 328, 30, 200
    sy = (B0 - T0) / float(ymax)
    b = T((L0 + R0) / 2, 16, title, 'lbb')
    for v in range(0, ymax + 1, step):
        yy = B0 - v * sy
        b += LN(L0, yy, R0, yy, 'gl')
        if v % label_step == 0:
            b += T(L0 - 7, yy + 4, str(v), 'lbs', 'end')
    slot = (R0 - L0) / float(len(cats))
    bw = slot * 0.56
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = L0 + i * slot + (slot - bw) / 2
        b += R(x, B0 - v * sy, bw, v * sy, 'colbar') + T(x + bw / 2, B0 + 16, c, 'lb')
    b += LN(L0, T0, L0, B0, 'ax2') + LN(L0, B0, R0, B0, 'ax2')
    b += '<text class="lbs" text-anchor="middle" transform="rotate(-90 14 %.1f)" x="14" y="%.1f">%s</text>' % ((T0 + B0) / 2, (T0 + B0) / 2, ytitle)
    b += T((L0 + R0) / 2, B0 + 36, xtitle, 'lbs')
    return svg(W, H, b, alt)


FIGS = {}
# --- Rule 2: a percent change is the change compared with the original (Example A: 40 to 52)
FIGS['r_change'] = {'svg': change_bars(40, 52, 'Two bars on the same scale. The original value is 40. The new value is 52, and the extra 12 is highlighted.',
                                       caption='change %s original = 12 %s 40 = 0.30, a 30%% increase' % (DIVIDE, DIVIDE))}
# --- Rule 3: where the multiplier comes from
FIGS['r_mult'] = {'svg': mult_fig('Two bar models. An increase of 35 percent adds 35 percent to the full 100 percent bar, for 135 percent. A decrease of 20 percent removes 20 percent of the bar, leaving 80 percent.')}
# --- Rule 4: two changes in a row (Example A: up 20 percent, then down 25 percent)
FIGS['r_chain'] = {'svg': chain(['100', '120', '90'], ['1.20', '0.75'], 'A chain of three boxes: 100 times 1.20 is 120, and 120 times 0.75 is 90.',
                                caption='1.20 %s 0.75 = 0.90: a 10%% decrease overall' % TIMES)}
# --- Rule 7: adding water (Example A). Drawn to scale: 30 liters, 20 liters, 50 liters
FIGS['r_mix'] = {'svg': mixture([(54, 0.20, ['30 L', '20% bleach', '6 L of bleach']), (36, 0, ['w L', 'water', '0 L of bleach']), (90, 0.12, ['(30 + w) L', '12% bleach', '6 L of bleach'])],
                                'Three containers. 30 liters of a 20 percent bleach solution plus w liters of water equals 30 plus w liters of a 12 percent solution. The amount of bleach, 6 liters, is the same before and after.')}
# --- Step 2: membership goes from 160 to 200 (the change is left for the student)
FIGS['s2'] = {'svg': change_bars(160, 200, 'Two bars on the same scale. The original value is 160 and the new value is 200. The extra part is marked with a question mark.', show_change=False)}
# --- Step 4: a 25 percent increase, then a 40 percent decrease
FIGS['s4'] = {'svg': chain(['original', '?', '?'], ['1.25', '0.60'], 'A chain of three boxes: the original price times 1.25, and that result times 0.60.')}
# --- Step 7: two acid solutions mixed (not to scale, so the picture does not give away x)
FIGS['s7'] = {'svg': mixture([(64, 0.15, ['x L', '15% acid', '0.15x L of acid']), (48, 0.45, ['8 L', '45% acid', '3.6 L of acid']), (86, 0.25, ['(x + 8) L', '25% acid', '0.25(x + 8) L of acid'])],
                             'Three containers. x liters of a 15 percent acid solution plus 8 liters of a 45 percent acid solution equals x plus 8 liters of a 25 percent acid solution.', note='not drawn to scale')}
# --- Practice 8: museum visitors in four months
FIGS['p8'] = {'svg': bar_chart('Museum visitors by month', ['Jan', 'Feb', 'Mar', 'Apr'], [200, 250, 350, 300], 400, 50, 100, 'Number of visitors', 'Month',
                               'A bar graph of museum visitors. January 200, February 250, March 350, April 300. Gridlines are 50 apart.')}

FIGS_JS = ('var FIGS = {\n' + ',\n'.join('    ' + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') for k, v in FIGS.items()) + '\n};\n'
           "function fig(name) { var f = FIGS[name]; return f ? (f.svg ? f.svg : graphSVG(f)) : ''; }")

# classes for the figures above, on top of the shell's figure styles
FIG_RULES = [
    ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }",
    ".fig .bar { fill: rgba(57,134,78,0.16); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .chg { fill: rgba(221,162,94,0.38); stroke: #BC6C26; stroke-width: 1.4; }",
    ".fig .cut { fill: none; stroke: #BC6C26; stroke-width: 1.4; stroke-dasharray: 4 3; }",
    ".fig .jar { fill: #FFFCF6; stroke: #21442B; stroke-width: 1.6; }",
    ".fig .pure { fill: rgba(188,108,38,0.45); stroke: none; }",
    ".fig .colbar { fill: rgba(57,134,78,0.5); stroke: #21442B; stroke-width: 1.2; }",
    ".fig .gl { stroke: #D8CDB5; stroke-width: 1; }",
    ".fig .ax2 { stroke: #2D2D2D; stroke-width: 1.4; }",
    ".fig .arr { stroke: #21442B; stroke-width: 1.6; fill: none; }",
    ".fig .arrh { fill: #21442B; stroke: none; }",
    ".fig text.lb { font-family: 'Inter', sans-serif; font-size: 12.5px; font-style: normal; fill: #2D2D2D; }",
    ".fig text.lbb { font-family: 'Inter', sans-serif; font-size: 12.5px; font-weight: 700; font-style: normal; fill: #21442B; }",
    ".fig text.lbs { font-family: 'Inter', sans-serif; font-size: 11.5px; font-style: normal; fill: #5A5A5A; }",
    ".fig text.op { font-family: 'Inter', sans-serif; font-size: 22px; font-weight: 700; font-style: normal; fill: #21442B; }",
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
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Percentages</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Percentages</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; PERCENTAGES')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Percentages')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Percent Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Percent rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>a percent is a percent of something, and taking it is one multiplication.</strong> Find the base first: the original value, the whole group or the total mixture. Then multiply by the percent as a decimal, or by the multiplier $1 \pm \dfrac{p}{100}$ when a value changes. To undo a change, divide by that same multiplier.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. You can leave off the percent sign and the dollar sign, and decimals such as 0.7 or .7 are both accepted. Sections A to E use the starred rules, and section F covers the unstarred ones. Once you feel comfortable, try responding without pausing for long.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and two include a table or a graph. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type: a percent of a number, a percent change, a change to apply, or a change to undo. Then find the base, the value the percent is taken of. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. For these questions it works mostly as a calculator, for example to compute $84 \div 0.70$ or $1.20 \times 0.75$. You still need to decide which multiplication or division the question calls for.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These eight questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each one combines rules you already have (a percent of a percent with an unknown, two changes in a row, two changes to undo, a chain of percent comparisons) or uses the unstarred rules (percent sentences with letters, mixtures). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the ones marked <em>extra</em> lean on the unstarred rules. One is tagged <em>exponent blend</em>: it repeats a multiplier, which leads into SAT Math 7, so treat it as stretch practice.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time a percent question shows up. Make it an if-then. (Shape: “When a question gives the value after a percent change, I ______ before I compute anything.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">A percent is a ratio out of 100, so this sheet builds on the one before it: <a href="' + RATIOS_URL + '" ' + A_STYLE + '>SAT Math 5: Ratios, Rates and Proportions &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">Ready for the next topic? Continue the series with <a href="' + EXP_URL + '" ' + A_STYLE + '>SAT Math 7: Exponents and Exponential Models &#8594;</a></p>',
        flags=re.S)

    # --- data arrays
    for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
        html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

    # --- figures: FIGS and fig(); the shell's graphSVG stays for any coordinate figure
    start = html.index('var FIGS = {')
    tail = "function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }"
    end = html.index(tail) + len(tail)
    html = html[:start] + FIGS_JS + html[end:]
    html = replace_once(html, ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }", FIG_CSS)

    # --- Skill Practice items can carry a figure; it sits between the question and the answer row
    html = replace_once(html, """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>';""",
                        """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>' + (it.fig ? fig(it.fig) : '');""")

    # --- results kit: carry each question's figure into the tutor report (practice, challenge and the Skill Practice reps that have one)
    html = replace_n(html, "stem: p.stem, trap: p.trap });", "stem: p.stem, fig: p.fig ? fig(p.fig) : '', trap: p.trap });", 2)
    html = replace_once(html, """'</b></span></div><div class="stem">' + r.i.stem + '</div>""", """'</b></span></div><div class="stem">' + (r.i.fig || '') + r.i.stem + '</div>""")
    html = replace_once(html, ": it.accept[0], q: it.q }); }", ": it.accept[0], q: it.q + (it.fig ? fig(it.fig) : '') }); }")
    html = replace_once(html, "'.nw{white-space:nowrap}table.vtab{", "'" + REPORT_FIG_CSS.replace('\\', '\\\\').replace("'", "\\'") + "' +\n        '.nw{white-space:nowrap}table.vtab{")

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', 'sat-percentages-sheet:rule')
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
