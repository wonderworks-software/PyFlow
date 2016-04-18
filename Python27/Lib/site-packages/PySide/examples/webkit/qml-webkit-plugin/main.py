#!/usr/bin/env python

'''QML PLugin for WebKit.

Adapted from QtLabs[1].

Usage: python main.py index.html

[1] http://blog.qtlabs.org.br/2011/05/30/transformando-o-qml-no-proximo-flash/
'''
import sys

from PySide.QtCore import QUrl
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView
from PySide.QtWebKit import QWebPluginFactory, QWebView, QWebSettings

class PluginFactory(QWebPluginFactory):

    def plugins(self):
        plugins = []

        mime = self.MimeType()
        mime.name = 'QmlFile'
        mime.fileExtensions = ['.qml']

        plugin = self.Plugin()
        plugin.name = 'QmlPlugin'
        plugin.mimeTypes = [mime]

        plugins.append(plugin)

        return plugins

    def create(self, mimeType, url, argumentNames, argumentValues):
        if mimeType != 'application/x-qml':
            return None

        for name, value in zip(argumentNames, argumentValues):
            if name == 'width':
                width = int(value)
            elif name == 'height':
                height = int(value)

        view = QDeclarativeView()
        view.resize(width, height)
        view.setSource(url)

        return view

def main():

    app = QApplication([])

    view = QWebView()
    fac = PluginFactory()
    view.page().setPluginFactory(fac)
    QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)

    view.load(QUrl(sys.argv[1]))

    view.resize(840, 600)
    view.show()

    return app.exec_()
if __name__ == '__main__':
    main()
