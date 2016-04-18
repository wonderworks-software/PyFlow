#!/usr/bin/env python

"""PyQt4 port of the network/http example from Qt v4.x"""

from PySide import QtCore, QtGui, QtNetwork, QtUiTools


class HttpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(HttpWindow, self).__init__(parent)

        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

        self.urlLineEdit = QtGui.QLineEdit('https://')

        urlLabel = QtGui.QLabel("&URL:")
        urlLabel.setBuddy(self.urlLineEdit)
        self.statusLabel = QtGui.QLabel("Please enter the URL of a file you "
                "want to download.")

        self.downloadButton = QtGui.QPushButton("Download")
        self.downloadButton.setDefault(True)
        self.quitButton = QtGui.QPushButton("Quit")
        self.quitButton.setAutoDefault(False)

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.http = QtNetwork.QHttp(self)

        self.urlLineEdit.textChanged.connect(self.enableDownloadButton)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.http.authenticationRequired.connect(self.slotAuthenticationRequired)
        self.http.sslErrors.connect(self.sslErrors)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.quitButton.clicked.connect(self.close)

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(urlLabel)
        topLayout.addWidget(self.urlLineEdit)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("HTTP")
        self.urlLineEdit.setFocus()

    def downloadFile(self):
        url = QtCore.QUrl(self.urlLineEdit.text())
        fileInfo = QtCore.QFileInfo(url.path())
        fileName = fileInfo.fileName()

        if not fileName:
            fileName = 'index.html'

        if QtCore.QFile.exists(fileName):
            ret = QtGui.QMessageBox.question(self, "HTTP",
                    "There already exists a file called %s in the current "
                    "directory." % fileName,
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Cancel)

            if ret == QtGui.QMessageBox.Cancel:
                return

            QtCore.QFile.remove(fileName)

        self.outFile = QtCore.QFile(fileName)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "HTTP",
                    "Unable to save the file %s: %s." % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        if url.scheme().lower() == 'https':
            mode = QtNetwork.QHttp.ConnectionModeHttps
        else:
            mode = QtNetwork.QHttp.ConnectionModeHttp

        port = url.port()

        if port == -1:
            port = 0

        self.http.setHost(url.host(), mode, port)

        if url.userName():
            self.http.setUser(url.userName(), url.password())

        self.httpRequestAborted = False

        path = QtCore.QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            try:
                # Python v3.
                path = str(path, encoding='utf-8')
            except TypeError:
                # Python v2.
                path = str(path)
        else:
            path = '/'

        self.httpGetId = self.http.get(path, self.outFile)

        self.progressDialog.setWindowTitle("HTTP")
        self.progressDialog.setLabelText("Downloading %s." % fileName)
        self.downloadButton.setEnabled(False)

    def cancelDownload(self):
        self.statusLabel.setText("Download canceled.")
        self.httpRequestAborted = True
        self.http.abort()
        self.downloadButton.setEnabled(True)

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None

            self.progressDialog.hide()
            return

        self.progressDialog.hide()
        self.outFile.close()

        if error:
            self.outFile.remove()
            QtGui.QMessageBox.information(self, "HTTP",
                    "Download failed: %s." % self.http.errorString())
        else:
            fileName = QtCore.QFileInfo(QtCore.QUrl(self.urlLineEdit.text()).path()).fileName()
            self.statusLabel.setText("Downloaded %s to current directory." % fileName)

        self.downloadButton.setEnabled(True)
        self.outFile = None

    def readResponseHeader(self, responseHeader):
        # Check for genuine error conditions.
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QtGui.QMessageBox.information(self, "HTTP",
                    "Download failed: %s." % responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.progressDialog.hide()
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return

        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)

    def enableDownloadButton(self):
        self.downloadButton.setEnabled(bool(self.urlLineEdit.text()))

    def slotAuthenticationRequired(self, hostName, _, authenticator):

        ui = os.path.join(os.path.dirname(__file__), 'authenticationdialog.ui')

        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(ui)
        dlg = loader.load(QFile(uifile, self))

        dlg.adjustSize()
        # ugly way to get the children. Somehow findChild wasn't working in this case
        siteDescripition = [x for x in dlg.children() if x.objectName() == 'siteDescription'][0]
        siteDescription.setText("%s at %s" % (authenticator.realm(), hostName))

        if dlg.exec_() == QtGui.QDialog.Accepted:
            authenticator.setUser(dlg.userEdit.text())
            authenticator.setPassword(dlg.passwordEdit.text())

    def sslErrors(self, errors):
        errorString = ", ".join([str(error.errorString()) for error in errors])

        ret = QtGui.QMessageBox.warning(self, "HTTP Example",
                "One or more SSL errors has occurred: %s" % errorString,
                QtGui.QMessageBox.Ignore | QtGui.QMessageBox.Abort)

        if ret == QtGui.QMessageBox.Ignore:
            self.http.ignoreSslErrors()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    httpWin = HttpWindow()
    httpWin.show()
    sys.exit(httpWin.exec_())
