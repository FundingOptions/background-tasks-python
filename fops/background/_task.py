from __future__ import annotations

from inspect import getmodule, isfunction
from typing import Callable

from pydantic import validate_arguments
from pydantic.decorator import ValidatedFunction

from . import dispatch
from .context import using_transport
from .interface import ITask, SupportsTask, TargetSpec, TaskEventPayload
from .transport import EAGER


def task() -> Callable[[SupportsTask], ITask[SupportsTask]]:
    return Task  # type: ignore


class Task:
    def __init__(self, fn: SupportsTask) -> None:
        self.compatibility_check(fn)
        self.target_spec = TargetSpec(
            module=fn.__module__,
            name=fn.__name__,
        )
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

        return TaskEventPayload(body=encoded)

    def get_validated_function(self) -> ValidatedFunction:
        return self.wrapped_func.vd
