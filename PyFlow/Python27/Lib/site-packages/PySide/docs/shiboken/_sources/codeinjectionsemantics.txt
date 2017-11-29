************************
Code Injection Semantics
************************

API Extractor provides the `inject-code
<http://www.pyside.org/docs/apiextractor/typesystem_manipulating_objects.html#inject-code>`_ tag
allowing the user to put custom written code to on specific locations of the generated code.
Yet this is only part of what is needed to generate proper binding code, where the custom code
should be written to depends upon the technology used on the generated binding code.

This is the ``inject-code`` tag options that matters to |project|.

    .. code-block:: xml

         <inject-code class="native | target" position="beginning | end">
             // custom code
         </inject-code>

Conventions
===========

**C++ Wrapper**
  This term refers to a generated C++ class that extends a class from the
  wrapped library. It is used only when a wrapped C++ class is polymorphic,
  i.e. it has or inherits any virtual methods.

**Python Wrapper**
  The code that exports the C++ wrapped class to Python. **Python wrapper**
  refers to all the code needed to export a C++ class to Python, and
  **Python method/function wrapper** means the specific function that calls
  the C++ method/function on behalf of Python.

**Native**
  This is a possible value for the ``class`` attribute of the ``inject-code``
  tag, it means things more akin to the C++ side.

**Target**
 Another ``class`` attribute value, it indicates things more close to the
 Python side.

inject-code tag
===============

The following table describes the semantics of ``inject-code`` tag as used on
|project|.

    +---------------+------+---------+--------------------------------------------------------------+
    |Parent Tag     |Class |Position |Meaning                                                       |
    +===============+======+=========+==============================================================+
    |value-type,    |native|beginning|Write to the beginning of a class wrapper ``.cpp`` file, right|
    |object-type    |      |         |after the ``#include`` clauses. A common use would be to write|
    |               |      |         |prototypes for custom functions whose definitions are put on a|
    |               |      |         |``native/end`` code injection.                                |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |Write to the end of a class wrapper ``.cpp`` file. Could be   |
    |               |      |         |used to write custom/helper functions definitions for         |
    |               |      |         |prototypes declared on ``native/beginning``.                  |
    |               +------+---------+--------------------------------------------------------------+
    |               |target|beginning|Put custom code on the beginning of the wrapper initializer   |
    |               |      |         |function (``init_CLASS(PyObject *module)``). This could be    |
    |               |      |         |used to manipulate the ``PyCLASS_Type`` structure before      |
    |               |      |         |registering it on Python.                                     |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |Write the given custom code at the end of the class wrapper   |
    |               |      |         |initializer function (``init_CLASS(PyObject *module)``). The  |
    |               |      |         |code here will be executed after all the wrapped class        |
    |               |      |         |components have been initialized.                             |
    +---------------+------+---------+--------------------------------------------------------------+
    |modify-function|native|beginning|Code here is put on the virtual method override of a C++      |
    |               |      |         |wrapper class (the one responsible for passing C++ calls to a |
    |               |      |         |Python override, if there is any), right after the C++        |
    |               |      |         |arguments have been converted but before the Python call.     |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |This code injection is put in a virtual method override on the|
    |               |      |         |C++ wrapper class, after the call to Python and before        |
    |               |      |         |dereferencing the Python method and tuple of arguments.       |
    |               +------+---------+--------------------------------------------------------------+
    |               |target|beginning|This code is injected on the Python method wrapper            |
    |               |      |         |(``PyCLASS_METHOD(...)``), right after the decisor have found |
    |               |      |         |which signature to call and also after the conversion of the  |
    |               |      |         |arguments to be used, but before the actual call.             |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |This code is injected on the Python method wrapper            |
    |               |      |         |(``PyCLASS_METHOD(...)``), right after the C++ method call,   |
    |               |      |         |but still inside the scope created by the overload for each   |
    |               |      |         |signature.                                                    |
    |               +------+---------+--------------------------------------------------------------+
    |               |shell |beginning|Used only for virtual functions. The code is injected when the|
    |               |      |         |function does not has a pyhton implementation, then the code  |
    |               |      |         |is inserted before c++ call                                   |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |Same as above, but the code is inserted after c++ call        |
    +---------------+------+---------+--------------------------------------------------------------+
    |typesystem     |native|beginning|Write code to the beginning of the module ``.cpp`` file, right|
    |               |      |         |after the ``#include`` clauses. This position has a similar   |
    |               |      |         |purpose as the ``native/beginning`` position on a wrapper     |
    |               |      |         |class ``.cpp`` file, namely write function prototypes, but not|
    |               |      |         |restricted to this use.                                       |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |Write code to the end of the module ``.cpp`` file. Usually    |
    |               |      |         |implementations for function prototypes inserted at the       |
    |               |      |         |beginning of the file with a ``native/beginning`` code        |
    |               |      |         |injection.                                                    |
    |               +------+---------+--------------------------------------------------------------+
    |               |target|beginning|Insert code at the start of the module initialization function|
    |               |      |         |(``initMODULENAME()``), before the calling ``Py_InitModule``. |
    |               |      +---------+--------------------------------------------------------------+
    |               |      |end      |Insert code at the end of the module initialization function  |
    |               |      |         |(``initMODULENAME()``), but before the checking that emits a  |
    |               |      |         |fatal error in case of problems importing the module.         |
    +---------------+------+---------+--------------------------------------------------------------+


