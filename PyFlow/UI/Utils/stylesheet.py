from Qt import QtGui
import inspect
import os
from PyFlow.UI.Utils.Settings import Colors
from PyFlow.Core.Common import clamp
from PyFlow.Core.Common import SingletonDecorator

# def clamp(val,min_value,max_value):
#     return max(min(val, max_value), min_value)
FILE_DIR = os.path.dirname(__file__)
STYLE_PATH = os.path.join(FILE_DIR,  "style.css") 
 
@SingletonDecorator
class editableStyleSheet():
  def __init__(self):

    self.TextColor = QtGui.QColor(228, 228, 228)

    self.MainColor = QtGui.QColor(215, 128, 26)
    self.MainColor_Lighter = QtGui.QColor(self.MainColor)
    self.MainColor_Lighter.setAlpha(128)

    self.BgColorDark = QtGui.QColor(53, 53, 53)
    self.BgColorDarker = QtGui.QColor(50, 50, 50)
    self.BgColorBright = QtGui.QColor(82, 82, 82)

    self.BorderColor = QtGui.QColor(10, 10, 10)
    self.InputFieldColor = QtGui.QColor(32, 32, 32)
    self.InputFieldHover = QtGui.QColor(95, 95, 95)

    self.InputTextSelBg = QtGui.QColor(59, 59, 59)
    self.InputTextSelColor = QtGui.QColor(255, 255, 255)

    self.ScrollBarColor =  QtGui.QColor(146, 146, 146)

    self.ButtonG1 = QtGui.QColor(80,80,80)
    self.ButtonG2 = QtGui.QColor(60,60,60)
    self.ButtonG3 = QtGui.QColor(50, 50, 50)

    self.DropDownIconBg = QtGui.QColor(0,0,0,100)
    self.storeDeffaults()

  def storeDeffaults(self):
    for name,obj in inspect.getmembers(self):
      if isinstance(obj,QtGui.QColor):
        obj.default = obj.getRgb()

  
  def getStyleSheet(self):
    with open(STYLE_PATH, 'r') as f:
        styleString = f.read()

    return styleString%("rgba%s"%str(self.TextColor.getRgb()),
                        "rgba%s"%str(self.BgColorDark.getRgb()),
                        "rgba%s"%str(self.BgColorDarker.getRgb()),
                        "rgba%s"%str(self.BgColorBright.getRgb()),
                        "rgba%s"%str(self.MainColor.getRgb()),
                        "rgba%s"%str(self.MainColor_Lighter.getRgb()),
                        "rgba%s"%str(self.MainColor_Lighter.getRgb()),
                        "rgba%s"%str(self.BorderColor.getRgb()),
                        "rgba%s"%str(self.InputFieldColor.getRgb()),
                        "rgba%s"%str(self.InputFieldHover.getRgb()),
                        "rgba%s"%str(self.InputTextSelBg.getRgb()),
                        "rgba%s"%str(self.InputTextSelColor.getRgb()),
                        "rgba%s"%str(self.ScrollBarColor.getRgb()),
                        "rgba%s"%str(self.ButtonG1.getRgb()),
                        "rgba%s"%str(self.ButtonG2.getRgb()),
                        "rgba%s"%str(self.ButtonG3.getRgb()),
                        "rgba%s"%str(self.DropDownIconBg.getRgb())                        
                        )



style = editableStyleSheet()

