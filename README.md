# README #


![nodes.PNG](https://bitbucket.org/repo/Radzbd/images/1686754309-nodes.PNG)


### Description and features ###

* Node based multithreaded extendable editor. For this moment this is just a calc.
* UI implemented using PySide, and you can start the editor under any Qt application that uses **Python** as ascripting language.( **Autodesk Maya**, **MotionBuilder**, **Houdini** etc.)
* The logic and ui are separated.
* Custom extendable console based scripting language
* Own file format.

To extend functionality use console command 
```
#!bash

pluginWizard ~mode [implementNode|implementCommand] ~n name
```
the result will open code template with your *.py associated application. For examples, see existing nodes/commands source code.

To get existing command list use **help** command.

This is my learning project of Qt and applicatoin developement. Use this as you wish.

[Detailed description here (russian language)](http://ilgarlunin.blogspot.ru/2015/09/blog-post.html)

### Install and run ###

Download repo and double click **QtNodes.vbs** script. Or execute **Launcher.py** with python interpreter