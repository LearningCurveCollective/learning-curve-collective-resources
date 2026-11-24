#!/usr/bin/env python3
"""Builds test-prep/sat/SAT-Math-5-Ratios-Rates-Proportions.html from the linear-equations sheet's shell.
Everything visual (CSS, tab layout, Desmos panel, graders, results kit) is reused; only the content
swaps. This sheet covers ratios (part to part and part to whole), proportions and unit rates, direct
variation, rates and average speed, inverse variation, and combined work. The question types follow
Tips 19, 20, 25, 27 and 34 of the class book; all questions use original numbers and contexts.

It was copied from build_special_right_triangles.py and keeps that file's conventions (the voice pass,
figures in the tutor report, the geoSVG renderer). Three things are added here: the curve and grid
extensions to the shell's graphSVG from build_functions.py (plus `inv` for a curve y = k/x), a `panels`
figure (a row of small labelled graphs, for "which graph" questions), and captions under rules-tab figures.
Answer key: verify_ratios.py (same folder) recomputes every answer."""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.exists(os.path.join(ROOT, 'catalog.js')):
    parent = os.path.dirname(ROOT)
    assert parent != ROOT, 'repo root with catalog.js not found above this script'
    ROOT = parent
sys.path.insert(0, HERE)
try:
    import desmos_voice as voice                      # the LCC voice table for shell and results-kit copy
except ImportError:                                   # e.g. when this file sits in the skill folder without it
    sys.path.insert(0, os.path.join(ROOT, '_build', 'skill-update-sat-math-topic-sheet', 'scripts'))
    import desmos_voice as voice

SRC = ROOT + '/test-prep/sat/SAT-Math-1-Linear-Equations.html'
OUT = ROOT + '/test-prep/sat/SAT-Math-5-Ratios-Rates-Proportions.html'
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'
LINEAR_URL = SITE + 'test-prep/sat/SAT-Math-1-Linear-Equations.html'
TRI_URL = SITE + 'test-prep/sat/SAT-Math-4-Triangles.html'
PCT_URL = SITE + 'test-prep/sat/SAT-Math-6-Percentages.html'
DESMOS1_URL = SITE + 'test-prep/sat/SAT-Desmos-1-Core-Moves.html'
A_STYLE = 'target="_blank" rel="noopener" style="color:var(--copper); font-weight:700;"'

# ---------------------------------------------------------------- text helpers
MATH_RE = re.compile(r'\$\$.*?\$\$|\$(?:\\.|[^$\\])+?\$', re.S)


def nw(s):
    """Keep inline math glued to the punctuation that follows it (house style)."""
    out, pos = [], 0
    for m in MATH_RE.finditer(s):
        out.append(s[pos:m.start()])
        seg, end = m.group(0), m.end()
        if not seg.startswith('$$'):
            pm = re.match(r'[.,:;?!]+(?=\s|<|$)', s[end:])
            if pm:
                out.append('<span class="nw">' + seg + pm.group(0) + '</span>')
                pos = end + pm.end()
                continue
        out.append(seg)
        pos = end
    out.append(s[pos:])
    return ''.join(out)


def nw_all(o):
    if isinstance(o, str):
        return nw(o)
    if isinstance(o, list):
        return [nw_all(v) for v in o]
    if isinstance(o, dict):
        return {k: (v if k in ('desmos', 'accept', 'fig', 'type', 'diff', 'sec') else nw_all(v)) for k, v in o.items()}
    return o


STAR = '<span class="star">&#9733;</span>'


def rule(n, name, ess, body):
    tag = (STAR if ess else '') + 'Rule ' + str(n)
    return ('<div class="ref-rule' + (' ess' if ess else '') + '"><div class="ref-rule-line"><span class="rtag">' + tag +
            '</span><span class="rname">' + name + '</span></div>\n' + body.strip('\n') + '\n</div>\n')


def frow(label, math_):
    return '<div class="frow"><div class="flabel">' + label + '</div><div class="fmath">' + math_ + '</div></div>\n'


def ex(letter, text):
    return '<div class="ref-ex"><span class="exlab">Example ' + letter + '</span>' + text + '</div>\n'


def note(text):
    return '<div class="ref-note">' + text + '</div>\n'


def mistake(n, name, text):
    return ('<div class="ref-case"><div class="ref-rule-line"><span class="rtag">Common mistake ' + str(n) + '</span><span class="rname">' +
            name + '</span></div><div class="ref-ex">' + text + '</div></div>\n')


def figslot(name):
    return '<div class="fig-slot" data-fig="' + name + '"></div>\n'

# ---------------------------------------------------------------- TAB 1: RULES
LINK_STYLE = 'target="_blank" rel="noopener" style="color:var(--copper); font-weight:600;"'

RULES = r'''
<p class="ref-intro">A ratio compares two quantities. A rate is a ratio of two different units, such as miles per hour. A proportion says that two ratios are equal. Most questions on this sheet come down to one habit: write the comparison as a fraction, label what is on top and what is on the bottom, and keep that order the same on both sides. As you practice, start by identifying the question type. Then decide whether a proportion or an equation fits it better, and check that your answer addresses what the question asks.</p>
<div class="legend"><span><span class="star">&#9733;</span> <strong>Essential:</strong> the rules you will use most often. Start here.</span><span><strong>Unstarred:</strong> comes up less often. Come back to these after you feel comfortable with the starred rules.</span></div>
''' + rule(1, 'Ratios: part to part and part to whole', True, r'''
<p class="ref-lead">A ratio of $4$ to $7$ can be written $4 : 7$ or $\dfrac{4}{7}$. Before you use a ratio, decide what it compares: one part to another part, or one part to the whole. The same mix gives different fractions depending on which comparison you need.</p>
''' + figslot('r_parts') + r'''<div class="fbox">
''' + frow('part to part', r'$a : b$ &nbsp; (for example, red tiles to blue tiles)') +
      frow('part to whole', r'$\dfrac{a}{a + b}$ and $\dfrac{b}{a + b}$ &nbsp; (the whole is $a + b$ parts)') +
      frow('a ratio as multiples', r'if $x : y = 4 : 7$, then $x = 4k$ and $y = 7k$ for the same number $k$') +
      frow('three parts', r'$a : b : c$ works the same way: the whole is $a + b + c$ parts') + r'''</div>
''' + ex('A', r'Red and blue tiles are in the ratio $4 : 7$. The red tiles are $\dfrac{4}{11}$ of the tiles, not $\dfrac{4}{7}$. If there are $55$ tiles, each part is $55 \div 11 = 5$ tiles, so there are $20$ red tiles and $35$ blue tiles.') +
    ex('B', r'If $\dfrac{x}{y} = \dfrac{3}{4}$ and $3x + 2y = 85$, write $x = 3k$ and $y = 4k$. Then $9k + 8k = 85$, so $k = 5$, $x = 15$ and $y = 20$.') +
    note(r'A ratio alone does not give the amounts. $4 : 7$ could be $4$ and $7$, $8$ and $14$, or $20$ and $35$. One more fact (a total, a difference, or one of the amounts) gives you $k$.')) + \
rule(2, 'Proportions and unit rates', True, r'''
<p class="ref-lead">A proportion says two ratios are equal. Set one up when a question says &ldquo;at this rate&rdquo; or &ldquo;at the same rate.&rdquo; Label the units, keep the same quantity on top on both sides, and solve.</p>
<div class="fbox">
''' + frow('the setup', r'$\dfrac{\text{pages}}{\text{minutes}} = \dfrac{\text{pages}}{\text{minutes}}$ &nbsp; (the same units in the same places)') +
      frow('cross-multiply', r'$\dfrac{a}{b} = \dfrac{c}{d}$ means $ad = bc$') +
      frow('unit rate', r'divide to find the amount for one unit, then multiply by the number of units you need') +
      frow('scale it', r'if one quantity is multiplied by $n$, the other is multiplied by $n$ too') + r'''</div>
''' + ex('A', r'A printer prints $45$ pages in $6$ minutes. At this rate, how many pages does it print in $16$ minutes? Proportion: $\dfrac{45}{6} = \dfrac{p}{16}$, so $6p = 720$ and $p = 120$. Unit rate: $45 \div 6 = 7.5$ pages per minute, and $7.5 \times 16 = 120$.') +
    ex('B', r'A recipe uses $2.5$ cups of flour for $20$ muffins. For $52$ muffins: $\dfrac{2.5}{20} = \dfrac{f}{52}$, so $f = \dfrac{2.5 \times 52}{20} = 6.5$ cups.') +
    note(r'Check the units before you solve. If one time is in minutes and the other is in hours, convert one of them first. Rule 4 shows how.')) + \
rule(3, r'Direct variation: $y = kx$', True, r'''
<p class="ref-lead">When $y$ is directly proportional to $x$, the ratio $\dfrac{y}{x}$ is the same for every pair of values. That constant ratio is $k$, and the equation is $y = kx$. A question may say &ldquo;varies directly with,&rdquo; &ldquo;is directly proportional to,&rdquo; or &ldquo;is proportional to.&rdquo; All three describe the same relationship.</p>
<div class="fig-row">
<div class="figcap">''' + figslot('r_direct').strip() + r'''<div class="cap">$y = 1.5x$: proportional</div></div>
<div class="figcap">''' + figslot('r_notdirect').strip() + r'''<div class="cap">$y = x + 3$: linear, not proportional</div></div>
<div class="figcap">''' + figslot('r_square').strip() + r'''<div class="cap">$y = 0.5x^2$: proportional to $x^2$</div></div>
</div>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Where you see it</th><th>What to look for</th></tr></thead><tbody>
<tr><td class="fname">Equation</td><td>$y = kx$, with nothing added, and $k = \dfrac{y}{x}$</td></tr>
<tr><td class="fname">Table</td><td>$\dfrac{y}{x}$ is the same for every pair: $\dfrac{3}{2} = \dfrac{6}{4} = \dfrac{9}{6} = 1.5$</td></tr>
<tr><td class="fname">Graph</td><td>a line through the origin with slope $k$</td></tr>
<tr><td class="fname">Two pairs</td><td>$\dfrac{y_1}{x_1} = \dfrac{y_2}{x_2}$, which is a proportion</td></tr>
<tr><td class="fname">Proportional to $x^2$</td><td>$y = kx^2$: a parabola with its vertex at the origin. Doubling $x$ multiplies $y$ by $4$</td></tr>
</tbody></table></div>
''' + ex('A', r'$y$ is directly proportional to $x$, and $y = 33$ when $x = 6$. Then $k = \dfrac{33}{6} = 5.5$, so $y = 5.5x$. When $x = 10$, $y = 55$.') +
    ex('B', r'$y$ is directly proportional to $x^2$, and $y = 12$ when $x = 2$. Then $12 = k(2)^2$, so $k = 3$. When $x = 5$, $y = 3(25) = 75$.') +
    note(r'A line such as $y = x + 3$ is linear but not proportional, because its graph misses the origin. In $y = kx$, the constant $k$ is the slope of the line. <a href="' + LINEAR_URL + '" ' + LINK_STYLE + r'''>SAT Math 1: Linear Equations</a> covers slope in detail.''')) + \
