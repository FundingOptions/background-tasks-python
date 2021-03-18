import logging

import boto3
import pytest
from botocore.stub import Stubber

from fops.background import dispatch
from fops.background.context import using_transport
from fops.background.transport.aws_lambda import LambdaTransport


@pytest.fixture
def dispatch_receive_mock(mocker):
    yield mocker.patch.object(dispatch, "receive")


@pytest.fixture
def caplog(caplog):
    caplog.set_level(logging.INFO)
    yield caplog


@pytest.fixture(scope="function")
def lambda_stub(lambda_client):
    with Stubber(lambda_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(scope="function")
def lambda_client(aws_region):
    return boto3.client("lambda", region_name=aws_region, verify=False)


@pytest.fixture
def aws_region():
    return "eu-west-1"


@pytest.fixture
def lambda_transport(lambda_client, lambda_stub):
    with using_transport(
        LambdaTransport(client=lambda_client, function_name="test")
    ) as transport:
        yield transport


@pytest.fixture
def fake_event(mocker, faker):
    yield {"test": faker.pyint()}
