from PySide import QtCore


class Guide(object):
    def __init__(self, follows=None):
        self.scaleX = 1.0
        self.scaleY = 1.0

        if follows is not None:
            while follows.nextGuide is not follows.firstGuide:
                follows = follows.nextGuide

            follows.nextGuide = self
            self.prevGuide = follows
            self.firstGuide = follows.firstGuide
            self.nextGuide = follows.firstGuide
            self.startLength = int(follows.startLength + follows.length()) + 1
        else:
            self.prevGuide = self
            self.firstGuide = self
            self.nextGuide = self
            self.startLength = 0

    def setScale(self, scaleX, scaleY, all=True):
        self.scaleX = scaleX
        self.scaleY = scaleY

        if all:
            next = self.nextGuide
            while next is not self:
                next.scaleX = scaleX
                next.scaleY = scaleY
                next = next.nextGuide

    def setFence(self, fence, all=True):
        self.fence = fence

        if all:
            next = self.nextGuide
            while next is not self:
                next.fence = fence
                next = next.nextGuide

    def lengthAll(self):
        len = self.length()
        next = self.nextGuide
        while next is not self:
            len += next.length()
            next = next.nextGuide

        return len

    def move(self, item, dest, moveSpeed):
        walkLine = QtCore.QLineF(item.getGuidedPos(), dest)
        if moveSpeed >= 0 and walkLine.length() > moveSpeed:
            # The item is too far away from it's destination point so we move
            # it towards it instead.
            dx = walkLine.dx()
            dy = walkLine.dy()

            if abs(dx) > abs(dy):
                # Walk along x-axis.
                if dx != 0:
                    d = moveSpeed * dy / abs(dx)

                    if dx > 0:
                        s = moveSpeed
                    else:
                        s = -moveSpeed

                    dest.setX(item.getGuidedPos().x() + s)
                    dest.setY(item.getGuidedPos().y() + d)
            else:
                # Walk along y-axis.
                if dy != 0:
                    d = moveSpeed * dx / abs(dy)

                    if dy > 0:
                        s = moveSpeed
                    else:
                        s = -moveSpeed

                    dest.setX(item.getGuidedPos().x() + d)
                    dest.setY(item.getGuidedPos().y() + s)

        item.setGuidedPos(dest)

    def startPos(self):
        return QtCore.QPointF(0, 0)

    def endPos(self):
        return QtCore.QPointF(0, 0)

    def length(self):
        return 1.0

    def guide(self, item, moveSpeed):
        raise NotImplementedError
