import pysideuic, os

def ui_to_py(ui_file):
    if not os.path.isfile(ui_file):
        msg = 'no such file'
        print msg
        return False
    py_file_name = os.path.splitext(ui_file)[0] + '.py'
    py_file = file(py_file_name, 'w')
    try:
        pysideuic.compileUi(ui_file, py_file)
        print '{0} converted to {1}.'.format(ui_file.upper(), py_file_name.upper())
        return True
    except:
        print 'Error: compilation error.'
    return False


ui_to_py(r"D:\GIT\NodesRepo\GraphEditor_ui.ui")
