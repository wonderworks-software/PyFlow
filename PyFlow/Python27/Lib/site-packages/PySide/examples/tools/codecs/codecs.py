#!/usr/bin/env python

"""PyQt4 port of the tools/codecs example from Qt v4.x"""

from PySide import QtCore, QtGui


def codec_name(codec):
    try:
        # Python v3.
        name = str(codec.name(), encoding='ascii')
    except TypeError:
        # Python v2.
        name = str(codec.name())

    return name


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setCentralWidget(self.textEdit)

        self.codecs = []
        self.findCodecs()

        self.previewForm = PreviewForm(self)
        self.previewForm.setCodecList(self.codecs)

        self.saveAsActs = []
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Codecs")
        self.resize(500, 400)

    def open(self):
        fileName, _ = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            inFile = QtCore.QFile(fileName)
            if not inFile.open(QtCore.QFile.ReadOnly):
                QtGui.QMessageBox.warning(self, "Codecs",
                        "Cannot read file %s:\n%s" % (fileName, inFile.errorString()))
                return

            data = inFile.readAll()

            self.previewForm.setEncodedData(data)
            if self.previewForm.exec_():
                self.textEdit.setPlainText(self.previewForm.decodedString())

    def save(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self)
        if fileName:
            outFile = QtCore.QFile(fileName)
            if not outFile.open(QtCore.QFile.WriteOnly|QtCore.QFile.Text):
                QtGui.QMessageBox.warning(self, "Codecs",
                        "Cannot write file %s:\n%s" % (fileName, outFile.errorString()))
                return

            action = self.sender()
            codecName = action.data()

            out = QtCore.QTextStream(outFile)
            out.setCodec(codecName)
            out << self.textEdit.toPlainText()

    def about(self):
        QtGui.QMessageBox.about(self, "About Codecs",
                "The <b>Codecs</b> example demonstrates how to read and "
                "write files using various encodings.")

    def aboutToShowSaveAsMenu(self):
        currentText = self.textEdit.toPlainText()

        for action in self.saveAsActs:
            codecName = str(action.data())
            codec = QtCore.QTextCodec.codecForName(codecName)
            action.setVisible(codec and codec.canEncode(currentText))

    def findCodecs(self):
        codecMap = []
        iso8859RegExp = QtCore.QRegExp('ISO[- ]8859-([0-9]+).*')

        for mib in QtCore.QTextCodec.availableMibs():
            codec = QtCore.QTextCodec.codecForMib(mib)
            sortKey = codec_name(codec).upper()
            rank = 0

            if sortKey.startswith('UTF-8'):
                rank = 1
            elif sortKey.startswith('UTF-16'):
                rank = 2
            elif iso8859RegExp.exactMatch(sortKey):
                if len(iso8859RegExp.cap(1)) == 1:
                    rank = 3
                else:
                    rank = 4
            else:
                rank = 5

            codecMap.append((str(rank) + sortKey, codec))

        codecMap.sort()
        self.codecs = [item[-1] for item in codecMap]

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        for codec in self.codecs:
            name = codec_name(codec)

            action = QtGui.QAction(name + '...', self, triggered=self.save)
            action.setData(name)
            self.saveAsActs.append(action)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.saveAsMenu = QtGui.QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        self.saveAsMenu.aboutToShow.connect(self.aboutToShowSaveAsMenu)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addMenu(self.saveAsMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.helpMenu)


class PreviewForm(QtGui.QDialog):
    def __init__(self, parent):
        super(PreviewForm, self).__init__(parent)

        self.encodingComboBox = QtGui.QComboBox()
        encodingLabel = QtGui.QLabel("&Encoding:")
        encodingLabel.setBuddy(self.encodingComboBox)

        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        self.encodingComboBox.activated.connect(self.updateTextEdit)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(encodingLabel, 0, 0)
        mainLayout.addWidget(self.encodingComboBox, 0, 1)
        mainLayout.addWidget(self.textEdit, 1, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Choose Encoding")
        self.resize(400, 300)

    def setCodecList(self, codecs):
        self.encodingComboBox.clear()
        for codec in codecs:
            self.encodingComboBox.addItem(codec_name(codec), codec.mibEnum())

    def setEncodedData(self, data):
        self.encodedData = data
        self.updateTextEdit()

    def decodedString(self):
        return self.decodedStr

    def updateTextEdit(self):
        mib = self.encodingComboBox.itemData(self.encodingComboBox.currentIndex())
        codec = QtCore.QTextCodec.codecForMib(mib)

        data = QtCore.QTextStream(self.encodedData)
        data.setAutoDetectUnicode(False)
        data.setCodec(codec)

        self.decodedStr = data.readAll()
        self.textEdit.setPlainText(self.decodedStr)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
