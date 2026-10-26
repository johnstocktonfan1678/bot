# NL25 preflop drills

An offline web app for drilling the NL25 100bb preflop charts on an iPhone.
Pick the spots, then answer each dealt hand with fold / call / raise. Hands on
the edge of a range (borders, suit splits, solver mixes) come up most, and
hands you miss come back more often.

Three apps share the chart data and one offline cache:

- `docs/` is the drills app, `docs/table/` plays hands against bots, `docs/painter/` paints charts from memory.
- `docs/sw.js` caches all three so they run with no connection.
- `tools/extract.py` rebuilds `docs/data.js` from the slide deck's files.

## Install on iPhone

For each app (`/bot/`, `/bot/table/`, `/bot/painter/`):

1. Open its GitHub Pages URL in Safari.
2. Share → Add to Home Screen.
3. Open it once from the home screen while online. After that it works in airplane mode.
