import os
import json
from enum import Enum
from Qt import QtCore, QtGui

from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Input import InputAction, InputManager, InputActionType


@SingletonDecorator
class ConfigManager(object):
    """Responsible for registering configuration files, reading/writing values to registered config files by aliases, providing QSettings from registered aliases."""

    CONFIGS_STORAGE = {}

    CONFIGS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Configs")
    INPUT_CONFIG_PATH = os.path.join(CONFIGS_DIR, "input.json")

    def __init__(self, *args, **kwargs):
        self.registerConfigFile("PREFS", os.path.join(self.CONFIGS_DIR, "prefs.ini"))
        self.registerConfigFile("APP_STATE", os.path.join(self.CONFIGS_DIR, "config.ini"))

        if not os.path.exists(self.INPUT_CONFIG_PATH):
            self.createDefaultInput()
            data = InputManager().serialize()
            if not os.path.exists(os.path.dirname(self.INPUT_CONFIG_PATH)):
                os.makedirs(os.path.dirname(self.INPUT_CONFIG_PATH))
            with open(self.INPUT_CONFIG_PATH, "w") as f:
                json.dump(data, f)
        else:
            with open(self.INPUT_CONFIG_PATH, "r") as f:
                data = json.load(f)
                InputManager().loadFromData(data)

    def registerConfigFile(self, alias, absPath):
        if alias not in self.CONFIGS_STORAGE:
            self.CONFIGS_STORAGE[alias] = absPath
            return True
        return False

    def getSettings(self, alias):
        if alias in self.CONFIGS_STORAGE:
            settings = QtCore.QSettings(self.CONFIGS_STORAGE[alias], QtCore.QSettings.IniFormat)
            return settings

    def getPrefsValue(self, configAlias, valueKey):
        settings = self.getSettings(configAlias)
        if settings:
            if settings.contains(valueKey):
                return settings.value(valueKey)

    def createDefaultInput(self):
        InputManager().registerAction(InputAction(name="Canvas.Pan", actionType=InputActionType.Mouse, group="Navigation", mouse=QtCore.Qt.MouseButton.MiddleButton))
        InputManager().registerAction(InputAction(name="Canvas.Pan", actionType=InputActionType.Mouse, group="Navigation", mouse=QtCore.Qt.MouseButton.LeftButton, modifiers=QtCore.Qt.AltModifier))
        InputManager().registerAction(InputAction(name="Canvas.Zoom", actionType=InputActionType.Mouse, group="Navigation", mouse=QtCore.Qt.MouseButton.RightButton))
        InputManager().registerAction(InputAction(name="Canvas.FrameSelected", actionType=InputActionType.Keyboard, group="Navigation", key=QtCore.Qt.Key_F))
        InputManager().registerAction(InputAction(name="Canvas.FrameAll", actionType=InputActionType.Keyboard, group="Navigation", key=QtCore.Qt.Key_H))
        InputManager().registerAction(InputAction(name="Canvas.ZoomIn", actionType=InputActionType.Keyboard, group="Navigation", key=QtCore.Qt.Key_Equal, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="Canvas.ZoomOut", actionType=InputActionType.Keyboard, group="Navigation", key=QtCore.Qt.Key_Minus, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="Canvas.ResetScale", actionType=InputActionType.Keyboard, group="Navigation", key=QtCore.Qt.Key_R, modifiers=QtCore.Qt.ControlModifier))

        InputManager().registerAction(InputAction(name="Canvas.AlignLeft", actionType=InputActionType.Keyboard, group="Refactoring", modifiers=QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier, key=QtCore.Qt.Key_Left))
        InputManager().registerAction(InputAction(name="Canvas.AlignTop", actionType=InputActionType.Keyboard, group="Refactoring", modifiers=QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier, key=QtCore.Qt.Key_Up))
        InputManager().registerAction(InputAction(name="Canvas.AlignRight", actionType=InputActionType.Keyboard, group="Refactoring", modifiers=QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier, key=QtCore.Qt.Key_Right))
        InputManager().registerAction(InputAction(name="Canvas.AlignBottom", actionType=InputActionType.Keyboard, group="Refactoring", modifiers=QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier, key=QtCore.Qt.Key_Down))

        InputManager().registerAction(InputAction(name="Canvas.Undo", actionType=InputActionType.Keyboard, group="Editing", modifiers=QtCore.Qt.ControlModifier, key=QtCore.Qt.Key_Z))
        InputManager().registerAction(InputAction(name="Canvas.Redo", actionType=InputActionType.Keyboard, group="Editing", modifiers=QtCore.Qt.ControlModifier, key=QtCore.Qt.Key_Y))
        InputManager().registerAction(InputAction(name="Canvas.KillSelected", actionType=InputActionType.Keyboard, group="Editing", key=QtCore.Qt.Key_Delete))
        InputManager().registerAction(InputAction(name="Canvas.CopyNodes", actionType=InputActionType.Keyboard, group="Editing", key=QtCore.Qt.Key_C, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="Canvas.CutNodes", actionType=InputActionType.Keyboard, group="Editing", key=QtCore.Qt.Key_X, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="Canvas.DragCopyNodes", actionType=InputActionType.Mouse, group="Editing", mouse=QtCore.Qt.MouseButton.LeftButton, modifiers=QtCore.Qt.AltModifier))
        InputManager().registerAction(InputAction(name="Canvas.DragCopyNodes", actionType=InputActionType.Mouse, group="Editing", mouse=QtCore.Qt.MouseButton.MiddleButton, modifiers=QtCore.Qt.AltModifier))
        InputManager().registerAction(InputAction(name="Canvas.DragNodes", actionType=InputActionType.Mouse, group="Editing", mouse=QtCore.Qt.MouseButton.MiddleButton))
        InputManager().registerAction(InputAction(name="Canvas.DragNodes", actionType=InputActionType.Mouse, group="Editing", mouse=QtCore.Qt.MouseButton.LeftButton))
        InputManager().registerAction(InputAction(name="Canvas.DragChainedNodes", actionType=InputActionType.Mouse, group="Editing", mouse=QtCore.Qt.MouseButton.MiddleButton))
        InputManager().registerAction(InputAction(name="Canvas.PasteNodes", actionType=InputActionType.Keyboard, group="Editing", key=QtCore.Qt.Key_V, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="Canvas.DuplicateNodes", actionType=InputActionType.Keyboard, group="Editing", key=QtCore.Qt.Key_D, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="Canvas.DisconnectPin", actionType=InputActionType.Mouse, group="Editing", mouse=QtCore.Qt.MouseButton.LeftButton, modifiers=QtCore.Qt.AltModifier))

        InputManager().registerAction(InputAction(name="App.NewFile", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_N, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="App.Save", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_S, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="App.SaveAs", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_S, modifiers=QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier))
        InputManager().registerAction(InputAction(name="App.Load", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_O, modifiers=QtCore.Qt.ControlModifier))
