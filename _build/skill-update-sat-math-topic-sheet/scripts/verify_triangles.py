#!/usr/bin/env python3
"""Answer-key recomputations for SAT Math 4: Triangles (needs sympy).
Run: python3 verify_triangles.py   -> prints the number of checks; exits non-zero on any failure."""
from sympy import sqrt, Rational as R, symbols, solve, Eq, simplify, sin, cos, pi, nsimplify, Abs, S
import math
n = 0
def ok(cond, what):
    global n
    n += 1
    assert bool(cond), 'FAILED: ' + what
x = symbols('x')
def sol1(eq): r = solve(eq, x); assert len(r) == 1, eq; return r[0]
def tri_ok(a, b, c): s = sorted([a, b, c]); return s[0] + s[1] > s[2]

# ---------------- RULES
# Rule 1
ok(180 - 112 == 68, 'R1 A')
v = sol1(Eq((3*x + 10) + (2*x + 20), 180)); ok(v == 30 and 3*v + 10 == 100 and 2*v + 20 == 80, 'R1 B')
v = sol1(Eq(5*x - 8, 3*x + 26)); ok(v == 17 and 5*v - 8 == 77, 'R1 C')
# Rule 2
ok(180 - 47 - 68 == 65 and 47 + 68 == 115 and 180 - 65 == 115, 'R2 A')
ok((180 - 40) / 2 == 70 and 180 - 2*40 == 100, 'R2 B')
ok(35 + 50 == 85, 'R2 C')
# Rule 3
ok(sqrt(9**2 + 12**2) == 15 and 81 + 144 == 225, 'R3 A')
ok(sqrt(26**2 - 10**2) == 24 and 676 - 100 == 576, 'R3 B')
ok(sqrt(4**2 + 6**2) == 2*sqrt(13) and 16 + 36 == 52 and abs(math.sqrt(52) - 7.21) < 0.005, 'R3 C')
ok(15 + 34 == 49 and sqrt(49) == 7, 'R3 D')
for t in [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(6,8,10),(9,12,15),(10,24,26)]:
    ok(t[0]**2 + t[1]**2 == t[2]**2, 'triple %s' % (t,))
# Rule 4
ok(simplify(14/sqrt(2) - 7*sqrt(2)) == 0, 'R4 A')
ok(R(18, 2) == 9, 'R4 B')
ok(simplify(12/sqrt(3) - 4*sqrt(3)) == 0 and simplify(2*12/sqrt(3) - 8*sqrt(3)) == 0, 'R4 C')
ok(simplify(10*sqrt(3)/2 - 5*sqrt(3)) == 0 and simplify(R(1,2)*10*5*sqrt(3) - 25*sqrt(3)) == 0 and simplify(10**2*sqrt(3)/4 - 25*sqrt(3)) == 0, 'R4 D')
ok(simplify(5*sqrt(2) - sqrt(50)) == 0 and 1.73 < math.sqrt(3) < 1.74, 'R4 table')
# Rule 5
ok(8 - 5 == 3 and 8 + 5 == 13 and len([c for c in range(1, 30) if tri_ok(5, 8, c)]) == 9 and min(c for c in range(1,30) if tri_ok(5,8,c)) == 4 and max(c for c in range(1,30) if tri_ok(5,8,c)) == 12, 'R5 A')
ok(not tri_ok(7, 10, 18) and tri_ok(7, 10, 16) and not tri_ok(4, 5, 9), 'R5 B')
# Rule 6
ok(R(18, 4) == R(9, 2) and R(18, 4)*10 == 45 and 18 + 45 == 63, 'R6 A')
# Rule 7
ok(sqrt(4*9) == 6, 'R7 A')
ok(sqrt(2*8) == 4 and simplify(sqrt(6*8) - 4*sqrt(3)) == 0 and 4**2 + 48 == 8**2, 'R7 B')
ok(sqrt(14**2 + 48**2) == 50 and R(14*48, 50) == R(1344, 100), 'R7 C')
# mistakes
ok(sqrt(169 - 25) == 12 and 169 + 25 == 194, 'M4')

