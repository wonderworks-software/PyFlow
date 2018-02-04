import os
_PINS = {}


def _REGISTER_PIN_TYPE(pinSubclass):
    dType = pinSubclass.pinDataType()[0]
    if dType not in _PINS:
        _PINS[pinSubclass.pinDataType()[0]] = pinSubclass
    else:
        raise Exception("Error registering pin type {0}\n pin with ID [{1}] already registered".format(pinSubclass.__name__))


# append from Pins
for n in os.listdir(os.path.dirname(__file__)):
    if n.endswith(".py") and "__init__" not in n:
        pinName = n.split(".")[0]
        try:
            exec("from {0} import {0}".format(pinName))
            exec("pin_class = {0}".format(pinName))
            _REGISTER_PIN_TYPE(pin_class)
        except Exception as e:
            print(e, pinName)
            pass


def findPinClassByType(dataType):
        return _PINS[dataType] if dataType in _PINS else None


def CreatePin(name, parent, dataType, direction):
    pinClass = findPinClassByType(dataType)
    if pinClass is None:
        return None
    inst = pinClass(name, parent, dataType, direction)
    return inst
