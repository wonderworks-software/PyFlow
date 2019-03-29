"""@file Settings.py

Some common variables related to appearance.
"""
from Qt import QtGui
from Qt import QtCore


class Spacings:
    kPinSpacing = 4
    kPinOffset = 12
    kSplitterHandleWidth = 5


class Colors:
    
    Orange =          QtGui.QColor(255, 160, 47)
    OrangeLighter =   QtGui.QColor(234, 165, 83)
    OrangeLighter2=   QtGui.QColor(255, 170, 0)
    OrangeDarker =    QtGui.QColor(215, 128, 26)

    BG_DARK =          QtGui.QColor(50, 50, 50)


    Grey =             QtGui.QColor(64, 64, 64)

    Grey1 =            QtGui.QColor(77, 77, 77)
    Grey2 =            QtGui.QColor(100, 100, 100)
    Grey3 =            QtGui.QColor(93, 93, 93)

    GREYDARK =         QtGui.QColor(30, 30, 30)

    NodeBackgrounds = QtGui.QColor(40, 40, 40, 200)
    NodeSelectedPenColor = QtGui.QColor(200, 200, 200, 150)
    NodeNameRect = QtGui.QColor(30, 80, 30, 200)

    NodeNameRectGreen = QtGui.QColor(74, 124, 39, 200)
    NodeNameRectBlue = QtGui.QColor(28, 74, 149, 200) 
       
    CommentNodeBrush = QtGui.QColor(100, 100, 100, 40)
    CommentNodeNameBackground = QtGui.QColor(100, 100, 100, 40)
    CommentNodePen = QtGui.QColor(0, 0, 0, 100)
    CommentNodeResizer = QtGui.QColor(255, 255, 255, 20)

    SplitterHandleColor = QtGui.QColor(255, 255, 255, 20)

    SceneBackground = QtGui.QColor(35, 35, 35)

    GridColor = QtGui.QColor(20, 20, 20, 100)
    GridColorDarker = QtGui.QColor(20, 20, 20)

    ConnectionLines = QtGui.QColor(255, 255, 255, 255)
    Connectors = QtGui.QColor(0, 100, 0, 255)
    PinLinesA = QtGui.QColor(0, 90, 0, 0)
    PinLinesB = QtGui.QColor(0, 0, 90, 0)
    PinNameColor = QtGui.QColor(255, 255, 255, 255)
    
    DirtyPen = QtGui.QColor(250, 250, 250, 200)
    Shadow = QtGui.QColor(20, 20, 20, 150)
    RubberRect = QtGui.QColor(255, 255, 255, 50)

    Red = QtGui.QColor(255, 0, 0, 255)
    Green = QtGui.QColor(96, 169, 23, 255)
    Blue = QtGui.QColor(0, 0, 255, 255)
    Black = QtGui.QColor(50, 50, 50, 255)
    AbsoluteBlack = QtGui.QColor(0, 0, 0, 255)    
    White = QtGui.QColor(255, 255, 255, 200)
    Pink = QtGui.QColor(255, 8, 127)
    Yellow = QtGui.QColor(255, 211, 25)
    DarkYellow = QtGui.QColor(255/2, 211/2, 25/2)
    Gray = QtGui.QColor(110, 110, 110)
    DarkGray = QtGui.QColor(60, 60, 60)
    LimeGreen = QtGui.QColor(0, 168, 107)

    Float = Green
    Int = LimeGreen
    Array = Gray
    Bool = Red
    Exec = QtGui.QColor(255, 255, 255)
    String = Pink
    FloatVector2 = QtGui.QColor(0, 0, 255)
    FloatVector3 = QtGui.QColor(170, 100, 200)
    FloatVector4 = QtGui.QColor(173, 216, 230)
    Quaternion = QtGui.QColor(32, 178, 170)
    Matrix33 = QtGui.QColor(150, 69, 20)
    Matrix44 = QtGui.QColor(150, 0, 20)
