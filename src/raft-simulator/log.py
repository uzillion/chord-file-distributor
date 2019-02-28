# Raft server log.
class Log:
    def __init__(self):
        self.entries = []  # list of instances of LogEntry

    class Entry:
        def __init__(self, term, command):
            self.term = term  # term in which created
            self.command = command  # command for state machine
            self.is_committed = False  # TODO: is this needed?

    def append(self, term, command):
        self.entries.append(self.Entry(term, command))
