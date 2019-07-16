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


from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo


class UISequenceNode(UINodeBase):
    def __init__(self, raw_node):
        super(UISequenceNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add out pin")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.setToolTip("Adds output execution pin")
        actionAddOut.triggered.connect(self.onAddOutPin)

    def onPinWasKilled(self, uiPin):
        index = 1
        uiPin.OnPinDeleted.disconnect(self.onPinWasKilled)
        pins = list(self.UIoutputs.values())
        pins.sort(key=lambda x: int(x._rawPin.name))
        for outPin in pins:
            outPin.setName(str(index), True)
            outPin.setDisplayName("Then {0}".format(index))
            index += 1

    def postCreate(self, jsonTemplate=None):
        super(UISequenceNode, self).postCreate(jsonTemplate)
        for outPin in self.UIoutputs.values():
            outPin.setDisplayName("Then {0}".format(outPin._rawPin.name))
            outPin.OnPinDeleted.connect(self.onPinWasKilled)

    def onAddOutPin(self):
        rawPin = self._rawNode.createOutputPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.OnPinDeleted.connect(self.onPinWasKilled)
        uiPin.setDisplayName("Then {0}".format(rawPin.name))
        return uiPin
