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



#ifndef SBK_QTXMLPATTERNS_PYTHON_H
#define SBK_QTXMLPATTERNS_PYTHON_H

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
#include <qabstractxmlnodemodel.h>
#include <qabstractxmlreceiver.h>
#include <qxmlquery.h>
#include <qxmlschemavalidator.h>
#include <qxmlformatter.h>
#include <qxmlresultitems.h>
#include <qabstracturiresolver.h>
#include <qxmlschema.h>
#include <qxmlnamepool.h>
#include <qxmlname.h>
#include <qabstractmessagehandler.h>
#include <qsourcelocation.h>
#include <qxmlserializer.h>
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
#define SBK_QXMLNAMEPOOL_IDX                                         10
#define SBK_QABSTRACTXMLNODEMODEL_IDX                                2
#define SBK_QABSTRACTXMLNODEMODEL_SIMPLEAXIS_IDX                     4
#define SBK_QABSTRACTXMLNODEMODEL_NODECOPYSETTING_IDX                3
#define SBK_QXMLNODEMODELINDEX_IDX                                   11
#define SBK_QXMLNODEMODELINDEX_NODEKIND_IDX                          13
#define SBK_QXMLNODEMODELINDEX_DOCUMENTORDER_IDX                     12
#define SBK_QSOURCELOCATION_IDX                                      6
#define SBK_QXMLRESULTITEMS_IDX                                      16
#define SBK_QABSTRACTXMLRECEIVER_IDX                                 5
#define SBK_QXMLSERIALIZER_IDX                                       19
#define SBK_QXMLFORMATTER_IDX                                        7
#define SBK_QXMLNAME_IDX                                             9
#define SBK_QXMLITEM_IDX                                             8
#define SBK_QABSTRACTURIRESOLVER_IDX                                 1
#define SBK_QXMLQUERY_IDX                                            14
#define SBK_QXMLQUERY_QUERYLANGUAGE_IDX                              15
#define SBK_QABSTRACTMESSAGEHANDLER_IDX                              0
#define SBK_QXMLSCHEMA_IDX                                           17
#define SBK_QXMLSCHEMAVALIDATOR_IDX                                  18
#define SBK_QtXmlPatterns_IDX_COUNT                                  20

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtXmlPatternsTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtXmlPatternsTypeConverters;

// Converter indices
#define SBK_QTXMLPATTERNS_QVECTOR_QXMLNODEMODELINDEX_IDX             0 // QVector<QXmlNodeModelIndex >
#define SBK_QTXMLPATTERNS_QVECTOR_QXMLNAME_IDX                       1 // QVector<QXmlName >
#define SBK_QTXMLPATTERNS_QLIST_QOBJECTPTR_IDX                       2 // const QList<QObject * > &
#define SBK_QTXMLPATTERNS_QLIST_QBYTEARRAY_IDX                       3 // QList<QByteArray >
#define SBK_QTXMLPATTERNS_QLIST_QVARIANT_IDX                         4 // QList<QVariant >
#define SBK_QTXMLPATTERNS_QLIST_QSTRING_IDX                          5 // QList<QString >
#define SBK_QTXMLPATTERNS_QMAP_QSTRING_QVARIANT_IDX                  6 // QMap<QString, QVariant >
#define SBK_QtXmlPatterns_CONVERTERS_IDX_COUNT                       7

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QXmlNamePool >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLNAMEPOOL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractXmlNodeModel::SimpleAxis >() { return SbkPySide_QtXmlPatternsTypes[SBK_QABSTRACTXMLNODEMODEL_SIMPLEAXIS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractXmlNodeModel::NodeCopySetting >() { return SbkPySide_QtXmlPatternsTypes[SBK_QABSTRACTXMLNODEMODEL_NODECOPYSETTING_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractXmlNodeModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QABSTRACTXMLNODEMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlNodeModelIndex::NodeKind >() { return SbkPySide_QtXmlPatternsTypes[SBK_QXMLNODEMODELINDEX_NODEKIND_IDX]; }
template<> inline PyTypeObject* SbkType< ::QXmlNodeModelIndex::DocumentOrder >() { return SbkPySide_QtXmlPatternsTypes[SBK_QXMLNODEMODELINDEX_DOCUMENTORDER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QXmlNodeModelIndex >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLNODEMODELINDEX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSourceLocation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QSOURCELOCATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlResultItems >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLRESULTITEMS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractXmlReceiver >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QABSTRACTXMLRECEIVER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlSerializer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLSERIALIZER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlFormatter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLFORMATTER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlName >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLNAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractUriResolver >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QABSTRACTURIRESOLVER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlQuery::QueryLanguage >() { return SbkPySide_QtXmlPatternsTypes[SBK_QXMLQUERY_QUERYLANGUAGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QXmlQuery >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLQUERY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractMessageHandler >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QABSTRACTMESSAGEHANDLER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlSchema >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLSCHEMA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlSchemaValidator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtXmlPatternsTypes[SBK_QXMLSCHEMAVALIDATOR_IDX]); }

} // namespace Shiboken

#endif // SBK_QTXMLPATTERNS_PYTHON_H

