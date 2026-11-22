#!/usr/bin/env python3
"""Recomputes the answer key of SAT-Math-4B-Special-Right-Triangles.html from build_special_right_triangles.py.
Every answer is worked out again here from the Pythagorean theorem, the law of cosines or an area formula,
then compared with the builder's data. Also checked: each multiple-choice item has one correct choice, every
accepted typed form matches, the worked numbers quoted in solutions and rules, every angle mark in a figure
against the angle actually drawn, and the Skill Practice figures against their answers (they are drawn to scale).
Needs sympy:  python3 verify_special_right_triangles.py"""
import math, os, re, sys
import sympy as sp
from sympy import sqrt, Rational as Q, pi, sin, cos, tan

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_special_right_triangles as b

N = [0]
FAIL = []


def same(got, want):
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


def tex(s):
    """'$12\\sqrt{2}$' or '$8 - 4\\sqrt{3}$' or '$\\dfrac{\\sqrt{3}}{2}$' as a sympy value."""
    s = s.strip().strip('$')
    for _ in range(3):
        s = re.sub(r'\\dfrac\{((?:[^{}]|\{[^{}]*\})*)\}\{((?:[^{}]|\{[^{}]*\})*)\}', r'((\1)/(\2))', s)
    s = s.replace('\\pi', 'pi')
    s = re.sub(r'\\sqrt\{(\d+)\}', r'sqrt(\1)', s)
    s = re.sub(r'(\d)\s*(sqrt|pi)', r'\1*\2', s)
    return sp.sympify(s)


# ---------------------------------------------------------------- geometry, from first principles
x, s_ = sp.symbols('x s', positive=True)


def t45(leg=None, hyp=None):
    """Isosceles right triangle: leg^2 + leg^2 = hyp^2."""
    if leg is None:
        leg = sp.solve(sp.Eq(2 * x ** 2, hyp ** 2), x)[0]
    leg = sp.sympify(leg)
    hyp = sqrt(2 * leg ** 2)
    return dict(leg=sp.simplify(leg), hyp=sp.simplify(hyp), area=sp.simplify(leg ** 2 / 2))


def t30(short=None, long=None, hyp=None):
    """Right triangle with a 30 degree angle: short = hyp sin 30, long = hyp cos 30."""
    if hyp is None:
        hyp = short / sin(pi / 6) if short is not None else long / cos(pi / 6)
    hyp = sp.sympify(hyp)
    short, long = hyp * sin(pi / 6), hyp * cos(pi / 6)
    truth('30-60-90 satisfies the Pythagorean theorem', same(short ** 2 + long ** 2, hyp ** 2))
    return dict(short=sp.simplify(short), long=sp.simplify(long), hyp=sp.simplify(hyp), area=sp.simplify(short * long / 2))


def eq(side=None, height=None, area=None, perimeter=None):
    """Equilateral triangle: the height comes from the Pythagorean theorem on half of the triangle."""
    if perimeter is not None: side = Q(perimeter) / 3
    if height is not None: side = sp.solve(sp.Eq(sqrt(s_ ** 2 - (s_ / 2) ** 2), height), s_)[0]
    if area is not None: side = sp.solve(sp.Eq(s_ * sqrt(s_ ** 2 - (s_ / 2) ** 2) / 2, area), s_)[0]
    side = sp.sympify(side)
    h = sqrt(side ** 2 - (side / 2) ** 2)
    return dict(side=sp.simplify(side), height=sp.simplify(h), area=sp.simplify(side * h / 2), perimeter=sp.simplify(3 * side))


def sq(side=None, diag=None, area=None, perimeter=None):
    if perimeter is not None: side = Q(perimeter) / 4
    if area is not None: side = sqrt(area)
    if diag is not None: side = sp.solve(sp.Eq(2 * x ** 2, diag ** 2), x)[0]
    side = sp.sympify(side)
    return dict(side=sp.simplify(side), diag=sp.simplify(sqrt(2 * side ** 2)), area=sp.simplify(side ** 2), perimeter=4 * side)


