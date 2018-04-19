import argparse

class Command:
    def __init__(self, name, help=None):
        self.name = name
        self.help = help
        
    def add_subparser(self, subparsers):
        self.parser = subparsers.add_parser(self.name, help=self.help)
        self.add_arguments()
        return self.parser

    def add_arguments(self):
        # Method must be implemented to setup the Command
        raise NotImplementedError

    def run(self, args, parser):
        # Method must be implemented to run the Command
        raise NotImplementedError


class Commander:

    def __init__(self, *commands):
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers(help="Commands", dest="cmd")
        self.commands = {}

        # Load commands if given
        if (commands != None and len(commands) > 0): self.load(*commands)

    def load(self, *commands):
        # Load the commands keys and their parsers
        for cmd in commands:
            if (isinstance(cmd, type)): cmd = cmd()
            if (not isinstance(cmd, Command)): raise TypeError("Given value is not of type 'Command'")
            self.commands[cmd.name] = cmd.run
            cmd.add_subparser(self.subparsers)
        
    def run(self, args=None):
        # Parse and determine which command to run
        self.args = self.parser.parse_args(args)
        run = self.commands.get(
            self.args.cmd, 
            lambda *_: self.parser.print_help())
        run(self.args, self.parser)

