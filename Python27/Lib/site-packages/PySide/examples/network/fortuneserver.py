#!/usr/bin/env python

"""PySide port of the network/fortuneserver example from Qt v4.x"""

import random

from PySide import QtCore, QtGui, QtNetwork


class Server(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtGui.QLabel()
        quitButton = QtGui.QPushButton("Quit")
        quitButton.setAutoDefault(False)

        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen():
            QtGui.QMessageBox.critical(self, "Fortune Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        statusLabel.setText("The server is running on port %d.\nRun the "
                "Fortune Client example now." % self.tcpServer.serverPort())

        self.fortunes = (
                "You've been leading a dog's life. Stay off the furniture.",
                "You've got to think about tomorrow.",
                "You will be surprised by a loud noise.",
                "You will feel hungry again in another hour.",
                "You might have mail.",
                "You cannot kill time without injuring eternity.",
                "Computers are not intelligent. They only think they are.")

        quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.sendFortune)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Server")

    def sendFortune(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        out.setVersion(QtCore.QDataStream.Qt_4_0)
        out.writeUInt16(0)
        fortune = self.fortunes[random.randint(0, len(self.fortunes) - 1)]

        try:
            # Python v3.
            fortune = bytes(fortune, encoding='ascii')
        except:
            # Python v2.
            pass

        out.writeString(fortune)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)

        clientConnection.write(block)
        clientConnection.disconnectFromHost()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    server = Server()
    random.seed(None)
    sys.exit(server.exec_())
