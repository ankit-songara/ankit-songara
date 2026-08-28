"""Regenerate the "Currently Working On" block in README.md.

Reads the user's recent public events, keeps the most recent activity per
non-fork repo, and rewrites the region between the ACTIVITY markers.
Run by .github/workflows/update-activity.yml.
"""

import json
import os
import re
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "ankit-songara")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
README = "README.md"
START = "<!-- ACTIVITY:START -->"
END = "<!-- ACTIVITY:END -->"
MAX_ROWS = 5

VERB = {
    "PushEvent": "pushed to",
    "CreateEvent": "started",
    "PullRequestEvent": "opened a PR in",
    "IssuesEvent": "filed an issue in",
    "ReleaseEvent": "released",
    "WatchEvent": "starred",
}


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


def ago(stamp):
    then = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    mins = int((datetime.now(timezone.utc) - then).total_seconds() // 60)
    if mins < 60:
        return "just now" if mins < 5 else "%dm ago" % mins
    if mins < 1440:
        return "%dh ago" % (mins // 60)
    days = mins // 1440
    return "yesterday" if days == 1 else "%dd ago" % days


def collect():
    try:
        events = api("/users/%s/events/public?per_page=100" % USER)
    except Exception as exc:  # network/rate-limit: leave the section untouched
        print("event fetch failed: %s" % exc)
        return None

    forks = set()
    seen = {}
    for ev in events:
        verb = VERB.get(ev.get("type"))
        if not verb or ev["type"] == "WatchEvent":
            continue
        name = ev["repo"]["name"]
        if name in seen:
            continue
        if name not in forks:
            try:
                if api("/repos/" + name).get("fork"):
                    forks.add(name)
                    continue
            except Exception:
                continue
        else:
            continue
        seen[name] = (verb, ev["created_at"])
        if len(seen) >= MAX_ROWS:
            break

    rows = []
    for name, (verb, stamp) in seen.items():
        short = name.split("/", 1)[1]
        rows.append(
            "| `%s` | [**%s**](https://github.com/%s) | %s |" % (verb, short, name, ago(stamp))
        )
    return rows


def render(rows):
    if not rows:
        return "_Nothing public in the last few days — probably heads-down on something internal._"
    header = "| | repo | when |\n| --- | --- | --- |"
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    return "%s\n%s\n\n<sub>Auto-generated from my public activity · last refreshed %s</sub>" % (
        header,
        "\n".join(rows),
        stamp,
    )


def main():
    rows = collect()
    if rows is None:
        return
    with open(README, encoding="utf-8") as fh:
        text = fh.read()
    block = "%s\n%s\n%s" % (START, render(rows), END)
    new = re.sub(
        re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S
    )
    if new != text:
        with open(README, "w", encoding="utf-8") as fh:
            fh.write(new)
        print("README updated with %d rows" % len(rows))
    else:
        print("no change")


if __name__ == "__main__":
    main()
