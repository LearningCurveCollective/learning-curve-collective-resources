#!/bin/bash
# Double-click to publish: commits everything new in this folder and pushes it to GitHub Pages.
cd "$(dirname "$0")" || exit 1
echo "Learning Curve Collective resources: publishing..."
if [ -z "$(git config user.name)" ]; then
  git config user.name "Learning Curve Collective"
  git config user.email "torin@learningcurvecollective.com"
fi
git add -A
if git diff --cached --quiet; then
  echo "Nothing new to publish."
else
  echo "Files in this update:"; git diff --cached --name-status | sed 's/^/   /'
  git commit -q -m "Publish $(date '+%Y-%m-%d %H:%M')" && echo "Committed."
fi
if git push origin main; then
  echo
  echo "Pushed. The site updates in about a minute:"
  echo "https://learningcurvecollective.github.io/learning-curve-collective-resources/"
else
  echo
  echo "Push did not go through (usually a sign-in prompt). Open GitHub Desktop and click 'Push origin'; the commit is already saved."
fi
echo; read -n 1 -s -r -p "Press any key to close this window."
