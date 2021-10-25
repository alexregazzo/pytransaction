import logging

import pytransaction.errors

logger = logging.getLogger("pytransaction")


class Transaction:
    def __init__(self, commit: bool = True):
        self.__states__ = []
        if commit:
            self.commit()

    def commit(self):
        self.__states__ = []

    def begin(self):
        new_state = {k: v for k, v in self.__dict__.items() if k != "__states__"}
        self.__states__.append(new_state)

    def rollback(self, ignore_no_commit: bool = True):
        if len(self.__states__) == 0:
            if ignore_no_commit is True:
                return
            raise pytransaction.errors.CommitFirstError
        all_states = self.__states__
        self.__dict__ = {
            **{k: v for k, v in all_states.pop().items()},
            "__states__": all_states
        }

    def __enter__(self):
        self.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
