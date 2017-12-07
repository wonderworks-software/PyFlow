from FunctionLibrary import *


class MathLib(FunctionLibraryBase):
    @staticmethod
    @annotated(returns=float)
    def AddFloat2(A=(float, 0.0), B=(float, 0.0)):
        return A + B

    @staticmethod
    @annotated(returns=int)
    def AddInt2(A=(int, 0), B=(int, 0)):
        return A + B
