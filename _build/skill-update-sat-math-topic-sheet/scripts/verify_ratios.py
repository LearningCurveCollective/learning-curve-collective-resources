#!/usr/bin/env python3
"""Answer-key recomputations for SAT Math 5: Ratios, Rates and Proportions (needs sympy).
Every answer is recomputed here from the question's own numbers, then compared with what the builder
stores: the first accepted form of a typed answer, or the option marked correct. For multiple-choice
items the script also confirms that exactly one option matches. Every accepted typed form is run
through the page's own matching rule (exact, or a decimal within 0.0011).
Run: python3 verify_ratios.py   -> prints the number of checks; exits non-zero on any failure."""
import os, re, sys
from sympy import Rational as R, symbols, solve, Eq, sqrt, simplify, Integer, nsimplify
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_ratios as B

n = 0
def ok(cond, what):
    global n
    n += 1
    assert bool(cond), 'FAILED: ' + what

x, y, k, d, b, t, a, r = symbols('x y k d b t a r', positive=True)
def one(eq, v):
    s = solve(eq, v); assert len(s) == 1, (eq, s); return s[0]

def val(s):
    """The number in a typed form or in a simple LaTeX option: 7/3, 0.35, $\\$7.50$, $16{,}200$, $\\dfrac{13}{40}$."""
    s = s.replace('\\$', '').replace('$', '').replace('{,}', '').replace(' ', '')
    m = re.fullmatch(r'\\d?frac\{(-?[\d.]+)\}\{(-?[\d.]+)\}', s)
    if m: return R(m.group(1)) / R(m.group(2))
    m = re.fullmatch(r'(-?[\d.]+)/(-?[\d.]+)', s)
    if m: return R(m.group(1)) / R(m.group(2))
    m = re.fullmatch(r'-?\d*\.?\d+', s)
    return R(s) if m else None

def typed(item, want, what):
    """A typed answer: the first accepted form is the exact answer, and every accepted form passes the page's rule."""
    acc = item['accept']
    ok(val(acc[0]) == want, what + ': stored ' + acc[0] + ', recomputed ' + str(want))
    for form in acc:
        v = val(form)
        ok(v is not None and (v == want or ('.' in form and abs(v - want) < R(11, 10000))), what + ': accepted form ' + form)

def typed_any(item, wants, what):
    """A typed answer with several correct values: the accepted list is that set."""
    ok(sorted(val(f) for f in item['accept']) == sorted(wants), what + ': accepted ' + str(item['accept']))

def choice(item, want, what, key='options'):
    """Multiple choice with numeric options: the marked option equals the recomputed value, and no other option does."""
    vals = [val(o) for o in item[key]]
    ok(None not in vals, what + ': an option did not parse ' + str(item[key]))
    ok(vals[item['correct']] == want, what + ': marked ' + str(item[key][item['correct']]) + ', recomputed ' + str(want))
    ok(sum(1 for v in vals if v == want) == 1, what + ': exactly one option matches')
    ok(len(set(vals)) == len(vals), what + ': options are distinct')

def choice_truth(item, truth, what, key='options'):
    """Multiple choice with non-numeric options: `truth` lists True/False per option, worked out here."""
    truth = [bool(v) for v in truth]
    ok(len(truth) == len(item[key]) and sum(truth) == 1 and truth[item['correct']], what + ': one true option, and it is the marked one')

