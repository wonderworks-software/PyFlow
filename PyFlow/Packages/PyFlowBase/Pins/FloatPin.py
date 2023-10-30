## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


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
        """data type index and default value"""
        return "FloatPin", 0.0

    @staticmethod
    def color():
        return (96, 169, 23, 255)

    @staticmethod
    def supportedDataTypes():
        return ("FloatPin", "IntPin")

    @staticmethod
    def internalDataStructure():
        return float

    @staticmethod
    def processData(data):
        return FloatPin.internalDataStructure()(data)
