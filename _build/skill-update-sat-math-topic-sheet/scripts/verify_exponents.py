#!/usr/bin/env python3
"""Answer-key recomputations for SAT Math 7: Exponents and Exponential Models (needs sympy).
Run: python3 verify_exponents.py   -> prints the number of checks; exits non-zero on any failure.

Every answer in the sheet is recomputed here from the question itself, then compared with what
build_exponents.py stores: the accepted grid-in forms, the index of the correct choice, and the
choice strings (so the two files cannot drift apart without this script noticing). Each
multiple-choice item is also checked to have one correct choice and three that are not."""
import os, sys
from fractions import Fraction as F
from sympy import symbols, Rational as R, sqrt, root, simplify, solve, Eq, Integer, powsimp, expand, factorint, nsimplify

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_exponents as B

n_checks = 0
def ok(cond, what):
    global n_checks
    n_checks += 1
    assert bool(cond), 'FAILED: ' + what

x, y, t, n, k, a, b, p, q, m = symbols('x y t n k a b p q m', positive=True)
def same(e1, e2): return simplify(e1 - e2) == 0

def val(s):
    """A typed answer as an exact fraction: '1/9', '.111', '6400.00'."""
    s = s.strip()
    if '/' in s:
        u, v = s.split('/'); return F(u) / F(v)
    return F(s if not s.startswith('.') else '0' + s)

def grid(item, true, what):
    """First accepted form is exact; every other form is exact or a 3-or-more-place truncation or rounding."""
    acc = item['accept']; true = F(str(true)) if not isinstance(true, F) else true
    ok(val(acc[0]) == true, what + ': first accepted form ' + acc[0])
    for s in acc[1:]:
        ok(abs(val(s) - true) < F(11, 10000) and ('.' in s or val(s) == true), what + ': accepted form ' + s)

def mc(item, values, true, strings, what, key='opts'):
    """`values` are the four choices as sympy objects (or numbers); exactly one equals `true`."""
    ok(item[key] == strings, what + ': choice strings match the builder')
    hits = [i for i, v in enumerate(values) if simplify(v - true) == 0]
    ok(len(hits) == 1, what + ': one correct choice (found %d)' % len(hits))
    ok(item['correct'] == hits[0], what + ': the builder marks choice %d' % hits[0])

def mc_test(item, flags, strings, what, key='opts'):
    """For choices that are models: `flags` says which choices pass the test; one should."""
    ok(item[key] == strings, what + ': choice strings match the builder')
    ok(flags.count(True) == 1, what + ': one correct choice')
    ok(item['correct'] == flags.index(True), what + ': the builder marks choice %d' % flags.index(True))

