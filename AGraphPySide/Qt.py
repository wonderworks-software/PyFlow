"""Minimal Python 2 & 3 shim around all Qt bindings

DOCUMENTATION
    Qt.py was born in the film and visual effects industry to address
    the growing need for the development of software capable of running
    with more than one flavour of the Qt bindings for Python - PySide,
    PySide2, PyQt4 and PyQt5.

    1. Build for one, run with all
    2. Explicit is better than implicit
    3. Support co-existence

    Default resolution order:
        - PySide2
        - PyQt5
        - PySide
        - PyQt4

    Usage:
        >> import sys
        >> from Qt import QtWidgets
        >> app = QtWidgets.QApplication(sys.argv)
        >> button = QtWidgets.QPushButton("Hello World")
        >> button.show()
        >> app.exec_()

    All members of PySide2 are mapped from other bindings, should they exist.
    If no equivalent member exist, it is excluded from Qt.py and inaccessible.
    The idea is to highlight members that exist across all supported binding,
    and guarantee that code that runs on one binding runs on all others.

    For more details, visit https://github.com/mottosso/Qt.py

LICENSE

    See end of file for license (MIT, BSD) information.

"""

import os
import sys
import types
import shutil
import importlib

__version__ = "1.0.0"

# Enable support for `from Qt import *`
__all__ = []

# Flags from environment variables
QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))
QT_PREFERRED_BINDING = os.getenv("QT_PREFERRED_BINDING", "")
QT_SIP_API_HINT = os.getenv("QT_SIP_API_HINT")

# Reference to Qt.py
Qt = sys.modules[__name__]
Qt.QtCompat = types.ModuleType("QtCompat")

"""Common members of all bindings

This is where each member of Qt.py is explicitly defined.
It is based on a "lowest commond denominator" of all bindings;
including members found in each of the 4 bindings.

Find or add excluded members in build_membership.py

"""

