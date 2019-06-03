import json
import weakref
try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QAbstractItemView
from Qt.QtWidgets import QFrame
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QVBoxLayout

from PyFlow import GET_PACKAGES

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodeBase


class NodeBoxLineEdit(QLineEdit):
    def __init__(self, parent, events=True):
        super(NodeBoxLineEdit, self).__init__(parent)
        self.setParent(parent)
        self._events = events
        self.parent = parent
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English,
                                      QtCore.QLocale.UnitedStates))
        self.setObjectName("le_nodes")
        style = "background-color: rgb(80, 80, 80);" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setPlaceholderText("enter node name..")


class NodeBoxTreeWidget(QTreeWidget):
    def __init__(self, parent, useDragAndDrop=True):
        super(NodeBoxTreeWidget, self).__init__(parent)
        style = "background-color: rgb(40, 40, 40);" +\
                "selection-background-color: rgb(50, 50, 50);" +\
                "border-radius: 2px;" +\
                "font-size: 14px;" +\
                "border-color: black; border-style: outset; border-width: 1px;"
        self.setStyleSheet(style)
        self.setParent(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Sunken)
        self.setObjectName("tree_nodes")
        self.setSortingEnabled(True)
        self.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.setColumnCount(0)
        self.setHeaderHidden(True)
        self.bUseDragAndDrop = useDragAndDrop
        if useDragAndDrop:
            self.setDragEnabled(True)
            self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setAnimated(True)
        self.categoryPaths = {}

    def _isCategoryExists(self, category_name, categories):
        bFound = False
        if category_name in categories:
            return True
        if not bFound:
            for c in categories:
                sepCatNames = c.split('|')
                if len(sepCatNames) == 1:
                    if category_name == c:
                        return True
                else:
                    for i in range(0, len(sepCatNames)):
                        c = '|'.join(sepCatNames)
                        if category_name == c:
                            return True
                        sepCatNames.pop()
        return False

    def insertNode(self, nodeCategoryPath, name, doc=None, libName=None):
        nodePath = nodeCategoryPath.split('|')
        categoryPath = ''
        # walk from tree top to bottom, creating folders if needed
        # also writing all paths in dict to avoid duplications
        for folderId in range(0, len(nodePath)):
            folderName = nodePath[folderId]
            if folderId == 0:
                categoryPath = folderName
                if categoryPath not in self.categoryPaths:
                    rootFolderItem = QTreeWidgetItem(self)
                    rootFolderItem.bCategory = True
                    rootFolderItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    rootFolderItem.setText(0, folderName)
                    rootFolderItem.setBackground(
                        folderId, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = rootFolderItem
            else:
                parentCategoryPath = categoryPath
                categoryPath += '|{}'.format(folderName)
                if categoryPath not in self.categoryPaths:
                    childCategoryItem = QTreeWidgetItem(
                        self.categoryPaths[parentCategoryPath])
                    childCategoryItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    childCategoryItem.bCategory = True
                    childCategoryItem.setText(0, folderName)
                    childCategoryItem.setBackground(
                        0, QtGui.QColor(80, 85, 80))
                    self.categoryPaths[categoryPath] = childCategoryItem
        # create node under constructed folder
        nodeItem = QTreeWidgetItem(self.categoryPaths[categoryPath])
        nodeItem.bCategory = False
        nodeItem.setText(0, name)
        nodeItem.libName = libName
        if doc:
            nodeItem.setToolTip(0, doc)

    def refresh(self, dataType=None, pattern='', pinType=None):
        self.clear()
        self.categoryPaths = {}

        for package_name, package in GET_PACKAGES().items():
            # annotated functions
            for libName, lib in package.GetFunctionLibraries().items():
                foos = lib.getFunctions()
                for name, foo in foos.items():
                    foo = foo
                    libName = foo.__annotations__["lib"]
                    fooArgNames = getargspec(foo).args
                    fooInpTypes = []
                    fooOutTypes = []
                    if foo.__annotations__['nodeType'] == NodeTypes.Callable:
                        fooInpTypes.append('ExecPin')
                        fooOutTypes.append('ExecPin')

                    # consider return type if not None
                    if foo.__annotations__['return'] is not None:
                        fooOutTypes.append(foo.__annotations__['return'][0])

                    for index in range(len(fooArgNames)):
                        dType = foo.__annotations__[fooArgNames[index]]
                        # if tuple - this means ref pin type (output) + default value
                        # eg: (3, True) - bool with True default val
                        if isinstance(dType, tuple):
                            fooOutTypes.append(dType[0])
                        else:
                            fooInpTypes.append(dType)

                    nodeCategoryPath = "{0}|{1}".format(
                        package_name, foo.__annotations__['meta']['Category'])
                    keywords = foo.__annotations__['meta']['Keywords']
                    checkString = name + nodeCategoryPath + ''.join(keywords)
                    if pattern.lower() in checkString.lower():
                        # create all nodes items if clicked on canvas
                        if dataType is None:
                            self.insertNode(nodeCategoryPath,
                                            name, foo.__doc__, libName)
                        else:
                            if pinType == PinDirection.Output:
                                if dataType in fooInpTypes:
                                    self.insertNode(
                                        nodeCategoryPath, name, foo.__doc__, libName)
                            else:
                                if dataType in fooOutTypes:
                                    self.insertNode(
                                        nodeCategoryPath, name, foo.__doc__, libName)

            # class based nodes
            for node_class in package.GetNodeClasses().values():
                if node_class.__name__ in ('setVar', 'getVar'):
                    continue

                nodeCategoryPath = "{0}|{1}".format(
                    package_name, node_class.category())

                checkString = node_class.__name__ + \
                    nodeCategoryPath + ''.join(node_class.keywords())
                if pattern.lower() not in checkString.lower():
                    continue
                if dataType is None:
                    self.insertNode(
                        nodeCategoryPath, node_class.__name__, node_class.description())
                else:
                    # if pressed pin is output pin
                    # filter by nodes input types
                    if pinType == PinDirection.Output:
                        if dataType in node_class.pinTypeHints()['inputs']:
                            self.insertNode(
                                nodeCategoryPath, node_class.__name__, node_class.description())
                    else:
                        # if pressed pin is input pin
                        # filter by nodes output types
                        if dataType in node_class.pinTypeHints()['outputs']:
                            self.insertNode(
                                nodeCategoryPath, node_class.__name__, node_class.description())
            # expand all categories
            if dataType is not None:
                for categoryItem in self.categoryPaths.values():
                    categoryItem.setExpanded(True)
        self.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
    def keyPressEvent(self, event):
        super(NodeBoxTreeWidget, self).keyPressEvent(event)
        key = event.key()
        canvas = self.parent().canvasRef()
        if key == QtCore.Qt.Key_Return:
            item_clicked = self.currentItem()
            if not item_clicked:
                event.ignore()
                return
            # check if clicked item is a category
            if item_clicked.bCategory:
                event.ignore()
                return
            # find top level parent
            rootItem = item_clicked
            while not rootItem.parent() is None:
                rootItem = rootItem.parent()
            packageName = rootItem.text(0)
            pressed_text = item_clicked.text(0)
            libName = item_clicked.libName
            if pressed_text in self.categoryPaths.keys():
                event.ignore()
                return

            nodeClassName = self.currentItem().text(0)
            name = nodeClassName
            pos = canvas.mapToScene(canvas.mouseReleasePos)
            nodeTemplate = NodeBase.jsonTemplate()
            nodeTemplate['package'] = packageName
            nodeTemplate['lib'] = libName
            nodeTemplate['type'] = pressed_text
            nodeTemplate['name'] = name
            nodeTemplate['x'] = pos.x()
            nodeTemplate['y'] = pos.y()
            nodeTemplate['meta']['label'] = nodeClassName
            nodeTemplate['uuid'] = str(uuid.uuid4())

            canvas.createNode(nodeTemplate)

    def mousePressEvent(self, event):
        super(NodeBoxTreeWidget, self).mousePressEvent(event)
        canvas = self.parent().canvasRef()
        item_clicked = self.currentItem()
        if not item_clicked:
            event.ignore()
            return
        # check if clicked item is a category
        if item_clicked.bCategory:
            event.ignore()
            return
        # find top level parent
        rootItem = item_clicked
        while not rootItem.parent() is None:
            rootItem = rootItem.parent()
        packageName = rootItem.text(0)
        pressed_text = item_clicked.text(0)
        libName = item_clicked.libName

        if pressed_text in self.categoryPaths.keys():
            event.ignore()
            return

        try:
            mousePos = canvas.mapToScene(canvas.mousePressPose)
        except:
            mousePos = canvas.mapToScene(canvas.mousePressPose.toPoint())

        jsonTemplate = NodeBase.jsonTemplate()
        jsonTemplate['package'] = packageName
        jsonTemplate['lib'] = libName
        jsonTemplate['type'] = pressed_text
        jsonTemplate['name'] = pressed_text
        jsonTemplate['uuid'] = str(uuid.uuid4())
        jsonTemplate['x'] = mousePos.x()
        jsonTemplate['y'] = mousePos.y()
        jsonTemplate['meta']['label'] = pressed_text

        if self.bUseDragAndDrop:
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()

            pressed_text = json.dumps(jsonTemplate)
            mime_data.setText(pressed_text)
            drag.setMimeData(mime_data)
            drag.exec_()
        else:
            canvas.createNode(jsonTemplate)


class NodesBox(QWidget):
    """doc string for NodesBox"""

    def __init__(self, parent, canvas=None):
        super(NodesBox, self).__init__(parent)
        self.canvasRef = weakref.ref(canvas)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.lineEdit = NodeBoxLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.treeWidget = NodeBoxTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.lineEdit.textChanged.connect(self.leTextChanged)
        self.treeWidget.refresh()

    def sizeHint(self):
        return QtCore.QSize(400, 250)

    def expandCategory(self):
        for i in self.treeWidget.categoryPaths:
            self.treeWidget.setItemExpanded(
                self.treeWidget.categoryPaths[i], True)

    def leTextChanged(self):
        if self.lineEdit.text() == '':
            self.lineEdit.setPlaceholderText("enter node name..")
            self.treeWidget.refresh()
            return
        self.treeWidget.refresh(None, self.lineEdit.text())
        self.expandCategory()
