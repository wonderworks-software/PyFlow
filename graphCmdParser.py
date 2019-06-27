import sys
import json

from PyFlow.Core.Common import *
from PyFlow import(
    INITIALIZE,
    GET_PACKAGES
)

from PyFlow.Core.GraphManager import GraphManager
from Qt.QtWidgets import *
from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance

if __name__ == '__main__':
    INITIALIZE()
    man = GraphManager()
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("plastique"))

    name_filter = "Graph files (*.json)"
    savepath = QFileDialog.getOpenFileName(filter=name_filter)
    if type(savepath) in [tuple, list]:
        fpath = savepath[0]
    else:
        fpath = savepath
    if not fpath == '':
        with open(fpath, 'r') as f:
            data = json.load(f)
        prop = PropertiesWidget()

        man.deserialize(data)
        inputs =  man.findNode(str("cmdInputs"))
        if inputs is not None:
            uiNode = getUINodeInstance(inputs)
            uiNodeJsonTemplate = inputs.serialize()
            uiNodeJsonTemplate["wrapper"] = inputs.wrapperJsonData        
            uiNode.postCreate(uiNodeJsonTemplate)
            uiNode.createOutputWidgets(prop,"input Parameters")
            prop.show()
        else:
            sys.exit()
    else:
        sys.exit()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)             