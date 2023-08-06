#!/usr/bin/env python3

"""
Allows to see sorted by date TODOS from code
"""
__version__ = "0.1.6"

import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

from termcolor import colored
from tabulate import tabulate

import click
from git import GitCommandError, Repo

SEARCH_PATTERNS = ["TODO", "FIXME"]
FILES_FILTER = [".py"]


@dataclass
class TodoLine:
    filepath: str
    line: str
    date: datetime
    author: str


def find_todolines(path, repo_path, extensions) -> List[TodoLine]:
    repo = Repo(repo_path)
    todolines = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if not any(filename.endswith(e) for e in extensions):
                continue
            filepath = os.path.join(root, filename)
            try:
                line_num = 0
                for commit, lines in repo.blame("HEAD", filepath):
                    for l in lines:
                        line_num += 1
                        if hasattr(l, "decode"):
                            continue  # Byte str, skip
                        if any(p in l for p in SEARCH_PATTERNS):
                            todolines.append(
                                TodoLine(
                                    filepath=f'File "{filepath}:{line_num}"',
                                    line=l.lstrip(" "),
                                    date=commit.committed_datetime,
                                    author=commit.author.name,
                                )
                            )

            except GitCommandError:
                pass
    return todolines


def print_list(todos):
    for t in todos:
        print(colored(t.date, 'red'), colored(t.author, 'green'))
        print(t.line)
        print(colored(t.filepath, 'blue'))
        print()

def print_table(todos):
    print(tabulate([asdict(t) for t in todos], headers={'date': 'Date', 'author': 'Author', 'line':'Line', 'filepath': 'Path'}, tablefmt='fancy_grid'))

@click.command()
@click.option(
    "--path", default=os.getcwd(), help="Git repo path", type=click.Path(exists=True),
)
@click.option(
    "-e", multiple=True, default=FILES_FILTER, help="File extensions filters"
)
@click.option(
    '--table', default=True, help="Print as table"
)
def list_todos(path, e, table):
    if isinstance(e, str):
        e = (e,)

    repo_path = path
    while repo_path != '/':
        if '.git' not in os.listdir(repo_path):
            repo_path = os.path.dirname(repo_path)
        else:
            break
    if repo_path == '/':
        raise Exception('Git repo not found')

    todolines = find_todolines(path, repo_path, e)
    todolines = sorted(todolines, key=lambda t: t.date)
    if table:
        print_table(todolines)
    else:
        print_list(todolines)


if __name__ == "__main__":
    list_todos()
