from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class ListLib(FunctionLibraryBase):
    '''doc string for ListLib'''
    def __init__(self, packageName):
        super(ListLib, self).__init__(packageName)

    # TODO: Create pin descriptor/builder class to pass as function arguments instead of tuples
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', '', {'constraint': '1'}), meta={'Category': 'List', 'Keywords': []})
    def selectInList(arr=('AnyPin', [], {'constraint': '1'}), Index=("IntPin", 0), Result=("Reference", ("BoolPin", False))):
        try:
            element = arr[Index]
            Result(True)
            return element
        except:
            Result(False)
