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



#ifndef SBK_QTCORE_PYTHON_H
#define SBK_QTCORE_PYTHON_H

#include <sbkpython.h>
#include <conversions.h>
#include <sbkenum.h>
#include <basewrapper.h>
#include <bindingmanager.h>
#include <memory>

#include <pysidesignal.h>
// Binded library includes
#include <qstatemachine.h>
#include <qprocess.h>
#include <qtextdocument.h>
#include <qeventtransition.h>
#include <qelapsedtimer.h>
#include <qfile.h>
#include <qrunnable.h>
#include <qbasictimer.h>
#include <qfilesystemwatcher.h>
#include <qfinalstate.h>
#include <qlibraryinfo.h>
#include <qsignalmapper.h>
#include <qabstractitemmodel.h>
#include <qthreadpool.h>
#include <qsettings.h>
#include <qobjectdefs.h>
#include <qabstracteventdispatcher.h>
#include <qresource.h>
#include <qtemporaryfile.h>
#include <qreadwritelock.h>
#include <qtconcurrentexception.h>
#include <qdiriterator.h>
#include <qsequentialanimationgroup.h>
#include <qmetaobject.h>
#include <qwaitcondition.h>
#include <qiodevice.h>
#include <qsystemsemaphore.h>
#include <qpoint.h>
#include <qsocketnotifier.h>
#include <QTextCodec>
#include <qthread.h>
#include <qstate.h>
#include <qabstractstate.h>
#include <qparallelanimationgroup.h>
#include <qmargins.h>
#include <qfactoryinterface.h>
#include <qcoreevent.h>
#include <qbytearraymatcher.h>
#include <qmutex.h>
#include <qsemaphore.h>
#include <qpluginloader.h>
#include <qtranslator.h>
#include <wtypes.h>
#include <qfileinfo.h>
#include <qtimeline.h>
#include <qabstractfileengine.h>
#include <qpropertyanimation.h>
#include <quuid.h>
#include <qdir.h>
#include <qhistorystate.h>
#include <qsignaltransition.h>
#include <qcryptographichash.h>
#include <qrect.h>
#include <qdatastream.h>
#include <qbitarray.h>
#include <qeasingcurve.h>
#include <qtextstream.h>
#include <qanimationgroup.h>
#include <qglobal.h>
#include <qfsfileengine.h>
#include <qabstractanimation.h>
#include <qmimedata.h>
#include <qbytearray.h>
#include <qvariantanimation.h>
#include <qtconcurrentreducekernel.h>
#include <qtextboundaryfinder.h>
#include <qnamespace.h>
#include <qregexp.h>
#include <qbuffer.h>
#include <qabstracttransition.h>
#include <qtextcodec.h>
#include <qdatetime.h>
#include <qpauseanimation.h>
#include <qxmlstream.h>
#include <qeventloop.h>
#include <qurl.h>
#include <qlocale.h>
#include <qcoreapplication.h>
#include <qobject.h>
#include <qsize.h>
#include <qline.h>
#include <qtimer.h>
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
#define SBK_QTCONCURRENT_IDX                                         294
#define SBK_QTCONCURRENT_REDUCEOPTION_IDX                            295
#define SBK_QFLAGS_QTCONCURRENT_REDUCEOPTION__IDX                    90
#define SBK_QT_IDX                                                   221
#define SBK_QT_GLOBALCOLOR_IDX                                       251
#define SBK_QT_KEYBOARDMODIFIER_IDX                                  260
#define SBK_QFLAGS_QT_KEYBOARDMODIFIER__IDX                          82
#define SBK_QT_MODIFIER_IDX                                          264
#define SBK_QT_MOUSEBUTTON_IDX                                       265
#define SBK_QFLAGS_QT_MOUSEBUTTON__IDX                               84
#define SBK_QT_ORIENTATION_IDX                                       267
#define SBK_QFLAGS_QT_ORIENTATION__IDX                               85
#define SBK_QT_FOCUSPOLICY_IDX                                       246
#define SBK_QT_SORTORDER_IDX                                         275
#define SBK_QT_TILERULE_IDX                                          280
#define SBK_QT_ALIGNMENTFLAG_IDX                                     222
#define SBK_QFLAGS_QT_ALIGNMENTFLAG__IDX                             75
#define SBK_QT_TEXTFLAG_IDX                                          277
#define SBK_QT_TEXTELIDEMODE_IDX                                     276
#define SBK_QT_WINDOWTYPE_IDX                                        293
#define SBK_QFLAGS_QT_WINDOWTYPE__IDX                                89
#define SBK_QT_WINDOWSTATE_IDX                                       292
#define SBK_QFLAGS_QT_WINDOWSTATE__IDX                               88
#define SBK_QT_WIDGETATTRIBUTE_IDX                                   289
#define SBK_QT_APPLICATIONATTRIBUTE_IDX                              225
#define SBK_QT_IMAGECONVERSIONFLAG_IDX                               253
#define SBK_QFLAGS_QT_IMAGECONVERSIONFLAG__IDX                       79
#define SBK_QT_BGMODE_IDX                                            229
#define SBK_QT_KEY_IDX                                               259
#define SBK_QT_ARROWTYPE_IDX                                         226
#define SBK_QT_PENSTYLE_IDX                                          270
#define SBK_QT_PENCAPSTYLE_IDX                                       268
#define SBK_QT_PENJOINSTYLE_IDX                                      269
#define SBK_QT_BRUSHSTYLE_IDX                                        230
#define SBK_QT_SIZEMODE_IDX                                          274
#define SBK_QT_UIEFFECT_IDX                                          287
#define SBK_QT_CURSORSHAPE_IDX                                       238
#define SBK_QT_TEXTFORMAT_IDX                                        278
#define SBK_QT_ASPECTRATIOMODE_IDX                                   227
#define SBK_QT_ANCHORATTRIBUTE_IDX                                   223
#define SBK_QT_DOCKWIDGETAREA_IDX                                    241
#define SBK_QFLAGS_QT_DOCKWIDGETAREA__IDX                            76
#define SBK_QT_DOCKWIDGETAREASIZES_IDX                               242
#define SBK_QT_TOOLBARAREA_IDX                                       282
#define SBK_QFLAGS_QT_TOOLBARAREA__IDX                               87
#define SBK_QT_TOOLBARAREASIZES_IDX                                  283
#define SBK_QT_DATEFORMAT_IDX                                        239
#define SBK_QT_TIMESPEC_IDX                                          281
#define SBK_QT_DAYOFWEEK_IDX                                         240
#define SBK_QT_SCROLLBARPOLICY_IDX                                   271
#define SBK_QT_CASESENSITIVITY_IDX                                   231
#define SBK_QT_CORNER_IDX                                            237
#define SBK_QT_CONNECTIONTYPE_IDX                                    234
#define SBK_QT_SHORTCUTCONTEXT_IDX                                   272
#define SBK_QT_FILLRULE_IDX                                          245
#define SBK_QT_MASKMODE_IDX                                          262
#define SBK_QT_CLIPOPERATION_IDX                                     233
#define SBK_QT_ITEMSELECTIONMODE_IDX                                 258
#define SBK_QT_TRANSFORMATIONMODE_IDX                                286
#define SBK_QT_AXIS_IDX                                              228
#define SBK_QT_FOCUSREASON_IDX                                       247
#define SBK_QT_CONTEXTMENUPOLICY_IDX                                 235
#define SBK_QT_INPUTMETHODQUERY_IDX                                  255
#define SBK_QT_INPUTMETHODHINT_IDX                                   254
#define SBK_QFLAGS_QT_INPUTMETHODHINT__IDX                           80
#define SBK_QT_TOOLBUTTONSTYLE_IDX                                   284
#define SBK_QT_LAYOUTDIRECTION_IDX                                   261
#define SBK_QT_ANCHORPOINT_IDX                                       224
#define SBK_QT_DROPACTION_IDX                                        243
#define SBK_QFLAGS_QT_DROPACTION__IDX                                77
#define SBK_QT_CHECKSTATE_IDX                                        232
#define SBK_QT_ITEMDATAROLE_IDX                                      256
#define SBK_QT_ITEMFLAG_IDX                                          257
#define SBK_QFLAGS_QT_ITEMFLAG__IDX                                  81
#define SBK_QT_MATCHFLAG_IDX                                         263
#define SBK_QFLAGS_QT_MATCHFLAG__IDX                                 83
#define SBK_QT_WINDOWMODALITY_IDX                                    291
#define SBK_QT_TEXTINTERACTIONFLAG_IDX                               279
#define SBK_QFLAGS_QT_TEXTINTERACTIONFLAG__IDX                       86
#define SBK_QT_EVENTPRIORITY_IDX                                     244
#define SBK_QT_SIZEHINT_IDX                                          273
#define SBK_QT_WINDOWFRAMESECTION_IDX                                290
#define SBK_QT_COORDINATESYSTEM_IDX                                  236
#define SBK_QT_TOUCHPOINTSTATE_IDX                                   285
#define SBK_QT_GESTURESTATE_IDX                                      249
#define SBK_QT_GESTURETYPE_IDX                                       250
#define SBK_QT_GESTUREFLAG_IDX                                       248
#define SBK_QFLAGS_QT_GESTUREFLAG__IDX                               78
#define SBK_QT_NAVIGATIONMODE_IDX                                    266
#define SBK_QT_CURSORMOVESTYLE_IDX                                   306
#define SBK_QT_HITTESTACCURACY_IDX                                   252
#define SBK_QT_WHITESPACEMODE_IDX                                    288
#define SBK_QTEXTDECODER_IDX                                         182
#define SBK_QLIBRARYINFO_IDX                                         97
#define SBK_QLIBRARYINFO_LIBRARYLOCATION_IDX                         98
#define SBK_QTEXTCODEC_IDX                                           179
#define SBK_QTEXTCODEC_CONVERSIONFLAG_IDX                            180
#define SBK_QFLAGS_QTEXTCODEC_CONVERSIONFLAG__IDX                    72
#define SBK_QTEXTCODEC_CONVERTERSTATE_IDX                            181
#define SBK_QTEXTENCODER_IDX                                         183
#define SBK_QXMLSTREAMATTRIBUTE_IDX                                  210
#define SBK_QXMLSTREAMENTITYRESOLVER_IDX                             213
#define SBK_QXMLSTREAMWRITER_IDX                                     220
#define SBK_QMUTEX_IDX                                               119
#define SBK_QMUTEX_RECURSIONMODE_IDX                                 120
#define SBK_QXMLSTREAMENTITYDECLARATION_IDX                          212
#define SBK_QXMLSTREAMNOTATIONDECLARATION_IDX                        215
#define SBK_QXMLSTREAMNAMESPACEDECLARATION_IDX                       214
#define SBK_QXMLSTREAMATTRIBUTES_IDX                                 211
#define SBK_QVECTOR_QXMLSTREAMATTRIBUTE_IDX                          211
#define SBK_QMUTEXLOCKER_IDX                                         121
#define SBK_QXMLSTREAMREADER_IDX                                     216
#define SBK_QXMLSTREAMREADER_TOKENTYPE_IDX                           219
#define SBK_QXMLSTREAMREADER_READELEMENTTEXTBEHAVIOUR_IDX            218
#define SBK_QXMLSTREAMREADER_ERROR_IDX                               217
#define SBK_QUUID_IDX                                                204
#define SBK_QUUID_VARIANT_IDX                                        205
#define SBK_QUUID_VERSION_IDX                                        206
#define SBK_QTEXTBOUNDARYFINDER_IDX                                  176
#define SBK_QTEXTBOUNDARYFINDER_BOUNDARYTYPE_IDX                     178
#define SBK_QTEXTBOUNDARYFINDER_BOUNDARYREASON_IDX                   177
#define SBK_QFLAGS_QTEXTBOUNDARYFINDER_BOUNDARYREASON__IDX           71
#define SBK_QFACTORYINTERFACE_IDX                                    55
#define SBK_QPROCESSENVIRONMENT_IDX                                  135
#define SBK_QABSTRACTFILEENGINE_IDX                                  7
#define SBK_QABSTRACTFILEENGINE_FILEFLAG_IDX                         9
#define SBK_QFLAGS_QABSTRACTFILEENGINE_FILEFLAG__IDX                 63
#define SBK_QABSTRACTFILEENGINE_FILENAME_IDX                         10
#define SBK_QABSTRACTFILEENGINE_FILEOWNER_IDX                        11
#define SBK_QABSTRACTFILEENGINE_FILETIME_IDX                         12
#define SBK_QABSTRACTFILEENGINE_EXTENSION_IDX                        8
#define SBK_QFSFILEENGINE_IDX                                        54
#define SBK_QABSTRACTFILEENGINEHANDLER_IDX                           13
#define SBK_QABSTRACTFILEENGINEITERATOR_IDX                          14
#define SBK_QDIR_IDX                                                 39
#define SBK_QDIR_FILTER_IDX                                          40
#define SBK_QFLAGS_QDIR_FILTER__IDX                                  64
#define SBK_QDIR_SORTFLAG_IDX                                        41
#define SBK_QFLAGS_QDIR_SORTFLAG__IDX                                65
#define SBK_QDIRITERATOR_IDX                                         42
#define SBK_QDIRITERATOR_ITERATORFLAG_IDX                            43
#define SBK_QFLAGS_QDIRITERATOR_ITERATORFLAG__IDX                    66
#define SBK_QFILEINFO_IDX                                            60
#define SBK_QWAITCONDITION_IDX                                       208
#define SBK_QRUNNABLE_IDX                                            146
#define SBK_QREADLOCKER_IDX                                          137
#define SBK_QSEMAPHORE_IDX                                           147
#define SBK_QWRITELOCKER_IDX                                         209
#define SBK_QREADWRITELOCK_IDX                                       138
#define SBK_QREADWRITELOCK_RECURSIONMODE_IDX                         139
#define SBK_QTEXTSTREAMMANIPULATOR_IDX                               189
#define SBK_QRECTF_IDX                                               141
#define SBK_QRECT_IDX                                                140
#define SBK_QSIZEF_IDX                                               156
#define SBK_QREGEXP_IDX                                              142
#define SBK_QREGEXP_PATTERNSYNTAX_IDX                                144
#define SBK_QREGEXP_CARETMODE_IDX                                    143
#define SBK_QLOCALE_IDX                                              102
#define SBK_QLOCALE_LANGUAGE_IDX                                     105
#define SBK_QLOCALE_SCRIPT_IDX                                       305
#define SBK_QLOCALE_COUNTRY_IDX                                      103
#define SBK_QLOCALE_MEASUREMENTSYSTEM_IDX                            106
#define SBK_QLOCALE_FORMATTYPE_IDX                                   104
#define SBK_QLOCALE_NUMBEROPTION_IDX                                 107
#define SBK_QFLAGS_QLOCALE_NUMBEROPTION__IDX                         70
#define SBK_QLOCALE_CURRENCYSYMBOLFORMAT_IDX                         303
#define SBK_QLOCALE_QUOTATIONSTYLE_IDX                               304
#define SBK_QRESOURCE_IDX                                            145
#define SBK_QSIZE_IDX                                                155
#define SBK_QMARGINS_IDX                                             108
#define SBK_QLINE_IDX                                                99
#define SBK_QPOINTF_IDX                                              128
#define SBK_QDATE_IDX                                                36
#define SBK_QDATE_MONTHNAMETYPE_IDX                                  37
#define SBK_QDATETIME_IDX                                            38
#define SBK_QTIME_IDX                                                193
#define SBK_QPOINT_IDX                                               127
#define SBK_QELAPSEDTIMER_IDX                                        47
#define SBK_QELAPSEDTIMER_CLOCKTYPE_IDX                              48
#define SBK_QSYSTEMLOCALE_IDX                                        170
#define SBK_QSYSTEMLOCALE_QUERYTYPE_IDX                              171
#define SBK_QLINEF_IDX                                               100
#define SBK_QLINEF_INTERSECTTYPE_IDX                                 101
#define SBK_QCRYPTOGRAPHICHASH_IDX                                   29
#define SBK_QCRYPTOGRAPHICHASH_ALGORITHM_IDX                         30
#define SBK_QBITARRAY_IDX                                            22
#define SBK_QBYTEARRAYMATCHER_IDX                                    25
#define SBK_QEASINGCURVE_IDX                                         45
#define SBK_QEASINGCURVE_TYPE_IDX                                    46
#define SBK_QMETAENUM_IDX                                            110
#define SBK_QBASICTIMER_IDX                                          21
#define SBK_QSYSTEMSEMAPHORE_IDX                                     172
#define SBK_QSYSTEMSEMAPHORE_ACCESSMODE_IDX                          173
#define SBK_QSYSTEMSEMAPHORE_SYSTEMSEMAPHOREERROR_IDX                174
#define SBK_QMETAPROPERTY_IDX                                        116
#define SBK_QEVENT_IDX                                               49
#define SBK_QEVENT_TYPE_IDX                                          50
#define SBK_QTIMEREVENT_IDX                                          199
#define SBK_QCHILDEVENT_IDX                                          26
#define SBK_QDYNAMICPROPERTYCHANGEEVENT_IDX                          44
#define SBK_QMETACLASSINFO_IDX                                       109
#define SBK_QPERSISTENTMODELINDEX_IDX                                125
#define SBK_QMODELINDEX_IDX                                          118
#define SBK_QDATASTREAM_IDX                                          31
#define SBK_QDATASTREAM_VERSION_IDX                                  35
#define SBK_QDATASTREAM_BYTEORDER_IDX                                32
#define SBK_QDATASTREAM_STATUS_IDX                                   34
#define SBK_QDATASTREAM_FLOATINGPOINTPRECISION_IDX                   33
#define SBK_QOBJECT_IDX                                              122
#define SBK_QTRANSLATOR_IDX                                          200
#define SBK_QABSTRACTANIMATION_IDX                                   2
#define SBK_QABSTRACTANIMATION_DIRECTION_IDX                         4
#define SBK_QABSTRACTANIMATION_STATE_IDX                             5
#define SBK_QABSTRACTANIMATION_DELETIONPOLICY_IDX                    3
#define SBK_QANIMATIONGROUP_IDX                                      20
#define SBK_QSEQUENTIALANIMATIONGROUP_IDX                            148
#define SBK_QPARALLELANIMATIONGROUP_IDX                              123
#define SBK_QVARIANTANIMATION_IDX                                    207
#define SBK_QPROPERTYANIMATION_IDX                                   136
#define SBK_QPAUSEANIMATION_IDX                                      124
#define SBK_QABSTRACTSTATE_IDX                                       17
#define SBK_QSTATE_IDX                                               159
#define SBK_QSTATE_CHILDMODE_IDX                                     160
#define SBK_QSTATEMACHINE_IDX                                        161
#define SBK_QSTATEMACHINE_EVENTPRIORITY_IDX                          163
#define SBK_QSTATEMACHINE_RESTOREPOLICY_IDX                          164
#define SBK_QSTATEMACHINE_ERROR_IDX                                  162
#define SBK_QSTATEMACHINE_WRAPPEDEVENT_IDX                           166
#define SBK_QSTATEMACHINE_SIGNALEVENT_IDX                            165
#define SBK_QFINALSTATE_IDX                                          62
#define SBK_QHISTORYSTATE_IDX                                        93
#define SBK_QHISTORYSTATE_HISTORYTYPE_IDX                            94
#define SBK_QABSTRACTITEMMODEL_IDX                                   15
#define SBK_QABSTRACTLISTMODEL_IDX                                   16
#define SBK_QABSTRACTTABLEMODEL_IDX                                  18
#define SBK_QABSTRACTTRANSITION_IDX                                  19
#define SBK_QEVENTTRANSITION_IDX                                     53
#define SBK_QSIGNALTRANSITION_IDX                                    154
#define SBK_QSOCKETNOTIFIER_IDX                                      157
#define SBK_QSOCKETNOTIFIER_TYPE_IDX                                 158
#define SBK_QTHREAD_IDX                                              190
#define SBK_QTHREAD_PRIORITY_IDX                                     191
#define SBK_QTIMER_IDX                                               198
#define SBK_QTIMELINE_IDX                                            194
#define SBK_QTIMELINE_STATE_IDX                                      197
#define SBK_QTIMELINE_DIRECTION_IDX                                  196
#define SBK_QTIMELINE_CURVESHAPE_IDX                                 195
#define SBK_QPLUGINLOADER_IDX                                        126
#define SBK_QSIGNALMAPPER_IDX                                        153
#define SBK_QFILESYSTEMWATCHER_IDX                                   61
#define SBK_QMIMEDATA_IDX                                            117
#define SBK_QEVENTLOOP_IDX                                           51
#define SBK_QEVENTLOOP_PROCESSEVENTSFLAG_IDX                         52
#define SBK_QFLAGS_QEVENTLOOP_PROCESSEVENTSFLAG__IDX                 67
#define SBK_QCOREAPPLICATION_IDX                                     27
#define SBK_QCOREAPPLICATION_APPLICATIONFLAGS_IDX                    300
#define SBK_QCOREAPPLICATION_ENCODING_IDX                            28
#define SBK_QABSTRACTEVENTDISPATCHER_IDX                             6
#define SBK_QIODEVICE_IDX                                            95
#define SBK_QIODEVICE_OPENMODEFLAG_IDX                               96
#define SBK_QFLAGS_QIODEVICE_OPENMODEFLAG__IDX                       69
#define SBK_QBUFFER_IDX                                              23
#define SBK_QFILE_IDX                                                56
#define SBK_QFILE_FILEERROR_IDX                                      57
#define SBK_QFILE_PERMISSION_IDX                                     59
#define SBK_QFLAGS_QFILE_PERMISSION__IDX                             68
#define SBK_QFILE_FILEHANDLEFLAG_IDX                                 301
#define SBK_QFLAGS_QFILE_FILEHANDLEFLAG__IDX                         302
#define SBK_QFILE_MEMORYMAPFLAGS_IDX                                 58
#define SBK_QTEMPORARYFILE_IDX                                       175
#define SBK_QTEXTSTREAM_IDX                                          184
#define SBK_QTEXTSTREAM_REALNUMBERNOTATION_IDX                       187
#define SBK_QTEXTSTREAM_FIELDALIGNMENT_IDX                           185
#define SBK_QTEXTSTREAM_STATUS_IDX                                   188
#define SBK_QTEXTSTREAM_NUMBERFLAG_IDX                               186
#define SBK_QFLAGS_QTEXTSTREAM_NUMBERFLAG__IDX                       73
#define SBK_QPROCESS_IDX                                             129
#define SBK_QPROCESS_PROCESSERROR_IDX                                133
#define SBK_QPROCESS_PROCESSSTATE_IDX                                134
#define SBK_QPROCESS_PROCESSCHANNEL_IDX                              131
#define SBK_QPROCESS_PROCESSCHANNELMODE_IDX                          132
#define SBK_QPROCESS_EXITSTATUS_IDX                                  130
#define SBK_QTHREADPOOL_IDX                                          192
#define SBK_QSETTINGS_IDX                                            149
#define SBK_QSETTINGS_STATUS_IDX                                     152
#define SBK_QSETTINGS_FORMAT_IDX                                     150
#define SBK_QSETTINGS_SCOPE_IDX                                      151
#define SBK_QBYTEARRAY_IDX                                           24
#define SBK_QURL_IDX                                                 201
#define SBK_QURL_PARSINGMODE_IDX                                     203
#define SBK_QURL_FORMATTINGOPTION_IDX                                202
#define SBK_QFLAGS_QURL_FORMATTINGOPTION__IDX                        74
#define SBK_MSG_IDX                                                  0
#define SBK_POINT_IDX                                                1
#define SBK_QGENERICARGUMENT_IDX                                     91
#define SBK_QMETAMETHOD_IDX                                          111
#define SBK_QMETAMETHOD_ACCESS_IDX                                   112
#define SBK_QMETAMETHOD_METHODTYPE_IDX                               113
#define SBK_QGENERICRETURNARGUMENT_IDX                               92
#define SBK_QMETAOBJECT_IDX                                          114
#define SBK_QMETAOBJECT_CALL_IDX                                     115
#define SBK_QSYSINFO_IDX                                             167
#define SBK_QSYSINFO_SIZES_IDX                                       169
#define SBK_QSYSINFO_ENDIAN_IDX                                      168
#define SBK_QTMSGTYPE_IDX                                            296
#define SBK_QTVALIDLICENSEFOROPENVGMODULE_IDX                        299
#define SBK_QTVALIDLICENSEFORMULTIMEDIAMODULE_IDX                    298
#define SBK_QTVALIDLICENSEFORDECLARATIVEMODULE_IDX                   297
#define SBK_QtCore_IDX_COUNT                                         307

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtCoreTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtCoreTypeConverters;

