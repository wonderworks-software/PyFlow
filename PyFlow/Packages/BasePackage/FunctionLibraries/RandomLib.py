from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *


class RandomLib(FunctionLibraryBase):
    '''doc string for RandomLib'''
    def __init__(self):
        super(RandomLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|random', 'Keywords': []})
    ## Return a random integer N such that a <= N <= b
    def randint(start=(DataTypes.Int, 0), end=(DataTypes.Int, 10), Result=(DataTypes.Reference, (DataTypes.Int, 0))):
        '''
        Return a random integer N such that a <= N <= b
        '''
        push(Result)
        Result(random.randint(start, end))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|random', 'Keywords': []})
    ## Shuffle the sequence x in place
    def shuffle(seq=(DataTypes.Array, []), Result=(DataTypes.Reference, (DataTypes.Array, []))):
        '''
        Shuffle the sequence x in place
        '''
        random.shuffle(seq)
        Result(seq)
