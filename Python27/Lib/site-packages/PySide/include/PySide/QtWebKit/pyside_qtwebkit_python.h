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



#ifndef SBK_QTWEBKIT_PYTHON_H
#define SBK_QTWEBKIT_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Module Includes
#include <pyside_qtcore_python.h>
#include <pyside_qtgui_python.h>
#include <pyside_qtnetwork_python.h>

// Binded library includes
#include <qwebpluginfactory.h>
#include <qwebhistoryinterface.h>
#include <qwebpage.h>
#include <qgraphicswebview.h>
#include <qwebsecurityorigin.h>
#include <qwebelement.h>
#include <qwebinspector.h>
#include <qwebhistory.h>
#include <qwebdatabase.h>
#include <qwebview.h>
#include <qwebframe.h>
#include <qwebsettings.h>
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
#define SBK_WEBCORE_IDX                                              38
#define SBK_QWEBHISTORYITEM_IDX                                      10
#define SBK_QWEBHITTESTRESULT_IDX                                    11
#define SBK_QWEBDATABASE_IDX                                         2
#define SBK_QWEBHISTORY_IDX                                          8
#define SBK_QWEBELEMENT_IDX                                          3
#define SBK_QWEBELEMENT_STYLERESOLVESTRATEGY_IDX                     4
#define SBK_QWEBSECURITYORIGIN_IDX                                   31
#define SBK_QWEBELEMENTCOLLECTION_IDX                                5
#define SBK_QWEBSETTINGS_IDX                                         32
#define SBK_QWEBSETTINGS_FONTFAMILY_IDX                              33
#define SBK_QWEBSETTINGS_WEBATTRIBUTE_IDX                            35
#define SBK_QWEBSETTINGS_WEBGRAPHIC_IDX                              36
#define SBK_QWEBSETTINGS_FONTSIZE_IDX                                34
#define SBK_QWEBHISTORYINTERFACE_IDX                                 9
#define SBK_QWEBPLUGINFACTORY_IDX                                    27
#define SBK_QWEBPLUGINFACTORY_EXTENSION_IDX                          28
#define SBK_QWEBPLUGINFACTORY_MIMETYPE_IDX                           29
#define SBK_QWEBPLUGINFACTORY_PLUGIN_IDX                             30
#define SBK_QWEBPAGE_IDX                                             13
#define SBK_QWEBPAGE_NAVIGATIONTYPE_IDX                              24
#define SBK_QWEBPAGE_WEBACTION_IDX                                   25
#define SBK_QWEBPAGE_FINDFLAG_IDX                                    22
#define SBK_QFLAGS_QWEBPAGE_FINDFLAG__IDX                            0
#define SBK_QWEBPAGE_LINKDELEGATIONPOLICY_IDX                        23
#define SBK_QWEBPAGE_WEBWINDOWTYPE_IDX                               26
#define SBK_QWEBPAGE_PERMISSIONPOLICY_IDX                            40
#define SBK_QWEBPAGE_FEATURE_IDX                                     39
#define SBK_QWEBPAGE_EXTENSION_IDX                                   19
#define SBK_QWEBPAGE_ERRORDOMAIN_IDX                                 16
#define SBK_QWEBPAGE_EXTENSIONRETURN_IDX                             21
#define SBK_QWEBPAGE_CHOOSEMULTIPLEFILESEXTENSIONRETURN_IDX          15
#define SBK_QWEBPAGE_EXTENSIONOPTION_IDX                             20
#define SBK_QWEBPAGE_CHOOSEMULTIPLEFILESEXTENSIONOPTION_IDX          14
#define SBK_QWEBPAGE_ERRORPAGEEXTENSIONRETURN_IDX                    18
#define SBK_QWEBPAGE_ERRORPAGEEXTENSIONOPTION_IDX                    17
#define SBK_QWEBINSPECTOR_IDX                                        12
#define SBK_QGRAPHICSWEBVIEW_IDX                                     1
#define SBK_QWEBVIEW_IDX                                             37
#define SBK_QWEBFRAME_IDX                                            6
#define SBK_QWEBFRAME_RENDERLAYER_IDX                                7
#define SBK_QtWebKit_IDX_COUNT                                       41

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtWebKitTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtWebKitTypeConverters;