# ---------------- RULES (examples, notes and common mistakes)
ok(R(4, 4 + 7) == R(4, 11) and 55 / 11 == 5 and 4 * 5 == 20 and 7 * 5 == 35 and 20 + 35 == 55, 'R1 A')
kk = one(Eq(3 * (3 * k) + 2 * (4 * k), 85), k); ok(kk == 5 and 3 * kk == 15 and 4 * kk == 20 and 9 + 8 == 17 and R(15, 20) == R(3, 4), 'R1 B')
ok(R(4, 7) == R(8, 14) == R(20, 35), 'R1 note')
p = one(Eq(R(45, 6), x / 16), x); ok(p == 120 and 6 * 120 == 720 and R(45, 6) == R(15, 2) and R(15, 2) * 16 == 120, 'R2 A')
f = one(Eq(R(5, 2) / 20, x / 52), x); ok(f == R(13, 2) and R(5, 2) * 52 / 20 == R(13, 2), 'R2 B')
ok(R(3, 2) == R(6, 4) == R(9, 6) == R(3, 2), 'R3 table')
ok(R(33, 6) == R(11, 2) and R(11, 2) * 10 == 55, 'R3 A')
kk = one(Eq(12, k * 2**2), k); ok(kk == 3 and kk * 5**2 == 75, 'R3 B')
ok(R(1, 2) * (2 * 1)**2 == 4 * (R(1, 2) * 1**2), 'R3 doubling x multiplies y by 4')
ok(2 * 35 == 70 and 3 * 55 == 165 and 70 + 165 == 235 and R(235, 5) == 47, 'R4 A')
ok(R(36, 36) == 1 and R(36, 18) == 2 and R(72, 3) == 24 and R(36 + 18, 2) == 27 and abs(24 - 18) < abs(36 - 24), 'R4 B, note and mistake 5')
dd = symbols('dd', positive=True); ok(simplify(2 * dd / (dd / 36 + dd / 18) - 24) == 0, 'R4 B for any distance')
ok(R(15 * 3600, 1000) == 54, 'R4 C')
ok(6 * 10 == 60 and R(60, 15) == 4, 'R5 A')
ok(3 * 20 == 60 and R(60, 5) == 12 and R(60, 12) == 5, 'R5 B')
ok(R(1, 6) + R(1, 12) == R(1, 4) and R(3, 12) == R(1, 4), 'R6 A')
ok(R(1, 6) - R(1, 10) == R(1, 15), 'R6 B')
ok(6 * 10 == 60 and R(60, 4) == 15 and R(12 * 15, 8) == R(45, 2), 'R6 C')
ok(simplify(1 / (1 / a + 1 / b) - a * b / (a + b)) == 0, 'R6 the shortcut')
ok(R(14, 4) == R(7, 2), 'M3')
ok((0 + 3, 1 + 3, 2 + 3) == (3, 4, 5) and R(4, 1) != R(5, 2), 'M4 the ratio y/x changes on y = x + 3')
ok(one(Eq(6 * 10, 15 * d), d) == 4, 'M6'); ok(6 + 12 == 18 and (6 + 12) / 2 == 9 and 1 / (R(1, 6) + R(1, 12)) == 4, 'M7')

# ---------------- STEPS
S = B.STEPS
ok(len(S) == 6 and [s['ess'] for s in S] == [True, True, True, True, False, False] and B.LAST_STARRED_STEP_INDEX == 3, 'steps: stars')
ok(72 / (7 + 5) == 6 and 5 * 6 == 30 and 7 * 6 == 42 and 42 + 30 == 72 and R(42, 30) == R(7, 5) and R(5, 12) * 72 == 30, 'S1')
typed(S[0]['micro'], R(2, 2 + 7), 'S1 quick check')
bb = one(Eq(R(84, 7), x / 90), x); ok(bb == 1080 and R(3, 2) * 60 == 90 and 84 * 90 == 7560 and R(84, 7) == 12 and R(84, 7) * R(3, 2) == 18, 'S2')
typed(S[1]['micro'], R(18, 8) * 20, 'S2 quick check'); ok(R(18, 8) == R(9, 4), 'S2 quick check unit price')
ok(R(10, 4) == R(5, 2) and R(5, 2) * 14 == 35 and R(10, 4) == R(35, 14) and R(14, 4) == R(7, 2) and 10 * R(7, 2) == 35, 'S3')
typed(S[2]['micro'], R(26, 8) * 6, 'S3 quick check'); ok(R(26, 8) == R(13, 4), 'S3 quick check k')
ok(R(90, 30) == 3 and R(90, 45) == 2 and R(180, 5) == 36 and simplify(2 * dd / (dd / 30 + dd / 45) - 36) == 0 and R(30 + 45, 2) == R(75, 2) and R(1, 30) + R(1, 45) == R(1, 18), 'S4')
typed(S[3]['micro'], R(3 + 5) / (R(24 + 56, 60)), 'S4 quick check')
tt = one(Eq(72 * t, 54 * 4), t); ok(tt == 3 and 54 * 4 == 216 and R(72, 54) == R(4, 3) and abs(float(R(72 * 4, 54)) - 5.33) < 0.01, 'S5')
typed(S[4]['micro'], R(8 * 15, 12), 'S5 quick check')
ok(R(1, 20) + R(1, 30) == R(1, 12) and R(20 * 30, 50) == 12 and 20 + 30 == 50 and (20 + 30) / 2 == 25, 'S6')
typed(S[5]['micro'], 1 / (R(1, 5) + R(1, 20)), 'S6 quick check')

