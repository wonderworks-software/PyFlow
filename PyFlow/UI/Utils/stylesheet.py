from Qt import QtGui, QtWidgets, QtCore
import inspect
import json
import os
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.ConfigManager import ConfigManager

from collections import defaultdict
# def clamp(val,min_value,max_value):
#     return max(min(val, max_value), min_value)
FILE_DIR = os.path.dirname(__file__)
STYLE_PATH = os.path.join(FILE_DIR, "style.css")
THEMES_PATH = os.path.join(os.path.dirname(FILE_DIR), "Themes")


class Colors:
    AbsoluteBlack = QtGui.QColor(0, 0, 0, 255)
    DarkGray = QtGui.QColor(60, 60, 60)
    DirtyPen = QtGui.QColor(250, 250, 250, 200)
    Gray = QtGui.QColor(110, 110, 110)
    Green = QtGui.QColor(96, 169, 23, 255)
    NodeBackgrounds = QtGui.QColor(40, 40, 40, 200)
    NodeNameRectBlue = QtGui.QColor(28, 74, 149, 200)
    NodeNameRectGreen = QtGui.QColor(74, 124, 39, 200)
    NodeSelectedPenColor = QtGui.QColor(200, 200, 200, 150)
    Red = QtGui.QColor(255, 0, 0, 255)
    White = QtGui.QColor(255, 255, 255, 200)
    Yellow = QtGui.QColor(255, 211, 25)


