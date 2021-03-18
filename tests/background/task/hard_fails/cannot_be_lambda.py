from fops.background import task

# Lambdas are nameless. Tasks must be discoverable.
x = task()(lambda: None)
