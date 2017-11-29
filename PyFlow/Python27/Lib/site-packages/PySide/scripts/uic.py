#!/usr/bin/env python
# This file is part of the PySide project.
#
# Copyright (C) 2009-2011 Nokia Corporation and/or its subsidiary(-ies).
# Copyright (C) 2010 Riverbank Computing Limited.
# Copyright (C) 2009 Torsten Marek
#
# Contact: PySide team <pyside@openbossa.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

import sys
import optparse

from PySide import QtCore
from pysideuic.driver import Driver
from PySide import __version__ as PySideVersion
from pysideuic import __version__ as PySideUicVersion

Version = "PySide User Interface Compiler version %s, running on PySide %s." % (PySideUicVersion, PySideVersion)

def main():
    if sys.hexversion >= 0x03000000:
        from pysideuic.port_v3.invoke import invoke
    else:
        from pysideuic.port_v2.invoke import invoke

    parser = optparse.OptionParser(usage="pyside-uic [options] <ui-file>",
            version=Version)
    parser.add_option("-p", "--preview", dest="preview", action="store_true",
            default=False,
            help="show a preview of the UI instead of generating code")
    parser.add_option("-o", "--output", dest="output", default="-", metavar="FILE",
            help="write generated code to FILE instead of stdout")
    parser.add_option("-x", "--execute", dest="execute", action="store_true",
            default=False,
            help="generate extra code to test and display the class")
    parser.add_option("-d", "--debug", dest="debug", action="store_true",
            default=False, help="show debug output")
    parser.add_option("-i", "--indent", dest="indent", action="store", type="int",
            default=4, metavar="N",
            help="set indent width to N spaces, tab if N is 0 (default: 4)")

    g = optparse.OptionGroup(parser, title="Code generation options")
    g.add_option("--from-imports", dest="from_imports", action="store_true",
            default=False, help="generate imports relative to '.'")
    parser.add_option_group(g)

    opts, args = parser.parse_args()

    if len(args) != 1:
        sys.stderr.write("Error: one input ui-file must be specified\n")
        sys.exit(1)

    sys.exit(invoke(Driver(opts, args[0])))

if __name__ == "__main__":
     main()
