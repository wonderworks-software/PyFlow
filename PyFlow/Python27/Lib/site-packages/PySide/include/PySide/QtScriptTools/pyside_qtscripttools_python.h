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



#ifndef SBK_QTSCRIPTTOOLS_PYTHON_H
#define SBK_QTSCRIPTTOOLS_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Module Includes
#include <pyside_qtscript_python.h>
#include <pyside_qtcore_python.h>
#include <pyside_qtgui_python.h>

// Binded library includes
#include <qscriptenginedebugger.h>
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
#define SBK_QSCRIPTENGINEDEBUGGER_IDX                                0
#define SBK_QSCRIPTENGINEDEBUGGER_DEBUGGERWIDGET_IDX                 3
#define SBK_QSCRIPTENGINEDEBUGGER_DEBUGGERACTION_IDX                 1
#define SBK_QSCRIPTENGINEDEBUGGER_DEBUGGERSTATE_IDX                  2
#define SBK_QtScriptTools_IDX_COUNT                                  4

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtScriptToolsTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtScriptToolsTypeConverters;

// Converter indices
#define SBK_QTSCRIPTTOOLS_QLIST_QOBJECTPTR_IDX                       0 // const QList<QObject * > &
#define SBK_QTSCRIPTTOOLS_QLIST_QBYTEARRAY_IDX                       1 // QList<QByteArray >
#define SBK_QTSCRIPTTOOLS_QLIST_QVARIANT_IDX                         2 // QList<QVariant >
#define SBK_QTSCRIPTTOOLS_QLIST_QSTRING_IDX                          3 // QList<QString >
#define SBK_QTSCRIPTTOOLS_QMAP_QSTRING_QVARIANT_IDX                  4 // QMap<QString, QVariant >
#define SBK_QtScriptTools_CONVERTERS_IDX_COUNT                       5

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QScriptEngineDebugger::DebuggerWidget >() { return SbkPySide_QtScriptToolsTypes[SBK_QSCRIPTENGINEDEBUGGER_DEBUGGERWIDGET_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptEngineDebugger::DebuggerAction >() { return SbkPySide_QtScriptToolsTypes[SBK_QSCRIPTENGINEDEBUGGER_DEBUGGERACTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptEngineDebugger::DebuggerState >() { return SbkPySide_QtScriptToolsTypes[SBK_QSCRIPTENGINEDEBUGGER_DEBUGGERSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptEngineDebugger >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptToolsTypes[SBK_QSCRIPTENGINEDEBUGGER_IDX]); }

} // namespace Shiboken

#endif // SBK_QTSCRIPTTOOLS_PYTHON_H

