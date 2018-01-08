def BKDRHash1(key):
    seed = 131 # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
      hash = (hash * seed) + ord(key[i])
    return hash

def BKDRHash2(key):
    seed = 1313 # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
      hash = (hash * seed) + ord(key[i])
    return hash

def BKDRHash3(key):
    seed = 13131 # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
      hash = (hash * seed) + ord(key[i])
    return hash

def BKDRHash4(key):
    seed = 131313 # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
      hash = (hash * seed) + ord(key[i])
    return hash

def BKDRHash5(key):
    seed = 1313131 # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
      hash = (hash * seed) + ord(key[i])
    return hash

def putData(Hash, i, m):
    Hash[BKDRHash1(str(i)) % m] = 1
    Hash[BKDRHash2(str(i)) % m] = 1
    Hash[BKDRHash3(str(i)) % m] = 1
    Hash[BKDRHash4(str(i)) % m] = 1
    Hash[BKDRHash5(str(i)) % m] = 1

def isInHash(HashList, i, m):
    return (HashList[BKDRHash1(str(i)) % m] and HashList[BKDRHash2(str(i)) % m] and HashList[BKDRHash3(str(i)) % m] and HashList[BKDRHash4(str(i)) % m] and HashList[BKDRHash5(str(i)) % m])
