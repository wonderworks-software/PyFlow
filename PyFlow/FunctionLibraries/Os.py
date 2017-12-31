from FunctionLibrary import *
# import types stuff
from AGraphCommon import *
# import stuff you need
# ...
import os
import platform


class Os(FunctionLibraryBase):
    '''doc string for Os'''
    def __init__(self):
        super(Os, self).__init__()

    @staticmethod
    @annotated(returns=None, meta={'Category': 'Os|Info', 'Keywords': ['version', 'os']})
    def getplatform(system=(DataTypes.Reference, DataTypes.String), version=(DataTypes.Reference, DataTypes.String)):
        '''Os information'''
        system.setData(platform.system())
        version.setData(platform.version())
