#!/usr/bin/env python3
"""Recomputes the answer key of SAT-Math-6-Percentages.html from build_percentages.py.
Every answer is worked out again here from the givens (percent of, percent change, multipliers,
dividing by a multiplier, the pure-amount equation for a mixture) and compared with the builder's data.
Also checked: each multiple-choice item has exactly one correct choice, every accepted typed form
equals the answer, every purely numeric equation written anywhere in the sheet (rules, examples,
solutions, explanations) is true, and the bar graph is drawn at the heights its question uses.
Needs sympy:  python3 verify_percentages.py"""
import os, re, sys
import sympy as sp
from sympy import Rational as Q

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_percentages as b

N = [0]
FAIL = []
MATH = re.compile(r'\$(?:\\.|[^$\\])+?\$', re.S)


def same(got, want):
    if isinstance(got, (list, tuple)) or isinstance(want, (list, tuple)):
        return len(got) == len(want) and all(same(g, w) for g, w in zip(got, want))
    try:
        return sp.simplify(sp.sympify(got) - sp.sympify(want)) == 0
    except Exception:
        return False


def check(name, got, want):
    N[0] += 1
    if not same(got, want):
        FAIL.append('%s: got %s, want %s' % (name, got, want))


def truth(name, cond):
    N[0] += 1
    if not cond:
        FAIL.append(name)


def D(s):
    """A decimal or whole number written as text, as an exact fraction."""
    return Q(str(s))


def tex(seg):
    """One math segment ('$\\$49$', '$24\\%$', '$\\dfrac{12}{5}$', '$\\dfrac{V(c - d)}{d}$') as a sympy value.
    A percent sign and a dollar sign are dropped: the caller knows which unit the number is in."""
    s = seg.strip().strip('$')
    s = s.replace('\\$', '').replace('\\%', '').replace('{,}', '').replace('\\left', '').replace('\\right', '')
    s = re.sub(r'(\d+)\\tfrac\{(\d+)\}\{(\d+)\}', r'(\1+(\2)/(\3))', s)
    for _ in range(3):
        s = re.sub(r'\\[dt]frac\{((?:[^{}]|\{[^{}]*\})*)\}\{((?:[^{}]|\{[^{}]*\})*)\}', r'((\1)/(\2))', s)
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace('\\div', '/').replace('^', '**')
    s = re.sub(r'(?<=[0-9.a-zA-Z)])\s*(?=\()', '*', s)                 # 0.40(12), V(c - d)
    s = re.sub(r'(?<=[0-9.])(?=[a-zA-Z])', '*', s)                      # 0.8d
    s = re.sub(r'(?<=[a-zA-Z])(?=[a-zA-Z])', '*', s)                    # Vd
    return sp.sympify(s, rational=True)


def val(text):
    """The value of the first math segment in a choice or an accepted answer."""
    m = MATH.search(text)
    return tex(m.group(0) if m else text.replace('$', '').replace('%', ''))


def typed(name, item, want):
    """A typed answer: the first accepted form and every other accepted form equal the recomputed value."""
    check(name, val(item['accept'][0]), want)
    for a in item['accept']:
        truth('%s: accepted form %r' % (name, a), same(val(a), want))


def choice(name, opts, correct, want):
    """A multiple-choice item: the keyed choice equals the recomputed value and no other choice does."""
    vals = [val(o) for o in opts]
    check(name, vals[correct], want)
    truth(name + ': exactly one correct choice', sum(1 for v in vals if same(v, want)) == 1)
    truth(name + ': four choices, all different', len(opts) == 4 and len(set(opts)) == 4)


# ---------------------------------------------------------------- the percent ideas, from first principles
def pct_of(p, n):                       # p percent of n
    return D(p) / 100 * D(n)

def pct_change(orig, new):              # percent change from orig to new (positive is an increase)
    return (D(new) - D(orig)) / D(orig) * 100

def up(p):                              # the multiplier for an increase of p percent
    return 1 + D(p) / 100

def down(p):                            # the multiplier for a decrease of p percent
    return 1 - D(p) / 100

x = sp.Symbol('x')

def solve1(eq):
    sol = sp.solve(eq, x)
    assert len(sol) == 1, sol
    return sol[0]

