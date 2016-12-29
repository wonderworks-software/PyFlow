from PySide import QtGui, QtCore


class Spacings(object):

    kPortSpacing = 4
    kPortOffset = 12
    kSplitterHandleWidth = 5

    def __init__(self):
        super(Spacings, self).__init__()


class LineTypes(object):

    lDotLine = 'lDotLine'
    lSolidLine = 'lSolidLine'
    lDashLine = 'lDashLine'
    lDashDotDotLine = 'lDashDotDotLine'
    lDashDotLine = 'lDashDotLine'

    def __init__(self):
        super(LineTypes, self).__init__()


def get_line_type(name):
    if name == 'lDotLine':
        opt_pen_selected_type = QtCore.Qt.DotLine
    elif name == 'lSolidLine':
        opt_pen_selected_type = QtCore.Qt.SolidLine
    elif name == 'lDashLine':
        opt_pen_selected_type = QtCore.Qt.DashLine
    elif name == 'lDashDotDotLine':
        opt_pen_selected_type = QtCore.Qt.DashDotDotLine
    else:
        opt_pen_selected_type = QtCore.Qt.DashDotLine
    return opt_pen_selected_type


class Colors(object):

    kNodeBackgrounds = QtGui.QColor(40, 40, 40, 255)
    kNodeSelectedPenColor = QtGui.QColor(255, 255, 255, 255)
    kWhite = QtGui.QColor(255, 255, 255, 200)
    kSceneBackground = QtGui.QColor(35, 35, 35)
    kInteger = QtGui.QColor(45, 48, 99, 255)
    kIntNodeBackground = QtGui.QColor(0, 0, 170, 100)
    kGridColor = QtGui.QColor(100, 100, 100, 100)
    kConnectors = QtGui.QColor(0, 100, 0, 255)
    kPortLinesA = QtGui.QColor(0, 90, 0, 0)
    kPortLinesB = QtGui.QColor(0, 0, 90, 0)
    kNodeNameRect = QtGui.QColor(100, 100, 100, 100)
    kRed = QtGui.QColor(255, 0, 0, 255)
    kGreen = QtGui.QColor(0, 255, 0, 255)
    kBlue = QtGui.QColor(0, 0, 255, 255)
    kBlack = QtGui.QColor(50, 50, 50, 255)
    kConnectionLines = QtGui.QColor(255, 255, 255, 255)
    kDirtyPen = QtGui.QColor(250, 250, 250, 200)
    kShadow = QtGui.QColor(20, 20, 20, 150)
    kRubberRect = QtGui.QColor(255, 255, 255, 50)
    kCommentNodeBrush = QtGui.QColor(100, 100, 100, 40)
    kCommentNodeNameBackground = QtGui.QColor(100, 100, 100, 40)
    kCommentNodePen = QtGui.QColor(0, 0, 0, 100)
    kCommentNodeResizer = QtGui.QColor(255, 255, 255, 20)
    kSplitterHandleColor = QtGui.QColor(255, 255, 255, 20)
    kPortNameColor = QtGui.QColor(255, 255, 255, 255)

    def __init__(self):
        super(Colors, self).__init__()