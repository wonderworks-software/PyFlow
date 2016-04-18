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

#ifndef SIGNALMANAGER_H
#define SIGNALMANAGER_H

#include "pysidemacros.h"
#include <sbkpython.h>
#include <Qt>
#include <QStringList>
#include <QMetaMethod>
#include <QMetaType>

class QObject;

namespace PySide
{

/// Thin wrapper for PyObject which increases the reference count at the constructor but *NOT* at destructor.
class PYSIDE_API PyObjectWrapper
{
public:
    PyObjectWrapper();
    PyObjectWrapper(PyObject* me);
    PyObjectWrapper(const PyObjectWrapper &other);
    ~PyObjectWrapper();
    operator PyObject*() const;
    PyObjectWrapper& operator=(const PyObjectWrapper &other);
private:
    PyObject* m_me;
    void*     m_data; //future
};

PYSIDE_API QDataStream &operator<<(QDataStream& out, const PyObjectWrapper& myObj);
PYSIDE_API QDataStream &operator>>(QDataStream& in, PyObjectWrapper& myObj);

class PYSIDE_API SignalManager
{
public:
    static SignalManager& instance();

    QObject* globalReceiver(QObject* sender, PyObject* callback);
    void releaseGlobalReceiver(const QObject* sender, QObject* receiver);
    int globalReceiverSlotIndex(QObject* sender, const char* slotSignature) const;
    void notifyGlobalReceiver(QObject* receiver);

    bool emitSignal(QObject* source, const char* signal, PyObject* args);
    static int qt_metacall(QObject* object, QMetaObject::Call call, int id, void** args);

    // Used to register a new signal/slot on QMetaobject of source.
    static bool registerMetaMethod(QObject* source, const char* signature, QMetaMethod::MethodType type);
    static int registerMetaMethodGetIndex(QObject* source, const char* signature, QMetaMethod::MethodType type);

    // used to discovery metaobject
    static const QMetaObject* retriveMetaObject(PyObject* self);

    // Used to discovery if SignalManager was connected with object "destroyed()" signal.
    int countConnectionsWith(const QObject *object);

    // Disconnect all signals managed by Globalreceiver
    void clear();

    // Utility function to call a python method usign args received in qt_metacall
    static int callPythonMetaMethod(const QMetaMethod& method, void** args, PyObject* obj, bool isShortCuit);

    PYSIDE_DEPRECATED(QObject* globalReceiver());
    PYSIDE_DEPRECATED(void addGlobalSlot(const char* slot, PyObject* callback));
    PYSIDE_DEPRECATED(int addGlobalSlotGetIndex(const char* slot, PyObject* callback));

    PYSIDE_DEPRECATED(void globalReceiverConnectNotify(QObject *sender, int slotIndex));
    PYSIDE_DEPRECATED(void globalReceiverDisconnectNotify(QObject *sender, int slotIndex));
    PYSIDE_DEPRECATED(bool hasConnectionWith(const QObject *object));

private:
    struct SignalManagerPrivate;
    SignalManagerPrivate* m_d;

    SignalManager();
    ~SignalManager();

    // disable copy
    SignalManager(const SignalManager&);
    SignalManager operator=(const SignalManager&);
};

}

Q_DECLARE_METATYPE(PySide::PyObjectWrapper)

#endif
