## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


class IUINode(object):
    """docstring for IUINode."""
    def __init__(self):
        super(IUINode, self).__init__()

    def serializationHook(self):
        raise NotImplementedError("serializationHook of IUINode is not implemented")


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
    def creationDateString():
        raise NotImplementedError('creationDateString method of IDataExporter is not implemented')

    @staticmethod
    def version():
        raise NotImplementedError('version method of IDataExporter is not implemented')

    @staticmethod
    def displayName():
        raise NotImplementedError('displayName method of IDataExporter is not implemented')

    @staticmethod
    def toolTip():
        return ''

    @staticmethod
    def createImporterMenu():
        return True

    @staticmethod
    def createExporterMenu():
        return True

    @staticmethod
    def doImport(pyFlowInstance):
        raise NotImplementedError('doImport method of IDataExporter is not implemented')

    @staticmethod
    def doExport(pyFlowInstance):
        raise NotImplementedError('doExport method of IDataExporter is not implemented')


class IPackage(object):
    def __init__(self):
        super(IPackage, self).__init__()

    @staticmethod
    def GetExporters():
        raise NotImplementedError('GetExporters method of IPackage is not implemented')

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
        return None

    @staticmethod
    def UINodesFactory():
        return None

    @staticmethod
    def PinsInputWidgetFactory():
        return None

    @staticmethod
    def PrefsWidgets():
        return None
