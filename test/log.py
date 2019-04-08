from collections import Mapping


class CobraLog(Mapping):
    def __new__(cls, event, args):
        obj = super().__new__(cls)
        obj._event = event
        obj._args = args
        return obj

    def __eq__(self, other):
        if not isinstance(other, CobraLog):
            return False
        if self._event != other._event:
            return False
        return self._args == other._args

    def __iter__(self):
        return iter(self._args)

    def __len__(self):
        return len(self._args)

    def __getitem__(self, key):
        return self._args[key]