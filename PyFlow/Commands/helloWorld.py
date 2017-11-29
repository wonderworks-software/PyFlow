import Command
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
            self.graph.write_to_console("HELLO WORLD! Your message: {0}".format(commandLine['~text']), True)
        except Exception as e:
            print("[ERROR] {0}".format(e))
            print(self.usage())
            self.graph.write_to_console(self.usage(), True)