_common_members = {
    "QtGui": [
        "QAbstractTextDocumentLayout",
        "QActionEvent",
        "QBitmap",
        "QBrush",
        "QClipboard",
        "QCloseEvent",
        "QColor",
        "QConicalGradient",
        "QContextMenuEvent",
        "QCursor",
        "QDoubleValidator",
        "QDrag",
        "QDragEnterEvent",
        "QDragLeaveEvent",
        "QDragMoveEvent",
        "QDropEvent",
        "QFileOpenEvent",
        "QFocusEvent",
        "QFont",
        "QFontDatabase",
        "QFontInfo",
        "QFontMetrics",
        "QFontMetricsF",
        "QGradient",
        "QHelpEvent",
        "QHideEvent",
        "QHoverEvent",
        "QIcon",
        "QIconDragEvent",
        "QIconEngine",
        "QImage",
        "QImageIOHandler",
        "QImageReader",
        "QImageWriter",
        "QInputEvent",
        "QInputMethodEvent",
        "QIntValidator",
        "QKeyEvent",
        "QKeySequence",
        "QLinearGradient",
        "QMatrix2x2",
        "QMatrix2x3",
        "QMatrix2x4",
        "QMatrix3x2",
        "QMatrix3x3",
        "QMatrix3x4",
        "QMatrix4x2",
        "QMatrix4x3",
        "QMatrix4x4",
        "QMouseEvent",
        "QMoveEvent",
        "QMovie",
        "QPaintDevice",
        "QPaintEngine",
        "QPaintEngineState",
        "QPaintEvent",
        "QPainter",
        "QPainterPath",
        "QPainterPathStroker",
        "QPalette",
        "QPen",
        "QPicture",
        "QPictureIO",
        "QPixmap",
        "QPixmapCache",
        "QPolygon",
        "QPolygonF",
        "QQuaternion",
        "QRadialGradient",
        "QRegExpValidator",
        "QRegion",
        "QResizeEvent",
        "QSessionManager",
        "QShortcutEvent",
        "QShowEvent",
        "QStandardItem",
        "QStandardItemModel",
        "QStatusTipEvent",
        "QSyntaxHighlighter",
        "QTabletEvent",
        "QTextBlock",
        "QTextBlockFormat",
        "QTextBlockGroup",
        "QTextBlockUserData",
        "QTextCharFormat",
        "QTextCursor",
        "QTextDocument",
        "QTextDocumentFragment",
        "QTextFormat",
        "QTextFragment",
        "QTextFrame",
        "QTextFrameFormat",
        "QTextImageFormat",
        "QTextInlineObject",
        "QTextItem",
        "QTextLayout",
        "QTextLength",
        "QTextLine",
        "QTextList",
        "QTextListFormat",
        "QTextObject",
        "QTextObjectInterface",
        "QTextOption",
        "QTextTable",
        "QTextTableCell",
        "QTextTableCellFormat",
        "QTextTableFormat",
        "QTransform",
        "QValidator",
        "QVector2D",
        "QVector3D",
        "QVector4D",
        "QWhatsThisClickedEvent",
        "QWheelEvent",
        "QWindowStateChangeEvent",
        "qAlpha",
        "qBlue",
        "qGray",
        "qGreen",
        "qIsGray",
        "qRed",
        "qRgb",
        "qRgb",
    ],
    "QtWidgets": [
        "QAbstractButton",
        "QAbstractGraphicsShapeItem",
        "QAbstractItemDelegate",
        "QAbstractItemView",
        "QAbstractScrollArea",
        "QAbstractSlider",
        "QAbstractSpinBox",
        "QAction",
        "QActionGroup",
        "QApplication",
        "QBoxLayout",
        "QButtonGroup",
        "QCalendarWidget",
        "QCheckBox",
        "QColorDialog",
        "QColumnView",
        "QComboBox",
        "QCommandLinkButton",
        "QCommonStyle",
        "QCompleter",
        "QDataWidgetMapper",
        "QDateEdit",
        "QDateTimeEdit",
        "QDesktopWidget",
        "QDial",
        "QDialog",
        "QDialogButtonBox",
        "QDirModel",
        "QDockWidget",
        "QDoubleSpinBox",
        "QErrorMessage",
        "QFileDialog",
        "QFileIconProvider",
        "QFileSystemModel",
        "QFocusFrame",
        "QFontComboBox",
        "QFontDialog",
        "QFormLayout",
        "QFrame",
        "QGesture",
        "QGestureEvent",
        "QGestureRecognizer",
        "QGraphicsAnchor",
        "QGraphicsAnchorLayout",
        "QGraphicsBlurEffect",
        "QGraphicsColorizeEffect",
        "QGraphicsDropShadowEffect",
        "QGraphicsEffect",
        "QGraphicsEllipseItem",
        "QGraphicsGridLayout",
        "QGraphicsItem",
        "QGraphicsItemGroup",
        "QGraphicsLayout",
        "QGraphicsLayoutItem",
        "QGraphicsLineItem",
        "QGraphicsLinearLayout",
        "QGraphicsObject",
        "QGraphicsOpacityEffect",
        "QGraphicsPathItem",
        "QGraphicsPixmapItem",
        "QGraphicsPolygonItem",
        "QGraphicsProxyWidget",
        "QGraphicsRectItem",
        "QGraphicsRotation",
        "QGraphicsScale",
        "QGraphicsScene",
        "QGraphicsSceneContextMenuEvent",
        "QGraphicsSceneDragDropEvent",
        "QGraphicsSceneEvent",
        "QGraphicsSceneHelpEvent",
        "QGraphicsSceneHoverEvent",
        "QGraphicsSceneMouseEvent",
        "QGraphicsSceneMoveEvent",
        "QGraphicsSceneResizeEvent",
        "QGraphicsSceneWheelEvent",
        "QGraphicsSimpleTextItem",
        "QGraphicsTextItem",
        "QGraphicsTransform",
        "QGraphicsView",
        "QGraphicsWidget",
        "QGridLayout",
        "QGroupBox",
        "QHBoxLayout",
        "QHeaderView",
        "QInputDialog",
        "QItemDelegate",
        "QItemEditorCreatorBase",
        "QItemEditorFactory",
        "QKeyEventTransition",
        "QLCDNumber",
        "QLabel",
        "QLayout",
        "QLayoutItem",
        "QLineEdit",
        "QListView",
        "QListWidget",
        "QListWidgetItem",
        "QMainWindow",
        "QMdiArea",
        "QMdiSubWindow",
        "QMenu",
        "QMenuBar",
        "QMessageBox",
        "QMouseEventTransition",
        "QPanGesture",
        "QPinchGesture",
        "QPlainTextDocumentLayout",
        "QPlainTextEdit",
        "QProgressBar",
        "QProgressDialog",
        "QPushButton",
        "QRadioButton",
        "QRubberBand",
        "QScrollArea",
        "QScrollBar",
        "QShortcut",
        "QSizeGrip",
        "QSizePolicy",
        "QSlider",
        "QSpacerItem",
        "QSpinBox",
        "QSplashScreen",
        "QSplitter",
        "QSplitterHandle",
        "QStackedLayout",
        "QStackedWidget",
        "QStatusBar",
        "QStyle",
        "QStyleFactory",
        "QStyleHintReturn",
        "QStyleHintReturnMask",
        "QStyleHintReturnVariant",
        "QStyleOption",
        "QStyleOptionButton",
        "QStyleOptionComboBox",
        "QStyleOptionComplex",
        "QStyleOptionDockWidget",
        "QStyleOptionFocusRect",
        "QStyleOptionFrame",
        "QStyleOptionGraphicsItem",
        "QStyleOptionGroupBox",
        "QStyleOptionHeader",
        "QStyleOptionMenuItem",
        "QStyleOptionProgressBar",
        "QStyleOptionRubberBand",
        "QStyleOptionSizeGrip",
        "QStyleOptionSlider",
        "QStyleOptionSpinBox",
        "QStyleOptionTab",
        "QStyleOptionTabBarBase",
        "QStyleOptionTabWidgetFrame",
        "QStyleOptionTitleBar",
        "QStyleOptionToolBar",
        "QStyleOptionToolBox",
        "QStyleOptionToolButton",
        "QStyleOptionViewItem",
        "QStylePainter",
        "QStyledItemDelegate",
        "QSwipeGesture",
        "QSystemTrayIcon",
        "QTabBar",
        "QTabWidget",
        "QTableView",
        "QTableWidget",
        "QTableWidgetItem",
        "QTableWidgetSelectionRange",
        "QTapAndHoldGesture",
        "QTapGesture",
        "QTextBrowser",
        "QTextEdit",
        "QTimeEdit",
        "QToolBar",
        "QToolBox",
        "QToolButton",
        "QToolTip",
        "QTreeView",
        "QTreeWidget",
        "QTreeWidgetItem",
        "QTreeWidgetItemIterator",
        "QUndoCommand",
        "QUndoGroup",
        "QUndoStack",
        "QUndoView",
        "QVBoxLayout",
        "QWhatsThis",
        "QWidget",
        "QWidgetAction",
        "QWidgetItem",
        "QWizard",
        "QWizardPage",
    ],
    "QtCore": [
        "QAbstractAnimation",
        "QAbstractEventDispatcher",
        "QAbstractItemModel",
        "QAbstractListModel",
        "QAbstractState",
        "QAbstractTableModel",
        "QAbstractTransition",
        "QAnimationGroup",
        "QBasicTimer",
        "QBitArray",
        "QBuffer",
        "QByteArray",
        "QByteArrayMatcher",
        "QChildEvent",
        "QCoreApplication",
        "QCryptographicHash",
        "QDataStream",
        "QDate",
        "QDateTime",
        "QDir",
        "QDirIterator",
        "QDynamicPropertyChangeEvent",
        "QEasingCurve",
        "QElapsedTimer",
        "QEvent",
        "QEventLoop",
        "QEventTransition",
        "QFile",
        "QFileInfo",
        "QFileSystemWatcher",
        "QFinalState",
        "QGenericArgument",
        "QGenericReturnArgument",
        "QHistoryState",
        "QIODevice",
        "QLibraryInfo",
        "QLine",
        "QLineF",
        "QLocale",
        "QMargins",
        "QMetaClassInfo",
        "QMetaEnum",
        "QMetaMethod",
        "QMetaObject",
        "QMetaProperty",
        "QMetaType",
        "QMimeData",
        "QModelIndex",
        "QMutex",
        "QMutexLocker",
        "QObject",
        "QParallelAnimationGroup",
        "QPauseAnimation",
        "QPersistentModelIndex",
        "QPluginLoader",
        "QPoint",
        "QPointF",
        "QProcess",
        "QProcessEnvironment",
        "QPropertyAnimation",
        "QReadLocker",
        "QReadWriteLock",
        "QRect",
        "QRectF",
        "QRegExp",
        "QResource",
        "QRunnable",
        "QSemaphore",
        "QSequentialAnimationGroup",
        "QSettings",
        "QSignalMapper",
        "QSignalTransition",
        "QSize",
        "QSizeF",
        "QSocketNotifier",
        "QState",
        "QStateMachine",
        "QSysInfo",
        "QSystemSemaphore",
        "QTemporaryFile",
        "QTextBoundaryFinder",
        "QTextCodec",
        "QTextDecoder",
        "QTextEncoder",
        "QTextStream",
        "QTextStreamManipulator",
        "QThread",
        "QThreadPool",
        "QTime",
        "QTimeLine",
        "QTimer",
        "QTimerEvent",
        "QTranslator",
        "QUrl",
        "QVariantAnimation",
        "QWaitCondition",
        "QWriteLocker",
        "QXmlStreamAttribute",
        "QXmlStreamAttributes",
        "QXmlStreamEntityDeclaration",
        "QXmlStreamEntityResolver",
        "QXmlStreamNamespaceDeclaration",
        "QXmlStreamNotationDeclaration",
        "QXmlStreamReader",
        "QXmlStreamWriter",
        "Qt",
        "QtCriticalMsg",
        "QtDebugMsg",
        "QtFatalMsg",
        "QtMsgType",
        "QtSystemMsg",
        "QtWarningMsg",
        "qAbs",
        "qAddPostRoutine",
        "qChecksum",
        "qCritical",
        "qDebug",
        "qFatal",
        "qFuzzyCompare",
        "qIsFinite",
        "qIsInf",
        "qIsNaN",
        "qIsNull",
        "qRegisterResourceData",
        "qUnregisterResourceData",
        "qVersion",
        "qWarning",
        "qrand",
        "qsrand",
    ],
    "QtXml": [
        "QDomAttr",
        "QDomCDATASection",
        "QDomCharacterData",
        "QDomComment",
        "QDomDocument",
        "QDomDocumentFragment",
        "QDomDocumentType",
        "QDomElement",
        "QDomEntity",
        "QDomEntityReference",
        "QDomImplementation",
        "QDomNamedNodeMap",
        "QDomNode",
        "QDomNodeList",
        "QDomNotation",
        "QDomProcessingInstruction",
        "QDomText",
        "QXmlAttributes",
        "QXmlContentHandler",
        "QXmlDTDHandler",
        "QXmlDeclHandler",
        "QXmlDefaultHandler",
        "QXmlEntityResolver",
        "QXmlErrorHandler",
        "QXmlInputSource",
        "QXmlLexicalHandler",
        "QXmlLocator",
        "QXmlNamespaceSupport",
        "QXmlParseException",
        "QXmlReader",
        "QXmlSimpleReader"
    ],
    "QtHelp": [
        "QHelpContentItem",
        "QHelpContentModel",
        "QHelpContentWidget",
        "QHelpEngine",
        "QHelpEngineCore",
        "QHelpIndexModel",
        "QHelpIndexWidget",
        "QHelpSearchEngine",
        "QHelpSearchQuery",
        "QHelpSearchQueryWidget",
        "QHelpSearchResultWidget"
    ],
    "QtNetwork": [
        "QAbstractNetworkCache",
        "QAbstractSocket",
        "QAuthenticator",
        "QHostAddress",
        "QHostInfo",
        "QLocalServer",
        "QLocalSocket",
        "QNetworkAccessManager",
        "QNetworkAddressEntry",
        "QNetworkCacheMetaData",
        "QNetworkConfiguration",
        "QNetworkConfigurationManager",
        "QNetworkCookie",
        "QNetworkCookieJar",
        "QNetworkDiskCache",
        "QNetworkInterface",
        "QNetworkProxy",
        "QNetworkProxyFactory",
        "QNetworkProxyQuery",
        "QNetworkReply",
        "QNetworkRequest",
        "QNetworkSession",
        "QSsl",
        "QTcpServer",
        "QTcpSocket",
        "QUdpSocket"
    ],
    "QtOpenGL": [
        "QGL",
        "QGLContext",
        "QGLFormat",
        "QGLWidget"
    ]
}


