TEMPLATE = app
LANGUAGE = C++
TARGET         = assistant

CONFIG        += qt warn_on
QT            += xml network

PROJECTNAME        = Assistant
DESTDIR            = ../../bin

FORMS += finddialog.ui \
        helpdialog.ui \
        mainwindow.ui \
        settingsdialog.ui \
        tabbedbrowser.ui \
        topicchooser.ui

SOURCES += main.cpp \
        helpwindow.cpp \
        topicchooser.cpp \
        docuparser.cpp \
        settingsdialog.cpp \
        index.cpp \
        profile.cpp \
        config.cpp \
        finddialog.cpp \
        helpdialog.cpp \
        mainwindow.cpp \
        tabbedbrowser.cpp

HEADERS        += helpwindow.h \
        topicchooser.h \
        docuparser.h \
        settingsdialog.h \
        index.h \
        profile.h \
        finddialog.h \
        helpdialog.h \
        mainwindow.h \
        tabbedbrowser.h \
        config.h

RESOURCES += assistant.qrc

DEFINES += QT_KEYWORDS
#DEFINES +=  QT_PALMTOPCENTER_DOCS
!network:DEFINES        += QT_INTERNAL_NETWORK
else:QT += network
!xml: DEFINES                += QT_INTERNAL_XML
else:QT += xml
include( ../../src/qt_professional.pri )

win32 {
    LIBS += -lshell32
    RC_FILE = assistant.rc
}

mac {
    ICON = assistant.icns
    TARGET = assistant
#    QMAKE_INFO_PLIST = Info_mac.plist
}

#target.path = $$[QT_INSTALL_BINS]
#INSTALLS += target

#assistanttranslations.files = *.qm
#assistanttranslations.path = $$[QT_INSTALL_TRANSLATIONS]
#INSTALLS += assistanttranslations

TRANSLATIONS        = assistant_de.ts \
                  assistant_fr.ts


unix:!contains(QT_CONFIG, zlib):LIBS += -lz


target.path=$$[QT_INSTALL_BINS]
INSTALLS += target
