from PyFlow.Core.Common import *


class Connection(object):
    def __init__(self, lhs, rhs):
        super(Connection, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
