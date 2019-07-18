rem CHANGE MAYA_ROOT variable to your maya installation
set MAYA_ROOT=c:\Program Files\Autodesk\Maya2019
set MAYA_SCRIPTS_FOLDER=c:\Users\ilunin\Documents\maya\2019\scripts

set PYFLOW_DESTINATION_FOLDER="%MAYA_SCRIPTS_FOLDER%\PyFlow"
set MAYA_BIN=%MAYA_ROOT%\bin
set MAYAPY=%MAYA_BIN%\mayapy.exe

rem remove pip installer if it exists
del get-pip.py

rem download get-pip.py
call powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

rem install pip to maya interpreter
%MAYAPY% get-pip.py --user

rem install requirements
cd ..\..\
"%MAYAPY%" -m pip install -r "%cd%\requirements\requirements-maya.txt" --user

rem cleanup
del integrations\maya\get-pip.py

rem copy pyflow to maya site packages
rmdir "%PYFLOW_DESTINATION_FOLDER%" /s /q
mkdir "%PYFLOW_DESTINATION_FOLDER%"
robocopy PyFlow "%PYFLOW_DESTINATION_FOLDER%" /s

pause
