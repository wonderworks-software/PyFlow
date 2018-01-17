from Qt import QtGui
from Qt import QtCore


class Spacings:
    kPortSpacing = 4
    kPortOffset = 12
    kSplitterHandleWidth = 5


class LineTypes:
    lDotLine = 'lDotLine'
    lSolidLine = 'lSolidLine'
    lDashLine = 'lDashLine'
    lDashDotDotLine = 'lDashDotDotLine'
    lDashDotLine = 'lDashDotLine'


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


class Colors:
    NodeBackgrounds = QtGui.QColor(30, 30, 30, 200)
    NodeSelectedPenColor = QtGui.QColor(200, 200, 200, 150)
    White = QtGui.QColor(255, 255, 255, 200)
    SceneBackground = QtGui.QColor(35, 35, 35)
    GridColor = QtGui.QColor(100, 100, 100, 100)
    GridColorDarker = QtGui.QColor(20, 20, 20)
    Connectors = QtGui.QColor(0, 100, 0, 255)
    PortLinesA = QtGui.QColor(0, 90, 0, 0)
    PortLinesB = QtGui.QColor(0, 0, 90, 0)
    NodeNameRect = QtGui.QColor(80, 80, 100, 200)
    Red = QtGui.QColor(255, 0, 0, 255)
    Green = QtGui.QColor(96, 169, 23, 255)
    Blue = QtGui.QColor(0, 0, 255, 255)
    Black = QtGui.QColor(50, 50, 50, 255)
    AbsoluteBlack = QtGui.QColor(0, 0, 0, 255)
    ConnectionLines = QtGui.QColor(255, 255, 255, 255)
    DirtyPen = QtGui.QColor(250, 250, 250, 200)
    Shadow = QtGui.QColor(20, 20, 20, 150)
    RubberRect = QtGui.QColor(255, 255, 255, 50)
    CommentNodeBrush = QtGui.QColor(100, 100, 100, 40)
    CommentNodeNameBackground = QtGui.QColor(100, 100, 100, 40)
    CommentNodePen = QtGui.QColor(0, 0, 0, 100)
    CommentNodeResizer = QtGui.QColor(255, 255, 255, 20)
    SplitterHandleColor = QtGui.QColor(255, 255, 255, 20)
    PortNameColor = QtGui.QColor(255, 255, 255, 255)
    Pink = QtGui.QColor(255, 8, 127)
    Yellow = QtGui.QColor(255, 211, 25)
    Gray = QtGui.QColor(110, 110, 110)
    DarkGray = QtGui.QColor(60, 60, 60)
    LimeGreen = QtGui.QColor(0, 168, 107)

    Float = Green
    Int = LimeGreen
    Any = Yellow
    Array = Gray
    Bool = Red
    Exec = QtGui.QColor(255, 255, 255, 255)
    String = Pink
    IntVector2 = QtGui.QColor(0, 0, 255, 200)
    FloatVector2 = QtGui.QColor(0, 0, 255, 200)
    IntVector3 = QtGui.QColor(0, 0, 255, 200)
    FloatVector3 = QtGui.QColor(0, 0, 255, 200)
    IntVector4 = QtGui.QColor(0, 0, 255, 200)
    FloatVector4 = QtGui.QColor(173, 216, 230, 200)
    Quaternion = QtGui.QColor(32, 178, 170, 200)
    Transform = QtGui.QColor(255, 69, 0, 200)
