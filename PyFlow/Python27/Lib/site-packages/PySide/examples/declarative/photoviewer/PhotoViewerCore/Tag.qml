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

Flipable {
    id: flipable

    property alias frontLabel: frontButton.label
    property alias backLabel: backButton.label

    property int angle: 0
    property int randomAngle: Math.random() * (2 * 6 + 1) - 6
    property bool flipped: false

    signal frontClicked
    signal backClicked
    signal tagChanged(string tag)

    front: EditableButton {
        id: frontButton; rotation: flipable.randomAngle
        anchors { centerIn: parent; verticalCenterOffset: -20 }
        onClicked: flipable.frontClicked()
        onLabelChanged: flipable.tagChanged(label)
    }

    back: Button {
        id: backButton; tint: "red"; rotation: flipable.randomAngle
        anchors { centerIn: parent; verticalCenterOffset: -20 }
        onClicked: flipable.backClicked()
    }

    transform: Rotation {
        origin.x: flipable.width / 2; origin.y: flipable.height / 2
        axis.x: 0; axis.y: 1; axis.z: 0
        angle: flipable.angle
    }

    states: State {
        name: "back"; when: flipable.flipped
        PropertyChanges { target: flipable; angle: 180 }
    }

    transitions: Transition {
        ParallelAnimation {
            NumberAnimation { properties: "angle"; duration: 400 }
            SequentialAnimation {
                NumberAnimation { target: flipable; property: "scale"; to: 0.8; duration: 200 }
                NumberAnimation { target: flipable; property: "scale"; to: 1.0; duration: 200 }
            }
        }
    }
}
