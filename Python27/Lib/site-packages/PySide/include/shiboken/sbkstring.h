/*
 * This file is part of the Shiboken Python Bindings Generator project.
 *
 * Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#ifndef SBKSTRING_H
#define SBKSTRING_H

#include "sbkpython.h"
#include "shibokenmacros.h"

#if PY_MAJOR_VERSION >= 3
    #define SBK_STR_NAME "unicode"
#else
    #define SBK_STR_NAME "str"
#endif

namespace Shiboken
{
namespace String
{
    LIBSHIBOKEN_API bool check(PyObject* obj);
    LIBSHIBOKEN_API bool checkType(PyTypeObject* obj);
    LIBSHIBOKEN_API bool checkChar(PyObject* obj);
    LIBSHIBOKEN_API bool isConvertible(PyObject* obj);
    LIBSHIBOKEN_API PyObject* fromCString(const char* value);
    LIBSHIBOKEN_API PyObject* fromCString(const char* value, int len);
    LIBSHIBOKEN_API const char* toCString(PyObject* str, Py_ssize_t* len = 0);
    LIBSHIBOKEN_API bool concat(PyObject** val1, PyObject* val2);
    LIBSHIBOKEN_API PyObject* fromFormat(const char* format, ...);
    LIBSHIBOKEN_API PyObject* fromStringAndSize(const char* str, Py_ssize_t size);
    LIBSHIBOKEN_API int compare(PyObject* val1, const char* val2);
    LIBSHIBOKEN_API Py_ssize_t len(PyObject* str);

} // namespace String
} // namespace Shiboken


#endif


