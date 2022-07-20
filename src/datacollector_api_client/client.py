import hmac
import base64
import hashlib
import json

import requests
import datetime

from typing import List

from datacollector_api_client.dbutils_proxy import DbUtilsProxy


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

    def __init__(self, workspace_id: str, workspace_key: str, dbutils=None) -> None:
        """ Constructs all attributes for this instance
        :param workspace_id: The id of the Log Analytics workspace.
        :param workspace_key: The key of the Log Analytics workspace.
        :param dbutils: The pyspark.dbutils.DBUtils instance from the consumer application,
        dbx additional info will be collected
        """

        self.workspace_id = workspace_id
        self.workspace_key = workspace_key
        self.dbutils = dbutils

    def get_uri(self):
        return f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"

    def log_info(self, structured_log_message: List[str], log_type: str = "logs_info") -> str:
        return self.__make_request(log_type, structured_log_message)

    def log_error(self, structured_log_message: List[str], log_type: str = "logs_info") -> str:
        return self.__make_request(log_type, structured_log_message)

    def __make_request(self, log_type: str, structured_log_message: List[str]) -> str:
        """ Makes a POST Http Request to Azure DataCollector API
        :param log_type: The custom log table name in Log Analytics
        :param structured_log_message: More collected info form the consumer application
        :return: Accepted on success, Not Accepted upon failure
        """

        if not structured_log_message:
            raise ValueError('structured_log_message argument is empty.')

        if self.dbutils is not None:
            json_log = json.loads(self.__get_dbx_data())
            for log in structured_log_message:
                json_log.update(json.loads(json.dumps(log)))
            data = json.dumps([json_log])
        else:
            data = json.dumps(structured_log_message)

        method = 'POST'
        content_type = 'application/json'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(data)
        signature = self.__build_signature(rfc1123date, method, content_length, content_type, '/api/logs')

        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': log_type,
            'x-ms-date': rfc1123date
        }

        response = requests.post(self.get_uri(), data=data, headers=headers)

        if 200 <= response.status_code <= 299:
            return 'Accepted'
        else:
            return f'Not Accepted: {response.content.decode()}'

    def __get_dbx_data(self) -> str:
        """
        Gets databricks notebook information from pyspark.dbutils.DBUtils instance given in the constructor of
        this class.
        :return: A json string
        """
        return json.dumps({
                "application": DbUtilsProxy.get_notebook(self.dbutils),
                "cluster_id": DbUtilsProxy.get_cluster_id(self.dbutils),
                "session_id": DbUtilsProxy.get_session_id(self.dbutils),
                "actor": DbUtilsProxy.get_current_user(self.dbutils)
            })

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
