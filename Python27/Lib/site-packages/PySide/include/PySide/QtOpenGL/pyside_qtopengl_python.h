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



#ifndef SBK_QTOPENGL_PYTHON_H
#define SBK_QTOPENGL_PYTHON_H

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
#include <qglshaderprogram.h>
#include <qgl.h>
#include <qglcolormap.h>
#include <qglframebufferobject.h>
#include <qglpixelbuffer.h>
#include <qglbuffer.h>
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
#define SBK_QGL_IDX                                                  4
#define SBK_QGL_FORMATOPTION_IDX                                     5
#define SBK_QFLAGS_QGL_FORMATOPTION__IDX                             0
#define SBK_QGLFRAMEBUFFEROBJECTFORMAT_IDX                           18
#define SBK_QGLCOLORMAP_IDX                                          10
#define SBK_QGLFORMAT_IDX                                            13
#define SBK_QGLFORMAT_OPENGLCONTEXTPROFILE_IDX                       14
#define SBK_QGLFORMAT_OPENGLVERSIONFLAG_IDX                          15
#define SBK_QFLAGS_QGLFORMAT_OPENGLVERSIONFLAG__IDX                  2
#define SBK_QGLBUFFER_IDX                                            6
#define SBK_QGLBUFFER_TYPE_IDX                                       8
#define SBK_QGLBUFFER_USAGEPATTERN_IDX                               9
#define SBK_QGLBUFFER_ACCESS_IDX                                     7
#define SBK_QGLCONTEXT_IDX                                           11
#define SBK_QGLCONTEXT_BINDOPTION_IDX                                12
#define SBK_QFLAGS_QGLCONTEXT_BINDOPTION__IDX                        1
#define SBK_QGLPIXELBUFFER_IDX                                       19
#define SBK_QGLFRAMEBUFFEROBJECT_IDX                                 16
#define SBK_QGLFRAMEBUFFEROBJECT_ATTACHMENT_IDX                      17
#define SBK_QGLWIDGET_IDX                                            23
#define SBK_QGLSHADER_IDX                                            20
#define SBK_QGLSHADER_SHADERTYPEBIT_IDX                              21
#define SBK_QFLAGS_QGLSHADER_SHADERTYPEBIT__IDX                      3
#define SBK_QGLSHADERPROGRAM_IDX                                     22
#define SBK_QtOpenGL_IDX_COUNT                                       24

// This variable stores all Python types exported by this module.
extern PyTypeObject** SbkPySide_QtOpenGLTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter** SbkPySide_QtOpenGLTypeConverters;

// Converter indices
#define SBK_QTOPENGL_QLIST_QACTIONPTR_IDX                            0 // QList<QAction * >
#define SBK_QTOPENGL_QLIST_QOBJECTPTR_IDX                            1 // const QList<QObject * > &
#define SBK_QTOPENGL_QLIST_QBYTEARRAY_IDX                            2 // QList<QByteArray >
#define SBK_QTOPENGL_QLIST_QGLSHADERPTR_IDX                          3 // QList<QGLShader * >
#define SBK_QTOPENGL_QLIST_QVARIANT_IDX                              4 // QList<QVariant >
#define SBK_QTOPENGL_QLIST_QSTRING_IDX                               5 // QList<QString >
#define SBK_QTOPENGL_QMAP_QSTRING_QVARIANT_IDX                       6 // QMap<QString, QVariant >
#define SBK_QtOpenGL_CONVERTERS_IDX_COUNT                            7

// Macros for type check

namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject* SbkType< ::QGL::FormatOption >() { return SbkPySide_QtOpenGLTypes[SBK_QGL_FORMATOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGL::FormatOption> >() { return SbkPySide_QtOpenGLTypes[SBK_QFLAGS_QGL_FORMATOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLFramebufferObjectFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLFRAMEBUFFEROBJECTFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLColormap >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLCOLORMAP_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLFormat::OpenGLContextProfile >() { return SbkPySide_QtOpenGLTypes[SBK_QGLFORMAT_OPENGLCONTEXTPROFILE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLFormat::OpenGLVersionFlag >() { return SbkPySide_QtOpenGLTypes[SBK_QGLFORMAT_OPENGLVERSIONFLAG_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGLFormat::OpenGLVersionFlag> >() { return SbkPySide_QtOpenGLTypes[SBK_QFLAGS_QGLFORMAT_OPENGLVERSIONFLAG__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLFormat >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLFORMAT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLBuffer::Type >() { return SbkPySide_QtOpenGLTypes[SBK_QGLBUFFER_TYPE_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLBuffer::UsagePattern >() { return SbkPySide_QtOpenGLTypes[SBK_QGLBUFFER_USAGEPATTERN_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLBuffer::Access >() { return SbkPySide_QtOpenGLTypes[SBK_QGLBUFFER_ACCESS_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLBuffer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLBUFFER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLContext::BindOption >() { return SbkPySide_QtOpenGLTypes[SBK_QGLCONTEXT_BINDOPTION_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGLContext::BindOption> >() { return SbkPySide_QtOpenGLTypes[SBK_QFLAGS_QGLCONTEXT_BINDOPTION__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLContext >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLCONTEXT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLPixelBuffer >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLPIXELBUFFER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLFramebufferObject::Attachment >() { return SbkPySide_QtOpenGLTypes[SBK_QGLFRAMEBUFFEROBJECT_ATTACHMENT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLFramebufferObject >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLFRAMEBUFFEROBJECT_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLWidget >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLWIDGET_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLShader::ShaderTypeBit >() { return SbkPySide_QtOpenGLTypes[SBK_QGLSHADER_SHADERTYPEBIT_IDX]; }
template<> inline PyTypeObject* SbkType< ::QFlags<QGLShader::ShaderTypeBit> >() { return SbkPySide_QtOpenGLTypes[SBK_QFLAGS_QGLSHADER_SHADERTYPEBIT__IDX]; }
template<> inline PyTypeObject* SbkType< ::QGLShader >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLSHADER_IDX]); }
template<> inline PyTypeObject* SbkType< ::QGLShaderProgram >() { return reinterpret_cast<PyTypeObject*>(SbkPySide_QtOpenGLTypes[SBK_QGLSHADERPROGRAM_IDX]); }

} // namespace Shiboken

#endif // SBK_QTOPENGL_PYTHON_H

