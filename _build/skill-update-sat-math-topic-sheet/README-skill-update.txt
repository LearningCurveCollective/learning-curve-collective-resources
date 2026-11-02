Skill files for .claude/skills/sat-math-topic-sheet (the remote tools cannot write into .claude).
Move them in with one Terminal line:

cd ~/Desktop/learning-curve-collective-resources && mv _build/skill-update-sat-math-topic-sheet/SKILL.md .claude/skills/sat-math-topic-sheet/SKILL.md && mv _build/skill-update-sat-math-topic-sheet/scripts/*.py .claude/skills/sat-math-topic-sheet/scripts/ && rm -r _build/skill-update-sat-math-topic-sheet
