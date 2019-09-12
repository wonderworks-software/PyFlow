from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE


class DemoLib(FunctionLibraryBase):
    '''doc string for DemoLib'''

    def __init__(self, packageName):
        super(DemoLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'DemoLib', NodeMeta.KEYWORDS: []})
    # Return a random integer N such that a <= N <= b
    def demoLibGreet(word=('StringPin', "Greet!")):
        """Docstrings are in **rst** format!"""
        print(word)
