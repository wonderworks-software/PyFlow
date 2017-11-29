.. _words-of-advice:

***************
Words of Advice
***************

When writing or using Python bindings there is some things you must keep in mind.


.. _duck-punching-and-virtual-methods:

Duck punching and virtual methods
=================================

The combination of duck punching, the practice of altering class characteristics
of already instantiated objects, and virtual methods of wrapped C++ classes, can
be tricky. That was an optimistic statement.

Let's see duck punching in action for educational purposes.

    .. code-block:: python

       import types
       import Binding

       obj = Binding.CppClass()

       # CppClass has a virtual method called 'virtualMethod',
       # but we don't like it anymore.
       def myVirtualMethod(self_obj, arg):
           pass

       obj.virtualMethod = types.MethodType(myVirtualMethod, obj, Binding.CppClass)


If some C++ code happens to call `CppClass::virtualMethod(...)` on the C++ object
held by "obj" Python object, the new duck punched "virtualMethod" method will be
properly called. That happens because the underlying C++ object is in fact an instance
of a generated C++ class that inherits from `CppClass`, let's call it `CppClassWrapper`,
responsible for receiving the C++ virtual method calls and finding out the proper Python
override to which handle such a call.

Now that you know this, consider the case when C++ has a factory method that gives you
new C++ objects originated somewhere in C++-land, in opposition to the ones generated in
Python-land by the usage of class constructors, like in the example above.

Brief interruption to show what I was saying:

    .. code-block:: python

       import types
       import Binding

       obj = Binding.createCppClass()
       def myVirtualMethod(self_obj, arg):
           pass

       # Punching a dead duck...
       obj.virtualMethod = types.MethodType(myVirtualMethod, obj, Binding.CppClass)


The `Binding.createCppClass()` factory method is just an example, C++ created objects
can pop out for a number of other reasons. Objects created this way have a Python wrapper
holding them as usual, but the object held is not a `CppClassWrapper`, but a regular
`CppClass`. All virtual method calls originated in C++ will stay in C++ and never reach
a Python virtual method overridden via duck punching.

Although duck punching is an interesting Python feature, it don't mix well with wrapped
C++ virtual methods, specially when you can't tell the origin of every single wrapped
C++ object. In summary: don't do it!


.. _pyside-old-style-class:

Python old style classes and PySide
===================================

Because of some architectural decisions and deprecated Python types. Since PySide 1.1 old style classes are not supported with multiple inheritance.

Below you can check the examples:

Example with old style class:

    .. code-block:: python

        from PySide import QtCore

        class MyOldStyleObject:
            pass

        class MyObject(QtCore, MyOldStyleObject):
            pass


this example will raise a 'TypeError' due to the limitation on PySide, to fix this you will need use the new style class:


    .. code-block:: python

        from PySide import QtCore

        class MyOldStyleObject(object):
            pass

        class MyObject(QtCore, MyOldStyleObject):
            pass


All classes used for multiple inheritance with other PySide types need to have 'object' as base class.
