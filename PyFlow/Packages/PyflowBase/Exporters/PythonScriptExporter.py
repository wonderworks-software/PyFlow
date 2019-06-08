from PyFlow.UI.UIInterfaces import IDataExporter


class PythonScriptExporter(IDataExporter):
    """docstring for PythonScriptExporter."""
    def __init__(self):
        super(PythonScriptExporter, self).__init__()

    @staticmethod
    def toolTip():
        return "Exports program as python script."

    @staticmethod
    def displayName():
        return "Pyflow program"

    @staticmethod
    def doExport(pyFlowInstance):
        # validate data
        # select out file path
        # export
        print("here will be export file generation!")
        print("num nodes:", len(pyFlowInstance.graphManager.getAllNodes()))
