#!/usr/bin/env python3
import argparse
import datetime
import random
import re
import sys
from collections import defaultdict
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple

from git import Repo
from git.objects.commit import Commit

COMMIT_RE: re.Pattern = re.compile("")
CATEGORIES: List[Tuple[str, str]] = []


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


def main(project_name: str = ""):
    if project_name:
        print(f"Generating changelog for {project_name}...")
    else:
        print("Generating changelog...")

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
        if not title.endswith("."):
            title += "."
        sections[section].append(f"* {title} [{commit.author}]")

    output.extend(process_month(sections, last_month))

    with open("CHANGELOG.md", "w") as outfile:
        outfile.writelines(line + "\n" for line in output)

    print("Done.")


def set_globals_from_categories(categories: str) -> None:
    """
    Set the `COMMIT_RE` and `CATEGORIES` globals from a string.
    """
    global COMMIT_RE, CATEGORIES
    for pair in categories.split("|"):
        shortcut, title = pair.split(":", 1)
        CATEGORIES.append((shortcut, title))
    shortcuts_re = rf"^({'|'.join([c[0] for c in CATEGORIES])}):\s*(.*)$"
    COMMIT_RE = re.compile(shortcuts_re)


def cli() -> int:
    parser = argparse.ArgumentParser(description="Generate a changelog.")
    parser.add_argument(
        "project_name",
        nargs="?",
        help="The project name",
    )
    parser.add_argument(
        "-s",
        "--stochasticity",
        metavar="N",
        type=int,
        default=1,
        help="How often to generate a change log (once every N runs)",
    )
    parser.add_argument(
        "-c",
        "--categories",
        metavar="C",
        type=str,
        default="fix:Fixes|feat:Features",
        help="The list of categories to use, along with their shortcuts",
    )

    args = parser.parse_args()
    set_globals_from_categories(args.categories)
    if random.random() > (1 / args.stochasticity):
        print("Will not generate a changelog right now because of stochasticity.")
        return 0
    main(args.project_name if args.project_name else "")
    return 0


if __name__ == "__main__":
    sys.exit(cli())
