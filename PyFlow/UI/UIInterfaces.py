

class IPropertiesViewSupport(object):
    """docstring for IPropertiesViewSupport."""
    def __init__(self):
        super(IPropertiesViewSupport, self).__init__()

    def createPropertiesWidget(self, propertiesWidget):
        pass


class IDataExporter(object):
    def __init__(self):
        super(IDataExporter, self).__init__()

    @staticmethod
    def displayName():
        raise NotImplementedError('displayName method of IDataExporter is not implemented')

    @staticmethod
    def toolTip():
        return ''

    @staticmethod
    def doExport(pyFlowInstance):
        raise NotImplementedError('doExport method of IDataExporter is not implemented')


class IDataImporter(object):
    def __init__(self):
        super(IDataImporter, self).__init__()

    @staticmethod
    def displayName():
        raise NotImplementedError('displayName method of IDataImporter is not implemented')

    @staticmethod
    def toolTip():
        return ''

    @staticmethod
    def doImport(pyFlowInstance):
        raise NotImplementedError('doImport method of IDataImporter is not implemented')


class IPackage(object):
    def __init__(self):
        super(IPackage, self).__init__()

    @staticmethod
    def GetExporters():
        raise NotImplementedError('GetExporters method of IPackage is not implemented')

    @staticmethod
    def GetImporters():
        raise NotImplementedError('GetImporters method of IPackage is not implemented')

    @staticmethod
    def GetFunctionLibraries():
        raise NotImplementedError('GetFunctionLibraries method of IPackage is not implemented')

    @staticmethod
    def GetNodeClasses():
        raise NotImplementedError('GetNodeClasses method of IPackage is not implemented')

    @staticmethod
    def GetPinClasses():
        raise NotImplementedError('GetPinClasses method of IPackage is not implemented')

    @staticmethod
    def GetToolClasses():
        raise NotImplementedError('GetToolClasses method of IPackage is not implemented')

    @staticmethod
    def UIPinsFactory():
        raise NotImplementedError('UIPinsFactory method of IPackage is not implemented')

    @staticmethod
    def UINodesFactory():
        raise NotImplementedError('UINodesFactory method of IPackage is not implemented')

    @staticmethod
    def PinsInputWidgetFactory():
        raise NotImplementedError('PinsInputWidgetFactory method of IPackage is not implemented')