# ---------------- SKILL PRACTICE
F = B.FLUENCY
ok([len(s['items']) for s in F] == [5, 5, 5, 5, 4], 'skill practice: 24 items in five sections')
A_, B_, C_, D_, E_ = [s['items'] for s in F]
typed(A_[0], R(4, 5 + 4), 'A1'); typed(A_[1], R(2, 5) * 40, 'A2'); typed(A_[2], 7 * one(Eq(7 * k + 2 * k, 63), k), 'A3')
typed(A_[3], R(12, 3) * 7, 'A4'); typed(A_[4], R(66, 5 + 6) * 6, 'A5')
typed(B_[0], one(Eq(R(6, 15), x / 35), x), 'B1'); typed(B_[1], 240 / R(96, 3), 'B2'); typed(B_[2], R(625, 100) / 5 * 12, 'B3')
typed(B_[3], one(Eq(R(15, 2), x / 9), x), 'B4'); typed(B_[4], R(18, 4) * 60, 'B5')
typed(C_[0], R(18, 4), 'C1'); typed(C_[1], R(12, 8) * 22, 'C2')
# C3: which equation has a constant ratio y/x for every x?
def proportional(fn): return len({fn(R(v)) / R(v) for v in (1, 2, 5)}) == 1
choice_truth(C_[2], [proportional(lambda v: v + 4), proportional(lambda v: 4 / v), proportional(lambda v: 4 * v), proportional(lambda v: 4 * v + 1)], 'C3', key='opts')
typed(C_[3], R(5, 4) * 14, 'C4'); typed(C_[4], one(Eq(18, k * 3**2), k) * 5**2, 'C5')
typed(D_[0], R(156, 3) * 5, 'D1'); typed(D_[1], R(2 * 12 + 1 * 18, 3), 'D2'); typed(D_[2], R(12) / (R(6, 2) + R(6, 6)), 'D3')
typed(D_[3], R(90 * 1000, 3600), 'D4')
avg = simplify(2 * dd / (dd / 24 + dd / 56)); ok(avg == R(168, 5) and R(336, 10) == R(168, 5) and R(168, 24) == 7 and R(168, 56) == 3 and R(24 + 56, 2) == 40, 'D5 value')
choice_truth(D_[4], [avg < 40, avg == 40, avg > 40, False], 'D5', key='opts')
typed(E_[0], R(4 * 9, 6), 'E1'); typed(E_[1], R(6 * 14, 4), 'E2'); typed(E_[2], 1 / (R(1, 9) + R(1, 18)), 'E3'); typed(E_[3], 1 / (R(1, 8) - R(1, 10)), 'E4')

# ---------------- SAT-STYLE PRACTICE
G = B.GAUNTLET
ok(len(G) == 10 and [g['type'] for g in G].count('mc') == 6 and [g['type'] for g in G].count('ne') == 4, 'practice: 10 items, both formats')
choice(G[0], R(210, 100) / 14 * 50, 'P1'); ok(R(210, 100) / 14 == R(15, 100) and R(210, 100) * 3 == R(63, 10), 'P1 work')
typed(G[1], R(77, 3 + 8) * 8, 'P2'); ok(3 * 7 + 56 == 77, 'P2 check')
ok(R(7, 2) == R(21, 6) == R(35, 10), 'P3 the ratio is constant')
choice_truth(G[2], [all(yv == xv + 5 for xv, yv in [(2, 7), (6, 21), (10, 35)]), all(yv == R(2, 7) * xv for xv, yv in [(2, 7), (6, 21), (10, 35)]),
                    all(yv == R(7, 2) * xv for xv, yv in [(2, 7), (6, 21), (10, 35)]), all(yv == 7 * xv for xv, yv in [(2, 7), (6, 21), (10, 35)])], 'P3')