rule(4, 'Rates and average speed', True, r'''
<p class="ref-lead">Distance, rate and time are tied together by one equation. For a trip with more than one part, the average speed is the total distance divided by the total time. It equals the plain average of the speeds only when the same amount of time is spent at each speed.</p>
''' + figslot('r_trip') + r'''<div class="fbox">
''' + frow('the equation', r'$d = rt$, so $r = \dfrac{d}{t}$ and $t = \dfrac{d}{r}$') +
      frow('average speed', r'$\dfrac{\text{total distance}}{\text{total time}}$') +
      frow('same distance, two speeds', r'find each time with $t = \dfrac{d}{r}$, then add. If no distance is given, choose one that both speeds divide evenly') +
      frow('unit conversion', r'multiply by a fraction equal to $1$ so that the unit you do not want cancels: $\dfrac{60 \text{ min}}{1 \text{ hr}}$ or $\dfrac{1 \text{ hr}}{60 \text{ min}}$') + r'''</div>
''' + ex('A', r'A driver travels for $2$ hours at $35$ miles per hour and then for $3$ hours at $55$ miles per hour. Total distance: $70 + 165 = 235$ miles. Total time: $5$ hours. Average speed: $\dfrac{235}{5} = 47$ miles per hour.') +
    ex('B', r'A driver goes to a lake at $36$ miles per hour and returns on the same road, in heavy traffic, at $18$ miles per hour. Choose a distance of $36$ miles each way: the times are $1$ hour and $2$ hours. Average speed: $\dfrac{72}{3} = 24$ miles per hour, not $27$.') +
    ex('C', r'A drone flies at $15$ meters per second. In kilometers per hour: $\dfrac{15 \text{ m}}{1 \text{ s}} \times \dfrac{3600 \text{ s}}{1 \text{ hr}} \times \dfrac{1 \text{ km}}{1000 \text{ m}} = 54$ kilometers per hour.') +
    note(r'When the distances are equal, more time is spent at the slower speed, so the average speed is closer to the slower speed. In Example B, $24$ is closer to $18$ than to $36$.')) + \
rule(5, r'Inverse variation: $xy = k$', False, r'''
<p class="ref-lead">When two quantities are inversely proportional, their product stays the same. If one is multiplied by $3$, the other is divided by $3$. Common pairs: workers and days for one job, speed and time for one trip, and people and cost per person for one bill.</p>
''' + figslot('r_inverse') + r'''<div class="tbl-wrap"><table class="cases"><thead><tr><th></th><th>Direct variation</th><th>Inverse variation</th></tr></thead><tbody>
<tr><td class="fname">Equation</td><td>$y = kx$</td><td>$xy = k$, or $y = \dfrac{k}{x}$</td></tr>
<tr><td class="fname">What stays the same</td><td>the ratio $\dfrac{y}{x}$</td><td>the product $xy$</td></tr>
<tr><td class="fname">Two pairs</td><td>$\dfrac{y_1}{x_1} = \dfrac{y_2}{x_2}$</td><td>$x_1 y_1 = x_2 y_2$</td></tr>
<tr><td class="fname">As $x$ increases (positive $k$)</td><td>$y$ increases</td><td>$y$ decreases</td></tr>
</tbody></table></div>
''' + ex('A', r'$6$ painters can paint a building in $10$ days. The job is $6 \times 10 = 60$ painter-days. With $15$ painters working at the same rate, it takes $60 \div 15 = 4$ days.') +
    ex('B', r'$y$ is inversely proportional to $x$, and $y = 20$ when $x = 3$. The product is $k = 60$. When $x = 5$, $y = 12$. When $x = 12$, $y = 5$.') +
    note(r'Check the direction with common sense. More workers should mean fewer days, and a faster speed should mean less time. If your answer moved the other way, the setup was a direct proportion.')) + \
rule(6, 'Combined work: add the rates', False, r'''
<p class="ref-lead">When two people or machines work on the same job, their times do not add. Their rates do. Write each rate as the fraction of the job finished in one hour.</p>
<div class="tbl-wrap"><table class="cases"><thead><tr><th>Worker</th><th>Time alone</th><th>Rate (jobs per hour)</th></tr></thead><tbody>
<tr><td class="fname">First</td><td>$a$ hours</td><td>$\dfrac{1}{a}$</td></tr>
<tr><td class="fname">Second</td><td>$b$ hours</td><td>$\dfrac{1}{b}$</td></tr>
<tr><td class="fname">Together</td><td>$t$ hours</td><td>$\dfrac{1}{a} + \dfrac{1}{b} = \dfrac{1}{t}$</td></tr>
</tbody></table></div>
<div class="fbox">
''' + frow('work rate', r'$\dfrac{1}{\text{time alone}}$ of the job per hour') +
      frow('two workers together', r'$t = \dfrac{ab}{a + b}$, which comes from $\dfrac{1}{a} + \dfrac{1}{b} = \dfrac{1}{t}$') +
      frow('equal workers in a group', r'count worker-hours: $\text{workers} \times \text{hours}$ measures the size of the job') + r'''</div>
''' + ex('A', r'One pump fills a tank in $6$ hours, and a second pump fills it in $12$ hours. Together they fill $\dfrac{1}{6} + \dfrac{1}{12} = \dfrac{3}{12} = \dfrac{1}{4}$ of the tank per hour, so they need $4$ hours.') +
    ex('B', r'Two machines finish an order together in $6$ hours. The first machine alone needs $10$ hours. The rate of the second machine is $\dfrac{1}{6} - \dfrac{1}{10} = \dfrac{1}{15}$, so alone it needs $15$ hours.') +
    ex('C', r'$6$ workers take $10$ hours to tile $4$ identical floors. That is $60$ worker-hours for $4$ floors, or $15$ worker-hours per floor. For $12$ floors, $8$ workers need $\dfrac{12 \times 15}{8} = 22.5$ hours.') +
    note(r'Working together takes less time than either worker needs alone. If your answer is larger than one of the solo times, check the setup.')) + r'''
<hr class="ref-divider"><div class="ref-h">Common mistakes and what to check</div>
<p>These are common setup and interpretation mistakes. Review them so you know what to check when an answer seems off.</p>
''' + mistake(1, 'using a part-to-part ratio as a fraction of the whole', r'A ratio of $4 : 7$ means $4$ parts and $7$ parts, so the whole is $11$ parts. The first part is $\dfrac{4}{11}$ of the whole, not $\dfrac{4}{7}$.') + \
      mistake(2, 'a proportion with the units in different places', r'If the left side is $\dfrac{\text{pages}}{\text{minutes}}$, the right side has to be $\dfrac{\text{pages}}{\text{minutes}}$ too. Write the units next to the numbers before you cross-multiply, and convert first if one side is in minutes and the other is in hours.') + \
      mistake(3, 'adding the same amount instead of multiplying', r'If $y$ is proportional to $x$ and $x$ goes from $4$ to $14$, then $y$ does not go up by $10$. It is multiplied by the same factor as $x$, here $\dfrac{14}{4} = 3.5$.') + \
      mistake(4, 'treating a line that misses the origin as proportional', r'$y = x + 3$ is a line, but $\dfrac{y}{x}$ changes from point to point. A proportional relationship has the form $y = kx$, and its graph passes through the origin.') + \
      mistake(5, 'averaging the two speeds', r'For equal distances at $36$ and $18$ miles per hour, the average speed is $24$, not $27$. Use total distance divided by total time.') + \
      mistake(6, 'using a direct proportion for an inverse relationship', r'If $6$ painters need $10$ days, then $15$ painters need fewer days, not more. When more of one quantity means less of the other, keep the product constant: $6 \times 10 = 15 \times d$.') + \
      mistake(7, 'adding or averaging the times of two workers', r'Pumps that need $6$ hours and $12$ hours alone do not need $18$ hours together, or $9$. Add the rates: $\dfrac{1}{6} + \dfrac{1}{12} = \dfrac{1}{4}$, so together they need $4$ hours.') + \
      mistake(8, 'stopping one step early', r'After you find $k$, a unit rate, or the size of one part, reread the question. It may ask for the other part, the total, or the value of $y$ at a new $x$.')

