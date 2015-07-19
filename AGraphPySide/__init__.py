import sys
import os
from PySide import QtCore
from PySide import QtGui
import Settings
import Port
import BaseNode
import Edge
import Widget
import IntNode

p = os.path.abspath('..')
if p not in sys.path:
    sys.path.append(p)
