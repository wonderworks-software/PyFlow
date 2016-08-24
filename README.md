# Qt node editor #

![nodes.PNG](https://bitbucket.org/repo/Radzbd/images/1686754309-nodes.PNG)


[Watch video](https://www.youtube.com/watch?v=HEP5E84O0mo)


### Description and features ###

* Node based multithreaded extendable editor. For this moment this is just a calc.
* UI implemented using PySide, and you can start the editor under any Qt application that uses **Python** as ascripting language.( **Autodesk Maya**, **MotionBuilder**, **Houdini** etc.)
* The logic and ui are separated.
* Custom extendable cmd like scripting language
* Own file format.

To extend functionality use console command 
```
#!bash

pluginWizard ~mode [implementNode|implementCommand] ~n name
```
as a result code template  with your *.py associated application will be opened. For examples, see existing nodes/commands source code. No extra work, new nodes/commands will be hooked up with restart automatically.

To get existing command list use **help** command. Call command with no parameters to get description.

This is my learning project of Qt and applicatoin developement. Use this as you wish.

[Detailed description here (russian language)](http://ilgarlunin.blogspot.ru/2015/09/blog-post.html)

### Install and run ###

Download repo and double click **QtNodes.vbs** script. Or execute **Launcher.py** with python interpreter