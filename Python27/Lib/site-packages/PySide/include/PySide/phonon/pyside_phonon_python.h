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



#ifndef SBK_PHONON_PYTHON_H
#define SBK_PHONON_PYTHON_H

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
#include <phononnamespace.h>
#include <backendinterface.h>
#include <mediaobjectinterface.h>
#include <videowidget.h>
#include <audiooutput.h>
#include <effectparameter.h>
#include <path.h>
#include <abstractmediastream.h>
#include <mediacontroller.h>
#include <streaminterface.h>
#include "pyside_phonon.h"
#include <seekslider.h>
#include <effectinterface.h>
#include <objectdescriptionmodel.h>
#include <abstractvideooutput.h>
#include <objectdescription.h>
#include <mediaobject.h>
#include <abstractaudiooutput.h>
#include <volumeslider.h>
#include <platformplugin.h>
#include <volumefadereffect.h>
#include <mediasource.h>
#include <medianode.h>
#include <backendcapabilities.h>
#include <videoplayer.h>
#include <effectwidget.h>
#include <volumefaderinterface.h>
#include <addoninterface.h>
#include <videowidgetinterface.h>
#include <effect.h>
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
#define SBK_PHONON_IDX                                               0
#define SBK_PHONON_OBJECTDESCRIPTIONTYPE_IDX                         39
#define SBK_PHONON_DISCTYPE_IDX                                      22
#define SBK_PHONON_METADATA_IDX                                      38
#define SBK_PHONON_STATE_IDX                                         43
#define SBK_PHONON_CATEGORY_IDX                                      21
#define SBK_PHONON_ERRORTYPE_IDX                                     30
#define SBK_PHONON_BACKENDCAPABILITIES_IDX                           17
#define SBK_PHONON_EFFECTINTERFACE_IDX                               26
#define SBK_PHONON_MEDIAOBJECTINTERFACE_IDX                          35
#define SBK_PHONON_STREAMINTERFACE_IDX                               44
#define SBK_PHONON_VIDEOWIDGETINTERFACE_IDX                          51
#define SBK_PHONON_PLATFORMPLUGIN_IDX                                41
#define SBK_PHONON_ADDONINTERFACE_IDX                                4
#define SBK_PHONON_ADDONINTERFACE_INTERFACE_IDX                      8
#define SBK_PHONON_ADDONINTERFACE_NAVIGATIONCOMMAND_IDX              9
#define SBK_PHONON_ADDONINTERFACE_CHAPTERCOMMAND_IDX                 7
#define SBK_PHONON_ADDONINTERFACE_ANGLECOMMAND_IDX                   5
#define SBK_PHONON_ADDONINTERFACE_TITLECOMMAND_IDX                   11
#define SBK_PHONON_ADDONINTERFACE_SUBTITLECOMMAND_IDX                10
#define SBK_PHONON_ADDONINTERFACE_AUDIOCHANNELCOMMAND_IDX            6
#define SBK_PHONON_VOLUMEFADERINTERFACE_IDX                          54
#define SBK_PHONON_EFFECTPARAMETER_IDX                               27
#define SBK_PHONON_EFFECTPARAMETER_HINT_IDX                          28
#define SBK_QFLAGS_PHONON_EFFECTPARAMETER_HINT__IDX                  56
#define SBK_PHONON_MEDIASOURCE_IDX                                   36
#define SBK_PHONON_MEDIASOURCE_TYPE_IDX                              37
#define SBK_PHONON_BACKENDINTERFACE_IDX                              19
#define SBK_PHONON_BACKENDINTERFACE_CLASS_IDX                        20
#define SBK_PHONON_AUDIOCHANNELDESCRIPTION_IDX                       13
#define SBK_PHONON_OBJECTDESCRIPTION_PHONON_AUDIOCHANNELTYPE_IDX     13
#define SBK_PHONON_AUDIOOUTPUTDEVICE_IDX                             15
#define SBK_PHONON_OBJECTDESCRIPTION_PHONON_AUDIOOUTPUTDEVICETYPE_IDX 15
#define SBK_PHONON_AUDIOCAPTUREDEVICE_IDX                            12
#define SBK_PHONON_OBJECTDESCRIPTION_PHONON_AUDIOCAPTUREDEVICETYPE_IDX 12
#define SBK_PHONON_SUBTITLEDESCRIPTION_IDX                           45
#define SBK_PHONON_OBJECTDESCRIPTION_PHONON_SUBTITLETYPE_IDX         45
#define SBK_PHONON_EFFECTDESCRIPTION_IDX                             24
#define SBK_PHONON_OBJECTDESCRIPTION_PHONON_EFFECTTYPE_IDX           24
#define SBK_PHONON_MEDIANODE_IDX                                     33
#define SBK_PHONON_ABSTRACTVIDEOOUTPUT_IDX                           3
#define SBK_PHONON_PATH_IDX                                          40
#define SBK_PHONON_BACKENDCAPABILITIES_NOTIFIERWRAPPER_IDX           18
#define SBK_PHONON_MEDIAOBJECT_IDX                                   34
#define SBK_PHONON_EFFECTDESCRIPTIONMODEL_IDX                        25
#define SBK_PHONON_OBJECTDESCRIPTIONMODEL_PHONON_EFFECTTYPE_IDX      25
#define SBK_PHONON_AUDIOOUTPUTDEVICEMODEL_IDX                        16
#define SBK_PHONON_OBJECTDESCRIPTIONMODEL_PHONON_AUDIOOUTPUTDEVICETYPE_IDX 16
#define SBK_PHONON_ABSTRACTMEDIASTREAM_IDX                           2
#define SBK_PHONON_MEDIACONTROLLER_IDX                               31
#define SBK_PHONON_MEDIACONTROLLER_FEATURE_IDX                       32
#define SBK_QFLAGS_PHONON_MEDIACONTROLLER_FEATURE__IDX               57
#define SBK_PHONON_VOLUMESLIDER_IDX                                  55
#define SBK_PHONON_VIDEOPLAYER_IDX                                   47
#define SBK_PHONON_EFFECTWIDGET_IDX                                  29
#define SBK_PHONON_SEEKSLIDER_IDX                                    42
#define SBK_PHONON_VIDEOWIDGET_IDX                                   48
#define SBK_PHONON_VIDEOWIDGET_ASPECTRATIO_IDX                       49
#define SBK_PHONON_VIDEOWIDGET_SCALEMODE_IDX                         50
#define SBK_PHONON_EFFECT_IDX                                        23
#define SBK_PHONON_VOLUMEFADEREFFECT_IDX                             52
#define SBK_PHONON_VOLUMEFADEREFFECT_FADECURVE_IDX                   53
#define SBK_PHONON_ABSTRACTAUDIOOUTPUT_IDX                           1
#define SBK_PHONON_AUDIOOUTPUT_IDX                                   14
#define SBK_phonon_IDX_COUNT                                         58

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_phononTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_phononTypeConverters;

