/****************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the QtDeclarative module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial Usage
** Licensees holding valid Qt Commercial licenses may use this file in
** accordance with the Qt Commercial License Agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and Nokia.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** In addition, as a special exception, Nokia gives you certain additional
** rights.  These rights are described in the Nokia Qt LGPL Exception
** version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3.0 as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU General Public License version 3.0 requirements will be
** met: http://www.gnu.org/copyleft/gpl.html.
**
** If you have questions regarding the use of this file, please contact
** Nokia at qt-info@nokia.com.
** $QT_END_LICENSE$
**
****************************************************************************/

import Qt 4.7
import "script/script.js" as Script

Package {
    Item { id: stackItem; Package.name: 'stack'; width: 160; height: 153; z: stackItem.PathView.z }
    Item { id: listItem; Package.name: 'list'; width: mainWindow.width + 40; height: 153 }
    Item { id: gridItem; Package.name: 'grid'; width: 160; height: 153 }

    Item {
        width: 160; height: 153

        Item {
            id: photoWrapper

            property double randomAngle: Math.random() * (2 * 6 + 1) - 6
            property double randomAngle2: Math.random() * (2 * 6 + 1) - 6

            x: 0; y: 0; width: 140; height: 133
            z: stackItem.PathView.z; rotation: photoWrapper.randomAngle

            BorderImage {
                anchors {
                    fill: border.visible ? border : placeHolder
                    leftMargin: -6; topMargin: -6; rightMargin: -8; bottomMargin: -8
                }
                source: 'images/box-shadow.png'; smooth: true
                border.left: 10; border.top: 10; border.right: 10; border.bottom: 10
            }
            Rectangle {
                id: placeHolder

                property int w: width
                property int h: height
                property double s: Script.calculateScale(w, h, photoWrapper.width)

                color: 'white'; anchors.centerIn: parent; smooth: true
                width:  w * s; height: h * s; visible: originalImage.status != Image.Ready
                Rectangle {
                    color: "#878787"; smooth: true
                    anchors { fill: parent; topMargin: 3; bottomMargin: 3; leftMargin: 3; rightMargin: 3 }
                }
            }
            Rectangle {
                id: border; color: 'white'; anchors.centerIn: parent; smooth: true
                width: originalImage.paintedWidth + 6; height: originalImage.paintedHeight + 6
                visible: !placeHolder.visible
            }
            BusyIndicator { anchors.centerIn: parent; on: originalImage.status != Image.Ready }
            Image {
                id: originalImage; smooth: true; source: model.url
                fillMode: Image.PreserveAspectFit; width: photoWrapper.width; height: photoWrapper.height
            }
            Image {
                id: hqImage; smooth: true; source: ""; visible: false
                fillMode: Image.PreserveAspectFit; width: photoWrapper.width; height: photoWrapper.height
            }
            Binding {
                target: mainWindow; property: "downloadProgress"; value: hqImage.progress
                when: listItem.ListView.isCurrentItem
            }
            Binding {
                target: mainWindow; property: "imageLoading"
                value: (hqImage.status == Image.Loading) ? 1 : 0; when: listItem.ListView.isCurrentItem
            }
            MouseArea {
                width: originalImage.paintedWidth; height: originalImage.paintedHeight; anchors.centerIn: originalImage
                onClicked: {
                    if (albumWrapper.state == 'inGrid') {
                        gridItem.GridView.view.currentIndex = index;
                        albumWrapper.state = 'fullscreen'
                    } else {
                        gridItem.GridView.view.currentIndex = index;
                        albumWrapper.state = 'inGrid'
                    }
                }
            }

            states: [
            State {
                name: 'stacked'; when: albumWrapper.state == ''
                ParentChange { target: photoWrapper; parent: stackItem; x: 10; y: 10 }
                PropertyChanges { target: photoWrapper; opacity: stackItem.PathView.onPath ? 1.0 : 0.0 }
            },
            State {
                name: 'inGrid'; when: albumWrapper.state == 'inGrid'
                ParentChange { target: photoWrapper; parent: gridItem; x: 10; y: 10; rotation: photoWrapper.randomAngle2 }
            },
            State {
                name: 'fullscreen'; when: albumWrapper.state == 'fullscreen'
                ParentChange {
                    target: photoWrapper; parent: listItem; x: 0; y: 0; rotation: 0
                    width: mainWindow.width; height: mainWindow.height
                }
                PropertyChanges { target: border; opacity: 0 }
                PropertyChanges { target: hqImage; source: listItem.ListView.isCurrentItem ? imageUrl : ""; visible: true }
            }
            ]

            transitions: [
            Transition {
                from: 'stacked'; to: 'inGrid'
                SequentialAnimation {
                    PauseAnimation { duration: 10 * index }
                    ParentAnimation {
                        target: photoWrapper; via: foreground
                        NumberAnimation {
                            target: photoWrapper; properties: 'x,y,rotation,opacity'; duration: 600; easing.type: 'OutQuart'
                        }
                    }
                }
            },
            Transition {
                from: 'inGrid'; to: 'stacked'
                ParentAnimation {
                    target: photoWrapper; via: foreground
                    NumberAnimation { properties: 'x,y,rotation,opacity'; duration: 600; easing.type: 'OutQuart' }
                }
            },
            Transition {
                from: 'inGrid'; to: 'fullscreen'
                SequentialAnimation {
                    PauseAnimation { duration: gridItem.GridView.isCurrentItem ? 0 : 600 }
                    ParentAnimation {
                        target: photoWrapper; via: foreground
                        NumberAnimation {
                            targets: [ photoWrapper, border ]
                            properties: 'x,y,width,height,opacity,rotation'
                            duration: gridItem.GridView.isCurrentItem ? 600 : 1; easing.type: 'OutQuart'
                        }
                    }
                }
            },
            Transition {
                from: 'fullscreen'; to: 'inGrid'
                ParentAnimation {
                    target: photoWrapper; via: foreground
                    NumberAnimation {
                        targets: [ photoWrapper, border ]
                        properties: 'x,y,width,height,rotation,opacity'
                        duration: gridItem.GridView.isCurrentItem ? 600 : 1; easing.type: 'OutQuart'
                    }
                }
            }
            ]
        }
    }
}
