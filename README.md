Introduce a way to define + call Background Tasks using AWS Lambda's Async Invoke.

# Installation

```shell
$ pip install fops-background
```

This provides a decorator for use, that wraps arbitrary functions.

## Defining a task

```py
# your_module.tasks.py
import requests
from fops.background import task


@task()
def long_process(identifier: str, message: str):
    requests.post(f"https://external.service.com/{identifier}", json={"message": message}).raise_for_status()
```

### Restrictions

Decorated tasks can only be stand-alone functions, the below examples are **not** valid.

```py
# your_module.tasks.py
from fops.background import task


class CustomClass:
    @task()
    def long_process(self, identifier: str, message: str):
        pass

cc = CustomClass()

# cannot be associated with a class
cc.fire_and_forget("123ABC", "Order received")

# python lambdas are nameless. Tasks must be discoverable.
x = task()(lambda: None)
```

## Calling a task

Once a task is defined, you can call it in 2 ways:

```py
# main.py
from your_module.tasks import long_process

# forced sync
long_process("123ABC", "Order received")

# background mode
long_process.fire_and_forget("123ABC", "Order received")
```

## Configuring the backend

During the setup phase of the app, a backend Transport should be configured.
By default, we set up in Eager mode (which means that `fire_and_forget()` runs synchronously)

Initial configuration lives within the `bootstrap.py` file.

```py
# bootstrap.py
from fops.background import set_transport
from fops.background.transport import LambdaTransport

lambda_transport = LambdaTransport(function_name='my-lambda-function-name')
set_transport(lambda_transport)
```

Alternatively you can set the `BACKGROUND_TASKS_LAMBDA_NAME` environmental variable
and call the Transport with no arguments:

```py
# bootstrap.py
from fops.background import set_transport
from fops.background.transport import LambdaTransport

lambda_transport = LambdaTransport()
set_transport(lambda_transport)
```

You can also temporarily use a backend transport with the `using_transport` context manager:

```py
# main.py
from fops.background import using_transport
from fops.background.transport import EagerTransport
from your_module.tasks import long_process

with using_transport(EagerTransport()):
    long_process.fire_and_forget(...)
```

Configuration of the Lambda function is required before we can assign tasks to be run with the LambdaTransport.
Using the [serverless](https://www.serverless.com/framework/docs/getting-started/) package you need to configure the
`serverless.yml` file with a handler.

```yaml
...
  environment:
      BACKGROUND_TASKS_LAMBDA_NAME: "${self:functions.background.name}"

functions:
  background:
    handler: my_module.tasks.handler
    name: "my-lambda-function-name"
    timeout: 120

  other-function:
    handler: main.handler

```

You want this to reference the `.lambda_handler` function from our `LambdaHandler` instance:

```python
# your_module.tasks
from bootstrap import lambda_transport

handler = lambda_transport.lambda_handler
```

### AWS Permissions

The role assigned to your `other-function` needs the `lambda:InvokeFunction` permission enabled.
