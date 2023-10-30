## -*- coding: utf-8 -*-
## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

## http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.Core import FunctionLibraryBase, IMPLEMENT_NODE
from PyFlow.Core.Common import *
import os
import os.path as osPath


class PathLib(FunctionLibraryBase):
    """
    Os.Path Library wrap
    """

    def __init__(self, packageName):
        super(PathLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def abspath(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return a absolute version of a path. On most platforms, this is equivalent to calling the function normpath()"""
        return osPath.abspath(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Extract",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def basename(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the base name of pathname path. This is the second element of the pair returned by passing path to the function split(). Note that the result of this function is different from the Unix basename program; where basename for '/foo/bar/' returns 'bar', the basename() function returns an empty string ('')"""
        return osPath.basename(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Extract",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def commonprefix(path=("StringPin", [])):
        """Return the longest path prefix (taken character-by-character) that is a prefix of all paths in list. If list is empty, return the empty string (''). Note that this may return invalid paths because it works a character at a time"""
        return osPath.commonprefix(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Extract",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def dirname(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the directory name of pathname path. This is the first element of the pair returned by passing path to the function split()."""
        return osPath.dirname(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "file", "folder", "path"],
        },
    )
    def exists(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if path refers to an existing path. Returns False for broken symbolic links. On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists."""
        return osPath.exists(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "file", "folder", "path"],
        },
    )
    def lexists(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if path refers to an existing path. Returns True for broken symbolic links. Equivalent to exists() on platforms lacking os.lstat()."""
        return osPath.lexists(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def expanduser(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user’s home directory.
        On Unix, an initial ~ is replaced by the environment variable HOME if it is set; otherwise the current user’s home directory is looked up in the password directory through the built-in module pwd. An initial ~user is looked up directly in the password directory.
        On Windows, HOME and USERPROFILE will be used if set, otherwise a combination of HOMEPATH and HOMEDRIVE will be used. An initial ~user is handled by stripping the last directory component from the created user path derived above.
        If the expansion fails or if the path does not begin with a tilde, the path is returned unchanged."""
        return osPath.expanduser(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def expandvars(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the argument with environment variables expanded. Substrings of the form $name or ${name} are replaced by the value of environment variable name. Malformed variable names and references to non-existing variables are left unchanged.
        On Windows, %name% expansions are supported in addition to $name and ${name}."""
        return osPath.expandvars(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Time",
            NodeMeta.KEYWORDS: ["time", "file", "path"],
        },
    )
    def getatime(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the time of last access of path. The return value is a number giving the number of seconds since the epoch (see the time module). Raise os.error if the file does not exist or is inaccessible."""
        return osPath.getatime(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Time",
            NodeMeta.KEYWORDS: ["time", "file", "path"],
        },
    )
    def getmtime(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the time of last modification of path. The return value is a number giving the number of seconds since the epoch (see the time module). Raise os.error if the file does not exist or is inaccessible."""
        return osPath.getmtime(path, path2)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Time",
            NodeMeta.KEYWORDS: ["time", "file", "path"],
        },
    )
    def getctime(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the system’s ctime which, on some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time for path. The return value is a number giving the number of seconds since the epoch (see the time module). Raise os.error if the file does not exist or is inaccessible."""
        return osPath.getctime(path, path2)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("IntPin", 0),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path",
            NodeMeta.KEYWORDS: ["size", "file", "path"],
        },
    )
    def getsize(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the size, in bytes, of path. Raise os.error if the file does not exist or is inaccessible."""
        return osPath.getctime(path, path2)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "file", "path"],
        },
    )
    def isabs(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if path is an absolute pathname. On Unix, that means it begins with a slash, on Windows that it begins with a (back)slash after chopping off a potential drive letter."""
        return osPath.isabs(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "file", "path"],
        },
    )
    def isFile(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if path is an existing regular file. This follows symbolic links, so both islink() and isfile() can be true for the same path."""
        return osPath.isfile(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "folder", "Directory", "dir", "path"],
        },
    )
    def isDir(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if path is an existing directory. This follows symbolic links, so both islink() and isdir() can be true for the same path."""
        return osPath.isdir(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "file", "path"],
        },
    )
    def islink(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if path refers to a directory entry that is a symbolic link. Always False if symbolic links are not supported by the Python runtime."""
        return osPath.islink(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Test",
            NodeMeta.KEYWORDS: ["test", "file", "path"],
        },
    )
    def ismount(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return True if pathname path is a mount point: a point in a file system where a different file system has been mounted. The function checks whether path’s parent, path/.., is on a different device than path, or whether path/.. and path point to the same i-node on the same device — this should detect mount points for all Unix and POSIX variants."""
        return osPath.ismount(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["test", "file", "path"],
        },
    )
    def join(
        base=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        paths=("StringPin", []),
    ):
        """Join one or more path components intelligently. The return value is the concatenation of path and any members of *paths with exactly one directory separator (os.sep) following each non-empty part except the last, meaning that the result will only end in a separator if the last part is empty. If a component is an absolute path, all previous components are thrown away and joining continues from the absolute path component.
        On Windows, the drive letter is not reset when an absolute path component (e.g., r'\foo') is encountered. If a component contains a drive letter, all previous components are thrown away and the drive letter is reset. Note that since there is a current directory for each drive, os.path.join("c:", "foo") represents a path relative to the current directory on drive C: (c:foo), not c:\foo."""
        return osPath.join(base, paths)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def normcase(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Normalize the case of a pathname. On Unix and Mac OS X, this returns the path unchanged; on case-insensitive filesystems, it converts the path to lowercase. On Windows, it also converts forward slashes to backward slashes."""
        return osPath.normcase(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def normpath(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B. This string manipulation may change the meaning of a path that contains symbolic links. On Windows, it converts forward slashes to backward slashes. To normalize case, use normcase()."""
        return osPath.normpath(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def realpath(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)."""
        return osPath.realpath(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Convert",
            NodeMeta.KEYWORDS: ["file", "folder", "path"],
        },
    )
    def relpath(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        start=("StringPin", os.curdir),
    ):
        """Return a relative filepath to path either from the current directory or from an optional start directory. This is a path computation: the filesystem is not accessed to confirm the existence or nature of path or start.
        start defaults to os.curdir.
        Availability: Windows, Unix."""
        return osPath.relpath(path)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Split",
            NodeMeta.KEYWORDS: ["file", "path"],
        },
    )
    def split(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        head=(REF, ("StringPin", "")),
        tail=(REF, ("StringPin", "")),
    ):
        """Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty. Trailing slashes are stripped from head unless it is the root (one or more slashes only). In all cases, join(head, tail) returns a path to the same location as path (but the strings may differ). Also see the functions dirname() and basename()."""
        splited = osPath.split(path)
        if len(splited):
            head(splited[0])
            tail(splited[1])
        else:
            head("")
            tail("")
        return list(splited)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Split",
            NodeMeta.KEYWORDS: ["file", "path"],
        },
    )
    def splitdrive(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        drive=(REF, ("StringPin", "")),
        tail=(REF, ("StringPin", "")),
    ):
        """Split the pathname path into a pair (drive, tail) where drive is either a drive specification or the empty string. On systems which do not use drive specifications, drive will always be the empty string. In all cases, drive + tail will be the same as path."""
        splited = osPath.splitdrive(path)
        if len(splited):
            drive(splited[0])
            tail(splited[1])
        else:
            drive("")
            tail("")
        return list(splited)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Split",
            NodeMeta.KEYWORDS: ["file", "path"],
        },
    )
    def splitext(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        root=(REF, ("StringPin", "")),
        ext=(REF, ("StringPin", "")),
    ):
        """Split the pathname path into a pair (root, ext) such that root + ext == path, and ext is empty or begins with a period and contains at most one period. Leading periods on the basename are ignored; splitext('.cshrc') returns ('.cshrc', '')."""
        splited = osPath.splitext(path)
        if len(splited):
            root(splited[0])
            ext(splited[1])
        else:
            root("")
            ext("")
        return list(splited)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|Split",
            NodeMeta.KEYWORDS: ["file", "path"],
        },
    )
    def splitunc(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        unc=(REF, ("StringPin", "")),
        rest=(REF, ("StringPin", "")),
    ):
        """Split the pathname path into a pair (unc, rest) so that unc is the UNC mount point (such as r'\\host\mount'), if present, and rest the rest of the path (such as r'\path\file.ext'). For paths containing drive letters, unc will always be the empty string."""
        splited = osPath.splitdrive(path)
        if len(splited):
            unc(splited[0])
            rest(splited[1])
        else:
            unc("")
            rest("")
        return list(splited)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|GetFiles",
            NodeMeta.KEYWORDS: ["get", "folder", "file", "Directory", "dir", "path"],
        },
    )
    def walk(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
        topdown=("BoolPin", False),
        files=(REF, ("StringPin", [])),
        folders=(REF, ("StringPin", [])),
    ):
        """Lists files and directories on Path recursive"""
        paths = []
        pfiles = []
        pfolders = []
        for root, dirs, ofiles in os.walk(path, topdown=topdown):
            for name in ofiles:
                paths.append(osPath.join(root, name))
                pfiles.append(osPath.join(root, name))
            for name in dirs:
                paths.append(osPath.join(root, name))
                pfolders.append(osPath.join(root, name))
        files(pfiles)
        folders(pfolders)
        return paths

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|GetFiles",
            NodeMeta.KEYWORDS: ["get", "folder", "dir", "Directory", "path"],
        },
    )
    def getFolders(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Lists directories on Path"""
        return [
            osPath.join(path, x)
            for x in os.listdir(path)
            if osPath.isdir(osPath.join(path, x))
        ]

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|GetFiles",
            NodeMeta.KEYWORDS: ["get", "File", "dir", "Directory", "path"],
        },
    )
    def getFiles(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Lists files on Path"""
        return [
            osPath.join(path, x)
            for x in os.listdir(path)
            if osPath.isfile(osPath.join(path, x))
        ]

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", []),
        meta={
            NodeMeta.CATEGORY: "Python|OS|Path|GetFiles",
            NodeMeta.KEYWORDS: ["get", "folder", "file", "Directory", "dir", "path"],
        },
    )
    def listDir(
        path=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})
    ):
        """Lists files and directories on Path"""
        return [osPath.join(path, x) for x in os.listdir(path)]
