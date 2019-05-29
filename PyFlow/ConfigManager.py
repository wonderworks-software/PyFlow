import os
import json
from enum import Enum
from Qt import QtCore, QtGui

from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Input import InputAction, InputManager, InputActionType


@SingletonDecorator
class ConfigManager(object):
    """Responsible for creating default configs creation and config's file paths."""
    CONFIGS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Configs")
    APP_SETTINGS_PATH = os.path.join(CONFIGS_DIR, "config.ini")
    INPUT_CONFIG_PATH = os.path.join(CONFIGS_DIR, "input.json")
    PREFERENCES_CONFIG_PATH = os.path.join(CONFIGS_DIR, "prefs.ini")

    def __init__(self, *args, **kwargs):
        if not os.path.exists(self.INPUT_CONFIG_PATH):
            self.createDefaultInput()
        else:
            with open(self.INPUT_CONFIG_PATH, "r") as f:
                data = json.load(f)
                InputManager().loadFromData(data)

    def createDefaultInput(self):
        InputManager().registerAction(InputAction(name="Canvas.Pan", actionType=InputActionType.Mouse, group="Navigation", mouse=QtCore.Qt.MouseButton.MiddleButton))
        InputManager().registerAction(InputAction(name="Canvas.Pan", actionType=InputActionType.Mouse, group="Navigation", mouse=QtCore.Qt.MouseButton.LeftButton, modifiers=QtCore.Qt.AltModifier))
        InputManager().registerAction(InputAction(name="Canvas.Zoom", actionType=InputActionType.Mouse, group="Navigation", mouse=QtCore.Qt.MouseButton.RightButton))
