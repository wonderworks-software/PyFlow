## Copyright 2023 David Lario

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from nine import str
from PyFlow.PyFlow.UI.Tool.Tool import FormTool
from PyFlow.PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.PyFlow.UI.Forms.PackageBuilder import PackageBuilder as PB
from qtpy import QtGui
from uuid import uuid4

class PackageBuilder(FormTool):
    """docstring for AlignBottomTool."""
    def __init__(self):
        super(PackageBuilder, self).__init__()
        self.guid = uuid4()

    @staticmethod
    def toolTip():
        return "Package Builder"

    def guid(self):
        return self.guid
    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "options_icon.png")

    @staticmethod
    def getSmallIconPath():
        return RESOURCES_DIR + "new_file_icon.png"

    @staticmethod
    def getLargeIconPath():
        return RESOURCES_DIR + "new_file_icon.png"

    @staticmethod
    def name():
        return str("PackageBuilder")

    def do(self):
        self.pyFlowInstance.newFileFromUi(PB.PackageBuilder(self.pyFlowInstance.parent, self.pyFlowInstance.parent))
