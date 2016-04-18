import QtQuick 1.1

Rectangle {
    id: root
    width: 300
    height: 300
    color: "red"

    Text {
        text: "Hello World!"
        font.pixelSize: 30
        anchors.centerIn: parent

        NumberAnimation on rotation {
            from: 0
            to: 360
            duration: 2000
            loops: Animation.Infinite
        }
    }
}
