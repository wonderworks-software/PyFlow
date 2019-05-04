

class IPropertiesViewSupport(object):
    """docstring for IPropertiesViewSupport."""
    def __init__(self):
        super(IPropertiesViewSupport, self).__init__()

    def createPropertiesWidget(self):
        pass


class IPackage(object):
    def __init__(self):
        super(IPackage, self).__init__()

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
