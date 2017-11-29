/*
 * This file is part of PySide: Python for Qt
 *
 * Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * version 2.1 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 *
 */



#ifndef SBK_QTUITOOLS_PYTHON_H
#define SBK_QTUITOOLS_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Module Includes
#include <pyside_qtgui_python.h>
#include <pyside_qtcore_python.h>
#include <pyside_qtxml_python.h>

// Binded library includes
#include <quiloader.h>
// Conversion Includes - Primitive Types
#include <QStringList>
#include <qabstractitemmodel.h>
#include <QString>
#include <signalmanager.h>
#include <typeresolver.h>
#include <QtConcurrentFilter>

// Conversion Includes - Container Types
#include <QMap>
#include <QStack>
#include <QLinkedList>
#include <QVector>
#include <QSet>
#include <QPair>
#include <pysideconversions.h>
#include <QQueue>
#include <QList>
#include <QMultiMap>

// Type indices
#define SBK_QUILOADER_IDX                                            0
#define SBK_QtUiTools_IDX_COUNT                                      1

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtUiToolsTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtUiToolsTypeConverters;

// Converter indices
#define SBK_QTUITOOLS_QLIST_QOBJECTPTR_IDX                           0 // const QList<QObject * > &
#define SBK_QTUITOOLS_QLIST_QBYTEARRAY_IDX                           1 // QList<QByteArray >
#define SBK_QTUITOOLS_QLIST_QVARIANT_IDX                             2 // QList<QVariant >
#define SBK_QTUITOOLS_QLIST_QSTRING_IDX                              3 // QList<QString >
#define SBK_QTUITOOLS_QMAP_QSTRING_QVARIANT_IDX                      4 // QMap<QString, QVariant >
#define SBK_QtUiTools_CONVERTERS_IDX_COUNT                           5

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QUiLoader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtUiToolsTypes[SBK_QUILOADER_IDX]); }

} // namespace Shiboken

#endif // SBK_QTUITOOLS_PYTHON_H

