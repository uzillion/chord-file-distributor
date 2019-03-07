import hashlib as h
M = 20
main_func = 'sha512'

def sha1(key):
  return int(h.sha1(key.encode()).hexdigest(), 16) %  2**M

def sha256(key):
  return int(h.sha256(key.encode()).hexdigest(), 16) %  2**M

def sha512(key):
  return int(h.sha512(key.encode()).hexdigest(), 16) %  2**M

def hash_(key):
  return abs(hash(key)) % 2**M

hash_funcs = {
  'sha1': sha1,
  'sha256': sha256,
  'sha512': sha512,
  'hash_': hash_
}