// Converter indices
#define SBK_PHONON_QLIST_PHONON_AUDIOCAPTUREDEVICE_IDX               0 // QList<Phonon::AudioCaptureDevice >
#define SBK_PHONON_QLIST_PHONON_EFFECTDESCRIPTION_IDX                1 // QList<Phonon::EffectDescription >
#define SBK_PHONON_QLIST_PHONON_AUDIOOUTPUTDEVICE_IDX                2 // QList<Phonon::AudioOutputDevice >
#define SBK_PHONON_QLIST_QOBJECTPTR_IDX                              3 // const QList<QObject * > &
#define SBK_PHONON_QLIST_QBYTEARRAY_IDX                              4 // QList<QByteArray >
#define SBK_PHONON_QLIST_QACTIONPTR_IDX                              5 // QList<QAction * >
#define SBK_PHONON_QLIST_PHONON_OBJECTDESCRIPTION_PHONON_EFFECTTYPE__IDX 6 // const QList<Phonon::ObjectDescription<Phonon::EffectType > > &
#define SBK_PHONON_QMAP_INT_QVARIANT_IDX                             7 // QMap<int, QVariant >
#define SBK_PHONON_QHASH_INT_QBYTEARRAY_IDX                          8 // const QHash<int, QByteArray > &
#define SBK_PHONON_QLIST_INT_IDX                                     9 // QList<int >
#define SBK_PHONON_QLIST_PHONON_OBJECTDESCRIPTION_PHONON_AUDIOOUTPUTDEVICETYPE__IDX 10 // const QList<Phonon::ObjectDescription<Phonon::AudioOutputDeviceType > > &
#define SBK_PHONON_QLIST_PHONON_EFFECTPARAMETER_IDX                  11 // QList<Phonon::EffectParameter >
#define SBK_PHONON_QPAIR_QBYTEARRAY_QSTRING_IDX                      12 // QPair<QByteArray, QString >
#define SBK_PHONON_QLIST_QPAIR_QBYTEARRAY_QSTRING_IDX                13 // QList<QPair<QByteArray, QString > >
#define SBK_PHONON_QHASH_QBYTEARRAY_QVARIANT_IDX                     14 // QHash<QByteArray, QVariant >
#define SBK_PHONON_QLIST_QVARIANT_IDX                                15 // const QList<QVariant > &
#define SBK_PHONON_QLIST_PHONON_AUDIOCHANNELDESCRIPTION_IDX          16 // QList<Phonon::AudioChannelDescription >
#define SBK_PHONON_QLIST_PHONON_SUBTITLEDESCRIPTION_IDX              17 // QList<Phonon::SubtitleDescription >
#define SBK_PHONON_QSET_QOBJECTPTR_IDX                               18 // QSet<QObject * >
#define SBK_PHONON_QLIST_PHONON_PATH_IDX                             19 // QList<Phonon::Path >
#define SBK_PHONON_QLIST_PHONON_MEDIASOURCE_IDX                      20 // const QList<Phonon::MediaSource > &
#define SBK_PHONON_QLIST_QURL_IDX                                    21 // const QList<QUrl > &
#define SBK_PHONON_QMULTIMAP_QSTRING_QSTRING_IDX                     22 // QMultiMap<QString, QString >
#define SBK_PHONON_QLIST_PHONON_EFFECTPTR_IDX                        23 // QList<Phonon::Effect * >
#define SBK_PHONON_QLIST_QSTRING_IDX                                 24 // QList<QString >
#define SBK_PHONON_QMAP_QSTRING_QVARIANT_IDX                         25 // QMap<QString, QVariant >
#define SBK_phonon_CONVERTERS_IDX_COUNT                              26

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::Phonon::ObjectDescriptionType >() { return SbkPySide_phononTypes[SBK_PHONON_OBJECTDESCRIPTIONTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::DiscType >() { return SbkPySide_phononTypes[SBK_PHONON_DISCTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::MetaData >() { return SbkPySide_phononTypes[SBK_PHONON_METADATA_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::State >() { return SbkPySide_phononTypes[SBK_PHONON_STATE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::Category >() { return SbkPySide_phononTypes[SBK_PHONON_CATEGORY_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::ErrorType >() { return SbkPySide_phononTypes[SBK_PHONON_ERRORTYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::EffectInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_EFFECTINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaObjectInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_MEDIAOBJECTINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::StreamInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_STREAMINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::VideoWidgetInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_VIDEOWIDGETINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::PlatformPlugin >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_PLATFORMPLUGIN_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::Interface >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_INTERFACE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::NavigationCommand >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_NAVIGATIONCOMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::ChapterCommand >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_CHAPTERCOMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::AngleCommand >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_ANGLECOMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::TitleCommand >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_TITLECOMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::SubtitleCommand >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_SUBTITLECOMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface::AudioChannelCommand >() { return SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_AUDIOCHANNELCOMMAND_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::AddonInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_ADDONINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::VolumeFaderInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_VOLUMEFADERINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::EffectParameter::Hint >() { return SbkPySide_phononTypes[SBK_PHONON_EFFECTPARAMETER_HINT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Phonon::EffectParameter::Hint> >() { return SbkPySide_phononTypes[SBK_QFLAGS_PHONON_EFFECTPARAMETER_HINT__IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::EffectParameter >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_EFFECTPARAMETER_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaSource::Type >() { return SbkPySide_phononTypes[SBK_PHONON_MEDIASOURCE_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaSource >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_MEDIASOURCE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::BackendInterface::Class >() { return SbkPySide_phononTypes[SBK_PHONON_BACKENDINTERFACE_CLASS_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::BackendInterface >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_BACKENDINTERFACE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AudioChannelDescription >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_AUDIOCHANNELDESCRIPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AudioOutputDevice >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_AUDIOOUTPUTDEVICE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AudioCaptureDevice >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_AUDIOCAPTUREDEVICE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::SubtitleDescription >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_SUBTITLEDESCRIPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::EffectDescription >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_EFFECTDESCRIPTION_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaNode >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_MEDIANODE_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AbstractVideoOutput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_ABSTRACTVIDEOOUTPUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::Path >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_PATH_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::BackendCapabilities::NotifierWrapper >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_BACKENDCAPABILITIES_NOTIFIERWRAPPER_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_MEDIAOBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::EffectDescriptionModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_EFFECTDESCRIPTIONMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AudioOutputDeviceModel >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_AUDIOOUTPUTDEVICEMODEL_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AbstractMediaStream >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_ABSTRACTMEDIASTREAM_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaController::Feature >() { return SbkPySide_phononTypes[SBK_PHONON_MEDIACONTROLLER_FEATURE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<Phonon::MediaController::Feature> >() { return SbkPySide_phononTypes[SBK_QFLAGS_PHONON_MEDIACONTROLLER_FEATURE__IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::MediaController >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_MEDIACONTROLLER_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::VolumeSlider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_VOLUMESLIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::VideoPlayer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_VIDEOPLAYER_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::EffectWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_EFFECTWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::SeekSlider >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_SEEKSLIDER_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::VideoWidget::AspectRatio >() { return SbkPySide_phononTypes[SBK_PHONON_VIDEOWIDGET_ASPECTRATIO_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::VideoWidget::ScaleMode >() { return SbkPySide_phononTypes[SBK_PHONON_VIDEOWIDGET_SCALEMODE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::VideoWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_VIDEOWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::Effect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_EFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::VolumeFaderEffect::FadeCurve >() { return SbkPySide_phononTypes[SBK_PHONON_VOLUMEFADEREFFECT_FADECURVE_IDX]; }
template<> inline PyTypeObject* SbkType< ::Phonon::VolumeFaderEffect >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_VOLUMEFADEREFFECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AbstractAudioOutput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_ABSTRACTAUDIOOUTPUT_IDX]); }
template<> inline PyTypeObject* SbkType< ::Phonon::AudioOutput >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_phononTypes[SBK_PHONON_AUDIOOUTPUT_IDX]); }

} // namespace Shiboken

#endif // SBK_PHONON_PYTHON_H

