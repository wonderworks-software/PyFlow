import os
import shutil
from string import ascii_uppercase
from random import choice

from PyFlow import Wizards


def generatePackageInit(packageName,
                        bIncludeClassNode=True,
                        bIncludeFooLib=True,
                        bIncludeUINodeFactory=True,
                        bIncludePin=True,
                        bIncludeUIPinFactory=True,
                        bIncludeTool=True,
                        bIncludeExporter=True,
                        bIncludePinInputWidgetFactory=True):
    result = "PACKAGE_NAME = '{0}'\n\n".format(packageName)
    result += "from collections import OrderedDict\n"
    result += "from PyFlow.UI.UIInterfaces import IPackage\n\n"

    if bIncludePin:
        result += "# Pins\n"
        result += "from PyFlow.Packages.{0}.Pins.DemoPin import DemoPin\n\n".format(packageName)

    if bIncludeFooLib:
        result += "# Function based nodes\n"
        result += "from PyFlow.Packages.{0}.FunctionLibraries.DemoLib import DemoLib\n\n".format(packageName)

    if bIncludeClassNode:
        result += "# Class based nodes\n"
        result += "from PyFlow.Packages.{0}.Nodes.DemoNode import DemoNode\n\n".format(packageName)

    if bIncludeTool:
        result += "# Tools\n"
        result += "from PyFlow.Packages.{0}.Tools.DemoShelfTool import DemoShelfTool\n".format(packageName)
        result += "from PyFlow.Packages.{0}.Tools.DemoDockTool import DemoDockTool\n\n".format(packageName)

    if bIncludeExporter:
        result += "# Exporters\n"
        result += "from PyFlow.Packages.{0}.Exporters.DemoExporter import DemoExporter\n\n".format(packageName)

    result += "# Factories\n"
    if bIncludeUIPinFactory:
        result += "from PyFlow.Packages.{0}.Factories.UIPinFactory import createUIPin\n".format(packageName)

    if bIncludeUINodeFactory:
        result += "from PyFlow.Packages.{0}.Factories.UINodeFactory import createUINode\n".format(packageName)

    if bIncludePinInputWidgetFactory:
        result += "from PyFlow.Packages.{0}.Factories.PinInputWidgetFactory import getInputWidget\n".format(packageName)
    result += "\n"

    result += "_FOO_LIBS = {}\n"
    result += "_NODES = {}\n"
    result += "_PINS = {}\n"
    result += "_TOOLS = OrderedDict()\n"
    result += "_EXPORTERS = OrderedDict()\n\n"

    if bIncludeFooLib:
        result += """_FOO_LIBS[DemoLib.__name__] = DemoLib(PACKAGE_NAME)\n\n"""

    if bIncludeClassNode:
        result += """_NODES[DemoNode.__name__] = DemoNode\n\n"""

    if bIncludePin:
        result += """_PINS[DemoPin.__name__] = DemoPin\n\n"""

    if bIncludeTool:
        result += """_TOOLS[DemoShelfTool.__name__] = DemoShelfTool\n"""
        result += """_TOOLS[DemoDockTool.__name__] = DemoDockTool\n\n"""

    if bIncludeExporter:
        result += """_EXPORTERS[DemoExporter.__name__] = DemoExporter\n\n"""

    result += "\nclass {0}(IPackage):\n\tdef __init__(self):\n\t\tsuper({0}, self).__init__()\n\n".format(packageName)
    result += """\t@staticmethod\n\tdef GetExporters():\n\t\treturn _EXPORTERS\n\n"""
    result += """\t@staticmethod\n\tdef GetFunctionLibraries():\n\t\treturn _FOO_LIBS\n\n"""
    result += """\t@staticmethod\n\tdef GetNodeClasses():\n\t\treturn _NODES\n\n"""
    result += """\t@staticmethod\n\tdef GetPinClasses():\n\t\treturn _PINS\n\n"""
    result += """\t@staticmethod\n\tdef GetToolClasses():\n\t\treturn _TOOLS\n\n"""

    if bIncludeUIPinFactory:
        result += """\t@staticmethod\n\tdef UIPinsFactory():\n\t\treturn createUIPin\n\n"""

    if bIncludeUINodeFactory:
        result += """\t@staticmethod\n\tdef UINodesFactory():\n\t\treturn createUINode\n\n"""

    if bIncludePinInputWidgetFactory:
        result += """\t@staticmethod\n\tdef PinsInputWidgetFactory():\n\t\treturn getInputWidget\n\n"""

    return result


