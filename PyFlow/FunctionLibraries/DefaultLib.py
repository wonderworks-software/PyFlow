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
    @annotated(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': ['print']})
    def pyprint(entity=(DataTypes.String, None)):
        '''print string'''
        print(entity)

    @staticmethod
    @annotated(returns=None, meta={'Category': 'DefaultLib|Info', 'Keywords': ['version', 'os']})
    def getplatform(system=(DataTypes.Reference, DataTypes.String), version=(DataTypes.Reference, DataTypes.String)):
        '''Os information'''
        system.setData(platform.system())
        version.setData(platform.version())