# ---------------- STEPS
v = sol1(Eq((3*x + 15) + (2*x + 5), 180)); ok(v == 32 and 3*v + 15 == 111 and 2*v + 5 == 69, 'S1'); ok(sol1(Eq(3*x + 15, 2*x + 5)) == -10, 'S1 mistake')
v = sol1(Eq(3*x + (2*x + 8), 128)); ok(v == 24 and 3*v == 72 and 2*v + 8 == 56 and 180 - 128 == 52 and 72 + 56 + 52 == 180, 'S2')
ok(38 + 57 == 95 and 180 - 95 == 85, 'S3'); ok((180 - 40)/2 == 70, 'S3 micro')
ok(74 - 25 == 49 and sqrt(49) == 7 and 5**2 + 7**2 == 74, 'S4')
ok(simplify(12/sqrt(3) - 4*sqrt(3)) == 0 and simplify(R(1,2)*12*4*sqrt(3) - 24*sqrt(3)) == 0 and 144 + 48 == 192 and simplify((8*sqrt(3))**2 - 192) == 0, 'S5'); ok(18/2 == 9, 'S5 micro')
s_ = symbols('s', positive=True); r = solve(Eq(s_**2*sqrt(3)/4, 25*sqrt(3)), s_); ok(r == [10], 'S6'); ok(simplify((14/sqrt(2))**2 - 98) == 0 and R(14**2, 2) == 98, 'S6 micro')
lo, hi = R(11 - 5 + 1, 2), R(11 + 5 + 1, 2); ok(lo == R(7,2) and hi == R(17,2), 'S7 range')
ints = [k for k in range(-5, 30) if 2*k - 1 > 0 and tri_ok(5, 11, 2*k - 1)]; ok(ints == [4,5,6,7,8], 'S7 integers')
ok(not tri_ok(4,5,9) and not tri_ok(3,8,12) and tri_ok(7,9,15) and not tri_ok(2,10,13), 'S7 micro')
ok(R(42, 7) == 6 and 6*3 == 18 and 6*10 == 60, 'S8'); ok(R(18,4)*10 == 45, 'S8 micro')
ok(sqrt(25*144) == 60 and 25 + 144 == 169 and 25*169 == 4225 and sqrt(4225) == 65 and 144*169 == 24336 and sqrt(24336) == 156 and 65**2 + 156**2 == 28561 == 169**2 and R(1,2)*65*156 == 5070 == R(1,2)*169*60 and (5*13, 12*13, 13*13) == (65, 156, 169), 'S9'); ok(sqrt(4*9) == 6, 'S9 micro')

# ---------------- SKILL PRACTICE
ok(180 - 133 == 47, 'F1')
v = sol1(Eq(2*x + 3*x + 25, 180)); ok(v == 31 and 2*v == 62 and 3*v + 25 == 118, 'F2')
ok(180 - 38 - 79 == 63, 'F3')
ok((180 - 96)/2 == 42, 'F4')
ok(sqrt(8**2 + 15**2) == 17, 'F5')
ok(sqrt(39**2 - 15**2) == 36, 'F6')
ok(sqrt(20**2 + 21**2) == 29, 'F7')
ok(17 + 64 == 81 and sqrt(81) == 9, 'F8')
ok(simplify(6*sqrt(2) - sqrt(72)) == 0, 'F9')
ok(2*7 == 14, 'F10')
ok(simplify(9/sqrt(3) - 3*sqrt(3)) == 0, 'F11')
ok(simplify(12**2*sqrt(3)/4 - 36*sqrt(3)) == 0, 'F12')
ok(max(c for c in range(1, 40) if tri_ok(6, 13, c)) == 18, 'F13')
ok(max([48, 61, 71]) == 71 and 48 + 61 + 71 == 180, 'F14')
ok(R(8, 2)*9 == 36, 'F15')
ok(sqrt(5*20) == 10, 'F16')

