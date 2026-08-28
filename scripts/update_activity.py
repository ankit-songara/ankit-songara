"""Regenerate the self-updating blocks in README.md.

Two sections are rewritten in place, between HTML comment markers:

  ACTIVITY  most recent public activity, one row per non-fork repo
  LANGS     language byte totals aggregated across all original repos

Everything comes from the public GitHub REST API, so nothing here depends on
a third-party card service staying up. Run by
.github/workflows/update-activity.yml.
"""

import json
import os
import re
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "ankit-songara")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
README = "README.md"
MAX_ROWS = 5
MAX_LANGS = 8
BAR_WIDTH = 26

VERB = {
    "PushEvent": "pushed to",
    "CreateEvent": "started",
    "PullRequestEvent": "opened a PR in",
    "IssuesEvent": "filed an issue in",
    "ReleaseEvent": "released",
}

# Languages that are almost always vendored assets rather than work I wrote.
LANG_SKIP = {"Makefile", "Dockerfile", "Batchfile", "Procfile"}


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
    """Every original (non-fork, non-archived) repo owned by USER."""
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


def ago(stamp):
    then = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    mins = int((datetime.now(timezone.utc) - then).total_seconds() // 60)
    if mins < 60:
        return "just now" if mins < 5 else "%dm ago" % mins
    if mins < 1440:
        return "%dh ago" % (mins // 60)
    days = mins // 1440
    return "yesterday" if days == 1 else "%dd ago" % days


def render_activity(own_names):
    try:
        events = api("/users/%s/events/public?per_page=100" % USER)
    except Exception as exc:
        print("event fetch failed: %s" % exc)
        return None

    rows, seen = [], set()
    for ev in events:
        verb = VERB.get(ev.get("type"))
        name = ev["repo"]["name"]
        if not verb or name in seen or name not in own_names:
            continue
        seen.add(name)
        rows.append(
            "| `%s` | [**%s**](https://github.com/%s) | %s |"
            % (verb, name.split("/", 1)[1], name, ago(ev["created_at"]))
        )
        if len(rows) >= MAX_ROWS:
            break

    if not rows:
        return "_Nothing public in the last few days — probably heads-down on something internal._"
    return "| | repo | when |\n| --- | --- | --- |\n" + "\n".join(rows)


def render_langs(repos):
    """Bars by primary language per repo.

    Deliberately not byte counts: a single vendored frontend or committed
    asset directory outweighs every hand-written Go service and makes the
    chart say the opposite of what the work actually is.
    """
    totals = {}
    for repo in repos:
        lang = repo.get("language")
        if lang and lang not in LANG_SKIP:
            totals[lang] = totals.get(lang, 0) + 1

    grand = sum(totals.values())
    if not grand:
        return None

    top = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))[:MAX_LANGS]
    width = max(len(lang) for lang, _ in top)
    lines = []
    for lang, count in top:
        pct = 100.0 * count / grand
        filled = int(round(pct / 100 * BAR_WIDTH))
        lines.append(
            "%-*s  %s%s  %2d repo%s"
            % (width, lang, "█" * filled, "░" * (BAR_WIDTH - filled), count, "" if count == 1 else "s")
        )
    header = "primary language across %d original repos\n\n" % grand
    return "```text\n%s%s\n```" % (header, "\n".join(lines))


def replace(text, tag, body):
    if body is None:
        return text
    start, end = "<!-- %s:START -->" % tag, "<!-- %s:END -->" % tag
    block = "%s\n%s\n%s" % (start, body, end)
    return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, text, flags=re.S)


def main():
    repos = own_repos()
    own_names = {r["full_name"] for r in repos}
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    footer = "\n\n<sub>Auto-generated from the GitHub API · last refreshed %s</sub>" % stamp

    activity = render_activity(own_names)
    langs = render_langs(repos)

    with open(README, encoding="utf-8") as fh:
        text = fh.read()
    new = replace(text, "ACTIVITY", activity and activity + footer)
    new = replace(new, "LANGS", langs and langs + footer)

    if new == text:
        print("no change")
        return
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(new)
    print("README updated")


if __name__ == "__main__":
    main()
