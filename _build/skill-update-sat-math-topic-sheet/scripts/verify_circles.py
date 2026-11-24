#!/usr/bin/env python3
"""Answer-key check for SAT Math 8: Circle Equations. Imports build_circles.py (keep the two files together)
and recomputes every keyed answer with sympy: the rules-tab examples, the worked steps and their quick checks,
Skill Practice, the practice set, the challenge questions and their extra reps, and the exit ticket. It also
confirms that each multiple-choice item has one correct choice, that every accepted typed form equals the
answer, and that each figure matches the numbers in its question and is drawn with equal scales.
Run: python3 verify_circles.py"""
import os, re, sys
from sympy import Rational as R, symbols, expand, Poly, sqrt, pi, nsimplify, simplify, solve, Eq, S

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_circles as B

x, y = symbols('x y')
N = [0]
FAIL = []


def ok(label, cond):
    N[0] += 1
    if not cond:
        FAIL.append(label)


def flat(v):
    if isinstance(v, (tuple, list)) or hasattr(v, 'args') and v.__class__.__name__ == 'Tuple':
        out = []
        for e in v:
            out += flat(e)
        return out
    return [S(v)]


def same(label, got, want):
    g, w = flat(got), flat(want)
    ok('%s: got %r, want %r' % (label, got, want), len(g) == len(w) and all(simplify(a - b) == 0 for a, b in zip(g, w)))


def circle(lhs, rhs):
    """Center and r^2 of the circle lhs = rhs (any form with equal x^2 and y^2 coefficients)."""
    p = Poly(expand(lhs - rhs), x, y)
    a = p.coeff_monomial(x**2)
    assert a != 0 and a == p.coeff_monomial(y**2) and p.coeff_monomial(x*y) == 0
    D, E, F = p.coeff_monomial(x) / a, p.coeff_monomial(y) / a, p.coeff_monomial(1) / a
    h, k = -D / 2, -E / 2
    return (h, k), h**2 + k**2 - F


def std(h, k, r2):
    return (x - h)**2 + (y - k)**2, r2


def val(s):
    """A typed answer such as '25/4', '-9' or '42.25' as an exact number."""
    return nsimplify(s, rational=True)


def typed(label, item, want):
    acc = item['accept']
    same(label + ' key', val(acc[0]), want)
    for a in acc[1:]:
        ok('%s: accepted form %s' % (label, a), abs(float(val(a)) - float(S(want))) < 0.0011)


def strip(s):
    return re.sub(r'<[^>]+>', '', s).replace('\\,', '')


def pis(opt):
    m = re.fullmatch(r'\$(\d+)\\pi\$', opt)
    return int(m.group(1))


def tup(opt):
    m = re.fullmatch(r'\$\((-?\d+), (-?\d+)\)\$', opt)
    return (int(m.group(1)), int(m.group(2)))


def eqn(opt):
    """(h, k, r^2) of an option written in standard form."""
    m = re.fullmatch(r'\$\(x ([+-]) (\d+)\)\^2 \+ \(y ([+-]) (\d+)\)\^2 = (\d+)\$', opt)
    h = int(m.group(2)) * (1 if m.group(1) == '-' else -1)
    k = int(m.group(4)) * (1 if m.group(3) == '-' else -1)
    return (h, k, int(m.group(5)))


def one_right(label, opts, correct, test):
    hits = [i for i, o in enumerate(opts) if test(o)]
    ok('%s: exactly one correct choice, and it is the keyed one (hits %r, key %r)' % (label, hits, correct), hits == [correct])


def need(label, text, *subs):
    for sub in subs:
        ok('%s: sheet text contains %r' % (label, sub), sub in text)


RULES, STEPS, FL, G, C, EX, FIGS = B.RULES, B.STEPS, B.FLUENCY, B.GAUNTLET, B.CHALLENGE, B.EXIT, B.FIGS

