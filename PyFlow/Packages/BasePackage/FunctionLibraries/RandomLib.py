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
    def randint(start=('IntPin', 0), end=('IntPin', 10), Result=(DataTypes.Reference, ('IntPin', 0))):
        '''
        Return a random integer N such that a <= N <= b
        '''
        push(Result)
        Result(random.randint(start, end))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|random', 'Keywords': []})
    ## Shuffle the sequence x in place
    def shuffle(seq=('ListPin', []), Result=(DataTypes.Reference, ('ListPin', []))):
        '''
        Shuffle the sequence x in place
        '''
        random.shuffle(seq)
        Result(seq)
