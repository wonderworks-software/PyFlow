from FunctionLibrary import *
# import types stuff
from AGraphCommon import *
# import stuff you need
# ...
import os
import platform


class DefaultLib(FunctionLibraryBase):
    '''doc string for DefaultLib'''
    def __init__(self):
        super(DefaultLib, self).__init__()

    @staticmethod
    @annotated(returns=None, meta={'Category': 'DefaultLib|Info', 'Keywords': ['version', 'os']})
    def getplatform(system=(DataTypes.Reference, DataTypes.String), version=(DataTypes.Reference, DataTypes.String)):
        '''Os information'''
        system.setData(platform.system())
        version.setData(platform.version())

    @staticmethod
    @annotated(returns=DataTypes.Any, meta={'Category': 'Array', 'Keywords': ['get', '[]']})
    def getitem(arr=(DataTypes.Array, []), index=(DataTypes.Int, 0)):
        '''Get item from iterable by index'''
        try:
            return arr[index]
        except:
            return None

    @staticmethod
    @annotated(returns=DataTypes.Bool, nodeType=NodeTypes.Callable, meta={'Category': 'Array', 'Keywords': ['set', '[]']})
    def setitem(arr=(DataTypes.Array, []), index=(DataTypes.Int, 0), dat=(DataTypes.Any, None)):
        '''Set iterable item by index'''
        try:
            arr[index] = dat
            return True
        except:
            return False