# ------------------------------------------------------------------ rules tab examples
same('R1 A', circle(*std(3, -2, 25)), ((3, -2), 25));              need('R1 A', RULES, r'$(x - 3)^2 + (y + 2)^2 = 25$ has center $(3, -2)$ and radius $5$')
same('R1 B', circle(x**2 + (y - 4)**2, 12), ((0, 4), 12));          same('R1 B root', sqrt(12), 2 * sqrt(3)); need('R1 B', RULES, r'center $(0, 4)$ and radius $\sqrt{12} = 2\sqrt{3}$')
same('R1 C', circle((x + 1)**2 + (y - 5)**2, 9), ((-1, 5), 9));     need('R1 C', RULES, r'center $(-1, 5)$ and radius $3$ has the equation $(x + 1)^2 + (y - 5)^2 = 9$')
same('R2 A', circle(x**2 + y**2 - 6*x + 4*y, 12), ((3, -2), 25));   need('R2 A', RULES, r'$(x - 3)^2 + (y + 2)^2 = 25$. The center is $(3, -2)$ and the radius is $5$')
same('R2 B', circle(x**2 + 8*x + y**2, 20), ((-4, 0), 36));         need('R2 B', RULES, r'$(x + 4)^2 + y^2 = 36$. The center is $(-4, 0)$ and the radius is $6$')
same('R2 C', circle(2*x**2 + 2*y**2 - 12*x + 4*y, 78), ((3, -1), 49)); need('R2 C', RULES, r'$x^2 + y^2 - 6x + 2y = 39$', r'$(x - 3)^2 + (y + 1)^2 = 49$. The radius is $7$')
same('R3 A', circle(*std(1, 6, 49))[1], 49);                         same('R3 A circ', 2 * pi * 7, 14 * pi); need('R3 A', RULES, r'the area is $49\pi$. The radius is $7$, so the circumference is $14\pi$')
same('R3 B', circle(x**2 + y**2 + 10*y, 119), ((0, -5), 144));      same('R3 B circ', 2 * pi * sqrt(144), 24 * pi); need('R3 B', RULES, r'$x^2 + (y + 5)^2 = 144$. The area is $144\pi$, and the circumference is $2\pi(12) = 24\pi$')
same('R3 C', circle((x + 2)**2 + y**2, 20)[1], 20);                  same('R3 C circ', 2 * pi * sqrt(20), 4 * sqrt(5) * pi); need('R3 C', RULES, r'$\sqrt{20} = 2\sqrt{5}$, so the circumference is $4\sqrt{5}\,\pi$')
same('R3 backward', (sqrt(49), 14 * pi / (2 * pi)), (7, 7))
same('R4 A', (5 - 2)**2 + (3 + 1)**2, 25);                            need('R4 A', RULES, r'$r^2 = (5 - 2)^2 + (3 + 1)^2 = 9 + 16 = 25$, and the equation is $(x - 2)^2 + (y + 1)^2 = 25$')
same('R4 B mid', (R(0 + 6, 2), R(1 + 5, 2)), (3, 3));                same('R4 B r2', (6 - 3)**2 + (5 - 3)**2, 13); need('R4 B', RULES, r'$(3, 3)$. From the center to $(6, 5)$: $r^2 = 3^2 + 2^2 = 13$. The equation is $(x - 3)^2 + (y - 3)^2 = 13$')
same('R4 C inside', (5 - 2)**2 + (2 + 1)**2, 18);                     same('R4 C on', (6 - 2)**2 + (2 + 1)**2, 25); need('R4 C', RULES, r'9 + 9 = 18$, which is less than $25$', r'$16 + 9 = 25$')
same('R5 A', circle(*std(4, 3, 3**2)), ((4, 3), 9));                 need('R5 A', RULES, r'$r = 3$ and the equation is $(x - 4)^2 + (y - 3)^2 = 9$. The circle touches the axis at $(4, 0)$')
same('R5 B', (11 - 4, 4), (7, 4));                                    need('R5 B', RULES, r'$B$ is the point $(11, 4)$', r'at $(7, 4)$, so $k = 7$')
same('R5 C', tuple(sorted(solve(Eq((x - 6)**2 + (0 - 4)**2, 25), x))), (3, 9)); need('R5 C', RULES, r'$(x - 6)^2 = 9$ and $x = 3$ or $x = 9$')
same('R6 A', (R(1 + 11, 2), R(11 - 1, 2), 3 + 9), (6, 5, 12));      same('R6 A heights', (3 - 6)**2, (9 - 6)**2); need('R6 A', RULES, r'The center is $(6, 0)$ and the radius is $5$', r'add to $12$, such as $3$ and $9$')
same('R6 B', (-1 - 6, -1 + 6), (-7, 5));                              need('R6 B', RULES, r'at $(-1, 0)$, and $r = 6$. The endpoints are $(-7, 0)$ and $(5, 0)$')
same('R6 C', (9 + 5, 9 - 5), (14, 4));                                need('R6 C', RULES, r'$9 + 5 = 14$ and the least is $9 - 5 = 4$')
# the common mistakes quote the rules' own numbers
same('M1', circle((x + 3)**2 + (y - 8)**2, 4)[0], (-3, 8));          need('M1', RULES, r'has center $(-3, 8)$, not $(3, -8)$')
same('M4', 12 + 9 + 4, 25);                                           need('M4', RULES, r'$12 + 9 + 4 = 25$')
same('M7', abs(-4), 4);                                               need('M7', RULES, r'center $(5, -4)$ that is tangent to the $x$-axis has radius $4$')

