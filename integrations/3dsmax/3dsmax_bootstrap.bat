@echo off

rem CHANGE MAX_ROOT variable to your 3ds max installation
set MAX_ROOT=c:\Program Files\Autodesk\3ds Max 2020
set MAXPY=%MAX_ROOT%\3dsmaxpy.exe

rem remove pip installer if it exists
del get-pip.py

rem download get-pip.py
powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"

rem install pip to maya interpreter
"%MAXPY%" get-pip.py --user

rem install requirements
cd ..\..\
"%MAXPY%" -m pip install -r "%cd%\requirements\requirements-3dsmax.txt" --user

rem cleanup
del integrations\3dsmax\get-pip.py

echo ""
echo "=============================================================="
echo "Requirements successfully installed"
echo "Add PyFlow parent folder to sys.path, and everything is ready!"
echo "=============================================================="
pause
