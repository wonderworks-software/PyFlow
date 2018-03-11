python.exe -m cProfile -o program.prof "%cd%/launcher.py"
snakeviz.exe program.prof
pause