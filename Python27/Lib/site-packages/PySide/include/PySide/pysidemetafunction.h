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

#ifndef PYSIDE_FUNCTION_H
#define PYSIDE_METAFUNCTION_H

#include <QObject>
#include <QString>
#include <QStringList>

#include <pysidemacros.h>
#include <sbkpython.h>

extern "C"
{
    extern PYSIDE_API PyTypeObject PySideMetaFunctionType;

    struct PySideMetaFunctionPrivate;
    struct PYSIDE_API PySideMetaFunction
    {
        PyObject_HEAD
        PySideMetaFunctionPrivate* d;
    };
}; //extern "C"

namespace PySide { namespace MetaFunction {

/**
 * This function creates a MetaFunction object
 *
 * @param   obj the QObject witch this fuction is part of
 * @param   methodIndex The index of this function on MetaObject
 * @return  Return a new reference of PySideMetaFunction
 **/
PYSIDE_API PySideMetaFunction*  newObject(QObject* obj, int methodIndex);

} //namespace MetaFunction
} //namespace PySide

#endif
