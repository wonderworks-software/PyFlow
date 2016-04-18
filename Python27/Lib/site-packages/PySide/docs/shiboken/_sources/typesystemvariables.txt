*********************
Type System Variables
*********************

User written code can be placed in arbitrary places using the
:doc:`inject-code <codeinjectionsemantics>` tag. To ease the binding developer
work, the injected code can make use of special variables that will be replaced
by the correct values. This also shields the developer from some |project|
implementation specifics.


.. _variables:

Variables
=========


.. _cpp_return_argument:

**%0**

  Replaced by the C++ return variable of the Python method/function wrapper.


.. _arg_number:

**%#**

  Replaced by the name of a C++ argument in the position indicated by ``#``.
  The argument counting starts with ``%1``, since ``%0`` represents the return
  variable name. If the number indicates a variable that was removed in the
  type system description, but there is a default value for it, this value will
  be used. Consider this example:

      .. code-block:: c++

          void argRemoval(int a0, int a1 = 123);


      .. code-block:: xml

            <modify-function signature="argRemoval(int, int)">
                <modify-argument index="2">
                    <remove-argument/>
                </modify-argument>
            </modify-function>

  The ``%1`` will be replaced by the C++ argument name, and ``%2`` will get the
  value ``123``.


.. _argument_names:

**%ARGUMENT_NAMES**

  Replaced by a comma separated list with the names of all C++ arguments that
  were not removed on the type system description for the method/function. When
  the removed argument has a default value (original or provided in the type
  system), this value will be inserted in the argument list. If you want to remove
  the argument so completely that it doesn't appear in any form on the
  ``%ARGUMENT_NAMES`` replacement, don't forget to remove also its default value
  with the `<remove-default-expression/>
  <http://www.pyside.org/docs/apiextractor/typesystem_arguments.html#remove-default-expression>`_
  type system tag.

  Take the following method and related type system description as an example:

      .. code-block:: c++

          void argRemoval(int a0, Point a1 = Point(1, 2), bool a2 = true, Point a3 = Point(3, 4), int a4 = 56);


      .. code-block:: xml

            <modify-function signature="argRemoval(int, Point, bool, Point, int)">
                <modify-argument index="2">
                    <remove-argument/>
                    <replace-default-expression with="Point(6, 9)"/>
                </modify-argument>
                <modify-argument index="4">
                    <remove-argument/>
                </modify-argument>
            </modify-function>

  As seen on the XML description, the function's ``a1`` and ``a3`` arguments
  were removed. If any ``inject-code`` for this function uses ``%ARGUMENT_NAMES``
  the resulting list will be the equivalent of using individual argument type
  system variables this way:

      .. code-block:: c++

            %1, Point(6, 9), %3, Point(3, 4), %5


.. _arg_type:

**%ARG#_TYPE**

  Replaced by the type of a C++ argument in the position indicated by ``#``.
  The argument counting starts with ``%1``, since ``%0`` represents the return
  variable in other contexts, but ``%ARG0_TYPE`` will not translate to the
  return type, as this is already done by the
  :ref:`%RETURN_TYPE <return_type>` variable.
  Example:

      .. code-block:: c++

          void argRemoval(int a0, int a1 = 123);


      .. code-block:: xml

            <modify-function signature="argRemoval(int, int)">
                <modify-argument index="2">
                    <remove-argument/>
                </modify-argument>
            </modify-function>

  The ``%1`` will be replaced by the C++ argument name, and ``%2`` will get the
  value ``123``.


.. _converttocpp:

**%CONVERTTOCPP[CPPTYPE]**

  Replaced by a |project| conversion call that converts a Python variable
  to a C++ variable of the type indicated by ``CPPTYPE``.


.. _converttopython:

**%CONVERTTOPYTHON[CPPTYPE]**

  Replaced by a |project| conversion call that converts a C++ variable of the
  type indicated by ``CPPTYPE`` to the proper Python object.


.. _isconvertible:

**%ISCONVERTIBLE[CPPTYPE]**

  Replaced by a |project| "isConvertible" call that checks if a Python
  variable is convertible (via an implicit conversion or cast operator call)
  to a C++ variable of the type indicated by ``CPPTYPE``.


.. _checktype:

**%CHECKTYPE[CPPTYPE]**

  Replaced by a |project| "checkType" call that verifies if a Python
  if of the type indicated by ``CPPTYPE``.


.. _cppself:

**%CPPSELF**

  Replaced by the wrapped C++ object instance that owns the method in which the
  code with this variable was inserted.

