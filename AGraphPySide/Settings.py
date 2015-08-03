from PySide import QtGui


class Spacings(object):

    kPortSpacing = 4
    kPortOffset = 12

    def __init__(self):
        super(Spacings, self).__init__()


class Colors(object):

    kNodeBackgrounds = QtGui.QColor(45, 45, 45, 120)
    kWhite = QtGui.QColor(255, 255, 255, 200)
    kSceneBackground = QtGui.QColor(25, 25, 25)
    kInteger = QtGui.QColor(45, 48, 99, 255)
    kIntNodeBackground = QtGui.QColor(0, 0, 170, 100)
    kGridColor = QtGui.QColor(100, 100, 100, 100)
    kConnectors = QtGui.QColor(0, 100, 0, 255)
    kPortLinesA = QtGui.QColor(0, 90, 0, 50)
    kPortLinesB = QtGui.QColor(0, 0, 90, 50)
    kNodeNameRect = QtGui.QColor(100, 100, 100, 100)
    kRed = QtGui.QColor(255, 0, 0, 255)
    kGreen = QtGui.QColor(0, 255, 0, 255)
    kBlue = QtGui.QColor(0, 0, 255, 255)
    kBlack = QtGui.QColor(50, 50, 50, 255)
    kConnectionLines = QtGui.QColor(255, 255, 255, 255)
    kDirtyPen = QtGui.QColor(250, 250, 250, 200)
    kShadow = QtGui.QColor(20, 20, 20, 150)
    kRubberRect = QtGui.QColor(255, 255, 255, 50)

    def __init__(self):
        super(Colors, self).__init__()
