#!/usr/bin/env python

# Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# Contact: PySide Team (pyside@openbossa.org)
#
# This file is part of the examples of PySide: Python for Qt.
#
# You may use this file under the terms of the BSD license as follows:
#
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
#     the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."

from PySide.QtCore import QObject, QUrl, QAbstractListModel, QModelIndex, QThread, QTimer
from PySide.QtCore import Property, Signal, Qt
from PySide import  QtGui, QtDeclarative

import gdata.photos, gdata.photos.service

class Photo(QObject):
    def __init__(self, gPhoto, parent=None):
        super(Photo, self).__init__(parent)
        self._data = gPhoto
        self._thumbnail = gPhoto.media.thumbnail[0]

    def getWidth(self):
        return int(self._thumbnail.width)

    def getHeight(self):
        return int(self._thumbnail.height)

    def getUrl(self):
        return self._thumbnail.url

    def getImageUrl(self):
        return self._data.GetMediaURL()

    onWidthChanged = Signal()
    onHeightChanged = Signal()
    onUrlChanged = Signal()

    width = Property(int, getWidth, notify=onWidthChanged)
    height = Property(int, getHeight, notify=onHeightChanged)
    url = Property(QUrl, getUrl, notify=onUrlChanged)
    imageUrl = Property(QUrl, getImageUrl, notify=onUrlChanged)

class PhotoLoad(QThread):
    def __init__(self, model, parent=None):
        super(PhotoLoad, self).__init__(parent)
        self._model = model

    def run(self):
        self._model._photos = []
        photos = self._model._album._service.GetFeed(self._model._album._data.GetPhotosUri()).entry
        size = 0
        temp = []
        for p in photos:
            temp.append(Photo(p))
            if len(temp) == 3:
                self._model.appendCache(temp)
                temp = []

        self._model.appendCache(temp)
        self._model._done = True


class PhotoListModel(QAbstractListModel):
    URL_ROLE = Qt.UserRole + 1
    IMAGE_URL_ROLE = Qt.UserRole + 2
    HEIGHT_ROLE = Qt.UserRole + 3
    WIDTH_ROLE = Qt.UserRole + 4

    def __init__(self, album, parent=None):
        super(PhotoListModel, self).__init__(parent)
        self._album = album
        self._photos = []
        self._cache = []
        self._done = False
        keys = {}
        keys[PhotoListModel.URL_ROLE] = "url"
        keys[PhotoListModel.IMAGE_URL_ROLE] = "imageUrl"
        keys[PhotoListModel.HEIGHT_ROLE] = "height"
        keys[PhotoListModel.WIDTH_ROLE] = "width"
        self.setRoleNames(keys)
        self._load = PhotoLoad(self)
        self._load.start()
        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.loadCache)
        self._timer.start()

    def rowCount(self, index):
        return len(self._photos)

    def appendCache(self, itens):
        self._cache += itens

    def loadCache(self):
        self.beginInsertRows(QModelIndex(), len(self._photos), len(self._photos) + len(self._cache))
        self._photos += self._cache
        self.endInsertRows()
        self._cache = []
        if self._done:
            self._timer.stop()

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.row() > len(self._photos):
            return None

        img = self._photos[index.row()]
        if role == PhotoListModel.URL_ROLE:
            return img.url
        elif role == PhotoListModel.IMAGE_URL_ROLE:
            return img.imageUrl
        elif role == PhotoListModel.HEIGHT_ROLE:
            return img.height
        elif role == PhotoListModel.WIDTH_ROLE:
            return img.width
        else:
            return None

class Album(QObject):
    def __init__(self, gService, gAlbum, parent=None):
        super(Album, self).__init__(parent)
        self._data = gAlbum
        self._service = gService
        self._photos = None

    def getName(self):
        return self._data.name.text

    def getStatus(self):
        return 0

    def getPhotos(self):
        if not self._photos:
            self._photos = PhotoListModel(self)

        return self._photos

    tag = Property(str, getName)
    status = Property(int, getStatus)
    images = Property(QAbstractListModel, getPhotos)

class AlbumListModel(QAbstractListModel):
    TAG_ROLE = Qt.UserRole + 1
    STATUS_ROLE = TAG_ROLE + 1
    PHOTOS_ROLE = STATUS_ROLE + 1

    def __init__(self, gService, parent=None):
        super(AlbumListModel, self).__init__(parent)
        self._service = gService
        self._albums = []
        keys = {}
        keys[AlbumListModel.TAG_ROLE] = "tag"
        keys[AlbumListModel.STATUS_ROLE] = "status"
        keys[AlbumListModel.PHOTOS_ROLE] = "photos"
        self.setRoleNames(keys)
        self.load()

    def load(self):
        self._albums = []
        albums = self._service.GetUserFeed().entry
        for a in albums:
            self._albums.append(Album(self._service, a))

        return self._albums

    def rowCount(self, index):
        return len(self._albums)

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.row() > len(self._albums):
            return None

        alb = self._albums[index.row()]
        if role == AlbumListModel.TAG_ROLE:
            return alb.tag
        elif role == AlbumListModel.STATUS_ROLE:
            return alb.status
        elif role == AlbumListModel.PHOTOS_ROLE:
            return alb.getPhotos()
        else:
            return None

class Picasa(object):
    def __init__(self, login, password):
        self._data = gdata.photos.service.PhotosService()
        self._data.ClientLogin(login, password)
        self._albumModel = None

    def getAlbumListModel(self):
        if not self._albumModel:
            self._albumModel = AlbumListModel(self._data)
        return self._albumModel

if __name__ == '__main__':
    import sys
    QtGui.QApplication.setGraphicsSystem("raster")
    app = QtGui.QApplication(sys.argv)

    username, ok = QtGui.QInputDialog.getText(None, "Username", "Username:", QtGui.QLineEdit.Normal)

    if not ok:
        print("Must provide a username")
        sys.exit(1)

    password, ok = QtGui.QInputDialog.getText(None, "Password", "Password:", QtGui.QLineEdit.Password)

    if not ok:
        print("Must provide a password")
        sys.exit(1)

    data = Picasa(username, password)

    view = QtDeclarative.QDeclarativeView()
    engine = view.engine()
    engine.quit.connect(app.quit)
    albums = data.getAlbumListModel()
    view.rootContext().setContextProperty("albumModel", albums)
    context = view.rootContext()
    view.setSource(QUrl('photoviewer.qml'))
    view.show()

    sys.exit(app.exec_())
