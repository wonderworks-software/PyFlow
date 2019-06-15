from datetime import datetime
from PyFlow.UI.UIInterfaces import IDataExporter
from PyFlow.Core.version import Version


class DemoExporter(IDataExporter):
    """docstring for DemoExporter."""

    def __init__(self):
        super(DemoExporter, self).__init__()

    @staticmethod
    def createImporterMenu():
        return True

    @staticmethod
    def creationDateString():
        return datetime.now().strftime("%I:%M%p on %B %d, %Y")

    @staticmethod
    def version():
        return Version(1, 0, 0)

    @staticmethod
    def toolTip():
        return "Demo Export/Import."

    @staticmethod
    def displayName():
        return "Demo exporter"

    @staticmethod
    def doImport(pyFlowInstance):
        print("DemoExporter import!")

    @staticmethod
    def doExport(pyFlowInstance):
        print("DemoExporter export!")
