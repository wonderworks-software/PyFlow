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



#ifndef SBK_QTMULTIMEDIA_PYTHON_H
#define SBK_QTMULTIMEDIA_PYTHON_H

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
#include <qabstractvideobuffer.h>
#include <qaudioengine.h>
#include <qaudioinput.h>
#include <qaudioengineplugin.h>
#include <qaudiodeviceinfo.h>
#include <qaudio.h>
#include <qaudiooutput.h>
#include <qvideoframe.h>
#include <qabstractvideosurface.h>
#include <qvideosurfaceformat.h>
#include <qaudioformat.h>
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
#define SBK_QAUDIO_IDX                                               8
#define SBK_QAUDIO_ERROR_IDX                                         9
#define SBK_QAUDIO_STATE_IDX                                         11
#define SBK_QAUDIO_MODE_IDX                                          10
#define SBK_QAUDIOFORMAT_IDX                                         15
#define SBK_QAUDIOFORMAT_SAMPLETYPE_IDX                              17
#define SBK_QAUDIOFORMAT_ENDIAN_IDX                                  16
#define SBK_QAUDIODEVICEINFO_IDX                                     12
#define SBK_QABSTRACTVIDEOBUFFER_IDX                                 3
#define SBK_QABSTRACTVIDEOBUFFER_HANDLETYPE_IDX                      4
#define SBK_QABSTRACTVIDEOBUFFER_MAPMODE_IDX                         5
#define SBK_QVIDEOSURFACEFORMAT_IDX                                  23
#define SBK_QVIDEOSURFACEFORMAT_DIRECTION_IDX                        24
#define SBK_QVIDEOSURFACEFORMAT_YCBCRCOLORSPACE_IDX                  25
#define SBK_QVIDEOFRAME_IDX                                          20
#define SBK_QVIDEOFRAME_FIELDTYPE_IDX                                21
#define SBK_QVIDEOFRAME_PIXELFORMAT_IDX                              22
#define SBK_QAUDIOENGINEFACTORYINTERFACE_IDX                         13
#define SBK_QABSTRACTAUDIODEVICEINFO_IDX                             0
#define SBK_QABSTRACTAUDIOINPUT_IDX                                  1
#define SBK_QABSTRACTVIDEOSURFACE_IDX                                6
#define SBK_QABSTRACTVIDEOSURFACE_ERROR_IDX                          7
#define SBK_QAUDIOENGINEPLUGIN_IDX                                   14
#define SBK_QAUDIOOUTPUT_IDX                                         19
#define SBK_QAUDIOINPUT_IDX                                          18
#define SBK_QABSTRACTAUDIOOUTPUT_IDX                                 2
#define SBK_QtMultimedia_IDX_COUNT                                   26

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtMultimediaTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtMultimediaTypeConverters;

// Converter indices
#define SBK_QTMULTIMEDIA_QLIST_QAUDIODEVICEINFO_IDX                  0 // QList<QAudioDeviceInfo >
#define SBK_QTMULTIMEDIA_QLIST_QAUDIOFORMAT_ENDIAN_IDX               1 // QList<QAudioFormat::Endian >
#define SBK_QTMULTIMEDIA_QLIST_INT_IDX                               2 // QList<int >
#define SBK_QTMULTIMEDIA_QLIST_QAUDIOFORMAT_SAMPLETYPE_IDX           3 // QList<QAudioFormat::SampleType >
#define SBK_QTMULTIMEDIA_QLIST_QBYTEARRAY_IDX                        4 // QList<QByteArray >
#define SBK_QTMULTIMEDIA_QLIST_QOBJECTPTR_IDX                        5 // const QList<QObject * > &
#define SBK_QTMULTIMEDIA_QLIST_QVIDEOFRAME_PIXELFORMAT_IDX           6 // QList<QVideoFrame::PixelFormat >
#define SBK_QTMULTIMEDIA_QLIST_QVARIANT_IDX                          7 // QList<QVariant >
#define SBK_QTMULTIMEDIA_QLIST_QSTRING_IDX                           8 // QList<QString >
#define SBK_QTMULTIMEDIA_QMAP_QSTRING_QVARIANT_IDX                   9 // QMap<QString, QVariant >
#define SBK_QtMultimedia_CONVERTERS_IDX_COUNT                        10

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QAudio::Error >() { return SbkPySide_QtMultimediaTypes[SBK_QAUDIO_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAudio::State >() { return SbkPySide_QtMultimediaTypes[SBK_QAUDIO_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAudio::Mode >() { return SbkPySide_QtMultimediaTypes[SBK_QAUDIO_MODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAudioFormat::SampleType >() { return SbkPySide_QtMultimediaTypes[SBK_QAUDIOFORMAT_SAMPLETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAudioFormat::Endian >() { return SbkPySide_QtMultimediaTypes[SBK_QAUDIOFORMAT_ENDIAN_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAudioFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QAUDIOFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAudioDeviceInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QAUDIODEVICEINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractVideoBuffer::HandleType >() { return SbkPySide_QtMultimediaTypes[SBK_QABSTRACTVIDEOBUFFER_HANDLETYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractVideoBuffer::MapMode >() { return SbkPySide_QtMultimediaTypes[SBK_QABSTRACTVIDEOBUFFER_MAPMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractVideoBuffer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QABSTRACTVIDEOBUFFER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVideoSurfaceFormat::Direction >() { return SbkPySide_QtMultimediaTypes[SBK_QVIDEOSURFACEFORMAT_DIRECTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QVideoSurfaceFormat::YCbCrColorSpace >() { return SbkPySide_QtMultimediaTypes[SBK_QVIDEOSURFACEFORMAT_YCBCRCOLORSPACE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QVideoSurfaceFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QVIDEOSURFACEFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QVideoFrame::FieldType >() { return SbkPySide_QtMultimediaTypes[SBK_QVIDEOFRAME_FIELDTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QVideoFrame::PixelFormat >() { return SbkPySide_QtMultimediaTypes[SBK_QVIDEOFRAME_PIXELFORMAT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QVideoFrame >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QVIDEOFRAME_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAudioEngineFactoryInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QAUDIOENGINEFACTORYINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractAudioDeviceInfo >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QABSTRACTAUDIODEVICEINFO_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractAudioInput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QABSTRACTAUDIOINPUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractVideoSurface::Error >() { return SbkPySide_QtMultimediaTypes[SBK_QABSTRACTVIDEOSURFACE_ERROR_IDX]; }
template<> inline PyTypeObject* SbkType< ::QAbstractVideoSurface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QABSTRACTVIDEOSURFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAudioEnginePlugin >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QAUDIOENGINEPLUGIN_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAudioOutput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QAUDIOOUTPUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAudioInput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QAUDIOINPUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QAbstractAudioOutput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtMultimediaTypes[SBK_QABSTRACTAUDIOOUTPUT_IDX]); }

} // namespace Shiboken

#endif // SBK_QTMULTIMEDIA_PYTHON_H

