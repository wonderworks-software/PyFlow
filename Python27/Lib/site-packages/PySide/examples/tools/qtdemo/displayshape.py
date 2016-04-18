############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

from math import ceil
from PySide import QtCore, QtGui, QtNetwork, QtXml


class DisplayShape:
    def __init__(self, position, maxSize):
        self.metadata = {}
        self.image = QtGui.QImage()
        self.pos = position
        self.targetPos = QtCore.QPointF()
        self.maxSize = maxSize
        self.interactive = False

    def animate(self):
        if not self.targetPos.isNull():
            displacement = QtCore.QLineF(self.pos, self.targetPos)
            newPosition = displacement.pointAt(0.25)
            if displacement.length() <= 1.0:
                self.pos = self.targetPos
                self.targetPos = QtCore.QPointF()
            else:
                self.pos = newPosition

            return True

        return False

    def isInteractive(self):
        return self.interactive

    def paint(self, painter):
        painter.save()
        painter.drawImage(self.pos, self.image)
        painter.restore()

    def position(self):
        return self.pos

    def rect(self):
        return QtCore.QRectF(self.pos, self.image.size())

    def setInteractive(self, enable):
        self.interactive = enable

    def setPosition(self, position):
        self.pos = position

    def setSize(self, size):
        self.maxSize = size

    def setTarget(self, position):
        self.targetPos = position

    def size(self):
        return self.maxSize

    def target(self):
        return self.targetPos


class PanelShape(DisplayShape):
    def __init__(self, path, normal, highlighted, pen, position, maxSize):
        DisplayShape.__init__(self, position, maxSize)

        self.normalBrush = normal
        self.path = path
        self.highlightedBrush = highlighted
        self.pen = pen
        self.brush = QtGui.QBrush(self.normalBrush)

    def animate(self):
        updated = False

        if not "destroy" in self.metadata:
            if "fade" in self.metadata:
                penColor = self.pen.color()
                brushColor = self.brush.color()
                penAlpha = penColor.alpha()
                brushAlpha = brushColor.alpha()
                fadeMinimum = int(self.metadata.get("fade minimum", "0"))

                if penAlpha != fadeMinimum or brushAlpha != fadeMinimum or self.metadata["fade"] > 0:
                    penAlpha = max(fadeMinimum, min(penAlpha + self.metadata["fade"], 255))
                    brushAlpha = max(fadeMinimum, min(brushAlpha + self.metadata["fade"], 255))

                    penColor.setAlpha(penAlpha)
                    brushColor.setAlpha(brushAlpha)
                    self.pen.setColor(penColor)
                    self.brush.setColor(brushColor)

                    if penAlpha == 0 and brushAlpha == 0:
                        self.metadata["destroy"] = True
                        del self.metadata["fade"]
                    elif penAlpha == 255 and brushAlpha == 255:
                        del self.metadata["fade"]

                    updated = True
            elif "highlight" in self.metadata:
                scale = float(self.metadata.get("highlight scale", "0.0"))
                color = QtGui.QColor(self.brush.color())

                if self.metadata["highlight"]:
                    scale = max(0.0, min(scale + 0.5, 1.0))
                else:
                    scale = max(0.0, min(scale - 0.2, 1.0))

                if scale == 0.0:
                    self.brush = QtGui.QBrush(self.normalBrush)
                    del self.metadata["highlight"]

                    try:
                        del self.metadata["highlight scale"]
                    except KeyError:
                        pass

                    updated = True
                elif scale != float(self.metadata.get("highlight scale", "0.0")):
                    self.metadata["highlight scale"] = scale

                    if scale == 1.0:
                        self.brush = QtGui.QBrush(self.highlightedBrush)
                    else:
                        normal = self.normalBrush.color()
                        highlighted = self.highlightedBrush.color()

                        color.setRedF((1.0 - scale) * normal.redF() + scale * highlighted.redF())
                        color.setGreenF((1.0 - scale) * normal.greenF() + scale * highlighted.greenF())
                        color.setBlueF((1.0 - scale) * normal.blueF() + scale * highlighted.blueF())
                        self.brush.setColor(color)

                    updated = True

        return (DisplayShape.animate(self) or updated)

    def paint(self, painter):
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.translate(self.pos)
        painter.drawPath(self.path)
        painter.restore()

    def rect(self):
        return QtCore.QRectF(self.pos + self.path.boundingRect().topLeft(),
                             self.path.boundingRect().size())


class TitleShape(DisplayShape):
    def __init__(self, text, font, pen, position, maxSize, alignment=QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeft):
        DisplayShape.__init__(self, position, maxSize)

        self.font = QtGui.QFont(font)
        self.text = QtCore.QString(text)
        self.pen = pen
        self.alignment = alignment

        fm = QtGui.QFontMetricsF(self.font)
        self.textRect = fm.boundingRect(QtCore.QRectF(QtCore.QPointF(0, 0), maxSize), self.alignment, self.text)

        textWidth = max(fm.width(self.text), self.textRect.width())
        textHeight = max(fm.height(), self.textRect.height())

        scale = min(maxSize.width() / textWidth, maxSize.height() / textHeight)

        self.font.setPointSizeF(self.font.pointSizeF() * scale)
        fm = QtGui.QFontMetricsF(self.font)
        self.textRect = fm.boundingRect(QtCore.QRectF(QtCore.QPointF(0, 0), maxSize), self.alignment, self.text)
        self.baselineStart = QtCore.QPointF(self.textRect.left(), self.textRect.bottom() - fm.descent())

    def animate(self):
        updated = False

        if "destroy" not in self.metadata:
            if "fade" in self.metadata:
                penColor = self.pen.color()
                penAlpha = penColor.alpha()

                penAlpha = max(int(self.metadata.get("fade minimum", "0")), min(penAlpha + self.metadata["fade"], 255))

                penColor.setAlpha(penAlpha)
                self.pen.setColor(penColor)

                if penAlpha == 0:
                    self.metadata["destroy"] = True
                    del self.metadata["fade"]
                elif penAlpha == 255:
                    del self.metadata["fade"]

                updated = True

        return (DisplayShape.animate(self) or updated)

    def paint(self, painter):
        rect = QtCore.QRectF(self.textRect)
        rect.translate(self.pos)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.setPen(self.pen)
        painter.setFont(self.font)
        painter.drawText(self.pos + self.baselineStart, self.text)
        painter.restore()

    def rect(self):
        rect = QtCore.QRectF(self.textRect)
        return rect.translated(self.pos)


