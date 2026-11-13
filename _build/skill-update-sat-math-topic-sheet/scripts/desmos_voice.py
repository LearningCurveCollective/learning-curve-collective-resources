"""LCCo voice pass (2026-11-12): visible-copy replacements for the shared shell, the results kit
and the Bluebook Tools tab. Each entry is (old, new, count) and is applied with an exact count check.
Only literal learner-facing text is listed here. No identifiers, keys, selectors or logic."""
import sys


def apply(src, pairs, where):
    for old, new, count in pairs:
        c = src.count(old)
        if c != count:
            sys.exit('voice[%s]: expected %d, found %d: %r' % (where, count, c, old[:90]))
        src = src.replace(old, new)
    return src


# ------------------------------------------------------------------ shell + results kit
SHELL = [
    # tab 3 name (visible labels only; the tab id and the FLUENCY array keep their names)
    ('>3. Fluency Drills</button>', '>3. Skill Practice</button>', 1),
    ('<h2>Fluency drills: mixed reps</h2>', '<h2>Skill Practice drills: mixed reps</h2>', 1),
    ("'Done here? Fluency Drills is next.'", "'Finished here? Skill Practice is next.'", 1),
    ("L.push('Fluency drills: '", "L.push('Skill Practice drills: '", 1),
    ("'fluency (of '", "'drills (of '", 1),
    ("'<h2>Fluency drills</h2>'", "'<h2>Skill Practice drills</h2>'", 1),
    ("s.fluency.attempted, 'fluency')", "s.fluency.attempted, 'drills')", 1),
    # tab 4 heading
    ('SAT-Style Practice: Apply Your Strategy', 'SAT-Style Practice: Choose Your Approach', 1),
    # "trap" labels
    ('The trap it pairs with', 'A common mistake to watch for', 1),
    ('The trap / takeaway', 'Common mistake / takeaway', 1),
    ('<h2>Review list: the misses and the trap behind each</h2>',
     '<h2>Review list: missed questions, with the common mistake or takeaway for each</h2>', 1),
    ('<b>The trap:</b>', '<b>Common mistake / takeaway:</b>', 1),
    # feedback lines
    ("'✓ got it' : '✗ not yet'", "'✓ Correct' : '✗ Not quite. Review the explanation below, then try again.'", 1),
    ("'✗ not yet: retry, or peek below'", "'✗ Not quite. Try again, or review the explanation below.'", 1),
    ("'✗ not this time: the mechanism below is the takeaway'", "'✗ Not quite. The explanation below shows how it works.'", 1),
    ("'✗ not this time'", "'✗ Not quite'", 1),
    ("'✗ not yet'", "'✗ Not quite'", 1),
    ("'✓ correct'", "'✓ Correct'", 4),
    ('A fraction like 7/3 or a decimal like 2.333 both count.', 'A fraction like 7/3 and a decimal like 2.333 are both accepted.', 1),
    # calculator button tooltip
    ('Open the Desmos calculator (same one as the digital SAT)', 'Open the Desmos graphing calculator', 1),
    # sharing and saving
    ('Nothing on this sheet is sent anywhere by itself, and nothing is lost either: your answers stay saved in this browser.',
     'Your answers are saved in this browser, but they are not sent to your tutor automatically.', 1),
    ('Nothing on this page is sent anywhere by itself, and nothing is lost either: your answers stay saved in this browser.',
     'Your answers are saved in this browser, but they are not sent to your tutor automatically.', 1),
    ('makes one file with every answer on this sheet (the practice set, challenge questions, drills, quick checks, exit ticket, and your takeaway): text or email that file to your tutor. <strong>Copy summary</strong> gives a short version to paste into a message.',
     'saves your responses from the practice set, challenge questions, drills, quick checks, exit ticket, and takeaway in one file. You can send that file to your tutor by email or text. <strong>Copy summary</strong> copies a short summary you can share with your tutor.', 1),
    ('Your answers are saved in this browser automatically, so you can close the tab and come back.',
     'Your answers save automatically in this browser, so you can return to them later.', 1),
    # Bluebook pointer on the exit tab
    ('It is the real test interface, Desmos included, and its full-length practice tests are the closest thing to the actual SAT.',
     'Bluebook uses the same interface you will see on test day, including Desmos, and offers official full-length practice tests.', 1),
    # report table header: these sheets list moves, not rules
    ("table(['Step', 'Rule', '']", "table(['Step', 'Move', '']", 1),
]

