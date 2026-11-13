#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Desmos-3-Mixed-Practice.html. Content only; desmos_common.build() does the assembly.

Sheet 3 has no new teaching. It is practice for the 17 moves in SAT Desmos 1 and SAT Desmos 2:
  - tab 2, Skill Practice: 16 quick questions (choose an approach, pick a move, what to type, read the report)
  - tab 3, Practice by Move: the 26 practice questions carried from SAT-Desmos-Strategies.html, plus new
    questions for the moves that sheet did not cover (the tilde moves, entry habits, degree mode)
  - tab 4, Timed Practice Set: the 15 SAT-style questions carried from the same sheet
The carried questions keep their numbers and answers (snapshot: desmos3_source.json; verify_desmos3.py
compares each answer with that snapshot). Three stems were adjusted so that each has one answer to enter:
P11 asks only for the maximum value, P19 asks for the greatest possible value of y, and the timed-set
prompts write money as typeset math. Every Desmos output quoted here (fitted constants, RMSE, R squared,
statistics, trig values) was read from the College Board version of the Desmos graphing calculator on 2026-11-12."""
import os, json, collections
from desmos_common import build, dz, kbd, table, window, slider, DEGREES, SITE, SAT_DIR, HERE
from build_desmos1 import A_STYLE, CB_DESMOS, LINEAR_URL, QUAD_URL, STAR

D1_URL = SITE + 'test-prep/sat/SAT-Desmos-1-Core-Moves.html'
D2_URL = SITE + 'test-prep/sat/SAT-Desmos-2-Next-Steps.html'
FUNC_URL = SITE + 'test-prep/sat/SAT-Math-3-Functions.html'
SOURCE = json.load(open(os.path.join(HERE, 'desmos3_source.json'), encoding='utf-8'))
RMSE0 = r'\text{RMSE} = 0'
MEAN, MEDIAN, TOTAL = r'\operatorname{mean}', r'\operatorname{median}', r'\operatorname{total}'
HOW_MANY = ["Zero", "Exactly one", "Exactly two", "Infinitely many"]


# ---------------------------------------------------------------- THE 17 MOVES
def M(sheet, n, name, ess, when, remind):
    return dict(sheet=sheet, n=n, name=name, ess=ess, when=when, remind=remind)


MOVES = collections.OrderedDict([
    ('1.1', M(1, 1, 'Type it the way the test prints it', True,
              'prints an equation you would rather not rearrange: standard form, fractions, a circle',
              r'Type the equation as it is printed, then read your line back before you use the graph. Press the right arrow to leave a fraction, an exponent or a root.')),
    ('1.2', M(1, 2, 'Read the gray dots', True,
              'asks for an intercept, a zero, a maximum or a minimum',
              r'Graph it, then click the curve. The gray dots mark the intercepts and the highest or lowest point. Check which coordinate the question asks for.')),
    ('1.3', M(1, 3, 'Intersections solve systems, and many single equations', True,
              'gives a system to solve, or a single equation such as an absolute value equation',
              r'Type both equations and click the point where the graphs cross. For a single equation, graph each side on its own line and read the $x$-coordinate of each crossing. Then check what the question asks you to do with those values.')),
    ('1.4', M(1, 4, 'Count the solutions', True,
              'asks how many solutions a system has',
              r'Graph both equations and count the points they share. Lines that cross have one solution, parallel lines have none, and one line drawn for two equations means infinitely many. Zoom out before you decide that two lines are parallel.')),
    ('1.5', M(1, 5, 'Slide an unknown constant', True,
              'has an unknown constant and a condition such as “no solution”',
              r'Type the equations with the unknown constant, add the slider, and move it until the graph shows the condition in the question. Then confirm the value with a short check: equal slopes, or one equation as a multiple of the other.')),
    ('1.6', M(1, 6, 'Name the function, then reuse it and test the choices', True,
              'shifts a graph, or asks which equation or expression matches',
              r'Name the function once, then reuse the name: $f(x) - 4$ for a shift down, $f(3)$ for a value. For a “which equation” question, graph the choices and compare each one with the condition.')),
    ('1.7', M(1, 7, 'Shade the inequalities', False,
              'gives a system of inequalities',
              r'Type each inequality with its symbol and look for the region where the shading overlaps. Points on a solid boundary are solutions; points on a dashed boundary are not.')),
    ('1.8', M(1, 8, 'Let lists do the statistics', False,
              'asks for the mean or median of a list of numbers',
              r'Type the values inside ' + kbd('mean(') + ' or ' + kbd('median(') + r', separated by commas. Then reread the question to see which statistic, or which combination, it asks for.')),
    ('1.9', M(1, 9, 'A table and a tilde: the line of best fit', False,
              'gives data points and asks about a line of best fit',
              r'Enter the points in a table, then type $y_1 \sim m x_1 + b$. In the report, $m$ is the slope and $b$ is the $y$-intercept.')),
    ('2.1', M(2, 1, 'Use a tilde to find the constants: a function through given points', True,
              'gives a few values of a function and asks for another value',
              r'Define the function with letters for the constants, then give Desmos the known inputs and outputs as matching lists with a tilde between them. Evaluate the function on a new line.')),
    ('2.2', M(2, 2, 'Read the report before you use the values', True,
              'has been typed with a tilde, and you are about to use the result',
              r'Before you use a fitted value, read the line underneath it. An RMSE of zero, or a tiny number such as $5 \times 10^{-15}$, indicates an exact match. A larger RMSE means Desmos did not find an exact match: there may be no solution, or the setup may need another look.')),
    ('2.3', M(2, 3, 'Use square brackets for several equations at once', True,
              'is a word problem with its own letters, or has three unknowns',
              r'Put the left sides in one pair of brackets and the right sides in another, in the same order, with a tilde between them. You still need to translate the question into the right equations.')),
    ('2.4', M(2, 4, 'Match two expressions for every $x$', True,
              'says “equivalent,” “for all values of $x$,” or “can be rewritten in the form”',
              r'Give Desmos a short list of inputs, write both expressions with that list in place of $x$, and use a tilde to look for the constants that make them agree. Then answer what the question asks, which may be a combination of the constants.')),
    ('2.5', M(2, 5, 'One solution, no solution: the touching condition', True,
              'says “exactly one solution” and the answer may not be a whole number',
              r'“Exactly one solution” for a line and a parabola means the graphs touch. A slider shows roughly where that happens. To find the value, set the equations equal, move every term to one side, and set the discriminant to zero.')),
    ('2.6', M(2, 6, 'Curves that cross: nonlinear systems and circles', False,
              'pairs a line with a circle or a parabola, or prints a circle in expanded form',
              r'Type each equation as printed, including a circle, and read the graph: count the crossings, or click one for its coordinates. For a circle, the center is halfway between the top and bottom dots.')),
    ('2.7', M(2, 7, 'Lists for statistics', False,
              'gives a frequency table',
              r'A frequency table becomes two lists, the values and their counts. The mean is the total of value times count, divided by the total count.')),
    ('2.8', M(2, 8, 'Degree mode for trigonometry', False,
              'uses sine, cosine or tangent with an angle in degrees',
              r'Desmos starts in radians. When the angle is in degrees, open the wrench menu and choose Degrees before you enter the trig expression.')),
])


def sheet_url(m):
    return D1_URL if m['sheet'] == 1 else D2_URL


def chip(m):
    return 'Desmos %d · Move %d' % (m['sheet'], m['n'])


def heading(m):
    return (STAR + ' ' if m['ess'] else '') + 'SAT Desmos %d, Move %d: %s' % (m['sheet'], m['n'], m['name'])


def remember(m):
    return (m['remind'] + ' <a href="' + sheet_url(m) + '" ' + A_STYLE + '>Review SAT Desmos %d, Move %d &#8594;</a>' % (m['sheet'], m['n']))


def given(g, rest):
    return '<strong>Given:</strong> ' + g + '<br><br>' + rest


def vtab(head1, row1, head2, row2):
    cells = lambda xs: ''.join('<td>$%s$</td>' % x for x in xs)
    return ("<table class='vtab'><tr><th>" + head1 + "</th>" + cells(row1) + "</tr><tr><th>" + head2 + "</th>" + cells(row2) + "</tr></table>")


# ---------------------------------------------------------------- TAB 3: PRACTICE BY MOVE
BY_MOVE, BY_MOVE_IDS, BY_MOVE_KEYS = [], [], []


def _add(qid, mv, d, desmos):
    m = MOVES[mv]
    assert not BY_MOVE_KEYS or list(MOVES).index(mv) >= list(MOVES).index(BY_MOVE_KEYS[-1]), 'keep questions grouped in move order: ' + qid
    d = dict({"ess": m['ess'], "diff": chip(m), "grp": heading(m)}, **d)
    d["trap"] = remember(m)
    if desmos:
        d["desmos"] = desmos
    BY_MOVE.append(d); BY_MOVE_IDS.append(qid); BY_MOVE_KEYS.append(mv)


def ne(qid, mv, stem, label, accept, sol, desmos=None):
    _add(qid, mv, {"type": "ne", "stem": stem, "label": label, "accept": accept, "sol": sol}, desmos)


def mc(qid, mv, stem, options, correct, sol, desmos=None):
    _add(qid, mv, {"type": "mc", "stem": stem, "options": options, "correct": correct, "sol": sol}, desmos)


# ----- SAT Desmos 1, Move 1
ne('N1', '1.1',
   r"$$\tfrac{3}{4}x + \tfrac{1}{2}y = 7$$ $$\tfrac{1}{4}x - y = 0$$ The solution to the system of equations above is $(x, y)$. What is the value of $x$?",
   "$x =$", ["8"],
   given(r"a system with fraction coefficients; the question asks for $x$.",
         dz([{'x': r'\tfrac{3}{4}x + \tfrac{1}{2}y = 7'}, {'x': r'\tfrac{1}{4}x - y = 0', 'see': 'click the crossing: (8, 2)'}]) +
         r"The $x$-coordinate of the crossing is $8$. Check: $\tfrac{3}{4}(8) + \tfrac{1}{2}(2) = 6 + 1 = 7$ and $\tfrac{1}{4}(8) - 2 = 0$. ✓ Give each fraction its own right arrow: type 3 / 4, press the arrow, then type $x$."),
   [r"\frac{3}{4}x+\frac{1}{2}y=7", r"\frac{1}{4}x-y=0", window(-2, 14, -4, 8)])

# ----- SAT Desmos 1, Move 2
ne('P1', '1.2',
   r"In the parabola $y = 2x^2 - 7$, what is the $x$-coordinate of the positive $x$-intercept, rounded to the nearest hundredth?",
   r"$x \approx$", ["1.87", "1.871"],
   given(r"$y = 2x^2 - 7$; the question asks for the positive $x$-intercept.",
         dz([{'x': r'y = 2x^2 - 7', 'see': 'click the right-hand dot on the x-axis: (1.871, 0)'}]) +
         r"Rounded to the nearest hundredth, $x \approx 1.87$. With algebra: $2x^2 = 7$, so $x = \sqrt{3.5} \approx 1.87$."),
   ["y=2x^2-7"])
ne('P2', '1.2',
   r"The graph of $y = -x^2 + 4x + 6$ has two $x$-intercepts. What is the $x$-coordinate of the one that is positive, rounded to the nearest hundredth?",
   r"$x \approx$", ["5.16", "5.162"],
   given(r"$y = -x^2 + 4x + 6$; the question asks for the positive $x$-intercept.",
         dz([{'x': r'y = -x^2 + 4x + 6', 'see': 'click the right-hand dot on the x-axis: (5.162, 0)'}]) +
         r"Rounded to the nearest hundredth, $x \approx 5.16$. With the quadratic formula: $x = 2 \pm \sqrt{10}$, and $2 + \sqrt{10} \approx 5.16$."),
   ["y=-x^2+4x+6", window(-4, 8, -6, 12)])
ne('P5', '1.2',
   r"The graph of the function $f(x) = x^2 - 6x + 5$ intersects the $x$-axis at two points. What is the sum of the $x$-coordinates of those points?",
   "Sum $=$", ["6"],
   given(r"$f(x) = x^2 - 6x + 5$; the question asks for the sum of the two $x$-intercepts.",
         dz([{'x': r'f(x) = x^2 - 6x + 5', 'see': 'dots on the x-axis: (1, 0) and (5, 0)'}]) +
         r"The sum is $1 + 5 = 6$. Check: $(x - 1)(x - 5) = x^2 - 6x + 5$. ✓"),
   ["f(x)=x^2-6x+5"])
ne('P6', '1.2',
   r"At what positive value of $x$ does the graph of $f(x) = 2x^2 - 5x - 3$ cross the $x$-axis?",
   "$x =$", ["3"],
   given(r"$f(x) = 2x^2 - 5x - 3$; the question asks for the positive zero.",
         dz([{'x': r'f(x) = 2x^2 - 5x - 3', 'see': 'dots on the x-axis: (&minus;0.5, 0) and (3, 0)'}]) +
         r"The positive zero is $3$. Check: $(2x + 1)(x - 3) = 2x^2 - 5x - 3$. ✓"),
   ["f(x)=2x^2-5x-3"])
ne('P11', '1.2',
   r"$$h(x) = -(x - 1)(x + 7)$$ What is the maximum value of the function $h$?",
   "Maximum $=$", ["16"],
   given(r"a parabola that opens downward, with zeros at $x = 1$ and $x = -7$; the question asks for the maximum value.",
         dz([{'x': r'h(x) = -(x - 1)(x + 7)', 'see': 'click the highest point: (&minus;3, 16)'}]) +
         r"The maximum value is the $y$-coordinate, $16$. It happens at $x = -3$. Without the graph: the vertex is halfway between the zeros, at $x = \dfrac{1 + (-7)}{2} = -3$, and $h(-3) = -(-4)(4) = 16$."),
   ["h(x)=-(x-1)(x+7)", window(-10, 4, -6, 20)])
ne('P12', '1.2',
   r"What is the minimum value of the function $f(x) = 2x^2 + 8x - 3$?",
   "Minimum $=$", ["-11"],
   given(r"$f(x) = 2x^2 + 8x - 3$, a parabola that opens upward; the question asks for the minimum value.",
         dz([{'x': r'f(x) = 2x^2 + 8x - 3', 'see': 'click the lowest point: (&minus;2, &minus;11)'}]) +
         r"The minimum value is the $y$-coordinate, $-11$. Check: $x = -\dfrac{b}{2a} = -2$, and $f(-2) = 8 - 16 - 3 = -11$. ✓"),
   ["f(x)=2x^2+8x-3", window(-8, 4, -14, 10)])

# ----- SAT Desmos 1, Move 3
ne('P3', '1.3',
   r"$$4x - 3y = 10$$ $$x + 2y = 8$$ If $(x, y)$ is the solution to the system above, what is the value of $x + y$?",
   "$x + y =$", ["6"],
   given(r"two linear equations; the question asks for $x + y$ at the solution.",
         dz([{'x': r'4x - 3y = 10'}, {'x': r'x + 2y = 8', 'see': 'click the crossing: (4, 2)'}]) +
         r"$x + y = 4 + 2 = 6$. Check what the question asks: it wants the sum, not $x$."),
   ["4x-3y=10", "x+2y=8"])
ne('P4', '1.3',
   r"$$y = -3x + 11$$ $$y = x - 5$$ The solution to the system above is $(x, y)$. What is the value of $y$?",
   "$y =$", ["-1"],
   given(r"two lines in slope-intercept form; the question asks for the $y$-value of the solution.",
         dz([{'x': r'y = -3x + 11'}, {'x': r'y = x - 5', 'see': 'click the crossing: (4, &minus;1)'}]) +
         r"The $y$-coordinate is $-1$. With algebra: $-3x + 11 = x - 5$ gives $4x = 16$, so $x = 4$ and $y = 4 - 5 = -1$."),
   ["y=-3x+11", "y=x-5"])
ne('P17', '1.3',
   r"What is the sum of the solutions to $|2x + 3| = 9$?",
   "Sum $=$", ["-3"],
   given(r"an absolute value equation; the question asks for the sum of its solutions.",
         dz([{'x': r'y = |2x + 3|'}, {'x': r'y = 9', 'see': 'crossings at x = &minus;6 and x = 3'}]) +
         r"The sum is $-6 + 3 = -3$. With algebra: $2x + 3 = 9$ gives $x = 3$, and $2x + 3 = -9$ gives $x = -6$."),
   [r"y=\left|2x+3\right|", "y=9", window(-10, 8, -3, 13)])
ne('P18', '1.3',
   r"What is the sum of the solutions to $|3x - 4| = 8$? Enter your answer as a fraction or a decimal.",
   "Sum $=$", ["8/3", "2.667", "2.666", "2.6667", "2.6666"],
   given(r"an absolute value equation; the question asks for the sum of its solutions.",
         dz([{'x': r'y = |3x - 4|'}, {'x': r'y = 8', 'see': 'crossings at x = &minus;1.333 and x = 4'}]) +
         r"The crossing at $-1.333$ is $-\tfrac{4}{3}$, so the sum is $4 + \left(-\tfrac{4}{3}\right) = \tfrac{8}{3}$. Enter $8/3$, $2.666$ or $2.667$. A shorter decimal such as $2.67$ is not accepted here; the Bluebook Tools tab in SAT Desmos 1 has practice with the entry rules."),
   [r"y=\left|3x-4\right|", "y=8", window(-6, 8, -3, 12)])

# ----- SAT Desmos 1, Move 4
mc('P7', '1.4',
   r"How many solutions does the following system have? $$6x - 4y = 10$$ $$3x - 2y = 5$$",
   HOW_MANY, 3,
   given(r"two equations in standard form; the question asks how many solutions the system has.",
         dz([{'x': r'6x - 4y = 10'}, {'x': r'3x - 2y = 5', 'see': 'only one line appears'}]) +
         r"The first equation is the second one doubled, so both describe the same line. Each point on that line satisfies both equations: infinitely many solutions."),
   ["6x-4y=10", "3x-2y=5"])
mc('P8', '1.4',
   r"How many solutions does the following system have? $$2x + 3y = 6$$ $$4x + 6y = 9$$",
   HOW_MANY, 0,
   given(r"two equations in standard form; the question asks how many solutions the system has.",
         dz([{'x': r'2x + 3y = 6'}, {'x': r'4x + 6y = 9', 'see': 'two parallel lines'}]) +
         r"Both lines have slope $-\tfrac{2}{3}$, with $y$-intercepts $2$ and $1.5$. Parallel lines share no points: zero solutions."),
   ["2x+3y=6", "4x+6y=9"])

# ----- SAT Desmos 1, Move 5
ne('P23', '1.5',
   r"$$5x - 2y = 7$$ $$10x + ky = 3$$ In the system above, $k$ is a constant. For what value of $k$ does the system have no solutions?",
   "$k =$", ["-4"],
   given(r"a system with an unknown constant; no solutions means the lines are parallel and different.",
         dz([{'x': r'5x - 2y = 7'}, {'x': r'10x + ky = 3', 'see': 'click <em>add slider: k</em>'}, {'x': r'k = -4', 'see': 'drag until the two lines are parallel'}]) +
         r"Confirm with slopes: $\tfrac{5}{2}$ and $-\tfrac{10}{k}$ match when $k = -4$. Then $10x - 4y = 3$ is not a multiple of $5x - 2y = 7$, so the lines are different."),
   ["5x-2y=7", "10x+ky=3", slider('k', 2, -10, 10, 1)])
ne('P24', '1.5',
   r"$$2x + 5y = 12$$ $$kx + 10y = 24$$ In the system above, $k$ is a constant. For what value of $k$ does the system have infinitely many solutions?",
   "$k =$", ["4"],
   given(r"a system with an unknown constant; infinitely many solutions means both equations describe the same line.",
         dz([{'x': r'2x + 5y = 12'}, {'x': r'kx + 10y = 24', 'see': 'click <em>add slider: k</em>'}, {'x': r'k = 4', 'see': 'drag until the second line sits on top of the first'}]) +
         r"Check: doubling $2x + 5y = 12$ gives $4x + 10y = 24$, so $k = 4$. ✓"),
   ["2x+5y=12", "kx+10y=24", slider('k', 1, -10, 10, 1)])

# ----- SAT Desmos 1, Move 6
ne('P13', '1.6',
   r"$$f(x) = x^2 - 6x + 10$$ The graph of $f$ is translated down $4$ units. How many times does the translated graph intersect the $x$-axis?",
   "Number of intersections $=$", ["2"],
   given(r"$f(x) = x^2 - 6x + 10$; the translated graph is $y = f(x) - 4$.",
         dz([{'x': r'f(x) = x^2 - 6x + 10'}, {'x': r'y = f(x) - 4', 'see': 'the translated parabola crosses the x-axis at two points'}]) +
         r"The vertex of $f$ is $(3, 1)$, above the axis. Moving down $4$ puts the vertex at $(3, -3)$, below the axis, and the parabola opens upward, so it crosses twice."),
   ["f(x)=x^2-6x+10", "y=f(x)-4"])
ne('P14', '1.6',
   r"$$f(x) = -x^2 + 2x + 3$$ The graph of $f$ is translated up $3$ units. What is the maximum value of the translated function?",
   "Maximum $=$", ["7"],
   given(r"$f(x) = -x^2 + 2x + 3$; the translated graph is $y = f(x) + 3$.",
         dz([{'x': r'f(x) = -x^2 + 2x + 3'}, {'x': r'y = f(x) + 3', 'see': 'click the highest point: (1, 7)'}]) +
         r"The vertex of $f$ is $(1, 4)$. Moving up $3$ puts it at $(1, 7)$, so the maximum value is $7$."),
   ["f(x)=-x^2+2x+3", "y=f(x)+3"])
mc('P21', '1.6',
   r"Which of the following is an equation of a line with slope $-2$ and $y$-intercept $6$?",
   ["$x + 2y = 6$", "$2x - y = 6$", "$2x + y = 6$", "$y = 2x + 6$"], 2,
   given(r"the line passes through $(0, 6)$ and falls $2$ for every $1$ to the right.",
         r"Graph the four choices. Only $2x + y = 6$ crosses the $y$-axis at $6$ and slopes downward at that rate. Rewritten, it is $y = -2x + 6$. Without the graph: solve each choice for $y$ and compare the slope and the constant."),
   ["x+2y=6", "2x-y=6", "2x+y=6", "y=2x+6"])
mc('P22', '1.6',
   r"Which of the following is an equation of a line that has an $x$-intercept of $3$ and passes through the point $(6, -4)$?",
   ["$3x + 4y = 12$", "$4x - 3y = 12$", "$3x - 4y = 12$", "$4x + 3y = 12$"], 3,
   given(r"the line passes through $(3, 0)$ and $(6, -4)$.",
         r"Type the point $(6, -4)$, then graph the four choices. $4x + 3y = 12$ passes through the point and crosses the $x$-axis at $3$. Check: $4(6) + 3(-4) = 12$. ✓ Choice B has the right $x$-intercept but does not pass through $(6, -4)$."),
   ["(6,-4)", "3x+4y=12", "4x-3y=12", "3x-4y=12", "4x+3y=12"])

# ----- SAT Desmos 1, Move 7
ne('P19', '1.7',
   r"$$y \le 2x - 1$$ $$y \ge -x + 5$$ The point $(3, y)$ is a solution to the system of inequalities above. What is the greatest possible value of $y$?",
   "$y =$", ["5"],
   given(r"$x = 3$, and the point must lie in both shaded regions.",
         dz([{'x': r'y \le 2x - 1'}, {'x': r'y \ge -x + 5'}, {'x': r'x = 3', 'see': 'along this line, the overlap runs from y = 2 up to y = 5'}]) +
         r"Both boundaries are solid, so the endpoints are solutions. The greatest value is $5$. Check: $5 \le 2(3) - 1 = 5$ and $5 \ge -3 + 5 = 2$. ✓"),
   [r"y\le 2x-1", r"y\ge -x+5", "x=3", window(-2, 8, -2, 9)])
mc('P20', '1.7',
   r"$$y \gt x + 1$$ $$y \lt -2x + 10$$ Which of the following points is a solution to the system of inequalities above?",
   ["$(1, 1)$", "$(2, 4)$", "$(0, 12)$", "$(4, 3)$"], 1,
   given(r"four points; a solution lies where the two shaded regions overlap.",
         dz([{'x': r'y \gt x + 1'}, {'x': r'y \lt -2x + 10', 'see': 'then type the four points: only (2, 4) lands in the overlap'}]) +
         r"Check: $4 \gt 2 + 1$ and $4 \lt -4 + 10$. ✓ The point $(0, 12)$ does not satisfy the second inequality, and $(1, 1)$ and $(4, 3)$ do not satisfy the first."),
   ["y>x+1", "y<-2x+10", "(1,1)", "(2,4)", "(0,12)", "(4,3)", window(-3, 8, -2, 14)])

# ----- SAT Desmos 1, Move 8
ne('P15', '1.8',
   r"The data set $\{4,\ 4,\ 9,\ 11,\ 15,\ 20,\ 21\}$ has mean $m$ and median $d$. What is $m - d$?",
   "$m - d =$", ["1"],
   given(r"seven values; the question asks for the mean minus the median.",
         dz([{'x': MEAN + r'(4, 4, 9, 11, 15, 20, 21)', 'val': '12'}, {'x': MEDIAN + r'(4, 4, 9, 11, 15, 20, 21)', 'val': '11'}]) +
         r"$m - d = 12 - 11 = 1$. By hand: the sum is $84$, so the mean is $\tfrac{84}{7} = 12$, and the fourth of the seven sorted values is $11$."),
   [MEAN + "(4,4,9,11,15,20,21)", MEDIAN + "(4,4,9,11,15,20,21)"])
ne('P16', '1.8',
   r"What is the sum of the mean and the median of the data set $\{6,\ 9,\ 10,\ 10,\ 14,\ 17,\ 22,\ 24\}$?",
   "Sum $=$", ["26"],
   given(r"eight values; the question asks for the mean plus the median.",
         dz([{'x': MEAN + r'(6, 9, 10, 10, 14, 17, 22, 24)', 'val': '14'}, {'x': MEDIAN + r'(6, 9, 10, 10, 14, 17, 22, 24)', 'val': '12'}]) +
         r"$14 + 12 = 26$. By hand: the sum is $112$, so the mean is $\tfrac{112}{8} = 14$. With an even count, the median is the average of the fourth and fifth values: $\tfrac{10 + 14}{2} = 12$."),
   [MEAN + "(6,9,10,10,14,17,22,24)", MEDIAN + "(6,9,10,10,14,17,22,24)"])

# ----- SAT Desmos 1, Move 9
mc('P25', '1.9',
   r"Which equation best approximates the line of best fit for the points $(1, 3)$, $(4, 8)$, $(6, 11)$, and $(10, 18)$?",
   ["$y = 1.7x + 1.3$", "$y = 1.3x + 1.7$", "$y = 2.1x - 0.4$", "$y = 0.6x + 4.5$"], 0,
   given(r"four data points; the question asks for a line $y \approx mx + b$.",
         dz([{'x': r'\text{table: }\ x_1 = 1, 4, 6, 10 \quad y_1 = 3, 8, 11, 18'}, {'x': r'y_1 \sim m x_1 + b', 'out': ['m = 1.66082', 'b = 1.2807'], 'stat': 'R^2 = 0.9993'}]) +
         r"Slope about $1.7$ and intercept about $1.3$: choice A. Choice B has the two numbers swapped; the slope is the number multiplying $x$."),
   [table([1, 4, 6, 10], [3, 8, 11, 18]), r"y_{1}\sim mx_{1}+b", window(-1, 12, -2, 22)])
mc('P26', '1.9',
   r"A line of best fit is drawn through the points $(0, 4)$, $(3, 7)$, $(5, 10)$, and $(8, 12)$. Which of the following best approximates its slope and $y$-intercept?",
   [r"slope $\approx 4.1$, intercept $\approx 1.0$", r"slope $\approx 1.0$, intercept $\approx 4.1$", r"slope $\approx 0.5$, intercept $\approx 4.0$", r"slope $\approx 1.5$, intercept $\approx 2.0$"], 1,
   given(r"four data points; the question asks for the slope and the $y$-intercept of a line of best fit.",
         dz([{'x': r'\text{table: }\ x_1 = 0, 3, 5, 8 \quad y_1 = 4, 7, 10, 12'}, {'x': r'y_1 \sim m x_1 + b', 'out': ['m = 1.02941', 'b = 4.13235'], 'stat': 'R^2 = 0.9804'}]) +
         r"Slope about $1.0$ and intercept about $4.1$: choice B. Choice A has the two numbers swapped."),
   [table([0, 3, 5, 8], [4, 7, 10, 12]), r"y_{1}\sim mx_{1}+b", window(-1, 10, -1, 15)])

# ----- SAT Desmos 2, Move 1
ne('N2', '2.1',
   r"The function $g$ is defined by $g(x) = a \cdot b^{x}$, where $a$ and $b$ are positive constants. If $g(1) = 10$ and $g(3) = 40$, what is the value of $g(5)$?",
   "$g(5) =$", ["160"],
   given(r"an exponential function with two known values; the question asks for a third value.",
         dz([{'x': r'g(x) = a \cdot b^{x}'}, {'x': r'g([1, 3]) \sim [10, 40]', 'out': ['a = 5', 'b = 2'], 'stat': r'\text{RMSE} = 5.18 \times 10^{-15}'}, {'x': r'g(5)', 'val': '160'}]) +
         r"In our check, the RMSE was a tiny number, not exactly zero. That is calculator rounding, and it indicates an exact match. With algebra: $\dfrac{g(3)}{g(1)} = b^2 = 4$, so $b = 2$ because $b$ is positive, $a = 5$, and $g(5) = 5 \cdot 2^{5} = 160$."),
   [r"g(x)=a\cdot b^{x}", r"g([1,3])\sim[10,40]", "g(5)"])
ne('N3', '2.1',
   r"The table shows three values of the quadratic function $f$." + vtab('$x$', ['-1', '1', '2'], '$f(x)$', ['9', '1', '3']) + r"What is the value of $f(4)$?",
   "$f(4) =$", ["19"],
   given(r"three points on a quadratic; the question asks for another value of the function.",
         dz([{'x': r'f(x) = ax^2 + bx + c'}, {'x': r'f([-1, 1, 2]) \sim [9, 1, 3]', 'out': ['a = 2', 'b = -4', 'c = 3'], 'stat': RMSE0}, {'x': r'f(4)', 'val': '19'}]) +
         r"Check: $f(x) = 2x^2 - 4x + 3$ gives $f(-1) = 9$, $f(1) = 1$ and $f(2) = 3$, so $f(4) = 32 - 16 + 3 = 19$. ✓"),
   ["f(x)=ax^2+bx+c", r"f([-1,1,2])\sim[9,1,3]", "f(4)"])

# ----- SAT Desmos 2, Move 2
mc('N4', '2.2',
   r"A student solving $3(p - 2) = 3p + 4$ types $3(p - 2) \sim 3p + 4$. Desmos reports a value for $p$, and the line underneath reads RMSE $= 10$. What does the report indicate?",
   [r"The reported value of $p$ is the solution.", r"The equation has no solution.", r"The equation has infinitely many solutions.", r"The solution is $p = 10$."], 1,
   given(r"a tilde line with an RMSE that is not zero.",
         dz([{'x': r'3(p - 2) \sim 3p + 4', 'out': ['p = 0'], 'stat': r'\text{RMSE} = 10'}]) +
         r"In our check, Desmos reported $p = 0$ with RMSE $= 10$. An RMSE of zero would indicate that the reported value makes the two sides equal. Here the left side is $3p - 6$ and the right side is $3p + 4$: for each value of $p$ they differ by $10$, which is the RMSE in the report. No value of $p$ makes them equal, so the equation has no solution. A graph agrees: $y = 3x - 6$ and $y = 3x + 4$ are parallel lines."),
   [r"3(p-2)\sim 3p+4", "y=3x-6", "y=3x+4"])

# ----- SAT Desmos 2, Move 3
ne('N5', '2.3',
   r"A hardware store sells bolts and washers. Four bolts and three washers cost $\$2.55$. Two bolts and five washers cost $\$2.15$. What is the cost, in dollars, of one bolt?",
   "Cost of one bolt, in dollars $=$", ["0.45", ".45", "9/20"],
   given(r"two purchases with two unknown prices: $b$ for a bolt and $w$ for a washer, in dollars.",
         dz([{'x': r'[4b + 3w,\ 2b + 5w] \sim [2.55,\ 2.15]', 'out': ['b = 0.45', 'w = 0.25'], 'stat': RMSE0}]) +
         r"One bolt costs $\$0.45$. Check: $4(0.45) + 3(0.25) = 1.80 + 0.75 = 2.55$ and $2(0.45) + 5(0.25) = 0.90 + 1.25 = 2.15$. ✓ The question asks for the bolt, not the washer."),
   [r"[4b+3w,2b+5w]\sim[2.55,2.15]"])
ne('N6', '2.3',
   r"Three numbers $a$, $b$ and $c$ have a sum of $32$. The number $a$ is three times $b$, and $c$ is $2$ more than $b$. What is the value of $a$?",
   "$a =$", ["18"],
   given(r"three unknowns and three conditions: $a + b + c = 32$, $a = 3b$ and $c = b + 2$.",
         dz([{'x': r'[a + b + c,\ a - 3b,\ c - b] \sim [32,\ 0,\ 2]', 'out': ['a = 18', 'b = 6', 'c = 8'], 'stat': RMSE0}]) +
         r"$a = 18$. With algebra: substitute $a = 3b$ and $c = b + 2$ into the sum to get $5b + 2 = 32$, so $b = 6$ and $a = 18$. The substitution is short here, so either approach works."),
   [r"[a+b+c,a-3b,c-b]\sim[32,0,2]"])

# ----- SAT Desmos 2, Move 4
ne('N7', '2.4',
   r"$$(x + 4)(x - 7) = x^2 + bx + c$$ In the equation above, $b$ and $c$ are constants, and the equation is true for all values of $x$. What is the value of $b + c$?",
   "$b + c =$", ["-31"],
   given(r"two expressions that agree for all values of $x$; the question asks for $b + c$.",
         dz([{'x': r'x_1 = [1, 2, 3, 4, 5]'}, {'x': r'(x_1 + 4)(x_1 - 7) \sim x_1^2 + b x_1 + c', 'out': ['b = -3', 'c = -28'], 'stat': RMSE0}, {'x': r'b + c', 'val': '-31'}]) +
         r"With algebra: $(x + 4)(x - 7) = x^2 - 7x + 4x - 28$, which simplifies to $x^2 - 3x - 28$. So $b + c = -3 + (-28) = -31$."),
   ["x_{1}=[1,2,3,4,5]", r"(x_{1}+4)(x_{1}-7)\sim x_{1}^{2}+bx_{1}+c", "b+c"])
ne('N8', '2.4',
   r"$$3x^2 + 12x + 5 = 3(x + h)^2 + k$$ In the equation above, $h$ and $k$ are constants, and the equation is true for all values of $x$. What is the value of $k$?",
   "$k =$", ["-7"],
   given(r"a quadratic rewritten in vertex form; the question asks for $k$.",
         dz([{'x': r'x_1 = [1, 2, 3, 4, 5]'}, {'x': r'3x_1^2 + 12x_1 + 5 \sim 3(x_1 + h)^2 + k', 'out': ['h = 2', 'k = -7'], 'stat': RMSE0}]) +
         r"$k = -7$. With algebra: $3(x^2 + 4x) + 5 = 3(x + 2)^2 - 12 + 5$, which simplifies to $3(x + 2)^2 - 7$. Another check: $k$ is the minimum value of the left side, and the graph of $y = 3x^2 + 12x + 5$ has its lowest point at $(-2, -7)$."),
   ["x_{1}=[1,2,3,4,5]", r"3x_{1}^{2}+12x_{1}+5\sim 3(x_{1}+h)^{2}+k"])

# ----- SAT Desmos 2, Move 5
ne('N9', '2.5',
   r"$$y = x^2 - 2x + 5$$ $$y = 3x + c$$ In the system above, $c$ is a constant. The system has exactly one solution. What is the value of $c$?",
   "$c =$", ["-5/4", "-1.25"],
   given(r"a parabola and a line; exactly one solution means the line touches the parabola.",
         r"Set the equations equal and move every term to one side: $x^2 - 2x + 5 = 3x + c$ becomes $x^2 - 5x + (5 - c) = 0$. There is one solution when the discriminant is zero." +
         dz([{'x': r'(-5)^2 - 4(1)(5 - c) \sim 0', 'out': ['c = -1.25'], 'stat': RMSE0}], cap='Type this in a blank graph') +
         r"By hand: $25 - 20 + 4c = 0$, so $c = -\tfrac{5}{4}$. A slider for $c$ shows the line touching the curve between $c = -2$ and $c = -1$, so a slider that moves in whole steps passes over the answer."),
   ["y=x^2-2x+5", "y=3x+c", slider('c', -3, -10, 10, 0.25), window(-3, 8, -2, 16)])

# ----- SAT Desmos 2, Move 6
ne('P9', '2.6',
   r"How many times does the circle $(x - 2)^2 + (y - 3)^2 = 9$ intersect the $x$-axis?",
   "Number of intersections $=$", ["1"],
   given(r"a circle with center $(2, 3)$ and radius $3$.",
         dz([{'x': r'(x - 2)^2 + (y - 3)^2 = 9', 'see': 'click the circle: the bottom dot is (2, 0)'}]) +
         r"The lowest point of the circle is at $y = 3 - 3 = 0$, which is on the $x$-axis. The circle touches the axis at one point, $(2, 0)$."),
   ["(x-2)^2+(y-3)^2=9", window(-4, 8, -2, 8)])
ne('P10', '2.6',
   r"How many times does the graph of $(x + 2)^2 + (y - 1)^2 = 25$ intersect the $x$-axis?",
   "Number of intersections $=$", ["2"],
   given(r"a circle with center $(-2, 1)$ and radius $5$.",
         dz([{'x': r'(x + 2)^2 + (y - 1)^2 = 25', 'see': 'the circle crosses the x-axis at two points'}]) +
         r"The center is $1$ unit above the axis and the radius is $5$, so the circle extends below the axis and crosses it twice, at $x \approx 2.90$ and $x \approx -6.90$."),
   ["(x+2)^2+(y-1)^2=25", window(-10, 6, -6, 8)])

# ----- SAT Desmos 2, Move 7
ne('N10', '2.7',
   r"The table shows the scores of $20$ students on a quiz." + vtab('Score', ['2', '3', '4', '5', '6'], 'Students', ['3', '5', '6', '4', '2']) + r"What is the mean score?",
   "Mean $=$", ["3.85", "77/20"],
   given(r"a frequency table: five scores and the number of students with each score.",
         dz([{'x': r'v = [2, 3, 4, 5, 6]'}, {'x': r'n = [3, 5, 6, 4, 2]'}, {'x': r'\dfrac{' + TOTAL + r'(v \cdot n)}{' + TOTAL + r'(n)}', 'val': '3.85'}]) +
         r"By hand: $\dfrac{6 + 15 + 24 + 20 + 12}{20} = \dfrac{77}{20} = 3.85$. Averaging the five scores without their counts gives $4$, which is a different question."),
   ["v=[2,3,4,5,6]", "n=[3,5,6,4,2]", r"\frac{" + TOTAL + r"(v\cdot n)}{" + TOTAL + r"(n)}"])

# ----- SAT Desmos 2, Move 8
ne('N11', '2.8',
   r"In right triangle $ABC$, angle $C$ is the right angle, the hypotenuse $AB$ has length $20$, and the measure of angle $A$ is $35^\circ$. What is the length of side $BC$, to the nearest tenth?",
   r"$BC \approx$", ["11.5", "11.47", "11.472"],
   given(r"hypotenuse $20$ and angle $A = 35^\circ$; side $BC$ is opposite angle $A$.",
         r"$\sin(35^\circ) = \dfrac{BC}{20}$, so $BC = 20 \sin(35^\circ)$." +
         dz([{'x': r'20 \sin(35)', 'val': '11.4715', 'see': 'in degree mode: wrench, then Degrees'}]) +
         r"To the nearest tenth, $BC \approx 11.5$. In radian mode the same entry shows about $-8.56$. A negative length is a sign to check the mode."),
   [DEGREES, r"20\sin(35)"])

CHALLENGE = BY_MOVE
N_MOVE = len(CHALLENGE)

# ---------------------------------------------------------------- TAB 2: SKILL PRACTICE
FLUENCY = [
 {"sec": "A. Desmos or algebra?", "items": [
   {"mc": True, "q": r"$5x - 8 = 27$. Which approach is likely to be quickest here?",
    "opts": [r"Graph $y = 5x - 8$ and $y = 27$, then click the crossing", r"Add $8$ to both sides, then divide by $5$", "Type the equation with a tilde", r"Add a slider for $x$"], "correct": 1,
    "exp": r"Two steps of algebra give $x = 7$. Graphing both sides also works, but it is more typing than the two algebra steps. Use Desmos when it helps; for simpler questions, algebra may be quicker."},
   {"mc": True, "q": r"How many solutions does $|4x - 5| = 3x + 9$ have? A practical first step is to",
    "opts": [r"add a slider for $x$", "type the equation with a tilde and read RMSE", r"graph $y = |4x - 5|$ and $y = 3x + 9$, then count the crossings", "switch to degree mode"], "correct": 2,
    "exp": r"The graphs cross at two points, $x = -\tfrac{4}{7}$ and $x = 14$, so there are two solutions. A tilde line reports one value at a time, so it is not a reliable way to count. With algebra: solve $4x - 5 = 3x + 9$ and $4x - 5 = -(3x + 9)$, then check each result in the original equation."},
   {"mc": True, "q": r"What is the $y$-intercept of the graph of $y = 4x^2 - 9x + 6$? The most direct route is to",
    "opts": ["read the constant term", r"graph it and click the dot on the $y$-axis", "use the quadratic formula", "type it with a tilde"], "correct": 0,
    "exp": r"At $x = 0$ the first two terms are zero, so $y = 6$. Graphing and clicking the dot on the $y$-axis gives the same value; reading the constant is quicker."},
   {"mc": True, "q": r"An exponential function $f$ has $f(2) = 20$ and $f(4) = 80$, and the question asks for $f(7)$. Which entry fits?",
    "opts": ['$' + MEAN + '(20, 80)$', r"$y = 20$ and $y = 80$ on two lines", r"a slider for $x$ from $2$ to $7$", r"$f(x) = a \cdot b^{x}$, then $f([2, 4]) \sim [20, 80]$"], "correct": 3,
    "exp": r"This is SAT Desmos 2, Move 1. In our check, Desmos reported $a = 5$ and $b = 2$, and $f(7)$ showed $640$. With algebra: $b^2 = \tfrac{80}{20} = 4$, so $b = 2$ and $a = 5$, and $f(7) = 5 \cdot 2^{7} = 640$."},
 ]},
 {"sec": "B. Which move fits?", "items": [
   {"mc": True, "q": r"$$2x - 3y = 4$$ $$6x + ky = 9$$ The system has no solution, and the question asks for $k$. Which move fits?",
    "opts": ["Read the gray dots on the first line", r"Slide $k$ until the lines are parallel, then confirm with slopes", "Shade both equations as inequalities", "Use mean() on the coefficients"], "correct": 1,
    "exp": r"SAT Desmos 1, Move 5. The lines are parallel when the slopes match: $\tfrac{2}{3} = -\tfrac{6}{k}$, so $k = -9$. At $k = -9$ the second equation is $6x - 9y = 9$, which is not a multiple of the first, so the lines are different and the system has no solution."},
   {"mc": True, "q": r"Which expression is equivalent to $(3x - 2)(x + 5)$? The question gives four choices. Which move fits?",
    "opts": ["Graph the original and each choice, and look for the choice whose graph matches the original", r"Click the $x$-intercepts and add them", "Switch to degree mode", "Type the expression as an inequality"], "correct": 0,
    "exp": r"SAT Desmos 1, Move 6. An equivalent expression has the same graph as the original. Expanding works too: $(3x - 2)(x + 5) = 3x^2 + 13x - 10$."},
   {"mc": True, "q": r"A question lists five data points and asks which equation is closest to the line of best fit. Which move fits?",
    "opts": [r"Graph each choice and count its $x$-intercepts", r"Type mean() of the $x$-values", r"Enter the points in a table, then type $y_1 \sim m x_1 + b$", "Add a slider for the slope and stop when it looks close"], "correct": 2,
    "exp": r"SAT Desmos 1, Move 9. The report gives the slope $m$ and the $y$-intercept $b$, which you can compare with the choices."},
   {"mc": True, "q": r"The graph of $x^2 + y^2 + 8x - 2y = 19$ is a circle, and the question asks for its radius. Which move fits?",
    "opts": ["Type it with a tilde and read RMSE", "Use median() on the coefficients", "Slide a constant until the circle disappears", "Type it as printed, click the circle, and take half the distance between the top and bottom dots"], "correct": 3,
    "exp": r"SAT Desmos 2, Move 6. The top dot is $(-4, 7)$ and the bottom dot is $(-4, -5)$, so the diameter is $12$ and the radius is $6$. Completing the square agrees: $(x + 4)^2 + (y - 1)^2 = 36$."},
 ]},
 {"sec": "C. What would you type?", "items": [
   {"mc": True, "q": r"Which entry graphs $y = \dfrac{2}{3}x + 1$?",
    "opts": [kbd('y=2/3x+1'), kbd('y=2/3', '&rarr;', 'x+1'), kbd('y=2/(3x+1)'), kbd('y=2/3x', '&rarr;', '+1')], "correct": 1,
    "exp": r"After the slash, what you type stays in the denominator until you press the right arrow. Type 2 / 3, press the arrow, then type $x + 1$. The first entry graphs $y = \dfrac{2}{3x + 1}$."},
   {"mc": True, "q": r"A quadratic function $f$ passes through $(0, 5)$, $(1, 4)$ and $(3, 14)$. After you define $f(x) = ax^2 + bx + c$, which line asks Desmos to find $a$, $b$ and $c$?",
    "opts": [r"$f([5, 4, 14]) \sim [0, 1, 3]$", r"$f([0, 1, 3]) = [5, 4, 14]$", r"$f([0, 1, 3]) \sim [5, 4, 14]$", r"$f(0, 1, 3) \sim (5, 4, 14)$"], "correct": 2,
    "exp": r"Inputs go in the first brackets and their outputs go in the second, in the same order, with a tilde between them. In our check, Desmos reported $a = 2$, $b = -3$ and $c = 5$ with RMSE $= 0$. With an equals sign in place of the tilde, Desmos did not report any values."},
   {"q": r"A frequency table has the values $v = [1, 2, 3]$ with counts $n = [5, 3, 2]$. You type $\dfrac{" + TOTAL + r"(v \cdot n)}{" + TOTAL + r"(n)}$. Desmos shows", "accept": ["1.7", "17/10"],
    "exp": r"Each value times its count, added up: $5 + 6 + 6 = 17$. Divide by the total count, $10$: the mean is $1.7$."},
   {"q": r"With the calculator in degree mode, you type $12\tan(40)$. To the nearest hundredth, Desmos shows", "accept": ["10.07", "10.069"],
    "exp": r"$12 \tan(40^\circ) \approx 10.07$. In radian mode the same entry shows about $-13.41$, so check the mode in the wrench menu before you enter a trig expression."},
 ]},
 {"sec": "D. Read what Desmos reports", "items": [
   {"mc": True, "q": r"A table fit $y_1 \sim m x_1 + b$ reports $m = 2.5$ and $b = -1.2$. Which equation is the line of best fit?",
    "opts": ["$y = -1.2x + 2.5$", "$y = 2.5x - 1.2$", "$y = 2.5x + 1.2$", "$y = 1.2x - 2.5$"], "correct": 1,
    "exp": r"$m$ multiplies $x$, so it is the slope, and $b$ is the $y$-intercept: $y = 2.5x - 1.2$."},
   {"q": r"You define $f(x) = a \cdot b^{x}$, and a tilde line reports $a = 2$ and $b = 3$. What is $f(4)$?", "accept": ["162"],
    "exp": r"$f(4) = 2 \cdot 3^{4} = 2 \cdot 81 = 162$. After a fit, the letters keep their fitted values, so typing $f(4)$ on a new line shows the same number."},
   {"q": r"You type $x^2 - 2x - 15 = 0$, and Desmos draws vertical lines at $x = -3$ and $x = 5$. The question asks for the sum of the solutions. The sum is", "accept": ["2"],
    "exp": r"$-3 + 5 = 2$. Each vertical line marks one solution, and the question asks for their sum. Check: $(x + 3)(x - 5) = x^2 - 2x - 15$."},
   {"q": r"You click a circle, and Desmos shows dots at $(3, 9)$ and $(3, -1)$: its top and its bottom. The radius is", "accept": ["5"],
    "exp": r"Top to bottom is $9 - (-1) = 10$, the diameter. The radius is half of that, $5$, and the center is halfway between the dots, at $(3, 4)$."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: TIMED PRACTICE SET
G8_FIG = SOURCE['timed'][7]['figure']
assert G8_FIG.startswith('<svg') and '$' not in G8_FIG


def both(g, desmos_way, other_way, other='With algebra'):
    return ('<strong>Given:</strong> ' + g + '<br><br><strong>In Desmos:</strong> ' + desmos_way +
            '<br><br><strong>' + other + ':</strong> ' + other_way)


GAUNTLET = [
 {"ess": False, "type": "mc", "diff": "Easy",
  "stem": r"A movie theater sold a total of $240$ tickets to a showing. Adult tickets cost $\$12$ each and child tickets cost $\$8$ each, and the theater collected $\$2{,}480$ from the sale. How many child tickets were sold?",
  "options": ["$100$", "$120$", "$140$", "$160$"], "correct": 0, "desmos": ["x+y=240", "12x+8y=2480", window(-20, 280, -20, 340)],
  "sol": both(r"$240$ tickets in total; $\$12$ for each adult ticket and $\$8$ for each child ticket; $\$2{,}480$ collected.",
              r"Let $x$ be the adult tickets and $y$ the child tickets." + dz([{'x': r'x + y = 240'}, {'x': r'12x + 8y = 2480', 'see': 'zoom out, then click the crossing: (140, 100)'}]) + r"The question asks for child tickets, the $y$-value: $100$.",
              r"$a + c = 240$ and $12a + 8c = 2480$. Substitute $a = 240 - c$: $2880 - 4c = 2480$, so $c = 100$."),
  "trap": r"Label your variables before you read the point. Here $x = 140$ is the number of adult tickets, and $140$ is one of the choices. The question asks for child tickets."},
 {"ess": False, "type": "ne", "diff": "Easy",
  "stem": r"A ball is thrown upward from a platform. The height of the ball above the ground, in feet, $t$ seconds after it is thrown is given by the function $h(t) = -16t^2 + 48t + 64$. How many seconds after it is thrown does the ball hit the ground?",
  "label": "Seconds $=$", "accept": ["4"], "desmos": ["y=-16x^2+48x+64", window(-2, 6, -20, 120)],
  "sol": both(r"$h(t) = -16t^2 + 48t + 64$; the ball hits the ground when the height is $0$.",
              r"Use $x$ in place of $t$." + dz([{'x': r'y = -16x^2 + 48x + 64', 'see': 'zoom out, then click the right-hand dot on the x-axis: (4, 0)'}]) + r"The other intercept, $x = -1$, is before the throw, so it does not answer the question.",
              r"Set $h(t) = 0$: $-16(t^2 - 3t - 4) = 0$, so $(t - 4)(t + 1) = 0$. Time is positive, so $t = 4$."),
  "trap": r"A graph can show more than the situation allows. Time starts at $t = 0$, so use the positive intercept."},
 {"ess": False, "type": "mc", "diff": "Easy",
  "stem": r"The table shows the number of pets owned by each of $20$ households in a survey." + vtab('Number of pets', ['0', '1', '2', '3'], 'Number of households', ['6', '8', '4', '2']) + r"What is the mean number of pets per household for the $20$ households?",
  "options": ["$1.0$", "$1.1$", "$1.5$", "$2.0$"], "correct": 1,
  "desmos": ["v=[0,1,2,3]", "n=[6,8,4,2]", r"\frac{" + TOTAL + r"(v\cdot n)}{" + TOTAL + r"(n)}"],
  "sol": both(r"a frequency table: four values and the number of households with each value.",
              dz([{'x': r'v = [0, 1, 2, 3]'}, {'x': r'n = [6, 8, 4, 2]'}, {'x': r'\dfrac{' + TOTAL + r'(v \cdot n)}{' + TOTAL + r'(n)}', 'val': '1.1'}]),
              r"The total number of pets is $0 + 8 + 8 + 6 = 22$ across $20$ households, so the mean is $\dfrac{22}{20} = 1.1$."),
  "trap": r"Weight each value by its count. Averaging the four values $0$, $1$, $2$, $3$ gives $1.5$, which leaves out how many households have each number of pets."},
 {"ess": False, "type": "ne", "diff": "Easy",
  "stem": r"A gym charges members a fixed monthly fee plus a constant charge for each visit. One member who visited $6$ times in a month was charged $\$57$, and another member who visited $11$ times in the same month was charged $\$77$. What is the fixed monthly fee, in dollars?",
  "label": "Fixed monthly fee $=$", "accept": ["33", "33.00"], "desmos": [table([6, 11], [57, 77]), r"y_{1}\sim mx_{1}+b", window(-2, 14, -10, 100)],
  "sol": both(r"a linear cost: $6$ visits cost $\$57$ and $11$ visits cost $\$77$.",
              dz([{'x': r'\text{table: }\ x_1 = 6, 11 \quad y_1 = 57, 77'}, {'x': r'y_1 \sim m x_1 + b', 'out': ['m = 4', 'b = 33'], 'stat': 'R^2 = 1'}]) + r"The intercept $b$ is the charge with zero visits: the monthly fee, $\$33$.",
              r"The charge per visit is $\dfrac{77 - 57}{11 - 6} = 4$ dollars. Then $57 - 6(4) = 33$."),
  "trap": r"The report gives two numbers. $m = 4$ is the charge per visit; the question asks for the fixed fee, $b = 33$."},
 {"ess": False, "type": "mc", "diff": "Easy",
  "stem": r"In the $xy$-plane, a circle has center $(-4, 6)$, and the point $(-4, 1)$ lies on the circle. Which equation represents the circle?",
  "options": ["$(x + 4)^2 + (y - 6)^2 = 25$", "$(x - 4)^2 + (y + 6)^2 = 25$", "$(x + 4)^2 + (y - 6)^2 = 5$", "$(x - 4)^2 + (y + 6)^2 = 5$"], "correct": 0,
  "desmos": ["(-4,6)", "(-4,1)", "(x+4)^2+(y-6)^2=25", window(-14, 6, -2, 14)],
  "sol": both(r"center $(-4, 6)$; the point $(-4, 1)$ is on the circle.",
              r"Type the points $(-4, 6)$ and $(-4, 1)$, then graph the choices. Choice A draws a circle that is centered on the first point and passes through the second.",
              r"The radius is the distance from $(-4, 6)$ to $(-4, 1)$, which is $5$, so $r^2 = 25$. In $(x - h)^2 + (y - k)^2 = r^2$, the center $(-4, 6)$ gives $(x + 4)^2 + (y - 6)^2 = 25$."),
  "trap": r"Two things to check in $(x - h)^2 + (y - k)^2 = r^2$: the signs inside the parentheses are the opposite of the center’s coordinates, and the right side is the radius squared, $25$, not $5$."},
 {"ess": False, "type": "ne", "diff": "Medium",
  "stem": r"The function $f$ is linear. If $f(2) = 7$ and $f(5) = 16$, what is the value of $f(10)$?",
  "label": "$f(10) =$", "accept": ["31"], "desmos": ["f(x)=mx+b", r"f([2,5])\sim[7,16]", "f(10)"],
  "sol": both(r"a linear function with $f(2) = 7$ and $f(5) = 16$.",
              dz([{'x': r'f(x) = mx + b'}, {'x': r'f([2, 5]) \sim [7, 16]', 'out': ['m = 3', 'b = 1'], 'stat': RMSE0}, {'x': r'f(10)', 'val': '31'}]),
              r"The slope is $\dfrac{16 - 7}{5 - 2} = 3$, so $f(x) = 3x + b$ with $7 = 6 + b$, which gives $b = 1$. Then $f(10) = 31$."),
  "trap": r"The fitted $m$ and $b$ are steps on the way. The question asks for $f(10)$, so evaluate the function before you enter an answer."},
 {"ess": False, "type": "mc", "diff": "Medium",
  "stem": r"A car was purchased for $\$24{,}000$. The value of the car decreases by $15\%$ each year after the purchase. According to this model, what is the least whole number of years after the purchase at which the value of the car will be less than half of the purchase price?",
  "options": ["$3$", "$4$", "$5$", "$6$"], "correct": 2, "desmos": ["y=24000(0.85)^x", "y=12000", window(-1, 10, -2000, 26000)],
  "sol": both(r"a starting value of $\$24{,}000$ that is multiplied by $0.85$ each year; half of the purchase price is $\$12{,}000$.",
              dz([{'x': r'y = 24000(0.85)^{x}'}, {'x': r'y = 12000', 'see': 'set the window to x from 0 to 10 and y from 0 to 25,000; the graphs cross at about x = 4.27'}]) + r"After $4$ years the value is still above half. After $5$ years it is below.",
              r"$24000(0.85)^{t} \lt 12000$ means $0.85^{t} \lt 0.5$. Check: $0.85^{4} \approx 0.522$, which is not yet below $0.5$, and $0.85^{5} \approx 0.444$. So $5$ years."),
  "trap": r"The crossing is at about $4.27$ years. The question asks for a whole number of years, so round up to $5$: at $4$ years the value is still above half."},
 {"ess": False, "type": "mc", "diff": "Medium",
  "stem": r"The scatterplot shows the daily ice cream sales, in dollars, at a shop on five days and the high temperature, in degrees Celsius, on each of those days. A line of best fit is also shown." + G8_FIG + r"Based on the line of best fit, which of the following is closest to the predicted sales, in dollars, on a day with a high temperature of $30^{\circ}$C?",
  "options": ["$350$", "$358$", "$364$", "$376$"], "correct": 2,
  "desmos": [table([20, 22, 25, 27, 29], [240, 265, 300, 330, 350]), r"y_{1}\sim mx_{1}+b", r"m\cdot 30+b", window(16, 34, 200, 420)],
  "sol": both(r"five data points, read from the graph: $(20, 240)$, $(22, 265)$, $(25, 300)$, $(27, 330)$ and $(29, 350)$.",
              dz([{'x': r'\text{table: }\ x_1 = 20, 22, 25, 27, 29', 'see': 'second column, y<sub>1</sub>: 240, 265, 300, 330, 350'}, {'x': r'y_1 \sim m x_1 + b', 'out': [r'm \approx 12.387', r'b \approx -7.726'], 'stat': 'R^2 = 0.9979'}, {'x': r'm \cdot 30 + b', 'see': 'shows about 363.89'}]) + r"The closest choice is $364$. Reading the drawn line at $30$ by eye gives about the same answer; the fitted line gives a more precise reading.",
              r"The line rises about $12$ dollars per degree, from $240$ at $20^{\circ}$ to about $350$ at $29^{\circ}$. One degree past the last point: $350 + 12 \approx 362$, so $364$ is the closest choice.", other='From the graph'),
  "trap": r"A prediction is read from the line, not from the nearest data point. At $29^{\circ}$C the line is near $350$; at $30^{\circ}$C it is about $12$ higher."},
 {"ess": False, "type": "mc", "diff": "Medium",
  "stem": r"Which of the following expressions is equivalent to $(x + 3)(x - 5) + 2(x - 1)$?",
  "options": ["$x^2 - 17$", "$x^2 - 4x - 17$", "$x^2 + 2x - 13$", "$x^2 - 2x - 17$"], "correct": 0,
  "desmos": ["y=(x+3)(x-5)+2(x-1)", "y=x^2-17", window(-8, 8, -20, 12)],
  "sol": both(r"an expression and four possible rewrites.",
              dz([{'x': r'y = (x + 3)(x - 5) + 2(x - 1)'}, {'x': r'y = x^2 - 17', 'see': 'choice A sits on top of the original; the other three choices do not'}]),
              r"$(x + 3)(x - 5) = x^2 - 2x - 15$ and $2(x - 1) = 2x - 2$. Adding: $x^2 - 2x - 15 + 2x - 2 = x^2 - 17$."),
  "trap": r"Two matching curves look like one. Click the colored circle beside a line to hide and show that curve, so you can confirm that both graphs are there."},
 {"ess": False, "type": "ne", "diff": "Medium",
  "stem": r"A delivery driver is paid $\$18$ per hour plus $\$4$ for each delivery completed. The driver works $7$ hours in one day and wants to earn at least $\$200$ that day. What is the minimum number of deliveries the driver must complete?",
  "label": "Deliveries $=$", "accept": ["19"], "desmos": ["y=18(7)+4x", "y=200", window(-2, 30, -20, 260)],
  "sol": both(r"$\$18$ per hour for $7$ hours, plus $\$4$ per delivery; the total must be at least $\$200$.",
              dz([{'x': r'y = 18(7) + 4x'}, {'x': r'y = 200', 'see': 'zoom out, then click the crossing: (18.5, 200)'}]) + r"Deliveries are whole numbers and the pay must reach at least $\$200$, so round up to $19$.",
              r"$126 + 4d \ge 200$ gives $4d \ge 74$, so $d \ge 18.5$. The smallest whole number is $19$. With $18$ deliveries the pay is $\$198$."),
  "trap": r"Rounding $18.5$ down to $18$ gives $\$198$, which is short of $\$200$. Substitute your answer back into the situation to check the direction of the rounding."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"The equation $2x^2 + bx + 8 = 0$, where $b$ is a positive constant, has exactly one solution. What is the value of $b$?",
  "label": "$b =$", "accept": ["8"], "desmos": ["y=2x^2+bx+8", slider('b', 3, -12, 12, 1), window(-8, 8, -6, 20)],
  "sol": both(r"a quadratic equation with an unknown positive constant $b$ and exactly one solution.",
              dz([{'x': r'y = 2x^2 + bx + 8', 'see': 'click <em>add slider: b</em>'}, {'x': r'b = 8', 'see': 'drag until the parabola touches the x-axis at one point'}]) + r"The parabola also touches the axis at $b = -8$, which the question excludes because $b$ is positive.",
              r"One solution means the discriminant is zero: $b^2 - 4(2)(8) = 0$, so $b^2 = 64$ and $b = 8$, since $b \gt 0$."),
  "trap": r"Two values make the parabola touch the axis, $8$ and $-8$. The question states that $b$ is positive, so reread the conditions before you enter the answer."},
 {"ess": False, "type": "mc", "diff": "Hard",
  "stem": r"The function $A(t) = 300(2)^{t/5}$ models the value, in dollars, of an investment $t$ years after it was made. Which of the following is closest to the percent increase in the value of the investment each year, according to the model?",
  "options": [r"$5\%$", r"$15\%$", r"$20\%$", r"$40\%$"], "correct": 1, "desmos": [r"2^{\frac{1}{5}}"],
  "sol": both(r"$A(t) = 300(2)^{t/5}$; the question asks for the percent increase from one year to the next.",
              r"Rewrite the growth factor for one year: $2^{t/5} = \left(2^{1/5}\right)^{t}$." + dz([{'x': r'2^{1/5}', 'val': '1.1487'}]) + r"A yearly factor of about $1.149$ is an increase of about $14.9\%$, which is closest to $15\%$.",
              r"Each year multiplies the value by $2^{1/5} \approx 1.149$, an increase of about $14.9\%$. The closest choice is $15\%$."),
  "trap": r"The value doubles in $5$ years, which can suggest $100\% \div 5 = 20\%$ per year. Growth compounds, so the yearly factor is $2^{1/5} \approx 1.149$, not $1.2$."},
 {"ess": False, "type": "mc", "diff": "Hard",
  "stem": r"In the $xy$-plane, the graph of $x^2 + y^2 - 6x + 4y = 12$ is a circle. How many points do the circle and the line $y = x - 1$ have in common?",
  "options": ["Zero", "Exactly one", "Exactly two", "More than two"], "correct": 2,
  "desmos": ["x^2+y^2-6x+4y=12", "y=x-1", window(-9, 15, -9, 5)],
  "sol": both(r"a circle in expanded form and a line.",
              dz([{'x': r'x^2 + y^2 - 6x + 4y = 12'}, {'x': r'y = x - 1', 'see': 'the line crosses the circle at two points'}]) + r"Desmos can graph the circle in this form, so you do not need to complete the square first.",
              r"Complete the square: $(x - 3)^2 + (y + 2)^2 = 25$, a circle with center $(3, -2)$ and radius $5$. The distance from the center to the line $x - y - 1 = 0$ is $\dfrac{|3 + 2 - 1|}{\sqrt{2}} \approx 2.83$, which is less than $5$, so the line crosses the circle twice."),
  "trap": r"A line and a circle share zero, one or two points. If a line looks as if it only touches the circle, zoom in before you choose “exactly one.”"},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"In the $xy$-plane, the graphs of $y = |x - 3| + 1$ and $y = 5$ intersect at two points. What is the area of the triangle formed by those two points and the vertex of the graph of $y = |x - 3| + 1$?",
  "label": "Area $=$", "accept": ["16"], "desmos": [r"y=\left|x-3\right|+1", "y=5", window(-4, 10, -1, 8)],
  "sol": both(r"a V-shaped graph and a horizontal line; the triangle has its corners at the two crossings and the vertex of the V.",
              dz([{'x': r'y = |x - 3| + 1', 'see': 'lowest point: (3, 1)'}, {'x': r'y = 5', 'see': 'crossings at (&minus;1, 5) and (7, 5)'}]) + r"The base along $y = 5$ is $7 - (-1) = 8$, and the height down to the vertex is $5 - 1 = 4$. The area is $\tfrac{1}{2}(8)(4) = 16$.",
              r"$|x - 3| + 1 = 5$ gives $|x - 3| = 4$, so $x = 7$ or $x = -1$. The base is $8$, the height is $4$, and the area is $16$."),
  "trap": r"The graph gives the three points; the area still comes from $\tfrac{1}{2} \cdot \text{base} \cdot \text{height}$. Entering the base, $8$, or the product $32$ leaves the question unfinished."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"$$y = x^2 + 4x + k$$ $$y = 2x + 1$$ In the given system of equations, $k$ is a constant. The system has exactly one solution. What is the value of $k$?",
  "label": "$k =$", "accept": ["2"], "desmos": ["y=x^2+4x+k", "y=2x+1", slider('k', 5, -10, 10, 1), window(-8, 6, -6, 12)],
  "sol": both(r"a parabola with an unknown constant and a line; exactly one solution means the line touches the parabola.",
              dz([{'x': r'y = x^2 + 4x + k', 'see': 'click <em>add slider: k</em>'}, {'x': r'y = 2x + 1'}, {'x': r'k = 2', 'see': 'drag until the line touches the parabola at one point'}]),
              r"Set the equations equal: $x^2 + 4x + k = 2x + 1$ becomes $x^2 + 2x + (k - 1) = 0$. There is one solution when the discriminant is zero: $4 - 4(k - 1) = 0$, so $k = 2$."),
  "trap": r"Move every term to one side before you use the discriminant. The quadratic to test is $x^2 + 2x + (k - 1) = 0$. Testing $x^2 + 4x + k$ by itself gives $k = 4$, which answers a different question."},
]
TIMED_IDS = ['G%d' % i for i in range(1, len(GAUNTLET) + 1)]

# ---------------------------------------------------------------- TAB 5: EXIT TICKET
EXIT = [
 {"q": r"A system of two linear equations has an unknown constant $k$, and the question asks for the value of $k$ that gives no solution. Which approach fits?",
  "opts": [r"Click the crossing and read its $y$-coordinate", r"Slide $k$ until the lines are parallel, then confirm with slopes", "Use mean() and median()", "Switch to degree mode"], "correct": 1,
  "exp": r"No solution means the lines are parallel and different. A slider shows roughly where that happens, and equal slopes confirm the value (SAT Desmos 1, Move 5)."},
 {"q": r"A tilde line reports $k = 3$ with RMSE $= 0$. What does the report indicate?",
  "opts": ["The equation has no solution", r"$k = 3$ makes the two sides match", r"$k = 3$ is the only value that works", "The calculator is in radian mode"], "correct": 1,
  "exp": r"An RMSE of zero indicates an exact match at $k = 3$. It does not show whether another value also works: when two solutions are possible, graph the equation and count (SAT Desmos 2, Move 2)."},
 {"q": r"Desmos shows a crossing at $(6, -2)$, and the question asks for the value of $x + y$. The answer is",
  "opts": ["$6$", "$-2$", "$8$", "$4$"], "correct": 3,
  "exp": r"$6 + (-2) = 4$. Finding the point is one step. Check what the question asks you to do with it."},
]

# ---------------------------------------------------------------- TAB 1: START HERE
COUNTS = collections.Counter(BY_MOVE_KEYS)
assert set(COUNTS) == set(MOVES), 'every move needs at least one question'


def link(url, text):
    return '<a href="' + url + '" ' + A_STYLE + '>' + text + '</a>'


def index_table(sheet):
    rows = ''
    for k, m in MOVES.items():
        if m['sheet'] != sheet:
            continue
        rows += ('<tr><td class="fname">' + (STAR + '&nbsp;' if m['ess'] else '') + 'Move %d</td>' % m['n'] +
                 '<td><strong>' + m['name'] + '</strong><br><span style="font-size:15px; color:var(--text-medium);">when the question ' + m['when'] + '</span></td>' +
                 '<td style="text-align:center;">%d</td></tr>\n' % COUNTS[k])
    return ('<div class="tbl-wrap"><table class="cases"><thead><tr><th>Move</th><th>Name, and when to reach for it</th><th>In tab 3</th></tr></thead><tbody>\n' +
            rows + '</tbody></table></div>\n')


N_QUICK = sum(len(s['items']) for s in FLUENCY)


def how(label, text):
    return '<div class="frow"><div class="flabel">' + label + '</div><div class="fmath" style="font-size:16.5px;">' + text + '</div></div>\n'

NUMBER_WORD = {10: 'Ten', 12: 'Twelve', 15: 'Fifteen', 16: 'Sixteen', 20: 'Twenty'}
RULES = (r'''
<p class="ref-intro">This sheet is practice only: it has no new moves. It gathers questions for the ''' + str(len(MOVES)) + r''' moves taught in SAT Desmos 1: Core Moves and SAT Desmos 2: Next Steps, so you can practice choosing a move as well as using one. As you practice, start by identifying the question type. Then decide whether Desmos or algebra makes more sense, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the skills you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred skills.</span></div>
<div class="ref-rule"><div class="ref-rule-line"><span class="rtag">Plan</span><span class="rname">How this sheet works</span></div>
<div class="fbox">
''' + how('2. Skill Practice', str(N_QUICK) + r' quick questions: choose an approach, pick a move, decide what to type, and read what Desmos reports. A good warm-up, or a short session by itself.') +
    how('3. Practice by Move', str(N_MOVE) + r' questions grouped by move. Check each one right away and read the worked solution. Use the switch to shuffle the questions when you want to practice identifying the move.') +
    how('4. Timed Practice Set', str(len(GAUNTLET)) + r' mixed SAT-style questions, scored at the end, with an optional timer. A good choice when you want a longer mixed set.') +
    how('5. Exit Ticket', str(len(EXIT)) + r' questions, and one sentence in your own words, for the end of a session.') + r'''</div>
<div class="ref-ex"><span class="exlab">Calculator</span>The Calculator button opens Desmos on this page. Type each line yourself. After you check an answer, <em>Load into Desmos</em> loads the lines from the solution so you can compare them with your own.</div>
<div class="ref-ex"><span class="exlab">Lessons</span>If a move feels unfamiliar, open its lesson first. Each solution in tab 3 ends with a link to the move it uses.</div>
<div class="ref-ex"><span class="exlab">Answer entry</span>For practice entering student-produced responses, use the Bluebook Tools tab in ''' + link(D1_URL, 'SAT Desmos 1: Core Moves') + r'''.</div>
</div>
<div class="ref-rule"><div class="ref-rule-line"><span class="rtag">Index</span><span class="rname">The moves from ''' + link(D1_URL, 'SAT Desmos 1: Core Moves &#8594;') + r'''</span></div>
''' + index_table(1) + r'''</div>
<div class="ref-rule"><div class="ref-rule-line"><span class="rtag">Index</span><span class="rname">The moves from ''' + link(D2_URL, 'SAT Desmos 2: Next Steps &#8594;') + r'''</span></div>
''' + index_table(2) + r'''<div class="ref-note">Use Desmos when it helps; for simpler questions, algebra may be quicker. Several solutions on this sheet show both approaches so you can compare them.</div>
</div>
''')

FIGS_JS = r'''var FIGS = {};
function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }'''

CONFIG = dict(
    out=os.path.join(SAT_DIR, 'SAT-Desmos-3-Mixed-Practice.html'),
    title='SAT Desmos 3: Mixed Practice',
    subtitle='CALCULATOR SKILLS &bull; MIXED PRACTICE',
    footer='SAT Desmos Series: Mixed Practice',
    tab1='1. Start Here', tab1_h2='Start here',
    key='sat-desmos-3-sheet',
    drills=True,
    RULES=RULES, STEPS=[], FLUENCY=FLUENCY, GAUNTLET=GAUNTLET, CHALLENGE=CHALLENGE, EXIT=EXIT, FIGS_JS=FIGS_JS,
    LAST_STARRED_STEP_INDEX=-1, last_hint='',
    bluebook_tools=False,
    tab2_intro='This sheet has no walkthrough. The lessons are in SAT Desmos 1 and SAT Desmos 2.',
    fluency_bar='There is no time limit here. These quick questions are about choosing an approach, entering it, and reading what Desmos reports. Open the calculator when you want to try an entry. You can enter fractions as 7/3 or 2.333; both are accepted.',
    tab4_intro=(NUMBER_WORD[len(GAUNTLET)] + r' SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions to harder ones, and they are mixed: no label names the move, so start by identifying the question type. Then decide whether Desmos or algebra makes more sense; on several of these, algebra may be quicker. Turn on the timer if you would like to practice pacing. The calculator starts blank, as it will on test day, so type each line yourself. After you finish and score the set, each solution shows a Desmos approach and a second approach, usually algebra, with a <em>Load into Desmos</em> button so you can compare the lines with your own.'),
    tab5_intro=(str(N_MOVE) + r' questions, grouped by the move they practice. Choose <em>By move</em> to work on one skill at a time: each group is headed by its move and the sheet that teaches it. Choose <em>Shuffled</em> to mix the questions and practice identifying the question type; the move label appears after you check each answer. Work each question in the calculator or on paper, then check it right away. Each solution shows the lines to type, with a <em>Load into Desmos</em> button, and ends with the move to remember and a link to its lesson. A <strong>&#9733; starred move</strong> chip marks an essential move; <em>extra</em> marks a move that comes up less often.'),
    exit_prompt='Write one sentence you can use the next time you open the calculator. Make it an if-then. (Shape: “When I am not sure which move fits, I ______ before I type anything.”)',
    exit_links=('<p style="font-size:14px; margin-top:10px;"><strong>Practice in the College Board version of Desmos.</strong> Desmos publishes this version of its graphing calculator, and the outputs quoted on this sheet were read there. <a href="' + CB_DESMOS + '" ' + A_STYLE + '>Open the College Board version of Desmos &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">For more questions sorted by topic, <strong>Khan Academy\'s Official Digital SAT Prep</strong> is a good next step. <a href="https://www.khanacademy.org/digital-sat" ' + A_STYLE + '>Open Khan Academy &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">To review a move, go back to its lesson: <a href="' + D1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a> and <a href="' + D2_URL + '" ' + A_STYLE + '>SAT Desmos 2: Next Steps &#8594;</a></p>\n'
                '            <p style="font-size:14px; margin-top:10px;">The algebra behind these moves is in <a href="' + LINEAR_URL + '" ' + A_STYLE + '>SAT Math 1: Linear Equations &#8594;</a>, <a href="' + QUAD_URL + '" ' + A_STYLE + '>SAT Math 2: Quadratics &#8594;</a> and <a href="' + FUNC_URL + '" ' + A_STYLE + '>SAT Math 3: Functions &#8594;</a></p>'),
)

if __name__ == '__main__':
    build(CONFIG)