def third_side(a, c, deg):
    """Law of cosines: the side across from an angle of deg degrees between sides a and c."""
    return sp.simplify(sqrt(a ** 2 + c ** 2 - 2 * a * c * cos(deg * pi / 180)))


def tri_area(a, c, deg):
    return sp.simplify(a * c * sin(deg * pi / 180) / 2)


# ---------------------------------------------------------------- the key, recomputed
STEP_MICRO = [
    t45(hyp=17 * sqrt(2))['leg'],                                   # 17
    t30(hyp=46)['long'] / sqrt(3),                                  # 23
    t45(hyp=22)['leg'] / sqrt(2),                                   # 11
    sq(diag=12 * sqrt(2))['side'] / 2,                              # 6
    eq(area=100 * sqrt(3))['side'],                                 # 20
    third_side(10, 10, 120) / sqrt(3),                              # 10
    sin(pi / 6),                                                    # 1/2
]
STEP_WORKED = [                                                     # numbers each solution states
    [t45(leg=9)['leg'], t45(leg=9)['hyp']],
    [t30(short=15)['hyp'], t30(short=15)['long']],
    [t30(long=21)['short'], t30(long=21)['hyp']],
    [sq(diag=10)['side'], sq(diag=10)['area']],
    [eq(side=8)['height'], eq(side=8)['area']],
    [6 * eq(side=4)['area'], 2 * eq(side=4)['height']],
    [sin(pi / 3), cos(pi / 3), tan(pi / 3)],
]
STEP_TEXT = [
    [r'BC = AC = 9', r'AB = 9\sqrt{2}'], [r'2x = 30', r'15\sqrt{3}'], [r'7\sqrt{3}', r'14\sqrt{3}'], [r'5\sqrt{2}', r'= 50'],
    [r'4\sqrt{3}', r'16\sqrt{3}'], [r'24\sqrt{3}', r'the distance is $4\sqrt{3}$'], [r'\dfrac{\sqrt{3}}{2}', r'\dfrac{1}{2}', r'= \sqrt{3}'],
]
STEP_SHOWN = [[9, 9 * sqrt(2)], [30, 15 * sqrt(3)], [7 * sqrt(3), 14 * sqrt(3)], [5 * sqrt(2), 50], [4 * sqrt(3), 16 * sqrt(3)],
              [24 * sqrt(3), 4 * sqrt(3)], [sqrt(3) / 2, Q(1, 2), sqrt(3)]]

FLU = [
    # A: the patterns (the correct choice, as text)
    [r"$x : x : x\sqrt{2}$", r"$x : x\sqrt{3} : 2x$", "the short leg, $x$", r"$x\sqrt{3}$", "$2$", r"$\sqrt{2}$",
     r"$45$-$45$-$90$ triangles, then $30$-$60$-$90$ triangles"],
    # B
    [t45(leg=12)['hyp'], t45(hyp=19 * sqrt(2))['leg'], t45(hyp=8)['leg'], t45(leg=3 * sqrt(2))['hyp'], t45(hyp=26)['leg'] / sqrt(2), t45(hyp=10)['area']],
    # C
    [t30(short=16)['hyp'], t30(short=10)['long'], t30(hyp=28)['short'], t30(hyp=12)['long'], t30(long=4 * sqrt(3))['short'],
     t30(long=17 * sqrt(3))['hyp'], t30(long=6)['short'], t30(long=27)['hyp'] / sqrt(3)],
    # D (also checked against the figures below)
    [t30(hyp=24)['short'], t30(short=9)['hyp'], t30(long=20 * sqrt(3))['hyp'], t45(hyp=5 * sqrt(2))['leg'], t30(long=33)['short'], t30(short=2 * sqrt(3))['long']],
    # E
    [sq(perimeter=44)['diag'] / sqrt(2), sq(diag=6)['area'], eq(side=18)['height'], eq(side=14)['area'] / sqrt(3), sq(diag=16)['area'],
     sq(diag=30 * sqrt(2))['side'] / 2, eq(height=10 * sqrt(3))['perimeter'], eq(perimeter=12)['area'] / sqrt(3)],
    # F
    [6 * eq(side=10)['area'] / sqrt(3), third_side(12, 12, 60), third_side(6, 6, 120), tan(pi / 3)],
]
D_GIVEN = {'d1': ('24', 24), 'd2': ('9', 9), 'd3': ('20√3', 20 * sqrt(3)), 'd4': ('5√2', 5 * sqrt(2)), 'd5': ('33', 33), 'd6': ('2√3', 2 * sqrt(3))}