# ------------------------------------------------------------------ worked steps and quick checks
s = STEPS
same('S1', circle((x + 4)**2 + (y - 7)**2, 81), ((-4, 7), 81));     need('S1', s[0]['sol'], r'The center is $(-4, 7)$', r'$r = 9$', r'$(5, 7)$')
same('S1 check', (5 + 4)**2 + (7 - 7)**2, 81)
c0, r0 = circle((x - 6)**2 + (y + 1)**2, 64);                         typed('S1 micro', s[0]['micro'], sqrt(r0)); same('S1 micro center', c0, (6, -1))
c0, r0 = circle(x**2 + y**2 + 4*x - 10*y, 20);                        same('S2', (c0, r0), ((-2, 5), 49)); need('S2', s[1]['sol'], r'$(x + 2)^2 + (y - 5)^2 = 20 + 4 + 25 = 49$', r'$r = \sqrt{49} = 7$')
same('S2 check', 5**2 + 5**2 + 4*5 - 10*5, 20);                       need('S2', s[1]['sol'], r'$25 + 25 + 20 - 50 = 20$')
c0, r0 = circle(x**2 + y**2 - 8*x, 9);                                typed('S2 micro', s[1]['micro'], sqrt(r0)); same('S2 micro', (c0, r0), ((4, 0), 25))
c0, r0 = circle(x**2 - 6*x + y**2 + 8*y, 75);                         same('S3', (c0, r0), ((3, -4), 100)); need('S3', s[2]['sol'], r'$(x - 3)^2 + (y + 4)^2 = 100$', r'$\pi r^2 = 100\pi$')
c0, r0 = circle(x**2 + y**2 + 2*y, 35);                               same('S3 micro', (c0, r0), ((0, -1), 36))
one_right('S3 micro', s[2]['micro']['opts'], s[2]['micro']['correct'], lambda o: pis(o) == 2 * sqrt(r0))
r2 = (3 - (-3))**2 + (10 - 2)**2;                                     same('S4', r2, 100); need('S4', s[3]['sol'], r'36 + 64 = 100$', r'$(x + 3)^2 + (y - 2)^2 = 100$'); same('S4 check', ((x + 3)**2 + (y - 2)**2).subs({x: 3, y: 10}), 100)
mid = (R(2 + 10, 2), R(5 + 11, 2));                                   same('S4 micro mid', mid, (6, 8)); typed('S4 micro', s[3]['micro'], sqrt((10 - mid[0])**2 + (11 - mid[1])**2))
same('S5', (13 - 5, 5, 13 - 2 * 5), (8, 5, 3));                       need('S5', s[4]['prob'], r'$(13, 5)$'); need('S5', s[4]['sol'], r'$(8, 5)$', r'$k = 8$', r'at $(3, 5)$, and $AB = 13 - 3 = 10 = 2r$')
typed('S5 micro', s[4]['micro'], abs(-6))
same('S6', (6 - 10, 6 + 10), (-4, 16));                               need('S6', s[5]['prob'], r'$P(6, 10)$'); need('S6', s[5]['sol'], r'$(-4, 0)$', r'$(16, 0)$')
typed('S6 micro', s[5]['micro'], 2 * R(-5 + 9, 2) - (-1))
ok('every multiple-choice quick check and drill is flagged mc', all(bool(st['micro'].get('mc')) == ('opts' in st['micro']) for st in STEPS) and all(bool(it.get('mc')) == ('opts' in it) for sec in FL for it in sec['items']))
ok('last starred step', B.LAST_STARRED_STEP_INDEX == max(i for i, st in enumerate(STEPS) if st['ess']) and [st['ess'] for st in STEPS] == [True] * 4 + [False] * 2)

