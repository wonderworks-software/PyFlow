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



#ifndef SBK_QTSVG_PYTHON_H
#define SBK_QTSVG_PYTHON_H

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
#include <qgraphicssvgitem.h>
#include <qsvggenerator.h>
#include <qsvgrenderer.h>
#include <qsvgwidget.h>
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
#define SBK_QSVGGENERATOR_IDX                                        1
#define SBK_QGRAPHICSSVGITEM_IDX                                     0
#define SBK_QSVGWIDGET_IDX                                           3
#define SBK_QSVGRENDERER_IDX                                         2
#define SBK_QtSvg_IDX_COUNT                                          4

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtSvgTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtSvgTypeConverters;

// Converter indices
#define SBK_QTSVG_QLIST_QGRAPHICSITEMPTR_IDX                         0 // QList<QGraphicsItem * >
#define SBK_QTSVG_QLIST_QGRAPHICSTRANSFORMPTR_IDX                    1 // const QList<QGraphicsTransform * > &
#define SBK_QTSVG_QLIST_QACTIONPTR_IDX                               2 // QList<QAction * >
#define SBK_QTSVG_QLIST_QOBJECTPTR_IDX                               3 // const QList<QObject * > &
#define SBK_QTSVG_QLIST_QBYTEARRAY_IDX                               4 // QList<QByteArray >
#define SBK_QTSVG_QLIST_QVARIANT_IDX                                 5 // QList<QVariant >
#define SBK_QTSVG_QLIST_QSTRING_IDX                                  6 // QList<QString >
#define SBK_QTSVG_QMAP_QSTRING_QVARIANT_IDX                          7 // QMap<QString, QVariant >
#define SBK_QtSvg_CONVERTERS_IDX_COUNT                               8

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QSvgGenerator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSvgTypes[SBK_QSVGGENERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsSvgItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSvgTypes[SBK_QGRAPHICSSVGITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSvgWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSvgTypes[SBK_QSVGWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSvgRenderer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtSvgTypes[SBK_QSVGRENDERER_IDX]); }

} // namespace Shiboken

#endif // SBK_QTSVG_PYTHON_H

