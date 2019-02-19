from PyFlow.Packages.Pyrr import PACKAGE_NAME
from PyFlow.UI.InputWidgets import REGISTER_UI_PIN_FACTORY
from PyFlow.Packages.Pyrr.Factories.PinInputWidgetFactory import getInputWidget

REGISTER_UI_PIN_FACTORY(PACKAGE_NAME, getInputWidget)
