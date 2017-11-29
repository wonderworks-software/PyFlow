**************************
Frequently Asked Questions
**************************

This is a list of Frequently Asked Questions about |project|.  Feel free to
suggest new entries!

General
=======

What is Shiboken?
-----------------

Shiboken is a `GeneratorRunner <http://www.pyside.org/home-binding/binding-generator>`_
plugin that outputs C++ code for CPython extensions. The first version of PySide
had source code based on Boost templates. It was easier to produce code but a
paradigm change was needed, as the next question explains.

Why did you switch from Boost.Python to Shiboken?
-------------------------------------------------

The main reason was the size reduction. Boost.Python makes excessive use of templates
resulting in a significant increase of the binaries size. On the other hand, as Shiboken
generates CPython code, the resulting binaries are smaller.

Creating bindings
=================

Can I wrap non-Qt libraries?
----------------------------

Yes. Check Shiboken source code for an example (libsample).


Is there any runtime dependency on the generated binding?
---------------------------------------------------------

Yes. Only libshiboken, and the obvious Python interpreter
and the C++ library that is being wrapped.

What do I have to do to create my bindings?
-------------------------------------------

.. todo: put link to typesystem documentation

Most of the work is already done by the API Extractor. The developer creates
a `typesystem <http://www.pyside.org/docs/apiextractor/typesystem.html>`_ file
with any customization wanted in the generated code, like removing classes or
changing method signatures. The generator will output the .h and .cpp files
with the CPython code that will wrap the target library for python.

Is there any recommended build system?
--------------------------------------

Both API Extractor and generator uses and recommends the CMake build system.

Can I write closed-source bindings with the generator?
------------------------------------------------------

Yes, as long as you use a LGPL version of Qt, due to runtime requirements.

What is 'inject code'?
----------------------

That's how we call customized code that will be *injected* into the
generated at specific locations. They are specified inside the typesytem.

