from PyFlow.UI.UIInterfaces import IDataImporter


class PythonScriptImporter(IDataImporter):
    """docstring for PythonScriptImporter."""
    def __init__(self):
        super(PythonScriptImporter, self).__init__()

    @staticmethod
    def toolTip():
        return "Imports program."

    @staticmethod
    def displayName():
        return "Pyflow program importer"

    @staticmethod
    def doImport(pyFlowInstance):
        # show open file dialog
        # validate
        # do stuff on PyFlow instance, create nodes, connections etc
        print("here will be import!")
        print("num nodes:", len(pyFlowInstance.graphManager.getAllNodes()))
