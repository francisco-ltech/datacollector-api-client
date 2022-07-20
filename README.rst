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

    from datacollector_api_client.client import DataCollectorWrapper

    wrapper = DataCollectorWrapper(LOGANALYTICS_WORKSPACE_ID, LOGANALYTICS_WORKSPACE_KEY)

    data = [{
       "application": "my_app",
       "message": "my log message"
    }]

    response = wrapper.log_info(structured_log_message=data)
    print(response)

Enriching structured logging with Databricks information
--------------------------------------------------------
Pass your dbutils instance from your Databricks session to the library

::

    wrapper = DataCollectorWrapper(LOGANALYTICS_WORKSPACE_ID, LOGANALYTICS_WORKSPACE_KEY, dbutils)

    data = [{
       "application": "Notebook",
       "message": f'Number of rows in dataframe: {df.count()}'
    }]

    response = wrapper.log_info(structured_log_message=data)
    print(response)


The following data is also collected and appended to your log:
 - dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
 - dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('clusterId')
 - dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('sessionId')
 - dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('user')