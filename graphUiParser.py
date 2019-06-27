import sys
import json
from Qt.QtWidgets import *
from Qt import QtGui
from Qt import QtCore
from PyFlow import INITIALIZE
from PyFlow.Core.Common import *
from PyFlow.Core.GraphManager import GraphManager
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Utils.stylesheet import editableStyleSheet
import PyFlow.UI.resources

if __name__ == '__main__':
    # New Qt App
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("plastique"))
    app.setStyleSheet(editableStyleSheet().getStyleSheet())
    # Load Graph File
    name_filter = "Graph files (*.json)"
    savepath = QFileDialog.getOpenFileName(filter=name_filter)
    if type(savepath) in [tuple, list]:
        fpath = savepath[0]
    else:
        fpath = savepath

    if not fpath == '':
        with open(fpath, 'r') as f:
            data = json.load(f)
        # Window to display Inputs
        prop = QDialog()
        prop.setLayout(QVBoxLayout())
        prop.setWindowTitle(fpath)
        prop.setWindowIcon(QtGui.QIcon(":/LogoBpApp.png"))
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(":/LogoBpApp.png"))
        msg.setIcon(QMessageBox.Critical)
        # Initalize Packages
        try:
            INITIALIZE()
            man = GraphManager()
            man.deserialize(data)
            grph = man.findRootGraph()
            inputs = grph.getNodesByClassName("graphInputs")
            # If no GraphInput Nodes Exit propgram
            if len(inputs) > 0:
                for inp in inputs:
                    uiNode = getUINodeInstance(inp)
                    uiNodeJsonTemplate = inp.serialize()
                    uiNodeJsonTemplate["wrapper"] = inp.wrapperJsonData
                    uiNode.postCreate(uiNodeJsonTemplate)
                    cat = uiNode.createOutputWidgets(prop.layout(), inp.name)
                    prop.show()
            else:
                msg.setInformativeText(fpath)
                msg.setDetailedText(
                    "The file doesn't containt graphInputs nodes")
                msg.setWindowTitle("PyFlow Ui Graph Parser")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.show()
        except Exception as e:
            msg.setText("Error reading Graph")
            msg.setInformativeText(fpath)
            msg.setDetailedText(str(e))
            msg.setWindowTitle("PyFlow Ui Graph Parser")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()
    else:
        msg.setText("File Not Found")
        msg.setInformativeText(fpath)
        msg.setWindowTitle("PyFlow Ui Graph Parser")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
