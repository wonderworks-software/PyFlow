#!/usr/bin/python

"""**************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the examples of the Qt Toolkit.
**
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
**     the names of its contributors may be used to endorse or promote
**     products derived from this software without specific prior written
**     permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
*****************************************************************************
** February 2011
** - stardelegate example ported to PySide by Arun Srinivasan 
**   <rulfzid@gmail.com>
**************************************************************************"""

from PySide.QtGui import (QItemDelegate, QStyledItemDelegate, QStyle)

from starrating import StarRating
from stareditor import StarEditor

class StarDelegate(QStyledItemDelegate):
    """ A subclass of QStyledItemDelegate that allows us to render our
        pretty star ratings.
    """

    def __init__(self, parent=None):
        super(StarDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        """ Paint the items in the table.
            
            If the item referred to by <index> is a StarRating, we handle the
            painting ourselves. For the other items, we let the base class
            handle the painting as usual.

            In a polished application, we'd use a better check than the 
            column number to find out if we needed to paint the stars, but
            it works for the purposes of this example.
        """
        if index.column() == 3:
            starRating = StarRating(index.data())
            
            # If the row is currently selected, we need to make sure we
            # paint the background accordingly.
            if option.state & QStyle.State_Selected:
                # The original C++ example used option.palette.foreground() to
                # get the brush for painting, but there are a couple of 
                # problems with that:
                #   - foreground() is obsolete now, use windowText() instead
                #   - more importantly, windowText() just returns a brush
                #     containing a flat color, where sometimes the style 
                #     would have a nice subtle gradient or something. 
                # Here we just use the brush of the painter object that's
                # passed in to us, which keeps the row highlighting nice
                # and consistent.
                painter.fillRect(option.rect, painter.brush())
            
            # Now that we've painted the background, call starRating.paint()
            # to paint the stars.
            starRating.paint(painter, option.rect, option.palette)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        """ Returns the size needed to display the item in a QSize object. """
        if index.column() == 3:
            starRating = StarRating(index.data())
            return starRating.sizeHint()
        else:
            return QStyledItemDelegate.sizeHint(self, option, index)

    # The next 4 methods handle the custom editing that we need to do.
    # If this were just a display delegate, paint() and sizeHint() would
    # be all we needed.

    def createEditor(self, parent, option, index):
        """ Creates and returns the custom StarEditor object we'll use to edit 
            the StarRating.
        """
        if index.column() == 3:
            editor = StarEditor(parent)
            editor.editingFinished.connect(self.commitAndCloseEditor)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """ Sets the data to be displayed and edited by our custom editor. """
        if index.column() == 3:
            editor.starRating = StarRating(index.data())
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """ Get the data from our custom editor and stuffs it into the model.
        """
        if index.column() == 3:
            model.setData(index, editor.starRating.starCount)
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def commitAndCloseEditor(self):
        """ Erm... commits the data and closes the editor. :) """
        editor = self.sender()

        # The commitData signal must be emitted when we've finished editing
        # and need to write our changed back to the model.
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)


if __name__ == "__main__":
    """ Run the application. """
    from PySide.QtGui import (QApplication, QTableWidget, QTableWidgetItem,
                              QAbstractItemView)
    import sys

    app = QApplication(sys.argv)

    # Create and populate the tableWidget
    tableWidget = QTableWidget(4, 4)
    tableWidget.setItemDelegate(StarDelegate())
    tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked | 
                                QAbstractItemView.SelectedClicked)
    tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
    tableWidget.setHorizontalHeaderLabels(["Title", "Genre", "Artist", "Rating"])

    data = [ ["Mass in B-Minor", "Baroque", "J.S. Bach", 5],
             ["Three More Foxes", "Jazz", "Maynard Ferguson", 4],
             ["Sex Bomb", "Pop", "Tom Jones", 3],
             ["Barbie Girl", "Pop", "Aqua", 5] ]

    for r in range(len(data)):
        tableWidget.setItem(r, 0, QTableWidgetItem(data[r][0]))
        tableWidget.setItem(r, 1, QTableWidgetItem(data[r][1]))
        tableWidget.setItem(r, 2, QTableWidgetItem(data[r][2]))
        item = QTableWidgetItem()
        item.setData(0, StarRating(data[r][3]).starCount)
        tableWidget.setItem(r, 3, item)

    tableWidget.resizeColumnsToContents()
    tableWidget.resize(500, 300)
    tableWidget.show()
    
    sys.exit(app.exec_())
                   