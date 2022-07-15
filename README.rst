DataCollector API Client Library
================================
A thin client to send log data to Azure Monitor by using the `HTTP Data Collector API <https://docs.microsoft.com/en-us/azure/azure-monitor/logs/data-collector-api>`_.

.. image:: https://github.com/francisco-ltech/datacollector-api-client/actions/workflows/tests.yml/badge.svg
  :alt: Linux and Windows build status
  
Installation
------------
::

   $ pip install datacollector-api-client

Usage
-----


::

    import json
    from datacollector_api_client import client

    data = {
        "application": "your_application_name",
        "message": "A log message."
    }

    data_json = json.dumps(data)

    wrapper = client.DataCollectorWrapper("your_log_analytics_workspace_id", "your_log_analytics_workspace_key")

    response = wrapper.post_data("custom_log_table_name", data_json)
