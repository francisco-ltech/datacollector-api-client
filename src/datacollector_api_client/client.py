import hmac
import base64
import hashlib
import requests
import datetime


class DataCollectorWrapper:
    """ A class to wrap the DataCollector API endpoints.

    ...

    Attributes
    ----------
    workspace_id : str
        The customer id.
    workspace_key : str
        The shared key.

    Methods
    -------
    post_data(log_type: str, body: str):
        Makes a POST Http Request to Azure DataCollector API.
    """

    def __init__(self, workspace_id: str, workspace_key: str):
        """ Constructs all attributes for this instance
        :param workspace_id: The log analytics workspace id
        :param workspace_key: The log analytics workspace key
        """

        self.workspace_id = workspace_id
        self.workspace_key = workspace_key

    def get_uri(self):
        return f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"

    def post_data(self, log_type: str, body: str) -> str:
        """ Makes a POST Http Request to Azure DataCollector API
        :param log_type: The custom log table name in Log Analytics
        :param body: The structured log message
        :return: Accepted on success, Not Accepted upon failure
        """

        method = 'POST'
        content_type = 'application/json'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        signature = self.__build_signature(rfc1123date, method, content_length, content_type, '/api/logs')

        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': log_type,
            'x-ms-date': rfc1123date
        }

        response = requests.post(self.get_uri(), data=body, headers=headers)

        if 200 <= response.status_code <= 299:
            return 'Accepted'
        else:
            return f'Not Accepted: {response.content.decode()}'

    def __build_signature(self, date: str, method: str, content_length: int, content_type: str, resource: str) -> str:
        """ Builds the signature required to make a Http Request to the DataCollectorAPI
        :param date: The date of the log message
        :param method: POST or GET
        :param content_length: The size of the payload
        :param content_type: The content-type value of the payload, e.g.: application/json
        :param resource: The sink for logs
        :return: The authorised signature
        """

        x_headers = f'x-ms-date:{date}'
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, 'UTF-8')
        decoded_key = base64.b64decode(self.workspace_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256)
                                        .digest()).decode('utf-8')
        authorization = f'SharedKey {self.workspace_id}:{encoded_hash}'
        return authorization
