class PyTransactErrors(Exception):
    pass


class CommitFirstError(PyTransactErrors):
    def __init__(self):
        super().__init__("No state to return to. Commit first to rollback!")