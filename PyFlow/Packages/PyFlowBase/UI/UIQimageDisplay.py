from Qt import QtGui
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from Qt.QtWidgets import QLabel
#import FreeCAD


class UIQimageDisplay(UINodeBase):
    def __init__(self, raw_node):
        super(UIQimageDisplay, self).__init__(raw_node)
        self.resizable = True
        self.Imagelabel = QLabel("test3")
        self.pixmap = QtGui.QPixmap(RESOURCES_DIR + "/wizard-cat.png")
        self.addWidget(self.Imagelabel)
        self.updateSize()
        self._rawNode.loadImage.connect(self.onLoadImage)

    def onLoadImage(self, imagePath):
        self.pixmap = QtGui.QPixmap(imagePath)
        self.w=QLabel("testzz")
        scaledPixmap = self.pixmap.scaledToWidth(400)
        self.w.setPixmap(scaledPixmap)
#        FreeCAD.w=self.w
        self.w.show()
        self.updateSize()

    def paint(self, painter, option, widget):
        self.updateSize()
        super(UIQimageDisplay, self).paint(painter, option, widget)

    def updateSize(self):
        scaledPixmap = self.pixmap.scaledToWidth(
            self.customLayout.geometry().width())
        self.Imagelabel.setPixmap(scaledPixmap)
