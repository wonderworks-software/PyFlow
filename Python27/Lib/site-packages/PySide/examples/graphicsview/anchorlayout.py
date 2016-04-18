#!/usr/bin/env python


from PySide import QtCore, QtGui


def createItem(minimum, preferred, maximum, name):
    w = QtGui.QGraphicsProxyWidget()

    w.setWidget(QtGui.QPushButton(name))
    w.setMinimumSize(minimum)
    w.setPreferredSize(preferred)
    w.setMaximumSize(maximum)
    w.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)

    return w


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    scene = QtGui.QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 480)

    minSize = QtCore.QSizeF(30, 100)
    prefSize = QtCore.QSizeF(210, 100)
    maxSize = QtCore.QSizeF(300, 100)

    a = createItem(minSize, prefSize, maxSize, "A")
    b = createItem(minSize, prefSize, maxSize, "B")
    c = createItem(minSize, prefSize, maxSize, "C")
    d = createItem(minSize, prefSize, maxSize, "D")
    e = createItem(minSize, prefSize, maxSize, "E")
    f = createItem(QtCore.QSizeF(30, 50), QtCore.QSizeF(150, 50), maxSize, "F")
    g = createItem(QtCore.QSizeF(30, 50), QtCore.QSizeF(30, 100), maxSize, "G")

    l = QtGui.QGraphicsAnchorLayout()
    l.setSpacing(0)

    w = QtGui.QGraphicsWidget(None, QtCore.Qt.Window)
    w.setPos(20, 20)
    w.setLayout(l)

    # Vertical.
    l.addAnchor(a, QtCore.Qt.AnchorTop, l, QtCore.Qt.AnchorTop)
    l.addAnchor(b, QtCore.Qt.AnchorTop, l, QtCore.Qt.AnchorTop)

    l.addAnchor(c, QtCore.Qt.AnchorTop, a, QtCore.Qt.AnchorBottom)
    l.addAnchor(c, QtCore.Qt.AnchorTop, b, QtCore.Qt.AnchorBottom)
    l.addAnchor(c, QtCore.Qt.AnchorBottom, d, QtCore.Qt.AnchorTop)
    l.addAnchor(c, QtCore.Qt.AnchorBottom, e, QtCore.Qt.AnchorTop)

    l.addAnchor(d, QtCore.Qt.AnchorBottom, l, QtCore.Qt.AnchorBottom)
    l.addAnchor(e, QtCore.Qt.AnchorBottom, l, QtCore.Qt.AnchorBottom)

    l.addAnchor(c, QtCore.Qt.AnchorTop, f, QtCore.Qt.AnchorTop)
    l.addAnchor(c, QtCore.Qt.AnchorVerticalCenter, f, QtCore.Qt.AnchorBottom)
    l.addAnchor(f, QtCore.Qt.AnchorBottom, g, QtCore.Qt.AnchorTop)
    l.addAnchor(c, QtCore.Qt.AnchorBottom, g, QtCore.Qt.AnchorBottom)

    # Horizontal.
    l.addAnchor(l, QtCore.Qt.AnchorLeft, a, QtCore.Qt.AnchorLeft)
    l.addAnchor(l, QtCore.Qt.AnchorLeft, d, QtCore.Qt.AnchorLeft)
    l.addAnchor(a, QtCore.Qt.AnchorRight, b, QtCore.Qt.AnchorLeft)

    l.addAnchor(a, QtCore.Qt.AnchorRight, c, QtCore.Qt.AnchorLeft)
    l.addAnchor(c, QtCore.Qt.AnchorRight, e, QtCore.Qt.AnchorLeft)

    l.addAnchor(b, QtCore.Qt.AnchorRight, l, QtCore.Qt.AnchorRight)
    l.addAnchor(e, QtCore.Qt.AnchorRight, l, QtCore.Qt.AnchorRight)
    l.addAnchor(d, QtCore.Qt.AnchorRight, e, QtCore.Qt.AnchorLeft)

    l.addAnchor(l, QtCore.Qt.AnchorLeft, f, QtCore.Qt.AnchorLeft)
    l.addAnchor(l, QtCore.Qt.AnchorLeft, g, QtCore.Qt.AnchorLeft)
    l.addAnchor(f, QtCore.Qt.AnchorRight, g, QtCore.Qt.AnchorRight)

    scene.addItem(w)
    scene.setBackgroundBrush(QtCore.Qt.darkGreen)

    view = QtGui.QGraphicsView(scene)
    view.show()

    sys.exit(app.exec_())
