from PyFlow.UI.UIInterfaces import IDataExporter


class PyFlowProgramExporter(IDataExporter):
    """docstring for PyFlowProgramExporter."""
    def __init__(self):
        super(PyFlowProgramExporter, self).__init__()

    @staticmethod
    def toolTip():
        return "Exports program as single script that can be evaluated outside the editor."

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
