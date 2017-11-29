#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PySide port of the network/ftp example from Qt v4.x"""

from PySide import QtCore, QtGui, QtNetwork

import ftp_rc


class FtpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FtpWindow, self).__init__(parent)

        self.isDirectory = {}
        self.currentPath = ''
        self.ftp = None
        self.outFile = None

        ftpServerLabel = QtGui.QLabel("Ftp &server:")
        self.ftpServerLineEdit = QtGui.QLineEdit('ftp.trolltech.com')
        ftpServerLabel.setBuddy(self.ftpServerLineEdit)

        self.statusLabel = QtGui.QLabel("Please enter the name of an FTP server.")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(False)

        self.connectButton = QtGui.QPushButton("Connect")
        self.connectButton.setDefault(True)

        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon(':/images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)

        self.downloadButton = QtGui.QPushButton("Download")
        self.downloadButton.setEnabled(False)

        self.quitButton = QtGui.QPushButton("Quit")

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.fileList.itemActivated.connect(self.processItem)
        self.fileList.currentItemChanged.connect(self.enableDownloadButton)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.connectButton.clicked.connect(self.connectOrDisconnect)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.quitButton.clicked.connect(self.close)

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(ftpServerLabel)
        topLayout.addWidget(self.ftpServerLineEdit)
        topLayout.addWidget(self.cdToParentButton)
        topLayout.addWidget(self.connectButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.fileList)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("FTP")

    def sizeHint(self):
        return QtCore.QSize(500, 300)

    def connectOrDisconnect(self):
        if self.ftp:
            self.ftp.abort()
            self.ftp.deleteLater()
            self.ftp = None

            self.fileList.setEnabled(False)
            self.cdToParentButton.setEnabled(False)
            self.downloadButton.setEnabled(False)
            self.connectButton.setEnabled(True)
            self.connectButton.setText("Connect")
            self.setCursor(QtCore.Qt.ArrowCursor)

            return

        self.setCursor(QtCore.Qt.WaitCursor)

        self.ftp = QtNetwork.QFtp(self)
        self.ftp.commandFinished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.addToList)
        self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath = ''
        self.isDirectory.clear()

        url = QtCore.QUrl(self.ftpServerLineEdit.text())
        if not url.isValid() or url.scheme().lower() != 'ftp':
            self.ftp.connectToHost(self.ftpServerLineEdit.text(), 21)
            self.ftp.login()
        else:
            self.ftp.connectToHost(url.host(), url.port(21))

            user_name = url.userName()
            if user_name:
                try:
                    # Python v3.
                    user_name = bytes(user_name, encoding='latin1')
                except:
                    # Python v2.
                    pass

                self.ftp.login(QtCore.QUrl.fromPercentEncoding(user_name), url.password())
            else:
                self.ftp.login()

            if url.path():
                self.ftp.cd(url.path())

        self.fileList.setEnabled(True)
        self.connectButton.setEnabled(False)
        self.connectButton.setText("Disconnect")
        self.statusLabel.setText("Connecting to FTP server %s..." % self.ftpServerLineEdit.text())

    def downloadFile(self):
        fileName = self.fileList.currentItem().text(0)

        if QtCore.QFile.exists(fileName):
            QtGui.QMessageBox.information(self, "FTP",
                    "There already exists a file called %s in the current "
                    "directory." % fileName)
            return

        self.outFile = QtCore.QFile(fileName)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "FTP",
                    "Unable to save the file %s: %s." % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        self.ftp.get(self.fileList.currentItem().text(0), self.outFile)

        self.progressDialog.setLabelText("Downloading %s..." % fileName)
        self.downloadButton.setEnabled(False)
        self.progressDialog.exec_()

    def cancelDownload(self):
        self.ftp.abort()

    def ftpCommandFinished(self, _, error):
        self.setCursor(QtCore.Qt.ArrowCursor)

        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(self, "FTP",
                        "Unable to connect to the FTP server at %s. Please "
                        "check that the host name is correct." % self.ftpServerLineEdit.text())
                self.connectOrDisconnect()
                return

            self.statusLabel.setText("Logged onto %s." % self.ftpServerLineEdit.text())
            self.fileList.setFocus()
            self.downloadButton.setDefault(True)
            self.connectButton.setEnabled(True)
            return

        if self.ftp.currentCommand() == QtNetwork.QFtp.Login:
            self.ftp.list()

        if self.ftp.currentCommand() == QtNetwork.QFtp.Get:
            if error:
                self.statusLabel.setText("Canceled download of %s." % self.outFile.fileName())
                self.outFile.close()
                self.outFile.remove()
            else:
                self.statusLabel.setText("Downloaded %s to current directory." % self.outFile.fileName())
                self.outFile.close()

            self.outFile = None
            self.enableDownloadButton()
            self.progressDialog.hide()
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            if not self.isDirectory:
                self.fileList.addTopLevelItem(QtGui.QTreeWidgetItem(["<empty>"]))
                self.fileList.setEnabled(False)

    def addToList(self, urlInfo):
        item = QtGui.QTreeWidgetItem()
        item.setText(0, urlInfo.name())
        item.setText(1, str(urlInfo.size()))
        item.setText(2, urlInfo.owner())
        item.setText(3, urlInfo.group())
        item.setText(4, urlInfo.lastModified().toString('MMM dd yyyy'))

        if urlInfo.isDir():
            icon = QtGui.QIcon(':/images/dir.png')
        else:
            icon = QtGui.QIcon(':/images/file.png')
        item.setIcon(0, icon)

        self.isDirectory[urlInfo.name()] = urlInfo.isDir()
        self.fileList.addTopLevelItem(item)
        if not self.fileList.currentItem():
            self.fileList.setCurrentItem(self.fileList.topLevelItem(0))
            self.fileList.setEnabled(True)

    def processItem(self, item):
        name = item.text(0)
        if self.isDirectory.get(name):
            self.fileList.clear()
            self.isDirectory.clear()
            self.currentPath += '/' + name
            self.ftp.cd(name)
            self.ftp.list()
            self.cdToParentButton.setEnabled(True)
            self.setCursor(QtCore.Qt.WaitCursor)

    def cdToParent(self):
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()

        dirs = self.currentPath.split('/')
        if len(dirs) > 1:
            self.currentPath = ''
            self.cdToParentButton.setEnabled(False)
            self.ftp.cd('/')
        else:
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp.cd(self.currentPath)

        self.ftp.list()

    def updateDataTransferProgress(self, readBytes, totalBytes):
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(readBytes)

    def enableDownloadButton(self):
        current = self.fileList.currentItem()
        if current:
            currentFile = current.text(0)
            self.downloadButton.setEnabled(not self.isDirectory.get(currentFile))
        else:
            self.downloadButton.setEnabled(False)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    ftpWin = FtpWindow()
    ftpWin.show()
    sys.exit(ftpWin.exec_())
