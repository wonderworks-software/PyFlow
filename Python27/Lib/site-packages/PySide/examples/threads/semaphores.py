#!/usr/bin/env python

############################################################################
# 
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
# 
#  This file is part of the example classes of the Qt Toolkit.
# 
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
# 
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
# 
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
############################################################################

import sys
import random
from PySide import QtCore


DataSize = 100000
BufferSize = 8192
buffer = range(BufferSize)

freeBytes = QtCore.QSemaphore(BufferSize)
usedBytes = QtCore.QSemaphore()


class Producer(QtCore.QThread):
    def run(self):
        for i in range(DataSize):
            freeBytes.acquire()
            buffer[i % BufferSize] = "ACGT"[random.randint(0, 3)]
            usedBytes.release()


class Consumer(QtCore.QThread):
    def run(self):
        for i in range(DataSize):
            usedBytes.acquire()
            sys.stderr.write(buffer[i % BufferSize])
            freeBytes.release()

        sys.stderr.write("\n")


if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)
    producer = Producer()
    consumer = Consumer()
    producer.start()
    consumer.start()
    producer.wait()
    consumer.wait()
