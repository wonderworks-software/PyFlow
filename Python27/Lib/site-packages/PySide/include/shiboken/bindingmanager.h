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

#ifndef BINDINGMANAGER_H
#define BINDINGMANAGER_H

#include "sbkpython.h"
#include <set>
#include "shibokenmacros.h"

struct SbkObject;
struct SbkObjectType;

namespace Shiboken
{

typedef void (*ObjectVisitor)(SbkObject*, void*);

class LIBSHIBOKEN_API BindingManager
{
public:
    static BindingManager& instance();

    bool hasWrapper(const void *cptr);

    void registerWrapper(SbkObject* pyObj, void* cptr);
    void releaseWrapper(SbkObject* wrapper);

    SbkObject* retrieveWrapper(const void* cptr);
    PyObject* getOverride(const void* cptr, const char* methodName);

    void addClassInheritance(SbkObjectType* parent, SbkObjectType* child);
    /**
     * \deprecated Use \fn resolveType(void**, SbkObjectType*), this version is broken when used with multiple inheritance
     *             because the \p cptr pointer of the discovered type may be different of the given \p cptr in case
     *             of multiple inheritance
     */
    SBK_DEPRECATED(SbkObjectType* resolveType(void* cptr, SbkObjectType* type));
    /**
     * Try to find the correct type of *cptr knowing that it's at least of type \p type.
     * In case of multiple inheritance this function may change the contents of cptr.
     * \param cptr a pointer to a pointer to the instance of type \p type
     * \param type type of *cptr
     * \warning This function is slow, use it only as last resort.
     */
    SbkObjectType* resolveType(void** cptr, SbkObjectType* type);

    std::set<PyObject*> getAllPyObjects();

    /**
     * Calls the function \p visitor for each object registered on binding manager.
     * \note As various C++ pointers can point to the same PyObject due to multiple inheritance
     *       a PyObject can be called more than one time for each PyObject.
     * \param visitor function called for each object.
     * \param data user data passed as second argument to the visitor function.
     */
    void visitAllPyObjects(ObjectVisitor visitor, void* data);

private:
    ~BindingManager();
    // disable copy
    BindingManager();
    BindingManager(const BindingManager&);
    BindingManager& operator=(const BindingManager&);

    struct BindingManagerPrivate;
    BindingManagerPrivate* m_d;
};

} // namespace Shiboken

#endif // BINDINGMANAGER_H

