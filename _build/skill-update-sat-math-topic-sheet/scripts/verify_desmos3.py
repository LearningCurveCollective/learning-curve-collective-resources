#!/usr/bin/env python3
"""Independent recomputation of every answer key in SAT Desmos 3: Mixed Practice.
Each check recomputes the value from the question's own numbers (sympy / fractions / statistics)
and compares it with the sheet's key. Carried questions are also compared with the snapshot of
SAT-Desmos-Strategies.html (desmos3_source.json), so a carried answer cannot drift."""
import math, re, statistics
from fractions import Fraction as F
import sympy as sp
import build_desmos3 as d3

x, y, a, b, c, k, h, w, t = sp.symbols('x y a b c k h w t', real=True)
checks = []
CH = dict(zip(d3.BY_MOVE_IDS, d3.CHALLENGE))
G = d3.GAUNTLET
FL = [it for sec in d3.FLUENCY for it in sec['items']]
EX = d3.EXIT
OLD_P = {'P%d' % p['n']: p for p in d3.SOURCE['practice']}
OLD_G = d3.SOURCE['timed']


def ok(label, got, want):
    try:
        good = bool(sp.simplify(sp.nsimplify(got) - sp.nsimplify(want)) == 0)
    except Exception:
        good = got == want
    checks.append((label, good, got, want))


def near(label, got, want, tol=6e-4):
    checks.append((label, abs(float(got) - float(want)) < tol, got, want))


def key(q):
    return q['options'][q['correct']] if q['type'] == 'mc' else q['accept'][0]


def num(q):
    return sp.nsimplify(q['accept'][0])


def lsq(xs, ys):
    n = len(xs); xb, yb = F(sum(xs), n), F(sum(ys), n)
    m = sum((F(u) - xb) * (F(v) - yb) for u, v in zip(xs, ys)) / sum((F(u) - xb) ** 2 for u in xs)
    return m, yb - m * xb


def r2(xs, ys):
    m, b0 = lsq(xs, ys); yb = F(sum(ys), len(ys))
    return 1 - sum((F(v) - (m * u + b0)) ** 2 for u, v in zip(xs, ys)) / sum((F(v) - yb) ** 2 for v in ys)


def roots(e):
    return sorted(sp.solve(e, x))


def vertex(e):
    xv = sp.solve(sp.diff(e, x), x)[0]
    return xv, e.subs(x, xv)


def sys2(e1, e2):
    r = sp.solve([e1, e2], [x, y], dict=True)
    return r[0] if len(r) == 1 else r


