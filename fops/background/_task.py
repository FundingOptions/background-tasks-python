from __future__ import annotations

import os
from inspect import getmodule, isfunction
from typing import Any, Callable, Optional

from pydantic import validate_arguments
from pydantic.decorator import ValidatedFunction

from . import dispatch
from .context import using_transport
from .interface import ITask, SupportsTask, TargetSpec, TaskEventPayload
from .transport import EAGER


def task(
    celery_app: Optional[Any] = None,
) -> Callable[[SupportsTask], ITask[SupportsTask]]:
    task_klass = Task
    if celery_app:
        task_klass.celery_app = celery_app

    return task_klass  # type: ignore


class Task:
    celery_app = None

    def __init__(self, fn: SupportsTask) -> None:
        self.compatibility_check(fn)
        # NOTE: this is just for retro-compatibility only, new tasks should use
        # @celery_app.task() decorator.
        if self.celery_app:
            self.celery_task = self.celery_app.task(fn)
        self.target_spec = TargetSpec(module=fn.__module__, name=fn.__name__,)
        self.wrapped_func = validate_arguments(fn)

    def __call__(self, *args, **kwargs) -> None:
        with using_transport(EAGER):
            self.fire_and_forget(*args, **kwargs)

    def fire_and_forget(self, *args, **kwargs) -> None:
        payload = self.construct_payload(*args, **kwargs)
        dispatch.fire(self, payload)

    def execute(self, payload: TaskEventPayload) -> None:
        validated_func = self.get_validated_function()
        instance = validated_func.model.parse_raw(payload["body"])

        if payload.get("is_celery", False) and self.celery_app:
            kwargs = instance.dict(exclude_unset=True)
            self.celery_task.delay(**kwargs)  # type: ignore
            return

        validated_func.execute(instance)

    @classmethod
    def compatibility_check(cls, fn: SupportsTask) -> None:
        module = getmodule(fn)
        fn_name = getattr(fn, "__qualname__", getattr(fn, "__name__", None))
        pretty_name = f"Task['{fn_name}']"

        assert isfunction(fn), f"{pretty_name} is not a function"
        assert module is not None, f"{pretty_name} not defined in a module"
        assert fn.__name__, f"{pretty_name} does not have a name"
        assert fn.__name__ != "<lambda>", f"{pretty_name} cannot be a nameless lambda"
        assert (
            "." not in fn.__qualname__
        ), f"{pretty_name} must be defined at the global scope of a module"

    def construct_payload(self, *args, **kwargs) -> TaskEventPayload:
        validated_func = self.get_validated_function()

        values = validated_func.build_values(args, kwargs)
        instance = validated_func.model(**values)
        encoded = instance.json(exclude_unset=True)

        is_celery = (
            os.environ.get("BACKGROUND_TASKS_USE_CELERY", False) or self.celery_app
        )

        return TaskEventPayload(body=encoded, is_celery=is_celery)

    def get_validated_function(self) -> ValidatedFunction:
        return self.wrapped_func.vd
