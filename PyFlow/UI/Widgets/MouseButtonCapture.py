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


from Qt.QtWidgets import *
from Qt import QtCore, QtGui


class MouseButtonCaptureWidget(QPushButton):
    """docstring for MouseButtonCaptureWidget."""
    captured = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(MouseButtonCaptureWidget, self).__init__(parent)
        self._currentButton = QtCore.Qt.NoButton
        # noButton has not a name
        #self.setText(self._currentButton.name.decode('utf-8'))
        self.bCapturing = False
        self.setCheckable(True)
        self.setToolTip("<b>Esc</b> will set button to <u>NoButton</u> clear.<br><b>Left mouse button</b> will initiate capturing")

    @property
    def currentButton(self):
        return self._currentButton

    @currentButton.setter
    def currentButton(self, btn):
        self._currentButton = btn
        self.setText(self._currentButton.name.decode('utf-8'))
        self.setChecked(False)
        self.bCapturing = False
        self.captured.emit(self._currentButton)

    def keyPressEvent(self, event):
        super(MouseButtonCaptureWidget, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Escape:
            self.currentButton = QtCore.Qt.NoButton

    def mousePressEvent(self, event):
        button = event.button()
        if self.bCapturing:
            # capture mouse button
            self.currentButton = button
        else:
            if button == QtCore.Qt.MouseButton.LeftButton and not self.bCapturing:
                self.bCapturing = True
                self.setText("capturing...")
                super(MouseButtonCaptureWidget, self).mousePressEvent(event)


if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)

    w = MouseButtonCaptureWidget()
    w.show()

    sys.exit(a.exec_())