Anatomy of Code Injection
=========================

To make things clear let's use a simplified example of generated wrapper code
and the places where each kind of code injection goes.

Below is the example C++ class for whom wrapper code will be generated.

    .. code-block:: c++

        class InjectCode {
        public:
            InjectCode();
            double overloadedMethod(int arg);
            double overloadedMethod(double arg);
            virtual int virtualMethod(int arg);
        };

From the C++ class, |project| will generate a ``injectcode_wrapper.cpp`` file
with the binding code. The next section will use a simplified version of the
generated wrapper code with the injection spots marked with comments.

Noteworthy Cases
----------------

The type system description system gives the binding developer a lot of
flexibility, which is power, which comes with responsibility. Some modifications
to the wrapped API will not be complete without some code injection.


Removing arguments and setting a default values for them
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A simple case is when a function have one argument removed, as when the C++
method ``METHOD(ARG)`` is modified to be used from Python as ``METHOD()``;
of course the binding developer must provide some guidelines to the generator
on what to do to call it. The most common solution is to remove the argument and
set a default value for it at the same time, so the original C++ method could be
called without problems.

Removing arguments and calling the method with your own hands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the argument is removed and no default value is provided, the generator will
not write any call to the method and expect the ``modify-function - target/beginning``
code injection to call the original C++ method on its own terms. If even this
custom code is not provided the generator will put an ``#error`` clause to
prevent compilation of erroneus binding code.

Calling the method with your own hands always!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your custom code to be injected contains a call to the wrapped C++ method,
it surely means that you don't want the generator to write another call to the
same method. As expected |project| will detect the user written call on the code
injection and will not write its own call, but for this to work properly the
binding developer must use the template variable ``%FUNCTION_NAME`` instead
of writing the actual name of the wrapped method/function.

In other words, use

    .. code-block:: xml

         <inject-code class="target" position="beginning | end">
             %CPPSELF.originalMethodName();
         </inject-code>


instead of


    .. code-block:: xml

         <inject-code class="target" position="beginning | end">
            %CPPSELF.%FUNCTION_NAME();
         </inject-code>


Code Injection for Functions/Methods
====================================


.. _codeinjecting_method_native:

On The Native Side
------------------

Notice that this is only used when there is a C++ wrapper, i.e. the wrapped
class is polymorphic.

    .. code-block:: c++

        int InjectCodeWrapper::virtualMethod(int arg)
        {
            PyObject* method = BindingManager::instance().getOverride(this, "virtualMethod");
            if (!py_override)
                return this->InjectCode::virtualMethod(arg);

            (... here C++ arguments are converted to Python ...)

            // INJECT-CODE: <modify-function><inject-code class="native" position="beginning">
            // Uses: pre method call custom code, modify the argument before the
            // Python call.

            (... Python method call goes in here ...)

            // INJECT-CODE: <modify-function><inject-code class="native" position="end">
            // Uses: post method call custom code, modify the result before delivering
            // it to C++ caller.

            (... Python method and argument tuple are dereferenced here ...)

            return Shiboken::Converter<int>::toCpp(method_result);
        }


On The Target Side
------------------

