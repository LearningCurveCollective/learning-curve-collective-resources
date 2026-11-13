#!/usr/bin/env python3
"""Shared builder for the SAT Desmos series (build_desmos1.py, build_desmos2.py, build_desmos3.py). Reuses the SAT Math topic-sheet shell
(SAT-Math-1-Linear-Equations.html: CSS, tabs, graders, Desmos panel, results kit) and swaps
in Desmos content. Adds, on top of the shell:
  - a "Desmos lines" mock (dz) that shows what to type and what Desmos reports
  - Load into Desmos on every worked example, with tables / window / degree mode support
  - no Load button on unanswered practice or challenge questions (typing is the skill)
  - an optional Bluebook Tools tab ported from SAT-Desmos-Strategies.html (sheet 1); its source is the
    snapshot desmos_tools_tab.json, so the build does not depend on that older sheet staying as it is
  - the LCCo voice pass (desmos_voice.py): visible shell, results-kit and tools-tab copy, applied last
  - an optional drills-only layout (drills=True, sheet 3): no stepper tab, the challenge tab becomes
    Practice by Move with a By move / Shuffled switch, and the practice set becomes the Timed Practice Set
Run build_desmos1.py / build_desmos2.py / build_desmos3.py; they write straight into test-prep/sat/.
"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.exists(os.path.join(ROOT, 'catalog.js')):
    parent = os.path.dirname(ROOT)
    assert parent != ROOT, 'repo root with catalog.js not found above this script'
    ROOT = parent
SAT_DIR = os.path.join(ROOT, 'test-prep', 'sat')
SRC = os.path.join(SAT_DIR, 'SAT-Math-1-Linear-Equations.html')          # the shell
FUNC_BUILDER = os.path.join(HERE, 'build_functions.py')                  # figure renderer blocks are read from it
if not os.path.exists(FUNC_BUILDER):                                     # e.g. when run from the _build staging folder
    FUNC_BUILDER = os.path.join(ROOT, '.claude', 'skills', 'sat-math-topic-sheet', 'scripts', 'build_functions.py')
TOOLS_SNAPSHOT = os.path.join(HERE, 'desmos_tools_tab.json')             # Bluebook Tools tab source
OLD_DESMOS = os.path.join(ROOT, 'retired-sheets', 'SAT-Desmos-Strategies.html')   # retired 2026-11-12; only read if the snapshot is missing
SITE = 'https://learningcurvecollective.github.io/learning-curve-collective-resources/'


# ------------------------------------------------------------------ text helpers
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
        return {k: (v if k in ('desmos', 'accept', 'fig', 'type', 'diff', 'sec', 'grp') else nw_all(v)) for k, v in o.items()}
    return o


def dz(rows, cap='Type this in Desmos'):
    """Mock of the Desmos expression list.
    rows: list of dicts {x: latex, out: [latex...], stat: latex, val: latex, see: text, note: text}"""
    h = '<div class="dz" role="group" aria-label="Lines to type in Desmos and what Desmos shows"><div class="dz-cap">' + cap + '</div>'
    for i, r in enumerate(rows, 1):
        if isinstance(r, str):
            r = {'x': r}
        h += '<div class="dz-row"><span class="dz-n">' + str(i) + '</span><div class="dz-main"><div class="dz-x">$' + r['x'] + '$</div>'
        if r.get('out') or r.get('stat'):
            h += '<div class="dz-out"><span class="dz-lab">Desmos reports</span>'
            for o in r.get('out', []):
                h += '<span>$' + o + '$</span>'
            if r.get('stat'):
                h += '<span class="dz-stat">$' + r['stat'] + '$</span>'
            h += '</div>'
        if r.get('see'):
            h += '<div class="dz-see">' + r['see'] + '</div>'
        h += '</div>'
        if r.get('val'):
            h += '<span class="dz-val">$= ' + r['val'] + '$</span>'
        h += '</div>'
    return h + '</div>'


def kbd(*keys):
    return ' '.join('<span class="kbd">' + k + '</span>' for k in keys)


def table(xs, ys):
    """Desmos load item: a two-column table x1 / y1."""
    return {'table': [list(xs), list(ys)]}


def window(l, r, b, t):
    return {'bounds': [l, r, b, t]}


DEGREES = {'degrees': True}


def slider(letter, start, lo=-20, hi=20, step=1):
    """Desmos load item: a slider with a set range, so the answer is reachable."""
    return {'expr': {'latex': '%s=%s' % (letter, start), 'sliderBounds': {'min': str(lo), 'max': str(hi), 'step': str(step)}}}

DZ_CSS = r'''
.dz { border: 1.5px solid #C9C9C9; border-radius: 8px; overflow: hidden; background: #fff; margin: 10px 0 12px; max-width: 470px; font-size: 15px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.ref-page .dz { margin-left: 24px; }
.dz-cap { background: #F1F1F1; border-bottom: 1px solid #DCDCDC; padding: 5px 12px; font: 700 10.5px 'Inter', sans-serif; letter-spacing: 0.8px; text-transform: uppercase; color: #5A5A5A; }
.dz-row { display: flex; align-items: stretch; border-bottom: 1px solid #E4E4E4; }
.dz-row:last-child { border-bottom: none; }
.dz-n { flex: 0 0 28px; background: #F1F1F1; border-right: 1px solid #E4E4E4; color: #8A8A8A; font: 600 11px 'Inter', sans-serif; padding: 9px 0 0 7px; }
.dz-main { flex: 1; padding: 8px 12px; min-width: 0; }
.dz-x { color: #1E1E1E; overflow-x: auto; }
.dz-out { margin-top: 6px; padding-top: 5px; border-top: 1px dashed #D6D6D6; display: flex; flex-wrap: wrap; gap: 2px 18px; font-size: 14px; color: var(--green-dark); }
.dz-out .dz-lab { flex-basis: 100%; font: 700 9.5px 'Inter', sans-serif; letter-spacing: 0.8px; text-transform: uppercase; color: #8A8A8A; }
.dz-out .dz-stat { color: var(--copper); }
.dz-see { margin-top: 5px; font: 500 12.5px 'Inter', sans-serif; color: var(--text-medium); line-height: 1.45; }
.dz-val { align-self: center; margin: 6px 10px 6px 0; padding: 3px 9px; background: #F1F1F1; border: 1px solid #DCDCDC; border-radius: 5px; font-size: 14px; white-space: nowrap; color: #1E1E1E; }
.kbd { display: inline-block; background: #F4F4F4; border: 1px solid #CFCFCF; border-bottom-width: 2px; border-radius: 4px; padding: 0 6px; font: 600 12.5px 'Inter', monospace; color: var(--brown-dark); white-space: nowrap; line-height: 1.5; }
.fig .circ { fill: none; stroke: #21442B; stroke-width: 2.2; }
.fig .shade2 { fill: rgba(188,108,38,0.16); stroke: none; }
.fig .gdot { fill: #8A8A8A; stroke: #fff; stroke-width: 1.2; }
@media (max-width: 768px) { .ref-page .dz { margin-left: 0; } }
'''


def _extract(name):
    src = open(FUNC_BUILDER, encoding='utf-8').read()
    m = re.search(r"^" + name + r" = r'''(.*?)'''", src, flags=re.S | re.M)
    assert m, name
    return m.group(1)


CURVES_JS = _extract('CURVES_JS')
GRID_JS = _extract('GRID_JS')
FIG_CSS = _extract('FIG_CSS')

# extra figure pieces for the Desmos sheets: circles, a second shaded polygon, gray "points of interest"
POLY2_JS = r'''    (o.poly2 ? [o.poly2] : []).forEach(function(pl) {
        s += '<polygon class="shade2" points="' + pl.map(function(p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '"/>';
    });
'''
CIRC_JS = r'''    (o.circles || []).forEach(function(c) {
        s += '<ellipse class="circ" clip-path="url(#clip' + id + ')" cx="' + X(c.x) + '" cy="' + Y(c.y) + '" rx="' + (X(c.x + c.r) - X(c.x)) + '" ry="' + (Y(c.y) - Y(c.y + c.r)) + '"/>';
    });
'''
GDOT_JS = r'''    (o.gdots || []).forEach(function(p) {
        s += '<circle class="gdot" cx="' + X(p.x) + '" cy="' + Y(p.y) + '" r="4.4"/>';
        if (p.label) s += '<text class="sm" x="' + (X(p.x) + (p.dx == null ? 7 : p.dx)) + '" y="' + (Y(p.y) + (p.dy == null ? -7 : p.dy)) + '">' + p.label + '</text>';
    });
'''


def _clean(o):
    if isinstance(o, str):
        return o.replace('\\"', '"')
    if isinstance(o, list):
        return [_clean(v) for v in o]
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    return o


def js_data(name, data):
    return 'var ' + name + ' = ' + json.dumps(_clean(data), ensure_ascii=False).replace('</', '<\\/') + ';\n'


def sub1(src, pattern, repl, flags=0, count=1):
    new, n = re.subn(pattern, lambda m: repl(m) if callable(repl) else repl, src, count=count, flags=flags)
    if n != count:
        sys.exit('pattern not found (%d of %d): %r' % (n, count, pattern[:80]))
    return new


def replace_once(src, old, new):
    if src.count(old) != 1:
        sys.exit('expected exactly one occurrence (%d): %r' % (src.count(old), old[:100]))
    return src.replace(old, new)


import desmos_voice as voice


# ------------------------------------------------------------------ Bluebook Tools tab (sheet 1)
def _tools_from_old_sheet():
    """Extracts the answer-format practice, the type-it-in practice and the formula reference
    from SAT-Desmos-Strategies.html. This is how desmos_tools_tab.json was made."""
    old = open(OLD_DESMOS, encoding='utf-8').read()
    i = old.index('<div id="tab-fillin"')
    j = old.index('<!-- ═══ TAB 6: PRACTICE')
    seg = old[i:j].rstrip()
    # fold the formulas tab into the same tab; renumber its section header
    a = seg.index('<!-- ═══ TAB 5: FORMULAS')
    fill, formulas = seg[:a].rstrip(), seg[a:]
    assert fill.endswith('</div>')
    fill = fill[:-len('</div>')].rstrip()
    formulas = formulas[formulas.index('<div class="section-header">'):]
    formulas = replace_once(formulas, '<div class="section-number">1</div>\n            <h2>Do They Provide Any Formulas?</h2>',
                            '<div class="section-number">4</div>\n            <h2>Do They Provide Any Formulas?</h2>')
    html = fill + '\n\n        ' + formulas
    # css rules the shell does not carry
    css_src = old[old.index('<style>'):old.index('</style>')]
    keep = ('formula-grid', 'formula-tile', 'fmt-', 'idea-box', 'warning-box', 'highlight-box', '.sp-', '.fs-', '.fp-', 'btn-mini', 'ext-link')
    rules = re.findall(r'(?m)^(?:@media[^{]*\{[^{}]*\{[^{}]*\}[^{}]*\}|[^{}@\n][^{}]*\{[^{}]*\})', css_src)
    css = '\n'.join(r.strip() for r in rules if any(k in r.split('{')[0] for k in keep))
    css += '\n#tab-fillin .card { margin-bottom: 20px; }\n#tab-fillin .card p { margin-bottom: 10px; line-height: 1.7; }\n#tab-fillin .section-header { margin-top: 30px; }\n#tab-fillin .section-header:first-child { margin-top: 0; }'
    a = old.index('/* ══════════ Formatting sprint ══════════ */')
    b = old.index('</script>', a)
    js = old[a:b].rstrip()
    assert 'rk:' not in html and 'rk:' not in js
    return html, css, js


def bluebook_tools_parts():
    """The Bluebook Tools tab for sheet 1: snapshot source plus the voice pass."""
    if os.path.exists(TOOLS_SNAPSHOT):
        d = json.load(open(TOOLS_SNAPSHOT, encoding='utf-8'))
        html, css, js = d['html'], d['css'], d['js']
    else:
        html, css, js = _tools_from_old_sheet()
    # LCCo voice pass: visible copy only
    html = voice.apply(html, voice.TOOLS_HTML, 'tools html')
    js = voice.apply(js, voice.TOOLS_JS, 'tools js')
    assert "indexOf('Next')" in js and 'Next &rarr;' in js   # the sprint key handler looks for this label
    return html, css, js


# ------------------------------------------------------------------ drills-only layout (SAT Desmos 3)
CH_ORDER_JS = r"""
/* Practice by Move: grouped by move, or shuffled so the student identifies the move */
var chShuffle = false, chPerm = null;
function chOrder() {
    var n = CHALLENGE.length, a = [];
    for (var k = 0; k < n; k++) a.push(k);
    if (!chShuffle) return a;
    if (!chPerm || chPerm.length !== n) {
        chPerm = a.slice();
        for (var j = n - 1; j > 0; j--) { var r = Math.floor(Math.random() * (j + 1)); var t = chPerm[j]; chPerm[j] = chPerm[r]; chPerm[r] = t; }
    }
    return chPerm;
}
function chSetOrder(sh) { chShuffle = sh; if (sh) chPerm = null; renderChallenge(); }
"""


def drills_mode(html):
    """No worked-example stepper. The challenge tab becomes Practice by Move (grouped, with a Shuffled
    switch) and the practice set becomes the Timed Practice Set. Applied after the voice pass, so the
    anchors below are the shell's strings as the voice table leaves them."""
    r = replace_once
    # --- tab bar: drop the stepper tab, put Practice by Move before the timed set, renumber
    html = r(html, """<button class="tab-button" data-group="core" onclick="switchTab('core', this)">2. Worked Examples &amp; Practice</button>""", '')
    html = sub1(html, r'    <!-- ============ TAB 2: STEPPER ============ -->.*?(?=    <!-- ============ TAB 3: FLUENCY)', '', flags=re.S)
    html = r(html, '<span class="row-label">Learn</span>', '<span class="row-label">Start</span>')
    html = r(html, '>3. Skill Practice</button>', '>2. Skill Practice</button>')
    html = r(html, """onclick="switchTab('gauntlet', this)">4. SAT-Style Practice</button>""", """onclick="switchTab('challenge', this)">3. Practice by Move</button>""")
    html = r(html, """onclick="switchTab('challenge', this)">5. Challenge Questions</button>""", """onclick="switchTab('gauntlet', this)">4. Timed Practice Set</button>""")
    html = r(html, '>6. Exit Ticket</button>', '>5. Exit Ticket</button>')
    html = r(html, '<div class="section-number">3</div><h2>Skill Practice drills: mixed reps</h2>', '<div class="section-number">2</div><h2>Skill Practice: quick drills</h2>')
    html = r(html, '<div class="section-number">4</div><h2>SAT-Style Practice: Choose Your Approach</h2>', '<div class="section-number">4</div><h2>Timed Practice Set</h2>')
    html = r(html, '<div class="section-number">5</div><h2>Challenge questions</h2>', '<div class="section-number">3</div><h2>Practice by move</h2>')
    html = r(html, '<div class="section-number">6</div><h2>Exit ticket</h2>', '<div class="section-number">5</div><h2>Exit ticket</h2>')
    # --- no stepper: guard its renderer, and take quick checks out of the results kit
    html = r(html, "function renderStep() {\n    var i = stepState.idx, s = STEPS[i];", "function renderStep() {\n    if (!STEPS.length) return;\n    var i = stepState.idx, s = STEPS[i];")
    html = sub1(html, r"\n[ \t]*L\.push\('Quick checks: '[^\n]*", '')
    html = sub1(html, r"\n[ \t]*tile\(s\.quick\.correct \+ '/' \+ s\.quick\.attempted, 'quick checks \(of ' \+ s\.quick\.total \+ '\)'\) \+", '')
    html = r(html, "tile(s.quick.correct + '/' + s.quick.attempted, 'quick checks') + ", '')
    html = sub1(html, r"\n[ \t]*h \+= '<h2>Quick checks \(worked examples\)</h2>'[^\n]*", '')
    # --- results kit labels for this layout
    html = r(html, "L.push('Practice set: '", "L.push('Timed practice set: '")
    html = r(html, "L.push('Challenge: '", "L.push('Practice by move: '")
    if html.count("'practice set'") != 2:
        sys.exit("drills: expected two 'practice set' tile labels")
    html = html.replace("'practice set'", "'timed set'")
    html = r(html, "'practice answered, not scored'", "'timed set answered, not scored'")
    html = r(html, "'practice answered'", "'timed set answered'")
    html = r(html, "'challenge (of '", "'by move (of '")
    html = r(html, "tile(s.challenge.correct + '/' + s.challenge.checked, 'challenge')", "tile(s.challenge.correct + '/' + s.challenge.checked, 'by move')")
    html = r(html, "h += '<h2>Practice set' + ", "h += '<h2>Timed practice set' + ")
    html = r(html, '&#8635; Retake practice set</button>', '&#8635; Retake timed set</button>')
    html = r(html, "{ tag: 'Practice Q' + i.n, i: i }", "{ tag: 'Timed set Q' + i.n, i: i }")
    html = r(html, "{ tag: 'Challenge ' + i.n, i: i }", "{ tag: 'By move, question ' + i.n, i: i }")
    html = r(html, "row(['C' + i.n + (i.starred", "row([i.n + (i.starred")
    html = r(html, "h += '<h2>Challenge questions</h2>' + table(['#', 'Difficulty',", "h += '<h2>Practice by move</h2>' + table(['#', 'Move',")
    html = r(html, 'saves your responses from the practice set, challenge questions, drills, quick checks, exit ticket, and takeaway in one file.',
             'saves your responses from the skill practice, the practice by move, the timed set, the exit ticket, and your takeaway in one file.')
    # --- Practice by Move: group headings, question numbers, the order switch
    html = r(html, "function renderChallenge() {\n    var host = document.getElementById('challengeArea');\n    var html = '';\n",
             CH_ORDER_JS.strip('\n') + "\nfunction renderChallenge() {\n    var host = document.getElementById('challengeArea');\n    var html = '';\n"
             "    var order = chOrder();\n"
             "    html += '<div class=\"toolbar\" style=\"margin-bottom:6px;\"><span style=\"font-size:13px; font-weight:700; color:var(--brown-dark);\">Question order</span> ' +\n"
             "        '<button class=\"btn btn-sm ' + (chShuffle ? 'btn-ghost' : 'btn-green') + '\" onclick=\"chSetOrder(false)\">By move</button> ' +\n"
             "        '<button class=\"btn btn-sm ' + (chShuffle ? 'btn-green' : 'btn-ghost') + '\" onclick=\"chSetOrder(true)\">Shuffled</button> ' +\n"
             "        '<span style=\"font-size:13px; color:var(--text-medium);\">' + (chShuffle ? 'The move label appears after you check each answer.' : 'Questions are grouped by the move they practice.') + '</span></div>';\n")
    html = r(html, "    CHALLENGE.forEach(function(p, i) {\n        var st = chState[i] || {};\n        html += '<div class=\"drill\" style=\"border-left-color: var(--gold);\">",
             "    order.forEach(function(i, pos) {\n        var p = CHALLENGE[i];\n        var st = chState[i] || {};\n"
             "        if (!chShuffle && p.grp && (pos === 0 || CHALLENGE[order[pos - 1]].grp !== p.grp)) html += '<h3 style=\"font-family:\\'Switzer\\',\\'Space Grotesk\\',sans-serif; color:var(--green-dark); margin:22px 0 10px;\">' + p.grp + '</h3>';\n"
             "        html += '<div class=\"drill\" style=\"border-left-color: var(--gold);\">")
    html = r(html, ">Challenge ' + (i+1) + ' of ' + CHALLENGE.length + (p.diff ? '<span class=\"diff-chip dark\">' + p.diff + '</span>' : '')",
             ">Question ' + (pos+1) + ' of ' + CHALLENGE.length + ((p.diff && (!chShuffle || st.checked)) ? '<span class=\"diff-chip dark\">' + p.diff + '</span>' : '') + ((chShuffle && st.checked) ? '<span style=\"text-transform:none; letter-spacing:0; font-weight:600;\">No. ' + (i+1) + ' in the by-move order</span>' : '')")
    # in the shuffled view the starred / extra chip also waits until the answer is checked
    html = r(html, "(p.ess ? '<span class=\"diff-chip dark star-chip\" title=\"Uses a starred move\">&#9733; starred move</span>' : '<span class=\"diff-chip dark\" style=\"opacity:0.7\" title=\"Uses an unstarred move\">extra</span>') + '</div>';",
             "((chShuffle && !st.checked) ? '' : (p.ess ? '<span class=\"diff-chip dark star-chip\" title=\"Uses a starred move\">&#9733; starred move</span>' : '<span class=\"diff-chip dark\" style=\"opacity:0.7\" title=\"Uses an unstarred move\">extra</span>')) + '</div>';")
    return html


