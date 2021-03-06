"""
Project 6
CSE 331 S21 (Onsay)
Your Name
hashtable.py
"""

from typing import TypeVar, List, Tuple

T = TypeVar("T")
HashNode = TypeVar("HashNode")
HashTable = TypeVar("HashTable")


class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key: str, value: T, deleted: bool = False) -> None:
        self.key = key
        self.value = value
        self.deleted = deleted

    def __str__(self) -> str:
        return f"HashNode({self.key}, {self.value})"

    __repr__ = __str__

    def __eq__(self, other: HashNode) -> bool:
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other: T) -> None:
        self.value += other


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity: int = 8) -> None:
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other: HashTable) -> bool:
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __str__(self) -> str:
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    __repr__ = __str__

    def _hash_1(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param key: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    def __len__(self) -> int:
        """
        Getter for size
        :return: size
        """
        return self.size

    def __setitem__(self, key: str, value: T) -> None:
        """
        DO NOT EDIT
        Allows for the use of the set operator to insert into table
        :param key: string key to insert
        :param value: value to insert
        :return: None
        """
        self._insert(key=key, value=value)

    def __getitem__(self, key: str) -> T:
        """
        DO NOT EDIT
        Allows get operator to retrieve a value from the table
        :param key: string key of item to retrieve from table
        :return: value associated with the item
        """
        if not self._get(key):
            raise KeyError
        return self._get(key).value

    def __delitem__(self, key: str) -> None:
        """
        Allows del operator to delete a value from the table
        :param key: the key of the item to remove from the table
        :return: None
        """
        if not self._get(key):
            raise KeyError
        self._delete(key)

    def __contains__(self, key: str) -> bool:
        """
        DO NOT EDIT
        Checks whether a given key exists in the table
        :param item: string key of item to retrieve
        :return: Bool
        """
        if self._get(key) is not None:
            return True
        return False

    def hash(self, key: str, inserting: bool = False) -> int:
        """
        Hash Method
        :param key: key to hash
        :param inserting: bool, are we inserting or not
        :return: hashed bin for table
        """
        # double hash until you find the right index
        index = self._hash_1(key)
        probe = 0
        ind = index
        node = self.table[index]

        # If I need to insert and this node has been deleted
        if node and node.deleted and inserting:
            return index

        # If I found the element with the key and it isnt deleted
        if node and not node.deleted and node.key == key:
            return index

        # If I found an element at the node that isn't the same key, I have a collision,
        # If it is None then I found the next available index
        while node is not None:
            if node and node.deleted and inserting:
                return index
            # If I found the element with the key return the index
            if node and not node.deleted and node.key == key:
                return index
            probe += 1  # Increment probe
            # New index is hash_1() + (p * hash_2()) % capacity
            index = (ind + probe * self._hash_2(key)) % self.capacity
            node = self.table[index]
        return index

    def _insert(self, key: str, value: T) -> None:
        """
        Insert key and value into HashTable
        :param key: string to be used as key value
        :param value: int to be used as value mapped to key
        """
        index = self.hash(key, inserting=True)

        # If the index is not invalid
        if index is not None:
            node = self.table[index]  # Get the node at that index

            # Found the node
            # If the node exists and the keys match, just update the value
            if node and node.key == key:
                node.value = value
            # Empty bin
            else:  # If it is an empty bin, then add a node to it
                self.table[index] = HashNode(key=key, value=value)
                self.size += 1

            if (self.size / self.capacity) >= 0.5:
                self._grow()

    def _get(self, key: str) -> HashNode:
        """
        Returns the hash node in the table based on the key
        :param key: key of hash node to find in hash table
        :return item: value in table if key exists, else None
        """
        index = self.hash(key)

        # If the key is valid
        if index is not None:
            node = self.table[index]
            if not node:  # The key does not exist in this case
                return None
            # Check if the index contains the correct key
            elif node.key == key:
                return node

        return None

    def _delete(self, key: str) -> None:
        """
        Delete a key from the dictionary
        :param key: the key we are deleting from the hash table
        :return: None
        """
        index = self.hash(key)

        # If the key is valid
        if index is not None:
            node = self.table[index]
            if not node:
                return
            # Check if the index contains the correct key
            # Create empty hashnode and set the deleted flag
            elif node.key == key:
                self.table[index] = HashNode(None, None, True)
                self.size -= 1

    def _grow(self) -> None:
        """
        Grow the table to double the capacity
        :return: None
        """
        old = self.table
        self.table = [None] * (self.capacity * 2)
        self.size = 0
        self.capacity *= 2

        j = self.prime_index
        while HashTable.primes[j] < self.capacity:
            j += 1
        self.prime_index = j - 1

        for i in old:
            if i and not i.deleted:
                self._insert(i.key, i.value)

    def update(self, pairs: List[Tuple[str, T]] = []) -> None:
        """
        Updates values in the hash table with an iterable of key value pairs. Inserts a new node if the value doesn't
        exist, or updates the existing value if it does
        :param pairs: an iterable of key/value pairs
        :return: None
        """
        for pair in pairs:
            key, value = pair
            self._insert(key, value)

    def keys(self) -> List[str]:
        """
        Creates a list of all the keys in the table
        :return: list of keys
        """
        return [node.key for node in self.table if node and not node.deleted]

    def values(self) -> List[T]:
        """
        Creates a list of all the values in the table
        :return: list of values
        """
        return [node.value for node in self.table if node and not node.deleted]

    def items(self) -> List[Tuple[str, T]]:
        """
        Creates a list of all the items in the table
        :return: list of items
        """
        return [(node.key, node.value) for node in self.table if node and not node.deleted]

    def clear(self) -> None:
        """
        Clears the hash table
        :return: None
        """
        for i in range(len(self.table)):
            self.table[i] = None
        self.size = 0


class CataData:
    def __init__(self) -> None:
        """
        Init for CataData
        """
        self.table = HashTable()
        self.current = HashTable()

    def enter(self, idx: str, origin: str, time: int) -> None:
        """
        Enter someone into the system
        :param idx: person ID
        :param origin: place getting on
        :param time: timestamp for getting on
        """
        self.current[idx] = origin, time

    def exit(self, idx: str, dest: str, time: int) -> None:
        """
        Exit someone into the system
        :param idx: person ID
        :param dest: place getting off
        :param time: timestamp for getting off
        """
        if idx not in self.current:
            return
        start_station, start_time = self.current[idx]
        if start_station not in self.table:
            self.table[start_station] = HashTable()
        if dest not in self.table[start_station]:
            self.table[start_station][dest] = (0, 0)
        current_total, trips = self.table[start_station][dest]
        current_total += time - start_time
        trips += 1
        self.table[start_station][dest] = (current_total, trips)
        del self.current[idx]

    def get_average(self, origin: str, dest: str) -> float:
        """
        Get the average time between two locations
        :param origin: location of origin
        :param dest: location of destination
        :return: float for the average time to get between two places
        """
        if origin not in self.table or dest not in self.table[origin]:
            return 0.0
        total_time, trips = self.table[origin][dest]
        return total_time / trips
