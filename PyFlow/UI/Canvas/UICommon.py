from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import *


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


## This function clears property view's layout.
# @param[in] layout QLayout class
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


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
        self.__contentMargins = 3
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
