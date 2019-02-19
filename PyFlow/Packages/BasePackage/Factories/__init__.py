from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.UI.InputWidgets import REGISTER_UI_PIN_FACTORY
from PyFlow.Packages.BasePackage.Factories.PinInputWidgetFactory import getInputWidget

REGISTER_UI_PIN_FACTORY(PACKAGE_NAME, getInputWidget)
