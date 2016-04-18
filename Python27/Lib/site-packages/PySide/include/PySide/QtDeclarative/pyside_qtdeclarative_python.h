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



#ifndef SBK_QTDECLARATIVE_PYTHON_H
#define SBK_QTDECLARATIVE_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Module Includes
#include <pyside_qtcore_python.h>
#include <pyside_qtnetwork_python.h>
#include <pyside_qtgui_python.h>

// Binded library includes
#include <qdeclarativeproperty.h>
#include <qdeclarativescriptstring.h>
#include <qdeclarativenetworkaccessmanagerfactory.h>
#include <qdeclarativeparserstatus.h>
#include <qdeclarativeexpression.h>
#include <qdeclarativecomponent.h>
#include <qdeclarativepropertymap.h>
#include <qdeclarativeitem.h>
#include <qdeclarativeview.h>
#include <qdeclarativeextensionplugin.h>
#include <qdeclarativepropertyvaluesource.h>
#include <qdeclarativelist.h>
#include <qdeclarativeengine.h>
#include <qdeclarativeerror.h>
#include <qdeclarativeimageprovider.h>
#include <qdeclarativecontext.h>
#include <qdeclarativeextensioninterface.h>
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
#define SBK_QDECLARATIVEIMAGEPROVIDER_IDX                            9
#define SBK_QDECLARATIVEIMAGEPROVIDER_IMAGETYPE_IDX                  10
#define SBK_QDECLARATIVEPROPERTY_IDX                                 16
#define SBK_QDECLARATIVEPROPERTY_PROPERTYTYPECATEGORY_IDX            17
#define SBK_QDECLARATIVEPROPERTY_TYPE_IDX                            18
#define SBK_QDECLARATIVESCRIPTSTRING_IDX                             21
#define SBK_QDECLARATIVEEXTENSIONINTERFACE_IDX                       7
#define SBK_QDECLARATIVEERROR_IDX                                    5
#define SBK_QDECLARATIVENETWORKACCESSMANAGERFACTORY_IDX              14
#define SBK_QDECLARATIVEPROPERTYVALUESOURCE_IDX                      20
#define SBK_QDECLARATIVELISTREFERENCE_IDX                            13
#define SBK_QDECLARATIVEPARSERSTATUS_IDX                             15
#define SBK_QDECLARATIVEITEM_IDX                                     11
#define SBK_QDECLARATIVEITEM_TRANSFORMORIGIN_IDX                     12
#define SBK_QDECLARATIVECONTEXT_IDX                                  2
#define SBK_QDECLARATIVECOMPONENT_IDX                                0
#define SBK_QDECLARATIVECOMPONENT_STATUS_IDX                         1
#define SBK_QDECLARATIVEEXPRESSION_IDX                               6
#define SBK_QDECLARATIVEPROPERTYMAP_IDX                              19
#define SBK_QDECLARATIVEENGINE_IDX                                   3
#define SBK_QDECLARATIVEENGINE_OBJECTOWNERSHIP_IDX                   4
#define SBK_QDECLARATIVEVIEW_IDX                                     22
#define SBK_QDECLARATIVEVIEW_RESIZEMODE_IDX                          23
#define SBK_QDECLARATIVEVIEW_STATUS_IDX                              24
#define SBK_QDECLARATIVEEXTENSIONPLUGIN_IDX                          8
#define SBK_QML_HAS_ATTACHED_PROPERTIES_IDX                          25
#define SBK_QtDeclarative_IDX_COUNT                                  26

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtDeclarativeTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtDeclarativeTypeConverters;

// Converter indices
#define SBK_QTDECLARATIVE_QLIST_QOBJECTPTR_IDX                       0 // const QList<QObject * > &
#define SBK_QTDECLARATIVE_QLIST_QBYTEARRAY_IDX                       1 // QList<QByteArray >
#define SBK_QTDECLARATIVE_QLIST_QDECLARATIVEERROR_IDX                2 // QList<QDeclarativeError >
#define SBK_QTDECLARATIVE_QLIST_QACTIONPTR_IDX                       3 // QList<QAction * >
#define SBK_QTDECLARATIVE_QLIST_QGRAPHICSITEMPTR_IDX                 4 // QList<QGraphicsItem * >
#define SBK_QTDECLARATIVE_QLIST_QWIDGETPTR_IDX                       5 // QList<QWidget * >
#define SBK_QTDECLARATIVE_QLIST_QRECTF_IDX                           6 // const QList<QRectF > &
#define SBK_QTDECLARATIVE_QLIST_QVARIANT_IDX                         7 // QList<QVariant >
#define SBK_QTDECLARATIVE_QLIST_QSTRING_IDX                          8 // QList<QString >
#define SBK_QTDECLARATIVE_QMAP_QSTRING_QVARIANT_IDX                  9 // QMap<QString, QVariant >
#define SBK_QtDeclarative_CONVERTERS_IDX_COUNT                       10

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QDeclarativeImageProvider::ImageType >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEIMAGEPROVIDER_IMAGETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeImageProvider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEIMAGEPROVIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeProperty::PropertyTypeCategory >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEPROPERTY_PROPERTYTYPECATEGORY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeProperty::Type >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEPROPERTY_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeProperty >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEPROPERTY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeScriptString >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVESCRIPTSTRING_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeExtensionInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEEXTENSIONINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeError >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEERROR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeNetworkAccessManagerFactory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVENETWORKACCESSMANAGERFACTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativePropertyValueSource >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEPROPERTYVALUESOURCE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeListReference >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVELISTREFERENCE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeParserStatus >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEPARSERSTATUS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeItem::TransformOrigin >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEITEM_TRANSFORMORIGIN_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeContext >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVECONTEXT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeComponent::Status >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVECOMPONENT_STATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeComponent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVECOMPONENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeExpression >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEEXPRESSION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativePropertyMap >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEPROPERTYMAP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeEngine::ObjectOwnership >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEENGINE_OBJECTOWNERSHIP_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeView::ResizeMode >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEVIEW_RESIZEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeView::Status >() { return SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEVIEW_STATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDeclarativeView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDeclarativeExtensionPlugin >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtDeclarativeTypes[SBK_QDECLARATIVEEXTENSIONPLUGIN_IDX]); }

} // namespace Shiboken

#endif // SBK_QTDECLARATIVE_PYTHON_H

