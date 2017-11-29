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

#ifndef TYPERESOLVER_H
#define TYPERESOLVER_H

#include "shibokenmacros.h"
#include "conversions.h"

namespace Shiboken
{

/* To C++ convertion functions. */
template <typename T>
inline void pythonToValueType(PyObject* pyobj, void** data)
{
    *reinterpret_cast<T*>(*data) = Shiboken::Converter<T>::toCpp(pyobj);
}

template <typename T>
inline void pythonToObjectType(PyObject* pyobj, void** data)
{
    *reinterpret_cast<T**>(*data) = Shiboken::Converter<T*>::toCpp(pyobj);
}

template <typename T>
inline PyObject* objectTypeToPython(void* cptr)
{
    return Shiboken::Converter<T*>::toPython(*reinterpret_cast<T**>(cptr));
}

template <typename T>
inline PyObject* referenceTypeToPython(void* cptr)
{
    // cptr comes the same way it come when we have a value type, but
    // we deliver a Python object of a reference
    return Shiboken::Converter<T&>::toPython(*reinterpret_cast<T*>(cptr));
}

/**
*   \internal This function is not part of the public API.
*   Initialize the TypeResource internal cache.
*/
void initTypeResolver();

class LIBSHIBOKEN_API TypeResolver
{
public:
    enum Type
    {
        ObjectType,
        ValueType,
        UnknownType
    };

    typedef PyObject* (*CppToPythonFunc)(void*);
    typedef void (*PythonToCppFunc)(PyObject*, void**);

    ~TypeResolver();

    template<typename T>
    static TypeResolver* createValueTypeResolver(const char* typeName)
    {
        return createTypeResolver(typeName, &Shiboken::Converter<T>::toPython, &pythonToValueType<T>, SbkType<T>());
    }

    template<typename T>
    static TypeResolver* createObjectTypeResolver(const char* typeName)
    {
        return createTypeResolver(typeName, &objectTypeToPython<T>, &pythonToObjectType<T>, SbkType<T>());
    }

    /**
     * This kind of type resolver is used only when we have a signal with a reference in their arguments
     * like on QSqlTableModel::primeInsert.
     */
    template<typename T>
    static TypeResolver* createReferenceTypeResolver(const char* typeName)
    {
        return createTypeResolver(typeName, &referenceTypeToPython<T>, &pythonToValueType<T>, SbkType<T>());
    }

    static Type getType(const char* name);
    static TypeResolver* get(const char* typeName);

    PyObject* toPython(void* cppObj);
    void toCpp(PyObject* pyObj, void** place);
    PyTypeObject* pythonType();

private:
    struct TypeResolverPrivate;
    TypeResolverPrivate* m_d;

    TypeResolver();
    // disable object copy
    TypeResolver(const TypeResolver&);
    TypeResolver& operator=(const TypeResolver&);

    static TypeResolver* createTypeResolver(const char* typeName, CppToPythonFunc cppToPy, PythonToCppFunc pyToCpp, PyTypeObject* pyType);
};
}

#endif
