/*
 * This file is part of the Shiboken Python Bindings Generator project.
 *
 * Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#ifndef SBK_CONVERTER_H
#define SBK_CONVERTER_H

#include "sbkpython.h"
#include <limits>
#include "shibokenmacros.h"
#include "basewrapper.h"

/**
 *  This is a convenience macro identical to Python's PyObject_TypeCheck,
 *  except that the arguments have swapped places, for the great convenience
 *  of generator.
 */
#define SbkObject_TypeCheck(tp, ob) \
        (Py_TYPE(ob) == (tp) || PyType_IsSubtype(Py_TYPE(ob), (tp)))

extern "C"
{

/**
 *  SbkConverter is used to perform type conversions from C++
 *  to Python and vice-versa;.and it is also used for type checking.
 *  SbkConverter is a private structure that must be accessed
 *  using the functions provided by the converter API.
 */
struct SbkConverter;

/**
 *  Given a void pointer to a C++ object, this function must return
 *  the proper Python object. It may be either an existing wrapper
 *  for the C++ object, or a newly create one. Or even the Python
 *  equivalent of the C++ value passed in the argument.
 *
 *  C++ -> Python
 */
typedef PyObject* (*CppToPythonFunc)(const void*);

/**
 *  This function converts a Python object to a C++ value, it may be
 *  a pointer, value, class, container or primitive type, passed via
 *  a void pointer, that will be cast properly inside the function.
 *  This function is usually returned by an IsConvertibleToCppFunc
 *  function, or obtained knowing the type of the Python object input,
 *  thus it will not check the Python object type, and will expect
 *  the void pointer to be pointing to a proper variable.
 *
 *  Python -> C++
 */
typedef void (*PythonToCppFunc)(PyObject*,void*);

/**
 *  Checks if the Python object passed in the argument is convertible to a
 *  C++ type defined inside the function, it returns the converter function
 *  that will transform a Python argument into a C++ value.
 *  It returns NULL if the Python object is not convertible to the C++ type
 *  that the function represents.
 *
 *  Python -> C++ ?
 */
typedef PythonToCppFunc (*IsConvertibleToCppFunc)(PyObject*);

} // extern "C"

namespace Shiboken {
namespace Conversions {


class LIBSHIBOKEN_API SpecificConverter
{
public:
    enum Type
    {
        InvalidConversion,
        CopyConversion,
        PointerConversion,
        ReferenceConversion
    };

    explicit SpecificConverter(const char* typeName);

    inline SbkConverter* converter() { return m_converter; }
    inline operator SbkConverter*() const { return m_converter; }

    inline bool isValid() { return m_type != InvalidConversion; }
    inline operator bool() const { return m_type != InvalidConversion; }

    inline Type conversionType() { return m_type; }

