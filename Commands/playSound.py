from AGraphPySide import Command
import winsound
from threading import Thread


class playSound(Command.Command):

    def __init__(self, graph):
        super(playSound, self).__init__(graph)

    def usage(self):

        return "[USAGE] playSound ~file [absolute file path]"

    def execute(self, line):
        commandLine = self.parse(line)
        try:
            t = Thread(target=lambda: winsound.PlaySound(commandLine["~file"], winsound.SND_FILENAME))
            t.start()
        except Exception as e:
            print(self.usage())
            print(e)
