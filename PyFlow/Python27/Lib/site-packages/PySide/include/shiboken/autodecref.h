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

#ifndef AUTODECREF_H
#define AUTODECREF_H

#include "sbkpython.h"
#include "shibokenmacros.h"

class SbkObject;
namespace Shiboken
{

/**
 *  AutoDecRef holds a PyObject pointer and decrement its reference counter when destroyed.
 */
class LIBSHIBOKEN_API AutoDecRef
{
public:
    /**
     * AutoDecRef constructor.
     * \param pyobj A borrowed reference to a Python object
     */
    explicit AutoDecRef(PyObject* pyObj) : m_pyObj(pyObj) {}
    /**
     * AutoDecRef constructor.
     * \param pyobj A borrowed reference to a Python object
     */
    explicit AutoDecRef(SbkObject* pyObj) : m_pyObj(reinterpret_cast<PyObject*>(pyObj)) {}

    /// Decref the borrowed python reference
    ~AutoDecRef()
    {
        Py_XDECREF(m_pyObj);
    }

    inline bool isNull() const { return m_pyObj == 0; }
    /// Returns the pointer of the Python object being held.
    inline PyObject* object() { return m_pyObj; }
    inline operator PyObject*() { return m_pyObj; }
    inline operator PyTupleObject*() { return reinterpret_cast<PyTupleObject*>(m_pyObj); }
    inline operator bool() const { return m_pyObj; }
    inline PyObject* operator->() { return m_pyObj; }

    template<typename T>
    T cast()
    {
        return reinterpret_cast<T>(m_pyObj);
    }

    /**
     * Decref the current borrowed python reference and take the reference
     * borrowed by \p other, so other.isNull() will return true.
     */
    void operator=(AutoDecRef& other)
    {
        Py_XDECREF(m_pyObj);
        m_pyObj = other.m_pyObj;
        other.m_pyObj = 0;
    }

    /**
     * Decref the current borrowed python reference and borrow \p other.
     */
    void operator=(PyObject* other)
    {
        Py_XDECREF(m_pyObj);
        m_pyObj = other;
    }
private:
    PyObject* m_pyObj;
    AutoDecRef(const AutoDecRef&);
    AutoDecRef& operator=(const AutoDecRef&);
};

} // namespace Shiboken

#endif // AUTODECREF_H

