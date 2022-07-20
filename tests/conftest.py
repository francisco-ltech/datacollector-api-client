import pytest
from datacollector_api_client.dbutils_proxy import DbUtilsProxy


@pytest.fixture
def dbutils(monkeypatch):

    def mock_get_notebook(dbutils):
        return 'my_notebook'

    def mock_get_cluster_id(dbutils):
        return 123

    def mock_get_session_id(dbutils):
        return 456

    def mock_get_current_user(dbutils):
        return 'me'

    monkeypatch.setattr(DbUtilsProxy, 'get_notebook', mock_get_notebook)
    monkeypatch.setattr(DbUtilsProxy, 'get_cluster_id', mock_get_cluster_id)
    monkeypatch.setattr(DbUtilsProxy, 'get_session_id', mock_get_session_id)
    monkeypatch.setattr(DbUtilsProxy, 'get_current_user', mock_get_current_user)

    return DbUtilsProxy