rect = t30(hyp=20)
GAU = [
    t45(leg=25)['hyp'], t30(hyp=38)['short'], t30(long=5 * sqrt(3))['hyp'], sq(area=50)['diag'], eq(area=121 * sqrt(3))['perimeter'],
    sq(diag=12)['area'], pi * (sq(diag=18 * sqrt(2))['side'] / 2) ** 2 / pi, rect['short'] * rect['long'], 6 * eq(side=6)['area'] / sqrt(3),
    t30(short=t45(hyp=8 * sqrt(2))['leg'])['hyp'],
]
CHA = [
    sq(diag=20)['area'], eq(height=30)['area'] / sqrt(3), 2 * tri_area(6, 6, 60) / sqrt(3), 8 - eq(side=8)['height'], third_side(10, 10, 120),
    24 * cos(pi / 3),
]
truth('challenge 5: an equilateral triangle in a circle has central angles of 120 degrees', same(third_side(10, 10, 120), 2 * 10 * sin(pi / 3)))
truth('challenge 6: the angle whose sine is root 3 over 2 is 60 degrees', same(sp.asin(sqrt(3) / 2), pi / 3))
CHA_X = {0: [sq(diag=sq(area=64)['side'])['area'], sq(diag=2 * sqrt(81))['area'], sq(diag=2 * 5 * sqrt(2))['side'] / 2],
         1: [eq(height=6)['side'] / sqrt(3), eq(area=9 * sqrt(3))['height'] / sqrt(3), eq(perimeter=54)['area'] / sqrt(3)]}
EXI = [t45(leg=13)['hyp'], t30(hyp=60)['long'], eq(side=2)['area']]


def item(name, it, want):
    """One graded item against the recomputed value: multiple choice or typed."""
    if it.get('mc') or it.get('type') == 'mc' or ('opts' in it and 'accept' not in it):
        opts = it.get('opts') or it.get('options')
        if isinstance(want, str):
            truth(name + ' (choice text)', opts[it['correct']] == want)
            truth(name + ' (one choice only)', opts.count(want) == 1)
        else:
            vals = [tex(o) for o in opts]
            check(name, vals[it['correct']], want)
            truth(name + ' (one correct choice)', sum(1 for v in vals if same(v, want)) == 1)
            truth(name + ' (four different choices)', len({sp.nsimplify(sp.N(v, 12)) for v in vals}) == len(vals))
    else:
        for a in it['accept']:
            check(name + ' accepts ' + a, sp.nsimplify(a.replace('°', '')), want)


for i, st in enumerate(b.STEPS):
    item('step %d quick check' % (i + 1), st['micro'], STEP_MICRO[i])
    for got, shown in zip(STEP_WORKED[i], STEP_SHOWN[i]):
        check('step %d worked value' % (i + 1), got, shown)
    for t in STEP_TEXT[i]:
        truth('step %d solution states %s' % (i + 1, t), t in st['sol'])
truth('7 steps', len(b.STEPS) == 7 and len(STEP_MICRO) == 7)
truth('last starred step', all(st['ess'] for st in b.STEPS[:b.LAST_STARRED_STEP_INDEX + 1]) and not any(st['ess'] for st in b.STEPS[b.LAST_STARRED_STEP_INDEX + 1:]))

n = 0
for si, sec in enumerate(b.FLUENCY):
    truth('skill practice section %s has %d items' % (sec['sec'][:1], len(FLU[si])), len(sec['items']) == len(FLU[si]))
    for ii, it in enumerate(sec['items']):
        n += 1
        item('skill practice %d' % n, it, FLU[si][ii])
truth('39 skill practice items', n == 39)
for i, it in enumerate(b.GAUNTLET):
    item('practice %d' % (i + 1), it, GAU[i])
