from Qt import QtWidgets, QtCore
import sys
import collections

class EditPropertiesTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self):
        super(EditPropertiesTreeWidget, self).__init__()
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setHeaderHidden(True)

    def addFolder(self, name, parent=None):
        icon = self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon)
        item = QtWidgets.QTreeWidgetItem([name])
        item.setIcon(0, icon)
        item.isFolder = True
        if parent is None:
            self.addTopLevelItem(item)
        else:
            parent.addChild(item)
        return item

    def addNormal(self, name, parent=None):
        item = QtWidgets.QTreeWidgetItem([name])
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsDropEnabled)
        item.isFolder = False
        if parent is not None:
            parent.addChild(item)
        else:
            self.addTopLevelItem(item)
        return item

    def fill_dict_from_model(self, parent_index, d, model):
        v = collections.OrderedDict()
        for i in range(model.rowCount(parent_index)):
            ix = model.index(i, 0, parent_index)
            self.fill_dict_from_model(ix, v, model)
        if len(v) == 0:
            v = None
        d[parent_index.data()] = v

    def model_to_dict(self):
        model = self.model()
        d = collections.OrderedDict()
        for i in range(model.rowCount()):
            ix = model.index(i, 0)
            self.fill_dict_from_model(ix, d, model)
        return d


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = EditPropertiesTreeWidget()
    form.addNormal("Normal")
    form.addNormal("Normal1")
    form.addFolder("Folder")
    form.addFolder("Folder1")
    form.show()

    app.exec_()
