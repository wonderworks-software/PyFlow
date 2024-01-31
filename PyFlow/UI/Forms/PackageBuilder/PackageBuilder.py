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


import os
import shutil
#import subprocess
import uuid
import inspect
import importlib

from qtpy.QtCore import QCoreApplication
from qtpy.QtGui import QIcon, QPixmap
from sqlalchemy.sql.coercions import cls

from PyFlow import Packages

from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtWidgets import *

from qtpy.uic import loadUiType, loadUi
from qtpy import QtUiTools
from blinker import Signal

path = os.path.dirname(os.path.abspath(__file__))
packageRoot = Packages.__path__[0]

uiFile = os.path.join(path, 'PackageBuilder.ui')
#WindowTemplate, TemplateBaseClass = loadUiType(uiFile)
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "UI/resources/")

from qtpy.QtCore import QItemSelectionModel #Because Pyside hijacked from pyqt
from qtpy.QtCore import QSortFilterProxyModel, QRegularExpression, QModelIndex
from qtpy.QtGui import QStandardItemModel, QStandardItem

class TableComboModel(QComboBox):
    #Should combine with to customWidgets
    #currentIndexChanged2 = pyqtSignal([dict])

    def __init__(self, parent, *args, **kwargs):
        super(TableComboModel, self).__init__(parent)
        #super(ComboModel, self).currentIndexChanged[dict].connect(self.currentIndexChangedDictionary)

        self.setModel(kwargs['dataModel'])
        self.setModelColumn(1)
        self.column = kwargs['column']
        self.row = kwargs['row']
        self.id = kwargs['id']

        self.dataout = {}
        self.dataout['id'] = kwargs['id']
        self.dataout['column'] = kwargs['column']
        self.dataout['row'] = kwargs['row']
        self.dataout['dataModel'] = kwargs['dataModel']
        self.newItemName = ""

        #for key in kwargs:
        #    print("another keyword arg: %s: %s" % (key, kwargs[key]))

        #self.currentIndexChanged.connect(self.currentIndexChangedDictionary)
        self.currentIndexChanged.connect(self.on_currentIndexChanged)
        self.currentIndexChanged.connect(self.currentIndexChangedDictionary)
        self.editTextChanged.connect(self.on_newInformation)
        self.setEditable(True)

    def column(self):
        return self.x

    def row(self):
        return self.y

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.dbIds)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return 2

    def setValue(self, index, column=0):
        for row in range(self.model().rowCount()):
            if str(self.model().index(row, column).data()) == str(index):
                #print(self.model().index(row, 0).data(), index)
                self.setCurrentIndex(row)
                break

    def data(self, index, role=QtCore.Qt.DisplayRole):
        #print('ComboModel data')
        if not index.isValid() or ( role != QtGui.Qt.DisplayRole and role != QtGui.Qt.EditRole ):
            print('ComboModel return invalid QVariant')
            return QtCore.QVariant()
        if index.column() == 0:
            return QtCore.QVariant(self.dbIds[index.row()])
        if index.column() == 1:
            return QtCore.QVariant(self.dbValues[index.row()])
        print('ComboModel return invalid QVariant')
        return QtCore.QVariant()

    def currentIndexChangedDictionary(self, index):
        #print("Combo Index changed2:", index)
        #self.dataout['index'] = index
        self.dataout['value'] = self.dataout['dataModel'].index(index, 0).data()
        #self.currentIndexChanged2.emit(self.dataout)

    def on_newInformation(self, newName):
        if 1==2:
            if newName != "":
                self.newItemName = newName
            else:
                #Create a new model that has old and new data
                cmbTableModel = QStandardItemModel(0, 1, self)
                cmbTableModel.setItem(0, 1, QStandardItem(self.newItemName))

                for row in range(self.dataout['dataModel'].rowCount()):
                    cmbTableModel.setItem(row+1, 1, QStandardItem(self.dataout['dataModel'].index(row,1).data()))

                self.setModel(cmbTableModel)

    def on_currentIndexChanged(self, index):
        pass
        #print("Combo Index changed:", index) #, self.sender().x(), self.y)
        #self.currentIndexChanged2.emit(self.dataout)

