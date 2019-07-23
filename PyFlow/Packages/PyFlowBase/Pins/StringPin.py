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
from PyFlow.Core.Common import *
from nine import str


class StringPin(PinBase):
    """doc string for StringPin"""
    def __init__(self, name, parent, direction, **kwargs):
        super(StringPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue("")

    @staticmethod
    def IsValuePin():
        return True

    def getInputWidgetVariant(self):
        if self.annotationDescriptionDict is not None:
            if "ValueList" in self.annotationDescriptionDict:
                return "EnumWidget"
        return DEFAULT_WIDGET_VARIANT

    @staticmethod
    def supportedDataTypes():
        return ('StringPin',)

    @staticmethod
    def color():
        return (255, 8, 127, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'StringPin', ''

    @staticmethod
    def internalDataStructure():
        return str

    @staticmethod
    def processData(data):
        return StringPin.internalDataStructure()(data)