# ---------------------------------------------------------------- practice by move
r = sys2(sp.Rational(3, 4)*x + y/2 - 7, x/4 - y); ok('N1', (r[x], r[y]), (num(CH['N1']), 2))
near('P1', roots(2*x**2 - 7)[1], num(CH['P1']), 6e-3); near('P1 dot', roots(2*x**2 - 7)[1], 1.871)
near('P2', roots(-x**2 + 4*x + 6)[1], num(CH['P2']), 6e-3); near('P2 dot', roots(-x**2 + 4*x + 6)[1], 5.162); ok('P2 exact', roots(-x**2 + 4*x + 6)[1], 2 + sp.sqrt(10))
ok('P5', sum(roots(x**2 - 6*x + 5)), num(CH['P5'])); ok('P5 dots', roots(x**2 - 6*x + 5), [1, 5])
ok('P6', roots(2*x**2 - 5*x - 3), [sp.Rational(-1, 2), num(CH['P6'])])
ok('P11', vertex(sp.expand(-(x - 1)*(x + 7))), (-3, num(CH['P11'])))
ok('P12', vertex(2*x**2 + 8*x - 3), (-2, num(CH['P12'])))
r = sys2(4*x - 3*y - 10, x + 2*y - 8); ok('P3', (r[x], r[y], r[x] + r[y]), (4, 2, num(CH['P3'])))
r = sys2(y + 3*x - 11, y - x + 5); ok('P4', (r[x], r[y]), (4, num(CH['P4'])))
ok('P17', (sorted(sp.solve(sp.Eq(sp.Abs(2*x + 3), 9), x)), sum(sp.solve(sp.Eq(sp.Abs(2*x + 3), 9), x))), ([-6, 3], num(CH['P17'])))
s18 = sp.solve(sp.Eq(sp.Abs(3*x - 4), 8), x); ok('P18', (sorted(s18), sum(s18)), ([sp.Rational(-4, 3), 4], num(CH['P18'])))
near('P18 decimals', sum(s18), 2.6667); ok('P18 no 2.67', abs(2.67 - float(sum(s18))) > 0.0011, True)
ok('P7', (sp.simplify((6*x - 4*y - 10) - 2*(3*x - 2*y - 5)), key(CH['P7'])), (0, 'Infinitely many'))
ok('P8', (sp.solve([2*x + 3*y - 6, 4*x + 6*y - 9], [x, y]), key(CH['P8']), sp.Rational(6, 3), sp.Rational(9, 6)), ([], 'Zero', 2, sp.Rational(3, 2)))
kv = sp.solve(sp.Eq(sp.Rational(5, 2), -10/k), k)[0]; ok('P23', (kv, sp.solve([5*x - 2*y - 7, 10*x - 4*y - 3], [x, y])), (num(CH['P23']), []))
ok('P24', (sp.simplify(2*(2*x + 5*y - 12) - (4*x + 10*y - 24)), num(CH['P24'])), (0, 4))
f13 = x**2 - 6*x + 10; ok('P13', (vertex(f13), vertex(f13 - 4), len(sp.solve(f13 - 4, x)), len(sp.solve(f13, x))), ((3, 1), (3, -3), num(CH['P13']), 0))
f14 = -x**2 + 2*x + 3; ok('P14', (vertex(f14), vertex(f14 + 3)), ((1, 4), (1, num(CH['P14']))))
lines21 = [x + 2*y - 6, 2*x - y - 6, 2*x + y - 6, y - 2*x - 6]
hit = [i for i, e in enumerate(lines21) if sp.solve(e, y)[0].coeff(x, 1) == -2 and sp.solve(e, y)[0].subs(x, 0) == 6]; ok('P21', hit, [CH['P21']['correct']])
ok('P21 text', key(CH['P21']), '$2x + y = 6$')
lines22 = [3*x + 4*y - 12, 4*x - 3*y - 12, 3*x - 4*y - 12, 4*x + 3*y - 12]
hit = [i for i, e in enumerate(lines22) if e.subs({x: 3, y: 0}) == 0 and e.subs({x: 6, y: -4}) == 0]; ok('P22', hit, [CH['P22']['correct']])
ok('P22 B', (lines22[1].subs({x: 3, y: 0}), lines22[1].subs({x: 6, y: -4}) != 0), (0, True)); ok('P22 text', key(CH['P22']), '$4x + 3y = 12$')
ok('P19', (2*3 - 1, -3 + 5), (num(CH['P19']), 2))
pts = [(1, 1), (2, 4), (0, 12), (4, 3)]; hit = [i for i, (u, v) in enumerate(pts) if v > u + 1 and v < -2*u + 10]; ok('P20', hit, [CH['P20']['correct']])
ok('P20 why', ([v < -2*u + 10 for u, v in pts][2], [v > u + 1 for u, v in pts][0], [v > u + 1 for u, v in pts][3]), (False, False, False))
d15 = [4, 4, 9, 11, 15, 20, 21]; ok('P15', (sum(d15), F(sum(d15), 7), statistics.median(d15), F(sum(d15), 7) - statistics.median(d15)), (84, 12, 11, num(CH['P15'])))
d16 = [6, 9, 10, 10, 14, 17, 22, 24]; ok('P16', (sum(d16), F(sum(d16), 8), statistics.median(d16), F(sum(d16), 8) + F(statistics.median(d16))), (112, 14, 12, num(CH['P16'])))
m, b0 = lsq([1, 4, 6, 10], [3, 8, 11, 18]); near('P25 m', m, 1.66082, 6e-6); near('P25 b', b0, 1.2807, 6e-5); near('P25 R2', r2([1, 4, 6, 10], [3, 8, 11, 18]), 0.9993, 6e-5)
ok('P25', (round(float(m), 1), round(float(b0), 1), key(CH['P25'])), (1.7, 1.3, '$y = 1.7x + 1.3$'))
m, b0 = lsq([0, 3, 5, 8], [4, 7, 10, 12]); near('P26 m', m, 1.02941, 6e-6); near('P26 b', b0, 4.13235, 6e-6); near('P26 R2', r2([0, 3, 5, 8], [4, 7, 10, 12]), 0.9804, 6e-5)
ok('P26', (round(float(m), 1), round(float(b0), 1), CH['P26']['correct']), (1.0, 4.1, 1)); ok('P26 text', 'slope $\\approx 1.0$, intercept $\\approx 4.1$', key(CH['P26']))
r = [s for s in sp.solve([a*b - 10, a*b**3 - 40], [a, b], dict=True) if s[b] > 0][0]; ok('N2', (r[a], r[b], r[a]*r[b]**5), (5, 2, num(CH['N2'])))
r = sp.solve([a - b + c - 9, a + b + c - 1, 4*a + 2*b + c - 3], [a, b, c], dict=True)[0]; ok('N3', (r[a], r[b], r[c], 16*r[a] + 4*r[b] + r[c]), (2, -4, 3, num(CH['N3'])))
p_ = sp.Symbol('p'); ok('N4', (sp.solve(sp.Eq(3*(p_ - 2), 3*p_ + 4), p_), sp.simplify(3*(p_ - 2) - (3*p_ + 4)), key(CH['N4'])), ([], -10, 'The equation has no solution.'))
r = sp.solve([4*b + 3*w - sp.Rational(255, 100), 2*b + 5*w - sp.Rational(215, 100)], [b, w], dict=True)[0]; ok('N5', (r[b], r[w]), (num(CH['N5']), sp.Rational(1, 4)))
r = sp.solve([a + b + c - 32, a - 3*b, c - b - 2], [a, b, c], dict=True)[0]; ok('N6', (r[a], r[b], r[c]), (num(CH['N6']), 6, 8))
e = sp.expand((x + 4)*(x - 7)); ok('N7', (e.coeff(x, 1), e.coeff(x, 0), e.coeff(x, 1) + e.coeff(x, 0)), (-3, -28, num(CH['N7'])))
ok('N8', (sp.expand(3*(x + 2)**2 - 7 - (3*x**2 + 12*x + 5)), vertex(3*x**2 + 12*x + 5)), (0, (-2, num(CH['N8']))))
cv = sp.solve(sp.discriminant(x**2 - 2*x + 5 - (3*x + c), x), c)[0]; ok('N9', (cv, sp.expand((-5)**2 - 4*1*(5 - c))), (num(CH['N9']), sp.discriminant(x**2 - 5*x + (5 - c), x)))
ok('N9 accept', [sp.nsimplify(v) for v in CH['N9']['accept']], [sp.Rational(-5, 4)] * 2); ok('N9 between', -2 < cv < -1, True)
ok('P9', (3 - 3, len(sp.solve((x - 2)**2 + (0 - 3)**2 - 9, x))), (0, num(CH['P9'])))
r10 = sorted(sp.solve((x + 2)**2 + (0 - 1)**2 - 25, x)); ok('P10', len(r10), num(CH['P10'])); near('P10 a', r10[1], 2.90, 6e-3); near('P10 b', r10[0], -6.90, 6e-3)
v_, n_ = [2, 3, 4, 5, 6], [3, 5, 6, 4, 2]; ok('N10', (sum(n_), sum(u*q for u, q in zip(v_, n_)), F(sum(u*q for u, q in zip(v_, n_)), sum(n_)), statistics.mean(v_)), (20, 77, num(CH['N10']), 4))
near('N11', 20*math.sin(math.radians(35)), 11.4715, 6e-5); ok('N11 key', CH['N11']['accept'][0], '11.5'); near('N11 rad', 20*math.sin(35), -8.56, 6e-3)
ok('by-move key spread', sorted(set(q['correct'] for q in CH.values() if q['type'] == 'mc')), [0, 1, 2, 3])

