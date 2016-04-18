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



#ifndef SBK_QTNETWORK_PYTHON_H
#define SBK_QTNETWORK_PYTHON_H

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
#include <qsslconfiguration.h>
#include <qnetworkconfiguration.h>
#include <qlocalserver.h>
#include <qhostaddress.h>
#include <qhostinfo.h>
#include <qsslcertificate.h>
#include <qsslsocket.h>
#include <qnetworkrequest.h>
#include <qnetworksession.h>
#include <qnetworkconfigmanager.h>
#include <qnetworkcookiejar.h>
#include <qssl.h>
#include <qnetworkdiskcache.h>
#include <qnetworkcookie.h>
#include <qnetworkaccessmanager.h>
#include <qnetworkproxy.h>
#include <qnetworkinterface.h>
#include <qudpsocket.h>
#include <qtcpsocket.h>
#include <qnetworkreply.h>
#include <qabstractnetworkcache.h>
#include <qftp.h>
#include <qtcpserver.h>
#include <qabstractsocket.h>
#include <qsslerror.h>
#include <qsslcipher.h>
#include <qauthenticator.h>
#include <qurlinfo.h>
#include <qsslkey.h>
#include <qhttp.h>
#include <qlocalsocket.h>
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
#define SBK_QSSL_IDX                                                 70
#define SBK_QSSL_KEYTYPE_IDX                                         74
#define SBK_QSSL_ENCODINGFORMAT_IDX                                  72
#define SBK_QSSL_KEYALGORITHM_IDX                                    73
#define SBK_QSSL_ALTERNATENAMEENTRYTYPE_IDX                          71
#define SBK_QSSL_SSLPROTOCOL_IDX                                     75
#define SBK_QSSLCIPHER_IDX                                           78
#define SBK_QNETWORKCONFIGURATION_IDX                                40
#define SBK_QNETWORKCONFIGURATION_TYPE_IDX                           44
#define SBK_QNETWORKCONFIGURATION_PURPOSE_IDX                        42
#define SBK_QNETWORKCONFIGURATION_STATEFLAG_IDX                      43
#define SBK_QFLAGS_QNETWORKCONFIGURATION_STATEFLAG__IDX              8
#define SBK_QNETWORKCONFIGURATION_BEARERTYPE_IDX                     41
#define SBK_QSSLERROR_IDX                                            80
#define SBK_QSSLERROR_SSLERROR_IDX                                   81
#define SBK_QSSLCONFIGURATION_IDX                                    79
#define SBK_QAUTHENTICATOR_IDX                                       7
#define SBK_QNETWORKPROXYQUERY_IDX                                   57
#define SBK_QNETWORKPROXYQUERY_QUERYTYPE_IDX                         58
#define SBK_QNETWORKPROXYFACTORY_IDX                                 56
#define SBK_QNETWORKCACHEMETADATA_IDX                                39
#define SBK_QURLINFO_IDX                                             90
#define SBK_QURLINFO_PERMISSIONSPEC_IDX                              91
#define SBK_QHTTPHEADER_IDX                                          27
#define SBK_QHTTPREQUESTHEADER_IDX                                   28
#define SBK_QNETWORKINTERFACE_IDX                                    51
#define SBK_QNETWORKINTERFACE_INTERFACEFLAG_IDX                      52
#define SBK_QFLAGS_QNETWORKINTERFACE_INTERFACEFLAG__IDX              10
#define SBK_QIPV6ADDRESS_IDX                                         30
#define SBK_QHTTPRESPONSEHEADER_IDX                                  29
#define SBK_QHOSTADDRESS_IDX                                         19
#define SBK_QHOSTADDRESS_SPECIALADDRESS_IDX                          20
#define SBK_QNETWORKPROXY_IDX                                        53
#define SBK_QNETWORKPROXY_PROXYTYPE_IDX                              55
#define SBK_QNETWORKPROXY_CAPABILITY_IDX                             54
#define SBK_QFLAGS_QNETWORKPROXY_CAPABILITY__IDX                     11
#define SBK_QHOSTINFO_IDX                                            21
#define SBK_QHOSTINFO_HOSTINFOERROR_IDX                              22
#define SBK_QNETWORKADDRESSENTRY_IDX                                 38
#define SBK_QNETWORKCONFIGURATIONMANAGER_IDX                         45
#define SBK_QNETWORKCONFIGURATIONMANAGER_CAPABILITY_IDX              46
#define SBK_QFLAGS_QNETWORKCONFIGURATIONMANAGER_CAPABILITY__IDX      9
#define SBK_QTCPSERVER_IDX                                           86
#define SBK_QNETWORKSESSION_IDX                                      67
#define SBK_QNETWORKSESSION_STATE_IDX                                69
#define SBK_QNETWORKSESSION_SESSIONERROR_IDX                         68
#define SBK_QNETWORKACCESSMANAGER_IDX                                35
#define SBK_QNETWORKACCESSMANAGER_OPERATION_IDX                      37
#define SBK_QNETWORKACCESSMANAGER_NETWORKACCESSIBILITY_IDX           36
#define SBK_QABSTRACTNETWORKCACHE_IDX                                0
#define SBK_QNETWORKDISKCACHE_IDX                                    50
#define SBK_QNETWORKCOOKIEJAR_IDX                                    49
#define SBK_QFTP_IDX                                                 13
#define SBK_QFTP_STATE_IDX                                           16
#define SBK_QFTP_ERROR_IDX                                           15
#define SBK_QFTP_COMMAND_IDX                                         14
#define SBK_QFTP_TRANSFERMODE_IDX                                    17
#define SBK_QFTP_TRANSFERTYPE_IDX                                    18
#define SBK_QHTTP_IDX                                                23
#define SBK_QHTTP_CONNECTIONMODE_IDX                                 24
#define SBK_QHTTP_STATE_IDX                                          26
#define SBK_QHTTP_ERROR_IDX                                          25
#define SBK_QLOCALSERVER_IDX                                         31
#define SBK_QABSTRACTSOCKET_IDX                                      1
#define SBK_QABSTRACTSOCKET_SOCKETTYPE_IDX                           6
#define SBK_QABSTRACTSOCKET_NETWORKLAYERPROTOCOL_IDX                 2
#define SBK_QABSTRACTSOCKET_SOCKETERROR_IDX                          3
#define SBK_QABSTRACTSOCKET_SOCKETSTATE_IDX                          5
#define SBK_QABSTRACTSOCKET_SOCKETOPTION_IDX                         4
#define SBK_QUDPSOCKET_IDX                                           88
#define SBK_QUDPSOCKET_BINDFLAG_IDX                                  89
#define SBK_QFLAGS_QUDPSOCKET_BINDFLAG__IDX                          12
#define SBK_QTCPSOCKET_IDX                                           87
#define SBK_QNETWORKREPLY_IDX                                        59
#define SBK_QNETWORKREPLY_NETWORKERROR_IDX                           60
#define SBK_QLOCALSOCKET_IDX                                         32
#define SBK_QLOCALSOCKET_LOCALSOCKETERROR_IDX                        33
#define SBK_QLOCALSOCKET_LOCALSOCKETSTATE_IDX                        34
#define SBK_QNETWORKCOOKIE_IDX                                       47
#define SBK_QNETWORKCOOKIE_RAWFORM_IDX                               48
#define SBK_QSSLCERTIFICATE_IDX                                      76
#define SBK_QSSLCERTIFICATE_SUBJECTINFO_IDX                          77
#define SBK_QSSLSOCKET_IDX                                           83
#define SBK_QSSLSOCKET_SSLMODE_IDX                                   85
#define SBK_QSSLSOCKET_PEERVERIFYMODE_IDX                            84
#define SBK_QSSLKEY_IDX                                              82
#define SBK_QNETWORKREQUEST_IDX                                      61
#define SBK_QNETWORKREQUEST_KNOWNHEADERS_IDX                         64
#define SBK_QNETWORKREQUEST_ATTRIBUTE_IDX                            62
#define SBK_QNETWORKREQUEST_CACHELOADCONTROL_IDX                     63
#define SBK_QNETWORKREQUEST_LOADCONTROL_IDX                          65
#define SBK_QNETWORKREQUEST_PRIORITY_IDX                             66
#define SBK_QtNetwork_IDX_COUNT                                      92

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtNetworkTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtNetworkTypeConverters;

