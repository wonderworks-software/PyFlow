import math

from PySide import QtCore

from guide import Guide


PI2 = 2 * math.pi


class GuideCircle(Guide):
    CW = 1
    CCW = -1

    def __init__(self, rect, startAngle=0.0, span=360.0, dir=CCW, follows=None):
        super(GuideCircle, self).__init__(follows)

        self.radiusX = rect.width() / 2.0
        self.radiusY = rect.height() / 2.0
        self.posX = rect.topLeft().x()
        self.posY = rect.topLeft().y()
        self.spanRad = span * PI2 / -360.0

        if dir == GuideCircle.CCW:
            self.startAngleRad = startAngle * PI2 / -360.0
            self.endAngleRad = self.startAngleRad + self.spanRad
            self.stepAngleRad = self.spanRad / self.length()
        else:
            self.startAngleRad = self.spanRad + (startAngle * PI2 / -360.0)
            self.endAngleRad = startAngle * PI2 / -360.0
            self.stepAngleRad = -self.spanRad / self.length()

    def length(self):
        return abs(self.radiusX * self.spanRad)

    def startPos(self):
        return QtCore.QPointF((self.posX + self.radiusX + self.radiusX * math.cos(self.startAngleRad)) * self.scaleX,
                (self.posY + self.radiusY + self.radiusY * math.sin(self.startAngleRad)) * self.scaleY)

    def endPos(self):
        return QtCore.QPointF((self.posX + self.radiusX + self.radiusX * math.cos(self.endAngleRad)) * self.scaleX,
                (self.posY + self.radiusY + self.radiusY * math.sin(self.endAngleRad)) * self.scaleY)

    def guide(self, item, moveSpeed):
        frame = item.guideFrame - self.startLength
        end = QtCore.QPointF((self.posX + self.radiusX + self.radiusX * math.cos(self.startAngleRad + (frame * self.stepAngleRad))) * self.scaleX,
                (self.posY + self.radiusY + self.radiusY * math.sin(self.startAngleRad + (frame * self.stepAngleRad))) * self.scaleY)
        self.move(item, end, moveSpeed)
