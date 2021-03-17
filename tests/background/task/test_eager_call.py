import datetime

import pytest
from pydantic import ValidationError, validate_arguments

from background.interface import ITask

from .fake_tasks import (coerce_example, fake_task_multi_args,
                         fake_task_multi_kwargs, fake_task_no_params,
                         fake_task_one_arg, fake_task_one_arg_one_kwarg,
                         fake_task_one_kwarg)


def _supports_multi_param_detection():
    @validate_arguments
    def foo(x):
        ...

    try:
        foo(1, x=2)
        return False
    except (ValidationError, TypeError):
        return True


# https://github.com/samuelcolvin/pydantic/issues/2249
XFAIL_NO_MULTI_PARAM_DETECTION = pytest.mark.xfail(
    condition=not _supports_multi_param_detection(),
    reason="Pydantic does not support Multi Param detection yet",
    strict=True,
)


@pytest.fixture
def spy_task_call(mocker):
    def inner(task: ITask):
        return mocker.spy(task.wrapped_func.vd, "raw_function")

    return inner


@pytest.mark.parametrize(
    ("fake_task", "args", "kwargs"),
    [
        (fake_task_no_params, (), {}),
        (fake_task_one_arg, (1,), {}),
        (fake_task_one_kwarg, (), {}),
        (fake_task_one_kwarg, (), {"x": 2}),
        (fake_task_one_arg_one_kwarg, (1,), {}),
        (fake_task_one_arg_one_kwarg, (1,), {"y": 3}),
        (fake_task_multi_args, (1, 2), {}),
        (fake_task_multi_args, (1,), {"y": 2}),
        (fake_task_multi_args, (), {"x": 1, "y": 2}),
        (fake_task_multi_kwargs, (), {}),
        (fake_task_multi_kwargs, (1,), {}),
        (fake_task_multi_kwargs, (1, 2), {}),
        (fake_task_multi_kwargs, (), {"x": 1}),
        (fake_task_multi_kwargs, (), {"y": 2}),
        (fake_task_multi_kwargs, (), {"x": 1, "y": 2}),
    ],
)
def test_original_func_is_called_when_direct(fake_task, args, kwargs, spy_task_call):
    spy = spy_task_call(fake_task)

    fake_task(*args, **kwargs)

    spy.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize(
    ("fake_task", "args", "kwargs"),
    [
        (fake_task_no_params, (1,), {}),
        (
            fake_task_no_params,
            (),
            {"x": 1},
        ),
        (fake_task_no_params, (1,), {"x": 1}),
        (
            fake_task_one_arg,
            (),
            {},
        ),
        (fake_task_one_arg, (1, 2), {}),
        (
            fake_task_one_arg,
            (),
            {"never": 1},
        ),
        (
            fake_task_one_arg,
            (1,),
            {"never": 1},
        ),
        (
            fake_task_one_kwarg,
            (),
            {"never": 1},
        ),
        pytest.param(
            fake_task_one_kwarg, (1,), {"x": 2}, marks=XFAIL_NO_MULTI_PARAM_DETECTION
        ),
        (
            fake_task_one_arg_one_kwarg,
            (),
            {},
        ),
        (
            fake_task_one_arg_one_kwarg,
            (),
            {"y": 3},
        ),
        pytest.param(
            fake_task_one_arg_one_kwarg,
            (1,),
            {"x": 3},
            marks=XFAIL_NO_MULTI_PARAM_DETECTION,
        ),
        (
            fake_task_multi_args,
            (),
            {},
        ),
        (fake_task_multi_args, (1,), {}),
        (
            fake_task_multi_args,
            (1, 2, 3),
            {},
        ),
        (
            fake_task_multi_kwargs,
            (1, 2, 3),
            {},
        ),
        pytest.param(
            fake_task_multi_kwargs,
            (1,),
            {"x": 1},
            marks=XFAIL_NO_MULTI_PARAM_DETECTION,
        ),
        pytest.param(
            fake_task_multi_kwargs,
            (1, 2),
            {"y": 2},
            marks=XFAIL_NO_MULTI_PARAM_DETECTION,
        ),
        pytest.param(
            fake_task_multi_kwargs,
            (1, 2),
            {"x": 1, "y": 2},
            marks=XFAIL_NO_MULTI_PARAM_DETECTION,
        ),
        (
            fake_task_multi_kwargs,
            (),
            {"never": 1},
        ),
    ],
)
def test_error_raised_when_invalid_params_given(fake_task, args, kwargs):
    with pytest.raises(ValidationError) as e:
        fake_task(*args, **kwargs)

    errors = e.value.errors()
    type_errors = [error for error in errors if error.get("type") == "type_error"]

    # not ideal, we should split these tests into sections so we can assert based on the message.
    for error in errors:
        assert error["type"] in ["type_error", "value_error.missing"]


def test_coercion_int_from_str(spy_task_call):
    spy = spy_task_call(coerce_example)
    coerce_example(integer="1")

    spy.assert_called_once_with(integer=1)


def test_coercion_string_from_number(spy_task_call):
    spy = spy_task_call(coerce_example)
    coerce_example(string=20.0)

    spy.assert_called_once_with(string="20.0")


def test_coercion_boolean_from_string(spy_task_call):
    spy = spy_task_call(coerce_example)
    coerce_example(boolean="true")

    spy.assert_called_once_with(boolean=True)


def test_coercion_datetime_from_string(spy_task_call):
    spy = spy_task_call(coerce_example)
    coerce_example(dt="2020-01-01T05:00:00")

    spy.assert_called_once_with(dt=datetime.datetime(2020, 1, 1, 5, 0, 0))


def test_coercion_list_of_strings(spy_task_call):
    spy = spy_task_call(coerce_example)
    coerce_example(string_list=[1, 2.0, "x", b"y", True])

    spy.assert_called_once_with(string_list=["1", "2.0", "x", "y", "True"])
