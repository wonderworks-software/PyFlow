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

from PyFlow.PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.PyFlow.Core.Common import *


class RandomLib(FunctionLibraryBase):
    """doc string for RandomLib"""

    def __init__(self, packageName):
        super(RandomLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'Math|random', NodeMeta.KEYWORDS: [], NodeMeta.CACHE_ENABLED: False})
    # Return a random integer N such that a <= N <= b
    def randint(start=('IntPin', 0), end=('IntPin', 10), Result=(REF, ('IntPin', 0))):
        """Return a random integer N such that a <= N <= b."""
        Result(random.randint(start, end))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'Math|random', NodeMeta.KEYWORDS: []})
    # Shuffle the sequence x in place
    def shuffle(seq=('AnyPin', [], {PinSpecifires.CONSTRAINT: "1"}), Result=(REF, ('AnyPin', [], {PinSpecifires.CONSTRAINT: "1"}))):
        """Shuffle the sequence x in place."""
        random.shuffle(seq)
        Result(seq)
