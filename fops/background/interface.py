from __future__ import annotations

from typing import NamedTuple

from typing_extensions import Callable, Protocol, TypedDict, TypeVar

# according to PEP 544: Protocol[...] must all be type variables
SupportsTask = TypeVar("SupportsTask", bound=Callable[..., None])


class TargetSpec(NamedTuple):
    module: str
    name: str


class ITask(Protocol[SupportsTask]):
    """Interface for the Task wrapper

    This interface is used to ensure type definitions are not lost
    for the user.
    For now, we're happy with saying that __call__ doesn't return anything.

    Once Pep-612 (ParamSpec) is merged into typing_extensions, we can migrate
    to that, which will enable us to mangle the Return statement to provide
    metadata to the caller.
    """

    # attributes
    target_spec: TargetSpec
    wrapped_func: SupportsTask

    # hacks
    __call__: SupportsTask
    fire_and_forget: SupportsTask

    def execute(self, event: TaskEventPayload) -> None:
        ...


class TaskEventPayload(TypedDict):
    body: str


class TaskEventMeta(TypedDict, total=False):
    traceId: str


class TaskEvent(TypedDict):
    target: str  # f"{func.__module__}:{func.__name__}"
    payload: TaskEventPayload
    meta: TaskEventMeta


class ITransport(Protocol):
    def send(self, event: TaskEvent) -> None:
        ...

    def on_receive(self, event: TaskEvent) -> None:
        ...
