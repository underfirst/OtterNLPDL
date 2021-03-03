from abc import ABC


class CommandMeta(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def exec(self):
        pass


class CommandPipeline:
    def __init__(self):
        self.commands = list()

    def add(self, command):
        self.commands.append(command)

    def exec(self):
        for command in self.commands:
            print(command.__class__.__name__)
            command.exec()
