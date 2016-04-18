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

#ifndef DYNAMICQMETAOBJECT_H
#define DYNAMICQMETAOBJECT_H

#include "pysidemacros.h"
#include <sbkpython.h>
#include <QMetaObject>
#include <QMetaMethod>

namespace PySide
{

class DynamicQMetaObject : public QMetaObject
{
public:
    DynamicQMetaObject(const char* className, const QMetaObject* metaObject);
    DynamicQMetaObject(PyTypeObject* type, const QMetaObject* metaobject);
    ~DynamicQMetaObject();


    int addMethod(QMetaMethod::MethodType mtype, const char* signature, const char* type);
    void removeMethod(QMetaMethod::MethodType mtype, uint index);
    int addSignal(const char* signal, const char* type = 0);
    int addSlot(const char* slot, const char* type = 0);
    int addProperty(const char* property, PyObject* data);
    void addInfo(const char* key, const char* value);
    void addInfo(QMap<QByteArray, QByteArray> info);

    void removeSignal(uint idex);
    void removeSlot(uint index);
    void removeProperty(uint index);

    const QMetaObject* update() const;

private:
    class DynamicQMetaObjectPrivate;
    DynamicQMetaObjectPrivate* m_d;

    void parsePythonType(PyTypeObject* type);
};


}
#endif
