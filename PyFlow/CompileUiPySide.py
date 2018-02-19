import os
import pyside2uic
import subprocess


CURRENT_DIR = os.path.dirname(__file__).replace('\\', '/') + '/'
INTERPRETER_PATH = CURRENT_DIR + 'Python27/python.exe'


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

    # convert to cross compatible code
    subprocess.call([INTERPRETER_PATH, '-m', 'Qt', '--convert', py_file_name])



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
