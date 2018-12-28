from PyFlow import _PINS


def findPinClassByType(dataType):
        return _PINS[dataType] if dataType in _PINS else None


def getPinDefaultValueByType(dataType):
    pin = findPinClassByType(dataType)
    if pin:
        return pin.pinDataTypeHint()[1]
    return None


def CreateRawPin(name, owningNode, dataType, direction, **kwds):
    pinClass = findPinClassByType(dataType)
    if pinClass is None:
        return None
    inst = pinClass(name, owningNode, dataType, direction, **kwds)
    return inst
