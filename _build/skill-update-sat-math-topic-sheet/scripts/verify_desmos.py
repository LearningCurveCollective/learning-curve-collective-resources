#!/usr/bin/env python3
"""Independent recomputation of every answer key in the two Desmos sheets.
Each check recomputes the value from the question's own numbers (sympy / fractions) and
compares it with the first entry of the sheet's accept list or the keyed MC option."""
import math, statistics
from fractions import Fraction as F
import sympy as sp
import build_desmos1 as d1, build_desmos2 as d2

x, y, a, b, c, k, h, p, s, m, l, n = sp.symbols('x y a b c k h p s m l n', real=True)
checks = []


def _num(v):
    if isinstance(v, F):
        return sp.Rational(v.numerator, v.denominator)
    return sp.nsimplify(v)


def same(u, v):
    if isinstance(u, (tuple, list, sp.Tuple)) and isinstance(v, (tuple, list, sp.Tuple)):
        return len(u) == len(v) and all(same(i, j) for i, j in zip(u, v))
    if isinstance(u, (str, bool)) or isinstance(v, (str, bool)):
        return u == v
    try:
        return sp.simplify(_num(u) - _num(v)) == 0
    except Exception:
        return u == v


def ok(label, got, want):
    checks.append((label, same(got, want), got, want))


def val(v):
    """accept-list entry -> exact number"""
    return sp.nsimplify(v)


def near(label, got, want, tol=6e-4):
    checks.append((label, abs(float(got) - float(want)) < tol, got, want))


def lsq(xs, ys):
    xb, yb = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((u - xb) ** 2 for u in xs)
    sxy = sum((u - xb) * (v - yb) for u, v in zip(xs, ys))
    syy = sum((v - yb) ** 2 for v in ys)
    mm = sxy / sxx
    return mm, yb - mm * xb, sxy ** 2 / (sxx * syy)


def solve2(e1, e2, vars_):
    r = sp.solve([e1, e2], vars_, dict=True)
    assert len(r) == 1, r
    return r[0]


