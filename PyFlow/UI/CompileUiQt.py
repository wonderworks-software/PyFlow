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


import os
import pyside2uic
import subprocess


CURRENT_DIR = os.path.dirname(__file__).replace("\\", "/") + "/"
INTERPRETER_PATH = "python.exe"


def ui_to_py(ui_file):
    if not os.path.isfile(ui_file):
        msg = "no such file"
        print(msg)
        return msg
    py_file_name = os.path.splitext(ui_file)[0] + ".py"
    with open(py_file_name, "w") as py_file:
        try:
            pyside2uic.compileUi(ui_file, py_file)
            print("{0} converted to {1}.".format(ui_file.upper(), py_file_name.upper()))
        except Exception as e:
            print("Error: compilation error.", e)

    bakFileName = py_file_name.replace(".py", "_backup.py")

    # convert to cross compatible code
    subprocess.call([INTERPRETER_PATH, "-m", "Qt", "--convert", py_file_name])

    if os.path.isfile(bakFileName):
        os.remove(bakFileName)
        print("REMOVING", bakFileName)


def compile():
    for d, dirs, files in os.walk(CURRENT_DIR):
        if "Python" in d or ".git" in d:
            continue
        for f in files:
            if "." in f:
                ext = f.split(".")[1]
                if ext == "ui":
                    uiFile = os.path.join(d, f)
                    ui_to_py(uiFile)


if __name__ == "__main__":
    compile()
