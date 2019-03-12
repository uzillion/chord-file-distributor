#!/usr/local/bin/python
import socket
from worker import Worker
from maintenance import Maintenance
from state import State
import sys
import os
import subprocess

class Node:
    # ip = socket.gethostbyname(socket.gethostname())
    # port = port
    # predecessor = None
    # successor = None
    # finger = []
    # addr_dict = {}
    # local_address = Address(ip, port)

  def start(port=8000):
    os.environ['PORT'] = str(port)
    state_ = State(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((state_.ip, port))
    s.listen()
    print('Listening on {}:{}'.format(state_.ip, port))

    # Start maintenance thread.
    Maintenance(Worker([None,None], state_, False)).start()

    while True:
      peer = s.accept()
      Worker(peer, state_).start()


    s.close()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    Node.start(int(sys.argv[1]))
  else:
    Node.start(8000)
