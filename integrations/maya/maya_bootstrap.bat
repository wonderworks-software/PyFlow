@echo off

rem CHANGE MAYA_ROOT variable to your maya installation
set MAYA_ROOT=c:\Program Files\Autodesk\Maya2019

set MAYA_BIN=%MAYA_ROOT%\bin
set MAYAPY=%MAYA_BIN%\mayapy.exe

rem remove pip installer if it exists
del get-pip.py

rem download get-pip.py
powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

rem install pip to maya interpreter
"%MAYAPY%" get-pip.py --user

rem install requirements
cd ..\..\
"%MAYAPY%" -m pip install -r "%cd%\requirements\requirements-maya.txt" --user

rem cleanup
del integrations\maya\get-pip.py

echo "Requirements successfully installed"
echo "Add PyFlow parent folder to sys.path, and everything is ready!"
pause