@SingletonDecorator
class editableStyleSheet():
    def __init__(self):

        self.TextColor = QtGui.QColor(228, 228, 228)

        self.MainColor = QtGui.QColor(215, 128, 26)

        self.BgColor = QtGui.QColor(53, 53, 53)
        self.BgColorDarker = QtGui.QColor(50, 50, 50)
        self.BgColorBright = QtGui.QColor(82, 82, 82)
        self.BorderColor = QtGui.QColor(10, 10, 10)

        self.LoggerBgColor = QtGui.QColor(35, 35, 35)

        self.InputFieldColor = QtGui.QColor(32, 32, 32)
        self.TextSelectedColor = QtGui.QColor(255, 255, 255)

        self.ButtonsColor = QtGui.QColor(60, 60, 60)

        self.CanvasBgColor = QtGui.QColor(35, 35, 35)
        self.CanvasGridColor = QtGui.QColor(20, 20, 20, 100)
        self.CanvasGridColorDarker = QtGui.QColor(20, 20, 20)
        self.GridSizeFine = [10]
        self.GridSizeHuge = [100]
        self.DrawNumbers = [0]
        self.SetAppStyleSheet = [1]

        self.storeDeffaults()
        self.presests = {}
        self.loadPresests(THEMES_PATH)
        try:
            themeName = ConfigManager().getPrefsValue("PREFS", "Theme/Theme_Name")
            if themeName:
                self.loadFromData(self.presests[themeName])
        except:
            pass

    def storeDeffaults(self):
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QtGui.QColor):
                obj.default = obj.getRgb()

    def serialize(self):
        result = defaultdict(list)
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QtGui.QColor):
                result[name].append(obj.getRgb())
            elif isinstance(obj, list):
                result[name].append(obj)

        return {"PyFLowStyleSheet": result}

    def loadPresests(self, folder):
        self.presests = {}
        for file in os.listdir(folder):
            name, _type = os.path.splitext(file)
            if _type == ".json":
                with open(os.path.join(folder, file), "r") as f:
                    try:
                        data = json.load(f)
                        self.presests[name] = data
                    except:
                        pass

    def loadFromData(self, data):
        if list(data.keys())[0] == "PyFLowStyleSheet":
            data = data["PyFLowStyleSheet"]
            for name in data.keys():
                if isinstance(data[name], list):
                    self.setColor(name, data[name][0])
            self.updateApp()

    def setColor(self, name, color, update=False):
        value = color
        if not isinstance(color, QtGui.QColor):
            if isinstance(color, list) and len(color) >= 3:
                a = 255
                if len(color) == 4:
                    a = color[3]
                color = QtGui.QColor(color[0], color[1], color[2], a)
        for objname, obj in inspect.getmembers(self):
            if objname == name:
                if isinstance(obj, QtGui.QColor):
                    obj.setRgba(color.rgba())
                elif isinstance(obj, list):
                    if isinstance(value, list):
                        value = value[0]
                    obj[0] = value
                if update:
                    self.updateApp()

    def updateApp(self):
        """calls update method all widgets in the app and calls app.setStyleSheet
        """
        if self.SetAppStyleSheet[0] > 0:
            app = QtWidgets.QApplication.instance()
            if app:
                app.setStyleSheet(self.getStyleSheet())
                for widget in app.allWidgets():
                    widget.update()

    def getStyleSheet(self):
        MainColor_Lighter = QtGui.QColor(self.MainColor)
        MainColor_Lighter.setAlpha(128)
        ButtonG1 = self.ButtonsColor.lighter(120)
        ButtonG3 = self.ButtonsColor.darker(110)
        InputFieldHover = self.InputFieldColor.lighter(200)
        with open(STYLE_PATH, 'r') as f:
            styleString = f.read()
            return styleString % ("rgba%s" % str(self.TextColor.getRgb()),
                                  "rgba%s" % str(self.BgColor.getRgb()),
                                  "rgba%s" % str(self.BgColorDarker.getRgb()),
                                  "rgba%s" % str(self.BgColorBright.getRgb()),
                                  "rgba%s" % str(self.MainColor.getRgb()),
                                  "rgba%s" % str(MainColor_Lighter.getRgb()),
                                  "rgba%s" % str(MainColor_Lighter.getRgb()),
                                  "rgba%s" % str(self.BorderColor.getRgb()),
                                  "rgba%s" % str(
                                      self.InputFieldColor.getRgb()),
                                  "rgba%s" % str(InputFieldHover.getRgb()),
                                  "rgba%s" % str(MainColor_Lighter.getRgb()),
                                  "rgba%s" % str(
                                      self.TextSelectedColor.getRgb()),
                                  "rgba%s" % str(ButtonG1.getRgb()),
                                  "rgba%s" % str(self.ButtonsColor.getRgb()),
                                  "rgba%s" % str(ButtonG3.getRgb()),
                                  "rgba%s" % str(QtGui.QColor(
                                      0, 0, 0, 100).getRgb())
                                  )

    def getSliderStyleSheet(self, name):

        Styles = {
            "sliderStyleSheetA": """
        QWidget{
            border: 1.25 solid black;
        }
        QSlider::groove:horizontal,
            QSlider::sub-page:horizontal {
            background: %s;
        }
        QSlider::add-page:horizontal,
            QSlider::sub-page:horizontal:disabled {
            background: rgb(32, 32, 32);
        }
        QSlider::add-page:horizontal:disabled {
            background: grey;
        }
        QSlider::handle:horizontal {
            width: 1px;
         }
        """ % "rgba%s" % str(self.MainColor.getRgb()),
            "sliderStyleSheetB": """
        QSlider::groove:horizontal {
            border: 1px solid #bbb;
            background: white;
            height: 3px;
            border-radius: 2px;
        }
        QSlider::sub-page:horizontal {
            background: %s;
            border: 0px solid #777;
            height: 3px;
            border-radius: 2px;
        }
        QSlider::add-page:horizontal {
            background: #fff;
            border: 1px solid #777;
            height: 3px;
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #eee, stop:1 #ccc);
            border: 1px solid #777;
            width: 4px;
            margin-top: -8px;
            margin-bottom: -8px;
            border-radius: 2px;
            height : 10px;
        }
        QSlider::handle:horizontal:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #fff, stop:1 #ddd);
            border: 1px solid #444;
            border-radius: 2px;
        }
        QSlider::sub-page:horizontal:disabled {
            background: #bbb;
            border-color: #999;
        }

        QSlider::add-page:horizontal:disabled {
            background: #eee;
            border-color: #999;
        }
        QSlider::handle:horizontal:disabled {
            background: #eee;
            border: 1px solid #aaa;
            border-radius: 2px;
            height : 10;
        }
        """ % "rgba%s" % str(self.MainColor.getRgb()),
            "sliderStyleSheetC": """
        QSlider,QSlider:disabled,QSlider:focus{
                                  background: qcolor(0,0,0,0);   }

         QSlider::groove:horizontal {
            border: 1px solid #999999;
            background: qcolor(0,0,0,0);
         }
        QSlider::handle:horizontal {
            background:  rgba(255, 255, 255, 150);
            width: 10px;
            border-radius: 4px;
            border: 1.5px solid black;
         }
         QSlider::handle:horizontal:hover {
            border: 2.25px solid %s;
         }
        """ % "rgba%s" % str(self.MainColor.getRgb()),
            "dragerstyleSheet": """
        QGroupBox{
            border: 0.5 solid darkgrey;
            background : black;
            color: white;
        }
        QLabel{
            background: transparent;
            border: 0 solid transparent;
            color: white;
        }
        """,
            "dragerstyleSheetHover": """
        QGroupBox{
            border: 0.5 solid darkgrey;
            background : %s;
            color: white;
        }
        QLabel{
            background: transparent;
            border: 0 solid transparent;
            color: white;
        }
        """ % "rgba%s" % str(self.MainColor.getRgb()),
            "timeStyleSheet": """
        QSlider,QSlider:disabled,QSlider:focus{  
                                  background: qcolor(0,0,0,0);   }
         QSlider::groove:horizontal {
            border: 1px solid #999999;
            background: qcolor(0,0,0,0);
         }
        QSlider::handle:horizontal {
            background:  %s;
            width: 3px;
         } 
        """ % "rgba%s" % str(self.MainColor.getRgb())
        }
        return Styles[name]