class ImageShape(DisplayShape):
    def __init__(self, original, position, maxSize, alpha=0, alignment=QtCore.Qt.AlignCenter):
        DisplayShape.__init__(self, position, maxSize)

        self.alpha = alpha
        self.alignment = alignment

        self.source = original.convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
        scale = min(min(self.maxSize.width() / self.source.width(), self.maxSize.height() / self.source.height()), 1.0)

        self.source = self.source.scaled(int(ceil(self.source.width() * scale)),
                                         int(ceil(self.source.height() * scale)),
                                         QtCore.Qt.KeepAspectRatio,
                                         QtCore.Qt.SmoothTransformation)

        self.image = QtGui.QImage(self.source.size(), QtGui.QImage.Format_ARGB32_Premultiplied)

        self.offset = QtCore.QPointF(0.0, 0.0)

        if self.alignment & QtCore.Qt.AlignHCenter:
            self.offset.setX((self.maxSize.width() - self.image.width()) / 2)
        elif self.alignment & QtCore.Qt.AlignRight:
            self.offset.setX(self.maxSize.width() - self.image.width())

        if alignment & QtCore.Qt.AlignVCenter:
            self.offset.setY((self.maxSize.height() - self.image.height()) / 2)
        elif self.alignment & QtCore.Qt.AlignBottom:
            self.offset.setY(self.maxSize.height() - self.image.height())

        self.redraw()

    def redraw(self):
        self.image.fill(QtGui.qRgba(self.alpha, self.alpha, self.alpha, self.alpha))

        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.drawImage(0, 0, self.source)
        painter.end()

    def paint(self, painter):
        painter.drawImage(self.pos + self.offset, self.image)

    def rect(self):
        return QtCore.QRectF(self.pos, self.maxSize)

    def animate(self):
        updated = False

        if "destroy" not in self.metadata:
            if "fade" in self.metadata:
                self.alpha = max(int(self.metadata.get("fade minimum", "0")), min(self.alpha + self.metadata["fade"], 255))
                self.redraw()

                if self.alpha == 0:
                    self.metadata["destroy"] = True
                    del self.metadata["fade"]
                elif self.alpha == 255:
                    del self.metadata["fade"]

                updated = True

        return (DisplayShape.animate(self) or updated)


class DocumentShape(DisplayShape):
    def __init__(self, text, font, position, maxSize, alpha=0):
        DisplayShape.__init__(self, position, maxSize)

        self.alpha = alpha
        self.textDocument = QtGui.QTextDocument()

        self.textDocument.setHtml(text)
        self.textDocument.setDefaultFont(font)
        self.textDocument.setPageSize(maxSize)
        documentSize = self.textDocument.documentLayout().documentSize()
        self.setSize(QtCore.QSizeF(self.maxSize.width(), min(self.maxSize.height(), documentSize.height())))

        self.source = QtGui.QImage(int(ceil(documentSize.width())),
                                   int(ceil(documentSize.height())),
                                   QtGui.QImage.Format_ARGB32_Premultiplied)
        self.source.fill(QtGui.qRgba(255, 255, 255, 255))

        context = QtGui.QAbstractTextDocumentLayout.PaintContext()
        self.textDocument.documentLayout().setPaintDevice(self.source)

        painter = QtGui.QPainter()
        painter.begin(self.source)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.textDocument.documentLayout().draw(painter, context)
        painter.end()

        self.source = self.source.scaled(int(ceil(self.maxSize.width())),
                                         int(ceil(self.maxSize.height())),
                                         QtCore.Qt.KeepAspectRatio,
                                         QtCore.Qt.SmoothTransformation)

        self.image = QtGui.QImage(self.source.size(), self.source.format())
        self.redraw()

    def animate(self):
        updated = False

        if "destroy" not in self.metadata:
            if "fade" in self.metadata:
                self.alpha = max(int(self.metadata.get("fade minimum", "0")), min(self.alpha + self.metadata["fade"], 255))
                self.redraw()

                if self.alpha == 0:
                    self.metadata["destroy"] = True
                    del self.metadata["fade"]
                elif self.alpha == 255:
                    del self.metadata["fade"]

                updated = True

        return (DisplayShape.animate(self) or updated)

    def redraw(self):
        self.image.fill(QtGui.qRgba(self.alpha, self.alpha, self.alpha, self.alpha))

        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.drawImage(0, 0, self.source)
        painter.end()

    def paint(self, painter):
        painter.drawImage(self.pos, self.image)

    def rect(self):
        return QtCore.QRectF(self.pos, self.maxSize)
