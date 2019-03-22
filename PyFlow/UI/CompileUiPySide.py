import os
import pyside2uic
import subprocess


CURRENT_DIR = os.path.join(os.path.dirname(__file__).replace('\\', '/') + '/',"Widgets")
INTERPRETER_PATH = 'python.exe'


def ui_to_py(ui_file):
    '''
    << ui_to_py(ui_file, py_file_name) >>
    convert *.ui to *.py to te same folder
    '''
    if not os.path.isfile(ui_file):
        msg = 'no such file'
        print(msg)
        return msg
    py_file_name = os.path.splitext(ui_file)[0] + '.py'
    with open(py_file_name, 'w') as py_file:
        try:
            pyside2uic.compileUi(ui_file, py_file)
            print('{0} converted to {1}.'.format(ui_file.upper(), py_file_name.upper()))
        except Exception as e:
            print('Error: compilation error.', e)

    bakFileName = py_file_name.replace("ui.py", "ui_backup.py")

    # convert to cross compatible code
    subprocess.call([INTERPRETER_PATH, '-m', 'Qt', '--convert', py_file_name])

    if(os.path.isfile(bakFileName)):
        os.remove(bakFileName)
        print("REMOVING", bakFileName)


def compile():
    for d, dirs, files in os.walk(CURRENT_DIR):
        if "Python" in d or ".git" in d:
            continue
        for f in files:
            if "." in f:
                ext = f.split('.')[1]
                if ext == 'ui':
                    uiFile = os.path.join(d, f)
                    ui_to_py(uiFile)


compile()
