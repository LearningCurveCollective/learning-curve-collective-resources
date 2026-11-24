#!/usr/bin/env python3
"""Recomputes the answer key of SAT Math 4C: Similar Figures.

It imports build_similar_figures.py (keep the two files in the same folder) and checks, with sympy:
every rules example, every worked step and quick check, every Skill Practice rep, every practice,
challenge, extra and exit answer; that each multiple-choice item has exactly one correct choice; that
every accepted typed form equals the answer; that each figure carries the numbers its question uses
and is drawn the way the question describes (parallel segments, tangent circles, equal pieces); and
that none of the class book's own numbers survive. Run: python3 verify_similar_figures.py"""
import os, re, sys
from sympy import Rational as R, Symbol, sqrt, pi, solve, simplify, Eq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_similar_figures as B

N = 0


def ok(cond, what):
    global N
    N += 1
    if not cond:
        sys.exit('FAILED: ' + what)


def num(s):
    """The value of a choice or an accepted answer: '$7.2$', '$44\\%$', '3/2', '.8'."""
    t = s.strip().strip('$').replace('\\%', '').replace('{,}', '')
    if re.fullmatch(r'-?\d*\.?\d+', t) or re.fullmatch(r'-?\d+/\d+', t):
        return R(t)
    return None


def has(text, *bits):
    for b in bits:
        ok(b in text, 'text should contain %r: %s' % (b, text[:70]))


def mc(item, want, key='options', q='stem'):
    vals = [num(o) for o in item[key]]
    ok(None not in vals, 'numeric choices: ' + item[q][:60])
    ok(vals[item['correct']] == want, 'keyed choice is %s, expected %s: %s' % (vals[item['correct']], want, item[q][:60]))
    ok(sum(1 for v in vals if v == want) == 1, 'exactly one correct choice: ' + item[q][:60])
    ok(len(set(vals)) == len(vals), 'choices are distinct: ' + item[q][:60])


def typed(item, want, q='stem'):
    ok(len(item['accept']) >= 1, 'has an accepted answer: ' + item[q][:60])
    for a in item['accept']:
        ok(num(a) == want, 'accepted form %r equals %s: %s' % (a, want, item[q][:60]))


def mc_text(item, want, key='opts', q='q'):
    ok(item[key][item['correct']] == want and item[key].count(want) == 1, 'keyed choice is %r: %s' % (want, item[q][:60]))


# ---- the relationships, written once
def match(a, a2, b):            # side b in the first figure; its match in the second, where a matches a2
    return R(b) * R(a2) / R(a)
def nest_bc(ad, db, de):        # nested picture: BC from AD, DB and DE
    return R(de) * (R(ad) + R(db)) / R(ad)
def nest_de(ad, db, bc):
    return R(bc) * R(ad) / (R(ad) + R(db))
def area_to(a, b, area):        # lengths a : b, area of the first figure; area of the second
    return R(area) * R(b) ** 2 / R(a) ** 2
def vol_to(a, b, vol):
    return R(vol) * R(b) ** 3 / R(a) ** 3