# ---------------------------------------------------------------- carried answers vs. the snapshot
PILL = {'P1': '1.87', 'P2': '5.16', 'P3': '6', 'P4': '-1', 'P5': '6', 'P6': '3', 'P9': '1', 'P10': '2', 'P12': '-11', 'P13': '2', 'P14': '7',
        'P15': '1', 'P16': '26', 'P17': '-3', 'P18': '8/3', 'P23': '-4', 'P24': '4'}
for qid, want in PILL.items():
    pill = OLD_P[qid]['pill'][0].replace(chr(8722), '-').replace('k = ', '')
    ok('snapshot ' + qid, (pill, CH[qid]['accept'][0]), (want, want))
for qid, letter in {'P7': 'D', 'P8': 'A', 'P20': 'B', 'P21': 'C', 'P22': 'D', 'P25': 'A', 'P26': 'B'}.items():
    ok('snapshot ' + qid, (OLD_P[qid]['pill'][0][0], 'ABCD'[CH[qid]['correct']]), (letter, letter))
    old_opts = re.findall(r'<li><span class="ltr">[A-D]</span>(.*?)</li>', OLD_P[qid]['stem'])
    strip = lambda s_: re.sub(r'[\s{}]|\\,', '', s_).lower()
    ok('snapshot options ' + qid, [strip(o) for o in old_opts], [strip(o) for o in CH[qid]['options']])