    PyObject* toPython(const void* cppIn);
    void toCpp(PyObject* pyIn, void* cppOut);
private:
    SbkConverter* m_converter;
    Type m_type;
};


/**
 *  Creates a converter for a wrapper type.
 *  \param type                  A Shiboken.ObjectType that will receive the new converter.
 *  \param toCppPointerConvFunc  Function to retrieve the C++ pointer held by a Python wrapper.
 *  \param toCppPointerCheckFunc Check and return the retriever function of the C++ pointer held by a Python wrapper.
 *  \param pointerToPythonFunc   Function to convert a C++ object to a Python \p type wrapper, keeping their identity.
 *  \param copyToPythonFunc      Function to convert a C++ object to a Python \p type, copying the object.
 *  \returns                     The new converter referred by the wrapper \p type.
 */
LIBSHIBOKEN_API SbkConverter* createConverter(SbkObjectType* type,
                                              PythonToCppFunc toCppPointerConvFunc,
                                              IsConvertibleToCppFunc toCppPointerCheckFunc,
                                              CppToPythonFunc pointerToPythonFunc,
                                              CppToPythonFunc copyToPythonFunc = 0);

/**
 *  Creates a converter for a non wrapper type (primitive or container type).
 *  \param type         Python type representing to the new converter.
 *  \param toPythonFunc Function to convert a C++ object to a Python \p type.
 *  \returns            A new type converter.
 */
LIBSHIBOKEN_API SbkConverter* createConverter(PyTypeObject* type, CppToPythonFunc toPythonFunc);

LIBSHIBOKEN_API void deleteConverter(SbkConverter* converter);

/// Sets the Python object to C++ pointer conversion function.
LIBSHIBOKEN_API void setCppPointerToPythonFunction(SbkConverter* converter, CppToPythonFunc pointerToPythonFunc);

/// Sets the C++ pointer to Python object conversion functions.
LIBSHIBOKEN_API void setPythonToCppPointerFunctions(SbkConverter* converter,
                                                    PythonToCppFunc toCppPointerConvFunc,
                                                    IsConvertibleToCppFunc toCppPointerCheckFunc);

/**
 *  Adds a new conversion of a Python object to a C++ value.
 *  This is used in copy and implicit conversions.
 */
LIBSHIBOKEN_API void addPythonToCppValueConversion(SbkConverter* converter,
                                                   PythonToCppFunc pythonToCppFunc,
                                                   IsConvertibleToCppFunc isConvertibleToCppFunc);
LIBSHIBOKEN_API void addPythonToCppValueConversion(SbkObjectType* type,
                                                   PythonToCppFunc pythonToCppFunc,
                                                   IsConvertibleToCppFunc isConvertibleToCppFunc);

// C++ -> Python ---------------------------------------------------------------------------

/**
 *  Retrieves the Python wrapper object for the given \p cppIn C++ pointer object.
 *  This function is used only for Value and Object Types.
 *  Example usage:
 *      TYPE* var;
 *      PyObject* pyVar = pointerToPython(SBKTYPE, &var);
 */
LIBSHIBOKEN_API PyObject* pointerToPython(SbkObjectType* type, const void* cppIn);
LIBSHIBOKEN_API PyObject* pointerToPython(SbkConverter* converter, const void* cppIn);

/**
 *  For the given \p cppIn C++ reference it returns the Python wrapper object,
 *  always for Object Types, and when they already exist for reference types;
 *  for when the latter doesn't have an existing wrapper type, the C++ object
 *  is copied to Python.
 *  Example usage:
 *      TYPE& var = SOMETHING;
 *      PyObject* pyVar = referenceToPython(SBKTYPE, &var);
 */
LIBSHIBOKEN_API PyObject* referenceToPython(SbkObjectType* type, const void* cppIn);
LIBSHIBOKEN_API PyObject* referenceToPython(SbkConverter* converter, const void* cppIn);

/**
 *  Retrieves the Python wrapper object for the given C++ value pointed by \p cppIn.
 *  This function is used only for Value Types.
 *  Example usage:
 *      TYPE var;
 *      PyObject* pyVar = copyToPython(SBKTYPE, &var);
 */
LIBSHIBOKEN_API PyObject* copyToPython(SbkObjectType* type, const void* cppIn);
LIBSHIBOKEN_API PyObject* copyToPython(SbkConverter* converter, const void* cppIn);

// Python -> C++ ---------------------------------------------------------------------------

/**
 *  Returns a Python to C++ conversion function if the Python object is convertible to a C++ pointer.
 *  It returns NULL if the Python object is not convertible to \p type.
 */
LIBSHIBOKEN_API PythonToCppFunc isPythonToCppPointerConvertible(SbkObjectType* type, PyObject* pyIn);

/**
 *  Returns a Python to C++ conversion function if the Python object is convertible to a C++ value.
 *  The resulting converter function will create a copy of the Python object in C++, or implicitly
 *  convert the object to the expected \p type.
 *  It returns NULL if the Python object is not convertible to \p type.
 */
LIBSHIBOKEN_API PythonToCppFunc isPythonToCppValueConvertible(SbkObjectType* type, PyObject* pyIn);

/**
 *  Returns a Python to C++ conversion function if the Python object is convertible to a C++ reference.
 *  The resulting converter function will return the underlying C++ object held by the Python wrapper,
 *  or a new C++ value if it must be a implicit conversion.
 *  It returns NULL if the Python object is not convertible to \p type.
 */
LIBSHIBOKEN_API PythonToCppFunc isPythonToCppReferenceConvertible(SbkObjectType* type, PyObject* pyIn);

/// This is the same as isPythonToCppValueConvertible function.
LIBSHIBOKEN_API PythonToCppFunc isPythonToCppConvertible(SbkConverter* converter, PyObject* pyIn);

/**
 *  Returns the C++ pointer for the \p pyIn object cast to the type passed via \p desiredType.
 *  It differs from Shiboken::Object::cppPointer because it casts the pointer to a proper
 *  memory offset depending on the desired type.
 */
LIBSHIBOKEN_API void* cppPointer(PyTypeObject* desiredType, SbkObject* pyIn);

/// Converts a Python object \p pyIn to C++ and stores the result in the C++ pointer passed in \p cppOut.
LIBSHIBOKEN_API void pythonToCppPointer(SbkObjectType* type, PyObject* pyIn, void* cppOut);
LIBSHIBOKEN_API void pythonToCppPointer(SbkConverter* converter, PyObject* pyIn, void* cppOut);

/// Converts a Python object \p pyIn to C++, and copies the result in the C++ variable passed in \p cppOut.
LIBSHIBOKEN_API void pythonToCppCopy(SbkObjectType* type, PyObject* pyIn, void* cppOut);
LIBSHIBOKEN_API void pythonToCppCopy(SbkConverter* converter, PyObject* pyIn, void* cppOut);

/**
 *  Helper function returned by generated convertible checking functions
 *  that returns a C++ NULL when the input Python object is None.
 */
LIBSHIBOKEN_API void nonePythonToCppNullPtr(PyObject*, void* cppOut);

/**
 *  Returns true if the \p toCpp function passed is an implicit conversion of Python \p type.
 *  It is used when C++ expects a reference argument, so it may be the same object received
 *  from Python, or another created through implicit conversion.
 */
LIBSHIBOKEN_API bool isImplicitConversion(SbkObjectType* type, PythonToCppFunc toCpp);

/// Registers a converter with a type name that may be used to retrieve the converter.
LIBSHIBOKEN_API void registerConverterName(SbkConverter* converter, const char* typeName);

/// Returns the converter for a given type name, or NULL if it wasn't registered before.
LIBSHIBOKEN_API SbkConverter* getConverter(const char* typeName);

/// Returns the converter for a primitive type.
LIBSHIBOKEN_API SbkConverter* primitiveTypeConverter(int index);

/// Returns true if a Python sequence is comprised of objects of the given \p type.
LIBSHIBOKEN_API bool checkSequenceTypes(PyTypeObject* type, PyObject* pyIn);

/// Returns true if a Python sequence is comprised of objects of a type convertible to the one represented by the given \p converter.
LIBSHIBOKEN_API bool convertibleSequenceTypes(SbkConverter* converter, PyObject* pyIn);

/// Returns true if a Python sequence is comprised of objects of a type convertible to \p type.
LIBSHIBOKEN_API bool convertibleSequenceTypes(SbkObjectType* type, PyObject* pyIn);

/// Returns true if a Python sequence can be converted to a C++ pair.
LIBSHIBOKEN_API bool checkPairTypes(PyTypeObject* firstType, PyTypeObject* secondType, PyObject* pyIn);

/// Returns true if a Python sequence can be converted to a C++ pair.
LIBSHIBOKEN_API bool convertiblePairTypes(SbkConverter* firstConverter, bool firstCheckExact, SbkConverter* secondConverter, bool secondCheckExact, PyObject* pyIn);

/// Returns true if a Python dictionary can be converted to a C++ hash or map.
LIBSHIBOKEN_API bool checkDictTypes(PyTypeObject* keyType, PyTypeObject* valueType, PyObject* pyIn);

/// Returns true if a Python dictionary can be converted to a C++ hash or map.
LIBSHIBOKEN_API bool convertibleDictTypes(SbkConverter* keyConverter, bool keyCheckExact, SbkConverter* valueConverter, bool valueCheckExact, PyObject* pyIn);

/// Returns the Python type object associated with the given \p converter.
LIBSHIBOKEN_API PyTypeObject* getPythonTypeObject(SbkConverter* converter);

/// Returns the Python type object for the given \p typeName.
LIBSHIBOKEN_API PyTypeObject* getPythonTypeObject(const char* typeName);

/// Returns true if the Python type associated with the converter is a value type.
LIBSHIBOKEN_API bool pythonTypeIsValueType(SbkConverter* converter);

/// Returns true if the Python type associated with the converter is an object type.
LIBSHIBOKEN_API bool pythonTypeIsObjectType(SbkConverter* converter);

/// Returns true if the Python type associated with the converter is a wrapper type.
LIBSHIBOKEN_API bool pythonTypeIsWrapperType(SbkConverter* converter);

#define SBK_PY_LONG_LONG_IDX            0
#define SBK_BOOL_IDX                    1
#define SBK_CHAR_IDX                    2
#define SBK_CONSTCHARPTR_IDX            3
#define SBK_DOUBLE_IDX                  4
#define SBK_FLOAT_IDX                   5
#define SBK_INT_IDX                     6
#define SBK_SIGNEDINT_IDX               6
#define SBK_LONG_IDX                    7
#define SBK_SHORT_IDX                   8
#define SBK_SIGNEDCHAR_IDX              9
#define SBK_STD_STRING_IDX             10
#define SBK_UNSIGNEDPY_LONG_LONG_IDX   11
#define SBK_UNSIGNEDCHAR_IDX           12
#define SBK_UNSIGNEDINT_IDX            13
#define SBK_UNSIGNEDLONG_IDX           14
#define SBK_UNSIGNEDSHORT_IDX          15
#define SBK_VOIDPTR_IDX                16

template<typename T> SbkConverter* PrimitiveTypeConverter() { return 0; }
template<> inline SbkConverter* PrimitiveTypeConverter<PY_LONG_LONG>() { return primitiveTypeConverter(SBK_PY_LONG_LONG_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<bool>() { return primitiveTypeConverter(SBK_BOOL_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<char>() { return primitiveTypeConverter(SBK_CHAR_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<const char*>() { return primitiveTypeConverter(SBK_CONSTCHARPTR_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<double>() { return primitiveTypeConverter(SBK_DOUBLE_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<float>() { return primitiveTypeConverter(SBK_FLOAT_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<int>() { return primitiveTypeConverter(SBK_INT_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<long>() { return primitiveTypeConverter(SBK_LONG_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<short>() { return primitiveTypeConverter(SBK_SHORT_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<signed char>() { return primitiveTypeConverter(SBK_SIGNEDCHAR_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<std::string>() { return primitiveTypeConverter(SBK_STD_STRING_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<unsigned PY_LONG_LONG>() { return primitiveTypeConverter(SBK_UNSIGNEDPY_LONG_LONG_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<unsigned char>() { return primitiveTypeConverter(SBK_UNSIGNEDCHAR_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<unsigned int>() { return primitiveTypeConverter(SBK_UNSIGNEDINT_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<unsigned long>() { return primitiveTypeConverter(SBK_UNSIGNEDLONG_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<unsigned short>() { return primitiveTypeConverter(SBK_UNSIGNEDSHORT_IDX); }
template<> inline SbkConverter* PrimitiveTypeConverter<void*>() { return primitiveTypeConverter(SBK_VOIDPTR_IDX); }

} } // namespace Shiboken::Conversions

struct _SbkGenericType { PyHeapTypeObject super; SbkConverter** converter; };
#define SBK_CONVERTER(pyType) (*reinterpret_cast<_SbkGenericType*>(pyType)->converter)


#endif // SBK_CONVERTER_H
