from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import *


class VisibilityPolicy(IntEnum):
    AlwaysVisible = 1
    AlwaysHidden = 2
    Auto = 3


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
        self.__layoutsSpacing = 10
        self.__cornersRoundFactor = 6

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