# ------------------------------------------------------------------ Skill Practice
A_, B_, C_, D_, E_ = [sec['items'] for sec in FL]
typed('A1', A_[0], sqrt(circle((x - 5)**2 + (y - 2)**2, 16)[1]))
typed('A2', A_[1], circle((x + 7)**2 + (y - 3)**2, 1)[0][0])
typed('A3', A_[2], circle(x**2 + (y + 9)**2, 121)[0][1])
typed('A4', A_[3], 2 * sqrt(circle((x - 4)**2 + (y + 6)**2, 400)[1]))
typed('A5', A_[4], 3**2)
typed('B1', B_[0], R(12, 2)**2);                                      same('B1 square', expand((x + 6)**2), x**2 + 12*x + 36)
typed('B2', B_[1], R(-5, 2)**2);                                      same('B2 square', expand((y - R(5, 2))**2), y**2 - 5*y + R(25, 4))
typed('B3', B_[2], sqrt(circle(x**2 + y**2 - 2*x - 6*y, 26)[1]));    same('B3 form', circle(x**2 + y**2 - 2*x - 6*y, 26), ((1, 3), 36))
typed('B4', B_[3], sqrt(circle(x**2 + y**2 + 18*x, 19)[1]));          same('B4 form', circle(x**2 + y**2 + 18*x, 19), ((-9, 0), 100))
typed('B5', B_[4], sqrt(circle(3*x**2 + 3*y**2 - 12*y, 36)[1]));      same('B5 form', circle(3*x**2 + 3*y**2 - 12*y, 36), ((0, 2), 16))
typed('C1', C_[0], circle((x - 2)**2 + (y - 2)**2, 64)[1])
typed('C2', C_[1], 2 * sqrt(circle((x + 1)**2 + y**2, 81)[1]))
typed('C3', C_[2], circle(x**2 + y**2, 30)[1])
typed('C4', C_[3], 2 * sqrt(circle(x**2 + y**2 - 14*x, 0)[1]));       same('C4 form', circle(x**2 + y**2 - 14*x, 0), ((7, 0), 49))
typed('C5', C_[4], 196)
typed('D1', D_[0], (-2)**2 + 7**2)
typed('D2', D_[1], sqrt((7 - 1)**2 + (12 - 4)**2))
typed('D3', D_[2], R(-7 + 3, 2))
typed('D4', D_[3], sqrt((8 - R(2 + 8, 2))**2 + (9 - R(1 + 9, 2))**2))
d5 = (5 - 3)**2 + (4 - 1)**2
same('D5 value', d5, 13)
one_right('D5', D_[4]['opts'], D_[4]['correct'], lambda o: {'inside the circle': d5 < 20, 'on the circle': d5 == 20, 'outside the circle': d5 > 20}[o])
typed('E1', E_[0], abs(-3))
typed('E2', E_[1], abs(-8))
typed('E3', E_[2], 7 + sqrt(16))
typed('E4', E_[3], 2 * (-2) - 3);                                     ok('E4 point exists', 49 - (3 + 2)**2 > 0)
typed('E5', E_[4], R(14 - 2, 2))
ok('Skill Practice count', sum(len(sec['items']) for sec in FL) == 25)

# ------------------------------------------------------------------ SAT-Style Practice
c0, r0 = circle((x - 9)**2 + (y + 4)**2, 36);                         one_right('P1', G[0]['options'], G[0]['correct'], lambda o: tup(o) == c0)
c0, r0 = circle((x + 2)**2 + (y - 11)**2, 169);                       typed('P2', G[1], 2 * sqrt(r0))
one_right('P3', G[2]['options'], G[2]['correct'], lambda o: eqn(o) == (5, -7, 4**2));  same('P3 check', ((x - 5)**2 + (y + 7)**2).subs({x: 9, y: -7}), 16)
c0, r0 = circle(x**2 + 2*x + y**2 - 12*y, 12);                        same('P4 form', (c0, r0), ((-1, 6), 49)); one_right('P4', G[3]['options'], G[3]['correct'], lambda o: pis(o) == r0)
same('P4 distractor C is the circumference', 2 * sqrt(r0), pis(G[3]['options'][2]))
c0, r0 = circle(x**2 + y**2 - 16*y, 36);                              same('P5 form', (c0, r0), ((0, 8), 100)); typed('P5', G[4], 2 * sqrt(r0)); same('P5 check', 0 + 18**2 - 16 * 18, 36)
r2 = (6 - 2)**2 + (4 - 1)**2;                                         same('P6 r2', r2, 25); one_right('P6', G[5]['options'], G[5]['correct'], lambda o: eqn(o) == (2, 1, r2))
mid = (R(-1 + 3, 2), R(-4 + 8, 2)); r2 = (3 - mid[0])**2 + (8 - mid[1])**2
same('P7', (mid, r2), ((1, 2), 40));                                  one_right('P7', G[6]['options'], G[6]['correct'], lambda o: eqn(o) == (1, 2, 40)); same('P7 distractor B', (3 + 1)**2 + (8 + 4)**2, 160)
typed('P8', G[7], 17 - 7);                                            need('P8', G[7]['stem'], r'$(17, 7)$'); need('P8', G[7]['sol'], r'$(10, 7)$', r'$A$ is $(3, 7)$, and $AB = 17 - 3 = 14 = 2r$')
cx, rr = R(-6 + 14, 2), R(14 + 6, 2)
def p9(o):
    a, b = [int(v) for v in re.fullmatch(r'\$(-?\d+)\$ and \$(-?\d+)\$', o).groups()]
    return a + b == 2 * cx and abs(a - cx) < rr and abs(b - cx) < rr
