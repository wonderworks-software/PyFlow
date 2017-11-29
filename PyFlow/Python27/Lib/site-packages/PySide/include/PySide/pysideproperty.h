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

#ifndef PYSIDE_PROPERTY_H
#define PYSIDE_PROPERTY_H

#include <pysidemacros.h>
#include <sbkpython.h>
#include <QObject>

extern "C"
{
    extern PYSIDE_API PyTypeObject PySidePropertyType;

    struct PySidePropertyPrivate;
    struct PYSIDE_API PySideProperty
    {
        PyObject_HEAD
        PySidePropertyPrivate* d;
    };
};

namespace PySide { namespace Property {

typedef void (*MetaCallHandler)(PySideProperty*,PyObject*,QMetaObject::Call, void**);

PYSIDE_API bool checkType(PyObject* pyObj);

/// @deprecated Use checkType
PYSIDE_DEPRECATED(PYSIDE_API bool isPropertyType(PyObject* pyObj));

/**
 * This function call set property function and pass value as arg
 * This function does not check the property object type
 *
 * @param   self The property object
 * @param   source The QObject witch has the property
 * @param   value The value to set in property
 * @return  Return 0 if ok or -1 if this function fail
 **/
PYSIDE_API int setValue(PySideProperty* self, PyObject* source, PyObject* value);

/**
 * This function call get property function
 * This function does not check the property object type
 *
 * @param   self The property object
 * @param   source The QObject witch has the property
 * @return  Return the result of property get function or 0 if this fail
 **/
PYSIDE_API PyObject* getValue(PySideProperty* self, PyObject* source);

/**
 * This function return the notify name used on this property
 *
 * @param   self The property object
 * @return  Return a const char with the notify name used
 **/
PYSIDE_API const char* getNotifyName(PySideProperty* self);


/**
 * This function search in the source object for desired property
 *
 * @param   source The QObject object
 * @param   name The property name
 * @return  Return a new reference to property object
 **/
PYSIDE_API PySideProperty* getObject(PyObject* source, PyObject* name);

PYSIDE_API void setMetaCallHandler(PySideProperty* self, MetaCallHandler handler);

PYSIDE_API void setTypeName(PySideProperty* self, const char* typeName);

PYSIDE_API void setUserData(PySideProperty* self, void* data);
PYSIDE_API void* userData(PySideProperty* self);

} //namespace Property
} //namespace PySide

#endif
