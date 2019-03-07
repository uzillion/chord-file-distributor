# Classes for testing RaftServer implementation.

class StateMachine:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0

    # Direction to edit state machine.
    class Command:
        # @command should be a string of the format "x = y",
        # where x is the StateMachine variable to
        # assign to, and y is the value to assign.
        def __init__(self, content):
            self.content = content

    def applyCommand(self, command):
        # Determine the assignment.
        tokens = command.content.split()
        varToEdit = tokens[0]
        valueToAssign = int(tokens[2])
        # Perform the assignment.
        self.__dict__[varToEdit] = valueToAssign
