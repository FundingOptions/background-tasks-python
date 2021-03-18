from .aws_lambda import LambdaTransport
from .eager import EagerTransport

EAGER = EagerTransport()

__all__ = [
    "EagerTransport",
    "LambdaTransport",
    "EAGER",
]
