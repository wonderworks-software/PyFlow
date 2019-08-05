Editor anatomy
==============

In the middle of the app there is a :class:`Canvas <PyFlow.UI.Canvas.Canvas.Canvas>`. This is where the fun happens.

.. image:: resources/canvas.png

Everything in editor except of canvas is a :class:`tool <PyFlow.UI.Tool.Tool.ToolBase>`. There are two types of tools

Shelf tool
**********
:class:`Shelf tools <PyFlow.UI.Tool.Tool.ShelfTool>` are located on the toolbar of editor main window.

.. image:: resources/shelf_tools.png


Dock tool
*********
:class:`Dock tools <PyFlow.UI.Tool.Tool.DockTool>` are floating widgets.

.. image:: resources/dock_tools.png

All registered dock tools can be found below corresponding section on menu bar.

.. image:: resources/dock_tools_menu.png


Subgraphs navigation
********************

On the top of canvas there is a :meth:`current location <PyFlow.Core.GraphBase.GraphBase.location>` widget. To step into subgraph - double click
on compound node. To step up - click on any parent button.

.. image:: resources/subgraph_navigation.gif

Exporter
********

Under `file->Custom IO` you can find all registered exporters and importers

.. image:: resources/exporter.png
