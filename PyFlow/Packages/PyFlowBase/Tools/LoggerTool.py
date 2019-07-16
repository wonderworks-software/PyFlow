from nine import str
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QAction, QTextBrowser
from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.ConfigManager import ConfigManager
import sys
import logging
import json
import os
import subprocess


REDIRECT = ConfigManager().getPrefsValue("PREFS", "General/RedirectOutput") == "true"
logger = logging.getLogger(None)

def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

addLoggingLevel('CONSOLEOUTPUT', logging.ERROR + 5)

@SingletonDecorator
class SignalHandler(QtCore.QObject):
    messageWritten = QtCore.Signal(str)
    errorWritten = QtCore.Signal(str)
    warningWritten = QtCore.Signal(str)
    flushSig = QtCore.Signal()
    progressSig = QtCore.Signal(int)
    _stdout = None
    _stderr = None
    text = ""

    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        sys.stdout = self

    def write(self, msg):
        if (not self.signalsBlocked()):
            if msg != '\n':
                self.text = msg
                logger.info(str(msg))

    def flush(self):
        print('flusing from handler')


class QtHandler(logging.Handler):
    def __init__(self, parent):
        logging.Handler.__init__(self)
        self.messageHolder = SignalHandler(parent)

    def emit(self, record):
        if record:
            msj = self.format(record)
            if 'flusing from handler' in msj:
                self.messageHolder.flushSig.emit()
            elif 'bytes Downloaded' in msj:
                nb = int(float(msj.split('(')[-1][:-2]))
                self.messageHolder.progressSig.emit(nb)
                self.messageHolder.messageWritten.emit('%s\n' % msj)
            else:
                if record.levelname in ['ERROR', 'CRITICAL']:
                    self.messageHolder.errorWritten.emit('%s\n' % msj)
                elif record.levelname == 'WARNING':
                    self.messageHolder.warningWritten.emit('%s\n' % msj)
                else:
                    self.messageHolder.messageWritten.emit('%s\n' % msj)


class LoggerTool(DockTool):
    """docstring for NodeBox tool."""

    formater = logging.Formatter("[%(levelname)s %(asctime)s]:   %(message)s", "%H:%M:%S")

    def __init__(self):
        super(LoggerTool, self).__init__()
        self.logView = QTextBrowser()
        self.logView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.logView.setOpenLinks(False)
        self.logView.setReadOnly(True)
        self.logView.setStyleSheet("background-color: %s; Font: 10pt 'Consolas'" %
                                   "rgba%s" % str(editableStyleSheet().LoggerBgColor.getRgb()))
        self.clearAction = QAction("Clear", None)
        self.clearAction.triggered.connect(self.clearView)
        self.logView.addAction(self.clearAction)
        self.logView.anchorClicked.connect(self.anchorClickedMethod)
        self.logView.setTextColor(QtGui.QColor('white'))
        self.setWidget(self.logView)
        #####################################################
        # Sys Output Redirection
        #####################################################
        self.handler = None
        if REDIRECT:
            self.handler = QtHandler(self)
        else:
            self.handler = logging.StreamHandler(sys.stdout)

        self.handler.setFormatter(LoggerTool.formater)
        logger.addHandler(self.handler)

        logger.setLevel(logging.DEBUG)
        sys.excepthook = LoggerTool.exceptHook
        if self.handler and REDIRECT:
            self.handler.messageHolder.messageWritten.connect(
                lambda value: self.logPython(value, 0))
            self.handler.messageHolder.warningWritten.connect(
                lambda value: self.logPython(value, 1))
            self.handler.messageHolder.errorWritten.connect(
                lambda value: self.logPython(value, 2))
            self.handler.messageHolder.flushSig.connect(self.flushPython)
    #####################################################
    # Logger
    #####################################################

    @staticmethod
    def exceptHook(excType, excValue, traceback, logger=logger):
        logger.error(excValue, exc_info=(excType, excValue, traceback))

    def clearView(self, *args):
        self.logView.clear()

    def onDestroy(self):
        try:
            sys.stdout = sys.__stdout__
            self.handler.messageHolder._stdout = None
            self.handler.messageHolder._stderr = None
            self.handler.messageHolder.messageWritten.disconnect()
            self.handler.messageHolder.warningWritten.disconnect()
            self.handler.messageHolder.errorWritten.disconnect()
            self.handler.messageHolder.flushSig.disconnect()
            del self.handler
            self.handler = None
        except:
            pass

    def logPython(self, text, mode=0):
        colorchart = {
            0: 'white',
            1: 'yellow',
            2: 'red'
        }
        for l in text.split('\n'):
            if len(l) > 0:
                splitted = l.split(",")
                if len(splitted) >= 3:
                    if "File" in splitted[0] and "line" in splitted[1] and "in" in splitted[2]:
                        file = splitted[0].split('"')[1]
                        line = splitted[1].split("line ")[1]
                        if os.path.exists(file):
                            file = file.replace("\\", "//")
                            errorLink = """<a href=%s><span style=" text-decoration: underline; color:red;">%s</span></a></p>""" % (
                                str(file + "::%s" % line), l)
                            self.logView.append(errorLink)
                    else:
                        self.logView.append(
                            '<span style=" color:%s;">%s<span>' % (colorchart[mode], l))
                else:
                    self.logView.append(
                        '<span style=" color:%s;">%s<span>' % (colorchart[mode], l))

    def flushPython(self):
        self.logView.moveCursor(QtWidgets.QTextCursor.End,
                                QtWidgets.QTextCursor.MoveAnchor)
        self.logView.moveCursor(QtWidgets.QTextCursor.Up,
                                QtWidgets.QTextCursor.MoveAnchor)
        self.logView.moveCursor(
            QtWidgets.QTextCursor.StartOfLine, QtWidgets.QTextCursor.MoveAnchor)
        self.logView.moveCursor(QtWidgets.QTextCursor.End,
                                QtWidgets.QTextCursor.KeepAnchor)
        self.logView.textCursor().removeSelectedText()

    def loglevelChanged(self, int):
        logger.setLevel(self.loggerLevels[int])

    def anchorClickedMethod(self, url):

        if os.path.exists(url.url().split("::")[0]):
            editCmd = ConfigManager().getPrefsValue("PREFS", "General/EditorCmd")
            editCmd = editCmd.replace("@FILE", url.url().replace("::", ":"))
            subprocess.Popen(editCmd)
        else:
            man = self.pyFlowInstance.graphManager
            node = man.get().findNode(str(url.url()))
            if node:
                self.pyFlowInstance.getCanvas().clearSelection()
                node.getWrapper().setSelected(True)
                self.pyFlowInstance.getCanvas().frameSelectedNodes()

    def update(self):
        self.logView.setStyleSheet("background-color: %s; Font: 10pt 'Consolas'" %
                                   "rgba%s" % str(editableStyleSheet().LoggerBgColor.getRgb()))
        super(LoggerTool, self).update()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":logger.png")

    def onShow(self):
        super(LoggerTool, self).onShow()

    def closeEvent(self, event):
        self.hide()

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.BottomDockWidgetArea

    @staticmethod
    def toolTip():
        return "Logger"

    @staticmethod
    def name():
        return str("Logger")
