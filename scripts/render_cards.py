"""Draw the profile's SVG cards into assets/.

Everything here is rendered locally and committed to the repo, so the README
depends on no third-party card service. Each card is emitted twice, dark and
light, and the README picks one with <picture> + prefers-color-scheme.

Cards:
  header-{dark,light}.svg   terminal window, three phrases typing in a loop
  langs-{dark,light}.svg    primary-language-per-repo bars

Run by .github/workflows/update-activity.yml.
"""

import json
import os
import urllib.request

USER = os.environ.get("GH_USER", "ankit-songara")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = "assets"

HEADER_LINES = [
    "Backend Engineer @ Razorpay",
    "Go · Distributed Systems · Payments",
    "Learning in public.",
]

# GitHub's own language colours, so the bars read the way repo pages do.
LANG_COLOR = {
    "Go": "#00ADD8",
    "Python": "#3572A5",
    "HTML": "#E34C26",
    "C++": "#F34B7D",
    "TypeScript": "#3178C6",
    "JavaScript": "#F1E05A",
    "CSS": "#563D7C",
    "Shell": "#89E051",
    "Java": "#B07219",
    "Rust": "#DEA584",
    "Vue": "#41B883",
    "C": "#555555",
    "Dockerfile": "#384D54",
}
FALLBACK_COLOR = "#8B949E"

THEMES = {
    "dark": {
        "bg": "#0D1117",
        "chrome": "#161B22",
        "border": "#30363D",
        "text": "#C9D1D9",
        "dim": "#8B949E",
        "accent": "#58A6FF",
        "green": "#3FB950",
        "track": "#21262D",
    },
    "light": {
        "bg": "#FFFFFF",
        "chrome": "#F6F8FA",
        "border": "#D0D7DE",
        "text": "#1F2328",
        "dim": "#656D76",
        "accent": "#0969DA",
        "green": "#1A7F37",
        "track": "#EAEEF2",
    },
}

MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"
CHAR_W = 8.4  # advance width of the 14px monospace stack, measured empirically


