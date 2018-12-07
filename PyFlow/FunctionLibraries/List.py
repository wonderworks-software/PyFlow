from ..Core.FunctionLibrary import *
# import types stuff
from ..Core.AGraphCommon import *
# import stuff you need
# ...


class List(FunctionLibraryBase):
    """
    doc string for List
    """
    def __init__(self):
        super(List, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'CategoryName|SubCategory name', 'Keywords': ['+', 'append', 'sum']})
    def append(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0)):
        """
        Sum of two ints.
        """
        return A + B