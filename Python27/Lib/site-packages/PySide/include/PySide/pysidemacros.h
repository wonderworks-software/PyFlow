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

#ifndef PYSIDEMACROS_H
#define PYSIDEMACROS_H

#if defined _WIN32
    #if PYSIDE_EXPORTS
        #define PYSIDE_API __declspec(dllexport)
    #else
        #if defined __MINGW32__
            #define PYSIDE_API
        #else
            #define PYSIDE_API __declspec(dllimport)
        #endif
    #endif
    #define PYSIDE_DEPRECATED(func) __declspec(deprecated) func
#else
    #if __GNUC__ >= 4
        #define PYSIDE_API __attribute__ ((visibility("default")))
        #define PYSIDE_DEPRECATED(func) func __attribute__ ((deprecated))
    #else
        #define PYSIDE_API
        #define PYSIDE_DEPRECATED(func) func
    #endif
#endif

#endif
