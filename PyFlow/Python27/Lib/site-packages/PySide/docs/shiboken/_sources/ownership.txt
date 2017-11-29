****************
Object ownership
****************

One of the main things a binding developer should have in mind is
how the C++ instances lives will cope with Python's reference count.
The last thing you want is to crash a program due to a segfault
when your C++ instance was deleted and the
wrapper object tries to access the invalid memory there.

In this section we'll show how |project| deals with object ownership
and parentship, taking advantage of the information provided by the
APIExtractor.

Ownership basics
================

As any python binding, |project|-based bindings uses reference counting
to handle the life of the wrapper object (the Python object that contains the
C++ object, do not confuse with the *wrapped* C++ object).
When a reference count reaches zero, the wrapper is deleted by Python garbage
collector and tries to delete the wrapped instance, but sometimes the wrapped
C++ object is already deleted, or maybe the C++ object should not be freed after
the Python wrapper go out of scope and die, because C++ is already taking care of
the wrapped instance.

In order to handle this, you should tell the
generator whether the instance's ownership belongs to the binding or
to the C++ Library. When belonging to the binding, we are sure that the C++ object
won't be deleted by C++ code and we can call the C++ destructor when the refcount
reaches 0. Otherwise, instances owned by C++ code can be destroyed arbitrarily,
without notifying the Python wrapper of its destruction.

Invalidating objects
====================

To prevent segfaults and double frees, the wrapper objects are invalidated.
An invalidated can't be passed as argument or have an attributte or method accessed.
Trying to do this will raise RuntimeError.

The following situations can invalidate an object:

C++ taking ownership
--------------------

    When an object is passed to a function or method that takes ownership of it, the wrapper
    is invalidated as we can't be sure of when the object is destroyed, unless it has a
    :ref:`virtual destructor <ownership-virt-method>` or the transfer is due to the special case
    of :ref:`parent ownership <ownership-parent>`.

    Besides being passed as argument, the callee object can have its ownership changed, like
    the `setParent` method in Qt's `QObject`.

Invalidate after use
--------------------

    Objects marked with *invalidate-after-use* in the type system description always are
    virtual method arguments provided by a C++ originated call. They should be
    invalidated right after the Python function returns.

.. _ownership-virt-method:

Objects with virtual methods
----------------------------

    A little bit of implementation details:
    virtual methods are supported by creating a C++ class, the **shell**, that inherits
    from the class with virtual methods, the native one, and override those methods to check if
    any derived class in Python also override it.

    If the class has a virtual destructor (and C++ classes with virtual methods should have), this
    C++ instance invalidates the wrapper only when the overriden destructor is called.

    One exception to this rule is when the object is created in C++, like in a
    factory method. This way the wrapped object is a C++ instance of the native
    class, not the shell one, and we cannot know when it is destroyed.

.. _ownership-parent:

Parent-child relationship
=========================

One special type of ownership is the parent-child relationship.
Being a child of an object means that when the object's parent dies,
the C++ instance also dies, so the Python references will be invalidated.
Qt's QObject system, for example, implements this behavior, but this is valid
for any C++ library with similar behavior.

.. _ownership-parent-heuristics:

Parentship heuristics
---------------------

    As the parent-child relationship is very common, |project| tries to automatically
    infer what methods falls into the parent-child scheme, adding the extra
    directives related to ownership.

    This heuristic will be triggered when generating code for a method and:

    * The function is a constructor.
    * The argument name is `parent`.
    * The argument type is a pointer to an object.

    When triggered, the heuristic will set the argument named "parent"
    as the parent of the object being created by the constructor.

    The main focus of this process was to remove a lot of hand written code from
    type system when binding Qt libraries. For Qt, this heuristic works in all cases,
    but be aware that it might not when binding your own libraries.

    To activate this heuristic, use the :ref:`--enable-parent-ctor-heuristic <parent-heuristic>`
    command line switch.

.. _return-value-heuristics:

Return value heuristics
-----------------------

    When enabled, object returned as pointer in C++ will become child of the object on which the method
    was called.

    To activate this heuristic, use the :ref:`--enable-return-value-heuristic <return-heuristic>`

Common pitfalls
===============

Not saving unowned objects references
-------------------------------------

    Sometimes when you pass an instance as argument to a method and the receiving
    instance will need that object to live indifinitely, but will not take ownership
    of the argument instance. In this case, you should hold a reference to the argument
    instance.

    For example, let's say that you have a renderer class that will use a source class
    in a setSource method but will not take ownership of it. The following code is wrong,
    because when `render` is called the `Source` object created during the call to `setSource`
    is already destroyed.

    .. code-block:: python

       renderer.setModel(Source())
       renderer.render()

    To solve this, you should hold a reference to the source object, like in

    .. code-block:: python

       source = Source()
       renderer.setSource(source)
       renderer.render()


