from Qt import QtWidgets
from Qt import QtCore

from Widgets.pyf_HueSlider import pyf_HueSlider, pyf_GradientSlider

if __name__ == '__main__':
    import sys
    sys.path.append("..")
    import stylesheet
else:
    from PyFlow.UI.Utils.stylesheet import editableStyleSheet
    #import resources


class StyleSheetEditor(QtWidgets.QWidget):
    """Style Sheet Editor"""
    Updated = QtCore.Signal()

    def __init__(self, parent=None):
        super(StyleSheetEditor, self).__init__(parent)
        self.style = editableStyleSheet()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.mainGroup = QtWidgets.QGroupBox(self)
        self.mainGroupLay = QtWidgets.QVBoxLayout(self.mainGroup)
        mainLabel = QtWidgets.QLabel("Main Color Hue", parent=self.mainGroup)
        self.main_hue = pyf_HueSlider(self.mainGroup)
        self.main_hue.valueChanged.connect(self.updateHue)
        self.main_light = pyf_GradientSlider(self.mainGroup)
        self.main_light.valueChanged.connect(self.updateLight)
        self.mainGroupLay.addWidget(mainLabel)
        self.mainGroupLay.addWidget(self.main_hue)
        self.mainGroupLay.addWidget(self.main_light)
        self.bgColor = pyf_GradientSlider(self)
        self.bgColor.valueChanged.connect(self.updateBg)
        self.layout().addWidget(self.mainGroup)
        self.layout().addWidget(self.bgColor)

        self.setColor(self.style.MainColor)
        self.bgColor.setValue(0.196)
        self.main_light.setValue(self.MainColor.lightnessF())
        self.USETEXTUREBG = True

    def setColor(self, color):
        self.MainColor = color
        self.main_hue.setColor(color)

    def hue(self):
        return self.main_hue.value()

    def getStyleSheet(self):
        return self.style.getStyleSheet()

    def updateHue(self, value):
        self.style.setHue(self.main_hue.value())
        self.style.setLightness(self.main_light.value())
        self.Updated.emit()

    def updateLight(self, value):
        self.main_hue.setLightness(self.main_light.value())
        self.main_hue.update()
        self.style.setLightness(self.main_light.value())
        self.Updated.emit()

    def updateBg(self, value):
        self.style.setBg(self.bgColor.value())

        self.Updated.emit()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    a = StyleSheetEditor()

    def update():
        app.setStyleSheet(a.getStyleSheet())

    app.setStyleSheet(a.getStyleSheet())
    a.Updated.connect(update)
    a.show()

    sys.exit(app.exec_())
