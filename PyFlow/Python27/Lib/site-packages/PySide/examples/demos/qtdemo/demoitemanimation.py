from PySide import QtCore, QtGui

from colors import Colors


class DemoItemAnimation(QtGui.QGraphicsItemAnimation):
    ANIM_IN, ANIM_OUT, ANIM_UNSPECIFIED = range(3)

    def __init__(self, item, inOrOut=ANIM_UNSPECIFIED):
        super(DemoItemAnimation, self).__init__()

        self.startPos = QtCore.QPointF()
        self.opacityAt0 = 1.0
        self.opacityAt1 = 1.0
        self.startDelay = 0
        self.inOrOut = inOrOut
        self.hideOnFinished = False
        self.forcePlay = False
        self.timeline = QtCore.QTimeLine(5000)
        self.timeline.setFrameRange(0, 2000)
        self.timeline.setUpdateInterval(int(1000.0/Colors.fps))
        self.moveOnPlay = False
        self.setTimeLine(self.timeline)
        self.setItem(item)

    def prepare(self):
        self.demoItem().prepare()

    def setStartPos(self, pos):
        self.startPos = pos

    def setDuration(self, duration):
        duration = int(duration * Colors.animSpeed)
        self.timeline.setDuration(duration)
        self.moveOnPlay = True

    def setCurrentTime(self, ms):
        self.timeline.setCurrentTime(ms)

    def notOwnerOfItem(self):
        return self is not self.demoItem().currentAnimation

    def play(self, fromStart=True, force=False):
        self.fromStart = fromStart
        self.forcePlay = force

        currPos = self.demoItem().pos()

        # If the item that this animation controls in currently under the
        # control of another animation, stop that animation first.
        if self.demoItem().currentAnimation is not None:
            self.demoItem().currentAnimation.timeline.stop()
        self.demoItem().currentAnimation = self
        self.timeline.stop()

        if Colors.noAnimations and not self.forcePlay:
            self.timeline.setCurrentTime(1)
            self.demoItem().setPos(self.posAt(1))
        else:
            if self.demoItem().isVisible():
                # If the item is already visible, start the animation from the
                # items current position rather than from start..
                self.setPosAt(0.0, currPos)
            else:
                self.setPosAt(0.0, self.startPos)

            if self.fromStart:
                self.timeline.setCurrentTime(0)
                self.demoItem().setPos(self.posAt(0))

        if self.inOrOut == DemoItemAnimation.ANIM_IN:
            self.demoItem().setRecursiveVisible(True)

        if self.startDelay:
            QtCore.QTimer.singleShot(self.startDelay, self.playWithoutDelay)
            return
        else:
            self.playWithoutDelay()

    def playWithoutDelay(self):
        if self.moveOnPlay and not (Colors.noAnimations and not self.forcePlay):
            self.timeline.start()
        self.demoItem().animationStarted(self.inOrOut)

    def stop(self, reset):
        self.timeline.stop()
        if reset:
            self.demoItem().setPos(self.posAt(0))
        if self.hideOnFinished and not self.moveOnPlay:
            self.demoItem().setRecursiveVisible(False)
        self.demoItem().animationStopped(self.inOrOut)

    def setRepeat(self, nr):
        self.timeline.setLoopCount(nr)

    def playReverse(self):
        pass

    def running(self):
        return self.timeLine().state() == QtCore.QTimeLine.Running

    def runningOrItemLocked(self):
        return self.running() or self.demoItem().locked

    def lockItem(self, state):
        self.demoItem().locked = state

    def demoItem(self):
        return self.item()

    def setOpacityAt0(self, opacity):
        self.opacityAt0 = opacity

    def setOpacityAt1(self, opacity):
        self.opacityAt1 = opacity

    def setOpacity(self, step):
        demoItem = self.item()
        demoItem.opacity = self.opacityAt0 + step * step * step * (self.opacityAt1 - self.opacityAt0)

    def afterAnimationStep(self, step):
        if step == 1.0:
            if self.timeline.loopCount() > 0:
                # Animation finished.
                if self.hideOnFinished:
                    self.demoItem().setRecursiveVisible(False)
                self.demoItem().animationStopped(self.inOrOut)
        elif Colors.noAnimations and not self.forcePlay:
            # The animation is not at end, but the animations should not play,
            # so go to end.
            self.setStep(1.0)
