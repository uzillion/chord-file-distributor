#!/usr/bin/python3
import subprocess
import os
import sys
import socket
# from address import Address

LOCAL_IP = socket.gethostbyname(socket.gethostname())
# LOCAL_PORT = 8000

if not os.path.isfile('./split'):
  subprocess.run(['make', 'all'])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

request = sys.argv[1]
LOCAL_PORT = int(sys.argv[2])
args  = sys.argv[3:]
print(len(args))


def generic_reqest(msg):
  if len(args) > 2:
    s.connect((args[0], args[1]))
    s.sendall('{} {} {}'.format(msg, LOCAL_IP, LOCAL_PORT).encode())
  elif len(args) == 0:
    s.connect((LOCAL_IP, LOCAL_PORT))
    s.sendall('{} {} {}'.format(msg, LOCAL_IP, LOCAL_PORT).encode())
  s.close()

if request == 'join':
  s.connect((LOCAL_IP, LOCAL_PORT))
  if len(args) > 1:
    print('join {} {}'.format(args[0], args[1]).encode())
    s.sendall('join {} {}'.format(args[0], args[1]).encode())
  elif len(args) == 0:
    s.sendall('create_ring'.encode())
  s.close()
elif request == 'stabilize':
  generic_reqest('stabilize')

    

