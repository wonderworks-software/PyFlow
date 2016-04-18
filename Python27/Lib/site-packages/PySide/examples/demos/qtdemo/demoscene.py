from PySide import QtGui


class DemoScene(QtGui.QGraphicsScene):
    def drawItems(self, painter, items, options, widget):
        for item, option in zip(items, options):
            painter.save()
            painter.setMatrix(item.sceneMatrix(), True)
            item.paint(painter, option, widget)
            painter.restore()
