from qtpy.QtWidgets import *


class FileDialog(QFileDialog):
    """docstring for ExecInputWidget"""

    def __init__(self, mode="all", multifile=False, parent=None, **kwargs):
        super(FileDialog, self).__init__(parent=parent, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        if mode == "all":
            self.setFileMode(QFileDialog.Directory)
            for but in self.findChildren(QPushButton):
                if "open" in but.text().lower() or "choose" in but.text().lower():
                    but.clicked.disconnect()
                    but.clicked.connect(self.chooseClicked)

        elif mode == "file":
            self.setFileMode(QFileDialog.AnyFile)

        elif mode == "directory":
            self.setFileMode(QFileDialog.DirectoryOnly)

        if multifile:
            self.listView = self.findChild(QListView)
            if self.listView:
                self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.treeView = self.findChild(QTreeView)
            if self.treeView:
                self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def chooseClicked(self):
        QDialog.accept(self)