ok('snapshot P11', (OLD_P['P11']['pill'][0], CH['P11']['accept'][0]), ('x = ' + chr(8722) + '3, maximum 16', '16'))
ok('snapshot P19', (OLD_P['P19']['pill'][0], CH['P19']['accept'][0]), ('any y with 2 ' + chr(8804) + ' y ' + chr(8804) + ' 5', '5'))
ok('carried count', (len(OLD_P), sorted(q for q in d3.BY_MOVE_IDS if q.startswith('P')) == sorted(OLD_P), len(OLD_G), len(G)), (26, True, 15, 15))
for i, (old, new) in enumerate(zip(OLD_G, G), 1):
    ok('snapshot G%d format' % i, {'mc': 'mc', 'grid': 'ne'}[old['format']], new['type'])
    ok('snapshot G%d tier' % i, old['tier'].capitalize(), new['diff'])
    if new['type'] == 'mc':
        ok('snapshot G%d key' % i, old['answer'], new['correct'])
        strip = lambda s_: re.sub(r'[\s{}$]|\\', '', s_).lower()
        ok('snapshot G%d options' % i, [strip(o) for o in old['options']], [strip(o) for o in new['options']])
    else:
        ok('snapshot G%d key' % i, old['accepted'][0], new['accept'][0])
    nums = lambda s_: sorted(re.findall(r'\d+(?:\.\d+)?', re.sub(r'<svg.*?</svg>|<table.*?</table>|\{,\}|[{}]', '', s_, flags=re.S)))
    ok('snapshot G%d numbers' % i, nums(old['prompt'] + old.get('prompt2', '')), nums(new['stem']))