# ---------------------------------------------------------------- TAB 2: STEPS
STEPS = [
 {"ess": True, "name": "Rule 1: Ratios, part to part and part to whole",
  "rule": r"$a : b$ compares the parts &nbsp;·&nbsp; the whole is $a + b$ parts &nbsp;·&nbsp; each amount is a multiple of the same $k$",
  "say": r"Count the parts first. A ratio of $7 : 5$ splits the whole into $12$ equal parts. Divide the total by $12$ to find the size of one part, then multiply by the number of parts you need.",
  "prob": r"The ratio of fiction books to nonfiction books on a shelf is $7 : 5$. There are $72$ books on the shelf. How many of the books are nonfiction?",
  "sol": r"<strong>Given:</strong> fiction to nonfiction is $7 : 5$, and the total is $72$ books.<br><strong>Step 1: count the parts.</strong> $7 + 5 = 12$ parts.<br><strong>Step 2: find one part.</strong> $72 \div 12 = 6$ books.<br><strong>Step 3: build the part you need.</strong> Nonfiction is $5$ parts: $5 \times 6 = 30$ books.<br><strong>Check:</strong> fiction is $7 \times 6 = 42$ books, and $42 + 30 = 72$. Also $42 : 30 = 7 : 5$. ✓",
  "trap": r"Taking $\dfrac{5}{7}$ of $72$. The $7$ is the other part, not the whole. Nonfiction is $\dfrac{5}{12}$ of the shelf.",
  "micro": {"q": r"A paint mix uses blue paint and white paint in the ratio $2 : 7$. The fraction of the mix that is blue is", "accept": ["2/9", "0.222", ".222", "0.2222", ".2222"],
            "exp": r"The whole is $2 + 7 = 9$ parts, and blue is $2$ of them: $\dfrac{2}{9}$."}},
 {"ess": True, "name": "Rule 2: Proportions and unit rates",
  "rule": r"the same units in the same places &nbsp;·&nbsp; $\dfrac{a}{b} = \dfrac{c}{d}$ means $ad = bc$",
  "say": r"The phrase &ldquo;at this rate&rdquo; tells you the ratio stays the same. Write the units beside the numbers so that each side of the proportion compares the same two things. If the units do not match, convert before you solve.",
  "prob": r"A machine fills $84$ bottles in $7$ minutes. At this rate, how many bottles does it fill in $1.5$ hours?",
  "sol": r"<strong>Given:</strong> $84$ bottles in $7$ minutes. The time asked about is $1.5$ hours.<br><strong>Step 1: match the units.</strong> $1.5$ hours is $90$ minutes.<br><strong>Step 2: set up the proportion.</strong> $\dfrac{84 \text{ bottles}}{7 \text{ min}} = \dfrac{b \text{ bottles}}{90 \text{ min}}$<br><strong>Step 3: solve.</strong> $7b = 84 \times 90 = 7560$, so $b = 1080$.<br><strong>Check:</strong> the unit rate is $84 \div 7 = 12$ bottles per minute, and $12 \times 90 = 1080$. ✓",
  "trap": r"Using $1.5$ as if it were minutes, which gives $18$ bottles. A machine that fills $84$ bottles in $7$ minutes fills far more than $18$ in an hour and a half, so a size check points you back to the units.",
  "micro": {"q": r"$8$ notebooks cost $\$18$. At the same price per notebook, the cost in dollars of $20$ notebooks is", "accept": ["45", "45.00", "45.0"],
            "exp": r"The unit price is $18 \div 8 = 2.25$ dollars, and $2.25 \times 20 = 45$. As a proportion: $\dfrac{18}{8} = \dfrac{c}{20}$, so $c = 45$."}},
 {"ess": True, "name": "Rule 3: Direct variation, y = kx", "fig": "s3",
  "rule": r"$y = kx$ &nbsp;·&nbsp; $k = \dfrac{y}{x}$ is the same for every pair &nbsp;·&nbsp; the graph is a line through the origin",
  "say": r"One pair of values gives you $k$. Divide $y$ by $x$, write the equation, and then use it for any other value. On a graph, read a point the line passes through: its coordinates are a pair.",
  "prob": r"In the $xy$-plane above, $y$ is directly proportional to $x$, and the graph passes through the point $(4, 10)$. What is the value of $y$ when $x = 14$?",
  "sol": r"<strong>Given:</strong> $y = kx$, and the pair $x = 4$, $y = 10$.<br><strong>Step 1: find $k$.</strong> $k = \dfrac{10}{4} = 2.5$<br><strong>Step 2: write the equation.</strong> $y = 2.5x$<br><strong>Step 3: use it.</strong> When $x = 14$, $y = 2.5(14) = 35$.<br><strong>Check:</strong> as a proportion, $\dfrac{10}{4} = \dfrac{35}{14}$, and both equal $2.5$. ✓",
  "trap": r"Adding instead of multiplying. From $x = 4$ to $x = 14$ is an increase of $10$, but $y$ does not increase by $10$. Proportional quantities are multiplied by the same factor: $\dfrac{14}{4} = 3.5$, and $10 \times 3.5 = 35$.",
  "micro": {"q": r"$y$ is directly proportional to $x$, and $y = 26$ when $x = 8$. When $x = 6$, $y =$", "accept": ["19.5", "39/2"],
            "exp": r"$k = \dfrac{26}{8} = 3.25$, so $y = 3.25(6) = 19.5$."}},
 {"ess": True, "name": "Rule 4: Rates and average speed", "fig": "s4",
  "rule": r"$d = rt$ &nbsp;·&nbsp; average speed $= \dfrac{\text{total distance}}{\text{total time}}$",
  "say": r"When a trip has two parts, find the distance and the time for each part, then divide the totals. If the question gives two speeds for the same road and no distance, choose a distance that both speeds divide evenly. The average comes out the same for any distance you choose.",
  "prob": r"Maya drove from home to a trailhead at an average speed of $30$ miles per hour. She drove home along the same road at an average speed of $45$ miles per hour. What was her average speed, in miles per hour, for the whole trip?",
  "sol": r"<strong>Given:</strong> the same road both ways, at $30$ miles per hour and then at $45$ miles per hour. No distance is given.<br><strong>Step 1: choose a distance.</strong> Let the road be $90$ miles long, since $30$ and $45$ both divide $90$.<br><strong>Step 2: find each time.</strong> Out: $\dfrac{90}{30} = 3$ hours. Back: $\dfrac{90}{45} = 2$ hours.<br><strong>Step 3: divide the totals.</strong> $\dfrac{90 + 90}{3 + 2} = \dfrac{180}{5} = 36$ miles per hour.<br><strong>Check with a letter:</strong> for a road of $d$ miles, the total time is $\dfrac{d}{30} + \dfrac{d}{45} = \dfrac{5d}{90} = \dfrac{d}{18}$ hours, and $2d \div \dfrac{d}{18} = 36$. The distance cancels. ✓",
  "trap": r"Answering $37.5$, the average of $30$ and $45$. Maya spends more time at the slower speed, so the average speed is below the midpoint of the two speeds.",
  "micro": {"q": r"A runner covers $3$ miles in $24$ minutes and then $5$ miles in $56$ minutes. Her average speed for the whole run, in miles per hour, is", "accept": ["6"],
            "exp": r"Total distance: $8$ miles. Total time: $80$ minutes, which is $\dfrac{80}{60} = \dfrac{4}{3}$ hours. Average speed: $8 \div \dfrac{4}{3} = 6$ miles per hour."}},
 {"ess": False, "name": "Rule 5: Inverse variation, xy = k",
  "rule": r"$xy = k$ &nbsp;·&nbsp; $x_1 y_1 = x_2 y_2$ &nbsp;·&nbsp; one goes up, the other goes down",
  "say": r"Ask what stays the same. For one trip, the distance is fixed, so speed times time is constant. For one job, workers times days is constant. Find that product from the pair you know, then divide.",
  "prob": r"The time it takes to drive a certain route is inversely proportional to the average speed. At an average speed of $54$ miles per hour, the drive takes $4$ hours. How many hours does the drive take at an average speed of $72$ miles per hour?",
  "sol": r"<strong>Given:</strong> speed $\times$ time is constant. One pair is $54$ miles per hour and $4$ hours.<br><strong>Step 1: find the product.</strong> $54 \times 4 = 216$. This is the length of the route in miles.<br><strong>Step 2: use the new speed.</strong> $72t = 216$, so $t = 3$ hours.<br><strong>Check:</strong> the speed was multiplied by $\dfrac{72}{54} = \dfrac{4}{3}$, and the time was divided by $\dfrac{4}{3}$: $4 \div \dfrac{4}{3} = 3$. ✓",
  "trap": r"Setting up $\dfrac{54}{4} = \dfrac{72}{t}$, which gives about $5.3$ hours. A faster speed cannot make the same drive take longer. When the answer moves the opposite way from what makes sense, the setup needs a constant product, not a constant ratio.",
  "micro": {"q": r"$8$ identical pumps can drain a pool in $15$ hours. Working at the same rate, $12$ of these pumps can drain the pool in how many hours?", "accept": ["10"],
            "exp": r"The job is $8 \times 15 = 120$ pump-hours. With $12$ pumps: $120 \div 12 = 10$ hours."}},
 {"ess": False, "name": "Rule 6: Combined work, add the rates",
  "rule": r"rate $= \dfrac{1}{\text{time alone}}$ &nbsp;·&nbsp; $\dfrac{1}{a} + \dfrac{1}{b} = \dfrac{1}{t}$",
  "say": r"Turn each time into a rate: the fraction of the job done in one hour. Add the rates to get the fraction done in one hour together. The time together is the reciprocal of that sum.",
  "prob": r"Ana can paint a fence in $20$ hours working alone. Ben can paint the same fence in $30$ hours working alone. If they work together at these rates, how many hours will it take them to paint the fence?",
  "sol": r"<strong>Given:</strong> Ana needs $20$ hours alone, and Ben needs $30$ hours alone.<br><strong>Step 1: write the rates.</strong> Ana paints $\dfrac{1}{20}$ of the fence per hour, and Ben paints $\dfrac{1}{30}$.<br><strong>Step 2: add them.</strong> $\dfrac{1}{20} + \dfrac{1}{30} = \dfrac{3}{60} + \dfrac{2}{60} = \dfrac{5}{60} = \dfrac{1}{12}$<br><strong>Step 3: flip the rate.</strong> Together they paint $\dfrac{1}{12}$ of the fence per hour, so the job takes $12$ hours.<br><strong>Check:</strong> $\dfrac{ab}{a + b} = \dfrac{20 \times 30}{50} = 12$, and $12$ is less than both solo times. ✓",
  "trap": r"Answering $50$ (adding the times) or $25$ (averaging them). Two people working together finish sooner than either one alone, so the answer has to be less than $20$.",
  "micro": {"q": r"One hose fills a pool in $5$ hours, and a second hose fills it in $20$ hours. With both hoses running, the number of hours needed to fill the pool is", "accept": ["4"],
            "exp": r"$\dfrac{1}{5} + \dfrac{1}{20} = \dfrac{5}{20} = \dfrac{1}{4}$ of the pool per hour, so it takes $4$ hours."}},
]
LAST_STARRED_STEP_INDEX = 3  # 0-based index of the last starred step (Rule 4)

# ---------------------------------------------------------------- TAB 3: SKILL PRACTICE (the FLUENCY array)
FLUENCY = [
 {"sec": "A. Ratios and parts", "items": [
   {"q": r"A snack mix has nuts and raisins in the ratio $5 : 4$. The fraction of the mix that is raisins is", "accept": ["4/9", "0.444", ".444", "0.4444", ".4444"], "exp": r"The whole is $5 + 4 = 9$ parts, and raisins are $4$ of them."},
   {"q": r"Red and green marbles are in the ratio $2 : 3$, and there are $40$ marbles in all. The number of red marbles is", "accept": ["16"], "exp": r"$5$ parts make $40$ marbles, so one part is $8$. Red is $2 \times 8 = 16$."},
   {"q": r"If $x : y = 7 : 2$ and $x + y = 63$, then $x =$", "accept": ["49"], "exp": r"$x = 7k$ and $y = 2k$, so $9k = 63$ and $k = 7$. Then $x = 49$."},
   {"q": r"The ratio of cats to dogs at a shelter is $3 : 7$. There are $12$ cats. The number of dogs is", "accept": ["28"], "exp": r"$3$ parts are $12$ cats, so one part is $4$. Dogs are $7 \times 4 = 28$."},
   {"q": r"A $66$-inch ribbon is cut into two pieces whose lengths are in the ratio $5 : 6$. The length of the longer piece, in inches, is", "accept": ["36"], "exp": r"$11$ parts make $66$ inches, so one part is $6$ inches. The longer piece is $6 \times 6 = 36$."},
 ]},
 {"sec": "B. Proportions and unit rates", "items": [
   {"q": r"If $\dfrac{6}{15} = \dfrac{x}{35}$, then $x =$", "accept": ["14"], "exp": r"Cross-multiply: $15x = 210$, so $x = 14$. Or simplify first: $\dfrac{6}{15} = \dfrac{2}{5}$, and $\dfrac{2}{5}$ of $35$ is $14$."},
   {"q": r"A car uses $3$ gallons of gas to travel $96$ miles. At this rate, the number of gallons it needs to travel $240$ miles is", "accept": ["7.5", "15/2"], "exp": r"The car travels $96 \div 3 = 32$ miles per gallon, and $240 \div 32 = 7.5$."},
   {"q": r"A $5$-pound bag of rice costs $\$6.25$. At the same price per pound, the cost in dollars of $12$ pounds of rice is", "accept": ["15", "15.00", "15.0"], "exp": r"$6.25 \div 5 = 1.25$ dollars per pound, and $1.25 \times 12 = 15$."},
   {"q": r"On a map, $2$ centimeters represents $15$ kilometers. Two towns are $9$ centimeters apart on the map. The actual distance between them, in kilometers, is", "accept": ["67.5", "135/2"], "exp": r"$\dfrac{15}{2} = \dfrac{d}{9}$, so $d = \dfrac{15 \times 9}{2} = 67.5$."},
   {"q": r"A faucet drips $18$ milliliters of water every $4$ minutes. The number of milliliters it drips in $1$ hour is", "accept": ["270"], "exp": r"$18 \div 4 = 4.5$ milliliters per minute, and one hour is $60$ minutes: $4.5 \times 60 = 270$."},
 ]},
 {"sec": "C. Direct variation", "items": [
   {"q": r"$y$ is directly proportional to $x$, and $y = 18$ when $x = 4$. In the equation $y = kx$, the value of $k$ is", "accept": ["4.5", "9/2"], "exp": r"$k = \dfrac{y}{x} = \dfrac{18}{4} = 4.5$."},
   {"q": r"$y$ varies directly with $x$, and $y = 12$ when $x = 8$. When $x = 22$, $y =$", "accept": ["33"], "exp": r"$k = \dfrac{12}{8} = 1.5$, and $1.5 \times 22 = 33$."},
   {"mc": True, "q": r"Which equation shows that $y$ is directly proportional to $x$?", "opts": [r"$y = x + 4$", r"$y = \dfrac{4}{x}$", r"$y = 4x$", r"$y = 4x + 1$"], "correct": 2, "exp": r"Direct variation has the form $y = kx$, with nothing added. In $y = \dfrac{4}{x}$ the product $xy$ is constant, which is inverse variation."},
   {"q": r"In the table, $y$ is directly proportional to $x$.<table class='vtab'><tr><th>$x$</th><td>$4$</td><td>$14$</td></tr><tr><th>$y$</th><td>$5$</td><td>$m$</td></tr></table>The value of $m$ is", "accept": ["17.5", "35/2"], "exp": r"$k = \dfrac{5}{4} = 1.25$, so $m = 1.25 \times 14 = 17.5$."},
   {"q": r"$y$ is directly proportional to $x^2$, and $y = 18$ when $x = 3$. When $x = 5$, $y =$", "accept": ["50"], "exp": r"$18 = k(3)^2$ gives $k = 2$. Then $y = 2(5)^2 = 50$."},
 ]},
 {"sec": "D. Rates and average speed", "items": [
   {"q": r"A train travels $156$ miles in $3$ hours at a constant speed. At that speed, the distance in miles it travels in $5$ hours is", "accept": ["260"], "exp": r"The speed is $156 \div 3 = 52$ miles per hour, and $52 \times 5 = 260$."},
   {"q": r"A cyclist rides for $2$ hours at $12$ miles per hour and then for $1$ hour at $18$ miles per hour. The average speed for the ride, in miles per hour, is", "accept": ["14"], "exp": r"Total distance: $24 + 18 = 42$ miles. Total time: $3$ hours. $42 \div 3 = 14$."},
   {"q": r"A hiker walks $6$ miles up a trail at $2$ miles per hour and walks back down the same trail at $6$ miles per hour. The average speed for the round trip, in miles per hour, is", "accept": ["3"], "exp": r"The times are $3$ hours and $1$ hour. Total: $12$ miles in $4$ hours, which is $3$ miles per hour."},
   {"q": r"A speed of $90$ kilometers per hour is how many meters per second?", "accept": ["25"], "exp": r"$\dfrac{90 \text{ km}}{1 \text{ hr}} \times \dfrac{1000 \text{ m}}{1 \text{ km}} \times \dfrac{1 \text{ hr}}{3600 \text{ s}} = 25$ meters per second."},
   {"mc": True, "q": r"A car travels the first half of a route at $24$ miles per hour and the second half of the route at $56$ miles per hour. The average speed for the route is", "opts": [r"less than $40$ miles per hour", r"equal to $40$ miles per hour", r"greater than $40$ miles per hour", "impossible to find without the distance"], "correct": 0, "exp": r"More time is spent on the slower half, so the average is below $40$. With $168$ miles in each half, the times are $7$ hours and $3$ hours, and $\dfrac{336}{10} = 33.6$."},
 ]},
 {"sec": "E. Less common: inverse variation and combined work", "items": [
   {"q": r"$y$ is inversely proportional to $x$, and $y = 9$ when $x = 4$. When $x = 6$, $y =$", "accept": ["6"], "exp": r"The product is $4 \times 9 = 36$, and $36 \div 6 = 6$."},
   {"q": r"$6$ workers can finish a job in $14$ days. Working at the same rate, the number of days $4$ workers need to finish the job is", "accept": ["21"], "exp": r"The job is $6 \times 14 = 84$ worker-days, and $84 \div 4 = 21$. Fewer workers need more days."},
   {"q": r"One machine completes an order in $9$ hours, and a second machine completes the same order in $18$ hours. Working together, the number of hours they need is", "accept": ["6"], "exp": r"$\dfrac{1}{9} + \dfrac{1}{18} = \dfrac{3}{18} = \dfrac{1}{6}$ of the order per hour, so they need $6$ hours."},
   {"q": r"Two pipes together fill a tank in $8$ hours. One of the pipes fills the tank alone in $10$ hours. The number of hours the other pipe needs to fill the tank alone is", "accept": ["40"], "exp": r"$\dfrac{1}{8} - \dfrac{1}{10} = \dfrac{5}{40} - \dfrac{4}{40} = \dfrac{1}{40}$, so the other pipe needs $40$ hours."},
 ]},
]

