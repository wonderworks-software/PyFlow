from AGraphPySide import Command


class notify(Command.Command):

    def __init__(self, graph):
        super(notify, self).__init__(graph)

    def usage(self):

        msg = """[USAGE] {0} ~text str ~duration int""".format(self.__class__.__name__)
        return msg

    def execute(self, line):
        commandLine = self.parse(line)
        try:
            text = commandLine["~text"]
            duration = int(commandLine["~duration"])
            self.graph.notify(text, duration)
        except Exception as e:
            print("[ERROR] {0}".format(e))
            print(self.usage())
            self.graph.write_to_console(self.usage(), True)
