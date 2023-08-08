## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import codecs
import shutil
import os
import requests
import pathlib

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class IOLib(FunctionLibraryBase):
    """doc string for IOLib"""

    def __init__(self, packageName):
        super(IOLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def readAllText( #inExec=("ExecPin", None), outExec=(REF, ("ExecPin", None)),
                    file=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "FilePathWidget"}), 
                    encoding=('StringPin', 'utf-8'),
                    text=(REF, ('StringPin', "")),
                    error_msg=(REF, ('StringPin', ""))):
        err_msg = ""
        all_text = ""
        try:
            with codecs.open(file, encoding=encoding) as f:
                all_text = f.read()
        except Exception as e:
            err_msg = str(e)
        error_msg(err_msg)
        text(all_text)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def readAllLines(file=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "FilePathWidget"}),
                     encoding=('StringPin', 'utf-8'),
                     lines=(REF, ('StringPin', [], {PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported})),
                     error_msg=(REF, ('StringPin', ""))):
        err_msg = ""
        try:
             with codecs.open(file, encoding) as f:
                all_lines = list(f.readlines())
        except Exception as e:
            err_msg = str(e)
        error_msg(err_msg)
        lines(all_lines if None != all_lines else [])
    
    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def copyFile(src=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "FilePathWidget"}),
                 dst=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "FilePathWidget"}),
                 ok=(REF, ('BoolPin', False)),
                 error_msg=(REF, ('StringPin', ""))):
        ret = True
        err_msg = ""
        try:
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)
        except Exception as e:
            ret = False
            err_msg = str(e)
        error_msg(err_msg)
        ok(ret)
        
    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def removeFile(file=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "FilePathWidget"}),
                 ok=(REF, ('BoolPin', False)),
                 error_msg=(REF, ('StringPin', ""))):
        ret = True
        err_msg = ""
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            ret = False
            err_msg = str(e)
        error_msg(err_msg)
        ok(ret)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def copyDir(src=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
                 dst=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
                 ok=(REF, ('BoolPin', False)),
                 error_msg=(REF, ('StringPin', False))):
        ret = True
        err_msg = ""
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        except Exception as e:
            ret = False
            err_msg = str(e)
        error_msg(err_msg)
        ok(ret)
        
    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Pure)
    def pathCombine(p1=("StringPin", "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}), p2=("StringPin", "")):
        ret: pathlib.PurePath = pathlib.PurePath(p1, p2)
        # ret = os.path.normpath(os.path.join(str(p1), str(p2)))
        return ret.as_posix()
    
    
    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def removeDir(dir=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"}),
                  ignore_error=('BoolPin', False),
                  ok=(REF, ('BoolPin', False)),
                  error_msg=(REF, ('StringPin', ""))):
        ret = True
        err_msg = ""
        try:
            if os.path.isdir(dir):
                shutil.rmtree(dir, ignore_error)
        except Exception as e:
            ret = False
            err_msg = str(e)
        error_msg(err_msg)
        ok(ret)
        
    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'IO', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Callable)
    def httpUploadFile(url=('StringPin', ""), 
                       store_path=('StringPin', ""),
                       file=('StringPin', "", {PinSpecifires.INPUT_WIDGET_VARIANT: "FilePathWidget"}),
                       ok=(REF, ('BoolPin', False)),
                       error_msg=(REF, ('StringPin', ""))):
        ret = True
        err_msg = ""
        try:
            if not os.path.isfile(file):
                ret = False
                error_msg = "file not exist"
            else:
                rsp: requests.Response = requests.post(url, {"file_path": store_path}, files={"file": open(file, 'rb')})
                if 200 != rsp.status_code:
                    ret = False
                    err_msg = rsp.content
        except Exception as e:
            ret = False
            err_msg = str(e)
        error_msg(err_msg)
        ok(ret)
        
        

    
    
    
    
    
    


    