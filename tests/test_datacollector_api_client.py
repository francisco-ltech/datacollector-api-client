import binascii
import json
import pytest
from datacollector_api_client.client import DataCollectorWrapper

requests_test_data = [
    (200, "Accepted"),
    (400, "Not Accepted"),
]


@pytest.mark.parametrize("expected_status_code, expected_response", requests_test_data)
def test_post_data(requests_mock, expected_status_code, expected_response):
    wrapper = DataCollectorWrapper('bcc5fbbb', '2KXEZcVf')

    requests_mock.post(wrapper.get_uri(), status_code=expected_status_code)

    data = {
        "application": "thin",
        "message": "test_datacollector_api_client.py."
    }

    data_json = json.dumps(data)

    resp = wrapper.post_data('custom_log_table', data_json)

    assert expected_response in resp


signature_data = [
    ('bcc5fbbb', '2KXEZcVf5', 'Invalid base64-encoded string'),
    ('invalid id', 'invalid key', 'Incorrect padding')
]


@pytest.mark.parametrize("workspace_id, workspace_key, expected_error", signature_data)
def test_post_data_signature_exception_error(requests_mock, workspace_id, workspace_key, expected_error):
    """
    This test case covers scenarios when a request signature cannot be constructed due to bad parameters.
    """

    wrapper = DataCollectorWrapper(workspace_id, workspace_key)

    requests_mock.post(wrapper.get_uri(), status_code=200)

    with pytest.raises(binascii.Error) as exc:
        wrapper.post_data('INFO', '{"job": "ingestion"}')

    exception_message = exc.value.args[0]
    assert expected_error in exception_message
