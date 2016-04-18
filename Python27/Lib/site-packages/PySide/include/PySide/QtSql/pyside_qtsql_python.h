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



#ifndef SBK_QTSQL_PYTHON_H
#define SBK_QTSQL_PYTHON_H

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

// Binded library includes
#include <qsqltablemodel.h>
#include <qsql.h>
#include <qsqlrelationaldelegate.h>
#include <qsqlquery.h>
#include <qsqlerror.h>
#include <qsqlindex.h>
#include <qsqldriver.h>
#include <qsqlrecord.h>
#include <qsqlresult.h>
#include <qsqldatabase.h>
#include <qsqlquerymodel.h>
#include <qsqlrelationaltablemodel.h>
#include <qsqlfield.h>
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
#define SBK_QSQL_IDX                                                 1
#define SBK_QSQL_LOCATION_IDX                                        2
#define SBK_QSQL_PARAMTYPEFLAG_IDX                                   4
#define SBK_QFLAGS_QSQL_PARAMTYPEFLAG__IDX                           0
#define SBK_QSQL_TABLETYPE_IDX                                       5
#define SBK_QSQL_NUMERICALPRECISIONPOLICY_IDX                        3
#define SBK_QSQLRELATION_IDX                                         21
#define SBK_QSQLRESULT_IDX                                           24
#define SBK_QSQLRESULT_BINDINGSYNTAX_IDX                             25
#define SBK_QSQLRESULT_VIRTUALHOOKOPERATION_IDX                      26
#define SBK_QSQLRECORD_IDX                                           20
#define SBK_QSQLINDEX_IDX                                            16
#define SBK_QSQLFIELD_IDX                                            14
#define SBK_QSQLFIELD_REQUIREDSTATUS_IDX                             15
#define SBK_QSQLERROR_IDX                                            12
#define SBK_QSQLERROR_ERRORTYPE_IDX                                  13
#define SBK_QSQLDRIVERCREATORBASE_IDX                                11
#define SBK_QSQLDATABASE_IDX                                         6
#define SBK_QSQLQUERY_IDX                                            17
#define SBK_QSQLQUERY_BATCHEXECUTIONMODE_IDX                         18
#define SBK_QSQLRELATIONALDELEGATE_IDX                               22
#define SBK_QSQLDRIVER_IDX                                           7
#define SBK_QSQLDRIVER_DRIVERFEATURE_IDX                             8
#define SBK_QSQLDRIVER_STATEMENTTYPE_IDX                             10
#define SBK_QSQLDRIVER_IDENTIFIERTYPE_IDX                            9
#define SBK_QSQLQUERYMODEL_IDX                                       19
#define SBK_QSQLTABLEMODEL_IDX                                       27
#define SBK_QSQLTABLEMODEL_EDITSTRATEGY_IDX                          28
#define SBK_QSQLRELATIONALTABLEMODEL_IDX                             23
#define SBK_QtSql_IDX_COUNT                                          29

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtSqlTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtSqlTypeConverters;

// Converter indices
#define SBK_QTSQL_QVECTOR_QVARIANT_IDX                               0 // QVector<QVariant > &
#define SBK_QTSQL_QMAP_QSTRING_QVARIANT_IDX                          1 // QMap<QString, QVariant >
#define SBK_QTSQL_QLIST_QOBJECTPTR_IDX                               2 // const QList<QObject * > &
#define SBK_QTSQL_QLIST_QBYTEARRAY_IDX                               3 // QList<QByteArray >
#define SBK_QTSQL_QMAP_INT_QVARIANT_IDX                              4 // QMap<int, QVariant >
#define SBK_QTSQL_QHASH_INT_QBYTEARRAY_IDX                           5 // const QHash<int, QByteArray > &
#define SBK_QTSQL_QLIST_QVARIANT_IDX                                 6 // QList<QVariant >
#define SBK_QTSQL_QLIST_QSTRING_IDX                                  7 // QList<QString >
#define SBK_QtSql_CONVERTERS_IDX_COUNT                               8

// Macros for type check

// Protected enum surrogates
enum PySide_QtSql_QSqlResult_BindingSyntax_Surrogate {};
enum PySide_QtSql_QSqlResult_VirtualHookOperation_Surrogate {};

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QSql::Location >() { return SbkPySide_QtSqlTypes[SBK_QSQL_LOCATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSql::ParamTypeFlag >() { return SbkPySide_QtSqlTypes[SBK_QSQL_PARAMTYPEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QSql::ParamTypeFlag> >() { return SbkPySide_QtSqlTypes[SBK_QFLAGS_QSQL_PARAMTYPEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QSql::TableType >() { return SbkPySide_QtSqlTypes[SBK_QSQL_TABLETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSql::NumericalPrecisionPolicy >() { return SbkPySide_QtSqlTypes[SBK_QSQL_NUMERICALPRECISIONPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlRelation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLRELATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::PySide_QtSql_QSqlResult_BindingSyntax_Surrogate >() { return SbkPySide_QtSqlTypes[SBK_QSQLRESULT_BINDINGSYNTAX_IDX]; }
template<> inline PyTypeObject* SbkType< ::PySide_QtSql_QSqlResult_VirtualHookOperation_Surrogate >() { return SbkPySide_QtSqlTypes[SBK_QSQLRESULT_VIRTUALHOOKOPERATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlResult >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLRESULT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlRecord >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLRECORD_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlIndex >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLINDEX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlField::RequiredStatus >() { return SbkPySide_QtSqlTypes[SBK_QSQLFIELD_REQUIREDSTATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlField >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLFIELD_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlError::ErrorType >() { return SbkPySide_QtSqlTypes[SBK_QSQLERROR_ERRORTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlError >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLERROR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlDriverCreatorBase >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLDRIVERCREATORBASE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlDatabase >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLDATABASE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlQuery::BatchExecutionMode >() { return SbkPySide_QtSqlTypes[SBK_QSQLQUERY_BATCHEXECUTIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlQuery >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLQUERY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlRelationalDelegate >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLRELATIONALDELEGATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlDriver::DriverFeature >() { return SbkPySide_QtSqlTypes[SBK_QSQLDRIVER_DRIVERFEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlDriver::StatementType >() { return SbkPySide_QtSqlTypes[SBK_QSQLDRIVER_STATEMENTTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlDriver::IdentifierType >() { return SbkPySide_QtSqlTypes[SBK_QSQLDRIVER_IDENTIFIERTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlDriver >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLDRIVER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlQueryModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLQUERYMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlTableModel::EditStrategy >() { return SbkPySide_QtSqlTypes[SBK_QSQLTABLEMODEL_EDITSTRATEGY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSqlTableModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLTABLEMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSqlRelationalTableModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSqlTypes[SBK_QSQLRELATIONALTABLEMODEL_IDX]); }

} // namespace Shiboken

#endif // SBK_QTSQL_PYTHON_H

