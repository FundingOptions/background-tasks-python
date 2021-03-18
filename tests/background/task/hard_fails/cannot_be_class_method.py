from fops.background import task


class Foo:
    @task()
    def bar(self):
        ...
