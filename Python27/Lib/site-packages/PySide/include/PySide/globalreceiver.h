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

#ifndef GLOBALRECEIVER_H
#define GLOBALRECEIVER_H

#include <sbkpython.h>
#include <QObject>
#include <QHash>
#include <QSet>
#include "dynamicqmetaobject.h"

namespace PySide
{

class DynamicSlotData;

class GlobalReceiver : public QObject
{
public:
    GlobalReceiver();
    ~GlobalReceiver();
    int qt_metacall(QMetaObject::Call call, int id, void** args);
    const QMetaObject* metaObject() const;
    int addSlot(const char* slot, PyObject* callback);
    void removeSlot(int slotId);
    void connectNotify(QObject* sender, int slotId);
    void disconnectNotify(QObject* sender, int slotId);
    bool hasConnectionWith(const QObject* object);

protected:
  using QObject::connectNotify;
  using QObject::disconnectNotify;

private:
    DynamicQMetaObject m_metaObject;
    QSet<int> m_shortCircuitSlots;
    QHash<int, DynamicSlotData* > m_slotReceivers;
};

}

#endif

