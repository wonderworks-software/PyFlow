__all__ = ['QtCore', 'QtGui', 'QtNetwork', 'QtOpenGL', 'QtSql', 'QtSvg', 'QtTest', 'QtWebKit', 'QtScript']
__version__         = "1.2.4"
__version_info__    = (1, 2, 4, "final", 0)


def _setupQtDirectories():
    import sys
    import os
    from . import _utils

    pysideDir = _utils.get_pyside_dir()

    # Register PySide qt.conf to override the built-in
    # configuration variables, if there is no default qt.conf in
    # executable folder
    prefix = pysideDir.replace('\\', '/')
    _utils.register_qt_conf(prefix=prefix,
                            binaries=prefix,
                            plugins=prefix+"/plugins",
                            imports=prefix+"/imports",
                            translations=prefix+"/translations")

    # On Windows add the PySide\openssl folder (if it exists) to the
    # PATH so the SSL DLLs can be found when Qt tries to dynamically
    # load them.  Tell Qt to load them and then reset the PATH.
    if sys.platform == 'win32':
        opensslDir = os.path.join(pysideDir, 'openssl')
        if os.path.exists(opensslDir):
            path = os.environ['PATH']
            try:
                os.environ['PATH'] = opensslDir + os.pathsep + path
                try:
                    from . import QtNetwork
                except ImportError:
                    pass
                else:
                    QtNetwork.QSslSocket.supportsSsl()
            finally:
                os.environ['PATH'] = path

_setupQtDirectories()
