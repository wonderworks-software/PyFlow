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


from Qt import (
    QtGui,
    QtCore
)

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.Canvas.UIPinBase import UIPinBase
from PyFlow.UI.Canvas.Painters import PinPainter


class UIExecPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIExecPin, self).__init__(owningNode, raw_pin)

    def paint(self, painter, option, widget):
        # PinPainter.asValuePin(self, painter, option, widget)
        PinPainter.asExecPin(self, painter, option, widget)

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        hoverMessage = "Data: {0}\r\nDirty: {1}".format(str(self._rawPin.currentData()), self._rawPin.dirty)
        self.setToolTip(hoverMessage)
        event.accept()
