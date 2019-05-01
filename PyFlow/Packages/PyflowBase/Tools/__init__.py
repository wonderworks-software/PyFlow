import os
RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + "/res/"

from PyFlow.UI.Tool import REGISTER_TOOL
from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Packages.PyflowBase.Tools.ScreenshotTool import ScreenshotTool
from PyFlow.Packages.PyflowBase.Tools.AlignLeftTool import AlignLeftTool
from PyFlow.Packages.PyflowBase.Tools.AlignTopTool import AlignTopTool
from PyFlow.Packages.PyflowBase.Tools.AlignRightTool import AlignRightTool
from PyFlow.Packages.PyflowBase.Tools.AlignBottomTool import AlignBottomTool
from PyFlow.Packages.PyflowBase.Tools.DockToolTest import DockToolTest


REGISTER_TOOL(PACKAGE_NAME, ScreenshotTool)
REGISTER_TOOL(PACKAGE_NAME, AlignLeftTool)
REGISTER_TOOL(PACKAGE_NAME, AlignTopTool)
REGISTER_TOOL(PACKAGE_NAME, AlignRightTool)
REGISTER_TOOL(PACKAGE_NAME, AlignBottomTool)
REGISTER_TOOL(PACKAGE_NAME, DockToolTest)