// Converter indices
#define SBK_QTWEBKIT_QLIST_QWEBHISTORYITEM_IDX                       0 // QList<QWebHistoryItem >
#define SBK_QTWEBKIT_QLIST_QWEBSECURITYORIGIN_IDX                    1 // QList<QWebSecurityOrigin >
#define SBK_QTWEBKIT_QLIST_QWEBDATABASE_IDX                          2 // QList<QWebDatabase >
#define SBK_QTWEBKIT_QLIST_QWEBELEMENT_IDX                           3 // QList<QWebElement >
#define SBK_QTWEBKIT_QLIST_QOBJECTPTR_IDX                            4 // const QList<QObject * > &
#define SBK_QTWEBKIT_QLIST_QBYTEARRAY_IDX                            5 // QList<QByteArray >
#define SBK_QTWEBKIT_QLIST_QWEBPLUGINFACTORY_PLUGIN_IDX              6 // QList<QWebPluginFactory::Plugin >
#define SBK_QTWEBKIT_QLIST_QWEBPLUGINFACTORY_MIMETYPE_IDX            7 // QList<QWebPluginFactory::MimeType >
#define SBK_QTWEBKIT_QLIST_QACTIONPTR_IDX                            8 // QList<QAction * >
#define SBK_QTWEBKIT_QLIST_QWEBFRAMEPTR_IDX                          9 // QList<QWebFrame * >
#define SBK_QTWEBKIT_QMULTIMAP_QSTRING_QSTRING_IDX                   10 // QMultiMap<QString, QString >
#define SBK_QTWEBKIT_QLIST_QVARIANT_IDX                              11 // QList<QVariant >
#define SBK_QTWEBKIT_QLIST_QSTRING_IDX                               12 // QList<QString >
#define SBK_QTWEBKIT_QMAP_QSTRING_QVARIANT_IDX                       13 // QMap<QString, QVariant >
#define SBK_QtWebKit_CONVERTERS_IDX_COUNT                            14

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QWebHistoryItem >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBHISTORYITEM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebHitTestResult >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBHITTESTRESULT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebDatabase >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBDATABASE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebHistory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBHISTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebElement::StyleResolveStrategy >() { return SbkPySide_QtWebKitTypes[SBK_QWEBELEMENT_STYLERESOLVESTRATEGY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebElement >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBELEMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebSecurityOrigin >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBSECURITYORIGIN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebElementCollection >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBELEMENTCOLLECTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebSettings::FontFamily >() { return SbkPySide_QtWebKitTypes[SBK_QWEBSETTINGS_FONTFAMILY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebSettings::WebAttribute >() { return SbkPySide_QtWebKitTypes[SBK_QWEBSETTINGS_WEBATTRIBUTE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebSettings::WebGraphic >() { return SbkPySide_QtWebKitTypes[SBK_QWEBSETTINGS_WEBGRAPHIC_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebSettings::FontSize >() { return SbkPySide_QtWebKitTypes[SBK_QWEBSETTINGS_FONTSIZE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebSettings >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBSETTINGS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebHistoryInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBHISTORYINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPluginFactory::Extension >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPLUGINFACTORY_EXTENSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPluginFactory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPLUGINFACTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPluginFactory::MimeType >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPLUGINFACTORY_MIMETYPE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPluginFactory::Plugin >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPLUGINFACTORY_PLUGIN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::NavigationType >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_NAVIGATIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::WebAction >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_WEBACTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::FindFlag >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_FINDFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QWebPage::FindFlag> >() { return SbkPySide_QtWebKitTypes[SBK_QFLAGS_QWEBPAGE_FINDFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::LinkDelegationPolicy >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_LINKDELEGATIONPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::WebWindowType >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_WEBWINDOWTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::PermissionPolicy >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_PERMISSIONPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::Feature >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_FEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::Extension >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_EXTENSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage::ErrorDomain >() { return SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_ERRORDOMAIN_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebPage >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::ExtensionReturn >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_EXTENSIONRETURN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::ChooseMultipleFilesExtensionReturn >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_CHOOSEMULTIPLEFILESEXTENSIONRETURN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::ExtensionOption >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_EXTENSIONOPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::ChooseMultipleFilesExtensionOption >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_CHOOSEMULTIPLEFILESEXTENSIONOPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::ErrorPageExtensionReturn >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_ERRORPAGEEXTENSIONRETURN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebPage::ErrorPageExtensionOption >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBPAGE_ERRORPAGEEXTENSIONOPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebInspector >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBINSPECTOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGraphicsWebView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QGRAPHICSWEBVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebView >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBVIEW_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWebFrame::RenderLayer >() { return SbkPySide_QtWebKitTypes[SBK_QWEBFRAME_RENDERLAYER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QWebFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtWebKitTypes[SBK_QWEBFRAME_IDX]); }

} // namespace Shiboken

#endif // SBK_QTWEBKIT_PYTHON_H

