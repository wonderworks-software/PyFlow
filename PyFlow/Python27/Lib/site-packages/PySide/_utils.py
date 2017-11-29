# This file is part of PySide: Python for Qt
#
# Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

import sys
import os
import fnmatch


if sys.platform == 'win32':
    # On Windows get the PySide package path in case sensitive format.
    # Even if the file system on Windows is case insensitive,
    # some parts in Qt environment such as qml imports path,
    # requires to be in case sensitive format.
    import ctypes
    from ctypes import POINTER, WinError, sizeof, byref, create_unicode_buffer
    from ctypes.wintypes import MAX_PATH, LPCWSTR, LPWSTR, DWORD

    GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
    GetShortPathNameW.argtypes = [LPCWSTR, LPWSTR, DWORD]
    GetShortPathNameW.restype = DWORD

    GetLongPathNameW = ctypes.windll.kernel32.GetLongPathNameW
    GetLongPathNameW.argtypes = [LPCWSTR, LPWSTR, DWORD]
    GetLongPathNameW.restype = DWORD

    PY_2 = sys.version_info[0] < 3

    if PY_2:
        def u(x):
            return unicode(x)
        def u_fs(x):
            return unicode(x, sys.getfilesystemencoding())
    else:
        def u(x):
            return x
        def u_fs(x):
            return x

    def _get_win32_short_name(s):
        """ Returns short name """
        buf_size = MAX_PATH
        for i in range(2):
            buf = create_unicode_buffer(u('\0') * (buf_size + 1))
            r = GetShortPathNameW(u_fs(s), buf, buf_size)
            if r == 0:
                raise WinError()
            if r < buf_size:
                if PY_2:
                    return buf.value.encode(sys.getfilesystemencoding())
                return buf.value
            buf_size = r
        raise WinError()

    def _get_win32_long_name(s):
        """ Returns long name """
        buf_size = MAX_PATH
        for i in range(2):
            buf = create_unicode_buffer(u('\0') * (buf_size + 1))
            r = GetLongPathNameW(u_fs(s), buf, buf_size)
            if r == 0:
                raise WinError()
            if r < buf_size:
                if PY_2:
                    return buf.value.encode(sys.getfilesystemencoding())
                return buf.value
            buf_size = r
        raise WinError()

    def _get_win32_case_sensitive_name(s):
        """ Returns long name in case sensitive format """
        path = _get_win32_long_name(_get_win32_short_name(s))
        return path

    def get_pyside_dir():
        try:
            from . import QtCore
        except ImportError:
            return _get_win32_case_sensitive_name(os.path.abspath(os.path.dirname(__file__)))
        else:
            return _get_win32_case_sensitive_name(os.path.abspath(os.path.dirname(QtCore.__file__)))

else:
    def get_pyside_dir():
        try:
            from . import QtCore
        except ImportError:
            return os.path.abspath(os.path.dirname(__file__))
        else:
            return os.path.abspath(os.path.dirname(QtCore.__file__))


def _filter_match(name, patterns):
    for pattern in patterns:
        if pattern is None:
            continue
        if fnmatch.fnmatch(name, pattern):
            return True
    return False


def _dir_contains(dir, filter):
    names = os.listdir(dir)
    for name in names:
        srcname = os.path.join(dir, name)
        if not os.path.isdir(srcname) and _filter_match(name, filter):
            return True
    return False


def _rcc_write_number(out, number, width):
    dividend = 1
    if width == 2:
        dividend = 256
    elif width == 3:
        dividend = 65536
    elif width == 4:
        dividend = 16777216
    while dividend >= 1:
        tmp = int(number / dividend)
        out.append("%02x" % tmp)
        number -= tmp * dividend
        dividend = int(dividend / 256)


def _rcc_write_data(out, data):
    _rcc_write_number(out, len(data), 4)
    for d in data:
        _rcc_write_number(out, ord(d), 1)


