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



#ifndef SBK_QTSCRIPT_PYTHON_H
#define SBK_QTSCRIPT_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Module Includes
#include <pyside_qtcore_python.h>

// Binded library includes
#include <qscriptvalueiterator.h>
#include <qscriptclass.h>
#include <qscriptvalue.h>
#include <qscriptcontext.h>
#include <qscriptprogram.h>
#include <qscriptextensioninterface.h>
#include <qscriptengineagent.h>
#include <qscriptclasspropertyiterator.h>
#include <qscriptextensionplugin.h>
#include <qscriptengine.h>
#include <qscriptcontextinfo.h>
#include <qscriptable.h>
#include <qscriptstring.h>
// Conversion Includes - Primitive Types
#include <QString>
#include <signalmanager.h>
#include <typeresolver.h>
#include <QtConcurrentFilter>
#include <QStringList>
#include <qabstractitemmodel.h>

// Conversion Includes - Container Types
#include <QList>
#include <QMap>
#include <QStack>
#include <QMultiMap>
#include <QVector>
#include <QPair>
#include <pysideconversions.h>
#include <QSet>
#include <QQueue>
#include <QLinkedList>

// Type indices
#define SBK_QSCRIPTCONTEXT_IDX                                       7
#define SBK_QSCRIPTCONTEXT_EXECUTIONSTATE_IDX                        9
#define SBK_QSCRIPTCONTEXT_ERROR_IDX                                 8
#define SBK_QSCRIPTVALUEITERATOR_IDX                                 25
#define SBK_QSCRIPTENGINEAGENT_IDX                                   15
#define SBK_QSCRIPTENGINEAGENT_EXTENSION_IDX                         16
#define SBK_QSCRIPTCLASS_IDX                                         3
#define SBK_QSCRIPTCLASS_QUERYFLAG_IDX                               5
#define SBK_QSCRIPTCLASS_EXTENSION_IDX                               4
#define SBK_QSCRIPTPROGRAM_IDX                                       19
#define SBK_QSCRIPTSTRING_IDX                                        20
#define SBK_QSCRIPTCONTEXTINFO_IDX                                   10
#define SBK_QSCRIPTCONTEXTINFO_FUNCTIONTYPE_IDX                      11
#define SBK_QSCRIPTCLASSPROPERTYITERATOR_IDX                         6
#define SBK_QSCRIPTVALUE_IDX                                         21
#define SBK_QSCRIPTVALUE_RESOLVEFLAG_IDX                             23
#define SBK_QFLAGS_QSCRIPTVALUE_RESOLVEFLAG__IDX                     2
#define SBK_QSCRIPTVALUE_PROPERTYFLAG_IDX                            22
#define SBK_QFLAGS_QSCRIPTVALUE_PROPERTYFLAG__IDX                    1
#define SBK_QSCRIPTVALUE_SPECIALVALUE_IDX                            24
#define SBK_QSCRIPTABLE_IDX                                          26
#define SBK_QSCRIPTEXTENSIONINTERFACE_IDX                            17
#define SBK_QSCRIPTEXTENSIONPLUGIN_IDX                               18
#define SBK_QSCRIPTENGINE_IDX                                        12
#define SBK_QSCRIPTENGINE_VALUEOWNERSHIP_IDX                         14
#define SBK_QSCRIPTENGINE_QOBJECTWRAPOPTION_IDX                      13
#define SBK_QFLAGS_QSCRIPTENGINE_QOBJECTWRAPOPTION__IDX              0
#define SBK_QtScript_IDX_COUNT                                       27

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtScriptTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtScriptTypeConverters;

// Converter indices
#define SBK_QTSCRIPT_QLIST_QSCRIPTVALUE_IDX                          0 // QList<QScriptValue >
#define SBK_QTSCRIPT_QLIST_QOBJECTPTR_IDX                            1 // const QList<QObject * > &
#define SBK_QTSCRIPT_QLIST_QBYTEARRAY_IDX                            2 // QList<QByteArray >
#define SBK_QTSCRIPT_QLIST_QVARIANT_IDX                              3 // QList<QVariant >
#define SBK_QTSCRIPT_QLIST_QSTRING_IDX                               4 // QList<QString >
#define SBK_QTSCRIPT_QMAP_QSTRING_QVARIANT_IDX                       5 // QMap<QString, QVariant >
#define SBK_QtScript_CONVERTERS_IDX_COUNT                            6

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QScriptContext::ExecutionState >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTCONTEXT_EXECUTIONSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptContext::Error >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTCONTEXT_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptContext >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTCONTEXT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptValueIterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTVALUEITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptEngineAgent::Extension >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTENGINEAGENT_EXTENSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptEngineAgent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTENGINEAGENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptClass::QueryFlag >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTCLASS_QUERYFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptClass::Extension >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTCLASS_EXTENSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptClass >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTCLASS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptProgram >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTPROGRAM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptString >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTSTRING_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptContextInfo::FunctionType >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTCONTEXTINFO_FUNCTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptContextInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTCONTEXTINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptClassPropertyIterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTCLASSPROPERTYITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptValue::ResolveFlag >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTVALUE_RESOLVEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QScriptValue::ResolveFlag> >() { return SbkPySide_QtScriptTypes[SBK_QFLAGS_QSCRIPTVALUE_RESOLVEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptValue::PropertyFlag >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTVALUE_PROPERTYFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QScriptValue::PropertyFlag> >() { return SbkPySide_QtScriptTypes[SBK_QFLAGS_QSCRIPTVALUE_PROPERTYFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptValue::SpecialValue >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTVALUE_SPECIALVALUE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptValue >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTVALUE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptable >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTABLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptExtensionInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTEXTENSIONINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptExtensionPlugin >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTEXTENSIONPLUGIN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QScriptEngine::ValueOwnership >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTENGINE_VALUEOWNERSHIP_IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptEngine::QObjectWrapOption >() { return SbkPySide_QtScriptTypes[SBK_QSCRIPTENGINE_QOBJECTWRAPOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QScriptEngine::QObjectWrapOption> >() { return SbkPySide_QtScriptTypes[SBK_QFLAGS_QSCRIPTENGINE_QOBJECTWRAPOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QScriptEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtScriptTypes[SBK_QSCRIPTENGINE_IDX]); }

} // namespace Shiboken

#endif // SBK_QTSCRIPT_PYTHON_H

