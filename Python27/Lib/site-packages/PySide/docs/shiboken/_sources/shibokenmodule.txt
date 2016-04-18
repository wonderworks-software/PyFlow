.. module:: shiboken

.. |maya| unicode:: Maya U+2122

Shiboken module
***************

Functions
^^^^^^^^^

.. container:: function_list

    *    def :meth:`isValid<shiboken.isValid>` (obj)
    *    def :meth:`wrapInstance<shiboken.wrapInstance>` (address, type)
    *    def :meth:`getCppPointer<shiboken.getCppPointer>` (obj)
    *    def :meth:`delete<shiboken.delete>` (obj)
    *    def :meth:`isOwnedByPython<shiboken.isOwnedByPython>` (obj)
    *    def :meth:`wasCreatedByPython<shiboken.wasCreatedByPython>` (obj)
    *    def :meth:`dump<shiboken.dump>` (obj)

Detailed description
^^^^^^^^^^^^^^^^^^^^

This Python module can be used to access internal information related to our
binding technology. Access to this internal information is required to e.g.:
integrate PySide with Qt based programs that offer Python scripting like |maya|
or just for debug purposes.

Some function description refer to "Shiboken based objects", wich means
Python objects instances of any Python Type created using Shiboken.


.. function:: isValid(obj)

    Given a Python object, returns True if the object methods can be called
    without an exception being thrown. A Python wrapper becomes invalid when
    the underlying C++ object is destroyed or unreachable.

.. function:: wrapInstance(address, type)

    Creates a Python wrapper for a C++ object instantiated at a given memory
    address - the returned object type will be the same given by the user.

    The type must be a Shiboken type, the C++ object will not be
    destroyed when the returned Python object reach zero references.

    If the address is invalid or doesn't point to a C++ object of given type
    the behavior is undefined.

.. function:: getCppPointer(obj)

    Returns a tuple of longs that contain the memory addresses of the
    C++ instances wrapped by the given object.

.. function:: delete(obj)

    Deletes the C++ object wrapped by the given Python object.

.. function:: isOwnedByPython(obj)

    Given a Python object, returns True if Python is responsible for deleting
    the underlying C++ object, False otherwise.

    If the object was not a Shiboken based object, a TypeError is
    thrown.

.. function:: wasCreatedByPython(obj)

    Returns true if the given Python object was created by Python.

.. function:: dump(obj)

    Returns a string with implementation-defined information about the
    object.
    This method should be used **only** for debug purposes by developers
    creating their own bindings as no guarantee is provided that
    the string format will be the same across different versions.

    If the object is not a Shiboken based object, a TypeError is thrown.
