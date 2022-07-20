import binascii
import pytest
from datacollector_api_client.client import DataCollectorWrapper

requests_test_data = [
    (200, "Accepted"),
    (400, "Not Accepted"),
]

signature_data = [
    ('bcc5fbbb', '2KXEZcVf5', 'Invalid base64-encoded string'),
    ('invalid id', 'invalid key', 'Incorrect padding')
]


def test_exception_raised_with_no_log():
    wrapper = DataCollectorWrapper('bcc5fbbb', '2KXEZcVf')
    with pytest.raises(ValueError) as exc:
        wrapper.log_info(structured_log_message=[])

    exception_message = exc.value.args[0]
    assert 'structured_log_message argument is empty' in exception_message


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


@pytest.mark.parametrize("expected_status_code, expected_response", requests_test_data)
def test_log_with_dbx_info(dbutils, requests_mock, expected_status_code, expected_response):
    wrapper = DataCollectorWrapper('bcc5fbbb', '2KXEZcVf', dbutils)

    requests_mock.post(wrapper.get_uri(), status_code=expected_status_code)

    data = [{
        "application": "thin",
        "message": "test_datacollector_api_client.py."
    }]

    resp = wrapper.log_info(structured_log_message=data)

    assert expected_response in resp


def test_log_without_dbx_info(requests_mock):
    wrapper = DataCollectorWrapper('bcc5fbbb', '2KXEZcVf')

    requests_mock.post(wrapper.get_uri(), status_code=200)

    data = [{
        "application": "thin",
        "message": "test_datacollector_api_client.py."
    }]

    resp = wrapper.log_info(structured_log_message=data)

    assert 'Accepted' in resp
