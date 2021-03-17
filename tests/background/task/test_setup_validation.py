import pytest

from background import task


def test_tasks_cannot_be_lambdas():
    with pytest.raises(AssertionError) as e:
        from .hard_fails import cannot_be_lambda

    assert "Task['<lambda>'] cannot be a nameless lambda" == str(e.value)


def test_tasks_must_be_global():
    def foo():
        ...

    with pytest.raises(AssertionError) as e:
        task()(foo)

    assert (
        "Task['test_tasks_must_be_global.<locals>.foo'] must be defined at the global scope of a module"
        == str(e.value)
    )


def test_tasks_cannot_be_class_methods():
    with pytest.raises(AssertionError) as e:
        from .hard_fails import cannot_be_class_method

    assert "Task['Foo.bar'] must be defined at the global scope of a module" in str(
        e.value
    )


@pytest.mark.parametrize(("input",), ([None], [True], [False], [1], [""]))
def test_task_must_be_a_function(input):
    with pytest.raises(AssertionError) as e:
        task()(input)

    assert "is not a function" in str(e.value)


def test_task_cannot_be_a_class():
    class Foo:
        def __call__(self):
            ...

    with pytest.raises(AssertionError) as e:
        task()(Foo)

    assert "is not a function" in str(e.value)
