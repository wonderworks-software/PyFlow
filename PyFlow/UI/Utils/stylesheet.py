from Qt import QtGui,QtWidgets
import inspect
import os
from PyFlow.UI.Utils.Settings import Colors
from PyFlow.Core.Common import clamp
from PyFlow.Core.Common import SingletonDecorator
from collections import defaultdict
# def clamp(val,min_value,max_value):
#     return max(min(val, max_value), min_value)
FILE_DIR = os.path.dirname(__file__)
STYLE_PATH = os.path.join(FILE_DIR,  "style.css") 
 
@SingletonDecorator
class editableStyleSheet():
    def __init__(self):

        self.TextColor = QtGui.QColor(228, 228, 228)

        self.MainColor = QtGui.QColor(215, 128, 26)

        self.BgColorDark = QtGui.QColor(53, 53, 53)
        self.BgColorDarker = QtGui.QColor(50, 50, 50)
        self.BgColorBright = QtGui.QColor(82, 82, 82)

        self.BorderColor = QtGui.QColor(10, 10, 10)

        self.InputFieldColor = QtGui.QColor(32, 32, 32)
        self.InputFieldHover = QtGui.QColor(95, 95, 95)

        self.InputTextSelbg = QtGui.QColor(59, 59, 59)
        self.InputTextSelColor = QtGui.QColor(255, 255, 255)

        self.ButtonsColor = QtGui.QColor(60,60,60)
        self.DropDownButton = QtGui.QColor(0,0,0,100)

        self.storeDeffaults()

    def storeDeffaults(self):
        for name,obj in inspect.getmembers(self):
            if isinstance(obj,QtGui.QColor):
                obj.default = obj.getRgb()

    def serialize(self):
        result = defaultdict(list)
        for name,obj in inspect.getmembers(self):
            if isinstance(obj,QtGui.QColor):        
                result[name].append(obj.getRgb())
        return result

    def loadFromData(self,data):
        for name in data.keys():
            self.setColor(name,data[name][0])

    def setColor(self,name,color):
        if not isinstance(color,QtGui.QColor):
            if isinstance(color,list) and len(color)>=3:
                a = 255
                if len(color)==4:
                    a = color[3]
                color = QtGui.QColor(color[0],color[1],color[2],a)
            else:
                return
        for objname,obj in inspect.getmembers(self):
            if isinstance(obj,QtGui.QColor):
                if objname == name and obj.getRgb() != color.getRgb():
                    obj.setRgb(color.rgba())
                    app = QtWidgets.QApplication.instance()
                    app.setStyleSheet(self.getStyleSheet())
                    for widget in app.allWidgets():
                        widget.update()

    def getStyleSheet(self):
        MainColor_Lighter = QtGui.QColor(self.MainColor)
        MainColor_Lighter.setAlpha(128)     
        ButtonG1 = self.ButtonsColor.lighter(120)
        ButtonG3 = self.ButtonsColor.darker(110)           
        with open(STYLE_PATH, 'r') as f:
            styleString = f.read()
            return styleString%("rgba%s"%str(self.TextColor.getRgb()),
                                "rgba%s"%str(self.BgColorDark.getRgb()),
                                "rgba%s"%str(self.BgColorDarker.getRgb()),
                                "rgba%s"%str(self.BgColorBright.getRgb()),
                                "rgba%s"%str(self.MainColor.getRgb()),
                                "rgba%s"%str(MainColor_Lighter.getRgb()),
                                "rgba%s"%str(MainColor_Lighter.getRgb()),
                                "rgba%s"%str(self.BorderColor.getRgb()),
                                "rgba%s"%str(self.InputFieldColor.getRgb()),
                                "rgba%s"%str(self.InputFieldHover.getRgb()),
                                "rgba%s"%str(self.InputTextSelbg.getRgb()),
                                "rgba%s"%str(self.InputTextSelColor.getRgb()),
                                "rgba%s"%str(ButtonG1.getRgb()),
                                "rgba%s"%str(self.ButtonsColor.getRgb()),
                                "rgba%s"%str(ButtonG3.getRgb()),
                                "rgba%s"%str(self.DropDownButton.getRgb())                        
                                )
    def getSliderStyleSheet(self,name):

        Styles = {"sliderStyleSheetA" : """
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
        """%"rgba%s"%str(self.MainColor.getRgb()),
        "sliderStyleSheetB" : """
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
        """%"rgba%s"%str(self.MainColor.getRgb()),
        "sliderStyleSheetC" : """
        QSlider,QSlider:disabled,QSlider:focus     {
                                  background: qcolor(0,0,0,0);   }

         QSlider::groove:horizontal {
            border: 1px solid #999999;
            background: qcolor(0,0,0,0);
         }
        QSlider::handle:horizontal {
            background:  rgba(100,100,100,255);
            width: 6px;
         }
        """,
        "dragerstyleSheet" : """
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
        "dragerstyleSheetHover" : """
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
        """%"rgba%s"%str(self.MainColor.getRgb()),
        "timeStyleSheet" : """
        QSlider,QSlider:disabled,QSlider:focus     {  
                                  background: qcolor(0,0,0,0);   }
         QSlider::groove:horizontal {
            border: 1px solid #999999;
            background: qcolor(0,0,0,0);
         }
        QSlider::handle:horizontal {
            background:  %s;
            width: 3px;
         } 
        """%"rgba%s"%str(self.MainColor.getRgb())
        }
        return Styles[name]

style = editableStyleSheet()

