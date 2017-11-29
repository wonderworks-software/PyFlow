#ifndef __PYSIDEWEAKREF__
#define __PYSIDEWEAKREF__

#include <pysidemacros.h>
#include <sbkpython.h>

typedef void (*PySideWeakRefFunction)(void* userData);

namespace PySide { namespace WeakRef {

PYSIDE_API PyObject* create(PyObject* ob, PySideWeakRefFunction func, void* userData);

} //PySide
} //WeakRef


#endif