def _apply_site_config():
    try:
        import QtSiteConfig
    except ImportError:
        # If no QtSiteConfig module found, no modifications
        # to _common_members are needed.
        pass
    else:
        # Update _common_members with any changes made by QtSiteConfig
        QtSiteConfig.update_members(_common_members)


def _new_module(name):
    return types.ModuleType(__name__ + "." + name)


def _setup(module, extras):
    """Install common submodules"""

    Qt.__binding__ = module.__name__

    for name in list(_common_members) + extras:
        try:
            # print("Trying %s" % name)
            submodule = importlib.import_module(
                module.__name__ + "." + name)
        except ImportError:
            # print("Failed %s" % name)
            continue

        setattr(Qt, "_" + name, submodule)

        if name not in extras:
            # Store reference to original binding,
            # but don't store speciality modules
            # such as uic or QtUiTools
            setattr(Qt, name, _new_module(name))


def _pyside2():
    """Initialise PySide2

    These functions serve to test the existence of a binding
    along with set it up in such a way that it aligns with
    the final step; adding members from the original binding
    to Qt.py

    """

    import PySide2 as module
    _setup(module, ["QtUiTools"])

    Qt.__binding_version__ = module.__version__

    if hasattr(Qt, "_QtUiTools"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtGui") and hasattr(Qt, "_QtCore"):
        Qt.QtCore.QStringListModel = Qt._QtGui.QStringListModel

    if hasattr(Qt, "_QtWidgets"):
        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtWidgets.QHeaderView.setSectionResizeMode

    if hasattr(Qt, "_QtCore"):
        Qt.__qt_version__ = Qt._QtCore.qVersion()
        Qt.QtCompat.translate = Qt._QtCore.QCoreApplication.translate

        Qt.QtCore.Property = Qt._QtCore.Property
        Qt.QtCore.Signal = Qt._QtCore.Signal
        Qt.QtCore.Slot = Qt._QtCore.Slot

        Qt.QtCore.QAbstractProxyModel = Qt._QtCore.QAbstractProxyModel
        Qt.QtCore.QSortFilterProxyModel = Qt._QtCore.QSortFilterProxyModel
        Qt.QtCore.QItemSelection = Qt._QtCore.QItemSelection
        Qt.QtCore.QItemSelectionRange = Qt._QtCore.QItemSelectionRange
        Qt.QtCore.QItemSelectionModel = Qt._QtCore.QItemSelectionModel


def _pyside():
    """Initialise PySide"""

    import PySide as module
    _setup(module, ["QtUiTools"])

    Qt.__binding_version__ = module.__version__

    if hasattr(Qt, "_QtUiTools"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtGui"):
        setattr(Qt, "QtWidgets", _new_module("QtWidgets"))
        setattr(Qt, "_QtWidgets", Qt._QtGui)

        Qt.QtCompat.setSectionResizeMode = Qt._QtGui.QHeaderView.setResizeMode

        if hasattr(Qt, "_QtCore"):
            Qt.QtCore.QAbstractProxyModel = Qt._QtGui.QAbstractProxyModel
            Qt.QtCore.QSortFilterProxyModel = Qt._QtGui.QSortFilterProxyModel
            Qt.QtCore.QStringListModel = Qt._QtGui.QStringListModel
            Qt.QtCore.QItemSelection = Qt._QtGui.QItemSelection
            Qt.QtCore.QItemSelectionRange = Qt._QtGui.QItemSelectionRange
            Qt.QtCore.QItemSelectionModel = Qt._QtGui.QItemSelectionModel

    if hasattr(Qt, "_QtCore"):
        Qt.__qt_version__ = Qt._QtCore.qVersion()

        Qt.QtCore.Property = Qt._QtCore.Property
        Qt.QtCore.Signal = Qt._QtCore.Signal
        Qt.QtCore.Slot = Qt._QtCore.Slot

        QCoreApplication = Qt._QtCore.QCoreApplication
        Qt.QtCompat.translate = (
            lambda context, sourceText, disambiguation, n:
            QCoreApplication.translate(
                context,
                sourceText,
                disambiguation,
                QCoreApplication.CodecForTr,
                n
            )
        )


def _pyqt5():
    """Initialise PyQt5"""

    import PyQt5 as module
    _setup(module, ["uic"])

    if hasattr(Qt, "_uic"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtWidgets"):
        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtWidgets.QHeaderView.setSectionResizeMode

    if hasattr(Qt, "_QtCore"):
        Qt.QtCompat.translate = Qt._QtCore.QCoreApplication.translate

        Qt.QtCore.Property = Qt._QtCore.pyqtProperty
        Qt.QtCore.Signal = Qt._QtCore.pyqtSignal
        Qt.QtCore.Slot = Qt._QtCore.pyqtSlot

        Qt.QtCore.QAbstractProxyModel = Qt._QtCore.QAbstractProxyModel
        Qt.QtCore.QSortFilterProxyModel = Qt._QtCore.QSortFilterProxyModel
        Qt.QtCore.QStringListModel = Qt._QtCore.QStringListModel
        Qt.QtCore.QItemSelection = Qt._QtCore.QItemSelection
        Qt.QtCore.QItemSelectionModel = Qt._QtCore.QItemSelectionModel
        Qt.QtCore.QItemSelectionRange = Qt._QtCore.QItemSelectionRange

        Qt.__qt_version__ = Qt._QtCore.QT_VERSION_STR
        Qt.__binding_version__ = Qt._QtCore.PYQT_VERSION_STR


def _pyqt4():
    """Initialise PyQt4"""

    import sip

    # Validation of envivornment variable. Prevents an error if
    # the variable is invalid since it's just a hint.
    try:
        hint = int(QT_SIP_API_HINT)
    except TypeError:
        hint = None  # Variable was None, i.e. not set.
    except ValueError:
        raise ImportError("QT_SIP_API_HINT=%s must be a 1 or 2")

    for api in ("QString",
                "QVariant",
                "QDate",
                "QDateTime",
                "QTextStream",
                "QTime",
                "QUrl"):
        try:
            sip.setapi(api, hint or 2)
        except AttributeError:
            raise ImportError("PyQt4 < 4.6 isn't supported by Qt.py")
        except ValueError:
            actual = sip.getapi(api)
            if not hint:
                raise ImportError("API version already set to %d" % actual)
            else:
                # Having provided a hint indicates a soft constraint, one
                # that doesn't throw an exception.
                sys.stderr.write(
                    "Warning: API '%s' has already been set to %d.\n"
                    % (api, actual)
                )

    import PyQt4 as module
    _setup(module, ["uic"])

    if hasattr(Qt, "_uic"):
        Qt.QtCompat.loadUi = _loadUi

    if hasattr(Qt, "_QtGui"):
        setattr(Qt, "QtWidgets", _new_module("QtWidgets"))
        setattr(Qt, "_QtWidgets", Qt._QtGui)

        Qt.QtCompat.setSectionResizeMode = \
            Qt._QtGui.QHeaderView.setResizeMode

        if hasattr(Qt, "_QtCore"):
            Qt.QtCore.QAbstractProxyModel = Qt._QtGui.QAbstractProxyModel
            Qt.QtCore.QSortFilterProxyModel = Qt._QtGui.QSortFilterProxyModel
            Qt.QtCore.QItemSelection = Qt._QtGui.QItemSelection
            Qt.QtCore.QStringListModel = Qt._QtGui.QStringListModel
            Qt.QtCore.QItemSelectionModel = Qt._QtGui.QItemSelectionModel
            Qt.QtCore.QItemSelectionRange = Qt._QtGui.QItemSelectionRange

    if hasattr(Qt, "_QtCore"):
        Qt.__qt_version__ = Qt._QtCore.QT_VERSION_STR
        Qt.__binding_version__ = Qt._QtCore.PYQT_VERSION_STR

        Qt.QtCore.Property = Qt._QtCore.pyqtProperty
        Qt.QtCore.Signal = Qt._QtCore.pyqtSignal
        Qt.QtCore.Slot = Qt._QtCore.pyqtSlot

        QCoreApplication = Qt._QtCore.QCoreApplication
        Qt.QtCompat.translate = (
            lambda context, sourceText, disambiguation, n:
            QCoreApplication.translate(
                context,
                sourceText,
                disambiguation,
                QCoreApplication.CodecForTr,
                n)
        )


def _none():
    """Internal option (used in installer)"""

    Mock = type("Mock", (), {"__getattr__": lambda Qt, attr: None})

    Qt.__binding__ = "None"
    Qt.__qt_version__ = "0.0.0"
    Qt.__binding_version__ = "0.0.0"
    Qt.QtCompat.loadUi = lambda uifile, baseinstance=None: None
    Qt.QtCompat.setSectionResizeMode = lambda *args, **kwargs: None

    for submodule in _common_members.keys():
        setattr(Qt, submodule, Mock())
        setattr(Qt, "_" + submodule, Mock())


def _log(text):
    if QT_VERBOSE:
        sys.stdout.write(text + "\n")


def _loadUi(uifile, baseinstance=None):
    """Dynamically load a user interface from the given `uifile`

    This function calls `uic.loadUi` if using PyQt bindings,
    else it implements a comparable binding for PySide.

    Documentation:
        http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#PyQt5.uic.loadUi

    Arguments:
        uifile (str): Absolute path to Qt Designer file.
        baseinstance (QWidget): Instantiated QWidget or subclass thereof

    Return:
        baseinstance if `baseinstance` is not `None`. Otherwise
        return the newly created instance of the user interface.

    """
    if hasattr(baseinstance, "layout") and baseinstance.layout():
        message = ("QLayout: Attempting to add Layout to %s which "
                   "already has a layout")
        raise RuntimeError(message % (baseinstance))

    if hasattr(Qt, "_uic"):
        return Qt._uic.loadUi(uifile, baseinstance)

    elif hasattr(Qt, "_QtUiTools"):
        # Implement `PyQt5.uic.loadUi` for PySide(2)

        class _UiLoader(Qt._QtUiTools.QUiLoader):
            """Create the user interface in a base instance.

            Unlike `Qt._QtUiTools.QUiLoader` itself this class does not
            create a new instance of the top-level widget, but creates the user
            interface in an existing instance of the top-level class if needed.

            This mimics the behaviour of `PyQt5.uic.loadUi`.

            """

            def __init__(self, baseinstance):
                super(_UiLoader, self).__init__(baseinstance)
                self.baseinstance = baseinstance

            def load(self, uifile, *args, **kwargs):
                from xml.etree.ElementTree import ElementTree

                # For whatever reason, if this doesn't happen then
                # reading an invalid or non-existing .ui file throws
                # a RuntimeError.
                etree = ElementTree()
                etree.parse(uifile)

                widget = Qt._QtUiTools.QUiLoader.load(
                    self, uifile, *args, **kwargs)

                # Workaround for PySide 1.0.9, see issue #208
                widget.parentWidget()

                return widget

            def createWidget(self, class_name, parent=None, name=""):
                """Called for each widget defined in ui file

                Overridden here to populate `baseinstance` instead.

                """

                if parent is None and self.baseinstance:
                    # Supposed to create the top-level widget,
                    # return the base instance instead
                    return self.baseinstance

                # For some reason, Line is not in the list of available
                # widgets, but works fine, so we have to special case it here.
                if class_name in self.availableWidgets() + ["Line"]:
                    # Create a new widget for child widgets
                    widget = Qt._QtUiTools.QUiLoader.createWidget(self,
                                                                  class_name,
                                                                  parent,
                                                                  name)

                else:
                    raise Exception("Custom widget '%s' not supported"
                                    % class_name)

                if self.baseinstance:
                    # Set an attribute for the new child widget on the base
                    # instance, just like PyQt5.uic.loadUi does.
                    setattr(self.baseinstance, name, widget)

                return widget

        widget = _UiLoader(baseinstance).load(uifile)
        Qt.QtCore.QMetaObject.connectSlotsByName(widget)

        return widget

    else:
        raise NotImplementedError("No implementation available for loadUi")


def _convert(lines):
    """Convert compiled .ui file from PySide2 to Qt.py

    Arguments:
        lines (list): Each line of of .ui file

    Usage:
        >> with open("myui.py") as f:
        ..   lines = _convert(f.readlines())

    """

    def parse(line):
        line = line.replace("from PySide2 import", "from Qt import QtCompat,")
        line = line.replace("QtWidgets.QApplication.translate",
                            "QtCompat.translate")
        return line

    parsed = list()
    for line in lines:
        line = parse(line)
        parsed.append(line)

    return parsed


def _cli(args):
    """Qt.py command-line interface"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--convert",
                        help="Path to compiled Python module, e.g. my_ui.py")
    parser.add_argument("--compile",
                        help="Accept raw .ui file and compile with native "
                             "PySide2 compiler.")
    parser.add_argument("--stdout",
                        help="Write to stdout instead of file",
                        action="store_true")
    parser.add_argument("--stdin",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)

    if args.stdout:
        raise NotImplementedError("--stdout")

    if args.stdin:
        raise NotImplementedError("--stdin")

    if args.compile:
        raise NotImplementedError("--compile")

    if args.convert:
        sys.stdout.write("#\n"
                         "# WARNING: --convert is an ALPHA feature.\n#\n"
                         "# See https://github.com/mottosso/Qt.py/pull/132\n"
                         "# for details.\n"
                         "#\n")

        #
        # ------> Read
        #
        with open(args.convert) as f:
            lines = _convert(f.readlines())

        backup = "%s_backup%s" % os.path.splitext(args.convert)
        sys.stdout.write("Creating \"%s\"..\n" % backup)
        shutil.copy(args.convert, backup)

        #
        # <------ Write
        #
        with open(args.convert, "w") as f:
            f.write("".join(lines))

        sys.stdout.write("Successfully converted \"%s\"\n" % args.convert)


def _install():
    # Default order (customise order and content via QT_PREFERRED_BINDING)
    default_order = ("PySide2", "PyQt5", "PySide", "PyQt4")
    preferred_order = list(
        b for b in QT_PREFERRED_BINDING.split(os.pathsep) if b
    )

    order = preferred_order or default_order

    available = {
        "PySide2": _pyside2,
        "PyQt5": _pyqt5,
        "PySide": _pyside,
        "PyQt4": _pyqt4,
        "None": _none
    }

    _log("Order: '%s'" % "', '".join(order))

    # Allow site-level customization of the available modules.
    _apply_site_config()

    found_binding = False
    for name in order:
        _log("Trying %s" % name)

        try:
            available[name]()
            found_binding = True
            break

        except ImportError as e:
            _log("ImportError: %s" % e)

        except KeyError:
            _log("ImportError: Preferred binding '%s' not found." % name)

    if not found_binding:
        # If not binding were found, throw this error
        raise ImportError("No Qt binding were found.")

    # Install individual members
    for name, members in _common_members.items():
        try:
            their_submodule = getattr(Qt, "_%s" % name)
        except AttributeError:
            continue

        our_submodule = getattr(Qt, name)

        # Enable import *
        __all__.append(name)

        # Enable direct import of submodule,
        # e.g. import Qt.QtCore
        sys.modules[__name__ + "." + name] = our_submodule

        for member in members:
            # Accept that a submodule may miss certain members.
            try:
                their_member = getattr(their_submodule, member)
            except AttributeError:
                _log("'%s.%s' was missing." % (name, member))
                continue

            setattr(our_submodule, member, their_member)

    # Backwards compatibility
    Qt.QtCompat.load_ui = Qt.QtCompat.loadUi


_install()

# Setup Binding Enum states
Qt.IsPySide2 = Qt.__binding__ == 'PySide2'
Qt.IsPyQt5 = Qt.__binding__ == 'PyQt5'
Qt.IsPySide = Qt.__binding__ == 'PySide'
Qt.IsPyQt4 = Qt.__binding__ == 'PyQt4'

"""Augment QtCompat

QtCompat contains wrappers and added functionality
to the original bindings, such as the CLI interface
and otherwise incompatible members between bindings,
such as `QHeaderView.setSectionResizeMode`.

"""

Qt.QtCompat._cli = _cli
Qt.QtCompat._convert = _convert

# Enable command-line interface
if __name__ == "__main__":
    _cli(sys.argv[1:])


# The MIT License (MIT)
#
# Copyright (c) 2016-2017 Marcus Ottosson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# In PySide(2), loadUi does not exist, so we implement it
#
# `_UiLoader` is adapted from the qtpy project, which was further influenced
# by qt-helpers which was released under a 3-clause BSD license which in turn
# is based on a solution at:
#
# - https://gist.github.com/cpbotha/1b42a20c8f3eb9bb7cb8
#
# The License for this code is as follows:
#
# qt-helpers - a common front-end to various Qt modules
#
# Copyright (c) 2015, Chris Beaumont and Thomas Robitaille
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the Glue project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Which itself was based on the solution at
#
# https://gist.github.com/cpbotha/1b42a20c8f3eb9bb7cb8
#
# which was released under the MIT license:
#
# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@gmail.com>
# Modifications by Charl Botha <cpbotha@vxlabs.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files
# (the "Software"),to deal in the Software without restriction,
# including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