truth('10 practice items', len(b.GAUNTLET) == 10 == len(GAU))
for i, it in enumerate(b.CHALLENGE):
    item('challenge %d' % (i + 1), it, CHA[i])
    for j, xx in enumerate(it.get('extras', [])):
        item('challenge %d%s' % (i + 1, 'abc'[j]), xx, CHA_X[i][j])
truth('6 challenge items', len(b.CHALLENGE) == 6 == len(CHA))
for i, it in enumerate(b.EXIT):
    item('exit %d' % (i + 1), it, EXI[i])

# ---------------------------------------------------------------- figures
def dist(p, q): return math.hypot(p[0] - q[0], p[1] - q[1])


def angle(at, p, q):
    a1 = math.atan2(p[1] - at[1], p[0] - at[0]); a2 = math.atan2(q[1] - at[1], q[0] - at[0])
    d = abs(a1 - a2) % (2 * math.pi)
    return math.degrees(min(d, 2 * math.pi - d))


for k, f in b.FIGS.items():
    truth('figure %s has alt text' % k, bool(f.get('alt')))
    for a in f.get('arcs', []):
        m = re.fullmatch(r'(\d+)°', a.get('t', ''))
        if m:
            truth('figure %s: the angle marked %s is drawn as %.2f degrees' % (k, a['t'], angle(a['at'], a['a'], a['b'])),
                  abs(angle(a['at'], a['a'], a['b']) - int(m.group(1))) < 0.2)
used = set()
for name in ('STEPS', 'GAUNTLET', 'CHALLENGE'):
    used |= {it['fig'] for it in getattr(b, name) if it.get('fig')}
used |= {it['fig'] for sec in b.FLUENCY for it in sec['items'] if it.get('fig')}
used |= set(re.findall(r'data-fig="([^"]+)"', b.RULES))
truth('every figure is used and every figure reference exists: %s' % sorted(used ^ set(b.FIGS)), used == set(b.FIGS))

# Skill Practice D: the figures are to scale, so the side marked y, measured against the labeled side, must give the answer
for (key, (label, value)), it, want in zip(D_GIVEN.items(), b.FLUENCY[3]['items'], FLU[3]):
    f = b.FIGS[key]
    truth('skill practice figure %s is the one the item uses' % key, it['fig'] == key)
    sides = {s['t']: dist(s['a'], s['b']) for s in f['sides']}
    truth('figure %s labels %s and y' % (key, label), set(sides) == {label, 'y'})
    truth('figure %s: y measures %.4f, key %.4f' % (key, float(value) * sides['y'] / sides[label], float(want)),
          abs(float(value) * sides['y'] / sides[label] - float(want)) < 0.01)
# the other figures drawn to scale: labeled lengths in proportion
p8 = b.FIGS['p8']; truth('practice 8 rectangle is 10 root 3 by 10', abs(dist(p8['segs'][0]['a'], p8['segs'][0]['b']) / dist(p8['segs'][1]['a'], p8['segs'][1]['b']) - math.sqrt(3)) < 0.01)
p10 = b.FIGS['p10']; truth('practice 10: BC is twice BD', abs(dist(p10['segs'][1]['a'], p10['segs'][1]['b']) / dist(p10['segs'][3]['a'], p10['segs'][3]['b']) - 2) < 0.01)
c4 = b.FIGS['c4']; truth('challenge 4: triangle ABE is equilateral', abs(dist(c4['segs'][4]['a'], c4['segs'][4]['b']) - dist(c4['segs'][0]['a'], c4['segs'][0]['b'])) < 0.01)

