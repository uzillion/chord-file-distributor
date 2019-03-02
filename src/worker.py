from threading import Thread
from address import Address
import socket
import sys
M = 20

def in_range(a, b, c, start=False, end=False):
  bla = None
  alc = None
  if start:
    bla = b <= a
  else:
    bla = b < a

  if end:
    alc = a <= c
  else:
    alc = a < c

  if b < c:
	  return bla and alc
  return bla or alc

def get_hash(str):
    return int( bin( hash(str) )[:M], 2)

class Worker(Thread):
  def __init__(self, peer, state):
    super().__init__()
    self.conn = peer[0]
    self.peer_addr = peer[1]
    self.state = state

  
  def run(self):
    data = self.conn.recv(1024)
    # print(data)
    request = data.decode('utf-8').split(' ')
    print(request)
    if request[0] == 'exit':
      sys.exit(0)
    try:
      getattr(self, request[0])(*request[1:])
    except Exception as e:
      print('Invalid function')
      raise TypeError('Crashed')
    finally:
      self.conn.close()

  def send(self, remote_addr, data):
    ip, port = remote_addr.ip, remote_addr.port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.sendall(data.encode())
    return s

  def ping(self):
    print('ping called')
    self.conn.sendall('Runing on {}:{}'.format(self.state.ip, self.state.port).encode())

  def create_ring(self):
    self.state.successor = self.state.local_address
    self.state.finger.insert(0, self.state.local_address.__hash__())
    self.state.addr_dict[str(self.state.finger[0])] = self.state.local_address

  def join(self, ip, port):
    print('joining {}:{}'.format(ip, port))
    try:
      s = self.send(Address(ip, port), 'find_successor {} {}'.format(self.state.ip, self.state.port))
      data = s.recv(1024).decode('utf-8')
      successor_ip, successor_port = data.split(':')
      self.state.successor = Address(successor_ip, successor_port)
      self.state.finger.insert(0, self.state.successor.__hash__())
      self.state.addr_dict[str(self.state.finger[0])] = self.state.successor
      print('successor found to be {}:{}'.format(successor_ip, successor_port))
      s.close()
      # self.stabilize()
    except Exception as e:
      print("Error sending request")
      raise TypeError('Ha!')
      # print(e)

  def get_successor(self):
    self.conn.sendall('{}:{}'.format(self.state.successor.ip, self.state.successor.port).encode())

  def get_predecessor(self):
    self.conn.sendall('{}:{}'.format(self.state.predecessor.ip, self.state.predecessor.port).encode())

  def find_successor(self, ip=None, port=None):
    id = get_hash('{}:{}'.format(ip, port))
    if in_range(id, self.state.local_address.__hash__(), self.state.finger[0], end=True):
      n_ = self.state.finger[0]
      n_ip = self.state.addr_dict[str(n_)].ip
      n_port = self.state.addr_dict[str(n_)].port
      self.conn.sendall('{}:{}'.format(n_ip, n_port).encode())
    else:
      n_ = self.closest_preceding_node(id)
      n_ip = self.state.addr_dict[str(n_)].ip
      n_port = self.state.addr_dict[str(n_)].port
      s = self.send(Address(n_ip, n_port), 'find_successor {} {}'.format(ip, port))
      self.conn.sendall(s.recv(1024))

  def closest_preceding_node(self, id):
    for i in range(M, 0, -1):
      if in_range(self.state.finger[i], self.state.local_address.__hash__(), id):
        return self.state.finger[i]
    return self.state.local_address.__hash__()

  def stabilize(self):
    s = self.send(self.state.successor, 'get_predecessor')
    x_ip, x_port = s.recv(1024).decode('utf-8').split(':')
    s.close()
    x = Address(x_ip, x_port)
    if in_range(x.__hash__(), self.state.local_address.__hash__(), self.state.successor.__hash__()):
      self.state.successor = x
    self.send(self.state.successor, 'notify {} {}'.format(self.state.ip, self.state.port))

  def notify(self, ip, port):
    n_ = Address(ip, port)
    if self.state.predecessor == None or\
       in_range(n_.__hash__(), self.state.predecessor.__hash__(), self.state.local_address.__hash__()):
      self.state.predecessor = n_   

  def fix_finger(self):
    self.state.lock.acquire()
    self.state.i = self.state.i + 1
    if self.state.i > M:
      self.state.i = 1
    # s = self.send(self.state.local_address, 'find_successor {}'.format
    

  def distribute(self, file):
    pass


