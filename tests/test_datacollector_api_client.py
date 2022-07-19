import binascii
import json
import pytest
from datacollector_api_client.client import DataCollectorWrapper

requests_test_data = [
    (200, "Accepted"),
    (400, "Not Accepted"),
]


@pytest.mark.parametrize("expected_status_code, expected_response", requests_test_data)
def test_log_info(dbutils, requests_mock, expected_status_code, expected_response):
    wrapper = DataCollectorWrapper('bcc5fbbb', '2KXEZcVf', dbutils)

    requests_mock.post(wrapper.get_uri(), status_code=expected_status_code)

    data = [{
        "application": "thin",
        "message": "test_datacollector_api_client.py."
    }]

    resp = wrapper.log_info(structured_log_message=data)

    assert expected_response in resp


signature_data = [
    ('bcc5fbbb', '2KXEZcVf5', 'Invalid base64-encoded string'),
    ('invalid id', 'invalid key', 'Incorrect padding')
]


@pytest.mark.parametrize("workspace_id, workspace_key, expected_error", signature_data)
def test_signature_exception_error(dbutils, requests_mock, workspace_id, workspace_key, expected_error):
    """
    This test case covers scenarios when a request signature cannot be constructed due to bad parameters.
    """

    wrapper = DataCollectorWrapper(workspace_id, workspace_key, dbutils)

    requests_mock.post(wrapper.get_uri(), status_code=200)

    with pytest.raises(binascii.Error) as exc:
        wrapper.log_info(structured_log_message=[{"job": "ingestion"}])

    exception_message = exc.value.args[0]
    assert expected_error in exception_message