def mix_two(p1, p2, amt2, target):      # liters of a p1% solution added to amt2 liters of a p2% solution to reach target%
    return solve1(sp.Eq(D(p1) / 100 * x + D(p2) / 100 * amt2, D(target) / 100 * (x + amt2)))

def add_water(amt, p, target):          # liters of water added to amt liters of a p% solution to reach target%
    return solve1(sp.Eq(D(p) / 100 * amt, D(target) / 100 * (amt + x)))

def add_pure(amt, p, target):           # amount of pure ingredient added to amt of a p% solution to reach target%
    return solve1(sp.Eq(D(p) / 100 * amt + x, D(target) / 100 * (amt + x)))


# ---------------------------------------------------------------- worked examples (tab 2)
S = b.STEPS
truth('7 steps, 5 starred first', len(S) == 7 and [s['ess'] for s in S] == [True] * 5 + [False] * 2 and b.LAST_STARRED_STEP_INDEX == 4)
k1 = solve1(sp.Eq(D('0.60') * D('0.40'), D('0.30') * x / 100))
check('step 1: k', k1, 80); truth('step 1 states k = 80', '$k = 80$' in S[0]['sol'])
typed('step 1 check', S[0]['micro'], D(27) / D('0.18'))
check('step 2: percent increase', pct_change(160, 200), 25); truth('step 2 states 25%', r'increased by $25\%$' in S[1]['sol'])
check('step 2 trap: 40 of 200', D(40) / 200 * 100, 20)
typed('step 2 check', S[1]['micro'], -pct_change(80, 68))
check('step 3: new price', 75 * up(12), 84); truth('step 3 states 84', r'$\$84$' in S[2]['sol'] and '$1.12$' in S[2]['sol'])
typed('step 3 check', S[2]['micro'], (1 - D('0.72')) * 100)
check('step 4: net multiplier', up(25) * down(40), D('0.75')); truth('step 4 states a 25% decrease', r'a $25\%$ decrease' in S[3]['sol'])
check('step 4 trap: 40% of 125', pct_of(40, 125), 50)
typed('step 4 check', S[3]['micro'], up(40) * down(50) * 100)
check('step 5: original price', D(68) / down(20), 85); truth('step 5 states 85', r'$\$85$' in S[4]['sol'])
check('step 5 trap', 68 + pct_of(20, 68), D('81.60'))
typed('step 5 check', S[4]['micro'], D(143) / up(10))
check('step 6: q as a percent of p', 1 / (D('0.20') * 4) * 100, 125); truth('step 6 states 125%', r'$125\%$ of $p$' in S[5]['sol'])
typed('step 6 check', S[5]['micro'], 1 / D('0.25') * 100)
check('step 7: liters', mix_two(15, 45, 8, 25), 16); truth('step 7 states x = 16', '$x = 16$' in S[6]['sol'])
typed('step 7 check', S[6]['micro'], pct_of(30, 50))

# ---------------------------------------------------------------- skill practice (tab 3)
F = {s['sec'][0]: s['items'] for s in b.FLUENCY}
truth('skill practice: 6 sections, 24 items', len(b.FLUENCY) == 6 and sum(len(s['items']) for s in b.FLUENCY) == 24)
typed('A1', F['A'][0], D(7) / 100)
typed('A2', F['A'][1], up(30))
typed('A3', F['A'][2], down(30))
truth('A4: multiplying by 0.45 is a 55% decrease', F['A'][3]['correct'] == 2 and 'decreasing' in F['A'][3]['opts'][2] and same(val(F['A'][3]['opts'][2]), (1 - D('0.45')) * 100))
truth('A4: one correct choice', sum(1 for o in F['A'][3]['opts'] if 'decreasing' in o and same(val(o), 55)) == 1)
typed('A5', F['A'][4], up(140))
typed('B1', F['B'][0], pct_of(20, 85))
typed('B2', F['B'][1], D(9) / 36 * 100)
typed('B3', F['B'][2], D(32) / D('0.40'))
typed('B4', F['B'][3], pct_of(125, 48))
typed('C1', F['C'][0], pct_change(50, 62))
typed('C2', F['C'][1], -pct_change(120, 90))
typed('C3', F['C'][2], pct_change(40, 100))
choice('C4', F['C'][3]['opts'], F['C'][3]['correct'], pct_change(1, 3))
typed('D1', F['D'][0], 40 * up(15))
typed('D2', F['D'][1], up(10) * down(10) * 100)
choice('D3', F['D'][2]['opts'], F['D'][2]['correct'], (up(20) * up(50) - 1) * 100)
typed('D4', F['D'][3], (1 - down(50) * down(20)) * 100)
typed('E1', F['E'][0], D(60) / up(25))
typed('E2', F['E'][1], D(53) / up(6))
d = sp.Symbol('d')
choice('E3', F['E'][2]['opts'], F['E'][2]['correct'], d / down(20))
typed('F1', F['F'][0], 1 / D('1.25') * 100)
typed('F2', F['F'][1], D('0.75') * 2)
typed('F3', F['F'][2], pct_of(15, 60))
typed('F4', F['F'][3], pct_of(40, 15) / (15 + 5) * 100)

