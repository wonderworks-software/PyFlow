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

#ifndef SHIBOKEN_BUFFER_H
#define SHIBOKEN_BUFFER_H

#include "sbkpython.h"
#include "shibokenmacros.h"

namespace Shiboken
{

namespace Buffer
{
    enum Type {
        ReadOnly,
        WriteOnly,
        ReadWrite
    };

    /**
     * Creates a new Python buffer pointing to a contiguous memory block at
     * \p memory of size \p size.
     */
    LIBSHIBOKEN_API PyObject* newObject(void* memory, Py_ssize_t size, Type type);

    /**
     * Creates a new <b>read only</b> Python buffer pointing to a contiguous memory block at
     * \p memory of size \p size.
     */
    LIBSHIBOKEN_API PyObject* newObject(const void* memory, Py_ssize_t size);

    /**
     * Check if is ok to use \p pyObj as argument in all function under Shiboken::Buffer namespace.
     */
    LIBSHIBOKEN_API bool checkType(PyObject* pyObj);

    /**
     * Returns a pointer to the memory pointed by the buffer \p pyObj, \p size is filled with the buffer
     * size if not null.
     *
     * If the \p pyObj is a non-contiguous buffer a Python error is set.
     */
    LIBSHIBOKEN_API void* getPointer(PyObject* pyObj, Py_ssize_t* size = 0);

} // namespace Buffer
} // namespace Shiboken

#endif
