import os
from enum import Enum
from Qt import QtCore, QtGui

from PyFlow.Core.Common import SingletonDecorator


@SingletonDecorator
class ConfigManager(object):
    """docstring for ConfigManager."""
    CONFIGS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Configs")
    APP_SETTINGS_PATH = os.path.join(CONFIGS_DIR, "config.ini")
    INPUT_CONFIG_PATH = os.path.join(CONFIGS_DIR, "input.ini")

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.INPUT_CONFIG_PATH):
            self.createDefaultInput()

    def createDefaultInput(self):
        input_config = QtCore.QSettings(self.INPUT_CONFIG_PATH, QtCore.QSettings.IniFormat, self)
        # input_config.beginGroup("Canvas")
        # input_config.setValue("Pan", QtGui.QKeySequence(QtCore.Qt.Key))
        # input_config.endGroup()
