# Raft server log.
class Log:
    def __init__(self):
        self.entries = []  # list of instances of LogEntry
        # Put dummy entry at zeroth index. TODO: is this good idea?
        self.entries.append(self.Entry(0,None))

    class Entry:
        def __init__(self, term, command):
            self.term = term  # term in which created
            self.command = command  # command for state machine
            self.is_committed = False  # TODO: is this needed?

    def get(self, index):
        assert(index >= 0)
        return self.entries[index]

    # Returns latest entry.
    def latest(self):
        return self.entries[-1]

    def size(self):
        return self.len()
    def length(self):
        return self.len()
    def len(self):
        return len(self.entries)

    def append(self, term, command):
        self.entries.append(self.Entry(term, command))
