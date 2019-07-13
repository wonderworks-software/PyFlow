from PyFlow import findPinClassByType
from PyFlow.UI.Widgets.SelectPinDialog import SelectPinDialog
from PyFlow.UI.Canvas.UIPinBase import UIPinBase
from Qt import QtGui


class UIAnyPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        """UI wrapper for :class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin`

        :param owningNode: Owning node
        :type owningNode: :class:`PyFlow.UI.Canvas.NodeBase`
        :param raw_pin: PinBase reference
        :type raw_pin: :class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin`
        """
        super(UIAnyPin, self).__init__(owningNode, raw_pin)
        self._defaultColor = self._pinColor
        self._rawPin.typeChanged.connect(self.setType)
        self._rawPin.dataTypeBeenSet.connect(self.dataTypeBeenSet)
        self._rawPin.onPinDisconnected.connect(self.disconnect)
        self.menu.addAction("InitAs").triggered.connect(self.selectInit)

        self.prevDataType = "AnyPin"
        self.prevColor = None

    def dataTypeBeenSet(self, *args, **kwargs):
        self.prevColor = None
        self.prevDataType = None
        self.setDefault(self._rawPin.defColor())

    def checkFree(self, checked=[], selfCheck=True):
        return self._rawPin.checkFree(checked, selfCheck)

    def disconnect(self, other):
        self.prevColor = None
        self.prevDataType = None

    @property
    def activeDataType(self):
        return self._rawPin.activeDataType

    def setDefault(self, defcolor):
        if defcolor != self.prevColor:
            self.prevColor = defcolor
            self._pinColor = QtGui.QColor(*defcolor)
            for e in self.connections:
                e.setColor(QtGui.QColor(*defcolor))
            self.OnPinChanged.emit(self)
            self.update()

    def selectInit(self):
        validPins = list(self._rawPin._defaultSupportedDataTypes)
        if "AnyPin" in validPins:
            validPins.remove("AnyPin")
        self.d = SelectPinDialog(validPins=validPins)
        self.d.exec_()
        dataType = self.d.getResult()
        if dataType is not None:
            self.initType(dataType, True)

    def initType(self, dataType, init=False):
        self._rawPin.initType(dataType, init)

    def setType(self, dataType):
        if dataType != self.prevDataType:
            self.prevDataType = dataType
            colorTuple = findPinClassByType(dataType).color()
            self._pinColor = QtGui.QColor(*colorTuple)
            for e in self.connections:
                e.setColor(self._pinColor)
            self.OnPinChanged.emit(self)
            self.update()
