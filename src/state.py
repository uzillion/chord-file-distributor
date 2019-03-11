import socket
from address import Address
from threading import Lock
from utils import M

class State:
  def __init__(self, port=8000):
    self.in_ring = False  # becomes True when this node has created or joined a ring
    self.ip = socket.gethostbyname(socket.gethostname())
    self.port = port
    self.local_address = Address(self.ip, self.port)
    self.id = self.local_address.__hash__()
    self.predecessor = None
    self.successor = None
    self.finger = [None]*M  # contains finger nodes' Chord ids
    self.addr_dict = {}  # key: a Chord id; value: corresponding Address (IP/port) 
    self.i = 1
    self.lock = Lock()
