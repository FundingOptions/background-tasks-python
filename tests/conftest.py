import pytest
import responses


# TEST SETTINGS
@pytest.fixture(scope="function", autouse=True)
def stub_aws_credentials(monkeypatch):
    """Prevent accidentally firing off actual AWS commands

    This is a fail safe. All AWS calls should be stubbed already.
    """
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
