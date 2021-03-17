from background import set_transport
from background.transport import LambdaTransport

lambda_transport = LambdaTransport()
set_transport(lambda_transport)
