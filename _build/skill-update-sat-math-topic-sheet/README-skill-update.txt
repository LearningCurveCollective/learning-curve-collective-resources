Files waiting to move into .claude/skills/sat-math-topic-sheet (the remote tools cannot write into .claude).

scripts/   Builder files for the SAT Desmos series and the SAT Math topic sheets. They already work from here: run
             python3 _build/skill-update-sat-math-topic-sheet/scripts/build_desmos1.py
             python3 _build/skill-update-sat-math-topic-sheet/scripts/build_desmos2.py
             python3 _build/skill-update-sat-math-topic-sheet/scripts/build_desmos3.py
           to rebuild the three SAT Desmos sheets in test-prep/sat/.
           desmos_common.py (shared assembly on the SAT Math 1 shell, including the drills-only layout used by
           SAT Desmos 3), desmos_voice.py (the LCC voice table for shell, results-kit and Bluebook Tools copy),
           build_desmos1.py, build_desmos2.py and build_desmos3.py (content), desmos_tools_tab.json (snapshot of
           the Bluebook Tools tab source), desmos3_source.json (snapshot of the retired sheet's practice and
           timed questions), verify_desmos.py (193 answer-key recomputations for sheets 1 and 2) and
           verify_desmos3.py (216 for sheet 3); both need sympy.
           build_quadratics.py and build_functions.py are the SAT Math 2 and SAT Math 3 builders, updated on
           2026-11-12: the Desmos link now goes to SAT Desmos 1 (the shell, SAT Math 1, was changed to match),
           and SAT Math 3 gained a forward link to SAT Desmos 2. They replace the copies already in the skill.

SKILL.md   The skill file updated on 2026-11-12: adds the three Desmos sheets to the series table, notes that
           the older Desmos sheet is retired, points all wording at the lcc-style-guide skill, and adds a
           language step to verification.

To move everything in, one Terminal line:

cd ~/Desktop/learning-curve-collective-resources && mv _build/skill-update-sat-math-topic-sheet/SKILL.md .claude/skills/sat-math-topic-sheet/SKILL.md && mv _build/skill-update-sat-math-topic-sheet/scripts/* .claude/skills/sat-math-topic-sheet/scripts/
