from PySide import QtGui


class PortTypes(object):

    kInput = 'input'
    kOutput = 'output'

    def __init__(self):
        super(PortTypes, self).__init__()


class Spacings(object):

    kPortSpacing = 4
    kPortOffset = 12

    def __init__(self):
        super(Spacings, self).__init__()


class Colors(object):

    kNodeBackgrounds = QtGui.QColor(45, 45, 45, 100)
    kSceneBackground = QtGui.QColor(65, 65, 65)
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
    kBlack = QtGui.QColor(255, 255, 255, 255)
    kConnectionLines = QtGui.QColor(255, 255, 255, 90)

    def __init__(self):
        super(Colors, self).__init__()
