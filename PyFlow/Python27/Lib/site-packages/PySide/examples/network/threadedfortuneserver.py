#!/usr/bin/env python

############################################################################
# 
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
# 
#  This file is part of the example classes of the Qt Toolkit.
# 
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
# 
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
# 
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
############################################################################

import random

from PySide import QtCore, QtGui, QtNetwork


class FortuneThread(QtCore.QThread):
    error = QtCore.Signal(QtNetwork.QTcpSocket.SocketError)

    def __init__(self, socketDescriptor, fortune, parent):
        super(FortuneThread, self).__init__(parent)

        self.socketDescriptor = socketDescriptor
        self.text = fortune

    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.error.emit(tcpSocket.error())
            return

        block = QtCore.QByteArray()
        outstr = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstr.setVersion(QtCore.QDataStream.Qt_4_0)
        outstr.writeUInt16(0)
        outstr.writeString(self.text)
        outstr.device().seek(0)
        outstr.writeUInt16(block.count() - 2)

        tcpSocket.write(block)
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()


class FortuneServer(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(FortuneServer, self).__init__(parent)

        self.fortunes = (
                "You've been leading a dog's life. Stay off the furniture.",
                "You've got to think about tomorrow.",
                "You will be surprised by a loud noise.",
                "You will feel hungry again in another hour.",
                "You might have mail.",
                "You cannot kill time without injuring eternity.",
                "Computers are not intelligent. They only think they are.")

    def incomingConnection(self, socketDescriptor):
        fortune = self.fortunes[random.randint(0, len(self.fortunes) - 1)]

        try:
            # Python v3.
            fortune = bytes(fortune, encoding='ascii')
        except:
            # Python v2.
            pass

        thread = FortuneThread(socketDescriptor, fortune, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.server = FortuneServer()

        statusLabel = QtGui.QLabel()
        quitButton = QtGui.QPushButton("Quit")
        quitButton.setAutoDefault(False)

        if not self.server.listen():
            QtGui.QMessageBox.critical(self, "Threaded Fortune Server",
                    "Unable to start the server: %s." % self.server.errorString())
            self.close()
            return

        statusLabel.setText("The server is running on port %d.\nRun the "
                "Fortune Client example now." % self.server.serverPort())

        quitButton.clicked.connect(self.close)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Threaded Fortune Server")


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(dialog.exec_())
