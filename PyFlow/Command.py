"""
base class for all commands. Use this to implement your own
"""

import re
from AbstractGraph import FLAG_SYMBOL


class Command(object):

    def __init__(self, graph):
        super(Command, self).__init__()
        self.graph = graph
        self.flags = []

    def flags(self):
        return self.flags

    def parse(self, line):
        '''
        returns - {'cmd': command, 'flags': {-x1: 50, -x2: 100}}
        '''
        flags = {}
        dashes = [m.start() for m in re.finditer(FLAG_SYMBOL, line)]
        for i in xrange(len(dashes) - 1):
            newLine = line[dashes[i]:]
            newLineDashes = [m.start() for m in re.finditer(FLAG_SYMBOL, newLine)]
            flag = newLine[:newLineDashes[1] - 1].split(" ", 1)  # flag + value
            flags[flag[0]] = flag[1]
        flag = line[dashes[-1]:].split(" ", 1)  # last flag + value
        flags[flag[0]] = flag[1]
        return flags

    def usage(self):

        msg = """[USAGE] none"""
        return msg

    def execute(self, line):
        pass