def generatePackage(packageName,
                    newPackageRoot,
                    bIncludeClassNode=True,
                    bIncludeFooLib=True,
                    bIncludeUINodeFactory=True,
                    bIncludePin=True,
                    bIncludeUIPinFactory=True,
                    bIncludeTool=True,
                    bIncludeExporter=True,
                    bIncludePinInputWidgetFactory=True):
    wizardsRoot = Wizards.__path__[0]
    templatesRoot = os.path.join(wizardsRoot, "Templates")
    packageTemplateDirPath = os.path.join(templatesRoot, "PackageTemplate")
    newPackagePath = os.path.join(newPackageRoot, packageName)

    if os.path.exists(newPackagePath):
        shutil.rmtree(newPackagePath)
    shutil.copytree(packageTemplateDirPath, newPackagePath)

    for path, dirs, files in os.walk(newPackagePath):
        for newFileName in files:
            pyFileName = newFileName.replace(".txt", ".py")
            pyFilePath = os.path.join(path, pyFileName)
            txtFilePath = os.path.join(path, newFileName)
            with open(txtFilePath, "r") as f:
                txtContent = f.read()
                pyContent = txtContent.replace("@PACKAGE_NAME", packageName)
                pyContent = pyContent.replace("@RAND", "".join([choice(ascii_uppercase) for i in range(5)]))
                with open(pyFilePath, "w") as pf:
                    pf.write(pyContent)
            os.remove(txtFilePath)

    moduleInitFilePath = os.path.join(newPackagePath, "__init__.py")
    with open(moduleInitFilePath, "w") as f:
        f.write(generatePackageInit(packageName, bIncludeClassNode=bIncludeClassNode,
                                    bIncludeFooLib=bIncludeFooLib,
                                    bIncludeUINodeFactory=bIncludeUINodeFactory,
                                    bIncludePin=bIncludePin,
                                    bIncludeUIPinFactory=bIncludeUIPinFactory,
                                    bIncludeTool=bIncludeTool,
                                    bIncludeExporter=bIncludeExporter,
                                    bIncludePinInputWidgetFactory=bIncludePinInputWidgetFactory))

    # remove unneeded directories
    for path, dirs, files in os.walk(newPackagePath):
        dirName = os.path.basename(path)
        if dirName == "Nodes" and not bIncludeClassNode:
            shutil.rmtree(path)
        if dirName == "FunctionLibraries" and not bIncludeFooLib:
            shutil.rmtree(path)
        if dirName == "Pins" and not bIncludePin:
            shutil.rmtree(path)
        if dirName == "Tools" and not bIncludeTool:
            shutil.rmtree(path)
        if dirName == "Exporters" and not bIncludeExporter:
            shutil.rmtree(path)
        if dirName == "Factories":
            removedFactoresCount = 0

            if not bIncludeUINodeFactory:
                os.remove(os.path.join(path, "UINodeFactory.py"))
                removedFactoresCount += 1
            if not bIncludeUIPinFactory:
                os.remove(os.path.join(path, "UIPinFactory.py"))
                removedFactoresCount += 1
            if not bIncludePinInputWidgetFactory:
                os.remove(os.path.join(path, "PinInputWidgetFactory.py"))
                removedFactoresCount += 1

            if removedFactoresCount == 3:
                shutil.rmtree(path)

        if dirName == "UI":
            removedUIClasses = 0

            if not bIncludePin or not bIncludeUIPinFactory:
                os.remove(os.path.join(path, "UIDemoPin.py"))
                removedUIClasses += 1

            if not bIncludeClassNode or not bIncludeUINodeFactory:
                os.remove(os.path.join(path, "UIDemoNode.py"))
                removedUIClasses += 1

            if removedUIClasses == 2:
                shutil.rmtree(path)
