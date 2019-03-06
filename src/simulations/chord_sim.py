import hashlib as h
from pprint import pprint
import math

M = 10

nodes = {
  "47.183.149.48:2736": {
    'f_table': [],
    'vals': []
  },
  "159.49.60.84:2736": {
    'f_table': [],
    'vals': []
  },
  "121.114.71.138:2736": {
    'f_table': [],
    'vals': []
  },
  "38.190.106.117:2736": {
    'f_table': [],
    'vals': []
  },
  "19.184.86.55:2736": {
    'f_table': [],
    'vals': []
  },
  "186.98.81.169:2736": {
    'f_table': [],
    'vals': []
  },
  "135.101.68.198:2736": {
    'f_table': [],
    'vals': []
  },
  "167.121.54.141:2736": {
    'f_table': [],
    'vals': []
  }
}

ring = []

def getHash(key, h_func = 1):
  if h_func == 1:
    return str(int(''.join(format(ord(x), 'b') for x in h.sha1(key.encode()).hexdigest())[:M], 2))
  elif h_func == 2:
    return str(int(''.join(format(ord(x), 'b') for x in h.sha256(key.encode()).hexdigest())[:M], 2))

def findSuccessor(ref, current = math.floor(len(ring)/2)):
  if current in range(0, len(ring)):
    if ref == ring[current]:
      return ring[current]

    elif ref < ring[current]:
      if current != 0:
        return findSuccessor(ref, current-1)
      else:
        return ring[current]

    elif ref > ring[current]:
      if (current + 1) < len(ring) and ref <= ring[current+1]:
        return ring[current+1]
      else:
        return findSuccessor(ref, current+2)
  else:
      return ring[0]

# i: int, n_id: int
def getSuccessor(i, n_id):
  ref = (n_id + pow(2, i)) % pow(2, M)
  return findSuccessor(ref)

addr_table = {}
visited = {}

files = ["image", "document", "pdf", "tax", "music", "videos", "project", "code", "show", "movie", "wallpaper", "file", "RAR", "zip", "c", "cpp"]

for n in nodes:
  n_id = getHash(n)
  addr_table[n_id] = n
  ring.append(int(n_id))

ring.sort()
print(ring)

for n in ring:
  for i in range(0, M):
    successor = getSuccessor(i, n)
    if successor == n:
      break
    else:
      nodes[addr_table[str(n)]]['f_table'].append(successor)

this_node = ring[0]
iterations = 0

# f_id: int, this: int, peer_id: int, f_table: List
def isPredecessor(f_id, this, peer_id, f_table):
  if (this < f_table[peer_id] and f_table[peer_id] < f_id) or \
     (this < f_table[peer_id] and f_id < this) or \
     (f_table[peer_id] < f_id and f_id < this):
      return True
  else:
      return False
  
# f_id: str, current: str
def findNode(f_id, current = str(this_node)):
  global iterations
  iterations = iterations + 1
  if f_id == current:
    return current
  else:
    visited[current] = 1
    f_table = nodes[addr_table[current]]['f_table']
    i = len(f_table)
    while i > 0:
      i = i - 1
      if isPredecessor(int(f_id), int(current), i, f_table):
        return findNode(f_id, str(f_table[i]))
      if f_id == f_table[i]:
        return str(f_table[i])

    return str(f_table[0])

print('==================================================')
for f in files:
  h_func = 1
  for i in range(0,2):
    iterations = 0
    visited = {}
    f_id = getHash(f, h_func)
    node = addr_table[findNode(f_id)]
    nodes[node]['vals'].append(f)
    print('file:', f_id, ', node:', getHash(node), ', found in', iterations, 'steps')
    h_func = 2

print('==================================================')
pprint(addr_table)

print('==================================================')
for n in nodes:
  print(n, nodes[n]['vals'])

print('==================================================')
for n in nodes:
  print(getHash(n), nodes[n]['f_table'])
