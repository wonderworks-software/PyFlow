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

#ifndef SBKDBG_H
#define SBKDBG_H

#include "sbkpython.h"
#include "basewrapper.h"
#include <iostream>

#ifndef NOCOLOR
    #define COLOR_END "\033[0m"
    #define COLOR_WHITE "\033[1;37m"
    #define COLOR_YELLOW "\033[1;33m"
    #define COLOR_GREEN "\033[0;32m"
    #define COLOR_RED "\033[0;31m"
#else
    #define COLOR_END ""
    #define COLOR_WHITE ""
    #define COLOR_YELLOW ""
    #define COLOR_GREEN ""
    #define COLOR_RED ""
#endif

#ifndef NDEBUG

class BaseLogger
{
public:
    BaseLogger(std::ostream& output, const char* function, const char* context)
        : m_stream(output), m_function(function), m_context(context) {}
    ~BaseLogger()
    {
        m_stream << std::endl;
    }
    std::ostream& operator()() { return m_stream; };
    template <typename T>
    std::ostream& operator<<(const T& t)
    {
        m_stream << '[';
        if (m_context[0])
            m_stream << COLOR_GREEN << m_context << COLOR_END << "|";
        return m_stream << COLOR_WHITE << m_function << COLOR_END << "] " << t;
    }
private:
    std::ostream& m_stream;
    const char* m_function;
    const char* m_context;
};

inline std::ostream& operator<<(std::ostream& out, PyObject* obj)
{
    PyObject* repr = Shiboken::Object::isValid(obj, false) ? PyObject_Repr(obj) : 0;
    if (repr) {
#ifdef IS_PY3K
        PyObject* str = PyUnicode_AsUTF8String(repr);
        Py_DECREF(repr);
        repr = str;
#endif
        out << PyBytes_AS_STRING(repr);
        Py_DECREF(repr);
    } else {
        out << reinterpret_cast<void*>(obj);
    }
    return out;
}

class _SbkDbg : public BaseLogger
{
public:
    _SbkDbg(const char* function, const char* context = "") : BaseLogger(std::cout, function, context) {}
};

#ifdef __GNUG__
#define SbkDbg(X) _SbkDbg(__PRETTY_FUNCTION__, X"")
#else
#define SbkDbg(X) _SbkDbg(__FUNCTION__, X"")
#endif

#else

struct SbkDbg {
    template <typename T>
    SbkDbg& operator<<(const T&) { return *this; }
};

#endif
#endif // LOGGER_H
