from AGraphPySide import Command
from AbstractGraph import FLAG_SYMBOL

class helloWorld(Command.Command):

    def __init__(self, graph):
        super(helloWorld, self).__init__(graph)

    def usage(self):

        msg = """[USAGE] {0} {1}text str""".format(self.__class__.__name__, FLAG_SYMBOL)
        return msg

    def execute(self, line):
        commandLine = self.parse(line)
        try:
            self.graph.write_to_console(commandLine["{0}text".format(FLAG_SYMBOL)])
        except Exception, e:
            print "[ERROR] {0}".format(e)
            print self.usage()