# ---------------------------------------------------------------- SAT-style practice (tab 4)
G = b.GAUNTLET
truth('practice: 10 items, the last one is the unstarred one', len(G) == 10 and [g['ess'] for g in G] == [True] * 9 + [False])
truth('practice: both formats', sum(g['type'] == 'mc' for g in G) == 6 and sum(g['type'] == 'ne' for g in G) == 4)
choice('P1', G[0]['options'], G[0]['correct'], pct_of(28, 450))
books = [84, 36, 48, 32]
truth('P2: the table holds the counts used', all('$%d$' % n in G[1]['stem'] for n in books))
choice('P2', G[1]['options'], G[1]['correct'], D(48) / sum(books) * 100)
check('P2 distractors: history and fiction', [D(32) / sum(books) * 100, D(84) / sum(books) * 100], [16, 42])
typed('P3', G[2], pct_change(20, 27))
choice('P4', G[3]['options'], G[3]['correct'], (D('1.24') - 1) * 100)
typed('P5', G[4], D(272) / down(15)); check('P5 check line', pct_of(15, 320), 48); check('P5 trap', 272 + pct_of(15, 272), D('312.80'))
choice('P6', G[5]['options'], G[5]['correct'], (1 - up(10) * down(30)) * 100)
w = D(70) / D('0.40')
choice('P7', G[6]['options'], G[6]['correct'], pct_of(30, 2 * w)); check('P7: w', w, 175)
choice('P9', G[8]['options'], G[8]['correct'], D(96) / (up(25) * down(20)))
check('P9 distractor B', round(float(D(96) / D('1.05')), 2), 91.43)
typed('P10', G[9], add_water(18, 25, 15))
# the bar graph (practice 8): read the heights back out of the SVG and recompute the answer from them
svg = b.FIGS['p8']['svg']
bars = re.findall(r'<rect class="colbar" x="[\d.]+" y="([\d.]+)" width="[\d.]+" height="([\d.]+)"/>', svg)
grid = sorted(set(float(y) for y in re.findall(r'<line class="gl" x1="[\d.]+" y1="([\d.]+)"', svg)), reverse=True)
unit = (grid[0] - grid[-1]) / 400.0                                        # pixels per visitor (the gridlines run from 0 to 400)
heights = [round(float(h) / unit) for _, h in bars]
check('P8: bar heights as drawn', heights, [200, 250, 350, 300])
truth('P8: nine gridlines, 50 apart', len(grid) == 9)
truth('P8: bars sit on the axis', all(abs(float(y) + float(h) - grid[0]) < 0.11 for y, h in bars))
typed('P8', G[7], pct_change(heights[1], heights[2]))
truth('P8 solution reads February 250 and March 350', '$= 250$' in G[7]['sol'] and '$= 350$' in G[7]['sol'] and G[7]['fig'] == 'p8')

