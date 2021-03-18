import datetime
from typing import List

from fops.background import task


@task()
def fake_task_no_params() -> None:
    pass


@task()
def fake_task_one_arg(x: int) -> None:
    pass


@task()
def fake_task_one_kwarg(x: int = 1) -> None:
    pass


@task()
def fake_task_one_arg_one_kwarg(x: int, y: int = 1) -> None:
    pass


@task()
def fake_task_multi_args(x: int, y: int) -> None:
    pass


@task()
def fake_task_multi_kwargs(x: int = 1, y: int = 1) -> None:
    pass


@task()
def coerce_example(
    integer: int = None,
    string: str = None,
    boolean: bool = None,
    dt: datetime.datetime = None,
    string_list: List[str] = None,
):
    pass
