from nine import str
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.ConfigManager import ConfigManager
import sys
import logging
import json
import os
import subprocess
REDIRECT = True

class SygnalHandler(QtCore.QObject):
    messageWritten = QtCore.Signal(str) 
    errorWritten   = QtCore.Signal(str)
    warningWritten = QtCore.Signal(str)
    flushSig = QtCore.Signal()
    progressSig = QtCore.Signal(int)
    _stdout = None
    _stderr = None
    text = ""
    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            if msg != '\n':
                self.text = msg
                logger.info(unicode(msg))
            #self.messageWritten.emit(unicode(msg))
    @staticmethod
    def stdout():
        if ( not SygnalHandler._stdout ):
            SygnalHandler._stdout = SygnalHandler()
            sys.stdout = SygnalHandler._stdout
        return SygnalHandler._stdout
    def flush(self):
        None
        #self.write(self.text)
        print 'flusing from handler'
class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.messageHolder = SygnalHandler()
        self.messageHolder.stdout()
    def emit(self, record):
        if record:
            msj = self.format(record)
            if 'flusing from handler' in msj:
                self.messageHolder.flushSig.emit()
            elif  'bytes Downloaded' in msj:
                nb = int(float(msj.split('(')[-1][:-2]))
                self.messageHolder.progressSig.emit(nb)
                self.messageHolder.messageWritten.emit('%s\n'%msj)
            else:
                if record.levelname in ['ERROR','CRITICAL']:
                    self.messageHolder.errorWritten.emit('%s\n'%msj)
                elif record.levelname == 'WARNING':
                    self.messageHolder.warningWritten.emit('%s\n'%msj)
                else:
                    self.messageHolder.messageWritten.emit('%s\n'%msj)

formater = logging.Formatter("[%(levelname)s %(asctime)s]:   %(message)s","%H:%M:%S")#"[%(levelname)s]: %(message)s")
logger = logging.getLogger(None)

def my_excepthook(excType, excValue, traceback, logger=logger):
    logger.error( excValue,exc_info=(excType, excValue, traceback))


settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat)

class LoggerTool(DockTool):
    """docstring for NodeBox tool."""
    def __init__(self):
        super(LoggerTool, self).__init__()
        self.logView = QtWidgets.QTextBrowser()
        self.logView.setOpenLinks(False)
        self.logView.setReadOnly(True)
        self.logView.setStyleSheet("background-color: %s; Font: 10pt 'Consolas'"%"rgba%s"%str(editableStyleSheet().LoggerBgColor.getRgb()))
        self.logView.anchorClicked.connect(self.anchorClickedMethod)
        self.logView.setTextColor(QtGui.QColor('white'))
        self.setWidget(self.logView)
        #####################################################
        # Sys Output Redirection
        ##################################################### 


        if REDIRECT:
            handler = QtHandler()
        else:
            handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(formater)
        logger.addHandler(handler)


        logger.setLevel(logging.DEBUG)
        sys.excepthook = my_excepthook        
        if handler and REDIRECT:
            handler.messageHolder.messageWritten.connect(lambda value:self.logPython(value,0))
            handler.messageHolder.warningWritten.connect(lambda value:self.logPython(value,1))
            handler.messageHolder.errorWritten.connect(lambda value:self.logPython(value,2))
            handler.messageHolder.flushSig.connect(self.flushPython)       
    #####################################################
    # Logger
    #####################################################    
    def logPython(self,text,mode=0):
        colorchart={
            0:'white',
            1:'yellow',
            2:'red'
        }
        for l in text.split('\n'):
            if len(l)>0:
                splited = l.split(",")
                if len(splited)>=3:
                    if "File" in splited[0] and "line" in splited[1] and "in" in splited[2]:
                        file = splited[0].split('"')[1]
                        line = splited[1].split("line ")[1]
                        #self.logView.append(int(line))
                        if os.path.exists(file):
                            file = file.replace("\\","//")
                            errorLink = """<a href=%s><span style=" text-decoration: underline; color:red;">%s</span></a></p>"""%(str(file+"::%s"%line),l)
                            self.logView.append(errorLink)
                else:
                    self.logView.append('<span style=" color:%s;">%s<span>'%(colorchart[mode],l)) 
    def flushPython(self):
        self.logView.moveCursor( QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.MoveAnchor );
        self.logView.moveCursor( QtWidgets.QTextCursor.Up, QtWidgets.QTextCursor.MoveAnchor );
        self.logView.moveCursor( QtWidgets.QTextCursor.StartOfLine, QtWidgets.QTextCursor.MoveAnchor );
        self.logView.moveCursor( QtWidgets.QTextCursor.End, QtWidgets.QTextCursor.KeepAnchor );
        self.logView.textCursor().removeSelectedText();   
    def loglevelChanged(self,int):
        logger.setLevel(self.logerLevels[int])

    def anchorClickedMethod(self,url):
        
        if os.path.exists(url.url().split("::")[0]):
            editCmd = settings.value("Preferences/General/EditorCmd")
            editCmd = editCmd.replace("@FILE", url.url().replace("::",":"))
            subprocess.Popen(editCmd)
        else:    
            man = self.pyFlowInstance.graphManager
            node = man.get().findNode(str(url.url()))
            if node:
                self.pyFlowInstance.getCanvas().clearSelection()
                node.getWrapper().setSelected(True)
                self.pyFlowInstance.getCanvas().frameSelectedNodes()
    def update(self):
        self.logView.setStyleSheet("background-color: %s; Font: 10pt 'Consolas'"%"rgba%s"%str(editableStyleSheet().LoggerBgColor.getRgb()))
        super(LoggerTool, self).update()
    @staticmethod
    def getIcon():
        return QtGui.QIcon(":node_box_icon.png")

    def onShow(self):
        super(LoggerTool, self).onShow()

    def closeEvent(self, event):
        self.hide()
        pass

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.LeftDockWidgetArea

    @staticmethod
    def toolTip():
        return "Logger"

    @staticmethod
    def name():
        return str("Logger")
    