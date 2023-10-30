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

    def isReroute(self):
        return False

    def serializationHook(self):
        raise NotImplementedError("serializationHook of IUINode is not implemented")


class IPropertiesViewSupport(object):
    """docstring for IPropertiesViewSupport."""

    def __init__(self):
        super(IPropertiesViewSupport, self).__init__()

    def createPropertiesWidget(self, propertiesWidget):
        pass


class IDataExporter(object):
    """Data exporter/importer

    Editor data can be exported/imported to/from arbitrary formats
    """

    def __init__(self):
        super(IDataExporter, self).__init__()

    @staticmethod
    def creationDateString():
        raise NotImplementedError(
            "creationDateString method of IDataExporter is not implemented"
        )

    @staticmethod
    def version():
        raise NotImplementedError("version method of IDataExporter is not implemented")

    @staticmethod
    def displayName():
        raise NotImplementedError(
            "displayName method of IDataExporter is not implemented"
        )

    @staticmethod
    def toolTip():
        return ""

    @staticmethod
    def createImporterMenu():
        return True

    @staticmethod
    def createExporterMenu():
        return True

    @staticmethod
    def doImport(pyFlowInstance):
        raise NotImplementedError("doImport method of IDataExporter is not implemented")

    @staticmethod
    def doExport(pyFlowInstance):
        raise NotImplementedError("doExport method of IDataExporter is not implemented")


class IPackage(object):
    """Class that describes a set of modules that can be plugged into the editor.

    Will be instantiated and used to create registered entities.
    """

    def __init__(self):
        super(IPackage, self).__init__()

    @staticmethod
    def GetExporters():
        """Registered editor data exporters

        :rtype: dict(str, class)
        """
        raise NotImplementedError("GetExporters method of IPackage is not implemented")

    @staticmethod
    def GetFunctionLibraries():
        """Registered function library instances

        :rtype: dict(str, object)
        """
        raise NotImplementedError(
            "GetFunctionLibraries method of IPackage is not implemented"
        )

    @staticmethod
    def GetNodeClasses():
        """Registered node classes

        :rtype: dict(str, class)
        """
        raise NotImplementedError(
            "GetNodeClasses method of IPackage is not implemented"
        )

    @staticmethod
    def GetPinClasses():
        """Registered pin classes

        :rtype: dict(str, class)
        """
        raise NotImplementedError("GetPinClasses method of IPackage is not implemented")

    @staticmethod
    def GetToolClasses():
        """Registered tool classes

        :rtype: dict(str, class)
        """
        raise NotImplementedError(
            "GetToolClasses method of IPackage is not implemented"
        )

    @staticmethod
    def UIPinsFactory():
        """Registered ui pin wrappers

        :rtype: function
        """
        return None

    @staticmethod
    def UINodesFactory():
        """Registered ui nodes

        :rtype: function
        """
        return None

    @staticmethod
    def PinsInputWidgetFactory():
        """Registered pin input widgets

        :rtype: function
        """
        return None

    @staticmethod
    def PrefsWidgets():
        """Registered preferences widgets

        :rtype: dict(str, class)
        """
        return None
