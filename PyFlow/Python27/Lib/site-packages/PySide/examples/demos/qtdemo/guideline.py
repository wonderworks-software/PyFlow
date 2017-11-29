from PySide import QtCore

from guide import Guide


class GuideLine(Guide):
    def __init__(self, line_or_point, follows=None):
        super(GuideLine, self).__init__(follows)

        if isinstance(line_or_point, QtCore.QLineF):
            self.line = line_or_point
        elif follows is not None:
            self.line = QtCore.QLineF(self.prevGuide.endPos(), line_or_point)
        else:
            self.line = QtCore.QLineF(QtCore.QPointF(0, 0), line_or_point)

    def length(self):
        return self.line.length()

    def startPos(self):
        return QtCore.QPointF(self.line.p1().x() * self.scaleX,
                self.line.p1().y() * self.scaleY)

    def endPos(self):
        return QtCore.QPointF(self.line.p2().x() * self.scaleX,
                self.line.p2().y() * self.scaleY)

    def guide(self, item, moveSpeed):
        frame = item.guideFrame - self.startLength
        endX = (self.line.p1().x() + (frame * self.line.dx() / self.length())) * self.scaleX
        endY = (self.line.p1().y() + (frame * self.line.dy() / self.length())) * self.scaleY
        pos = QtCore.QPointF(endX, endY)
        self.move(item, pos, moveSpeed)