one_right('P9', G[8]['options'], G[8]['correct'], p9);                need('P9', G[8]['sol'], r'$-2 + 9 = 7$, $0 + 9 = 9$, $1 + 7 = 8$, $3 + 6 = 9$')
c0, r0 = circle(2*x**2 + 2*y**2 + 12*x - 20*y, 94);                   same('P10 form', (c0, r0), ((-3, 5), 81)); typed('P10', G[9], sqrt(r0)); same('P10 check', 2*36 + 2*25 + 12*6 - 20*5, 94)
ok('practice: ten items, both formats', len(G) == 10 and {g['type'] for g in G} == {'mc', 'ne'})
ok('practice: starred chips', [g['ess'] for g in G] == [True] * 7 + [False, False, True])

# ------------------------------------------------------------------ Challenge
cc = symbols('c')
typed('Ch1', C[0], solve(Eq(cc + 16 + 9, 7**2), cc)[0])
typed('Ch1 x1', C[0]['extras'][0], solve(Eq(cc + 25, 8**2), cc)[0])
typed('Ch1 x2', C[0]['extras'][1], solve(Eq(cc + 4 + 36, 9**2), cc)[0])
typed('Ch1 x3', C[0]['extras'][2], solve(Eq(cc + 1 + 1, 20), cc)[0])
a = symbols('a')
typed('Ch2', C[1], max(solve(Eq((a - 3)**2 + (5 + 1)**2, 100), a)));  same('Ch2 roots', tuple(sorted(solve(Eq((a - 3)**2 + 36, 100), a))), (-5, 11))
typed('Ch2 x1', C[1]['extras'][0], max(solve(Eq(16 + a**2, 41), a)))
typed('Ch2 x2', C[1]['extras'][1], max(solve(Eq((a + 1)**2 + (-2 - 4)**2, 45), a)));  same('Ch2 x2 roots', tuple(sorted(solve(Eq((a + 1)**2 + 36, 45), a))), (-4, 2))
typed('Ch2 x3', C[1]['extras'][2], min(solve(Eq((7 - 2)**2 + (a - 3)**2, 169), a)));  same('Ch2 x3 roots', tuple(sorted(solve(Eq(25 + (a - 3)**2, 169), a))), (-9, 15))
one_right('Ch3', C[2]['options'], C[2]['correct'], lambda o: (tup(o)[0] + 2)**2 + (tup(o)[1] - 3)**2 < 25)
same('Ch3 values', tuple((tup(o)[0] + 2)**2 + (tup(o)[1] - 3)**2 for o in C[2]['options']), (25, 25, 20, 36))
d2 = (8 + 4)**2 + (6 - 1)**2;                                         same('Ch4 diameter', sqrt(d2), 13); typed('Ch4', C[3], R(d2, 4)); same('Ch4 check', 6**2 + R(5, 2)**2, R(169, 4))
ex = expand((x - 5)**2 + (y + 4)**2 - 4**2);                          same('Ch5 expanded', ex, x**2 + y**2 - 10*x + 8*y + 25); typed('Ch5', C[4], Poly(ex, x, y).coeff_monomial(1))
same('Ch5 distractor', Poly(expand((x - 5)**2 + (y + 4)**2 - 5**2), x, y).coeff_monomial(1), 16)
t = symbols('t')
typed('Ch6', C[5], max(solve(Eq((t - 1)**2 + 5**2, 13**2), t)));      same('Ch6 roots', tuple(sorted(solve(Eq((t - 1)**2 + 25, 169), t))), (-11, 13))
sol7 = solve([Eq(y, x + 1), Eq(x**2 + y**2, 25)], [x, y])
same('Ch7 points', tuple(sorted(sol7)), ((-4, -3), (3, 4)));          typed('Ch7', C[6], [p for p in sol7 if p[0] > 0 and p[1] > 0][0][0])
ok('challenge: seven items, hardest last', len(C) == 7 and C[0]['diff'] == 'Medium-hard' and C[-1]['diff'].startswith('Hard'))

