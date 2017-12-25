rem PySide should be installed as well as python.exe should present in Path
%cd%/Python27/Scripts/python.exe %cd%/%~n0.py
%cd%/Python27/Lib/site-packages/PySide/pyside-rcc.exe -o %cd%/nodes_res_rc.py %cd%/nodes_res.qrc

pause