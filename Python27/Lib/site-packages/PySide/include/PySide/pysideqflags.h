/*
 * This file is part of the PySide project.
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

#ifndef PYSIDE_QFLAGS_H
#define PYSIDE_QFLAGS_H

#include <sbkpython.h>
#include "pysidemacros.h"


extern "C"
{
    struct PYSIDE_API PySideQFlagsObject {
        PyObject_HEAD
        long ob_value;
    };

    PYSIDE_API PyObject* PySideQFlagsNew(PyTypeObject *type, PyObject *args, PyObject *kwds);
    PYSIDE_API PyObject* PySideQFlagsRichCompare(PyObject *self, PyObject *other, int op);
}


namespace PySide
{
namespace QFlags
{
    /**
     * Creates a new QFlags type.
     */
    PYSIDE_API PyTypeObject* create(const char* name, PyNumberMethods* numberMethods);
    /**
     * Creates a new QFlags instance of type \p type and value \p value.
     */
    PYSIDE_API PySideQFlagsObject* newObject(long value, PyTypeObject* type);
    /**
     * Returns the value held by a QFlag.
     */
    PYSIDE_API long getValue(PySideQFlagsObject* self);
}
}

#endif

