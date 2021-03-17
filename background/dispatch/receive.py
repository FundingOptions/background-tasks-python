from importlib import import_module

from ..interface import ITask, TaskEvent


def _load_target(target_def: str) -> ITask:
    # target_def always build by `_build_target` which only point the crisp syntax
    # In case of an error will turn out that the firing side did not use internal `fire` function
    assert target_def.count(":") == 1, f"Invalid TargetDef provided, '{target_def}'"

    module_name, fn_name = target_def.split(":")
    module = import_module(module_name)

    return getattr(module, fn_name)


def receive(event: TaskEvent) -> None:
    task = _load_target(event["target"])
    task.execute(event["payload"])