# ---------------- PRACTICE SET
ok(180 - 124 == 56 and 124 - 90 == 34, 'P1')
ok(180 - 52 - 71 == 57 and 52 + 71 == 123, 'P2')
ok(sqrt(37**2 - 12**2) == 35 and 37**2 == 1369 and 1369 - 144 == 1225 and 37**2 + 12**2 == 1513, 'P3')
v = sol1(Eq(4*x - 5, (x + 20) + 2*x)); ok(v == 25 and v + 20 == 45 and 2*v == 50 and 4*v - 5 == 95, 'P4')
ok(42/3 == 14 and simplify(14*sqrt(3)/2 - 7*sqrt(3)) == 0, 'P5')
ok(min(c for c in range(1, 40) if tri_ok(9, 14, c)) == 6 and 9 + 14 + 6 == 29, 'P6')
ok(34 + 47 == 81 and 180 - 81 == 99 and 47 - 34 == 13 and 2*81 == 162, 'P7')
ok(sqrt(7**2 + 24**2) == 25 and sqrt(25**2 - 15**2) == 20 and 625 + 225 == 850 and simplify(sqrt(850) - 5*sqrt(34)) == 0, 'P8')
ok(14*R(3,2) == 21 and 14 + 21 == 35 and 2*35 == 70, 'P9')
area = R(1,2)*6*6*sin(2*pi/3); ok(simplify(area - 9*sqrt(3)) == 0 and simplify(2*6*sin(pi/3) - 6*sqrt(3)) == 0 and 6*cos(pi/3) == 3 and simplify(R(1,2)*6*sqrt(3)*3 - 9*sqrt(3)) == 0, 'P10')

# ---------------- CHALLENGE
ok(180 - 104 == 76 and (180 - 76)/2 == 52, 'C2'); ok((180 - 104)/2 == 38 and 180 - 38 - 52 == 90, 'C2 a b'); ok((180-130)/2 == 25 and 130/2 == 65 and 180 - 25 - 65 == 90, 'C2 c')
ok(simplify(6/sqrt(3) - 2*sqrt(3)) == 0 and simplify(12 + 5 + 5 + 2*4*sqrt(3) - (22 + 8*sqrt(3))) == 0, 'C3')
ok(52/4 == 13, 'C3 a'); ok(simplify(22*sqrt(3)/2 - 11*sqrt(3)) == 0, 'C3 b'); ok(simplify(2*15/sqrt(3) - 10*sqrt(3)) == 0, 'C3 c')
both = [d for d in [5, 6, 13, 14] if tri_ok(5, 9, d) and tri_ok(6, 12, d)]; ok(both == [13], 'C4'); ok(9 - 5 == 4 and 9 + 5 == 14 and 12 - 6 == 6 and 12 + 6 == 18, 'C4 ranges')
PQ = 6/sin(pi/6); QR = 6/cos(pi/6); ok(PQ == 12 and simplify(QR - 4*sqrt(3)) == 0 and simplify(PQ*QR - 48*sqrt(3)) == 0, 'C5')
ok(simplify(sqrt(12**2 - 6**2)*sqrt(QR**2 - 6**2) - 36) == 0, 'C5 altitude check')
FH = R(12**2, 9); ok(FH == 16 and FH - 9 == 7 and 144 - 81 == 63 and R(63, 9) == 7, 'C6')
ok(sqrt(3*27) == 9 and sqrt(4*9) == 6 and R(5*12, 13) == R(60, 13) and abs(60/13 - 4.615) < 0.0011 and abs(60/13 - 4.616) < 0.0011, 'C6 extras')
ab = R(16**2 - 12**2, 2); ok(ab == 56 and ab/2 == 28, 'C7'); a_, b_ = 8 + 2*sqrt(2), 8 - 2*sqrt(2); ok(simplify(a_**2 + b_**2 - 144) == 0 and a_ + b_ == 16 and simplify(a_*b_ - 56) == 0, 'C7 legs')
ok(4 + 9 == 13 and R(78, 13) == 6 and 6*9 == 54 and 6*4 == 24 and 24 + 54 == 78, 'C8')

# ---------------- EXIT
ok(180 - 75 == 105, 'X1'); ok(sqrt(12**2 + 16**2) == 20 and simplify(sqrt(16**2 - 12**2) - 4*sqrt(7)) == 0 and 12 + 16 == 28 and 144 + 256 == 400, 'X3')
print(n, 'checks passed')