def esc(text):
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER + "-profile-bot",
            **({"Authorization": "Bearer " + TOKEN} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def own_repos():
    repos, page = [], 1
    while True:
        batch = api("/users/%s/repos?type=owner&per_page=100&page=%d" % (USER, page))
        if not batch:
            break
        repos += [r for r in batch if not r["fork"] and not r["archived"]]
        if len(batch) < 100:
            break
        page += 1
    return repos


def window(width, height, title, theme, body):
    """Terminal-window chrome shared by every card."""
    t = THEMES[theme]
    dots = "".join(
        '<circle cx="%d" cy="16" r="5" fill="%s" opacity="0.85"/>' % (x, c)
        for x, c in ((22, "#FF5F56"), (40, "#FFBD2E"), (58, "#27C93F"))
    )
    return """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<style>text{{font-family:{mono};}}</style>
<rect x="0.5" y="0.5" width="{iw}" height="{ih}" rx="10" fill="{bg}" stroke="{border}"/>
<path d="M0.5 10.5a10 10 0 0 1 10-10h{cw}a10 10 0 0 1 10 10V32H0.5Z" fill="{chrome}"/>
<line x1="0.5" y1="32" x2="{w}" y2="32" stroke="{border}"/>
{dots}
<text x="{mid}" y="21" fill="{dim}" font-size="12" text-anchor="middle">{title}</text>
{body}
</svg>
""".format(
        w=width,
        h=height,
        iw=width - 1,
        ih=height - 1,
        cw=width - 21,
        mid=width / 2,
        mono=MONO,
        bg=t["bg"],
        chrome=t["chrome"],
        border=t["border"],
        dim=t["dim"],
        dots=dots,
        title=esc(title),
        body=body,
    )


def header_svg(theme):
    """Three phrases typed out in a loop, revealed by an animating clip."""
    t = THEMES[theme]
    width, slot = 680, 1.0 / len(HEADER_LINES)
    prompt_x, cycle = 24, 12
    body = ['<text x="%d" y="74" fill="%s" font-size="14">$</text>' % (prompt_x, t["green"])]
    text_x = prompt_x + 18

    cursor_times, cursor_x = [], []
    for i, line in enumerate(HEADER_LINES):
        run = len(line) * CHAR_W
        a = i * slot
        reveal = a + slot * 0.42
        hold = a + slot * 0.92
        end = (i + 1) * slot
        # Clip rect widens across the phrase, so the text appears to be typed.
        # The static width is the *resting* state, not the starting one: where
        # SMIL never runs (frame-zero snapshots, reduced motion, some readers)
        # the first phrase must still show fully rather than a blank card.
        body.append(
            '<clipPath id="t%d"><rect x="%d" y="56" height="26" width="%.1f">'
            '<animate attributeName="width" dur="%ds" repeatCount="indefinite"'
            ' values="0;0;%.1f;%.1f;0;0" keyTimes="0;%.4f;%.4f;%.4f;%.4f;1"/>'
            "</rect></clipPath>"
            % (i, text_x, run if i == 0 else 0, cycle, run, run, a, reveal, hold, end)
        )
        body.append(
            '<text x="%d" y="74" fill="%s" font-size="14" clip-path="url(#t%d)">%s</text>'
            % (text_x, t["accent"], i, esc(line))
        )
        cursor_times += [a, reveal, hold, end]
        cursor_x += [text_x, text_x + run, text_x + run, text_x]

    # One cursor for the whole cycle, not one per phrase, or the phrases that
    # are not showing would still park a caret over the visible line.
    body.append(
        '<rect y="62" width="8" height="15" fill="%s" x="%.1f">'
        '<animate attributeName="x" dur="%ds" repeatCount="indefinite"'
        ' values="%s" keyTimes="%s"/>'
        '<animate attributeName="opacity" dur="1s" repeatCount="indefinite"'
        ' values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1"/></rect>'
        % (
            t["dim"],
            text_x + len(HEADER_LINES[0]) * CHAR_W,
            cycle,
            ";".join("%.1f" % v for v in cursor_x),
            ";".join("%.4f" % v for v in cursor_times),
        )
    )

    return window(width, 104, "ankit@github: ~", theme, "\n".join(body))


def langs_svg(theme, rows, total):
    t = THEMES[theme]
    width, top, step = 680, 62, 30
    label_w = max(len(name) for name, _ in rows) * CHAR_W
    bar_x = 26 + label_w + 14
    bar_w = width - bar_x - 96
    body = [
        '<text x="26" y="50" fill="%s" font-size="12">primary language across %d repositories</text>'
        % (t["dim"], total)
    ]

    for i, (name, count) in enumerate(rows):
        y = top + i * step
        fill = LANG_COLOR.get(name, FALLBACK_COLOR)
        run = max(6.0, bar_w * count / total)
        body.append(
            '<text x="26" y="%d" fill="%s" font-size="14">%s</text>' % (y + 12, t["text"], esc(name))
        )
        body.append(
            '<rect x="%d" y="%d" width="%d" height="10" rx="5" fill="%s"/>'
            % (bar_x, y + 3, bar_w, t["track"])
        )
        # Deliberately not animated. A grow-on-load bar is only ever correct
        # once it finishes, and any renderer that samples it early reports the
        # wrong proportion — which is the whole point of the chart.
        body.append(
            '<rect x="%d" y="%d" width="%.1f" height="10" rx="5" fill="%s"/>'
            % (bar_x, y + 3, run, fill)
        )
        body.append(
            '<text x="%d" y="%d" fill="%s" font-size="13" text-anchor="end">%d repo%s</text>'
            % (width - 26, y + 12, t["dim"], count, "" if count == 1 else "s")
        )

    height = top + len(rows) * step + 14
    return window(width, height, "languages", theme, "\n".join(body))


def main():
    repos = own_repos()
    counts = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    rows = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
    total = sum(counts.values())
    if not rows:
        print("no languages found; leaving cards alone")
        return

    os.makedirs(OUT, exist_ok=True)
    for theme in THEMES:
        for name, svg in (
            ("header", header_svg(theme)),
            ("langs", langs_svg(theme, rows, total)),
        ):
            path = os.path.join(OUT, "%s-%s.svg" % (name, theme))
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(svg)
            print("wrote %s" % path)


if __name__ == "__main__":
    main()
