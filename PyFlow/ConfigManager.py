import os
import json
from enum import Enum
from Qt import QtCore, QtGui

from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Input import InputAction, InputManager


@SingletonDecorator
class ConfigManager(object):
    """Responsible for creating default configs creation and config's file paths."""
    CONFIGS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Configs")
    APP_SETTINGS_PATH = os.path.join(CONFIGS_DIR, "config.ini")
    INPUT_CONFIG_PATH = os.path.join(CONFIGS_DIR, "input.json")

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.INPUT_CONFIG_PATH):
            self.createDefaultInput()
        else:
            with open(self.INPUT_CONFIG_PATH, "r") as f:
                data = json.load(f)
                InputManager().loadFromData(data)

    def createDefaultInput(self):
        InputManager().registerAction(InputAction("Pan", "Navigation", QtCore.Qt.MouseButton.MiddleButton))
        InputManager().registerAction(InputAction("Pan", "Navigation", QtCore.Qt.MouseButton.LeftButton, modifiers=QtCore.Qt.AltModifier))
        InputManager().registerAction(InputAction("Zoom", "Navigation", QtCore.Qt.MouseButton.RightButton))
