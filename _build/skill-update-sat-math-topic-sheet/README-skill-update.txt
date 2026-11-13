Builder files for the SAT Desmos series, waiting to move into .claude/skills/sat-math-topic-sheet/scripts
(the remote tools cannot write into .claude). They already work from here: run
  python3 _build/skill-update-sat-math-topic-sheet/scripts/build_desmos1.py
  python3 _build/skill-update-sat-math-topic-sheet/scripts/build_desmos2.py
to rebuild test-prep/sat/SAT-Desmos-1-Core-Moves.html and SAT-Desmos-2-Next-Steps.html.

Files: desmos_common.py (shared assembly on the SAT Math 1 shell), desmos_voice.py (the LCCo voice
table for shell, results-kit and Bluebook Tools copy), build_desmos1.py and build_desmos2.py (content),
desmos_tools_tab.json (snapshot of the Bluebook Tools tab source), verify_desmos.py (193 answer-key
recomputations; needs sympy).

To move them in, one Terminal line:

cd ~/Desktop/learning-curve-collective-resources && mv _build/skill-update-sat-math-topic-sheet/scripts/* .claude/skills/sat-math-topic-sheet/scripts/
