from __future__ import annotations

import time
from collections import defaultdict
from pathlib import Path
from types import TracebackType
from typing import Sequence

try:
    import graphlib
except ImportError:
    import graphlib_backport as graphlib  # type: ignore

import rich.progress as progress

from myqueue.scheduler import Scheduler
from myqueue.task import Task
from myqueue.utils import plural
from myqueue.virtenv import find_activation_scripts

from .states import State

TaskName = Path


class DependencyError(Exception):
    """Bad dependency."""


def find_dependency(dname: TaskName,
                    current: dict[TaskName, Task],
                    new: dict[TaskName, Task],
                    force: bool = False) -> Task:
    """Convert dependency name to task."""
    if dname in current:
        task = current[dname]
        if task.state.is_bad():
            if force:
                if dname not in new:
                    raise DependencyError(dname)
                task = new[dname]
    elif dname in new:
        task = new[dname]
    else:
        raise DependencyError(dname)
    return task


def mark_children(task: Task, children: dict[Task, list[Task]]) -> None:
    """Mark children of task as FAILED."""
    for child in children[task]:
        child.state = State.FAILED
        mark_children(child, children)


def remove_bad_tasks(tasks: list[Task]) -> list[Task]:
    """Create list without bad dependencies."""
    children = defaultdict(list)
    for task in tasks:
        for dep in task.dtasks:
            children[dep].append(task)

    for task in list(children):
        if task.state.is_bad():
            mark_children(task, children)

    return [task for task in tasks if not task.state.is_bad()]


def submit_tasks(scheduler: Scheduler,
                 tasks: Sequence[Task],
                 current: dict[Path, Task],
                 force: bool,
                 max_tasks: int,
                 verbosity: int,
                 dry_run: bool) -> tuple[list[Task],
                                         list[Task],
                                         Exception | None]:
    """Submit tasks."""

    new = {task.dname: task for task in tasks}

    count: dict[State, int] = defaultdict(int)
    submit = []
    for task in tasks:
        if task.workflow:
            if task.dname in current:
                task.state = current[task.dname].state
            else:
                if task.state == State.undefined:
                    task.state = task.read_state_file()

        count[task.state] += 1

        if task.state == State.undefined:
            submit.append(task)
        elif task.state.is_bad() and force:
            task.state = State.undefined
            submit.append(task)

    count.pop(State.undefined, None)
    if count:
        print(', '.join(f'{state}: {n}' for state, n in count.items()))
    if any(state.is_bad() for state in count) and not force:
        print('Use --force to ignore failed tasks.')

    for task in submit:
        task.dtasks = []
        for dname in task.deps:
            dep = find_dependency(dname, current, new, force)
            if dep.state != 'done':
                task.dtasks.append(dep)

    n = len(submit)
    submit = remove_bad_tasks(submit)
    n = n - len(submit)
    if n > 0:
        print('Skipping', plural(n, 'task'), '(bad dependency)')

    submit = [task
              for task in graphlib.TopologicalSorter(
                  {task: task.dtasks for task in submit}).static_order()
              if task.state == State.undefined]

    submit = submit[:max_tasks]

    t = time.time()
    for task in submit:
        task.state = State.queued
        task.tqueued = t
        task.deps = [dep.dname for dep in task.dtasks]

    activation_scripts = find_activation_scripts([task.folder
                                                  for task in submit])
    for task in submit:
        task.activation_script = activation_scripts.get(task.folder)

    submitted = []
    ex = None

    pb: progress.Progress | NoProgressBar

    if verbosity and len(submit) > 1:
        pb = progress.Progress('[progress.description]{task.description}',
                               progress.BarColumn(),
                               progress.MofNCompleteColumn())
    else:
        pb = NoProgressBar()

    with pb:
        try:
            id = pb.add_task('Submitting tasks:', total=len(submit))
            for task in submit:
                scheduler.submit(
                    task,
                    dry_run,
                    verbosity >= 2)
                submitted.append(task)
                if not dry_run:
                    task.remove_state_file()
                pb.advance(id)
        except Exception as x:
            ex = x

    return submitted, submit[len(submitted):], ex


class NoProgressBar:
    def __enter__(self) -> NoProgressBar:
        return self

    def __exit__(self,
                 type: Exception,
                 value: Exception,
                 tb: TracebackType) -> None:
        pass

    def add_task(self, text: str, total: int) -> progress.TaskID:
        return progress.TaskID(0)

    def advance(self, id: progress.TaskID) -> None:
        pass
