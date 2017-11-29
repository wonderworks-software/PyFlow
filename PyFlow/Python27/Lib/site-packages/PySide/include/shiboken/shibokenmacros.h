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

#ifndef SHIBOKENMACROS_H
#define SHIBOKENMACROS_H

// LIBSHIBOKEN_API macro is used for the public API symbols.
#if defined _WIN32
    #if LIBSHIBOKEN_EXPORTS
        #define LIBSHIBOKEN_API __declspec(dllexport)
    #else
        #ifdef _MSC_VER
            #define LIBSHIBOKEN_API __declspec(dllimport)
        #endif
    #endif
    #define SBK_DEPRECATED(func) __declspec(deprecated) func
#elif __GNUC__ >= 4
    #define LIBSHIBOKEN_API __attribute__ ((visibility("default")))
    #define SBK_DEPRECATED(func) func __attribute__ ((deprecated))
#endif

#ifndef LIBSHIBOKEN_API
    #define LIBSHIBOKEN_API
    #define SBK_DEPRECATED(func) func
#endif

#endif
