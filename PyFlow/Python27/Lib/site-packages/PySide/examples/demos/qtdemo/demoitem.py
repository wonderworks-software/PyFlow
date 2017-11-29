from PySide import QtCore, QtGui

from colors import Colors


class SharedImage(object):
    def __init__(self):
        self.refCount = 0
        self.image = None
        self.pixmap = None
        self.matrix = QtGui.QMatrix()
        self.unscaledBoundingRect = QtCore.QRectF()


class DemoItem(QtGui.QGraphicsItem):
    sharedImageHash = {}

    matrix = QtGui.QMatrix()

    def __init__(self, scene=None, parent=None):
        super(DemoItem, self).__init__(parent, scene)

        self.opacity = 1.0
        self.locked = False
        self.prepared = False
        self.neverVisible = False
        self.noSubPixeling = False
        self.currentAnimation = None
        self.currGuide = None
        self.guideFrame = 0.0
        self.sharedImage = SharedImage()
        self.sharedImage.refCount += 1

        self.startFrame = 0.0
        self.hashKey = ''

    def __del__(self):
        self.sharedImage.refCount -= 1
        if self.sharedImage.refCount == 0:
            if self.hashKey:
                del DemoItem.sharedImageHash[self.hashKey]

    def animationStarted(self, id=0):
        pass

    def animationStopped(self, id=0):
        pass

    def setNeverVisible(self, never=True):
        pass

    def setRecursiveVisible(self, visible):
        if visible and self.neverVisible:
            self.setVisible(False)
            return

        self.setVisible(visible)
        for c in self.childItems():
            c.setVisible(visible)

    def useGuide(self, guide, startFrame=0.0):
        self.startFrame = startFrame
        self.guideFrame = startFrame
        while self.guideFrame > guide.startLength + guide.length():
            if guide.nextGuide == guide.firstGuide:
                break

            guide = guide.nextGuide

        self.currGuide = guide

    def guideAdvance(self, distance):
        self.guideFrame += distance
        while self.guideFrame > self.currGuide.startLength + self.currGuide.length():
            self.currGuide = self.currGuide.nextGuide
            if self.currGuide == self.currGuide.firstGuide:
                self.guideFrame -= self.currGuide.lengthAll()

    def guideMove(self, moveSpeed):
        self.currGuide.guide(self, moveSpeed)

    def setPosUsingSheepDog(self, dest, sceneFence):
        self.setPos(dest)
        if sceneFence.isNull():
            return

        itemWidth = self.boundingRect().width()
        itemHeight = self.boundingRect().height()
        fenceRight = sceneFence.x() + sceneFence.width()
        fenceBottom = sceneFence.y() + sceneFence.height()

        if self.scenePos().x() < sceneFence.x():
            self.moveBy(self.mapFromScene(QtCore.QPointF(sceneFence.x(), 0)).x(), 0)

        if self.scenePos().x() > fenceRight - itemWidth:
            self.moveBy(self.mapFromScene(QtCore.QPointF(fenceRight - itemWidth, 0)).x(), 0)

        if self.scenePos().y() < sceneFence.y():
            self.moveBy(0, self.mapFromScene(QtCore.QPointF(0, sceneFence.y())).y())

        if self.scenePos().y() > fenceBottom - itemHeight:
            self.moveBy(0, self.mapFromScene(QtCore.QPointF(0, fenceBottom - itemHeight)).y())

    def setGuidedPos(self, pos):
        # Make sure we have a copy.
        self.guidedPos = QtCore.QPointF(pos)

    def getGuidedPos(self):
        # Return a copy so that it can be changed.
        return QtCore.QPointF(self.guidedPos)

    def switchGuide(self, guide):
        self.currGuide = guide
        self.guideFrame = 0.0

    def inTransition(self):
        if self.currentAnimation:
            return self.currentAnimation.running()
        else:
            return False

    @staticmethod
    def setMatrix(matrix):
        DemoItem.matrix = matrix

    def useSharedImage(self, hashKey):
        self.hashKey = hashKey
        if hashKey not in DemoItem.sharedImageHash:
            DemoItem.sharedImageHash[hashKey] = self.sharedImage
        else:
            self.sharedImage.refCount -= 1
            self.sharedImage = DemoItem.sharedImageHash[hashKey]
            self.sharedImage.refCount += 1

    def validateImage(self):
        if (self.sharedImage.matrix != DemoItem.matrix and not Colors.noRescale) or (self.sharedImage.image is None and self.sharedImage.pixmap is None):
            # (Re)create image according to new matrix.
            self.sharedImage.image = None
            self.sharedImage.pixmap = None
            self.sharedImage.matrix = DemoItem.matrix

            # Let subclass create and draw a new image according to the new
            # matrix.
            if Colors.noRescale:
                m = QtGui.QMatrix()
            else:
                m = DemoItem.matrix
            image = self.createImage(m)
            if image is not None:
                if Colors.showBoundingRect:
                    # Draw red transparent rect.
                    painter = QtGui.QPainter(image)
                    painter.fillRect(image.rect(), QtGui.QColor(255, 0, 0, 50))
                    painter.end()

                self.sharedImage.unscaledBoundingRect = self.sharedImage.matrix.inverted()[0].mapRect(QtCore.QRectF(image.rect()))

                if Colors.usePixmaps:
                    if image.isNull():
                        self.sharedImage.pixmap = QtGui.QPixmap(1, 1)
                    else:
                        self.sharedImage.pixmap = QtGui.QPixmap(image.size())

                    self.sharedImage.pixmap.fill(QtGui.QColor(0, 0, 0, 0))
                    painter = QtGui.QPainter(self.sharedImage.pixmap)
                    painter.drawImage(0, 0, image)
                else:
                    self.sharedImage.image = image

                return True
            else:
                return False

        return True

    def boundingRect(self):
        self.validateImage()
        return self.sharedImage.unscaledBoundingRect

    def paint(self, painter, option=None, widget=None):
        if self.validateImage():
            wasSmoothPixmapTransform = painter.testRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

            if Colors.noRescale:
                # Let the painter scale the image for us.  This may degrade
                # both quality and performance.
                if self.sharedImage.image is not None:
                    painter.drawImage(self.pos(), self.sharedImage.image)
                else:
                    painter.drawPixmap(self.pos(), self.sharedImage.pixmap)
            else:
                m = painter.worldMatrix()
                painter.setWorldMatrix(QtGui.QMatrix())

                x = m.dx()
                y = m.dy()
                if self.noSubPixeling:
                    x = QtCore.qRound(x)
                    y = QtCore.qRound(y)

                if self.sharedImage.image is not None:
                    painter.drawImage(QtCore.QPointF(x, y),
                            self.sharedImage.image)
                else:
                    painter.drawPixmap(QtCore.QPointF(x, y),
                            self.sharedImage.pixmap)

            if not wasSmoothPixmapTransform:
                painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform,
                        False)

    def createImage(self, matrix):
        return None

    def collidesWithItem(self, item, mode):
        return False
