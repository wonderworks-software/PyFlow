# Overview
<p align="center">
  <img src="PyFlow/UI/resources/PyFlow.jpg">
</p>

**PyFlow** is a general purpose runtime extendable python qt node editor.

Watch [video](https://youtu.be/chnRrr1Qfj8)

# Table of contents
- [Features](#features)
- [Installation](#installation)
- [Pip dependencies](#dependencies)
- [Usage](#usage)
- [Licensing](#licensing)

# Features
- Json serializable
- Easy node creation from annotated functions
- Categories tree
- Undo stack
- Properties view
- Dirty propagation for optimal graph computation
- Runtime nodes creation
- Variables

# Installation
1. Download repository.
2. Install [conda](https://conda.io/miniconda.html) with pyside2 and python 2.7 environment. [Instruction](https://fredrikaverpil.github.io/2017/08/28/pyside2-easy-install/) here
3. Go to **PyFlow/** folder and install dependencies
	```bash
	pip install -r requirements.txt
	```
4. Execute **starter.bat**


# Dependencies
- [Qt.py](https://github.com/mottosso/Qt.py)
- PySide or PySide2 or PyQt5 or PyQt4
- [pyrr](https://github.com/adamlwgriffiths/Pyrr) for builtin math. (optional)

# Usage
App's entry point is **App.py** file under PyFlow folder. There are also several handy bat scripts for debugging and profiling.
Right click on empty space to show node box then drag and drop on to canvas. Or press enter with node name selected.
Connect and execute pins from property view or using timer node.

# Extending
See source code. **FunctionLibraries** folder for annotated nodes, **Nodes** folder for
class based nodes. **Pins**, for data types and **Commands** for editor commands.

# Discussion
[Discord channel](https://discord.gg/SwmkqMj)

# Donate
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/ILunin)
