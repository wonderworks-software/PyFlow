#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the PySide project.
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation. Please
# review the following information to ensure the GNU Lesser General
# Public License version 2.1 requirements will be met:
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
# #
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA


import os
from PySide.QtGui import QApplication
from PySide.phonon import Phonon

app = QApplication([])
app.setApplicationName('Phonon Video Player')

#file_path = os.path.join(os.path.dirname(__file__), '320x240.ogv')
file_path = os.path.join(os.path.dirname(__file__), 'FolgersCoffe_512kb_mp4_026vbr260.ogv')
media_src = Phonon.MediaSource(file_path)

media_obj = Phonon.MediaObject()
media_obj.setCurrentSource(media_src)

video_widget = Phonon.VideoWidget()
Phonon.createPath(media_obj, video_widget)

audio_out = Phonon.AudioOutput(Phonon.VideoCategory)
Phonon.createPath(media_obj, audio_out)

video_widget.show()

media_obj.play()

app.exec_()