# ---------------------------------------------------------------- challenge (tab 5)
C = b.CHALLENGE
truth('challenge: 8 items', len(C) == 8 and [c['ess'] for c in C] == [True, True, False, True, True, False, False, True])
typed('C1', C[0], solve1(sp.Eq(D('0.35') * D('0.60'), D('0.14') * x / 100)))
e = C[0]['extras']
typed('C1 extra 1', e[0], D('0.20') * D('0.45') * 100)
typed('C1 extra 2', e[1], solve1(sp.Eq(D('0.50') * x / 100 * 80, 10)))
typed('C1 extra 3', e[2], solve1(sp.Eq(D('0.80') * D('0.25'), D('0.40') * x / 100)))
choice('C2', C[1]['options'], C[1]['correct'], (up(8) * down(4) - 1) * 100)
a_, b_ = sp.symbols('a b')
ratio = sp.solve(sp.Eq(5 * a_ + 2 * b_, D('1.40') * 10 * b_), a_)[0] / b_
choice('C3', C[2]['options'], C[2]['correct'], ratio)
e = C[2]['extras']
typed('C3 extra 1', e[0], 1 / (D('1.25') * 4) * 100)
u_, v_ = sp.symbols('u v')
typed('C3 extra 2', e[1], sp.solve(sp.Eq(2 * u_ + v_, D('1.20') * 5 * v_), u_)[0] / v_)
t = D(24) / D('0.15')
typed('C3 extra 3', e[2], pct_of(45, 2 * t)); check('C3 extra 3: t', t, 160)
typed('C4', C[3], D(144) / (up(60) * down(25))); check('C4 check line', [120 * up(60), 192 * down(25)], [192, 144])
choice('C5', C[4]['options'], C[4]['correct'], up(60) * down(50) * 100)
V, c_, d_ = sp.symbols('V c d')
water = sp.solve(sp.Eq(c_ / 100 * V, d_ / 100 * (V + x)), x)[0]
choice('C6', C[5]['options'], C[5]['correct'], water)
check('C6 numeric check', water.subs({V: 30, c_: 20, d_: 12}), add_water(30, 20, 12))
e = C[5]['extras']
typed('C6 extra 1', e[0], add_pure(12, 30, 44))
typed('C6 extra 2', e[1], add_water(24, 50, 30))
typed('C6 extra 3', e[2], mix_two(60, 20, 10, 44))
typed('C7', C[6], solve1(sp.Eq(D('0.25') * (40 - x) + x, D('0.40') * 40)))
typed('C8', C[7], down(20) ** 3 * 100)

# ---------------------------------------------------------------- exit ticket (tab 6)
E = b.EXIT
truth('exit: 3 items', len(E) == 3)
choice('X1', E[0]['opts'], E[0]['correct'], 70 * down(30))
choice('X2', E[1]['opts'], E[1]['correct'], pct_change(150, 174)); check('X2 distractor', round(float(D(24) / 174 * 100), 1), 13.8)
choice('X3', E[2]['opts'], E[2]['correct'], D(90) / up(20)); check('X3 distractor', 90 * down(20), 72)

