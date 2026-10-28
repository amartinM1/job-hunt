#!/usr/bin/env python3
"""Render a job posting's keywords as a bubble-map HTML page.

Usage:
    python keyword_map.py posting.json out.html

posting.json shape:
{
  "company": "Acme AI",
  "title": "Forward Deployed Engineer",
  "url": "https://...",
  "fit_score": 7,
  "fit_rationale": "one line",
  "sections": [
    {
      "name": "Required qualifications",
      "keywords": [
        {"term": "Python", "status": "gap", "note": "Daily language on the team"},
        {"term": "REST APIs", "status": "have", "note": "Spring Boot services at Citi"}
      ]
    }
  ]
}

status is one of: have | partial | gap. Gaps are the rabbit holes.
"""
import html
import json
import sys

STATUS_LABEL = {"have": "You have it", "partial": "Partial", "gap": "Rabbit hole"}
STATUS_ORDER = {"gap": 0, "partial": 1, "have": 2}


def esc(s):
    return html.escape(str(s or ""))


def render(data):
    sections = data.get("sections", [])
    counts = {"have": 0, "partial": 0, "gap": 0}
    for sec in sections:
        for kw in sec.get("keywords", []):
            counts[kw.get("status", "gap")] = counts.get(kw.get("status", "gap"), 0) + 1

    rabbit = []
    sec_html = []
    for sec in sections:
        kws = sorted(sec.get("keywords", []), key=lambda k: STATUS_ORDER.get(k.get("status"), 0))
        bubbles = []
        for kw in kws:
            st = kw.get("status", "gap")
            if st == "gap":
                rabbit.append((kw.get("term"), sec.get("name"), kw.get("note")))
            bubbles.append(
                f'<button class="bubble {esc(st)}" title="{esc(kw.get("note"))}">'
                f'<span class="term">{esc(kw.get("term"))}</span>'
                f'<span class="tip">{esc(STATUS_LABEL.get(st, st))}'
                f'{" · " + esc(kw.get("note")) if kw.get("note") else ""}</span></button>'
            )
        sec_html.append(
            f'<section class="cluster"><div class="hub">{esc(sec.get("name"))}'
            f'<small>{len(kws)}</small></div><div class="bubbles">{"".join(bubbles)}</div></section>'
        )

    rabbit_html = "".join(
        f"<li><strong>{esc(t)}</strong> <span class='src'>{esc(s)}</span>"
        f"{'<br><span class=note>' + esc(n) + '</span>' if n else ''}</li>"
        for t, s, n in rabbit
    ) or "<li>No hard gaps. Go apply.</li>"

    title = f"{data.get('company','')} keyword map".strip()
    score = data.get("fit_score", "")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>
:root{{--bg:#f7f6f2;--fg:#1d1d1b;--muted:#6b6a64;--card:#fff;--line:#e2e0d8;
--have:#d8f0de;--have-b:#2f8a4a;--part:#fbeccb;--part-b:#b7791f;--gap:#fadbd8;--gap-b:#c0392b;--hub:#1d1d1b;--hub-fg:#fff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151514;--fg:#ecebe6;--muted:#9a998f;--card:#1f1f1d;--line:#33322e;
--have:#183a23;--have-b:#5cc27c;--part:#3d2f12;--part-b:#e0a640;--gap:#421c18;--gap-b:#ef6b5c;--hub:#ecebe6;--hub-fg:#151514}}}}
:root[data-theme="dark"]{{--bg:#151514;--fg:#ecebe6;--muted:#9a998f;--card:#1f1f1d;--line:#33322e;
--have:#183a23;--have-b:#5cc27c;--part:#3d2f12;--part-b:#e0a640;--gap:#421c18;--gap-b:#ef6b5c;--hub:#ecebe6;--hub-fg:#151514}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px 48px}}
header h1{{margin:0;font-size:1.5rem}}header p{{margin:4px 0;color:var(--muted)}}header a{{color:inherit}}
.stats{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}}.stat{{padding:6px 12px;border-radius:999px;border:1.5px solid;font-weight:600;font-size:.85rem}}
.stat.fit{{border-color:var(--fg)}}.stat.have{{background:var(--have);border-color:var(--have-b)}}.stat.partial{{background:var(--part);border-color:var(--part-b)}}.stat.gap{{background:var(--gap);border-color:var(--gap-b)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}
.cluster{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;position:relative}}
.hub{{display:inline-flex;align-items:center;gap:8px;background:var(--hub);color:var(--hub-fg);border-radius:999px;padding:8px 14px;font-weight:700;margin-bottom:14px}}
.hub small{{opacity:.7;font-weight:500}}
.bubbles{{display:flex;flex-wrap:wrap;gap:8px;border-left:2px dashed var(--line);padding-left:12px;margin-left:16px}}
.bubble{{position:relative;font:inherit;color:var(--fg);border:1.5px solid;border-radius:999px;padding:6px 12px;cursor:default;text-align:left}}
.bubble.have{{background:var(--have);border-color:var(--have-b)}}.bubble.partial{{background:var(--part);border-color:var(--part-b)}}
.bubble.gap{{background:var(--gap);border-color:var(--gap-b);font-weight:600}}
.tip{{display:none;position:absolute;z-index:5;left:0;top:calc(100% + 6px);width:240px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 10px;font-size:.8rem;font-weight:400;box-shadow:0 6px 18px rgba(0,0,0,.15)}}
.bubble:hover .tip,.bubble:focus .tip{{display:block}}
aside{{margin-top:24px;background:var(--card);border:1.5px solid var(--gap-b);border-radius:18px;padding:16px 20px}}
aside h2{{margin:0 0 8px;font-size:1.1rem}}aside ul{{margin:0;padding-left:18px}}aside li{{margin:6px 0}}
.src{{color:var(--muted);font-size:.8rem}}.note{{color:var(--muted);font-size:.85rem}}
</style></head><body><main>
<header><h1>{esc(data.get('title',''))} · {esc(data.get('company',''))}</h1>
<p>{esc(data.get('fit_rationale',''))}</p>
{f'<p><a href="{esc(data.get("url"))}" target="_blank" rel="noopener">View posting</a></p>' if data.get('url') else ''}</header>
<div class="stats"><span class="stat fit">Fit {esc(score)}/10</span>
<span class="stat have">{counts['have']} have</span><span class="stat partial">{counts['partial']} partial</span>
<span class="stat gap">{counts['gap']} rabbit holes</span></div>
<div class="grid">{''.join(sec_html)}</div>
<aside><h2>Rabbit holes to go down</h2><ul>{rabbit_html}</ul></aside>
</main></body></html>"""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1]) as f:
        data = json.load(f)
    with open(sys.argv[2], "w") as f:
        f.write(render(data))


if __name__ == "__main__":
    main()