# P4: which panel is a line through the origin? Read from the figure specs themselves.
def is_prop(spec):
    if spec.get('curves'): return False
    ln = spec['lines'][0]
    return ln['b'] == 0 and ln['m'] != 0
panels = [B.FIGS[p['fig']] for p in B.FIGS['p4']['panels']]
choice_truth(G[3], [is_prop(s) for s in panels], 'P4'); ok([p['t'] for p in B.FIGS['p4']['panels']] == ['A', 'B', 'C', 'D'] and G[3]['options'] == ['Graph A', 'Graph B', 'Graph C', 'Graph D'], 'P4 labels')
typed(G[4], R(2 * 51 + 3 * 56, 5), 'P5'); ok(R(51 + 56, 2) == R(107, 2) and 102 + 168 == 270, 'P5 the plain average is 53.5')
choice(G[5], R(45, 20) * 6 * 60, 'P6'); ok(R(45, 20) * 6 == R(27, 2) and 45 * 6 == 270 and 45 * 360 == 16200 and 360 / 20 == 18, 'P6 work')
s2 = solve([Eq(x / y, R(5, 2)), Eq(3 * x - 4 * y, 56)], [x, y], dict=True); ok(len(s2) == 1 and s2[0][x] == 40 and s2[0][y] == 16, 'P7 system')
typed(G[6], s2[0][x], 'P7')
kk = 3 * 60; ok(9 * 20 == kk, 'P8 constant product'); choice(G[7], R(kk, 6) - R(kk, 18), 'P8'); ok(R(kk, 6) == 30 and R(kk, 18) == 10 and 30 + 10 == 40, 'P8 work')
dv = one(Eq(d / 20 + d / 12, 4), d); choice(G[8], dv, 'P9'); ok(dv == 30 and R(30, 20) + R(30, 12) == 4 and R(20 + 12, 2) * 4 == 64, 'P9 work')
bv = one(Eq(R(1, 28) + 1 / b, R(1, 12)), b); typed(G[9], bv, 'P10'); ok(bv == 21 and R(28 * 21, 49) == 12 and R(1, 12) - R(1, 28) == R(4, 84), 'P10 work')
ok([g['ess'] for g in G] == [True] * 7 + [False, True, False], 'practice: starred chips')