def shoelace(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2
def slice_ratio(f, g=1):        # nested triangles from one vertex with side fractions f < g: (band area) / (whole triangle area), by coordinates
    A, Bp, C = (R(2), R(5)), (R(0), R(0)), (R(7), R(0))
    on = lambda P, Q, t: (P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t)
    band = shoelace([on(A, Bp, f), on(A, Bp, g), on(A, C, g), on(A, C, f)])
    return band / shoelace([A, Bp, C])


# ================================================================ rules tab
RU = B.RULES
ok(R(12, 8) == R(3, 2) and match(8, 12, 10) == 15 and match(8, 12, 12) == 18, 'Rule 1 example A')
has(RU, r'k = \dfrac{12}{8} = 1.5', r'EF = 1.5 \cdot 10 = 15', r'DF = 1.5 \cdot 12 = 18')
ok(match(9, 6, 12) == 8 and match(9, 6, 18) == 12, 'Rule 1 example B'); has(RU, r'$\dfrac{6}{9} = \dfrac{2}{3}$, so its other sides are $8$ and $12$')
ok(nest_de(6, 3, 12) == 8, 'Rule 2 example A'); has(RU, r'$AB = 9$, so $\dfrac{DE}{12} = \dfrac{6}{9}$ and $DE = 8$')
ok(match(4, 10, 6) == 15, 'Rule 2 example B'); has(RU, r'$\dfrac{SM}{6} = \dfrac{10}{4}$ and $SM = 15$')
ok(match(6, 10, 24) == 40 and R(10, 6) == R(5, 3), 'Rule 3 example A'); has(RU, r'$24 \cdot \dfrac{5}{3} = 40$')
ok(2 * pi * 4 == 8 * pi and 2 * pi * 10 == 20 * pi and R(4, 10) == R(2, 5), 'Rule 3 example B'); has(RU, r'$8\pi$ and $20\pi$', r'$2 : 5$')
ok(5 ** 2 + 12 ** 2 == 13 ** 2 and R(39, 13) == 3 and 15 ** 2 + 36 ** 2 == 39 ** 2, 'Rule 3 example C'); has(RU, r'has $k = 3$, so its sides are $15$ and $36$')
ok(area_to(2, 5, 12) == 75, 'Rule 4 example A'); has(RU, r'$12 \cdot \dfrac{25}{4} = 75$')
ok(area_to(3, 4, 54) == 96, 'Rule 4 example B'); has(RU, r'$54 \cdot \dfrac{16}{9} = 96$')
ok(sqrt(49) == 7 and sqrt(100) == 10 and match(7, 10, 21) == 30, 'Rule 4 example C'); has(RU, r'ratio $7 : 10$', r'is $21$, the matching side of the larger is $30$')
ok(sqrt(R(16, 25)) == R(4, 5), 'Rule 4 going back'); has(RU, r'areas in the ratio $16 : 25$ mean lengths in the ratio $4 : 5$')
ok(R(18, 9) == 2 and area_to(3, 4, 18) - 18 == 14 and 16 - 9 == 7, 'Rule 5 example A (ring)'); has(RU, r'$\dfrac{4}{3}$ times', r'the ring is $7$ parts', r'one part is $2$ and the ring has an area of $14$')
ok(slice_ratio(R(1, 3)) == R(8, 9) and R(88) / R(8, 9) == 99 and R(88, 8) == 11, 'Rule 5 example B (slice)'); has(RU, r'$AD : AB = 1 : 3$', r'is $8$ parts. If its area is $88$, one part is $11$ and $\triangle ABC$ has an area of $99$')
ok(16 - 9 == 7 and (4 - 3) ** 2 == 1, 'Rule 5 note'); has(RU, r'$16 - 9 = 7$ parts, not $(4 - 3)^2 = 1$ part')
ok(vol_to(4, 6, 40) == 135 and R(6, 4) ** 3 == R(27, 8), 'Rule 6 example A'); has(RU, r'$40 \cdot \dfrac{27}{8} = 135$')
ok(R(8, 125) == R(2, 5) ** 3 and R(2, 5) ** 2 == R(4, 25), 'Rule 6 example B'); has(RU, r'ratio $2 : 5$, and their surface areas are in the ratio $4 : 25$')
ok(R(1, 10) ** 3 == R(1, 1000) and 3 ** 2 == 9 and 3 ** 3 == 27, 'Rule 6 note and table'); has(RU, r'<td>$k^3$</td><td>$27$</td>', r'<td>$k^2$</td><td>$9$</td>')
ok(6 + 3 == 9 and match(8, 12, 10) == 15 and 10 * 2 ** 2 == 40 and 25 - 4 == 21 and (5 - 2) ** 2 == 9, 'common mistakes')
has(RU, r'$AB = 9$', r'$10 \cdot 1.5 = 15$', r'$10 \cdot 2^2 = 40$', r'the ring is $21$ parts', r'$(5 - 2)^2 = 9$')
ok(RU.count('class="ref-case"') == 8 and RU.count('class="ref-rule-line"') == 6 + 8, 'six rules and eight common mistakes')

# ================================================================ worked examples
S = B.STEPS
ok(len(S) == 6 and [s['ess'] for s in S] == [True] * 4 + [False] * 2 and B.LAST_STARRED_STEP_INDEX == 3, 'six steps, four starred')
has(S[0]['prob'], '$AB = 10$', '$BC = 14$', '$DE = 15$'); ok(match(10, 15, 14) == 21, 'step 1'); has(S[0]['sol'], r'$EF = 1.5 \cdot 14 = 21$'); has(S[0]['trap'], '$14 + 5 = 19$')
has(S[0]['micro']['q'], '$JK = 8$', '$MN = 20$', '$KL = 12$'); typed(S[0]['micro'], match(8, 20, 12), 'q'); ok(match(8, 20, 12) == 30, 'step 1 check')
has(S[1]['prob'], '$AD = 8$', '$DB = 4$', '$DE = 10$'); ok(nest_bc(8, 4, 10) == 15 and R(10) * 4 / 8 == 5, 'step 2'); has(S[1]['sol'], '$BC = 15$'); has(S[1]['trap'], '$BC = 5$')
has(S[1]['micro']['q'], '$PQ = 6$', '$RS = 15$', '$QM = 8$'); typed(S[1]['micro'], match(6, 15, 8), 'q'); ok(match(6, 15, 8) == 20, 'step 2 check')
has(S[2]['prob'], '$9$, $12$ and $15$', 'shortest side has length $15$'); ok(match(9, 15, 9 + 12 + 15) == 60 and [match(9, 15, x) for x in (9, 12, 15)] == [15, 20, 25], 'step 3'); has(S[2]['sol'], r'$36 \cdot \dfrac{5}{3} = 60$', '$15$, $20$ and $25$')
has(S[2]['micro']['q'], '$3$ times', 'is $7$'); typed(S[2]['micro'], R(21), 'q')
has(S[3]['prob'], r'\dfrac{a}{b} = \dfrac{4}{3}', 'area of $27$'); ok(area_to(3, 4, 27) == 48 and R(27) * 4 / 3 == 36, 'step 4'); has(S[3]['sol'], r'$27 \cdot \dfrac{16}{9} = 48$'); has(S[3]['trap'], 'gives $36$')
has(S[3]['micro']['q'], '$50$ and $72$', '$5 : n$'); ok(sqrt(R(50, 72)) == R(5, 6), 'step 4 check'); typed(S[3]['micro'], R(6), 'q')
has(S[4]['prob'], r'\dfrac{7}{4}', 'area of $32$'); ok(area_to(4, 7, 32) == 98 and 98 - 32 == 66 and R(32, 16) == 2 and 33 * 2 == 66 and R(32) * 7 / 4 == 56, 'step 5'); has(S[4]['sol'], r'$33 \cdot 2 = 66$', '$98 - 32 = 66$'); has(S[4]['trap'], '$98$', '$56$')
has(S[4]['micro']['q'], '$AD = 2$', '$DB = 3$', 'triangle $ADE$ is $8$'); want = R(8) / (1 - slice_ratio(R(2, 5))) * slice_ratio(R(2, 5)); ok(want == 42, 'step 5 check by coordinates'); typed(S[4]['micro'], want, 'q')
has(S[5]['prob'], '$6$ inches and $9$ inches', '$80$ cubic inches'); ok(vol_to(6, 9, 80) == 270 and R(80) * 3 / 2 == 120 and R(80) * 9 / 4 == 180, 'step 6'); has(S[5]['sol'], r'$80 \cdot \dfrac{27}{8} = 270$'); has(S[5]['trap'], '= 120$', '= 180$')
typed(S[5]['micro'], R(4) ** 3, 'q')
for s in S:
    ok(('fig' not in s) or s['fig'] in B.FIGS, 'step figure exists: ' + s['name'])

# ================================================================ skill practice
F = B.FLUENCY
ok([len(x['items']) for x in F] == [5, 5, 4, 5, 4], 'skill practice: 23 reps in five sections')
a, b, c, d, e = [x['items'] for x in F]
has(a[0]['q'], '$AB = 6$', '$DE = 9$'); typed(a[0], R(9, 6), 'q')
mc_text(a[1], r'$\overline{YZ}$')
has(a[2]['q'], '$AB = 4$', '$BC = 9$', '$DE = 12$'); typed(a[2], match(4, 12, 9), 'q'); ok(match(4, 12, 9) == 27, 'A3')
has(a[3]['q'], '$10$, $16$ and $20$', 'longest side of length $15$'); typed(a[3], match(20, 15, 10), 'q'); ok(match(20, 15, 10) == R(15, 2), 'A4')
typed(a[4], match(6, 10, 9), 'q'); ok(match(6, 10, 9) == 15, 'A5')
typed(b[0], nest_bc(3, 9, 4), 'q'); ok(nest_bc(3, 9, 4) == 16, 'B1')
typed(b[1], nest_de(10, 15, 35), 'q'); ok(nest_de(10, 15, 35) == 14, 'B2')
typed(b[2], match(8, 12, 6), 'q'); ok(match(8, 12, 6) == 9, 'B3')
has(b[3]['q'], '$QR = 24$'); x = Symbol('x'); qm = solve(Eq(x / (24 - x), R(5, 15)), x)[0]; typed(b[3], qm, 'q'); ok(qm == 6, 'B4')
has(b[4]['q'], '$AD = 5$', '$DB = 10$'); ok(R(5, 5 + 10) == R(1, 3), 'B5'); mc_text(b[4], '$1 : 3$')
has(c[0]['q'], '$8$ and $12$', 'perimeter of $26$'); typed(c[0], match(8, 12, 26), 'q'); ok(match(8, 12, 26) == 39, 'C1')
has(c[1]['q'], '$6$ and $15$', '$2 : n$'); ok(R(6, 15) == R(2, 5), 'C2'); typed(c[1], R(5), 'q')
has(c[2]['q'], '$28$ and $42$', 'length $8$'); typed(c[2], match(28, 42, 8), 'q'); ok(match(28, 42, 8) == 12, 'C3')
has(c[3]['q'], '$9$ and $6$', 'base of $33$'); typed(c[3], match(9, 6, 33), 'q'); ok(match(9, 6, 33) == 22, 'C4')
mc(d[0], R(3) ** 2, 'opts', 'q')
has(d[1]['q'], '$3$ and $5$', 'area of $18$'); typed(d[1], area_to(3, 5, 18), 'q'); ok(area_to(3, 5, 18) == 50, 'D2')
has(d[2]['q'], '$1 : 4$', 'area of $5$'); typed(d[2], area_to(1, 4, 5), 'q'); ok(area_to(1, 4, 5) == 80, 'D3')
has(d[3]['q'], '$36$ and $121$', '$6 : n$'); ok(sqrt(R(36, 121)) == R(6, 11), 'D4'); typed(d[3], R(11), 'q')
has(d[4]['q'], '$32$ and $50$', 'length $12$'); want = 12 * sqrt(R(50, 32)); typed(d[4], want, 'q'); ok(want == 15, 'D5')
has(e[0]['q'], '$1 : 2$', 'area of $13$'); typed(e[0], area_to(1, 2, 13) - 13, 'q'); ok(area_to(1, 2, 13) - 13 == 39, 'E1')
has(e[1]['q'], '$AD : AB = 1 : 2$', 'triangle $ABC$ is $80$'); want = 80 * slice_ratio(R(1, 2)); typed(e[1], want, 'q'); ok(want == 60, 'E2 by coordinates')
mc(e[2], R(2) ** 3, 'opts', 'q')
has(e[3]['q'], '$2$ and $5$', 'volume of $16$'); typed(e[3], vol_to(2, 5, 16), 'q'); ok(vol_to(2, 5, 16) == 250, 'E4')
for sec in F:
    for it in sec['items']:
        ok(('fig' not in it) or it['fig'] in B.FIGS, 'skill practice figure exists')
        ok(('mc' in it) != ('accept' in it), 'each rep is multiple choice or typed')

# ================================================================ SAT-style practice
G = B.GAUNTLET
ok(len(G) == 10 and [g['diff'] for g in G] == ['Easy', 'Easy', 'Easy to medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium-hard', 'Medium-hard'], 'practice ramp')
ok([g['ess'] for g in G] == [True] * 7 + [False] * 3 and sum(1 for g in G if 'fig' in g) == 8, 'practice: starred chips and eight figures')
ok(sum(1 for g in G if g['type'] == 'mc') == 5 and sum(1 for g in G if g['type'] == 'ne') == 5, 'practice: five multiple choice and five typed')
mc(G[0], match(9, 15, 12)); ok(match(9, 15, 12) == 20, 'P1'); has(G[0]['sol'], '$AB = 9$', '$AC = 12$', '$DE = 15$')
has(G[1]['stem'], 'length $8$', 'length $20$', 'is $34$'); typed(G[1], match(8, 20, 34)); ok(match(8, 20, 34) == 85, 'P2')
mc(G[2], nest_bc(10, 6, 15)); ok(nest_bc(10, 6, 15) == 24 and R(15) * 10 / 6 == 25 and R(15) * 6 / 10 == 9 and 15 + 6 == 21, 'P3 and its distractors'); has(G[2]['sol'], '$AD = 10$', '$DB = 6$', '$DE = 15$')
has(G[3]['stem'], r'\dfrac{3}{5}', 'area of $36$'); typed(G[3], area_to(3, 5, 36)); ok(area_to(3, 5, 36) == 100 and R(36) * 5 / 3 == 60, 'P4')
has(G[4]['stem'], '$5$-foot post', '$3$-foot shadow', '$21$-foot shadow'); mc(G[4], match(3, 5, 21)); ok(match(3, 5, 21) == 35 and R(21) * 3 / 5 == R('12.6') and 5 + (21 - 3) == 23, 'P5 and its distractors')
has(G[5]['stem'], r'\dfrac{a}{b} = \dfrac{7}{4}', 'area of $98$'); typed(G[5], area_to(7, 4, 98)); ok(area_to(7, 4, 98) == 32 and R(98) * 4 / 7 == 56, 'P6')
has(G[6]['stem'], 'area of $6$', 'area of $54$', 'is $14$'); want = 14 * sqrt(R(54, 6)); mc(G[6], want); ok(want == 42 and 14 * R(54, 6) == 126 and 14 + (54 - 6) == 62, 'P7 and its distractors')
has(G[7]['stem'], r'\dfrac{3}{5}', 'area of $63$'); typed(G[7], area_to(3, 5, 63) - 63); ok(area_to(3, 5, 63) == 175 and 175 - 63 == 112, 'P8')
# P9 by coordinates: A (0,0), C (5,0), B (0,h); Q at x = 1 and R at x = 3 (AQ : QR : RC = 1 : 2 : 2); P and S on BC
h = Symbol('h', positive=True)
yb = lambda t: h * (1 - R(t, 5))
quad = shoelace([(1, yb(1)), (1, 0), (3, 0), (3, yb(3))]); whole = R(1, 2) * 5 * h
has(G[8]['stem'], '$AM : MN : NC = 1 : 2 : 2$', '$KMNL$ is $60$'); want = simplify(60 * whole / quad); mc(G[8], want); ok(want == 125 and simplify(quad / whole) == R(12, 25), 'P9 by coordinates')
r = Symbol('r', positive=True)
has(G[9]['stem'], '$2$ times', r'$36\pi$'); want = solve(Eq(pi * (3 * r) ** 2 - pi * (2 * r) ** 2 - pi * r ** 2, 36 * pi), r)[0]; typed(G[9], want); ok(want == 3 and (2 * r * 2 + 2 * r) / 2 == 3 * r, 'P10')
for g in G:
    ok(('fig' not in g) or g['fig'] in B.FIGS, 'practice figure exists')

# ================================================================ challenge
C = B.CHALLENGE
ok(len(C) == 7 and [c_['ess'] for c_ in C] == [True] * 4 + [False] * 3 and sum(len(c_.get('extras', [])) for c_ in C) == 6, 'challenge: seven questions, six extras')
x = Symbol('x', positive=True)
has(C[0]['stem'], '$AD = x$', '$DB = 6$', '$DE = 10$', '$BC = 25$'); want = solve(Eq(x / (x + 6), R(10, 25)), x)[0]; typed(C[0], want); ok(want == 4 and R(6) * 10 / 25 == R('2.4'), 'C1')
ex = C[0]['extras']
typed(ex[0], solve(Eq(x / (x + 5), R(6, 9)), x)[0], 'q'); has(ex[0]['q'], '$DB = 5$', '$DE = 6$', '$BC = 9$'); ok(solve(Eq(x / (x + 5), R(6, 9)), x)[0] == 10, 'C1 extra 1')
typed(ex[1], solve(Eq(6 / (6 + x), R(8, 20)), x)[0], 'q'); has(ex[1]['q'], '$AD = 6$', '$DE = 8$', '$BC = 20$'); ok(solve(Eq(6 / (6 + x), R(8, 20)), x)[0] == 9, 'C1 extra 2')
sol = solve(Eq(x / (3 * x - 4), R(4, 10)), x)[0]; typed(ex[2], sol, 'q'); has(ex[2]['q'], '$AB = 3x - 4$', '$DE = 4$', '$BC = 10$'); ok(sol == 8 and 3 * sol - 4 == 20, 'C1 extra 3')
has(C[1]['stem'], '$PQ = 12$', '$RS = 21$', 'is $32$'); typed(C[1], area_to(12, 21, 32)); ok(area_to(12, 21, 32) == 98 and R(32) * 7 / 4 == 56, 'C2')
has(C[2]['stem'], '$AC = 16$', '$BC = 12$', '$2.5$ times'); hyp = sqrt(16 ** 2 + 12 ** 2); typed(C[2], R(16) / hyp); ok(hyp == 20 and R(16 * R('2.5')) / (hyp * R('2.5')) == R(4, 5), 'C3')
has(C[3]['stem'], r'$20\%$'); mc(C[3], (R('1.2') ** 2 - 1) * 100); ok(R('1.2') ** 2 == R('1.44'), 'C4')
bands = [slice_ratio(0, R(1, 3)), slice_ratio(R(1, 3), R(2, 3)), slice_ratio(R(2, 3), 1)]
has(C[4]['stem'], '$AD = DF = FB$', '$FBCG$ is $45$'); want = 45 / bands[2] * bands[1]; typed(C[4], want); ok(want == 27 and bands == [R(1, 9), R(3, 9), R(5, 9)], 'C5 by coordinates')
ex = C[4]['extras']
has(ex[0]['q'], '$3 : 5$', 'area of $80$'); want = R(80) / (R(25, 9) - 1); typed(ex[0], want, 'q'); ok(want == 45, 'C5 extra 1')
has(ex[1]['q'], '$AD : DB = 1 : 3$', 'is $96$'); want = 96 * slice_ratio(R(1, 4)); typed(ex[1], want, 'q'); ok(want == 90, 'C5 extra 2 by coordinates')
has(ex[2]['q'], '$2$ and $3$'); want = (R(2 * 2 + 2 * 3, 2) ** 2 - 2 ** 2 - 3 ** 2); typed(ex[2], want, 'q'); ok(want == 12, 'C5 extra 3')
has(C[5]['stem'], '$90$ square centimeters', '$160$ square centimeters', '$54$ cubic centimeters'); want = 54 * sqrt(R(160, 90)) ** 3; typed(C[5], want); ok(want == 128 and R(54) * 16 / 9 == 96, 'C6')
has(C[6]['stem'], '$AB = 12$', r'$k\sqrt{2}$'); ad = 12 * sqrt(R(1, 2)); typed(C[6], simplify(ad / sqrt(2))); ok(simplify(ad / sqrt(2)) == 6 and slice_ratio(0, R(1, 2)) == R(1, 4), 'C7')
for c_ in C:
    ok(('fig' not in c_) or c_['fig'] in B.FIGS, 'challenge figure exists')

# ================================================================ exit ticket
E = B.EXIT
ok(len(E) == 3, 'three exit questions')
has(E[0]['q'], '$AB = 12$', '$DE = 18$', '$AC = 20$'); mc(E[0], match(12, 18, 20), 'opts', 'q'); ok(match(12, 18, 20) == 30, 'exit 1')
has(E[1]['q'], '$AD = 6$', '$DB = 12$', '$BC = 27$'); mc(E[1], nest_de(6, 12, 27), 'opts', 'q'); ok(nest_de(6, 12, 27) == 9 and R(27) * 6 / 12 == R('13.5'), 'exit 2')
has(E[2]['q'], '$5$ and $15$', 'area of $7$'); mc(E[2], area_to(5, 15, 7), 'opts', 'q'); ok(area_to(5, 15, 7) == 63, 'exit 3')

# ================================================================ figures: labels and geometry
FG = B.FIGS
def labels(name):
    return sorted(s['t'] for s in FG[name].get('sides', []))
def cross(a, b, c, d):
    return (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
for name, want in {'r_sim': ['10', '12', '12', '15', '18', '8'], 's1': ['10', '14', '15'], 's2': ['10', '4', '8'], 'fa5': ['10', '6', '9', 'x'], 'fb1': ['3', '4', '9'],
                   'fb2': ['10', '15', '35'], 'fb3': ['12', '6', '8'], 'fb4': ['15', '5'], 'p1': ['12', '15', '9'], 'p3': ['10', '15', '6'], 'p6': ['a', 'b'],
                   'c1': ['10', '25', '6', 'x'], 'c2': ['12', '21'], 's4': ['a', 'b']}.items():
    ok(labels(name) == sorted(want), 'figure %s carries the labels %s (has %s)' % (name, want, labels(name)))
for name in ('r_nest', 'r_slice', 's2', 'fb1', 'fb2', 'p3', 'c1', 'c7'):          # nested: segments AB, BC, CA, DE in that order
    sg = FG[name]['segs']; A_, B_, C_, D_, E_ = sg[0]['a'], sg[0]['b'], sg[1]['b'], sg[3]['a'], sg[3]['b']
    ok(abs(cross(D_, E_, B_, C_)) < 1e-6 and abs(cross(A_, D_, A_, B_)) < 2e-2 and abs(cross(A_, E_, A_, C_)) < 2e-2, name + ': DE is parallel to BC, with D on AB and E on AC')
for name in ('r_bow', 'fb3', 'fb4', 'p7', 'c2'):                                   # bowtie: segments PQ, RS, PS, QR in that order
    sg = FG[name]['segs']; P_, Q_, R_, S_ = sg[0]['a'], sg[0]['b'], sg[1]['a'], sg[1]['b']
    ok(abs(cross(P_, Q_, R_, S_)) < 2e-2 and abs(cross(P_, [0, 0], P_, S_)) < 2e-2 and abs(cross(Q_, [0, 0], Q_, R_)) < 2e-2, name + ': PQ is parallel to RS and both segments pass through M')
    ok(dist(R_, S_) > dist(P_, Q_), name + ': RS is drawn longer than PQ')
t = [s for s in FG['r_sim']['segs']]
ok(abs(dist(t[0]['a'], t[0]['b']) / dist(t[2]['a'], t[2]['b']) - 8 / 12) < 1e-3 and abs(dist(t[1]['a'], t[1]['b']) / dist(t[2]['a'], t[2]['b']) - 10 / 12) < 1e-3, 'r_sim: triangle ABC drawn to scale (8, 10, 12)')
ok(abs(dist(t[3]['a'], t[3]['b']) / dist(t[0]['a'], t[0]['b']) - 1.5) < 1e-3, 'r_sim: triangle DEF drawn 1.5 times as large')
p9 = FG['p9']; sg = p9['segs']; A_, B_, C_ = sg[0]['a'], sg[0]['b'], sg[1]['b']; P_, Q_, S_, R_ = sg[3]['a'], sg[3]['b'], sg[4]['a'], sg[4]['b']
ok(abs(cross(B_, P_, B_, C_)) < 1e-2 and abs(cross(B_, S_, B_, C_)) < 1e-2 and P_[0] == Q_[0] and S_[0] == R_[0], 'p9: P and S are on BC, directly above Q and R')
ok(abs((Q_[0] - A_[0]) * 2 - (R_[0] - Q_[0])) < 1e-6 and abs((R_[0] - Q_[0]) - (C_[0] - R_[0])) < 1e-6, 'p9: AM : MN : NC drawn as 1 : 2 : 2')
c3 = FG['p10']['circles']
ok(abs(dist(c3[1]['c'], c3[2]['c']) - (c3[1]['r'] + c3[2]['r'])) < 1e-6 and all(abs(dist(c3[0]['c'], k['c']) + k['r'] - c3[0]['r']) < 1e-6 for k in c3[1:]), 'p10: the inner circles touch each other and the large circle')
ok(c3[1]['r'] == 2 * c3[2]['r'], 'p10: radii drawn 2 : 1')
for name, ratio in (('s5', 7 / 4), ('p8', 5 / 3), ('r_ring', 4 / 3)):
    cc = FG[name]['circles']; ok(abs(cc[0]['r'] / cc[1]['r'] - ratio) < 1e-6 and cc[0]['c'] == cc[1]['c'], name + ': ring drawn with the stated ratio')
c5 = FG['c5']['segs']; A_, B_, D_, F_ = c5[0]['a'], c5[0]['b'], c5[3]['a'], c5[4]['a']
ok(abs(dist(A_, D_) - dist(D_, F_)) < 1e-2 and abs(dist(D_, F_) - dist(F_, B_)) < 1e-2 and abs(cross(c5[3]['a'], c5[3]['b'], c5[1]['a'], c5[1]['b'])) < 1e-2, 'c5: three equal pieces and parallel segments')
c7 = FG['c7']['segs']; ok(abs(dist(c7[0]['a'], c7[3]['a']) / dist(c7[0]['a'], c7[0]['b']) - 2 ** -0.5) < 1e-3, 'c7: AD / AB drawn as 1 over root 2')
ok(all(v.get('alt') for v in FG.values()), 'every figure has alt text')
used = {s.get('fig') for s in S} | {it.get('fig') for sec in F for it in sec['items']} | {g.get('fig') for g in G} | {c_.get('fig') for c_ in C} | set(re.findall(r'data-fig="(\w+)"', RU))
ok(used - {None} == set(FG), 'every figure is used, and every figure used exists')

# ================================================================ nothing from the class book survives
def strings(o):
    if isinstance(o, str): return [o]
    if isinstance(o, dict): return [t for v in o.values() for t in strings(v)]
    if isinstance(o, list): return [t for v in o for t in strings(v)]
    return []
blob = RU + ' '.join(strings([S, F, G, C, E]))
for bad in (r'96\pi', '$147$', '22.5', '$4.8$', '2 : 2 : 3', '$4 : 9$', r'\dfrac{5}{2}', '$3 : 1$', r'$\dfrac{a}{b} = \dfrac{5}{2}$'):
    ok(bad not in blob, 'book number %r does not appear' % bad)
ok(chr(8212) not in blob and chr(8212) not in open(__file__, encoding='utf-8').read(), 'no em dash')

print('verify_similar_figures: %d checks passed' % N)
