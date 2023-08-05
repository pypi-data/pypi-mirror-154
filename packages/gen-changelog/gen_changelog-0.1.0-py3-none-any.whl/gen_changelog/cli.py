#!/usr/bin/env python3
import datetime
import re
import sys
from collections import defaultdict
from typing import Dict
from typing import Iterable
from typing import List

from git import Repo
from git.objects.commit import Commit

COMMIT_RE: re.Pattern = re.compile(r"^(fix|feat):\s*(.*)$")
CATEGORIES = (("fix", "Fixes"), ("feat", "Features"))


def get_conventional_commits(repo: Repo) -> Iterable[Commit]:
    """Get all commits that are prefixed with a category."""
    commits = sorted(
        repo.iter_commits(), key=lambda x: x.authored_datetime, reverse=True
    )
    conventional_commits = []
    for commit in commits:
        if not re.search(COMMIT_RE, commit.summary):
            continue
        conventional_commits.append(commit)
    return conventional_commits


def process_month(sections: Dict[str, List[str]], month: datetime.date) -> List[str]:
    """Process the commits of a given (full) month."""
    output = []
    if sections:
        output.append("\n")
        month_title = month.strftime("%B %Y")
        output.append(month_title)
        output.append("-" * len(month_title))

    for ctag, ctitle in CATEGORIES:
        if ctag in sections:
            output.append(f"\n### {ctitle}\n")
            output.extend(sections[ctag])

    return output


def main(project_name: str):
    repo = Repo(".")
    commits = get_conventional_commits(repo)
    last_month = datetime.date(1900, 1, 1)
    output = []

    log_title = f"{project_name} Changelog".strip()
    output.append(log_title)
    output.append("=" * len(log_title))

    sections: Dict[str, List[str]] = defaultdict(list)
    for commit in commits:
        dt = datetime.datetime.fromtimestamp(commit.authored_date)
        if dt.month != last_month.month:
            # The month changes (or we're done).
            output.extend(process_month(sections, last_month))

            sections = defaultdict(list)
            # We only need the month.
            last_month = dt.replace(day=1)

        section, title = COMMIT_RE.search(commit.summary).groups()  # type: ignore
        sections[section].append(f"* {title} - {commit.author}")

    output.extend(process_month(sections, last_month))

    with open("CHANGELOG.md", "w") as outfile:
        outfile.writelines(line + "\n" for line in output)


def cli():
    """The entrypoint for this script."""
    project_name = sys.argv[1] if len(sys.argv) > 1 else ""
    if project_name:
        print(f"Generating changelog for {project_name}...")
    else:
        print("Generating changelog...")
    main(project_name)


if __name__ == "__main__":
    cli()
