from AGraphPySide import Command


class enableShadows(Command.Command):

    def __init__(self, graph):
        super(enableShadows, self).__init__(graph)

    def usage(self):

        return "[USAGE] enableShadows ~state [0|1]"

    def execute(self, line):
        commandLine = self.parse(line)
        try:
            state = int(commandLine["~state"])
            self.graph.set_shadows_enabled(state)
        except Exception as e:
            print(self.usage())