// Converter indices
#define SBK_QTNETWORK_QLIST_QNETWORKCONFIGURATION_IDX                0 // QList<QNetworkConfiguration >
#define SBK_QTNETWORK_QLIST_QSSLCERTIFICATE_IDX                      1 // QList<QSslCertificate >
#define SBK_QTNETWORK_QLIST_QSSLCIPHER_IDX                           2 // QList<QSslCipher >
#define SBK_QTNETWORK_QHASH_QSTRING_QVARIANT_IDX                     3 // QHash<QString, QVariant >
#define SBK_QTNETWORK_QLIST_QNETWORKPROXY_IDX                        4 // QList<QNetworkProxy >
#define SBK_QTNETWORK_QHASH_QNETWORKREQUEST_ATTRIBUTE_QVARIANT_IDX   5 // QHash<QNetworkRequest::Attribute, QVariant >
#define SBK_QTNETWORK_QPAIR_QBYTEARRAY_QBYTEARRAY_IDX                6 // QPair<QByteArray, QByteArray >
#define SBK_QTNETWORK_QLIST_QPAIR_QBYTEARRAY_QBYTEARRAY_IDX          7 // QList<QPair<QByteArray, QByteArray > >
#define SBK_QTNETWORK_QPAIR_QSTRING_QSTRING_IDX                      8 // QPair<QString, QString >
#define SBK_QTNETWORK_QLIST_QPAIR_QSTRING_QSTRING_IDX                9 // const QList<QPair<QString, QString > > &
#define SBK_QTNETWORK_QLIST_QNETWORKADDRESSENTRY_IDX                 10 // QList<QNetworkAddressEntry >
#define SBK_QTNETWORK_QLIST_QHOSTADDRESS_IDX                         11 // QList<QHostAddress >
#define SBK_QTNETWORK_QLIST_QNETWORKINTERFACE_IDX                    12 // QList<QNetworkInterface >
#define SBK_QTNETWORK_QPAIR_QHOSTADDRESS_INT_IDX                     13 // const QPair<QHostAddress, int > &
#define SBK_QTNETWORK_QLIST_QOBJECTPTR_IDX                           14 // const QList<QObject * > &
#define SBK_QTNETWORK_QLIST_QBYTEARRAY_IDX                           15 // QList<QByteArray >
#define SBK_QTNETWORK_QLIST_QSSLERROR_IDX                            16 // const QList<QSslError > &
#define SBK_QTNETWORK_QLIST_QNETWORKCOOKIE_IDX                       17 // QList<QNetworkCookie >
#define SBK_QTNETWORK_QMULTIMAP_QSSL_ALTERNATENAMEENTRYTYPE_QSTRING_IDX 18 // QMultiMap<QSsl::AlternateNameEntryType, QString >
#define SBK_QTNETWORK_QLIST_QVARIANT_IDX                             19 // QList<QVariant >
#define SBK_QTNETWORK_QLIST_QSTRING_IDX                              20 // QList<QString >
#define SBK_QTNETWORK_QMAP_QSTRING_QVARIANT_IDX                      21 // QMap<QString, QVariant >
#define SBK_QtNetwork_CONVERTERS_IDX_COUNT                           22

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QSsl::KeyType >() { return SbkPySide_QtNetworkTypes[SBK_QSSL_KEYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSsl::EncodingFormat >() { return SbkPySide_QtNetworkTypes[SBK_QSSL_ENCODINGFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSsl::KeyAlgorithm >() { return SbkPySide_QtNetworkTypes[SBK_QSSL_KEYALGORITHM_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSsl::AlternateNameEntryType >() { return SbkPySide_QtNetworkTypes[SBK_QSSL_ALTERNATENAMEENTRYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSsl::SslProtocol >() { return SbkPySide_QtNetworkTypes[SBK_QSSL_SSLPROTOCOL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSslCipher >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QSSLCIPHER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkConfiguration::Type >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATION_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkConfiguration::Purpose >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATION_PURPOSE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkConfiguration::StateFlag >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATION_STATEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QNetworkConfiguration::StateFlag> >() { return SbkPySide_QtNetworkTypes[SBK_QFLAGS_QNETWORKCONFIGURATION_STATEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkConfiguration::BearerType >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATION_BEARERTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkConfiguration >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSslError::SslError >() { return SbkPySide_QtNetworkTypes[SBK_QSSLERROR_SSLERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSslError >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QSSLERROR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSslConfiguration >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QSSLCONFIGURATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAuthenticator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QAUTHENTICATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkProxyQuery::QueryType >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKPROXYQUERY_QUERYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkProxyQuery >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKPROXYQUERY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkProxyFactory >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKPROXYFACTORY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkCacheMetaData >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKCACHEMETADATA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUrlInfo::PermissionSpec >() { return SbkPySide_QtNetworkTypes[SBK_QURLINFO_PERMISSIONSPEC_IDX]; }
template<> inline PyTypeObject* SbkType< ::QUrlInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QURLINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHttpHeader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QHTTPHEADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHttpRequestHeader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QHTTPREQUESTHEADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkInterface::InterfaceFlag >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKINTERFACE_INTERFACEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QNetworkInterface::InterfaceFlag> >() { return SbkPySide_QtNetworkTypes[SBK_QFLAGS_QNETWORKINTERFACE_INTERFACEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIPv6Address >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QIPV6ADDRESS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHttpResponseHeader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QHTTPRESPONSEHEADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHostAddress::SpecialAddress >() { return SbkPySide_QtNetworkTypes[SBK_QHOSTADDRESS_SPECIALADDRESS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHostAddress >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QHOSTADDRESS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkProxy::ProxyType >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKPROXY_PROXYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkProxy::Capability >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKPROXY_CAPABILITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QNetworkProxy::Capability> >() { return SbkPySide_QtNetworkTypes[SBK_QFLAGS_QNETWORKPROXY_CAPABILITY__IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkProxy >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKPROXY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHostInfo::HostInfoError >() { return SbkPySide_QtNetworkTypes[SBK_QHOSTINFO_HOSTINFOERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHostInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QHOSTINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkAddressEntry >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKADDRESSENTRY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkConfigurationManager::Capability >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATIONMANAGER_CAPABILITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QNetworkConfigurationManager::Capability> >() { return SbkPySide_QtNetworkTypes[SBK_QFLAGS_QNETWORKCONFIGURATIONMANAGER_CAPABILITY__IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkConfigurationManager >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKCONFIGURATIONMANAGER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTcpServer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QTCPSERVER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkSession::State >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKSESSION_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkSession::SessionError >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKSESSION_SESSIONERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkSession >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKSESSION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkAccessManager::Operation >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKACCESSMANAGER_OPERATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkAccessManager::NetworkAccessibility >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKACCESSMANAGER_NETWORKACCESSIBILITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkAccessManager >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKACCESSMANAGER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractNetworkCache >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QABSTRACTNETWORKCACHE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkDiskCache >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKDISKCACHE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkCookieJar >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKCOOKIEJAR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFtp::State >() { return SbkPySide_QtNetworkTypes[SBK_QFTP_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFtp::Error >() { return SbkPySide_QtNetworkTypes[SBK_QFTP_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFtp::Command >() { return SbkPySide_QtNetworkTypes[SBK_QFTP_COMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFtp::TransferMode >() { return SbkPySide_QtNetworkTypes[SBK_QFTP_TRANSFERMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFtp::TransferType >() { return SbkPySide_QtNetworkTypes[SBK_QFTP_TRANSFERTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFtp >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QFTP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHttp::ConnectionMode >() { return SbkPySide_QtNetworkTypes[SBK_QHTTP_CONNECTIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHttp::State >() { return SbkPySide_QtNetworkTypes[SBK_QHTTP_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHttp::Error >() { return SbkPySide_QtNetworkTypes[SBK_QHTTP_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHttp >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QHTTP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLocalServer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QLOCALSERVER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractSocket::SocketType >() { return SbkPySide_QtNetworkTypes[SBK_QABSTRACTSOCKET_SOCKETTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSocket::NetworkLayerProtocol >() { return SbkPySide_QtNetworkTypes[SBK_QABSTRACTSOCKET_NETWORKLAYERPROTOCOL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSocket::SocketError >() { return SbkPySide_QtNetworkTypes[SBK_QABSTRACTSOCKET_SOCKETERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSocket::SocketState >() { return SbkPySide_QtNetworkTypes[SBK_QABSTRACTSOCKET_SOCKETSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSocket::SocketOption >() { return SbkPySide_QtNetworkTypes[SBK_QABSTRACTSOCKET_SOCKETOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractSocket >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QABSTRACTSOCKET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUdpSocket::BindFlag >() { return SbkPySide_QtNetworkTypes[SBK_QUDPSOCKET_BINDFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QUdpSocket::BindFlag> >() { return SbkPySide_QtNetworkTypes[SBK_QFLAGS_QUDPSOCKET_BINDFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QUdpSocket >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QUDPSOCKET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTcpSocket >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QTCPSOCKET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkReply::NetworkError >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKREPLY_NETWORKERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkReply >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKREPLY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLocalSocket::LocalSocketError >() { return SbkPySide_QtNetworkTypes[SBK_QLOCALSOCKET_LOCALSOCKETERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocalSocket::LocalSocketState >() { return SbkPySide_QtNetworkTypes[SBK_QLOCALSOCKET_LOCALSOCKETSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocalSocket >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QLOCALSOCKET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkCookie::RawForm >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKCOOKIE_RAWFORM_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkCookie >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKCOOKIE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSslCertificate::SubjectInfo >() { return SbkPySide_QtNetworkTypes[SBK_QSSLCERTIFICATE_SUBJECTINFO_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSslCertificate >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QSSLCERTIFICATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSslSocket::SslMode >() { return SbkPySide_QtNetworkTypes[SBK_QSSLSOCKET_SSLMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSslSocket::PeerVerifyMode >() { return SbkPySide_QtNetworkTypes[SBK_QSSLSOCKET_PEERVERIFYMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSslSocket >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QSSLSOCKET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSslKey >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QSSLKEY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QNetworkRequest::KnownHeaders >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKREQUEST_KNOWNHEADERS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkRequest::Attribute >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKREQUEST_ATTRIBUTE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkRequest::CacheLoadControl >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKREQUEST_CACHELOADCONTROL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkRequest::LoadControl >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKREQUEST_LOADCONTROL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkRequest::Priority >() { return SbkPySide_QtNetworkTypes[SBK_QNETWORKREQUEST_PRIORITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QNetworkRequest >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtNetworkTypes[SBK_QNETWORKREQUEST_IDX]); }

} // namespace Shiboken

#endif // SBK_QTNETWORK_PYTHON_H

