# Overview

![](logoBp.png)

[PyFlow](@ref PyFlow.PyFlow.PyFlow) is a general purpose extendable python qt node editor.

# Table of contents
- [Features](#features)
- [Installation](#installation)
- [Pip dependencies](#dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [Credits](#credits)

# Features
- Json serializable
- Easy node creation from annotated functions
- Categories tree
- Undo stack
- Properties view
- Dirty propagation for optimal graph computation
- Runtime nodes creation
- Variables and variables view

# Installation
This repository is a self contained app with python virtualenv configured. So treat it as standalone version.

# Pip dependencies:
- [Qt.py](https://github.com/mottosso/Qt.py)
- PySide or PySide2 or PyQt5
- [pyrr](https://github.com/adamlwgriffiths/Pyrr) for builtin math. (optional)

# Usage
App's entry point is a **PyFlow.py** file. There are also several handy bat scripts for debugging and profiling.
Right click on empty space to show node box then drag and drop on to canvas. Or press enter with node name selected.
Connect pins and execute the graph with [Call](@ref PyFlow.Nodes.call.call) node.

Writing this project i was inspired by Unreal Engine blueprints. So, if you are familiar with it, you will quickly figure out what's what.

For in depth descriptin and how it works, see video tutorials and documentation.