All the overloads of a method from C++ are gathered together on a single Python
method that uses an overload decisor to call the correct C++ method based on the
arguments passed by the Python call. Each overloaded method signature has its
own ``beginning`` and ``end`` code injections.

    .. code-block:: c++

            static PyObject*
            PyInjectCode_overloadedMethod(PyObject* self, PyObject* arg)
            {
                PyObject* py_result = 0;
                if (PyFloat_Check(arg)) {
                    double cpp_arg0 = Shiboken::Converter<double >::toCpp(arg);

                    // INJECT-CODE: <modify-function><inject-code class="target" position="beginning">
                    // Uses: pre method call custom code.

                    py_result = Shiboken::Converter<double >::toPython(
                        PyInjectCode_cptr(self)->InjectCode::overloadedMethod(cpp_arg0)
                    );

                    // INJECT-CODE: <modify-function><inject-code class="target" position="end">
                    // Uses: post method call custom code.

                } else if (PyNumber_Check(arg)) {
                    (... other overload calling code ...)
                } else goto PyInjectCode_overloadedMethod_TypeError;

                if (PyErr_Occurred() || !py_result)
                    return 0;

                return py_result;

                PyInjectCode_overloadedMethod_TypeError:
                    PyErr_SetString(PyExc_TypeError, "'overloadedMethod()' called with wrong parameters.");
                    return 0;
            }


.. _codeinjecting_classes:

Code Injection for Wrapped Classes
==================================

.. _codeinjecting_classes_native:

On The Native Side
------------------

Those injections go in the body of the ``CLASSNAME_wrapper.cpp`` file for the
wrapped class.

    .. code-block:: c++

        // Start of ``CLASSNAME_wrapper.cpp``
        #define protected public
        // default includes
        #include <shiboken.h>
        (...)
        #include "injectcode_wrapper.h"
        using namespace Shiboken;

        // INJECT-CODE: <value/object-type><inject-code class="native" position="beginning">
        // Uses: prototype declarations

        (... C++ wrapper virtual methods, if any ...)

        (... Python wrapper code ...)

        PyAPI_FUNC(void)
        init_injectcode(PyObject *module)
        {
            (...)
        }

        (...)

        // INJECT-CODE: <value/object-type><inject-code class="native" position="end">
        // Uses: definition of functions prototyped at ``native/beginning``.

        // End of ``CLASSNAME_wrapper.cpp``


.. _codeinjecting_classes_target:

On The Target Side
------------------

Code injections to the class Python initialization function.

    .. code-block:: c++

        // Start of ``CLASSNAME_wrapper.cpp``

        (...)

        PyAPI_FUNC(void)
        init_injectcode(PyObject *module)
        {
            // INJECT-CODE: <value/object-type><inject-code class="target" position="beginning">
            // Uses: Alter something in the PyInjectCode_Type (tp_flags value for example)
            // before registering it.

            if (PyType_Ready(&PyInjectCode_Type) < 0)
                return;

            Py_INCREF(&PyInjectCode_Type);
            PyModule_AddObject(module, "InjectCode",
                ((PyObject*)&PyInjectCode_Type));

            // INJECT-CODE: <value/object-type><inject-code class="target" position="end">
            // Uses: do something right after the class is registered, like set some static
            // variable injected on this same file elsewhere.
        }

        (...)

        // End of ``CLASSNAME_wrapper.cpp``

Code Injection for Modules
==========================

The C++ libraries are wapped as Python modules, a collection of classes,
functions, enums and namespaces. |project| creates wrapper files for all of
them and also one extra ``MODULENAME_module_wrapper.cpp`` to register the whole
module. Code injection xml tags who have the ``typesystem`` tag as parent will
be put on this file.

On The Native Side
------------------

This works exactly as the class wrapper code injections :ref:`codeinjecting_classes_native`.

On The Target Side
------------------

This is very similar to class wrapper code injections :ref:`codeinjecting_classes_target`.
Notice that the inject code at ``target/end`` is inserted before the check for errors
to prevent bad custom code to pass unnoticed.

    .. code-block:: c++

        // Start of ``MODULENAME_module_wrapper.cpp``

        (...)
        initMODULENAME()
        {
            // INJECT-CODE: <typesystem><inject-code class="target" position="beginning">
            // Uses: do something before the module is created.

            PyObject* module = Py_InitModule("MODULENAME", MODULENAME_methods);

            (... initialization of wrapped classes, namespaces, functions and enums ...)

            // INJECT-CODE: <typesystem><inject-code class="target" position="end">
            // Uses: do something after the module is registered and initialized.

            if (PyErr_Occurred())
                Py_FatalError("can't initialize module sample");
        }

        (...)

        // Start of ``MODULENAME_module_wrapper.cpp``

