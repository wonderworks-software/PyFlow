## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from docutils import core
from PyFlow import GET_PACKAGES
from PyFlow.Core.Common import *
from PyFlow.UI.Utils.stylesheet import Colors


# DEFAULT_WIDGET_VARIANT = "DefaultWidget"


def rst2html(rst):
    if rst is not None:
        return core.publish_string(rst, writer_name="html").decode("utf-8")
    return ""


def fetchPackageNames(graphJson):
    """Parses serialized graph and returns all package names it uses

    :param graphJson: Serialized graph
    :type graphJson: dict
    :rtyoe: list(str)
    """
    packages = set()

    def worker(graphData):
        for node in graphData["nodes"]:
            packages.add(node["package"])

            for inpJson in node["inputs"]:
                packages.add(inpJson["package"])

            for outJson in node["inputs"]:
                packages.add(outJson["package"])

            if "graphData" in node:
                worker(node["graphData"])

    worker(graphJson)
    return packages


def validateGraphDataPackages(graphData, missedPackages=None):
    """Checks if packages used in serialized data accessible

    Missed packages will be added to output set

    :param graphData: Serialized graph
    :type graphData: dict
    :param missedPackages: Package names that missed
    :type missedPackages: set
    :rtype: bool
    """
    if missedPackages is None:
        missedPackages = set()
    existingPackages = GET_PACKAGES().keys()
    graphPackages = fetchPackageNames(graphData)
    for pkg in graphPackages:
        if pkg not in existingPackages:
            missedPackages.add(pkg)
    return len(missedPackages) == 0


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


class Spacings:
    kPinSpacing = 4
    kPinOffset = 12
    kSplitterHandleWidth = 5


def lineRectIntersection(l, r):
    it_left, impactLeft = l.intersect(QtCore.QLineF(r.topLeft(), r.bottomLeft()))
    if it_left == QtCore.QLineF.BoundedIntersection:
        return impactLeft
    it_top, impactTop = l.intersect(QtCore.QLineF(r.topLeft(), r.topRight()))
    if it_top == QtCore.QLineF.BoundedIntersection:
        return impactTop
    it_bottom, impactBottom = l.intersect(
        QtCore.QLineF(r.bottomLeft(), r.bottomRight())
    )
    if it_bottom == QtCore.QLineF.BoundedIntersection:
        return impactBottom
    it_right, impactRight = l.intersect(QtCore.QLineF(r.topRight(), r.bottomRight()))
    if it_right == QtCore.QLineF.BoundedIntersection:
        return impactRight


# This function clears property view's layout.
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
    def COMPUTING_NODE_HEAD_COLOR(self):
        return Colors.Red

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


@SingletonDecorator
class SessionDescriptor(object):
    def __init__(self):
        self.software = ""
