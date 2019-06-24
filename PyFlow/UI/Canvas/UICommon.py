from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import *
from docutils import core


DEFAULT_WIDGET_VARIANT = "DefaultWidget"


def rst2html(rst):
    if rst is not None:
        return core.publish_string(rst, writer_name="html").decode("utf-8")
    return ""


class VisibilityPolicy(IntEnum):
    AlwaysVisible = 1
    AlwaysHidden = 2
    Auto = 3


class CanvasState(IntEnum):
    DEFAULT = 0
    COMMENT_OWNERSHIP_VALIDATION = 1


class CanvasManipulationMode(IntEnum):
    NONE = 0
    SELECT = 1
    PAN = 2
    MOVE = 3
    ZOOM = 4
    COPY = 5


def lineRectIntersection(l, r):
    it_left, impactLeft = l.intersect(QtCore.QLineF(r.topLeft(), r.bottomLeft()))
    if it_left == QtCore.QLineF.BoundedIntersection:
        return impactLeft
    it_top, impactTop = l.intersect(QtCore.QLineF(r.topLeft(), r.topRight()))
    if it_top == QtCore.QLineF.BoundedIntersection:
        return impactTop
    it_bottom, impactBottom = l.intersect(QtCore.QLineF(r.bottomLeft(), r.bottomRight()))
    if it_bottom == QtCore.QLineF.BoundedIntersection:
        return impactBottom
    it_right, impactRight = l.intersect(QtCore.QLineF(r.topRight(), r.bottomRight()))
    if it_right == QtCore.QLineF.BoundedIntersection:
        return impactRight


## This function clears property view's layout.
# @param[in] layout QLayout class
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def findItemIndex(graphicsLayout, item):
    for i in range(graphicsLayout.count()):
        if item == graphicsLayout.itemAt(i).graphicsItem():
            return i
    return -1


@SingletonDecorator
class PinDefaults(object):
    """docstring for PinDefaults."""
    def __init__(self):
        self.__pinSize = 6

    @property
    def PIN_SIZE(self):
        return self.__pinSize


@SingletonDecorator
class NodeDefaults(object):
    """docstring for NodeDefaults."""
    def __init__(self):
        self.__contentMargins = 5
        self.__layoutsSpacing = 5
        self.__cornersRoundFactor = 6
        self.__svgIconKey = "svgIcon"
        self.__layer = 1000000

    @property
    def Z_LAYER(self):
        return self.__layer

    @property
    def SVG_ICON_KEY(self):
        return self.__svgIconKey

    @property
    def PURE_NODE_HEAD_COLOR(self):
        return Colors.NodeNameRectGreen

    @property
    def CALLABLE_NODE_HEAD_COLOR(self):
        return Colors.NodeNameRectBlue

    @property
    def CONTENT_MARGINS(self):
        return self.__contentMargins

    @property
    def LAYOUTS_SPACING(self):
        return self.__layoutsSpacing

    @property
    def CORNERS_ROUND_FACTOR(self):
        return self.__cornersRoundFactor


class NodeActionButtonInfo(object):
    """Used to populate node header with buttons representing node's actions from node's menu.

    See UINodeBase constructor and postCrate method.
    """
    def __init__(self, defaultSvgIcon, actionButtonClass=None):
        super(NodeActionButtonInfo, self).__init__()
        self._defaultSvgIcon = defaultSvgIcon
        self._actionButtonClass = actionButtonClass

    def actionButtonClass(self):
        return self._actionButtonClass

    def filePath(self):
        return self._defaultSvgIcon
