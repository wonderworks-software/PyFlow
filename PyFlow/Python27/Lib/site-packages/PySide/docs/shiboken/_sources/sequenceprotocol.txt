Sequence Protocol
-----------------

Support for the sequence protocol is achieved adding functions with special names, this is done using the add-function tag.

The special function names are:

    ============= =============================================== ==================== ===================
    Function name Parameters                                      Return type          CPython equivalent
    ============= =============================================== ==================== ===================
    __len__       PyObject* self                                  Py_ssize_t           PySequence_Size
    __getitem__   PyObject* self, Py_ssize_t _i                   PyObject*            PySequence_GetItem
    __setitem__   PyObject* self, Py_ssize_t _i, PyObject* _value int                  PySequence_SetItem
    __contains__  PyObject* self, PyObject* _value                int                  PySequence_Contains
    __concat__    PyObject* self, PyObject* _other                PyObject*            PySequence_Concat
    ============= =============================================== ==================== ===================

You just need to inform the function name to the add-function tag, without any parameter or return type information, when you do it, |project| will create a C function with parameters and return type definied by the table above.

The function needs to follow the same semantics of the *CPython equivalent* function, the only way to do it is using the :doc:`inject-code <codeinjectionsemantics>` tag.

A concrete exemple how to add sequence protocol support to a class can be found on shiboken tests, more precisely in the definition of the Str class in ``tests/samplebinding/typesystem_sample.xml``.