// Converter indices
#define SBK_QSTRING_IDX                                              0
#define SBK_QVARIANT_IDX                                             1
#define SBK_QBOOL_IDX                                                2
#define SBK_QVARIANT_TYPE_IDX                                        3
#define SBK_HWND_IDX                                                 4
#define SBK_QSTRINGREF_IDX                                           5
#define SBK_QSTRINGLIST_IDX                                          6
#define SBK_QMODELINDEXLIST_IDX                                      7
#define SBK_QCHAR_IDX                                                8
#define SBK_QTCORE_QLIST_QBYTEARRAY_IDX                              9 // QList<QByteArray >
#define SBK_QTCORE_QLIST_INT_IDX                                     10 // QList<int >
#define SBK_QTCORE_QVECTOR_QXMLSTREAMATTRIBUTE_IDX                   11 // QVector<QXmlStreamAttribute > &
#define SBK_QTCORE_QLIST_QXMLSTREAMATTRIBUTE_IDX                     12 // const QList<QXmlStreamAttribute > &
#define SBK_QTCORE_QVECTOR_QXMLSTREAMNAMESPACEDECLARATION_IDX        13 // const QVector<QXmlStreamNamespaceDeclaration > &
#define SBK_QTCORE_QVECTOR_QXMLSTREAMENTITYDECLARATION_IDX           14 // QVector<QXmlStreamEntityDeclaration >
#define SBK_QTCORE_QVECTOR_QXMLSTREAMNOTATIONDECLARATION_IDX         15 // QVector<QXmlStreamNotationDeclaration >
#define SBK_QTCORE_QLIST_QFILEINFO_IDX                               16 // QList<QFileInfo >
#define SBK_QTCORE_QLIST_QLOCALE_COUNTRY_IDX                         17 // QList<QLocale::Country >
#define SBK_QTCORE_QLIST_QLOCALE_IDX                                 18 // QList<QLocale >
#define SBK_QTCORE_QLIST_QT_DAYOFWEEK_IDX                            19 // QList<Qt::DayOfWeek >
#define SBK_QTCORE_QLIST_QOBJECTPTR_IDX                              20 // const QList<QObject * > &
#define SBK_QTCORE_QPAIR_QREAL_QVARIANT_IDX                          21 // QPair<qreal, QVariant >
#define SBK_QTCORE_QVECTOR_QPAIR_QREAL_QVARIANT_IDX                  22 // QVector<QPair<qreal, QVariant > >
#define SBK_QTCORE_QLIST_QABSTRACTTRANSITIONPTR_IDX                  23 // QList<QAbstractTransition * >
#define SBK_QTCORE_QSET_QABSTRACTSTATEPTR_IDX                        24 // QSet<QAbstractState * >
#define SBK_QTCORE_QLIST_QABSTRACTANIMATIONPTR_IDX                   25 // QList<QAbstractAnimation * >
#define SBK_QTCORE_QLIST_QVARIANT_IDX                                26 // const QList<QVariant > &
#define SBK_QTCORE_QMAP_INT_QVARIANT_IDX                             27 // QMap<int, QVariant >
#define SBK_QTCORE_QHASH_INT_QBYTEARRAY_IDX                          28 // const QHash<int, QByteArray > &
#define SBK_QTCORE_QLIST_QABSTRACTSTATEPTR_IDX                       29 // const QList<QAbstractState * > &
#define SBK_QTCORE_QLIST_QURL_IDX                                    30 // const QList<QUrl > &
#define SBK_QTCORE_QPAIR_INT_INT_IDX                                 31 // QPair<int, int >
#define SBK_QTCORE_QLIST_QPAIR_INT_INT_IDX                           32 // QList<QPair<int, int > >
#define SBK_QTCORE_QPAIR_QBYTEARRAY_QBYTEARRAY_IDX                   33 // QPair<QByteArray, QByteArray >
#define SBK_QTCORE_QLIST_QPAIR_QBYTEARRAY_QBYTEARRAY_IDX             34 // QList<QPair<QByteArray, QByteArray > >
#define SBK_QTCORE_QPAIR_QSTRING_QSTRING_IDX                         35 // QPair<QString, QString >
#define SBK_QTCORE_QLIST_QPAIR_QSTRING_QSTRING_IDX                   36 // QList<QPair<QString, QString > >
#define SBK_QTCORE_QLIST_QSTRING_IDX                                 37 // QList<QString >
#define SBK_QTCORE_QMAP_QSTRING_QVARIANT_IDX                         38 // QMap<QString, QVariant >
#define SBK_QtCore_CONVERTERS_IDX_COUNT                              39

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QtMsgType >() { return SbkPySide_QtCoreTypes[SBK_QTMSGTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QtValidLicenseForOpenVGModule >() { return SbkPySide_QtCoreTypes[SBK_QTVALIDLICENSEFOROPENVGMODULE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QtValidLicenseForMultimediaModule >() { return SbkPySide_QtCoreTypes[SBK_QTVALIDLICENSEFORMULTIMEDIAMODULE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QtValidLicenseForDeclarativeModule >() { return SbkPySide_QtCoreTypes[SBK_QTVALIDLICENSEFORDECLARATIVEMODULE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QtConcurrent::ReduceOption >() { return SbkPySide_QtCoreTypes[SBK_QTCONCURRENT_REDUCEOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QtConcurrent::ReduceOption> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QTCONCURRENT_REDUCEOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::GlobalColor >() { return SbkPySide_QtCoreTypes[SBK_QT_GLOBALCOLOR_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::KeyboardModifier >() { return SbkPySide_QtCoreTypes[SBK_QT_KEYBOARDMODIFIER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::KeyboardModifier> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_KEYBOARDMODIFIER__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::Modifier >() { return SbkPySide_QtCoreTypes[SBK_QT_MODIFIER_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::MouseButton >() { return SbkPySide_QtCoreTypes[SBK_QT_MOUSEBUTTON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::MouseButton> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_MOUSEBUTTON__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::Orientation >() { return SbkPySide_QtCoreTypes[SBK_QT_ORIENTATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::Orientation> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_ORIENTATION__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::FocusPolicy >() { return SbkPySide_QtCoreTypes[SBK_QT_FOCUSPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::SortOrder >() { return SbkPySide_QtCoreTypes[SBK_QT_SORTORDER_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TileRule >() { return SbkPySide_QtCoreTypes[SBK_QT_TILERULE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::AlignmentFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_ALIGNMENTFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::AlignmentFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_ALIGNMENTFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TextFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_TEXTFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TextElideMode >() { return SbkPySide_QtCoreTypes[SBK_QT_TEXTELIDEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::WindowType >() { return SbkPySide_QtCoreTypes[SBK_QT_WINDOWTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::WindowType> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_WINDOWTYPE__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::WindowState >() { return SbkPySide_QtCoreTypes[SBK_QT_WINDOWSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::WindowState> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_WINDOWSTATE__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::WidgetAttribute >() { return SbkPySide_QtCoreTypes[SBK_QT_WIDGETATTRIBUTE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ApplicationAttribute >() { return SbkPySide_QtCoreTypes[SBK_QT_APPLICATIONATTRIBUTE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ImageConversionFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_IMAGECONVERSIONFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::ImageConversionFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_IMAGECONVERSIONFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::BGMode >() { return SbkPySide_QtCoreTypes[SBK_QT_BGMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::Key >() { return SbkPySide_QtCoreTypes[SBK_QT_KEY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ArrowType >() { return SbkPySide_QtCoreTypes[SBK_QT_ARROWTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::PenStyle >() { return SbkPySide_QtCoreTypes[SBK_QT_PENSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::PenCapStyle >() { return SbkPySide_QtCoreTypes[SBK_QT_PENCAPSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::PenJoinStyle >() { return SbkPySide_QtCoreTypes[SBK_QT_PENJOINSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::BrushStyle >() { return SbkPySide_QtCoreTypes[SBK_QT_BRUSHSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::SizeMode >() { return SbkPySide_QtCoreTypes[SBK_QT_SIZEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::UIEffect >() { return SbkPySide_QtCoreTypes[SBK_QT_UIEFFECT_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::CursorShape >() { return SbkPySide_QtCoreTypes[SBK_QT_CURSORSHAPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TextFormat >() { return SbkPySide_QtCoreTypes[SBK_QT_TEXTFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::AspectRatioMode >() { return SbkPySide_QtCoreTypes[SBK_QT_ASPECTRATIOMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::AnchorAttribute >() { return SbkPySide_QtCoreTypes[SBK_QT_ANCHORATTRIBUTE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::DockWidgetArea >() { return SbkPySide_QtCoreTypes[SBK_QT_DOCKWIDGETAREA_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::DockWidgetArea> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_DOCKWIDGETAREA__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::DockWidgetAreaSizes >() { return SbkPySide_QtCoreTypes[SBK_QT_DOCKWIDGETAREASIZES_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ToolBarArea >() { return SbkPySide_QtCoreTypes[SBK_QT_TOOLBARAREA_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::ToolBarArea> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_TOOLBARAREA__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ToolBarAreaSizes >() { return SbkPySide_QtCoreTypes[SBK_QT_TOOLBARAREASIZES_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::DateFormat >() { return SbkPySide_QtCoreTypes[SBK_QT_DATEFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TimeSpec >() { return SbkPySide_QtCoreTypes[SBK_QT_TIMESPEC_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::DayOfWeek >() { return SbkPySide_QtCoreTypes[SBK_QT_DAYOFWEEK_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ScrollBarPolicy >() { return SbkPySide_QtCoreTypes[SBK_QT_SCROLLBARPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::CaseSensitivity >() { return SbkPySide_QtCoreTypes[SBK_QT_CASESENSITIVITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::Corner >() { return SbkPySide_QtCoreTypes[SBK_QT_CORNER_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ConnectionType >() { return SbkPySide_QtCoreTypes[SBK_QT_CONNECTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ShortcutContext >() { return SbkPySide_QtCoreTypes[SBK_QT_SHORTCUTCONTEXT_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::FillRule >() { return SbkPySide_QtCoreTypes[SBK_QT_FILLRULE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::MaskMode >() { return SbkPySide_QtCoreTypes[SBK_QT_MASKMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ClipOperation >() { return SbkPySide_QtCoreTypes[SBK_QT_CLIPOPERATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ItemSelectionMode >() { return SbkPySide_QtCoreTypes[SBK_QT_ITEMSELECTIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TransformationMode >() { return SbkPySide_QtCoreTypes[SBK_QT_TRANSFORMATIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::Axis >() { return SbkPySide_QtCoreTypes[SBK_QT_AXIS_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::FocusReason >() { return SbkPySide_QtCoreTypes[SBK_QT_FOCUSREASON_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ContextMenuPolicy >() { return SbkPySide_QtCoreTypes[SBK_QT_CONTEXTMENUPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::InputMethodQuery >() { return SbkPySide_QtCoreTypes[SBK_QT_INPUTMETHODQUERY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::InputMethodHint >() { return SbkPySide_QtCoreTypes[SBK_QT_INPUTMETHODHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::InputMethodHint> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_INPUTMETHODHINT__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ToolButtonStyle >() { return SbkPySide_QtCoreTypes[SBK_QT_TOOLBUTTONSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::LayoutDirection >() { return SbkPySide_QtCoreTypes[SBK_QT_LAYOUTDIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::AnchorPoint >() { return SbkPySide_QtCoreTypes[SBK_QT_ANCHORPOINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::DropAction >() { return SbkPySide_QtCoreTypes[SBK_QT_DROPACTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::DropAction> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_DROPACTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::CheckState >() { return SbkPySide_QtCoreTypes[SBK_QT_CHECKSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ItemDataRole >() { return SbkPySide_QtCoreTypes[SBK_QT_ITEMDATAROLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::ItemFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_ITEMFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::ItemFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_ITEMFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::MatchFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_MATCHFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::MatchFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_MATCHFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::WindowModality >() { return SbkPySide_QtCoreTypes[SBK_QT_WINDOWMODALITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TextInteractionFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_TEXTINTERACTIONFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::TextInteractionFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_TEXTINTERACTIONFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::EventPriority >() { return SbkPySide_QtCoreTypes[SBK_QT_EVENTPRIORITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::SizeHint >() { return SbkPySide_QtCoreTypes[SBK_QT_SIZEHINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::WindowFrameSection >() { return SbkPySide_QtCoreTypes[SBK_QT_WINDOWFRAMESECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::CoordinateSystem >() { return SbkPySide_QtCoreTypes[SBK_QT_COORDINATESYSTEM_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::TouchPointState >() { return SbkPySide_QtCoreTypes[SBK_QT_TOUCHPOINTSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::GestureState >() { return SbkPySide_QtCoreTypes[SBK_QT_GESTURESTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::GestureType >() { return SbkPySide_QtCoreTypes[SBK_QT_GESTURETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::GestureFlag >() { return SbkPySide_QtCoreTypes[SBK_QT_GESTUREFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Qt::GestureFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QT_GESTUREFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::NavigationMode >() { return SbkPySide_QtCoreTypes[SBK_QT_NAVIGATIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::CursorMoveStyle >() { return SbkPySide_QtCoreTypes[SBK_QT_CURSORMOVESTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::HitTestAccuracy >() { return SbkPySide_QtCoreTypes[SBK_QT_HITTESTACCURACY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Qt::WhiteSpaceMode >() { return SbkPySide_QtCoreTypes[SBK_QT_WHITESPACEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextDecoder >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTDECODER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLibraryInfo::LibraryLocation >() { return SbkPySide_QtCoreTypes[SBK_QLIBRARYINFO_LIBRARYLOCATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLibraryInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QLIBRARYINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextCodec::ConversionFlag >() { return SbkPySide_QtCoreTypes[SBK_QTEXTCODEC_CONVERSIONFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextCodec::ConversionFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QTEXTCODEC_CONVERSIONFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextCodec >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTCODEC_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextCodec::ConverterState >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTCODEC_CONVERTERSTATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextEncoder >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTENCODER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamAttribute >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMATTRIBUTE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamEntityResolver >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMENTITYRESOLVER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamWriter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMWRITER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMutex::RecursionMode >() { return SbkPySide_QtCoreTypes[SBK_QMUTEX_RECURSIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMutex >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMUTEX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamEntityDeclaration >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMENTITYDECLARATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamNotationDeclaration >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMNOTATIONDECLARATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamNamespaceDeclaration >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMNAMESPACEDECLARATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamAttributes >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMATTRIBUTES_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMutexLocker >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMUTEXLOCKER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QXmlStreamReader::TokenType >() { return SbkPySide_QtCoreTypes[SBK_QXMLSTREAMREADER_TOKENTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QXmlStreamReader::ReadElementTextBehaviour >() { return SbkPySide_QtCoreTypes[SBK_QXMLSTREAMREADER_READELEMENTTEXTBEHAVIOUR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QXmlStreamReader::Error >() { return SbkPySide_QtCoreTypes[SBK_QXMLSTREAMREADER_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QXmlStreamReader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QXMLSTREAMREADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUuid::Variant >() { return SbkPySide_QtCoreTypes[SBK_QUUID_VARIANT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QUuid::Version >() { return SbkPySide_QtCoreTypes[SBK_QUUID_VERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QUuid >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QUUID_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextBoundaryFinder::BoundaryType >() { return SbkPySide_QtCoreTypes[SBK_QTEXTBOUNDARYFINDER_BOUNDARYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextBoundaryFinder::BoundaryReason >() { return SbkPySide_QtCoreTypes[SBK_QTEXTBOUNDARYFINDER_BOUNDARYREASON_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextBoundaryFinder::BoundaryReason> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QTEXTBOUNDARYFINDER_BOUNDARYREASON__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextBoundaryFinder >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTBOUNDARYFINDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFactoryInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QFACTORYINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QProcessEnvironment >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPROCESSENVIRONMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngine::FileFlag >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINE_FILEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QAbstractFileEngine::FileFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QABSTRACTFILEENGINE_FILEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngine::FileName >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINE_FILENAME_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngine::FileOwner >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINE_FILEOWNER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngine::FileTime >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINE_FILETIME_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngine::Extension >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINE_EXTENSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFSFileEngine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QFSFILEENGINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngineHandler >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINEHANDLER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractFileEngineIterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTFILEENGINEITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDir::Filter >() { return SbkPySide_QtCoreTypes[SBK_QDIR_FILTER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QDir::Filter> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QDIR_FILTER__IDX]; }
template<> inline PyTypeObject* SbkType< ::QDir::SortFlag >() { return SbkPySide_QtCoreTypes[SBK_QDIR_SORTFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QDir::SortFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QDIR_SORTFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QDir >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QDIR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDirIterator::IteratorFlag >() { return SbkPySide_QtCoreTypes[SBK_QDIRITERATOR_ITERATORFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QDirIterator::IteratorFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QDIRITERATOR_ITERATORFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QDirIterator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QDIRITERATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFileInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QFILEINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWaitCondition >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QWAITCONDITION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRunnable >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QRUNNABLE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QReadLocker >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QREADLOCKER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSemaphore >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSEMAPHORE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QWriteLocker >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QWRITELOCKER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QReadWriteLock::RecursionMode >() { return SbkPySide_QtCoreTypes[SBK_QREADWRITELOCK_RECURSIONMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QReadWriteLock >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QREADWRITELOCK_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextStreamManipulator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTSTREAMMANIPULATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRectF >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QRECTF_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QRECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSizeF >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSIZEF_IDX]); }
template<> inline PyTypeObject* SbkType< ::QRegExp::PatternSyntax >() { return SbkPySide_QtCoreTypes[SBK_QREGEXP_PATTERNSYNTAX_IDX]; }
template<> inline PyTypeObject* SbkType< ::QRegExp::CaretMode >() { return SbkPySide_QtCoreTypes[SBK_QREGEXP_CARETMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QRegExp >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QREGEXP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLocale::Language >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_LANGUAGE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::Script >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_SCRIPT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::Country >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_COUNTRY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::MeasurementSystem >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_MEASUREMENTSYSTEM_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::FormatType >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_FORMATTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::NumberOption >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_NUMBEROPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QLocale::NumberOption> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QLOCALE_NUMBEROPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::CurrencySymbolFormat >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_CURRENCYSYMBOLFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale::QuotationStyle >() { return SbkPySide_QtCoreTypes[SBK_QLOCALE_QUOTATIONSTYLE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLocale >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QLOCALE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QResource >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QRESOURCE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSize >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSIZE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMargins >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMARGINS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QLINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPointF >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPOINTF_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDate::MonthNameType >() { return SbkPySide_QtCoreTypes[SBK_QDATE_MONTHNAMETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDate >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QDATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDateTime >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QDATETIME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTime >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTIME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPoint >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPOINT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QElapsedTimer::ClockType >() { return SbkPySide_QtCoreTypes[SBK_QELAPSEDTIMER_CLOCKTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QElapsedTimer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QELAPSEDTIMER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSystemLocale::QueryType >() { return SbkPySide_QtCoreTypes[SBK_QSYSTEMLOCALE_QUERYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSystemLocale >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSYSTEMLOCALE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QLineF::IntersectType >() { return SbkPySide_QtCoreTypes[SBK_QLINEF_INTERSECTTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QLineF >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QLINEF_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCryptographicHash::Algorithm >() { return SbkPySide_QtCoreTypes[SBK_QCRYPTOGRAPHICHASH_ALGORITHM_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCryptographicHash >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QCRYPTOGRAPHICHASH_IDX]); }
template<> inline PyTypeObject* SbkType< ::QBitArray >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QBITARRAY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QByteArrayMatcher >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QBYTEARRAYMATCHER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QEasingCurve::Type >() { return SbkPySide_QtCoreTypes[SBK_QEASINGCURVE_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QEasingCurve >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QEASINGCURVE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMetaEnum >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMETAENUM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QBasicTimer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QBASICTIMER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSystemSemaphore::AccessMode >() { return SbkPySide_QtCoreTypes[SBK_QSYSTEMSEMAPHORE_ACCESSMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSystemSemaphore::SystemSemaphoreError >() { return SbkPySide_QtCoreTypes[SBK_QSYSTEMSEMAPHORE_SYSTEMSEMAPHOREERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSystemSemaphore >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSYSTEMSEMAPHORE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMetaProperty >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMETAPROPERTY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QEvent::Type >() { return SbkPySide_QtCoreTypes[SBK_QEVENT_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTimerEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTIMEREVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QChildEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QCHILDEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDynamicPropertyChangeEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QDYNAMICPROPERTYCHANGEEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMetaClassInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMETACLASSINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPersistentModelIndex >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPERSISTENTMODELINDEX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QModelIndex >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMODELINDEX_IDX]); }
template<> inline PyTypeObject* SbkType< ::QDataStream::Version >() { return SbkPySide_QtCoreTypes[SBK_QDATASTREAM_VERSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDataStream::ByteOrder >() { return SbkPySide_QtCoreTypes[SBK_QDATASTREAM_BYTEORDER_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDataStream::Status >() { return SbkPySide_QtCoreTypes[SBK_QDATASTREAM_STATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDataStream::FloatingPointPrecision >() { return SbkPySide_QtCoreTypes[SBK_QDATASTREAM_FLOATINGPOINTPRECISION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QDataStream >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QDATASTREAM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTranslator >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTRANSLATOR_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractAnimation::Direction >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTANIMATION_DIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractAnimation::State >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTANIMATION_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractAnimation::DeletionPolicy >() { return SbkPySide_QtCoreTypes[SBK_QABSTRACTANIMATION_DELETIONPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractAnimation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTANIMATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAnimationGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QANIMATIONGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSequentialAnimationGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSEQUENTIALANIMATIONGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QParallelAnimationGroup >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPARALLELANIMATIONGROUP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVariantAnimation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QVARIANTANIMATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPropertyAnimation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPROPERTYANIMATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPauseAnimation >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPAUSEANIMATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractState >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTSTATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QState::ChildMode >() { return SbkPySide_QtCoreTypes[SBK_QSTATE_CHILDMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QState >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSTATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStateMachine::EventPriority >() { return SbkPySide_QtCoreTypes[SBK_QSTATEMACHINE_EVENTPRIORITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStateMachine::RestorePolicy >() { return SbkPySide_QtCoreTypes[SBK_QSTATEMACHINE_RESTOREPOLICY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStateMachine::Error >() { return SbkPySide_QtCoreTypes[SBK_QSTATEMACHINE_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QStateMachine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSTATEMACHINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStateMachine::WrappedEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSTATEMACHINE_WRAPPEDEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QStateMachine::SignalEvent >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSTATEMACHINE_SIGNALEVENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFinalState >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QFINALSTATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QHistoryState::HistoryType >() { return SbkPySide_QtCoreTypes[SBK_QHISTORYSTATE_HISTORYTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QHistoryState >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QHISTORYSTATE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractItemModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTITEMMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractListModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTLISTMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractTableModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTTABLEMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractTransition >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTTRANSITION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QEventTransition >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QEVENTTRANSITION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSignalTransition >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSIGNALTRANSITION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSocketNotifier::Type >() { return SbkPySide_QtCoreTypes[SBK_QSOCKETNOTIFIER_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSocketNotifier >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSOCKETNOTIFIER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QThread::Priority >() { return SbkPySide_QtCoreTypes[SBK_QTHREAD_PRIORITY_IDX]; }
template<> inline PyTypeObject* SbkType< ::QThread >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTHREAD_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTimer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTIMER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTimeLine::State >() { return SbkPySide_QtCoreTypes[SBK_QTIMELINE_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTimeLine::Direction >() { return SbkPySide_QtCoreTypes[SBK_QTIMELINE_DIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTimeLine::CurveShape >() { return SbkPySide_QtCoreTypes[SBK_QTIMELINE_CURVESHAPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTimeLine >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTIMELINE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QPluginLoader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPLUGINLOADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSignalMapper >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSIGNALMAPPER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFileSystemWatcher >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QFILESYSTEMWATCHER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMimeData >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMIMEDATA_IDX]); }
template<> inline PyTypeObject* SbkType< ::QEventLoop::ProcessEventsFlag >() { return SbkPySide_QtCoreTypes[SBK_QEVENTLOOP_PROCESSEVENTSFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QEventLoop::ProcessEventsFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QEVENTLOOP_PROCESSEVENTSFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QEventLoop >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QEVENTLOOP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QCoreApplication::Encoding >() { return SbkPySide_QtCoreTypes[SBK_QCOREAPPLICATION_ENCODING_IDX]; }
template<> inline PyTypeObject* SbkType< ::QCoreApplication >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QCOREAPPLICATION_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractEventDispatcher >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QABSTRACTEVENTDISPATCHER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QIODevice::OpenModeFlag >() { return SbkPySide_QtCoreTypes[SBK_QIODEVICE_OPENMODEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QIODevice::OpenModeFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QIODEVICE_OPENMODEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QIODevice >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QIODEVICE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QBuffer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QBUFFER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QFile::FileError >() { return SbkPySide_QtCoreTypes[SBK_QFILE_FILEERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFile::Permission >() { return SbkPySide_QtCoreTypes[SBK_QFILE_PERMISSION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QFile::Permission> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QFILE_PERMISSION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QFile::FileHandleFlag >() { return SbkPySide_QtCoreTypes[SBK_QFILE_FILEHANDLEFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QFile::FileHandleFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QFILE_FILEHANDLEFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QFile::MemoryMapFlags >() { return SbkPySide_QtCoreTypes[SBK_QFILE_MEMORYMAPFLAGS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFile >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QFILE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTemporaryFile >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEMPORARYFILE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QTextStream::RealNumberNotation >() { return SbkPySide_QtCoreTypes[SBK_QTEXTSTREAM_REALNUMBERNOTATION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextStream::FieldAlignment >() { return SbkPySide_QtCoreTypes[SBK_QTEXTSTREAM_FIELDALIGNMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextStream::Status >() { return SbkPySide_QtCoreTypes[SBK_QTEXTSTREAM_STATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextStream::NumberFlag >() { return SbkPySide_QtCoreTypes[SBK_QTEXTSTREAM_NUMBERFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QTextStream::NumberFlag> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QTEXTSTREAM_NUMBERFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QTextStream >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTEXTSTREAM_IDX]); }
template<> inline PyTypeObject* SbkType< ::QProcess::ProcessError >() { return SbkPySide_QtCoreTypes[SBK_QPROCESS_PROCESSERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QProcess::ProcessState >() { return SbkPySide_QtCoreTypes[SBK_QPROCESS_PROCESSSTATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QProcess::ProcessChannel >() { return SbkPySide_QtCoreTypes[SBK_QPROCESS_PROCESSCHANNEL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QProcess::ProcessChannelMode >() { return SbkPySide_QtCoreTypes[SBK_QPROCESS_PROCESSCHANNELMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QProcess::ExitStatus >() { return SbkPySide_QtCoreTypes[SBK_QPROCESS_EXITSTATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QProcess >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QPROCESS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QThreadPool >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QTHREADPOOL_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSettings::Status >() { return SbkPySide_QtCoreTypes[SBK_QSETTINGS_STATUS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSettings::Format >() { return SbkPySide_QtCoreTypes[SBK_QSETTINGS_FORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSettings::Scope >() { return SbkPySide_QtCoreTypes[SBK_QSETTINGS_SCOPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSettings >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSETTINGS_IDX]); }
template<> inline PyTypeObject* SbkType< ::QByteArray >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QBYTEARRAY_IDX]); }
template<> inline PyTypeObject* SbkType< ::QUrl::ParsingMode >() { return SbkPySide_QtCoreTypes[SBK_QURL_PARSINGMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QUrl::FormattingOption >() { return SbkPySide_QtCoreTypes[SBK_QURL_FORMATTINGOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QUrl::FormattingOption> >() { return SbkPySide_QtCoreTypes[SBK_QFLAGS_QURL_FORMATTINGOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QUrl >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QURL_IDX]); }
template<> inline PyTypeObject* SbkType< ::MSG >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_MSG_IDX]); }
template<> inline PyTypeObject* SbkType< ::POINT >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_POINT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGenericArgument >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QGENERICARGUMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMetaMethod::Access >() { return SbkPySide_QtCoreTypes[SBK_QMETAMETHOD_ACCESS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMetaMethod::MethodType >() { return SbkPySide_QtCoreTypes[SBK_QMETAMETHOD_METHODTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMetaMethod >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMETAMETHOD_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGenericReturnArgument >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QGENERICRETURNARGUMENT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QMetaObject::Call >() { return SbkPySide_QtCoreTypes[SBK_QMETAOBJECT_CALL_IDX]; }
template<> inline PyTypeObject* SbkType< ::QMetaObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QMETAOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QSysInfo::Sizes >() { return SbkPySide_QtCoreTypes[SBK_QSYSINFO_SIZES_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSysInfo::Endian >() { return SbkPySide_QtCoreTypes[SBK_QSYSINFO_ENDIAN_IDX]; }
template<> inline PyTypeObject* SbkType< ::QSysInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtCoreTypes[SBK_QSYSINFO_IDX]); }

} // namespace Shiboken

#endif // SBK_QTCORE_PYTHON_H

