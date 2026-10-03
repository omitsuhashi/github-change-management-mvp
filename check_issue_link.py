"""Validate same-repository Issue references in the latest PR body."""

import json
import os
import re
from urllib.request import Request, urlopen


def github_get(path):
    request = Request(
        f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}/{path}",
        headers={
            "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=15) as response:
        return json.load(response)


def check_issue_link():
    pull = github_get(f"pulls/{int(os.environ['PR_NUMBER'])}")
    numbers = sorted({int(number) for number in re.findall(
        r"^[ \t]*(?:refs?|close[sd]?|fix(?:es|ed)?|resolve[sd]?)[ \t]*:?[ \t]+#([1-9][0-9]*)[ \t]*\r?$",
        pull.get("body") or "",
        re.IGNORECASE | re.MULTILINE,
    )})
    if not numbers:
        raise ValueError("Add a standalone 'Refs #<issue-number>' line to the PR body.")
    repository_url = f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}"
    for number in numbers:
        issue = github_get(f"issues/{number}")
        if "pull_request" in issue:
            raise ValueError(f"#{number} is a pull request, not an Issue.")
        if issue["repository_url"] != repository_url or issue["number"] != number:
            raise ValueError(f"Issue #{number} has moved; use its current repository and number.")
    return numbers


if __name__ == "__main__":
    print("Validated related Issues:", check_issue_link())
