import socket
from address import Address
from threading import Lock

lock = Lock()

class State:
  def __init__(self, port=8000):
    self.ip = socket.gethostbyname(socket.gethostname())
    self.port = port
    self.predecessor = None
    self.successor = None
    self.finger = []
    self.addr_dict = {}
    self.local_address = Address(self.ip, self.port)