# ---------------------------------------------------------------- TAB 4: SAT-STYLE PRACTICE (the GAUNTLET array)
GAUNTLET = [
 {"ess": True, "type": "mc", "diff": "Easy",
  "stem": r"A copy shop charges $\$2.10$ to print $14$ pages. At this rate, what is the charge to print $50$ pages?",
  "options": [r"$\$6.30$", r"$\$7.00$", r"$\$7.50$", r"$\$8.40$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $\$2.10$ for $14$ pages, and the same rate for $50$ pages.<br><br><strong>Unit rate:</strong> $2.10 \div 14 = 0.15$ dollars per page.<br><strong>Scale up:</strong> $0.15 \times 50 = 7.50$ dollars.<br><strong>Check:</strong> as a proportion, $\dfrac{2.10}{14} = \dfrac{7.50}{50}$, and both equal $0.15$. ✓",
  "trap": r"Choice A triples the charge, as if $50$ pages were three times $14$ pages. Divide to find the price of one page before you scale."},
 {"ess": True, "type": "ne", "diff": "Easy",
  "stem": r"The ratio of sophomores to juniors in a club is $3 : 8$. The club has $77$ members, and each member is a sophomore or a junior. How many juniors are in the club?",
  "label": "Juniors $=$", "accept": ["56"],
  "sol": r"<strong>Given:</strong> sophomores to juniors is $3 : 8$, and the total is $77$.<br><br><strong>Count the parts:</strong> $3 + 8 = 11$ parts.<br><strong>One part:</strong> $77 \div 11 = 7$ members.<br><strong>Juniors:</strong> $8 \times 7 = 56$.<br><strong>Check:</strong> sophomores are $3 \times 7 = 21$, and $21 + 56 = 77$. ✓",
  "trap": r"Dividing $77$ by $8$, or taking $\dfrac{3}{8}$ of $77$. The $8$ is one part of the ratio. The whole club is $3 + 8 = 11$ parts."},
 {"ess": True, "type": "mc", "diff": "Easy to medium",
  "stem": r"<table class='vtab'><tr><th>$x$</th><td>$2$</td><td>$6$</td><td>$10$</td></tr><tr><th>$y$</th><td>$7$</td><td>$21$</td><td>$35$</td></tr></table>The table shows three pairs of values of $x$ and $y$. If $y$ is directly proportional to $x$, which equation relates $y$ and $x$?",
  "options": [r"$y = x + 5$", r"$y = \dfrac{2}{7}x$", r"$y = 3.5x$", r"$y = 7x$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $y = kx$ for some constant $k$.<br><br><strong>Find $k$ from one pair:</strong> $k = \dfrac{7}{2} = 3.5$<br><strong>Check the other pairs:</strong> $\dfrac{21}{6} = 3.5$ and $\dfrac{35}{10} = 3.5$. ✓<br>The equation is $y = 3.5x$.",
  "trap": r"Choice A fits the first pair only: $2 + 5 = 7$, but $6 + 5$ is not $21$. Choice B has the ratio upside down: $k$ is $\dfrac{y}{x}$, not $\dfrac{x}{y}$."},
 {"ess": True, "type": "mc", "diff": "Medium", "fig": "p4",
  "stem": r"If $y$ is directly proportional to $x$, which of the graphs above could be the graph of $y = f(x)$ in the $xy$-plane?",
  "options": ["Graph A", "Graph B", "Graph C", "Graph D"], "correct": 3,
  "sol": r"<strong>Given:</strong> $y = kx$ for some constant $k$.<br><br>The graph of $y = kx$ is a line, and it passes through the origin because $x = 0$ gives $y = 0$. Graph D is the only line through the origin.<br>Graph A passes through the origin, but it is a curve. Graph B is a line that crosses the $y$-axis below the origin. Graph C is a horizontal line, so $y$ does not change when $x$ changes.",
  "trap": r"Choosing Graph B because it is a rising line. A proportional relationship also needs a $y$-intercept of $0$. Graph A shows a different relationship, $y = kx^2$."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"Dana drove for $2$ hours at an average speed of $51$ miles per hour and then for $3$ hours at an average speed of $56$ miles per hour. What was her average speed, in miles per hour, for the $5$ hours?",
  "label": "Average speed $=$", "accept": ["54"],
  "sol": r"<strong>Given:</strong> $2$ hours at $51$ miles per hour, then $3$ hours at $56$ miles per hour.<br><br><strong>Total distance:</strong> $2(51) + 3(56) = 102 + 168 = 270$ miles.<br><strong>Total time:</strong> $5$ hours.<br><strong>Average speed:</strong> $\dfrac{270}{5} = 54$ miles per hour.<br><strong>Check:</strong> more of the time was spent at $56$, so the average is closer to $56$ than to $51$. ✓",
  "trap": r"Answering $53.5$, the average of $51$ and $56$. The two speeds were held for different lengths of time, so they do not count equally."},
 {"ess": True, "type": "mc", "diff": "Medium",
  "stem": r"A pump moves $45$ liters of water every $20$ seconds. At this rate, how many liters of water does the pump move in $6$ minutes?",
  "options": ["$13.5$", "$270$", "$810$", r"$16{,}200$"], "correct": 2,
  "sol": r"<strong>Given:</strong> $45$ liters every $20$ seconds. The time asked about is $6$ minutes.<br><br><strong>Match the units:</strong> $6$ minutes is $360$ seconds.<br><strong>Proportion:</strong> $\dfrac{45}{20} = \dfrac{w}{360}$, so $w = \dfrac{45 \times 360}{20} = 810$ liters.<br><strong>Check:</strong> $360$ seconds is $18$ groups of $20$ seconds, and $18 \times 45 = 810$. ✓",
  "trap": r"Choice A uses $6$ where $360$ belongs: $\dfrac{45}{20} \times 6 = 13.5$. Choice B multiplies $45$ by $6$. Convert the minutes to seconds before you set up the proportion."},
 {"ess": True, "type": "ne", "diff": "Medium",
  "stem": r"If $\dfrac{x}{y} = \dfrac{5}{2}$ and $3x - 4y = 56$, what is the value of $x$?",
  "label": "$x =$", "accept": ["40"], "desmos": [r"\frac{x}{y}=\frac{5}{2}", "3x-4y=56"],
  "sol": r"<strong>Given:</strong> $x : y = 5 : 2$, and $3x - 4y = 56$.<br><br><strong>Write the ratio as multiples:</strong> $x = 5k$ and $y = 2k$.<br><strong>Substitute:</strong> $3(5k) - 4(2k) = 15k - 8k = 7k = 56$, so $k = 8$.<br><strong>Build $x$:</strong> $x = 5(8) = 40$.<br><strong>Check:</strong> $y = 16$, $\dfrac{40}{16} = \dfrac{5}{2}$, and $3(40) - 4(16) = 120 - 64 = 56$. ✓",
  "trap": r"Stopping at $k = 8$, or answering with $y = 16$. The question asks for $x$, which is $5k$."},
 {"ess": False, "type": "mc", "diff": "Medium",
  "stem": r"<table class='vtab'><tr><th>$x$</th><td>$3$</td><td>$6$</td><td>$9$</td><td>$18$</td></tr><tr><th>$y$</th><td>$60$</td><td>$a$</td><td>$20$</td><td>$b$</td></tr></table>In the table above, $y$ is inversely proportional to $x$. What is the value of $a - b$?",
  "options": ["$10$", "$20$", "$30$", "$40$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $xy = k$ for every pair in the table.<br><br><strong>Find $k$:</strong> $3 \times 60 = 180$, and $9 \times 20 = 180$ agrees.<br><strong>Find $a$ and $b$:</strong> $6a = 180$ gives $a = 30$, and $18b = 180$ gives $b = 10$.<br><strong>Answer the question:</strong> $a - b = 30 - 10 = 20$.",
  "trap": r"Choice A is $b$ alone, choice C is $a$ alone, and choice D is $a + b$. After you find the two values, reread what the question asks for."},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"Luis biked from his house to the beach at an average speed of $20$ miles per hour. He biked home along the same route at an average speed of $12$ miles per hour. If he spent a total of $4$ hours biking, what is the distance, in miles, from his house to the beach?",
  "options": ["$30$", "$32$", "$60$", "$64$"], "correct": 0, "desmos": [r"\frac{x}{20}+\frac{x}{12}=4"],
  "sol": r"<strong>Given:</strong> the same distance $d$ each way, at $20$ and $12$ miles per hour, and $4$ hours in all.<br><br><strong>Write each time:</strong> $\dfrac{d}{20}$ hours out and $\dfrac{d}{12}$ hours back.<br><strong>Add them:</strong> $\dfrac{d}{20} + \dfrac{d}{12} = 4$<br><strong>Solve:</strong> multiply both sides by $60$: $3d + 5d = 240$, so $d = 30$.<br><strong>Check:</strong> $\dfrac{30}{20} = 1.5$ hours and $\dfrac{30}{12} = 2.5$ hours, and $1.5 + 2.5 = 4$. ✓",
  "trap": r"Choice B comes from averaging the speeds: $16 \times 4 = 64$ miles for the round trip, or $32$ each way. Choice C is the round trip. The times at the two speeds are different, so write a separate time for each leg."},
 {"ess": False, "type": "ne", "diff": "Medium-hard",
  "stem": r"Machine A can complete a production order in $28$ hours working alone. Machines A and B, working together at their constant rates, can complete the same order in $12$ hours. How many hours would it take machine B to complete the order working alone?",
  "label": "Hours $=$", "accept": ["21"], "desmos": [r"\frac{1}{28}+\frac{1}{x}=\frac{1}{12}"],
  "sol": r"<strong>Given:</strong> A alone needs $28$ hours, and A and B together need $12$ hours. Let $b$ be the number of hours B needs alone.<br><br><strong>Write the rates:</strong> $\dfrac{1}{28} + \dfrac{1}{b} = \dfrac{1}{12}$<br><strong>Isolate the rate of B:</strong> $\dfrac{1}{b} = \dfrac{1}{12} - \dfrac{1}{28} = \dfrac{7}{84} - \dfrac{3}{84} = \dfrac{4}{84} = \dfrac{1}{21}$<br><strong>Flip it:</strong> $b = 21$ hours.<br><strong>Check:</strong> $\dfrac{28 \times 21}{28 + 21} = \dfrac{588}{49} = 12$. ✓",
  "trap": r"Subtracting the times: $28 - 12 = 16$. Times do not add or subtract, but rates do. Also check the size: B alone has to take longer than the $12$ hours the two machines need together."},
]

# ---------------------------------------------------------------- TAB 5: CHALLENGE
CHALLENGE = [
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"Trail mix A is made by mixing $3$ parts peanuts with $2$ parts raisins. Trail mix B is made by mixing $3$ parts almonds with $1$ part raisins. If equal amounts of mix A and mix B are combined, what fraction of the new mixture is raisins?",
  "options": [r"$\dfrac{3}{10}$", r"$\dfrac{13}{40}$", r"$\dfrac{1}{3}$", r"$\dfrac{13}{20}$"], "correct": 1,
  "sol": r"<strong>Given:</strong> mix A is $3 : 2$, mix B is $3 : 1$, and the two mixes are combined in equal amounts.<br><br><strong>Raisins in each mix:</strong> mix A is $\dfrac{2}{5}$ raisins, and mix B is $\dfrac{1}{4}$ raisins.<br><strong>Choose an amount:</strong> take $20$ cups of each mix, since $20$ is a multiple of $5$ and of $4$. Mix A has $8$ cups of raisins, and mix B has $5$ cups.<br><strong>Combine:</strong> $\dfrac{8 + 5}{40} = \dfrac{13}{40}$<br><strong>Check:</strong> $\dfrac{13}{40}$ is halfway between $\dfrac{2}{5} = \dfrac{16}{40}$ and $\dfrac{1}{4} = \dfrac{10}{40}$, as it should be for equal amounts. ✓",
  "trap": r"Adding the parts: $2 + 1 = 3$ raisin parts out of $5 + 4 = 9$ parts gives $\dfrac{1}{3}$. A part of mix A is not the same size as a part of mix B, so turn each ratio into a fraction of its own mix first. Choice D adds the two fractions without dividing by $2$.",
  "extrasIntro": r"Two mixes combined in equal amounts: turn each ratio into a fraction of its own mix, then average the fractions. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"A drink is made with $1$ part syrup and $4$ parts water. A second drink is made with $1$ part syrup and $1$ part water. Equal amounts of the two drinks are combined. The fraction of the result that is syrup is", "label": "$=$", "accept": ["7/20", "0.35", ".35"], "exp": r"The syrup fractions are $\dfrac{1}{5}$ and $\dfrac{1}{2}$. In $10$ cups of each drink, syrup is $2 + 5 = 7$ cups out of $20$."},
   {"type": "ne", "q": r"Alloy X is $2$ parts copper to $3$ parts zinc. Alloy Y is $3$ parts copper to $1$ part zinc. Equal amounts of the two alloys are melted together. The fraction of the result that is copper is", "label": "$=$", "accept": ["23/40", "0.575", ".575"], "exp": r"The copper fractions are $\dfrac{2}{5}$ and $\dfrac{3}{4}$. In $20$ grams of each alloy, copper is $8 + 15 = 23$ grams out of $40$."},
   {"type": "ne", "q": r"Batter P is flour and sugar in the ratio $7 : 3$. Batter Q is flour and sugar in the ratio $3 : 1$. Equal amounts of the two batters are combined. The fraction of the result that is sugar is", "label": "$=$", "accept": ["11/40", "0.275", ".275"], "exp": r"The sugar fractions are $\dfrac{3}{10}$ and $\dfrac{1}{4}$. In $20$ cups of each batter, sugar is $6 + 5 = 11$ cups out of $40$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Medium-hard",
  "stem": r"<table class='vtab'><tr><th>$x$</th><td>$2$</td><td>$a$</td></tr><tr><th>$y$</th><td>$a$</td><td>$32$</td></tr></table>In the table above, $y$ is directly proportional to $x$, and $a$ is a positive constant. What is the value of $a$?",
  "label": "$a =$", "accept": ["8"],
  "sol": r"<strong>Given:</strong> $\dfrac{y}{x}$ is the same for both pairs, and $a > 0$.<br><br><strong>Set the ratios equal:</strong> $\dfrac{a}{2} = \dfrac{32}{a}$<br><strong>Cross-multiply:</strong> $a^2 = 64$, so $a = 8$ (the positive value).<br><strong>Check:</strong> the pairs are $(2, 8)$ and $(8, 32)$, and $\dfrac{8}{2} = \dfrac{32}{8} = 4$. ✓",
  "trap": r"Writing the two ratios in different orders, such as $\dfrac{a}{2} = \dfrac{a}{32}$. Keep $y$ over $x$ in both ratios. A letter in the table is handled like any other value."},
 {"ess": True, "type": "ne", "diff": "Medium-hard · geometry blend", "fig": "c3",
  "stem": r"In the figure above, right triangle $ABC$ is similar to right triangle $DEF$, with right angles at $C$ and $F$. If $AC = 6$, $BC = 8$ and $EF = 20$, what is the length of $\overline{DE}$?",
  "label": "$DE =$", "accept": ["25"],
  "sol": r"<strong>Given:</strong> similar triangles, so matching sides are in the same ratio. $\overline{BC}$ matches $\overline{EF}$, and $\overline{AB}$ matches $\overline{DE}$.<br><br><strong>Find $AB$:</strong> $AB = \sqrt{6^2 + 8^2} = \sqrt{100} = 10$<br><strong>Set up the proportion:</strong> $\dfrac{DE}{AB} = \dfrac{EF}{BC}$, so $\dfrac{DE}{10} = \dfrac{20}{8}$<br><strong>Solve:</strong> $DE = \dfrac{10 \times 20}{8} = 25$<br><strong>Check:</strong> the scale factor is $\dfrac{20}{8} = \dfrac{5}{2}$, so $DF = 6 \times \dfrac{5}{2} = 15$, and $15^2 + 20^2 = 625 = 25^2$. ✓",
  "trap": r"Adding $12$ to each side because $EF$ is $12$ more than $BC$. Similar figures are scaled by multiplying, so the hypotenuse is $10 \times \dfrac{5}{2}$, not $10 + 12$."},
 {"ess": True, "type": "mc", "diff": "Medium-hard",
  "stem": r"A delivery driver traveled from a warehouse to a store. For the first half of the distance, the driver averaged $28$ miles per hour. For the second half of the distance, the driver averaged $70$ miles per hour. What was the average speed of the driver, in miles per hour, for the whole trip?",
  "options": ["$40$", "$42$", "$49$", "$56$"], "correct": 0,
  "sol": r"<strong>Given:</strong> equal distances at $28$ and $70$ miles per hour. No distance is given.<br><br><strong>Choose a distance:</strong> let each half be $140$ miles, a multiple of $28$ and of $70$.<br><strong>Find each time:</strong> $\dfrac{140}{28} = 5$ hours and $\dfrac{140}{70} = 2$ hours.<br><strong>Divide the totals:</strong> $\dfrac{280}{7} = 40$ miles per hour.<br><strong>Check:</strong> $40$ is between the two speeds and closer to the slower one, where more of the time was spent. ✓",
  "trap": r"Choice C is the average of $28$ and $70$. That would be correct for equal times. Here the distances are equal, so the slower half takes longer and pulls the average down.",
  "extrasIntro": r"Equal distances at two speeds: choose a distance, find each time, and divide the totals. Three more reps.",
  "extras": [
   {"type": "ne", "q": r"A driver goes to a town at $30$ miles per hour and returns on the same road at $70$ miles per hour. The average speed for the round trip, in miles per hour, is", "label": "$=$", "accept": ["42"], "exp": r"Let the road be $210$ miles long. The times are $7$ hours and $3$ hours, and $\dfrac{420}{10} = 42$."},
   {"type": "ne", "q": r"A hiker covers the first half of a trail at $12$ kilometers per hour on a bike and the second half at $4$ kilometers per hour on foot. The average speed for the trail, in kilometers per hour, is", "label": "$=$", "accept": ["6"], "exp": r"Let each half be $12$ kilometers. The times are $1$ hour and $3$ hours, and $\dfrac{24}{4} = 6$."},
   {"type": "ne", "q": r"A plane flies $600$ miles at $400$ miles per hour and then $600$ miles at $240$ miles per hour. The average speed for the $1{,}200$ miles, in miles per hour, is", "label": "$=$", "accept": ["300"], "exp": r"The times are $1.5$ hours and $2.5$ hours, and $\dfrac{1200}{4} = 300$."},
  ]},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"In $4$ years, the ratio of Priya&rsquo;s age to Omar&rsquo;s age will be $2 : 3$. In $12$ years, the ratio of Priya&rsquo;s age to Omar&rsquo;s age will be $3 : 4$. What is the sum of their ages now?",
  "label": "Sum $=$", "accept": ["32"],
  "sol": r"<strong>Given:</strong> two ratios, $8$ years apart. Let their ages in $4$ years be $2k$ and $3k$.<br><br><strong>Move $8$ more years ahead:</strong> the ages are $2k + 8$ and $3k + 8$, and their ratio is $3 : 4$.<br><strong>Write the proportion:</strong> $\dfrac{2k + 8}{3k + 8} = \dfrac{3}{4}$<br><strong>Cross-multiply:</strong> $8k + 32 = 9k + 24$, so $k = 8$.<br><strong>Go back to now:</strong> in $4$ years they are $16$ and $24$, so now they are $12$ and $20$. The sum is $32$.<br><strong>Check:</strong> in $12$ years they are $24$ and $32$, and $24 : 32 = 3 : 4$. ✓",
  "trap": r"Treating the ages as $2$ and $3$ and adding years to those numbers. The ratio numbers are multiples of an unknown $k$, so the ages are $2k$ and $3k$. Also note which moment the question asks about: the sum now is $32$, while the sum in $4$ years is $40$."},
 {"ess": True, "type": "ne", "diff": "Hard",
  "stem": r"The positive integers $a$ and $b$ satisfy $\dfrac{a}{b} = \dfrac{4}{7}$. If $a$ is divisible by $6$, $b$ is divisible by $10$, and $a + b < 1{,}000$, what is one possible value of $a + b$?",
  "label": "$a + b =$", "accept": ["330", "660", "990"],
  "sol": r"<strong>Given:</strong> $a : b = 4 : 7$. Since $4$ and $7$ share no common factor, $a = 4k$ and $b = 7k$ for a positive integer $k$.<br><br><strong>Use the first condition:</strong> $4k$ is divisible by $6$ when $k$ is a multiple of $3$.<br><strong>Use the second condition:</strong> $7k$ is divisible by $10$ when $k$ is a multiple of $10$.<br><strong>Combine:</strong> $k$ is a multiple of $30$, so $a + b = 11k$ is $330$, $660$ or $990$. Each is less than $1{,}000$, and any one of them is a correct response.<br><strong>Check $k = 30$:</strong> $a = 120$ and $b = 210$. $120$ is divisible by $6$, $210$ is divisible by $10$, and $\dfrac{120}{210} = \dfrac{4}{7}$. ✓",
  "trap": r"Testing only $a = 4$ and $b = 7$. The ratio gives a family of pairs, $4k$ and $7k$, and the divisibility conditions decide which values of $k$ are allowed."},
 {"ess": False, "type": "ne", "diff": "Hard",
  "stem": r"Working together at their constant rates, pump A and pump B can fill a pool in $6$ hours. Pump A works $3$ times as fast as pump B. How many hours would it take pump B to fill the pool working alone?",
  "label": "Hours $=$", "accept": ["24"],
  "sol": r"<strong>Given:</strong> together the pumps need $6$ hours, and the rate of A is $3$ times the rate of B. Let $r$ be the fraction of the pool that pump B fills in one hour.<br><br><strong>Write the rates:</strong> B fills $r$ per hour, and A fills $3r$ per hour.<br><strong>Add them:</strong> $r + 3r = 4r = \dfrac{1}{6}$, so $r = \dfrac{1}{24}$.<br><strong>Flip it:</strong> pump B alone needs $24$ hours.<br><strong>Check:</strong> pump A alone needs $8$ hours, and $\dfrac{1}{8} + \dfrac{1}{24} = \dfrac{4}{24} = \dfrac{1}{6}$. ✓",
  "trap": r"Answering $18$, which is $3 \times 6$. The $6$ hours belongs to both pumps together. Split the combined rate into $4$ equal shares first: B does one share, so B alone needs $4 \times 6 = 24$ hours."},
 {"ess": False, "type": "mc", "diff": "Hard",
  "stem": r"It takes $6$ workers $8$ hours to assemble $4$ identical sheds. At the same rate per worker, how many hours will it take $9$ workers to assemble $15$ of these sheds?",
  "options": ["$12$", "$20$", "$30$", "$45$"], "correct": 1,
  "sol": r"<strong>Given:</strong> $6$ workers, $8$ hours, $4$ sheds. Then $9$ workers and $15$ sheds.<br><br><strong>Size of the job:</strong> $6 \times 8 = 48$ worker-hours for $4$ sheds, which is $12$ worker-hours per shed.<br><strong>The new job:</strong> $15 \times 12 = 180$ worker-hours.<br><strong>Share it:</strong> $180 \div 9 = 20$ hours.<br><strong>Check:</strong> the number of sheds is multiplied by $\dfrac{15}{4}$ and the crew by $\dfrac{3}{2}$, so the time is $8 \times \dfrac{15}{4} \div \dfrac{3}{2} = 20$. ✓",
  "trap": r"Choice C scales for the sheds but not for the larger crew: $8 \times \dfrac{15}{4} = 30$. Choice D multiplies by both factors. More sheds means more time, but more workers means less time, so one factor multiplies and the other divides."},
]

# ---------------------------------------------------------------- TAB 6: EXIT
EXIT = [
 {"q": r"Blue tiles and green tiles are in the ratio $2 : 5$. What fraction of the tiles are green?", "opts": [r"$\dfrac{2}{7}$", r"$\dfrac{2}{5}$", r"$\dfrac{5}{7}$", r"$\dfrac{5}{2}$"], "correct": 2,
  "exp": r"The whole is $2 + 5 = 7$ parts, and green is $5$ of them. $\dfrac{2}{5}$ compares blue to green, not green to the whole."},
 {"q": r"$y$ is directly proportional to $x$, and $y = 24$ when $x = 9$. What is the value of $y$ when $x = 15$?", "opts": ["$30$", "$40$", "$45$", "$54$"], "correct": 1,
  "exp": r"$k = \dfrac{24}{9} = \dfrac{8}{3}$, and $\dfrac{8}{3} \times 15 = 40$. Adding $6$ to both numbers gives $30$, but proportional quantities are multiplied by the same factor."},
 {"q": r"A driver travels $66$ miles at $33$ miles per hour and then $66$ miles at $22$ miles per hour. What is the average speed for the $132$ miles?", "opts": [r"$26.4$ miles per hour", r"$27.5$ miles per hour", r"$30$ miles per hour", r"$55$ miles per hour"], "correct": 0,
  "exp": r"The times are $2$ hours and $3$ hours. Total: $132$ miles in $5$ hours, which is $26.4$ miles per hour. The plain average of the speeds, $27.5$, ignores that more time is spent at the slower speed."},
]
# ---------------------------------------------------------------- FIGURES
# Specs are Python dicts dumped to JS. An entry with a `box` key is drawn by geoSVG (plain geometry, equal
# scale); an entry with `panels` is a row of small labelled graphs; anything else goes to the shell's graphSVG,
# which this builder extends with curves, a labelled grid and a clip path (as SAT Math 3 does).
def pt(x, y): return [round(x, 3), round(y, 3)]
def seg(a, b, cls=None):
    o = {'a': a, 'b': b}
    if cls: o['cls'] = cls
    return o
def ang3(at, a, b, t=None, **k):
    """Angle at `at` between the rays toward points a and b."""
    o = {'at': at, 'a': a, 'b': b}
    if t: o['t'] = t
    o.update(k)
    return o
def side(a, b, t, off=13, **k):
    """A label beside the middle of segment a-b; off > 0 is to the left of a->b."""
    o = {'a': a, 'b': b, 't': t, 'off': off}
    o.update(k)
    return o
def lab(p, t, deg=None, away=None, **k):
    """A letter beside point p, in direction deg (degrees) or pushed away from the point `away`; d= sets the distance in px."""
    o = {'p': p, 't': t}
    if away is not None: o['away'] = away
    else: o['dir'] = deg
    o.update(k)
    return o
def txt(at, t, **k):
    o = {'at': at, 't': t}
    o.update(k)
    return o

FIGS = {}

# --- Rule 1: a bar of 11 equal parts, 4 of one kind and 7 of the other
FIGS['r_parts'] = dict(box=[-0.3, -1.25, 11.3, 2.0], w=400, h=128, pad=8,
    alt='a bar split into 11 equal parts: 4 parts are red tiles and 7 parts are blue tiles',
    polys=[dict(pts=[pt(i, 0), pt(i + 1, 0), pt(i + 1, 1), pt(i, 1)], cls=('tileR' if i < 4 else 'tileB')) for i in range(11)],
    segs=[seg(pt(0, -0.3), pt(11, -0.3), 'thin'), seg(pt(0, -0.45), pt(0, -0.15), 'thin'), seg(pt(11, -0.45), pt(11, -0.15), 'thin')],
    texts=[txt(pt(2, 1.5), '4 parts red', cls='lbl'), txt(pt(7.5, 1.5), '7 parts blue', cls='lbl'), txt(pt(5.5, -0.85), '11 parts in all', cls='lbl')])

# --- Rule 3: proportional, linear but not proportional, proportional to the square
FIGS['r_direct'] = dict(xmin=-1.2, xmax=7.6, ymin=-1.2, ymax=10.6, w=210, h=250, grid=dict(step=1, label=2),
    alt='the line y = 1.5x on a grid, passing through the origin and the points (2, 3), (4, 6) and (6, 9)',
    ox=-13, oy=-6, lines=[dict(m=1.5, b=0)], points=[dict(x=2, y=3), dict(x=4, y=6), dict(x=6, y=9)])
FIGS['r_notdirect'] = dict(xmin=-1.2, xmax=7.6, ymin=-1.2, ymax=10.6, w=210, h=250, grid=dict(step=1, label=2),
    alt='the line y = x + 3 on a grid, crossing the y-axis at 3, so it misses the origin',
    lines=[dict(m=1, b=3)], points=[dict(x=0, y=3)])
FIGS['r_square'] = dict(xmin=-4.4, xmax=4.4, ymin=-1.2, ymax=10.6, w=210, h=250, grid=dict(step=1, label=2),
    alt='the parabola y = 0.5 x squared on a grid, with its vertex at the origin',
    curves=[dict(a=0.5, b=0, c=0)], points=[dict(x=2, y=2), dict(x=4, y=8)])

# --- Rule 4: one road, two speeds (36 miles each way)
def trip(out_text, back_text, left, right, alt):
    return dict(box=[-1.0, -1.45, 9.0, 1.75], w=400, h=150, pad=6, alt=alt,
        segs=[seg(pt(0, 0.4), pt(8, 0.4)), seg(pt(8, -0.4), pt(0, -0.4)),
              seg(pt(0, -0.75), pt(0, 0.75), 'thin'), seg(pt(8, -0.75), pt(8, 0.75), 'thin')],
        polys=[dict(pts=[pt(8, 0.4), pt(7.62, 0.6), pt(7.62, 0.2)], cls='fillg'),
               dict(pts=[pt(0, -0.4), pt(0.38, -0.2), pt(0.38, -0.6)], cls='fillg')],
        texts=[txt(pt(4, 0.88), out_text, cls='lbl'), txt(pt(4, -0.95), back_text, cls='lbl'),
               txt(pt(0, 1.3), left, cls='lbl'), txt(pt(8, 1.3), right, cls='lbl')])
FIGS['r_trip'] = trip('out: 36 miles at 36 mph takes 1 hour', 'back: 36 miles at 18 mph takes 2 hours', 'home', 'lake',
    'a road from home to a lake: 36 miles out at 36 miles per hour takes 1 hour, and 36 miles back at 18 miles per hour takes 2 hours')

# --- Rule 5: the curve xy = 12
FIGS['r_inverse'] = dict(xmin=-1.2, xmax=13.4, ymin=-1.2, ymax=13.4, w=270, h=260, grid=dict(step=2, label=4),
    alt='the curve xy = 12 in the first quadrant, falling from left to right through the points (2, 6), (3, 4) and (6, 2)',
    curves=[dict(inv=12, **{'from': 0.9, 'to': 13.2})],
    points=[dict(x=2, y=6, label='(2, 6)', dx=8, dy=-4), dict(x=3, y=4, label='(3, 4)', dx=8, dy=-4), dict(x=6, y=2, label='(6, 2)', dx=3, dy=-10)],
    labels=[dict(x=9.2, y=4.6, text='xy = 12', dx=0, dy=0)])

# --- Step 3: a proportional line through (4, 10)
FIGS['s3'] = dict(xmin=-1.2, xmax=7.4, ymin=-2.4, ymax=17, w=250, h=290, grid=dict(step=2, label=4),
    alt='a line through the origin and the point (4, 10) on a grid',
    ox=-13, oy=-6, lines=[dict(m=2.5, b=0)], points=[dict(x=4, y=10, label='(4, 10)', dx=9, dy=5)])

# --- Step 4: the same road at 30 and then 45 miles per hour
FIGS['s4'] = trip('out: 30 miles per hour', 'back: 45 miles per hour', 'home', 'trailhead',
    'a road from home to a trailhead, driven out at 30 miles per hour and back at 45 miles per hour')

# --- Practice 4: four small graphs, labelled A to D
PANEL = dict(xmin=-3.3, xmax=3.3, ymin=-3.3, ymax=3.3, w=150, h=150)
FIGS['p4a'] = dict(PANEL, alt='graph A: a U-shaped curve with its lowest point at the origin', curves=[dict(a=0.55, b=0, c=0)])
FIGS['p4b'] = dict(PANEL, alt='graph B: a rising line that crosses the y-axis below the origin', lines=[dict(m=1, b=-1.4)])
FIGS['p4c'] = dict(PANEL, alt='graph C: a horizontal line above the x-axis', lines=[dict(m=0, b=1.5)])
FIGS['p4d'] = dict(PANEL, alt='graph D: a rising line through the origin', ox=-13, oy=-6, lines=[dict(m=1.6, b=0)])
FIGS['p4'] = dict(alt='four graphs labelled A, B, C and D',
    panels=[dict(t='A', fig='p4a'), dict(t='B', fig='p4b'), dict(t='C', fig='p4c'), dict(t='D', fig='p4d')])

# --- Challenge 3: two similar right triangles, drawn to scale (6-8-10 and 15-20-25)
U = 0.18
A, C, B = pt(0, 0), pt(6 * U, 0), pt(6 * U, 8 * U)
D, F, E = pt(2.3, 0), pt(2.3 + 15 * U, 0), pt(2.3 + 15 * U, 20 * U)
FIGS['c3'] = dict(box=[-0.5, -0.55, 5.7, 3.95], w=320, h=240,
    alt='two right triangles: triangle ABC with legs AC = 6 and BC = 8 and the right angle at C, and a larger triangle DEF with leg EF = 20 and the right angle at F; the angles at A and D are marked equal',
    segs=[seg(A, C), seg(C, B), seg(A, B), seg(D, F), seg(F, E), seg(D, E)],
    rights=[dict(at=C, a=A, b=B), dict(at=F, a=D, b=E)],
    arcs=[ang3(A, C, B, r=20), ang3(D, F, E, r=20)],
    sides=[side(A, C, '6', -14), side(C, B, '8', -13), side(F, E, '20', -15)],
    pts=[lab(A, 'A', 200), lab(B, 'B', 90), lab(C, 'C', -40, d=15), lab(D, 'D', 200), lab(E, 'E', 90), lab(F, 'F', -40, d=15)])

GEO_JS = r'''
/* Geometry figures: no axes, equal scale. Points are [x, y] with y up; `box` is [xmin, ymin, xmax, ymax]. */
function geoSVG(o) {
    var w = o.w || 300, h = o.h || 200, pad = o.pad == null ? 22 : o.pad, B = o.box, noteH = o.note ? 22 : 0;
    var sc = Math.min((w - 2 * pad) / (B[2] - B[0]), (h - noteH - 2 * pad) / (B[3] - B[1]));
    var ox = (w - sc * (B[2] - B[0])) / 2, oy = (h - noteH - sc * (B[3] - B[1])) / 2;
    function X(x) { return ox + (x - B[0]) * sc; }
    function Y(y) { return h - noteH - oy - (y - B[1]) * sc; }
    function P(p) { return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }
    function U(a, b) { var dx = b[0] - a[0], dy = b[1] - a[1], L = Math.sqrt(dx * dx + dy * dy) || 1; return [dx / L, dy / L]; }
    function T(x, y, t, c, anc) {
        var k = c || (/[A-Za-zℓ]/.test(t) ? 'g it' : 'g');
        return '<text class="' + k + '" text-anchor="' + (anc || 'middle') + '" x="' + x.toFixed(1) + '" y="' + (y + 5).toFixed(1) + '">' + t + '</text>';
    }
    var s = '<svg class="fig" viewBox="0 0 ' + w + ' ' + h + '" width="' + w + '" height="' + h + '" role="img" aria-label="' + (o.alt || 'geometry figure') + '">';
    (o.semis || []).forEach(function(m) {       // a semicircle on diameter a-b, on the left of a->b
        var r = Math.sqrt(Math.pow(X(m.b[0]) - X(m.a[0]), 2) + Math.pow(Y(m.b[1]) - Y(m.a[1]), 2)) / 2;
        s += '<path class="' + (m.cls || 'tile') + '" d="M' + P(m.a) + ' A' + r.toFixed(1) + ',' + r.toFixed(1) + ' 0 0 1 ' + P(m.b) + ' Z"/>';
    });
    (o.polys || []).forEach(function(pl) { s += '<polygon class="' + (pl.cls || 'shade') + '" points="' + pl.pts.map(P).join(' ') + '"/>'; });
    (o.circles || []).forEach(function(c) { s += '<circle class="circ" cx="' + X(c.c[0]).toFixed(1) + '" cy="' + Y(c.c[1]).toFixed(1) + '" r="' + (c.r * sc).toFixed(1) + '"/>'; });
    (o.segs || []).forEach(function(g) { s += '<line class="' + (g.cls || 'ln') + '" x1="' + X(g.a[0]).toFixed(1) + '" y1="' + Y(g.a[1]).toFixed(1) + '" x2="' + X(g.b[0]).toFixed(1) + '" y2="' + Y(g.b[1]).toFixed(1) + '"/>'; });
    (o.rights || []).forEach(function(q) {      // right-angle mark at q.at, opening toward the points q.a and q.b
        var k = q.s || 9, u = U(q.at, q.a), v = U(q.at, q.b), px = X(q.at[0]), py = Y(q.at[1]);
        s += '<path class="sq" d="M' + (px + u[0] * k).toFixed(1) + ',' + (py - u[1] * k).toFixed(1) + ' L' + (px + (u[0] + v[0]) * k).toFixed(1) + ',' + (py - (u[1] + v[1]) * k).toFixed(1) + ' L' + (px + v[0] * k).toFixed(1) + ',' + (py - v[1] * k).toFixed(1) + '"/>';
    });
    (o.arcs || []).forEach(function(c) {        // the angle at c.at between the rays toward c.a and c.b: an arc (r > 0) and a label on the bisector
        var a1 = Math.atan2(c.a[1] - c.at[1], c.a[0] - c.at[0]), a2 = Math.atan2(c.b[1] - c.at[1], c.b[0] - c.at[0]);
        var d = a2 - a1; while (d > Math.PI) d -= 2 * Math.PI; while (d <= -Math.PI) d += 2 * Math.PI;
        var px = X(c.at[0]), py = Y(c.at[1]), r = c.r == null ? 15 : c.r, am = a1 + d / 2;
        if (r > 0) s += '<path class="arc" d="M' + (px + r * Math.cos(a1)).toFixed(1) + ',' + (py - r * Math.sin(a1)).toFixed(1) + ' A' + r + ',' + r + ' 0 0 ' + (d > 0 ? 0 : 1) + ' ' + (px + r * Math.cos(a2)).toFixed(1) + ',' + (py - r * Math.sin(a2)).toFixed(1) + '"/>';
        if (c.t) { var lr = c.lr == null ? r + 14 : c.lr; s += T(px + lr * Math.cos(am) + (c.dx || 0), py - lr * Math.sin(am) + (c.dy || 0), c.t, c.cls); }
    });
    (o.ticks || []).forEach(function(k) {       // n short marks across the middle of segment a-b (equal lengths)
        var u = U(k.a, k.b), mx = (X(k.a[0]) + X(k.b[0])) / 2, my = (Y(k.a[1]) + Y(k.b[1])) / 2, n = k.n || 1;
        for (var i = 0; i < n; i++) {
            var off = (i - (n - 1) / 2) * 4, cx = mx + u[0] * off, cy = my - u[1] * off;
            s += '<line class="tick" x1="' + (cx - u[1] * 5).toFixed(1) + '" y1="' + (cy - u[0] * 5).toFixed(1) + '" x2="' + (cx + u[1] * 5).toFixed(1) + '" y2="' + (cy + u[0] * 5).toFixed(1) + '"/>';
        }
    });
    (o.sides || []).forEach(function(l) {       // a label beside segment a-b; off > 0 puts it on the left of a->b
        var u = U(l.a, l.b), off = l.off == null ? 13 : l.off, f = l.f == null ? 0.5 : l.f;
        s += T(X(l.a[0] + (l.b[0] - l.a[0]) * f) - u[1] * off + (l.dx || 0), Y(l.a[1] + (l.b[1] - l.a[1]) * f) - u[0] * off + (l.dy || 0), l.t, l.cls);
    });
    (o.dots || []).forEach(function(p) { s += '<circle class="pt" cx="' + X(p[0]).toFixed(1) + '" cy="' + Y(p[1]).toFixed(1) + '" r="3"/>'; });
    (o.pts || []).forEach(function(p) {         // a letter beside the point p.p: in direction p.dir (degrees), or pushed away from the point p.away
        var u = p.away ? U(p.away, p.p) : [Math.cos((p.dir || 0) * Math.PI / 180), Math.sin((p.dir || 0) * Math.PI / 180)], d = p.d == null ? 13 : p.d;
        s += T(X(p.p[0]) + u[0] * d + (p.dx || 0), Y(p.p[1]) - u[1] * d + (p.dy || 0), p.t, p.cls);
    });
    (o.texts || []).forEach(function(t) { s += T(X(t.at[0]) + (t.dx || 0), Y(t.at[1]) + (t.dy || 0), t.t, t.cls, t.anc); });
    if (o.note) s += '<text class="note" text-anchor="middle" x="' + (w / 2) + '" y="' + (h - 8) + '">' + o.note + '</text>';
    return s + '</svg>';
}
function fig(name) {
    var f = FIGS[name];
    if (!f) return '';
    if (f.panels) return '<div class="fig-row panels" role="group" aria-label="' + (f.alt || 'graphs') + '">' + f.panels.map(function(p) { return '<div class="panel"><div class="plab">' + p.t + '</div>' + fig(p.fig) + '</div>'; }).join('') + '</div>';
    return f.box ? geoSVG(f) : graphSVG(f);
}'''

FIGS_JS = 'var FIGS = {\n' + ',\n'.join('    ' + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in FIGS.items()) + '\n};' + GEO_JS

# figure classes on top of the shell's figure styles; the fig-row rules match sheets 3, 4 and 4B
FIG_RULES = [
    ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }",
    ".fig text.g { font-size: 15px; }",
    ".fig .thin { stroke: #21442B; stroke-width: 1.3; fill: none; }",
    ".fig .arc { stroke: #BC6C26; stroke-width: 1.4; fill: none; }",
    ".fig .tick { stroke: #21442B; stroke-width: 1.5; }",
    ".fig .circ { fill: none; stroke: #21442B; stroke-width: 2; }",
    ".fig .shade2 { fill: rgba(57,134,78,0.16); stroke: none; }",
    ".fig .tile { fill: rgba(221,162,94,0.12); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .tileR { fill: rgba(192,57,43,0.24); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .tileB { fill: rgba(52,101,164,0.20); stroke: #21442B; stroke-width: 1.4; }",
    ".fig .fillg { fill: #21442B; stroke: none; }",
    ".fig .grid { stroke: rgba(45,45,45,0.13); stroke-width: 1; }",
    ".fig text.sm { font-family: 'Inter', sans-serif; font-size: 11px; font-style: normal; fill: #5A5A5A; }",
    ".fig text.lbl { font-family: 'Inter', sans-serif; font-size: 12.5px; font-style: normal; fill: #2D2D2D; }",
    ".fig text.note { font-family: 'Inter', sans-serif; font-size: 11.5px; font-style: normal; fill: #5A5A5A; }",
]
PANEL_RULES = [
    ".fig-row { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: flex-start; justify-content: center; margin: 4px 0 10px; }",
    ".fig-row .fig { margin: 4px 0; }",
    ".panel { text-align: center; }",
    ".panel .plab { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 700; color: #21442B; }",
]
FIG_CSS = '\n'.join(FIG_RULES + PANEL_RULES) + r'''
.ref-page .fig-row { margin-left: 24px; }
@media (max-width: 768px) { .ref-page .fig-row { margin-left: 0; } }
.figcap { text-align: center; }
.figcap .cap { font-family: 'Inter', sans-serif; font-size: 12.5px; color: #5A5A5A; margin: -2px 0 8px; }'''
# the same figure styles, on one line, for the downloaded results report (which has its own style block)
REPORT_FIG_CSS = (".fig{display:block;margin:4px 0 10px;max-width:100%;height:auto}.fig .ax{stroke:#2D2D2D;stroke-width:1.4}.fig .ln{stroke:#21442B;stroke-width:2;fill:none}"
                  ".fig .dash{stroke:#8B6914;stroke-width:1.4;stroke-dasharray:5 4;fill:none}.fig .pt{fill:#21442B}.fig .shade{fill:rgba(221,162,94,0.25);stroke:none}"
                  ".fig text{font-family:\"Times New Roman\",Georgia,serif;font-size:13px;fill:#2D2D2D}.fig text.it{font-style:italic}" +
                  ''.join(re.sub(r'\s*([{};:,])\s*', r'\1', r).replace(';}', '}') for r in FIG_RULES + PANEL_RULES))


