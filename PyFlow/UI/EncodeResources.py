# Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import subprocess
from qtpy import __binding__

binding = __import__(__binding__)
path = os.path.dirname(binding.__file__)

if __binding__ == "PySide2":
    app = 'pyside2-rcc.exe'
elif __binding__ == "PySide":
    app = 'pyside-rcc.exe'
elif __binding__ == "PyQt4":
    app = 'pyrcc4.exe'
elif __binding__ == "PyQt5":
    app = 'pyrcc5.exe'


def main():
    print('Encoding : Resources')
    filepath = os.path.abspath("./resources")
    resourceFile = 'Resources.qrc'

    with open(resourceFile, 'w') as outf:
        outf.write('<RCC>\n  <qresource>\n')
        for root, dirs, files in os.walk("resources"):
            for file in files:
                if '.qrc' not in file:
                    dirname = os.path.relpath(os.path.join(root, file))
                    print(dirname)
                    write = '     <file alias="%s">%s</file>\n' % (
                        file, dirname)
                    outf.write(write)
        outf.write("  </qresource>\n</RCC>")
    outf.close()
    args = [os.path.join(path, app), "-compress", "2", "-threshold", "3", '-o',
            os.path.join(os.path.dirname(filepath), r'resources.py'), resourceFile]
    p = subprocess.Popen(
        args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(out)
    print(err)
    # import resources
    print('Compiled : Resources')


if __name__ == "__main__":
    main()