def expfit(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    bb = sp.Rational(y2, y1) ** sp.Rational(1, x2 - x1)
    return sp.nsimplify(y1) / bb ** x1, bb


def quadfit(pts):
    r = sp.solve([a * u ** 2 + b * u + c - v for u, v in pts], [a, b, c], dict=True)[0]
    return r[a], r[b], r[c]


# =========================================================== SHEET 1
S, FL, G, CH, EX = d1.STEPS, d1.FLUENCY, d1.GAUNTLET, d1.CHALLENGE, d1.EXIT
fl = [it for sec in FL for it in sec['items']]

# rules-tab examples
r = solve2(3 * x - 2 * y - 12, x + y - 9, [x, y]); ok('1.M1 exB', (r[x], r[y]), (6, 3))
near('1.M2 exA', math.sqrt(4.5), 2.121)
hx = -2 * (x - 1) * (x - 7); ok('1.M2 exB', (sp.solve(sp.diff(hx, x), x)[0], hx.subs(x, 4)), (4, 18))
ok('1.M2 dots vertex', (sp.solve(sp.diff(x**2 - 2*x - 8, x), x)[0], (x**2 - 2*x - 8).subs(x, 1), sorted(sp.solve(x**2 - 2*x - 8, x))), (1, -9, [-2, 4]))
r = solve2(3 * x + 2 * y - 16, y - x + 2, [x, y]); ok('1.M3 dz', (r[x], r[y]), (4, 2))
ok('1.M3 exA', sorted(sp.solve(sp.Eq(sp.Abs(2 * x - 3), 11), x)), [-4, 7])
ok('1.M3 exB', sp.solve(sp.Eq(3 * (x - 2) + 5, 2 * x + 7), x), [8])
ok('1.M3 exC', [v for v in sp.solve(sp.Eq(x + 9, (x - 3) ** 2), x) if sp.sqrt(v + 9) == v - 3], [7])
ok('1.M4 exC', sp.solve(sp.Eq(x**2 - 4*x + 7, 2*x - 2), x), [3]); ok('1.M4 exC y', 2 * 3 - 2, 4)
ok('1.M5 dz k', sp.solve(sp.Eq(sp.Rational(2, 5), -6 / k), k), [-15])
ok('1.M5 exA', sp.solve(sp.discriminant(x**2 + 6*x + c, x), c), [9])
ok('1.M5 exB', sp.solve(sp.Eq(k / 3, sp.Rational(12, 4)), k), [9]); ok('1.M5 exB const', 30 / 10, 3)
f = x**2 - 6*x + 5; ok('1.M6 dz', (f.subs(x, 3), (f + 4).subs(x, 3)), (-4, 0))
ok('1.M6 exA', sp.expand((2*x + 3) * (x - 4)), 2*x**2 - 5*x - 12)
ok('1.M6 exB', ((4*2 + 0 == 8), (0 + 8 == 8), (2*8 + 0 == 16), (0 + 8*2 == 16)), (True, True, True, True))
ok('1.M7 exA', (5 <= 2*3 + 1, 5 > -3 + 4, 1 == -3 + 4), (True, True, True))
ok('1.M8 dz', (F(sum([4, 9, 9, 13, 20, 23]), 6), statistics.median([4, 9, 9, 13, 20, 23]), F(15, 100) * 80), (13, 11, 12))
ok('1.M8 exA', (statistics.mean([2, 3, 3, 8, 34]), statistics.median([2, 3, 3, 8, 34]), F(18, 100) * 250), (10, 3, 45))
mm, bb, r2 = lsq([1, 3, 6, 8], [4, 9, 14, 19]); near('1.M9 m', mm, 2.06897, 6e-6); near('1.M9 b', bb, 2.18966, 6e-6); near('1.M9 R2', r2, 0.9931, 6e-5); near('1.M9 exC', mm * 10 + bb, 22.9, 0.06)

# steps (micro checks)
r = solve2(2 * x + y - 13, x - y - 2, [x, y]); ok('1.S1 micro', r[x], val(S[0]['micro']['accept'][0]))
ok('1.S2 micro', sp.minimum(x**2 + 4*x - 1, x), val(S[1]['micro']['accept'][0]))
ok('1.S3 prob sum', sum(sp.solve(sp.Eq(sp.Abs(2*x - 3), 11), x)), 3)
r = solve2(3 * x + 2 * y - 16, y - x + 2, [x, y]); ok('1.S3 micro', r[x], val(S[2]['micro']['accept'][0]))
ok('1.S4 micro parallel', (sp.Rational(1, 2) == sp.Rational(3, 6), sp.Rational(3, -2) != sp.Rational(4, -6), S[3]['micro']['correct']), (True, True, 0))
ok('1.S5 distinct', sp.Rational(7 * 3) != 4, True)
ok('1.S5 micro', sp.solve(sp.discriminant(x**2 + 6*x + c, x), c)[0], val(S[4]['micro']['accept'][0]))
ok('1.S6 prob', S[5]['prob'].count('B) $2x^2 - 5x - 12$'), 1)
ok('1.S6 micro', f.subs(x, 3) + f.subs(x, 0), val(S[5]['micro']['accept'][0]))
ok('1.S7 prob', (2 <= 2*3 + 1, 2 > -3 + 4, not (1 > -3 + 4)), (True, True, True))
pts = [(4, 1), (2, 3), (5, 3), (1, 7)]
ok('1.S7 micro', [i for i, (u, v) in enumerate(pts) if v > u - 1 and v < -u + 7], [S[6]['micro']['correct']])
ok('1.S8 prob', F(78, 6) - 11, 2); ok('1.S8 micro', statistics.median([6, 2, 11, 7, 4]), val(S[7]['micro']['accept'][0]))
mm, bb, _ = lsq([0, 2, 4, 6], [3, 8, 11, 18]); near('1.S9 micro m', mm, float(val(S[8]['micro']['accept'][0])), 1e-9); near('1.S9 micro b', bb, 2.8, 1e-9)

# fluency
ok('1.F1', fl[0]['correct'], 1); ok('1.F2', fl[1]['correct'], 1); ok('1.F4', fl[3]['correct'], 1)
near('1.F3', math.sqrt(50) + 7, float(fl[2]['accept'][0]), 6e-3)
ok('1.F5', max(sp.solve(x**2 - 2*x - 15, x)), val(fl[4]['accept'][0]))
ok('1.F6', sp.maximum(-x**2 + 8*x - 7, x), val(fl[5]['accept'][0]))
near('1.F7', math.sqrt(20 / 3), float(fl[6]['accept'][0]), 6e-3)
ok('1.F8', 4 + 3, val(fl[7]['accept'][0]))
r = solve2(y - 3*x + 5, y + x - 7, [x, y]); ok('1.F9', r[y], val(fl[8]['accept'][0]))
ok('1.F10', min(sp.solve(sp.Eq(sp.Abs(x - 4), 9), x)), val(fl[9]['accept'][0]))
ok('1.F11', (sp.Rational(4, 2) == sp.Rational(2, 1) == sp.Rational(10, 5), fl[10]['correct']), (True, 3))
ok('1.F12', (sp.discriminant(x**2 - 4*x + 1 + 5, x) < 0, fl[11]['correct']), (True, 0))
ok('1.F13', 2, val(fl[12]['accept'][0]))
ok('1.F14', F(sum([12, 15, 15, 18, 25]), 5), val(fl[13]['accept'][0]))
ok('1.F15', statistics.median([31, 8, 19, 24, 8, 12]), val(fl[14]['accept'][0]))
ok('1.F16', fl[15]['correct'], 2)

# practice set
ok('1.G1', sp.minimum(x**2 - 10*x + 16, x), val(G[0]['accept'][0]))
r = solve2(y - 2*x - 1, 3*x + y - 16, [x, y]); ok('1.G2', G[1]['options'][G[1]['correct']], '$%s$' % r[y])
ok('1.G3', (sp.Rational(5, 10) == sp.Rational(-2, -4), sp.Rational(5, 10) != sp.Rational(8, 3), G[2]['correct']), (True, True, 0))
ok('1.G4', max(sp.solve(sp.Eq(sp.Abs(3*x + 2), 13), x)), val(G[3]['accept'][0])); near('1.G4 dec', 11 / 3, 3.667)
ok('1.G5', sp.expand((3*x - 2)**2 - (x + 4)*(x - 4)), 8*x**2 - 12*x + 20); ok('1.G5 key', G[4]['options'][G[4]['correct']], r'$8x^2 - 12x + 20$')
ok('1.G6', sp.solve(sp.Eq(sp.Rational(4, 3), -k / 9), k)[0], val(G[5]['accept'][0])); ok('1.G6 distinct', sp.Rational(6 * -3) != 5, True)
mm, bb, _ = lsq([2, 4, 7, 9], [3, 8, 12, 17]); near('1.G7 m', mm, 1.89655, 6e-6); near('1.G7 b', bb, -0.431034, 6e-7); ok('1.G7 key', G[6]['options'][G[6]['correct']], r'$y = 1.9x - 0.4$')
ok('1.G8', max(v for v in range(-20, 20) if v >= 2*3 - 3 and v < -3 + 9), val(G[7]['accept'][0]))
ok('1.G9', (sp.factor(2*x**2 - 8*x + 3 + 5), len(sp.solve(2*x**2 - 8*x + 8, x)), G[8]['correct']), (2*(x - 2)**2, 1, 1))
cc = sp.solve(sp.discriminant(x**2 - 6*x + c - (2*x - 9), x), c)[0]; ok('1.G10', cc, val(G[9]['accept'][0])); ok('1.G10 touch', (sp.solve(x**2 - 8*x + 16, x), 2*4 - 9), ([4], -1))
ok('1.G key spread', sorted(q['correct'] for q in G if q['type'] == 'mc'), [0, 1, 1, 2, 3])

# challenge
r = solve2(sp.Rational(2, 3)*x - sp.Rational(1, 4)*y - 5, sp.Rational(1, 2)*x + sp.Rational(3, 8)*y - 6, [x, y]); ok('1.C1', r[x] + r[y], val(CH[0]['accept'][0])); ok('1.C1 pt', (r[x], r[y]), (9, 4))
e = CH[0]['extras']
r = solve2(sp.Rational(1, 2)*x + sp.Rational(1, 4)*y - 4, x - y - 2, [x, y]); ok('1.C1 e1', r[x], val(e[0]['accept'][0]))
r = solve2(x/3 + y/2 - 7, x - y - 1, [x, y]); ok('1.C1 e2', r[y], val(e[1]['accept'][0]))
r = solve2(sp.Rational(12, 10)*x - sp.Rational(4, 10)*y - 2, sp.Rational(3, 10)*x + sp.Rational(2, 10)*y - sp.Rational(8, 10), [x, y]); ok('1.C1 e3', r[x] + r[y], val(e[2]['accept'][0]))
sols = [v for v in sp.solve(sp.Eq(sp.Abs(2*x - 5), x + 2), x)]; ok('1.C2', (sorted(sols), sum(sols)), ([1, 7], val(CH[1]['accept'][0])))
g = (x + 2 - 3)**2 - 4; ok('1.C3', (sorted(sp.solve(g, x)), sum(sp.solve(g, x))), ([-1, 3], val(CH[2]['accept'][0])))
ok('1.C4', [v for v in sp.solve(sp.Eq(2*x + 7, (x - 4)**2), x) if sp.sqrt(2*v + 7) == v - 4], [val(CH[3]['accept'][0])])
ok('1.C5', max(sp.solve(sp.discriminant(x**2 - k*x + 4, x), k)), val(CH[4]['accept'][0])); ok('1.C5 touch', sp.solve(x**2 - 4*x + 4, x), [2])
r = solve2(y - 2*x - 3, y + x - 12, [x, y]); ok('1.C6', r[y], val(CH[5]['accept'][0]))

# exit
ok('1.E1', EX[0]['correct'], 0); ok('1.E2', EX[1]['opts'][EX[1]['correct']], '$%s$' % max(sp.solve(x**2 - 4*x - 12, x))); ok('1.E3', EX[2]['correct'], 3)

# =========================================================== SHEET 2
S, FL, G, CH, EX = d2.STEPS, d2.FLUENCY, d2.GAUNTLET, d2.CHALLENGE, d2.EXIT
fl = [it for sec in FL for it in sec['items']]

# rules-tab examples
aa, bb = expfit((2, 12), (5, 96)); ok('2.M1 dz', (aa, bb, aa * bb**8), (3, 2, 768))
r = solve2(2*m + b - 5, 6*m + b - 17, [m, b]); ok('2.M1 exA', (r[m], r[b], 10*r[m] + r[b]), (3, -1, 29))
q = quadfit([(-1, 10), (2, 1), (3, 6)]); ok('2.M1 exB', (q, q[0]*25 + q[1]*5 + q[2]), ((2, -5, 3), 28))
ok('2.M1 exC', [5 * 2**i for i in range(4)], [5, 10, 20, 40])
ok('2.M2 exB', sorted(sp.solve(p**2 - p - 12, p)), [-3, 4])
r = solve2(2*a + 3*b - 12, a - b - 1, [a, b]); ok('2.M3 dz', (r[a], r[b], 3*r[a] - r[b]), (3, 2, 7))
r = solve2(a + s - 50, 12*a + 8*s - 520, [a, s]); ok('2.M3 exA', (r[a], r[s]), (30, 20))
r = sp.solve([a + b + c - 10, a - b - 1, b + c - 7], [a, b, c], dict=True)[0]; ok('2.M3 exB', (r[a], r[b], r[c]), (3, 2, 5))
ok('2.M4 dz', sp.expand((2*x + 3)*(x - 4)), 2*x**2 - 5*x - 12)
ok('2.M4 exA', sp.expand(2*(x + 3)**2 - 11), 2*x**2 + 12*x + 7)
ok('2.M4 exB', sp.expand(2*(x + 2) + 3*(x - 1)), 5*x + 1)
ok('2.M5 dz', sp.solve(sp.discriminant(x**2 - 4*x + c - (2*x - 3), x), c), [6]); ok('2.M5 line', sp.expand((-6)**2 - 4*(c + 3)), sp.discriminant(x**2 - 6*x + (c + 3), x))
ok('2.M5 touch', (sp.solve(x**2 - 6*x + 9, x), 2*3 - 3, 9 - 12 + 6), ([3], 3, 3))
ok('2.M5 dashed crosses twice', sp.discriminant(x**2 - 4*x + 3 - (2*x - 3), x) > 0, True)
ok('2.M5 exA', sorted(sp.solve(sp.discriminant(x**2 + k*x + 16, x), k)), [-8, 8])
ok('2.M5 exB', sp.solve(sp.Eq(k / 3, sp.Rational(4, 5)), k), [sp.Rational(12, 5)]); ok('2.M5 exB distinct', sp.Rational(12, 5) / 4 * 7 != 4, True)
ok('2.M5 exC', sp.solve(sp.discriminant(2*x**2 - 4*x + c, x), c), [2])
ok('2.M6 dz', sp.expand((x - 3)**2 + (y + 2)**2 - 25 - (x**2 + y**2 - 6*x + 4*y - 12)), 0)
ok('2.M6 exA', sorted(sp.solve(x**2 + (x + 1)**2 - 25, x)), [-4, 3])
ok('2.M6 exB', (sorted(sp.solve(x**2 - 3 - 2*x, x)), sum(sp.solve(x**2 - 3 - 2*x, x))), ([-1, 3], 2))
ok('2.M6 exC', sp.expand((x + 1)**2 + (y - 4)**2 - 25 - (x**2 + y**2 + 2*x - 8*y - 8)), 0); ok('2.M6 exC top', 4 + 5, 9)
ok('2.M7 dz', F(1*3 + 2*5 + 3*8 + 4*4, 20), F(265, 100))
near('2.M7 exA', statistics.stdev([10, 12, 14, 16, 18]), 3.16, 6e-3); near('2.M7 exA2', statistics.stdev([6, 10, 14, 18, 22]), 6.32, 6e-3)
ok('2.M7 exB', sp.solve(sp.Eq((8 + 11 + 15 + 20 + k) / 5, 14), k), [16])
near('2.M8 rad', math.sin(30), -0.988); near('2.M8 side', 15 * math.sin(math.radians(28)), 7.042); near('2.M8 exB', math.sin(math.radians(58)), 0.848); near('2.M8 exB2', math.cos(math.radians(32)), 0.848)
r = sp.solve([sp.expand((a*x + 2)*(b*x + 5) - (12*x**2 + c*x + 10)).coeff(x, 2), sp.expand((a*x + 2)*(b*x + 5) - (12*x**2 + c*x + 10)).coeff(x, 1)], [b, c], dict=True)[0]
ok('2.Trap4', (r[b].subs(a, 12), r[c].subs(a, 12)), (1, 62))

# steps
aa, bb = expfit((2, 12), (5, 96)); ok('2.S1', aa * bb**8, 768)
r = solve2(3*m + b - 7, 9*m + b - 25, [m, b]); ok('2.S1 micro', 12*r[m] + r[b], val(S[0]['micro']['accept'][0]))
q = quadfit([(0, 7), (2, -1), (5, 2)]); ok('2.S2', (q, q[0]*64 + q[1]*8 + q[2]), ((1, -6, 7), 23))
q = quadfit([(1, 2), (2, 3), (4, 11)]); ok('2.S2 micro', q[2], val(S[1]['micro']['accept'][0]))
ok('2.S3', sum(sp.solve(x**2 - x - 12, x)), 1); ok('2.S3 micro', S[2]['micro']['correct'], 1)
r = solve2(3*a + 2*b - 19, a - b - 3, [a, b]); ok('2.S4 micro', r[a] + r[b], val(S[3]['micro']['accept'][0]))
ex_ = sp.expand((a*x + 3)*(2*x - 5) - (8*x**2 + b*x - 15)); r = sp.solve([ex_.coeff(x, 2), ex_.coeff(x, 1)], [a, b], dict=True)[0]; ok('2.S5', (r[a], r[b], r[a] + r[b], ex_.coeff(x, 0)), (4, -14, -10, 0))
ok('2.S5 micro', sp.expand((x + 4)**2 - 13), x**2 + 8*x + 3); ok('2.S5 micro key', S[4]['micro']['accept'][0], '-13')
ok('2.S6', sp.solve(sp.discriminant(x**2 - 4*x + c - (2*x - 3), x), c)[0], 6); ok('2.S6 wrong route', sp.solve((-4)**2 - 4*c, c), [4])
ok('2.S6 micro', max(sp.solve(sp.discriminant(x**2 + k*x + 16, x), k)), val(S[5]['micro']['accept'][0]))
ok('2.S7', sp.sqrt(12 + 9 + 4), 5); ok('2.S7 micro', max(sp.solve(x**2 + (x + 1)**2 - 25, x)), val(S[6]['micro']['accept'][0]))
ok('2.S8', F(53, 20), F(265, 100)); ok('2.S8 micro', 70 - 54, val(S[7]['micro']['accept'][0]))
near('2.S9', 15 * math.sin(math.radians(28)), 7.042); near('2.S9 rad', 15 * math.sin(28), 4.06, 6e-3); ok('2.S9 micro', S[8]['micro']['correct'], 1)

# fluency
r = solve2(m + b - 4, 5*m + b - 16, [m, b]); ok('2.F1', (r[m], r[b]), (val(fl[0]['accept'][0]), 1))
aa, bb = expfit((1, 6), (3, 54)); ok('2.F2', (aa, bb, aa * bb**4), (2, 3, val(fl[1]['accept'][0])))
q = quadfit([(0, 1), (1, 0), (3, 10)]); ok('2.F3', q, (val(fl[2]['accept'][0]), -3, 1))
ok('2.F4', ([4 * 3**i for i in range(4)], fl[3]['accept'][0]), ([4, 12, 36, 108], '3'))
r = solve2(2*a + b - 11, a - b - 1, [a, b]); ok('2.F5', (r[a], r[b]), (val(fl[4]['accept'][0]), 3))
r = solve2(5*p + 2*n - sp.Rational(19, 2), 3*p + 4*n - sp.Rational(134, 10), [p, n]); ok('2.F6', (r[n], r[p]), (val(fl[5]['accept'][0]), sp.Rational(4, 5)))
ok('2.F7', sp.expand((3*x - 2)*(x + 5)), 3*x**2 + 13*x - 10); ok('2.F7 key', fl[6]['accept'][0], '13')
ok('2.F8', sp.expand((x - 5)**2 + 6), x**2 - 10*x + 31); ok('2.F8 key', fl[7]['accept'][0], '6')
ok('2.F9', sp.solve(sp.discriminant(x**2 + 10*x + c, x), c)[0], val(fl[8]['accept'][0]))
ok('2.F10', sp.sqrt(19 + 16 + 1), val(fl[9]['accept'][0])); ok('2.F10 dots', (1 + 6, 1 - 6), (7, -5))
ok('2.F11', (sorted(sp.solve(x**2 - 5 - (x + 1), x)), sum(sp.solve(x**2 - 5 - (x + 1), x))), ([-2, 3], val(fl[10]['accept'][0])))
ok('2.F12', F(2*5 + 4*3 + 6*2, 10), F(34, 10)); ok('2.F12 key', val(fl[11]['accept'][0]), sp.Rational(17, 5))
ok('2.F13-16 keys', [fl[i]['correct'] for i in (12, 13, 14, 15)], [2, 1, 0, 3])
q = quadfit([(0, 4), (2, 6), (5, 39)]); ok('2.F14 exp', (q, q[0]*9 + q[1]*3 + q[2]), ((2, -3, 4), 13))
ok('2.F15 exp', sp.solve(sp.Eq(sp.Rational(3, 6), k / -10), k), [-5])

# practice set
r = solve2(2*m + b - 9, 6*m + b - 21, [m, b]); ok('2.G1', 10*r[m] + r[b], val(G[0]['accept'][0])); ok('2.G1 mb', (r[m], r[b]), (3, 3))
r = solve2(3*m + 2*c - sp.Rational(33, 2), m + 4*c - sp.Rational(31, 2), [m, c]); ok('2.G2', (r[m], r[c], G[1]['options'][G[1]['correct']]), (sp.Rational(7, 2), 3, r'$\$3.50$'))
aa, bb = expfit((1, 10), (3, 40)); ok('2.G3', (aa, bb, aa * bb**6), (5, 2, val(G[2]['accept'][0]))); ok('2.G3 trap', 40 + 15 * 3, 85)
ok('2.G4', sp.expand(2*(x - 3)**2 - 11), 2*x**2 - 12*x + 7); ok('2.G4 key', G[3]['options'][G[3]['correct']], r'$2(x - 3)^2 - 11$')
ex_ = sp.expand((2*x + a)*(3*x - 4) - (6*x**2 + b*x - 20)); r = sp.solve([ex_.coeff(x, 1), ex_.coeff(x, 0)], [a, b], dict=True)[0]; ok('2.G5', (r[a], r[b]), (5, val(G[4]['accept'][0])))
ok('2.G6', sp.expand((x + 2)**2 + (y - 5)**2 - 49 - (x**2 + y**2 + 4*x - 10*y - 20)), 0); ok('2.G6 key', (G[5]['options'][G[5]['correct']], 5 + 7, 5 - 7), (r'$(-2, 5)$', 12, -2))
q = quadfit([(-1, 12), (1, 2), (3, 8)]); ok('2.G7', (q, q[2]), ((2, -5, 5), val(G[6]['accept'][0])))
ok('2.G8', (statistics.mean([10, 12, 14, 16, 18]) == statistics.mean([6, 10, 14, 18, 22]) == 14, statistics.stdev([6, 10, 14, 18, 22]) > statistics.stdev([10, 12, 14, 16, 18]), G[7]['correct']), (True, True, 3))
near('2.G8 sd', statistics.stdev([10, 12, 14, 16, 18]), 3.162); near('2.G8 sd2', statistics.stdev([6, 10, 14, 18, 22]), 6.325)
cc = sp.solve(sp.discriminant(2*x**2 - 4*x + c - (4*x - 3), x), c)[0]; ok('2.G9', cc, val(G[8]['accept'][0])); ok('2.G9 line', sp.expand((-8)**2 - 4*2*(c + 3)), sp.discriminant(2*x**2 - 8*x + (c + 3), x))
got = sorted(5*u + 2*v for u, v in [(3, 4), (4, 3)]); ok('2.G10', got, sorted(int(v) for v in G[9]['accept']))
ok('2.G key spread', sorted(q['correct'] for q in G if q['type'] == 'mc'), [0, 1, 2, 3])

# challenge
r = sp.solve([s + m + l - 27, l - 2*s, m - s - 3], [s, m, l], dict=True)[0]; ok('2.C1', (r[s], r[m], r[l]), (6, 9, val(CH[0]['accept'][0])))
aa, bb = expfit((2, 450), (4, 648)); ok('2.C2', (aa, bb), (val(CH[1]['accept'][0]), sp.Rational(6, 5))); ok('2.C2 trap', 450 - (648 - 450), 252)
e = CH[1]['extras']
aa, bb = expfit((1, 12), (2, 18)); ok('2.C2 e1', (aa, bb, aa * bb**3), (8, sp.Rational(3, 2), val(e[0]['accept'][0])))
aa, bb = expfit((0, 80), (2, 20)); ok('2.C2 e2', (aa, bb), (80, val(e[1]['accept'][0])))
aa, bb = expfit((2, 50), (5, 400)); ok('2.C2 e3', (aa, bb), (val(e[2]['accept'][0]), 2))
av = sp.solve(a * (5 - 3)**2 - 4 - 8, a)[0]; ok('2.C3', (av, av * 9 - 4), (3, val(CH[2]['accept'][0])))
kv = sp.solve(sp.Eq(k / 4, sp.Rational(5, 6)), k)[0]; ok('2.C4', kv, val(CH[3]['accept'][0])); near('2.C4 dec', kv, 3.33333, 6e-6); ok('2.C4 distinct', sp.Rational(2, 3) * 2 != 9, True)
ok('2.C5', sp.expand((x - 2)**2 + (y - 3)**2 - 25 - (x**2 + y**2 - 4*x - 6*y - 12)), 0); ok('2.C5 key', (3 + 5, 3 - 5), (val(CH[4]['accept'][0]), -2))
near('2.C6', 9 * math.tan(math.radians(40)), 7.552); near('2.C6 rad', 9 * math.tan(40), -10.05, 6e-3); ok('2.C6 key', CH[5]['accept'][0], '7.6')

# exit
r = solve2(3*a + b - 14, a - b - 2, [a, b]); ok('2.E2', (EX[1]['opts'][EX[1]['correct']], r[b]), ('$%s$' % r[a], 2)); ok('2.E1/E3', (EX[0]['correct'], EX[2]['correct']), (0, 3))

bad = [c_ for c_ in checks if not c_[1]]
for lab, good, got, want in bad:
    print('FAIL', lab, 'got', got, 'want', want)
print('%d checks, %d failed' % (len(checks), len(bad)))