# The shell draws lines, dashed segments, points, polygons. This sheet adds: general
# function curves (with gaps), polylines, horizontal and vertical dashed lines, thick
# domain/range highlights on the axes, and an optional labeled grid.
CURVES_JS = r'''    (o.curves || []).forEach(function(c) {
        // y = a x^2 + b x + c, or y = inv / x, or any function c.f, sampled across [from, to] and split at gaps
        var fn = c.f || (c.inv != null ? function(x) { return c.inv / x; } : function(x) { return c.a * x * x + c.b * x + c.c; });
        var x0 = (c.from != null ? c.from : xmin), x1 = (c.to != null ? c.to : xmax);
        var n = 240, run = [], runs = [], band = 2 * (ymax - ymin);
        for (var i = 0; i <= n; i++) {
            var x = x0 + (x1 - x0) * i / n, y = fn(x);
            if (!isFinite(y) || y < ymin - band || y > ymax + band) { if (run.length) { runs.push(run); run = []; } continue; }
            run.push(X(x).toFixed(1) + ',' + Y(y).toFixed(1));
        }
        if (run.length) runs.push(run);
        runs.forEach(function(r) { if (r.length > 1) s += '<polyline class="' + (c.cls || 'ln') + '" clip-path="url(#clip' + id + ')" points="' + r.join(' ') + '"/>'; });
        if (c.label) s += '<text class="it" x="' + (X(c.lx) + (c.dx || 0)) + '" y="' + (Y(c.ly) + (c.dy || 0)) + '">' + c.label + '</text>';
    });
    (o.polylines || []).forEach(function(c) {
        s += '<polyline class="' + (c.cls || 'ln') + '" points="' + c.pts.map(function(p) { return X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }).join(' ') + '"/>';
        if (c.label) s += '<text class="it" x="' + (X(c.lx) + (c.dx || 0)) + '" y="' + (Y(c.ly) + (c.dy || 0)) + '">' + c.label + '</text>';
    });
    (o.hlines || []).forEach(function(l) {
        s += '<line class="' + (l.cls || 'dash') + '" x1="' + X(xmin) + '" y1="' + Y(l.y) + '" x2="' + X(xmax) + '" y2="' + Y(l.y) + '"/>';
        if (l.label) s += '<text class="it" x="' + (X(l.lx != null ? l.lx : xmin) + (l.dx || 0)) + '" y="' + (Y(l.y) + (l.dy || -5)) + '">' + l.label + '</text>';
    });
    (o.vlines || []).forEach(function(l) {
        s += '<line class="' + (l.cls || 'dash') + '" x1="' + X(l.x) + '" y1="' + Y(ymin) + '" x2="' + X(l.x) + '" y2="' + Y(ymax) + '"/>';
        if (l.label) s += '<text class="it" x="' + (X(l.x) + (l.dx || 5)) + '" y="' + (Y(l.ly != null ? l.ly : ymax) + (l.dy || 12)) + '">' + l.label + '</text>';
    });
    (o.thick || []).forEach(function(t) {
        s += '<line class="dom" x1="' + X(t.x1) + '" y1="' + Y(t.y1) + '" x2="' + X(t.x2) + '" y2="' + Y(t.y2) + '"/>';
    });
'''

