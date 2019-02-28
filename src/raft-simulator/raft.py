from enum import Enum
from threading import Thread
import time

# Defined by me.
from state_machine import StateMachine
from log import Log

# TODO: remove this class
class Temp:
    NUM_SERVERS = 5
    HEARTBEAT_PERIOD = 1  # in seconds
    servers = []

# Represents a request from a client.
class Request:
    def __init__(self, command):
        self.command = command  # says how to change the state machine

# Public API:
#   __init__(): (constructor) 
#   handle_request()
class RaftServer:
    def __init__(self, id):
        self.id = id  # unique id for this RaftServer
        
        self.state_machine = StateMachine()

        # Persistent state on a server.
        self.current_term = 0
        self.voted_for = None  # candidate_id that received vote
                               # in current term
        self.log = Log()

        # Volatile state on a server.
        self.commit_index = 0   # index of highest log entry known
                                # to be committed
        self.last_applied = 0   # index of highest log entry applied
                                # to state machine

        # Volatile state on a leader.
        # (Reinitialized after election.)
        # for each server, index of next log
        # entry to send to that server:
        self.next_index = []
        # for each server, index of highest
        # log entry known to be replicated on server:
        self.match_index = []
        
        self.state = self.State.FOLLOWER

        # Start heartbeat thread.
        self.heartbeat_thread = Thread(target=self.__send_heartbeat)
        self.heartbeat_thread.start()

    class State(Enum):
        FOLLOWER = 1
        CANDIDATE = 2
        LEADER = 3

    # For heartbeat thread.
    # If leader, sends heartbeat to all followers,
    # then wait until must send next heartbeat.
    def __send_heartbeat(self):
        while True:
            if self.state == self.State.LEADER:
                # for each follower
                    # send empty AppendEntries RPC
                print("u make mah heart beat")
                time.sleep(Temp.HEARTBEAT_PERIOD)

    # Called if no communication from leader and
    # election timeout reached.
    def __start_election(self):
        self.current_term += 1
        # self.voted_for = # what is my id?
        # reset election timer
        # send Requestvote RPCs to all other servers

    def __become_leader(self):
        self.state = RaftServerState.LEADER
        initial_next_index = self.last_applied + 1
        self.next_index = [initial_next_index] * Temp.NUM_SERVERS
        self.match_index = [0] * Temp.NUM_SERVERS

    def __handle_request(self, request):
        self.log.append(self.current_term, request.command)

    # Used to receive request from client.
    # @request must be instance of Request.
    def handle_request(self, request):
        if self.state == RaftServerState.LEADER:
            self.__handle_request(request)
        else:
            pass  # redirect to leader

    # Invoked by the leader on other raft servers to replicate
    # log entries. Also used as a heartbeat.
    # Simulates an RPC.
    # Output: tuple (@term, @success), where @term is the
    # current term, and @success indicating success (boolean).
    def append_entries_RPC(term, leader_id, prev_log_index,
                           prev_log_term, entries,
                           leader_commit):
        if self.id == leader_id:  # if leader sent RPC to itself
            raise AssertionError("Leader sent AppendEntries RPC to itself")

        if term < current_term:
            return (self.current_term, False)
        if (len(self.log) <= prev_log_index
            or self.log[prev_log_index].term != prev_log_term):
            return (self.current_term, False)
        # TODO: #3 and 4 and 5
        # if leader_commit > self.commit_index:
            # self.commit_index = min(leader_commit, (index of last new entry))
        
        return (self.current_term, True)

    # TODO: remove
    def make_leader(self):
        self.state = self.State.LEADER
    def make_follower(self):
        self.state = self.State.FOLLOWER

def test_run():
    for i in range(Temp.NUM_SERVERS):
        Temp.servers.append(RaftServer(i))
