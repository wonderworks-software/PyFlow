## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import sys
from PyFlow.App import PyFlow
from qtpy.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    instance = PyFlow.instance(software="standalone")
    if instance is not None:
        instance.activateWindow()
        instance.show()

        try:
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