# ------------------------------------------------------------------ Bluebook Tools tab: markup
TOOLS_HTML = [
    ('<h2>About a Quarter of Math Questions Have No Answer Choices</h2>', '<h2>Student-Produced Responses (Grid-Ins)</h2>', 1),
    ('<strong>A right answer typed the wrong way does not earn the point</strong>, so the format is worth two minutes of your life right now.',
     '<strong>Your entry needs to follow Bluebook&rsquo;s answer-format rules</strong>, so it is worth practicing the format before test day.', 1),
    ('Same rules apply. Just be sure to type the minus sign first.', 'The same rules apply. Type the minus sign first.', 1),
    ('Enter just one of them. Never a list like &ldquo;0.5 or &frac12;&rdquo;. Just pick one!',
     'Enter one of them, not a list like &ldquo;0.5 or &frac12;&rdquo;.', 1),
    ('Glance at it every time; it catches a stray character or a fraction typed as a decimal before you submit.',
     'Check it each time; it can help you catch a stray character or a mistyped fraction before you move on.', 1),
    ('<h2>Sprint: Would It Earn the Point?</h2>', '<h2>Answer-Format Practice: Accepted or Not?</h2>', 1),
    ('. Under three seconds an item is test speed.</p>', '. Once you feel comfortable, try responding without pausing for long.</p>', 1),
    ('Every item is decided by one of the six rules above.', 'Each item is based on one of the six rules above.', 1),
    ('<p>Now the real thing. Each answer is given in words.', '<p>Now practice with the answer-entry format. Each answer is written in words.', 1),
    ('The checker follows College Board&rsquo;s rules exactly: digits,', 'The checker is based on College Board&rsquo;s published entry rules: digits,', 1),
    ('Bluebook has a reference sheet you can open and close on any Math question. It covers geometry and basic trig. It does <strong>not</strong> cover algebra, which is most of the test, so the quadratic formula, slope, exponent rules, and the like must be memorized. Here is what the popup contains:',
     'Bluebook has a reference sheet you can open and close during the Math section. It covers geometry and basic trig. It does <strong>not</strong> cover algebra, so it helps to know the quadratic formula, slope, exponent rules, and similar formulas before test day. Here is what the reference sheet includes:', 1),
    ('<strong>Memorize these. They are NOT on the sheet:</strong>', '<strong>Review these formulas separately. They are not included on the reference sheet:</strong>', 1),
    ('Khan Academy posts the exact reference sheet Bluebook shows you:', 'Khan Academy posts a copy of the reference sheet:', 1),
]

# ------------------------------------------------------------------ Bluebook Tools tab: strings inside its script
# The answer data (expected value, typed entry, accepted or not, rule name) is untouched; only the explanations change.
TOOLS_JS = [
    ('so you have to fill every space: .6666 or .6667 (0.666 and 0.667 also work). .67 is cut short.',
     'so the entry needs to fill every space: .6666 or .6667 (0.666 and 0.667 also work). .67 is too short.', 1),
    ('"The fraction itself is always fine."', '"The fraction itself is accepted."', 1),
    ('"Enter just one number. Never a range or a list."', '"Enter one number, not a range or a list."', 1),
    ('"Pick one. Typing both is marked wrong."', '"Enter one of them. An entry that lists both is not accepted."', 1),
    ('Too short. College Board rejects -.33 and -0.33.', 'Too short. College Board lists -.33 and -0.33 as not accepted.', 1),
    ('>Sprint finished<small>', '>Round complete<small>', 1),
    ("(avg <= 3 ? '. That is test speed.' : '. Aim for under three.')",
     "(avg <= 3 ? '. That is a comfortable pace.' : '. These checks get quicker with practice.')", 1),
    ('>Run it again</button>', '>Try another round</button>', 1),
    ("'Type something first.'", "'Type an answer first.'", 1),
    ("'Exactly right: '", "'Correct. '", 1),
    ("'Risky. '", "'Check the length. '", 1),
    (' is not on their list, so do not gamble on it. Fill every space: ', ' is not on their list, so it may not be accepted. Fill every space: ', 1),
]
