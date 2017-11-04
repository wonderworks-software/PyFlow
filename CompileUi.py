import os
import pysideuic


CURRENT_DIR = os.path.dirname(__file__).replace('\\', '/') + '/'


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
            pysideuic.compileUi(ui_file, py_file)
            print('{0} converted to {1}.'.format(ui_file.upper(), py_file_name.upper()))
        except Exception as e:
            print('Error: compilation error.', e)


for d, dirs, files in os.walk(CURRENT_DIR):
    if "Python" in d or ".git" in d:
        continue
    for f in files:
        ext = f.split('.')[1]
        if ext == 'ui':
            uiFile = os.path.join(d, f)
            ui_to_py(uiFile)
