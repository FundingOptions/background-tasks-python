import pytest


def test_lambda_transport_send(lambda_transport, fake_event, lambda_stub, caplog):
    expected_response = {
        "StatusCode": 200,
        "Payload": b"",
    }
    lambda_stub.add_response("invoke", expected_response)

    lambda_transport.send(fake_event)

    assert f"LambdaTransport start sending event: {fake_event}" in caplog.text
    assert f"Result of sending by LambdaTransport: {expected_response}" in caplog.text


def test_lambda_transport_send_exception(
    lambda_transport, fake_event, lambda_stub, caplog
):
    lambda_stub.add_client_error(
        "invoke",
        http_status_code=429,
        service_message="Too Many Requests",
    )
    lambda_transport.send(fake_event)
    assert (
        "LambdaTransport:An error occurred () when calling the Invoke operation: Too Many Requests"
        in caplog.text
    )


def test_lambda_transport_handler(lambda_transport, fake_event, dispatch_receive_mock):
    lambda_transport.lambda_handler(fake_event, context="test")
    dispatch_receive_mock.assert_called_once_with(fake_event)
