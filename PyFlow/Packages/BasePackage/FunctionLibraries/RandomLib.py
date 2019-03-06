import random

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


class RandomLib(FunctionLibraryBase):
    packageName = PACKAGE_NAME
    '''doc string for RandomLib'''
    def __init__(self):
        super(RandomLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'Math|random', 'Keywords': [], PROPAGATE_DIRTY: ['Result']})
    ## Return a random integer N such that a <= N <= b
    def randint(start=('IntPin', 0), end=('IntPin', 10), Result=("Reference", ('IntPin', 0))):
        '''
        Return a random integer N such that a <= N <= b
        '''
        Result(random.randint(start, end))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|random', 'Keywords': [], PROPAGATE_DIRTY: ['Result']})
    ## Shuffle the sequence x in place
    def shuffle(seq=('ListPin', []), Result=("Reference", ('ListPin', []))):
        '''
        Shuffle the sequence x in place
        '''
        random.shuffle(seq)
        Result(seq)
