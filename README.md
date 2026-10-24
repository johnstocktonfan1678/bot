# NL25 preflop drills

An offline web app for drilling the NL25 100bb preflop charts on an iPhone.
Pick the spots, then answer each dealt hand with fold / call / raise. Hands on
the edge of a range (borders, suit splits, solver mixes) come up most, and
hands you miss come back more often.

- `docs/` is the app (served by GitHub Pages). `docs/sw.js` caches it so it runs with no connection.
- `tools/extract.py` rebuilds `docs/data.js` from the slide deck's files.

## Install on iPhone

1. Open the GitHub Pages URL in Safari.
2. Share → Add to Home Screen.
3. Open it once from the home screen while online. After that it works in airplane mode.