def _get_qt_conf_resource(prefix, binaries, plugins, imports, translations):
    """
    Generate Qt resource with embedded qt.conf
    """
    qt_conf_template = "\
[Paths]\x0d\x0a\
Prefix = %(prefix)s\x0d\x0a\
Binaries = %(binaries)s\x0d\x0a\
Imports = %(imports)s\x0d\x0a\
Plugins = %(plugins)s\x0d\x0a\
Translations = %(translations)s"

    rc_data_input = qt_conf_template % {"prefix": prefix,
                                        "binaries": binaries,
                                        "plugins": plugins,
                                        "imports": imports,
                                        "translations": translations}
    rc_data_ouput = []
    _rcc_write_data(rc_data_ouput, rc_data_input)

    # The rc_struct and rc_name was pre-generated by pyside-rcc from file:
    # <!DOCTYPE RCC><RCC version="1.0">
    # <qresource>
    #   <file>qt/etc/qt.conf</file>
    # </qresource>
    # </RCC>
    PY_2 = sys.version_info[0] < 3
    if PY_2:
        rc_struct = "\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x0a\x00\x02\x00\x00\
\x00\x01\x00\x00\x00\x03\x00\x00\x00\x16\x00\x00\x00\x00\x00\x01\x00\x00\
\x00\x00"
        rc_name = "\
\x00\x02\x00\x00\x07\x84\x00q\x00t\x00\x03\x00\x00l\xa3\x00e\x00t\x00c\x00\
\x07\x08t\xa6\xa6\x00q\x00t\x00.\x00c\x00o\x00n\x00f"
        rc_data = "".join(rc_data_ouput).decode('hex')
    else:
        rc_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x0a\x00\x02\x00\x00\
\x00\x01\x00\x00\x00\x03\x00\x00\x00\x16\x00\x00\x00\x00\x00\x01\x00\x00\
\x00\x00"
        rc_name = b"\
\x00\x02\x00\x00\x07\x84\x00q\x00t\x00\x03\x00\x00l\xa3\x00e\x00t\x00c\x00\
\x07\x08t\xa6\xa6\x00q\x00t\x00.\x00c\x00o\x00n\x00f"
        rc_data = bytes.fromhex("".join(rc_data_ouput))

    return rc_struct, rc_name, rc_data


def register_qt_conf(prefix, binaries, plugins, imports, translations,
                     force=False):
    """
    Register qt.conf in Qt resource system to override the built-in
    configuration variables, if there is no default qt.conf in
    executable folder and another qt.conf is not already registered in
    Qt resource system.
    """
    try:
        from . import QtCore
    except ImportError:
        return

    # Check folder structure
    if not prefix or not os.path.exists(prefix):
        if force:
            raise RuntimeError("Invalid prefix path specified: %s" % prefix)
        else:
            return
    if not binaries or not os.path.exists(binaries):
        if force:
            raise RuntimeError("Invalid binaries path specified: %s" % binaries)
        else:
            return
    else:
        # Check if required Qt libs exists in binaries folder
        if sys.platform == 'win32':
            pattern = ["QtCore*.dll"]
        else:
            pattern = ["libQtCore.so.*"]
        if not _dir_contains(binaries, pattern):
            if force:
                raise RuntimeError("QtCore lib not found in folder: %s" % \
                    binaries)
            else:
                return
    if not plugins or not os.path.exists(plugins):
        if force:
            raise RuntimeError("Invalid plugins path specified: %s" % plugins)
        else:
            return
    if not imports or not os.path.exists(imports):
        if force:
            raise RuntimeError("Invalid imports path specified: %s" % imports)
        else:
            return
    if not translations or not os.path.exists(translations):
        if force:
            raise RuntimeError("Invalid translations path specified: %s" \
                % translations)
        else:
            return

    # Check if there is no default qt.conf in executable folder
    exec_prefix = os.path.dirname(sys.executable)
    qtconf_path = os.path.join(exec_prefix, 'qt.conf')
    if os.path.exists(qtconf_path) and not force:
        return

    # Check if another qt.conf is not already registered in Qt resource system
    if QtCore.QFile.exists(":/qt/etc/qt.conf") and not force:
        return

    rc_struct, rc_name, rc_data = _get_qt_conf_resource(prefix, binaries,
                                                        plugins, imports,
                                                        translations)
    QtCore.qRegisterResourceData(0x01, rc_struct, rc_name, rc_data)

    # Initialize the Qt library by querying the QLibraryInfo
    prefixPath = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PrefixPath)
