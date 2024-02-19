from qtpy.QtWidgets import *

from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.UI.Widgets.PreferencesWindow import CategoryWidgetBase


class DemoPrefs(CategoryWidgetBase):
    """docstring for DemoPrefs"""

    def __init__(self, parent=None):
        super(DemoPrefs, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)

        demoSection = CollapsibleFormWidget(headName="Demo section")
        self.exampleProperty = QLineEdit("Property value")
        demoSection.addWidget("Example property", self.exampleProperty)

        self.layout.addWidget(demoSection)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def initDefaults(self, settings):
        settings.setValue("ExampleProperty", "property value")

    def serialize(self, settings):
        settings.setValue("ExampleProperty", self.exampleProperty.text())

    def onShow(self, settings):
        self.exampleProperty.setText(settings.value("ExampleProperty"))
