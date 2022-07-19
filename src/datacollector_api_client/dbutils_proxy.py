class DbUtilsProxy:

    @staticmethod
    def get_notebook(dbutils):
        return dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()

    @staticmethod
    def get_cluster_id(dbutils):
        return dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('clusterId')

    @staticmethod
    def get_session_id(dbutils):
        return dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('sessionId')

    @staticmethod
    def get_current_user(dbutils):
        return dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('user')
