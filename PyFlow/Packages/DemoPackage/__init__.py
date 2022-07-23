PACKAGE_NAME = 'DemoPackage'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.DemoPackage.Pins.DemoPin import DemoPin

# Class based nodes
from PyFlow.Packages.DemoPackage.Nodes.DemoNode import DemoNode

# Factories
from PyFlow.Packages.DemoPackage.Factories.PinInputWidgetFactory import getInputWidget

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

_NODES[DemoNode.__name__] = DemoNode

_PINS[DemoPin.__name__] = DemoPin


class DemoPackage(IPackage):
	def __init__(self):
		super(DemoPackage, self).__init__()

	@staticmethod
	def GetExporters():
		return _EXPORTERS

	@staticmethod
	def GetFunctionLibraries():
		return _FOO_LIBS

	@staticmethod
	def GetNodeClasses():
		return _NODES

	@staticmethod
	def GetPinClasses():
		return _PINS

	@staticmethod
	def GetToolClasses():
		return _TOOLS

	@staticmethod
	def PinsInputWidgetFactory():
		return getInputWidget

