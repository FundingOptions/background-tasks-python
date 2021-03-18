import json
import logging
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

from ..interface import ITransport, TaskEvent

LOG = logging.getLogger(__name__)


class LambdaTransport(ITransport):
    def __init__(self, *, function_name: str = None, client: Any = None):
        self.function_name = function_name or os.getenv(
            "FOPS_BACKGROUND_TASKS_LAMBDA_NAME"
        )
        self.client = client or boto3.client("lambda")

    def send(self, event: TaskEvent) -> None:
        LOG.info(f"{self.__class__.__name__} start sending event: {event}")
        try:
            response = self.client.invoke(
                FunctionName=self.function_name,
                InvocationType="Event",
                Payload=json.dumps(event),
            )
        except ClientError as exc:
            LOG.error(f"{self.__class__.__name__}:{exc}")
        else:
            LOG.info(f"Result of sending by {self.__class__.__name__}: {response}")

    def on_receive(self, event: TaskEvent) -> None:
        from .. import dispatch

        dispatch.receive(event)

    def lambda_handler(self, event: TaskEvent, context) -> None:
        self.on_receive(event)
