class HashTable:
    def __init__(self):
        self.size = 10
        self.hashmap = [[] for _ in range(0, self.size)]

    def hashing_func(self, key):
        hashed_key = hash(key) % self.size
        return hashed_key

    def set(self, key, value, value2, value3):
        hash_key = self.hashing_func(key)
        key_exists = False
        slot = self.hashmap[hash_key]
        for i, kvwx in enumerate(slot):
            k, v, w, x = kvwx
            if key == k:
                key_exists = True
                break

        if key_exists:
            slot[i] = ((key, value, value2, value3))
        else:
            slot.append((key, value, value2, value3))

    def get(self, key):
        hash_key = self.hashing_func(key)
        slot = self.hashmap[hash_key]
        for i in range(0, len(slot)):
            if slot[i][0] == key:
                return slot[i]
            else:
                pass

        raise KeyError('La llave ingresada no existe.')

    def buscar(self, key):
        hash_key = self.hashing_func(key)
        slot = self.hashmap[hash_key]
        for j in range(0, len(slot)):
            if slot[j][0] == key:
                return True
        return False

    def __setitem__(self, key, value, value2, value3):
        return self.set(key, value, value2, value3)

    def __getitem__(self, key):
        return self.get(key)