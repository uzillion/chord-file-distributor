import hashlib as h
from pprint import pprint
import math

M = 10

'''
Virtual Nodes
f_table - Finger table
vals - segments held by the node
'''
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

def getHash(key):
  return str(int(''.join(format(ord(x), 'b') for x in h.sha1(key.encode()).hexdigest())[:M], 2))

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
    # if current < 0:
      return ring[0]
    # elif current >= len(ring):
      # return ring[len(ring) - 1]

# i: int, n_id: int
def getSuccessor(i, n_id):
  ref = (n_id + pow(2, i)) % pow(2, M)
  return findSuccessor(ref)

addr_table = {}
visited = {}

# virtual files
files = ["image", "document", "pdf", "tax", "music", "videos", "project", "code", "show", "movie", "wallpaper", "file", "RAR", "zip", "c", "cpp"]

# Creating a table mapping from hash to node ip:port, and then placing the node on the ring
for n in nodes:
  n_id = getHash(n);
  # print(int(n_id, 16))
  addr_table[n_id] = n
  ring.append(int(n_id))

ring.sort();
print(ring);
# print(pow(2, M))
# print(addr_table)

# Creating finger table for each node
for n in ring:
  # print(addr_table[str(n)])
  for i in range(0, M):
    successor = getSuccessor(i, n)
    if successor == n:
      break;
    else:
      nodes[addr_table[str(n)]]['f_table'].append(successor)

# Simulating as if the the file is being created in the node with hash value 780....
this_node = ring[0]

# Check if peer is predecessor to the key
# f_id: int, this: int, peer_id: int, f_table: List
def isPredecessor(f_id, this, peer_id, f_table):
  if peer_id in range(1, len(f_table)):
    prospective_prev_id = f_table[peer_id]
    tmp_f_id = f_id
    # 1)
    prospective_prev_id -= tmp_f_id
    tmp_f_id = 0
    # 2) 
    tmp_f_id += len(ring) - 1
    prospective_prev_id += len(ring) - 1
    # 3)
    tmp_f_id %= len(ring)
    prospective_prev_id %= len(ring)
    print("tmp_f_id: ", tmp_f_id)
    print("prospective_prev_id: ", prospective_prev_id)
    
    # if ((f_table[peer_id] < f_id and this < f_table[peer_id])\
    # or (f_table[peer_id] > f_id and f_table[len(f_table) - 1] < f_table[peer_id]))\
    # and (dict.get(visited, str(f_table[peer_id])) == None): # problematic when f_id: 844, this: 822, peer: 892
    if prospective_prev_id < tmp_f_id:
      print(visited)
      print(str(f_table[peer_id]))
      print(dict.get(visited, str(f_table[peer_id])))
      # print("returning", f_table[peer_id], "for", f_id)
      return True
    # elif f_table[peer_id] > f_id:

      '''Need to figure out how to manage when f_id is on the other side of the ring while peed_id is not'''
      # if f_table[peer_id-1] > f_id:
      #   return True
      # else:
        # return False
      # return False
    else:
      visited[str(f_table[peer_id])] = 1
      return False
  else:
    return False

# find the node that will ultimately hold the file
# f_id: str, current: str
def findNode(f_id, current = str(this_node)):
  # print("f_id:", f_id)
  # print("current:", current, addr_table[current])
  # print(int(f_id) == int(current))
  if f_id == current:
    return current
  else:
    visited[current] = 1
    f_table = nodes[addr_table[current]]['f_table']
    i = len(f_table)
    while i > 0:
      i = i - 1
      if isPredecessor(int(f_id), int(current), i, f_table):
        # print("jumping to node", f_table[i])
        return findNode(f_id, str(f_table[i]))
      if f_id == f_table[i]:
        return str(f_table[i])

    # print("f_table", f_table)
    # print("current", current)
    return str(f_table[0])

print('==================================================')
for f in files:
  visited = {} # A crude way to not mistake the nodes on the other side of 0 as predecessors
  f_id = getHash(f)
  # print("f_id:", f_id, f)
  node = addr_table[findNode(f_id)]
  # print("node", node)
  nodes[node]['vals'].append(f)
  print('file:', f_id, ', node:', getHash(node))

# for f in files:
#   f_key = getHash(f)
#   print("\n{}".format(int(f_key, 16)))
#   if f_key in addr_table:
#     nodes[addr_table[f_key]].append(f)
#   else:
#     f_key_n = int(f_key, 16)
#     neg = 0;
#     pos = pow(2, M);
#     for n in ring:
#       d = n - f_key_n
#       # print(d, neg, pos)
#       if d < neg:
#         neg = d
#       elif d < pos and d > 0:
#         pos = d
#     # print(neg, pos)
#     dest = f_key_n + neg if pos == pow(2, M) else f_key_n + pos
#     print("dest", dest)

#     nodes[addr_table[hex(dest)[2:]]].append(f)

print('==================================================')
pprint(addr_table)

# pprint(nodes)
print('==================================================')
for n in nodes:
  print(n, nodes[n]['vals'])

print('==================================================')
for n in nodes:
  print(getHash(n), nodes[n]['f_table'])
