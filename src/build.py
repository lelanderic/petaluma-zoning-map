#!/usr/bin/env python3
"""Assemble public/index.html from the template, the zone text in zones.py and the prepared assets.

Run from the repository root:  python3 src/build.py
Needs only the Python standard library.
"""
import base64, json, pathlib
import zones

SRC = pathlib.Path(__file__).parent
A = SRC / "assets"
OUT = SRC.parent / "public" / "index.html"

colors = json.loads((A / "colors.json").read_text())
stats = json.loads((A / "stats.json").read_text())
gp = json.loads((A / "gp_meta.json").read_text())
pud = json.loads((A / "pud_names.json").read_text())
total = sum(stats.values())

zs = []
for z in zones.ZONES:
    d = dict(z)
    d["col"] = "#%02x%02x%02x" % tuple(colors[z["c"]])
    d["pct"] = round(100 * stats[z["c"]] / total, 2)
    zs.append(d)
assert [z["c"] for z in zs] == list(stats.keys()), "zone order must match the lookup grid"


def uri(name, mime):
    return f"data:{mime};base64," + base64.b64encode((A / name).read_bytes()).decode()


def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


html = (SRC / "template.html").read_text()
for key, val in {
    "__ZONES__": js(zs),
    "__GROUPS__": js([dict(k=k, n=n, col=c) for k, n, c in zones.GROUPS]),
    "__OVERLAYS__": js(zones.OVERLAYS),
    "__LABELS__": js(zones.LABELS),
    "__PUDN__": js(pud),
    "__GPN__": js(gp["names"]),
    "__GPU__": js(gp["usual"]),
    "__BASE__": uri("base.webp", "image/webp"),
    "__GRID__": uri("grid.png", "image/png"),
    "__GP__": uri("gp.png", "image/png"),
}.items():
    assert key in html, key
    html = html.replace(key, val)
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html)
print(f"wrote {OUT} ({len(html) // 1024} KB)")
