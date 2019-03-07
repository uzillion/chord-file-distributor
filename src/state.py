import socket
from address import Address
from threading import Lock
from config import M

class State:
  def __init__(self, port=8000):
    self.ip = socket.gethostbyname(socket.gethostname())
    self.port = port
    self.predecessor = None
    self.successor = None
    self.finger = [None]*M
    self.addr_dict = {}
    self.local_address = Address(self.ip, self.port)
    self.id = self.local_address.__hash__()
    self.i = 1
    self.lock = Lock()