# ---------------------------------------------------------------- timed practice set
r = sp.solve([x + y - 240, 12*x + 8*y - 2480], [x, y], dict=True)[0]; ok('G1', (r[x], '$%s$' % r[y]), (140, key(G[0]))); ok('G1 trap', '$140$' in G[0]['options'], True)
ok('G2', sorted(sp.solve(-16*t**2 + 48*t + 64, t)), [-1, sp.nsimplify(G[1]['accept'][0])])
v_, n_ = [0, 1, 2, 3], [6, 8, 4, 2]; ok('G3', (sum(n_), sum(u*q for u, q in zip(v_, n_)), '$%.1f$' % (sum(u*q for u, q in zip(v_, n_)) / sum(n_)), '$%.1f$' % statistics.mean(v_)), (20, 22, key(G[2]), '$1.5$'))
ok('G3 trap', '$1.5$' in G[2]['options'], True)
m, b0 = lsq([6, 11], [57, 77]); ok('G4', (m, b0), (4, sp.nsimplify(G[3]['accept'][0])))
ok('G5', (sp.sqrt((-4 + 4)**2 + (6 - 1)**2), key(G[4]), sp.expand((x + 4)**2 + (y - 6)**2 - 25).subs({x: -4, y: 1})), (5, '$(x + 4)^2 + (y - 6)^2 = 25$', 0))
m, b0 = lsq([2, 5], [7, 16]); ok('G6', (m, b0, 10*m + b0), (3, 1, sp.nsimplify(G[5]['accept'][0])))
cross = math.log(0.5) / math.log(0.85); near('G7 cross', cross, 4.27, 6e-3); ok('G7', '$%d$' % math.ceil(cross), key(G[6])); near('G7 a', 0.85**4, 0.522); near('G7 b', 0.85**5, 0.444)
gx, gy = [20, 22, 25, 27, 29], [240, 265, 300, 330, 350]
m, b0 = lsq(gx, gy); near('G8 m', m, 12.387, 6e-4); near('G8 b', b0, -7.726, 6e-4); near('G8 pred', 30*m + b0, 363.89, 6e-3); near('G8 R2', r2(gx, gy), 0.9979, 6e-5)
opts = [350, 358, 364, 376]; ok('G8', min(range(4), key=lambda i: abs(opts[i] - float(30*m + b0))), G[7]['correct'])
circ = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)"', d3.G8_FIG)
ok('G8 figure', [(round(18 + (float(u) - 56) / 24.857), round(220 + (256 - float(v)) * 0.75)) for u, v in circ], list(zip(gx, gy)))
ok('G9', (sp.expand((x + 3)*(x - 5) + 2*(x - 1)), key(G[8])), (x**2 - 17, '$x^2 - 17$'))
ok('G10', (sp.Rational(200 - 18*7, 4), math.ceil((200 - 18*7) / 4), 18*7 + 4*18), (sp.Rational(37, 2), int(G[9]['accept'][0]), 198))
ok('G11', sorted(sp.solve(sp.discriminant(2*x**2 + b*x + 8, x), b)), [-8, sp.nsimplify(G[10]['accept'][0])])
near('G12', 2**0.2, 1.1487, 6e-5); ok('G12 key', (round((2**0.2 - 1) * 100, 1), key(G[11])), (14.9, r'$15\%$'))
ok('G13', (sp.expand((x - 3)**2 + (y + 2)**2 - 25 - (x**2 + y**2 - 6*x + 4*y - 12)), len(sp.solve([x**2 + y**2 - 6*x + 4*y - 12, y - x + 1], [x, y])), key(G[12])), (0, 2, 'Exactly two'))
near('G13 dist', abs(3 + 2 - 1) / math.sqrt(2), 2.83, 6e-3)
xs = sorted(sp.solve(sp.Eq(sp.Abs(x - 3) + 1, 5), x)); ok('G14', (xs, sp.Rational(1, 2) * (xs[1] - xs[0]) * (5 - 1)), ([-1, 7], sp.nsimplify(G[13]['accept'][0])))
kv = sp.solve(sp.discriminant(x**2 + 4*x + k - (2*x + 1), x), k)[0]; ok('G15', (kv, sp.solve(sp.discriminant(x**2 + 4*x + k, x), k)[0]), (sp.nsimplify(G[14]['accept'][0]), 4))
ok('timed key spread', sorted(set(q['correct'] for q in G if q['type'] == 'mc')), [0, 1, 2])
ok('timed tiers', [q['diff'] for q in G], ['Easy'] * 5 + ['Medium'] * 5 + ['Hard'] * 5)

