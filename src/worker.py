from threading import Thread
from address import Address, hash_
from config import M
import socket
import sys
import time
import hashlib as h
import os

CACHE_DIR = './cache'

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
      # self.conn.sendall('Exiti')
      sys.exit(0)
    try:
      response = getattr(self, request[0])(*request[1:])
      if not response:
        response = 'Operation Completed Successfully'
      self.conn.sendall(response.encode())
    except:
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
    return 'Runing on {}:{}'.format(self.state.ip, self.state.port)

  def create_ring(self):
    self.state.successor = self.state.local_address
    # self.state.predecessor = self.state.local_address
    self.state.finger[0] = self.state.id
    self.state.addr_dict[str(self.state.finger[0])] = self.state.local_address
    return "New ring created"

  def join(self, ip, port):
    print('joining {}:{}'.format(ip, port))
    try:
      s = self.send(Address(ip, port), 'find_successor {}'.format(self.state.id))
      data = s.recv(1024).decode('utf-8')
      successor_ip, successor_port = data.split(':')
      self.state.lock.acquire()
      self.state.successor = Address(successor_ip, successor_port)
      self.state.finger[0] = self.state.successor.__hash__()
      self.state.addr_dict[str(self.state.finger[0])] = self.state.successor
      self.state.lock.release()
      s.close()
      self.stabilize()
      # self.state.predecessor = Address(successor_ip, successor_port)
      # self.send(self.state.predecessor, 'stabilize').close()
      return 'successor found to be {}:{}'.format(successor_ip, successor_port)
    except:
      raise Exception()
    finally:
      return "Error sending request to server"
      # print(e)

  def get_successor(self):
    return '{}:{}'.format(self.state.successor.ip, self.state.successor.port)

  def get_predecessor(self):
    try:
      return '{}:{}'.format(self.state.predecessor.ip, self.state.predecessor.port)
    except:
      return 'None'

  def get_hash(self, str_=None):
    if str_ != None:
      return str(hash_(str))
    return str(self.state.id)

  def find_successor(self, id):
    id = int(id)
    if in_range(id, self.state.id, self.state.finger[0], end=True):
      n_ = self.state.finger[0]
      n_ip = self.state.addr_dict[str(n_)].ip
      n_port = self.state.addr_dict[str(n_)].port
      return '{}:{}'.format(n_ip, n_port)
    else:
      n_ = self.closest_preceding_node(id)
      n_ip = self.state.addr_dict[str(n_)].ip
      n_port = self.state.addr_dict[str(n_)].port
      s = self.send(Address(n_ip, n_port), 'find_successor {}'.format(id))
      return s.recv(1024).decode('utf-8')

  def closest_preceding_node(self, id):
    for i in range(M-1, 0, -1):
      # Lazy check. 
      # Should implement a pointer to point to the last entry in table
      if self.state.finger[i]:
        if in_range(self.state.finger[i], self.state.id, id):
          return self.state.finger[i]
    return self.state.id

  def stabilize(self):
    try:
      s = self.send(self.state.successor, 'get_predecessor')
      x_ip, x_port = s.recv(1024).decode('utf-8').split(':')
      s.close()
      x = Address(x_ip, x_port)
      if in_range(x.__hash__(), self.state.id, self.state.successor.__hash__()):
        self.state.lock.acquire()
        self.state.finger[0] = x.__hash__()
        self.state.successor = x
        self.state.addr_dict[str(x.__hash__())] = x
        self.state.lock.release()
    except: pass
    self.send(self.state.successor, 'notify {} {}'.format(self.state.ip, self.state.port)).close()

  def notify(self, ip, port):
    n_ = Address(ip, port)
    if self.state.predecessor == None or\
       in_range(n_.__hash__(), self.state.predecessor.__hash__(), self.state.id):
      self.state.lock.acquire()      
      self.state.predecessor = n_
      self.state.lock.release()   

  def fix_finger(self):
    self.state.lock.acquire()
    self.state.i = self.state.i + 1
    if self.state.i > M:
      self.state.i = 1
    s = self.send(self.state.local_address, 'find_successor {}'.format((self.state.id + pow(2, self.state.i-1)) % 2**M))
    n_ip, n_port = s.recv(1024).decode('utf-8').split(':')
    n = Address(n_ip, n_port)
    s.close()
    self.state.addr_dict[str(n.__hash__())] = n
    self.state.finger[self.state.i-1] = n.__hash__()
    print("Finger:", self.state.finger)
    self.state.lock.release()

  def check_predecessor(self):
    try:
      s = send(self.state.predecessor, 'ping')
      response = s.recv(1024)
      if not response[:7] == 'Running':
        print("Failed to get response from predecessor")
        self.state.predecessor = None
    except:
      print("Failed to get response from predecessor")
      self.state.predecessor = None

  def return_segment(self, seg_name):
    seg_size = os.stat('{}/{}'.format(CACHE_DIR, seg_name)).st_size
    self.conn.sendall(str(seg_size).encode())
    ready = self.conn.recv(1024).decode('utf-8')
    print(ready)
    if ready == 'READY':
      f = open('{}/{}'.format(CACHE_DIR, seg_name), 'rb')
      # print(f)
      self.conn.sendfile(f, offset=0, count=seg_size)
    

      
  def store(self, seg_name, n_bytes):
    self.conn.sendall('OK'.encode())
    chunk = 0
    data = self.conn.recv(8 * 1024)
    while True:
      data += self.conn.recv(8 * 1024)
      chunk = len(data)
      if chunk == int(n_bytes):
        break
    print('file recieved')
    self.conn.sendall(str(len(data)).encode())
    print('writing file')
    f = open('{}/{}'.format(CACHE_DIR, seg_name), 'wb+')
    f.write(data)
    print('file written')
    f.close()

  def get_finger(self):
    return str(self.state.finger)

  def send_segment(self, file_, seg_id, start, n_bytes):
    seg_name = '{}_{}'.format(file_.split('/')[-1:][0], seg_id)
    ip, port = self.find_successor(hash_(seg_name)).split(':')
    s = self.send(Address(ip, port), 'store {} {}'.format(seg_name, n_bytes))
    if s.recv(512).decode('utf-8') == 'OK':
      f = open(file_, 'rb+')
      print("sending file...")
      s.sendfile(f, int(start), int(n_bytes))
      print("waiting for ack...")
      data = s.recv(1024).decode('utf-8')
      print('ack received')
      s.close()
      f.close()
      return 'segment {}: {} bytes sent, {} recieved'.format(seg_id, n_bytes, data)
    else:
      s.close()
      return 'Error sending segment {} to {}:{}'.format(seg_id, ip, port)

  def pull(self, file_):
    f = open(file_, 'r')
    file_meta = []
    for line in f:
      file_meta.append(line)
    f.close()
    name = file_meta[0].replace('\n', '')
    size = int(file_meta[1].replace('\n', ''))
    n_segments = int(file_meta[2].replace('\n', ''))
    data = ''.encode()
    chunk = ''.encode()
    for i in range(0, n_segments):
      seg_name = name + '_' + str(i)
      ip, port = self.find_successor(hash_(seg_name)).split(':')
      s = self.send(Address(ip, port), 'return_segment {}'.format(seg_name))
      seg_size = int(s.recv(1024).decode('utf-8'))
      print('seg_size:', seg_size)
      s.sendall('READY'.encode())
      # chunk = s.recv(seg_size)
      # ========= Chunked download downloading extra bytes; 1 byte at time too slow ========#
      while True:
        # print(len(data))
        chunk += s.recv(1)
        # chunk += s.recv(8 * 1024)
        if len(chunk) >= seg_size:
          break
      #====================================================================================#
      data += chunk
      print('{}: {}/{} bytes recieved'.format(seg_name, len(chunk), seg_size))
      chunk = b''
      # chunk = len(data)
      s.close()
    
    if len(data) == size:
      f = open(name, 'wb+')
      f.write(data)
      f.close()
      return 'File pulled successfully'
    else:
      return 'Failed to pull file'
    # print(file_meta)
    


