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

#ifndef PYSIDE_SIGNAL_H
#define PYSIDE_SIGNAL_H

#include <QObject>
#include <QString>
#include <QStringList>

#include <pysidemacros.h>
#include <sbkpython.h>
#include <basewrapper.h>

extern "C"
{
    extern PYSIDE_API PyTypeObject PySideSignalType;
    extern PYSIDE_API PyTypeObject PySideSignalInstanceType;

    // Internal object
    struct PYSIDE_API PySideSignal;

    struct PySideSignalInstancePrivate;
    struct PYSIDE_API PySideSignalInstance
    {
        PyObject_HEAD
        PySideSignalInstancePrivate* d;
    };
}; // extern "C"

namespace PySide {
namespace Signal {

PYSIDE_API bool checkType(PyObject* type);

/**
 * This function creates a Signal object which stays attached to QObject class
 *
 * @param   name of the Signal to be registered on meta object
 * @param   signatures a list of signatures supported by this signal, ended with a NULL pointer
 * @return  Return a new reference to PyObject* of type  PySideSignal
 * @deprecated Use registerSignals
 **/
PYSIDE_DEPRECATED(PYSIDE_API PySideSignal* newObject(const char* name, ...));

/**
 * Register all C++ signals of a QObject on Python type.
 */
PYSIDE_API void registerSignals(SbkObjectType* pyObj, const QMetaObject* metaObject);

/**
 * This function creates a Signal object which stays attached to QObject class based on a list of QMetaMethods
 *
 * @param   source of the Signal to be registered on meta object
 * @param   methods a list of QMetaMethod wich contains the supported signature
 * @return  Return a new reference to PyObject* of type  PySideSignal
 **/
PYSIDE_API PySideSignalInstance* newObjectFromMethod(PyObject* source, const QList<QMetaMethod>& methods);

/**
 * This function initializes the Signal object by creating a PySideSignalInstance
 *
 * @param   self a Signal object used as base to PySideSignalInstance
 * @param   name the name to be used on PySideSignalInstance
 * @param   object the PyObject where the signal will be attached
 * @return  Return a new reference to PySideSignalInstance
 **/
PYSIDE_API PySideSignalInstance* initialize(PySideSignal* signal, PyObject* name, PyObject* object);

/**
 * This function is used to retrieve the object in which the signal is attached
 *
 * @param   self The Signal object
 * @return  Return the internal reference to the parent object of the signal
 **/
PYSIDE_API PyObject* getObject(PySideSignalInstance* signal);

/**
 * This function is used to retrieve the signal signature
 *
 * @param   self The Signal object
 * @return  Return the signal signature
 **/
PYSIDE_API const char* getSignature(PySideSignalInstance* signal);

/**
 * This function is used to retrieve the signal signature
 *
 * @param   self The Signal object
 * @return  Return the signal signature
 **/
PYSIDE_API void updateSourceObject(PyObject* source);

/**
 * @deprecated Use registerSignals
 **/
PYSIDE_DEPRECATED(PYSIDE_API void addSignalToWrapper(SbkObjectType* wrapperType, const char* signalName, PySideSignal* signal));

/**
 * This function verifies if the signature is a QtSignal base on SIGNAL flag
 * @param   signature   The signal signature
 * @return  Return true if this is a Qt Signal, otherwise return false
 **/
PYSIDE_API bool isQtSignal(const char* signature);

/**
 * This function is similar to isQtSignal, however if it fails, it'll raise a Python error instead.
 *
 * @param   signature   The signal signature
 * @return  Return true if this is a Qt Signal, otherwise return false
 **/
PYSIDE_API bool checkQtSignal(const char* signature);

/**
 * This function is used to retrieve the signature base on Signal and receiver callback
 * @param   signature   The signal signature
 * @param   receiver    The QObject which will receive the signal
 * @param   callback    Callback function which will connect to the signal
 * @param   encodeName  Used to specify if the returned signature will be encoded with Qt signal/slot style
 * @return  Return the callback signature
 **/
PYSIDE_API QString getCallbackSignature(const char* signal, QObject* receiver, PyObject* callback, bool encodeName);

/**
 * This function parses the signature and then returns a list of argument types.
 *
 * @param   signature       The signal signature
 * @param   isShortCircuit  If this is a shortCircuit(python<->python) signal
 * @return  Return true if this is a Qt Signal, otherwise return false
 * @todo    replace return type by QList<QByteArray>
 **/
QStringList getArgsFromSignature(const char* signature, bool* isShortCircuit = 0);

} // namespace Signal
} // namespace PySide

#endif
