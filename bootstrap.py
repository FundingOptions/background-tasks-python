from fops.background import set_transport
from fops.background.transport import LambdaTransport

lambda_transport = LambdaTransport()
set_transport(lambda_transport)
