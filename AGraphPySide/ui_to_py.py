import pysideuic, os
from subprocess import call


rcc_py_path = os.path.dirname(__file__)+"/nodes_res_rc.py"


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
        # kill last line ( import nodes_res_rc )
        return True
    except:
        print 'Error: compilation error.'
    return False

def rcc_to_py(rcc_exe, py_path, qrc_path):
    if not os.path.isfile(rcc_exe):
        return False
    call([rcc_exe, "-o", py_path, qrc_path])
    print "{0} converted".format(py_path.upper())

ui_to_py(r"D:\GIT\nodes\GraphEditor_ui.ui")
# rcc_to_py(r"C:\Python27\Lib\site-packages\PySide\pyside-rcc.exe", rcc_py_path, r"D:\GIT\NodesRepo\resources\nodes_res.qrc")
