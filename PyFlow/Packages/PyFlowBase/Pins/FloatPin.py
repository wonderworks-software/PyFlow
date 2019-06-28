from PyFlow.Core import PinBase


class FloatPin(PinBase):
    """doc string for FloatPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(FloatPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(0.0)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def pinDataTypeHint():
        '''data type index and default value'''
        return 'FloatPin', 0.0

    @staticmethod
    def color():
        return (96, 169, 23, 255)

    @staticmethod
    def supportedDataTypes():
        return ('FloatPin', 'IntPin',)

    @staticmethod
    def internalDataStructure():
        return float

    @staticmethod
    def processData(data):
        return FloatPin.internalDataStructure()(data)