# ------------------------------------------------------------------ Exit ticket
one_right('X1', EX[0]['opts'], EX[0]['correct'], lambda o: int(o.strip('$')) == sqrt(circle((x + 5)**2 + (y - 12)**2, 9)[1]))
c0, r0 = circle(x**2 + y**2 - 4*x + 14*y, 3);                         same('X2 form', (c0, r0), ((2, -7), 56)); one_right('X2', EX[1]['opts'], EX[1]['correct'], lambda o: tup(o) == c0)
r2 = (9 - 1)**2 + (13 + 2)**2;                                        same('X3 r2', r2, 289); one_right('X3', EX[2]['opts'], EX[2]['correct'], lambda o: pis(o) == r2); same('X3 circumference', 2 * sqrt(r2), 34)

# ------------------------------------------------------------------ figures
used = set(re.findall(r'data-fig="([^"]+)"', RULES)) | {q['fig'] for q in STEPS + G + C if q.get('fig')}
ok('every figure is used and every reference exists', used == set(FIGS))
for name, f in FIGS.items():
    sx, sy = (f['w'] - 44) / (f['xmax'] - f['xmin']), (f['h'] - 44) / (f['ymax'] - f['ymin'])
    ok('%s: equal scales (%.3f, %.3f)' % (name, sx, sy), abs(sx - sy) < 0.03 * sx)
    ok('%s: has alt text' % name, len(f.get('alt', '')) > 20)
    for c_ in f['circles']:
        top = c_['y'] + c_['r']
        ok('%s: circle inside the plot box' % name, f['xmin'] < c_['x'] - c_['r'] and c_['x'] + c_['r'] < f['xmax'] and top < f['ymax'] and (c_.get('half') or f['ymin'] < c_['y'] - c_['r']))
def circ(name): return FIGS[name]['circles'][0]
def on(name, px, py):
    c_ = circ(name); return abs((px - c_['x'])**2 + (py - c_['y'])**2 - c_['r']**2) < 1e-3
ok('r_standard: (7, 5) on the circle', on('r_standard', 7, 5))
ok('r_diam: both ends on the circle', on('r_diam', 0, 1) and on('r_diam', 6, 5) and (circ('r_diam')['x'], circ('r_diam')['y']) == (3, 3))
ok('r_tanx touches the x-axis', circ('r_tanx')['y'] == circ('r_tanx')['r'] == 3 and circ('r_tanx')['x'] == 4)
ok('r_tany touches the y-axis', circ('r_tany')['x'] == circ('r_tany')['r'] == 3 and circ('r_tany')['y'] == 4)
ok('r_semi', on('r_semi', 1, 0) and on('r_semi', 11, 0) and on('r_semi', 3, 4) and on('r_semi', 9, 4) and on('r_semi', 6, 5))
ok('s5', on('s5', 13, 5) and on('s5', 3, 5) and on('s5', 8, 0) and circ('s5')['y'] == circ('s5')['r'])
ok('s6', on('s6', 6, 10) and on('s6', -4, 0) and circ('s6').get('half') is True)
ok('p6', on('p6', 6, 4) and (circ('p6')['x'], circ('p6')['y']) == (2, 1))
ok('p8', on('p8', 17, 7) and on('p8', 3, 7) and on('p8', 10, 0) and circ('p8')['y'] == circ('p8')['r'])
ok('p9', on('p9', -6, 0) and on('p9', 14, 0) and circ('p9').get('half') is True)
ok('c6', on('c6', 1, 13) and on('c6', 13, 5) and circ('c6').get('half') is True)
for name in ('s5', 's6', 'p8', 'p9', 'c6'):
    ok('%s has no grid (the answer cannot be read off it)' % name, 'grid' not in FIGS[name])

if FAIL:
    print('FAILED %d of %d checks:' % (len(FAIL), N[0]))
    for f in FAIL:
        print('  -', f)
    sys.exit(1)
print('verify_circles: %d checks passed' % N[0])
