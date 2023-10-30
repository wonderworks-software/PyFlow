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


from Qt import QtGui
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from Qt.QtWidgets import QLabel


class UIImageDisplayNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIImageDisplayNode, self).__init__(raw_node)
        self.resizable = True
        self.Imagelabel = QLabel("test3")
        self.pixmap = QtGui.QPixmap(RESOURCES_DIR + "/wizard-cat.png")
        self.addWidget(self.Imagelabel)
        self.updateSize()
        self._rawNode.loadImage.connect(self.onLoadImage)

    def onLoadImage(self, imagePath):
        self.pixmap = QtGui.QPixmap(imagePath)
        self.updateSize()

    def paint(self, painter, option, widget):
        self.updateSize()
        super(UIImageDisplayNode, self).paint(painter, option, widget)

    def updateSize(self):
        scaledPixmap = self.pixmap.scaledToWidth(self.customLayout.geometry().width())
        self.Imagelabel.setPixmap(scaledPixmap)
