#!/usr/local/bin/python
import subprocess
import os
import sys
import socket
from address import Address
# from address import Address

LOCAL_IP = socket.gethostbyname(socket.gethostname())
LOCAL_PORT = int(os.environ['PORT'])
print('For {}:{}'.format(LOCAL_IP, LOCAL_PORT))

if not os.path.isfile('./split'):
  subprocess.run(['make', 'all'])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

request = sys.argv[1]
# LOCAL_PORT = int(sys.argv[2])
args  = sys.argv[2:]
# print(len(args))

def local_request(msg, arg1=None, arg2=None):
  s.connect((LOCAL_IP, LOCAL_PORT))
  s.sendall('{} {} {}'.format(msg, arg1, arg2).encode())
  data = s.recv(1024).decode('utf-8')
  print(data)

def local_request_s(msg):
  s.connect((LOCAL_IP, LOCAL_PORT))
  s.sendall(msg.encode())
  data = s.recv(1024).decode('utf-8')
  print(data)

def remote_request(msg, dest_ip=None, dest_port=None, arg1=None, arg2=None):
  if dest_ip != None and dest_port != None:
    s.connect((dest_ip, int(dest_port)))
    s.sendall('{} {} {}'.format(msg, arg1, arg2).encode())
    data = s.recv(1024).decode('utf-8')
    print(data)
  else:
    print("Missing ip/port")

def remote_request_s(msg, dest_ip=None, dest_port=None):
  if dest_ip != None and dest_port != None:
    s.connect((dest_ip, dest_port))
    s.sendall(msg.encode())
    data = s.recv(1024).decode('utf-8')
    print(data)
  else:
    print("Missing ip/port")

def join_(ip=None, port=None):
  s.connect((LOCAL_IP, LOCAL_PORT))
  print('join {} {}'.format(ip, port).encode())
  s.sendall('join {} {}'.format(ip, port).encode())
  
if request == 'join':
  if len(args) > 1:
    local_request('join', args[0], args[1])
  elif len(args) == 0:
    local_request_s('create_ring')

elif request == 'stabilize':
  if len(args) > 1:
    remote_request_s(request, args[0], args[1])
  elif len(args) == 0:
    local_request_s('stabilize')

elif request == 'ping':
  if len(args) > 1:
    remote_request_s('ping', args[0], args[1])
  elif len(args) == 0:  
    local_request_s('ping')

# elif request == 'get_hash':
#   if len(args) > 1:
#     print(Address(args[0], args[1]).__hash__())
#   elif len(args) == 0:  
#     print(Address(LOCAL_IP, LOCAL_PORT).__hash__())

elif request[:4] == 'get_':
  if len(args) > 1:
    remote_request_s(request, args[0], args[1])
  elif len(args) == 0:
    local_request_s(request)

else:
  print("Invalid Request, please select one of the following:")
  print("\t-> ping")
  print("\t-> join")
  print("\t-> stabilize")
  print("\t-> get_successor")
  print("\t-> get_predecessor")
  print("\t-> get_hash")
  


s.close()
    