# ------------------------------------------------------------------ the build
def build(c):
    html = open(SRC, encoding='utf-8').read()
    html = re.sub(r'\s*<p style="font-size:14px; margin-top:10px;">Ready for the next topic\?.*?</p>', '', html, flags=re.S)

    # --- header / titles / footer
    html = replace_once(html, '<title>SAT Math: Linear Equations</title>', '<title>' + c['title'] + '</title>')
    html = replace_once(html, '<h1>SAT Math: Linear Equations</h1>', '<h1>' + c['title'] + '</h1>')
    html = replace_once(html, 'CONCEPT + DRILLS &bull; LINEAR EQUATIONS', c['subtitle'])
    html = replace_once(html, 'SAT MATH SERIES', 'SAT DESMOS SERIES')
    html = replace_once(html, 'SAT Math Series: Linear Equations', c['footer'])
    html = replace_once(html, '>1. Linear Rules</button>', '>' + c['tab1'] + '</button>')
    html = replace_once(html, '<h2>Linear rules</h2>', '<h2>' + c['tab1_h2'] + '</h2>')

    # --- tab 1 body
    start = html.index('<div class="ref-page">') + len('<div class="ref-page">')
    end = html.index('</div>\n    </div>\n\n    <!-- ============ TAB 2')
    html = html[:start] + nw(c['RULES']).rstrip('\n') + '\n' + html[end:]

    # --- tab 2 intro card
    html = replace_once(html,
        '<p>Everything on the rules tab runs on one idea: <strong>a line is a starting value plus a constant rate.</strong> The intercept is where you start, the slope is how fast you move, and every SAT question about lines is asking you to find one of those two numbers, or to compare them across two lines.</p>',
        '<p>' + nw(c['tab2_intro']) + '</p>')
    html = replace_once(html,
        "The walkthrough below takes the rules one at a time, each with a worked example, the trap it pairs with, and a quick check. The starred steps are the essentials. Reading a rule isn't knowing it; the check is the point.",
        "The walkthrough covers each skill with a worked example, a common mistake to watch for, and a short check for understanding. <em>Load into Desmos</em> loads the example into the calculator so you can see what Desmos displays. Start with the starred skills, and practice entering each one on your own.")

    # --- tab 3 toolbar
    html = replace_once(html,
        'Untimed. Fractions can be entered as 7/3 or 2.333; both count. Negative slopes need the minus sign.',
        c['fluency_bar'])

    # --- tab 4 and tab 5 intro cards (whole paragraphs)
    html = sub1(html, r'(<div id="tab-gauntlet".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(c['tab4_intro']) + m.group(3), flags=re.S)
    html = sub1(html, r'(<div id="tab-challenge".*?<div class="card">\s*<p>)(.*?)(</p>)',
                lambda m: m.group(1) + nw(c['tab5_intro']) + m.group(3), flags=re.S)

    # --- tab 6: takeaway prompt and the extra-reps card
    html = replace_once(html,
        'One sentence you will say to yourself the next time a line shows up. Make it an if-then. (Shape: “When a system question says no solution, I ______ before I touch the constants.”)',
        c['exit_prompt'])
    html = sub1(html,
        r'<p style="font-size:14px; margin-top:10px;">For skill-by-skill reps.*?</p>\s*<p style="font-size:14px; margin-top:10px;">For the calculator side.*?</p>',
        c['exit_links'], flags=re.S)

    # --- data arrays
    for name in ('STEPS', 'FLUENCY', 'GAUNTLET', 'CHALLENGE', 'EXIT'):
        html = sub1(html, r'var ' + name + r' = \[.*?\];\n', js_data(name, nw_all(c[name])), flags=re.S)

    # --- figures
    start = html.index('var FIGS = {')
    tail = "function fig(name) { return FIGS[name] ? graphSVG(FIGS[name]) : ''; }"
    end = html.index(tail) + len(tail)
    html = html[:start] + c['FIGS_JS'] + html[end:]
    html = replace_once(html,
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker></defs>';""",
        """    s += '<defs><marker id="' + id + '" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2D2D2D"/></marker>' +
        '<clipPath id="clip' + id + '"><rect x="' + X(xmin) + '" y="' + Y(ymax) + '" width="' + (X(xmax) - X(xmin)) + '" height="' + (Y(ymin) - Y(ymax)) + '"/></clipPath></defs>';""")
    html = replace_once(html, "    if (o.poly) {\n", GRID_JS + POLY2_JS + "    if (o.poly) {\n")
    html = replace_once(html, "    (o.lines || []).forEach(function(l) {\n", CURVES_JS + CIRC_JS + "    (o.lines || []).forEach(function(l) {\n")
    html = replace_once(html, "    (o.labels || []).forEach(function(t) {\n", GDOT_JS + "    (o.labels || []).forEach(function(t) {\n")
    html = replace_once(html, ".fig .sq { fill: none; stroke: #2D2D2D; stroke-width: 1.2; }", FIG_CSS + DZ_CSS)

    # --- Desmos: richer loads, a Load button on worked examples, none on unanswered questions
    html = replace_once(html,
        "        list.forEach(function(l, i) { desmosCalc.setExpression({ id: 'load' + i, latex: l }); });",
        "        if (desmosCalc.updateSettings) desmosCalc.updateSettings({ degreeMode: false });\n"
        "        if (desmosCalc.setMathBounds) desmosCalc.setMathBounds({ left: -10, right: 10, bottom: -10, top: 10 });\n"
        "        list.forEach(function(l, i) {\n"
        "            if (typeof l === 'string') desmosCalc.setExpression({ id: 'load' + i, latex: l });\n"
        "            else if (l.table) desmosCalc.setExpression({ id: 'load' + i, type: 'table', columns: [{ latex: 'x_{1}', values: l.table[0].map(String) }, { latex: 'y_{1}', values: l.table[1].map(String) }] });\n"
        "            else if (l.bounds) desmosCalc.setMathBounds({ left: l.bounds[0], right: l.bounds[1], bottom: l.bounds[2], top: l.bounds[3] });\n"
        "            else if (l.degrees) desmosCalc.updateSettings({ degreeMode: true });\n"
        "            else if (l.expr) desmosCalc.setExpression(Object.assign({ id: 'load' + i }, l.expr));\n"
        "        });")
    html = replace_once(html,
        "(solOpen[i] ? 'Hide solution' : 'Show solution') + '</button></div>' +",
        "(solOpen[i] ? 'Hide solution' : 'Show solution') + '</button> ' + desmosBtn(s) + '</div>' +")
    html = replace_once(html, "        desmosBtn(p) +\n        '<span style=\"flex:1\"></span><button class=\"btn btn-gold\" onclick=\"gFinish()\">",
                        "        '<span style=\"flex:1\"></span><button class=\"btn btn-gold\" onclick=\"gFinish()\">")
    html = replace_once(html, """<button class="btn btn-green btn-sm" onclick="chCheck(' + i + ')">Check</button>' + desmosBtn(p) + '</div>';""",
                        """<button class="btn btn-green btn-sm" onclick="chCheck(' + i + ')">Check</button></div>';""")
    html = replace_once(html, "title=\"Graph this question\\'s equations\">&#128202; Load into Desmos</button>",
                        "title=\"Load these lines into the calculator\">&#128202; Load into Desmos</button>")

    # --- vocabulary: these sheets teach moves, not rules
    html = html.replace('starred rule', 'starred move')

    # --- misc: storage key, last-starred-step hint, step count
    html = html.replace('sat-linear-sheet:rule', c['key'] + ':rule')
    html = replace_once(html, "(i === 5 ? 'That was the last starred step. The next three are the extras.' : '')",
                        "(i === %d ? '%s' : '')" % (c['LAST_STARRED_STEP_INDEX'], c['last_hint']))
    html = replace_once(html, "Step 1 of 9", "Step 1 of %d" % len(c['STEPS']))

    # --- optional Bluebook Tools tab
    if c.get('bluebook_tools'):
        t_html, t_css, t_js = bluebook_tools_parts()
        html = replace_once(html,
            '            <button class="calc-btn" onclick="toggleDesmos()"',
            '            <button class="tab-button" data-group="core" onclick="switchTab(\'fillin\', this)">Bluebook Tools</button>\n'
            '            <button class="calc-btn" onclick="toggleDesmos()"')
        html = replace_once(html, '    <!-- ============ TAB 2: STEPPER ============ -->',
                            '    <!-- ============ BLUEBOOK TOOLS (ported from SAT Desmos Strategies) ============ -->\n    '
                            + t_html + '\n\n    <!-- ============ TAB 2: STEPPER ============ -->')
        html = replace_once(html, DZ_CSS, DZ_CSS + '\n/* Bluebook Tools tab */\n' + t_css + '\n')
        k = html.rindex('</body>')
        html = html[:k] + '<script>\n' + t_js + '\n</script>\n' + html[k:]

    # --- LCCo voice pass: visible shell and results-kit copy
    html = voice.apply(html, voice.SHELL, 'shell')
    if c.get('drills'):
        html = drills_mode(html)

    if '\u2014' in html:
        i = html.index('\u2014')
        sys.exit('em dash found: ' + html[max(0, i - 80):i + 40])
    os.makedirs(os.path.dirname(c['out']), exist_ok=True)
    open(c['out'], 'w', encoding='utf-8').write(html)
    print('wrote', c['out'], len(html), 'bytes;', len(c['STEPS']), 'steps,',
          sum(len(s['items']) for s in c['FLUENCY']), 'fluency,', len(c['GAUNTLET']), 'practice,',
          len(c['CHALLENGE']), 'challenge,', len(c['EXIT']), 'exit')
