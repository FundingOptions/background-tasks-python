from ..context import get_transport
from ..interface import ITask, TaskEvent, TaskEventPayload


def _build_target(task: ITask) -> str:
    target_spec = task.target_spec
    return f"{target_spec.module}:{target_spec.name}"


def _build_meta():
    return {}


def fire(task: ITask, payload: TaskEventPayload) -> None:
    target_def = _build_target(task)
    meta = _build_meta()

    event = TaskEvent(
        target=target_def,
        payload=payload,
        meta=meta,
    )

    transport = get_transport()
    transport.send(event)