# ---------------------------------------------------------------- numbers quoted on the rules tab and in explanations
IDENT = [
    (20 / sqrt(2), 10 * sqrt(2)), (24 / sqrt(3), 8 * sqrt(3)), (2 * 8 * sqrt(3), 16 * sqrt(3)), (30 / sqrt(2), 15 * sqrt(2)), (5 / sqrt(3), 5 * sqrt(3) / 3),
    ((5 * sqrt(2)) ** 2, 50), ((4 * sqrt(3)) ** 2, 48), (t45(hyp=6)['leg'], 3 * sqrt(2)), (t45(hyp=6)['area'], 9),
    (t30(short=3)['long'], 3 * sqrt(3)), (t30(short=3)['hyp'], 6), (t30(hyp=50)['short'], 25), (t30(hyp=50)['long'], 25 * sqrt(3)),
    (t30(short=13)['long'], 13 * sqrt(3)), (t30(short=13)['hyp'], 26), (t45(leg=8)['hyp'], 8 * sqrt(2)), (t45(hyp=9 * sqrt(2))['leg'], 9),
    (sq(side=15)['diag'], 15 * sqrt(2)), (sq(diag=22)['area'], 242), (sq(diag=22)['side'], 11 * sqrt(2)), (sq(diag=6)['side'], 3 * sqrt(2)), (sq(diag=6)['area'], 18),
    (sq(diag=8 * sqrt(2))['side'], 8), (eq(side=6)['height'], 3 * sqrt(3)), (eq(side=6)['area'], 9 * sqrt(3)), (eq(area=64 * sqrt(3))['side'], 16),
    (eq(height=9 * sqrt(3))['side'], 18), (eq(height=6)['side'], 4 * sqrt(3)), (eq(height=6)['area'], 12 * sqrt(3)), (6 * eq(side=2)['area'], 6 * sqrt(3)),
    (third_side(8, 8, 120), 8 * sqrt(3)), (tri_area(8, 8, 120), 16 * sqrt(3)), (8 * cos(pi / 3), 4), (third_side(9, 9, 60), 9), (third_side(9, 9, 90), 9 * sqrt(2)),
    (sin(pi / 6), Q(1, 2)), (cos(pi / 6), sqrt(3) / 2), (tan(pi / 6), sqrt(3) / 3), (sin(pi / 4), sqrt(2) / 2), (cos(pi / 4), sqrt(2) / 2), (tan(pi / 4), 1),
    (sin(pi / 3), sqrt(3) / 2), (cos(pi / 3), Q(1, 2)), (tan(pi / 3), sqrt(3)), (10 * sin(pi / 6), 5), (eq(side=30)['height'], 15 * sqrt(3)), (eq(side=30)['area'], 225 * sqrt(3)),
    (eq(side=14)['height'], 7 * sqrt(3)), (eq(side=10)['area'], 25 * sqrt(3)), (eq(side=18)['area'], 81 * sqrt(3)), (eq(side=6)['height'], 3 * sqrt(3)),
    (t30(long=27)['short'], 9 * sqrt(3)), (t30(long=33)['short'], 11 * sqrt(3)), (t30(hyp=10)['long'], 5 * sqrt(3)), (t30(hyp=6)['long'], 3 * sqrt(3)),
    (eq(height=30)['side'], 20 * sqrt(3)), (30 / sqrt(3), 10 * sqrt(3)), (24 * sqrt(3) / 2, 12 * sqrt(3)), (24 ** 2 - (12 * sqrt(3)) ** 2, 144),
    (t30(short=8)['long'], 8 * sqrt(3)), (sq(side=10)['diag'], 10 * sqrt(2)), (eq(side=4)['area'], 4 * sqrt(3)), (eq(side=4)['height'], 2 * sqrt(3)),
]
for got, want in IDENT:
    check('quoted value', got, want)
APPROX = [(sqrt(2), '1.41'), (sqrt(3), '1.73'), (9 * sqrt(2), '12.7'), (7 * sqrt(3), '12.1'), (5 * sqrt(2), '7.1'), (5 * sqrt(2), '7.07'), (4 * sqrt(3), '6.9'),
          (4 * sqrt(2), '5.7'), (2 * sqrt(3), '3.5'), (8 - 4 * sqrt(3), '1.07'), (24 / sqrt(3), '13.86'), (8 * sqrt(3), '13.9'), (24 * sqrt(3), '41.6')]
for v, shown in APPROX:
    truth('%s is about %s' % (v, shown), ('%.*f' % (len(shown.split('.')[1]), float(v))) == shown)

if FAIL:
    print('\n'.join(FAIL))
    sys.exit('%d of %d checks FAILED' % (len(FAIL), N[0]))
print('all %d checks passed' % N[0])
