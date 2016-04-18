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



#ifndef SBK_QTHELP_PYTHON_H
#define SBK_QTHELP_PYTHON_H

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
#include <qhelpsearchresultwidget.h>
#include <qhelpsearchengine.h>
#include <qhelpindexwidget.h>
#include <qhelpsearchquerywidget.h>
#include <qhelpcontentwidget.h>
#include <qhelpenginecore.h>
#include <qhelpengine.h>
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
#define SBK_QHELPSEARCHQUERY_IDX                                     8
#define SBK_QHELPSEARCHQUERY_FIELDNAME_IDX                           9
#define SBK_QHELPCONTENTITEM_IDX                                     0
#define SBK_QHELPINDEXMODEL_IDX                                      5
#define SBK_QHELPCONTENTMODEL_IDX                                    1
#define SBK_QHELPSEARCHQUERYWIDGET_IDX                               10
#define SBK_QHELPSEARCHRESULTWIDGET_IDX                              11
#define SBK_QHELPCONTENTWIDGET_IDX                                   2
#define SBK_QHELPINDEXWIDGET_IDX                                     6
#define SBK_QHELPENGINECORE_IDX                                      4
#define SBK_QHELPENGINE_IDX                                          3
#define SBK_QHELPSEARCHENGINE_IDX                                    7
#define SBK_QtHelp_IDX_COUNT                                         12

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtHelpTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtHelpTypeConverters;

// Converter indices
#define SBK_QTHELP_QLIST_QOBJECTPTR_IDX                              0 // const QList<QObject * > &
#define SBK_QTHELP_QLIST_QBYTEARRAY_IDX                              1 // QList<QByteArray >
#define SBK_QTHELP_QMAP_INT_QVARIANT_IDX                             2 // QMap<int, QVariant >
#define SBK_QTHELP_QMAP_QSTRING_QURL_IDX                             3 // QMap<QString, QUrl >
#define SBK_QTHELP_QHASH_INT_QBYTEARRAY_IDX                          4 // const QHash<int, QByteArray > &
#define SBK_QTHELP_QLIST_QACTIONPTR_IDX                              5 // QList<QAction * >
#define SBK_QTHELP_QLIST_QHELPSEARCHQUERY_IDX                        6 // QList<QHelpSearchQuery >
#define SBK_QTHELP_QLIST_QWIDGETPTR_IDX                              7 // QList<QWidget * >
#define SBK_QTHELP_QLIST_QURL_IDX                                    8 // QList<QUrl >
#define SBK_QTHELP_QLIST_QSTRINGLIST_IDX                             9 // QList<QStringList >
#define SBK_QTHELP_QPAIR_QSTRING_QSTRING_IDX                         10 // QPair<QString, QString >
#define SBK_QTHELP_QLIST_QPAIR_QSTRING_QSTRING_IDX                   11 // QList<QPair<QString, QString > >
#define SBK_QTHELP_QLIST_QVARIANT_IDX                                12 // QList<QVariant >
#define SBK_QTHELP_QLIST_QSTRING_IDX                                 13 // QList<QString >
#define SBK_QTHELP_QMAP_QSTRING_QVARIANT_IDX                         14 // QMap<QString, QVariant >
#define SBK_QtHelp_CONVERTERS_IDX_COUNT                              15

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QHelpSearchQuery::FieldName >() { return SbkPySide_QtHelpTypes[SBK_QHELPSEARCHQUERY_FIELDNAME_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHelpSearchQuery >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPSEARCHQUERY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpContentItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPCONTENTITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpIndexModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPINDEXMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpContentModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPCONTENTMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpSearchQueryWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPSEARCHQUERYWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpSearchResultWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPSEARCHRESULTWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpContentWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPCONTENTWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpIndexWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPINDEXWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpEngineCore >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPENGINECORE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHelpSearchEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtHelpTypes[SBK_QHELPSEARCHENGINE_IDX]); }

} // namespace Shiboken

#endif // SBK_QTHELP_PYTHON_H

