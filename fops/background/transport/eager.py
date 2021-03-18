import logging

from ..interface import ITransport, TaskEvent

LOG = logging.getLogger(__name__)


class EagerTransport(ITransport):
    def send(self, event: TaskEvent) -> None:
        LOG.info(event)
        self.on_receive(event)

    def on_receive(self, event: TaskEvent) -> None:
        from .. import dispatch

        dispatch.receive(event)
