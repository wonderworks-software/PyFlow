#!/usr/bin/env python

"""PySide port of the network/http example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui, QtNetwork


class HttpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.urlLineEdit = QtGui.QLineEdit("http://www.ietf.org/iesg/1rfc_index.txt")

        self.urlLabel = QtGui.QLabel(self.tr("&URL:"))
        self.urlLabel.setBuddy(self.urlLineEdit)
        self.statusLabel = QtGui.QLabel(self.tr("Please enter the URL of a file "
                                                "you want to download."))

        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
        self.downloadButton = QtGui.QPushButton(self.tr("Download"))
        self.downloadButton.setDefault(True)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.http = QtNetwork.QHttp(self)
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

        self.connect(self.urlLineEdit, QtCore.SIGNAL("textChanged(QString &)"),
                     self.enableDownloadButton)
        self.connect(self.http, QtCore.SIGNAL("requestFinished(int, bool)"),
                     self.httpRequestFinished)
        self.connect(self.http, QtCore.SIGNAL("dataReadProgress(int, int)"),
                     self.updateDataReadProgress)
        self.connect(self.http, QtCore.SIGNAL("responseHeaderReceived(QHttpResponseHeader &)"),
                     self.readResponseHeader)
        self.connect(self.progressDialog, QtCore.SIGNAL("canceled()"),
                     self.cancelDownload)
        self.connect(self.downloadButton, QtCore.SIGNAL("clicked()"),
                     self.downloadFile)
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.urlLabel)
        topLayout.addWidget(self.urlLineEdit)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.downloadButton)
        buttonLayout.addWidget(self.quitButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("HTTP"))
        self.urlLineEdit.setFocus()

    def downloadFile(self):
        url = QtCore.QUrl(self.urlLineEdit.text())
        fileInfo = QtCore.QFileInfo(url.path())
        fileName = fileInfo.fileName()

        if QtCore.QFile.exists(fileName):
            QtGui.QMessageBox.information(self, self.tr("HTTP"), self.tr(
                                          "There already exists a file called %s "
                                          "in the current directory.") % (fileName))
            return

        self.outFile = QtCore.QFile(fileName)
        if  not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, self.tr("HTTP"),
                                          self.tr("Unable to save the file %(name)s: %(error)s.")
                                          % {'name': fileName,
                                             'error': self.outFile.errorString()})
            self.outFile = None
            return

        if url.port() != -1:
            self.http.setHost(url.host(), url.port())
        else:
            self.http.setHost(url.host(), 80)
        if url.userName():
            self.http.setUser(url.userName(), url.password())

        self.httpRequestAborted = False
        self.httpGetId = self.http.get(url.path(), self.outFile)

        self.progressDialog.setWindowTitle(self.tr("HTTP"))
        self.progressDialog.setLabelText(self.tr("Downloading %s.") % (fileName))
        self.downloadButton.setEnabled(False)

    def cancelDownload(self):
        self.statusLabel.setText(self.tr("Download canceled."))
        self.httpRequestAborted = True
        self.http.abort()
        self.downloadButton.setEnabled(True)

    def httpRequestFinished(self, requestId, error):
        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None

            self.progressDialog.hide()
            return

        if requestId != self.httpGetId:
            return

        self.progressDialog.hide()
        self.outFile.close()

        if error:
            self.outFile.remove()
            QtGui.QMessageBox.information(self, self.tr("HTTP"),
                                          self.tr("Download failed: %s.")
                                          % (self.http.errorString()))
        else:
            fileName = QtCore.QFileInfo(QtCore.QUrl(self.urlLineEdit.text()).path()).fileName()
            self.statusLabel.setText(self.tr("Downloaded %s to current directory.") % (fileName))

        self.downloadButton.setEnabled(True)
        self.outFile = None

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() != 200:
            QtGui.QMessageBox.information(self, self.tr("HTTP"),
                                          self.tr("Download failed: %s.")
                                          % (responseHeader.reasonPhrase()))
            self.httpRequestAborted = True
            self.progressDialog.hide()
            self.http.abort()
            return

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return

        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)

    def enableDownloadButton(self):
        self.downloadButton.setEnabled(not self.urlLineEdit.text())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    httpWin = HttpWindow()
    sys.exit(httpWin.exec_())
