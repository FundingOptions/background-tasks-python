from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, Optional

from .interface import ITransport
from .transport import EAGER

_transport: ContextVar[ITransport] = ContextVar(
    "background_tasks_transport", default=EAGER
)
get_transport = _transport.get
set_transport = _transport.set


@contextmanager
def using_transport(transport: Optional[ITransport] = None) -> Iterator[ITransport]:
    transport = transport or get_transport()
    token = set_transport(transport)
    try:
        yield transport
    finally:
        _transport.reset(token)
