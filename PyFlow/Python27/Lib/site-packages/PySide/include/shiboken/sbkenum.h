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

#ifndef SBKENUM_H
#define SBKENUM_H

#include "sbkpython.h"
#include "shibokenmacros.h"

extern "C"
{

extern LIBSHIBOKEN_API PyTypeObject SbkEnumType_Type;
struct SbkObjectType;
struct SbkConverter;

} // extern "C"

namespace Shiboken
{

inline bool isShibokenEnum(PyObject* pyObj)
{
    return Py_TYPE(pyObj->ob_type) == &SbkEnumType_Type;
}

namespace Enum
{
    LIBSHIBOKEN_API bool check(PyObject* obj);
    /**
     *  Creates a new enum type (and its flags type, if any is given)
     *  and registers it to Python and adds it to \p module.
     *  \param module       Module to where the new enum type will be added.
     *  \param name         Name of the enum.
     *  \param fullName     Name of the enum that includes all scope information (e.g.: "module.Enum").
     *  \param cppName      Full qualified C++ name of the enum.
     *  \param flagsType    Optional Python type for the flags associated with the enum.
     *  \return The new enum type or NULL if it fails.
     */
    LIBSHIBOKEN_API PyTypeObject* createGlobalEnum(PyObject* module,
                                                   const char* name,
                                                   const char* fullName,
                                                   const char* cppName,
                                                   PyTypeObject* flagsType = 0);
    /// This function does the same as createGlobalEnum, but adds the enum to a Shiboken type or namespace.
    LIBSHIBOKEN_API PyTypeObject* createScopedEnum(SbkObjectType* scope,
                                                   const char* name,
                                                   const char* fullName,
                                                   const char* cppName,
                                                   PyTypeObject* flagsType = 0);

    /**
     *  Creates a new enum item for a given enum type and adds it to \p module.
     *  \param enumType  Enum type to where the new enum item will be added.
     *  \param module    Module to where the enum type of the new enum item belongs.
     *  \param itemName  Name of the enum item.
     *  \param itemValue Numerical value of the enum item.
     *  \return true if everything goes fine, false if it fails.
     */
    LIBSHIBOKEN_API bool createGlobalEnumItem(PyTypeObject* enumType, PyObject* module, const char* itemName, long itemValue);
    /// This function does the same as createGlobalEnumItem, but adds the enum to a Shiboken type or namespace.
    LIBSHIBOKEN_API bool createScopedEnumItem(PyTypeObject* enumType, SbkObjectType* scope, const char* itemName, long itemValue);

    LIBSHIBOKEN_API PyObject* newItem(PyTypeObject* enumType, long itemValue, const char* itemName = 0);

    /// \deprecated Use 'newTypeWithName'
    SBK_DEPRECATED(LIBSHIBOKEN_API PyTypeObject* newType(const char* name));
    LIBSHIBOKEN_API PyTypeObject* newTypeWithName(const char* name, const char* cppName);
    LIBSHIBOKEN_API const char* getCppName(PyTypeObject* type);

    LIBSHIBOKEN_API long getValue(PyObject* enumItem);
    LIBSHIBOKEN_API PyObject* getEnumItemFromValue(PyTypeObject* enumType, long itemValue);

    /// Sets the enum's type converter.
    LIBSHIBOKEN_API void setTypeConverter(PyTypeObject* enumType, SbkConverter* converter);
    /// Returns the converter assigned to the enum \p type.
    LIBSHIBOKEN_API SbkConverter* getTypeConverter(PyTypeObject* enumType);
}

} // namespace Shiboken

#endif // SKB_PYENUM_H