.. _cpptype:

**%CPPTYPE**

  Replaced by the original name of the C++ class, without any namespace prefix,
  that owns the method in which the code with this variable was inserted. It will
  work on class level code injections also. Notice that ``CPPTYPE`` differs from
  the :ref:`%TYPE <type>` variable, for this latter may be translated to the original
  C++ class name or to the C++ wrapper class name.

  Namespaces will are treated as classes, so ``CPPTYPE`` will work for them and their
  enclosed functions as well.

.. _function_name:

**%FUNCTION_NAME**

  Replaced by the name of a function or method.



.. _py_return_argument:

**%PYARG_0**

  Replaced by the name of the Python return variable of the Python method/function wrapper.


.. _pyarg:

**%PYARG_#**

  Similar to ``%#``, but is replaced by the Python arguments (PyObjects)
  received by the Python wrapper method.

  If used in the context of a native code injection, i.e. in a virtual method
  override, ``%PYARG_#`` will be translated to one item of the Python tuple
  holding the arguments that should be passed to the Python override for this
  virtual method.

  The example

      .. code-block:: c++

          long a = PyInt_AS_LONG(%PYARG_1);


  is equivalent of

      .. code-block:: c++

          long a = PyInt_AS_LONG(PyTuple_GET_ITEM(%PYTHON_ARGUMENTS, 0));


  The generator tries to be smart with attributions, but it will work for the
  only simplest cases.

  This example

      .. code-block:: c++

           Py_DECREF(%PYARG_1);
           %PYARG_1 = PyInt_FromLong(10);


  is equivalent of

      .. code-block:: c++

          Py_DECREF(PyTuple_GET_ITEM(%PYTHON_ARGUMENTS, 0));
          PyTuple_SET_ITEM(%PYTHON_ARGUMENTS, 0, PyInt_FromLong(10));


.. _pyself:

**%PYSELF**

  Replaced by the Python wrapper variable (a PyObject) representing the instance
  bounded to the Python wrapper method which receives the custom code.


.. _python_arguments:

**%PYTHON_ARGUMENTS**

  Replaced by the pointer to the Python tuple with Python objects converted from
  the C++ arguments received on the binding override of a virtual method.
  This tuple is the same passed as arguments to the Python method overriding the
  C++ parent's one.


.. _python_method_override:

**%PYTHON_METHOD_OVERRIDE**

  This variable is used only on :ref:`native method code injections
  <codeinjecting_method_native>`, i.e. on the binding overrides for C++ virtual
  methods. It is replaced by a pointer to the Python method override.


.. _pythontypeobject:

**%PYTHONTYPEOBJECT**

  Replaced by the Python type object for the context in which it is inserted:
  method or class modification.


.. _beginallowthreads:

**%BEGIN_ALLOW_THREADS**

  Replaced by a thread state saving procedure.
  Must match with a :ref:`%END_ALLOW_THREADS <endallowthreads>` variable.


.. _endallowthreads:

**%END_ALLOW_THREADS**

  Replaced by a thread state restoring procedure.
  Must match with a :ref:`%BEGIN_ALLOW_THREADS <beginallowthreads>` variable.


.. _return_type:

**%RETURN_TYPE**

  Replaced by the type returned by a function or method.


.. _type:

**%TYPE**

  Replaced by the name of the class to which a function belongs. May be used
  in code injected at method or class level.


.. _example:

Example
=======

Just to illustrate the usage of the variables described in the previous
sections, below is an excerpt from the type system description of a |project|
test. It changes a method that received ``argc/argv`` arguments into something
that expects a Python sequence instead.

    .. code-block:: xml

        <modify-function signature="overloadedMethod(int, char**)">
            <modify-argument index="1">
                <replace-type modified-type="PySequence" />
            </modify-argument>
            <modify-argument index="2">
                <remove-argument />
            </modify-argument>
            <inject-code class="target" position="beginning">
                int argc;
                char** argv;
                if (!PySequence_to_argc_argv(%PYARG_1, &amp;argc, &amp;argv)) {
                    PyErr_SetString(PyExc_TypeError, "error");
                    return 0;
                }
                %RETURN_TYPE foo = %CPPSELF.%FUNCTION_NAME(argc, argv);
                %0 = %CONVERTTOPYTHON[%RETURN_TYPE](foo);

                for (int i = 0; i &lt; argc; ++i)
                    delete[] argv[i];
                delete[] argv;
            </inject-code>
        </modify-function>