GRID_JS = r'''    if (o.grid) {
        var gs = o.grid.step || 1, gl = o.grid.label || 0, k;
        for (k = Math.ceil(xmin / gs); k * gs <= xmax + 1e-9; k++) s += '<line class="grid" x1="' + X(k * gs) + '" y1="' + Y(ymin) + '" x2="' + X(k * gs) + '" y2="' + Y(ymax) + '"/>';
        for (k = Math.ceil(ymin / gs); k * gs <= ymax + 1e-9; k++) s += '<line class="grid" x1="' + X(xmin) + '" y1="' + Y(k * gs) + '" x2="' + X(xmax) + '" y2="' + Y(k * gs) + '"/>';
        if (gl && ymin <= 0 && ymax >= 0) for (k = Math.ceil(xmin / gl); k * gl <= xmax - 0.5; k++) if (k !== 0) s += '<text class="sm" text-anchor="middle" x="' + X(k * gl) + '" y="' + (Y(0) + 14) + '">' + (k * gl < 0 ? '−' + (-k * gl) : k * gl) + '</text>';
        if (gl && xmin <= 0 && xmax >= 0) for (k = Math.ceil(ymin / gl); k * gl <= ymax - 0.5; k++) if (k !== 0) s += '<text class="sm" text-anchor="end" x="' + (X(0) - 5) + '" y="' + (Y(k * gl) + 4) + '">' + (k * gl < 0 ? '−' + (-k * gl) : k * gl) + '</text>';
    }
'''

