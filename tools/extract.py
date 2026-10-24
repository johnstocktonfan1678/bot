"""Extract chart data from the NL25 preflop slide deck into data.json.

Usage: python3 tools/extract.py <deck-folder-with-project/> docs/data.js
"""
import json, re, sys, os, html

COLORS = {"#cbc3b3": "fold", "#3a74c4": "call", "#58a394": "limp",
          "#e0782f": "raise", "#7a2e22": "allin", "#efece6": None}
AGGR = ["fold", "call", "limp", "raise", "allin"]  # least -> most aggressive

deck = sys.argv[1]
idx = json.load(open(os.path.join(deck, "project/deck.json")))
sections = {v["start"]: v["description"] for v in idx["sections"].values()}

def cells(svg):
    """Map hand label -> list of (x, width, action) rects for that cell."""
    out = {}
    pending = []
    for m in re.finditer(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="([^"]+)"/>|<text[^>]*>([^<]+)</text>', svg):
        if m.group(6):
            out[m.group(6)] = pending
            pending = []
        elif m.group(4) == "40":
            pending.append((int(m.group(1)), int(m.group(3)), COLORS[m.group(5)]))
    return out

def act(word):
    return {"fold": "fold", "call": "call", "check": "call", "limp": "limp"}.get(word, "raise")

spots, section = [], None
for sid in idx["order"]:
    if sid in sections:
        section = sections[sid]
    path = os.path.join(deck, "project/slides", sid + ".html")
    if not os.path.exists(path):
        continue
    s = open(path).read()
    svgs = dict((lab, body) for body, lab in re.findall(r'(<svg[^>]*aria-label="([^"]*)".*?</svg>)', s, re.S))
    if "Your range" not in svgs:
        continue
    title = html.unescape(re.search(r"<h2[^>]*>([^<]*)", s).group(1))
    labels = {}
    for row in re.findall(r"<tr><td[^>]*>(?:<span[^>]*>)?■(?:</span>)? ([^<]+)</td>", s):
        a = row.split()[0]
        key = {"fold": "fold", "call": "call", "check": "call", "limp": "limp", "all-in": "allin", "jam": "allin"}.get(a, "raise")
        labels[key] = row.strip()
    why = [html.unescape(re.sub(r"<[^>]+>", "", li)) for li in re.findall(r"<li[^>]*>(.*?)</li>", s, re.S)
           if not re.search(r" if (it has a ♥|♥/♦ suited)", li)]
    aside = re.search(r"<aside>(.*?)</aside>", s, re.S)
    yours, gto = cells(svgs["Your range"]), cells(svgs["GTO mix"])
    # Split hands are listed in prose, e.g. "<b>66</b>: call if it has a ♥, else fold"
    splits = {}
    for h, hi, cond, lo in re.findall(r"<b>(\w+)</b>: (\S+) if (it has a ♥|♥/♦ suited), else (\w+)", s):
        splits[h] = (act(hi), act(lo), "heart" if "has" in cond else "red")
    hands = {}
    for h, rects in yours.items():
        acts = [a for _, _, a in sorted(rects)]
        if acts == [None]:
            continue
        g = {}
        for _, w, a in gto.get(h, []):
            if a:
                g[a] = g.get(a, 0) + w / 40
        g = {k: round(v, 3) for k, v in g.items()}
        if h in splits:
            hi, lo, cond = splits[h]
            hands[h] = {"a": hi, "b": lo, "c": cond, "g": g}
        else:
            assert len(acts) == 1, (sid, h, acts)
            hands[h] = {"a": acts[0], "g": g}
    assert set(splits) <= set(hands), sid
    spots.append({"id": sid, "title": title, "section": section, "labels": labels,
                  "why": why, "notes": html.unescape(aside.group(1)).strip() if aside else "",
                  "hands": hands})

with open(sys.argv[2], "w") as f:
    f.write("window.SPOTS=" + json.dumps(spots, separators=(",", ":"), ensure_ascii=False) + ";\n")
print(len(spots), "spots")
