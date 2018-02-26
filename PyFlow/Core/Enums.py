from enum import IntEnum

_enumClasses = {}


def appendEnumInstance(inst):
    if inst.__name__ not in _enumClasses:
        _enumClasses[inst.__name__] = inst


def findByName(name):
    if name in _enumClasses:
        return _enumClasses[name]


class ENone(IntEnum):
    none = 0

appendEnumInstance(ENone)
