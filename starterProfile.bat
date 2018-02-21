%cd%/PyFlow/Python27/Scripts/python.exe -m cProfile -o program.prof "%cd%/launcher.py"
%cd%/PyFlow/Python27/Scripts/snakeviz.exe program.prof
pause