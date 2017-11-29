rem PySide should be installed as well as python.exe should present in Path
python.exe %cd%/%~n0.py
pyside-rcc.exe -o %cd%/nodes_res_rc.py %cd%/nodes_res.qrc
pause