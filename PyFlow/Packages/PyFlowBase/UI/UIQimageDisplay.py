from Qt import QtCore
from Qt import QtGui
import Qt
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase,InputTextField
from PyFlow.UI.Widgets.TextEditDialog import TextEditDialog
from PyFlow.UI.Widgets.QtSliders import pyf_ColorSlider
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from Qt.QtWidgets import QGraphicsTextItem, QGraphicsWidget, QGraphicsItem,QGraphicsProxyWidget,QLabel,QSizePolicy,QPushButton


class UIQimageDisplay(UINodeBase):
    def __init__(self, raw_node):
        super(UIQimageDisplay, self).__init__(raw_node)
        self.resizable = True
        self.roundness = 1
        self.Imagelabel = QLabel("test3")
        self.pixmap = QtGui.QPixmap(RESOURCES_DIR+"/wizard-cat.png") 
        self.addWidget(self.Imagelabel)
        self.updateSize()

    def paint(self, painter, option, widget):
        self.updateSize()
        super(UIQimageDisplay, self).paint( painter, option, widget)

    def updateSize(self):
        scaledPixmap = self.pixmap.scaledToWidth(self.customLayout.geometry().width())
        self.Imagelabel.setPixmap(scaledPixmap)

