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


from math import pi

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class FloatLib(FunctionLibraryBase):
    '''doc string for FloatLib'''
    def __init__(self, packageName):
        super(FloatLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': ['lerp']})
    ## Linear interpolate
    def lerpf(a=('FloatPin', 0.0), b=('FloatPin', 0.0), alpha=('FloatPin', 0.0)):
        '''
        Linear interpolate
        '''
        return lerp(a, b, clamp(alpha, 0.0, 1.0))

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Float', 'Keywords': []})
    def nearlyEqual(a=('FloatPin', 0.0), b=('FloatPin', 0.0), abs_tol=('FloatPin', 0.0)):
        return abs(a - b) < abs_tol

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def multByPi(a=('FloatPin', 0.0)):
        '''
        Multiplies the input value by pi.
        '''
        return a * pi

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def normalizeToRange(Value=('FloatPin', 0.0), RangeMin=('FloatPin', 0.0), RangeMax=('FloatPin', 0.0)):
        '''
        Returns Value normalized to the given range. (e.g. 20 normalized to the range 10->50 would result in 0.25)
        '''
        if RangeMin == RangeMax:
            return RangeMin

        if RangeMin > RangeMax:
            RangeMin, RangeMax = RangeMax, RangeMin
        return (Value - RangeMin) / (RangeMax - RangeMin)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Float', 'Keywords': []})
    def roundf(Value=('FloatPin', 0.0), Digits=('IntPin', 0)):
        '''
        Round a number to a given precision in decimal digits.
        '''
        return round(Value, Digits)
