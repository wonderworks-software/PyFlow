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


import random

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class StringLib(FunctionLibraryBase):
    """doc string for StringLib"""

    def __init__(self, packageName):
        super(StringLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def lower(s=('StringPin', "")):
        return str.lower(s)

    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def upper(s=('StringPin', "")):
        return str.upper(s)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def tostring(s=('AnyPin', 0)):
        return str(s)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def isEmpty(s=('StringPin', "")):
        return len(s) <= 0
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def notEmpty(s=('StringPin', "")):
        return len(s) > 0
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def equal(l=('StringPin', ""), r=('StringPin', "")):
        return l == r
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def strimp(s=('StringPin', ""), chars=('StringPin', "")):
        return s.strip(chars)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def lstrip(s=('StringPin', ""), chars=('StringPin', "")):
        return s.lstrip(chars)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ""), meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def rstrip(s=('StringPin', ""), chars=('StringPin', "")):
        return s.rstrip(chars)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported}), 
                    meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def split(s=('StringPin', ""), sep=('StringPin', "")):
        return str.split(s, sep)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported}), 
                    meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def starstWith(s=('StringPin', ""), prefix=('StringPin', "", { PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported|PinOptions.ChangeTypeOnConnection })):
        return s.startswith(prefix)
    
    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported}), 
                    meta={NodeMeta.CATEGORY: 'String', NodeMeta.KEYWORDS: []})
    def endsWith(s=('StringPin', ""), suffix=('StringPin', "", { PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported|PinOptions.ChangeTypeOnConnection })):
        return s.endswith(suffix)
    
    
    
    
    
    
    
    
    
    


    