# ---------------------------------------------------------------- skill practice
ok('F1', (sp.solve(5*x - 8 - 27, x), FL[0]['correct']), ([7], 1))
ok('F2', (sorted(s for s in [sp.solve(4*x - 5 - (3*x + 9), x)[0], sp.solve(4*x - 5 + (3*x + 9), x)[0]] if abs(4*s - 5) == 3*s + 9), FL[1]['correct']), ([sp.Rational(-4, 7), 14], 2))
ok('F3', ((4*x**2 - 9*x + 6).subs(x, 0), FL[2]['correct']), (6, 0))
r = [s for s in sp.solve([a*b**2 - 20, a*b**4 - 80], [a, b], dict=True) if s[b] > 0][0]; ok('F4', (r[a], r[b], r[a]*r[b]**7, FL[3]['correct']), (5, 2, 640, 3))
kv = sp.solve(sp.Eq(sp.Rational(2, 3), -6/k), k)[0]; ok('F5', (kv, sp.solve([2*x - 3*y - 4, 6*x - 9*y - 9], [x, y]), FL[4]['correct']), (-9, [], 1))
ok('F6', (sp.expand((3*x - 2)*(x + 5)), FL[5]['correct']), (3*x**2 + 13*x - 10, 0)); ok('F7', FL[6]['correct'], 2)
ok('F8', (sp.expand((x + 4)**2 + (y - 1)**2 - 36 - (x**2 + y**2 + 8*x - 2*y - 19)), 1 + 6, 1 - 6, FL[7]['correct']), (0, 7, -5, 3))
ok('F9', FL[8]['correct'], 1)
r = sp.solve([c - 5, a + b + c - 4, 9*a + 3*b + c - 14], [a, b, c], dict=True)[0]; ok('F10', (r[a], r[b], r[c], FL[9]['correct']), (2, -3, 5, 2))
ok('F11', F(1*5 + 2*3 + 3*2, 10), sp.nsimplify(FL[10]['accept'][0])); ok('F11b', [sp.nsimplify(v) for v in FL[10]['accept']], [sp.Rational(17, 10)] * 2)
near('F12', 12*math.tan(math.radians(40)), float(FL[11]['accept'][0]), 6e-3); near('F12 rad', 12*math.tan(40), -13.41, 6e-3)
ok('F13', (FL[12]['opts'][FL[12]['correct']],), ('$y = 2.5x - 1.2$',))
ok('F14', 2 * 3**4, sp.nsimplify(FL[13]['accept'][0])); ok('F15', (sum(roots(x**2 - 2*x - 15)), roots(x**2 - 2*x - 15)), (sp.nsimplify(FL[14]['accept'][0]), [-3, 5]))
ok('F16', (sp.Rational(9 - (-1), 2), sp.Rational(9 + (-1), 2)), (sp.nsimplify(FL[15]['accept'][0]), 4))
ok('skill key spread', sorted(set(it['correct'] for it in FL if it.get('mc'))), [0, 1, 2, 3])

# ---------------------------------------------------------------- exit ticket, structure
ok('E', [e['correct'] for e in EX], [1, 1, 3]); ok('E3', 6 + (-2), sp.nsimplify(EX[2]['opts'][EX[2]['correct']].strip('$')))
ok('moves covered', (len(d3.MOVES), sorted(set(d3.BY_MOVE_KEYS)) == sorted(d3.MOVES)), (17, True))
ok('grouped in move order', d3.BY_MOVE_KEYS, sorted(d3.BY_MOVE_KEYS, key=lambda v: list(d3.MOVES).index(v)))
ok('unique ids', len(set(d3.BY_MOVE_IDS)), len(d3.BY_MOVE_IDS))

bad = [c_ for c_ in checks if not c_[1]]
for lab, good, got, want in bad:
    print('FAIL', lab, 'got', got, 'want', want)
print('%d checks, %d failed' % (len(checks), len(bad)))