class PackageBuilder(QMdiSubWindow):
    def __init__(self, parent=None):
        super(PackageBuilder, self).__init__(parent)

        self.ui = QtUiTools.QUiLoader().load(uiFile)
        self.PackageName = "PackageBuilder"
        self.parent = parent

        self.defaultfolderlist = ["Tools", "FunctionLibraries", "Nodes", "Pins", "PrefsWidgets", "UI"]
        packageRoot = Packages.__path__[0]
        self.ui.txtPackageFolderLocation.setText(packageRoot)

        rowcount = 0
        self.tooldict = {}

        self.functiondict = {}
        self.pindict = {}

        self.pindefs = {}
        self.pindefs["Inputs"] = {}
        self.pindefs["Outputs"] = {}

        self.codeDict = {}
        self.codeList = []
        self.pindata = {}
        self.selectedPinName = ""
        self.selectedPinDir = ""
        self.workingFile = ""

        packagelistmodel = QStandardItemModel(0, 1)
        for directories in os.listdir(packageRoot):
            if directories[1] != "_":
                packagelistmodel.setItem(rowcount, 0, QStandardItem(directories))
                rowcount += 1

        self.packagelistModelproxy = QtCore.QSortFilterProxyModel(self)
        #self.packagelistModelproxy.setSourceModel(packagelistmodel)

        self.ui.lstPackages.setModel(self.packagelistModelproxy)
        self.ui.lstPackages.setModel(packagelistmodel)
        self.ui.lstPackages.setModelColumn(0)
        self.ui.lstPackages.clicked.connect(self.onSelectPackage)

        self.ui.cmdOpenPackageFolder.clicked.connect(self.onOpenPackageFolder)
        self.ui.txtPackageFilter.textChanged.connect(self.onChangeFilterValue)
        self.ui.tvPackageItems.header().hide()

        #self.ui.tblFInputPins.selectionModel().selectionChanged.connect(self.on_tblFInputPins_Changed)
        self.ui.tblFInputPins.clicked.connect(self.on_tblFInputPins_clicked)

        #self.ui.tblFOutputPins.selectionModel().selectionChanged.connect(self.on_tblFOutputPins_Changed)
        self.ui.tblFOutputPins.clicked.connect(self.on_tblFOutputPins_clicked)
        self.ui.tvPackageItems.itemClicked.connect(self.on_tvPackageItems_clicked)


        self.ui.cmdCreatePackage.clicked.connect(self.on_cmdCreatePackage_clicked)

        self.ui.cmdCommandAddSmallIcon.clicked.connect(self.on_cmdCommandAddSmallIcon_clicked)
        self.ui.cmdCommandAddMediumIcon.clicked.connect(self.on_cmdCommandAddMediumIcon_clicked)
        self.ui.cmdCommandAddLargeIcon.clicked.connect(self.on_cmdCommandAddLargeIcon_clicked)

        self.onPinScan()

    @staticmethod
    def supportedSoftwares():
        """Under what software to work
        """
        return ["any"]

    def getMenuOrder(self):
        menuOrder = ["Tools", "Windows", "Help"]
        return menuOrder

    def getMenuLayout(self):
        menuDict = {}
        separatorCount = 0
        packageList = []
        menuDict["Packages"] = packageList

        fileMenuList = []
        menuDict["File"] = fileMenuList

        packageToolList = []
        packageToolList.append({"Action": "Add Action", "Package": "PackageBuilder", "PackageGroup": "ProgramBase","Instance": self, "Command": "PackageBuilder"})
        menuDict["Tools"] = packageToolList

        windowMenuList = []
        menuDict["Windows"] = windowMenuList

        helpMenuList = []
        helpMenuList.append({"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Instance": self, "Command": "About"})
        helpMenuList.append({"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Instance": self, "Command": "HomePage"})
        menuDict["Help"] = helpMenuList

        return menuDict

    def getRibbonOrder(self):
        ribbonOrder = ["Tools"]
        return ribbonOrder

    def getRibbonLayout(self):
        ribbonBarDict = {}
        ribbonItems = []
        ribbonItems.append({"Bar": "ProgramBase", "Section": "Tools", "Widget": "Small Button", "SmallIcon": RESOURCES_DIR + "new_file_icon.png", "LargeIcon": RESOURCES_DIR + "new_file_icon.png", "Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase","Instance": self, "Command": "ToolBar"})
        ribbonBarDict["Tools"] = ribbonItems
        return ribbonBarDict

    def getToolBarLayout(self):

        toolBarDict = {}
        pyFlowToolBar = []
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action", "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "NewFile"})
        toolBarDict["File"] = pyFlowToolBar

        return toolBarDict

    def onChangeFilterValue(self, text):
        #self.packagelistModelproxy.setFilterKeyColumn(text)

        search = QtCore.QRegularExpression(str(text), QRegularExpression.CaseInsensitiveOption)
        #self.packagelistModelproxy.setFilterRegExp(search)

    def onSelectPackage(self, index):
        QCoreApplication.processEvents()
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(index.row(), 0).data()
        #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex(), 0, None).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        self.ui.tvPackageItems.clear()
        self.ui.txtPackageName.setText(selectedpackage)

        CommandList = {}
        FunctionList = {}
        PrefsWidgetsList = {}

        for directories in os.listdir(packagepath):
            if directories[1] != "_":
                parent = QTreeWidgetItem(self.ui.tvPackageItems)
                parent.setText(0, directories)
                #parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                filepath = os.path.join(packagepath, directories)
                for file in os.listdir(filepath):
                    if file[1] != "_" and file[-3:]==".py":
                        child = QTreeWidgetItem(parent)
                        #child.clicked.connect(self.on_tvPackageItems_clicked)
                        #child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                        child.setText(0, file[:-3])
                        #child.setCheckState(0, QtCore.Qt.Unchecked)
                        filefullpath = os.path.join(filepath, file)

                        try:
                            f = open(filefullpath, "r")
                            for lineitem in f:
                                if directories[1] == "FunctionLibrary":
                                    if len(lineitem) > 10:
                                        if lineitem[:5] == "class":
                                            classnamestart = lineitem.find(" ")
                                            classnameend  = lineitem.find("(")
                                            #child2 = QTreeWidgetItem(child)
                                            #child2.setFlags(child2.flags() | QtCore.Qt.ItemIsUserCheckable)
                                            #child2.setText(0, lineitem[classnamestart+1:classnameend])
                                            #child2.setCheckState(0, QtCore.Qt.Unchecked)
                                        if lineitem.find("def ") != -1:
                                            if lineitem[8] != "_":
                                                classnamestart = 7
                                                classnameend = lineitem.find("(")
                                                child2 = QTreeWidgetItem(child)
                                                #child2.setFlags(child2.flags() | QtCore.Qt.ItemIsUserCheckable)
                                                classname = lineitem[classnamestart+1:classnameend]
                                                if file.find(lineitem[classnamestart+1:classnameend]) == -1:
                                                    functionname = lineitem[classnamestart+1:classnameend]
                                                    child2.setText(0, functionname)
                                                    #child2.setCheckState(0, QtCore.Qt.Unchecked)
                        except:
                            pass

    def packageScan(self):
        print(f"Class name: {cls.__name__}")
        print("Methods:")
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        for _, method in methods:
            print(method)

    def analyze_package(package_name):
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            print(f"Error: Package '{package_name}' not found.")
            return

        classes = inspect.getmembers(package, predicate=inspect.isclass)
        functions = inspect.getmembers(package, predicate=inspect.isfunction)

        print(f"Package name: {package_name}\n")
        '''print("Classes:")
        for _, cls in classes:
            print_class_info(cls)

        print("Functions:")
        for _, function in functions:
            print_function_info(function)'''

    def userFriendlyCurrentFile(self):
        return "Friendly Name" #self.strippedName(self.curFile)

    def onPinScan(self):
        packageRoot = Packages.__path__[0]
        self.pinDict = {}
        for root, dirs, files in os.walk(packageRoot, topdown=False):
            for name in files:
                directories = os.path.join(root, name)
                if "Pin.py" in name:
                    PinName = name.replace(".py", "")
                    self.pinDict[PinName] = directories

    @QtCore.Slot(QTreeWidgetItem, int)
    def on_tvPackageItems_clicked(self, it, col):
        QCoreApplication.processEvents()
        parents = []
        current_item = it
        current_parent = current_item.parent()

        # Walk up the tree and collect all parent items of this item
        while not current_parent is None:
            parents.insert(0, current_parent.text(col))
            current_item = current_parent
            current_parent = current_item.parent()

        filefullpath = Packages.__path__[0] + "\\"
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        selecteditem = it.text(col) + ".py"
        filefullpath = os.path.join(filefullpath, selectedpackage)

        for items in parents:
            filefullpath = os.path.join(filefullpath, items)

        filefullpath = os.path.join(filefullpath, selecteditem)

        if filefullpath.find("\\Tools") != -1:

            #todo: check if package level was selected
            deft = it.text(col)
            self.workingFile = filefullpath
            self.initializeform
            self.initializePinData
            filename = filefullpath.split("\\")[-1]

            self.ui.twPackage.setCurrentIndex(1)
            implementdata = ""
            definitiondata = ""
            codedata = ""

            if os.path.exists(filefullpath):
                self.ui.txtCommandFileName.setText(filename)
                self.ui.txtCommandName.setText(deft)
                self.loadToolData(filefullpath)


        if filefullpath.find("\\FunctionLibraries") != -1:
            self.loadAllFunctions()
            #todo: check if package level was selected
            deft = it.text(col)
            self.workingFile = filefullpath
            self.initializeform
            self.initializePinData
            filename = filefullpath.split("\\")[-1]
            self.ui.txtFunctionFileName.setText(filename)
            self.ui.txtFunctionName.setText(deft)

            self.loadAllFunctions()
            implementdata = ""
            definitiondata = ""
            codedata = ""
            self.ui.twPackage.setCurrentIndex(2)

            try:
                for idata in self.functiondict[deft]["Implement"]:
                    implementdata += idata
                self.ui.txtFImplement.setText(implementdata)

                for ddata in self.functiondict[deft]["Definition"]:
                    definitiondata += ddata
                self.ui.txtFDef.setText(definitiondata)

                code = ""
                for codeline in self.functiondict[deft]["Code"]:
                    code += codeline
                self.ui.txtCode.setText(code)

                self.ui.chkPSDraggerSteps.setChecked(False)
                self.ui.txtPSDraggerSteps.setText("")

                if "CATEGORY" in self.functiondict[deft]["MetaData"]:
                    self.ui.txtMetaCategory.setText(self.functiondict[deft]["MetaData"]["CATEGORY"])
                if "KEYWORDS" in self.functiondict[deft]["MetaData"]:
                    self.ui.txtMetaKeywords.setText(self.functiondict[deft]["MetaData"]["KEYWORDS"])
                if "CacheEnabled" in self.functiondict[deft]["MetaData"]:
                    self.ui.chkMetaCacheEnabled.setChecked(self.functiondict[deft]["MetaData"]["CacheEnabled"])

                self.pindefs = self.functiondict[deft]["PinDefs"]

                if deft in self.functiondict:
                    self.loadPinTable(deft)

            except:
                pass

        if filefullpath.find("\\Nodes") != -1:
            deft = it.text(col)
            self.ui.txtNodeFileName.setText(deft)
            self.selectedNodeDataName = deft.replace(".py", "")
            #filefullpath = os.path.join(filefullpath, deft)
            self.loadNodeProperties(filefullpath)
            self.parseNodePins()
            self.ui.twPackage.setCurrentIndex(3)

        if filefullpath.find("\\Pins") != -1:
            self.loadPinProperties(filefullpath)
            print(self.pindict)


        if filefullpath.find("\\SQL") != -1:
            deft = it.text(col)
            self.loadTableProperties(filefullpath)
            self.ui.twPackage.setCurrentIndex(8)


    def onOpenPackageFolder(self):

        #print(Packages.__path__[0] + "\\")
        os.startfile(Packages.__path__[0])
        #subprocess.Popen(r'explorer' + Packages.__path__[0] + "\\")


    def loadFunctionProperties(self, filefullpath, functionname):

        previousitem = ""
        implementdata = ""
        readingimplementdata = -1
        readingdefdata = 0
        defdata = ""
        codedata = []
        eof = 0
        defname = ""
        code = ""
        codedescription = ""
        NestDict = {}
        try:
            filesize = len(open(filefullpath).readlines())
            f = open(filefullpath, "r")

            for index, lineitem in enumerate(f):
                #Reading the parts of the code (Implement, Def, Code)
                if lineitem.find("class") != -1:
                    self.intro = code
                precode = code
                code += lineitem
                codedata.append(lineitem)
                #print(lineitem)
                if lineitem.find("super") != -1:
                    code = ""
                    codedata = []

                if lineitem.find("@staticmethod") != -1 or index == filesize-1:
                    readingdefdata = 0
                    if defname == functionname:
                        if precode.find("@staticmethod") != -1:
                            NestDict = {}
                            implement2 = implementdata
                            NestDict["Implement"] = implement2.replace("@staticmethod", "")
                            NestDict["Definition"] = defdata
                            NestDict["CodeDescription"] = codedescription
                            NestDict["Code"] = codedata[:-1]
                            self.functiondict[functionname] = NestDict

                            self.parseFunctionFile(functionname)
                        break
                    else:
                        implementdata = ""

                if lineitem.find("def ") != -1 and lineitem.find(" " + functionname) != -1:
                    defnamestart = 7
                    defnameend = lineitem.find("(")
                    defname = lineitem[defnamestart + 1:defnameend]
                    readingdefdata = 1

                if readingdefdata == 1:
                    if lineitem.find("def ") != -1:
                        lineitem = lineitem[defnameend+1:]
                    readingimplementdata = 0
                    defdata += lineitem.strip()
                    if defdata[-1] == ":":
                        readingdefdata = 0
                        codedata = []

                if (lineitem.find("@IMPLEMENT_NODE") != -1) or readingimplementdata == 1:
                    implementdata += lineitem.strip()
                    readingimplementdata = 1

                '''if "\'\'\'" in lineitem or "\"\"\"" in lineitem and readingdefdata == 0:
                    codedescription += lineitem[8:]
                else:
                    codedata.append(lineitem[8:])'''
        except:
            pass


    def loadToolData(self, filefullpath):
        codenotes = 0
        importlist = []
        importstart = 0
        classstart = 0
        super = 0
        staticmethod = []
        definition = []
        codedata = []

        filefullpath2 = Packages.__path__[0] + "\\"
        filename = self.ui.txtCommandFileName.text()
        defname = filename[:-3]

        filefullpath2 = os.path.join(filefullpath2, self.ui.txtPackageName.text())
        filefullpath2 = os.path.join(filefullpath2, "Tools")

        self.initToolDict(defname)

        self.tooldict[defname]["Filename"] = defname

        self.tooldict[defname]["Description"] = ""
        self.tooldict[defname]["Category"] = ""
        self.tooldict[defname]["Keywords"] = ""

        self.tooldict[defname]["KeyboardShortCut"] = ""
        self.tooldict[defname]["ResourceFolder"] = ""

        self.ui.cmdCommandAddSmallIcon.setIcon(QIcon())
        self.ui.txtCommandSmallIcon.setText("")
        self.ui.cmdCommandAddMediumIcon.setIcon(QIcon())
        self.ui.cmdCommandAddMediumIcon.setText("")
        self.ui.cmdCommandAddLargeIcon.setIcon(QIcon())
        self.ui.txtCommandLargeIcon.setText("")

        filesize = len(open(filefullpath).readlines())
        f = open(filefullpath, "r")

        for index, lineitem in enumerate(f):
            #Reading the parts of the code (Implement, Def, Code)
            codedata.append(lineitem)

            if lineitem.find("import") != -1:
                importlist.append(index)

            if lineitem.find("class") != -1:
                classstart = index

            if lineitem.find("def") != -1:
                definition.append(index)

        defCount = len(definition)
        for count, defitem in enumerate(definition):
            line = codedata[defitem]
            if count == defCount-1:
                endCodeBlock = len(codedata)
            else:
                endCodeBlock = definition[count+1]-1

            if codedata[defitem - 1].find("@staticmethod") != -1:
                staticmethod = True
            else:
                staticmethod = False

            if codedata[defitem].find("__init__") != -1:
                if codedata[defitem].find("super") != -1:
                    pass

            if codedata[defitem].find("toolTip") != -1:
                for row in range(defitem,endCodeBlock):
                    line2 = codedata[row]
                    if codedata[row].find("return") != -1:
                        tooltip = codedata[row][15:]
                        self.ui.txtCommandToolTip.setText(tooltip[1:-2])
                        self.tooldict[defname]["ToolTip"] = ""

            if codedata[defitem].find("getIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    a = codedata[row]
                    if codedata[row].find("return") != -1:
                        getIcon = codedata[row][15:]
                        #Todo: Load Icon Image to Button
                        parts = getIcon.split("(")
                        icon_path = parts[1][:-1]
                        parts = icon_path.split('"')
                        filename = parts[1]
                        RESOURCES_DIR = os.path.join(filefullpath2, "res")
                        self.ui.cmdCommandAddSmallIcon.setIcon(QtGui.QIcon(os.path.join(RESOURCES_DIR, filename)))
                        self.ui.txtCommandSmallIcon.setText(filename)
                        self.tooldict[defname]["SmallIcon"] = getIcon

            if codedata[defitem].find("getSmallIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getSmallIcon = codedata[row][15:]
                        #self.ui.txtCommandgetIcon.setText(getSmallIcon)
                        # self.ui.cmdCommandCommandAddSmallIcon.setIcon(QtGui.QIcon(getIcon))
                        self.tooldict[defname]["SmallIcon"] = getSmallIcon

            if codedata[defitem].find("getMediumIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getMediumIcon = codedata[row][15:]
                        #self.ui.txtCommandgetIcon.setText(getMediumIcon)
                        # self.ui.cmdAddCommandMediumIcon.setIcon(QtGui.QIcon(getIcon))
                        self.tooldict[defname]["MediumIcon"] = getMediumIcon


            if codedata[defitem].find("getIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getLargeIcon = codedata[row][15:]
                        #self.ui.txtCommandgetIcon.setText(getLargeIcon)
                        # self.ui.cmdCommandAddLargeIcon.setIcon(QtGui.QIcon(getIcon))
                        self.tooldict[defname]["LargeIcon"] = getLargeIcon

            if codedata[defitem].find("keywords") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        keywords = codedata[row][15:]
                        self.ui.txtCommandgetIcon.setText(keywords)
                        self.tooldict[defname]["keywords"] = keywords

            if codedata[defitem].find("keyboardshortcut") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        keywords = codedata[row][15:]
                        self.ui.txtKeyBoardShortcut.setText(keywords)
                        self.tooldict[defname]["keyboardshortcut"] = keywords

            if codedata[defitem].find("name") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        name = codedata[row][15:]
                        parts = name.split('"')
                        self.ui.txtCommandName.setText(parts[1])
                        #Todo: Remove String Data
                        self.tooldict[defname]["Name"] = name

            if codedata[defitem].find("do") != -1:
                code = ""
                for codeline in codedata[defitem:endCodeBlock]:
                    code += codeline
                self.ui.txtCommandCode.setText(code)
                self.tooldict[defname]["PythonCode"] = ""
    @QtCore.Slot()
    def on_cmdCommandAddSmallIcon_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        self.ui.cmdCommandAddSmallIcon.setIcon(QtGui.QIcon(file_path))
        self.ui.txtCommandSmallIcon.setText(os.path.basename(file_path))

    @QtCore.Slot()
    def on_cmdCommandAddMediumIcon_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        self.ui.cmdCommandAddMediumIcon.setIcon(QtGui.QIcon(file_path))
        self.ui.txtCommandMediumIcon.setText(os.path.basename(file_path))

    @QtCore.Slot()
    def on_cmdCommandAddLargeIcon_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        self.ui.cmdCommandAddLargeIcon.setIcon(QtGui.QIcon(file_path))
        self.ui.txtCommandLargeIcon.setText(os.path.basename(file_path))

    def parseFunctionFile(self, defname):
            #https://nedbatchelder.com/text/python-parsers.html
            #Maybe use Code Parser

            '''     Function Dictionary Structure
                    ["Name"]                    - Function Name
                    ["Order"]                   - Order in Appearance
                    ["Meta"]                    - Meta Data
                    ["Inputs"]                  - Pin Input List
                        ["Variable"]            - Input Pin Name
                            ["DataType"]        - Input Pin Data Type
                            ["DefaultValue"]    - Input Pin Default Value
                            ["PinSpecifiers"]   - Input Pin Options
                    ["Outputs"]
                        ["Variable"]            - Output Pin Name
                            ["DataType"]        - Output Pin Data Type
                            ["DefaultValue"]    - Output Pin Default Value
                            ["PinSpecifiers"]   - Output Pin Options
                '''

            implementdata = self.functiondict[defname]["Implement"]

            '''IMPLEMENT_NODE(func=None, returns=(DataType, DefaultValue, PinSpecficiers), meta={NodeMeta.CATEGORY: 'Default', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Pure):'''
            istyle = "kwarg"
            ikeywords = ["func", "returns", "meta"]

            '''PinSpecifires = {PinSpecifires.List: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported, PinSpecifires.Value: "1"}'''
            parseparameters = {"start":"{", "end": "}", "delimination": ","}
            valuetype = {"\"": "Value", "|": "List"}

            '''meta = {NodeMeta.CATEGORY: 'Utils', NodeMeta.KEYWORDS: ['id'], NodeMeta.CACHE_ENABLED: False}'''
            parseparameters = {"start": "{", "end": "}", "delimination": ","}
            valuetype = {"\"": "Value", "[]": "List"}

            defdata = self.functiondict[defname]["Definition"]
            style = "csv"
            pos = ["DataType", "DefaultValue", "PinSpecifiers"]

            codedata = self.functiondict[defname]["Code"]

            implementdata2 = []
            defdata2 = []

            code = ""
            for line, linedata in enumerate(codedata):
                if "staticmethod" not in linedata:
                    if line == 0:
                        output = linedata.replace("\"", "").replace("\'","")[8:]
                        self.ui.txtCodeDescription.setText(output)
                    else:
                        code += linedata[8:]

            self.functiondict[defname]["Code"] = codedata

            #Extracting Information from Implement
            itemdict = {}
            itemdict["FunctionName"] = defname

            idata = {}
            pos = 1

            while pos <= len(implementdata)-1:
                if implementdata[pos] == "=":
                    pos2 = pos
                    while implementdata[pos2] != "(" and implementdata[pos2] != ",":
                        pos2 -= 1
                    variable = implementdata[pos2 + 1:pos].strip()
                    pos3 = pos + 1
                    while implementdata[pos3] != "=" and pos3 != len(implementdata) - 1:
                        pos3 += 1
                    if pos3 != len(implementdata) - 1:
                        pos4 = pos3
                        while implementdata[pos4] != ",":
                            pos4 -= 1
                        settings = implementdata[pos + 1:pos4].strip()
                    else:
                        settings = implementdata[pos + 1:len(implementdata) - 1].strip()
                        pos4 = len(implementdata) - 1
                    idata[variable] = settings.strip()
                    pos = pos4
                pos += 1

            bracketstart = implementdata.find("returns") + len("returns") + 2
            bracketend = bracketstart
            bracketcount = 1
            while bracketend < len(implementdata) and bracketcount != 0:
                if implementdata[bracketend:bracketend + 1] == "(":
                    bracketcount += 1
                if implementdata[bracketend:bracketend + 1] == ")":
                    bracketcount -= 1
                bracketend += 1
            bracketstuff = implementdata[bracketstart:bracketend-1]
            #implementdata = implementdata.replace(bracketstuff,"bracketstuff")

            curlbracketstart = implementdata.find("meta") + len("meta") + 2
            curlbracketend = curlbracketstart
            bracketcount = 1
            metadata = {}

            if curlbracketstart != -1:
                while curlbracketend < len(implementdata) and bracketcount != 0:
                    if implementdata[curlbracketend:curlbracketend + 1] == "{":
                        bracketcount += 1
                    if implementdata[curlbracketend:curlbracketend + 1] == "}":
                        bracketcount -= 1
                    curlbracketend += 1

                metalist = implementdata[curlbracketstart:curlbracketend-1]
                for y in metalist.split(","):
                    itemdata = y.strip().split(":")
                    if itemdata[0] == "NodeMeta.CATEGORY":
                        metadata["CATEGORY"] = itemdata[1].strip()
                        #self.ui.txtMetaCategory.setText(itemdata[1])
                    if itemdata[0] == "NodeMeta.KEYWORDS":
                        metadata["KEYWORDS"] = itemdata[1].strip()
                        #self.ui.txtMetaKeywords.setText(itemdata[1])
                    if itemdata[0] == "NodeMeta.CACHE_ENABLED":
                        metadata["CACHE_ENABLED"] = itemdata[1].strip()
                        #self.ui.chkMetaCacheEnabled.setChecked(itemdata[1])


            self.functiondict[defname]["MetaData"] = metadata
            implementdata2.append(implementdata[:curlbracketstart-6])
            implementdata2.append(implementdata[curlbracketstart-6:curlbracketend - 1] + "})")

            #Definition Item
            defs = {}
            pos = 1
            while pos <= len(defdata)-1:
                if defdata[pos] == "=":
                    pos2 = pos
                    while pos2 != -1 and defdata[pos2] != ",":
                        pos2 -= 1
                    variable = defdata[pos2 + 1:pos].strip()
                    pos3 = pos + 1
                    while defdata[pos3] != "=" and pos3 != len(defdata) - 1:
                        pos3 += 1
                    if pos3 != len(defdata) - 1:
                        pos4 = pos3
                        while defdata[pos4] != ",":
                            pos4 -= 1
                        settings = defdata[pos + 1:pos4].strip()
                    else:
                        settings = defdata[pos + 1:len(defdata) - 1].strip()
                        pos4 = len(defdata) - 1
                    defs[variable] = settings.strip()
                    pos = pos4
                pos += 1

            #Output Pin

            outputpinlistmodel = QtGui.QStandardItemModel(0, 2)
            rowcount = 0
            pinOutCounter = 0
            pindefs = {}
            pindefs["Inputs"] = {}
            pindefs["Outputs"] = {}
            pindata = {}
            data = idata["returns"]

            if data != "None":
                pinOutCounter += 1
                curlbracketstart = data.find("{") + 1
                curlbracketend = curlbracketstart
                bracketcount = 1
                if curlbracketstart != 0:
                    while curlbracketend < len(data) and bracketcount != 0:
                        if data[curlbracketend:curlbracketend + 1] == "{":
                            bracketcount += 1
                        if data[curlbracketend:curlbracketend + 1] == "}":
                            bracketcount -= 1
                        curlbracketend += 1

                    curlystuff3 = data[curlbracketstart:curlbracketend - 1]
                    #data = data.replace(curlystuff3, "curlystuff")
                    pindata = {}
                    for y in curlystuff3.split(","):
                        itemdata = y.strip().split(":")
                        if itemdata[0] == "PinSpecifires.SUPPORTED_DATA_TYPES":
                            pindata["SUPPORTED_DATA_TYPES"] = itemdata[1][1:].strip()
                        if itemdata[0] == "PinSpecifires.CONSTRAINT":
                            pindata["CONSTRAINT"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.STRUCT_CONSTRAINT":
                            pindata["STRUCT_CONSTRAINT"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.ENABLED_OPTIONS":
                            pindata["ENABLED_OPTIONS"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.DISABLED_OPTIONS":
                            pindata["DISABLED_OPTIONS"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.INPUT_WIDGET_VARIANT":
                            pindata["INPUT_WIDGET_VARIANT"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.DESCRIPTION":
                            pindata["DESCRIPTION"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.VALUE_LIST":
                            pindata["VALUE_LIST"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.VALUE_RANGE":
                            pindata["VALUE_RANGE"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.DRAGGER_STEPS":
                            pindata["DRAGGER_STEPS"] = itemdata[1].strip()

                listdata = data.split(",")
                pindata["Name"] = "out"
                pindata["Direction"] = "Out"
                pindata["Order"] = pinOutCounter
                pindata["DataType"] = listdata[0][1:].strip().replace("\"", "").replace("\'", "")
                pindata["DefaultValue"] = listdata[1].strip().replace("))","")
                pindefs["Outputs"]["out"] = pindata

            #InputPin

            rowcount2 = 0

            pindata = {}
            curlystuff3 = None
            PinCounter = 0

            for variable, data in defs.items():
                #print(variable, data)
                PinCounter += 1
                if data.find("REF") == -1:
                    curlbracketstart = data.find("{") + 1
                    curlbracketend = curlbracketstart
                    bracketcount = 1
                    if curlbracketstart != 0:
                        while curlbracketend < len(data) and bracketcount != 0:
                            if data[curlbracketend:curlbracketend + 1] == "{":
                                bracketcount += 1
                            if data[curlbracketend:curlbracketend + 1] == "}":
                                bracketcount -= 1
                            curlbracketend += 1

                        curlystuff3 = data[curlbracketstart:curlbracketend - 1]

                    if curlystuff3 != None: data = data.replace(curlystuff3, "curlystuff")
                    listdata = data.split(",")
                    pindata = {}
                    pindata["Name"] = variable
                    pindata["Direction"] = "In"
                    pindata["Order"] = PinCounter
                    pindata["DataType"] = listdata[0][1:].strip().replace("\"", "").replace("\'", "")
                    if len(listdata) >= 2:
                        pindata["DefaultValue"] = listdata[1].strip()

                    if curlystuff3 is not None:
                        for y in curlystuff3.split(","):
                            itemdata = y.strip().split(":")
                            if itemdata[0] == "PinSpecifires.SUPPORTED_DATA_TYPES":
                                pindata["SUPPORTED_DATA_TYPES"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.CONSTRAINT":
                                pindata["CONSTRAINT"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.STRUCT_CONSTRAINT":
                                pindata["STRUCT_CONSTRAINT"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.ENABLED_OPTIONS":
                                pindata["ENABLED_OPTIONS"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.DISABLED_OPTIONS":
                                pindata["DISABLED_OPTIONS"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.INPUT_WIDGET_VARIANT":
                                pindata["INPUT_WIDGET_VARIANT"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.DESCRIPTION":
                                pindata["DESCRIPTION"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.VALUE_LIST":
                                pindata["VALUE_LIST"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.VALUE_RANGE":
                                pindata["VALUE_RANGE"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.DRAGGER_STEPS":
                                pindata["DRAGGER_STEPS"] = itemdata[1].strip()

                    pindefs["Inputs"][variable] = pindata

                    rowcount2 += 1
                else:
                    pinOutCounter += 1
                    startvalue = data.find("\"")
                    if startvalue == -1:
                        startvalue = data.find("\'")

                    endvalue = data.find(")")
                    pindata = {}
                    pindata["Name"] = variable
                    pindata["Direction"] = "Out"
                    pindata["Order"] = pinOutCounter

                    listdata = data[startvalue:endvalue].split(",")
                    pindata["DataType"] = listdata[0].strip().replace("\"", "").replace("\'", "")

                    if len(listdata) >= 2: pindata["DefaultValue"] = listdata[1].strip()

                    pindefs["Outputs"][variable] = pindata

                    rowcount += 1

            self.functiondict[defname]["PinDefs"] = pindefs

            self.functiondict[defname]["Implement"] = implementdata2

            for variable, data in defs.items():
                defdata2.append(variable + "=" + data)

            self.functiondict[defname]["Definition"] = defdata2

    def loadPinTable(self, defname):
        # InputPin
        pindatatypemodel = QtGui.QStandardItemModel(0, 2)
        for index, key in enumerate(self.pinDict):
            pindatatypemodel.setItem(index, 0, QtGui.QStandardItem(str(index)))
            pindatatypemodel.setItem(index, 1, QtGui.QStandardItem(key))

        if "PinDefs" in self.functiondict[defname]:
            inputpinlistmodel = QtGui.QStandardItemModel(0, 2)
            inputPinList = []
            if "Inputs" in self.functiondict[defname]["PinDefs"]:
                for pindata in self.functiondict[defname]["PinDefs"]["Inputs"]:
                    row = int(self.functiondict[defname]["PinDefs"]["Inputs"][pindata]["Order"]) - 1
                    inputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))
                    DataTypeValue = ""
                    if "DataType" in self.functiondict[defname]["PinDefs"]["Inputs"][pindata]:
                        inputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(self.functiondict[defname]["PinDefs"]["Inputs"][pindata]["DataType"]))
                        DataTypeValue = self.functiondict[defname]["PinDefs"]["Inputs"][pindata]["DataType"]
                    inputPinList.append(DataTypeValue)
                    if "DefaultValue" in self.functiondict[defname]["PinDefs"]["Inputs"][pindata]:
                        inputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(self.functiondict[defname]["PinDefs"]["Inputs"][pindata]["DefaultValue"]))

                inputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                inputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                inputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            outputPinList = []
            if "Outputs" in self.functiondict[defname]["PinDefs"]:
                outputpinlistmodel = QtGui.QStandardItemModel(0, 2)
                for rowcount2, pindata in enumerate(self.functiondict[defname]["PinDefs"]["Outputs"]):
                    row = int(self.functiondict[defname]["PinDefs"]["Outputs"][pindata]["Order"]) - 1
                    DataTypeValue = ""
                    if rowcount2 == 0:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem("out"))
                    else:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))

                    if "DataType" in self.functiondict[defname]["PinDefs"]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(self.functiondict[defname]["PinDefs"]["Outputs"][pindata]["DataType"]))
                        DataTypeValue = self.functiondict[defname]["PinDefs"]["Outputs"][pindata]["DataType"]
                    outputPinList.append(DataTypeValue)

                    if "DefaultValue" in self.functiondict[defname]["PinDefs"]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(self.functiondict[defname]["PinDefs"]["Outputs"][pindata]["DefaultValue"]))

                outputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            self.ui.tblFInputPins.setModel(inputpinlistmodel)
            self.ui.tblFOutputPins.setModel(outputpinlistmodel)

            if "Inputs" in self.functiondict[defname]["PinDefs"]:
                for row, data in enumerate(self.functiondict[defname]["PinDefs"]["Inputs"]):
                    self.ui.tblFInputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                    c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)
                    c.setValue(self.functiondict[defname]["PinDefs"]["Inputs"][data]["DataType"], 1)
                    i = self.ui.tblFInputPins.model().index(row, 1)
                    #c.currentIndexChanged2[dict].connect(self.on_lstPinSettings_cmbTableChanged)
                    self.ui.tblFInputPins.setIndexWidget(i, c)

            if "Outputs" in self.functiondict[defname]["PinDefs"]:
                for row, data in enumerate(self.functiondict[defname]["PinDefs"]["Outputs"]):
                    self.ui.tblFOutputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                    c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)
                    c.setValue(self.functiondict[defname]["PinDefs"]["Outputs"][data]["DataType"], 1)
                    i = self.ui.tblFOutputPins.model().index(row, 1)
                    #c.currentIndexChanged2[dict].connect(self.on_lstTableSettings_cmbTableChanged)
                    self.ui.tblFOutputPins.setIndexWidget(i, c)

            #self.ui.tblFInputPins.resizeColumnsToContents()
            #self.ui.tblFOutputPins.resizeColumnsToContents()

            #self.ui.tblFInputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))
            #self.ui.tblFOutputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))

            self.initializePinData()

            '''for z in curlystuff2.split(","):
                itemdata = z.strip().split(":")
                #print(itemdata[0], itemdata[1].strip())'''

    def on_lstPinSettings_cmbTableChanged(self, int):
        print(int)

    def initializeform(self):

        self.ui.txtFunctionFileName.setText("")
        self.ui.txtFunctionName.setText("")
        #self.ui.tblFInputPins
        #self.ui.tblFOutputPins
        self.ui.txtFImplement.setText("")
        self.ui.txtFDef.setText("")
        self.ui.txtCodeDescription.setText("")
        self.ui.txtCode.setText("")

        self.ui.txtMetaCategory.setText("")
        self.ui.txtMetaKeywords.setText("")
        self.ui.chkMetaCacheEnabled.setChecked(False)

    def blockPinSignals(self):
        self.ui.chkPSSupportedDataTypes.blockSignals(True)
        self.ui.chkPSSupportedDataTypes.blockSignals(True)
        self.ui.txtPSSupportedDataTypes.blockSignals(True)
        self.ui.chkPSConstraint.blockSignals(True)
        self.ui.txtPSConstraint.blockSignals(True)
        self.ui.chkPSStructConstraint.blockSignals(True)
        self.ui.txtPSStructConstraint.blockSignals(True)
        #self.ui.chkPSEnableOptions.blockSignals(True)
        #self.ui.txtPSEnableOptions.blockSignals(True)
        self.ui.chkPSDisableOptions.blockSignals(True)
        self.ui.txtPSDisableOptions.blockSignals(True)
        self.ui.chkPSInputWidget.blockSignals(True)
        self.ui.txtPSInputWidget.blockSignals(True)
        self.ui.chkPSDescription.blockSignals(True)
        self.ui.txtPSDescription.blockSignals(True)
        self.ui.chkPSValueList.blockSignals(True)
        self.ui.txtPSValueList.blockSignals(True)
        self.ui.chkPSValueRange.blockSignals(True)
        self.ui.txtPSValueRange.blockSignals(True)
        self.ui.chkPSDraggerSteps.setChecked(False)
        self.ui.txtPSDraggerSteps.blockSignals(True)

        self.ui.chkArraySupported.blockSignals(True)
        self.ui.chkDictionarySupported.blockSignals(True)
        self.ui.chkSupportOnlyArrays.blockSignals(True)
        self.ui.chkAllowMultipleConnections.blockSignals(True)
        self.ui.chkChangeTypeOnConnection.blockSignals(True)
        self.ui.chkRenamingEnabled.blockSignals(True)
        self.ui.chkDynamic.blockSignals(True)
        self.ui.chkAlwaysPushDirty.blockSignals(True)
        self.ui.chkStorable.blockSignals(True)
        self.ui.chkAllowAny.blockSignals(True)
        self.ui.chkDictionaryElementSupported.blockSignals(True)

    def unblockPinSignals(self):
        self.ui.chkPSSupportedDataTypes.blockSignals(False)
        self.ui.txtPSSupportedDataTypes.blockSignals(False)
        self.ui.chkPSConstraint.blockSignals(False)
        self.ui.txtPSConstraint.blockSignals(False)
        self.ui.chkPSStructConstraint.blockSignals(False)
        self.ui.txtPSStructConstraint.blockSignals(False)
        #self.ui.chkPSEnableOptions.blockSignals(False)
        #self.ui.txtPSEnableOptions.blockSignals(False)
        self.ui.chkPSDisableOptions.blockSignals(False)
        self.ui.txtPSDisableOptions.blockSignals(False)
        self.ui.chkPSInputWidget.blockSignals(False)
        self.ui.txtPSInputWidget.blockSignals(False)
        self.ui.chkPSDescription.blockSignals(False)
        self.ui.txtPSDescription.blockSignals(False)
        self.ui.chkPSValueList.blockSignals(False)
        self.ui.txtPSValueList.blockSignals(False)
        self.ui.chkPSValueRange.blockSignals(False)
        self.ui.txtPSValueRange.blockSignals(False)
        self.ui.chkPSDraggerSteps.setChecked(False)
        self.ui.txtPSDraggerSteps.blockSignals(False)

        self.ui.chkArraySupported.blockSignals(False)
        self.ui.chkDictionarySupported.blockSignals(False)
        self.ui.chkSupportOnlyArrays.blockSignals(False)
        self.ui.chkAllowMultipleConnections.blockSignals(False)
        self.ui.chkChangeTypeOnConnection.blockSignals(False)
        self.ui.chkRenamingEnabled.blockSignals(False)
        self.ui.chkDynamic.blockSignals(False)
        self.ui.chkAlwaysPushDirty.blockSignals(False)
        self.ui.chkStorable.blockSignals(False)
        self.ui.chkAllowAny.blockSignals(False)
        self.ui.chkDictionaryElementSupported.blockSignals(False)

    def initializePinData(self):
        self.blockPinSignals()
        self.ui.chkPSSupportedDataTypes.setChecked(False)
        self.ui.txtPSSupportedDataTypes.setText("")
        self.ui.chkPSConstraint.setChecked(False)
        self.ui.txtPSConstraint.setText("")
        self.ui.chkPSStructConstraint.setChecked(False)
        self.ui.txtPSStructConstraint.setText("")
        #self.ui.chkPSEnableOptions.setChecked(False)
        #self.ui.txtPSEnableOptions.setText("")
        self.ui.chkPSDisableOptions.setChecked(False)
        self.ui.txtPSDisableOptions.setText("")
        self.ui.chkPSInputWidget.setChecked(False)
        self.ui.txtPSInputWidget.setText("")
        self.ui.chkPSDescription.setChecked(False)
        self.ui.txtPSDescription.setText("")
        self.ui.chkPSValueList.setChecked(False)
        self.ui.txtPSValueList.setText("")
        self.ui.chkPSValueRange.setChecked(False)
        self.ui.txtPSValueRange.setText("")
        self.ui.chkPSDraggerSteps.setChecked(False)
        self.ui.txtPSDraggerSteps.setText("")

        self.ui.chkArraySupported.setChecked(False)
        self.ui.chkDictionarySupported.setChecked(False)
        self.ui.chkSupportOnlyArrays.setChecked(False)
        self.ui.chkAllowMultipleConnections.setChecked(False)
        self.ui.chkChangeTypeOnConnection.setChecked(False)
        self.ui.chkRenamingEnabled.setChecked(False)
        self.ui.chkDynamic.setChecked(False)
        self.ui.chkAlwaysPushDirty.setChecked(False)
        self.ui.chkStorable.setChecked(False)
        self.ui.chkAllowAny.setChecked(False)
        self.ui.chkDictionaryElementSupported.setChecked(False)
        self.unblockPinSignals()

    def writepindata(self):
        self.functiondict = {}

    #@QtCore.pyqtSlot(int)
    def on_chkPSSupportedDataTypes_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["SUPPORTED_DATA_TYPES"] = self.ui.txtPSSupportedDataTypes.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSSupportedDataTypes_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["SUPPORTED_DATA_TYPES"] = self.ui.txtPSSupportedDataTypes.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSConstraint_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["CONSTRAINT"] = self.ui.txtPSConstraint.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSConstraint_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["CONSTRAINT"] = self.ui.txtPSConstraint.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSStructConstraint_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["STRUCT_CONSTRAINT"] = self.ui.txtPSStructConstraint.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSStructConstraint_stateChanged(self):
        a = self.ui.txtPSStructConstraint.text()
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["STRUCT_CONSTRAINT"] = self.ui.txtPSStructConstraint.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSDisableOptions_stateChanged(self):
        a = self.ui.chkPSDisableOptions.isChecked()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.setFunctionDirty()

    #@QtCore.pyqtSlot(str)
    def on_txtPSDisableOptions_textChanged(self):
        b = self.ui.txtPSDisableOptions.text()
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)

    #@QtCore.pyqtSlot(int)
    def on_chkPSInputWidget_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["INPUT_WIDGET_VARIANT"] = self.ui.txtPSInputWidget.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSInputWidget_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["INPUT_WIDGET_VARIANT"] = self.ui.txtPSInputWidget.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSDescription_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DESCRIPTION"] = self.ui.txtPSDescription.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSDescription_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DESCRIPTION"] = self.ui.txtPSDescription.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSValueList_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_LIST"] = self.ui.txtPSValueList.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSValueList_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_LIST"] = self.ui.txtPSValueList.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSValueRange_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_RANGE"] = self.ui.txtPSValueRange.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSValueRange_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_RANGE"] = self.ui.txtPSValueRange.text()

    #@QtCore.pyqtSlot(int)
    def on_chkPSDraggerSteps_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DRAGGER_STEPS"] = self.ui.txtPSDraggerSteps.text()

    #@QtCore.pyqtSlot(str)
    def on_txtPSDraggerSteps_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DRAGGER_STEPS"] = self.ui.txtPSDraggerSteps.text()

    #@QtCore.pyqtSlot(int)
    def on_chkArraySupported_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["ArraySupported"] = self.ui.chkArraySupported.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkDictionarySupported_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DictSupported"] = self.ui.chkDictionarySupported.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkSupportOnlyArrays_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["SupportsOnlyArrays"] = self.ui.chkSupportOnlyArrays.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkAllowMultipleConnections_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["AllowMultipleConnections"] = self.ui.chkAllowMultipleConnections.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkChangeTypeOnConnection_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["ChangeTypeOnConnection"] = self.ui.chkChangeTypeOnConnection.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkRenamingEnabled_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["RenamingEnabled"] = self.ui.chkRenamingEnabled.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkDynamic_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["Dynamic"] = self.ui.chkDynamic.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkAlwaysPushDirty_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["AlwaysPushDirty"] = self.ui.chkAlwaysPushDirty.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkStorable_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["Storable"] = self.ui.chkStorable.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkAllowAny_stateChanged(self, value):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["AllowAny"] = self.ui.chkAllowAny.isChecked()

    #@QtCore.pyqtSlot(int)
    def on_chkDictionaryElementSupported_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DictElementSupported"] = self.ui.chkDictionaryElementSupported.isChecked()

    def pinDictCheck(self, Direction, PinName):
        if Direction not in self.pindefs:
            self.pindefs[Direction] = {}

        if PinName not in self.pindefs["Inputs"] and PinName not in self.pindefs["Outputs"]:
            self.pindefs[Direction][PinName] = {}
            return(True)
        else:
            return(False)

    #@QtCore.pyqtSlot()
    def on_cmdUpOrderFInputPin_clicked(self):
        order = self.pindefs["Inputs"][self.selectedPinName]["Order"]

        if order > 1:
            for key, data in self.pindefs["Inputs"].items():
                if data["Order"] == order - 1:
                    data["Order"] += 1
                    self.pindefs["Inputs"][self.selectedPinName]["Order"] -= 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdDownOrderFInputPin_clicked(self):
        order = self.pindefs["Inputs"][self.selectedPinName]["Order"]

        if order < len(self.pindefs["Inputs"]):
            for key, data in self.pindefs["Inputs"].items():
                if data["Order"] == order + 1:
                    data["Order"] -= 1
                    self.pindefs["Inputs"][self.selectedPinName]["Order"] += 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdAddFInputPin_clicked(self):
        self.setFunctionDirty()
        if self.ui.txtFunctionName.text() != "":

            newPinName = "NewPinName"
            pinnum = ""
            counter = 0
            while not self.pinDictCheck("Inputs", newPinName + pinnum):
                counter += 1
                pinnum = "_" + str(counter)

            newPinName = newPinName + pinnum

            self.pindefs["Inputs"][newPinName]["DataType"] = 'AnyPin'
            self.pindefs["Inputs"][newPinName]["DefaultValue"] = 'None'
            self.pindefs["Inputs"][newPinName]["Order"] = len(self.pindefs["Inputs"])
            self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdRemoveFInputPin_clicked(self):
        self.setFunctionDirty()
        order = self.pindefs["Inputs"][self.selectedPinName]["Order"]
        self.pindefs["Inputs"].pop(self.selectedPinName)
        for key, data in self.pindefs["Inputs"].items():
            if data["Order"] > order:
                data["Order"] -= 1
        self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdUpOrderFOutputPin_clicked(self):
        order = self.pindefs["Outputs"][self.selectedPinName]["Order"]

        if order > 1:
            for key, data in self.pindefs["Outputs"].items():
                if data["Order"] == order - 1:
                    data["Order"] += 1
                    self.pindefs["Outputs"][self.selectedPinName]["Order"] -= 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdDownOrderFOutputPin_clicked(self):
        order = self.pindefs["Outputs"][self.selectedPinName]["Order"]

        if order < len(self.pindefs["Outputs"]):
            for key, data in self.pindefs["Outputs"].items():
                if data["Order"] == order + 1:
                    data["Order"] -= 1
                    self.pindefs["Outputs"][self.selectedPinName]["Order"] += 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdAddFOutputPin_clicked(self):
        self.setFunctionDirty()
        if self.ui.txtFunctionName.text() != "":
            newPinName = "NewPinName"
            pinnum = ""
            counter = 0
            while not self.pinDictCheck("Outputs", newPinName + pinnum):
                counter += 1
                pinnum = "_" + str(counter)

            newPinName = newPinName + pinnum

            self.pinDictCheck("Outputs", "NewPinName")
            self.pindefs["Outputs"][newPinName]["DataType"] = 'AnyPin'
            self.pindefs["Outputs"][newPinName]["DefaultValue"] = 'None'
            self.pindefs["Outputs"][newPinName]["Order"] = len(self.pindefs["Outputs"])
            self.loadPinTable(self.ui.txtFunctionName.text())

    #@QtCore.pyqtSlot()
    def on_cmdRemoveFOutputPin_clicked(self):
        self.setFunctionDirty()
        order = self.pindefs["Outputs"][self.selectedPinName]["Order"]
        self.pindefs["Outputs"].pop(self.selectedPinName)
        for key, data in self.pindefs["Outputs"].items():
            if data["Order"] > order:
                data["Order"] -= 1
        self.loadPinTable(self.ui.txtFunctionName.text())


    def setFunctionDirty(self):
        self.ui.cmdSaveFunction.setEnabled(True)
        self.ui.cmdSaveFunction.setVisible(True)
        self.ui.cmdSaveFunction.setStyleSheet("background-color: red")

    #@QtCore.pyqtSlot()
    def on_cmdSaveFunction_clicked(self):
        self.ui.cmdSaveFunction.setEnabled(False)
        self.ui.cmdSaveFunction.setVisible(False)
        self.writeFunction()
        self.writeFile()

    #@QtCore.pyqtSlot()
    def on_cmdCreateNewFunction_clicked(self):
        functionName = self.ui.txtFunctionName.text()
        if functionName not in self.functiondict:

            self.setFunctionDirty()
            self.functiondict[functionName] = {}

            self.functiondict[functionName]["PinDefs"] = {}
            self.functiondict[functionName]["Implement"] = {}
            self.functiondict[functionName]["Definition"] = {}
            self.functiondict[functionName]["MetaData"] = {}
            self.functiondict[functionName]["Code"] = ["Pass"]

            #self.initializeform
            self.initializePinData

            #self.loadAllFunctions()
            #self.loadPinTable(deft)
        else:
            print("Function Name Taken")

    def renamePin(self, mydict, old_key, new_key):
        mydict[new_key] = mydict.pop(old_key)

    def loadAllFunctions(self):
        try:
            f = open(self.workingFile, "r")
            for lineitem in f:
                if lineitem.find("def ") != -1:
                    if lineitem[8] != "_":
                        classnamestart = 7
                        classnameend = lineitem.find("(")
                        if self.workingFile.find(lineitem[classnamestart+1:classnameend]) == -1:
                            functionname = lineitem[classnamestart+1:classnameend]
                            self.functiondict[functionname] = {}
                            self.loadFunctionProperties(self.workingFile, functionname)
        except:
            pass

    def initToolDict(self, defname):
        tooldict = {}
        tooldict["Author"] = ""
        tooldict["CopyrightYear"] = ""
        tooldict["RevisionHistory"] = ""
        tooldict["Filename"] = ""
        tooldict["Name"] = ""
        tooldict["Description"] = ""
        tooldict["Category"] = ""
        tooldict["Keywords"] = ""
        tooldict["ToolTip"] = ""
        tooldict["KeyboardShortCut"] = ""
        tooldict["SmallIcon"] = ""
        tooldict["MediumIcon"] = ""
        tooldict["LargeIcon"] = ""
        tooldict["ResourceFolder"] = ""
        tooldict["PythonCode"] = ""
        tooldict["PyflowFile"] = ""

        self.tooldict[defname] = tooldict
    @QtCore.Slot()
    def on_cmdSaveCommand_clicked(self):
        filename = self.ui.txtCommandFileName.text()
        # Write File
        fname = filename
        filefullpath = Packages.__path__[0] + "\\"
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        filefullpath = os.path.join(filefullpath, selectedpackage)
        filefullpath = os.path.join(filefullpath, "Tools")
        filefullpath = os.path.join(filefullpath, fname)

        Filename = filename.split(".")[0]
        classline = "class %s(ShelfTool):\n" % (Filename)
        classline += "#doc string\n\n"
        classline += "    def __init__(self):\n"
        classline += "        super(%s, self).__init__()\n" % (Filename)

        with open(filefullpath, 'w') as f:
            self.addCopyright(f)
            # TODO add the prestuff
            # Revision History

            f.write("from PyFlow.UI.Tool.Tool import ShelfTool\n")
            f.write("from PyFlow.Core.Common import Direction\n")
            f.write("from qtpy import QtGui\n")
            f.write("from PyFlow.Packages.%s.Tools import RESOURCES_DIR\n\n" % (selectedpackage))

            f.write(classline)
            for variable, code in self.tooldict.items():
                if code != {}:
                    if variable != "do":
                        f.write("    @staticmethod\n")
                    f.write("    " + "def " + variable + "():\n")
                    f.write("       " + "return " + code["Code"] + ":\n")

    def writeFunction(self):

        defname = self.ui.txtFunctionName.text()
        implementdata = []
        defindata = []
        defoutdata = []

        print("Pin Def", self.pindefs)
        idata = "@IMPLEMENT_NODE(returns=("
        # @IMPLEMENT_NODE(returns=('AnyPin', None, {
        outCounter = 0
        if "out" in self.pindefs["Outputs"]:
            data = self.pindefs["Outputs"]["out"]
            idata += "\'" + data["DataType"].strip() + "\'"
            if data["DefaultValue"] is not None:
                idata += ", " + data["DefaultValue"]
            else:
                idata += ", None"

            pinspecifiers = ""
            if "SUPPORTED_DATA_TYPES" in data:
                pinspecifiers += "PinSpecifires.SUPPORTED_DATA_TYPES: " + data["SUPPORTED_DATA_TYPES"] + ", "
            if "CONSTRAINT" in data:
                pinspecifiers += "PinSpecifires.CONSTRAINT: " + data["CONSTRAINT"] + ", "
            if "STRUCT_CONSTRAINT" in data:
                pinspecifiers += "PinSpecifires.STRUCT_CONSTRAINT: " + data["STRUCT_CONSTRAINT"] + ", "
            if "ENABLED_OPTIONS" in data:
                pinspecifiers += "PinSpecifires.ENABLED_OPTIONS: " + data["ENABLED_OPTIONS"] + ", "
            if "DISABLED_OPTIONS" in data:
                pinspecifiers += "PinSpecifires.DISABLED_OPTIONS: " + data["DISABLED_OPTIONS"] + ", "
            if "INPUT_WIDGET_VARIANT" in data:
                pinspecifiers += "PinSpecifires.INPUT_WIDGET_VARIANT: " + data["INPUT_WIDGET_VARIANT"] + ", "
            if "DESCRIPTION" in data:
                pinspecifiers += "PinSpecifires.DESCRIPTION: \'" + data["DESCRIPTION"] + "\', "
            if "VALUE_LIST" in data:
                pinspecifiers += "PinSpecifires.VALUE_LIST: " + data["VALUE_LIST"] + ", "
            if "VALUE_RANGE" in data:
                pinspecifiers += "PinSpecifires.VALUE_RANGE: " + data["VALUE_RANGE"] + ", "
            if "DRAGGER_STEPS" in data:
                pinspecifiers += "PinSpecifires.DRAGGER_STEPS: " + data["DRAGGER_STEPS"] + ", "
            if pinspecifiers != "":
                idata += ", {" + pinspecifiers[:-2] + "})"

            idata += ", "

        implementdata.append(idata)
        mdata = ""
        if "CATEGORY" in self.functiondict[defname]["MetaData"]:
            mdata += "NodeMeta.CATEGORY: " + self.functiondict[defname]["MetaData"]["CATEGORY"] + ", "
        if "KEYWORDS" in self.functiondict[defname]["MetaData"]:
            mdata += "NodeMeta.KEYWORDS: " + self.functiondict[defname]["MetaData"]["KEYWORDS"] + ", "
        if "CACHE_ENABLED" in self.functiondict[defname]["MetaData"]:
            mdata += "NodeMeta.CACHE_ENABLED: " + self.functiondict[defname]["MetaData"]["CACHE_ENABLED"] + ", "

        implementdata.append("meta={" + mdata[:-2] + "})")

        for pin, data in self.pindefs["Inputs"].items():

            didata = pin + "=("
            didata += "\'" + data["DataType"].strip() + "\'"
            if data["DefaultValue"] is not None:
                didata += ", " + data["DefaultValue"]
            else:
                didata += ", None"

            pinspecifiers = ""
            if "SUPPORTED_DATA_TYPES" in data:
                pinspecifiers += "PinSpecifires.SUPPORTED_DATA_TYPES: " + data["SUPPORTED_DATA_TYPES"] + ", "
            if "CONSTRAINT" in data:
                pinspecifiers += "PinSpecifires.CONSTRAINT: " + data["CONSTRAINT"] + ", "
            if "STRUCT_CONSTRAINT" in data:
                pinspecifiers += "PinSpecifires.STRUCT_CONSTRAINT: " + data["STRUCT_CONSTRAINT"] + ", "
            if "ENABLED_OPTIONS" in data:
                pinspecifiers += "PinSpecifires.ENABLED_OPTIONS: " + data["ENABLED_OPTIONS"] + ", "
            if "DISABLED_OPTIONS" in data:
                pinspecifiers += "PinSpecifires.DISABLED_OPTIONS: " + data["DISABLED_OPTIONS"] + ", "
            if "INPUT_WIDGET_VARIANT" in data:
                pinspecifiers += "PinSpecifires.INPUT_WIDGET_VARIANT: " + data["INPUT_WIDGET_VARIANT"] + ", "
            if "DESCRIPTION" in data:
                pinspecifiers += "PinSpecifires.DESCRIPTION: " + data["DESCRIPTION"] + ", "
            if "VALUE_LIST" in data:
                pinspecifiers += "PinSpecifires.VALUE_LIST: " + data["VALUE_LIST"] + ", "
            if "VALUE_RANGE" in data:
                pinspecifiers += "PinSpecifires.VALUE_RANGE: " + data["VALUE_RANGE"] + ", "
            if "DRAGGER_STEPS" in data:
                pinspecifiers += "PinSpecifires.DRAGGER_STEPS: " + data["DRAGGER_STEPS"] + ", "
            if pinspecifiers != "":
                didata += ", {" + pinspecifiers[:-2] + "}"

            didata += ")"
            defindata.append(didata)

        outCounter = -1
        for pin, data in self.pindefs["Outputs"].items():
            ddata = ""
            outCounter += 1
            if outCounter != 0:
                ddata += pin + "=("
                ddata += "REF, ("

                ddata += "\'" + data["DataType"].strip() + "\'"
                if data["DefaultValue"] is not None:
                    ddata += ", " + data["DefaultValue"]
                else:
                    ddata += ", None"

                pinspecifiers = ""
                if "SUPPORTED_DATA_TYPES" in data:
                    pinspecifiers += "PinSpecifires.SUPPORTED_DATA_TYPES: " + data["SUPPORTED_DATA_TYPES"] + ", "
                if "CONSTRAINT" in data:
                    pinspecifiers += "PinSpecifires.CONSTRAINT: " + data["CONSTRAINT"] + ", "
                if "STRUCT_CONSTRAINT" in data:
                    pinspecifiers += "PinSpecifires.STRUCT_CONSTRAINT: " + data["STRUCT_CONSTRAINT"] + ", "
                if "ENABLED_OPTIONS" in data:
                    pinspecifiers += "PinSpecifires.ENABLED_OPTIONS: " + data["ENABLED_OPTIONS"] + ", "
                if "DISABLED_OPTIONS" in data:
                    pinspecifiers += "PinSpecifires.DISABLED_OPTIONS: " + data["DISABLED_OPTIONS"] + ", "
                if "INPUT_WIDGET_VARIANT" in data:
                    pinspecifiers += "PinSpecifires.INPUT_WIDGET_VARIANT: " + data["INPUT_WIDGET_VARIANT"] + ", "
                if "DESCRIPTION" in data:
                    pinspecifiers += "PinSpecifires.DESCRIPTION: " +  "\'" + data["DESCRIPTION"] + "\', "
                if "VALUE_LIST" in data:
                    pinspecifiers += "PinSpecifires.VALUE_LIST: " + data["VALUE_LIST"] + ", "
                if "VALUE_RANGE" in data:
                    pinspecifiers += "PinSpecifires.VALUE_RANGE: " + data["VALUE_RANGE"] + ", "
                if "DRAGGER_STEPS" in data:
                    pinspecifiers += "PinSpecifires.DRAGGER_STEPS: " + data["DRAGGER_STEPS"] + ", "
                if pinspecifiers != "":
                    ddata += ", {" + pinspecifiers[:-2] + "}"

                if outCounter == len(self.pindefs["Outputs"]) - 1:
                    ddata = ddata + ")))"
                else:
                    ddata += "))"

                defoutdata.append(ddata)

        self.functiondict[defname]["Implement"] = implementdata
        self.functiondict[defname]["Definition"] = defindata + defoutdata

    def writeFile(self):
        # Write Code
        filename = self.ui.txtFunctionFileName.text()
        # Write File
        '''wizardfile = Wizards.__path__[0] + "\\"
        filefullpath = os.path.join(wizardfile, "FunctionHeader.txt")
        codestart = ""

        f = open(filefullpath, "r")
        for lineitem in f:
            codestart += lineitem'''

        fname = filename
        filefullpath = Packages.__path__[0] + "\\"
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        filefullpath = os.path.join(filefullpath, selectedpackage)
        filefullpath = os.path.join(filefullpath, "FunctionLibraries")
        filefullpath = os.path.join(filefullpath, fname)

        Filename = filename.split(".")[0]
        classline = "class %s(FunctionLibraryBase):\n" % (Filename)
        classline += "#doc string\n\n"
        classline += "    def __init__(self, packageName):\n"
        classline += "        super(%s, self).__init__(packageName)\n" % (Filename)

        with open(filefullpath, 'w') as f:
            f.write(self.intro)
            f.write(classline)
            for variable, code in self.functiondict.items():
                if code != {}:
                    f.write("    @staticmethod\n")
                    for iitems in code["Implement"]:

                        if "meta" in iitems:
                            if len(iitems["meta"]):
                                f.write("                    " + iitems + "\n")
                            else:
                                f.write("    " + iitems + "\n")
                    if code["Definition"] == []:
                        f.write("    " + "def " + variable + "():\n")
                    else:
                        for row, ditems in enumerate(code["Definition"]):
                            if row == len(code["Definition"])-1:
                                defend = ":"
                            else:
                                defend = ", "

                            if row == 0:
                                f.write("    " + "def " + variable + "("+ ditems + defend + "\n")
                            else:
                                f.write("                 " + ditems + defend + "\n")

                    #f.write(code["CodeDescription"])
                    for codeline in code["Code"]:
                        f.write(codeline)

        print("Done")


    def on_tblFInputPins_Changed(self, index):
        print("changed")
        row = self.ui.tblFInputPins.selectionModel().currentIndex().row()
        column = self.ui.tblFInputPins.selectionModel().currentIndex().column()
        value = self.ui.tblFInputPins.selectionModel().currentIndex().data(0)
        print("IP On Change", row, column, value)

    def on_tblFInputPins_clicked(self, index):
        '''print(index)
        print("Click", self.ui.tblFInputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.ui.tblFInputPins.model().data(index, QtCore.Qt.UserRole))'''
        #self.ReferenceNumber_id = self.ui.tblFInputPins.model().index(index.row(), 0).data()

        self.selectedPinDir = "Inputs"
        self.selectedPinName = self.ui.tblFInputPins.model().index(index.row(), 0).data()

        if self.selectedPinName in self.pindefs[self.selectedPinDir]:
            self.selectedPinData = self.pindefs[self.selectedPinDir][self.selectedPinName]
            self.loadPinData(self.selectedPinData)

    def on_tblFInputPins_doubleclicked(self, index):
        print("Double Click", self.ui.tblFInputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.ui.tblFInputPins.model().data(index, QtCore.Qt.UserRole))

    def on_tblFOutputPins_Changed(self, index):
        row = self.ui.tblFOutputPins.selectionModel().currentIndex().row()
        column = self.ui.tblFOutputPins.selectionModel().currentIndex().column()
        value = self.ui.tblFOutputPins.selectionModel().currentIndex().data(0)
        print("IP On Change", row, column, value)

    def on_tblFOutputPins_clicked(self, index):
        print("Click", self.ui.tblFOutputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.ui.tblFOutputPins.model().data(index, QtCore.Qt.UserRole))
        self.ReferenceNumber_id = self.ui.tblFOutputPins.model().index(index.row(), 0).data()
        #self.loadProjectdata()

        self.selectedPinDir = "Outputs"
        self.selectedPinName = self.ui.tblFOutputPins.model().index(index.row(), 0).data()

        if self.selectedPinName in self.pindefs[self.selectedPinDir]:
            self.selectedPinData = self.pindefs[self.selectedPinDir][self.selectedPinName]
            self.loadPinData(self.selectedPinData)

    def on_tblFOutputPins_doubleclicked(self, index):
        print("Double Click", self.tblFOutputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.tblFOutputPins.model().data(index, QtCore.Qt.UserRole))

    def loadPinData(self, data):
        self.initializePinData()
        self.blockPinSignals()
        if "SUPPORTED_DATA_TYPES" in data:
            self.ui.chkPSSupportedDataTypes.setChecked(True)
            self.ui.txtPSSupportedDataTypes.setText(data["SUPPORTED_DATA_TYPES"])
        if "CONSTRAINT" in data:
            self.ui.chkPSConstraint.setChecked(True)
            self.ui.txtPSConstraint.setText(data["CONSTRAINT"])
        if "STRUCT_CONSTRAINT" in data:
            self.ui.chkPSStructConstraint.setChecked(True)
            self.ui.txtPSStructConstraint.setText(data["STRUCT_CONSTRAINT"])
        if "ENABLED_OPTIONS" in data:
            options = data["ENABLED_OPTIONS"].split("|")
            for option in options:
                if "ArraySupported" in option:  #: Pin can hold array data structure
                    self.ui.chkArraySupported.setChecked(True)
                if "DictSupported" in option:  #: Pin can hold dict data structure
                    self.ui.chkDictionarySupported.setChecked(True)
                if "SupportsOnlyArrays" in option:   #: Pin will only support other pins with array data structure
                    self.ui.chkSupportOnlyArrays.setChecked(True)
                if "AllowMultipleConnections" in option:   #: This enables pin to allow more that one input connection. See :func:`~PyFlow.Core.Common.connectPins`
                    self.ui.chkAllowMultipleConnections.setChecked(True)
                if "ChangeTypeOnConnection" in option:  #: Used by :class:`~PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` to determine if it can change its data type on new connection.
                    self.ui.chkChangeTypeOnConnection.setChecked(True)
                if "RenamingEnabled" in option:  #: Determines if pin can be renamed
                    self.ui.chkRenamingEnabled.setChecked(True)
                if "Dynamic" in option:  #: Specifies if pin was created dynamically (during program runtime)
                    self.ui.chkDynamic.setChecked(True)
                if "AlwaysPushDirty" in option:  #: Pin will always be seen as dirty (computation needed)
                    self.ui.chkAlwaysPushDirty.setChecked(True)
                if "Storable" in option:  #: Determines if pin data can be stored when pin serialized
                    self.ui.chkStorable.setChecked(True)
                if "AllowAny" in option:  #: Special flag that allow a pin to be :class:`~PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin`, which means non typed without been marked as error. By default a :py:class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` need to be initialized with some data type, other defined pin. This flag overrides that. Used in lists and non typed nodes
                    self.ui.chkAllowAny.setChecked(True)
                if "DictElementSupported" in option:  #: Dicts are constructed with :class:`DictElement` objects. So dict pins will only allow other dicts until this flag enabled. Used in :class:`~PyFlow.Packages.PyFlowBase.Nodes.makeDict` node
                    self.ui.chkDictionaryElementSupported.setChecked(True)

        if "DISABLED_OPTIONS" in data:
            self.ui.chkPSDisableOptions.setChecked(True)
            self.ui.txtPSDisableOptions.setText(data["DISABLED_OPTIONS"])
        if "INPUT_WIDGET_VARIANT" in data:
            self.ui.chkPSInputWidget.setChecked(True)
            self.ui.txtPSInputWidget.setText(data["INPUT_WIDGET_VARIANT"])
        if "DESCRIPTION" in data:
            self.ui.chkPSDescription.setChecked(True)
            self.ui.txtPSDescription.setText(data["DESCRIPTION"])
        if "VALUE_LIST" in data:
            self.ui.chkPSValueList.setChecked(True)
            self.ui.txtPSValueList.setText(data["VALUE_LIST"])
        if "VALUE_RANGE" in data:
            self.ui.chkPSValueRange.setChecked(True)
            self.ui.txtPSValueRange.setText(data["VALUE_RANGE"])
        if "DRAGGER_STEPS" in data:
            self.ui.chkPSDraggerSteps.setChecked(True)
            self.ui.txtPSDraggerSteps.setText(data["DRAGGER_STEPS"])
        self.unblockPinSignals()


    def loadNodeProperties(self, filefullpath):
            preamble = ""
            precode = ""
            readingimplementdata = -1
            readingdefdata = 0
            defdata = ""
            codedata = []
            eof = 0
            defname = ""
            code = ""
            self.selectedNodeData = {}
            self.selectedNodeData[self.selectedNodeDataName] = {}

            addDecorator = ""

            try:
                filesize = len(open(filefullpath).readlines())
                f = open(filefullpath, "r")

                for index, lineitem in enumerate(f):
                    # Reading the parts of the code (Implement, Def, Code)
                    if lineitem.find("def ") != -1 or index == filesize:
                        if lineitem.find("_init_") != -1:
                            defname = "init"

                        else:
                            defnamestart = 7
                            defnameend = lineitem.find("(")

                            if "@" in codedata[-1]:
                                addDecorator = codedata[-1].replace("    ", "")
                                codedata.pop()
                                self.selectedNodeData[self.selectedNodeDataName][defname] = codedata
                                #Starts the Next Group of code
                                codedata = [addDecorator]
                            else:
                                addDecorator = ""
                                self.selectedNodeData[self.selectedNodeDataName][defname] = codedata
                                codedata = []

                            defname = lineitem[defnamestart + 1:defnameend]

                    if lineitem.find("class ") != -1:
                        preamble = precode
                        base = ""
                        codedata = []
                    else:
                        codedata.append(lineitem.replace("    ","").replace("\n",""))
            except:
                pass


    def loadTableProperties(self, filefullpath):
            className = None
            tableName = None
            baseName = None

            fieldName = None
            fieldDataType = None
            fieldSize = None
            fieldOptions = None

            try:
                filesize = len(open(filefullpath).readlines())
                f = open(filefullpath, "r")

                for index, lineitem in enumerate(f):
                    if lineitem.find("__tablename__") != -1:
                        print(lineitem)
                    if lineitem.find("class ") != -1:
                        print(lineitem)
                        codedata = []
                        if className:
                            pass
                    else:
                        codedata.append(lineitem.replace("    ","").replace("\n",""))

                    if className:
                        fieldName = None
                        fieldDataType = None
                        fieldSize = None
                        fieldOptions = None
            except:
                pass

    def parseNodePins(self):
        defname = self.selectedNodeDataName
        self.selectedNodeData[defname]["PinDefs"] = {}
        self.selectedNodeData[defname]["PinDefs"]["Inputs"] = {}
        self.selectedNodeData[defname]["PinDefs"]["Outputs"] = {}
        inputPinOrder = 0
        outputPinOrder = 0
        try:
            for item in self.selectedNodeData[defname]["init"]:
                if "=" in item:
                    phrase = item.split("=")
                    pinName = phrase[0].replace("self.", "")

                    pinOptionsStart = phrase[1].find("(")
                    pinOptionEnd = phrase[1].find(")")
                    if pinOptionsStart != -1:
                        pinOptions = phrase[1][pinOptionsStart:pinOptionEnd]

                        '''def createInputPin(self, pinName, dataType, defaultValue=None, callback=None,
                                           structure=StructureType.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group=""):'''

                        '''createOutputPin(self, pinName, dataType, defaultValue=None, structure=StructureType.Single, constraint=None,
                                        structConstraint=None, supportedPinDataTypes=[], group=""):'''
                        pinOptionList = pinOptions.split(",")

                        pinData = {}

                        pinName = pinOptionList[0].replace("\"","").replace("\'","").replace("(","").replace(")","").replace(" ","").strip()
                        pinData["DataType"] = pinOptionList[1][2:-1].replace("\"","").replace("\'","").strip()

                        for row, options in enumerate(pinOptionList):
                            if row > 2:
                                if "=" not in options:
                                    if row == 2:
                                        pinData["DefaultValue"] = options.replace("\"","").replace("\'","").strip()
                                    if row == 3:
                                        pinData["foo"] = options.replace("\"","").replace("\'","").strip()
                                else:
                                    moreoptions = options.split("=")
                                    pinData[moreoptions[0]] = moreoptions[0]
                    else:
                        if "headerColor" in phrase[0]:
                            self.selectedNodeData[defname]["HeaderColor"] = phrase[1].strip()
                            self.ui.txtNodeHeaderColor.setText(self.selectedNodeData[defname]["HeaderColor"])

                    if 'createOutputPin' in phrase[1]:
                        outputPinOrder += 1
                        self.selectedNodeData[defname]
                        self.selectedNodeData[defname]["PinDefs"]["Outputs"][pinName] = {}
                        pinData["Order"] = outputPinOrder

                        self.selectedNodeData[defname]["PinDefs"]["Outputs"][pinName] = pinData
                    if 'createInputPin' in phrase[1]:
                        inputPinOrder += 1
                        self.selectedNodeData[defname]["PinDefs"]["Inputs"][pinName] = {}
                        pinData["Order"] = inputPinOrder

                        self.selectedNodeData[defname]["PinDefs"]["Inputs"][pinName] = pinData

        except:
            print(self.selectedNodeDataName, "Fail")

        print(self.selectedNodeData[defname])
        value = ""
        if "description" in self.selectedNodeData[defname]:
            for items in self.selectedNodeData[defname]["description"]:
                if "return" in items or len(value):
                    value += items.replace("return","").replace("\'","").strip()

                self.ui.txtNodeDescription.setText(value)

        if "category" in self.selectedNodeData[defname]:
            for items in self.selectedNodeData[defname]["category"]:
                if "return" in items:
                    value = items.replace("return","").replace("\'","").strip()
                    self.ui.txtNodeCategory.setText(value)

        if "keywords" in self.selectedNodeData[defname]:
            for items in self.selectedNodeData[defname]["keywords"]:
                if "return" in items:
                    value = items.replace("return","").replace("\'","").replace("[","").replace("]","").strip()
                    self.ui.txtNodeKeyWords.setText(value)

        self.loadNodePinTable()

    def loadNodePinTable(self):
        # InputPin
        defname = self.selectedNodeDataName
        pindatatypemodel = QtGui.QStandardItemModel(0, 2)

        for index, key in enumerate(self.pinDict):
            pindatatypemodel.setItem(index, 0, QtGui.QStandardItem(str(index)))
            pindatatypemodel.setItem(index, 1, QtGui.QStandardItem(key))
        pindatatypemodel.setItem(index+1, 0, QtGui.QStandardItem(str(index+1)))
        pindatatypemodel.setItem(index+1, 1, QtGui.QStandardItem('ExecPin'))

        if "PinDefs" in self.selectedNodeData[defname]:
            inputpinlistmodel = QtGui.QStandardItemModel(0, 2)
            inputPinList = []
            if "Inputs" in self.selectedNodeData[defname]["PinDefs"]:
                for rowcount1, pindata in enumerate(self.selectedNodeData[defname]["PinDefs"]["Inputs"]):
                    row = int(self.selectedNodeData[defname]["PinDefs"]["Inputs"][pindata]["Order"]) - 1
                    inputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))
                    DataTypeValue = ""
                    if "DataType" in self.selectedNodeData[defname]["PinDefs"]["Inputs"][pindata]:
                        inputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(
                            self.selectedNodeData[defname]["PinDefs"]["Inputs"][pindata]["DataType"]))
                        DataTypeValue = self.selectedNodeData[defname]["PinDefs"]["Inputs"][pindata]["DataType"]
                    inputPinList.append(DataTypeValue)
                    if "DefaultValue" in self.selectedNodeData[defname]["PinDefs"]["Inputs"][pindata]:
                        inputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(
                            self.selectedNodeData[defname]["PinDefs"]["Inputs"][pindata]["DefaultValue"]))

                inputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                inputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                inputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            outputPinList = []
            outputpinlistmodel = QtGui.QStandardItemModel(0, 2)
            if "Outputs" in self.selectedNodeData[defname]["PinDefs"]:
                for rowcount2, pindata in enumerate(self.selectedNodeData[defname]["PinDefs"]["Outputs"]):
                    row = int(self.selectedNodeData[defname]["PinDefs"]["Outputs"][pindata]["Order"]) - 1
                    DataTypeValue = ""
                    if rowcount2 == 0:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem("out"))
                    else:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))

                    if "DataType" in self.selectedNodeData[defname]["PinDefs"]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(
                            self.selectedNodeData[defname]["PinDefs"]["Outputs"][pindata]["DataType"]))
                        DataTypeValue = self.selectedNodeData[defname]["PinDefs"]["Outputs"][pindata]["DataType"]
                    outputPinList.append(DataTypeValue)

                    if "DefaultValue" in self.selectedNodeData[defname]["PinDefs"]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(
                            self.selectedNodeData[defname]["PinDefs"]["Outputs"][pindata]["DefaultValue"]))

                outputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            self.ui.tblNInputPins.setModel(inputpinlistmodel)
            self.ui.tblNOutputPins.setModel(outputpinlistmodel)

            if "Inputs" in self.selectedNodeData[defname]["PinDefs"]:
                for row, data in enumerate(self.selectedNodeData[defname]["PinDefs"]["Inputs"]):
                    self.ui.tblNInputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                    c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)

                    c.setValue(self.selectedNodeData[defname]["PinDefs"]["Inputs"][data]["DataType"], 1)
                    i = self.ui.tblNInputPins.model().index(row, 1)
                    # c.currentIndexChanged2[dict].connect(self.on_lstPinSettings_cmbTableChanged)
                    self.ui.tblNInputPins.setIndexWidget(i, c)

            if "Outputs" in self.selectedNodeData[defname]["PinDefs"]:
                for row,  data in enumerate(self.selectedNodeData[defname]["PinDefs"]["Outputs"]):
                    self.ui.tblNOutputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                    c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)
                    c.setValue(self.selectedNodeData[defname]["PinDefs"]["Outputs"][data]["DataType"], 1)
                    i = self.ui.tblNOutputPins.model().index(row, 1)
                    # c.currentIndexChanged2[dict].connect(self.on_lstTableSettings_cmbTableChanged)
                    self.ui.tblNOutputPins.setIndexWidget(i, c)

            # self.ui.tblNInputPins.resizeColumnsToContents()
            # self.ui.tblNOutputPins.resizeColumnsToContents()

            # self.ui.tblNInputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))
            # self.ui.tblNOutputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))

            #self.initializePinData()

            '''for z in curlystuff2.split(","):
                itemdata = z.strip().split(":")
                #print(itemdata[0], itemdata[1].strip())'''


    def loadPinProperties(self, filefullpath):

        previousitem = ""
        implementdata = ""
        readingimplementdata = -1
        readingdefdata = 0
        defdata = ""
        codedata = []
        eof = 0
        defname = ""
        code = ""
        codedescription = ""
        NestDict = {}
        try:
            filesize = len(open(filefullpath).readlines())
            f = open(filefullpath, "r")

            for index, lineitem in enumerate(f):
                #Reading the parts of the code (Implement, Def, Code)
                if lineitem.find("class") != -1:
                    self.intro = code
                precode = code
                code += lineitem
                codedata.append(lineitem)
                #print(lineitem)
                if lineitem.find("super") != -1:
                    code = ""
                    codedata = []

                if lineitem.find("@staticmethod") != -1 or index == filesize-1:
                    readingdefdata = 0
                    if precode.find("@staticmethod") != -1:
                        NestDict = {}
                        implement2 = implementdata
                        NestDict["Implement"] = implement2.replace("@staticmethod", "")
                        NestDict["Definition"] = defdata
                        NestDict["CodeDescription"] = codedescription
                        NestDict["Code"] = codedata[:-1]
                        self.pindict[defname] = NestDict

                        #self.parseFunctionFile(defname)
                        break
                    else:
                        implementdata = ""

                if lineitem.find("def ") != -1 and lineitem.find(" " + defname) != -1:
                    defnamestart = 7
                    defnameend = lineitem.find("(")
                    defname = lineitem[defnamestart + 1:defnameend]
                    readingdefdata = 1

                if readingdefdata == 1:
                    if lineitem.find("def ") != -1:
                        lineitem = lineitem[defnameend+1:]
                    readingimplementdata = 0
                    defdata += lineitem.strip()
                    if defdata[-1] == ":":
                        readingdefdata = 0
                        codedata = []
        except:
            pass


    def loadPinData(self, filefullpath):
        codenotes = 0
        importlist = []
        importstart = 0
        classstart = 0
        super = 0
        staticmethod = []
        definition = []
        codedata = []

        filesize = len(open(filefullpath).readlines())
        f = open(filefullpath, "r")

        for index, lineitem in enumerate(f):
            #Reading the parts of the code (Implement, Def, Code)
            codedata.append(lineitem)

            if lineitem.find("import") != -1:
                importlist.append(index)

            if lineitem.find("class") != -1:
                classstart = index

            if lineitem.find("def") != -1:
                definition.append(index)

        defCount = len(definition)
        for count, defitem in enumerate(definition):
            line = codedata[defitem]
            if count == defCount-1:
                endCodeBlock = len(codedata)
            else:
                endCodeBlock = definition[count+1]-1

            if codedata[defitem - 1].find("@staticmethod") != -1:
                staticmethod = True
            else:
                staticmethod = False

            if codedata[defitem].find("__init__") != -1:
                if codedata[defitem].find("super") != -1:
                    pass

            if codedata[defitem].find("toolTip") != -1:
                for row in range(defitem,endCodeBlock):
                    line2 = codedata[row]
                    if codedata[row].find("return") != -1:
                        tooltip = codedata[row][15:]
                        self.ui.txtCommandToolTip.setText(tooltip)

            if codedata[defitem].find("getIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getIcon = codedata[row][15:]
                        self.ui.txtCommandgetIcon.setText(getIcon)

            if codedata[defitem].find("name") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        name = codedata[row][15:]
                        self.ui.txtCommandName.setText(name)

            if codedata[defitem].find("do") != -1:
                code = ""
                for codeline in codedata[defitem:endCodeBlock]:
                    code += codeline
                self.ui.txtCommandCode.setText(code)

    @QtCore.Slot()
    def on_cmdCreatePackage_clicked(self):
        packageRoot = Packages.__path__[0]
        packagename = self.ui.txtPackageName.text()
        if packagename == "":
            return
        packageFolderPath = os.path.join(packageRoot, packagename)
        filepath = self.createfolder(packageFolderPath)
        self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageResource.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Resource"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageCommands.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Commands"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageFunctions.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Functions"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageWidgets.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Widgets"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageUI.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "UI"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackagePins.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Pins"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageTools.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Tools"))
            self.createfolder(os.path.join(filepath, "res"))

            with open(filepath, "__init__.py", "w") as f:
                self.addCopyright(f)
                f.write("import os\n")
                f.write("RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + \"/res/\"\n")

        if self.ui.chkPackageExporters.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Exporters"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageFactories.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Factories"))
            self.createfile(os.path.join(filepath, "__init__.py"))

    def createfolder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def createfile(self, file_name):
        if not os.path.exists(file_name):
            open(file_name, 'a').close()

    @QtCore.Slot()
    def on_cmdUpdateInit_clicked(self):
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filefullpath = os.path.join(packagepath, "__init__.py")

        fileList = []
        for file in os.listdir(packagepath):
            fileList.append(file)

        with open(filefullpath, 'w') as f:
            self.addIntro(f)

            self.defineFiles(f, "Pins")
            self.defineFiles(f, "FunctionLibraries")
            self.defineFiles(f, "Nodes")
            self.defineFiles(f, "Tools")
            self.defineFiles(f, "Exporters")


            self.defineFiles2(f, "def ", "Factories")
            self.defineFiles2(f, "class ", "PrefsWidgets")

            self.defineFoo(f, "FunctionLibraries", "_FOO_LIBS")
            self.defineDict(f, "Nodes", "_NODES")
            self.defineDict(f, "Pins", "_PINS")

            self.defineOrderedDict(f, "Tools", "_TOOLS")
            self.defineOrderedDict(f, "Exporters", "_EXPORTERS")
            self.defineOrderedDict2(f, "PrefsWidgets", "_PREFS_WIDGETS")

            self.createBasePackage(f)

    def loadInit(self, f):
        '''["Class Imports", "Pins", "Functions", "Nodes", "Factories", "Prefs widgets",
                          "Foo Dict", "Node Dict", "Pin Dict", "Toolbar Dict", "Export", "Preferred Widgets",
                          "Base Package"]'''

        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        #selectedpackage = self.ui.lstPackages.model().index(self.ui.listPackages.row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        initfile = "__init__.py"
        filename = os.path.join(packagepath, initfile)

        category = "Introduction"
        initDict = {}
        initDict[category] = []
        try:
            f = open(filename, "r")

            for index, lineitem in enumerate(f):
                if "# [" in lineitem:
                    start = lineitem.find("[")
                    stop = lineitem.find("]")
                    category = lineitem[start+1:stop]
                    initDict[category] = [lineitem.replace("\n", "")]
                else:
                    initDict[category].append(lineitem.replace("\n", ""))
        except:
            pass

        for row, item in enumerate(initDict):
            print(item)
            for line in initDict[item]:
                print("    ", line)

    def addCopyright(self, f):
        f.write("## Copyright " + self.ui.txtCopyrightAuthor.text() + " " + self.ui.dteCopyrightYear.value())
        f.write(self.ui.txtCopyright.text())

    def addIntro(self, f):
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()

        f.write("\'\'\'%s\n" % (selectedpackage))
        f.write("\'\'\'\n")
        f.write("PACKAGE_NAME = \'%s\'\n" % (selectedpackage))

        f.write("# [Class Imports]\n")
        f.write("from collections import OrderedDict\n")
        f.write("from PyFlow.UI.UIInterfaces import IPackage\n")

        f.write("\n")

    def defineFiles(self, f, foldername):
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filepath = os.path.join(packagepath, foldername)

        f.write("# [%s]\n" % (foldername))
        #f.write("%s = {" % (category))
        for file in os.listdir(filepath):
            if file[1] != "_":
                file2 = file.replace(".py","")
                #from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin
                f.write("from PyFlow.Packages.%s.%s.%s import %s\n"% (selectedpackage, foldername, file2, file2))
        f.write("\n")

    def defineFiles2(self, f, search, foldername):
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filepath = os.path.join(packagepath, foldername)

        f.write("# [%s]\n" % (foldername))
        for file in os.listdir(filepath):
            if file[1] != "_":
                file2 = file.replace(".py","")

                f2 = open(os.path.join(filepath, file), "r")
                for index, lineitem in enumerate(f2):

                    if lineitem[:len(search)] == search:
                        classnamestart = len(search)
                        classnameend = lineitem.find("(")
                        if self.workingFile.find(lineitem[classnamestart + 1:classnameend]) == -1:
                            functionname = lineitem[classnamestart :classnameend]
                            f.write("from PyFlow.Packages.%s.%s.%s import %s\n" % (selectedpackage, foldername, file2, functionname))
                        break
                #from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin

        f.write("\n")

    def defineFoo(self, f, foldername, category):
        "_FOO_LIBS, _NODES, _PINS"
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filepath = os.path.join(packagepath, foldername)

        f.write("# [%s]\n" % (foldername))
        f.write("%s = {\n" % (category))
        for file in os.listdir(filepath):
            if file[1] != "_":
                file2 = file.replace(".py","")
                f.write("    %s.__name__: %s(PACKAGE_NAME),\n"% (file2, file2))
        f.write("}\n")
        f.write("\n")

    def defineDict(self, f, foldername, category):
        "_FOO_LIBS, _NODES, _PINS"
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filepath = os.path.join(packagepath, foldername)

        f.write("# [%s]\n" % (foldername))
        f.write("%s = {\n" % (category))
        for file in os.listdir(filepath):
            if file[1] != "_":
                file2 = file.replace(".py","")
                f.write("    %s.__name__: %s,\n"% (file2, file2))
        f.write("}\n")
        f.write("\n")

    def defineOrderedDict(self, f, foldername, category):
        "_TOOLS, _EXPORTERS, _PREFS_WIDGETS"
        '''_TOOLS = OrderedDict()
           _TOOLS[CompileTool.__name__] = CompileTool'''

        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filepath = os.path.join(packagepath, foldername)

        f.write("# [%s]\n" % (foldername))
        f.write("%s = OrderedDict()\n" % category)
        for file in os.listdir(filepath):
            if file[1] != "_":
                file2 = file.replace(".py","")
                f.write("%s[%s.__name__] = %s\n"% (category, file2, file2))
        f.write("\n")

    def defineOrderedDict2(self, f, foldername, category):
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        filepath = os.path.join(packagepath, foldername)
        search = "class "
        f.write("# [%s]\n" % (foldername))
        f.write("%s = OrderedDict()\n" % category)
        for file in os.listdir(filepath):
            if file[1] != "_":
                file2 = file.replace(".py","")
                f2 = open(os.path.join(filepath, file), "r")
                for index, lineitem in enumerate(f2):

                    if lineitem[:len(search)] == search:
                        classnamestart = len(search)
                        classnameend = lineitem.find("(")
                        if self.workingFile.find(lineitem[classnamestart + 1:classnameend]) == -1:
                            functionname = lineitem[classnamestart:classnameend]

                            f.write("%s[\"%s\"] = %s\n"% (category, file2, functionname))
                            break
        f.write("\n")

    def createBasePackage(self, f):
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()

        f.write("# [%s Package]\n" % (selectedpackage))
        f.write("class %s(IPackage):\n" % (selectedpackage))
        f.write("    \"\"\"%s package\n"% (selectedpackage))
        f.write("    \"\"\"\n\n")

        f.write("    def __init__(self):\n")
        f.write("        super(%s, self).__init__()\n\n" % (selectedpackage))

        f.write("    @staticmethod\n")
        f.write("    def GetExporters():\n")
        f.write("        return _EXPORTERS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetFunctionLibraries():\n")
        f.write("        return _FOO_LIBS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetNodeClasses():\n")
        f.write("        return _NODES\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetPinClasses():\n")
        f.write("        return _PINS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetToolClasses():\n")
        f.write("        return _TOOLS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def UIPinsFactory():\n")
        f.write("        return createUIPin\n\n")

        f.write("    @staticmethod\n")
        f.write("    def UINodesFactory():\n")
        f.write("        return createUINode\n\n")

        f.write("    @staticmethod\n")
        f.write("    def PinsInputWidgetFactory():\n")
        f.write("        return getInputWidget\n\n")

        f.write("    @staticmethod\n")
        f.write("    def PrefsWidgets():\n")
        f.write("        return _PREFS_WIDGETS")

    def onDone(self):
        # if we are here, everything is correct
        self.accept()