from threading import Thread
from address import Address
import socket
from state import lock
import sys
M = 20

def in_range(a, b, c, start=False, end=True):
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

  def send(self, ip, port, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.sendall(data.encode())
    return s

  def create_ring(self):
    self.state.successor = self.state.local_address
    self.state.finger.insert(0, self.state.local_address.__hash__())
    self.state.addr_dict[str(self.state.finger[0])] = self.state.local_address

  def join(self, ip, port):
    print('joining {}:{}'.format(ip, port))
    try:
      s = self.send(ip, port, 'find_successor {} {}'.format(self.state.ip, self.state.port))
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

  def find_successor(self, ip, port):
    id = get_hash('{}:{}'.format(ip, port))
    if in_range(id, self.state.local_address.__hash__(), self.state.finger[0]):
      n_ = self.state.finger[0]
      n_ip = self.state.addr_dict[str(n_)].ip
      n_port = self.state.addr_dict[str(n_)].port
      self.conn.sendall('{}:{}'.format(n_ip, n_port).encode())
    else:
      n_ = self.closest_preceding_node(id)
      n_ip = self.state.addr_dict[str(n_)].ip
      n_port = self.state.addr_dict[str(n_)].port
      s = self.send(n_ip, n_port, 'find_successor {} {}'.format(ip, port))
      self.conn.sendall(s.recv(1024))

  def closest_preceding_node(self, id):
    for i in range(M, 0, -1):
      if in_range(self.state.finger[i], self.state.local_address.__hash__(), id, end=False):
        return self.state.finger[i]
    return self.state.local_address.__hash__()

  # def stabilize(self):
  #   try:
  #     s = self.send(self.successor, 'get_predecessor')
  #     ip, port = s.recv(1024).decode('utf-8').split(':')
  #     x = Address(ip, port)
  #     if in_range(x.__hash__(), self.local_address.__hash__(), self.successor.__hash__()):
  #       self.successor = x
  #     s.sendall('notify {} {}'.format(self.local_address.ip, self.local_address.port).encode())
  #   except Exception as e:
  #     print("Error sending request")
  #     print(e)
  #   finally:
  #     s.close()

  # def get_predecessor

  def notify(self, ip, port):
    pass
  
  def distribute(self, file):
    pass

  def refreshFingerTable(self):
    pass