# ---------------------------------------------------------------- rules tab: the examples and the numbers quoted in the rules
check('R1 A', pct_of(35, 80), 28); check('R1 B', D(18) / 72 * 100, 25); check('R1 C', D(45) / D('0.15'), 300); check('R1 D', pct_of(30, pct_of(50, 240)), 36)
check('R2 A', pct_change(40, 52), 30); check('R2 B', pct_change(250, 210), -16); check('R2 C', pct_change(50, 150), 200); check('R2 note', D(150) / 50 * 100, 300)
check('R3 A', 60 * up(35), 81); check('R3 B', 1500 * down(12), 1320); check('R3 C', 45 * up(8), D('48.60')); check('R3 D', (1 - D('0.7')) * 100, 30)
check('R3 table', [up(8), up(35), up(120), down(8), down(35), down(60)], [D('1.08'), D('1.35'), D('2.20'), D('0.92'), D('0.65'), D('0.40')])
check('R3 reading a multiplier', [(D('1.3') - 1) * 100, (1 - D('0.82')) * 100, (D('2.1') - 1) * 100], [30, 18, 110])
check('R4 A', (up(20) * down(25) - 1) * 100, -10); check('R4 B', (up(10) * up(10) - 1) * 100, 21); check('R4 C', 80 * down(25) * up(5), 63)
check('R4 same percent', (up(20) * down(20) - 1) * 100, -4)
check('R5 A', D(1500) / up(25), 1200); check('R5 B', D(84) / down(30), 120); check('R5 C', D('64.80') / up(8), 60); check('R5 note', 1500 * down(25), 1125)
check('R6 flip', 1 / D('0.2') * 100, 500); check('R6 A', 1 / (D('0.4') * 5) * 100, 50)
check('R6 B', sp.solve(sp.Eq(3 * a_ + 2 * b_, D('1.75') * 8 * b_), a_)[0] / b_, 4); check('R6 C', pct_of(20, 3 * D(45) / D('0.30')), 90)
check('R7 A', add_water(30, 20, 12), 20); check('R7 B', mix_two(10, 40, 12, 20), 24); check('R7 C', add_pure(20, 40, 50), 4)
check('mistake 1', round(float(D(12) / 52 * 100)), 23); check('mistake 7', (pct_of(10, 1) + pct_of(40, 1)) / 2 * 100, 25)
# the figures on the rules tab repeat numbers from the examples
truth('figure r_change shows 40, 52 and 30%', all(s in b.FIGS['r_change']['svg'] for s in ('Original value: 40', 'New value: 52', '+12', '0.30, a 30% increase')))
truth('figure r_chain shows 100, 120, 90', all('>%s<' % s in b.FIGS['r_chain']['svg'] for s in ('100', '120', '90')) and '0.90: a 10% decrease' in b.FIGS['r_chain']['svg'])
check('figure r_mult', [up(35), down(20)], [D('1.35'), D('0.80')])
truth('figure r_mix is to scale', all(s in b.FIGS['r_mix']['svg'] for s in ('height="54.0"', 'height="36.0"', 'height="90.0"')))
truth('no dollar sign inside a figure', all('$' not in f['svg'] for f in b.FIGS.values()))


# a choice that ends in math plus punctuation would pick up a no-wrap span, which the tutor report prints as text
all_opts = [o for g in G + C for o in g.get('options', [])] + [o for e_ in E for o in e_['opts']] + [o for sec in b.FLUENCY for it in sec['items'] for o in it.get('opts', [])]
truth('no choice has punctuation right after math', all('class="nw"' not in b.nw(o) for o in all_opts))

# ---------------------------------------------------------------- every purely numeric equation in the sheet
def numeric_equations(text):
    """Yield (segment, ok) for each math segment that is a chain of equalities between plain numbers."""
    for m in MATH.finditer(text):
        seg = m.group(0)
        body = seg.strip('$')
        if '=' not in body or '\\text' in body or '\\to' in body or '\\pm' in body:
            continue
        plain = re.sub(r'\\(dfrac|tfrac|times|cdot|div|left|right|%|\$)', '', body)
        if re.search(r'[A-Za-z]', plain):
            continue                                                       # has a variable: checked by hand above
        sides = body.split('=')
        if any(not side.strip() for side in sides):
            continue                                                       # a label such as "original $= 20$" or "$p =$"
        try:
            vals = [tex('$' + (re.sub(r'([\d.]+)\\%', r'((\1)/100)', s)) + '$') for s in sides]
        except Exception as err:
            yield seg, 'could not read (%s)' % err
            continue
        yield seg, all(same(vals[i], vals[i + 1]) for i in range(len(vals) - 1))


def walk(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for v in o:
            for s in walk(v):
                yield s
    elif isinstance(o, dict):
        for v in o.values():
            for s in walk(v):
                yield s


n_eq = 0
for text in [b.RULES] + list(walk([b.STEPS, b.FLUENCY, b.GAUNTLET, b.CHALLENGE, b.EXIT])):
    for seg, ok in numeric_equations(text):
        n_eq += 1
        truth('numeric equation ' + seg + ('' if ok in (True, False) else ' ' + str(ok)), ok is True)
truth('the scan found the numeric equations (%d)' % n_eq, n_eq >= 85)

if FAIL:
    print('FAILED %d of %d checks' % (len(FAIL), N[0]))
    for f in FAIL:
        print('  -', f)
    sys.exit(1)
print('all %d checks passed (%d numeric equations scanned)' % (N[0], n_eq))