# ---------------- RULES (examples, formula rows, notes, common mistakes)
ok(same(x**7 * x**5, x**12) and same((3*x**4)**2, 9*x**8) and same(12*x**9 / (4*x**3), 3*x**6), 'R1 examples')
ok(same(x**2 * x**3, x**5) and same((x**2)**3, x**6) and not same((a + b)**2, a**2 + b**2), 'R1 why and note')
ok(R(4)**-2 == R(1, 16) and same(x**3 * y**-2 / x**-1, x**4 / y**2) and R(2, 5)**-2 == R(25, 4), 'R2 examples')
ok([R(2)**e for e in (3, 2, 1, 0, -1, -2)] == [8, 4, 2, 1, R(1, 2), R(1, 4)] and (-2)**4 == 16 and (-2)**3 == -8 and -2**4 == -16, 'R2 rows')
ok(same(x**3 / x**-1, x**4), 'R2 note')
ok(Integer(27)**R(2, 3) == 9 and root(27, 3) == 3 and same(root(x**3, 4), x**R(3, 4)) and same(sqrt(x**5), x**R(5, 2)), 'R3 A, B')
ok(same((x**6 * y**10)**R(1, 2), x**3 * y**5) and Integer(16)**R(-3, 4) == R(1, 8) and Integer(16)**R(3, 4) == 8, 'R3 C, D')
ok([2**e for e in (2, 3, 4, 5, 6)] == [4, 8, 16, 32, 64] and [3**2, 3**3, 3**4, 5**2, 5**3] == [9, 27, 81, 25, 125], 'R4 powers')
ok(solve(Eq(2*x, 12), x) == [6] and 9**6 == 27**4 and 3 * 3**5 == 3**6 and 5 * 5**4 == 5**5, 'R4 A, B, row')
ok(R(3)**-4 == R(9)**-2 and solve(Eq(p**-2, R(3)**-4), p) == [9] and 2**3 * 2**3 == 2**6 and 2**3 + 2**3 == 2**4, 'R4 C, note')
ok(F('1.03')**2 == F('1.0609') and 800 * F('1.0609') == F('848.72') and 1 - F('0.12') == F('0.88'), 'R5 A, B, C')
ok(F('0.6') / 100 == F('0.006') and 1 + F('0.006') == F('1.006') and 1 - F('0.006') == F('0.994') and F(4, 100) == F('0.04') and F('0.4') / 100 == F('0.004'), 'R5 rows, note')
ok([(F(s) - 1) * 100 for s in ('1.03', '1.3', '1.003')] == [3, 30, F('0.3')] and (1 - F('0.97')) * 100 == 3, 'R6 factor to rate')
ok((F('1.035') - 1) * 100 == F('3.5') and 1 - F('0.91') == F('0.09'), 'R6 A, B')
ok([80 * F(3, 2)**i for i in range(4)] == [80, 120, 180, 270] and F(120, 80) == F(180, 120) == F(270, 180) == F(3, 2), 'R6 C table')
ok(50 * 2**(12 // 4) == 400 and 12 % 4 == 0, 'R6 D')
ok([200 * F(3, 2)**i for i in range(3)] == [200, 300, 450], 'R6 figure points')
ok(100 + 50 * 0 == 100 * F(3, 2)**0 == 100 and 100 * 1.5**5 > 100 + 50 * 5, 'R6 linear and exponential figure')
ok(F(150 * 30 - 600, 30) == 130 and 310 - 130 == 180, 'R7 A')
ok(F(4**2 - (-1)**2, 4 - (-1)) == 3, 'R7 B')
ok(F(100 * 2**3 - 100 * 2**1, 3 - 1) == 300 and F(100 * 2**5 - 100 * 2**3, 2) == 1200 and 100 * 2**5 == 3200, 'R7 C')
ok(same(x**3 * x**4, x**7) and same((x**3)**4, x**12) and same((2*x**3)**4, 16*x**12) and R(5)**-2 == R(1, 25), 'mistakes 1 to 3')
ok(2**5 + 2**5 == 2**6 and Integer(8)**R(2, 3) == 4 and abs(float(sqrt(8**3)) - 22.6) < 0.05, 'mistakes 4, 5')
ok(1 + F('0.04') == F('1.04') and 1 - F('0.04') == F('0.96') and F('0.2') / 100 == F('0.002') and 1 - F('0.002') == F('0.998') and (1 - F('0.98')) * 100 == 2, 'mistakes 6, 7')
ok((1 - F('0.82')) * 100 == 18 and F('0.9')**3 == F('0.729') and (1 - F('0.729')) * 100 == F('27.1'), 'mistakes 8, 9')

# ---------------- STEPS
S = B.STEPS
ok(same((2*x**3)**4 * x**5 / (8*x**9), 2*x**8) and same((2*x**3)**4, 16*x**12) and F(16**4 * 32, 8 * 512) == 512 == 2 * 2**8, 'S1')
grid(S[0]['micro'], 7, 'S1 micro'); ok(same((x**4)**3 / x**5, x**7), 'S1 micro value')
r = solve(Eq(6*m**4*n**-2, 54*m**2*n**2), m); ok(len(r) == 1 and same(r[0], 3*n**2), 'S2')
ok(6 * 12**4 * F(1, 4) == 31104 == 54 * 144 * 4, 'S2 check')
grid(S[1]['micro'], F(1, 7), 'S2 micro'); ok(solve(Eq(k**-2, 49), k) == [R(1, 7)], 'S2 micro value')
ok(factorint(392) == {2: 3, 7: 2} and same((a**4*b**6)**R(1, 2), a**2*b**3), 'S3 setup')
sols = [(i, j) for i in range(1, 400) for j in range(1, 400) if i**2 * j**3 == 392]; ok(sols == [(7, 2)] and 7 + 2 == 9, 'S3 the only positive integers')
ok(7**4 * 2**6 == 153664 == 392**2 and 7**4 == 2401, 'S3 check')
grid(S[2]['micro'], 27, 'S3 micro'); ok(Integer(81)**R(3, 4) == 27, 'S3 micro value')
ok(((-3)**3 * 9**2)**2 == 3**14 == 9**7 == 4782969 and (-3)**3 * 9**2 == -(3**7) == -2187 and 27 * 81 == 2187, 'S4')
ok(solve(Eq(2*x, 14), x) == [7], 'S4 exponent'); grid(S[3]['micro'], 5, 'S4 micro'); ok(3 * 9**2 == 3**5, 'S4 micro value')
ok(6400 * F(3, 4)**3 == 2700 and F(3, 4)**3 == F('0.421875') and [6400 * F(3, 4)**i for i in range(4)] == [6400, 4800, 3600, 2700], 'S5')
ok(6400 - 3 * 1600 == 1600 and [6400 - 4800, 4800 - 3600, 3600 - 2700] == [1600, 1200, 900], 'S5 common mistake')
grid(S[4]['micro'], F('1.035'), 'S5 micro'); ok(1 + F('3.5') / 100 == F('1.035'), 'S5 micro value')
ok(5200 * F('0.96') == 4992 and 5200 - 4992 == 208 and F(208, 5200) == F('0.04') and (1 - F('0.96')) * 100 == 4, 'S6')
grid(S[5]['micro'], F('0.8'), 'S6 micro'); ok((F('1.008') - 1) * 100 == F('0.8'), 'S6 micro value')
ok(F(120 * 40 - 360, 40) == 111 and 4800 - 360 == 4440 and 136 - 111 == 25, 'S7')
grid(S[6]['micro'], 4, 'S7 micro'); ok(F((5**2 + 1) - ((-1)**2 + 1), 5 - (-1)) == 4 and 5**2 + 1 == 26, 'S7 micro value')
ok(len(S) == 7 and [s['ess'] for s in S] == [True] * 6 + [False] and B.LAST_STARRED_STEP_INDEX == 5, 'steps: stars')

# ---------------- SKILL PRACTICE
FL = {s['sec'][0]: s['items'] for s in B.FLUENCY}
A, Bs, C, D, E = FL['A'], FL['B'], FL['C'], FL['D'], FL['E']
ok([len(v) for v in (A, Bs, C, D, E)] == [5, 7, 5, 7, 3], 'skill practice counts')
grid(A[0], 9, 'A1'); ok(same(x**6 * x**3, x**9), 'A1 value')
grid(A[1], 20, 'A2'); ok(same((x**5)**4, x**20), 'A2 value')
grid(A[2], 7, 'A3'); ok(same(x**11 / x**4, x**7), 'A3 value')
mc(A[3], [3*x**5, 3*x**6, 9*x**6, 27*x**6], (3*x**2)**3, ["$3x^5$", "$3x^6$", "$9x^6$", "$27x^6$"], 'A4')
grid(A[4], 5, 'A5'); ok(same((x**3)**2 * x**4 / x**5, x**5), 'A5 value')
grid(Bs[0], F(1, 8), 'B1'); ok(R(2)**-3 == R(1, 8), 'B1 value')
grid(Bs[1], 9, 'B2'); ok(R(1, 3)**-2 == 9, 'B2 value')
grid(Bs[2], 8, 'B3'); ok(7**0 + 7**1 == 8, 'B3 value')
mc(Bs[3], [-x**4, x**-4, x**4, 1/x**4], 1 / x**-4, ["$-x^4$", "$x^{-4}$", "$x^4$", r"$\dfrac{1}{x^4}$"], 'B4')
grid(Bs[4], 7, 'B5'); ok(sqrt(49) == 7, 'B5 value')
grid(Bs[5], 16, 'B6'); ok(Integer(8)**R(4, 3) == 16, 'B6 value')
mc(Bs[6], [x**R(3, 5), x**R(5, 3), x**15, x**2], root(x**5, 3), [r"$x^{\frac{3}{5}}$", r"$x^{\frac{5}{3}}$", "$x^{15}$", "$x^2$"], 'B7')
grid(C[0], 10, 'C1'); ok(4**5 == 2**10, 'C1 value')
grid(C[1], 4, 'C2'); ok(27**4 == 3**12, 'C2 value')
grid(C[2], 8, 'C3'); ok(2**7 + 2**7 == 2**8, 'C3 value')
grid(C[3], 5, 'C4'); ok(6 * 6**4 == 6**5, 'C4 value')
grid(C[4], 25, 'C5'); ok(25**3 == 5**6, 'C5 value')
grid(D[0], F('1.06'), 'D1'); grid(D[1], F('0.7'), 'D2'); grid(D[2], F('1.009'), 'D3')
ok(1 + F(6, 100) == F('1.06') and 1 - F(30, 100) == F('0.7') and 1 + F('0.9') / 100 == F('1.009'), 'D1 to D3 values')
grid(D[3], 25, 'D4'); grid(D[4], F('1.5'), 'D5'); grid(D[5], 75, 'D6')
ok((F('1.25') - 1) * 100 == 25 and (1 - F('0.985')) * 100 == F('1.5') and 75 * 3**0 == 75, 'D4 to D6 values')
mc(D[6], [2, 50, 100, 200], (2 - 1) * 100, [r"$2\%$", r"$50\%$", r"$100\%$", r"$200\%$"], 'D7')
grid(E[0], 8, 'E1'); ok(20 - F(60, 5) == 8, 'E1 value')
grid(E[1], 8, 'E2'); ok(F(6**2 - 2**2, 6 - 2) == 8, 'E2 value')
grid(E[2], 4, 'E3'); ok(F(3**2 - 3**0, 2 - 0) == 4, 'E3 value')

# ---------------- SAT-STYLE PRACTICE
G = B.GAUNTLET
ok(len(G) == 10 and [g['diff'] for g in G] == ['Easy'] * 3 + ['Medium'] * 5 + ['Medium-hard'] * 2, 'practice: ten items, difficulty order')
ok([g['ess'] for g in G] == [True] * 7 + [False] + [True] * 2, 'practice: stars')
mc(G[0], [7*x**7, 7*x**12, 10*x**7, 10*x**12], (2*x**3) * (5*x**4), ["$7x^7$", "$7x^{12}$", "$10x^7$", "$10x^{12}$"], 'P1', 'options')
ok(16 * 80 == 1280 == 10 * 2**7, 'P1 check')
grid(G[1], 5, 'P2'); ok(8**5 == 2**15 == 32768, 'P2 value')
models = [750 * R('4.5')**t, 750 * R('1.045')**t, 750 * R('1.45')**t, 750 + R('1.045')**t]
mc_test(G[2], [all(mdl.subs(t, i) == 750 * (1 + R('4.5') / 100)**i for i in range(4)) for mdl in models],
        [r"$S = 750(4.5)^t$", r"$S = 750(1.045)^t$", r"$S = 750(1.45)^t$", r"$S = 750 + (1.045)^t$"], 'P3', 'options')
ok(750 * F('1.045') == F('783.75') and 750 * F('0.045') == F('33.75') and (F('1.45') - 1) * 100 == 45, 'P3 check')
grid(G[3], F('0.982'), 'P4'); ok(1 - F('1.8') / 100 == F('0.982') and 640 * F('0.982') == F('628.48') and 640 - F('628.48') == F('11.52') and F('11.52') / 640 == F('0.018'), 'P4 value')
grid(G[4], F(1, 9), 'P5'); ok(solve(Eq(k**-2 * 3**2, 3**6), k) == [R(1, 9)] and 81 * 9 == 729 == 3**6, 'P5 value')
mc(G[5], [x**R(1, 3), x**R(3, 5), x**R(6, 7), x**R(7, 6)], root(x**2, 3) * sqrt(x), [r"$x^{\frac{1}{3}}$", r"$x^{\frac{3}{5}}$", r"$x^{\frac{6}{7}}$", r"$x^{\frac{7}{6}}$"], 'P6', 'options')
ok(root(64**2, 3) == 16 and sqrt(64) == 8 and Integer(64)**R(7, 6) == 128 == 2**7 and R(2, 3) + R(1, 2) == R(7, 6) and R(2, 3) * R(1, 2) == R(1, 3), 'P6 check')
tab = [(0, F(96)), (1, F(72)), (2, F(54)), (3, F('40.5'))]
fns = [lambda i: 96 * F(1, 4)**i, lambda i: 96 * F(3, 4)**i, lambda i: 72 * F(3, 4)**i, lambda i: 96 - 24 * i]
mc_test(G[6], [all(f(i) == v for i, v in tab) for f in fns],
        [r"$f(x) = 96(0.25)^x$", r"$f(x) = 96(0.75)^x$", r"$f(x) = 72(0.75)^x$", r"$f(x) = 96 - 24x$"], 'P7', 'options')
ok("<td>$96$</td><td>$72$</td><td>$54$</td><td>$40.5$</td>" in G[6]['stem'] and 96 - 24 * 2 == 48 and G[6]['desmos'] == ["(0,96)", "(1,72)", "(2,54)", "(3,40.5)"], 'P7 table and points')
grid(G[7], 79, 'P8'); ok(F(180 * 60 - 540, 60) == 171 and 250 - 171 == 79 and 10800 - 540 == 10260, 'P8 value')
grid(G[8], F(3, 2), 'P9'); ok(solve(Eq(20 * b**2, 45), b) == [R(3, 2)] and F(45, 20) == F('2.25') and 20 * F(3, 2)**2 == 45, 'P9 value')
grid(G[9], 3, 'P10'); ok(solve(Eq((a**-5 * a**3)**-2, 81), a) == [3] and 3**3 == 27 and 3**5 == 243 and F(27, 243) == F(1, 9) and F(1, 9)**-2 == 81, 'P10 value')
ok('a^{-5}b' in G[9]['stem'] and 'b = a^3' in G[9]['stem'], 'P10 stem matches the recomputation')

# ---------------- CHALLENGE
Cq = B.CHALLENGE
ok(len(Cq) == 7 and [c['ess'] for c in Cq] == [True] * 6 + [False] and [c['diff'] for c in Cq] == ['Medium-hard'] * 4 + ['Hard'] * 3, 'challenge: seven items, stars, difficulty order')
grid(Cq[0], 4, 'C1'); ok(solve(Eq(p**-2, R(6)**-4), p) == [36] and solve(Eq(q**-2, 9**2), q) == [R(1, 9)] and 36 * R(1, 9) == 4 and 36**2 == 1296 == 6**4, 'C1 value')
e = Cq[0]['extras']
grid(e[0], 16, 'C1 extra 1'); ok(solve(Eq(p**-3, R(4)**-6), p) == [16], 'C1 extra 1 value')
grid(e[1], F(1, 5), 'C1 extra 2'); ok(solve(Eq(q**-2, 25), q) == [R(1, 5)], 'C1 extra 2 value')
grid(e[2], F(1, 9), 'C1 extra 3'); ok(solve(Eq(m**R(-1, 2), 3), m) == [R(1, 9)], 'C1 extra 3 value')
r = solve(Eq(5*x**6*y**-1, 80*x**4*y**5), x); ok(len(r) == 1 and same(r[0], 4*y**3), 'C2 value')
mc_test(Cq[1], [simplify((5*x**6/y - 80*x**4*y**5).subs(x, cand)) == 0 for cand in (4*y**3, 16*y**3, 4*y**6, 4/y**3)],
        [r"$x = 4y^3$", r"$x = 16y^3$", r"$x = 4y^6$", r"$x = \dfrac{4}{y^3}$"], 'C2', 'options')
ok(5 * 2**30 * F(1, 2) == 5 * 2**29 == 80 * 2**20 * 2**5 and 32 == 4 * 2**3, 'C2 check')
grid(Cq[2], 7, 'C3'); ok(factorint(500) == {2: 2, 5: 3} and same((a**9*b**6)**R(1, 3), a**3*b**2), 'C3 setup')
sols = [(i, j) for i in range(1, 600) for j in range(1, 600) if i**3 * j**2 == 500]; ok(sols == [(5, 2)], 'C3 the only positive integers')
grid(Cq[3], 5120, 'C4'); ok(12500 * (1 - F(20, 100))**4 == 5120 and F('0.8')**4 == F('0.4096') and [12500 * F(4, 5)**i for i in range(5)] == [12500, 10000, 8000, 6400, 5120] and 12500 * F(20, 100) == 2500, 'C4 value')
ok('$4$ years after' in Cq[3]['stem'] and Cq[3]['desmos'] == ['12500(1-\\frac{20}{100})^4'], 'C4 stem and calculator line match the recomputation')
e = Cq[3]['extras']
grid(e[0], 8820, 'C4 extra 1'); ok(8000 * F('1.05')**2 == 8820 and F('1.05')**2 == F('1.1025'), 'C4 extra 1 value')
grid(e[1], 125, 'C4 extra 2'); ok(2000 * F(1, 2)**4 == 125, 'C4 extra 2 value')
grid(e[2], 13310, 'C4 extra 3'); ok(10000 * F('1.1')**3 == 13310 and F('1.1')**3 == F('1.331'), 'C4 extra 3 value')
cands = [lambda u: 400 * 3.0**(5 * u), lambda u: 400 * 3.0**(u / 5), lambda u: 400 * 5.0**(u / 3), lambda u: 400 * 1.6**u]
mc_test(Cq[4], [all(abs(f(u) - v) < 1e-6 for u, v in ((0, 400), (5, 1200), (10, 3600))) for f in cands],
        [r"$P(t) = 400(3)^{5t}$", r"$P(t) = 400(3)^{\frac{t}{5}}$", r"$P(t) = 400(5)^{\frac{t}{3}}$", r"$P(t) = 400(1.6)^{t}$"], 'C5', 'options')
ok(Cq[4]['desmos'] == ["(0,400)", "(5,1200)", "(10,3600)"], 'C5 points')
grid(Cq[5], F('8.16'), 'C6'); ok((F('1.04')**2 - 1) * 100 == F('8.16') and 1500 * F('1.0816') == F('1622.40') and F('122.40') / 1500 == F('0.0816'), 'C6 value')
grid(Cq[6], 7, 'C7'); ok(solve(Eq(((25 + 5*k) - (1 + k)) / 4, 13), k) == [7] and F((25 + 35) - (1 + 7), 4) == 13, 'C7 value')

# ---------------- EXIT
X = B.EXIT
mc(X[0], [y**3 / x**5, y**7 / x, x * y**3, x**5 * y**3], x**-2 * y**5 / (x**3 * y**2), [r"$\dfrac{y^3}{x^5}$", r"$\dfrac{y^7}{x}$", r"$xy^3$", r"$x^5y^3$"], 'E1')
mc(X[1], [R('0.4'), R('0.96'), R('0.996'), R('1.004')], 1 - R('0.4') / 100, [r"$60(0.4)^t$", r"$60(0.96)^t$", r"$60(0.996)^t$", r"$60(1.004)^t$"], 'E2')
mc(X[2], [6, 8, 12, 64], Integer(16)**R(3, 4), ["$6$", "$8$", "$12$", "$64$"], 'E3')
ok(len(X) == 3, 'exit: three items')

# ---------------- every answer field is covered: counts of graded items
graded = (len(S) + sum(len(s['items']) for s in B.FLUENCY) + len(G) + len(Cq) + sum(len(c.get('extras', [])) for c in Cq) + len(X))
ok(graded == 7 + 27 + 10 + 7 + 6 + 3 == 60, 'graded items: %d' % graded)
print('verify_exponents: %d checks passed' % n_checks)