def _clean(o):
    """Content strings may arrive with backslash+quote from r-strings; drop the backslash."""
    if isinstance(o, str): return o.replace('\\"', '"')
    if isinstance(o, list): return [_clean(v) for v in o]
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    return o

def js_data(name, data):
    return 'var ' + name + ' = ' + json.dumps(_clean(nw_all(data)), ensure_ascii=False).replace('</', '<\\/') + ';\n'

def sub1(src, pattern, repl, flags=0, count=1):
    new, n = re.subn(pattern, (repl if callable(repl) else (lambda m: repl)), src, count=count, flags=flags)
    if n != count:
        sys.exit('pattern not found (%d of %d): %r' % (n, count, pattern[:80]))
    return new

def replace_once(src, old, new):
    if src.count(old) != 1:
        sys.exit('expected exactly one occurrence (%d): %r' % (src.count(old), old[:100]))
    return src.replace(old, new)

def replace_n(src, old, new, n):
    if src.count(old) != n:
        sys.exit('expected %d occurrences (%d): %r' % (n, src.count(old), old[:100]))
    return src.replace(old, new)




def build(out=OUT):
    html = open(SRC, encoding='utf-8').read()
    html = re.sub(r'\s*<p style="font-size:14px; margin-top:10px;">Ready for the next topic\?.*?</p>', '', html, flags=re.S)

    # --- header / titles / footer
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>SAT Math: Ratios, Rates and Proportions</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>SAT Math: Ratios, Rates and Proportions</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', 'CONCEPT + DRILLS &bull; RATIOS, RATES AND PROPORTIONS')
    html = replace_once(html, 'SAT Math Series: Linear Equations', 'SAT Math Series: Ratios, Rates and Proportions')
    html = replace_once(html, '>1. Linear Rules</button>', '>1. Ratio Rules</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>Ratio, rate and proportion rules</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(RULES).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(r'The main idea behind these rules is simple: <strong>a ratio is a comparison you can scale.</strong> Multiply or divide both quantities by the same number, and the relationship stays the same. Each question asks you to decide what is being compared, set up the comparison with matching units, and find the missing value.') + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each rule with a worked example, a common mistake to watch for, and a short check for understanding. Start with the starred rules, and try each problem on paper before you reveal the solution.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        'There is no time limit here. You can enter fractions as 7/3 or 2.333; both are accepted. Sections A to D use the starred rules, and section E covers the unstarred ones. Once you feel comfortable, try responding without pausing for long.')

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'Ten SAT-style questions in the two digital-test formats: four-choice multiple choice and student-produced response (type the number). They move from easier questions through medium to medium-hard at the end, and three include a table or a figure. A <strong>&#9733; starred rule</strong> chip means the question uses one of the starred rules from tab 1. Before you compute, identify the question type: does a ratio stay the same, does a product stay the same, or do rates add? Then write the units next to the numbers as you set up. Desmos is available throughout the SAT Math section, so it is available here: the button in the corner opens it. For these questions it works mostly as a calculator. It can also graph an equation in one variable, such as $\dfrac{x}{20} + \dfrac{x}{12} = 4$, so that you can read the solution from the graph. For a one-step proportion, cross-multiplying by hand is usually quicker.') + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(r'These eight questions build on the practice set, with medium-hard to hard examples similar to ones you may encounter later in a Math module. Each one adds a second idea to a rule you already have (two mixes combined, a table with a letter in it, a ratio inside a pair of similar triangles, equal distances at two speeds, ages that change over time, divisibility conditions, one pump that is faster than the other, a crew that changes size). Work each one, then check it right away. Focus on understanding why each approach works, even when your first attempt needs adjusting. Questions marked <strong>&#9733; starred rule</strong> use the essential rules; the ones marked <em>extra</em> lean on the unstarred rules. One is tagged <em>geometry blend</em>: it pairs a proportion with the Pythagorean theorem from SAT Math 4, and that pairing appears less often, so treat it as stretch practice.') + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        nw(r'Write one sentence you can use the next time a ratio or a rate shows up. Make it an if-then. (Shape: “When a question says ‘at this rate,’ I ______ before I cross-multiply.”)'))
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        '<p style="font-size:14px; margin-top:10px;">Direct variation is a line through the origin, so the slope work in <a href="' + LINEAR_URL + '" ' + A_STYLE + '>SAT Math 1: Linear Equations &#8594;</a> carries over. The previous sheet in the series is <a href="' + TRI_URL + '" ' + A_STYLE + '>SAT Math 4: Triangles &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">For calculator practice, see <a href="' + DESMOS1_URL + '" ' + A_STYLE + '>SAT Desmos 1: Core Moves &#8594;</a></p>\n'
        '            <p style="font-size:14px; margin-top:10px;">Ready for the next topic? Continue the series with <a href="' + PCT_URL + '" ' + A_STYLE + '>SAT Math 6: Percentages &#8594;</a></p>',
        flags=re.S)

    # --- data arrays
    for name, data in [('STEPS', STEPS), ('FLUENCY', FLUENCY), ('GAUNTLET', GAUNTLET), ('CHALLENGE', CHALLENGE), ('EXIT', EXIT)]:
        html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, data), flags=re.S)

    # --- figures: FIGS, the geometry renderer and fig(); the shell's graphSVG gains curves, a grid and a clip path
    start = html.index('var FIGS = {')
    tail = "function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }"
    end = html.index(tail) + len(tail)
    html = html[:start] + FIGS_JS + html[end:]
    html = replace_once(html,
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';""",
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker>' +
        '<clipPath id="clip' + id + '"><rect x="' + X(xmin) + '" y="' + Y(ymax) + '" width="' + (X(xmax) - X(xmin)) + '" height="' + (Y(ymin) - Y(ymax)) + '"/></clipPath></defs>';""")
    html = replace_once(html, """s += '<text class="it" x="' + (X(0) - 12) + '" y="' + (Y(0) + 14) + '">O</text>';""",
                        """s += '<text class="it" x="' + (X(0) + (o.ox == null ? -12 : o.ox)) + '" y="' + (Y(0) + (o.oy == null ? 14 : o.oy)) + '">O</text>';""")   # ox, oy: move the O when a line runs through its usual spot
    html = replace_once(html, "    if (o.poly) {\n", GRID_JS + "    if (o.poly) {\n")
    html = replace_once(html, "    (o.lines || []).forEach(function(l) {\n", CURVES_JS + "    (o.lines || []).forEach(function(l) {\n")
    html = replace_once(html, ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }", FIG_CSS)

    # --- Skill Practice items can carry a figure; it sits between the question and the answer row
    html = replace_once(html, """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>';""",
                        """html += '<div class="drill"><div class="drill-q">' + n + '. &nbsp;' + it.q + '</div>' + (it.fig ? fig(it.fig) : '');""")

    # --- results kit: carry each question's figure into the tutor report (practice, challenge and any Skill Practice rep that has one)
    html = replace_n(html, "stem: p.stem, trap: p.trap });", "stem: p.stem, fig: p.fig ? fig(p.fig) : '', trap: p.trap });", 2)
    html = replace_once(html, """'</b></span></div><div class="stem">' + r.i.stem + '</div>""", """'</b></span></div><div class="stem">' + (r.i.fig || '') + r.i.stem + '</div>""")
    html = replace_once(html, ": it.accept[0], q: it.q }); }", ": it.accept[0], q: it.q + (it.fig ? fig(it.fig) : '') }); }")
    html = replace_once(html, "'.nw{white-space:nowrap}table.vtab{", "'" + REPORT_FIG_CSS.replace('\\', '\\\\').replace("'", "\\'") + "' +\n        '.nw{white-space:nowrap}table.vtab{")

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', 'sat-ratios-sheet:rule')
    html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                        "(i === %d ? 'That was the last starred step. The next two cover ideas that come up less often.' : '')" % LAST_STARRED_STEP_INDEX)
    html = replace_once(html, "Step 1 of 9", "Step 1 of %d" % len(STEPS))

    # --- LCC voice pass: visible shell and results-kit copy (the last entry renames a column for the Desmos sheets only)
    html = voice.apply(html, voice.SHELL[:-1], 'shell')

    dash = chr(8212)                                  # the em dash, written this way so this file contains none
    if dash in html:
        i = html.index(dash)
        sys.exit('em dash found: ' + html[max(0, i - 80):i + 40])
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out, len(html), 'bytes;', len(STEPS), 'steps,', sum(len(s['items']) for s in FLUENCY), 'skill practice,',
          len(GAUNTLET), 'practice,', len(CHALLENGE), 'challenge,', len(EXIT), 'exit,', len(FIGS), 'figures')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else OUT)
