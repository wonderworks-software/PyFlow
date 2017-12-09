%cd%/Python27/python.exe -m cProfile -o program.prof "%cd%/Launcher.py"
%cd%/Python27/Scripts/snakeviz.exe program.prof
pause