# ---------------- CHALLENGE
Cq = B.CHALLENGE
ok(len(Cq) == 8, 'challenge: 8 items')
mixv = (R(2, 5) + R(1, 4)) / 2; choice(Cq[0], mixv, 'Ch1'); ok(mixv == R(13, 40) and R(2 + 1, 5 + 4) == R(1, 3) and R(2, 5) + R(1, 4) == R(13, 20) and R(8 + 5, 40) == mixv, 'Ch1 work')
typed(Cq[0]['extras'][0], (R(1, 5) + R(1, 2)) / 2, 'Ch1a'); typed(Cq[0]['extras'][1], (R(2, 5) + R(3, 4)) / 2, 'Ch1b'); typed(Cq[0]['extras'][2], (R(3, 10) + R(1, 4)) / 2, 'Ch1c')
av = solve(Eq(a / 2, 32 / a), a); ok(av == [8], 'Ch2 one positive value'); typed(Cq[1], av[0], 'Ch2')
AB = sqrt(6**2 + 8**2); DE = AB * R(20, 8); ok(AB == 10 and DE == 25 and R(20, 8) == R(5, 2) and 6 * R(5, 2) == 15 and 15**2 + 20**2 == 25**2 and 20 - 8 == 12, 'Ch3 work'); typed(Cq[2], DE, 'Ch3')
f3 = B.FIGS['c3']; P = {p['t']: p['p'] for p in f3['pts']}
def dist(u, v): return ((u[0] - v[0])**2 + (u[1] - v[1])**2) ** 0.5
ok(abs(dist(P['B'], P['C']) / dist(P['A'], P['C']) - 8 / 6) < 1e-6 and abs(dist(P['E'], P['F']) / dist(P['B'], P['C']) - 20 / 8) < 1e-6 and abs(dist(P['D'], P['F']) / dist(P['A'], P['C']) - 20 / 8) < 1e-6, 'Ch3 the figure is drawn to scale')
ok({s['t'] for s in f3['sides']} == {'6', '8', '20'}, 'Ch3 figure labels')
choice(Cq[3], simplify(2 * dd / (dd / 28 + dd / 70)), 'Ch4'); ok(R(140, 28) == 5 and R(140, 70) == 2 and R(280, 7) == 40 and R(28 + 70, 2) == 49, 'Ch4 work')
typed(Cq[3]['extras'][0], simplify(2 * dd / (dd / 30 + dd / 70)), 'Ch4a'); typed(Cq[3]['extras'][1], simplify(2 * dd / (dd / 12 + dd / 4)), 'Ch4b'); typed(Cq[3]['extras'][2], R(1200) / (R(600, 400) + R(600, 240)), 'Ch4c')
pa, om = symbols('pa om'); s5 = solve([Eq((pa + 4) / (om + 4), R(2, 3)), Eq((pa + 12) / (om + 12), R(3, 4))], [pa, om], dict=True)
ok(len(s5) == 1 and s5[0][pa] == 12 and s5[0][om] == 20, 'Ch5 ages'); typed(Cq[4], s5[0][pa] + s5[0][om], 'Ch5')
ok(one(Eq((2 * k + 8) / (3 * k + 8), R(3, 4)), k) == 8 and 16 + 24 == 40, 'Ch5 work')
sums = sorted({u + v for u in range(1, 1000) for v in range(1, 1000) if 7 * u == 4 * v and u % 6 == 0 and v % 10 == 0 and u + v < 1000})
ok(sums == [330, 660, 990], 'Ch6 by search'); typed_any(Cq[5], sums, 'Ch6')
rv = one(Eq(r + 3 * r, R(1, 6)), r); typed(Cq[6], 1 / rv, 'Ch7'); ok(1 / (3 * rv) == 8 and R(1, 8) + R(1, 24) == R(1, 6), 'Ch7 work')
choice(Cq[7], R(6 * 8, 4) * 15 / 9, 'Ch8'); ok(6 * 8 == 48 and 48 / 4 == 12 and 15 * 12 == 180 and 8 * R(15, 4) == 30 and 8 * R(15, 4) * R(9, 6) == 45 and 8 * R(15, 4) / R(3, 2) == 20, 'Ch8 work')
ok([c['ess'] for c in Cq] == [True] * 6 + [False, False], 'challenge: starred chips')

# ---------------- EXIT
X = B.EXIT
choice(X[0], R(5, 2 + 5), 'X1', key='opts'); choice(X[1], R(24, 9) * 15, 'X2', key='opts')
ok(X[2]['opts'][X[2]['correct']].startswith('$26.4$') and R(132) / (R(66, 33) + R(66, 22)) == R(132, 5) and R(132, 5) == R(264, 10) and R(33 + 22, 2) == R(55, 2) and 66 + 66 == 132, 'X3')
ok(len({o.split(' ')[0] for o in X[2]['opts']}) == 4, 'X3 options are distinct')

# ---------------- figures used in the rules
ok(B.FIGS['r_direct']['lines'][0] == dict(m=1.5, b=0) and all(p['y'] == 1.5 * p['x'] for p in B.FIGS['r_direct']['points']), 'fig r_direct')
ok(B.FIGS['r_notdirect']['lines'][0] == dict(m=1, b=3), 'fig r_notdirect')
ok(all(p['y'] == 0.5 * p['x']**2 for p in B.FIGS['r_square']['points']), 'fig r_square')
ok(all(p['x'] * p['y'] == 12 for p in B.FIGS['r_inverse']['points']) and B.FIGS['r_inverse']['curves'][0]['inv'] == 12, 'fig r_inverse')
ok(B.FIGS['s3']['lines'][0]['m'] * 4 == 10 and B.FIGS['s3']['points'][0]['x'] == 4 and B.FIGS['s3']['points'][0]['y'] == 10, 'fig s3')
print(n, 'checks passed')
